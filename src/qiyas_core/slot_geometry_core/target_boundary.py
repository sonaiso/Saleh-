"""
target_boundary.py — حد الطبقة المستهدف

TargetBoundary يُعرّف بدقة ما تُغلقه الطبقة وما لا تُغلقه.

القانون:
    Gamma للحرف+الحركة لا تفحص المقطع.
    Gamma للمقطع لا تفحص الجذر.
    Gamma للجذر لا تفحص المعنى.
    كل Gamma مقيدة بـ TargetBoundary محدد.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClosureState(Enum):
    """
    حالات إغلاق الطبقة.

    OPEN              — الطبقة مفتوحة، الانتقال ممكن
    MINIMALLY_CLOSED  — الطبقة مغلقة بالحد الأدنى الكافي
    PERFORATED_CLOSED — الطبقة مغلقة مع بقايا غير قاطعة
    BLOCKED           — الانتقال محجوب
    FORBIDDEN_LEAP    — محاولة تجاوز حد الطبقة (قفزة محظورة)
    """
    OPEN = "open"
    MINIMALLY_CLOSED = "minimally_closed"
    PERFORATED_CLOSED = "perforated_closed"
    BLOCKED = "blocked"
    FORBIDDEN_LEAP = "forbidden_leap"


@dataclass(frozen=True)
class TargetBoundary:
    """
    حد الطبقة المستهدف — ما الذي تُغلقه هذه الطبقة بالضبط؟

    closes:     ما تُغلقه هذه الطبقة (مسموح بإنتاجه)
    does_not_close: ما لا تُغلقه — أي إنتاج لأي منها يعد FORBIDDEN_LEAP

    مثال صحيح:
        closes = ("written_surface_units",)
        does_not_close = ("syllable", "phoneme", "root", "meaning", "hukm")
    """
    closes: tuple[str, ...]
    does_not_close: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.closes:
            raise ValueError(
                "TargetBoundary.closes is required — لا حد بلا ما يُغلقه"
            )
        # لا تداخل بين ما يُغلق وما لا يُغلق
        overlap = set(self.closes) & set(self.does_not_close)
        if overlap:
            raise ValueError(
                f"TargetBoundary: same type in both closes and does_not_close: {overlap}"
            )

    def forbids(self, output_type: str) -> bool:
        """هل هذا النوع محظور الإنتاج في هذه الطبقة؟"""
        return output_type in self.does_not_close

    def allows(self, output_type: str) -> bool:
        """هل هذا النوع مسموح إنتاجه في هذه الطبقة؟"""
        return output_type in self.closes

    def check_output(self, output_type: str) -> ClosureState:
        """
        فحص ما إذا كان الـ output_type مسموحًا به في هذا الحد.

        Returns:
            MINIMALLY_CLOSED إذا كان النوع ضمن closes
            FORBIDDEN_LEAP   إذا كان النوع ضمن does_not_close
            OPEN             إذا لم يُذكر (غير محدد بعد)
        """
        if self.allows(output_type):
            return ClosureState.MINIMALLY_CLOSED
        if self.forbids(output_type):
            return ClosureState.FORBIDDEN_LEAP
        return ClosureState.OPEN
