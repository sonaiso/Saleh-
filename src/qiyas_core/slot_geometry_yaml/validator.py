"""
validator.py — مُحقِّق ملفات YAML لـ SlotGeometry

القانون:
    لا SlotGeometry بلا YAML.
    لا YAML بلا Origin وBranch.
    لا Origin/Branch بلا Qiyas.
    لا Qiyas بلا Boundary.
    لا Boundary بلا MinimumCompletion.
    لا MinimumCompletion بلا IdentityInheritance وTrace وResiduals وRank وGamma.

المُحقِّق يتحقق من:
    1. schema_version موجود وصحيح
    2. slot_geometry.id وname وphase غير فارغة
    3. status قيمة مسموحة
    4. origin.layer_id وorigin.output_type غير فارغتين
    5. branch.output_type وbranch.branch_reason غير فارغتين
    6. branch.rank_ceiling قيمة مسموحة
    7. qiyas.shared_cause وeffective_attribute وbranching_reason غير فارغة
    8. target_boundary.closes غير فارغ
    9. target_boundary: لا تداخل بين closes وdoes_not_close
    10. identity_inheritance.preserves غير فارغ
    11. identity_inheritance: لا تداخل بين allowed_changes وforbidden_changes
    12. forbidden_outputs.absolute تحتوي HukmCandidate وRealityClaim وFinalMeaning
    13. gamma.target غير فارغ
    14. registry.layer_id غير فارغ

YAML لا ينتج runtime.
YAML لا يثبت حكمًا.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

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
)

if TYPE_CHECKING:
    from .loader import SlotGeometrySpec


_SUPPORTED_SCHEMA_VERSIONS = frozenset({"1.0"})
_VALID_STATUSES = frozenset({"PLANNED", "SPECIFIED", "IMPLEMENTED", "AUDITED", "CLOSED"})
_VALID_RANK_CEILINGS = frozenset({
    "Prior", "Candidate", "LicensedCandidate",
    "StrongCandidate", "Certificate", "Judgment",
})
_ABSOLUTE_FORBIDDEN = frozenset({"HukmCandidate", "RealityClaim", "FinalMeaning"})


@dataclass(frozen=True)
class ValidationResult:
    """
    نتيجة التحقق من ملف YAML.

    Attributes:
        is_valid:    هل النتيجة صالحة؟
        violations:  قائمة الانتهاكات (فارغة عند النجاح)
    """
    is_valid: bool
    violations: tuple[SchemaViolation, ...]

    @property
    def has_violations(self) -> bool:
        return bool(self.violations)


class SlotGeometryValidator:
    """
    مُحقِّق SlotGeometrySpec.

    الاستخدام:
        spec = load_slot_geometry_yaml(path)
        validator = SlotGeometryValidator()
        result = validator.validate(spec)
        if not result.is_valid:
            for v in result.violations:
                print(v)

    أو للحصول على الانتهاك الأول مباشرةً:
        validator.validate_strict(spec)  # يرفع SchemaViolation عند أول انتهاك
    """

    def validate(self, spec: "SlotGeometrySpec") -> ValidationResult:
        """
        تحقق من SlotGeometrySpec وأعد ValidationResult.

        يجمع جميع الانتهاكات بدلًا من التوقف عند الأول.
        """
        violations: list[SchemaViolation] = []

        # 1. schema_version
        if not spec.schema_version:
            violations.append(MissingRequiredField("schema_version"))
        elif spec.schema_version not in _SUPPORTED_SCHEMA_VERSIONS:
            violations.append(SchemaViolation(
                "schema_version",
                f"unsupported schema_version '{spec.schema_version}'. "
                f"Supported: {sorted(_SUPPORTED_SCHEMA_VERSIONS)}"
            ))

        # 2. slot_geometry.id
        if not spec.id:
            violations.append(EmptyRequiredField("slot_geometry.id"))

        # 3. slot_geometry.name
        if not spec.name:
            violations.append(EmptyRequiredField("slot_geometry.name"))

        # 4. slot_geometry.phase
        if not spec.phase:
            violations.append(EmptyRequiredField("slot_geometry.phase"))

        # 5. status
        if spec.status not in _VALID_STATUSES:
            violations.append(InvalidStatusValue(spec.status))

        # 6. origin.layer_id
        if not spec.origin.layer_id:
            violations.append(EmptyRequiredField("slot_geometry.origin.layer_id"))

        # 7. origin.output_type
        if not spec.origin.output_type:
            violations.append(EmptyRequiredField("slot_geometry.origin.output_type"))

        # 8. branch.output_type
        if not spec.branch.output_type:
            violations.append(EmptyRequiredField("slot_geometry.branch.output_type"))

        # 9. branch.branch_reason
        if not spec.branch.branch_reason:
            violations.append(EmptyRequiredField("slot_geometry.branch.branch_reason"))

        # 10. branch.rank_ceiling
        if spec.branch.rank_ceiling not in _VALID_RANK_CEILINGS:
            violations.append(InvalidRankCeiling(spec.branch.rank_ceiling))

        # 11. qiyas.shared_cause
        if not spec.qiyas.shared_cause:
            violations.append(EmptyRequiredField("slot_geometry.qiyas.shared_cause"))

        # 12. qiyas.effective_attribute
        if not spec.qiyas.effective_attribute:
            violations.append(EmptyRequiredField("slot_geometry.qiyas.effective_attribute"))

        # 13. qiyas.branching_reason
        if not spec.qiyas.branching_reason:
            violations.append(EmptyRequiredField("slot_geometry.qiyas.branching_reason"))

        # 14. target_boundary.closes must not be empty
        if not spec.target_boundary.closes:
            violations.append(EmptyTargetBoundaryCloses())

        # 15. target_boundary: no overlap between closes and does_not_close
        overlap = set(spec.target_boundary.closes) & set(spec.target_boundary.does_not_close)
        if overlap:
            from .errors import TargetBoundaryViolation
            violations.append(TargetBoundaryViolation(overlap))

        # 16. identity_inheritance.preserves must not be empty
        if not spec.identity_inheritance.preserves:
            violations.append(EmptyIdentityInheritancePreserves())

        # 17. identity_inheritance: no overlap between allowed_changes and forbidden_changes
        ii_overlap = (
            set(spec.identity_inheritance.allowed_changes)
            & set(spec.identity_inheritance.forbidden_changes)
        )
        if ii_overlap:
            violations.append(AllowedForbiddenOverlap(ii_overlap))

        # 18. forbidden_outputs.absolute must include absolute forbidden set
        present = set(spec.forbidden_outputs.absolute)
        missing = _ABSOLUTE_FORBIDDEN - present
        if missing:
            violations.append(MissingAbsoluteForbidden(missing))

        # 19. gamma.target must not be empty
        if not spec.gamma.target:
            violations.append(MissingGammaTarget())

        # 20. registry.layer_id must not be empty
        if not spec.registry.layer_id:
            violations.append(EmptyRequiredField("slot_geometry.registry.layer_id"))

        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=tuple(violations),
        )

    def validate_strict(self, spec: "SlotGeometrySpec") -> None:
        """
        تحقق صارم — يرفع SchemaViolation عند أول انتهاك.

        Args:
            spec: SlotGeometrySpec المُراد التحقق منه

        Raises:
            SchemaViolation: عند أول انتهاك يُكتشف
        """
        result = self.validate(spec)
        if result.has_violations:
            raise result.violations[0]
