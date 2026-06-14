"""REC-5 slot_geometry YAML schema — enforcement tests.

Authority: PROJECT_RECOVERY_CANONICAL_MAP.md §7 (REC-5) + §8 supreme law
(لا Runtime بلا YAML مصدّق). REC-5 adds a *validated source artifact* for the
canonical LayerSpecs:

  schemas/slot_geometry/layerspec.schema.yaml  — validation contract
  schemas/slot_geometry/layers.yaml            — the 19 LayerSpecs serialized

The Python registry (`build_master_registry_seed()`) remains the single runtime
source of truth. The YAML is **not** read or executed by any runtime code
(REC-5 non-goal: "No runtime execution of YAML"). These tests prove the source
is structurally valid and faithfully mirrors the registry.

  REC5-SCHEMA-*       — the schema file is a well-formed JSON-Schema
  REC5-DATA-*         — the source file parses and is well-formed
  REC5-VALIDATE-*     — the source validates against the schema
  REC5-CONSISTENCY-*  — the source mirrors build_master_registry_seed()
  REC5-ABSOLUTE-*     — every layer forbids Hukm/Reality/FinalMeaning
  REC5-NORUNTIME-*    — no runtime execution path for the YAML
  REC5-FREEZE-*       — no status advancement; REC-3 naming preserved
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")
jsonschema = pytest.importorskip("jsonschema")

from qiyas_core.slot_geometry_core import build_master_registry_seed

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_FILE = REPO_ROOT / "schemas" / "slot_geometry" / "layerspec.schema.yaml"
DATA_FILE = REPO_ROOT / "schemas" / "slot_geometry" / "layers.yaml"
SRC = REPO_ROOT / "src"

EXPECTED_LAYER_COUNT = 19


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _schema():
    return _load(SCHEMA_FILE)


def _document():
    return _load(DATA_FILE)


def _spec_to_dict(spec) -> "OrderedDict":
    """Mirror a registry LayerSpec into the YAML source shape (drift guard)."""
    return OrderedDict(
        id=spec.id,
        name=spec.name,
        phase=spec.phase,
        status=spec.status.value,
        origin=OrderedDict(
            layer_id=spec.origin.layer_id, output_type=spec.origin.output_type
        ),
        branch=OrderedDict(
            output_type=spec.branch.output_type, branch_reason=spec.branch.branch_reason
        ),
        shared_cause=spec.shared_cause,
        conditions=list(spec.conditions),
        blockers=list(spec.blockers),
        invalidating_differences=list(spec.invalidating_differences),
        target_boundary_closes=list(spec.target_boundary_closes),
        target_boundary_opens=list(spec.target_boundary_opens),
        forbidden_outputs=list(spec.forbidden_outputs),
        minimum_required_fields=list(spec.minimum_required_fields),
        preserves_ids=list(spec.preserves_ids),
        allowed_changes=list(spec.allowed_changes),
        forbidden_changes=list(spec.forbidden_changes),
        allowed_previous_layer_ids=list(spec.allowed_previous_layer_ids),
        allowed_next_layer_ids=list(spec.allowed_next_layer_ids),
        forbidden_direct_next_layer_ids=list(spec.forbidden_direct_next_layer_ids),
    )


def _registry_by_id():
    return {s.id: s for s in build_master_registry_seed().all_layers()}


# ─────────────────────────────────────────────────────────────────────────────
# REC5-SCHEMA
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_SCHEMA_01_schema_file_exists_and_parses():
    """REC5-SCHEMA-01: the schema file exists and parses as YAML."""
    assert SCHEMA_FILE.is_file()
    assert isinstance(_schema(), dict)


def test_REC5_SCHEMA_02_schema_is_valid_jsonschema():
    """REC5-SCHEMA-02: the schema is a well-formed Draft-07 JSON-Schema."""
    jsonschema.Draft7Validator.check_schema(_schema())


# ─────────────────────────────────────────────────────────────────────────────
# REC5-DATA
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_DATA_01_source_file_exists_and_parses():
    """REC5-DATA-01: the source file exists and parses as YAML."""
    assert DATA_FILE.is_file()
    doc = _document()
    assert isinstance(doc, dict)
    assert isinstance(doc.get("layers"), list)


def test_REC5_DATA_02_layer_count_field_matches_list_and_expected():
    """REC5-DATA-02: declared layer_count equals the list length and is 19."""
    doc = _document()
    assert doc["layer_count"] == len(doc["layers"]) == EXPECTED_LAYER_COUNT


def test_REC5_DATA_03_ids_unique():
    """REC5-DATA-03: layer ids in the source are unique."""
    ids = [layer["id"] for layer in _document()["layers"]]
    assert len(ids) == len(set(ids))


# ─────────────────────────────────────────────────────────────────────────────
# REC5-VALIDATE
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_VALIDATE_01_source_validates_against_schema():
    """REC5-VALIDATE-01: the source document validates against the schema."""
    jsonschema.validate(instance=_document(), schema=_schema())


# ─────────────────────────────────────────────────────────────────────────────
# REC5-CONSISTENCY — the source mirrors the canonical registry
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_CONSISTENCY_01_same_id_set():
    """REC5-CONSISTENCY-01: source ids equal the registered layer ids."""
    yaml_ids = {layer["id"] for layer in _document()["layers"]}
    assert yaml_ids == set(_registry_by_id())


def test_REC5_CONSISTENCY_02_same_count():
    """REC5-CONSISTENCY-02: source and registry agree on the layer count."""
    assert len(_document()["layers"]) == len(_registry_by_id()) == EXPECTED_LAYER_COUNT


def test_REC5_CONSISTENCY_03_every_layer_matches_registry_field_by_field():
    """REC5-CONSISTENCY-03: each source entry equals its registry LayerSpec
    field-by-field (full drift guard)."""
    registry = _registry_by_id()
    for layer in _document()["layers"]:
        spec = registry[layer["id"]]
        expected = _spec_to_dict(spec)
        # Compare as plain dicts (OrderedDict == dict by content in Python 3).
        assert dict(layer) == dict(expected), layer["id"]


def test_REC5_CONSISTENCY_04_source_order_matches_registry_order():
    """REC5-CONSISTENCY-04: source preserves registry registration order."""
    yaml_ids = [layer["id"] for layer in _document()["layers"]]
    registry_ids = [s.id for s in build_master_registry_seed().all_layers()]
    assert yaml_ids == registry_ids


# ─────────────────────────────────────────────────────────────────────────────
# REC5-ABSOLUTE
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_ABSOLUTE_01_every_layer_forbids_absolute_outputs():
    """REC5-ABSOLUTE-01: every source layer forbids the absolute outputs."""
    for layer in _document()["layers"]:
        for name in ("HukmCandidate", "RealityClaim", "FinalMeaning"):
            assert name in layer["forbidden_outputs"], layer["id"]


# ─────────────────────────────────────────────────────────────────────────────
# REC5-NORUNTIME — REC-5 introduces no runtime execution of YAML
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_NORUNTIME_01_no_slot_geometry_yaml_package():
    """REC5-NORUNTIME-01: no slot_geometry_yaml runtime package exists."""
    assert not (SRC / "qiyas_core" / "slot_geometry_yaml").exists()


def test_REC5_NORUNTIME_02_runtime_does_not_read_the_yaml():
    """REC5-NORUNTIME-02: no src/ module imports yaml or references the schema
    files — the YAML is a source artifact, not a runtime input."""
    offenders = []
    for path in SRC.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "import yaml" in text or "schemas/slot_geometry" in text:
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert offenders == [], offenders


# ─────────────────────────────────────────────────────────────────────────────
# REC5-FREEZE — no status advancement; REC-3 naming preserved
# ─────────────────────────────────────────────────────────────────────────────

def test_REC5_FREEZE_01_statuses_match_registry_no_advancement():
    """REC5-FREEZE-01: source statuses equal current registry statuses."""
    registry = _registry_by_id()
    for layer in _document()["layers"]:
        assert layer["status"] == registry[layer["id"]].status.value, layer["id"]


def test_REC5_FREEZE_02_rec3_naming_preserved_in_source():
    """REC5-FREEZE-02: the source carries the REC-3 canonical haraka id/name and
    not the legacy spelling."""
    layers = _document()["layers"]
    ids = {layer["id"] for layer in layers}
    assert "P1_HARAKA_MARK_IDENTITY_CARRIER" in ids
    assert "P1_HARAKA_FUNCTION_CARRIER" not in ids
    haraka = next(l for l in layers if l["id"] == "P1_HARAKA_MARK_IDENTITY_CARRIER")
    assert haraka["name"] == "HarakaMarkIdentityCarrierLayer"
    assert haraka["branch"]["output_type"] == "HarakaMarkIdentityCarrier"
