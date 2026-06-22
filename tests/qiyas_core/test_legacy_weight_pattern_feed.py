"""Legacy → P3.1 proposal feed tests (audit-governed; candidate-only).

Proves the Stage A legacy fixtures feed ONLY root / wazn / weight-alignment / weak-
shadda-hamza-madd-ambiguity evidence into the EXISTING P3.1 WeightPattern adapter; that
class / mabni-mu'rab / word-kind / role / case / relations / events / meaning / Q&A are
ignored raw context; that suspicious / unsafe entries never ACCEPT; that no external
analyzer is called; and that Qiyas P3.1 — not the legacy analyzer — makes every verdict,
emitting no final root/wazn/i'rab/meaning judgment.
"""

from __future__ import annotations

import pathlib

import legacy_weight_pattern_feed as F
import legacy_harness as H


def _provider():
    return F.LegacyWeightPatternProposalProvider()


def _verdict(token):
    p = _provider().get(token)
    cs, raw, gated = F.feed_proposal_to_p3_1(p)
    return gated, raw, cs, p


def _patterns(cs):
    return sorted({x.split(":", 1)[1] for c in cs.candidates
                   for x in c.trace_ids if x.startswith("candidate_weight_pattern:")})


# ── legacy root/wazn → P3.1 weight-pattern proposal evidence (safe sound) ──────


def test_WF_01_safe_sound_examples_map_to_weight_pattern_evidence():
    for t in ("كَتَبَ", "كَاتِب", "مَكْتُوب", "مَكْتَب", "مُسْلِم"):
        p = _provider().get(t)
        assert p.reliability_tag == H.PROPOSAL_EVIDENCE, t
        assert p.mapped_candidate_hint in (F.WEIGHT_PATTERN_HINT, F.ROOT_SLOT_ALIGNMENT_HINT), t
        assert p.p3_1_evidence["surface"] == t
        assert "legacy_root" in p.consumed_fields and "legacy_wazn" in p.consumed_fields


def test_WF_02_katab_is_accept_eligible_only_through_qiyas_checks():
    # The proposal carries only a HINT; the ACCEPT verdict comes from the P3.1 rule.
    gated, raw, cs, p = _verdict("كَتَبَ")
    assert p.mapped_candidate_hint == F.WEIGHT_PATTERN_HINT
    assert gated == "ACCEPT" and raw == "ACCEPT"
    # The accepted candidate is produced by the Qiyas weight-pattern rule, not the legacy.
    assert cs.accepted and cs.accepted[0].source_rule_id.startswith("weight_pattern")
    assert "فَعَلَ" in _patterns(cs)


def test_WF_02b_darab_is_not_in_stage_a_fixtures():
    # HONEST coverage note: ضَرَبَ was never captured into the 34-token Stage A set, so
    # the fixture-only feed has no proposal for it (no fabrication).
    import pytest
    with pytest.raises(KeyError):
        _provider().get("ضَرَبَ")


def test_WF_03_added_letter_forms_map_to_root_slot_alignment_evidence():
    for t in ("كَاتِب", "مَكْتُوب"):
        p = _provider().get(t)
        assert p.mapped_candidate_hint == F.ROOT_SLOT_ALIGNMENT_HINT, t
        assert p.mapped_evidence_kind == "root_slot_and_added_letter_alignment", t
        gated, _, cs, _ = _verdict(t)
        assert gated == "ACCEPT", t
    assert "فَاعِل" in _patterns(_verdict("كَاتِب")[2])
    assert "مَفْعُول" in _patterns(_verdict("مَكْتُوب")[2])


# ── suspicious / weak / hamza / shadda / madd must NOT ACCEPT ──────────────────


def test_WF_04_suspicious_weak_hollow_examples_do_not_accept():
    for t in ("قَالَ", "بَاعَ", "خَافَ", "صَامَ", "قِيلَ", "يَبِيعُ"):
        gated, _, _, p = _verdict(t)
        assert p.reliability_tag == H.SUSPICIOUS_DEFER, t
        assert p.mapped_candidate_hint == F.WEAK_LETTER_DEFER_HINT, t
        assert gated != "ACCEPT", t


def test_WF_05_hamza_shadda_madd_defer_unless_licensed():
    cases = {"مَدَّ": F.SHADDA_DEFER_HINT, "آمَنَ": F.HAMZA_DEFER_HINT}
    for t, hint in cases.items():
        gated, _, _, p = _verdict(t)
        assert p.mapped_candidate_hint == hint, t
        assert gated == "DEFER", t  # P3.1 DEFERs on shadda/hamza; not licensed → not ACCEPT


def test_WF_05b_unvocalized_suspicious_accept_is_gated_down_to_defer():
    # P3.1 structurally aligns مَفْعُول for unvocalized مكتوب, but the legacy proposal is
    # suspicious_defer (wrong root from no vocalization) → the feed must NOT promote it.
    gated, raw, cs, p = _verdict("مكتوب")
    assert p.reliability_tag == H.SUSPICIOUS_DEFER
    assert raw == "ACCEPT"        # P3.1's bare structural alignment
    assert gated == "DEFER"       # gated: suspicious legacy entry never ACCEPTs


# ── this feed consumes ONLY root/wazn; ignores class/role/case/relations/… ─────


def test_WF_06_root_wazn_consumed_only_in_this_bridge_not_in_p5_1_feed():
    # root/wazn are consumed here…
    p = _provider().get("كتاب")
    assert "legacy_root" in p.consumed_fields and "legacy_wazn" in p.consumed_fields
    # …and the SIBLING P5.1 feed explicitly IGNORES root/wazn (consumed only here).
    import legacy_inflectional_closure_feed as P51
    p51 = P51.LegacyInflectionalClosureProposalProvider().get("كتاب")
    assert "legacy_root" in p51.ignored_fields and "legacy_wazn" in p51.ignored_fields
    assert "root" not in str(p51.p5_1_evidence) and "wazn" not in str(p51.p5_1_evidence)


def test_WF_07_class_and_mabni_murab_fields_are_ignored():
    p = _provider().get("هو")  # legacy ISM_MABNI
    for fam in ("legacy_class", "mabni_murab", "word_kind"):
        assert fam in p.ignored_fields, fam
    assert "class" not in str(p.p3_1_evidence) and "mabni" not in str(p.p3_1_evidence)
    assert "word_kind" not in p.p3_1_evidence


def test_WF_08_role_and_case_fields_are_ignored():
    p = _provider().get("رجل")
    for fam in ("grammatical_role", "case/i'rab"):
        assert fam in p.ignored_fields, fam
    assert "role" not in str(p.p3_1_evidence) and "case" not in str(p.p3_1_evidence)


def test_WF_09_relations_events_meaning_qa_fields_are_ignored():
    p = _provider().get("كَتَبَ")
    for fam in ("relations", "events", "speech_act", "resolution/anaphora",
                "meaning_graph", "reasoning/qa"):
        assert fam in p.ignored_fields, fam


# ── no external analyzer call; P3.1 still decides; defers without evidence ─────


def test_WF_10_no_external_subprocess_or_analyzer_call_in_feed():
    import ast
    tree = ast.parse(pathlib.Path(F.__file__).read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert "subprocess" not in imported, f"feed must not import subprocess; {imported}"
    assert not any(isinstance(n, ast.Attribute) and getattr(n, "attr", "") == "run"
                   and isinstance(n.value, ast.Name) and n.value.id == "subprocess"
                   for n in ast.walk(tree))
    assert len(_provider().proposals()) == 34  # fixture-only, no external dir needed


def test_WF_11_p3_1_defers_when_no_safe_root_wazn_evidence():
    # Hollow/weak suspicious surfaces carry no licensed alignment → DEFER (never guess).
    for t in ("قَالَ", "صَامَ", "قِيلَ"):
        gated, _, _, _ = _verdict(t)
        assert gated == "DEFER", t


def test_WF_12_qiyas_makes_the_verdict_proposal_is_only_a_hint():
    p = _provider().get("مَكْتَب")
    assert p.mapped_candidate_hint == F.ROOT_SLOT_ALIGNMENT_HINT
    _, _, cs, _ = _verdict("مَكْتَب")
    assert cs.accepted and all(c.source_rule_id.startswith("weight_pattern")
                               for c in cs.accepted)


# ── no final-judgment leakage across the whole feed ───────────────────────────


_FORBIDDEN = (
    "RootFinalJudgment", "WeightFinalJudgment", "RootJudgment", "WaznJudgment",
    "WordKindFinalJudgment", "IrabFinalDecision", "CaseJudgment", "IrabCandidate",
    "MeaningCandidate", "DalalahCandidate", "DalalahJudgment", "IfadahCandidate",
    "HukmCandidate", "RealityClaim", "TruthJudgment", "FinalMeaning",
)


def test_WF_13_no_final_judgment_emitted_across_all_proposals():
    types = set()
    for p in _provider().proposals():
        cs, _, _ = F.feed_proposal_to_p3_1(p)
        types |= {c.candidate_type for c in cs.candidates}
    assert types <= {"WeightPatternCandidate"}, types
    assert not (types & set(_FORBIDDEN))


def test_WF_14_proposal_carries_required_provenance_fields():
    p = _provider().get("كَتَبَ")
    assert p.proposal_source == "legacy_stage_a_fixture"
    assert p.raw_token == "كَتَبَ" and p.raw_root == "كتب" and p.raw_wazn == "فعل"
    assert p.consumed_fields and p.ignored_fields


# ── governance: auxiliary non-registry; count 19; no P13 ──────────────────────


def test_WF_GOV_01_registry_count_19_no_p13_p3_1_still_auxiliary():
    from qiyas_core.slot_geometry_core import master_registry_seed as MRS
    layers = list(MRS.build_master_registry_seed().all_layers())
    assert len(layers) == 19
    assert not any("WeightPattern" in s.name or "WeightPattern" in s.id for s in layers)
    assert not any("P13" in n for n in dir(MRS) if n.startswith("LAYER_ID_"))


def test_WF_GOV_02_no_runtime_module_imports_this_feed():
    # TEST-SIDE only: no src/qiyas_core or run_qiyas module may reference the feed.
    import ast
    root = pathlib.Path(__file__).resolve().parents[2]
    targets = list((root / "src" / "qiyas_core").rglob("*.py")) + [root / "run_qiyas.py"]
    for path in targets:
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            assert not any("legacy_weight_pattern_feed" in (n or "") or "legacy_harness" in (n or "")
                           for n in names), f"{path} must not import the legacy feed"
