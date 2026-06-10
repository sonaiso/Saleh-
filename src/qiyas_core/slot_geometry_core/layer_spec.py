"""
layer_spec.py — عقد الطبقة الدستوري

كل طبقة في المشروع يجب أن تُعرَّف عبر LayerSpec قبل أي كود.
LayerSpec هو العقد التنفيذي الملزم الذي يجيب عن الأسئلة العشرة:
    1. ما أصلها؟
    2. ما فرعها؟
    3. ما مقايسها؟
    4. ما حدها؟
    5. ما اكتمالها الأدنى؟
    6. ما هويتها الموروثة؟
    7. ما ممنوعاتها؟
    8. ما أثرها؟
    9. ما بقاياها؟
    10. ما رتبتها؟
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class LayerStatus(Enum):
    """حالة الطبقة في دورة حياتها."""
    PLANNED = "planned"
    SPECIFIED = "specified"
    IMPLEMENTED = "implemented"
    AUDITED = "audited"
    CLOSED = "closed"


@dataclass(frozen=True)
class OriginSpec:
    """
    أصل الطبقة — من أين جاءت؟

    لا طبقة بلا أصل.
    الأصل هو طبقة سابقة مسجلة أو مصدر Unicode.
    """
    layer_id: str
    output_type: str

    def __post_init__(self) -> None:
        if not self.layer_id:
            raise ValueError("OriginSpec.layer_id is required — لا طبقة بلا أصل")
        if not self.output_type:
            raise ValueError("OriginSpec.output_type is required")


@dataclass(frozen=True)
class BranchSpec:
    """
    فرع الطبقة — ما الذي تنتجه؟

    الفرع يجب أن يكون مصرحًا به في MasterLayerRegistry.
    الفرع لا يجوز أن يتجاوز TargetBoundary الخاص به.
    """
    output_type: str
    branch_reason: str

    def __post_init__(self) -> None:
        if not self.output_type:
            raise ValueError("BranchSpec.output_type is required")
        if not self.branch_reason:
            raise ValueError("BranchSpec.branch_reason is required — لا فرع بلا سبب تفريع")


@dataclass(frozen=True)
class LayerSpec:
    """
    عقد الطبقة الدستوري الكامل.

    هذا هو شرط الإمكان البرمجي الأول:
    كل طبقة تصبح عقدًا قابلًا للتحقق، لا فكرة في وثيقة.

    الحقول الإلزامية:
        id              — معرّف فريد (مثل L01_UNICODE)
        name            — اسم الطبقة الكانونيكي
        phase           — مرحلة التطوير
        origin          — OriginSpec محدد
        branch          — BranchSpec محدد
        shared_cause    — العلة الجامعة بين الأصل والفرع
        conditions      — شروط تحقق الانتقال
        blockers        — موانع تمنع الانتقال
        invalidating_differences — فروق قادحة تبطل القياس
        target_boundary_closes   — ما يُغلقه هذا الطبقة
        target_boundary_opens    — ما يفتحه للطبقة التالية (لا يغلقه)
        forbidden_outputs        — مخرجات محظورة صراحةً
        minimum_required_fields  — حقول MinimumCompletionSpec المطلوبة
        preserves_ids            — هويات يجب الحفاظ عليها من الأصل
        allowed_changes          — ما يُسمح تغييره
        forbidden_changes        — ما يُمنع تغييره صراحةً
        status                   — حالة الطبقة
    """
    id: str
    name: str
    phase: str
    origin: OriginSpec
    branch: BranchSpec

    # QiyasContract fields
    shared_cause: str
    conditions: tuple[str, ...]
    blockers: tuple[str, ...]
    invalidating_differences: tuple[str, ...]

    # TargetBoundary fields
    target_boundary_closes: tuple[str, ...]
    target_boundary_opens: tuple[str, ...]

    # ForbiddenOutputs — always required
    forbidden_outputs: tuple[str, ...]

    # MinimumCompletion fields
    minimum_required_fields: tuple[str, ...]

    # IdentityInheritance fields
    preserves_ids: tuple[str, ...]
    allowed_changes: tuple[str, ...]
    forbidden_changes: tuple[str, ...]

    status: LayerStatus = LayerStatus.SPECIFIED

    # Optional: allowed previous and next layers for registry enforcement
    allowed_previous_layer_ids: tuple[str, ...] = field(default=())
    allowed_next_layer_ids: tuple[str, ...] = field(default=())
    forbidden_direct_next_layer_ids: tuple[str, ...] = field(default=())

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("LayerSpec.id is required")
        if not self.name:
            raise ValueError("LayerSpec.name is required")
        if not self.phase:
            raise ValueError("LayerSpec.phase is required")
        if not self.shared_cause:
            raise ValueError(
                "LayerSpec.shared_cause is required — لا مقايسة بلا علة جامعة"
            )
        if not self.conditions:
            raise ValueError(
                "LayerSpec.conditions must have at least one condition"
            )
        if not self.target_boundary_closes:
            raise ValueError(
                "LayerSpec.target_boundary_closes is required — لا حد بلا ما يُغلقه"
            )
        if not self.forbidden_outputs:
            raise ValueError(
                "LayerSpec.forbidden_outputs is required — كل طبقة يجب أن تُصرّح بممنوعاتها"
            )
        # المخرجات المحظورة الإلزامية لكل طبقة
        _absolute_forbidden = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
        missing = _absolute_forbidden - set(self.forbidden_outputs)
        if missing:
            raise ValueError(
                f"LayerSpec.forbidden_outputs must include {missing} — "
                "لا طبقة تنتج حكمًا أو واقعًا أو معنى نهائيًا"
            )
        if not self.minimum_required_fields:
            raise ValueError(
                "LayerSpec.minimum_required_fields is required — "
                "لا اكتمال بلا تعريف الاكتمال الأدنى"
            )
        if not self.preserves_ids:
            raise ValueError(
                "LayerSpec.preserves_ids is required — لا هوية بلا أثر"
            )
        # Validate no forbidden_changes listed as allowed_changes
        overlap = set(self.allowed_changes) & set(self.forbidden_changes)
        if overlap:
            raise ValueError(
                f"allowed_changes and forbidden_changes overlap: {overlap}"
            )
