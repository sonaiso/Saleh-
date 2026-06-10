"""
minimum_completion.py — الاكتمال الأدنى

MinimumCompletion ليس checklist سطحيًا.
هو برهان أن الفرع مشروع من أصله.

أي MinimumCompletion يجب أن يثبت:
    1. الأصل موجود.
    2. الفرع مصرح به في MasterLayerRegistry.
    3. توجد علة جامعة بين الأصل والفرع.
    4. يوجد سبب تفريع.
    5. تحققت الشروط.
    6. انتفت الموانع.
    7. فُحص الفرق القادح.
    8. حفظت الهوية.
    9. ظهرت البقايا.
    10. لم ينتج مخرجًا خارج TargetBoundary.

MinimumCompletion = OriginBranchLegitimacy + BoundaryCompletion
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .layer_spec import LayerSpec
    from .target_boundary import TargetBoundary


class MinimumCompletionViolation(Exception):
    """رُفع عند فشل التحقق من الاكتمال الأدنى."""
    pass


@dataclass(frozen=True)
class MinimumCompletionSpec:
    """
    مواصفات الاكتمال الأدنى لطبقة ما.

    required_fields:    الحقول الإلزامية في مخرج الطبقة
    requires_origin:    هل يجب وجود origin_trace؟
    requires_residuals: هل يجب ظهور residuals (حتى لو فارغة)؟
    requires_identity:  هل يجب حفظ الهوية؟
    requires_trace:     هل يجب وجود أثر؟
    requires_forbidden_declared: هل يجب الإعلان عن المحظورات؟
    """
    required_fields: tuple[str, ...]
    requires_origin: bool = True
    requires_residuals: bool = True
    requires_identity: bool = True
    requires_trace: bool = True
    requires_forbidden_declared: bool = True

    def __post_init__(self) -> None:
        if not self.required_fields:
            raise ValueError(
                "MinimumCompletionSpec.required_fields must not be empty — "
                "لا اكتمال بلا تعريف الحقول المطلوبة"
            )

    def verify(
        self,
        candidate_fields: frozenset[str],
        has_origin_trace: bool,
        has_residuals: bool,
        has_identity: bool,
        has_trace: bool,
        has_forbidden_declared: bool,
        output_type: str,
        target_boundary: "TargetBoundary",
    ) -> None:
        """
        تحقق من اكتمال الطبقة. يرفع MinimumCompletionViolation عند الفشل.

        الفحوصات:
            - الحقول الإلزامية موجودة في الـ candidate
            - الأصل له أثر
            - البقايا مُسجَّلة
            - الهوية محفوظة
            - الأثر موجود
            - المحظورات مُعلنة
            - المخرج لا يتجاوز TargetBoundary (لا قفزة محظورة)
        """
        violations: list[str] = []

        # 1. الحقول الإلزامية
        missing_fields = set(self.required_fields) - candidate_fields
        if missing_fields:
            violations.append(
                f"missing required fields: {sorted(missing_fields)}"
            )

        # 2. الأصل له أثر
        if self.requires_origin and not has_origin_trace:
            violations.append("origin trace is missing — الأصل بلا أثر")

        # 3. البقايا مسجلة
        if self.requires_residuals and not has_residuals:
            violations.append("residuals not registered — البقايا مفقودة")

        # 4. الهوية محفوظة
        if self.requires_identity and not has_identity:
            violations.append("identity not preserved — الهوية ضائعة")

        # 5. الأثر موجود
        if self.requires_trace and not has_trace:
            violations.append("trace is missing — لا هوية بلا أثر")

        # 6. المحظورات مُعلنة
        if self.requires_forbidden_declared and not has_forbidden_declared:
            violations.append("forbidden outputs not declared — لا طبقة بلا ممنوعات")

        # 7. المخرج لا يتجاوز الحد (فحص TargetBoundary)
        boundary_state = target_boundary.check_output(output_type)
        from .target_boundary import ClosureState
        if boundary_state == ClosureState.FORBIDDEN_LEAP:
            violations.append(
                f"output_type '{output_type}' is a FORBIDDEN_LEAP — "
                f"تجاوز حد الطبقة ممنوع. الحد يُغلق: {target_boundary.closes}"
            )

        if violations:
            raise MinimumCompletionViolation(
                "MinimumCompletion failed:\n" + "\n".join(f"  - {v}" for v in violations)
            )
