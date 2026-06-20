"""SCG-P11 IrabGeometry — behavioral runtime tests.

Narrow SCG-P11 implementation (2026-06-20). Refines a candidate-only i'rab-position
geometry from a single accepted P10 RelationGeometryCandidate:
RelationGeometryCandidate -> IrabGeometryCandidate.

Candidate-only / structural-only (IRAB_GEOMETRY_CONSTITUTION.md + the SCG-P11
design gate / design resolution). THE JUDGMENT-ADJACENCY BOUNDARY: i'rab POSITIONS
and possibilities only, NEVER an i'rab judgment. case_marker_evidence is NOT
CaseJudgment; irab_position_evidence is NOT IrabFinalDecision. NOT ifadah / hukm /
reality / meaning / dalalah / final-syntax, NOT any P12 candidate. Opens ONLY
ifadah_speech_force_candidates (ACCEPT) and closes irab_geometry_candidates. P11
runs only behind an accepted P10; one accepted P10 candidate is enough.
"""

from __future__ import annotations

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank, ResidualEffect, ResidualSeverity
from qiyas_core.kernel import QiyasKernel
from qiyas_core.residual import Residual
from qiyas_core.irab_geometry_adapter import (
    CLOSED_PRIOR_PREFIX,
    IRAB_GEOMETRY_EVIDENCE_PREFIX,
    OPENED_PRIOR_PREFIX,
    RELATION_GEOMETRY_REF_PREFIX,
    IrabGeometryLayerAdapter,
)
from qiyas_core.rules.irab_geometry_rules import (
    CARRIED_RELATION_GEOMETRY_RESIDUALS,
    CASE_MARKER_UNDERSPECIFIED,
    CLOSED_PRIORS,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    IRAB_CONTEXT_UNDERSPECIFIED,
    IRAB_IDENTITY_UNDERSPECIFIED,
    IRAB_POSITION_UNDERSPECIFIED,
    IRAB_CONTEXT_BLOCKED,
    OPENED_PRIORS,
    WAQF_READINESS_UNDERSPECIFIED,
)

import run_qiyas as rq


# ── synthetic accepted-P10 RelationGeometryCandidate builder ──────────────────


def _p10_relation_geometry(
    *, distinct=2, relation_scope_closed=1, relation_type=1, dependency_scope=1,
    verdict="accept", with_rg_evidence=True, residuals=(), extra_trace=(),
    with_identity=True,
):
    """Build a synthetic accepted P10 RelationGeometryCandidate as P11 input."""
    ids = []
    if with_identity:
        for u in range(max(distinct, 1)):
            ids.append(f"identity:codepoint:unit{u}")
        ids.append("identity:sentence_geometry_domain")
    trace = [f"relation_unit_identities:distinct={distinct}"]
    if with_rg_evidence:
        trace.append(
            f"relation_geometry_evidence:relation_scope_closed={relation_scope_closed};"
            f"relation_type={relation_type};dependency_scope={dependency_scope};"
            f"verdict={verdict}"
        )
    trace += list(extra_trace)
    return Candidate(
        candidate_id="accepted:RelationGeometryQiyas:text",
        candidate_type="RelationGeometryCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="RelationGeometryQiyas",
        source_rule_id="relation_geometry.compose",
        asl_id="اصل:relation_geometry_domain",
        far_id="فرع:sentence_geometry:x",
        identity_ids=tuple(ids),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=tuple(residuals),
        trace_ids=tuple(trace),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _compose(rg, **kw):
    return IrabGeometryLayerAdapter(kernel=QiyasKernel()).compose(rg, **kw)


def _trace_value(c, prefix):
    for t in c.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ── RUN ───────────────────────────────────────────────────────────────────────


def test_P11_RUN_01_accepts_from_accepted_p10():
    r = _compose(_p10_relation_geometry())
    assert r.accepted and not r.deferred and not r.blocked
    assert r.accepted[0].candidate_type == "IrabGeometryCandidate"


def test_P11_RUN_02_candidate_only_flag():
    assert "CandidateOnly" in _compose(_p10_relation_geometry()).accepted[0].output_flags


# ── ACCEPT ────────────────────────────────────────────────────────────────────


def test_P11_ACCEPT_01_opens_only_ifadah_speech_force_prior():
    c = _compose(_p10_relation_geometry()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"ifadah_speech_force_candidates"}


def test_P11_ACCEPT_02_closes_irab_geometry_prior():
    c = _compose(_p10_relation_geometry()).accepted[0]
    closed = {t[len(CLOSED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(CLOSED_PRIOR_PREFIX)}
    assert closed == set(CLOSED_PRIORS) == {"irab_geometry_candidates"}


def test_P11_ACCEPT_03_does_not_emit_ifadah_candidate():
    c = _compose(_p10_relation_geometry()).accepted[0]
    assert c.candidate_type == "IrabGeometryCandidate"
    assert "IfadahCandidate" not in c.candidate_type


def test_P11_ACCEPT_04_evidence_is_structural_positions_not_verdict():
    ev = _trace_value(_compose(_p10_relation_geometry()).accepted[0], IRAB_GEOMETRY_EVIDENCE_PREFIX)
    assert ev is not None
    assert "irab_context_closed=1" in ev and "irab_position=1" in ev
    assert "case_marker=1" in ev and "waqf_readiness=1" in ev
    # geometry of possibilities — never a marfu'/mansub/... verdict string
    for verdict_word in ("marfu", "mansub", "majrur", "majzum", "CaseJudgment", "IrabFinalDecision"):
        assert verdict_word not in ev


def test_P11_ACCEPT_05_carries_relation_geometry_ref():
    ref = _trace_value(_compose(_p10_relation_geometry()).accepted[0], RELATION_GEOMETRY_REF_PREFIX)
    assert ref == "accepted:RelationGeometryQiyas:text"


# ── DEFER (one per under-determined condition) ────────────────────────────────


def test_P11_DEFER_01_irab_context_underspecified():
    r = _compose(_p10_relation_geometry(), irab_context_closed=False)
    assert r.deferred and f"deferred_{IRAB_CONTEXT_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P11_DEFER_02_irab_position_underspecified():
    r = _compose(_p10_relation_geometry(), irab_position_evidence=False)
    assert r.deferred and f"deferred_{IRAB_POSITION_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P11_DEFER_03_case_marker_underspecified():
    r = _compose(_p10_relation_geometry(), case_marker_evidence=False)
    assert r.deferred and f"deferred_{CASE_MARKER_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P11_DEFER_04_waqf_readiness_underspecified():
    r = _compose(_p10_relation_geometry(), waqf_readiness_evidence=False)
    assert r.deferred and f"deferred_{WAQF_READINESS_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P11_DEFER_05_carried_relation_geometry_residuals():
    res = (Residual(residual_type="deferred_upstream", severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER, message="upstream", source_rule_id="r",
                    layer="RelationGeometryQiyas", trace_ids=()),)
    r = _compose(_p10_relation_geometry(residuals=res))
    assert r.deferred and f"deferred_{CARRIED_RELATION_GEOMETRY_RESIDUALS}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P11_DEFER_06_irab_identity_underspecified():
    r = _compose(_p10_relation_geometry(), irab_identity_determined=False)
    assert r.deferred and f"deferred_{IRAB_IDENTITY_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


# ── BLOCK ─────────────────────────────────────────────────────────────────────


def test_P11_BLOCK_01_irab_context_blocked_without_relation_geometry():
    # No relation-geometry evidence marker -> no usable P10 i'rab context.
    r = _compose(_p10_relation_geometry(with_rg_evidence=False))
    assert r.blocked and not r.accepted
    assert any(IRAB_CONTEXT_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P11_BLOCK_02_identity_collapse_blocked_single_unit():
    # Relation geometry present but multi-unit identity collapsed to <2 distinct.
    r = _compose(_p10_relation_geometry(distinct=1))
    assert r.blocked and not r.accepted
    assert any(IDENTITY_COLLAPSE_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P11_BLOCK_03_irab_position_conflict():
    r = _compose(_p10_relation_geometry(), irab_position_conflict=True)
    assert r.blocked and not r.accepted
    assert any("irab_position_conflict" in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P11_BLOCK_04_forbidden_output_attempted():
    rg = _p10_relation_geometry(extra_trace=("IfadahCandidate",))
    r = _compose(rg)
    assert r.blocked and not r.accepted
    assert any(FORBIDDEN_OUTPUT_ATTEMPTED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


# ── IDENTITY / TRACE ──────────────────────────────────────────────────────────


def test_P11_IDENTITY_01_preserves_relation_geometry_identity():
    c = _compose(_p10_relation_geometry()).accepted[0]
    assert "identity:sentence_geometry_domain" in c.identity_ids


def test_P11_IDENTITY_02_preserves_transitive_multi_unit_structure():
    c = _compose(_p10_relation_geometry(distinct=2)).accepted[0]
    assert "identity:codepoint:unit0" in c.identity_ids
    assert "identity:codepoint:unit1" in c.identity_ids


def test_P11_IDENTITY_03_irab_evidence_is_trace_only():
    c = _compose(_p10_relation_geometry()).accepted[0]
    assert any(t.startswith(IRAB_GEOMETRY_EVIDENCE_PREFIX) for t in c.trace_ids)
    assert not any(iid.startswith(IRAB_GEOMETRY_EVIDENCE_PREFIX) for iid in c.identity_ids)


def test_P11_IDENTITY_04_identity_trace_disjoint():
    c = _compose(_p10_relation_geometry()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ── NO-LEAKAGE ────────────────────────────────────────────────────────────────


_FORBIDDEN_TYPES = (
    "IfadahCandidate", "CaseJudgment", "IrabFinalDecision", "IrabCandidate",
    "MeaningCandidate", "DalalahCandidate", "DalalahJudgment", "HukmCandidate",
    "RealityClaim", "FinalMeaning", "SyntaxLabelJudgment",
)


def test_P11_NOLEAK_01_output_is_only_irab_geometry_candidate():
    for v in (_compose(_p10_relation_geometry()),
              _compose(_p10_relation_geometry(), irab_context_closed=False),
              _compose(_p10_relation_geometry(with_rg_evidence=False))):
        for c in v.candidates:
            assert c.candidate_type == "IrabGeometryCandidate"


def test_P11_NOLEAK_02_no_forbidden_type_emitted():
    cands = _compose(_p10_relation_geometry()).candidates
    types = {c.candidate_type for c in cands}
    assert not (types & set(_FORBIDDEN_TYPES))


def test_P11_NOLEAK_03_no_irab_case_ifadah_hukm_change_in_trace():
    c = _compose(_p10_relation_geometry()).accepted[0]
    for forbidden in ("assign_case_judgment", "assign_ifadah", "assign_hukm"):
        assert not any(forbidden in t for t in c.trace_ids)


# ── PIPELINE (run_qiyas integration) ──────────────────────────────────────────


def _p11_steps(text):
    reports = rq.process_text(text)
    return [s for r in reports for s in r.steps if s.layer == "IrabGeometryQiyas"]


def _p10_steps(text):
    reports = rq.process_text(text)
    return [s for r in reports for s in r.steps if s.layer == "RelationGeometryQiyas"]


def test_P11_PIPELINE_01_accepts_behind_accepted_p10():
    assert _p10_steps("ضَرَبَ كَتَبَ")[0].status == "accepted"
    p11 = _p11_steps("ضَرَبَ كَتَبَ")
    assert p11 and p11[0].status == "accepted"
    assert p11[0].candidate_type == "IrabGeometryCandidate"


def test_P11_PIPELINE_02_only_behind_accepted_p10():
    # Single word -> no P10 -> no P11 step at all.
    assert _p10_steps("ضَرَبَ") == []
    assert _p11_steps("ضَرَبَ") == []


def test_P11_PIPELINE_03_opens_only_ifadah_prior_not_p12():
    p11 = _p11_steps("ضَرَبَ كَتَبَ")[0]
    opened = {t.split(":", 1)[1] for t in p11.trace_ids if t.startswith("opens_prior:")}
    assert opened == {"ifadah_speech_force_candidates"}
    assert p11.candidate_type == "IrabGeometryCandidate"


# ── EXPANDED PROBES ───────────────────────────────────────────────────────────


def _types(text):
    return {s.candidate_type for r in rq.process_text(text) for s in r.steps}


# IfadahCandidate (SCG-P12, terminal) is now licensed behind accepted P11, so it is
# no longer forbidden in the full pipeline; every case/verdict/meaning/hukm/reality/
# final object remains forbidden.
_PROBE_FORBIDDEN = (
    "CaseJudgment", "IrabFinalDecision", "IrabCandidate",
    "MeaningCandidate", "DalalahCandidate", "HukmCandidate", "RealityClaim", "FinalMeaning",
)


def test_P11_PROBE_01_verb_positives_reach_p11_accept():
    # Same P10-positive verb structures are the initial P11-positive surface.
    for txt in ("ضَرَبَ كَتَبَ", "كَتَبَ ضَرَبَ", "ضَرَبَ كَتَبَ فَعَلَ"):
        assert _p10_steps(txt)[0].status == "accepted", txt
        p11 = _p11_steps(txt)
        assert p11 and p11[0].status == "accepted", txt
        opened = {t.split(":", 1)[1] for t in p11[0].trace_ids if t.startswith("opens_prior:")}
        assert opened == {"ifadah_speech_force_candidates"}, txt


def test_P11_PROBE_02_three_verb_preserves_ordered_units():
    p11 = _p11_steps("ضَرَبَ كَتَبَ فَعَلَ")[0]
    distinct = None
    for t in p11.trace_ids:
        if t.startswith("irab_unit_identities:distinct="):
            distinct = int(t.split("distinct=", 1)[1])
    assert distinct == 3  # transitive multi-unit identity not collapsed


def test_P11_PROBE_03_negatives_do_not_fabricate_p11():
    # No accepted P10 -> no P11 (no fabricated i'rab geometry).
    for txt in ("ضَرَبَ", "كَتَبَ زَيْدٌ", "ضَرَبَ زَيْدٌ عَمْرًا",
                "جَاءَ زَيْدٌ وَعَمْرٌ", "فَسَيَكفِكَهُم"):
        assert _p11_steps(txt) == [], txt
        assert "IrabGeometryCandidate" not in _types(txt), txt


def test_P11_PROBE_04_no_leakage_across_all_probes():
    for txt in ("ضَرَبَ", "ضَرَبَ كَتَبَ", "كَتَبَ ضَرَبَ", "ضَرَبَ كَتَبَ فَعَلَ",
                "كَتَبَ زَيْدٌ", "ضَرَبَ زَيْدٌ عَمْرًا", "جَاءَ زَيْدٌ وَعَمْرٌ",
                "فَسَيَكفِكَهُم"):
        leak = _types(txt) & set(_PROBE_FORBIDDEN)
        assert not leak, (txt, leak)
