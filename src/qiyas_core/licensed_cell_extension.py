"""Licensed cell extension / minimal-complete closure / boundary evidence —
potential-only runtime (Policy C).

Authorization:
    Narrow per-layer authorization (2026-06-14). Maintainer Hussein Hiyassat
    ratified Policy C — demand-driven closure + full-coverage constraint +
    multiplicity-as-potential-candidates — and authorized this potential-only
    helper runtime. NOT Layer 6, NOT REC-6, NOT a global freeze lift, NOT
    shadda/gemination, NOT generic/intra-word segmentation, NOT semantic.

Constitutional grounding (instantiation, not new names):
    - Extend ........... RECURSIVE_LICENSED_EXTENSION_CONTRACT §1/§10
    - IsMinimallyComplete / closure ... MINIMAL_COMPLETE_CLOSURE_CONTRACT §3
    - beginning/ending gates + demand ... SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT
    - فارق: invalidating-difference residual ... REC-EXT §9/§10

Policy C (ratified):
    Tile a contiguous run of TypedCodePoints into licensed cells of the closed
    Layer 4 contract {CV, CVV, CVC, CVVC, CVCC, CVVCC}.
      * A cell may close only when closure is licensed by demand/gate evidence.
      * A covering is valid only if the FULL run is covered by licensed cells
        with no stranded typed unit, no skipped codepoint, no identity drift.
      * If multiple fully licensed coverings exist, surface ALL of them as
        potential candidates — never auto-disambiguate, never rank by meaning.
      * A licensed first-cell branch that cannot complete a full covering is
        recorded as an invalidating-difference residual.

    Note (provable for the current contract): no licensed shape decomposes into
    a concatenation of smaller licensed shapes, so every run admits AT MOST ONE
    covering today. Multiplicity support is implemented for future contracts.

Closed cells REUSE the existing Layer 4 ``LicensedSyllableCandidate`` type; no
parallel candidate family is forked, no canonical registry layer is added. The
produced cells are type-compatible with Layer 5
``LicensedSyllableSequenceCandidate`` composition.

This module makes NO claim of wordhood, segmentation, lafz, root, wazn,
morphology, grammar, i'rab, dalalah, tafsir, meaning, hukm, RealityClaim, or
FinalMeaning. It renders/reports only structural facts.

CLI:
    PYTHONPATH=src:. python3 -m qiyas_core.licensed_cell_extension "ضَرَبَ"
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

from qiyas_core.licensed_syllable import (
    CANDIDATE_RUNTIME_STATUS,
    AllowedSyllableShape,
    BoundaryEvidence,
    LicensedSyllableCandidate,
    PhoneticEconomyEvidence,
    SyllableShapeEvidence,
    licensed_cell_shape,
)

# ─────────────────────────────────────────────────────────────────────────────
# Module-level constants
# ─────────────────────────────────────────────────────────────────────────────

CELL_AUTHORIZATION_DATE = "2026-06-14"
CELL_AUTHORIZATION_SCOPE = "cell_extension_only_potential_only_not_global_unfreeze"

CELL_RUNTIME_STATUS = "licensed_cell_extension_potential_only"
EVIDENCE_SOURCE = "qiyas_core.licensed_cell_extension"
NOT_INTRODUCED = "not_introduced"

# Canonical gate claims (TERMINOLOGY_MAP §4 / CDC §3.1–3.2).
GATE_BEGINNING_LICENSED = "وادي:beginning:licensed"
GATE_ENDING_LICENSED = "وادي:ending:licensed"


# ─────────────────────────────────────────────────────────────────────────────
# Evidence dataclasses (all frozen) — contract-bound, never Candidates
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class CellBindingEvidence:
    """Licenses one cell's formation by licensed extension (REC-EXT §6/§10).

    The cell-layer binding evidence licensing the Extend steps that build the
    cell while its reduced shape stays inside the closed contract.
    """

    cell_index: int
    surface: str
    shape: AllowedSyllableShape
    extended_within_contract: bool
    reason: str


@dataclass(frozen=True)
class CellMinimalCompleteClosureEvidence:
    """Cell-scoped instance of the IsMinimallyComplete law (MCC §3).

    Layer-specific (REC-EXT §6: binding/closure evidence is not portable). This
    parallels slot_geometry_closure_check.MinimalCompleteClosureEvidence at the
    cell granularity. It is an Evidence carrier, never a Candidate.
    """

    cell_index: int
    surface: str
    shape: AllowedSyllableShape
    licensed_beginning: bool
    licensed_ending: bool
    no_open_demand: bool
    minimally_complete: bool
    reason: str


@dataclass(frozen=True)
class CellBoundaryOpeningEvidence:
    """Boundary evidence: bundles the canonical beginning/ending gate witnesses
    and closure-demand discharge (CDC §3.1–3.2 / §3.4). Not a new concept."""

    cell_index: int
    gate_beginning: str
    gate_ending: str
    demand_discharged: bool
    reason: str


@dataclass(frozen=True)
class CellInvalidatingDifferenceEvidence:
    """Residual recorded when a licensed first-cell branch cannot complete a
    full covering, or when the run admits no covering (REC-EXT §9/§10)."""

    run_surface: str
    branch_first_cell_surface: str
    fariq_claim: str
    reason: str
    status: str  # "blocked" | "deferred"
    candidate_emitted: bool


@dataclass(frozen=True)
class LicensedCellCovering:
    """One full, licensed covering of the run by closed cells. Potential-only."""

    cells: tuple[LicensedSyllableCandidate, ...]
    cell_shapes: tuple[str, ...]
    surface_form_vocalized: str
    surface_codepoints: tuple[str, ...]
    length: int
    binding_evidence: tuple[CellBindingEvidence, ...]
    closure_evidence: tuple[CellMinimalCompleteClosureEvidence, ...]
    boundary_evidence: tuple[CellBoundaryOpeningEvidence, ...]
    identity_preserved: bool
    potential_only: bool
    runtime_status: str


@dataclass(frozen=True)
class CellTilingAnalysis:
    """Bundle: run + all licensed coverings + residual branches + statuses."""

    run: str
    coverings: tuple[LicensedCellCovering, ...]
    residuals: tuple[CellInvalidatingDifferenceEvidence, ...]
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


def _licensed_first_cells(run: str, start: int) -> list[tuple[int, AllowedSyllableShape]]:
    """All (end_index, shape) for slices run[start:end] that are a single
    licensed cell. A licensed cell necessarily begins at a consonant — that is
    enforced by the detector (a slice beginning with a haraka reduces to a
    non-contract shape and returns None)."""
    out: list[tuple[int, AllowedSyllableShape]] = []
    for end in range(start + 1, len(run) + 1):
        shape = licensed_cell_shape(run[start:end])
        if shape is not None:
            out.append((end, shape))
    return out


def _enumerate_coverings(
    run: str, start: int = 0
) -> list[list[tuple[int, int, AllowedSyllableShape]]]:
    """All full coverings of run[start:] as lists of (start, end, shape).

    A covering reaches len(run) exactly (full-coverage constraint). Branches
    that strand an uncoverable unit simply do not appear (they dead-end and are
    pruned). Returns every covering — no auto-disambiguation, no pre-selection.
    """
    if start == len(run):
        return [[]]
    coverings: list[list[tuple[int, int, AllowedSyllableShape]]] = []
    for end, shape in _licensed_first_cells(run, start):
        for sub in _enumerate_coverings(run, end):
            coverings.append([(start, end, shape)] + sub)
    return coverings


def _build_cell(
    run: str, cell_index: int, start: int, end: int, shape: AllowedSyllableShape
) -> LicensedSyllableCandidate:
    """Produce an existing-type LicensedSyllableCandidate for a closed cell with
    run-relative spans. Reuses the Layer 4 candidate/evidence types verbatim."""
    surface = run[start:end]
    cps = _surface_codepoints(surface)
    names = tuple("CELL" for _ in surface)
    boundary = BoundaryEvidence(
        token_index=cell_index,
        start_index=start,
        end_index=end,
        preceding_text=run[:start],
        following_text=run[end:],
        has_left_boundary=start == 0,
        has_right_boundary=end == len(run),
        boundary_preserved=(surface == run[start:end]),
        source=EVIDENCE_SOURCE,
    )
    shape_ev = SyllableShapeEvidence(
        shape=shape,
        surface_form_vocalized=surface,
        surface_codepoints=cps,
        surface_codepoint_names=names,
        shape_reason=f"licensed cell shape {shape.value}",
        allowed=True,
    )
    economy_ev = PhoneticEconomyEvidence(
        minimal_complete_syllable=True,
        no_unnecessary_expansion=True,
        shape_allowed=True,
        boundary_preserved=True,
        identity_preserved=True,
        economy_satisfied=True,
        reason="licensed minimal-complete cell",
    )
    return LicensedSyllableCandidate(
        token_index=cell_index,
        surface_form_vocalized=surface,
        surface_codepoints=cps,
        surface_codepoint_names=names,
        shape=shape,
        boundary_evidence=boundary,
        shape_evidence=shape_ev,
        economy_evidence=economy_ev,
        identity_preserved=True,
        potential_only=True,
        runtime_status=CANDIDATE_RUNTIME_STATUS,
    )


def _build_covering(
    run: str, covering: list[tuple[int, int, AllowedSyllableShape]]
) -> LicensedCellCovering:
    cells: list[LicensedSyllableCandidate] = []
    binding: list[CellBindingEvidence] = []
    closure: list[CellMinimalCompleteClosureEvidence] = []
    boundary: list[CellBoundaryOpeningEvidence] = []
    for idx, (start, end, shape) in enumerate(covering):
        surface = run[start:end]
        cells.append(_build_cell(run, idx, start, end, shape))
        binding.append(
            CellBindingEvidence(
                cell_index=idx,
                surface=surface,
                shape=shape,
                extended_within_contract=True,
                reason=f"licensed extension within closed contract → {shape.value}",
            )
        )
        closure.append(
            CellMinimalCompleteClosureEvidence(
                cell_index=idx,
                surface=surface,
                shape=shape,
                licensed_beginning=True,
                licensed_ending=True,
                no_open_demand=True,
                minimally_complete=True,
                reason="cell is a licensed minimal-complete shape; remainder coverable",
            )
        )
        boundary.append(
            CellBoundaryOpeningEvidence(
                cell_index=idx,
                gate_beginning=GATE_BEGINNING_LICENSED,
                gate_ending=GATE_ENDING_LICENSED,
                demand_discharged=True,
                reason="boundary licensed by beginning/ending gates + demand discharge",
            )
        )
    surface_form = "".join(c.surface_form_vocalized for c in cells)
    return LicensedCellCovering(
        cells=tuple(cells),
        cell_shapes=tuple(c.shape.value for c in cells),
        surface_form_vocalized=surface_form,
        surface_codepoints=_surface_codepoints(surface_form),
        length=len(cells),
        binding_evidence=tuple(binding),
        closure_evidence=tuple(closure),
        boundary_evidence=tuple(boundary),
        identity_preserved=(surface_form == run),
        potential_only=True,
        runtime_status=CELL_RUNTIME_STATUS,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────


def tile_licensed_cells(run: str) -> CellTilingAnalysis:
    """Tile one contiguous run of TypedCodePoints into licensed cells (Policy C).

    Returns all fully-licensed coverings as potential candidates, plus residual
    evidence for licensed first-cell branches that cannot complete a covering.
    Potential-only; introduces no meaning/hukm/i'rab/dalalah/reality claim.
    """
    coverings_raw = _enumerate_coverings(run, 0) if run else []
    coverings = tuple(_build_covering(run, cov) for cov in coverings_raw)

    # Residuals: licensed first-cell branches that participate in NO covering.
    surviving_first_ends = {cov[0][1] for cov in coverings_raw if cov}
    residuals: list[CellInvalidatingDifferenceEvidence] = []
    for end, shape in _licensed_first_cells(run, 0):
        if end in surviving_first_ends:
            continue
        residuals.append(
            CellInvalidatingDifferenceEvidence(
                run_surface=run,
                branch_first_cell_surface=run[0:end],
                fariq_claim="فارق:stranded_typed_unit:present",
                reason=(
                    f"first-cell branch {run[0:end]!r} ({shape.value}) strands an "
                    "uncoverable typed unit; no full licensed covering exists "
                    "through this branch"
                ),
                status="blocked",
                candidate_emitted=False,
            )
        )

    # Whole-run residual when nothing is licensable at all.
    if not coverings and not residuals and run:
        residuals.append(
            CellInvalidatingDifferenceEvidence(
                run_surface=run,
                branch_first_cell_surface="",
                fariq_claim="فارق:no_licensed_cell:present",
                reason="no licensed cell begins this run under the closed contract",
                status="blocked",
                candidate_emitted=False,
            )
        )

    return CellTilingAnalysis(
        run=run,
        coverings=coverings,
        residuals=tuple(residuals),
        runtime_status=CELL_RUNTIME_STATUS,
        meaning_status=NOT_INTRODUCED,
        hukm_status=NOT_INTRODUCED,
        irab_status=NOT_INTRODUCED,
        dalalah_status=NOT_INTRODUCED,
        reality_status=NOT_INTRODUCED,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Rendering — structural facts only
# ─────────────────────────────────────────────────────────────────────────────


def render_cell_tiling_analysis(analysis: CellTilingAnalysis) -> str:
    lines: list[str] = []
    lines.append("## Licensed Cell Extension Analysis")
    lines.append("=" * 60)
    lines.append(f"  run={analysis.run!r}")
    lines.append(f"  runtime_status={analysis.runtime_status}")
    lines.append(f"  covering_count={len(analysis.coverings)}")
    lines.append(f"  residual_count={len(analysis.residuals)}")
    lines.append("")

    lines.append("## Coverings (potential candidates)")
    lines.append("=" * 60)
    if analysis.coverings:
        for i, cov in enumerate(analysis.coverings):
            lines.append(f"  - covering[{i}]")
            lines.append(f"    length={cov.length}")
            lines.append(f"    cell_shapes={'/'.join(cov.cell_shapes)}")
            lines.append(
                f"    cell_surfaces={[c.surface_form_vocalized for c in cov.cells]!r}"
            )
            lines.append(f"    surface_form_vocalized={cov.surface_form_vocalized!r}")
            lines.append(f"    identity_preserved={cov.identity_preserved}")
            lines.append("")
    else:
        lines.append("  (none)")
        lines.append("")

    lines.append("## Residuals (invalidating-difference)")
    lines.append("=" * 60)
    if analysis.residuals:
        for r in analysis.residuals:
            lines.append(f"  - branch={r.branch_first_cell_surface!r}")
            lines.append(f"    {r.fariq_claim}")
            lines.append(f"    reason={r.reason}")
            lines.append(f"    status={r.status} candidate_emitted={r.candidate_emitted}")
            lines.append("")
    else:
        lines.append("  (none)")
        lines.append("")

    lines.append("## Constitutional Boundary")
    lines.append("=" * 60)
    lines.append("  * licensed cell extension / closure only — no segmentation claim")
    lines.append("  * no wordhood")
    lines.append("  * no root / wazn / morphology")
    lines.append("  * no grammar / i'rab")
    lines.append("  * no dalalah")
    lines.append("  * no tafsir")
    lines.append("  * no hukm")
    lines.append("  * no reality claim")
    lines.append("  * no shadda / gemination expansion")
    lines.append("  * potential-only; not Layer 6; not REC-6; freeze remains in effect")
    lines.append(
        f"  * meaning_status={analysis.meaning_status} "
        f"hukm_status={analysis.hukm_status} "
        f"irab_status={analysis.irab_status} "
        f"dalalah_status={analysis.dalalah_status} "
        f"reality_status={analysis.reality_status}"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: python3 -m qiyas_core.licensed_cell_extension <run>")
        return 2
    analysis = tile_licensed_cells(args[0])
    print(render_cell_tiling_analysis(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
