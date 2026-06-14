"""Licensed shadda expansion — codepoint-faithful evidence layer (potential-only).

Authorization:
    Narrow per-layer authorization (2026-06-14). Maintainer Hussein Hiyassat
    ratified a codepoint-faithful shadda expansion EVIDENCE layer. NOT Layer 6,
    NOT REC-6, NOT a global freeze lift, NOT morphology/grammar/meaning, NOT a
    semantic runtime.

Ratified rule (a shadda is not a haraka, not a vowel, not meaning — it licenses
consonant doubling only):

    Cّ with explicit carried vowel V  ->  Cْ + C V     (V reused, never invented)
    Cّ with no explicit carried vowel ->  Cْ + C       (bare second consonant)

Therefore:
    عَدَّ  ->  عَدْدَ      (carried fatha reused)
    شَاذّ  ->  شَاذْذ      (bare; NO final fatha invented — NOT شَاذْذَ)

Hard identity rule:
    The original ``surface_form_vocalized`` remains the identity carrier and is
    never replaced. The original shadda codepoint (U+0651) is retained in the
    original codepoints. The expanded form is ADDITIVE trace/evidence only.

This layer emits EVIDENCE (a trace), never a candidate. It does not itself
decide cell coverage; an additive hook ``cover_expanded_trace`` may feed the
expanded trace to the existing licensed cell-extension runtime where the caller
chooses. The layer never forces a surface to become a valid candidate.

Constitutional note (honest coverage consequence):
    Under the current closed six-shape contract {CV, CVV, CVC, CVVC, CVCC,
    CVVCC}, the bare expansion ``شَاذْذ`` reduces to ``CVVCC`` — a licensed
    shape — so cell-extension covers it as a single CVVCC cell. A bare final
    consonant is a permitted syllable coda (as in قَالْتْ). This layer reports
    that honestly; it does not invent a vowel and does not change the contract.

CLI:
    PYTHONPATH=src:. python3 -m qiyas_core.licensed_shadda_expansion "عَدَّ"
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

from qiyas_core.licensed_syllable import (
    DAMMA,
    FATHA,
    KASRA,
    SHADDA,
    SHORT_VOWELS,
    SUKUN,
)

SHADDA_AUTHORIZATION_DATE = "2026-06-14"
SHADDA_RUNTIME_STATUS = "licensed_shadda_expansion_potential_only"
EVIDENCE_SOURCE = "qiyas_core.licensed_shadda_expansion"
NOT_INTRODUCED = "not_introduced"


def _is_arabic_consonant(ch: str) -> bool:
    return bool(ch) and 0x0621 <= ord(ch) <= 0x064A and ch not in SHORT_VOWELS


def _cps(surface: str) -> tuple[str, ...]:
    return tuple(f"U+{ord(c):04X}" for c in surface)


# ─────────────────────────────────────────────────────────────────────────────
# Evidence dataclasses (frozen) — trace/evidence only, never Candidates
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ShaddaExpansionTrace:
    """The additive expansion trace. The original is preserved separately."""

    original_surface: str
    original_codepoints: tuple[str, ...]
    expanded_form: str
    expanded_codepoints: tuple[str, ...]
    # Per shadda site, in order:
    site_base_consonants: tuple[str, ...]
    site_carried_vowels: tuple[Optional[str], ...]
    site_bare: tuple[bool, ...]
    # expanded index -> original index (or -1 for inserted sukun / duplicated C)
    index_map: tuple[int, ...]


@dataclass(frozen=True)
class LicensedShaddaExpansionEvidence:
    """Licensed shadda expansion evidence for a surface carrying >=1 shadda."""

    surface_form_vocalized: str          # the identity carrier (unchanged)
    trace: ShaddaExpansionTrace
    final_consonant_bare: bool           # any site expanded bare (no carried vowel)
    identity_preserved: bool
    shadda_retained_in_identity: bool
    reason: str
    source: str
    potential_only: bool
    runtime_status: str


@dataclass(frozen=True)
class ShaddaExpansionResidual:
    """Recorded reason a shadda could not be licensed for expansion."""

    surface_form_vocalized: str
    reason: str
    fariq_claim: str
    status: str            # "blocked" | "deferred"
    candidate_emitted: bool


@dataclass(frozen=True)
class ShaddaExpansionAnalysis:
    """Bundle: original + (optional) expansion evidence + residuals + statuses."""

    original_surface: str
    had_shadda: bool
    evidence: Optional[LicensedShaddaExpansionEvidence]
    residuals: tuple[ShaddaExpansionResidual, ...]
    runtime_status: str
    meaning_status: str
    hukm_status: str
    irab_status: str
    dalalah_status: str
    reality_status: str


# ─────────────────────────────────────────────────────────────────────────────
# Core expansion — codepoint-faithful, no vowel invention, no source replacement
# ─────────────────────────────────────────────────────────────────────────────


def _vowel_name(ch: str) -> str:
    return {FATHA: "fatha", DAMMA: "damma", KASRA: "kasra"}.get(ch, "unknown")


def expand_shadda(surface: str) -> ShaddaExpansionAnalysis:
    """Produce the codepoint-faithful expansion trace for `surface`.

    Walks the codepoints; at each shadda it doubles the base consonant:
      * base consonant immediately preceded by a short haraka V  →  C sukun C V
        (the existing V is reused on the second copy; NEVER invented)
      * base consonant with no preceding haraka                  →  C sukun C
        (bare; no vowel added)
    The original surface is returned unchanged (identity carrier); the shadda
    codepoint stays in the original codepoints; the expanded form is additive.
    """
    original_cps = _cps(surface)
    had_shadda = SHADDA in surface

    out: list[str] = []          # expanded codepoints
    omap: list[int] = []         # expanded index -> original index (-1 = inserted)
    base_consonants: list[str] = []
    carried_vowels: list[Optional[str]] = []
    bare_sites: list[bool] = []
    residuals: list[ShaddaExpansionResidual] = []

    for i, ch in enumerate(surface):
        if ch != SHADDA:
            out.append(ch)
            omap.append(i)
            continue

        # Shadda site. The base consonant is the last emitted consonant; a short
        # haraka may sit between it and the shadda (the carried vowel).
        if out and out[-1] in SHORT_VOWELS:
            carried = out[-1]
            base = out[-2] if len(out) >= 2 else ""
            if not _is_arabic_consonant(base):
                residuals.append(
                    ShaddaExpansionResidual(
                        surface_form_vocalized=surface,
                        reason="shadda has a carried vowel but no base consonant",
                        fariq_claim="فارق:shadda_without_base_consonant:present",
                        status="blocked",
                        candidate_emitted=False,
                    )
                )
                continue
            # Reuse the carried vowel on the second copy: ...C V shadda -> C sukun C V
            popped_vowel = out.pop()
            popped_idx = omap.pop()
            out.append(SUKUN)
            omap.append(-1)
            out.append(base)
            omap.append(-1)
            out.append(popped_vowel)
            omap.append(popped_idx)
            base_consonants.append(base)
            carried_vowels.append(_vowel_name(carried))
            bare_sites.append(False)
        elif out and _is_arabic_consonant(out[-1]):
            base = out[-1]
            # Bare doubling: ...C shadda -> C sukun C  (no vowel invented)
            out.append(SUKUN)
            omap.append(-1)
            out.append(base)
            omap.append(-1)
            base_consonants.append(base)
            carried_vowels.append(None)
            bare_sites.append(True)
        else:
            residuals.append(
                ShaddaExpansionResidual(
                    surface_form_vocalized=surface,
                    reason="shadda has no preceding base consonant",
                    fariq_claim="فارق:shadda_without_base_consonant:present",
                    status="blocked",
                    candidate_emitted=False,
                )
            )
            continue

    evidence: Optional[LicensedShaddaExpansionEvidence] = None
    if base_consonants:  # at least one licensed shadda site expanded
        expanded_form = "".join(out)
        trace = ShaddaExpansionTrace(
            original_surface=surface,
            original_codepoints=original_cps,
            expanded_form=expanded_form,
            expanded_codepoints=_cps(expanded_form),
            site_base_consonants=tuple(base_consonants),
            site_carried_vowels=tuple(carried_vowels),
            site_bare=tuple(bare_sites),
            index_map=tuple(omap),
        )
        evidence = LicensedShaddaExpansionEvidence(
            surface_form_vocalized=surface,
            trace=trace,
            final_consonant_bare=any(bare_sites),
            identity_preserved=True,
            shadda_retained_in_identity=(SHADDA in surface),
            reason="codepoint-faithful consonant doubling; no vowel invented",
            source=EVIDENCE_SOURCE,
            potential_only=True,
            runtime_status=SHADDA_RUNTIME_STATUS,
        )

    return ShaddaExpansionAnalysis(
        original_surface=surface,
        had_shadda=had_shadda,
        evidence=evidence,
        residuals=tuple(residuals),
        runtime_status=SHADDA_RUNTIME_STATUS,
        meaning_status=NOT_INTRODUCED,
        hukm_status=NOT_INTRODUCED,
        irab_status=NOT_INTRODUCED,
        dalalah_status=NOT_INTRODUCED,
        reality_status=NOT_INTRODUCED,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Additive integration hook with licensed cell extension (optional)
# ─────────────────────────────────────────────────────────────────────────────


def cover_expanded_trace(evidence: LicensedShaddaExpansionEvidence):
    """Optional additive hook: feed the expanded trace to the existing licensed
    cell-extension runtime. Returns its CellTilingAnalysis verbatim. This layer
    makes no covering claim of its own; coverage is the cell-extension's result.
    """
    from qiyas_core.licensed_cell_extension import tile_licensed_cells

    return tile_licensed_cells(evidence.trace.expanded_form)


# ─────────────────────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────────────────────


def render_shadda_expansion_analysis(analysis: ShaddaExpansionAnalysis) -> str:
    lines: list[str] = []
    lines.append("## Licensed Shadda Expansion Analysis")
    lines.append("=" * 60)
    lines.append(f"  original_surface={analysis.original_surface!r}  (identity carrier)")
    lines.append(f"  had_shadda={analysis.had_shadda}")
    lines.append(f"  runtime_status={analysis.runtime_status}")
    lines.append("")
    if analysis.evidence is not None:
        t = analysis.evidence.trace
        lines.append("## Expansion Trace (additive evidence only)")
        lines.append("=" * 60)
        lines.append(f"  expanded_form={t.expanded_form!r}")
        lines.append(f"  base_consonants={t.site_base_consonants!r}")
        lines.append(f"  carried_vowels={t.site_carried_vowels!r}")
        lines.append(f"  site_bare={t.site_bare!r}")
        lines.append(f"  final_consonant_bare={analysis.evidence.final_consonant_bare}")
        lines.append(f"  identity_preserved={analysis.evidence.identity_preserved}")
        lines.append(
            f"  shadda_retained_in_identity="
            f"{analysis.evidence.shadda_retained_in_identity}"
        )
        lines.append("")
    if analysis.residuals:
        lines.append("## Residuals")
        lines.append("=" * 60)
        for r in analysis.residuals:
            lines.append(f"  - {r.fariq_claim}  ({r.reason})")
        lines.append("")
    lines.append("## Constitutional Boundary")
    lines.append("=" * 60)
    lines.append("  * shadda licenses consonant doubling only — not a haraka, not meaning")
    lines.append("  * no vowel invented; no source replacement; shadda retained in identity")
    lines.append("  * expansion is additive trace/evidence; emits no candidate")
    lines.append("  * no morphology / grammar / hukm / i'rab / dalalah / tafsir / meaning")
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
        print("usage: python3 -m qiyas_core.licensed_shadda_expansion <surface>")
        return 2
    print(render_shadda_expansion_analysis(expand_shadda(args[0])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
