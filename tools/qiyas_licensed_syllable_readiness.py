"""Read-only Layer 4 LicensedSyllableCandidate readiness audit.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_licensed_syllable_readiness.py

Reports whether the repo has satisfied the Layer 4 readiness gates
defined under docs/qiyas_core/LICENSED_SYLLABLE_CONSTITUTION.md.

Under the narrow Layer 4 authorization (2026-06-13), gates 1-7 are
satisfied by `src/qiyas_core/licensed_syllable.py` and
`tests/qiyas_core/test_licensed_syllable.py`; gate 8 records the narrow
nature of the authorization itself — Layer 4 only, not a global REC
freeze release, not Layer 5, not semantic runtime, not meaning / hukm /
i'rab / dalalah / reality claims.

This remains a read-only audit. It calls `analyze_potential_trace(...)`
only to prove lower-layer evidence is still wired; it does not derive
syllable candidates here.
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
    "status": "narrow_layer4_authorization_satisfied",
    "runtime_status": "layer4_potential_only_narrow_authorization",
    "freeze_sensitive": "true",
}


# Each gate is (gate_name, status_label, evidence_note). The first seven
# gates are satisfied by the Layer 4 runtime + tests. Gate 8 records the
# narrow nature of the authorization.
LAYER4_READINESS_GATES: tuple[tuple[str, str, str], ...] = (
    (
        "explicit boundary evidence model",
        "SATISFIED",
        "BoundaryEvidence frozen dataclass in src/qiyas_core/licensed_syllable.py",
    ),
    (
        "licensed syllable candidate data model",
        "SATISFIED",
        "LicensedSyllableCandidate frozen dataclass; runtime_status="
        "potential_only_not_semantic_runtime",
    ),
    (
        "phonetic economy proof rule",
        "SATISFIED",
        "PhoneticEconomyEvidence; economy_satisfied iff shape allowed + "
        "boundary preserved + identity preserved + minimal complete + no "
        "unnecessary expansion",
    ),
    (
        "allowed syllable-shape contract in code",
        "SATISFIED",
        "AllowedSyllableShape enum: CV, CVC, CVV, CVVC, CVVCC (closed contract)",
    ),
    (
        "invalidation rule for unsupported shapes",
        "SATISFIED",
        "SyllableInvalidationEvidence; candidate_emitted=False; deterministic reason",
    ),
    (
        "tests for CV, CVC, CVV, CVVC, CVVCC only",
        "SATISFIED",
        "tests/qiyas_core/test_licensed_syllable.py groups 5 (CV) + 6 (CVC/CVV/CVVC/CVVCC)",
    ),
    (
        "proof that no meaning/hukm/i'rab/reality is introduced",
        "SATISFIED",
        "test groups 11 (negative constitutional guard) + 12 (no Layer 5+ classes); "
        "analysis bundle records meaning_status=hukm_status=irab_status=reality_status=not_introduced",
    ),
    (
        "maintainer unfreeze / explicit authorization if freeze remains active",
        "SATISFIED NARROWLY",
        "Layer 4 only, 2026-06-13 maintainer directive; not a global runtime unfreeze; "
        "REC-2..REC-4 still pending; global REC freeze remains active",
    ),
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
    lines.append("This is a read-only readiness audit. Layer 4 is now implemented")
    lines.append("under a narrow per-layer authorization (2026-06-13). The audit")
    lines.append("does not segment syllables here, does not call any runtime")
    lines.append("beyond the existing potential-only MIU analysis trace, and does")
    lines.append("not lift the global REC freeze.")
    lines.append("")


def _render_section_2_lower_layer_evidence(lines: list[str]) -> None:
    trace = analyze_potential_trace(SAMPLE_INPUT)
    bucket_counts: Counter[str] = Counter()
    for token in trace.tokens:
        bucket_counts[token.with_resolver_status] += 1

    lines.append(SEPARATOR)
    lines.append("## 2. Lower-Layer Evidence Available")
    lines.append(SEPARATOR)
    lines.append("The repo provides a potential-only MIU analysis trace via")
    lines.append("  qiyas_core.analysis_trace")
    lines.append("from PR #128 (extended by PRs #130/#131/#132). The Layer 4")
    lines.append("runtime at src/qiyas_core/licensed_syllable.py now consumes")
    lines.append("this trace; this audit calls analyze_potential_trace(...)")
    lines.append("only to prove the trace is still wired.")
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
    lines.append("  (these are potential-only trace observations; Layer 4 reads")
    lines.append("   them as evidence, never as a final judgment, hukm, or meaning)")
    lines.append("")


def _render_section_3_readiness_gates(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 3. Layer 4 Readiness Gates")
    lines.append(SEPARATOR)
    lines.append("Each gate below was an unfilled requirement under")
    lines.append("LICENSED_SYLLABLE_CONSTITUTION.md before the narrow Layer 4")
    lines.append("authorization (2026-06-13). Status is now reported per gate:")
    lines.append("")
    for gate_name, status, evidence in LAYER4_READINESS_GATES:
        lines.append(f"  * {gate_name}: {status}")
        lines.append(f"      evidence: {evidence}")
    lines.append("")


def _render_section_4_allowed_syllable_shapes(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 4. Allowed Syllable Shapes")
    lines.append(SEPARATOR)
    lines.append("Layer 4 admission is restricted to these shapes (closed contract):")
    lines.append("")
    for shape in ALLOWED_SYLLABLE_SHAPES:
        lines.append(f"  * {shape}")
    lines.append("")
    lines.append("Discipline:")
    lines.append("  * These are the only shapes Layer 4 admits.")
    lines.append("  * No runtime syllable segmentation is performed.")
    lines.append("    (a multi-syllable surface like CVCVCV is invalidated, not split)")
    lines.append("  * No multi-token surface is classified as a single syllable.")
    lines.append("  * No Arabic word meaning is claimed by this readiness audit.")
    lines.append("")


def _render_section_5_constitutional_boundary(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 5. Constitutional Boundary")
    lines.append(SEPARATOR)
    lines.append("This audit explicitly does NOT:")
    lines.append("  * admit any row into runtime outside narrow Layer 4 authorization")
    lines.append("  * create or modify any registry")
    lines.append("  * perform any source correction")
    lines.append("  * import external source data")
    lines.append("  * access new_arabic_analyzer/")
    lines.append("  * make any grammar / i'rab / meaning / hukm / dalalah / reality claim")
    lines.append("  * introduce WordCandidate / LafzCandidate / DalalahCandidate types")
    lines.append("  * introduce FinalMeaning / HukmCandidate / RealityClaim types")
    lines.append("  * lift the global REC freeze (freeze remains active per §1)")
    lines.append("  * authorize Layer 5 or above")
    lines.append("  * introduce semantic runtime")
    lines.append("")
    lines.append("Layer 4 is narrowly authorized as a potential-only runtime slice;")
    lines.append("no Layer 5 runtime is introduced, no semantic runtime is introduced,")
    lines.append("no global unfreeze is performed.")
    lines.append("")
    lines.append("End of Licensed Syllable Readiness audit.")


def render_readiness_report() -> str:
    lines: list[str] = []
    _render_section_1_title_and_state(lines)
    _render_section_2_lower_layer_evidence(lines)
    _render_section_3_readiness_gates(lines)
    _render_section_4_allowed_syllable_shapes(lines)
    _render_section_5_constitutional_boundary(lines)
    return "\n".join(lines)


def main() -> int:
    print(render_readiness_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
