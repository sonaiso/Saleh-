"""
slot_geometry_yaml — PR-SCG-YAML-0
حزمة تحميل والتحقق من ملفات YAML لطبقات SlotGeometry.

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
    أي LayerSpec لاحق يجب أن يكون له YAML مطابق.
"""

from .errors import (
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
    SlotGeometryYAMLError,
    TargetBoundaryViolation,
    YAMLLoadError,
)
from .loader import (
    BranchData,
    ForbiddenOutputsData,
    GammaData,
    IdentityInheritanceData,
    OriginData,
    QiyasData,
    RankData,
    RegistryData,
    ResidualPolicyData,
    SlotGeometrySpec,
    TargetBoundaryData,
    TestsData,
    TraceData,
    load_slot_geometry_yaml,
)
from .validator import SlotGeometryValidator, ValidationResult

__all__ = [
    # errors
    "AllowedForbiddenOverlap",
    "EmptyIdentityInheritancePreserves",
    "EmptyRequiredField",
    "EmptyTargetBoundaryCloses",
    "InvalidRankCeiling",
    "InvalidStatusValue",
    "MissingAbsoluteForbidden",
    "MissingGammaTarget",
    "MissingRequiredField",
    "SchemaViolation",
    "SlotGeometryYAMLError",
    "TargetBoundaryViolation",
    "YAMLLoadError",
    # loader
    "BranchData",
    "ForbiddenOutputsData",
    "GammaData",
    "IdentityInheritanceData",
    "OriginData",
    "QiyasData",
    "RankData",
    "RegistryData",
    "ResidualPolicyData",
    "SlotGeometrySpec",
    "TargetBoundaryData",
    "TestsData",
    "TraceData",
    "load_slot_geometry_yaml",
    # validator
    "SlotGeometryValidator",
    "ValidationResult",
]
