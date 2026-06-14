"""Layer 5 LicensedSyllableSequenceCandidate runtime — potential-only.

Authorization:
    Narrow Layer 5 authorization (2026-06-14). Maintainer Hussein Hiyassat
    explicitly authorized this module as a potential-only runtime slice that
    composes already-licensed Layer 4 ``LicensedSyllableCandidate`` objects
    into an ordered, identity-preserving structural sequence. This is a
    single-layer narrow authorization, NOT a global runtime unfreeze, NOT
    REC-6, and NOT authorization for Layer 6+.

Constitutional boundary:
    - runtime_status     = "layer5_potential_only"
    - meaning_status     = "not_introduced"
    - hukm_status        = "not_introduced"
    - irab_status        = "not_introduced"
    - reality_status     = "not_introduced"
    - candidate.runtime  = "potential_only_not_semantic_runtime"

Role (anti-duplication):
    Layer 5 only *composes* adjacent, ordered, boundary-preserving Layer 4
    syllable candidates into a potential-only sequence candidate. It does not
    license individual syllables (that is Layer 4), does not assess single-unit
    readiness (that is the MIU readiness layer), and does not check closure
    (that is slot_geometry_closure_check). It constructs; it does not infer.

This module makes NO claim of wordhood, lafz, root, wazn, morphology, grammar,
i'rab, dalalah, tafsir, lexical meaning, hukm, RealityClaim, or FinalMeaning.
It renders/reports only structural facts.

Public surface:
    SequenceAdjacencyEvidence
    SequenceOrderEvidence
    SequenceIdentityPreservationEvidence
    SequenceBoundaryPreservationEvidence
    SyllableSequenceInvalidationEvidence
    LicensedSyllableSequenceCandidate
    LicensedSyllableSequenceAnalysis
    compose_syllable_sequence(candidates)            -> (candidate|None, invalidation|None)
    analyze_licensed_syllable_sequence(text)         -> LicensedSyllableSequenceAnalysis
    render_licensed_syllable_sequence_analysis(a)    -> str

CLI:
    PYTHONPATH=src:. python3 -m qiyas_core.licensed_syllable_sequence "بِ ضَ وَ يَ"
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional, Sequence

from qiyas_core.licensed_syllable import (
    CANDIDATE_RUNTIME_STATUS as LAYER4_CANDIDATE_RUNTIME_STATUS,
    LicensedSyllableCandidate,
    analyze_licensed_syllables,
)

# ─────────────────────────────────────────────────────────────────────────────
# Module-level constants
# ─────────────────────────────────────────────────────────────────────────────

LAYER5_AUTHORIZATION_DATE = "2026-06-14"
LAYER5_AUTHORIZATION_SCOPE = "layer5_only_potential_only_not_global_unfreeze"

LAYER5_RUNTIME_STATUS = "layer5_potential_only"
SEQUENCE_CANDIDATE_RUNTIME_STATUS = "potential_only_not_semantic_runtime"
NOT_INTRODUCED = "not_introduced"

# A structural separator only — Layer 5 reconstructs the observed token spacing
# and makes no wordhood claim by joining constituents.
SEQUENCE_SEPARATOR = " "


# ─────────────────────────────────────────────────────────────────────────────
# Evidence dataclasses (all frozen)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SequenceAdjacencyEvidence:
    """Proves constituents occupy consecutive Layer 4 token indices."""

    token_indices: tuple[int, ...]
    adjacent: bool
    gap_free: bool
    reason: str


@dataclass(frozen=True)
class SequenceOrderEvidence:
    """Proves constituents are in strictly increasing token order."""

    token_indices: tuple[int, ...]
    strictly_increasing: bool
    reason: str


@dataclass(frozen=True)
class SequenceIdentityPreservationEvidence:
    """Proves each constituent's surface identity is preserved unchanged."""

    per_constituent_preserved: tuple[bool, ...]
    identity_preserved: bool
    reason: str


@dataclass(frozen=True)
class SequenceBoundaryPreservationEvidence:
    """Proves each constituent boundary is preserved and spans do not overlap."""

    spans: tuple[tuple[int, int], ...]
    per_constituent_preserved: tuple[bool, ...]
    non_overlapping: bool
    boundary_preserved: bool
    reason: str


@dataclass(frozen=True)
class SyllableSequenceInvalidationEvidence:
    """Recorded reason a sequence candidate was NOT emitted (residual)."""

    constituent_surfaces: tuple[str, ...]
    reason: str
    adjacent: bool
    ordered: bool
    identity_preserved: bool
    boundary_preserved: bool
    candidate_emitted: bool


@dataclass(frozen=True)
class LicensedSyllableSequenceCandidate:
    """Potential-only Layer 5 candidate; no semantic runtime claim is made."""

    token_index_span: tuple[int, int]
    constituent_token_indices: tuple[int, ...]
    constituent_surfaces: tuple[str, ...]
    constituent_shapes: tuple[str, ...]
    surface_form_vocalized: str
    surface_codepoints: tuple[str, ...]
    length: int
    adjacency_evidence: SequenceAdjacencyEvidence
    order_evidence: SequenceOrderEvidence
    identity_evidence: SequenceIdentityPreservationEvidence
    boundary_evidence: SequenceBoundaryPreservationEvidence
    identity_preserved: bool
    potential_only: bool
    runtime_status: str


@dataclass(frozen=True)
class LicensedSyllableSequenceAnalysis:
    """Bundle: input + lower trace summary + emitted candidates + invalidations."""

    input_text: str
    lower_trace_summary: str
    candidates: tuple[LicensedSyllableSequenceCandidate, ...]
    invalidations: tuple[SyllableSequenceInvalidationEvidence, ...]
    runtime_status: str
    meaning_status: str
    hukm_status: str
    irab_status: str
    dalalah_status: str
    reality_status: str


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _surface_codepoints(surface: str) -> tuple[str, ...]:
    return tuple(f"U+{ord(ch):04X}" for ch in surface)


def _is_licensed_layer4(c: LicensedSyllableCandidate) -> bool:
    """A Layer 4 candidate is admissible input iff it is a licensed,
    potential-only candidate whose own surface identity is self-consistent."""
    return (
        c.potential_only
        and c.runtime_status == LAYER4_CANDIDATE_RUNTIME_STATUS
        and c.surface_codepoints == _surface_codepoints(c.surface_form_vocalized)
    )


def _invalidation(
    candidates: Sequence[LicensedSyllableCandidate],
    *,
    reason: str,
    adjacent: bool,
    ordered: bool,
    identity_preserved: bool,
    boundary_preserved: bool,
) -> SyllableSequenceInvalidationEvidence:
    return SyllableSequenceInvalidationEvidence(
        constituent_surfaces=tuple(c.surface_form_vocalized for c in candidates),
        reason=reason,
        adjacent=adjacent,
        ordered=ordered,
        identity_preserved=identity_preserved,
        boundary_preserved=boundary_preserved,
        candidate_emitted=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Core composition
# ─────────────────────────────────────────────────────────────────────────────


def compose_syllable_sequence(
    candidates: Sequence[LicensedSyllableCandidate],
) -> tuple[
    Optional[LicensedSyllableSequenceCandidate],
    Optional[SyllableSequenceInvalidationEvidence],
]:
    """Compose Layer 4 candidates into a Layer 5 sequence candidate.

    Returns (candidate, invalidation); exactly one is non-None. A candidate is
    emitted only when every lower candidate is licensed and adjacency, order,
    identity, and boundary evidence are all satisfied. Otherwise an invalidation
    residual is returned and no candidate is emitted.
    """
    cands = tuple(candidates)
    token_indices = tuple(c.token_index for c in cands)

    # 1. Non-empty.
    if not cands:
        return None, _invalidation(
            cands,
            reason="no licensed lower candidates to compose",
            adjacent=False,
            ordered=False,
            identity_preserved=False,
            boundary_preserved=False,
        )

    # 2. Every lower candidate must be a licensed potential-only Layer 4 candidate.
    if not all(_is_licensed_layer4(c) for c in cands):
        return None, _invalidation(
            cands,
            reason=(
                "one or more lower units are not licensed potential-only "
                "Layer 4 candidates"
            ),
            adjacent=False,
            ordered=False,
            identity_preserved=False,
            boundary_preserved=False,
        )

    # 3. Identity preserved per constituent.
    per_identity = tuple(c.identity_preserved for c in cands)
    identity_ok = all(per_identity)
    if not identity_ok:
        return None, _invalidation(
            cands,
            reason="identity drift in one or more lower candidates",
            adjacent=False,
            ordered=False,
            identity_preserved=False,
            boundary_preserved=False,
        )

    # 4. Boundary preserved per constituent.
    per_boundary = tuple(c.boundary_evidence.boundary_preserved for c in cands)
    boundary_ok = all(per_boundary)
    spans = tuple(
        (c.boundary_evidence.start_index, c.boundary_evidence.end_index)
        for c in cands
    )
    if not boundary_ok:
        return None, _invalidation(
            cands,
            reason="boundary drift in one or more lower candidates",
            adjacent=False,
            ordered=False,
            identity_preserved=identity_ok,
            boundary_preserved=False,
        )

    # 5. Strict order.
    strictly_increasing = all(
        token_indices[i] < token_indices[i + 1] for i in range(len(token_indices) - 1)
    )
    if not strictly_increasing:
        return None, _invalidation(
            cands,
            reason="lower candidates are out of token order",
            adjacent=False,
            ordered=False,
            identity_preserved=identity_ok,
            boundary_preserved=boundary_ok,
        )

    # 6. Adjacency (consecutive token indices, no gap).
    adjacent = all(
        token_indices[i + 1] - token_indices[i] == 1
        for i in range(len(token_indices) - 1)
    )
    if not adjacent:
        return None, _invalidation(
            cands,
            reason="lower candidates are not adjacent (token-index gap)",
            adjacent=False,
            ordered=True,
            identity_preserved=identity_ok,
            boundary_preserved=boundary_ok,
        )

    # 7. Character spans must not overlap (boundary preservation across the run).
    non_overlapping = all(
        spans[i][1] <= spans[i + 1][0] for i in range(len(spans) - 1)
    )
    if not non_overlapping:
        return None, _invalidation(
            cands,
            reason="lower candidate character spans overlap",
            adjacent=True,
            ordered=True,
            identity_preserved=identity_ok,
            boundary_preserved=False,
        )

    # All evidence satisfied — build the sequence candidate.
    surfaces = tuple(c.surface_form_vocalized for c in cands)
    surface_form = SEQUENCE_SEPARATOR.join(surfaces)

    adjacency_evidence = SequenceAdjacencyEvidence(
        token_indices=token_indices,
        adjacent=True,
        gap_free=True,
        reason="consecutive token indices with no gap",
    )
    order_evidence = SequenceOrderEvidence(
        token_indices=token_indices,
        strictly_increasing=True,
        reason="token indices strictly increasing",
    )
    identity_evidence = SequenceIdentityPreservationEvidence(
        per_constituent_preserved=per_identity,
        identity_preserved=True,
        reason="every constituent surface identity preserved",
    )
    boundary_evidence = SequenceBoundaryPreservationEvidence(
        spans=spans,
        per_constituent_preserved=per_boundary,
        non_overlapping=True,
        boundary_preserved=True,
        reason="constituent boundaries preserved and non-overlapping",
    )

    candidate = LicensedSyllableSequenceCandidate(
        token_index_span=(token_indices[0], token_indices[-1]),
        constituent_token_indices=token_indices,
        constituent_surfaces=surfaces,
        constituent_shapes=tuple(c.shape.value for c in cands),
        surface_form_vocalized=surface_form,
        surface_codepoints=_surface_codepoints(surface_form),
        length=len(cands),
        adjacency_evidence=adjacency_evidence,
        order_evidence=order_evidence,
        identity_evidence=identity_evidence,
        boundary_evidence=boundary_evidence,
        identity_preserved=True,
        potential_only=True,
        runtime_status=SEQUENCE_CANDIDATE_RUNTIME_STATUS,
    )
    return candidate, None


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────


def analyze_licensed_syllable_sequence(text: str) -> LicensedSyllableSequenceAnalysis:
    """Run Layer 5 over input text.

    Steps:
      1. Run Layer 4 analyze_licensed_syllables(text).
      2. If Layer 4 produced any invalidation (some token unlicensed), the
         lower set is incomplete — emit a sequence invalidation, no candidate.
      3. Otherwise compose the ordered Layer 4 candidates into a sequence.

    The bundle is potential-only; no meaning / hukm / i'rab / dalalah / reality
    claim is introduced. The four status fields remain "not_introduced". Layer 4
    output is consumed read-only and is not mutated.
    """
    lower = analyze_licensed_syllables(text)
    lower_summary = (
        f"lower_candidates={len(lower.candidates)} "
        f"lower_invalidations={len(lower.invalidations)} "
        f"lower_runtime_status={lower.runtime_status}"
    )

    if lower.invalidations:
        invalidation = _invalidation(
            lower.candidates,
            reason=(
                "lower layer produced unlicensed units; sequence composition "
                "requires every lower unit to be a licensed Layer 4 candidate"
            ),
            adjacent=False,
            ordered=False,
            identity_preserved=False,
            boundary_preserved=False,
        )
        candidates: tuple[LicensedSyllableSequenceCandidate, ...] = ()
        invalidations: tuple[SyllableSequenceInvalidationEvidence, ...] = (
            invalidation,
        )
    else:
        candidate, invalidation = compose_syllable_sequence(lower.candidates)
        candidates = (candidate,) if candidate is not None else ()
        invalidations = (invalidation,) if invalidation is not None else ()

    return LicensedSyllableSequenceAnalysis(
        input_text=text,
        lower_trace_summary=lower_summary,
        candidates=candidates,
        invalidations=invalidations,
        runtime_status=LAYER5_RUNTIME_STATUS,
        meaning_status=NOT_INTRODUCED,
        hukm_status=NOT_INTRODUCED,
        irab_status=NOT_INTRODUCED,
        dalalah_status=NOT_INTRODUCED,
        reality_status=NOT_INTRODUCED,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Rendering — structural facts only
# ─────────────────────────────────────────────────────────────────────────────


def _render_candidate(c: LicensedSyllableSequenceCandidate) -> list[str]:
    return [
        f"  - token_index_span={c.token_index_span}",
        f"    length={c.length}",
        f"    constituent_token_indices={c.constituent_token_indices}",
        f"    constituent_surfaces={c.constituent_surfaces!r}",
        f"    constituent_shapes={','.join(c.constituent_shapes)}",
        f"    surface_form_vocalized={c.surface_form_vocalized!r}",
        f"    identity_preserved={c.identity_preserved}",
        f"    adjacent={c.adjacency_evidence.adjacent}",
        f"    strictly_increasing={c.order_evidence.strictly_increasing}",
        f"    boundary_preserved={c.boundary_evidence.boundary_preserved}",
        f"    codepoints={','.join(c.surface_codepoints)}",
    ]


def _render_invalidation(inv: SyllableSequenceInvalidationEvidence) -> list[str]:
    return [
        f"  - constituent_surfaces={inv.constituent_surfaces!r}",
        f"    reason={inv.reason}",
        f"    adjacent={inv.adjacent}",
        f"    ordered={inv.ordered}",
        f"    identity_preserved={inv.identity_preserved}",
        f"    boundary_preserved={inv.boundary_preserved}",
        f"    candidate_emitted={inv.candidate_emitted}",
    ]


def render_licensed_syllable_sequence_analysis(
    analysis: LicensedSyllableSequenceAnalysis,
) -> str:
    """Deterministic terminal-readable rendering of a Layer 5 analysis."""
    lines: list[str] = []

    lines.append("## Licensed Syllable Sequence Analysis")
    lines.append("=" * 60)
    lines.append(f"  input_text={analysis.input_text!r}")
    lines.append(f"  runtime_status={analysis.runtime_status}")
    lines.append(f"  candidate_count={len(analysis.candidates)}")
    lines.append(f"  invalidation_count={len(analysis.invalidations)}")
    lines.append(f"  lower_trace_summary={analysis.lower_trace_summary}")
    lines.append("")

    lines.append("## Candidates")
    lines.append("=" * 60)
    if analysis.candidates:
        for c in analysis.candidates:
            lines.extend(_render_candidate(c))
            lines.append("")
    else:
        lines.append("  (none)")
        lines.append("")

    lines.append("## Invalidations")
    lines.append("=" * 60)
    if analysis.invalidations:
        for inv in analysis.invalidations:
            lines.extend(_render_invalidation(inv))
            lines.append("")
    else:
        lines.append("  (none)")
        lines.append("")

    lines.append("## Constitutional Boundary")
    lines.append("=" * 60)
    lines.append("  * structural composition only — no wordhood")
    lines.append("  * no lexical meaning introduced")
    lines.append("  * no root / wazn / morphology introduced")
    lines.append("  * no grammar / i'rab introduced")
    lines.append("  * no dalalah introduced")
    lines.append("  * no tafsir introduced")
    lines.append("  * no hukm introduced")
    lines.append("  * no reality claim introduced")
    lines.append("  * potential-only Layer 5")
    lines.append("  * no Layer 6 runtime")
    lines.append(
        f"  * narrow authorization: Layer 5 only "
        f"({LAYER5_AUTHORIZATION_DATE} maintainer directive); "
        "the global REC freeze remains in effect; not REC-6"
    )
    lines.append(
        f"  * meaning_status={analysis.meaning_status} "
        f"hukm_status={analysis.hukm_status} "
        f"irab_status={analysis.irab_status} "
        f"dalalah_status={analysis.dalalah_status} "
        f"reality_status={analysis.reality_status}"
    )

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: python3 -m qiyas_core.licensed_syllable_sequence <text>")
        return 2
    text = args[0]
    analysis = analyze_licensed_syllable_sequence(text)
    print(render_licensed_syllable_sequence_analysis(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
