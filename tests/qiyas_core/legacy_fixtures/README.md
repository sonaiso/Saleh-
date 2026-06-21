# Legacy analyzer fixtures — Stage A (audit only)

**Provenance.** These files are **verbatim captured outputs** of the external legacy
Arabic analyzer at `/Users/husseinhiyassat/fractal/hussein/clean_code`
(`analyze_verse_v3.py`), captured read-only on 2026-06-21. They are **analyzer
outputs**, not a corpus — they are NOT the Quran and contain no source-text snapshot
beyond the few representative tokens/phrase analyzed.

**Files**
- `words_morph_i3rab.raw.txt` — raw stdout for 34 representative tokens
  (`analyze_verse_v3.py "<tok>" --morph --i3rab`), one delimited block per token,
  **exactly as emitted (including errors — no silent correction)**.
- `phrase_all.raw.txt` — raw stdout for one phrase (`--all`, full L1–L8) capturing the
  relations / events / resolution / meaning / reasoning families.
- `classification.json` — a Qiyas-side **reliability tagging** of each token's output
  families (`proposal_evidence` / `useful_ambiguous` / `suspicious_defer` /
  `unsafe_final_looking` / `quarantine`). The extracted fields are verbatim; the tags
  are how Qiyas must *treat* the output, **not** a correction of it.

**Governance (constitutional).**
- The legacy analyzer **PROPOSES**; only Qiyas rules license / defer / block. **Nothing
  here is consumed by the Qiyas runtime** (`run_qiyas`, any adapter, any rule). Enforced
  by `tests/qiyas_core/test_legacy_fixture_harness.py`.
- These fixtures produce **no** Qiyas `Candidate` / `CandidateSet`. No registry change,
  count stays 19, no P13, P0–P12 untouched.
- The legacy `class | role+case | root | wazn` L3 line is a **committed (final-looking)
  i'rab decision** and is tagged `unsafe_final_looking` — it must be downgraded, never
  trusted as a Qiyas judgment.
- Regeneration (by hand, not in CI): `LegacyAnalyzerProposalProvider(mode="subprocess")`
  in `tests/qiyas_core/legacy_harness.py` re-runs the external analyzer. Default mode is
  fixture-only so CI needs no external dependency.

This directory is Stage A of the legacy-integration roadmap: **capture only**. No
wiring into P3.1 / P5.1 or any other layer is performed.
