"""
test_slot_geometry_yaml_schema.py — PR-SCG-YAML-0

اختبارات التحقق من صحة ملفات YAML لطبقات SlotGeometry.

القانون:
    لا SlotGeometry بلا YAML.
    لا YAML بلا Origin وBranch.
    لا Origin/Branch بلا Qiyas.
    لا Qiyas بلا Boundary.
    لا Boundary بلا MinimumCompletion.
    لا MinimumCompletion بلا IdentityInheritance وTrace وResiduals وRank وGamma.

    YAML لا ينتج runtime.
    YAML لا يثبت حكمًا.
    YAML يعرّف SlotGeometrySpec قابلًا للتحقق.

معرّفات الاختبارات:
    SCG-YAML-LOAD-*     تحميل ملفات YAML
    SCG-YAML-VALID-*    التحقق من ملفات صالحة
    SCG-YAML-SCHEMA-*   فحص القالب الأعلى
    SCG-YAML-MISS-*     كشف الحقول المفقودة
    SCG-YAML-BOUND-*    فحص target_boundary
    SCG-YAML-FORB-*     فحص forbidden_outputs
    SCG-YAML-IDENT-*    فحص identity_inheritance
    SCG-YAML-GAMMA-*    فحص gamma
    SCG-YAML-REG-*      فحص registry
    SCG-YAML-RANK-*     فحص rank_ceiling
    SCG-YAML-STATUS-*   فحص status
    SCG-YAML-SPEC-*     فحص الملفات النموذجية
"""
from __future__ import annotations

import textwrap
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

from qiyas_core.slot_geometry_yaml import (
    AllowedForbiddenOverlap,
    EmptyIdentityInheritancePreserves,
    EmptyRequiredField,
    EmptyTargetBoundaryCloses,
    InvalidRankCeiling,
    InvalidStatusValue,
    MissingAbsoluteForbidden,
    MissingGammaTarget,
    MissingRequiredField,
    SchemaViolation,
    SlotGeometryValidator,
    SlotGeometryYAMLError,
    TargetBoundaryViolation,
    YAMLLoadError,
    load_slot_geometry_yaml,
)

# ─── مسارات الملفات النموذجية ────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).parent.parent.parent
_EXAMPLES = _REPO_ROOT / "examples" / "slot_geometries"
_SCHEMAS = _REPO_ROOT / "schemas"

_SG_ORIGIN = _EXAMPLES / "SG_ORIGIN_01_ARABIC_HUMAN_VOICE_TRACE.yaml"
_SG_DAL = _EXAMPLES / "SG_DAL_04_HARAKA_MARK_IDENTITY.yaml"
_SG_MANTUQ = _EXAMPLES / "SG_MANTUQ_00_MANTUQ_CANDIDATE.yaml"
_SCHEMA_FILE = _SCHEMAS / "slot_geometry.schema.yaml"


# ─── أداة مساعدة: بناء YAML مؤقت من نص ────────────────────────────────────

def _build_yaml(text: str, tmp_path: Path) -> Path:
    """اكتب محتوى YAML إلى ملف مؤقت وأعد مساره."""
    p = tmp_path / "test_spec.yaml"
    p.write_text(textwrap.dedent(text), encoding="utf-8")
    return p


def _minimal_valid_yaml(
    *,
    sg_id: str = "SG_TEST_01",
    name: str = "TestGeometry",
    phase: str = "TEST_PHASE",
    status: str = "PLANNED",
    origin_layer: str = "ORIGIN_LAYER",
    origin_output: str = "OriginType",
    branch_output: str = "BranchType",
    branch_reason: str = "test branch reason",
    rank_ceiling: str = "Candidate",
    shared_cause: str = "test shared cause",
    effective_attribute: str = "test effective attribute",
    branching_reason: str = "test branching reason",
    closes: str = "test_boundary",
    preserves: str = "origin_identity",
    registry_layer: str = "TEST_LAYER",
    gamma_target: str = "test_boundary",
) -> str:
    return f"""\
schema_version: "1.0"
slot_geometry:
  id: "{sg_id}"
  name: "{name}"
  phase: "{phase}"
  status: "{status}"
  origin:
    layer_id: "{origin_layer}"
    output_type: "{origin_output}"
    trace_required: true
    identity_required: true
    closure_required: "MINIMALLY_CLOSED"
  branch:
    output_type: "{branch_output}"
    branch_reason: "{branch_reason}"
    rank_ceiling: "{rank_ceiling}"
  qiyas:
    shared_cause: "{shared_cause}"
    effective_attribute: "{effective_attribute}"
    branching_reason: "{branching_reason}"
    conditions:
      - condition_one
    blockers: []
    invalidating_differences: []
  target_boundary:
    closes:
      - {closes}
    opens: []
    does_not_close: []
  minimum_completion:
    required:
      - origin_exists
      - branch_declared
  identity_inheritance:
    preserves:
      - {preserves}
    allowed_changes: []
    forbidden_changes: []
  forbidden_outputs:
    absolute:
      - HukmCandidate
      - RealityClaim
      - FinalMeaning
    layer_specific: []
  residual_policy:
    residuals_allowed: true
    residuals_must_be_visible: true
    blocking_residuals: []
    non_blocking_residuals: []
  trace:
    source_trace: true
    operation_trace: true
    evidence_trace: false
    residual_trace: true
  rank:
    initial: "Candidate"
    ceiling: "Candidate"
    upgrade_requires_gate: true
    allowed_upgrade_gates: []
  gamma:
    target: "{gamma_target}"
    allowed_states:
      - OPEN
      - MINIMALLY_CLOSED
    minimally_closed_requires:
      - minimum_completion_passed
  registry:
    layer_id: "{registry_layer}"
    allowed_previous_layers: []
    allowed_next_layers: []
    forbidden_direct_layers: []
  tests:
    required_test_ids: []
"""


# ─── SCG-YAML-LOAD: تحميل الملفات ───────────────────────────────────────────

class TestLoad:
    """SCG-YAML-LOAD: اختبارات تحميل ملفات YAML."""

    def test_SCG_YAML_LOAD_01_load_origin_example(self):
        """SCG-YAML-LOAD-01: يمكن تحميل ملف SG_ORIGIN_01 بنجاح."""
        spec = load_slot_geometry_yaml(_SG_ORIGIN)
        assert spec.id == "SG_ORIGIN_01_ARABIC_HUMAN_VOICE_TRACE"
        assert spec.schema_version == "1.0"

    def test_SCG_YAML_LOAD_02_load_dal_example(self):
        """SCG-YAML-LOAD-02: يمكن تحميل ملف SG_DAL_04 بنجاح."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert spec.id == "SG_DAL_04_HARAKA_MARK_IDENTITY"
        assert spec.schema_version == "1.0"

    def test_SCG_YAML_LOAD_03_load_mantuq_example(self):
        """SCG-YAML-LOAD-03: يمكن تحميل ملف SG_MANTUQ_00 بنجاح."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert spec.id == "SG_MANTUQ_00_MANTUQ_CANDIDATE"
        assert spec.schema_version == "1.0"

    def test_SCG_YAML_LOAD_04_nonexistent_raises(self, tmp_path):
        """SCG-YAML-LOAD-04: يرفع YAMLLoadError عند مسار غير موجود."""
        with pytest.raises(YAMLLoadError):
            load_slot_geometry_yaml(tmp_path / "nonexistent.yaml")

    def test_SCG_YAML_LOAD_05_invalid_yaml_syntax_raises(self, tmp_path):
        """SCG-YAML-LOAD-05: يرفع YAMLLoadError عند بناء جملة YAML خاطئ."""
        bad = tmp_path / "bad.yaml"
        bad.write_text("{ not: valid: yaml: [\n", encoding="utf-8")
        with pytest.raises(YAMLLoadError):
            load_slot_geometry_yaml(bad)

    def test_SCG_YAML_LOAD_06_schema_file_loadable(self):
        """SCG-YAML-LOAD-06: ملف القالب الأعلى يمكن تحميله كـ YAML صالح."""
        with _SCHEMA_FILE.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        assert isinstance(raw, dict)
        assert "schema_version" in raw
        assert "slot_geometry" in raw

    def test_SCG_YAML_LOAD_07_path_as_string(self, tmp_path):
        """SCG-YAML-LOAD-07: load_slot_geometry_yaml يقبل مسارًا كـ str."""
        p = _build_yaml(_minimal_valid_yaml(), tmp_path)
        spec = load_slot_geometry_yaml(str(p))
        assert spec.id == "SG_TEST_01"

    def test_SCG_YAML_LOAD_08_path_as_path_object(self, tmp_path):
        """SCG-YAML-LOAD-08: load_slot_geometry_yaml يقبل مسارًا كـ Path."""
        p = _build_yaml(_minimal_valid_yaml(), tmp_path)
        spec = load_slot_geometry_yaml(p)
        assert spec.id == "SG_TEST_01"


# ─── SCG-YAML-VALID: التحقق من الملفات الصالحة ──────────────────────────────

class TestValidFiles:
    """SCG-YAML-VALID: اختبارات التحقق من الملفات النموذجية الصالحة."""

    def test_SCG_YAML_VALID_01_origin_example_passes(self):
        """SCG-YAML-VALID-01: ملف SG_ORIGIN_01 يجتاز التحقق."""
        spec = load_slot_geometry_yaml(_SG_ORIGIN)
        result = SlotGeometryValidator().validate(spec)
        assert result.is_valid, [str(v) for v in result.violations]

    def test_SCG_YAML_VALID_02_dal_example_passes(self):
        """SCG-YAML-VALID-02: ملف SG_DAL_04 يجتاز التحقق."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        result = SlotGeometryValidator().validate(spec)
        assert result.is_valid, [str(v) for v in result.violations]

    def test_SCG_YAML_VALID_03_mantuq_example_passes(self):
        """SCG-YAML-VALID-03: ملف SG_MANTUQ_00 يجتاز التحقق."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        result = SlotGeometryValidator().validate(spec)
        assert result.is_valid, [str(v) for v in result.violations]

    def test_SCG_YAML_VALID_04_minimal_valid_passes(self, tmp_path):
        """SCG-YAML-VALID-04: ملف YAML أدنى صالح يجتاز التحقق."""
        p = _build_yaml(_minimal_valid_yaml(), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert result.is_valid, [str(v) for v in result.violations]

    def test_SCG_YAML_VALID_05_validate_strict_passes_on_valid(self, tmp_path):
        """SCG-YAML-VALID-05: validate_strict لا يرفع على ملف صالح."""
        p = _build_yaml(_minimal_valid_yaml(), tmp_path)
        spec = load_slot_geometry_yaml(p)
        SlotGeometryValidator().validate_strict(spec)  # must not raise


# ─── SCG-YAML-SCHEMA: فحص القالب الأعلى ─────────────────────────────────────

class TestSchemaFile:
    """SCG-YAML-SCHEMA: اختبارات وجود وصحة ملف القالب الأعلى."""

    def test_SCG_YAML_SCHEMA_01_schema_file_exists(self):
        """SCG-YAML-SCHEMA-01: ملف schemas/slot_geometry.schema.yaml موجود."""
        assert _SCHEMA_FILE.exists(), f"Schema file not found: {_SCHEMA_FILE}"

    def test_SCG_YAML_SCHEMA_02_schema_has_schema_version(self):
        """SCG-YAML-SCHEMA-02: القالب يحتوي schema_version: "1.0"."""
        with _SCHEMA_FILE.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        assert raw["schema_version"] == "1.0"

    def test_SCG_YAML_SCHEMA_03_schema_has_slot_geometry_root(self):
        """SCG-YAML-SCHEMA-03: القالب يحتوي slot_geometry كمفتاح جذري."""
        with _SCHEMA_FILE.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        assert "slot_geometry" in raw

    def test_SCG_YAML_SCHEMA_04_schema_documents_all_required_sections(self):
        """SCG-YAML-SCHEMA-04: القالب يوثق جميع الأقسام الإلزامية."""
        with _SCHEMA_FILE.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        sg = raw["slot_geometry"]
        required_sections = [
            "id", "name", "phase", "status",
            "origin", "branch", "qiyas",
            "target_boundary", "minimum_completion",
            "identity_inheritance", "forbidden_outputs",
            "residual_policy", "trace", "rank", "gamma",
            "registry", "tests",
        ]
        for section in required_sections:
            assert section in sg, f"Schema missing section: {section}"

    def test_SCG_YAML_SCHEMA_05_examples_directory_has_three_files(self):
        """SCG-YAML-SCHEMA-05: مجلد examples/slot_geometries يحتوي على الملفات الثلاثة."""
        assert _SG_ORIGIN.exists()
        assert _SG_DAL.exists()
        assert _SG_MANTUQ.exists()


# ─── SCG-YAML-MISS: كشف الحقول المفقودة ─────────────────────────────────────

class TestMissingFields:
    """SCG-YAML-MISS: اختبارات كشف الحقول الإلزامية المفقودة."""

    def test_SCG_YAML_MISS_01_missing_id_raises(self, tmp_path):
        """SCG-YAML-MISS-01: غياب slot_geometry.id يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(sg_id=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_02_missing_name_raises(self, tmp_path):
        """SCG-YAML-MISS-02: غياب slot_geometry.name يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(name=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_03_missing_phase_raises(self, tmp_path):
        """SCG-YAML-MISS-03: غياب slot_geometry.phase يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(phase=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_04_missing_origin_layer_id_raises(self, tmp_path):
        """SCG-YAML-MISS-04: غياب origin.layer_id يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(origin_layer=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_05_missing_origin_output_type_raises(self, tmp_path):
        """SCG-YAML-MISS-05: غياب origin.output_type يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(origin_output=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_06_missing_branch_output_type_raises(self, tmp_path):
        """SCG-YAML-MISS-06: غياب branch.output_type يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(branch_output=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_07_missing_branch_reason_raises(self, tmp_path):
        """SCG-YAML-MISS-07: غياب branch.branch_reason يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(branch_reason=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_08_missing_shared_cause_raises(self, tmp_path):
        """SCG-YAML-MISS-08: غياب qiyas.shared_cause يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(shared_cause=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_09_missing_effective_attribute_raises(self, tmp_path):
        """SCG-YAML-MISS-09: غياب qiyas.effective_attribute يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(effective_attribute=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_10_missing_branching_reason_raises(self, tmp_path):
        """SCG-YAML-MISS-10: غياب qiyas.branching_reason يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(branching_reason=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)

    def test_SCG_YAML_MISS_11_missing_registry_layer_id_raises(self, tmp_path):
        """SCG-YAML-MISS-11: غياب registry.layer_id يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(registry_layer=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)


# ─── SCG-YAML-BOUND: فحص target_boundary ────────────────────────────────────

class TestTargetBoundary:
    """SCG-YAML-BOUND: اختبارات target_boundary."""

    def test_SCG_YAML_BOUND_01_empty_closes_raises(self, tmp_path):
        """SCG-YAML-BOUND-01: closes فارغ يُنتج EmptyTargetBoundaryCloses."""
        p = _build_yaml(_minimal_valid_yaml(closes=""), tmp_path)
        # closes فارغ يعني أن القائمة ستحتوي على سلسلة فارغة — نحتاج YAML مختلف
        raw_yaml = """\
schema_version: "1.0"
slot_geometry:
  id: "SG_TEST_EMPTY_CLOSES"
  name: "TestGeometry"
  phase: "TEST"
  status: "PLANNED"
  origin:
    layer_id: "ORIGIN"
    output_type: "OriginType"
    trace_required: true
    identity_required: true
    closure_required: "MINIMALLY_CLOSED"
  branch:
    output_type: "BranchType"
    branch_reason: "test"
    rank_ceiling: "Candidate"
  qiyas:
    shared_cause: "test cause"
    effective_attribute: "test attr"
    branching_reason: "test reason"
    conditions: [cond]
    blockers: []
    invalidating_differences: []
  target_boundary:
    closes: []
    opens: []
    does_not_close: []
  minimum_completion:
    required: [origin_exists]
  identity_inheritance:
    preserves: [origin_id]
    allowed_changes: []
    forbidden_changes: []
  forbidden_outputs:
    absolute: [HukmCandidate, RealityClaim, FinalMeaning]
    layer_specific: []
  residual_policy:
    residuals_allowed: true
    residuals_must_be_visible: true
    blocking_residuals: []
    non_blocking_residuals: []
  trace:
    source_trace: true
    operation_trace: true
    evidence_trace: false
    residual_trace: true
  rank:
    initial: "Candidate"
    ceiling: "Candidate"
    upgrade_requires_gate: true
    allowed_upgrade_gates: []
  gamma:
    target: "test_boundary"
    allowed_states: [OPEN, MINIMALLY_CLOSED]
    minimally_closed_requires: [minimum_completion_passed]
  registry:
    layer_id: "TEST_LAYER"
    allowed_previous_layers: []
    allowed_next_layers: []
    forbidden_direct_layers: []
  tests:
    required_test_ids: []
"""
        p2 = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p2)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyTargetBoundaryCloses) for v in result.violations)

    def test_SCG_YAML_BOUND_02_overlap_closes_does_not_close_raises(self, tmp_path):
        """SCG-YAML-BOUND-02: تداخل closes وdoes_not_close يُنتج TargetBoundaryViolation."""
        raw_yaml = """\
schema_version: "1.0"
slot_geometry:
  id: "SG_TEST_OVERLAP"
  name: "TestGeometry"
  phase: "TEST"
  status: "PLANNED"
  origin:
    layer_id: "ORIGIN"
    output_type: "OriginType"
    trace_required: true
    identity_required: true
    closure_required: "MINIMALLY_CLOSED"
  branch:
    output_type: "BranchType"
    branch_reason: "test"
    rank_ceiling: "Candidate"
  qiyas:
    shared_cause: "test cause"
    effective_attribute: "test attr"
    branching_reason: "test reason"
    conditions: [cond]
    blockers: []
    invalidating_differences: []
  target_boundary:
    closes: [boundary_x, boundary_y]
    opens: []
    does_not_close: [boundary_x]
  minimum_completion:
    required: [origin_exists]
  identity_inheritance:
    preserves: [origin_id]
    allowed_changes: []
    forbidden_changes: []
  forbidden_outputs:
    absolute: [HukmCandidate, RealityClaim, FinalMeaning]
    layer_specific: []
  residual_policy:
    residuals_allowed: true
    residuals_must_be_visible: true
    blocking_residuals: []
    non_blocking_residuals: []
  trace:
    source_trace: true
    operation_trace: true
    evidence_trace: false
    residual_trace: true
  rank:
    initial: "Candidate"
    ceiling: "Candidate"
    upgrade_requires_gate: true
    allowed_upgrade_gates: []
  gamma:
    target: "boundary_x"
    allowed_states: [OPEN, MINIMALLY_CLOSED]
    minimally_closed_requires: [minimum_completion_passed]
  registry:
    layer_id: "TEST_LAYER"
    allowed_previous_layers: []
    allowed_next_layers: []
    forbidden_direct_layers: []
  tests:
    required_test_ids: []
"""
        p = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, TargetBoundaryViolation) for v in result.violations)

    def test_SCG_YAML_BOUND_03_dal_closes_haraka_mark_identity(self):
        """SCG-YAML-BOUND-03: SG_DAL_04 يُغلق haraka_mark_identity_carrier."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "haraka_mark_identity_carrier" in spec.target_boundary.closes

    def test_SCG_YAML_BOUND_04_dal_does_not_close_haraka_function(self):
        """SCG-YAML-BOUND-04: SG_DAL_04 لا يُغلق haraka_function."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "haraka_function" in spec.target_boundary.does_not_close

    def test_SCG_YAML_BOUND_05_mantuq_closes_mantuq_candidate(self):
        """SCG-YAML-BOUND-05: SG_MANTUQ_00 يُغلق mantuq_candidate."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert "mantuq_candidate" in spec.target_boundary.closes

    def test_SCG_YAML_BOUND_06_mantuq_does_not_close_hukm(self):
        """SCG-YAML-BOUND-06: SG_MANTUQ_00 لا يُغلق final_hukm."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert "final_hukm" in spec.target_boundary.does_not_close

    def test_SCG_YAML_BOUND_07_origin_does_not_close_letter_identity(self):
        """SCG-YAML-BOUND-07: SG_ORIGIN_01 لا يُغلق letter_identity."""
        spec = load_slot_geometry_yaml(_SG_ORIGIN)
        assert "letter_identity" in spec.target_boundary.does_not_close


# ─── SCG-YAML-FORB: فحص forbidden_outputs ───────────────────────────────────

class TestForbiddenOutputs:
    """SCG-YAML-FORB: اختبارات forbidden_outputs."""

    def test_SCG_YAML_FORB_01_missing_HukmCandidate_raises(self, tmp_path):
        """SCG-YAML-FORB-01: غياب HukmCandidate من absolute يُنتج MissingAbsoluteForbidden."""
        raw_yaml = _minimal_valid_yaml().replace(
            "      - HukmCandidate\n      - RealityClaim\n      - FinalMeaning",
            "      - RealityClaim\n      - FinalMeaning",
        )
        p = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, MissingAbsoluteForbidden) for v in result.violations)

    def test_SCG_YAML_FORB_02_missing_RealityClaim_raises(self, tmp_path):
        """SCG-YAML-FORB-02: غياب RealityClaim من absolute يُنتج MissingAbsoluteForbidden."""
        raw_yaml = _minimal_valid_yaml().replace(
            "      - HukmCandidate\n      - RealityClaim\n      - FinalMeaning",
            "      - HukmCandidate\n      - FinalMeaning",
        )
        p = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, MissingAbsoluteForbidden) for v in result.violations)

    def test_SCG_YAML_FORB_03_missing_FinalMeaning_raises(self, tmp_path):
        """SCG-YAML-FORB-03: غياب FinalMeaning من absolute يُنتج MissingAbsoluteForbidden."""
        raw_yaml = _minimal_valid_yaml().replace(
            "      - HukmCandidate\n      - RealityClaim\n      - FinalMeaning",
            "      - HukmCandidate\n      - RealityClaim",
        )
        p = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, MissingAbsoluteForbidden) for v in result.violations)

    def test_SCG_YAML_FORB_04_dal_forbids_HarakaFunctionCarrier(self):
        """SCG-YAML-FORB-04: SG_DAL_04 يُصرّح بتحريم HarakaFunctionCarrier."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        all_forbidden = set(spec.forbidden_outputs.absolute) | set(spec.forbidden_outputs.layer_specific)
        assert "HarakaFunctionCarrier" in all_forbidden

    def test_SCG_YAML_FORB_05_all_examples_forbid_HukmCandidate(self):
        """SCG-YAML-FORB-05: جميع الملفات النموذجية تُصرّح بتحريم HukmCandidate."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert "HukmCandidate" in spec.forbidden_outputs.absolute, \
                f"{path.name} missing HukmCandidate in absolute forbidden"

    def test_SCG_YAML_FORB_06_all_examples_forbid_RealityClaim(self):
        """SCG-YAML-FORB-06: جميع الملفات النموذجية تُصرّح بتحريم RealityClaim."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert "RealityClaim" in spec.forbidden_outputs.absolute, \
                f"{path.name} missing RealityClaim in absolute forbidden"

    def test_SCG_YAML_FORB_07_all_examples_forbid_FinalMeaning(self):
        """SCG-YAML-FORB-07: جميع الملفات النموذجية تُصرّح بتحريم FinalMeaning."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert "FinalMeaning" in spec.forbidden_outputs.absolute, \
                f"{path.name} missing FinalMeaning in absolute forbidden"


# ─── SCG-YAML-IDENT: فحص identity_inheritance ───────────────────────────────

class TestIdentityInheritance:
    """SCG-YAML-IDENT: اختبارات identity_inheritance."""

    def test_SCG_YAML_IDENT_01_empty_preserves_raises(self, tmp_path):
        """SCG-YAML-IDENT-01: preserves فارغ يُنتج EmptyIdentityInheritancePreserves."""
        raw_yaml = """\
schema_version: "1.0"
slot_geometry:
  id: "SG_TEST_EMPTY_PRESERVES"
  name: "TestGeometry"
  phase: "TEST"
  status: "PLANNED"
  origin:
    layer_id: "ORIGIN"
    output_type: "OriginType"
    trace_required: true
    identity_required: true
    closure_required: "MINIMALLY_CLOSED"
  branch:
    output_type: "BranchType"
    branch_reason: "test"
    rank_ceiling: "Candidate"
  qiyas:
    shared_cause: "test cause"
    effective_attribute: "test attr"
    branching_reason: "test reason"
    conditions: [cond]
    blockers: []
    invalidating_differences: []
  target_boundary:
    closes: [boundary_x]
    opens: []
    does_not_close: []
  minimum_completion:
    required: [origin_exists]
  identity_inheritance:
    preserves: []
    allowed_changes: []
    forbidden_changes: []
  forbidden_outputs:
    absolute: [HukmCandidate, RealityClaim, FinalMeaning]
    layer_specific: []
  residual_policy:
    residuals_allowed: true
    residuals_must_be_visible: true
    blocking_residuals: []
    non_blocking_residuals: []
  trace:
    source_trace: true
    operation_trace: true
    evidence_trace: false
    residual_trace: true
  rank:
    initial: "Candidate"
    ceiling: "Candidate"
    upgrade_requires_gate: true
    allowed_upgrade_gates: []
  gamma:
    target: "boundary_x"
    allowed_states: [OPEN, MINIMALLY_CLOSED]
    minimally_closed_requires: [minimum_completion_passed]
  registry:
    layer_id: "TEST_LAYER"
    allowed_previous_layers: []
    allowed_next_layers: []
    forbidden_direct_layers: []
  tests:
    required_test_ids: []
"""
        p = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyIdentityInheritancePreserves) for v in result.violations)

    def test_SCG_YAML_IDENT_02_overlap_allowed_forbidden_raises(self, tmp_path):
        """SCG-YAML-IDENT-02: تداخل allowed_changes وforbidden_changes يُنتج AllowedForbiddenOverlap."""
        raw_yaml = """\
schema_version: "1.0"
slot_geometry:
  id: "SG_TEST_OVERLAP_CHANGES"
  name: "TestGeometry"
  phase: "TEST"
  status: "PLANNED"
  origin:
    layer_id: "ORIGIN"
    output_type: "OriginType"
    trace_required: true
    identity_required: true
    closure_required: "MINIMALLY_CLOSED"
  branch:
    output_type: "BranchType"
    branch_reason: "test"
    rank_ceiling: "Candidate"
  qiyas:
    shared_cause: "test cause"
    effective_attribute: "test attr"
    branching_reason: "test reason"
    conditions: [cond]
    blockers: []
    invalidating_differences: []
  target_boundary:
    closes: [boundary_x]
    opens: []
    does_not_close: []
  minimum_completion:
    required: [origin_exists]
  identity_inheritance:
    preserves: [origin_id]
    allowed_changes: [change_x, change_y]
    forbidden_changes: [change_x]
  forbidden_outputs:
    absolute: [HukmCandidate, RealityClaim, FinalMeaning]
    layer_specific: []
  residual_policy:
    residuals_allowed: true
    residuals_must_be_visible: true
    blocking_residuals: []
    non_blocking_residuals: []
  trace:
    source_trace: true
    operation_trace: true
    evidence_trace: false
    residual_trace: true
  rank:
    initial: "Candidate"
    ceiling: "Candidate"
    upgrade_requires_gate: true
    allowed_upgrade_gates: []
  gamma:
    target: "boundary_x"
    allowed_states: [OPEN, MINIMALLY_CLOSED]
    minimally_closed_requires: [minimum_completion_passed]
  registry:
    layer_id: "TEST_LAYER"
    allowed_previous_layers: []
    allowed_next_layers: []
    forbidden_direct_layers: []
  tests:
    required_test_ids: []
"""
        p = _build_yaml(raw_yaml, tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, AllowedForbiddenOverlap) for v in result.violations)

    def test_SCG_YAML_IDENT_03_dal_preserves_typed_codepoint_identity(self):
        """SCG-YAML-IDENT-03: SG_DAL_04 يحفظ typed_codepoint_identity."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "typed_codepoint_identity" in spec.identity_inheritance.preserves

    def test_SCG_YAML_IDENT_04_dal_forbids_prove_haraka_function(self):
        """SCG-YAML-IDENT-04: SG_DAL_04 يُصرّح بتحريم prove_haraka_function."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "prove_haraka_function" in spec.identity_inheritance.forbidden_changes

    def test_SCG_YAML_IDENT_05_dal_allows_prove_haraka_mark_identity(self):
        """SCG-YAML-IDENT-05: SG_DAL_04 يُسمح بـ prove_haraka_mark_identity فقط."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "prove_haraka_mark_identity" in spec.identity_inheritance.allowed_changes

    def test_SCG_YAML_IDENT_06_mantuq_forbids_infer_mafhum_without_qiyas(self):
        """SCG-YAML-IDENT-06: SG_MANTUQ_00 يُصرّح بتحريم infer_mafhum_without_new_qiyas."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert "infer_mafhum_without_new_qiyas" in spec.identity_inheritance.forbidden_changes

    def test_SCG_YAML_IDENT_07_mantuq_forbids_assert_hukm(self):
        """SCG-YAML-IDENT-07: SG_MANTUQ_00 يُصرّح بتحريم assert_hukm."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert "assert_hukm" in spec.identity_inheritance.forbidden_changes


# ─── SCG-YAML-GAMMA: فحص gamma ───────────────────────────────────────────────

class TestGamma:
    """SCG-YAML-GAMMA: اختبارات gamma."""

    def test_SCG_YAML_GAMMA_01_empty_gamma_target_raises(self, tmp_path):
        """SCG-YAML-GAMMA-01: gamma.target فارغ يُنتج MissingGammaTarget."""
        p = _build_yaml(_minimal_valid_yaml(gamma_target=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, MissingGammaTarget) for v in result.violations)

    def test_SCG_YAML_GAMMA_02_dal_gamma_target_is_haraka_mark_identity_carrier(self):
        """SCG-YAML-GAMMA-02: SG_DAL_04 تستهدف Gamma haraka_mark_identity_carrier."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert spec.gamma.target == "haraka_mark_identity_carrier"

    def test_SCG_YAML_GAMMA_03_mantuq_gamma_target_is_mantuq_candidate(self):
        """SCG-YAML-GAMMA-03: SG_MANTUQ_00 تستهدف Gamma mantuq_candidate."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert spec.gamma.target == "mantuq_candidate"

    def test_SCG_YAML_GAMMA_04_origin_gamma_target_is_arabic_voice_trace(self):
        """SCG-YAML-GAMMA-04: SG_ORIGIN_01 تستهدف Gamma arabic_voice_trace_candidate."""
        spec = load_slot_geometry_yaml(_SG_ORIGIN)
        assert spec.gamma.target == "arabic_voice_trace_candidate"

    def test_SCG_YAML_GAMMA_05_all_examples_have_MINIMALLY_CLOSED_state(self):
        """SCG-YAML-GAMMA-05: جميع الملفات النموذجية تتضمن MINIMALLY_CLOSED في allowed_states."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert "MINIMALLY_CLOSED" in spec.gamma.allowed_states, \
                f"{path.name} missing MINIMALLY_CLOSED in gamma.allowed_states"

    def test_SCG_YAML_GAMMA_06_all_examples_have_BLOCKED_state(self):
        """SCG-YAML-GAMMA-06: جميع الملفات النموذجية تتضمن BLOCKED في allowed_states."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert "BLOCKED" in spec.gamma.allowed_states, \
                f"{path.name} missing BLOCKED in gamma.allowed_states"


# ─── SCG-YAML-REG: فحص registry ─────────────────────────────────────────────

class TestRegistry:
    """SCG-YAML-REG: اختبارات registry."""

    def test_SCG_YAML_REG_01_dal_registry_layer_id_is_P1_HARAKA_MARK_IDENTITY(self):
        """SCG-YAML-REG-01: SG_DAL_04 يُعلن layer_id=P1_HARAKA_MARK_IDENTITY_CARRIER."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert spec.registry.layer_id == "P1_HARAKA_MARK_IDENTITY_CARRIER"

    def test_SCG_YAML_REG_02_dal_forbids_P1_HARAKA_FUNCTION_CARRIER(self):
        """SCG-YAML-REG-02: SG_DAL_04 يُصرّح بتحريم الانتقال إلى P1_HARAKA_FUNCTION_CARRIER."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "P1_HARAKA_FUNCTION_CARRIER" in spec.registry.forbidden_direct_layers

    def test_SCG_YAML_REG_03_dal_previous_is_P0_TYPED_CODEPOINT(self):
        """SCG-YAML-REG-03: SG_DAL_04 يُعلن P0_TYPED_CODEPOINT كطبقة سابقة."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "P0_TYPED_CODEPOINT" in spec.registry.allowed_previous_layers

    def test_SCG_YAML_REG_04_missing_registry_layer_id_raises(self, tmp_path):
        """SCG-YAML-REG-04: غياب registry.layer_id يُنتج EmptyRequiredField."""
        p = _build_yaml(_minimal_valid_yaml(registry_layer=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, EmptyRequiredField) for v in result.violations)


# ─── SCG-YAML-RANK: فحص rank_ceiling ────────────────────────────────────────

class TestRankCeiling:
    """SCG-YAML-RANK: اختبارات rank_ceiling."""

    def test_SCG_YAML_RANK_01_invalid_rank_ceiling_raises(self, tmp_path):
        """SCG-YAML-RANK-01: قيمة rank_ceiling غير مسموحة تُنتج InvalidRankCeiling."""
        p = _build_yaml(_minimal_valid_yaml(rank_ceiling="AbsoluteCertainty"), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, InvalidRankCeiling) for v in result.violations)

    def test_SCG_YAML_RANK_02_all_valid_rank_ceilings_pass(self, tmp_path):
        """SCG-YAML-RANK-02: جميع قيم rank_ceiling الصالحة تجتاز التحقق."""
        valid_ceilings = [
            "Prior", "Candidate", "LicensedCandidate",
            "StrongCandidate", "Certificate", "Judgment",
        ]
        for rc in valid_ceilings:
            p = _build_yaml(_minimal_valid_yaml(rank_ceiling=rc), tmp_path)
            spec = load_slot_geometry_yaml(p)
            result = SlotGeometryValidator().validate(spec)
            assert result.is_valid, f"rank_ceiling={rc} should be valid but got: {[str(v) for v in result.violations]}"

    def test_SCG_YAML_RANK_03_dal_rank_ceiling_is_Candidate(self):
        """SCG-YAML-RANK-03: SG_DAL_04 rank_ceiling = Candidate."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert spec.branch.rank_ceiling == "Candidate"

    def test_SCG_YAML_RANK_04_mantuq_rank_ceiling_is_LicensedCandidate(self):
        """SCG-YAML-RANK-04: SG_MANTUQ_00 rank_ceiling = LicensedCandidate."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert spec.branch.rank_ceiling == "LicensedCandidate"


# ─── SCG-YAML-STATUS: فحص status ─────────────────────────────────────────────

class TestStatus:
    """SCG-YAML-STATUS: اختبارات status."""

    def test_SCG_YAML_STATUS_01_invalid_status_raises(self, tmp_path):
        """SCG-YAML-STATUS-01: قيمة status غير مسموحة تُنتج InvalidStatusValue."""
        p = _build_yaml(_minimal_valid_yaml(status="UNKNOWN"), tmp_path)
        spec = load_slot_geometry_yaml(p)
        result = SlotGeometryValidator().validate(spec)
        assert not result.is_valid
        assert any(isinstance(v, InvalidStatusValue) for v in result.violations)

    def test_SCG_YAML_STATUS_02_all_valid_statuses_pass(self, tmp_path):
        """SCG-YAML-STATUS-02: جميع قيم status الصالحة تجتاز التحقق."""
        for status in ["PLANNED", "SPECIFIED", "IMPLEMENTED", "AUDITED", "CLOSED"]:
            p = _build_yaml(_minimal_valid_yaml(status=status), tmp_path)
            spec = load_slot_geometry_yaml(p)
            result = SlotGeometryValidator().validate(spec)
            assert result.is_valid, f"status={status} should be valid"

    def test_SCG_YAML_STATUS_03_examples_are_SPECIFIED(self):
        """SCG-YAML-STATUS-03: الملفات النموذجية تحمل status=SPECIFIED."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert spec.status == "SPECIFIED", f"{path.name} expected SPECIFIED"


# ─── SCG-YAML-SPEC: فحص الملفات النموذجية تفصيليًا ──────────────────────────

class TestExampleSpecs:
    """SCG-YAML-SPEC: اختبارات تفصيلية للملفات النموذجية."""

    def test_SCG_YAML_SPEC_01_dal_qiyas_shared_cause_present(self):
        """SCG-YAML-SPEC-01: SG_DAL_04 يحتوي shared_cause المطلوب."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "TypedCodePoint" in spec.qiyas.shared_cause

    def test_SCG_YAML_SPEC_02_dal_qiyas_conditions_include_mark(self):
        """SCG-YAML-SPEC-02: SG_DAL_04 شروط الـ qiyas تشمل codepoint_type_is_mark."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "codepoint_type_is_mark" in spec.qiyas.conditions

    def test_SCG_YAML_SPEC_03_dal_branch_output_is_HarakaMarkIdentityCarrier(self):
        """SCG-YAML-SPEC-03: SG_DAL_04 branch.output_type = HarakaMarkIdentityCarrier."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert spec.branch.output_type == "HarakaMarkIdentityCarrier"

    def test_SCG_YAML_SPEC_04_mantuq_origin_is_IFADAH_CLOSURE(self):
        """SCG-YAML-SPEC-04: SG_MANTUQ_00 origin.layer_id = IFADAH_CLOSURE."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert spec.origin.layer_id == "IFADAH_CLOSURE"

    def test_SCG_YAML_SPEC_05_mantuq_branch_output_is_MantuqCandidate(self):
        """SCG-YAML-SPEC-05: SG_MANTUQ_00 branch.output_type = MantuqCandidate."""
        spec = load_slot_geometry_yaml(_SG_MANTUQ)
        assert spec.branch.output_type == "MantuqCandidate"

    def test_SCG_YAML_SPEC_06_origin_origin_is_HUMAN_VOICE_EVENT(self):
        """SCG-YAML-SPEC-06: SG_ORIGIN_01 origin.layer_id = HUMAN_VOICE_EVENT."""
        spec = load_slot_geometry_yaml(_SG_ORIGIN)
        assert spec.origin.layer_id == "HUMAN_VOICE_EVENT"

    def test_SCG_YAML_SPEC_07_origin_branch_output_is_ArabicVoiceTraceCandidate(self):
        """SCG-YAML-SPEC-07: SG_ORIGIN_01 branch.output_type = ArabicVoiceTraceCandidate."""
        spec = load_slot_geometry_yaml(_SG_ORIGIN)
        assert spec.branch.output_type == "ArabicVoiceTraceCandidate"

    def test_SCG_YAML_SPEC_08_spec_does_not_produce_runtime(self):
        """SCG-YAML-SPEC-08: SlotGeometrySpec لا يحتوي على أي دوال runtime."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        # SlotGeometrySpec هو dataclass بيانات فقط — لا run()، لا execute()، لا apply()
        assert not hasattr(spec, "run")
        assert not hasattr(spec, "execute")
        assert not hasattr(spec, "apply")
        assert not hasattr(spec, "produce")

    def test_SCG_YAML_SPEC_09_spec_is_frozen(self):
        """SCG-YAML-SPEC-09: SlotGeometrySpec لا يمكن تعديله (frozen dataclass)."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        with pytest.raises((AttributeError, TypeError, FrozenInstanceError)):
            spec.id = "MODIFIED"  # type: ignore[misc]

    def test_SCG_YAML_SPEC_10_spec_schema_version_is_1_0(self):
        """SCG-YAML-SPEC-10: schema_version في جميع الملفات = "1.0"."""
        for path in [_SG_ORIGIN, _SG_DAL, _SG_MANTUQ]:
            spec = load_slot_geometry_yaml(path)
            assert spec.schema_version == "1.0", f"{path.name} wrong schema_version"

    def test_SCG_YAML_SPEC_11_dal_invalidating_differences_correct(self):
        """SCG-YAML-SPEC-11: SG_DAL_04 يتضمن الفروق القادحة الصحيحة."""
        spec = load_slot_geometry_yaml(_SG_DAL)
        assert "mark_claims_case_function" in spec.qiyas.invalidating_differences
        assert "mark_claims_idgham_function" in spec.qiyas.invalidating_differences

    def test_SCG_YAML_SPEC_12_validate_strict_raises_on_invalid(self, tmp_path):
        """SCG-YAML-SPEC-12: validate_strict يرفع SchemaViolation عند انتهاك."""
        p = _build_yaml(_minimal_valid_yaml(sg_id=""), tmp_path)
        spec = load_slot_geometry_yaml(p)
        with pytest.raises(SchemaViolation):
            SlotGeometryValidator().validate_strict(spec)
