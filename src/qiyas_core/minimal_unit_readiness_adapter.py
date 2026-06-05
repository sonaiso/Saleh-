"""MinimalIndependentUnitReadinessLayerAdapter — Phase-2 follow-up.

Implements the readiness layer's admission predicate per
``MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md``.

The adapter consumes three witnesses (contract §2) plus an optional
fourth (added by PR #82 per ``ARABIC_VARIANT_RESOLUTION_CONTRACT.md``
§10.3):

  1. ``SlotGeometryCandidate(length = 1, construction_mode = "seed")``
  2. ``ArabicArticulationRegistry`` metadata (via the existing read-only
     reader at ``qiyas_core.arabic_articulation_registry``)
  3. ``MinimalCompleteClosureEvidence`` (via the existing
     ``slot_geometry_closure_check`` evidence carrier — produced once,
     consumed read-only here)
  4. **(optional)** ``ArabicVariantResolutionEvidence`` (via the
     ``arabic_variant_resolver`` producer — produced once, consumed
     read-only here). Removes the ``variant_ambiguity`` deferral
     reason for multi-variant symbols (``و`` / ``ي``) **only**;
     does NOT by itself authorise admission (§7 / §10.3 of
     ARABIC_VARIANT_RESOLUTION_CONTRACT.md).

It produces exactly one output type:

  ``MinimalUnitReadinessCandidate`` with ``output_flags ⊇ {CandidateOnly}``

The output is **always** a ``MinimalUnitReadinessCandidate``: ACCEPTED
when all witnesses pass, BLOCKED when a structural witness fails
(geometry shape, closure-evidence presence, registry rejection,
resolved-variant ineligibility), DEFERRED when the registry returns
variant ambiguity for the symbol and either (a) no variant resolution
evidence is supplied, or (b) the supplied evidence is invalid /
foreign / mismatched (treated as absent per §7 — DEFER, never BLOCK).

Per the contract:

  * Failure NEVER produces a ``Candidate`` of any other type
    (CONSTITUTIONAL_BASE + the §8 list, including
    ``MinimalIndependentMeaningCandidate``).
  * Readiness NEVER re-proves the closure conditions; it consumes the
    closure-evidence carrier read-only (contract §10.3).
  * Readiness does NOT consult the registry to substitute for any
    qiyas-layer transition; the registry is metadata only and
    licenses no algebraic transition by itself (contract §10).
  * Variant resolution evidence is consumed read-only and removes
    only the ``variant_ambiguity`` defer reason; all other MIU
    invariants (length=1, construction_mode=seed, closure presence,
    registry eligibility, output flags) still apply unchanged
    (§7 / §10.3 of ARABIC_VARIANT_RESOLUTION_CONTRACT.md).
  * No segment linking; no admission of multi-slot geometries.

Phase 2 Batch-1 / Batch-2 / Closure-check artifacts are NOT modified by
this module. The adapter consumes their licensed outputs read-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import uuid

from .arabic_articulation_registry import (
    ArabicArticulationEntry,
    get_articulation_by_id,
    get_articulations_by_symbol,
    get_primary_articulation,
)
from .arabic_variant_resolution_evidence import (
    ArabicVariantResolutionEvidence,
    RESERVED_VARIANT_LABELS,
)
from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.minimal_unit_readiness_rules import (
    MINIMAL_UNIT_READINESS_ADMIT_RULE,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Trace-id prefixes / markers per contract §5 / §6.
_LENGTH_TRACE_PREFIX = "trace:slot_geometry:length:"
_MODE_TRACE_PREFIX = "trace:slot_geometry:construction_mode:"
_READY_TRACE_PREFIX = "trace:miu_readiness:is_minimal_unit_ready:"
_SYMBOL_TRACE_PREFIX = "trace:miu_readiness:symbol:"

# Arabic letter range — used to distinguish a letter codepoint from a
# haraka codepoint inside the geometry's identity_ids.
_ARABIC_LETTER_RANGE = (0x0621, 0x064A)

# Required output flag (CLAUDE.md §4 invariant 9).
_REQUIRED_OUTPUT_FLAG = "CandidateOnly"
_FORBIDDEN_FINAL_FLAGS = frozenset({
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
    "FinalCaseJudgment",
    "DalalahCandidate",
})


# ---------------------------------------------------------------------------
# Helpers (all observation; no mutation, no kernel invocation)
# ---------------------------------------------------------------------------


def _read_length(geom: Any) -> int | None:
    for tid in getattr(geom, "trace_ids", ()):
        if isinstance(tid, str) and tid.startswith(_LENGTH_TRACE_PREFIX):
            try:
                return int(tid[len(_LENGTH_TRACE_PREFIX):])
            except ValueError:
                return None
    return None


def _read_construction_mode(geom: Any) -> str | None:
    for tid in getattr(geom, "trace_ids", ()):
        if isinstance(tid, str) and tid.startswith(_MODE_TRACE_PREFIX):
            return tid[len(_MODE_TRACE_PREFIX):]
    return None


def _extract_letter_symbol(geom: Any) -> str | None:
    """Find the Arabic-letter codepoint identity carried by the
    geometry and return its character.

    A ``SlotGeometryCandidate(length = 1)`` produced by the slot-
    composition pipeline carries the letter's
    ``identity:codepoint:<hex>`` entry alongside the haraka's. Only the
    letter codepoint (range 0x0621 .. 0x064A) is treated as the
    symbol; harakat (0x064B .. 0x0652+) are filtered out.
    """
    lo, hi = _ARABIC_LETTER_RANGE
    for iid in getattr(geom, "identity_ids", ()):
        if not (isinstance(iid, str) and iid.startswith("identity:codepoint:")):
            continue
        try:
            cp = int(iid[len("identity:codepoint:"):], 16)
        except ValueError:
            continue
        if lo <= cp <= hi:
            return chr(cp)
    return None


def _is_slot_geometry_candidate_shaped(geom: Any) -> bool:
    candidate_type = getattr(geom, "candidate_type", None)
    layer = getattr(geom, "layer", None)
    return (
        candidate_type == "SlotGeometryCandidate"
        and layer == "SlotGeometryQiyas"
    )


def _has_no_forbidden_final_flags(geom: Any) -> bool:
    flags = getattr(geom, "output_flags", frozenset())
    return not (flags & _FORBIDDEN_FINAL_FLAGS)


def _try_apply_variant_resolution(
    evidence: ArabicVariantResolutionEvidence | None,
    symbol: str,
    geometry_candidate_id: str,
) -> ArabicArticulationEntry | None:
    """Try to resolve variant ambiguity using the supplied evidence.

    Per ``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §7 / §10.3:

      * Absent evidence ⇒ ``None`` (caller keeps deferring).
      * Mismatched symbol ⇒ ``None`` (foreign; DEFER, not BLOCK).
      * Mismatched geometry id ⇒ ``None`` (foreign; DEFER, not BLOCK).
      * Unreserved variant label ⇒ ``None`` (malformed; DEFER).
      * Entry id not found in registry ⇒ ``None`` (malformed; DEFER).
      * Resolved entry's variant disagrees with the evidence's
        ``selected_variant`` ⇒ ``None`` (inconsistent; DEFER).

    A successful match returns the registry entry whose semantics
    the evidence selected. The caller plugs that entry into the
    same wasf/fariq emission path used by the single-primary case,
    so the rule's existing claim grammar handles ACCEPT/BLOCK
    decisions without amendment.
    """
    if evidence is None:
        return None
    if evidence.symbol != symbol:
        return None
    if evidence.geometry_candidate_id != geometry_candidate_id:
        return None
    if evidence.selected_variant not in RESERVED_VARIANT_LABELS:
        return None
    entry = get_articulation_by_id(evidence.selected_entry_id)
    if entry is None:
        return None
    if entry.symbol != symbol:
        return None
    if entry.variant != evidence.selected_variant:
        return None
    return entry


def _effective_primary(
    symbol: str | None,
    variant_resolution_evidence: ArabicVariantResolutionEvidence | None,
    geometry_candidate_id: str,
) -> ArabicArticulationEntry | None:
    """Return the registry entry the readiness layer should treat as
    the slot's primary articulation, threading optional variant
    resolution evidence through.

    Falls back to ``get_primary_articulation(symbol)`` when the
    registry already resolves uniquely. When the registry returns
    ``None`` (multi-variant symbol), tries the optional evidence.
    Returns ``None`` if the evidence is absent or invalid — the
    caller then emits the ``variant_ambiguity`` defer claim per
    contract §7.
    """
    if symbol is None:
        return None
    primary = get_primary_articulation(symbol)
    if primary is not None:
        return primary
    return _try_apply_variant_resolution(
        variant_resolution_evidence, symbol, geometry_candidate_id,
    )


# ---------------------------------------------------------------------------
# The adapter
# ---------------------------------------------------------------------------


@dataclass
class MinimalIndependentUnitReadinessLayerAdapter:
    """Adapter that admits a single-slot geometry as a minimal-unit
    readiness candidate, or blocks/defers per the contract.

    Per ``MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`` §3, the
    admission predicate ``Admit(S, M, E)`` is True iff all three
    witnesses pass. The adapter is the only place where the witnesses
    are translated into the canonical Arabic-rooted claim grammar the
    kernel reads.
    """

    kernel: QiyasKernel

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------

    def admit(
        self,
        geometry: Any,
        closure_evidence: Any,
        trace_prefix: str = "",
        variant_resolution_evidence: ArabicVariantResolutionEvidence | None = None,
    ) -> CandidateSet:
        """Attempt admission of ``geometry`` as a
        ``MinimalUnitReadinessCandidate``.

        Returns a ``CandidateSet`` whose ``accepted`` member contains
        the ACCEPTED ``MinimalUnitReadinessCandidate`` on success, or
        whose ``blocked`` / ``deferred`` members carry the residuals
        on failure / ambiguity.

        Failure (BLOCKED) cases:
          * ``geometry.candidate_type != "SlotGeometryCandidate"`` (or
            wrong layer);
          * ``length != 1``;
          * ``construction_mode != "seed"``;
          * ``closure_evidence is None``;
          * registry has no entry for the geometry's symbol;
          * the registry-resolved primary OR the variant-evidence-
            resolved entry has ``can_function_as_minimal_independent_unit
            == False``.

        Deferral (DEFERRED) cases:
          * registry returns multiple variants for the symbol AND
            either (a) no ``variant_resolution_evidence`` was
            supplied, or (b) the supplied evidence is invalid /
            foreign / mismatched (treated as absent per
            ARABIC_VARIANT_RESOLUTION_CONTRACT.md §7 — DEFER, never
            BLOCK).

        ``variant_resolution_evidence`` is optional. When supplied,
        it removes the ``variant_ambiguity`` defer reason **only**;
        all other MIU invariants still apply. Presence of variant
        resolution does not by itself authorise admission
        (contract §7 / §10.3).
        """
        if not trace_prefix:
            trace_prefix = f"miu_readiness:admit:{uuid.uuid4().hex[:8]}"

        asl = self._build_asl(trace_prefix)
        far = self._build_far(geometry, trace_prefix)
        evidence = self._build_evidence(
            geometry,
            closure_evidence,
            trace_prefix,
            variant_resolution_evidence,
        )

        request = QiyasRequest(
            rule=MINIMAL_UNIT_READINESS_ADMIT_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="MinimalIndependentUnitReadinessQiyas"),
        )
        return self.kernel.apply(request)

    # -----------------------------------------------------------------
    # Request builders
    # -----------------------------------------------------------------

    def _build_asl(self, trace_prefix: str) -> QiyasNodeRef:
        return QiyasNodeRef(
            node_id="اصل:minimal_unit_readiness_domain",
            node_type="MinimalIndependentUnitReadinessDomain",
            identity_ids=("identity:minimal_unit_readiness_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

    def _build_far(self, geometry: Any, trace_prefix: str) -> QiyasNodeRef:
        # The far carries the geometry's identity_ids verbatim so the
        # kernel's identity-preservation invariant holds across the
        # admission step. The node_type is the geometry's
        # candidate_type so the kernel's _check_node_types matches
        # rule.far_type ("SlotGeometryCandidate") in the canonical
        # case; for non-geometry inputs this will mismatch and the
        # kernel will record a `far_type_mismatch` residual in
        # addition to the explicit فارق claims emitted below.
        candidate_type = getattr(geometry, "candidate_type", "Unknown")
        identity_ids = tuple(getattr(geometry, "identity_ids", ()))
        candidate_id = getattr(geometry, "candidate_id", "unknown")
        rank = getattr(geometry, "rank", EvidenceRank.NO_EVIDENCE)
        return QiyasNodeRef(
            node_id=f"فرع:{candidate_type}:{candidate_id}",
            node_type=candidate_type,
            identity_ids=identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=rank,
        )

    def _build_evidence(
        self,
        geometry: Any,
        closure_evidence: Any,
        trace_prefix: str,
        variant_resolution_evidence: ArabicVariantResolutionEvidence | None = None,
    ) -> EvidenceSet:
        proves: list[str] = [
            "اصل:established",
            "فرع:determined",
        ]

        # §4.1 — geometry shape checks.
        if _is_slot_geometry_candidate_shaped(geometry):
            proves.append("وصف:input_is_slot_geometry_candidate:evidenced")
        else:
            proves.append("فارق:input_not_slot_geometry_candidate:present")

        length = _read_length(geometry)
        if length == 1:
            proves.append("وصف:geometry_length_is_one:evidenced")
        else:
            proves.append("فارق:length_not_one:present")

        mode = _read_construction_mode(geometry)
        if mode == "seed":
            proves.append("وصف:geometry_construction_mode_is_seed:evidenced")
        else:
            proves.append("فارق:construction_mode_not_seed:present")

        # §4.3 — closure-evidence presence (read-only consumption).
        # Light duck-type check: the carrier exposes the eight
        # condition booleans plus geometry_candidate_id; we treat
        # presence + non-None as the gate. The closure conditions are
        # NOT re-proved here (contract §10.3).
        closure_present = closure_evidence is not None
        if closure_present:
            proves.append("وصف:closure_evidence_present:evidenced")
        else:
            proves.append("فارق:closure_evidence_missing:present")

        # §4.2 — registry metadata witness, threaded through optional
        # variant resolution evidence per ARABIC_VARIANT_RESOLUTION
        # CONTRACT.md §10.3.
        symbol = _extract_letter_symbol(geometry)
        symbol_for_trace: str = symbol if symbol is not None else "?"
        geometry_candidate_id = getattr(geometry, "candidate_id", "")
        primary = _effective_primary(
            symbol, variant_resolution_evidence, geometry_candidate_id,
        )
        if symbol is None:
            proves.append("فارق:registry_metadata_missing_for_symbol:present")
        else:
            matches = get_articulations_by_symbol(symbol)
            if not matches:
                proves.append("فارق:registry_metadata_missing_for_symbol:present")
            else:
                proves.append("وصف:registry_metadata_present:evidenced")
                if primary is None:
                    # Variant ambiguity — DEFER per §4.2 / §7 / §13.3.
                    # Either the registry has multiple variants and
                    # no variant resolution evidence was supplied,
                    # or the supplied evidence was invalid /
                    # mismatched (per §7 of
                    # ARABIC_VARIANT_RESOLUTION_CONTRACT.md, invalid
                    # is treated as absent — DEFER, not BLOCK).
                    proves.append("defer:variant_ambiguity:present")
                else:
                    proves.append(
                        "وصف:single_primary_articulation_resolved:evidenced"
                    )
                    if primary.can_function_as_minimal_independent_unit:
                        proves.append(
                            "وصف:symbol_eligible_for_minimal_unit:evidenced"
                        )
                    else:
                        proves.append(
                            "فارق:symbol_not_eligible_for_minimal_unit:present"
                        )

        # §5 — output discipline. These wasfs are asserted
        # unconditionally; the kernel will block the candidate via a
        # blocking-fariq or defer it via the defer claim above when
        # any of the upstream witnesses failed. The output flags
        # invariant is enforced by the kernel itself at
        # _make_candidate_set time, but we restate it here so the
        # rule's required_effective_wasf list passes for the canonical
        # admit path.
        if _has_no_forbidden_final_flags(geometry):
            proves.append("وصف:output_remains_candidate_only:evidenced")
        else:
            proves.append("فارق:forbidden_final_flag_present:present")
        proves.append("وصف:is_minimal_unit_ready_marker_emitted:evidenced")

        # عللة / wadi — invariant licensing of the admission step.
        proves.extend([
            "علة:belongs_to_minimal_unit_readiness_domain:verified",
            "علة:minimal_unit_readiness_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ])

        # Metadata-on-trace per contract §5. The `is_minimal_unit_ready`
        # marker travels on trace_ids — never on identity_ids — so the
        # kernel's _make_candidate_set carries it through to the output.
        ready = (
            symbol is not None
            and closure_present
            and length == 1
            and mode == "seed"
            and _is_slot_geometry_candidate_shaped(geometry)
            and bool(get_articulations_by_symbol(symbol))
            and primary is not None
            and primary.can_function_as_minimal_independent_unit
        )
        ready_marker = f"{_READY_TRACE_PREFIX}{'true' if ready else 'false'}"
        symbol_marker = f"{_SYMBOL_TRACE_PREFIX}{symbol_for_trace}"
        closure_audit = (
            f"trace:miu_readiness:closure_evidence_id:"
            f"{getattr(closure_evidence, 'evidence_id', 'absent')}"
            if closure_present
            else "trace:miu_readiness:closure_evidence_id:absent"
        )
        # Variant-resolution audit trace: records whether evidence was
        # supplied and whether it was applied (used to resolve the
        # primary). Per CLAUDE.md §4 invariant 3 this audit string is
        # on trace_ids — never on identity_ids — and adds trace without
        # consuming identity.
        if variant_resolution_evidence is None:
            variant_audit = "trace:miu_readiness:variant_resolution:absent"
        else:
            variant_applied = (
                primary is not None
                and get_primary_articulation(symbol_for_trace) is None
                and variant_resolution_evidence.symbol == symbol_for_trace
            )
            variant_audit = (
                f"trace:miu_readiness:variant_resolution:"
                f"{'applied' if variant_applied else 'rejected'}:"
                f"{variant_resolution_evidence.evidence_id}"
            )

        return EvidenceSet(
            items=(
                Evidence(
                    evidence_id=(
                        f"ev:miu_readiness:{uuid.uuid4().hex[:8]}"
                    ),
                    source_layer="MinimalIndependentUnitReadinessQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(
                        f"{trace_prefix}:ev",
                        ready_marker,
                        symbol_marker,
                        closure_audit,
                        variant_audit,
                    ),
                ),
            )
        )
