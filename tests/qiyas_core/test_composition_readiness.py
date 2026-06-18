"""SCG-P7 CompositionReadiness — behavioral runtime tests.

Narrow SCG-P7 implementation (2026-06-18). Attests structural READINESS to enter
composition: VerbalSignifiedCandidate -> CompositionReadinessCandidate.

Candidate-only and READINESS-only (COMPOSITION_READINESS_CONSTITUTION.md): it
attests readiness; it performs NO actual composition, NO syntax, NO amil/mamul
relation, NO i'rab, NO meaning / dalalah / hukm. Opens amil/mamul + sentence-
geometry priors; emits no AmilMamulCandidate / downstream / semantic output.
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
from qiyas_core.verbal_signified_adapter import VerbalSignifiedLayerAdapter
from qiyas_core.composition_readiness_adapter import (
    COMPOSABILITY_PROFILE_PREFIX,
    OPENED_PRIOR_PREFIX,
    READINESS_EVIDENCE_PREFIX,
    VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX,
    CompositionReadinessLayerAdapter,
)
from qiyas_core.rules.composition_readiness_rules import COMPOSITION_READINESS_RULE, OPENED_PRIORS


def _verbal_signified():
    """A real VerbalSignifiedCandidate for بَ via the full P1->P6 chain."""
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
    mw = MufradWordLayerAdapter(kernel=k).form(jm).accepted[0]
    return VerbalSignifiedLayerAdapter(kernel=k).open(mw).accepted[0]


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
# P7-RUN-OUTPUT
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_RUN_01_verbal_signified_attests_composition_readiness():
    result = _attest(_verbal_signified())
    assert result.accepted
    assert result.accepted[0].candidate_type == "CompositionReadinessCandidate"


def test_P7_RUN_02_consumes_verbal_signified_far_type():
    assert COMPOSITION_READINESS_RULE.far_type == "VerbalSignifiedCandidate"
    assert COMPOSITION_READINESS_RULE.output_candidate_type == "CompositionReadinessCandidate"


def test_P7_RUN_03_candidate_only():
    assert "CandidateOnly" in _attest(_verbal_signified()).accepted[0].output_flags


# ─────────────────────────────────────────────────────────────────────────────
# P7-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_IDENTITY_01_preserves_upstream_identities():
    vs = _verbal_signified()
    c = _attest(vs).accepted[0]
    for iid in vs.identity_ids:
        assert iid in c.identity_ids, iid


def test_P7_TRACE_01_identity_disjoint_from_trace():
    c = _attest(_verbal_signified()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P7-STRUCTURAL — readiness evidence; opens priors
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_STRUCTURAL_01_carries_composability_profile_and_readiness_evidence():
    c = _attest(_verbal_signified()).accepted[0]
    prof = _trace_value(c, COMPOSABILITY_PROFILE_PREFIX)
    assert prof is not None and prof.startswith("compsig:")  # geometry profile, no syntax
    assert _has_trace(c, READINESS_EVIDENCE_PREFIX)
    assert _has_trace(c, VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX)


def test_P7_STRUCTURAL_02_opens_amil_mamul_and_sentence_geometry_priors():
    c = _attest(_verbal_signified()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"amil_mamul_relation_priors", "sentence_geometry_priors"}


def test_P7_STRUCTURAL_03_does_not_emit_amil_mamul():
    c = _attest(_verbal_signified()).accepted[0]
    assert c.candidate_type != "AmilMamulCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P7-FORBIDDEN — no syntax / amil-mamul / i'rab / meaning / hukm; no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_FORBIDDEN_01_no_syntax_no_amil_mamul_no_irab():
    forbidden = set(COMPOSITION_READINESS_RULE.forbidden_outputs)
    for name in ("AmilMamulCandidate", "SentenceCandidate", "SentenceGeometryCandidate",
                 "RelationGeometryCandidate", "IrabGeometryCandidate", "IrabCandidate",
                 "CaseEffect", "CaseJudgment", "Irab", "IsnadJudgment"):
        assert name in forbidden, name


def test_P7_FORBIDDEN_02_no_meaning_no_dalalah_no_hukm_no_reality():
    forbidden = set(COMPOSITION_READINESS_RULE.forbidden_outputs)
    for name in ("MeaningCandidate", "DalalahCandidate", "TafsirCandidate",
                 "HukmCandidate", "RealityClaim", "FinalMeaning", "IfadahCandidate"):
        assert name in forbidden, name


def test_P7_FORBIDDEN_03_residual_diffs_explicit():
    assert COMPOSITION_READINESS_RULE.invalidating_differences
