"""SCG-P7 CompositionReadiness — behavioral runtime tests (INFORMATION-GAIN layer).

SCG-P7 strengthening (2026-06-18). P7 is no longer a forwarding stamp: it READS
the upstream P6 verdict + carrier geometry from the VerbalSignifiedCandidate's
trace and discriminates the COMPOSITION-READINESS geometry into ACCEPT / DEFER /
BLOCK, routed through the kernel's ``defer:`` / ``فارق:`` machinery.

  ACCEPT : P6 ACCEPT and a clean composition boundary — short-vowel cadence AND
           n_consonants >= 3 (an unambiguous composition operand).
  DEFER  : P6-accepted carrier whose composition boundary is ambiguous — e.g.
           شَاذّ (CVVCC, long-vowel-heavy) which P6 accepts via gemination but which
           is under-specified as a composition operand (cadence == 0).
  BLOCK  : P6 was DEFER/BLOCK (non-accepted upstream), or no usable geometry.

P7 is the readiness GATE, not actual composition: NO composition, NO syntax, NO
amil/mamul relation, NO i'rab, NO final word-type / meaning / dalalah / hukm.
``composition_readiness_prior_type`` is a STRUCTURAL readiness class
(input-dependent), never a linguistic label. Opens amil/mamul + sentence-geometry
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
from qiyas_core.verbal_signified_adapter import VerbalSignifiedLayerAdapter
from qiyas_core.composition_readiness_adapter import (
    COMPOSABILITY_PROFILE_PREFIX,
    COMPOSITION_BOUNDARY_EVIDENCE_PREFIX,
    COMPOSITION_READINESS_PRIOR_TYPE_PREFIX,
    OPENED_PRIOR_PREFIX,
    READINESS_EVIDENCE_PREFIX,
    VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX,
    CompositionReadinessLayerAdapter,
)
from qiyas_core.rules.composition_readiness_rules import (
    ALLOWED_COMPOSITION_READINESS_PRIOR_TYPES,
    CADENCE_BOUNDARY_PRIOR,
    COMPOSITION_READINESS_GEOMETRY_CLASS,
    COMPOSITION_READINESS_RULE,
    COMPOSITION_READINESS_UNDERSPECIFIED,
    OPENED_PRIORS,
)

_LINGUISTIC_FORBIDDEN = {"Noun", "Verb", "Ism", "Fil", "Past", "Present", "Imperative",
                        "Tense", "Aspect", "Mood", "Active", "Passive", "Subject",
                        "Object", "Agent", "Patient", "Singular", "Plural", "Jamid",
                        "Mushtaq", "Root", "Wazn", "Lemma", "Meaning", "EventMeaning",
                        "Dalalah", "Irab", "Hukm", "Reality"}

# Structural codepoint sequences (purely geometric).
_DARABA = [0x0636, 0x064E, 0x0631, 0x064E, 0x0628, 0x064E]  # CVCVCV cadence nC3 open
_ADDA = [0x0639, 0x064E, 0x062F, 0x0651]                   # CVCC   cadence nC3 closed (gem)
_SHADHTH = [0x0634, 0x064E, 0x0627, 0x0630, 0x0651]        # CVVCC  gem, cadence=0 (P6 acc; P7 DEFER)
_BAB = [0x0628, 0x064E, 0x0627, 0x0628]                    # CVVC   (P6 DEFER)


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


def _verbal_signified(profile_cps=_DARABA):
    """An accepted VerbalSignifiedCandidate carrying P6 evidence for the given profile."""
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(profile_cps)
    ).accepted[0]
    jm = JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]
    mw = MufradWordLayerAdapter(kernel=k).form(jm).accepted[0]
    return VerbalSignifiedLayerAdapter(kernel=k).open(mw).accepted[0]


def _deferred_verbal_signified():
    """A P6-DEFERRED VerbalSignifiedCandidate (بَاب: long-vowel word unit, no cadence)."""
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(_BAB)
    ).accepted[0]
    jm = JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]
    mw = MufradWordLayerAdapter(kernel=k).form(jm).accepted[0]
    return VerbalSignifiedLayerAdapter(kernel=k).open(mw).deferred[0]


def _attest(vs):
    return CompositionReadinessLayerAdapter(kernel=QiyasKernel()).attest(vs)


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


def test_P7_RUN_01_verbal_signified_attests_composition_readiness_candidate():
    result = _attest(_verbal_signified())
    assert result.accepted
    assert result.accepted[0].candidate_type == "CompositionReadinessCandidate"


def test_P7_RUN_02_consumes_verbal_signified_far_type():
    assert COMPOSITION_READINESS_RULE.far_type == "VerbalSignifiedCandidate"
    assert COMPOSITION_READINESS_RULE.output_candidate_type == "CompositionReadinessCandidate"


def test_P7_RUN_03_candidate_only():
    assert "CandidateOnly" in _attest(_verbal_signified()).accepted[0].output_flags


def test_P7_RUN_04_does_not_open_behind_deferred_p6():
    assert not _attest(_deferred_verbal_signified()).accepted


# ─────────────────────────────────────────────────────────────────────────────
# 2. VERDICT
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_VERDICT_01_accept_visible_in_evidence():
    c = _attest(_verbal_signified(_DARABA)).accepted[0]
    ev = _trace_value(c, READINESS_EVIDENCE_PREFIX)
    assert ev is not None and "verdict=accept" in ev and "p6verdict=accept" in ev


def test_P7_VERDICT_02_long_vowel_carrier_defers():
    result = _attest(_verbal_signified(_SHADHTH))  # P6-accepted (gem) but cadence==0
    assert result.deferred and not result.accepted and not result.blocked


def test_P7_VERDICT_03_non_accepted_p6_blocks():
    result = _attest(_deferred_verbal_signified())
    assert result.blocked and not result.accepted


# ─────────────────────────────────────────────────────────────────────────────
# 3. INFORMATION_GAIN
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_INFOGAIN_01_p6_accepted_but_p7_deferred_exists():
    # شَاذّ is ACCEPTED by P6 (geminated carrier) yet DEFERRED by P7 (no clean
    # composition cadence boundary): P7 accepted count < P6 accepted count.
    vs = _verbal_signified(_SHADHTH)
    assert vs.candidate_type == "VerbalSignifiedCandidate"  # P6 accepted
    assert not _attest(vs).accepted                          # P7 does not accept


def test_P7_INFOGAIN_02_prior_type_is_input_dependent():
    pt_open = _trace_value(_attest(_verbal_signified(_DARABA)).accepted[0],
                           COMPOSITION_READINESS_PRIOR_TYPE_PREFIX)
    pt_closed = _trace_value(_attest(_verbal_signified(_ADDA)).accepted[0],
                             COMPOSITION_READINESS_PRIOR_TYPE_PREFIX)
    assert pt_open == COMPOSITION_READINESS_GEOMETRY_CLASS
    assert pt_closed == CADENCE_BOUNDARY_PRIOR
    assert pt_open != pt_closed


def test_P7_INFOGAIN_03_readiness_evidence_is_real_not_constant():
    e1 = _trace_value(_attest(_verbal_signified(_DARABA)).accepted[0], READINESS_EVIDENCE_PREFIX)
    e2 = _trace_value(_attest(_verbal_signified(_ADDA)).accepted[0], READINESS_EVIDENCE_PREFIX)
    assert e1 != e2 and "cadence=1" in e1


# ─────────────────────────────────────────────────────────────────────────────
# 4. STRUCTURAL_ONLY
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_STRUCTURAL_01_carries_structural_composability_profile():
    c = _attest(_verbal_signified(_DARABA)).accepted[0]
    sig = _trace_value(c, COMPOSABILITY_PROFILE_PREFIX)
    assert sig is not None and sig.startswith("compsig:") and "CVCVCV" in sig


def test_P7_STRUCTURAL_02_carries_boundary_and_ref():
    c = _attest(_verbal_signified()).accepted[0]
    assert _has_trace(c, COMPOSITION_BOUNDARY_EVIDENCE_PREFIX)
    assert _has_trace(c, VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX)


def test_P7_STRUCTURAL_03_prior_type_is_structural_never_linguistic():
    for prof in (_DARABA, _ADDA):
        pt = _trace_value(_attest(_verbal_signified(prof)).accepted[0],
                          COMPOSITION_READINESS_PRIOR_TYPE_PREFIX)
        assert pt in ALLOWED_COMPOSITION_READINESS_PRIOR_TYPES
        assert pt not in _LINGUISTIC_FORBIDDEN


def test_P7_STRUCTURAL_04_opens_amil_sentence_priors_on_accept_only():
    c = _attest(_verbal_signified()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"amil_mamul_relation_priors", "sentence_geometry_priors"}
    # deferred -> opens nothing
    d = _attest(_verbal_signified(_SHADHTH)).deferred[0]
    assert not _has_trace(d, OPENED_PRIOR_PREFIX)


def test_P7_STRUCTURAL_05_output_always_composition_readiness():
    c = _attest(_verbal_signified()).accepted[0]
    assert c.candidate_type == "CompositionReadinessCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# 5. IDENTITY_STABILITY
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_IDENTITY_01_preserves_upstream_identities():
    vs = _verbal_signified()
    c = _attest(vs).accepted[0]
    for iid in vs.identity_ids:
        assert iid in c.identity_ids, iid


def test_P7_IDENTITY_02_defer_and_block_preserve_identity():
    vs_amb = _verbal_signified(_SHADHTH)
    d = _attest(vs_amb).deferred[0]
    for iid in vs_amb.identity_ids:
        assert iid in d.identity_ids
    vs_def = _deferred_verbal_signified()
    b = _attest(vs_def).blocked[0]
    for iid in vs_def.identity_ids:
        assert iid in b.identity_ids


def test_P7_IDENTITY_03_identity_disjoint_and_candidate_only():
    c = _attest(_verbal_signified()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))
    assert "CandidateOnly" in c.output_flags


def test_P7_DEFER_residual_is_explicit():
    d = _attest(_verbal_signified(_SHADHTH)).deferred[0]
    assert f"deferred_{COMPOSITION_READINESS_UNDERSPECIFIED}" in {r.residual_type for r in d.residuals}


# ─────────────────────────────────────────────────────────────────────────────
# 6. FORBIDDEN_DOWNSTREAM
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_FORBIDDEN_01_no_amil_no_syntax_no_irab_no_meaning():
    forbidden = set(COMPOSITION_READINESS_RULE.forbidden_outputs)
    for name in ("AmilMamulCandidate", "SentenceCandidate", "IsnadJudgment",
                 "MeaningCandidate", "DalalahCandidate", "TafsirCandidate",
                 "IrabCandidate", "CaseEffect", "CaseJudgment", "Irab"):
        assert name in forbidden, name


def test_P7_FORBIDDEN_02_no_jump_to_p8_plus_or_absolutes():
    forbidden = set(COMPOSITION_READINESS_RULE.forbidden_outputs)
    for name in ("SentenceGeometryCandidate", "RelationGeometryCandidate",
                 "IrabGeometryCandidate", "IfadahCandidate", "SlotGeometry",
                 "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P7_FORBIDDEN_03_output_always_composition_readiness():
    for prof in (_DARABA, _ADDA, _SHADHTH):
        for c in _attest(_verbal_signified(prof)).candidates:
            assert c.candidate_type == "CompositionReadinessCandidate"


def test_P7_FORBIDDEN_04_residual_diffs_explicit():
    assert COMPOSITION_READINESS_RULE.invalidating_differences
