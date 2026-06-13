"""Layer 4 LicensedSyllableCandidate runtime — potential-only.

Authorization:
    Narrow Layer 4 authorization (2026-06-13). Maintainer Hussein Hiyassat
    explicitly authorized this module as a potential-only runtime slice,
    ahead of the full REC-1…REC-5 sequence. This is a single-layer narrow
    authorization, not a global runtime unfreeze. No Layer 5, no semantic
    runtime, no meaning/hukm/i'rab/dalalah/reality claim.

Constitutional boundary:
    - runtime_status     = "layer4_potential_only"
    - meaning_status     = "not_introduced"
    - hukm_status        = "not_introduced"
    - irab_status        = "not_introduced"
    - reality_status     = "not_introduced"
    - candidate.runtime  = "potential_only_not_semantic_runtime"

The module consumes lower-layer evidence from qiyas_core.analysis_trace
(PRs #128 / #130 / #131 / #132). It does not mutate that evidence and does
not rewrite MIU statuses.

Allowed syllable shapes (closed contract):
    CV, CVC, CVV, CVVC, CVVCC. No other shape is valid. Any unsupported
    surface emits SyllableInvalidationEvidence; no candidate is emitted
    for it.

Public surface:
    AllowedSyllableShape
    BoundaryEvidence
    SyllableShapeEvidence
    PhoneticEconomyEvidence
    SyllableInvalidationEvidence
    LicensedSyllableCandidate
    LicensedSyllableAnalysis
    analyze_licensed_syllables(text)         -> LicensedSyllableAnalysis
    render_licensed_syllable_analysis(a)     -> str

CLI:
    PYTHONPATH=src:. python3 -m qiyas_core.licensed_syllable "بِ ضَ وَ يَ ضَرَبَ"
"""

from __future__ import annotations

import sys
import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from qiyas_core.analysis_trace import (
    QiyasAnalysisTrace,
    TokenAnalysisTrace,
    analyze_potential_trace,
)

# ─────────────────────────────────────────────────────────────────────────────
# Module-level constants
# ─────────────────────────────────────────────────────────────────────────────

LAYER4_AUTHORIZATION_DATE = "2026-06-13"
LAYER4_AUTHORIZATION_SCOPE = "layer4_only_potential_only_not_global_unfreeze"

LAYER4_RUNTIME_STATUS = "layer4_potential_only"
CANDIDATE_RUNTIME_STATUS = "potential_only_not_semantic_runtime"
EVIDENCE_SOURCE = "qiyas_core.analysis_trace"
NOT_INTRODUCED = "not_introduced"

# Arabic vowel marks
FATHA = "َ"
DAMMA = "ُ"
KASRA = "ِ"
SUKUN = "ْ"
SHADDA = "ّ"

SHORT_VOWELS = (FATHA, DAMMA, KASRA)

# Arabic long-vowel letters
ALEF = "ا"
WAW = "و"
YEH = "ي"
ALEF_MAKSURA = "ى"

LONG_VOWEL_LETTERS = (ALEF, WAW, YEH, ALEF_MAKSURA)

# Short-vowel + long-letter pairs that form a true long vowel
LONG_VOWEL_PAIRS = {
    (FATHA, ALEF): "long_fatha_alef",
    (FATHA, ALEF_MAKSURA): "long_fatha_alef_maksura",
    (DAMMA, WAW): "long_damma_waw",
    (KASRA, YEH): "long_kasra_yeh",
}


# ─────────────────────────────────────────────────────────────────────────────
# AllowedSyllableShape — closed contract
# ─────────────────────────────────────────────────────────────────────────────


class AllowedSyllableShape(Enum):
    CV = "CV"
    CVC = "CVC"
    CVV = "CVV"
    CVVC = "CVVC"
    CVVCC = "CVVCC"


ALLOWED_SYLLABLE_SHAPES: tuple[AllowedSyllableShape, ...] = (
    AllowedSyllableShape.CV,
    AllowedSyllableShape.CVC,
    AllowedSyllableShape.CVV,
    AllowedSyllableShape.CVVC,
    AllowedSyllableShape.CVVCC,
)

_ALLOWED_CV_STRINGS = frozenset(s.value for s in ALLOWED_SYLLABLE_SHAPES)


# ─────────────────────────────────────────────────────────────────────────────
# Evidence dataclasses (all frozen)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class BoundaryEvidence:
    """Boundary evidence sourced from qiyas_core.analysis_trace token metadata."""

    token_index: int
    start_index: int
    end_index: int
    preceding_text: str
    following_text: str
    has_left_boundary: bool
    has_right_boundary: bool
    boundary_preserved: bool
    source: str


@dataclass(frozen=True)
class SyllableShapeEvidence:
    """Codepoint-pattern shape evidence. Classifies only codepoint patterns.

    Does not infer phonology, roots, wordhood, or grammar.
    """

    shape: Optional[AllowedSyllableShape]
    surface_form_vocalized: str
    surface_codepoints: tuple[str, ...]
    surface_codepoint_names: tuple[str, ...]
    shape_reason: str
    allowed: bool


@dataclass(frozen=True)
class PhoneticEconomyEvidence:
    """Economy evidence: shape allowed + boundary preserved + identity preserved.

    economy_satisfied is true iff all five conjunct conditions hold.
    """

    minimal_complete_syllable: bool
    no_unnecessary_expansion: bool
    shape_allowed: bool
    boundary_preserved: bool
    identity_preserved: bool
    economy_satisfied: bool
    reason: str


@dataclass(frozen=True)
class SyllableInvalidationEvidence:
    """Recorded reason a candidate was NOT emitted for a surface."""

    surface_form_vocalized: str
    reason: str
    unsupported_shape: Optional[str]
    boundary_preserved: bool
    identity_preserved: bool
    candidate_emitted: bool


@dataclass(frozen=True)
class LicensedSyllableCandidate:
    """Potential-only Layer 4 candidate; no semantic runtime claim is made."""

    token_index: int
    surface_form_vocalized: str
    surface_codepoints: tuple[str, ...]
    surface_codepoint_names: tuple[str, ...]
    shape: AllowedSyllableShape
    boundary_evidence: BoundaryEvidence
    shape_evidence: SyllableShapeEvidence
    economy_evidence: PhoneticEconomyEvidence
    identity_preserved: bool
    potential_only: bool
    runtime_status: str


@dataclass(frozen=True)
class LicensedSyllableAnalysis:
    """Bundle: input + trace summary + emitted candidates + invalidations."""

    input_text: str
    trace_summary: str
    candidates: tuple[LicensedSyllableCandidate, ...]
    invalidations: tuple[SyllableInvalidationEvidence, ...]
    allowed_shapes: tuple[AllowedSyllableShape, ...]
    runtime_status: str
    meaning_status: str
    hukm_status: str
    irab_status: str
    reality_status: str


# ─────────────────────────────────────────────────────────────────────────────
# Shape detection — codepoint-pattern only, no phonology beyond explicit rules
# ─────────────────────────────────────────────────────────────────────────────


def _is_arabic_letter_consonant(ch: str) -> bool:
    """True iff ch is in the Arabic letter block and not a haraka mark."""
    if not ch:
        return False
    cp = ord(ch)
    return 0x0621 <= cp <= 0x064A


def _classify_codepoint(ch: str) -> str:
    """Return a single-letter class for shape detection:

    v = short vowel mark         (FATHA / DAMMA / KASRA)
    s = sukun                    (closes preceding consonant)
    g = shadda (gemination)      (unsupported in initial Layer 4 detector)
    L = potentially long-vowel letter (ALEF / WAW / YEH / ALEF_MAKSURA)
    C = consonant                (other Arabic letter)
    ? = unsupported              (anything else)
    """
    if ch in SHORT_VOWELS:
        return "v"
    if ch == SUKUN:
        return "s"
    if ch == SHADDA:
        return "g"
    if ch in LONG_VOWEL_LETTERS:
        return "L"
    if _is_arabic_letter_consonant(ch):
        return "C"
    return "?"


def _detect_shape(surface: str) -> tuple[Optional[str], str]:
    """Detect CV/CVC/CVV/CVVC/CVVCC pattern in surface.

    Returns (cv_string_or_none, reason). cv_string is one of the five
    allowed shape strings, or None when the surface does not match the
    closed contract.

    The detector inspects codepoints only. It does not infer phonology
    beyond the explicit short-vowel/long-letter pairing rules, does not
    infer roots, does not infer wordhood, and does not infer grammar.
    """
    if not surface:
        return None, "empty surface"

    chars = list(surface)
    classes = [_classify_codepoint(c) for c in chars]

    # Reject any unsupported codepoint outright.
    if "?" in classes:
        idx = classes.index("?")
        return None, (
            f"unsupported codepoint at index {idx}: "
            f"U+{ord(chars[idx]):04X}"
        )

    # Reject shadda in the initial detector — gemination is out of scope
    # for the closed contract of CV/CVC/CVV/CVVC/CVVCC.
    if "g" in classes:
        idx = classes.index("g")
        return None, (
            f"shadda (gemination) at index {idx} is unsupported "
            "in the initial Layer 4 shape detector"
        )

    reduced: list[str] = []
    i = 0
    n = len(chars)
    while i < n:
        cls = classes[i]
        if cls == "C":
            reduced.append("C")
            i += 1
        elif cls == "v":
            # Short vowel — V slot. If followed by a matching long-vowel
            # letter, extend to a true long vowel (VV).
            if i + 1 < n and classes[i + 1] == "L":
                pair = (chars[i], chars[i + 1])
                if pair in LONG_VOWEL_PAIRS:
                    reduced.append("V")
                    reduced.append("V")
                    i += 2
                    continue
            reduced.append("V")
            i += 1
        elif cls == "L":
            # Standalone long-vowel letter (no preceding matching short
            # vowel) is read as a consonant — WAW / YEH are consonants
            # in initial position; ALEF / ALEF_MAKSURA without a matching
            # short vowel are out-of-contract.
            if chars[i] in (WAW, YEH):
                reduced.append("C")
                i += 1
            else:
                return None, (
                    f"long-vowel letter U+{ord(chars[i]):04X} at index {i} "
                    "has no preceding matching short vowel"
                )
        elif cls == "s":
            # Sukun is a no-op in the reduced pattern: the consonant it
            # closes is already in `reduced`.
            i += 1
        else:  # pragma: no cover — defensive
            return None, f"unexpected class {cls!r} at index {i}"

    cv_string = "".join(reduced)
    if cv_string in _ALLOWED_CV_STRINGS:
        return cv_string, f"reduced pattern {cv_string} matches allowed shape"
    return None, (
        f"reduced pattern {cv_string!r} not in allowed shapes "
        f"{sorted(_ALLOWED_CV_STRINGS)}"
    )


def _surface_codepoints(surface: str) -> tuple[str, ...]:
    return tuple(f"U+{ord(ch):04X}" for ch in surface)


def _surface_codepoint_names(surface: str) -> tuple[str, ...]:
    return tuple(unicodedata.name(ch, "UNKNOWN") for ch in surface)


# ─────────────────────────────────────────────────────────────────────────────
# Per-token analysis: build evidence + candidate or invalidation
# ─────────────────────────────────────────────────────────────────────────────


def _build_boundary_evidence(
    token: TokenAnalysisTrace, input_text: str
) -> BoundaryEvidence:
    slice_text = input_text[token.start_index : token.end_index]
    boundary_preserved = token.surface_form_vocalized == slice_text
    return BoundaryEvidence(
        token_index=token.token_index,
        start_index=token.start_index,
        end_index=token.end_index,
        preceding_text=token.preceding_text,
        following_text=token.following_text,
        has_left_boundary=token.has_leading_boundary,
        has_right_boundary=token.has_trailing_boundary,
        boundary_preserved=boundary_preserved,
        source=EVIDENCE_SOURCE,
    )


def _identity_preserved(token: TokenAnalysisTrace, input_text: str) -> bool:
    if not token.surface_nfc_equal:
        return False
    if not token.surface_slice_equal:
        return False
    if token.surface_form_vocalized != input_text[token.start_index : token.end_index]:
        return False
    return True


def _analyze_token(
    token: TokenAnalysisTrace, input_text: str
) -> tuple[
    Optional[LicensedSyllableCandidate], Optional[SyllableInvalidationEvidence]
]:
    """Return (candidate, invalidation). Exactly one is non-None."""
    surface = token.surface_form_vocalized
    cps = token.surface_codepoints
    cp_names = token.surface_codepoint_names

    boundary = _build_boundary_evidence(token, input_text)
    identity_ok = _identity_preserved(token, input_text)
    cv_string, shape_reason = _detect_shape(surface)
    shape = (
        AllowedSyllableShape(cv_string) if cv_string is not None else None
    )

    shape_evidence = SyllableShapeEvidence(
        shape=shape,
        surface_form_vocalized=surface,
        surface_codepoints=cps,
        surface_codepoint_names=cp_names,
        shape_reason=shape_reason,
        allowed=cv_string is not None,
    )

    minimal_complete = shape_evidence.allowed
    no_expansion = shape_evidence.allowed
    economy_satisfied = (
        shape_evidence.allowed
        and boundary.boundary_preserved
        and identity_ok
        and minimal_complete
        and no_expansion
    )
    economy_reason_parts: list[str] = []
    if not shape_evidence.allowed:
        economy_reason_parts.append("shape not allowed")
    if not boundary.boundary_preserved:
        economy_reason_parts.append("boundary not preserved")
    if not identity_ok:
        economy_reason_parts.append("identity not preserved")
    economy_reason = (
        "all five conjunct conditions hold"
        if economy_satisfied
        else "; ".join(economy_reason_parts) or "economy conditions not all true"
    )

    economy_evidence = PhoneticEconomyEvidence(
        minimal_complete_syllable=minimal_complete,
        no_unnecessary_expansion=no_expansion,
        shape_allowed=shape_evidence.allowed,
        boundary_preserved=boundary.boundary_preserved,
        identity_preserved=identity_ok,
        economy_satisfied=economy_satisfied,
        reason=economy_reason,
    )

    if (
        shape_evidence.allowed
        and shape is not None
        and boundary.boundary_preserved
        and identity_ok
        and economy_satisfied
    ):
        candidate = LicensedSyllableCandidate(
            token_index=token.token_index,
            surface_form_vocalized=surface,
            surface_codepoints=cps,
            surface_codepoint_names=cp_names,
            shape=shape,
            boundary_evidence=boundary,
            shape_evidence=shape_evidence,
            economy_evidence=economy_evidence,
            identity_preserved=identity_ok,
            potential_only=True,
            runtime_status=CANDIDATE_RUNTIME_STATUS,
        )
        return candidate, None

    if not shape_evidence.allowed:
        reason = f"shape not in closed contract: {shape_reason}"
        unsupported = "out_of_contract"
    elif not boundary.boundary_preserved:
        reason = "boundary not preserved against input slice"
        unsupported = None
    elif not identity_ok:
        reason = "identity not preserved (NFC / slice / vocalized identity)"
        unsupported = None
    else:  # pragma: no cover — defensive
        reason = "economy not satisfied"
        unsupported = None

    invalidation = SyllableInvalidationEvidence(
        surface_form_vocalized=surface,
        reason=reason,
        unsupported_shape=unsupported,
        boundary_preserved=boundary.boundary_preserved,
        identity_preserved=identity_ok,
        candidate_emitted=False,
    )
    return None, invalidation


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────


def analyze_licensed_syllables(text: str) -> LicensedSyllableAnalysis:
    """Run Layer 4 over input text.

    Steps:
      1. Call qiyas_core.analysis_trace.analyze_potential_trace(text) to get
         the lower-layer trace (PR #128 / #130 / #131 / #132).
      2. For each token, build BoundaryEvidence, SyllableShapeEvidence,
         PhoneticEconomyEvidence.
      3. Emit a LicensedSyllableCandidate iff boundary preserved AND
         identity preserved AND shape allowed AND economy satisfied.
      4. Otherwise emit SyllableInvalidationEvidence for that token.

    The returned bundle preserves the lower-layer aggregate trace; it is
    not mutated, and MIU statuses are not rewritten. The bundle is
    potential-only; no meaning / hukm / i'rab / dalalah / reality claim
    is introduced. The four status fields remain "not_introduced".
    """
    trace: QiyasAnalysisTrace = analyze_potential_trace(text)

    candidates: list[LicensedSyllableCandidate] = []
    invalidations: list[SyllableInvalidationEvidence] = []
    for token in trace.tokens:
        candidate, invalidation = _analyze_token(token, text)
        if candidate is not None:
            candidates.append(candidate)
        if invalidation is not None:
            invalidations.append(invalidation)

    trace_summary = (
        f"tokens={trace.total_token_count} "
        f"identity_carrier={trace.identity_carrier} "
        f"diagnostic_key={trace.diagnostic_key} "
        f"mode={trace.mode} "
        f"lower_runtime_status={trace.runtime_status}"
    )

    return LicensedSyllableAnalysis(
        input_text=text,
        trace_summary=trace_summary,
        candidates=tuple(candidates),
        invalidations=tuple(invalidations),
        allowed_shapes=ALLOWED_SYLLABLE_SHAPES,
        runtime_status=LAYER4_RUNTIME_STATUS,
        meaning_status=NOT_INTRODUCED,
        hukm_status=NOT_INTRODUCED,
        irab_status=NOT_INTRODUCED,
        reality_status=NOT_INTRODUCED,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────────────────────


def _render_candidate(c: LicensedSyllableCandidate) -> list[str]:
    return [
        f"  - token_index={c.token_index}",
        f"    surface_form_vocalized={c.surface_form_vocalized!r}",
        f"    shape={c.shape.value}",
        f"    identity_preserved={c.identity_preserved}",
        f"    boundary_preserved={c.boundary_evidence.boundary_preserved}",
        f"    economy_satisfied={c.economy_evidence.economy_satisfied}",
        f"    codepoints={','.join(c.surface_codepoints)}",
        f"    codepoint_names={'|'.join(c.surface_codepoint_names)}",
    ]


def _render_invalidation(inv: SyllableInvalidationEvidence) -> list[str]:
    return [
        f"  - surface_form_vocalized={inv.surface_form_vocalized!r}",
        f"    reason={inv.reason}",
        f"    unsupported_shape={inv.unsupported_shape!r}",
        f"    boundary_preserved={inv.boundary_preserved}",
        f"    identity_preserved={inv.identity_preserved}",
        f"    candidate_emitted={inv.candidate_emitted}",
    ]


def render_licensed_syllable_analysis(analysis: LicensedSyllableAnalysis) -> str:
    """Deterministic terminal-readable rendering of a Layer 4 analysis."""
    allowed_shapes_str = ",".join(s.value for s in analysis.allowed_shapes)
    lines: list[str] = []

    lines.append("## Licensed Syllable Analysis")
    lines.append("=" * 60)
    lines.append(f"  input_text={analysis.input_text!r}")
    lines.append(f"  runtime_status={analysis.runtime_status}")
    lines.append(f"  allowed_shapes={allowed_shapes_str}")
    lines.append(f"  candidate_count={len(analysis.candidates)}")
    lines.append(f"  invalidation_count={len(analysis.invalidations)}")
    lines.append(f"  trace_summary={analysis.trace_summary}")
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
    lines.append("  * no meaning introduced")
    lines.append("  * no hukm introduced")
    lines.append("  * no i'rab introduced")
    lines.append("  * no dalalah introduced")
    lines.append("  * no reality claim introduced")
    lines.append("  * potential-only Layer 4")
    lines.append("  * no Layer 5 runtime")
    lines.append(
        f"  * narrow authorization: Layer 4 only "
        f"({LAYER4_AUTHORIZATION_DATE} maintainer directive); "
        "the global REC freeze remains in effect"
    )
    lines.append(
        f"  * meaning_status={analysis.meaning_status} "
        f"hukm_status={analysis.hukm_status} "
        f"irab_status={analysis.irab_status} "
        f"reality_status={analysis.reality_status}"
    )

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: python3 -m qiyas_core.licensed_syllable <text>")
        return 2
    text = args[0]
    analysis = analyze_licensed_syllables(text)
    print(render_licensed_syllable_analysis(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
