"""SlotGeometryClosureCheck — Phase-2 follow-up.

Implements the runtime carrier ``MinimalCompleteClosureEvidence`` and the
deterministic producer ``SlotGeometryClosureCheck`` per
``MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md``.

This module is **observation only**. Per contract §3, the producer:

  * reads structural facts about a ``SlotGeometryCandidate``,
  * returns a fully-populated ``MinimalCompleteClosureEvidence`` when
    all eight §6 conditions hold,
  * returns ``None`` when at least one condition fails,
  * does NOT mutate the input,
  * does NOT invoke ``QiyasKernel.apply``,
  * does NOT emit any qiyas ``Candidate`` of any type,
  * does NOT consult ``ArabicArticulationRegistry``,
  * does NOT consult ``SequenceContextTokenizer`` markers or raw text.

Per contract §2, ``MinimalCompleteClosureEvidence`` is an **Evidence
carrier**, not a ``Candidate``. The carrier carries one boolean
witness per §6 closure condition plus audit metadata about the
consumed geometry. The forbidden name ``MinimalCompleteClosureCandidate``
is not defined anywhere in this module.

Per contract §5, the producer is **length-agnostic**: it accepts any
``SlotGeometryCandidate`` regardless of ``length`` or ``construction_mode``.
The downstream MIU readiness layer narrows scope at its own admission
boundary.

Per contract §6.1, audit trace strings follow the schema

    trace:slot_geometry_closure:<condition_name>:passed
    trace:slot_geometry_closure:<condition_name>:failed

with ``<condition_name>`` ranging over the eight §6 booleans.

Authority basis (cited verbatim in the contract):
  CLAUDE.md §0 / §3 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
  RECURSIVE_LICENSED_EXTENSION_CONTRACT.md §1 / §7 / §10 / §11 / §12,
  MINIMAL_COMPLETE_CLOSURE_CONTRACT.md §1 / §3 / §5 / §9 / §11 / §12,
  SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md §1 / §6 / §8 / §9 / §11,
  MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md
    (this module's controlling contract).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Eight condition names — single source of truth for both the dataclass
# field labels and the §6.1 audit_trace_ids schema.
CLOSURE_CONDITION_NAMES: tuple[str, ...] = (
    "licensed_beginning",
    "licensed_ending",
    "all_internal_bindings_licensed",
    "no_open_demand",
    "no_blocking_difference",
    "residuals_preserved",
    "rank_above_no_evidence",
    "output_remains_candidate_only",
)

# §6.1 audit-trace schema prefix.
_AUDIT_TRACE_PREFIX = "trace:slot_geometry_closure:"

# Trace-id prefixes that carry geometry metadata, written by
# ``slot_geometry_adapter.py`` onto a ``SlotGeometryCandidate``'s
# ``trace_ids``. Read-only — this module does not modify the geometry.
_LENGTH_TRACE_PREFIX = "trace:slot_geometry:length:"
_MODE_TRACE_PREFIX = "trace:slot_geometry:construction_mode:"

# §4.1 of the alignment-trace contract — the SlotGeometryCandidate's
# source_rule_id must be one of these two.
_VALID_SLOT_GEOMETRY_RULE_IDS: frozenset[str] = frozenset({
    "slot_geometry.seed",
    "slot_geometry.extend",
})

_VALID_CONSTRUCTION_MODES: frozenset[str] = frozenset({"seed", "extension"})

# Output-flag discipline (mirrors CLAUDE.md §4 invariant 9 and
# alignment-trace contract §6.1).
_REQUIRED_OUTPUT_FLAG = "CandidateOnly"
_FORBIDDEN_FINAL_FLAGS: frozenset[str] = frozenset({
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
    "FinalCaseJudgment",
    "DalalahCandidate",
})


# ---------------------------------------------------------------------------
# Public-facing Protocol — duck-typed interface for a SlotGeometryCandidate.
#
# The producer reads only structural fields off the input. We declare a
# Protocol so that callers' tooling type-checks correctly without this
# module having to import the concrete ``Candidate`` class — that is the
# §3 / §11 producer-import discipline of the contract.
# ---------------------------------------------------------------------------


class SlotGeometryCandidateLike(Protocol):
    """Structural interface this producer expects from its input.

    A real ``qiyas_core.candidate.Candidate`` with
    ``candidate_type == "SlotGeometryCandidate"`` satisfies this
    protocol; so does any test fixture that exposes the same attributes.
    """

    candidate_type: str
    layer: str
    source_rule_id: str
    candidate_id: str
    identity_ids: tuple[str, ...]
    trace_ids: tuple[str, ...]
    output_flags: frozenset[str]
    rank: Any           # enum-like; structurally read via `.name`
    residuals: tuple[Any, ...]
    status: Any         # enum-like; structurally read via `.value`


# ---------------------------------------------------------------------------
# MinimalCompleteClosureEvidence — frozen Evidence carrier (NOT a Candidate)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MinimalCompleteClosureEvidence:
    """Immutable Evidence carrier for slot-geometry closure.

    Per ``MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md`` §2:

      * **Evidence carrier**, not a ``Candidate``.
      * Eight boolean fields, one per §6 closure condition.
      * Audit metadata about the consumed geometry (preserved verbatim).
      * Construction is conjunctive: the carrier is **only** instantiated
        when all eight booleans are ``True``. If any condition fails,
        ``SlotGeometryClosureCheck.check`` returns ``None`` rather than
        building a half-true carrier.

    Deliberately has **no** ``candidate_type``, **no** ``status``, **no**
    ``output_flags`` field — the carrier is structurally NOT a
    Candidate-shape.
    """

    # § The eight §6 closure-condition booleans.
    licensed_beginning: bool
    licensed_ending: bool
    all_internal_bindings_licensed: bool
    no_open_demand: bool
    no_blocking_difference: bool
    residuals_preserved: bool
    rank_above_no_evidence: bool
    output_remains_candidate_only: bool

    # § Audit metadata about the consumed geometry, preserved verbatim.
    geometry_candidate_id: str
    geometry_layer: str
    geometry_length: int
    geometry_construction_mode: str
    geometry_identity_ids: tuple[str, ...]
    geometry_trace_ids: tuple[str, ...]
    geometry_rank: str       # rank.name as a string (no enum coupling)

    # § Per-evidence unique identifier — never an identity.
    evidence_id: str

    # § The §6.1 audit_trace_ids — eight `:passed` entries when the
    # carrier is constructed.
    audit_trace_ids: tuple[str, ...]


# ---------------------------------------------------------------------------
# §6.1 audit-trace helpers
# ---------------------------------------------------------------------------


def audit_trace_entry(condition_name: str, passed: bool) -> str:
    """Build a single audit_trace_ids entry per the §6.1 schema.

    The function is public so that tests (and the producer below) share
    one canonical implementation; it never mutates input.
    """
    if condition_name not in CLOSURE_CONDITION_NAMES:
        raise ValueError(
            f"unknown closure condition name: {condition_name!r}"
        )
    status = "passed" if passed else "failed"
    return f"{_AUDIT_TRACE_PREFIX}{condition_name}:{status}"


# ---------------------------------------------------------------------------
# Geometry-metadata readers — local, deliberately do not import from
# slot_geometry_adapter.py (the contract scopes this batch to two new
# files; importing helpers would still respect scope, but inlining the
# readers keeps the module fully self-contained and eliminates any
# transitive Candidate import via the adapter).
# ---------------------------------------------------------------------------


def _read_length_from_trace(geom: SlotGeometryCandidateLike) -> int | None:
    for tid in geom.trace_ids:
        if tid.startswith(_LENGTH_TRACE_PREFIX):
            try:
                return int(tid[len(_LENGTH_TRACE_PREFIX):])
            except ValueError:
                return None
    return None


def _read_construction_mode_from_trace(
    geom: SlotGeometryCandidateLike,
) -> str | None:
    for tid in geom.trace_ids:
        if tid.startswith(_MODE_TRACE_PREFIX):
            return tid[len(_MODE_TRACE_PREFIX):]
    return None


def _read_status_value(geom: SlotGeometryCandidateLike) -> str | None:
    """Return ``status.value`` as a string, or ``None`` when absent."""
    status = getattr(geom, "status", None)
    if status is None:
        return None
    value = getattr(status, "value", None)
    return value if isinstance(value, str) else None


def _read_rank_name(geom: SlotGeometryCandidateLike) -> str | None:
    """Return ``rank.name`` as a string, or ``None`` when absent."""
    rank = getattr(geom, "rank", None)
    if rank is None:
        return None
    name = getattr(rank, "name", None)
    return name if isinstance(name, str) else None


# ---------------------------------------------------------------------------
# §6 condition evaluators — each returns a single boolean, read structurally
# off the input. None of them mutates the geometry or any of its fields.
# ---------------------------------------------------------------------------


def _check_licensed_beginning(
    geom: SlotGeometryCandidateLike,
    length: int,
    construction_mode: str,
) -> bool:
    """§6 condition 1.

    A geometrically-licensed beginning is witnessed by:
      * length >= 1, and
      * source_rule_id is a SlotGeometry rule, and
      * construction_mode is "seed" (length=1 trivial) or "extension"
        (length>1, transitively rooted in a seed).
    """
    if length < 1:
        return False
    if geom.source_rule_id not in _VALID_SLOT_GEOMETRY_RULE_IDS:
        return False
    return construction_mode in _VALID_CONSTRUCTION_MODES


def _check_licensed_ending(
    geom: SlotGeometryCandidateLike,
    length: int,
    construction_mode: str,
) -> bool:
    """§6 condition 2.

    For length=1 (Seed) the ending coincides with the beginning. For
    length>1 the geometry's accepted status is the witness that the
    last Extend step terminated cleanly.
    """
    if length < 1:
        return False
    if construction_mode not in _VALID_CONSTRUCTION_MODES:
        return False
    status_value = _read_status_value(geom)
    if status_value is None:
        return False
    return status_value == "accepted"


def _check_all_internal_bindings_licensed(
    geom: SlotGeometryCandidateLike,
    length: int,
    construction_mode: str,
) -> bool:
    """§6 condition 3.

    For length=1 this is vacuously true (no ``Extend`` step exists).
    For length>1 the geometry's accepted status implies every
    ``SlotBindingEvidence`` along the construction history was accepted
    under the slot-geometry layer's gate policy (the kernel would
    otherwise have blocked the candidate).
    """
    if length == 1:
        return construction_mode == "seed"
    if length > 1:
        status_value = _read_status_value(geom)
        return (
            construction_mode == "extension"
            and status_value == "accepted"
        )
    return False


def _check_no_open_demand(geom: SlotGeometryCandidateLike) -> bool:
    """§6 condition 4.

    The slot-geometry layer's Demand Catalogue is fully discharged. The
    catalogue's initial contents are deferred (per the closure contract
    §3.4 / §4); the structural witness here is that the geometry carries
    no deferred residual.
    """
    for r in geom.residuals:
        rtype = getattr(r, "residual_type", "")
        if isinstance(rtype, str) and rtype.startswith("deferred_"):
            return False
    return True


def _check_no_blocking_difference(geom: SlotGeometryCandidateLike) -> bool:
    """§6 condition 5.

    No ``فارق:*:present`` (invalidating-difference) claim is present.
    The kernel records such claims as residuals with
    ``residual_type == "blocking_fariq_present"``.

    Additionally enforces that the candidate's status is ACCEPTED — a
    blocked candidate cannot satisfy closure regardless of which
    specific residual blocked it.
    """
    if _read_status_value(geom) != "accepted":
        return False
    for r in geom.residuals:
        rtype = getattr(r, "residual_type", "")
        if rtype == "blocking_fariq_present":
            return False
    return True


def _check_residuals_preserved(geom: SlotGeometryCandidateLike) -> bool:
    """§6 condition 6.

    Structural witness: the geometry carries a well-formed
    ``residuals`` tuple, and no residual is marked as ``discarded``.
    """
    residuals = getattr(geom, "residuals", None)
    if not isinstance(residuals, tuple):
        return False
    for r in residuals:
        rtype = getattr(r, "residual_type", "")
        if isinstance(rtype, str) and "discarded" in rtype.lower():
            return False
    return True


def _check_rank_above_no_evidence(geom: SlotGeometryCandidateLike) -> bool:
    """§6 condition 7.

    ``rank > NO_EVIDENCE``. We compare ``rank.name`` as a string so we
    do not couple this module to the ``EvidenceRank`` enum.
    """
    rank_name = _read_rank_name(geom)
    return rank_name is not None and rank_name != "NO_EVIDENCE"


def _check_output_remains_candidate_only(
    geom: SlotGeometryCandidateLike,
) -> bool:
    """§6 condition 8.

    ``output_flags ⊇ {CandidateOnly}`` and ``output_flags`` carries no
    final-judgment flag.
    """
    flags = getattr(geom, "output_flags", None)
    if not isinstance(flags, (set, frozenset)):
        return False
    if _REQUIRED_OUTPUT_FLAG not in flags:
        return False
    if flags & _FORBIDDEN_FINAL_FLAGS:
        return False
    return True


# ---------------------------------------------------------------------------
# Internal driver — evaluates the eight conditions, builds the carrier
# (or returns None) per §3 / §6.
# ---------------------------------------------------------------------------


def _looks_like_slot_geometry_candidate(geom: Any) -> bool:
    """Light shape check before condition evaluation.

    The producer's consumption surface is closed to
    ``SlotGeometryCandidate`` (contract §4). If the input does not look
    like one (wrong ``candidate_type`` or ``layer``), the producer
    returns ``None`` immediately — the eight conditions are only
    meaningful when the input is the right shape.
    """
    candidate_type = getattr(geom, "candidate_type", None)
    layer = getattr(geom, "layer", None)
    if candidate_type != "SlotGeometryCandidate":
        return False
    if layer != "SlotGeometryQiyas":
        return False
    return True


def _evaluate(geom: SlotGeometryCandidateLike) -> MinimalCompleteClosureEvidence | None:
    """Internal implementation shared by the class and the convenience
    function. Returns the carrier when all eight conditions hold, or
    ``None`` otherwise."""
    if not _looks_like_slot_geometry_candidate(geom):
        return None

    length = _read_length_from_trace(geom)
    construction_mode = _read_construction_mode_from_trace(geom)

    if length is None or construction_mode is None:
        return None
    if construction_mode not in _VALID_CONSTRUCTION_MODES:
        return None

    # Evaluate the eight conditions in §6 order.
    cond_results = {
        "licensed_beginning": _check_licensed_beginning(
            geom, length, construction_mode
        ),
        "licensed_ending": _check_licensed_ending(
            geom, length, construction_mode
        ),
        "all_internal_bindings_licensed": _check_all_internal_bindings_licensed(
            geom, length, construction_mode
        ),
        "no_open_demand": _check_no_open_demand(geom),
        "no_blocking_difference": _check_no_blocking_difference(geom),
        "residuals_preserved": _check_residuals_preserved(geom),
        "rank_above_no_evidence": _check_rank_above_no_evidence(geom),
        "output_remains_candidate_only": _check_output_remains_candidate_only(
            geom
        ),
    }

    # Conjunctive: build the carrier only when all eight pass.
    if not all(cond_results.values()):
        return None

    audit_trace_ids = tuple(
        audit_trace_entry(name, True)
        for name in CLOSURE_CONDITION_NAMES
    )

    return MinimalCompleteClosureEvidence(
        licensed_beginning=cond_results["licensed_beginning"],
        licensed_ending=cond_results["licensed_ending"],
        all_internal_bindings_licensed=cond_results["all_internal_bindings_licensed"],
        no_open_demand=cond_results["no_open_demand"],
        no_blocking_difference=cond_results["no_blocking_difference"],
        residuals_preserved=cond_results["residuals_preserved"],
        rank_above_no_evidence=cond_results["rank_above_no_evidence"],
        output_remains_candidate_only=cond_results["output_remains_candidate_only"],
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=geom.layer,
        geometry_length=length,
        geometry_construction_mode=construction_mode,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        geometry_rank=_read_rank_name(geom) or "",
        evidence_id=f"ev:slot_geometry_closure:{uuid.uuid4().hex[:12]}",
        audit_trace_ids=audit_trace_ids,
    )


# ---------------------------------------------------------------------------
# Public API — the reserved name from contract §3 plus a thin
# module-level convenience.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SlotGeometryClosureCheck:
    """Deterministic checker for slot-geometry closure.

    Per ``MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md`` §3:

      * **Not** a Qiyas layer.
      * **Not** a ``QiyasRule``.
      * **Does not** invoke ``QiyasKernel.apply``.
      * **Does not** produce a ``Candidate`` of any type.
      * Returns ``MinimalCompleteClosureEvidence | None``.

    The class is stateless; instances are interchangeable. A
    ``check(geom)`` call and a ``call(geom)`` are equivalent.
    """

    def check(
        self,
        geom: SlotGeometryCandidateLike,
    ) -> MinimalCompleteClosureEvidence | None:
        """Evaluate the eight §6 closure conditions on ``geom``.

        Returns a fully-populated ``MinimalCompleteClosureEvidence``
        when all eight hold; returns ``None`` otherwise.
        """
        return _evaluate(geom)

    def __call__(
        self,
        geom: SlotGeometryCandidateLike,
    ) -> MinimalCompleteClosureEvidence | None:
        return self.check(geom)


def check_slot_geometry_closure(
    geom: SlotGeometryCandidateLike,
) -> MinimalCompleteClosureEvidence | None:
    """Module-level convenience — equivalent to
    ``SlotGeometryClosureCheck().check(geom)``.

    Provided so tests and downstream consumers can call the checker
    without instantiating the class.
    """
    return _evaluate(geom)
