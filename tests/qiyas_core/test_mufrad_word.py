"""SCG-P5 MufradWord — behavioral runtime tests.

Narrow SCG-P5 implementation (2026-06-18). Forms a candidate-only single-word
POSSIBILITY: JamidMushtaqCandidate -> MufradWordCandidate.

Candidate-only and structural-only (MUFRAD_WORD_CONSTITUTION.md): NOT a final
lexical word (WordCandidate forbidden), NOT a dictionary entry, NOT morphology /
grammar / meaning / i'rab / hukm. Opens verbal-signified + phrase-level priors;
emits no VerbalSignifiedCandidate / downstream / semantic output.
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
from qiyas_core.mufrad_word_adapter import (
    JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX,
    OPENED_PRIOR_PREFIX,
    SLOT_SEQUENCE_REFS_PREFIX,
    WORDHOOD_EVIDENCE_PREFIX,
    WORD_BOUNDARY_EVIDENCE_PREFIX,
    MufradWordLayerAdapter,
)
from qiyas_core.rules.mufrad_word_rules import MUFRAD_WORD_RULE, OPENED_PRIORS


def _jamid_mushtaq():
    """A real JamidMushtaqCandidate for بَ via the full P1->P4 chain."""
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
    return JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]


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
# P5-RUN-OUTPUT
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


# ─────────────────────────────────────────────────────────────────────────────
# P5-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_IDENTITY_01_preserves_upstream_identities():
    jm = _jamid_mushtaq()
    c = _form(jm).accepted[0]
    for iid in jm.identity_ids:
        assert iid in c.identity_ids, iid


def test_P5_TRACE_01_identity_disjoint_from_trace():
    c = _form(_jamid_mushtaq()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P5-STRUCTURAL — structural wordhood evidence; opens priors
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_STRUCTURAL_01_carries_structural_wordhood_evidence():
    c = _form(_jamid_mushtaq()).accepted[0]
    sig = _trace_value(c, WORDHOOD_EVIDENCE_PREFIX)
    assert sig is not None and sig.startswith("wordsig:")  # geometry signature, no lexicon


def test_P5_STRUCTURAL_02_carries_boundary_and_refs():
    c = _form(_jamid_mushtaq()).accepted[0]
    assert _has_trace(c, WORD_BOUNDARY_EVIDENCE_PREFIX)
    assert _has_trace(c, JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX)
    assert _has_trace(c, SLOT_SEQUENCE_REFS_PREFIX)


def test_P5_STRUCTURAL_03_opens_verbal_signified_and_phrase_priors():
    c = _form(_jamid_mushtaq()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"verbal_signified_candidates", "phrase_level_priors"}


def test_P5_STRUCTURAL_04_does_not_emit_verbal_signified():
    c = _form(_jamid_mushtaq()).accepted[0]
    assert c.candidate_type != "VerbalSignifiedCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P5-FORBIDDEN — no final word / no dictionary / no morphology / no meaning / no-jump
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


def test_P5_FORBIDDEN_03_residual_diffs_explicit():
    assert MUFRAD_WORD_RULE.invalidating_differences
