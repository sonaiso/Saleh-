"""SCG-P4 JamidMushtaq — behavioral runtime tests.

Narrow SCG-P4 implementation (2026-06-18). Opens a structural derivation-class
POSSIBILITY: RootStemCandidate -> JamidMushtaqCandidate.

Candidate-only and structural-only (JAMID_MUSHTAQ_CONSTITUTION.md): NOT a final
جامد/مشتق judgment (WordTypeJudgment forbidden), NOT wazn (WeightCandidate
forbidden), NOT morphology / wordhood / meaning / i'rab / hukm. The
jamid_mushtaq_prior_type is a STRUCTURAL category, never a linguistic one. Opens
word-type priors; emits no MufradWordCandidate / downstream / semantic output.
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
from qiyas_core.jamid_mushtaq_adapter import (
    DERIVATION_POSSIBILITY_PREFIX,
    JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX,
    OPENED_PRIOR_PREFIX,
    PATTERN_EVIDENCE_PREFIX,
    ROOT_STEM_CANDIDATE_REF_PREFIX,
    JamidMushtaqLayerAdapter,
)
from qiyas_core.rules.jamid_mushtaq_rules import (
    ALLOWED_DERIVATION_PRIOR_TYPES,
    JAMID_MUSHTAQ_RULE,
    OPENED_PRIORS,
)

_LINGUISTIC_FORBIDDEN = {"Jamid", "Mushtaq", "Derived", "Verb", "Noun", "Particle", "Root", "Wazn"}


def _root_stem():
    """A real RootStemCandidate for بَ via the full P1->P2->P3 chain."""
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
    return RootStemLayerAdapter(kernel=k).close(proj).accepted[0]


def _classify(root_stem):
    return JamidMushtaqLayerAdapter(kernel=QiyasKernel()).classify(root_stem)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


def _has_trace(candidate, prefix):
    return any(t.startswith(prefix) for t in candidate.trace_ids)


# ─────────────────────────────────────────────────────────────────────────────
# P4-RUN-OUTPUT
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_RUN_01_root_stem_classifies_to_jamid_mushtaq_candidate():
    result = _classify(_root_stem())
    assert result.accepted
    assert result.accepted[0].candidate_type == "JamidMushtaqCandidate"


def test_P4_RUN_02_consumes_root_stem_far_type():
    assert JAMID_MUSHTAQ_RULE.far_type == "RootStemCandidate"
    assert JAMID_MUSHTAQ_RULE.output_candidate_type == "JamidMushtaqCandidate"


def test_P4_RUN_03_candidate_only():
    assert "CandidateOnly" in _classify(_root_stem()).accepted[0].output_flags


# ─────────────────────────────────────────────────────────────────────────────
# P4-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_IDENTITY_01_preserves_identities():
    rs = _root_stem()
    c = _classify(rs).accepted[0]
    for iid in rs.identity_ids:
        assert iid in c.identity_ids, iid


def test_P4_TRACE_01_identity_disjoint_from_trace():
    c = _classify(_root_stem()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P4-STRUCTURAL — structural derivation possibility; prior type NOT linguistic
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_STRUCTURAL_01_carries_structural_derivation_possibility():
    c = _classify(_root_stem()).accepted[0]
    sig = _trace_value(c, DERIVATION_POSSIBILITY_PREFIX)
    assert sig is not None and sig.startswith("derivsig:")  # geometry signature, no judgment


def test_P4_STRUCTURAL_02_prior_type_is_structural_not_linguistic():
    c = _classify(_root_stem()).accepted[0]
    pt = _trace_value(c, JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX)
    assert pt in ALLOWED_DERIVATION_PRIOR_TYPES, pt
    assert pt not in _LINGUISTIC_FORBIDDEN
    assert pt == "DerivationGeometryClass"


def test_P4_STRUCTURAL_03_carries_root_stem_ref_and_pattern_evidence():
    c = _classify(_root_stem()).accepted[0]
    assert _has_trace(c, ROOT_STEM_CANDIDATE_REF_PREFIX)
    assert _has_trace(c, PATTERN_EVIDENCE_PREFIX)


def test_P4_STRUCTURAL_04_opens_word_type_priors():
    c = _classify(_root_stem()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"word_type_candidates"}


def test_P4_STRUCTURAL_05_does_not_emit_mufrad_word():
    c = _classify(_root_stem()).accepted[0]
    assert c.candidate_type != "MufradWordCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P4-FORBIDDEN — no final judgment / no wazn / no morphology / no meaning / no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_FORBIDDEN_01_no_final_judgment_no_wazn_no_word_no_meaning():
    forbidden = set(JAMID_MUSHTAQ_RULE.forbidden_outputs)
    for name in ("WordTypeJudgment", "WeightCandidate", "RootCandidate", "FormCandidate",
                 "WordCandidate", "MeaningCandidate", "DalalahCandidate", "IrabCandidate",
                 "CaseEffect", "Irab"):
        assert name in forbidden, name


def test_P4_FORBIDDEN_02_no_jump_to_p5_plus_or_absolutes():
    forbidden = set(JAMID_MUSHTAQ_RULE.forbidden_outputs)
    for name in ("MufradWordCandidate", "VerbalSignifiedCandidate", "IfadahCandidate",
                 "SlotGeometry", "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P4_FORBIDDEN_03_residual_diffs_explicit():
    assert JAMID_MUSHTAQ_RULE.invalidating_differences
