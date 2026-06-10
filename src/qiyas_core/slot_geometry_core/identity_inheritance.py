"""
identity_inheritance.py — عقد الهوية الموروثة

كل طبقة يجب أن تُثبت:
    - ما الهويات التي تحفظها من الأصل
    - ما الذي يُسمح تغييره
    - ما الذي يُمنع تغييره

القانون:
    Evidence may add trace but must not consume identity.
    Candidate identity must preserve source identities.
"""
from __future__ import annotations

from dataclasses import dataclass


class IdentityInheritanceViolation(Exception):
    """رُفع عند فشل التحقق من الهوية الموروثة."""
    pass


@dataclass(frozen=True)
class IdentityInheritance:
    """
    عقد الهوية الموروثة.

    preserves:         هويات يجب إيجادها في المخرج
    allowed_changes:   ما يُسمح تغييره (تجميع وحدات، إضافة context)
    forbidden_changes: ما يُمنع تغييره صراحةً (تعيين جذر، معنى، إعراب)
    """
    preserves: tuple[str, ...]
    allowed_changes: tuple[str, ...]
    forbidden_changes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.preserves:
            raise ValueError(
                "IdentityInheritance.preserves is required — "
                "لا هوية بلا أثر: كل طبقة يجب أن تحفظ هويات من أصلها"
            )
        overlap = set(self.allowed_changes) & set(self.forbidden_changes)
        if overlap:
            raise ValueError(
                f"IdentityInheritance: same item in both allowed and forbidden: {overlap}"
            )

    def verify(
        self,
        source_identity_ids: frozenset[str],
        output_identity_ids: frozenset[str],
        output_operation: str,
    ) -> None:
        """
        تحقق من الهوية الموروثة.

        يرفع IdentityInheritanceViolation إذا:
            - هوية مطلوبة الحفظ غابت من المخرج
            - عملية محظورة وُجدت في المخرج
        """
        violations: list[str] = []

        # كل هوية مطلوبة يجب أن تظهر في المخرج
        for required_id_pattern in self.preserves:
            # الفحص بالمطابقة المباشرة أو المطابقة الجزئية
            preserved = any(
                required_id_pattern in oid
                for oid in output_identity_ids
            ) or any(
                required_id_pattern in sid
                for sid in source_identity_ids
                if sid in output_identity_ids
            )
            if not preserved:
                violations.append(
                    f"identity '{required_id_pattern}' not preserved in output"
                )

        # العملية لا تجوز أن تكون محظورة
        if output_operation in self.forbidden_changes:
            violations.append(
                f"operation '{output_operation}' is forbidden — "
                f"ممنوع: {self.forbidden_changes}"
            )

        if violations:
            raise IdentityInheritanceViolation(
                "IdentityInheritance failed:\n"
                + "\n".join(f"  - {v}" for v in violations)
            )
