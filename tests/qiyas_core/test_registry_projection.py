"""SCG-P2 RegistryProjection — behavioral runtime tests.

Narrow SCG-P2 implementation authorization (2026-06-18). Projects a SlotCandidate
onto registry membership classes: SlotCandidate -> RegistryProjectionCandidate.

Structural-only (REGISTRY_PROJECTION_CONSTITUTION.md §§9–12): registry_entry_ref =
canonical structural signature from slot geometry (no class names); membership_
prior_type = a STRUCTURAL registry category (never a linguistic one); opens
root/stem + word-type priors; emits NO RootStemCandidate / downstream / semantic
output.
"""

from __future__ import annotations

from qiyas_core.kernel import QiyasKernel
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.conditioned_typed_sequence_adapter import ConditionedTypedSequenceLayerAdapter
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.slot_adapter import SlotLayerAdapter
from qiyas_core.registry_projection_adapter import (
    MEMBERSHIP_PRIOR_TYPE_PREFIX,
    OPENED_PRIOR_PREFIX,
    REGISTRY_ENTRY_REF_PREFIX,
    RegistryProjectionLayerAdapter,
)
from qiyas_core.rules.registry_projection_rules import (
    ALLOWED_MEMBERSHIP_PRIOR_TYPES,
    OPENED_PRIORS,
    REGISTRY_PROJECTION_RULE,
)

_LINGUISTIC_FORBIDDEN = {"Verb", "Noun", "Particle", "Derived", "Jamid", "Mushtaq", "Root", "Wazn"}


def _real_slot():
    """A real SlotCandidate for بَ (BAA+FATHA) via the canonical P1 chain."""
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
    return SlotLayerAdapter(kernel=k).compose_slot(letter, haraka, pos, alignment_evidence=cb).accepted[0]


def _project(slot):
    return RegistryProjectionLayerAdapter(kernel=QiyasKernel()).project(slot)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# P2-RUN-OUTPUT
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_RUN_01_slot_projects_to_registry_projection_candidate():
    result = _project(_real_slot())
    assert result.accepted, "a licensed SlotCandidate must project"
    assert result.accepted[0].candidate_type == "RegistryProjectionCandidate"


def test_P2_RUN_02_consumes_slot_candidate_far_type():
    assert REGISTRY_PROJECTION_RULE.far_type == "SlotCandidate"
    assert REGISTRY_PROJECTION_RULE.output_candidate_type == "RegistryProjectionCandidate"


def test_P2_RUN_03_output_is_candidate_only():
    c = _project(_real_slot()).accepted[0]
    assert "CandidateOnly" in c.output_flags


# ─────────────────────────────────────────────────────────────────────────────
# P2-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_IDENTITY_01_preserves_slot_candidate_identity():
    slot = _real_slot()
    c = _project(slot).accepted[0]
    # Every slot identity must ride through (slot_candidate_identity preserved).
    for iid in slot.identity_ids:
        assert iid in c.identity_ids, iid


def test_P2_TRACE_01_identity_disjoint_from_trace():
    c = _project(_real_slot()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P2-PROJECTION — registry_entry_ref + membership_prior_type (structural only)
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_PROJECTION_01_carries_structural_registry_entry_ref():
    c = _project(_real_slot()).accepted[0]
    ref = _trace_value(c, REGISTRY_ENTRY_REF_PREFIX)
    assert ref is not None and ref.startswith("geomsig:")  # structural signature, no class name


def test_P2_PROJECTION_02_membership_prior_type_is_structural_not_linguistic():
    c = _project(_real_slot()).accepted[0]
    mpt = _trace_value(c, MEMBERSHIP_PRIOR_TYPE_PREFIX)
    assert mpt in ALLOWED_MEMBERSHIP_PRIOR_TYPES, mpt
    assert mpt not in _LINGUISTIC_FORBIDDEN
    assert mpt == "GeometryMembershipClass"


def test_P2_PROJECTION_03_opens_root_stem_and_word_type_priors():
    c = _project(_real_slot()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"root_stem_candidates", "word_type_priors"}


def test_P2_PROJECTION_04_does_not_emit_root_stem_candidate():
    c = _project(_real_slot()).accepted[0]
    assert c.candidate_type != "RootStemCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P2-FORBIDDEN — no-jump + no morphology/meaning/hukm
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_FORBIDDEN_01_forbids_downstream_and_semantic_outputs():
    forbidden = set(REGISTRY_PROJECTION_RULE.forbidden_outputs)
    for name in (
        "RootStemCandidate", "JamidMushtaqCandidate", "MufradWordCandidate",
        "VerbalSignifiedCandidate", "IfadahCandidate", "SlotGeometry",
        "RootCandidate", "WeightCandidate", "MeaningCandidate", "DalalahCandidate",
        "HukmCandidate", "RealityClaim", "FinalMeaning", "Irab", "CaseEffect",
    ):
        assert name in forbidden, name


def test_P2_FORBIDDEN_02_residual_diffs_explicit():
    assert REGISTRY_PROJECTION_RULE.invalidating_differences
