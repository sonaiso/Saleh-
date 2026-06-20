"""SCG-P12 IfadahSpeechForce — behavioral runtime tests. TERMINAL layer.

Narrow SCG-P12 implementation (2026-06-20). Builds a candidate-only ifadah
(speech-force) possibility from a single accepted P11 IrabGeometryCandidate:
IrabGeometryCandidate -> IfadahCandidate.

Candidate-only / structural-only (IFADAH_CONSTITUTION.md + the SCG-P12 spec). THE
HUKM/REALITY FRONTIER: ifadah is the structural POSSIBILITY of a speech force,
NEVER a hukm / reality claim / truth value / final meaning / completed pragmatic
force. NOT HukmCandidate / RealityClaim / RealityMapping / TruthJudgment /
FinalMeaning / IrabFinalDecision. TERMINAL: P12 opens NOTHING and only closes
ifadah_candidates. P12 runs only behind an accepted P11; one accepted P11 candidate
is enough. There is no P13.
"""

from __future__ import annotations

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank, ResidualEffect, ResidualSeverity
from qiyas_core.kernel import QiyasKernel
from qiyas_core.residual import Residual
from qiyas_core.ifadah_adapter import (
    CLOSED_PRIOR_PREFIX,
    IFADAH_GEOMETRY_EVIDENCE_PREFIX,
    IRAB_GEOMETRY_REF_PREFIX,
    OPENED_PRIOR_PREFIX,
    IfadahSpeechForceLayerAdapter,
)
from qiyas_core.rules.ifadah_rules import (
    CARRIED_IRAB_GEOMETRY_RESIDUALS,
    CLOSED_PRIORS,
    COMPLETION_BOUNDARY_UNDERSPECIFIED,
    FINAL_JUDGMENT_ATTEMPTED,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    IFADAH_CONTEXT_UNDERSPECIFIED,
    IFADAH_IDENTITY_UNDERSPECIFIED,
    IFADAH_PRECONDITION_BLOCKED,
    OPENED_PRIORS,
    SPEECH_FORCE_READINESS_UNDERSPECIFIED,
)

import run_qiyas as rq


# ── synthetic accepted-P11 IrabGeometryCandidate builder ──────────────────────


def _p11_irab_geometry(
    *, distinct=2, irab_context_closed=1, irab_position=1, case_marker=1,
    waqf_readiness=1, verdict="accept", with_ig_evidence=True, residuals=(),
    extra_trace=(), with_identity=True,
):
    """Build a synthetic accepted P11 IrabGeometryCandidate as P12 input."""
    ids = []
    if with_identity:
        for u in range(max(distinct, 1)):
            ids.append(f"identity:codepoint:unit{u}")
        ids.append("identity:sentence_geometry_domain")
    trace = [f"irab_unit_identities:distinct={distinct}"]
    if with_ig_evidence:
        trace.append(
            f"irab_geometry_evidence:irab_context_closed={irab_context_closed};"
            f"irab_position={irab_position};case_marker={case_marker};"
            f"waqf_readiness={waqf_readiness};verdict={verdict}"
        )
    trace += list(extra_trace)
    return Candidate(
        candidate_id="accepted:IrabGeometryQiyas:text",
        candidate_type="IrabGeometryCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="IrabGeometryQiyas",
        source_rule_id="irab_geometry.compose",
        asl_id="اصل:irab_geometry_domain",
        far_id="فرع:relation_geometry:x",
        identity_ids=tuple(ids),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=tuple(residuals),
        trace_ids=tuple(trace),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _compose(ig, **kw):
    return IfadahSpeechForceLayerAdapter(kernel=QiyasKernel()).compose(ig, **kw)


def _trace_value(c, prefix):
    for t in c.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ── RUN ───────────────────────────────────────────────────────────────────────


def test_P12_RUN_01_accepts_from_accepted_p11():
    r = _compose(_p11_irab_geometry())
    assert r.accepted and not r.deferred and not r.blocked
    assert r.accepted[0].candidate_type == "IfadahCandidate"


def test_P12_RUN_02_candidate_only_flag():
    assert "CandidateOnly" in _compose(_p11_irab_geometry()).accepted[0].output_flags


# ── ACCEPT (terminal) ─────────────────────────────────────────────────────────


def test_P12_ACCEPT_01_terminal_opens_nothing():
    c = _compose(_p11_irab_geometry()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set() == set(OPENED_PRIORS)  # TERMINAL — opens nothing


def test_P12_ACCEPT_02_closes_ifadah_candidates():
    c = _compose(_p11_irab_geometry()).accepted[0]
    closed = {t[len(CLOSED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(CLOSED_PRIOR_PREFIX)}
    assert closed == set(CLOSED_PRIORS) == {"ifadah_candidates"}


def test_P12_ACCEPT_03_emits_only_ifadah_candidate():
    c = _compose(_p11_irab_geometry()).accepted[0]
    assert c.candidate_type == "IfadahCandidate"


def test_P12_ACCEPT_04_evidence_is_possibility_not_claim():
    ev = _trace_value(_compose(_p11_irab_geometry()).accepted[0], IFADAH_GEOMETRY_EVIDENCE_PREFIX)
    assert ev is not None
    assert "ifadah_context_closed=1" in ev and "speech_force=1" in ev and "completion_boundary=1" in ev
    # possibility only — never a reality/truth/hukm/final claim string
    for claim in ("Hukm", "Reality", "Truth", "FinalMeaning", "marfu", "mansub"):
        assert claim not in ev


def test_P12_ACCEPT_05_carries_irab_geometry_ref():
    ref = _trace_value(_compose(_p11_irab_geometry()).accepted[0], IRAB_GEOMETRY_REF_PREFIX)
    assert ref == "accepted:IrabGeometryQiyas:text"


# ── DEFER (one per under-determined condition) ────────────────────────────────


def test_P12_DEFER_01_ifadah_context_underspecified():
    r = _compose(_p11_irab_geometry(), ifadah_context_closed=False)
    assert r.deferred and f"deferred_{IFADAH_CONTEXT_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P12_DEFER_02_speech_force_readiness_underspecified():
    r = _compose(_p11_irab_geometry(), speech_force_evidence=False)
    assert r.deferred and f"deferred_{SPEECH_FORCE_READINESS_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P12_DEFER_03_completion_boundary_underspecified():
    r = _compose(_p11_irab_geometry(), ifadah_boundary_evidence=False)
    assert r.deferred and f"deferred_{COMPLETION_BOUNDARY_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P12_DEFER_04_carried_irab_geometry_residuals():
    res = (Residual(residual_type="deferred_upstream", severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER, message="upstream", source_rule_id="r",
                    layer="IrabGeometryQiyas", trace_ids=()),)
    r = _compose(_p11_irab_geometry(residuals=res))
    assert r.deferred and f"deferred_{CARRIED_IRAB_GEOMETRY_RESIDUALS}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P12_DEFER_05_ifadah_identity_underspecified():
    r = _compose(_p11_irab_geometry(), ifadah_identity_determined=False)
    assert r.deferred and f"deferred_{IFADAH_IDENTITY_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P12_DEFER_06_mukhatab_context_folds_into_context():
    r = _compose(_p11_irab_geometry(), mukhatab_context_evidence=False)
    assert r.deferred and f"deferred_{IFADAH_CONTEXT_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


# ── BLOCK ─────────────────────────────────────────────────────────────────────


def test_P12_BLOCK_01_ifadah_precondition_blocked_without_irab_geometry():
    r = _compose(_p11_irab_geometry(with_ig_evidence=False))
    assert r.blocked and not r.accepted
    assert any(IFADAH_PRECONDITION_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P12_BLOCK_02_identity_collapse_blocked_single_unit():
    r = _compose(_p11_irab_geometry(distinct=1))
    assert r.blocked and not r.accepted
    assert any(IDENTITY_COLLAPSE_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P12_BLOCK_03_speech_force_conflict():
    r = _compose(_p11_irab_geometry(), speech_force_conflict=True)
    assert r.blocked and not r.accepted
    assert any("speech_force_conflict" in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P12_BLOCK_04_forbidden_output_attempted():
    ig = _p11_irab_geometry(extra_trace=("HukmCandidate",))
    r = _compose(ig)
    assert r.blocked and not r.accepted
    assert any(FORBIDDEN_OUTPUT_ATTEMPTED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P12_BLOCK_05_final_judgment_attempted_frontier_guard():
    # The reality/truth/hukm frontier guard — any attempt to cross is BLOCKED.
    r = _compose(_p11_irab_geometry(), final_judgment_attempted=True)
    assert r.blocked and not r.accepted
    assert any(FINAL_JUDGMENT_ATTEMPTED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


# ── IDENTITY / TRACE ──────────────────────────────────────────────────────────


def test_P12_IDENTITY_01_preserves_irab_geometry_identity():
    c = _compose(_p11_irab_geometry()).accepted[0]
    assert "identity:sentence_geometry_domain" in c.identity_ids


def test_P12_IDENTITY_02_preserves_transitive_multi_unit_structure():
    c = _compose(_p11_irab_geometry(distinct=2)).accepted[0]
    assert "identity:codepoint:unit0" in c.identity_ids
    assert "identity:codepoint:unit1" in c.identity_ids


def test_P12_IDENTITY_03_ifadah_evidence_is_trace_only():
    c = _compose(_p11_irab_geometry()).accepted[0]
    assert any(t.startswith(IFADAH_GEOMETRY_EVIDENCE_PREFIX) for t in c.trace_ids)
    assert not any(iid.startswith(IFADAH_GEOMETRY_EVIDENCE_PREFIX) for iid in c.identity_ids)


def test_P12_IDENTITY_04_identity_trace_disjoint():
    c = _compose(_p11_irab_geometry()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ── NO-LEAKAGE ────────────────────────────────────────────────────────────────


_FORBIDDEN_TYPES = (
    "HukmCandidate", "RealityClaim", "RealityMapping", "TruthJudgment",
    "FinalMeaning", "IrabFinalDecision", "CaseJudgment", "MeaningCandidate",
    "DalalahCandidate", "DalalahJudgment", "SyntaxLabelJudgment",
)


def test_P12_NOLEAK_01_output_is_only_ifadah_candidate():
    for v in (_compose(_p11_irab_geometry()),
              _compose(_p11_irab_geometry(), ifadah_context_closed=False),
              _compose(_p11_irab_geometry(with_ig_evidence=False))):
        for c in v.candidates:
            assert c.candidate_type == "IfadahCandidate"


def test_P12_NOLEAK_02_no_forbidden_type_emitted():
    cands = _compose(_p11_irab_geometry()).candidates
    types = {c.candidate_type for c in cands}
    assert not (types & set(_FORBIDDEN_TYPES))


def test_P12_NOLEAK_03_no_reality_truth_hukm_change_in_trace():
    c = _compose(_p11_irab_geometry()).accepted[0]
    for forbidden in ("assign_reality_claim", "assign_truth_value", "assign_hukm"):
        assert not any(forbidden in t for t in c.trace_ids)


# ── PIPELINE (run_qiyas integration) ──────────────────────────────────────────


def _p12_steps(text):
    reports = rq.process_text(text)
    return [s for r in reports for s in r.steps if s.layer == "IfadahSpeechForceQiyas"]


def _p11_steps(text):
    reports = rq.process_text(text)
    return [s for r in reports for s in r.steps if s.layer == "IrabGeometryQiyas"]


def test_P12_PIPELINE_01_accepts_behind_accepted_p11():
    assert _p11_steps("ضَرَبَ كَتَبَ")[0].status == "accepted"
    p12 = _p12_steps("ضَرَبَ كَتَبَ")
    assert p12 and p12[0].status == "accepted"
    assert p12[0].candidate_type == "IfadahCandidate"


def test_P12_PIPELINE_02_only_behind_accepted_p11():
    assert _p11_steps("ضَرَبَ") == []
    assert _p12_steps("ضَرَبَ") == []


def test_P12_PIPELINE_03_terminal_opens_nothing():
    p12 = _p12_steps("ضَرَبَ كَتَبَ")[0]
    opened = {t.split(":", 1)[1] for t in p12.trace_ids if t.startswith("opens_prior:")}
    assert opened == set()  # TERMINAL — no P13
    assert p12.candidate_type == "IfadahCandidate"


# ── EXPANDED PROBES ───────────────────────────────────────────────────────────


def _types(text):
    return {s.candidate_type for r in rq.process_text(text) for s in r.steps}


_PROBE_FORBIDDEN = (
    "HukmCandidate", "RealityClaim", "RealityMapping", "TruthJudgment",
    "FinalMeaning", "IrabFinalDecision", "CaseJudgment", "MeaningCandidate",
    "DalalahCandidate",
)


def test_P12_PROBE_01_verb_positives_reach_p12_accept():
    for txt in ("ضَرَبَ كَتَبَ", "كَتَبَ ضَرَبَ", "ضَرَبَ كَتَبَ فَعَلَ"):
        assert _p11_steps(txt)[0].status == "accepted", txt
        p12 = _p12_steps(txt)
        assert p12 and p12[0].status == "accepted", txt
        # TERMINAL — opens nothing on any positive probe.
        opened = {t.split(":", 1)[1] for t in p12[0].trace_ids if t.startswith("opens_prior:")}
        assert opened == set(), txt


def test_P12_PROBE_02_three_verb_preserves_ordered_units():
    p12 = _p12_steps("ضَرَبَ كَتَبَ فَعَلَ")[0]
    distinct = None
    for t in p12.trace_ids:
        if t.startswith("ifadah_unit_identities:distinct="):
            distinct = int(t.split("distinct=", 1)[1])
    assert distinct == 3  # transitive multi-unit identity not collapsed


def test_P12_PROBE_03_negatives_do_not_fabricate_p12():
    for txt in ("ضَرَبَ", "كَتَبَ زَيْدٌ", "ضَرَبَ زَيْدٌ عَمْرًا",
                "جَاءَ زَيْدٌ وَعَمْرٌ", "فَسَيَكفِكَهُم"):
        assert _p12_steps(txt) == [], txt
        assert "IfadahCandidate" not in _types(txt), txt


def test_P12_PROBE_04_no_final_object_leakage_across_all_probes():
    for txt in ("ضَرَبَ", "ضَرَبَ كَتَبَ", "كَتَبَ ضَرَبَ", "ضَرَبَ كَتَبَ فَعَلَ",
                "كَتَبَ زَيْدٌ", "ضَرَبَ زَيْدٌ عَمْرًا", "جَاءَ زَيْدٌ وَعَمْرٌ",
                "فَسَيَكفِكَهُم"):
        leak = _types(txt) & set(_PROBE_FORBIDDEN)
        assert not leak, (txt, leak)
