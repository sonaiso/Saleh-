"""SCG-P5 MufradWord — behavioral runtime tests (INFORMATION-GAIN layer).

SCG-P5 strengthening (2026-06-18). P5 is no longer a forwarding stamp: it READS
the upstream P4 verdict + word-unit geometry from the JamidMushtaqCandidate's
trace and discriminates the ISOLATED-WORD-UNIT geometry into ACCEPT / DEFER /
BLOCK, routed through the kernel's ``defer:`` / ``فارق:`` machinery.

  ACCEPT : P4 ACCEPT and enough word-unit body — n_consonants >= 2 AND one of
           {>=2 vowels, closed ending, gemination}.
  DEFER  : word-unit geometry too thin — e.g. بْتَ (CCV: two consonants, a single
           open vowel) which P4 accepts (nC==2) but which under-specifies an
           isolated word unit.
  BLOCK  : P4 was DEFER/BLOCK (non-accepted upstream), or geometry conflicts.

P5 means ONLY "enough isolated-word-unit geometry exists to open a
MufradWordCandidate". NOT a final word / مفرد / singular / noun / verb / جامد /
مشتق judgment, NOT wazn / root / lemma / dictionary / meaning / dalalah / i'rab.
``mufrad_word_prior_type`` is a STRUCTURAL class (input-dependent), never linguistic.
"""

from __future__ import annotations

from qiyas_core.kernel import QiyasKernel
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.conditioned_typed_sequence_adapter import ConditionedTypedSequenceLayerAdapter
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.slot_adapter import SlotLayerAdapter
from qiyas_core.registry_projection_adapter import RegistryProjectionLayerAdapter
from qiyas_core.root_stem_adapter import RootStemLayerAdapter, build_sequence_profile
from qiyas_core.jamid_mushtaq_adapter import JamidMushtaqLayerAdapter
from qiyas_core.mufrad_word_adapter import (
    JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX,
    MUFRAD_UNIT_EVIDENCE_PREFIX,
    MUFRAD_WORD_PRIOR_TYPE_PREFIX,
    OPENED_PRIOR_PREFIX,
    SLOT_SEQUENCE_REFS_PREFIX,
    WORDHOOD_EVIDENCE_PREFIX,
    WORD_BOUNDARY_EVIDENCE_PREFIX,
    MufradWordLayerAdapter,
)
from qiyas_core.rules.mufrad_word_rules import (
    ALLOWED_MUFRAD_WORD_PRIOR_TYPES,
    ISOLATED_UNIT_BOUNDARY_PRIOR,
    MUFRAD_UNIT_GEOMETRY_CLASS,
    MUFRAD_WORD_RULE,
    OPENED_PRIORS,
    WORD_UNIT_SHAPE_POSSIBILITY,
    WORD_UNIT_UNDERSPECIFIED,
)

_LINGUISTIC_FORBIDDEN = {"Noun", "Verb", "Ism", "Fil", "Jamid", "Mushtaq", "Singular",
                        "Plural", "Word", "Root", "Wazn", "Meaning", "Dalalah", "Irab"}

# Structural codepoint sequences (purely geometric).
_BARA = [0x0628, 0x064E, 0x0631, 0x064E]               # بَرَ -> CVCV  (P4 acc; P5 acc, GeometryClass)
_SHADHTH = [0x0634, 0x064E, 0x0627, 0x0630, 0x0651]    # شَاذّ -> CVVCC (P5 acc, ShapePossibility/gem)
_BAB = [0x0628, 0x064E, 0x0627, 0x0628]                # بَاب -> CVVC  (P5 acc, BoundaryPrior/closed)
_BTA = [0x0628, 0x0652, 0x062A, 0x064E]                # بْتَ -> CCV   (P4 acc nC2; P5 DEFER, thin)
_MAA = [0x0645, 0x064E, 0x0627]                        # مَا  -> CVV   (P3 acc; P4 DEFER nC1)


def _projection():
    """A real RegistryProjectionCandidate for بَ via the full P1->P2 chain."""
    k = QiyasKernel()
    typed = TypedCodePointLayerAdapter(kernel=k)
    lt = typed.classify_codepoint(0x0628).accepted[0]
    ht = typed.classify_codepoint(0x064E).accepted[0]
    letter = LetterIdentityLayerAdapter(kernel=k).process_letter_codepoint(lt).accepted[0]
    haraka = HarakaFunctionLayerAdapter(kernel=k).prove_from_codepoint(0x064E).accepted[0]
    cts = ConditionedTypedSequenceLayerAdapter(kernel=k)
    pe = cts.prove_letter_position(lt, index=0, sequence_length=2).accepted[0]
    pos = PositionLayerAdapter(kernel=k).prove_position(pe, index=0).accepted[0]
    cb = cts.prove_carrier_binding(haraka_typed=ht, carrier_letter_typed=lt, index=1, sequence_length=2).accepted[0]
    slot = SlotLayerAdapter(kernel=k).compose_slot(letter, haraka, pos, alignment_evidence=cb).accepted[0]
    return RegistryProjectionLayerAdapter(kernel=k).project(slot).accepted[0]


def _jamid_mushtaq(profile_cps=_BARA):
    """An accepted JamidMushtaqCandidate carrying P4 evidence for the given profile."""
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(profile_cps)
    ).accepted[0]
    return JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]


def _deferred_jamid_mushtaq():
    """A P4-DEFERRED JamidMushtaqCandidate (مَا: nC==1)."""
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(_MAA)
    ).accepted[0]
    return JamidMushtaqLayerAdapter(kernel=k).classify(rs).deferred[0]


def _form(jm):
    return MufradWordLayerAdapter(kernel=QiyasKernel()).form(jm)


def _has_trace(candidate, prefix):
    return any(t.startswith(prefix) for t in candidate.trace_ids)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 1. RUN
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_RUN_01_jamid_mushtaq_forms_mufrad_word_candidate():
    result = _form(_jamid_mushtaq())
    assert result.accepted
    assert result.accepted[0].candidate_type == "MufradWordCandidate"


def test_P5_RUN_02_consumes_jamid_mushtaq_far_type():
    assert MUFRAD_WORD_RULE.far_type == "JamidMushtaqCandidate"
    assert MUFRAD_WORD_RULE.output_candidate_type == "MufradWordCandidate"


def test_P5_RUN_03_candidate_only():
    assert "CandidateOnly" in _form(_jamid_mushtaq()).accepted[0].output_flags


def test_P5_RUN_04_does_not_open_behind_deferred_p4():
    # A non-accepted (deferred) P4 must not yield an accepted MufradWordCandidate.
    assert not _form(_deferred_jamid_mushtaq()).accepted


# ─────────────────────────────────────────────────────────────────────────────
# 2. VERDICT
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_VERDICT_01_accept_visible_in_evidence():
    c = _form(_jamid_mushtaq(_SHADHTH)).accepted[0]
    ev = _trace_value(c, MUFRAD_UNIT_EVIDENCE_PREFIX)
    assert ev is not None and "verdict=accept" in ev and "p4verdict=accept" in ev


def test_P5_VERDICT_02_thin_shape_defers():
    result = _form(_jamid_mushtaq(_BTA))  # CCV: P4-accepted but word-unit-thin
    assert result.deferred and not result.accepted and not result.blocked


def test_P5_VERDICT_03_non_accepted_p4_blocks():
    result = _form(_deferred_jamid_mushtaq())
    assert result.blocked and not result.accepted


# ─────────────────────────────────────────────────────────────────────────────
# 3. INFORMATION_GAIN
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_INFOGAIN_01_p4_accepted_but_p5_deferred_exists():
    # بْتَ is ACCEPTED by P4 (nC==2) yet DEFERRED by P5 (thin word unit):
    # P5 accepted count is strictly below P4 accepted count for this input.
    jm = _jamid_mushtaq(_BTA)
    assert jm.candidate_type == "JamidMushtaqCandidate"  # P4 accepted
    assert not _form(jm).accepted                        # P5 does not accept


def test_P5_INFOGAIN_02_prior_type_is_input_dependent():
    pt_gem = _trace_value(_form(_jamid_mushtaq(_SHADHTH)).accepted[0], MUFRAD_WORD_PRIOR_TYPE_PREFIX)
    pt_closed = _trace_value(_form(_jamid_mushtaq(_BAB)).accepted[0], MUFRAD_WORD_PRIOR_TYPE_PREFIX)
    pt_multi = _trace_value(_form(_jamid_mushtaq(_BARA)).accepted[0], MUFRAD_WORD_PRIOR_TYPE_PREFIX)
    assert pt_gem == WORD_UNIT_SHAPE_POSSIBILITY
    assert pt_closed == ISOLATED_UNIT_BOUNDARY_PRIOR
    assert pt_multi == MUFRAD_UNIT_GEOMETRY_CLASS
    assert len({pt_gem, pt_closed, pt_multi}) == 3


def test_P5_INFOGAIN_03_mufrad_unit_evidence_is_real_not_constant():
    e1 = _trace_value(_form(_jamid_mushtaq(_SHADHTH)).accepted[0], MUFRAD_UNIT_EVIDENCE_PREFIX)
    e2 = _trace_value(_form(_jamid_mushtaq(_BARA)).accepted[0], MUFRAD_UNIT_EVIDENCE_PREFIX)
    assert e1 != e2 and "gem=1" in e1


# ─────────────────────────────────────────────────────────────────────────────
# 4. STRUCTURAL_ONLY
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_STRUCTURAL_01_carries_structural_wordhood_evidence():
    c = _form(_jamid_mushtaq(_SHADHTH)).accepted[0]
    sig = _trace_value(c, WORDHOOD_EVIDENCE_PREFIX)
    assert sig is not None and sig.startswith("wordsig:") and "CVVCC" in sig


def test_P5_STRUCTURAL_02_carries_boundary_and_refs():
    c = _form(_jamid_mushtaq()).accepted[0]
    assert _has_trace(c, WORD_BOUNDARY_EVIDENCE_PREFIX)
    assert _has_trace(c, JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX)
    assert _has_trace(c, SLOT_SEQUENCE_REFS_PREFIX)


def test_P5_STRUCTURAL_03_prior_type_is_structural_never_linguistic():
    for prof in (_SHADHTH, _BAB, _BARA):
        pt = _trace_value(_form(_jamid_mushtaq(prof)).accepted[0], MUFRAD_WORD_PRIOR_TYPE_PREFIX)
        assert pt in ALLOWED_MUFRAD_WORD_PRIOR_TYPES
        assert pt not in _LINGUISTIC_FORBIDDEN


def test_P5_STRUCTURAL_04_opens_priors_on_accept_only():
    c = _form(_jamid_mushtaq()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"verbal_signified_candidates", "phrase_level_priors"}
    # deferred -> opens nothing
    d = _form(_jamid_mushtaq(_BTA)).deferred[0]
    assert not _has_trace(d, OPENED_PRIOR_PREFIX)


def test_P5_STRUCTURAL_05_does_not_emit_verbal_signified():
    c = _form(_jamid_mushtaq()).accepted[0]
    assert c.candidate_type != "VerbalSignifiedCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# 5. IDENTITY_STABILITY
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_IDENTITY_01_preserves_upstream_identities():
    jm = _jamid_mushtaq()
    c = _form(jm).accepted[0]
    for iid in jm.identity_ids:
        assert iid in c.identity_ids, iid


def test_P5_IDENTITY_02_defer_and_block_preserve_identity():
    jm_thin = _jamid_mushtaq(_BTA)
    d = _form(jm_thin).deferred[0]
    for iid in jm_thin.identity_ids:
        assert iid in d.identity_ids
    jm_def = _deferred_jamid_mushtaq()
    b = _form(jm_def).blocked[0]
    for iid in jm_def.identity_ids:
        assert iid in b.identity_ids


def test_P5_IDENTITY_03_identity_disjoint_from_trace_and_candidate_only():
    c = _form(_jamid_mushtaq()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))
    assert "CandidateOnly" in c.output_flags


def test_P5_DEFER_residual_is_explicit():
    d = _form(_jamid_mushtaq(_BTA)).deferred[0]
    assert f"deferred_{WORD_UNIT_UNDERSPECIFIED}" in {r.residual_type for r in d.residuals}


# ─────────────────────────────────────────────────────────────────────────────
# 6. FORBIDDEN_DOWNSTREAM
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_FORBIDDEN_01_no_final_word_no_lexicon_no_morphology_no_meaning():
    forbidden = set(MUFRAD_WORD_RULE.forbidden_outputs)
    for name in ("WordCandidate", "LexicalEntryCandidate", "WordTypeJudgment",
                 "RootCandidate", "WeightCandidate", "FormCandidate",
                 "MeaningCandidate", "DalalahCandidate", "IrabCandidate",
                 "CaseEffect", "Irab"):
        assert name in forbidden, name


def test_P5_FORBIDDEN_02_no_jump_to_p6_plus_or_absolutes():
    forbidden = set(MUFRAD_WORD_RULE.forbidden_outputs)
    for name in ("VerbalSignifiedCandidate", "CompositionReadinessCandidate",
                 "IfadahCandidate", "SlotGeometry", "HukmCandidate",
                 "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P5_FORBIDDEN_03_output_and_traces_never_downstream_types():
    for prof in (_SHADHTH, _BAB, _BARA, _BTA):
        for c in _form(_jamid_mushtaq(prof)).candidates:
            assert c.candidate_type == "MufradWordCandidate"


def test_P5_FORBIDDEN_04_residual_diffs_explicit():
    assert MUFRAD_WORD_RULE.invalidating_differences
