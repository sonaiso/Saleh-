"""P5.1 InflectionalClosure (Mabni / Mu'rab readiness) — behavioral tests.

AUXILIARY non-registry sub-pass (NOT a LayerSpec; registry count stays 19, no P13,
P0–P12 spine untouched). Classifies an accepted P5 MufradWordCandidate into the binary
structural partition MabniReadinessCandidate | Mu'rabReadinessCandidate — candidate-only
evidence, never a grammatical judgment, i'rab decision, dalalah, ifadah, hukm, reality,
or final meaning.

HONESTY NOTE: the fixtures below are SMALL, LABELLED fixtures — they are NOT the whole
Quran. The architectural classification reference is the FULL Quran token inventory
after tokenization; full-Quran completeness is a separate governed follow-up task
(requires an approved in-repo corpus snapshot/data contract). No fixture here is, or may
be presented as, Quran-complete.
"""

from __future__ import annotations

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank, ResidualEffect, ResidualSeverity
from qiyas_core.kernel import QiyasKernel
from qiyas_core.residual import Residual
from qiyas_core.inflectional_closure_adapter import (
    CLASSIFICATION_TRACE_PREFIX,
    INFLECTIONAL_CLOSURE_EVIDENCE_PREFIX,
    InflectionalClosureLayerAdapter,
)
from qiyas_core.rules.inflectional_closure_rules import (
    CARRIED_MUFRAD_RESIDUALS,
    CLASS_MABNI,
    CLASS_MURAB,
    IDENTITY_COLLAPSE_BLOCKED,
    INFLECTION_CLASS_CONFLICT,
    WORD_KIND_UNDERSPECIFIED,
)

import run_qiyas as rq


# ── synthetic accepted-P5 MufradWordCandidate builder ─────────────────────────


def _mufrad(surface, *, ids=("identity:codepoint:0628",), residuals=(), trace=()):
    return Candidate(
        candidate_id=f"accepted:MufradWordQiyas:{surface}",
        candidate_type="MufradWordCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="MufradWordQiyas",
        source_rule_id="mufrad_word.form",
        asl_id="اصل:mufrad_word_domain",
        far_id="فرع:jamid_mushtaq_candidate:x",
        identity_ids=tuple(ids),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=tuple(residuals),
        trace_ids=tuple(trace),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _adapter():
    return InflectionalClosureLayerAdapter(kernel=QiyasKernel())


def _classify(surface, **kw):
    return _adapter().classify(_mufrad(surface), token_surface=surface, **kw)


def _only(cset):
    cands = cset.accepted + cset.deferred + cset.blocked
    return cands[0]


def _classification(c):
    for t in c.trace_ids:
        if t.startswith(CLASSIFICATION_TRACE_PREFIX):
            return t[len(CLASSIFICATION_TRACE_PREFIX):]
    return None


# ── MABNI categories ──────────────────────────────────────────────────────────


def test_IC_MABNI_01_closed_particle():
    c = _classify("مِن", closed_category="preposition").accepted[0]
    assert c.candidate_type == "MabniReadinessCandidate"
    assert _classification(c) == CLASS_MABNI


def test_IC_MABNI_02_pronoun():
    assert _classify("هو", closed_category="pronoun").accepted[0].candidate_type == "MabniReadinessCandidate"


def test_IC_MABNI_03_demonstrative():
    assert _classify("هذا", closed_category="demonstrative").accepted[0].candidate_type == "MabniReadinessCandidate"


def test_IC_MABNI_04_relative():
    assert _classify("الذي", closed_category="relative").accepted[0].candidate_type == "MabniReadinessCandidate"


def test_IC_MABNI_05_closed_compounds():
    for w in ("عليه", "منه", "بكم"):
        assert _classify(w, is_closed_compound=True).accepted[0].candidate_type == "MabniReadinessCandidate", w


def test_IC_MABNI_06_past_verb():
    assert _classify("ضَرَبَ", word_kind="verbal", verb_tense="past").accepted[0].candidate_type == "MabniReadinessCandidate"


def test_IC_MABNI_07_imperative_verb():
    assert _classify("اضرب", word_kind="verbal", verb_tense="imperative").accepted[0].candidate_type == "MabniReadinessCandidate"


def test_IC_MABNI_08_fawatih_al_suwar():
    c = _classify("الم", is_fawatih=True).accepted[0]
    assert c.candidate_type == "MabniReadinessCandidate"
    assert _classification(c) == CLASS_MABNI


# ── MU'RAB categories ─────────────────────────────────────────────────────────


def test_IC_MURAB_01_visible_declinable_noun():
    c = _classify("رجل", word_kind="nominal").accepted[0]
    assert c.candidate_type == "Mu'rabReadinessCandidate"
    assert _classification(c) == CLASS_MURAB


def test_IC_MURAB_02_derived_noun():
    assert _classify("كاتب", word_kind="nominal", is_derived=True).accepted[0].candidate_type == "Mu'rabReadinessCandidate"


def test_IC_MURAB_03_present_verb_open():
    assert _classify("يكتب", word_kind="verbal", verb_tense="present").accepted[0].candidate_type == "Mu'rabReadinessCandidate"


# ── PRECEDENCE (error-prevention) ─────────────────────────────────────────────


def test_IC_PRECEDENCE_01_closed_particle_with_wazn_trap_stays_mabni():
    # A harf with misleading morphological analyzability (wazn/root/derived) must NOT
    # slip into mu'rab — mabni precedence wins.
    c = _classify("مِن", closed_category="harf", is_derived=True).accepted[0]
    assert c.candidate_type == "MabniReadinessCandidate"


def test_IC_PRECEDENCE_02_pronoun_with_morphology_trap_stays_mabni():
    c = _classify("هو", closed_category="pronoun", is_derived=True).accepted[0]
    assert c.candidate_type == "MabniReadinessCandidate"


def test_IC_PRECEDENCE_03_past_verb_not_demoted_by_present_absence():
    # verbal + past stays mabni even if other (morphological) markers are present.
    c = _classify("ضَرَبَ", word_kind="verbal", verb_tense="past", is_derived=True).accepted[0]
    assert c.candidate_type == "MabniReadinessCandidate"


# ── DEFER / BLOCK (never guessed) ─────────────────────────────────────────────


def test_IC_DEFER_01_word_kind_underspecified():
    r = _classify("?")
    assert r.deferred and not r.accepted
    assert f"deferred_{WORD_KIND_UNDERSPECIFIED}" in {x.residual_type for x in r.deferred[0].residuals}


def test_IC_DEFER_02_carried_mufrad_residuals():
    res = (Residual(residual_type="deferred_x", severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER, message="m", source_rule_id="r",
                    layer="MufradWordQiyas", trace_ids=()),)
    r = _adapter().classify(_mufrad("رجل", residuals=res), word_kind="nominal")
    assert r.deferred and f"deferred_{CARRIED_MUFRAD_RESIDUALS}" in {x.residual_type for x in r.deferred[0].residuals}


def test_IC_BLOCK_01_class_conflict():
    r = _classify("x", class_conflict=True)
    assert r.blocked and not r.accepted
    assert any(INFLECTION_CLASS_CONFLICT in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


def test_IC_BLOCK_02_identity_collapse_when_no_identity():
    r = _adapter().classify(_mufrad("x", ids=()), word_kind="nominal")
    assert r.blocked and not r.accepted
    assert any(IDENTITY_COLLAPSE_BLOCKED in res.message or res.residual_type == "blocking_fariq_present"
               for res in r.blocked[0].residuals)


# ── IDENTITY / TRACE ──────────────────────────────────────────────────────────


def test_IC_IDENTITY_01_preserves_mufrad_word_identity():
    c = _adapter().classify(_mufrad("رجل", ids=("identity:codepoint:0631", "identity:mufrad_word_domain")),
                            word_kind="nominal").accepted[0]
    assert "identity:codepoint:0631" in c.identity_ids
    assert "identity:mufrad_word_domain" in c.identity_ids


def test_IC_IDENTITY_02_classification_is_trace_only():
    c = _classify("رجل", word_kind="nominal").accepted[0]
    assert any(t.startswith(CLASSIFICATION_TRACE_PREFIX) for t in c.trace_ids)
    assert not any(i.startswith(CLASSIFICATION_TRACE_PREFIX) for i in c.identity_ids)


def test_IC_IDENTITY_03_identity_trace_disjoint():
    c = _classify("رجل", word_kind="nominal").accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ── NO-LEAKAGE (candidate-only; never a judgment / i'rab / meaning / hukm) ─────


_FORBIDDEN_TYPES = (
    "MabniJudgment", "MurabJudgment", "IrabFinalDecision", "IrabGeometryCandidate",
    "CaseJudgment", "IrabCandidate", "IfadahCandidate", "MeaningCandidate",
    "DalalahCandidate", "DalalahJudgment", "HukmCandidate", "RealityClaim",
    "RealityMapping", "TruthJudgment", "FinalMeaning", "SyntaxLabelJudgment",
)
# Final i'rab position/sign words that must never appear as a verdict.
_FORBIDDEN_IRAB_WORDS = ("raf", "nasb", "jarr", "jazm", "marfu", "mansub", "majrur", "majzum")


def test_IC_NOLEAK_01_output_is_only_readiness_candidate():
    for kw in (dict(closed_category="preposition"), dict(word_kind="nominal"),
               dict(is_fawatih=True), {}):
        for c in _classify("t", **kw).candidates:
            assert c.candidate_type in ("MabniReadinessCandidate", "Mu'rabReadinessCandidate",
                                        "InflectionalClosureCandidate")
            assert c.candidate_type not in _FORBIDDEN_TYPES


def test_IC_NOLEAK_02_no_irab_position_or_sign_judgment_in_trace():
    for kw in (dict(closed_category="preposition"), dict(word_kind="nominal"),
               dict(word_kind="verbal", verb_tense="present")):
        c = _classify("t", **kw).accepted[0]
        for w in _FORBIDDEN_IRAB_WORDS:
            assert not any(w in t.lower() for t in c.trace_ids), (w, kw)


def test_IC_NOLEAK_03_no_meaning_hukm_reality_change_in_trace():
    c = _classify("رجل", word_kind="nominal").accepted[0]
    for forbidden in ("assign_hukm", "assign_reality", "assign_truth", "final_meaning",
                      "dalalah_judgment", "MabniJudgment", "MurabJudgment"):
        assert not any(forbidden in t for t in c.trace_ids)


# ── BINARY PARTITION INVARIANT (fixture-level — NOT the whole Quran) ───────────

# A small, HONESTLY-LABELLED fixture of word tokens "after tokenization". This is a
# fixture, NOT the Quran. Each token carries explicit, labelled classification evidence
# so the partition is total (zero deferred/blocked). The architectural reference remains
# the full Quran token inventory; full-Quran completeness is a separate governed task.
_FIXTURE_TOKENS = (
    # surface,   evidence kwargs,                                    expected class
    ("مِن",      dict(closed_category="preposition"),               CLASS_MABNI),
    ("لا",       dict(closed_category="negation"),                  CLASS_MABNI),
    ("إنْ",      dict(closed_category="condition"),                 CLASS_MABNI),
    ("و",        dict(closed_category="conjunction"),               CLASS_MABNI),
    ("إلا",      dict(closed_category="exception"),                 CLASS_MABNI),
    ("هو",       dict(closed_category="pronoun"),                   CLASS_MABNI),
    ("هذا",      dict(closed_category="demonstrative"),             CLASS_MABNI),
    ("الذي",     dict(closed_category="relative"),                  CLASS_MABNI),
    ("عليه",     dict(is_closed_compound=True),                     CLASS_MABNI),
    ("منه",      dict(is_closed_compound=True),                     CLASS_MABNI),
    ("بكم",      dict(is_closed_compound=True),                     CLASS_MABNI),
    ("ضَرَبَ",    dict(word_kind="verbal", verb_tense="past"),       CLASS_MABNI),
    ("اضرب",     dict(word_kind="verbal", verb_tense="imperative"), CLASS_MABNI),
    ("الم",      dict(is_fawatih=True),                             CLASS_MABNI),  # fawatih → mabni, counted
    ("حم",       dict(is_fawatih=True),                             CLASS_MABNI),  # fawatih → mabni, counted
    ("رجل",      dict(word_kind="nominal"),                         CLASS_MURAB),
    ("كتاب",     dict(word_kind="nominal"),                         CLASS_MURAB),
    ("كاتب",     dict(word_kind="nominal", is_derived=True),        CLASS_MURAB),
    ("مكتوب",    dict(word_kind="nominal", is_derived=True),        CLASS_MURAB),
    ("يكتب",     dict(word_kind="verbal", verb_tense="present"),    CLASS_MURAB),
    ("يضرب",     dict(word_kind="verbal", verb_tense="present"),    CLASS_MURAB),
)


def _classify_fixture():
    a = _adapter()
    mabni, murab, unclassified = [], [], []
    for surface, kw, _expected in _FIXTURE_TOKENS:
        r = a.classify(_mufrad(surface), token_surface=surface, **kw)
        if r.accepted and r.accepted[0].candidate_type == "MabniReadinessCandidate":
            mabni.append(surface)
        elif r.accepted and r.accepted[0].candidate_type == "Mu'rabReadinessCandidate":
            murab.append(surface)
        else:
            unclassified.append(surface)
    return mabni, murab, unclassified


def test_IC_PARTITION_01_binary_total_no_token_dropped():
    mabni, murab, unclassified = _classify_fixture()
    total = len(_FIXTURE_TOKENS)
    assert not unclassified, f"tokens left outside the binary partition: {unclassified}"
    assert len(mabni) + len(murab) == total  # mabni_count + murab_count == total


def test_IC_PARTITION_02_each_token_matches_expected_class():
    a = _adapter()
    for surface, kw, expected in _FIXTURE_TOKENS:
        c = a.classify(_mufrad(surface), token_surface=surface, **kw).accepted[0]
        got = CLASS_MABNI if c.candidate_type == "MabniReadinessCandidate" else CLASS_MURAB
        assert got == expected, (surface, got, expected)


def test_IC_PARTITION_03_fawatih_counted_as_mabni_in_denominator():
    mabni, murab, _ = _classify_fixture()
    # Both fawatih tokens are present in the mabni set and in the denominator.
    assert "الم" in mabni and "حم" in mabni
    total = len(_FIXTURE_TOKENS)
    assert len(mabni) + len(murab) == total  # fawatih NOT excluded from the denominator


# ── PIPELINE (run_qiyas integration — honest: real text lacks detailed evidence) ──


def test_IC_PIPELINE_01_p51_step_present_and_candidate_only():
    # The P5.1 step runs behind accepted P5 in the live pipeline. Real text currently
    # carries no detailed word-kind/closed-category evidence, so it DEFERs honestly —
    # it never guesses a classification. The point: the step exists, is candidate-only,
    # and emits no forbidden object.
    steps = [s for r in rq.process_text("ضَرَبَ") for s in r.steps
             if s.layer == "InflectionalClosureQiyas"]
    assert steps, "P5.1 InflectionalClosureQiyas step must appear behind accepted P5"
    types = {s.candidate_type for s in steps}
    assert not (types & set(_FORBIDDEN_TYPES))


# Final / judgment / semantic objects that must NOT leak ANYWHERE in the full pipeline.
# (IfadahCandidate (P12) and IrabGeometryCandidate (P11) are LICENSED downstream
# candidates and are intentionally excluded from this forbidden set.)
_PIPELINE_FORBIDDEN = (
    "MabniJudgment", "MurabJudgment", "IrabFinalDecision", "CaseJudgment",
    "IrabCandidate", "MeaningCandidate", "DalalahCandidate", "DalalahJudgment",
    "HukmCandidate", "RealityClaim", "RealityMapping", "TruthJudgment",
    "FinalMeaning", "SyntaxLabelJudgment",
)


def test_IC_PIPELINE_02_no_final_or_semantic_leakage_anywhere():
    types = {s.candidate_type for r in rq.process_text("ضَرَبَ كَتَبَ") for s in r.steps}
    assert not (types & set(_PIPELINE_FORBIDDEN))
