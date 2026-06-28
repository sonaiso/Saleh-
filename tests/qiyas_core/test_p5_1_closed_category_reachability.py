"""Step C2 — closed-category reachability into P5.1 (boss-visible).

Single-token closed-category units (حروف / ضمائر / أسماء موصولة) do not form an accepted
P5 MufradWord, so P5.1 never fires for them through the normal chain. C2 adds a narrow
structural reachability bridge: when the committed v1 Hussein snapshot supplies a SAFE
closed-category proposal, a ClosedCategoryMufradCarrier is synthesized so P5.1 can classify
mabni-readiness. Structural only — no meaning / i'rab / role / relation / final judgment.
Quarantined / suspicious rows create no reachability; P5.1 still decides; non-gating.

NOTE on vocalization: the committed v1 snapshot stores the pronoun as ``هو`` (no harakat),
so the closed-category demos use the snapshot's exact surfaces. The fully-vocalized ``هُوَ``
is a DISTINCT surface absent from v1 and is intentionally NOT force-matched — matching is
exact-surface to preserve vocalized identity (مِنْ ≠ مَنْ) and avoid the مَكْتُوب/مكتوب
unvocalized-key collision.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

import run_qiyas as rq
from qiyas_core.hussein_snapshot_provider import HusseinSnapshotProvider

REPO = pathlib.Path(__file__).resolve().parents[2]
PROVIDER_SRC = REPO / "src" / "qiyas_core" / "hussein_snapshot_provider.py"

# هو is intentionally EXCLUDED (policy quarantine — standalone pronoun); see CC_12.
CLOSED_CATEGORY = ("مِن", "إلى", "على", "هذا", "الذي", "الذين")
QUARANTINED = ("بَاعَ", "صَامَ", "مكتوب", "هو")


def _provider():
    return HusseinSnapshotProvider()


def _steps(token, layer):
    return [s for r in rq.process_text(token) for s in r.steps if s.layer == layer]


def _p5_1(token):
    st = _steps(token, "InflectionalClosureQiyas")
    return st[0] if st else None


# ── provider-level reachability gating ────────────────────────────────────────


def test_CC_01_reachability_uses_only_committed_snapshot():
    p = _provider()
    assert p.closed_category_reachability("مِن") is not None  # triggers load + serves


def test_CC_02_provider_refuses_stage_a_paths():
    with pytest.raises(ValueError):
        HusseinSnapshotProvider(snapshot_dir=REPO / "tests" / "qiyas_core" / "legacy_fixtures")


def test_CC_03_no_subprocess_or_analyzer_import():
    tree = ast.parse(PROVIDER_SRC.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert "subprocess" not in imported
    assert not any("analyze_verse" in m for m in imported)


def test_CC_04_reachability_only_for_manually_reviewed_closed_category():
    p = _provider()
    for tok in CLOSED_CATEGORY:
        assert p.closed_category_reachability(tok) is not None, tok


def test_CC_05_no_reachability_for_quarantined_rows():
    p = _provider()
    for tok in QUARANTINED:
        assert p.closed_category_reachability(tok) is None, tok


def test_CC_06_no_reachability_for_suspicious_rows():
    assert _provider().closed_category_reachability("قَالَ") is None


def test_CC_06b_no_reachability_for_verbs_and_nominals():
    # verbs/nominals reach P5 normally → the bridge must NOT fire for them.
    p = _provider()
    for tok in ("كَتَبَ", "يَقُولُ", "مَكْتُوب"):
        assert p.closed_category_reachability(tok) is None, tok


def test_CC_07_carrier_exposes_no_root_or_wazn():
    p = _provider()
    for tok in CLOSED_CATEGORY:
        carrier_set, kwargs = p.closed_category_reachability(tok)
        assert "root" not in str(kwargs) and "wazn" not in str(kwargs)
        c = carrier_set.candidates[0]
        blob = str(c.identity_ids) + str(c.trace_ids)
        assert "root" not in blob and "wazn" not in blob
        assert c.candidate_type == "ClosedCategoryMufradCarrier"


def test_CC_08_carrier_exposes_no_forbidden_families():
    p = _provider()
    keys = set()
    for tok in CLOSED_CATEGORY:
        _cs, kwargs = p.closed_category_reachability(tok)
        keys |= set(kwargs.keys())
    assert keys <= {"closed_category", "is_closed_compound"}
    for forbidden in ("role", "case", "irab", "relation", "event", "meaning",
                      "qa", "tafsir", "hukm", "truth", "reality"):
        assert not any(forbidden in k.lower() for k in keys)


# ── live runtime reachability (tests 9–15) ────────────────────────────────────


def test_CC_09_min_reaches_p5_1_native_source_takes_precedence():
    # مِن is now served by the Qiyas-NATIVE closed-function-word inventory, which takes
    # precedence over the (still-present) v1 snapshot HARF row. It still reaches P5.1 and
    # ACCEPTs MabniReadiness — but the source is native, not Hussein.
    s = _p5_1("مِن")
    assert s is not None and s.status == "accepted"
    assert s.candidate_type == "MabniReadinessCandidate"
    assert any("qiyas_native_closed_function_word" in t for t in s.trace_ids)
    assert not any("hussein_snapshot_v1" in t for t in s.trace_ids)


def test_CC_10_ila_reaches_p5_1_with_snapshot_source():
    s = _p5_1("إلى")
    assert s and s.status == "accepted" and any("hussein_snapshot_v1" in t for t in s.trace_ids)


def test_CC_11_ala_reaches_p5_1_with_snapshot_source():
    s = _p5_1("على")
    assert s and s.status == "accepted" and any("hussein_snapshot_v1" in t for t in s.trace_ids)


def test_CC_12_standalone_pronoun_huwa_excluded_by_policy():
    # POLICY: the standalone pronoun هو is referential/indexical and must NOT be
    # runtime-consumable as a context-free closed-category unit (quarantined /
    # out_of_scope_pronoun in v1) — even though Hussein produced it in Stage A.
    p = _provider()
    assert p.closed_category_reachability("هو") is None
    assert p.get_p5_1_proposal("هو") is None
    assert _p5_1("هو") is None
    # no reachability carrier or snapshot source for هو
    assert not _steps("هو", "ClosedCategoryReachabilityQiyas")


def test_CC_13_demonstrative_hadha_reaches_p5_1():
    s = _p5_1("هذا")
    assert s and s.status == "accepted" and any("hussein_snapshot_v1" in t for t in s.trace_ids)


def test_CC_14_relative_alladhi_reaches_p5_1():
    s = _p5_1("الذي")
    assert s and s.status == "accepted" and any("hussein_snapshot_v1" in t for t in s.trace_ids)


def test_CC_15_relative_alladhina_reaches_p5_1():
    s = _p5_1("الذين")
    assert s and s.status == "accepted" and any("hussein_snapshot_v1" in t for t in s.trace_ids)


def test_CC_15b_reachability_step_visible_in_ladder():
    # the bridge emits a visible carrier step. مِن is now served natively
    # (NativeClosedFunctionWordQiyas); the rest go via the snapshot
    # ClosedCategoryReachabilityQiyas bridge. Either carrier is admissible.
    for tok in CLOSED_CATEGORY:
        assert (
            _steps(tok, "ClosedCategoryReachabilityQiyas")
            or _steps(tok, "NativeClosedFunctionWordQiyas")
        ), tok


def test_CC_15c_fully_vocalized_huwa_is_distinct_surface_not_matched():
    # هُوَ (vocalized) is not in v1 → no reachability (exact-surface discipline).
    assert _provider().closed_category_reachability("هُوَ") is None
    assert _p5_1("هُوَ") is None


# ── only readiness output; negatives; stability; isolation ────────────────────


def test_CC_16_p5_1_emits_only_readiness_not_final_judgment():
    forbidden = {"MabniJudgment", "MurabJudgment", "IrabFinalDecision", "CaseJudgment",
                 "MeaningCandidate", "DalalahCandidate", "HukmCandidate", "RealityClaim",
                 "TruthJudgment", "FinalMeaning"}
    seen = set()
    for tok in CLOSED_CATEGORY:
        s = _p5_1(tok)
        if s:
            seen.add(s.candidate_type)
    assert seen <= {"MabniReadinessCandidate", "Mu'rabReadinessCandidate",
                    "InflectionalClosureCandidate"}
    assert not (seen & forbidden)


def test_CC_17_quarantined_examples_gain_no_reachability_accept():
    for tok in QUARANTINED:
        # no reachability carrier from a quarantined snapshot row
        assert not any("hussein_snapshot_v1" in t
                       for st in _steps(tok, "ClosedCategoryReachabilityQiyas")
                       for t in st.trace_ids)
        s = _p5_1(tok)
        # if P5.1 fires at all (بَاعَ/صَامَ via normal chain) it must NOT be a snapshot ACCEPT
        if s is not None:
            assert not (s.status == "accepted"
                        and any("hussein_snapshot_v1" in t for t in s.trace_ids)), tok


def test_CC_18_existing_step_c1_examples_unchanged():
    for tok, ct in (("كَتَبَ", "MabniReadinessCandidate"),
                    ("يَقُولُ", "Mu'rabReadinessCandidate"),
                    ("مَكْتُوب", "Mu'rabReadinessCandidate")):
        s = _p5_1(tok)
        assert s and s.status == "accepted" and s.candidate_type == ct, tok
        assert any("hussein_snapshot_v1" in t for t in s.trace_ids), tok
        # these reach P5.1 via the normal chain, NOT the C2 bridge
        assert not _steps(tok, "ClosedCategoryReachabilityQiyas"), tok


def test_CC_19_p3_1_trace_free_of_snapshot():
    for tok in CLOSED_CATEGORY + ("كَتَبَ",):
        for s in _steps(tok, "WeightPatternQiyas"):
            assert not any("hussein_snapshot" in t for t in s.trace_ids), tok


def test_CC_20_weight_pattern_behaviour_unchanged():
    assert all(s.status == "accepted" for s in _steps("كَتَبَ", "WeightPatternQiyas"))
    assert all(s.status == "deferred" for s in _steps("قَالَ", "WeightPatternQiyas"))


def test_CC_21_p6_still_follows_p5_1_non_gating():
    # كَتَبَ reaches P6; closed-category units terminate at P5.1 (no P6 unit) but P5.1
    # being ACCEPT/DEFER never blocks the spine where P6 is reachable.
    order = []
    for r in rq.process_text("كَتَبَ"):
        for s in r.steps:
            if s.layer not in order:
                order.append(s.layer)
    assert order.index("VerbalSignifiedQiyas") > order.index("InflectionalClosureQiyas")


def test_CC_22_registry_19_no_p13_no_layerspec():
    from qiyas_core.slot_geometry_core import master_registry_seed as MRS
    layers = list(MRS.build_master_registry_seed().all_layers())
    assert len(layers) == 19
    assert not any("ClosedCategory" in (s.name + s.id) for s in layers)
    assert not any("InflectionalClosure" in (s.name + s.id) for s in layers)
    assert not any("P13" in n for n in dir(MRS) if n.startswith("LAYER_ID_"))
