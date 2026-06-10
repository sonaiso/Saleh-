"""
registry_entry.py — مدخل السجل الجبري

القانون:
    العضوية في قائمة = Prior
    وليست حكمًا.

كل قائمة يجب أن تُسجَّل كـ RegistryEntry بحيث:
    - membership_opens: فتح Prior لا إصدار Judgment
    - forbidden_outputs: ما لا يجوز أن ينتجه هذا الـ entry
    - upgrade_requires: ما يلزم لرفع الـ Prior إلى Candidate

مثال:
    حروف الزيادة "سألتمونيها" لا تعني أن الحرف وقع فيه زيادة.
    بل تعني: WeaknessPrior / AugmentEligibilityPrior مفتوح مع بقايا.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RegistryDomain(Enum):
    """نطاق السجل — في أي مرحلة ينتمي هذا الـ entry؟"""
    PHONOLOGICAL_PRIOR = "phonological_prior"
    MORPHOLOGICAL_PRIOR = "morphological_prior"
    SYNTACTIC_PRIOR = "syntactic_prior"
    SEMANTIC_PRIOR = "semantic_prior"
    GENERAL = "general"


class RegistryScope(Enum):
    """نطاق تطبيق السجل."""
    PRE_JUDGMENT = "pre_judgment"
    PRE_CANDIDATE = "pre_candidate"
    EVIDENCE_ONLY = "evidence_only"


class RegistryEntryViolation(Exception):
    """رُفع عند محاولة RegistryEntry إصدار judgment."""
    pass


@dataclass(frozen=True)
class RegistryEntry:
    """
    مدخل السجل الجبري.

    هذا الكائن لا ينتج Judgment، بل يفتح Prior فقط.

    Attributes:
        id:               معرّف فريد للـ entry
        domain:           نطاق السجل
        scope:            نطاق التطبيق (يجب أن يكون pre_judgment)
        membership_opens: ما يفتحه عضوية هذا الـ entry (Prior)
        forbidden_outputs: ما لا يجوز إنتاجه مباشرةً
        upgrade_requires: ما يلزم لرفع Prior إلى Candidate
        notes:            ملاحظات توضيحية (اختياري)
    """
    id: str
    domain: RegistryDomain
    scope: RegistryScope
    membership_opens: str
    forbidden_outputs: tuple[str, ...]
    upgrade_requires: tuple[str, ...]
    notes: str = ""
    # Optional members list (as string keys, not logic)
    members: tuple[str, ...] = field(default=())

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("RegistryEntry.id is required")
        if not self.membership_opens:
            raise ValueError(
                "RegistryEntry.membership_opens is required — "
                "العضوية في السجل تفتح Prior، لا تُصدر Judgment"
            )
        if not self.forbidden_outputs:
            raise ValueError(
                "RegistryEntry.forbidden_outputs is required — "
                "كل entry يجب أن يُصرّح صراحةً بما لا ينتجه"
            )
        if not self.upgrade_requires:
            raise ValueError(
                "RegistryEntry.upgrade_requires is required — "
                "يجب تحديد شروط رفع Prior إلى Candidate"
            )
        # الـ scope يجب أن يكون pre_judgment
        if self.scope not in (RegistryScope.PRE_JUDGMENT, RegistryScope.PRE_CANDIDATE, RegistryScope.EVIDENCE_ONLY):
            raise ValueError(
                f"RegistryEntry.scope must be pre_judgment, pre_candidate, or evidence_only. Got: {self.scope}"
            )

    def opens_prior(self, for_member: str) -> str:
        """
        إرجاع نوع الـ Prior الذي تفتحه هذه العضوية.
        لا ينتج Judgment ولا Candidate مباشرة.
        """
        if for_member not in self.members and self.members:
            raise RegistryEntryViolation(
                f"'{for_member}' is not a member of registry '{self.id}'"
            )
        return self.membership_opens

    def assert_no_judgment(self, output_type: str) -> None:
        """
        تأكد أن المخرج المقترح ليس Judgment محظورًا.
        يرفع RegistryEntryViolation إذا كان المخرج محظورًا.
        """
        if output_type in self.forbidden_outputs:
            raise RegistryEntryViolation(
                f"RegistryEntry '{self.id}' cannot produce '{output_type}'. "
                f"This entry only opens: '{self.membership_opens}'. "
                f"Forbidden outputs: {self.forbidden_outputs}"
            )
