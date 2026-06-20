"""SCG-P1 PR-3 SlotCandidate convergence IMPLEMENTED — enforcement tests (P1-IMPL-*).

Narrow SCG-P1 PR-3 implementation authorization (2026-06-17). Advances ONLY
P1_SLOT_CANDIDATE from SPECIFIED to IMPLEMENTED via
`build_p1_slot_implemented_registry`, atop the four implemented ingredient
layers (PR-1 atomic carriers + PR-2 sequence/position). With this, all five P1
layers are IMPLEMENTED (P1 phase complete).

slot_adapter is CERTIFY_AS_IS — it already composes the four pillars and produces
SlotCandidates end-to-end (kataba). PR-3 is registry status + conformance tests.

SlotCandidate stays LOCAL-only: no SlotGeometry, no P2/RegistryProjection, no
syllable/word/root/meaning/grammar. P2-P12 remain SPECIFIED; freeze ACTIVE.
"""

from __future__ import annotations

from qiyas_core.kernel import QiyasKernel
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.conditioned_typed_sequence_adapter import ConditionedTypedSequenceLayerAdapter
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.slot_adapter import SlotLayerAdapter
from qiyas_core.slot_geometry_core import (
    LayerStatus,
    build_p1_sequence_position_implemented_registry,
    build_p1_slot_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)

_P1_ALL = (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)


def _build_real_slot():
    """Compose a SlotCandidate from the four REAL layer outputs via the canonical
    adapter chain (mirrors run_qiyas.py), for بَ (BAA + FATHA)."""
    kernel = QiyasKernel()
    typed = TypedCodePointLayerAdapter(kernel=kernel)
    letter_typed = typed.classify_codepoint(0x0628).accepted[0]   # ب
    haraka_typed = typed.classify_codepoint(0x064E).accepted[0]   # ◌َ
    letter = LetterIdentityLayerAdapter(kernel=kernel).process_letter_codepoint(letter_typed).accepted[0]
    haraka = HarakaFunctionLayerAdapter(kernel=kernel).prove_from_codepoint(0x064E).accepted[0]
    cts = ConditionedTypedSequenceLayerAdapter(kernel=kernel)
    pe = cts.prove_letter_position(letter_typed, index=0, sequence_length=2).accepted[0]
    position = PositionLayerAdapter(kernel=kernel).prove_position(pe, index=0).accepted[0]
    cb = cts.prove_carrier_binding(
        haraka_typed=haraka_typed, carrier_letter_typed=letter_typed,
        index=1, sequence_length=2,
    ).accepted[0]
    return letter, haraka, position, cb, SlotLayerAdapter(kernel=kernel).compose_slot(
        letter, haraka, position, alignment_evidence=cb
    )


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-ADVANCE — only Slot advanced; P1 phase complete
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_ADVANCE_01_slot_implemented():
    assert build_p1_slot_implemented_registry().get(LAYER_ID_P1_SLOT_CANDIDATE).status is LayerStatus.IMPLEMENTED


def test_P1_IMPL_ADVANCE_02_all_five_p1_layers_implemented():
    reg = build_p1_slot_implemented_registry()
    for lid in _P1_ALL:
        assert reg.get(lid).status is LayerStatus.IMPLEMENTED, lid


def test_P1_IMPL_ADVANCE_03_base_leaves_slot_specified():
    base = build_p1_sequence_position_implemented_registry()
    assert base.get(LAYER_ID_P1_SLOT_CANDIDATE).status is LayerStatus.SPECIFIED


def test_P1_IMPL_ADVANCE_04_p2_p12_remain_specified_p0_implemented():
    reg = build_p1_slot_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1")
    )


def test_P1_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p1_slot_implemented_registry().all_layers())) == 19


def test_P1_IMPL_ADVANCE_06_only_p0_and_all_p1_implemented():
    reg = build_p1_slot_implemented_registry()
    impl = {s.id for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    p0 = {s.id for s in reg.all_layers() if s.phase == "SCG-P0"}
    assert impl == p0 | set(_P1_ALL)


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-NOFULL — slot-only partial, not the prohibited full builder
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P1_IMPL_NOFULL_02_no_full_p1_or_p4_implemented_builder():
    # build_p2/build_p3_implemented_registry are authorized as of SCG-P2/P3.
    assert not hasattr(MRS, "build_p1_implemented_registry")
    assert not hasattr(MRS, "build_p10_implemented_registry")


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-GATE — Slot's declared origin (Letter) is IMPLEMENTED
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_GATE_01_slot_origin_is_letter_and_implemented():
    seed = MRS.build_master_registry_seed()
    assert seed.get(LAYER_ID_P1_SLOT_CANDIDATE).origin.layer_id == LAYER_ID_P1_LETTER_IDENTITY_CARRIER
    reg = build_p1_slot_implemented_registry()
    assert reg.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER).status is LayerStatus.IMPLEMENTED


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-CONFORMANCE — SlotCandidate from the four real layer outputs
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_CONFORMANCE_01_slot_built_from_four_real_ingredients():
    letter, haraka, position, cb, result = _build_real_slot()
    assert letter.candidate_type == "LetterIdentityCarrier"
    assert haraka.candidate_type == "HarakaMarkIdentityCarrier"   # canonical, accepted by slot
    assert position.candidate_type == "PositionCarrier"
    assert cb.candidate_type == "CarrierBindingCandidate"
    assert result.accepted, "all four ingredients present must yield a SlotCandidate"
    assert result.accepted[0].candidate_type == "SlotCandidate"


def test_P1_IMPL_CONFORMANCE_02_output_type_matches_layerspec():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P1_SLOT_CANDIDATE)
    assert spec.branch.output_type == "SlotCandidate"
    *_, result = _build_real_slot()
    assert result.accepted[0].candidate_type == spec.branch.output_type


def test_P1_IMPL_CONFORMANCE_03_canonical_haraka_accepted_by_slot():
    _, haraka, _, _, result = _build_real_slot()
    # PR-1 canonical name flows through slot despite the transitional alias.
    assert haraka.candidate_type == "HarakaMarkIdentityCarrier"
    assert result.accepted, "slot must accept the canonical HarakaMarkIdentityCarrier"


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-LOCAL — SlotCandidate is local only
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_LOCAL_01_forbids_slotgeometry_and_downstream():
    from qiyas_core.rules.slot_rules import SLOT_COMPOSITION_RULE
    forbidden = set(SLOT_COMPOSITION_RULE.forbidden_outputs)
    for name in ("SlotGeometry", "SyllableCandidate", "MeaningCandidate", "RootCandidate",
                 "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P1_IMPL_LOCAL_02_output_is_slot_candidate_not_geometry_or_p2():
    *_, result = _build_real_slot()
    ct = result.accepted[0].candidate_type
    assert ct == "SlotCandidate"
    assert ct not in ("SlotGeometry", "RegistryProjectionCandidate")
