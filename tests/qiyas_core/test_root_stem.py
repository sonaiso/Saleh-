"""SCG-P3 RootStemClosure — behavioral runtime tests.

Narrow SCG-P3 implementation (2026-06-18). Closes a structural root/stem
POSSIBILITY: RegistryProjectionCandidate -> RootStemCandidate.

Candidate-only and structural-only (ROOT_STEM_CLOSURE_CONSTITUTION.md): NOT final
root extraction (RootCandidate forbidden), NOT wazn (WeightCandidate forbidden),
NOT morphology / wordhood / meaning / i'rab / hukm. Opens jamid/mushtaq +
word-pattern priors; emits no JamidMushtaqCandidate / downstream / semantic output.
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
from qiyas_core.root_stem_adapter import (
    OPENED_PRIOR_PREFIX,
    REGISTRY_PROJECTION_REF_PREFIX,
    ROOT_PATTERN_EVIDENCE_PREFIX,
    ROOT_STEM_SIGNATURE_PREFIX,
    SLOT_SEQUENCE_REFS_PREFIX,
    STEM_BOUNDARY_EVIDENCE_PREFIX,
    RootStemLayerAdapter,
)
from qiyas_core.rules.root_stem_rules import OPENED_PRIORS, ROOT_STEM_RULE


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


def _close(projection):
    return RootStemLayerAdapter(kernel=QiyasKernel()).close(projection)


def _has_trace(candidate, prefix):
    return any(t.startswith(prefix) for t in candidate.trace_ids)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# P3-RUN-OUTPUT
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_RUN_01_projection_closes_to_root_stem_candidate():
    result = _close(_projection())
    assert result.accepted
    assert result.accepted[0].candidate_type == "RootStemCandidate"


def test_P3_RUN_02_consumes_registry_projection_far_type():
    assert ROOT_STEM_RULE.far_type == "RegistryProjectionCandidate"
    assert ROOT_STEM_RULE.output_candidate_type == "RootStemCandidate"


def test_P3_RUN_03_candidate_only():
    assert "CandidateOnly" in _close(_projection()).accepted[0].output_flags


# ─────────────────────────────────────────────────────────────────────────────
# P3-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_IDENTITY_01_preserves_slot_candidate_identities():
    proj = _projection()
    c = _close(proj).accepted[0]
    for iid in proj.identity_ids:
        assert iid in c.identity_ids, iid


def test_P3_TRACE_01_identity_disjoint_from_trace():
    c = _close(_projection()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P3-STRUCTURAL — structural evidence only; opens priors
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_STRUCTURAL_01_carries_structural_root_stem_signature():
    c = _close(_projection()).accepted[0]
    sig = _trace_value(c, ROOT_STEM_SIGNATURE_PREFIX)
    assert sig is not None and sig.startswith("rootstemsig:")  # geometry signature, no root/wazn


def test_P3_STRUCTURAL_02_carries_required_structural_evidence():
    c = _close(_projection()).accepted[0]
    assert _has_trace(c, REGISTRY_PROJECTION_REF_PREFIX)
    assert _has_trace(c, SLOT_SEQUENCE_REFS_PREFIX)
    assert _has_trace(c, ROOT_PATTERN_EVIDENCE_PREFIX)
    assert _has_trace(c, STEM_BOUNDARY_EVIDENCE_PREFIX)


def test_P3_STRUCTURAL_03_opens_jamid_mushtaq_and_word_pattern_priors():
    c = _close(_projection()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"jamid_mushtaq_candidates", "word_pattern_candidates"}


def test_P3_STRUCTURAL_04_does_not_emit_jamid_mushtaq():
    c = _close(_projection()).accepted[0]
    assert c.candidate_type != "JamidMushtaqCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P3-FORBIDDEN — no final root / no wazn / no morphology / no meaning / no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_FORBIDDEN_01_no_final_root_no_wazn_no_word_no_meaning():
    forbidden = set(ROOT_STEM_RULE.forbidden_outputs)
    for name in ("RootCandidate", "WeightCandidate", "FormCandidate", "WordCandidate",
                 "MeaningCandidate", "DalalahCandidate", "Irab", "CaseEffect"):
        assert name in forbidden, name


def test_P3_FORBIDDEN_02_no_jump_to_p4_plus_or_absolutes():
    forbidden = set(ROOT_STEM_RULE.forbidden_outputs)
    for name in ("JamidMushtaqCandidate", "MufradWordCandidate", "VerbalSignifiedCandidate",
                 "IfadahCandidate", "SlotGeometry", "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P3_FORBIDDEN_03_root_stem_candidate_is_not_root_candidate():
    # The output is a structural POSSIBILITY, not a final root.
    assert ROOT_STEM_RULE.output_candidate_type == "RootStemCandidate"
    assert "RootCandidate" in ROOT_STEM_RULE.forbidden_outputs


def test_P3_FORBIDDEN_04_residual_diffs_explicit():
    assert ROOT_STEM_RULE.invalidating_differences
