"""SCG-P10 RelationGeometry — behavioral runtime tests.

Narrow SCG-P10 implementation (2026-06-20). Refines a candidate-only relation
geometry from a single accepted P9 SentenceGeometryCandidate:
SentenceGeometryCandidate -> RelationGeometryCandidate.

Candidate-only / structural-only (RELATION_GEOMETRY_CONSTITUTION.md + the SCG-P10
design gate / design resolution): NOT i'rab/case (IrabCandidate/CaseJudgment
forbidden), NOT ifadah, NOT meaning/dalalah/final-syntax/hukm/reality, NOT any
P11+ candidate. Opens ONLY irab_geometry_candidates (ACCEPT) and closes
relation_geometry_candidates. P10 does NOT re-prove sentencehood (≥2 distinct units
already enforced at P9); one accepted P9 candidate is enough.
"""

from __future__ import annotations

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank, ResidualEffect, ResidualSeverity
from qiyas_core.kernel import QiyasKernel
from qiyas_core.residual import Residual
from qiyas_core.relation_geometry_adapter import (
    CLOSED_PRIOR_PREFIX,
    OPENED_PRIOR_PREFIX,
    RELATION_GEOMETRY_EVIDENCE_PREFIX,
    SENTENCE_GEOMETRY_REF_PREFIX,
    RelationGeometryLayerAdapter,
)
from qiyas_core.rules.relation_geometry_rules import (
    CARRIED_SENTENCE_GEOMETRY_RESIDUALS,
    CLOSED_PRIORS,
    DEPENDENCY_SCOPE_UNDERSPECIFIED,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    OPENED_PRIORS,
    RELATION_IDENTITY_UNDERSPECIFIED,
    RELATION_SCOPE_UNDERSPECIFIED,
    RELATION_STRUCTURE_BLOCKED,
    RELATION_TYPE_UNDERSPECIFIED,
)

import run_qiyas as rq


# ── synthetic accepted-P9 SentenceGeometryCandidate builder ───────────────────


def _p9_sentence_geometry(
    *, units=2, distinct=2, adjacency=1, boundary=1, verdict="accept",
    with_sg_evidence=True, residuals=(), extra_trace=(), with_identity=True,
):
    """Build a synthetic accepted P9 SentenceGeometryCandidate as P10 input."""
    ids = []
    if with_identity:
        # Two distinct unit identities (ordered multi-unit structure from P9).
        for u in range(max(distinct, 1)):
            ids.append(f"identity:codepoint:unit{u}")
        ids.append("identity:sentence_geometry_domain")
    unit_tuple = ";".join(f"u{u}=[unit{u}]" for u in range(max(distinct, 1)))
    trace = [f"sentence_unit_identities:{unit_tuple}"]
    if with_sg_evidence:
        trace.append(
            f"sentence_geometry_evidence:units={units};distinct={distinct};"
            f"adjacency={adjacency};boundary={boundary};verdict={verdict}"
        )
    trace += list(extra_trace)
    return Candidate(
        candidate_id="accepted:SentenceGeometryQiyas:text",
        candidate_type="SentenceGeometryCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SentenceGeometryQiyas",
        source_rule_id="sentence_geometry.compose",
        asl_id="اصل:sentence_geometry_domain",
        far_id="فرع:amil_mamul_units:x",
        identity_ids=tuple(ids),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=tuple(residuals),
        trace_ids=tuple(trace),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _compose(sg, **kw):
    return RelationGeometryLayerAdapter(kernel=QiyasKernel()).compose(sg, **kw)


def _trace_value(c, prefix):
    for t in c.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ── RUN ───────────────────────────────────────────────────────────────────────


def test_P10_RUN_01_accepts_from_accepted_p9():
    r = _compose(_p9_sentence_geometry())
    assert r.accepted and not r.deferred and not r.blocked
    assert r.accepted[0].candidate_type == "RelationGeometryCandidate"


def test_P10_RUN_02_candidate_only_flag():
    assert "CandidateOnly" in _compose(_p9_sentence_geometry()).accepted[0].output_flags


# ── ACCEPT ────────────────────────────────────────────────────────────────────


def test_P10_ACCEPT_01_opens_only_irab_geometry_prior():
    c = _compose(_p9_sentence_geometry()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"irab_geometry_candidates"}


def test_P10_ACCEPT_02_closes_relation_geometry_prior():
    c = _compose(_p9_sentence_geometry()).accepted[0]
    closed = {t[len(CLOSED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(CLOSED_PRIOR_PREFIX)}
    assert closed == set(CLOSED_PRIORS) == {"relation_geometry_candidates"}


def test_P10_ACCEPT_03_does_not_emit_irab_geometry_candidate():
    c = _compose(_p9_sentence_geometry()).accepted[0]
    assert c.candidate_type == "RelationGeometryCandidate"
    assert "IrabGeometryCandidate" not in c.candidate_type


def test_P10_ACCEPT_04_evidence_is_structural():
    ev = _trace_value(_compose(_p9_sentence_geometry()).accepted[0], RELATION_GEOMETRY_EVIDENCE_PREFIX)
    assert ev is not None
    assert "relation_scope_closed=1" in ev and "relation_type=1" in ev and "dependency_scope=1" in ev


def test_P10_ACCEPT_05_carries_sentence_geometry_ref():
    ref = _trace_value(_compose(_p9_sentence_geometry()).accepted[0], SENTENCE_GEOMETRY_REF_PREFIX)
    assert ref == "accepted:SentenceGeometryQiyas:text"


# ── DEFER (one per under-determined condition) ────────────────────────────────


def test_P10_DEFER_01_relation_scope_underspecified():
    r = _compose(_p9_sentence_geometry(), relation_scope_closed=False)
    assert r.deferred and f"deferred_{RELATION_SCOPE_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P10_DEFER_02_relation_type_underspecified():
    r = _compose(_p9_sentence_geometry(), relation_type_evidence=False)
    assert r.deferred and f"deferred_{RELATION_TYPE_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P10_DEFER_03_dependency_scope_underspecified():
    r = _compose(_p9_sentence_geometry(), dependency_scope_evidence=False)
    assert r.deferred and f"deferred_{DEPENDENCY_SCOPE_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P10_DEFER_04_carried_sentence_geometry_residuals():
    res = (Residual(residual_type="deferred_upstream", severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER, message="upstream", source_rule_id="r",
                    layer="SentenceGeometryQiyas", trace_ids=()),)
    r = _compose(_p9_sentence_geometry(residuals=res))
    assert r.deferred and f"deferred_{CARRIED_SENTENCE_GEOMETRY_RESIDUALS}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P10_DEFER_05_relation_identity_underspecified():
    r = _compose(_p9_sentence_geometry(), relation_identity_determined=False)
    assert r.deferred and f"deferred_{RELATION_IDENTITY_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


# ── BLOCK ─────────────────────────────────────────────────────────────────────


def test_P10_BLOCK_01_relation_structure_blocked_without_sentence_geometry():
    # No sentence-geometry evidence marker -> no usable P9 structure.
    r = _compose(_p9_sentence_geometry(with_sg_evidence=False))
    assert r.blocked and not r.accepted
    assert any(RELATION_STRUCTURE_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P10_BLOCK_02_identity_collapse_blocked_single_unit():
    # Sentence geometry present but multi-unit identity collapsed to <2 distinct.
    r = _compose(_p9_sentence_geometry(units=1, distinct=1))
    assert r.blocked and not r.accepted
    assert any(IDENTITY_COLLAPSE_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P10_BLOCK_03_relation_type_conflict():
    r = _compose(_p9_sentence_geometry(), relation_type_conflict=True)
    assert r.blocked and not r.accepted
    assert any("relation_type_conflict" in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_P10_BLOCK_04_forbidden_output_attempted():
    sg = _p9_sentence_geometry(extra_trace=("IrabGeometryCandidate",))
    r = _compose(sg)
    assert r.blocked and not r.accepted
    assert any(FORBIDDEN_OUTPUT_ATTEMPTED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


# ── IDENTITY / TRACE ──────────────────────────────────────────────────────────


def test_P10_IDENTITY_01_preserves_sentence_geometry_identity():
    sg = _p9_sentence_geometry()
    c = _compose(sg).accepted[0]
    assert "identity:sentence_geometry_domain" in c.identity_ids


def test_P10_IDENTITY_02_preserves_ordered_multi_unit_structure():
    sg = _p9_sentence_geometry(distinct=2)
    c = _compose(sg).accepted[0]
    # Both unit identities survive — not collapsed into one relation identity.
    assert "identity:codepoint:unit0" in c.identity_ids
    assert "identity:codepoint:unit1" in c.identity_ids


def test_P10_IDENTITY_03_relation_evidence_is_trace_only():
    c = _compose(_p9_sentence_geometry()).accepted[0]
    # relation-geometry evidence lives in trace, never identity.
    assert any(t.startswith(RELATION_GEOMETRY_EVIDENCE_PREFIX) for t in c.trace_ids)
    assert not any(iid.startswith(RELATION_GEOMETRY_EVIDENCE_PREFIX) for iid in c.identity_ids)


def test_P10_IDENTITY_04_identity_trace_disjoint():
    c = _compose(_p9_sentence_geometry()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ── NO-LEAKAGE ────────────────────────────────────────────────────────────────


_FORBIDDEN_TYPES = (
    "IrabGeometryCandidate", "IfadahCandidate", "IrabCandidate", "CaseJudgment",
    "MeaningCandidate", "DalalahCandidate", "DalalahJudgment", "HukmCandidate",
    "RealityClaim", "FinalMeaning", "SyntaxLabelJudgment",
)


def test_P10_NOLEAK_01_output_is_only_relation_geometry_candidate():
    for v in (_compose(_p9_sentence_geometry()),
              _compose(_p9_sentence_geometry(), relation_scope_closed=False),
              _compose(_p9_sentence_geometry(with_sg_evidence=False))):
        for c in v.candidates:
            assert c.candidate_type == "RelationGeometryCandidate"


def test_P10_NOLEAK_02_no_forbidden_type_emitted():
    cands = _compose(_p9_sentence_geometry()).candidates
    types = {c.candidate_type for c in cands}
    assert not (types & set(_FORBIDDEN_TYPES))


def test_P10_NOLEAK_03_no_irab_case_change_in_trace():
    c = _compose(_p9_sentence_geometry()).accepted[0]
    for forbidden in ("assign_irab", "assign_case", "assign_ifadah"):
        assert not any(forbidden in t for t in c.trace_ids)


# ── PIPELINE (run_qiyas integration) ──────────────────────────────────────────


def _p10_steps(text):
    reports = rq.process_text(text)
    return [s for r in reports for s in r.steps if s.layer == "RelationGeometryQiyas"]


def _p9_steps(text):
    reports = rq.process_text(text)
    return [s for r in reports for s in r.steps if s.layer == "SentenceGeometryQiyas"]


def test_P10_PIPELINE_01_accepts_behind_accepted_p9():
    p9 = _p9_steps("ضَرَبَ كَتَبَ")
    p10 = _p10_steps("ضَرَبَ كَتَبَ")
    assert p9 and p9[0].status == "accepted"
    assert p10 and p10[0].status == "accepted"
    assert p10[0].candidate_type == "RelationGeometryCandidate"


def test_P10_PIPELINE_02_only_behind_accepted_p9():
    # Single word -> P9 BLOCK -> no P10 step at all.
    assert _p9_steps("ضَرَبَ")[0].status == "blocked"
    assert _p10_steps("ضَرَبَ") == []


def test_P10_PIPELINE_03_opens_only_irab_prior_not_p11():
    p10 = _p10_steps("ضَرَبَ كَتَبَ")[0]
    opened = {t.split(":", 1)[1] for t in p10.trace_ids if t.startswith("opens_prior:")}
    assert opened == {"irab_geometry_candidates"}
    # P10 never emits IrabGeometryCandidate or any P11/P12 object.
    assert p10.candidate_type == "RelationGeometryCandidate"


# ── LADDER PROBE (expanded Arabic structural coverage) ────────────────────────
#
# Only verb-signified words currently reach accepted P8 evidence (the P6
# VerbalSignified gate admits verbs, not nouns), so only ≥2 distinct VERB units
# form ≥2 P9 units. Noun-bearing / single-word / complex-word inputs therefore do
# NOT fabricate sentencehood — they honestly stop before P9 ACCEPT and produce no
# P10 step. These probes lock in BOTH the genuine multi-unit P10 ACCEPT path and
# the honest no-fabrication path. (Runtime is unchanged; tests only.)

# IrabGeometryCandidate (SCG-P11) is now licensed behind accepted P10, so it is no
# longer forbidden in the full pipeline; P12 (IfadahCandidate) + semantic/verdict
# objects remain forbidden.
_PROBE_FORBIDDEN = (
    "IfadahCandidate", "CaseJudgment", "IrabFinalDecision", "IrabCandidate",
    "MeaningCandidate", "DalalahCandidate", "DalalahJudgment", "HukmCandidate",
    "RealityClaim", "FinalMeaning", "SyntaxLabelJudgment",
)


def _types(text):
    return {s.candidate_type for r in rq.process_text(text) for s in r.steps}


def _p10_distinct_units(step):
    for t in step.trace_ids:
        if t.startswith("relation_unit_identities:distinct="):
            return int(t.split("distinct=", 1)[1])
    return 0


def test_P10_PROBE_01_new_two_verb_positive_accepts():
    # New two-word positive (distinct from the original probe): two verbs.
    txt = "كَتَبَ ضَرَبَ"
    assert _p9_steps(txt)[0].status == "accepted"
    p10 = _p10_steps(txt)
    assert p10 and p10[0].status == "accepted"
    assert p10[0].candidate_type == "RelationGeometryCandidate"
    opened = {t.split(":", 1)[1] for t in p10[0].trace_ids if t.startswith("opens_prior:")}
    assert opened == {"irab_geometry_candidates"}


def test_P10_PROBE_02_three_verb_positive_preserves_ordered_units():
    # Three-word positive: ordered multi-unit identity preserved across 3 units.
    txt = "ضَرَبَ كَتَبَ فَعَلَ"
    assert _p9_steps(txt)[0].status == "accepted"
    p10 = _p10_steps(txt)[0]
    assert p10.status == "accepted"
    assert _p10_distinct_units(p10) == 3  # not collapsed into one relation identity
    closed = {t.split(":", 1)[1] for t in p10.trace_ids if t.startswith("closes_prior:")}
    assert closed == {"relation_geometry_candidates"}


def test_P10_PROBE_03_noun_bearing_input_does_not_fabricate_p10():
    # كَتَبَ زَيْدٌ: زَيْدٌ is a noun and does not reach accepted P8, so only one P9
    # unit forms -> P9 BLOCK, NO P10 step (no fabricated sentencehood/relation).
    assert _p9_steps("كَتَبَ زَيْدٌ")[0].status == "blocked"
    assert _p10_steps("كَتَبَ زَيْدٌ") == []
    assert "RelationGeometryCandidate" not in _types("كَتَبَ زَيْدٌ")


def test_P10_PROBE_04_complex_single_word_no_p9_or_p10():
    # A single complex word must not create sentencehood: no P9 ACCEPT, no P10.
    txt = "فَسَيَكفِكَهُم"
    assert all(s.status != "accepted" for s in _p9_steps(txt))
    assert _p10_steps(txt) == []


def test_P10_PROBE_05_no_leakage_across_all_probes():
    for txt in ("ضَرَبَ", "ضَرَبَ كَتَبَ", "كَتَبَ ضَرَبَ", "ضَرَبَ كَتَبَ فَعَلَ",
                "كَتَبَ زَيْدٌ", "ضَرَبَ زَيْدٌ عَمْرًا", "جَاءَ زَيْدٌ وَعَمْرٌ",
                "فَسَيَكفِكَهُم"):
        leak = _types(txt) & set(_PROBE_FORBIDDEN)
        assert not leak, (txt, leak)
