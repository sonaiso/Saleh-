"""test_master_layer_registry.py — implementation-dependency gate (GATE-*).

Narrow governance authorization (2026-06-16): add a structural gate inside
`MasterLayerRegistry.update_status` so that a layer cannot advance to
IMPLEMENTED unless its origin is already IMPLEMENTED. GOVERNANCE ONLY — no SCG
phase runtime, no `build_pN_implemented_registry`, no status changes to the
canonical seed/builders.

Hybrid rule (enforced by `_assert_origin_implemented`):

    On transition to IMPLEMENTED for layer L with origin O:
      - O == ROOT                  -> allow.
      - O.phase == L.phase (INTRA) -> require the specific origin layer O IMPLEMENTED.
      - O.phase != L.phase (CROSS) -> require every layer in O.phase IMPLEMENTED.
      - otherwise                  -> RegistryViolation.

DEFERRED (NOT implemented, by maintainer decision): the *origin-downgrade
companion* rule — preventing an origin from being downgraded out of IMPLEMENTED
while a consumer remains IMPLEMENTED — is recorded as deferred governance work.
`test_GATE_downgrade_companion_07_*` documents that current behavior does NOT
enforce it.

These tests build throwaway registries and flip statuses locally only to
exercise the guard; no runtime is implemented and no canonical builder is added.
"""

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p0_implemented_registry,
    build_p1_specified_registry,
    build_p2_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P0_GLYPH_CLASSIFICATION,
    LAYER_ID_P0_TYPED_CODEPOINT,
    LAYER_ID_P0_UNICODE_CANDIDATE,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
    LAYER_ID_P2_REGISTRY_PROJECTION,
)

# P1 layers in a dependency-safe implementation order (origins first):
#   Letter/Haraka/Conditioned consume P0 (CROSS, P0 fully implemented);
#   Position consumes Conditioned (INTRA); Slot consumes Letter (INTRA).
_P1_IMPL_ORDER = (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)


def _implement(reg, layer_id):
    """SPECIFIED->IMPLEMENTED helper (assumes already SPECIFIED)."""
    reg.update_status(layer_id, LayerStatus.IMPLEMENTED)


# ─────────────────────────────────────────────────────────────────────────────
# GATE-ROOT — ROOT-origin layers are exempt
# ─────────────────────────────────────────────────────────────────────────────


def test_GATE_ROOT_01_root_origin_layer_can_be_implemented():
    reg = build_master_registry_seed()
    # P0_UNICODE_CANDIDATE origin is ROOT -> gate must allow.
    reg.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.SPECIFIED)
    reg.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.IMPLEMENTED)
    assert reg.get(LAYER_ID_P0_UNICODE_CANDIDATE).status is LayerStatus.IMPLEMENTED


# ─────────────────────────────────────────────────────────────────────────────
# GATE-INTRA — same-phase origin must be the specific layer implemented
# ─────────────────────────────────────────────────────────────────────────────


def test_GATE_INTRA_02_blocks_when_specific_origin_layer_not_implemented():
    reg = build_master_registry_seed()
    # Bring Unicode + TypedCodePoint to SPECIFIED but DO NOT implement Unicode.
    reg.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.SPECIFIED)
    reg.update_status(LAYER_ID_P0_TYPED_CODEPOINT, LayerStatus.SPECIFIED)
    # TypedCodePoint origin = Unicode (INTRA, same phase P0), still SPECIFIED.
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P0_TYPED_CODEPOINT, LayerStatus.IMPLEMENTED)


def test_GATE_INTRA_03_allows_once_specific_origin_layer_implemented():
    reg = build_master_registry_seed()
    reg.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.SPECIFIED)
    reg.update_status(LAYER_ID_P0_TYPED_CODEPOINT, LayerStatus.SPECIFIED)
    _implement(reg, LAYER_ID_P0_UNICODE_CANDIDATE)  # origin now IMPLEMENTED
    _implement(reg, LAYER_ID_P0_TYPED_CODEPOINT)    # INTRA gate satisfied
    assert reg.get(LAYER_ID_P0_TYPED_CODEPOINT).status is LayerStatus.IMPLEMENTED


# ─────────────────────────────────────────────────────────────────────────────
# GATE-CROSS — different-phase origin requires the WHOLE origin phase implemented
# ─────────────────────────────────────────────────────────────────────────────


def test_GATE_CROSS_04_blocks_when_origin_phase_incomplete():
    # build_p1_specified: P0 IMPLEMENTED, P1 SPECIFIED (not implemented), P2 PLANNED.
    reg = build_p1_specified_registry()
    reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.SPECIFIED)
    # P2 origin = P1_SLOT_CANDIDATE (phase P1); P1 not fully IMPLEMENTED -> block.
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED)


def test_GATE_CROSS_05_allows_when_full_origin_phase_implemented():
    # Locally implement all of P1 (in dependency order), then P2 may implement.
    reg = build_p1_specified_registry()
    for layer_id in _P1_IMPL_ORDER:
        _implement(reg, layer_id)
    assert all(
        reg.get(lid).status is LayerStatus.IMPLEMENTED for lid in _P1_IMPL_ORDER
    )
    reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.SPECIFIED)
    reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED)
    assert reg.get(LAYER_ID_P2_REGISTRY_PROJECTION).status is LayerStatus.IMPLEMENTED


def test_GATE_CROSS_05b_partial_origin_phase_still_blocks():
    # Implement only part of P1 (omit SLOT) -> P2 still blocked.
    reg = build_p1_specified_registry()
    for layer_id in _P1_IMPL_ORDER[:-1]:  # everything except SLOT_CANDIDATE
        _implement(reg, layer_id)
    reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.SPECIFIED)
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED)


# ─────────────────────────────────────────────────────────────────────────────
# GATE-P0BUILDER — existing build_p0_implemented_registry remains valid
# ─────────────────────────────────────────────────────────────────────────────


def test_GATE_P0BUILDER_06_p0_implemented_builder_still_green():
    reg = build_p0_implemented_registry()
    p0 = [s for s in reg.all_layers() if s.phase == "SCG-P0"]
    assert p0 and all(s.status is LayerStatus.IMPLEMENTED for s in p0)
    # P1-P12 untouched by the P0 builder (remain PLANNED).
    assert all(
        s.status is LayerStatus.PLANNED for s in reg.all_layers() if s.phase != "SCG-P0"
    )


# ─────────────────────────────────────────────────────────────────────────────
# GATE-PREMATURE — P1/P2 premature IMPLEMENTED stays blocked; no impl builders
# ─────────────────────────────────────────────────────────────────────────────


def test_GATE_PREMATURE_07_p1_slot_premature_implemented_blocked():
    # From P0-implemented, P1 carriers are PLANNED; SlotCandidate's INTRA origin
    # (LetterIdentityCarrier) is not IMPLEMENTED -> SlotCandidate cannot implement.
    reg = build_p0_implemented_registry()
    reg.update_status(LAYER_ID_P1_SLOT_CANDIDATE, LayerStatus.SPECIFIED)
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P1_SLOT_CANDIDATE, LayerStatus.IMPLEMENTED)


def test_GATE_PREMATURE_08_p2_premature_implemented_blocked():
    reg = build_p2_specified_registry()  # P1+P2 SPECIFIED, P1 not implemented
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED)


def test_GATE_PREMATURE_09_no_full_p1_implemented_builder_exists():
    # The FULL build_p1_implemented_registry remains forbidden (P1 is completed
    # via slot-only partials). build_p2_implemented_registry is authorized as of
    # SCG-P2 (2026-06-18) and is intentionally NOT asserted absent here.
    assert not hasattr(MRS, "build_p1_implemented_registry")
    assert not hasattr(MRS, "build_p13_implemented_registry")


# ─────────────────────────────────────────────────────────────────────────────
# GATE-DEFERRED — origin-downgrade companion is intentionally NOT enforced
# ─────────────────────────────────────────────────────────────────────────────


def test_GATE_downgrade_companion_10_origin_downgrade_not_blocked_deferred():
    """Documents deferred behavior: downgrading an origin out of IMPLEMENTED is
    allowed even while a consumer remains IMPLEMENTED (companion rule deferred)."""
    reg = build_p0_implemented_registry()  # P0 fully IMPLEMENTED
    # Glyph (consumer of TypedCodePoint) is IMPLEMENTED; downgrading its origin
    # TypedCodePoint is currently permitted — the gate only checks on -> IMPLEMENTED.
    assert reg.get(LAYER_ID_P0_GLYPH_CLASSIFICATION).status is LayerStatus.IMPLEMENTED
    reg.update_status(LAYER_ID_P0_TYPED_CODEPOINT, LayerStatus.SPECIFIED)  # no raise
    assert reg.get(LAYER_ID_P0_TYPED_CODEPOINT).status is LayerStatus.SPECIFIED
