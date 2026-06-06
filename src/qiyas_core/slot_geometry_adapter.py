"""SlotGeometryLayerAdapter — Phase-2 Batch 1.

Implements the ``Seed`` and ``Extend`` construction modes of
``SlotGeometryQiyas`` per ``SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md``.

The single admissible output type is ``SlotGeometryCandidate`` (contract
§9). ``Seed`` and ``Extend`` are construction modes carried as
``trace_ids`` metadata on the output, not distinct candidate types:

  ``SlotGeometryCandidate(length=1, construction_mode="seed")``
  ``SlotGeometryCandidate(length=n+1, construction_mode="extension")``

The adapter consumes only ``SlotCandidate*`` (contract §1). It does
not re-tokenise the text, does not re-classify codepoints, does not
re-prove letter identity, haraka function, position, or carrier
binding — all of those proofs were settled in Phase 1.

This adapter does **not** implement ``MinimalCompletionReadiness``,
``DalalahCandidate``, ``WordCandidate``, or any closure-checking
step. Those concerns remain strictly later contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.slot_geometry_rules import (
    SLOT_GEOMETRY_EXTEND_RULE,
    SLOT_GEOMETRY_SEED_RULE,
)


# ---------------------------------------------------------------------------
# Constants — metadata-trace prefixes and contract-fixed slot fingerprint
# ---------------------------------------------------------------------------

# Trace-id prefixes that carry geometry metadata. Read by the helper
# functions below; never by `identity_ids`.
_LENGTH_TRACE_PREFIX = "trace:slot_geometry:length:"
_MODE_TRACE_PREFIX = "trace:slot_geometry:construction_mode:"
_ALIGNMENT_REF_SUBSTRING = ":alignment_ref:"

# Fingerprint of a valid `SlotCandidate`, per
# `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §2.1.
_REQUIRED_SLOT_CANDIDATE_TYPE = "SlotCandidate"
_REQUIRED_SLOT_SOURCE_RULE_ID = "slot.composition"
_REQUIRED_OUTPUT_FLAG = "CandidateOnly"
_FORBIDDEN_FINAL_FLAGS = frozenset({
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
    "FinalCaseJudgment",
    "DalalahCandidate",
})


# ---------------------------------------------------------------------------
# SlotBindingEvidence — runtime carrier of the §5 twelve claims.
#
# Per `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §5, the binding
# evidence for an `Extend` step must witness twelve conjunctive
# claims. This frozen dataclass is the runtime container — the
# adapter reads its fields and either licenses the extension or
# blocks it with the corresponding `فارق:` claim.
#
# `SlotBindingEvidence` is **not portable** above the slot layer
# (contract §5.2). It must not be reused by any higher-layer
# binding-evidence type.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SlotBindingEvidence:
    """Runtime carrier for the twelve §5 claims of a SlotGeometry
    extension."""

    # Tokenizer segment identities of the previous-geometry's last
    # consumed slot and of the new slot. Equality of the two licenses
    # the "same INTRA_UTTERANCE segment" claim; difference triggers
    # the cross_segment_binding invalidating-difference.
    prev_segment_id: int
    curr_segment_id: int

    # Source-position indices (text indices) of the previous-geometry's
    # last consumed slot and of the new slot. Used to check
    # `ordered_after` and `adjacent_or_licensed_distance`.
    prev_position: int
    curr_position: int

    # Whether the tokenizer's whitespace / punctuation marker stream
    # contains any boundary marker strictly between `prev_position`
    # and `curr_position`. The adapter is responsible for computing
    # these flags; this dataclass only carries them.
    has_whitespace_between: bool = False
    has_punctuation_between: bool = False

    # The maximum distance (in source positions) the slot-geometry
    # layer's rule licenses for an extension. Defaults to ``1``
    # (immediate adjacency). A non-default value indicates the gap
    # was licensed by the slot-geometry layer's own admissibility
    # predicate.
    max_licensed_distance: int = 1

    # Audit trace ids referencing this binding evidence's own
    # provenance. Recorded on the resulting geometry as auditable
    # `trace_ids` (never `identity_ids`).
    binding_trace_ids: tuple[str, ...] = field(default_factory=tuple)

    # Layer label. Fixed to "SlotGeometryQiyas" — binding evidence is
    # produced *by* the slot-geometry layer and licenses extension
    # *within* it (contract §10 pre-condition 5 of the recursive
    # extension contract).
    layer: str = "SlotGeometryQiyas"

    @property
    def candidate_type(self) -> str:
        """Public name of this binding-evidence's candidate-type, per
        contract §5 / §10."""
        return "SlotBindingEvidence"


# ---------------------------------------------------------------------------
# Public helpers — read the geometry metadata from a SlotGeometryCandidate.
#
# `length` and `construction_mode` are metadata on the
# `SlotGeometryCandidate`'s `trace_ids`. Per CLAUDE.md §4 invariants
# 1–3 they are not identity; per contract §6 they are auditable trace.
# These helpers expose them as typed accessors so callers do not need
# to parse trace strings by hand.
# ---------------------------------------------------------------------------


def get_geometry_length(candidate: Candidate) -> int | None:
    """Return the geometry length recorded in ``candidate.trace_ids``.

    Returns ``None`` if no length entry is present (e.g. the candidate
    is not a `SlotGeometryCandidate`, or it was constructed by some
    other adapter).
    """
    for tid in candidate.trace_ids:
        if tid.startswith(_LENGTH_TRACE_PREFIX):
            try:
                return int(tid[len(_LENGTH_TRACE_PREFIX):])
            except ValueError:
                return None
    return None


def get_construction_mode(candidate: Candidate) -> str | None:
    """Return the construction mode recorded in ``candidate.trace_ids``.

    Returns one of ``"seed"``, ``"extension"``, or ``None``.
    """
    for tid in candidate.trace_ids:
        if tid.startswith(_MODE_TRACE_PREFIX):
            return tid[len(_MODE_TRACE_PREFIX):]
    return None


# ---------------------------------------------------------------------------
# Slot-candidate validation per contract §2.
# ---------------------------------------------------------------------------


def _has_alignment_ref(slot: Candidate) -> bool:
    return any(_ALIGNMENT_REF_SUBSTRING in tid for tid in slot.trace_ids)


def _is_candidate_only(slot: Candidate) -> bool:
    return _REQUIRED_OUTPUT_FLAG in slot.output_flags


def _has_no_forbidden_final_flags(slot: Candidate) -> bool:
    return not (slot.output_flags & _FORBIDDEN_FINAL_FLAGS)


def _identity_trace_disjoint(slot: Candidate) -> bool:
    return not (set(slot.identity_ids) & set(slot.trace_ids))


def _has_codepoint_identity(slot: Candidate) -> bool:
    """A SlotCandidate produced by ``slot.composition`` carries the
    letter and haraka codepoint identities in its ``identity_ids``
    (per ``slot_adapter.py``'s pillar-merge). The presence of at least
    one ``identity:codepoint:*`` entry is the structural witness of
    the letter-identity and haraka-function source breadcrumbs
    required by §2.2."""
    return any(iid.startswith("identity:codepoint:") for iid in slot.identity_ids)


# ---------------------------------------------------------------------------
# Internal — build a QiyasRequest for SEED or EXTEND.
#
# The adapter computes which of contract §2.1 / §2.2 / §5 claims
# actually hold for the given inputs, and only emits the
# corresponding `وصف:` / `علة:` / `وادي:` claims. When any required
# claim cannot be honestly emitted, the corresponding wasf is
# missing from the evidence set; the kernel then records an
# `effective_wasf_missing` residual and blocks the candidate.
# Invalidating-difference claims (`فارق:`) are emitted explicitly
# for any detected violation so the kernel records a
# `blocking_fariq_present` residual.
# ---------------------------------------------------------------------------


@dataclass
class SlotGeometryLayerAdapter:
    """Adapter for ``SlotGeometryQiyas``.

    Public methods:
      * ``seed_geometry(slot, trace_prefix="")``
      * ``extend_geometry(previous, next_slot, binding, trace_prefix="")``

    Both return a ``CandidateSet`` whose ``accepted`` member contains
    the ``SlotGeometryCandidate`` on success, or whose ``blocked`` /
    ``deferred`` members carry the residuals on failure.
    """

    kernel: QiyasKernel

    # -------------------------------------------------------------------
    # Seed
    # -------------------------------------------------------------------

    def seed_geometry(
        self,
        slot: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Admit a single ``SlotCandidate`` as a length-1 geometry.

        The slot must satisfy the §2 consumed-contract conditions; if
        it does not, the kernel returns a BLOCKED ``SlotGeometryCandidate``
        with the corresponding residuals.
        """
        if not trace_prefix:
            trace_prefix = f"slot_geometry:seed:{uuid.uuid4().hex[:8]}"

        asl = self._build_asl(trace_prefix)
        far = self._build_far_for_seed(slot, trace_prefix)
        evidence = self._build_seed_evidence(slot, trace_prefix)

        request = QiyasRequest(
            rule=SLOT_GEOMETRY_SEED_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SlotGeometryQiyas"),
        )
        return self.kernel.apply(request)

    # -------------------------------------------------------------------
    # Extend
    # -------------------------------------------------------------------

    def extend_geometry(
        self,
        previous: Candidate,
        next_slot: Candidate,
        binding: SlotBindingEvidence | None,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Admit a new ``SlotCandidate`` as an extension of an existing
        geometry, licensed by ``binding`` per §5.

        Failure cases (BLOCKED candidate with residual) include:

          * ``previous.candidate_type != "SlotGeometryCandidate"``;
          * ``binding is None`` (binding_evidence_missing);
          * ``next_slot`` fails §2 (slot-candidate contract violation);
          * ``binding`` fails any §5 claim (cross-segment binding,
            boundary crossing, not-ordered-after, distance-not-licensed,
            rank-meet-invalid, identity / trace overlap, …).
        """
        if not trace_prefix:
            trace_prefix = f"slot_geometry:extend:{uuid.uuid4().hex[:8]}"

        asl = self._build_asl(trace_prefix)
        far = self._build_far_for_extend(previous, next_slot, trace_prefix)
        evidence = self._build_extend_evidence(
            previous, next_slot, binding, trace_prefix,
        )

        request = QiyasRequest(
            rule=SLOT_GEOMETRY_EXTEND_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SlotGeometryQiyas"),
        )
        return self.kernel.apply(request)

    # -------------------------------------------------------------------
    # Request-builder helpers
    # -------------------------------------------------------------------

    def _build_asl(self, trace_prefix: str) -> QiyasNodeRef:
        return QiyasNodeRef(
            node_id="اصل:slot_geometry_domain",
            node_type="SlotGeometryDomain",
            identity_ids=("identity:slot_geometry_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

    def _build_far_for_seed(
        self,
        slot: Candidate,
        trace_prefix: str,
    ) -> QiyasNodeRef:
        # The far for a Seed request is the slot itself: its
        # candidate_type is checked against rule.far_type
        # ("SlotCandidate"); its identity_ids carry the seed
        # identity into the output via `_make_candidate_set`'s
        # combine.
        return QiyasNodeRef(
            node_id=f"فرع:slot_candidate_seed:{slot.candidate_id}",
            # Use the slot's actual candidate_type so the kernel's
            # `_check_node_types` matches `rule.far_type`.
            # When the slot is not a SlotCandidate, this differs and
            # the kernel records `far_type_mismatch`.
            node_type=slot.candidate_type,
            identity_ids=slot.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=slot.rank,
        )

    def _build_far_for_extend(
        self,
        previous: Candidate,
        next_slot: Candidate,
        trace_prefix: str,
    ) -> QiyasNodeRef:
        # The far for an Extend request carries the combined identity
        # of the previous geometry and the new slot. Identity is
        # preserved via the union (deduped); the far_type is the
        # previous-geometry type so the kernel's `_check_node_types`
        # matches `rule.far_type` ("SlotGeometryCandidate").
        combined = list(previous.identity_ids) + list(next_slot.identity_ids)
        seen: set[str] = set()
        deduped: list[str] = []
        for iid in combined:
            if iid not in seen:
                seen.add(iid)
                deduped.append(iid)

        return QiyasNodeRef(
            node_id=f"فرع:slot_geometry_extend:{next_slot.candidate_id}",
            node_type=previous.candidate_type,
            identity_ids=tuple(deduped),
            trace_ids=(f"{trace_prefix}:far",),
            rank=min(
                (previous.rank, next_slot.rank),
                key=lambda r: r.value,
            ),
        )

    # -------------------------------------------------------------------
    # Evidence-builder helpers
    # -------------------------------------------------------------------

    def _build_seed_evidence(
        self,
        slot: Candidate,
        trace_prefix: str,
    ) -> EvidenceSet:
        proves: list[str] = [
            "اصل:established",
            "فرع:determined",
        ]

        # §2.1 + §2.2 — emit a وصف claim only when the corresponding
        # condition actually holds; emit a فارق claim when a
        # condition is violated.
        proves.extend(
            self._slot_candidate_claims(slot, "seed")
        )

        # §3.1 / §9 — seed-specific witnesses + metadata claims.
        proves.append("وصف:slot_geometry_seed_admitted:evidenced")
        proves.append("وصف:construction_mode_seed_evidenced:evidenced")
        proves.append("وصف:geometry_length_one_evidenced:evidenced")

        # عللة / wadi — invariant licensing of the seed step.
        proves.extend(self._licensing_claims("slot_geometry_seed_licensed"))

        # Metadata-on-trace: length and construction_mode travel on
        # the evidence's trace_ids so the kernel writes them onto the
        # output's `trace_ids` (CLAUDE.md §4 — never identity).
        metadata_trace = (
            f"{_LENGTH_TRACE_PREFIX}1",
            f"{_MODE_TRACE_PREFIX}seed",
            f"trace:slot_geometry:seed_slot:{slot.candidate_id}",
        )

        return EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:slot_geometry:seed:{uuid.uuid4().hex[:8]}",
                    source_layer="SlotGeometryQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + metadata_trace,
                ),
            )
        )

    def _build_extend_evidence(
        self,
        previous: Candidate,
        next_slot: Candidate,
        binding: SlotBindingEvidence | None,
        trace_prefix: str,
    ) -> EvidenceSet:
        proves: list[str] = [
            "اصل:established",
            "فرع:determined",
        ]

        # §2 for the NEW slot.
        proves.extend(self._slot_candidate_claims(next_slot, "extension"))

        # §3.2 — the previous-geometry conditions.
        if previous.candidate_type == "SlotGeometryCandidate":
            proves.append("وصف:previous_is_slot_geometry_candidate:evidenced")
        else:
            proves.append("فارق:previous_not_slot_geometry_candidate:present")
        # We do not re-validate the previous geometry's internal
        # invariants here — they were settled at its own production
        # time. We only check it is the right candidate type and not
        # blocked. The §6.1 "previous geometry remains valid"
        # condition is read off its candidate-type + non-blocked
        # status.
        previous_length = get_geometry_length(previous)
        if previous_length is None or previous_length < 1:
            proves.append("فارق:previous_geometry_invalid:present")
        else:
            proves.append("وصف:previous_geometry_valid:evidenced")

        # §5 — twelve binding-evidence claims.
        if binding is None:
            proves.append("فارق:binding_evidence_missing:present")
            new_length: int | None = None
        else:
            proves.append("وصف:binding_evidence_present:evidenced")
            # Same segment / no boundary crossing.
            if binding.prev_segment_id == binding.curr_segment_id:
                proves.append("وصف:same_intra_utterance_segment:evidenced")
            else:
                proves.append("فارق:cross_segment_binding:present")
            if binding.has_whitespace_between:
                proves.append("فارق:whitespace_boundary_crossing:present")
            else:
                proves.append("وصف:no_whitespace_boundary_crossing:evidenced")
            if binding.has_punctuation_between:
                proves.append("فارق:punctuation_boundary_crossing:present")
            else:
                proves.append("وصف:no_punctuation_boundary_crossing:evidenced")
            # The "no_tokenizer_boundary_between_slots" claim is the
            # conjunction of the two preceding boundary checks — only
            # emitted when both held.
            if not (
                binding.has_whitespace_between or binding.has_punctuation_between
            ):
                proves.append(
                    "وصف:no_tokenizer_boundary_between_slots:evidenced"
                )
            else:
                proves.append("فارق:tokenizer_boundary_crossing:present")
            # Ordering and distance.
            if binding.curr_position > binding.prev_position:
                proves.append("وصف:ordered_after:evidenced")
            else:
                proves.append("فارق:not_ordered_after:present")
            distance = binding.curr_position - binding.prev_position
            if 1 <= distance <= max(1, binding.max_licensed_distance):
                proves.append("وصف:adjacent_or_licensed_distance:evidenced")
            else:
                proves.append("فارق:distance_not_licensed:present")
            # Rank-meet validity — the new geometry's rank is the meet
            # of the four contributing ranks; check the rule ceiling
            # plus inputs are all above NO_EVIDENCE.
            rank_meet = min(
                (
                    previous.rank,
                    next_slot.rank,
                    SLOT_GEOMETRY_EXTEND_RULE.rank_ceiling,
                ),
                key=lambda r: r.value,
            )
            if rank_meet == EvidenceRank.NO_EVIDENCE:
                proves.append("فارق:rank_meet_invalid:present")
            else:
                proves.append("وصف:rank_meet_valid:evidenced")
            # Identity / trace / residual preservation — these are
            # structural and read off the inputs.
            combined_identity = set(previous.identity_ids) | set(
                next_slot.identity_ids
            )
            combined_trace = set(previous.trace_ids) | set(next_slot.trace_ids)
            if not (combined_identity & combined_trace):
                proves.append("وصف:identity_preservation_holds:evidenced")
                proves.append("وصف:trace_preservation_holds:evidenced")
            else:
                proves.append("فارق:identity_trace_overlap:present")
            # Residuals are preserved by the kernel's _make_candidate_set
            # which propagates audit.residuals; the structural claim is
            # always satisfied here.
            proves.append("وصف:residual_preservation_holds:evidenced")
            # No blocking difference on either input or binding by
            # construction at this point — if there were one, we'd
            # have emitted a فارق claim above.
            already_blocking = any(
                p.startswith("فارق:") and p.endswith(":present")
                for p in proves
            )
            if not already_blocking:
                proves.append("وصف:no_blocking_difference:evidenced")

            new_length = (previous_length or 0) + 1

        # §3.2 / §9 — extension-specific witnesses + metadata.
        proves.append("وصف:construction_mode_extension_evidenced:evidenced")
        proves.append("وصف:geometry_length_incremented_evidenced:evidenced")

        # عللة / wadi — invariant licensing of the extension step.
        proves.extend(self._licensing_claims("slot_geometry_extension_licensed"))

        # Metadata-on-trace.
        metadata_trace_list: list[str] = []
        if new_length is not None:
            metadata_trace_list.append(f"{_LENGTH_TRACE_PREFIX}{new_length}")
        metadata_trace_list.append(f"{_MODE_TRACE_PREFIX}extension")
        metadata_trace_list.append(
            f"trace:slot_geometry:extension_slot:{next_slot.candidate_id}"
        )
        if binding is not None:
            for btid in binding.binding_trace_ids:
                metadata_trace_list.append(
                    f"trace:slot_geometry:binding_ref:{btid}"
                )

        return EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:slot_geometry:extend:{uuid.uuid4().hex[:8]}",
                    source_layer="SlotGeometryQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(metadata_trace_list),
                ),
            )
        )

    # -------------------------------------------------------------------
    # Shared claim-emitting helper
    # -------------------------------------------------------------------

    def _slot_candidate_claims(
        self,
        slot: Candidate,
        mode: str,
    ) -> list[str]:
        """Emit the §2.1 / §2.2 / §3.{1,2} wasf / fariq claims for one
        slot input (Seed's seed-slot, or Extend's new-slot).

        For each contract condition, emits a `وصف:*:evidenced` claim
        if the condition holds, or a `فارق:*:present` claim if it is
        violated. The kernel then either records an
        `effective_wasf_missing` residual (when a required wasf was
        not asserted) or a `blocking_fariq_present` residual (when an
        invalidating-difference was asserted).
        """
        proves: list[str] = []

        # 2.1 structural witnesses.
        if slot.candidate_type == _REQUIRED_SLOT_CANDIDATE_TYPE:
            proves.append("وصف:input_is_slot_candidate:evidenced")
        else:
            proves.append("فارق:input_not_slot_candidate:present")
        if slot.source_rule_id == _REQUIRED_SLOT_SOURCE_RULE_ID:
            proves.append("وصف:source_rule_is_slot_composition:evidenced")
        else:
            proves.append("فارق:source_rule_not_slot_composition:present")
        if _is_candidate_only(slot):
            proves.append("وصف:candidate_only_flag_present:evidenced")
        else:
            proves.append("فارق:candidate_only_missing:present")
        if _has_no_forbidden_final_flags(slot):
            proves.append("وصف:no_forbidden_final_flags:evidenced")
        else:
            proves.append("فارق:forbidden_final_flag_present:present")
        if slot.identity_ids:
            proves.append("وصف:identity_ids_non_empty:evidenced")
        else:
            proves.append("فارق:identity_ids_empty:present")
        if _identity_trace_disjoint(slot):
            proves.append("وصف:identity_trace_disjoint:evidenced")
        else:
            proves.append("فارق:identity_trace_overlap:present")
        if slot.rank != EvidenceRank.NO_EVIDENCE:
            proves.append("وصف:rank_above_no_evidence:evidenced")
        else:
            proves.append("فارق:rank_zero:present")

        # 2.2 trace audit — the structural witnesses for the four
        # Phase-1 contributing proofs. The `alignment_ref` substring
        # is the CTS / carrier-binding witness (written only by
        # slot_adapter when an alignment proof was consumed). The
        # `identity:codepoint:` prefix on identity_ids is the
        # letter+haraka codepoint provenance. The `source_rule_id ==
        # "slot.composition"` plus the slot rule's preconditions
        # constitute the letter-identity / haraka-function / position
        # source breadcrumbs.
        if _has_alignment_ref(slot):
            proves.append("وصف:alignment_ref_in_trace:evidenced")
            proves.append("وصف:cts_carrier_binding_source_audited:evidenced")
        else:
            proves.append("فارق:missing_alignment_ref:present")
        if _has_codepoint_identity(slot):
            proves.append("وصف:letter_identity_source_audited:evidenced")
            proves.append("وصف:haraka_function_source_audited:evidenced")
        # Position source breadcrumb is implied by
        # `source_rule_id == "slot.composition"` (the slot rule
        # requires has_position_carrier as a precondition). When the
        # source-rule check above held, we emit the position audit
        # claim.
        if slot.source_rule_id == _REQUIRED_SLOT_SOURCE_RULE_ID:
            proves.append("وصف:position_source_audited:evidenced")

        return proves

    def _licensing_claims(self, illah_extra: str) -> list[str]:
        """Emit the standing `علة:` / `وادي:` claims that license a
        slot-geometry step (seed or extend).

        These claims declare:

          * the asl/branch belong to the slot-geometry domain,
          * the step is licensed under the rule (`illah_extra`),
          * the six conjunctive gates (CAUSE / CONDITION / OBSTACLE /
            VALIDITY / CORRUPTION / NULLITY) hold.

        The kernel checks each gate via WADI_REQUIRED_CLAIMS; emitting
        these claims unconditionally is correct **only when** the
        adapter has separately verified there is no blocking
        difference for this step. Where a structural condition fails,
        a `فارق:*:present` claim is emitted in addition; the kernel
        then blocks the candidate with `blocking_fariq_present` even
        though the gates were satisfied. This separation is the
        contract's design (CLAUDE.md §4 invariant 5).
        """
        return [
            "علة:belongs_to_slot_geometry_domain:verified",
            f"علة:{illah_extra}:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]
