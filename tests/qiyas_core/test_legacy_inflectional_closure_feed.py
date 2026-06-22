"""Legacy → P5.1 proposal feed tests (audit-governed; candidate-only).

Proves the Stage A legacy fixtures feed ONLY class / closed-category / safe-verb-kind
evidence into the EXISTING P5.1 adapter; that root/wazn/role/case/relations/events/
meaning are ignored; that suspicious / unsafe entries never ACCEPT; that no external
analyzer is called; and that Qiyas P5.1 — not the legacy analyzer — makes every verdict,
emitting no final judgment.
"""

from __future__ import annotations

import pathlib

import legacy_inflectional_closure_feed as F
import legacy_harness as H


def _provider():
    return F.LegacyInflectionalClosureProposalProvider()


def _verdict(token):
    p = _provider().get(token)
    cs = F.feed_proposal_to_p5_1(p)
    if cs.accepted:
        return "ACCEPT", cs.accepted[0].candidate_type, cs
    if cs.deferred:
        return "DEFER", None, cs
    return "BLOCK", None, cs


# ── class → P5.1 evidence mapping ─────────────────────────────────────────────


def test_LF_01_harf_maps_to_mabni_readiness():
    for t in ("مِن", "إلى", "على"):
        v, ct, _ = _verdict(t)
        assert v == "ACCEPT" and ct == "MabniReadinessCandidate", t


def test_LF_02_ism_mabni_maps_to_mabni_readiness():
    for t in ("هو", "هذا", "ذلكم"):
        v, ct, _ = _verdict(t)
        assert v == "ACCEPT" and ct == "MabniReadinessCandidate", t


def test_LF_03_ism_mawsool_maps_to_mabni_readiness():
    for t in ("الذي", "الذين"):
        v, ct, _ = _verdict(t)
        assert v == "ACCEPT" and ct == "MabniReadinessCandidate", t


def test_LF_04_closed_compounds_map_to_mabni_readiness():
    for t in ("عليه", "منه", "بكم"):
        p = _provider().get(t)
        assert p.p5_1_evidence == {"is_closed_compound": True}
        v, ct, _ = _verdict(t)
        assert v == "ACCEPT" and ct == "MabniReadinessCandidate", t


def test_LF_05_ism_muarab_and_jamid_map_to_murab_when_safe():
    for t in ("رجل", "كتاب", "كاتب"):
        v, ct, _ = _verdict(t)
        assert v == "ACCEPT" and ct == "Mu'rabReadinessCandidate", t


def test_LF_06_fiil_past_and_imperative_via_safe_verb_kind_hint():
    for t in ("كَتَبَ", "اضرب"):
        p = _provider().get(t)
        assert p.p5_1_evidence.get("word_kind") == "verbal"
        assert p.p5_1_evidence.get("verb_tense") in ("past", "imperative")
        v, ct, _ = _verdict(t)
        assert v == "ACCEPT" and ct == "MabniReadinessCandidate", t


def test_LF_07_fiil_present_open_via_safe_verb_kind_hint():
    p = _provider().get("يكتب")
    assert p.p5_1_evidence == {"word_kind": "verbal", "verb_tense": "present"}
    v, ct, _ = _verdict("يكتب")
    assert v == "ACCEPT" and ct == "Mu'rabReadinessCandidate"


# ── suspicious / unsafe must NOT ACCEPT ───────────────────────────────────────


def test_LF_08_suspicious_defer_entries_do_not_accept():
    for t in ("بَاعَ", "صَامَ", "قِيلَ", "يَبِيعُ", "مكتوب"):
        p = _provider().get(t)
        assert p.mapped_candidate_hint == F.DEFER_HINT, t
        assert p.p5_1_evidence == {}, t
        v, _, _ = _verdict(t)
        assert v != "ACCEPT", t  # never ACCEPTs from legacy evidence


def test_LF_09_unsafe_final_looking_role_case_is_ignored_raw_field_only():
    # The L3 role/case is committed (unsafe) — flagged, never fed into P5.1 evidence.
    p = _provider().get("كَاتِب") if False else _provider().get("رجل")
    assert p.unsafe_final_label is True            # role/case flagged unsafe
    assert "role" not in str(p.p5_1_evidence)      # role/case NOT in fed evidence
    assert "case" not in str(p.p5_1_evidence)
    # a noun's role (i'rab) is recorded only as ignored.
    p2 = _provider().get("كتاب")
    assert any("i'rab" in f or "case" in f for f in p2.ignored_fields)


# ── ignored families (root/wazn/role/case/relations/events/meaning/Q&A) ───────


def test_LF_10_root_and_wazn_are_ignored_not_fed():
    for t in ("كتاب", "كاتب", "كَتَبَ"):
        p = _provider().get(t)
        # raw root/wazn retained for audit, but NEVER fed as evidence.
        assert "root" not in str(p.p5_1_evidence) and "wazn" not in str(p.p5_1_evidence)
        assert "legacy_root" in p.ignored_fields and "legacy_wazn" in p.ignored_fields


def test_LF_11_relations_events_meaning_qa_are_ignored():
    p = _provider().get("مِن")
    for fam in ("relations", "events", "speech_act", "resolution/anaphora",
                "meaning_graph", "reasoning/qa"):
        assert fam in p.ignored_fields


# ── no external analyzer call; P5.1 still decides ─────────────────────────────


def test_LF_12_no_external_subprocess_or_analyzer_call_in_feed():
    # Import-graph check (not prose — the docstring legitimately *names* subprocess to
    # state it does NOT use it).
    import ast
    tree = ast.parse(pathlib.Path(F.__file__).read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert "subprocess" not in imported, f"feed must not import subprocess; {imported}"
    # No call into the external analyzer / its dir.
    assert not any(isinstance(n, ast.Attribute) and getattr(n, "attr", "") == "run"
                   and isinstance(n.value, ast.Name) and n.value.id == "subprocess"
                   for n in ast.walk(tree))
    # The provider works fixture-only (no external dir needed).
    assert len(_provider().proposals()) == 34


def test_LF_13_p5_1_defers_when_no_safe_legacy_class_evidence():
    # An ignore/suspicious proposal carries no evidence → P5.1 DEFERs (never guesses).
    for t in ("الله", "بَاعَ"):
        v, _, _ = _verdict(t)
        assert v == "DEFER", t


def test_LF_14_qiyas_makes_the_verdict_proposal_is_only_a_hint():
    # The proposal carries a HINT; the actual candidate_type comes from the P5.1 rule.
    p = _provider().get("مِن")
    assert p.mapped_candidate_hint == F.MABNI_HINT
    cs = F.feed_proposal_to_p5_1(p)
    # P5.1 (not the legacy analyzer) produced the readiness candidate.
    assert cs.accepted and cs.accepted[0].source_rule_id.startswith("inflectional_closure")


# ── no final-judgment leakage across the whole feed ───────────────────────────


_FORBIDDEN = (
    "MabniJudgment", "MurabJudgment", "WordKindFinalJudgment", "IrabFinalDecision",
    "CaseJudgment", "IrabCandidate", "MeaningCandidate", "DalalahCandidate",
    "DalalahJudgment", "IfadahCandidate", "HukmCandidate", "RealityClaim",
    "RealityMapping", "TruthJudgment", "FinalMeaning",
)


def test_LF_15_no_final_judgment_emitted_across_all_proposals():
    types = set()
    for p in _provider().proposals():
        cs = F.feed_proposal_to_p5_1(p)
        types |= {c.candidate_type for c in cs.candidates}
    assert types <= {"MabniReadinessCandidate", "Mu'rabReadinessCandidate",
                     "InflectionalClosureCandidate"}
    assert not (types & set(_FORBIDDEN))


def test_LF_16_proposal_carries_required_provenance_fields():
    p = _provider().get("هو")
    assert p.proposal_source == "legacy_stage_a_fixture"
    assert p.raw_token == "هو" and p.raw_class_label == "ISM_MABNI"
    assert p.mapped_candidate_hint == F.MABNI_HINT
    assert p.consumed_fields and p.ignored_fields
