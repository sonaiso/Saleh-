"""Stage A — legacy fixture harness tests (audit only).

Proves: (1) raw legacy outputs are captured & preserved verbatim (no correction),
(2) each output family is classified by Qiyas reliability, and — the constitutional
crux — (3) NOTHING from the legacy analyzer is consumed by the Qiyas runtime. No
Candidate/CandidateSet is produced; no registry/spine change.
"""

from __future__ import annotations

import json
import os
import pathlib

import legacy_harness as H


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


# ── Fixtures captured & raw-preserved ─────────────────────────────────────────


def test_LFH_01_raw_fixtures_exist_and_nonempty():
    assert os.path.getsize(H.WORDS_RAW) > 0
    assert os.path.getsize(H.PHRASE_RAW) > 0


def test_LFH_02_thirtyfour_tokens_loaded_verbatim():
    fixtures = H.load_word_fixtures()
    assert len(fixtures) == 34
    one = next(f for f in fixtures if f.token == "كَاتِب")
    # raw stdout is verbatim — contains the legacy layer headers and the token.
    assert "L3 — الإِعراب" in one.raw_stdout
    assert "كَاتِب" in one.raw_stdout
    assert "class=ISM_MUARAB" in one.raw_stdout


def test_LFH_03_errors_preserved_not_silently_corrected():
    fx = {f.token: f.raw_stdout for f in H.load_word_fixtures()}
    # بَاعَ is misclassified ISM_MUARAB by the legacy analyzer — we keep it VERBATIM.
    assert "class=ISM_MUARAB" in fx["بَاعَ"]
    assert "class=FIIL" not in fx["بَاعَ"].split("L3")[1]
    # صَامَ's questionable wazn فَالَ is preserved exactly.
    assert "فَالَ" in fx["صَامَ"]


def test_LFH_04_phrase_fixture_has_full_pipeline_families():
    raw = H.load_phrase_fixture()
    # the --all phrase capture carries the higher families verbatim.
    assert "L1 — التَّقطيع" in raw
    assert "L3 — الإِعراب" in raw


# ── Classification (reliability tagging, not correction) ──────────────────────


def test_LFH_05_classification_snapshot_matches_harness():
    with open(os.path.join(H.FIXTURE_DIR, "classification.json"), encoding="utf-8") as fh:
        snap = json.load(fh)
    assert snap["consumed_by_qiyas_runtime"] is False
    by_token = {r["token"]: r for r in snap["rows"]}
    for row in H.capability_rows():
        s = by_token[row.token]
        # verbatim fields round-trip exactly (no drift / no correction)
        assert s["legacy_class"] == row.legacy_class
        assert s["legacy_role"] == row.legacy_role
        assert s["legacy_root"] == row.legacy_root
        assert s["legacy_wazn"] == row.legacy_wazn
        assert s["family_reliability"] == row.family_reliability


def test_LFH_06_committed_irab_tagged_unsafe_final_looking():
    # Every token whose L3 emits a role/case is a committed i'rab decision → must be
    # tagged unsafe_final_looking (Qiyas must downgrade it, never trust it).
    for row in H.capability_rows():
        if row.legacy_role and row.legacy_role != "—":
            assert row.family_reliability[H.FAMILY_ROLE_CASE] == H.UNSAFE_FINAL_LOOKING, row.token


def test_LFH_07_known_errors_and_ambiguities_tagged():
    rows = {r.token: r for r in H.capability_rows()}
    assert rows["بَاعَ"].family_reliability[H.FAMILY_WORD_CLASS] == H.SUSPICIOUS_DEFER
    assert rows["صَامَ"].family_reliability[H.FAMILY_WORD_CLASS] == H.SUSPICIOUS_DEFER
    assert rows["آمَنَ"].family_reliability[H.FAMILY_ROOT_WAZN] == H.SUSPICIOUS_DEFER  # hamza
    assert rows["مَدَّ"].family_reliability[H.FAMILY_ROOT_WAZN] == H.SUSPICIOUS_DEFER   # shadda
    # clean closed-class / sound triliteral stays proposal evidence.
    assert rows["مِن"].family_reliability[H.FAMILY_WORD_CLASS] == H.PROPOSAL_EVIDENCE
    assert rows["كَتَبَ"].family_reliability[H.FAMILY_ROOT_WAZN] == H.PROPOSAL_EVIDENCE


# ── CONSTITUTIONAL PROOF: nothing reaches the Qiyas runtime ────────────────────


def test_LFH_08_harness_produces_no_qiyas_candidate():
    assert H.produces_qiyas_candidates() is False


def test_LFH_09_harness_imports_no_qiyas_runtime():
    # The harness must not IMPORT the kernel / candidate / adapters / rules / run_qiyas.
    # (Checked via the import graph, not prose — the docstring legitimately *names*
    # Candidate/CandidateSet to state it produces none.)
    import ast
    tree = ast.parse(pathlib.Path(H.__file__).read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert not any(m and (m == "run_qiyas" or m.startswith("qiyas_core")) for m in imported), \
        f"harness must not import qiyas runtime; imports={imported}"
    # And it must not have pulled qiyas_core into sys.modules via this harness.
    assert getattr(H, "QiyasKernel", None) is None and getattr(H, "Candidate", None) is None


def test_LFH_10_no_runtime_module_consumes_the_legacy_harness_or_fixtures():
    # Scan every Qiyas runtime source + run_qiyas for ANY reference to the legacy
    # harness, the fixtures, or the external analyzer path. There must be NONE.
    targets = list((REPO_ROOT / "src" / "qiyas_core").rglob("*.py"))
    targets.append(REPO_ROOT / "run_qiyas.py")
    needles = ("legacy_harness", "legacy_fixtures", "LegacyAnalyzer",
               "hussein/clean_code", "analyze_verse_v3")
    offenders = []
    for p in targets:
        text = p.read_text(encoding="utf-8", errors="ignore")
        for n in needles:
            if n in text:
                offenders.append((str(p.relative_to(REPO_ROOT)), n))
    assert not offenders, f"Qiyas runtime must not consume legacy outputs (Stage A): {offenders}"


def test_LFH_11_legacy_layer_not_wired_into_pipeline():
    # The run_qiyas pipeline emits no legacy-sourced step.
    import run_qiyas as rq
    layers = {s.layer for r in rq.process_text("كَتَبَ") for s in r.steps}
    assert not any("Legacy" in lyr or "legacy" in lyr for lyr in layers)
