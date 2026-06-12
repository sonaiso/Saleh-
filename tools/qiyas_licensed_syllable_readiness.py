"""Read-only Layer 4 LicensedSyllableCandidate readiness audit.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_licensed_syllable_readiness.py

Reports whether the repo is ready to implement Layer 4 (LicensedSyllableCandidate)
under docs/qiyas_core/LICENSED_SYLLABLE_CONSTITUTION.md, using the merged
``qiyas_core.analysis_trace`` as lower-layer evidence.

This is a readiness/audit artifact, NOT runtime. It performs no syllable
segmentation, defines no LicensedSyllableCandidate class, calls no registry,
imports no external source, modifies no file. It calls
``analyze_potential_trace(...)`` only to prove lower-layer evidence is wired,
never to derive a syllable.
"""

from __future__ import annotations

from collections import Counter

from qiyas_core.analysis_trace import (
    DIAGNOSTIC_KEY_LABEL,
    IDENTITY_CARRIER_LABEL,
    analyze_potential_trace,
)


SAMPLE_INPUT = "بِ ضَ وَ يَ ضَرَبَ"
SEPARATOR = "=" * 60


READINESS_LABELS = {
    "layer": "Layer 4",
    "target": "LicensedSyllableCandidate",
    "status": "readiness_only",
    "runtime_status": "not_implemented",
    "freeze_sensitive": "true",
}


MISSING_EVIDENCE: tuple[str, ...] = (
    "explicit boundary evidence model",
    "licensed syllable candidate data model",
    "phonetic economy proof rule",
    "allowed syllable-shape contract in code",
    "invalidation rule for unsupported shapes",
    "tests for CV, CVC, CVV, CVVC, CVVCC only",
    "proof that no meaning/hukm/i'rab/reality is introduced",
    "maintainer unfreeze / explicit authorization if freeze remains active",
)


ALLOWED_SYLLABLE_SHAPES: tuple[str, ...] = (
    "CV",
    "CVC",
    "CVV",
    "CVVC",
    "CVVCC",
)


def _render_section_1_title_and_state(lines: list[str]) -> None:
    lines.append("## 1. Licensed Syllable Readiness")
    lines.append(SEPARATOR)
    lines.append("")
    lines.append(f"  layer={READINESS_LABELS['layer']}")
    lines.append(f"  target={READINESS_LABELS['target']}")
    lines.append(f"  status={READINESS_LABELS['status']}")
    lines.append(f"  runtime_status={READINESS_LABELS['runtime_status']}")
    lines.append(f"  freeze_sensitive={READINESS_LABELS['freeze_sensitive']}")
    lines.append("")
    lines.append("This is a read-only readiness audit. It does not implement")
    lines.append("Layer 4, does not segment syllables, does not call any runtime")
    lines.append("beyond the existing potential-only MIU analysis trace.")
    lines.append("")


def _render_section_2_lower_layer_evidence(lines: list[str]) -> None:
    trace = analyze_potential_trace(SAMPLE_INPUT)
    bucket_counts: Counter[str] = Counter()
    for token in trace.tokens:
        bucket_counts[token.with_resolver_status] += 1

    lines.append(SEPARATOR)
    lines.append("## 2. Lower-Layer Evidence Available")
    lines.append(SEPARATOR)
    lines.append("The repo now provides a potential-only MIU analysis trace via")
    lines.append("  qiyas_core.analysis_trace")
    lines.append("from PR #128. The audit calls analyze_potential_trace(...) to")
    lines.append("prove the trace is wired and producing evidence; it does NOT")
    lines.append("consume the trace as a syllable input.")
    lines.append("")
    lines.append(f"  identity_carrier={IDENTITY_CARRIER_LABEL}")
    lines.append(f"  diagnostic_key={DIAGNOSTIC_KEY_LABEL}")
    lines.append("  token surfaces preserved with vocalization (harakat retained)")
    lines.append("  resolver effects visible as trace, not final judgment")
    lines.append("")
    lines.append(f"  sample input: {SAMPLE_INPUT}")
    lines.append(f"  input preserved: {trace.input_text == SAMPLE_INPUT}")
    lines.append(f"  token_count={len(trace.tokens)}")
    lines.append("")
    lines.append("  accepted/deferred/blocked statuses available from analysis trace:")
    for bucket in ("ACCEPTED", "DEFERRED", "BLOCKED"):
        lines.append(f"    {bucket}: {bucket_counts.get(bucket, 0)}")
    lines.append("")
    lines.append("  (these are potential-only trace observations; the audit does")
    lines.append("   not promote them into Layer 4 admission decisions)")
    lines.append("")


def _render_section_3_missing_evidence(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 3. Required Missing Evidence Before Runtime")
    lines.append(SEPARATOR)
    lines.append("The following gates are NOT yet satisfied. Each is a separate")
    lines.append("explicit cycle. None is opened by this audit.")
    lines.append("")
    for item in MISSING_EVIDENCE:
        lines.append(f"  * {item}")
    lines.append("")


def _render_section_4_allowed_syllable_shapes(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 4. Allowed Syllable Shapes")
    lines.append(SEPARATOR)
    lines.append("Future Layer 4 admission would be restricted to these shapes:")
    lines.append("")
    for shape in ALLOWED_SYLLABLE_SHAPES:
        lines.append(f"  * {shape}")
    lines.append("")
    lines.append("Discipline:")
    lines.append("  * These are readiness labels only.")
    lines.append("  * No runtime syllable segmentation is performed.")
    lines.append("  * No Arabic word is classified as a syllable in this PR.")
    lines.append("")


def _render_section_5_constitutional_boundary(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 5. Constitutional Boundary")
    lines.append(SEPARATOR)
    lines.append("This audit explicitly does NOT:")
    lines.append("  * admit any row into runtime")
    lines.append("  * create or modify any registry")
    lines.append("  * perform any source correction")
    lines.append("  * import external source data")
    lines.append("  * access new_arabic_analyzer/")
    lines.append("  * make any grammar / i'rab / meaning / hukm / dalalah / reality claim")
    lines.append("  * introduce WordCandidate / LafzCandidate / DalalahCandidate types")
    lines.append("  * introduce FinalMeaning / HukmCandidate / RealityClaim types")
    lines.append("  * introduce LicensedSyllableCandidate implementation in this PR")
    lines.append("")
    lines.append("End of Licensed Syllable Readiness audit.")


def render_readiness_report() -> str:
    lines: list[str] = []
    _render_section_1_title_and_state(lines)
    _render_section_2_lower_layer_evidence(lines)
    _render_section_3_missing_evidence(lines)
    _render_section_4_allowed_syllable_shapes(lines)
    _render_section_5_constitutional_boundary(lines)
    return "\n".join(lines)


def main() -> int:
    print(render_readiness_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
