"""P3.1 WeightPattern (Arabic wazn extraction) — behavioral tests. مرشّح الوزن الصرفي.

AUXILIARY non-registry sub-pass (NOT a LayerSpec; registry count stays 19, no P13,
P0–P12 spine untouched). Extracts candidate-only wazn(s) from an accepted P3
RootStemCandidate. Candidate-only / non-final: it never asserts a final root, final
wazn, final word-kind, final i'rab, dalalah, ifadah, hukm, truth, reality, or intended
meaning. It may emit MULTIPLE WeightPatternCandidate objects per token (no final winner
forced). Surface letters are never silently rewritten.
"""

from __future__ import annotations

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.weight_pattern_adapter import (
    ADDED_LETTER_ALIGNMENT_PREFIX,
    CANDIDATE_WEIGHT_PATTERN_PREFIX,
    ROOT_SLOT_ALIGNMENT_PREFIX,
    TOKEN_SURFACE_PREFIX,
    WEIGHT_PATTERN_EVIDENCE_PREFIX,
    WeightPatternLayerAdapter,
)
from qiyas_core.rules.weight_pattern_rules import (
    WEIGHT_PATTERN_BLOCK_INVALID_ALIGNMENT,
    WEIGHT_PATTERN_BLOCK_NO_LICENSED_PATTERN,
    WEIGHT_PATTERN_DEFER_HAMZA_NORMALIZATION_REQUIRED,
    WEIGHT_PATTERN_DEFER_SHADDA_EXPANSION_REQUIRED,
    WEIGHT_PATTERN_DEFER_WEAK_LETTER_AMBIGUITY,
)

import run_qiyas as rq


# ── synthetic accepted-P3 RootStemCandidate builder ───────────────────────────


def _root_stem(surface, *, with_identity=True, cv="CVCVCV", extra_trace=()):
    ids = []
    if with_identity:
        ids = [f"identity:codepoint:{ord(ch):04x}" for ch in surface
               if 0x0621 <= ord(ch) <= 0x064A]
        ids.append("identity:root_stem_domain")
    return Candidate(
        candidate_id=f"accepted:RootStemQiyas:{surface}",
        candidate_type="RootStemCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="RootStemQiyas",
        source_rule_id="root_stem.close",
        asl_id="اصل:root_stem_domain",
        far_id="فرع:registry_projection_candidate:x",
        identity_ids=tuple(ids),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(f"root_pattern_evidence:cv={cv};slots=3",) + tuple(extra_trace),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _adapter():
    return WeightPatternLayerAdapter(kernel=QiyasKernel())


def _extract(surface, **kw):
    return _adapter().extract(_root_stem(surface), surface=surface, **kw)


def _patterns(cset):
    out = []
    for c in cset.candidates:
        for t in c.trace_ids:
            if t.startswith(CANDIDATE_WEIGHT_PATTERN_PREFIX):
                out.append(t[len(CANDIDATE_WEIGHT_PATTERN_PREFIX):])
    return out


def _reason(c):
    for t in c.trace_ids:
        if t.startswith(WEIGHT_PATTERN_EVIDENCE_PREFIX):
            return t.split("reason=", 1)[1]
    return None


def _trace_value(c, prefix):
    for t in c.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ── ACCEPT (clean alignment) ──────────────────────────────────────────────────


def test_WP_ACCEPT_01_triliteral_fa3ala():
    for w in ("كَتَبَ", "ضَرَبَ"):
        r = _extract(w)
        assert r.accepted and "فَعَلَ" in _patterns(r), w


def test_WP_ACCEPT_02_faail_with_added_alif_and_root_slot_alignment():
    r = _extract("كَاتِب")
    assert r.accepted
    c = r.accepted[0]
    assert _trace_value(c, CANDIDATE_WEIGHT_PATTERN_PREFIX) == "فَاعِل"
    # root_slot_alignment: ك→ف ; ت→ع ; ب→ل ; added ا@1
    assert _trace_value(c, ROOT_SLOT_ALIGNMENT_PREFIX) == "ك→ف;ت→ع;ب→ل"
    assert _trace_value(c, ADDED_LETTER_ALIGNMENT_PREFIX) == "ا@1"


def test_WP_ACCEPT_03_mafuul_with_added_letters():
    r = _extract("مَكْتُوب")
    assert r.accepted and "مَفْعُول" in _patterns(r)
    c = r.accepted[0]
    assert _trace_value(c, ROOT_SLOT_ALIGNMENT_PREFIX) == "ك→ف;ت→ع;ب→ل"


def test_WP_ACCEPT_04_multiple_licensed_candidates_not_forced_to_one():
    # م-R-R-R skeleton is licensed by BOTH مَفْعَل and مُفْعِل — both remain candidates.
    r = _extract("مَكْتَب")
    pats = _patterns(r)
    assert "مَفْعَل" in pats and "مُفْعِل" in pats
    assert len(r.accepted) >= 2  # multiple candidates, no final winner


def test_WP_ACCEPT_05_muslim_multiple_candidates():
    r = _extract("مُسْلِم")
    pats = _patterns(r)
    assert "مَفْعَل" in pats and "مُفْعِل" in pats


# ── DEFER (ambiguity — never guessed) ─────────────────────────────────────────


def test_WP_DEFER_01_shadda_expansion_required():
    r = _extract("مَدَّ")
    assert r.deferred and not r.accepted
    assert _reason(r.deferred[0]) == WEIGHT_PATTERN_DEFER_SHADDA_EXPANSION_REQUIRED


def test_WP_DEFER_02_hamza_normalization_required():
    r = _extract("آمَنَ")
    assert r.deferred and _reason(r.deferred[0]) == WEIGHT_PATTERN_DEFER_HAMZA_NORMALIZATION_REQUIRED


def test_WP_DEFER_03_weak_letter_ambiguity_hollow():
    for w in ("قَالَ", "بَاعَ"):
        r = _extract(w)
        assert r.deferred and not r.accepted, w
        assert _reason(r.deferred[0]) == WEIGHT_PATTERN_DEFER_WEAK_LETTER_AMBIGUITY, w


def test_WP_DEFER_04_deferred_candidate_does_not_assert_a_weight():
    c = _extract("قَالَ").deferred[0]
    # a deferred (ambiguous) candidate must NOT assert a concrete final weight
    assert _trace_value(c, CANDIDATE_WEIGHT_PATTERN_PREFIX) == "underdetermined"


# ── BLOCK ─────────────────────────────────────────────────────────────────────


def test_WP_BLOCK_01_no_licensed_pattern():
    r = _extract("قلزرد")  # five sound consonants — no licensed triliteral wazn
    assert r.blocked and not r.accepted
    assert any(WEIGHT_PATTERN_BLOCK_NO_LICENSED_PATTERN in res.message
               or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_WP_BLOCK_02_invalid_alignment_claims_letter_absent_from_surface():
    # An external alignment claiming a root letter not present on the surface is an
    # identity violation → BLOCK (no rewriting).
    r = _adapter().extract(_root_stem("كتب"), surface="كتب", external_root_letters=["ز"])
    assert r.blocked and not r.accepted
    assert any(WEIGHT_PATTERN_BLOCK_INVALID_ALIGNMENT in res.message
               or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_WP_BLOCK_03_identity_collapse_when_no_identity():
    r = _adapter().extract(_root_stem("كتب", with_identity=False), surface="كتب")
    assert r.blocked and not r.accepted


# ── IDENTITY / TRACE (surface not silently rewritten) ─────────────────────────


def test_WP_IDENTITY_01_preserves_root_stem_identity():
    rs = _root_stem("كَاتِب")
    c = _adapter().extract(rs, surface="كَاتِب").accepted[0]
    assert "identity:root_stem_domain" in c.identity_ids
    for iid in rs.identity_ids:
        if iid.startswith("identity:codepoint:"):
            assert iid in c.identity_ids  # codepoint identities preserved


def test_WP_IDENTITY_02_surface_carried_verbatim_not_rewritten():
    c = _extract("كَاتِب").accepted[0]
    assert _trace_value(c, TOKEN_SURFACE_PREFIX) == "كَاتِب"  # exact surface, no rewrite


def test_WP_IDENTITY_03_classification_is_trace_only_and_disjoint():
    c = _extract("كَتَبَ").accepted[0]
    assert any(t.startswith(CANDIDATE_WEIGHT_PATTERN_PREFIX) for t in c.trace_ids)
    assert not any(i.startswith(CANDIDATE_WEIGHT_PATTERN_PREFIX) for i in c.identity_ids)
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ── NO-LEAKAGE (no final weight/root/word-kind/i'rab/meaning/hukm) ─────────────


_FORBIDDEN_TYPES = (
    "WeightFinalJudgment", "WeightCandidate", "WeightJudgment", "RootFinalJudgment",
    "RootCandidate", "PatternCandidate", "WordKindFinalJudgment", "MabniJudgment",
    "MurabJudgment", "IrabFinalDecision", "CaseJudgment", "IrabCandidate",
    "MeaningCandidate", "DalalahCandidate", "DalalahJudgment", "HukmCandidate",
    "RealityClaim", "RealityMapping", "TruthJudgment", "FinalMeaning",
)


def test_WP_NOLEAK_01_output_is_only_weight_pattern_candidate():
    for w in ("كَتَبَ", "مَكْتَب", "قَالَ", "قلزرد"):
        for c in _extract(w).candidates:
            assert c.candidate_type == "WeightPatternCandidate", w
            assert c.candidate_type not in _FORBIDDEN_TYPES


def test_WP_NOLEAK_02_no_final_root_or_weight_judgment_in_trace():
    for w in ("كَتَبَ", "كَاتِب", "مَكْتُوب"):
        c = _extract(w).accepted[0]
        for forbidden in ("WeightFinalJudgment", "RootFinalJudgment", "final_root",
                          "final_weight", "WordKindFinalJudgment"):
            assert not any(forbidden in t for t in c.trace_ids), (w, forbidden)


def test_WP_NOLEAK_03_no_pos_meaning_irab_hukm_in_trace():
    c = _extract("كَاتِب").accepted[0]
    for forbidden in ("part_of_speech", "final_pos", "MeaningCandidate", "dalalah",
                      "IrabFinalDecision", "assign_hukm", "RealityClaim", "fa3il", "maf3ul"):
        assert not any(forbidden in t for t in c.trace_ids)


# ── PIPELINE (run_qiyas integration — auxiliary, candidate-only) ──────────────


def test_WP_PIPELINE_01_p31_step_present_and_candidate_only():
    steps = [s for r in rq.process_text("ضَرَبَ") for s in r.steps
             if s.layer == "WeightPatternQiyas"]
    assert steps, "P3.1 WeightPatternQiyas step must appear behind accepted P3"
    types = {s.candidate_type for s in steps}
    assert types <= {"WeightPatternCandidate"}
    assert not (types & set(_FORBIDDEN_TYPES))


# ── GOVERNANCE (auxiliary non-registry; count 19; no P13) ─────────────────────


def test_WP_GOV_01_not_a_registered_layerspec_count_19_no_p13():
    from qiyas_core.slot_geometry_core import master_registry_seed as MRS
    layers = list(MRS.build_master_registry_seed().all_layers())
    assert len(layers) == 19  # registry count unchanged
    assert not any("WeightPattern" in s.name or "WeightPattern" in s.id for s in layers)
    assert not any("P13" in n for n in dir(MRS) if n.startswith("LAYER_ID_"))


def test_WP_GOV_02_registered_via_auxiliary_forbidden_pattern():
    from qiyas_core.forbidden_outputs import LAYER_FORBIDDEN_OUTPUTS
    assert "WeightPatternQiyas" in LAYER_FORBIDDEN_OUTPUTS
