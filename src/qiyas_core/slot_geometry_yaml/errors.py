"""
errors.py — أخطاء slot_geometry_yaml

كل خطأ يجب أن يكون محددًا ويحمل موضع الخطأ في ملف YAML.

القانون:
    لا YAML بلا Origin وBranch.
    لا Origin/Branch بلا Qiyas.
    لا Qiyas بلا Boundary.
    لا Boundary بلا MinimumCompletion.
    لا MinimumCompletion بلا IdentityInheritance وTrace وResiduals وRank وGamma.
"""
from __future__ import annotations


class SlotGeometryYAMLError(Exception):
    """الخطأ الجذر لجميع أخطاء slot_geometry_yaml."""
    pass


class SchemaViolation(SlotGeometryYAMLError):
    """
    رُفع عند انتهاك بنية القالب الأعلى.

    يحمل:
        field_path: مسار الحقل المنتهك (مثل "slot_geometry.origin.layer_id")
        reason:     سبب الانتهاك بالعربية والإنجليزية
    """
    def __init__(self, field_path: str, reason: str) -> None:
        self.field_path = field_path
        self.reason = reason
        super().__init__(f"SchemaViolation at '{field_path}': {reason}")


class MissingRequiredField(SchemaViolation):
    """رُفع عند غياب حقل إلزامي في ملف YAML."""
    def __init__(self, field_path: str) -> None:
        super().__init__(
            field_path=field_path,
            reason=f"field is required but missing — الحقل إلزامي وغير موجود",
        )


class EmptyRequiredField(SchemaViolation):
    """رُفع عند وجود حقل إلزامي لكنه فارغ أو سلسلة فارغة."""
    def __init__(self, field_path: str) -> None:
        super().__init__(
            field_path=field_path,
            reason="field is required and must not be empty — الحقل إلزامي ولا يجوز أن يكون فارغًا",
        )


class InvalidStatusValue(SchemaViolation):
    """رُفع عند استخدام قيمة غير مسموحة لـ status."""
    ALLOWED = frozenset({"PLANNED", "SPECIFIED", "IMPLEMENTED", "AUDITED", "CLOSED"})

    def __init__(self, value: str) -> None:
        super().__init__(
            field_path="slot_geometry.status",
            reason=(
                f"'{value}' is not a valid status. "
                f"Allowed: {sorted(self.ALLOWED)} — "
                "القيمة غير مسموحة"
            ),
        )


class InvalidRankCeiling(SchemaViolation):
    """رُفع عند استخدام رتبة غير مسموحة."""
    ALLOWED = frozenset({
        "Prior", "Candidate", "LicensedCandidate",
        "StrongCandidate", "Certificate", "Judgment",
    })

    def __init__(self, value: str, field_path: str = "slot_geometry.branch.rank_ceiling") -> None:
        super().__init__(
            field_path=field_path,
            reason=(
                f"'{value}' is not a valid rank_ceiling. "
                f"Allowed: {sorted(self.ALLOWED)} — "
                "الرتبة غير مسموحة"
            ),
        )


class MissingAbsoluteForbidden(SchemaViolation):
    """رُفع عند غياب أحد المحظورات المطلقة الإلزامية."""
    REQUIRED = frozenset({"HukmCandidate", "RealityClaim", "FinalMeaning"})

    def __init__(self, missing: set[str]) -> None:
        super().__init__(
            field_path="slot_geometry.forbidden_outputs.absolute",
            reason=(
                f"missing absolute forbidden outputs: {sorted(missing)} — "
                "المحظورات المطلقة الإلزامية غير موجودة: "
                "HukmCandidate وRealityClaim وFinalMeaning إلزامية في كل طبقة"
            ),
        )


class TargetBoundaryViolation(SchemaViolation):
    """رُفع عند وجود تعارض في target_boundary (closes ∩ does_not_close ≠ ∅)."""
    def __init__(self, overlap: set[str]) -> None:
        super().__init__(
            field_path="slot_geometry.target_boundary",
            reason=(
                f"same entries in both closes and does_not_close: {sorted(overlap)} — "
                "لا يجوز أن يكون الحد في closes وdoes_not_close معًا"
            ),
        )


class EmptyTargetBoundaryCloses(SchemaViolation):
    """رُفع عند خلوّ target_boundary.closes من أي عنصر."""
    def __init__(self) -> None:
        super().__init__(
            field_path="slot_geometry.target_boundary.closes",
            reason=(
                "target_boundary.closes must contain at least one entry — "
                "لا حد بلا ما يُغلقه"
            ),
        )


class EmptyIdentityInheritancePreserves(SchemaViolation):
    """رُفع عند خلوّ identity_inheritance.preserves من أي عنصر."""
    def __init__(self) -> None:
        super().__init__(
            field_path="slot_geometry.identity_inheritance.preserves",
            reason=(
                "identity_inheritance.preserves must contain at least one entry — "
                "لا هوية موروثة بلا تصريح بما يُحفَظ"
            ),
        )


class AllowedForbiddenOverlap(SchemaViolation):
    """رُفع عند تداخل allowed_changes وforbidden_changes."""
    def __init__(self, overlap: set[str]) -> None:
        super().__init__(
            field_path="slot_geometry.identity_inheritance",
            reason=(
                f"allowed_changes and forbidden_changes overlap: {sorted(overlap)} — "
                "تعارض بين المسموح والمحظور"
            ),
        )


class MissingGammaTarget(SchemaViolation):
    """رُفع عند غياب gamma.target أو خلوّه."""
    def __init__(self) -> None:
        super().__init__(
            field_path="slot_geometry.gamma.target",
            reason="gamma.target is required and must not be empty — لا Gamma بلا حد مستهدف",
        )


class YAMLLoadError(SlotGeometryYAMLError):
    """رُفع عند فشل تحميل ملف YAML (خطأ بناء جملة أو مسار غير صحيح)."""
    def __init__(self, path: str, cause: Exception) -> None:
        self.path = path
        self.cause = cause
        super().__init__(f"Failed to load YAML from '{path}': {cause}")
