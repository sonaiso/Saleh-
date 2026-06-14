"""REC-3 Naming Correction (option O3) — enforcement tests.

Authority: PROJECT_RECOVERY_CANONICAL_MAP.md §6.1 (suspension ruling) + §7
(REC-3 row), executed as **option O3**: registry + docs surface rename plus
transitional compatibility aliases. Conversion table: TERMINOLOGY_MAP.md §8.

The atomic haraka layer is renamed:

    HarakaFunctionCarrier      → HarakaMarkIdentityCarrier
    P1_HARAKA_FUNCTION_CARRIER → P1_HARAKA_MARK_IDENTITY_CARRIER

Ruling: الحركة أولًا علامة ذات هوية؛ ثم لاحقًا قد تصير وظيفة، بعد Gate وسياق
وتركيب (the haraka is first a mark with an identity; function is a later, gated
claim). The correction removes a premature function claim and adds none.

These tests enforce:

  REC3-RENAME-*    — the canonical LayerSpec id/name/output_type are renamed
  REC3-ALIAS-*     — the legacy ID constant is a transitional alias to the new id
  REC3-NOTCANON-*  — the legacy name/id is NOT any registered canonical surface
  REC3-PRESERVE-*  — layer count, phase, status, boundaries unchanged
  REC3-BOUNDARY-*  — sibling forbidden_outputs keep BOTH names (transition-safe)
  REC3-DEFER-*     — O3 did not rename the runtime adapter/rules (deferred)
  REC3-DOC-*       — docs record the terminology conversion
"""

from __future__ import annotations

from pathlib import Path

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    build_master_registry_seed,
    build_p1_specified_registry,
)
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P0_TYPED_CODEPOINT,
    LAYER_ORIGIN_NOTES,
    ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
)

LEGACY_NAME = "HarakaFunctionCarrierLayer"
LEGACY_ID = "P1_HARAKA_FUNCTION_CARRIER"
LEGACY_OUTPUT = "HarakaFunctionCarrier"
CANON_NAME = "HarakaMarkIdentityCarrierLayer"
CANON_ID = "P1_HARAKA_MARK_IDENTITY_CARRIER"
CANON_OUTPUT = "HarakaMarkIdentityCarrier"

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "docs" / "qiyas_core"
SRC = REPO_ROOT / "src"
TERMINOLOGY_MAP_DOC = DOCS / "TERMINOLOGY_MAP.md"
LAYER_REGISTRY_DOC = DOCS / "LAYER_REGISTRY.md"
RECOVERY_MAP_DOC = DOCS / "PROJECT_RECOVERY_CANONICAL_MAP.md"
HARAKA_ADAPTER_SRC = SRC / "qiyas_core" / "haraka_function_adapter.py"
HARAKA_RULES_SRC = SRC / "qiyas_core" / "rules" / "haraka_function_rules.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _haraka_spec():
    return build_p1_specified_registry().get(CANON_ID)


# ─────────────────────────────────────────────────────────────────────────────
# REC3-RENAME — the canonical surface is renamed
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_RENAME_01_canonical_id():
    """REC3-RENAME-01: the canonical LayerSpec id is the new string."""
    assert _haraka_spec().id == CANON_ID
    assert LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER == CANON_ID


def test_REC3_RENAME_02_canonical_name():
    """REC3-RENAME-02: the canonical LayerSpec name is HarakaMarkIdentityCarrierLayer."""
    assert _haraka_spec().name == CANON_NAME


def test_REC3_RENAME_03_canonical_output_type():
    """REC3-RENAME-03: the canonical output_type is HarakaMarkIdentityCarrier."""
    assert _haraka_spec().branch.output_type == CANON_OUTPUT


# ─────────────────────────────────────────────────────────────────────────────
# REC3-ALIAS — transitional compatibility alias
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_ALIAS_01_legacy_constant_resolves_to_new_id():
    """REC3-ALIAS-01: the legacy ID constant resolves to the new canonical id."""
    assert LAYER_ID_P1_HARAKA_FUNCTION_CARRIER == CANON_ID


def test_REC3_ALIAS_02_lookup_via_legacy_constant_works():
    """REC3-ALIAS-02: registry.get via the legacy constant returns the renamed layer."""
    registry = build_p1_specified_registry()
    assert registry.get(LAYER_ID_P1_HARAKA_FUNCTION_CARRIER).id == CANON_ID


# ─────────────────────────────────────────────────────────────────────────────
# REC3-NOTCANON — the legacy name/id is not the canonical surface anymore
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_NOTCANON_01_legacy_id_string_is_not_canonical():
    """REC3-NOTCANON-01: the literal legacy id string is not the canonical id."""
    assert LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER != LEGACY_ID
    assert LAYER_ID_P1_HARAKA_FUNCTION_CARRIER != LEGACY_ID


def test_REC3_NOTCANON_02_no_registered_layer_uses_legacy_surface():
    """REC3-NOTCANON-02: no registered layer carries the legacy name/id/output_type."""
    for spec in build_master_registry_seed().all_layers():
        assert spec.id != LEGACY_ID
        assert spec.name != LEGACY_NAME
        assert spec.branch.output_type != LEGACY_OUTPUT


def test_REC3_NOTCANON_03_seed_source_drops_legacy_layer_name():
    """REC3-NOTCANON-03: the registry seed no longer defines the legacy LayerSpec name."""
    seed = _read(SRC / "qiyas_core" / "slot_geometry_core" / "master_registry_seed.py")
    assert CANON_NAME in seed
    assert LEGACY_NAME not in seed


# ─────────────────────────────────────────────────────────────────────────────
# REC3-PRESERVE — count, phase, status, origin, absolute boundaries unchanged
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_PRESERVE_01_layer_count_unchanged():
    """REC3-PRESERVE-01: the seed still has exactly 19 layers."""
    assert len(list(build_master_registry_seed().all_layers())) == 19


def test_REC3_PRESERVE_02_phase_unchanged():
    """REC3-PRESERVE-02: the renamed layer keeps phase SCG-P1."""
    assert _haraka_spec().phase == "SCG-P1"


def test_REC3_PRESERVE_03_status_unchanged():
    """REC3-PRESERVE-03: the renamed layer keeps status SPECIFIED in the P1 registry."""
    assert _haraka_spec().status == LayerStatus.SPECIFIED


def test_REC3_PRESERVE_04_origin_trace_preserved():
    """REC3-PRESERVE-04: the renamed layer keeps its الأصل الثاني origin note."""
    assert (
        LAYER_ORIGIN_NOTES[CANON_ID] == ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM
    )
    assert LEGACY_ID not in LAYER_ORIGIN_NOTES


def test_REC3_PRESERVE_05_origin_layer_id_unchanged():
    """REC3-PRESERVE-05: the renamed layer still branches from TypedCodePoint."""
    assert _haraka_spec().origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT


def test_REC3_PRESERVE_06_absolute_forbidden_outputs_intact():
    """REC3-PRESERVE-06: the renamed layer still forbids the absolute outputs."""
    forbidden = _haraka_spec().forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden


def test_REC3_PRESERVE_07_no_new_function_claim():
    """REC3-PRESERVE-07: the rename adds no SlotCandidate/SlotGeometry capability."""
    forbidden = _haraka_spec().forbidden_outputs
    assert "SlotCandidate" in forbidden
    assert "SlotGeometry" in forbidden


# ─────────────────────────────────────────────────────────────────────────────
# REC3-BOUNDARY — sibling forbidden_outputs keep BOTH names during transition
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_BOUNDARY_01_siblings_forbid_both_output_names():
    """REC3-BOUNDARY-01: parallel-proof siblings forbid BOTH the legacy and the
    canonical haraka output, preserving every boundary during the transition."""
    registry = build_p1_specified_registry()
    siblings = (
        LAYER_ID_P0_TYPED_CODEPOINT,
        LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
        LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
        LAYER_ID_P1_POSITION_CARRIER,
    )
    for layer_id in siblings:
        forbidden = registry.get(layer_id).forbidden_outputs
        assert LEGACY_OUTPUT in forbidden, layer_id
        assert CANON_OUTPUT in forbidden, layer_id


# ─────────────────────────────────────────────────────────────────────────────
# REC3-DEFER — O3 explicitly does NOT rename the runtime files
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_DEFER_01_runtime_adapter_keeps_legacy_spelling():
    """REC3-DEFER-01: the runtime adapter is out of O3 scope and keeps the legacy
    spelling (a full transitive rename was explicitly not performed)."""
    adapter = _read(HARAKA_ADAPTER_SRC)
    assert LEGACY_OUTPUT in adapter
    assert CANON_OUTPUT not in adapter


def test_REC3_DEFER_02_runtime_rules_keep_legacy_spelling():
    """REC3-DEFER-02: the runtime rules are out of O3 scope and keep the legacy
    spelling."""
    rules = _read(HARAKA_RULES_SRC)
    assert CANON_OUTPUT not in rules


# ─────────────────────────────────────────────────────────────────────────────
# REC3-DOC — the terminology conversion is documented
# ─────────────────────────────────────────────────────────────────────────────

def test_REC3_DOC_01_terminology_map_records_conversion():
    """REC3-DOC-01: TERMINOLOGY_MAP.md records the former → canonical conversion."""
    text = _read(TERMINOLOGY_MAP_DOC)
    assert LEGACY_OUTPUT in text
    assert CANON_OUTPUT in text
    assert LEGACY_ID in text
    assert CANON_ID in text


def test_REC3_DOC_02_layer_registry_uses_canonical_name():
    """REC3-DOC-02: LAYER_REGISTRY.md presents the canonical name and a REC-3 note."""
    text = _read(LAYER_REGISTRY_DOC)
    assert CANON_OUTPUT in text
    assert "REC-3" in text


def test_REC3_DOC_03_recovery_map_keeps_both_names():
    """REC3-DOC-03: the recovery map still records both the suspended legacy name
    and the corrective canonical name."""
    text = _read(RECOVERY_MAP_DOC)
    assert LEGACY_OUTPUT in text
    assert CANON_OUTPUT in text
