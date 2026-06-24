"""Step C — P5.1 runtime provider against the committed v1 Hussein snapshot.

Validates the narrow runtime provider (`HusseinSnapshotProvider`) and its live wiring
into P5.1 InflectionalClosureQiyas: it reads ONLY the committed snapshot (never Stage A,
never the analyzer), supplies ONLY closed-category / verb-kind hints (never root/wazn,
never role/case/relation/event/meaning), and lets the P5.1 rule decide. Quarantined /
suspicious rows never ACCEPT; P3.1 is not wired to the snapshot; P5.1 stays non-gating.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

import run_qiyas as rq
from qiyas_core.hussein_snapshot_provider import HusseinSnapshotProvider

REPO = pathlib.Path(__file__).resolve().parents[2]
PROVIDER_SRC = REPO / "src" / "qiyas_core" / "hussein_snapshot_provider.py"


def _provider():
    return HusseinSnapshotProvider()


def _p5_1_step(token):
    for r in rq.process_text(token):
        for s in r.steps:
            if s.layer == "InflectionalClosureQiyas":
                return s
    return None


def _layer_order(token):
    layers = []
    for r in rq.process_text(token):
        for s in r.steps:
            if s.layer not in layers:
                layers.append(s.layer)
    return layers


# ── provider loading / source discipline ──────────────────────────────────────


def test_PC_01_provider_loads_manifest_and_csv():
    p = _provider()
    assert p.get_p5_1_proposal("كَتَبَ") is not None  # triggers load
    assert p.get_p5_1_proposal("مِن") is not None


def test_PC_02_provider_refuses_stage_a_fixtures():
    bad = REPO / "tests" / "qiyas_core" / "legacy_fixtures"
    with pytest.raises(ValueError):
        HusseinSnapshotProvider(snapshot_dir=bad)


def test_PC_03_provider_has_no_subprocess_or_analyzer_import():
    # Import-graph check (not prose — the docstring legitimately names subprocess to say
    # it does NOT use it).
    tree = ast.parse(PROVIDER_SRC.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert "subprocess" not in imported, imported
    assert not any("analyze_verse" in m for m in imported)
    # no subprocess.run / os.system call
    assert not any(isinstance(n, ast.Attribute) and n.attr in ("run", "Popen", "system")
                   and isinstance(n.value, ast.Name) and n.value.id in ("subprocess", "os")
                   for n in ast.walk(tree))


# ── consumability gating ──────────────────────────────────────────────────────


def test_PC_04_proposals_only_for_manually_reviewed_p5_1_target_rows():
    p = _provider()
    # manually_reviewed + P5.1 target → proposal present
    for tok in ("مِن", "هو", "الذي", "كَتَبَ", "يَقُولُ", "مَكْتُوب"):
        assert p.get_p5_1_proposal(tok) is not None, tok


def test_PC_05_none_for_quarantined_rows():
    p = _provider()
    for tok in ("بَاعَ", "صَامَ", "مكتوب"):  # quarantined in v1
        assert p.get_p5_1_proposal(tok) is None, tok


def test_PC_06_evidence_excludes_root_and_wazn():
    p = _provider()
    for tok in ("مِن", "هو", "الذي", "كَتَبَ", "يَقُولُ", "مَكْتُوب"):
        prop = p.get_p5_1_proposal(tok)
        assert "root" not in str(prop.classify_kwargs)
        assert "wazn" not in str(prop.classify_kwargs)
        # the proposal object itself carries no root/wazn attribute
        assert not hasattr(prop, "legacy_root") and not hasattr(prop, "legacy_wazn")


def test_PC_07_evidence_excludes_forbidden_families():
    p = _provider()
    kwargs_keys = set()
    for tok in ("مِن", "هو", "الذي", "كَتَبَ", "يَقُولُ", "مَكْتُوب"):
        kwargs_keys |= set(p.get_p5_1_proposal(tok).classify_kwargs.keys())
    # only closed-category / verb-kind kwargs are ever handed to P5.1
    assert kwargs_keys <= {"word_kind", "closed_category", "verb_tense", "is_closed_compound"}
    for forbidden in ("role", "case", "irab", "i3rab", "relation", "event",
                      "meaning", "qa", "tafsir", "hukm", "truth", "reality"):
        assert not any(forbidden in k.lower() for k in kwargs_keys), forbidden


def test_PC_08_unsafe_final_looking_field_never_passed_as_evidence():
    p = _provider()
    prop = p.get_p5_1_proposal("كَتَبَ")
    assert prop.unsafe_final_looking == "true"          # row flags the ignored i'rab
    assert "unsafe" not in str(prop.classify_kwargs)    # but it is never fed
    assert "i3rab" in prop.ignored_fields_summary       # the role/i'rab stays ignored


def test_PC_09_suspicious_defer_rows_yield_no_evidence():
    # قَالَ etc. collapse to suspicious_defer in v1 → no proposal → P5.1 will DEFER.
    p = _provider()
    assert p.get_p5_1_proposal("قَالَ") is None


# ── runtime consumption (tokens that reach P5.1) ──────────────────────────────


def test_PC_10_provider_serves_harf_closed_category_rows():
    # HARF rows are served as mabni hints (closed-category). NOTE: single ḥarf tokens do
    # not reach P5.1 in the live pipeline (no accepted P5 MufradWord) — see PC_18.
    p = _provider()
    for tok in ("مِن", "إلى", "على"):
        prop = p.get_p5_1_proposal(tok)
        assert prop.p5_1_candidate_hint == "mabni" and prop.legacy_class == "HARF", tok


def test_PC_11_provider_serves_mabni_and_relative_rows():
    p = _provider()
    assert p.get_p5_1_proposal("هو").classify_kwargs == {"closed_category": "pronoun"}
    assert p.get_p5_1_proposal("هذا").classify_kwargs == {"closed_category": "demonstrative"}
    assert p.get_p5_1_proposal("الذي").classify_kwargs == {"closed_category": "relative"}


def test_PC_12_runtime_p5_1_accepts_fiil_past_and_present_via_snapshot():
    # كَتَبَ (past → mabni-readiness) and يَقُولُ (present → mu'rab-readiness) reach P5.1
    # and ACCEPT through the snapshot proposal.
    s = _p5_1_step("كَتَبَ")
    assert s.status == "accepted" and s.candidate_type == "MabniReadinessCandidate"
    assert any("hussein_snapshot_v1" in t for t in s.trace_ids)
    s2 = _p5_1_step("يَقُولُ")
    assert s2.status == "accepted" and s2.candidate_type == "Mu'rabReadinessCandidate"
    # nominal mu'rab-readiness
    s3 = _p5_1_step("مَكْتُوب")
    assert s3.status == "accepted" and s3.candidate_type == "Mu'rabReadinessCandidate"


def test_PC_13_quarantined_examples_produce_no_p5_1_accept():
    for tok in ("بَاعَ", "صَامَ"):  # reach P5.1 but are quarantined → no snapshot evidence
        s = _p5_1_step(tok)
        assert s is not None and s.status == "deferred", tok
        assert not any("hussein_snapshot_v1" in t for t in s.trace_ids), tok


def test_PC_14_p3_1_runtime_trace_does_not_mention_snapshot():
    for tok in ("كَتَبَ", "مَكْتُوب", "بَاعَ"):
        for r in rq.process_text(tok):
            for s in r.steps:
                if s.layer == "WeightPatternQiyas":
                    assert not any("hussein_snapshot" in t for t in s.trace_ids), tok
                    assert not any("legacy_root" in t or "legacy_wazn" in t
                                   for t in s.trace_ids), tok


def test_PC_15_weight_pattern_behaviour_unchanged_from_pr190():
    # PR #190 surface binding still holds: sound ACCEPT, weak DEFER.
    def wp(token):
        return [s for r in rq.process_text(token) for s in r.steps
                if s.layer == "WeightPatternQiyas"]
    assert all(s.status == "accepted" for s in wp("كَتَبَ"))
    assert any("فَعَلَ" in t for s in wp("كَتَبَ") for t in s.trace_ids)
    assert all(s.status == "deferred" for s in wp("قَالَ"))


def test_PC_16_p5_1_remains_non_gating():
    # P6 VerbalSignifiedQiyas follows P5.1 whether it ACCEPTs (كَتَبَ) or DEFERs (بَاعَ).
    for tok in ("كَتَبَ", "بَاعَ"):
        order = _layer_order(tok)
        assert "InflectionalClosureQiyas" in order and "VerbalSignifiedQiyas" in order, tok
        assert order.index("VerbalSignifiedQiyas") > order.index("InflectionalClosureQiyas"), tok


# ── governance + no-leakage ───────────────────────────────────────────────────


def test_PC_17_registry_19_no_p13_p12_terminal_p5_1_auxiliary():
    from qiyas_core.slot_geometry_core import master_registry_seed as MRS
    layers = list(MRS.build_master_registry_seed().all_layers())
    assert len(layers) == 19
    assert not any("InflectionalClosure" in (s.name + s.id) for s in layers)
    assert not any("P13" in n for n in dir(MRS) if n.startswith("LAYER_ID_"))


def test_PC_18_residual_unreached_tokens_honest_limit():
    # Step C2 closed the closed-category reachability gap for v1 rows (مِن/إلى/على/هو/
    # هذا/الذي/الذين now reach P5.1 via the reachability bridge — see the C2 suite).
    # The residual honest limit is tokens that are NOT an exact v1 surface (the fully
    # vocalized هُوَ ≠ committed هو) or are quarantined (unvocalized مكتوب): they still
    # do not reach P5.1. No fuzzy harakat-stripping is done (مَكْتُوب≠مكتوب safety).
    for tok in ("هُوَ", "مكتوب"):
        assert _p5_1_step(tok) is None, tok


def test_PC_19_no_final_judgment_leakage_across_p5_1():
    forbidden = {"MabniJudgment", "MurabJudgment", "IrabFinalDecision", "CaseJudgment",
                 "IrabCandidate", "MeaningCandidate", "DalalahCandidate", "HukmCandidate",
                 "RealityClaim", "TruthJudgment", "FinalMeaning"}
    seen = set()
    for tok in ("كَتَبَ", "يَقُولُ", "مَكْتُوب", "بَاعَ", "صَامَ"):
        s = _p5_1_step(tok)
        if s:
            seen.add(s.candidate_type)
    assert seen <= {"MabniReadinessCandidate", "Mu'rabReadinessCandidate",
                    "InflectionalClosureCandidate"}
    assert not (seen & forbidden)


def test_PC_20_no_stage_a_or_snapshot_read_path_in_runtime_modules():
    # run_qiyas may import the provider, but must not itself reference Stage A fixtures
    # or read the snapshot file path directly.
    txt = (REPO / "run_qiyas.py").read_text(encoding="utf-8")
    assert "legacy_fixtures" not in txt
    assert "external_snapshots" not in txt  # the provider owns the path, not run_qiyas
