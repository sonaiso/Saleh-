"""
loader.py — محمّل ملفات YAML لـ SlotGeometry

القانون:
    YAML لا ينتج runtime.
    YAML لا يثبت حكمًا.
    YAML يعرّف SlotGeometrySpec قابلًا للتحقق.
    أي LayerSpec لاحق يجب أن يكون له YAML مطابق.

SlotGeometrySpec هو تمثيل Python للبيانات المحمّلة من ملف YAML،
قبل أي تحقق من الصحة. يُمرَّر إلى validator.py للتحقق.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .errors import YAMLLoadError

try:
    import yaml
except ImportError as _e:
    raise ImportError(
        "PyYAML is required for slot_geometry_yaml. "
        "Install it with: pip install pyyaml"
    ) from _e


# ─── SlotGeometrySpec dataclass ──────────────────────────────────────────────

@dataclass(frozen=True)
class OriginData:
    layer_id: str
    output_type: str
    trace_required: bool
    identity_required: bool
    closure_required: str


@dataclass(frozen=True)
class BranchData:
    output_type: str
    branch_reason: str
    rank_ceiling: str


@dataclass(frozen=True)
class QiyasData:
    shared_cause: str
    effective_attribute: str
    branching_reason: str
    conditions: tuple[str, ...]
    blockers: tuple[str, ...]
    invalidating_differences: tuple[str, ...]


@dataclass(frozen=True)
class TargetBoundaryData:
    closes: tuple[str, ...]
    opens: tuple[str, ...]
    does_not_close: tuple[str, ...]


@dataclass(frozen=True)
class IdentityInheritanceData:
    preserves: tuple[str, ...]
    allowed_changes: tuple[str, ...]
    forbidden_changes: tuple[str, ...]


@dataclass(frozen=True)
class ForbiddenOutputsData:
    absolute: tuple[str, ...]
    layer_specific: tuple[str, ...]


@dataclass(frozen=True)
class ResidualPolicyData:
    residuals_allowed: bool
    residuals_must_be_visible: bool
    blocking_residuals: tuple[str, ...]
    non_blocking_residuals: tuple[str, ...]


@dataclass(frozen=True)
class TraceData:
    source_trace: bool
    operation_trace: bool
    evidence_trace: bool
    residual_trace: bool


@dataclass(frozen=True)
class RankData:
    initial: str
    ceiling: str
    upgrade_requires_gate: bool
    allowed_upgrade_gates: tuple[str, ...]


@dataclass(frozen=True)
class GammaData:
    target: str
    allowed_states: tuple[str, ...]
    minimally_closed_requires: tuple[str, ...]


@dataclass(frozen=True)
class RegistryData:
    layer_id: str
    allowed_previous_layers: tuple[str, ...]
    allowed_next_layers: tuple[str, ...]
    forbidden_direct_layers: tuple[str, ...]


@dataclass(frozen=True)
class TestsData:
    required_test_ids: tuple[str, ...]


@dataclass(frozen=True)
class SlotGeometrySpec:
    """
    تمثيل Python للبيانات المحمّلة من ملف YAML لطبقة SlotGeometry.

    هذا الكائن يحمل البيانات الخام قبل التحقق.
    يُمرَّر إلى SlotGeometryValidator.validate() للتحقق من الصحة.

    القانون:
        SlotGeometrySpec لا ينتج runtime.
        SlotGeometrySpec لا يثبت حكمًا.
        SlotGeometrySpec يعرّف العقد قابلًا للتحقق.
    """
    schema_version: str
    id: str
    name: str
    phase: str
    status: str
    origin: OriginData
    branch: BranchData
    qiyas: QiyasData
    target_boundary: TargetBoundaryData
    minimum_completion_required: tuple[str, ...]
    identity_inheritance: IdentityInheritanceData
    forbidden_outputs: ForbiddenOutputsData
    residual_policy: ResidualPolicyData
    trace: TraceData
    rank: RankData
    gamma: GammaData
    registry: RegistryData
    tests: TestsData


# ─── Helper: safe dict access ────────────────────────────────────────────────

def _get(d: dict[str, Any], key: str, default: Any = None) -> Any:
    """قراءة مفتاح من dict مع إرجاع قيمة افتراضية إذا لم يكن موجودًا."""
    return d.get(key, default)


def _get_str(d: dict[str, Any], key: str, default: str = "") -> str:
    v = d.get(key, default)
    return str(v) if v is not None else default


def _get_bool(d: dict[str, Any], key: str, default: bool = True) -> bool:
    v = d.get(key, default)
    return bool(v)


def _get_list(d: dict[str, Any], key: str) -> list[Any]:
    v = d.get(key, [])
    return list(v) if v is not None else []


def _to_strtuple(lst: list[Any]) -> tuple[str, ...]:
    return tuple(str(x) for x in lst)


# ─── Loader ──────────────────────────────────────────────────────────────────

def load_slot_geometry_yaml(path: str | Path) -> SlotGeometrySpec:
    """
    حمّل ملف YAML لطبقة SlotGeometry وأعد SlotGeometrySpec.

    لا يُجري أي تحقق من الصحة — استخدم SlotGeometryValidator لذلك.

    Args:
        path: مسار ملف YAML

    Returns:
        SlotGeometrySpec يحمل البيانات المحمّلة

    Raises:
        YAMLLoadError: إذا فشل تحميل الملف أو كان بناء الجملة خاطئًا
    """
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f)
    except Exception as e:
        raise YAMLLoadError(str(path), e) from e

    if not isinstance(raw, dict):
        raise YAMLLoadError(str(path), ValueError("YAML root must be a mapping"))

    schema_version = _get_str(raw, "schema_version")
    sg: dict[str, Any] = _get(raw, "slot_geometry") or {}

    # origin
    orig: dict[str, Any] = _get(sg, "origin") or {}
    origin = OriginData(
        layer_id=_get_str(orig, "layer_id"),
        output_type=_get_str(orig, "output_type"),
        trace_required=_get_bool(orig, "trace_required", True),
        identity_required=_get_bool(orig, "identity_required", True),
        closure_required=_get_str(orig, "closure_required", "MINIMALLY_CLOSED"),
    )

    # branch
    br: dict[str, Any] = _get(sg, "branch") or {}
    branch = BranchData(
        output_type=_get_str(br, "output_type"),
        branch_reason=_get_str(br, "branch_reason"),
        rank_ceiling=_get_str(br, "rank_ceiling", "Candidate"),
    )

    # qiyas
    qy: dict[str, Any] = _get(sg, "qiyas") or {}
    qiyas = QiyasData(
        shared_cause=_get_str(qy, "shared_cause"),
        effective_attribute=_get_str(qy, "effective_attribute"),
        branching_reason=_get_str(qy, "branching_reason"),
        conditions=_to_strtuple(_get_list(qy, "conditions")),
        blockers=_to_strtuple(_get_list(qy, "blockers")),
        invalidating_differences=_to_strtuple(_get_list(qy, "invalidating_differences")),
    )

    # target_boundary
    tb: dict[str, Any] = _get(sg, "target_boundary") or {}
    target_boundary = TargetBoundaryData(
        closes=_to_strtuple(_get_list(tb, "closes")),
        opens=_to_strtuple(_get_list(tb, "opens")),
        does_not_close=_to_strtuple(_get_list(tb, "does_not_close")),
    )

    # minimum_completion
    mc: dict[str, Any] = _get(sg, "minimum_completion") or {}
    minimum_completion_required = _to_strtuple(_get_list(mc, "required"))

    # identity_inheritance
    ii: dict[str, Any] = _get(sg, "identity_inheritance") or {}
    identity_inheritance = IdentityInheritanceData(
        preserves=_to_strtuple(_get_list(ii, "preserves")),
        allowed_changes=_to_strtuple(_get_list(ii, "allowed_changes")),
        forbidden_changes=_to_strtuple(_get_list(ii, "forbidden_changes")),
    )

    # forbidden_outputs
    fo: dict[str, Any] = _get(sg, "forbidden_outputs") or {}
    forbidden_outputs = ForbiddenOutputsData(
        absolute=_to_strtuple(_get_list(fo, "absolute")),
        layer_specific=_to_strtuple(_get_list(fo, "layer_specific")),
    )

    # residual_policy
    rp: dict[str, Any] = _get(sg, "residual_policy") or {}
    residual_policy = ResidualPolicyData(
        residuals_allowed=_get_bool(rp, "residuals_allowed", True),
        residuals_must_be_visible=_get_bool(rp, "residuals_must_be_visible", True),
        blocking_residuals=_to_strtuple(_get_list(rp, "blocking_residuals")),
        non_blocking_residuals=_to_strtuple(_get_list(rp, "non_blocking_residuals")),
    )

    # trace
    tr: dict[str, Any] = _get(sg, "trace") or {}
    trace = TraceData(
        source_trace=_get_bool(tr, "source_trace", True),
        operation_trace=_get_bool(tr, "operation_trace", True),
        evidence_trace=_get_bool(tr, "evidence_trace", False),
        residual_trace=_get_bool(tr, "residual_trace", True),
    )

    # rank
    rk: dict[str, Any] = _get(sg, "rank") or {}
    rank = RankData(
        initial=_get_str(rk, "initial", "Candidate"),
        ceiling=_get_str(rk, "ceiling", "Candidate"),
        upgrade_requires_gate=_get_bool(rk, "upgrade_requires_gate", True),
        allowed_upgrade_gates=_to_strtuple(_get_list(rk, "allowed_upgrade_gates")),
    )

    # gamma
    gm: dict[str, Any] = _get(sg, "gamma") or {}
    gamma = GammaData(
        target=_get_str(gm, "target"),
        allowed_states=_to_strtuple(_get_list(gm, "allowed_states")),
        minimally_closed_requires=_to_strtuple(_get_list(gm, "minimally_closed_requires")),
    )

    # registry
    rg: dict[str, Any] = _get(sg, "registry") or {}
    registry = RegistryData(
        layer_id=_get_str(rg, "layer_id"),
        allowed_previous_layers=_to_strtuple(_get_list(rg, "allowed_previous_layers")),
        allowed_next_layers=_to_strtuple(_get_list(rg, "allowed_next_layers")),
        forbidden_direct_layers=_to_strtuple(_get_list(rg, "forbidden_direct_layers")),
    )

    # tests
    ts: dict[str, Any] = _get(sg, "tests") or {}
    tests = TestsData(
        required_test_ids=_to_strtuple(_get_list(ts, "required_test_ids")),
    )

    return SlotGeometrySpec(
        schema_version=schema_version,
        id=_get_str(sg, "id"),
        name=_get_str(sg, "name"),
        phase=_get_str(sg, "phase"),
        status=_get_str(sg, "status", "PLANNED"),
        origin=origin,
        branch=branch,
        qiyas=qiyas,
        target_boundary=target_boundary,
        minimum_completion_required=minimum_completion_required,
        identity_inheritance=identity_inheritance,
        forbidden_outputs=forbidden_outputs,
        residual_policy=residual_policy,
        trace=trace,
        rank=rank,
        gamma=gamma,
        registry=registry,
        tests=tests,
    )
