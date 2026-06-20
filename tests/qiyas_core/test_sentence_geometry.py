"""SCG-P9 SentenceGeometry — behavioral runtime tests (FIRST multi-unit layer).

Narrow SCG-P9 implementation (2026-06-20). Composes a candidate-only sentence
geometry from >=2 distinct word/segment-level units, each with accepted P8
AmilMamulCandidate evidence: AmilMamulCandidate (units) -> SentenceGeometryCandidate.

Candidate-only / structural-only (SENTENCE_GEOMETRY_CONSTITUTION.md + the SCG-P9
design gate / design resolution): NOT i'rab/case (IrabCandidate/CaseJudgment
forbidden), NOT ifadah, NOT meaning/dalalah/final-syntax/hukm/reality, NOT any
P10+ candidate. Opens ONLY relation_geometry_candidates (ACCEPT). CRITICAL: a
single word is ONE unit even with multiple internal P8 accepts; ACCEPT requires
>=2 distinct units.
"""

from __future__ import annotations

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank, ResidualEffect, ResidualSeverity
from qiyas_core.kernel import QiyasKernel
from qiyas_core.residual import Residual
from qiyas_core.sentence_geometry_adapter import (
    ADJACENCY_EVIDENCE_PREFIX,
    AMIL_MAMUL_REFS_PREFIX,
    OPENED_PRIOR_PREFIX,
    SENTENCE_GEOMETRY_EVIDENCE_PREFIX,
    SENTENCE_UNIT_IDENTITIES_PREFIX,
    SentenceGeometryLayerAdapter,
    SentenceUnit,
)
from qiyas_core.rules.sentence_geometry_rules import (
    ADJACENCY_UNDERSPECIFIED,
    CARRIED_UPSTREAM_RESIDUALS,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    IDENTITY_JOIN_UNDERSPECIFIED,
    OPENED_PRIORS,
    RELATION_COVERAGE_UNDERSPECIFIED,
    SENTENCE_BOUNDARY_UNDERSPECIFIED,
    SENTENCE_GEOMETRY_RULE,
    SENTENCE_STRUCTURE_BLOCKED,
)

import run_qiyas as rq


# ── synthetic accepted-P8 unit builder ───────────────────────────────────────


def _p8_unit(codepoints, position, *, prior_type="StructuralRelationPrior",
             residuals=(), extra_trace=(), with_codepoint=True):
    ids = []
    if with_codepoint:
        ids += [f"identity:codepoint:{c}" for c in codepoints]
    ids += ["identity:amil_mamul_domain"]
    trace = [f"amil_mamul_prior_type:{prior_type}"] + list(extra_trace)
    cand = Candidate(
        candidate_id=f"accepted:AmilMamulQiyas:{position}_{'_'.join(codepoints)}",
        candidate_type="AmilMamulCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="AmilMamulQiyas",
        source_rule_id="amil_mamul.relate",
        asl_id="اصل:amil_mamul_domain",
        far_id="فرع:composition_readiness_candidate:x",
        identity_ids=tuple(ids),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=tuple(residuals),
        trace_ids=tuple(trace),
        output_flags=frozenset({"CandidateOnly"}),
    )
    return SentenceUnit(candidate=cand, position=position)


def _compose(units, **kw):
    return SentenceGeometryLayerAdapter(kernel=QiyasKernel()).compose(units, **kw)


def _two_distinct_adjacent():
    return [_p8_unit(["0636", "064e"], 0), _p8_unit(["0643", "064e"], 1)]


def _trace_value(c, prefix):
    for t in c.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


def _has(c, prefix):
    return any(t.startswith(prefix) for t in c.trace_ids)


# ── RUN ───────────────────────────────────────────────────────────────────────


def test_P9_RUN_01_two_units_compose_sentence_geometry():
    r = _compose(_two_distinct_adjacent())
    assert r.accepted and r.accepted[0].candidate_type == "SentenceGeometryCandidate"


def test_P9_RUN_02_far_and_output_types():
    assert SENTENCE_GEOMETRY_RULE.far_type == "AmilMamulCandidate"
    assert SENTENCE_GEOMETRY_RULE.output_candidate_type == "SentenceGeometryCandidate"


def test_P9_RUN_03_candidate_only():
    assert "CandidateOnly" in _compose(_two_distinct_adjacent()).accepted[0].output_flags


# ── UNIT BOUNDARY (the critical rule) ─────────────────────────────────────────


def test_P9_UNIT_01_single_unit_blocks():
    # One word = one unit, even with internal P8 accepts -> BLOCK (sentence_structure).
    r = _compose([_p8_unit(["0636", "064e"], 0)])
    assert r.blocked and not r.accepted


def test_P9_UNIT_02_internal_multiplicity_does_not_make_two_units():
    # Two SentenceUnit objects with identical identity (same word) collapse to <2.
    same = [_p8_unit(["0636", "064e"], 0), _p8_unit(["0636", "064e"], 1)]
    r = _compose(same)
    assert r.blocked
    assert any(IDENTITY_COLLAPSE_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


# ── ACCEPT ────────────────────────────────────────────────────────────────────


def test_P9_ACCEPT_01_opens_only_relation_geometry_prior():
    c = _compose(_two_distinct_adjacent()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"relation_geometry_candidates"}


def test_P9_ACCEPT_02_evidence_is_multi_unit():
    c = _compose(_two_distinct_adjacent()).accepted[0]
    ev = _trace_value(c, SENTENCE_GEOMETRY_EVIDENCE_PREFIX)
    assert ev is not None and "units=2" in ev and "distinct=2" in ev and "adjacency=1" in ev


# ── DEFER (one per under-determined condition) ────────────────────────────────


def test_P9_DEFER_01_adjacency_underspecified():
    units = [_p8_unit(["0636", "064e"], 0), _p8_unit(["0643", "064e"], 2)]  # gap
    r = _compose(units)
    assert r.deferred and f"deferred_{ADJACENCY_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P9_DEFER_02_sentence_boundary_underspecified():
    r = _compose(_two_distinct_adjacent(), boundary_closed=False)
    assert r.deferred and f"deferred_{SENTENCE_BOUNDARY_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P9_DEFER_03_relation_coverage_underspecified():
    units = [_p8_unit(["0636", "064e"], 0),
             _p8_unit(["0643", "064e"], 1, prior_type="", extra_trace=())]
    # second unit lacks amil_mamul_prior_type marker -> coverage gap
    units[1] = SentenceUnit(
        candidate=Candidate(
            candidate_id="accepted:AmilMamulQiyas:nocov",
            candidate_type="AmilMamulCandidate", status=CandidateStatus.ACCEPTED,
            layer="AmilMamulQiyas", source_rule_id="amil_mamul.relate",
            asl_id="a", far_id="f",
            identity_ids=("identity:codepoint:0643", "identity:amil_mamul_domain"),
            rank=EvidenceRank.FORMAL_STRUCTURE, residuals=(),
            trace_ids=("structural_relation_possibility:relsig:x",),  # no prior_type
            output_flags=frozenset({"CandidateOnly"}),
        ),
        position=1,
    )
    r = _compose(units)
    assert r.deferred and f"deferred_{RELATION_COVERAGE_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P9_DEFER_04_carried_upstream_residuals():
    res = (Residual(residual_type="deferred_x", severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER, message="m", source_rule_id="r",
                    layer="AmilMamulQiyas", trace_ids=()),)
    units = [_p8_unit(["0636", "064e"], 0), _p8_unit(["0643", "064e"], 1, residuals=res)]
    r = _compose(units)
    assert r.deferred and f"deferred_{CARRIED_UPSTREAM_RESIDUALS}" in {x.residual_type for x in r.deferred[0].residuals}


def test_P9_DEFER_05_identity_join_underspecified():
    units = [_p8_unit(["0636", "064e"], 0),
             _p8_unit(["0643"], 1, with_codepoint=False)]  # unit lacks codepoint identity
    r = _compose(units)
    assert r.deferred and f"deferred_{IDENTITY_JOIN_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


# ── BLOCK ─────────────────────────────────────────────────────────────────────


def test_P9_BLOCK_01_fewer_than_two_units():
    r = _compose([_p8_unit(["0636", "064e"], 0)])
    assert r.blocked
    assert any(SENTENCE_STRUCTURE_BLOCKED in x.message or x.residual_type == "blocking_fariq_present"
               for x in r.blocked[0].residuals)


def test_P9_BLOCK_02_forbidden_output_attempted():
    units = [_p8_unit(["0636", "064e"], 0),
             _p8_unit(["0643", "064e"], 1, extra_trace=("leaked:IrabCandidate",))]
    r = _compose(units)
    assert r.blocked
    assert any(FORBIDDEN_OUTPUT_ATTEMPTED in x.message or x.residual_type == "blocking_fariq_present"
               for x in r.blocked[0].residuals)


# ── IDENTITY / TRACE ──────────────────────────────────────────────────────────


def test_P9_IDENTITY_01_union_preserves_each_unit_identity():
    units = _two_distinct_adjacent()
    c = _compose(units).accepted[0]
    for u in units:
        for iid in u.candidate.identity_ids:
            assert iid in c.identity_ids


def test_P9_IDENTITY_02_disjoint_from_trace():
    c = _compose(_two_distinct_adjacent()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_P9_IDENTITY_03_ordered_tuple_in_trace_not_identity():
    c = _compose(_two_distinct_adjacent()).accepted[0]
    tup = _trace_value(c, SENTENCE_UNIT_IDENTITIES_PREFIX)
    assert tup is not None and "u0=" in tup and "u1=" in tup
    assert _has(c, AMIL_MAMUL_REFS_PREFIX) and _has(c, ADJACENCY_EVIDENCE_PREFIX)


# ── FORBIDDEN / NO-LEAKAGE ────────────────────────────────────────────────────


def test_P9_FORBIDDEN_01_no_irab_case_ifadah_meaning_dalalah_hukm_reality():
    forbidden = set(SENTENCE_GEOMETRY_RULE.forbidden_outputs)
    for name in ("IrabCandidate", "CaseJudgment", "CaseEffect", "Irab", "IfadahCandidate",
                 "MeaningCandidate", "DalalahCandidate", "HukmCandidate", "RealityClaim",
                 "FinalMeaning"):
        assert name in forbidden, name


def test_P9_FORBIDDEN_02_no_jump_to_p10_plus():
    forbidden = set(SENTENCE_GEOMETRY_RULE.forbidden_outputs)
    for name in ("RelationGeometryCandidate", "IrabGeometryCandidate", "IfadahCandidate"):
        assert name in forbidden, name


def test_P9_FORBIDDEN_03_output_always_sentence_geometry():
    for r in (_compose(_two_distinct_adjacent()),
              _compose([_p8_unit(["0636", "064e"], 0)]),
              _compose(_two_distinct_adjacent(), boundary_closed=False)):
        for c in r.candidates:
            assert c.candidate_type == "SentenceGeometryCandidate"


# ── run_qiyas integration ─────────────────────────────────────────────────────


def test_P9_PIPELINE_01_two_words_accept_open_relation_prior():
    reps = rq.process_text("ضَرَبَ كَتَبَ")
    p9 = [s for r in reps for s in r.steps if s.layer == "SentenceGeometryQiyas"]
    assert len(p9) == 1 and p9[0].status == "accepted"
    # P9 ITSELF emits SentenceGeometryCandidate and opens only the P10 prior; the
    # P10 RelationGeometryCandidate is produced by the separate RelationGeometryQiyas
    # step, never by P9 directly.
    assert p9[0].candidate_type == "SentenceGeometryCandidate"
    opened = {t.split(":", 1)[1] for t in p9[0].trace_ids if t.startswith("opens_prior:")}
    assert opened == {"relation_geometry_candidates"}


def test_P9_PIPELINE_02_single_word_is_one_unit_blocks():
    reps = rq.process_text("ضَرَبَ")
    p9 = [s for r in reps for s in r.steps if s.layer == "SentenceGeometryQiyas"]
    assert len(p9) == 1 and p9[0].status == "blocked"


def test_P9_PIPELINE_03_no_final_or_semantic_leakage_anywhere():
    types = {s.candidate_type for r in rq.process_text("ضَرَبَ كَتَبَ") for s in r.steps}
    # P10 RelationGeometryCandidate, P11 IrabGeometryCandidate, and P12 (terminal)
    # IfadahCandidate are now licensed (behind accepted upstream); every
    # case/verdict/meaning/dalalah/hukm/reality/final object must still not leak.
    leak = types & {"CaseJudgment", "IrabFinalDecision", "RealityMapping", "TruthJudgment",
                    "IrabCandidate", "MeaningCandidate", "DalalahCandidate", "HukmCandidate",
                    "RealityClaim", "FinalMeaning"}
    assert not leak, leak
