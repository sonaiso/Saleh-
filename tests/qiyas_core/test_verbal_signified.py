"""SCG-P6 VerbalSignified — behavioral runtime tests (INFORMATION-GAIN layer).

SCG-P6 strengthening (2026-06-18). P6 is no longer a forwarding stamp: it READS
the upstream P5 verdict + carrier geometry from the MufradWordCandidate's trace
and discriminates the VERBAL-SIGNIFIED CARRIER geometry into ACCEPT / DEFER /
BLOCK, routed through the kernel's ``defer:`` / ``فارق:`` machinery.

  ACCEPT : P5 ACCEPT and verbal-carrier geometry — nC >= 2 AND
           ( (nC >= 3 AND short-vowel cadence) OR gemination ).
  DEFER  : isolated word-unit support exists but verbal-carrier cadence is
           underspecified — e.g. بَاب / بَيت (CVVC: long-vowel-only, nC==2, no
           gemination) which P5 accepts as a word unit but which lacks cadence.
  BLOCK  : P5 was DEFER/BLOCK (non-accepted upstream), or no vowel geometry.

P6 is PRE-SEMANTIC and structural. NOT a verb / فعل, NOT tense/aspect/mood/voice,
NOT subject/object/agent/patient, NOT event meaning / dalalah / i'rab / hukm /
root / wazn / lemma. ``verbal_signified_prior_type`` is a STRUCTURAL carrier
class (input-dependent), never a linguistic label. Opens meaning + dalalah
PRIORS on ACCEPT only.
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
from qiyas_core.mufrad_word_adapter import MufradWordLayerAdapter
from qiyas_core.verbal_signified_adapter import (
    MUFRAD_WORD_CANDIDATE_REF_PREFIX,
    OPENED_PRIOR_PREFIX,
    SIGNIFIED_EVIDENCE_PREFIX,
    VERBAL_CADENCE_EVIDENCE_PREFIX,
    VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX,
    VERBAL_SIGNIFIED_PRIOR_TYPE_PREFIX,
    VerbalSignifiedLayerAdapter,
)
from qiyas_core.rules.verbal_signified_rules import (
    ALLOWED_VERBAL_SIGNIFIED_PRIOR_TYPES,
    GEMINATED_CARRIER_POSSIBILITY,
    OPENED_PRIORS,
    SHORT_VOWEL_CADENCE_PRIOR,
    VERBAL_CARRIER_UNDERSPECIFIED,
    VERBAL_SIGNIFIED_RULE,
)

_LINGUISTIC_FORBIDDEN = {"Verb", "Fil", "Past", "Present", "Imperative", "Tense",
                        "Aspect", "Mood", "Active", "Passive", "Subject", "Object",
                        "Agent", "Patient", "EventMeaning", "Meaning", "Dalalah",
                        "Root", "Wazn", "Lemma", "Irab", "Hukm", "Reality"}

# Structural codepoint sequences (purely geometric).
_DARABA = [0x0636, 0x064E, 0x0631, 0x064E, 0x0628, 0x064E]  # ضَرَبَ CVCVCV (P6 acc, cadence)
_SHADHTH = [0x0634, 0x064E, 0x0627, 0x0630, 0x0651]        # شَاذّ CVVCC (P6 acc, geminated)
_BAB = [0x0628, 0x064E, 0x0627, 0x0628]                    # بَاب CVVC (P5 acc; P6 DEFER, long-v)
_BTA = [0x0628, 0x0652, 0x062A, 0x064E]                    # بْتَ CCV (P5 DEFER)


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


def _mufrad_word(profile_cps=_DARABA):
    """An accepted MufradWordCandidate carrying P5 evidence for the given profile."""
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(profile_cps)
    ).accepted[0]
    jm = JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]
    return MufradWordLayerAdapter(kernel=k).form(jm).accepted[0]


def _deferred_mufrad_word():
    """A P5-DEFERRED MufradWordCandidate (بْتَ: thin word unit)."""
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(_BTA)
    ).accepted[0]
    jm = JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]
    return MufradWordLayerAdapter(kernel=k).form(jm).deferred[0]


def _open(mw):
    return VerbalSignifiedLayerAdapter(kernel=QiyasKernel()).open(mw)


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


def test_P6_RUN_01_mufrad_word_opens_verbal_signified_candidate():
    result = _open(_mufrad_word())
    assert result.accepted
    assert result.accepted[0].candidate_type == "VerbalSignifiedCandidate"


def test_P6_RUN_02_consumes_mufrad_word_far_type():
    assert VERBAL_SIGNIFIED_RULE.far_type == "MufradWordCandidate"
    assert VERBAL_SIGNIFIED_RULE.output_candidate_type == "VerbalSignifiedCandidate"


def test_P6_RUN_03_candidate_only():
    assert "CandidateOnly" in _open(_mufrad_word()).accepted[0].output_flags


def test_P6_RUN_04_does_not_open_behind_deferred_p5():
    assert not _open(_deferred_mufrad_word()).accepted


# ─────────────────────────────────────────────────────────────────────────────
# 2. VERDICT
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_VERDICT_01_accept_visible_in_evidence():
    c = _open(_mufrad_word(_DARABA)).accepted[0]
    ev = _trace_value(c, VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX)
    assert ev is not None and "verdict=accept" in ev and "p5verdict=accept" in ev


def test_P6_VERDICT_02_long_vowel_word_unit_defers():
    result = _open(_mufrad_word(_BAB))  # CVVC: P5-accepted but no verbal cadence
    assert result.deferred and not result.accepted and not result.blocked


def test_P6_VERDICT_03_non_accepted_p5_blocks():
    result = _open(_deferred_mufrad_word())
    assert result.blocked and not result.accepted


# ─────────────────────────────────────────────────────────────────────────────
# 3. INFORMATION_GAIN
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_INFOGAIN_01_p5_accepted_but_p6_deferred_exists():
    # بَاب is ACCEPTED by P5 (word unit) yet DEFERRED by P6 (no verbal cadence).
    mw = _mufrad_word(_BAB)
    assert mw.candidate_type == "MufradWordCandidate"   # P5 accepted
    assert not _open(mw).accepted                        # P6 does not accept


def test_P6_INFOGAIN_02_prior_type_is_input_dependent():
    pt_cadence = _trace_value(_open(_mufrad_word(_DARABA)).accepted[0], VERBAL_SIGNIFIED_PRIOR_TYPE_PREFIX)
    pt_gem = _trace_value(_open(_mufrad_word(_SHADHTH)).accepted[0], VERBAL_SIGNIFIED_PRIOR_TYPE_PREFIX)
    assert pt_cadence == SHORT_VOWEL_CADENCE_PRIOR
    assert pt_gem == GEMINATED_CARRIER_POSSIBILITY
    assert pt_cadence != pt_gem


def test_P6_INFOGAIN_03_carrier_evidence_is_real_not_constant():
    e1 = _trace_value(_open(_mufrad_word(_DARABA)).accepted[0], VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX)
    e2 = _trace_value(_open(_mufrad_word(_SHADHTH)).accepted[0], VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX)
    assert e1 != e2 and "cadence=1" in e1 and "gem=1" in e2


# ─────────────────────────────────────────────────────────────────────────────
# 4. STRUCTURAL_ONLY
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_STRUCTURAL_01_carries_structural_signified_evidence():
    c = _open(_mufrad_word(_DARABA)).accepted[0]
    sig = _trace_value(c, SIGNIFIED_EVIDENCE_PREFIX)
    assert sig is not None and sig.startswith("sigsig:") and "CVCVCV" in sig


def test_P6_STRUCTURAL_02_carries_cadence_and_ref():
    c = _open(_mufrad_word()).accepted[0]
    assert _has_trace(c, VERBAL_CADENCE_EVIDENCE_PREFIX)
    assert _has_trace(c, MUFRAD_WORD_CANDIDATE_REF_PREFIX)


def test_P6_STRUCTURAL_03_prior_type_is_structural_never_linguistic():
    for prof in (_DARABA, _SHADHTH):
        pt = _trace_value(_open(_mufrad_word(prof)).accepted[0], VERBAL_SIGNIFIED_PRIOR_TYPE_PREFIX)
        assert pt in ALLOWED_VERBAL_SIGNIFIED_PRIOR_TYPES
        assert pt not in _LINGUISTIC_FORBIDDEN


def test_P6_STRUCTURAL_04_opens_meaning_dalalah_priors_on_accept_only():
    c = _open(_mufrad_word()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"meaning_priors", "dalalah_priors"}
    # deferred -> opens nothing
    d = _open(_mufrad_word(_BAB)).deferred[0]
    assert not _has_trace(d, OPENED_PRIOR_PREFIX)


def test_P6_STRUCTURAL_05_does_not_emit_meaning_or_downstream():
    c = _open(_mufrad_word()).accepted[0]
    assert c.candidate_type == "VerbalSignifiedCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# 5. IDENTITY_STABILITY
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_IDENTITY_01_preserves_upstream_identities():
    mw = _mufrad_word()
    c = _open(mw).accepted[0]
    for iid in mw.identity_ids:
        assert iid in c.identity_ids, iid


def test_P6_IDENTITY_02_defer_and_block_preserve_identity():
    mw_unit = _mufrad_word(_BAB)
    d = _open(mw_unit).deferred[0]
    for iid in mw_unit.identity_ids:
        assert iid in d.identity_ids
    mw_def = _deferred_mufrad_word()
    b = _open(mw_def).blocked[0]
    for iid in mw_def.identity_ids:
        assert iid in b.identity_ids


def test_P6_IDENTITY_03_identity_disjoint_and_candidate_only():
    c = _open(_mufrad_word()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))
    assert "CandidateOnly" in c.output_flags


def test_P6_DEFER_residual_is_explicit():
    d = _open(_mufrad_word(_BAB)).deferred[0]
    assert f"deferred_{VERBAL_CARRIER_UNDERSPECIFIED}" in {r.residual_type for r in d.residuals}


# ─────────────────────────────────────────────────────────────────────────────
# 6. FORBIDDEN_DOWNSTREAM
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_FORBIDDEN_01_no_meaning_no_dalalah_no_grammar():
    forbidden = set(VERBAL_SIGNIFIED_RULE.forbidden_outputs)
    for name in ("MeaningCandidate", "MeaningJudgment", "DalalahCandidate",
                 "DalalahJudgment", "TafsirCandidate", "WordTypeJudgment",
                 "RootCandidate", "WeightCandidate", "IrabCandidate", "CaseEffect", "Irab"):
        assert name in forbidden, name


def test_P6_FORBIDDEN_02_no_jump_to_p7_plus_or_absolutes():
    forbidden = set(VERBAL_SIGNIFIED_RULE.forbidden_outputs)
    for name in ("CompositionReadinessCandidate", "AmilMamulCandidate",
                 "IfadahCandidate", "SlotGeometry", "HukmCandidate",
                 "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P6_FORBIDDEN_03_output_always_verbal_signified():
    for prof in (_DARABA, _SHADHTH, _BAB):
        for c in _open(_mufrad_word(prof)).candidates:
            assert c.candidate_type == "VerbalSignifiedCandidate"


def test_P6_FORBIDDEN_04_residual_diffs_explicit():
    assert VERBAL_SIGNIFIED_RULE.invalidating_differences
