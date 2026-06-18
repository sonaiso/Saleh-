"""SCG-P6 VerbalSignified — behavioral runtime tests.

Narrow SCG-P6 implementation (2026-06-18). Opens verbal-signified semantic
POSSIBILITIES: MufradWordCandidate -> VerbalSignifiedCandidate.

Candidate-only and PRIORS-only (VERBAL_SIGNIFIED_CONSTITUTION.md): it OPENS
meaning + dalalah priors; it NEVER produces actual meaning (MeaningCandidate),
dalalah (DalalahCandidate/DalalahJudgment), tafsir, hukm, or reality/final
meaning.
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
from qiyas_core.root_stem_adapter import RootStemLayerAdapter
from qiyas_core.jamid_mushtaq_adapter import JamidMushtaqLayerAdapter
from qiyas_core.mufrad_word_adapter import MufradWordLayerAdapter
from qiyas_core.verbal_signified_adapter import (
    MUFRAD_WORD_CANDIDATE_REF_PREFIX,
    OPENED_PRIOR_PREFIX,
    SIGNIFIED_EVIDENCE_PREFIX,
    VerbalSignifiedLayerAdapter,
)
from qiyas_core.rules.verbal_signified_rules import OPENED_PRIORS, VERBAL_SIGNIFIED_RULE


def _mufrad_word():
    """A real MufradWordCandidate for بَ via the full P1->P5 chain."""
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
    proj = RegistryProjectionLayerAdapter(kernel=k).project(slot).accepted[0]
    rs = RootStemLayerAdapter(kernel=k).close(proj).accepted[0]
    jm = JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]
    return MufradWordLayerAdapter(kernel=k).form(jm).accepted[0]


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
# P6-RUN-OUTPUT
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


# ─────────────────────────────────────────────────────────────────────────────
# P6-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_IDENTITY_01_preserves_mufrad_word_identity():
    mw = _mufrad_word()
    c = _open(mw).accepted[0]
    for iid in mw.identity_ids:
        assert iid in c.identity_ids, iid


def test_P6_TRACE_01_identity_disjoint_from_trace():
    c = _open(_mufrad_word()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P6-PRIORS — opens meaning + dalalah priors; carries structural evidence
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_PRIORS_01_opens_meaning_and_dalalah_priors():
    c = _open(_mufrad_word()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"meaning_priors", "dalalah_priors"}


def test_P6_PRIORS_02_carries_structural_signified_evidence_and_ref():
    c = _open(_mufrad_word()).accepted[0]
    sig = _trace_value(c, SIGNIFIED_EVIDENCE_PREFIX)
    assert sig is not None and sig.startswith("sigsig:")  # geometry signature, no meaning
    assert _has_trace(c, MUFRAD_WORD_CANDIDATE_REF_PREFIX)


# ─────────────────────────────────────────────────────────────────────────────
# P6-FORBIDDEN — emits no meaning / dalalah / hukm / reality / final meaning; no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_FORBIDDEN_01_emits_no_meaning_no_dalalah_no_tafsir():
    forbidden = set(VERBAL_SIGNIFIED_RULE.forbidden_outputs)
    for name in ("MeaningCandidate", "MeaningJudgment", "DalalahCandidate",
                 "DalalahJudgment", "TafsirCandidate"):
        assert name in forbidden, name


def test_P6_FORBIDDEN_02_emits_no_hukm_reality_finalmeaning():
    forbidden = set(VERBAL_SIGNIFIED_RULE.forbidden_outputs)
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P6_FORBIDDEN_03_no_jump_to_p7_plus():
    forbidden = set(VERBAL_SIGNIFIED_RULE.forbidden_outputs)
    for name in ("CompositionReadinessCandidate", "AmilMamulCandidate",
                 "SentenceGeometryCandidate", "RelationGeometryCandidate",
                 "IrabGeometryCandidate", "IfadahCandidate"):
        assert name in forbidden, name


def test_P6_FORBIDDEN_04_does_not_emit_composition_readiness():
    c = _open(_mufrad_word()).accepted[0]
    assert c.candidate_type != "CompositionReadinessCandidate"


def test_P6_FORBIDDEN_05_residual_diffs_explicit():
    assert VERBAL_SIGNIFIED_RULE.invalidating_differences
