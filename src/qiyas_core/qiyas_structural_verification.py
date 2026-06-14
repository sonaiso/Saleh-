"""Unified structural verification — the in-repo authoritative public verifier.

Authorization:
    Narrow per-layer authorization (2026-06-14). This module unifies the public
    structural verification path so that a licensed shadda expansion, when it
    exists and its expanded trace is covered, is consumed BEFORE the final
    public covering report. The direct single-cell Layer 4 result is retained
    only as a labeled diagnostic and never overrides the licensed shadda path.

    Potential-only and READ-ONLY over the existing layers. It adds no new
    analysis logic, no new cell shape, and no semantics. It does NOT modify
    Layer 4, Layer 5, cell-extension, or shadda-expansion. NOT Layer 6, NOT
    REC-6, NOT a global freeze lift.

Pipeline (minimal official order):
    analysis_trace identity (surface + codepoints, identity preserved)
      -> licensed_shadda_expansion evidence, if U+0651 present
      -> licensed_cell_extension covering on (expanded trace if shadda else original)
      -> Layer 5 sequence if applicable
      -> final public structural status

Structural statuses (structural ONLY — not meaning/hukm/i'rab/dalalah/tafsir):
    covered_direct                 the original surface tiles into licensed cells
    covered_via_shadda_expansion   the licensed shadda-expanded trace tiles
    residual                       neither path covers (diagnostics preserved)

CLI:
    PYTHONPATH=src:. python3 -m qiyas_core.qiyas_structural_verification "شَاذّ عَدَّ بَيت"
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional

from qiyas_core.licensed_syllable import (
    SHADDA,
    SHORT_VOWELS,
    analyze_licensed_syllables,
)
from qiyas_core.licensed_cell_extension import tile_licensed_cells
from qiyas_core.licensed_shadda_expansion import expand_shadda
from qiyas_core.licensed_syllable_sequence import compose_syllable_sequence

STRUCTURAL_RUNTIME_STATUS = "structural_verification_potential_only"
NOT_INTRODUCED = "not_introduced"

# Structural status constants (structural only — never semantic).
COVERED_DIRECT = "covered_direct"
COVERED_VIA_SHADDA_EXPANSION = "covered_via_shadda_expansion"
RESIDUAL = "residual"


@dataclass(frozen=True)
class StructuralVerification:
    """Authoritative structural verification of a single token surface."""

    identity_surface: str
    identity_codepoints: tuple[str, ...]
    shadda_present: bool

    # Direct path (cell-extension on the original surface).
    direct_covering_shapes: tuple[tuple[str, ...], ...]
    direct_residual_count: int

    # Direct single-cell Layer 4 — diagnostic only, never the final status.
    direct_layer4_diagnostic_status: str
    direct_layer4_diagnostic_reason: str

    # Licensed shadda path.
    shadda_expansion_trace: Optional[str]
    shadda_expansion_covering_shapes: tuple[tuple[str, ...], ...]
    shadda_residual_count: int
    vowel_invented: bool

    # Layer 5 sequence (optional, informational) — lengths of composed sequences.
    layer5_sequence_lengths: tuple[int, ...]

    final_status: str
    identity_preserved: bool

    runtime_status: str = STRUCTURAL_RUNTIME_STATUS
    meaning_status: str = NOT_INTRODUCED
    hukm_status: str = NOT_INTRODUCED
    irab_status: str = NOT_INTRODUCED
    dalalah_status: str = NOT_INTRODUCED
    reality_status: str = NOT_INTRODUCED


def _codepoints(surface: str) -> tuple[str, ...]:
    return tuple(f"U+{ord(c):04X}" for c in surface)


def _short_vowels(surface: str) -> list[str]:
    return sorted(c for c in surface if c in SHORT_VOWELS)


def _direct_layer4_diagnostic(surface: str) -> tuple[str, str]:
    """Single-cell Layer 4 observation — diagnostic only."""
    la = analyze_licensed_syllables(surface)
    if la.candidates:
        return "covered_single_cell", (
            f"single licensed cell {la.candidates[0].shape.value}"
        )
    if la.invalidations:
        reason = la.invalidations[0].reason
        if "shadda" in reason:
            return "invalid_direct_shadda_unsupported", reason
        return "invalid_direct", reason
    return "invalid_direct", "no single-cell candidate emitted"


def verify_token_structure(surface: str) -> StructuralVerification:
    """Authoritative structural verification of one contiguous token surface.

    The original surface is the identity carrier and is never replaced. The
    direct single-cell Layer 4 result is a labeled diagnostic only; if a
    licensed shadda expansion exists and its expanded trace is covered, the
    final status is ``covered_via_shadda_expansion``. Potential-only; no
    meaning / hukm / i'rab / dalalah / reality claim is introduced.
    """
    identity_codepoints = _codepoints(surface)
    shadda_present = SHADDA in surface

    # --- direct path: cell-extension on the ORIGINAL surface ---
    direct = tile_licensed_cells(surface)
    direct_shapes = tuple(cov.cell_shapes for cov in direct.coverings)

    # --- direct single-cell Layer 4 diagnostic (informational only) ---
    diag_status, diag_reason = _direct_layer4_diagnostic(surface)

    # --- licensed shadda path ---
    expansion_trace: Optional[str] = None
    shadda_shapes: tuple[tuple[str, ...], ...] = ()
    shadda_residual_count = 0
    vowel_invented = False
    shadda_cov = None
    if shadda_present:
        sh = expand_shadda(surface)
        if sh.evidence is not None:
            expansion_trace = sh.evidence.trace.expanded_form
            # authoritative vowel-invention test: short-vowel multiset unchanged
            vowel_invented = _short_vowels(expansion_trace) != _short_vowels(surface)
            shadda_cov = tile_licensed_cells(expansion_trace)
            shadda_shapes = tuple(cov.cell_shapes for cov in shadda_cov.coverings)
            shadda_residual_count = len(shadda_cov.residuals)
        else:
            shadda_residual_count = len(sh.residuals)

    # --- final status decision (shadda path consulted before declaring residual) ---
    if direct.coverings:
        final_status = COVERED_DIRECT
        chosen_coverings = direct.coverings
    elif shadda_present and shadda_shapes:
        final_status = COVERED_VIA_SHADDA_EXPANSION
        chosen_coverings = shadda_cov.coverings
    else:
        final_status = RESIDUAL
        chosen_coverings = ()

    # --- Layer 5 sequence (optional, informational) ---
    layer5_lengths: list[int] = []
    for cov in chosen_coverings:
        candidate, _inv = compose_syllable_sequence(cov.cells)
        if candidate is not None:
            layer5_lengths.append(candidate.length)

    return StructuralVerification(
        identity_surface=surface,
        identity_codepoints=identity_codepoints,
        shadda_present=shadda_present,
        direct_covering_shapes=direct_shapes,
        direct_residual_count=len(direct.residuals),
        direct_layer4_diagnostic_status=diag_status,
        direct_layer4_diagnostic_reason=diag_reason,
        shadda_expansion_trace=expansion_trace,
        shadda_expansion_covering_shapes=shadda_shapes,
        shadda_residual_count=shadda_residual_count,
        vowel_invented=vowel_invented,
        layer5_sequence_lengths=tuple(layer5_lengths),
        final_status=final_status,
        identity_preserved=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Rendering — terminal-visible, structural facts only
# ─────────────────────────────────────────────────────────────────────────────


def render_structural_verification(v: StructuralVerification) -> str:
    lines: list[str] = []
    lines.append("## Structural Verification")
    lines.append("=" * 60)
    lines.append(f"  identity_surface={v.identity_surface!r}")
    lines.append(f"  identity_codepoints={','.join(v.identity_codepoints)}")
    lines.append(f"  shadda_present={v.shadda_present}  (U+0651 in identity={'U+0651' in v.identity_codepoints})")
    lines.append("")
    lines.append("  DIRECT_LAYER4_DIAGNOSTIC:")
    lines.append(f"    status={v.direct_layer4_diagnostic_status}")
    lines.append(f"    reason={v.direct_layer4_diagnostic_reason}")
    lines.append(f"    note=diagnostic only; does not set the final public status")
    lines.append("")
    if v.shadda_present:
        lines.append("  LICENSED_SHADDA_PATH:")
        lines.append(f"    expansion={v.shadda_expansion_trace!r}")
        lines.append(
            "    covering="
            + (
                "; ".join("/".join(s) for s in v.shadda_expansion_covering_shapes)
                or "(none)"
            )
        )
        lines.append(f"    vowel_invented={v.vowel_invented}")
        lines.append("")
    lines.append("  DIRECT_PATH (cell-extension on original surface):")
    lines.append(
        "    covering="
        + ("; ".join("/".join(s) for s in v.direct_covering_shapes) or "(none)")
    )
    lines.append("")
    lines.append(f"  final_status={v.final_status}")
    lines.append(f"  identity_preserved={v.identity_preserved}")
    lines.append(f"  layer5_sequence_lengths={v.layer5_sequence_lengths}")
    lines.append(f"  runtime_status={v.runtime_status}")
    lines.append(
        f"  meaning_status={v.meaning_status} hukm_status={v.hukm_status} "
        f"irab_status={v.irab_status} dalalah_status={v.dalalah_status} "
        f"reality_status={v.reality_status}"
    )
    return "\n".join(lines)


def verify_text(text: str) -> tuple[StructuralVerification, ...]:
    """Verify each whitespace-delimited token of `text` (read-only)."""
    return tuple(verify_token_structure(tok) for tok in text.split())


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: python3 -m qiyas_core.qiyas_structural_verification <text>")
        return 2
    for v in verify_text(args[0]):
        print(render_structural_verification(v))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
