"""
gamma.py — دالة Gamma المقيدة بالحد المستهدف

القانون:
    لا Gamma بلا LayerSpec.
    لا Gamma بلا TargetBoundary.
    لا Gamma بلا Candidate.

    Gamma للحرف+الحركة لا تفحص المقطع.
    Gamma للمقطع لا تفحص الجذر.
    Gamma للجذر لا تفحص المعنى.

الصيغة الصحيحة:
    gamma(candidate, layer_spec, target_boundary) -> GammaResult
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .layer_spec import LayerSpec
    from .target_boundary import TargetBoundary


class GammaStatus(Enum):
    """
    حالة نتيجة Gamma.

    MINIMALLY_CLOSED  — الفرع اكتمل اكتمالًا أدنى داخل الحد
    PERFORATED_CLOSED — الفرع مكتمل لكن مع بقايا غير قاطعة
    OPEN              — الفرع لم يكتمل بعد (قابل للاستمرار)
    BLOCKED           — الفرع محجوب (شروط أو موانع فشلت)
    FORBIDDEN_LEAP    — محاولة تجاوز الحد المستهدف
    """
    MINIMALLY_CLOSED = "minimally_closed"
    PERFORATED_CLOSED = "perforated_closed"
    OPEN = "open"
    BLOCKED = "blocked"
    FORBIDDEN_LEAP = "forbidden_leap"


@dataclass(frozen=True)
class GammaResult:
    """
    نتيجة تطبيق Gamma على مرشح.

    Attributes:
        status:         حالة الاكتمال
        layer_id:       معرّف الطبقة التي طُبّقت عليها Gamma
        target_boundary_closes: الحد المستهدف الذي فُحص الاكتمال داخله
        violations:     انتهاكات وُجدت (فارغة عند الاكتمال)
        residual_keys:  مفاتيح البقايا المُسجَّلة
        is_complete:    اختصار — هل اكتمل الفرع؟
    """
    status: GammaStatus
    layer_id: str
    target_boundary_closes: tuple[str, ...]
    violations: tuple[str, ...]
    residual_keys: tuple[str, ...]

    @property
    def is_complete(self) -> bool:
        return self.status in (
            GammaStatus.MINIMALLY_CLOSED,
            GammaStatus.PERFORATED_CLOSED,
        )

    @property
    def is_forbidden_leap(self) -> bool:
        return self.status == GammaStatus.FORBIDDEN_LEAP


def gamma(
    candidate_type: str,
    candidate_fields: frozenset[str],
    candidate_has_residuals: bool,
    candidate_identity_ids: frozenset[str],
    candidate_trace_ids: frozenset[str],
    layer_spec: "LayerSpec",
    target_boundary: "TargetBoundary",
) -> GammaResult:
    """
    دالة Gamma المقيدة بالحد المستهدف.

    تفحص هل هذا الفرع اكتمل اكتمالًا أدنى داخل هذا الحد المستهدف.

    لا تفحص:
        - اكتمال طبقة أخرى
        - صحة المعنى اللغوي
        - المخرجات النهائية

    Args:
        candidate_type:          نوع المرشح المُنتَج
        candidate_fields:        مجموعة أسماء الحقول الموجودة في المرشح
        candidate_has_residuals: هل المرشح يحمل بقايا؟
        candidate_identity_ids:  هويات المرشح
        candidate_trace_ids:     آثار المرشح
        layer_spec:              عقد الطبقة التي أنتجت المرشح
        target_boundary:         الحد المستهدف لهذه الطبقة

    Returns:
        GammaResult مع الحالة والانتهاكات
    """
    from .target_boundary import ClosureState

    violations: list[str] = []
    residual_keys: list[str] = []

    # 1. فحص TargetBoundary — هل نوع المخرج مسموح به؟
    boundary_state = target_boundary.check_output(candidate_type)
    if boundary_state == ClosureState.FORBIDDEN_LEAP:
        return GammaResult(
            status=GammaStatus.FORBIDDEN_LEAP,
            layer_id=layer_spec.id,
            target_boundary_closes=target_boundary.closes,
            violations=(
                f"FORBIDDEN_LEAP: '{candidate_type}' is not within "
                f"target_boundary.closes={target_boundary.closes}. "
                f"does_not_close={target_boundary.does_not_close}",
            ),
            residual_keys=(),
        )

    # 2. فحص الحقول الإلزامية
    missing_fields = set(layer_spec.minimum_required_fields) - candidate_fields
    if missing_fields:
        violations.append(f"missing required fields: {sorted(missing_fields)}")
        residual_keys.append("missing_required_fields")

    # 3. فحص المخرجات المحظورة
    if candidate_type in layer_spec.forbidden_outputs:
        violations.append(
            f"candidate_type '{candidate_type}' is in layer forbidden_outputs"
        )
        residual_keys.append("forbidden_output_type")

    # 4. فحص الهوية — يجب أن تكون موجودة
    if not candidate_identity_ids:
        violations.append("candidate has no identity_ids — الهوية مفقودة")
        residual_keys.append("missing_identity")

    # 5. فحص الأثر — يجب أن يكون موجودًا
    if not candidate_trace_ids:
        violations.append("candidate has no trace_ids — الأثر مفقود")
        residual_keys.append("missing_trace")

    # 6. فحص identity ≠ trace (الثابت الدستوري الأول)
    id_trace_overlap = candidate_identity_ids & candidate_trace_ids
    if id_trace_overlap:
        violations.append(
            f"identity and trace overlap: {id_trace_overlap} — "
            "identity is not trace (Constitutional Invariant #1)"
        )
        residual_keys.append("identity_trace_overlap")

    # 7. فحص الشروط الدنيا
    missing_conditions = set(layer_spec.conditions) - candidate_fields
    if missing_conditions:
        # الشروط المفقودة تُدرج كبقايا لا كحجب كامل
        residual_keys.extend(f"condition_not_met:{c}" for c in sorted(missing_conditions))

    # 8. فحص الموانع (blockers)
    active_blockers = set(layer_spec.blockers) & candidate_fields
    if active_blockers:
        violations.append(f"active blockers found: {sorted(active_blockers)}")
        residual_keys.append("active_blockers")

    # تحديد الحالة النهائية
    if violations:
        return GammaResult(
            status=GammaStatus.BLOCKED,
            layer_id=layer_spec.id,
            target_boundary_closes=target_boundary.closes,
            violations=tuple(violations),
            residual_keys=tuple(residual_keys),
        )

    if residual_keys:
        # بقايا موجودة لكن لا انتهاكات قاطعة
        return GammaResult(
            status=GammaStatus.PERFORATED_CLOSED,
            layer_id=layer_spec.id,
            target_boundary_closes=target_boundary.closes,
            violations=(),
            residual_keys=tuple(residual_keys),
        )

    return GammaResult(
        status=GammaStatus.MINIMALLY_CLOSED,
        layer_id=layer_spec.id,
        target_boundary_closes=target_boundary.closes,
        violations=(),
        residual_keys=(),
    )
