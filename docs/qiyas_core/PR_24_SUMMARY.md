# PR #24: Make Type-Specific Proof Required by Rule

## الفجوة الدستورية (Constitutional Gap)

بعد PR #23، كانت الأدلة النوعية موجودة في `EvidenceSet`:

```text
wasf:is_arabic_letter:evidenced
illah:belongs_to_letter_class:verified
```

لكن `QiyasRule` نفسها كانت تطلب فقط:

```text
required_effective_wasf = ("is_classifiable_codepoint",)
required_illah = ("belongs_to_typed_domain",)
```

هذا يعني أن النوع المحدد (LetterCodePoint، HarakaCodePoint، إلخ) كان يُحدد ديناميكيًا من قبل adapter عبر تعديل `output_candidate_type`، وليس من خلال متطلبات القاعدة نفسها.

## الحل (Solution)

PR #24 يغلق هذه الفجوة بإنشاء **5 قواعد canonical** بدلاً من قاعدة عامة واحدة:

### القواعد الخمس الجديدة

#### 1. LETTER_CODEPOINT_CLASSIFICATION
```python
required_effective_wasf = (
    "is_classifiable_codepoint",
    "is_arabic_letter",  # Type-specific!
)
required_illah = (
    "belongs_to_typed_domain",
    "belongs_to_letter_class",  # Type-specific!
)
output_candidate_type = "LetterCodePoint"
```

#### 2. HARAKA_CODEPOINT_CLASSIFICATION
```python
required_effective_wasf = (
    "is_classifiable_codepoint",
    "is_arabic_haraka",  # Type-specific!
)
required_illah = (
    "belongs_to_typed_domain",
    "belongs_to_haraka_class",  # Type-specific!
)
output_candidate_type = "HarakaCodePoint"
```

#### 3. BOUNDARY_CODEPOINT_CLASSIFICATION
```python
required_effective_wasf = (
    "is_classifiable_codepoint",
    "is_whitespace_boundary",  # Type-specific!
)
required_illah = (
    "belongs_to_typed_domain",
    "belongs_to_boundary_class",  # Type-specific!
)
output_candidate_type = "BoundaryCodePoint"
```

#### 4. PUNCTUATION_CODEPOINT_CLASSIFICATION
```python
required_effective_wasf = (
    "is_classifiable_codepoint",
    "is_arabic_punctuation",  # Type-specific!
)
required_illah = (
    "belongs_to_typed_domain",
    "belongs_to_punctuation_class",  # Type-specific!
)
output_candidate_type = "PunctuationCodePoint"
```

#### 5. RESIDUAL_CODEPOINT_CLASSIFICATION
```python
required_effective_wasf = (
    "is_classifiable_codepoint",
    "is_unclassified_codepoint",  # Type-specific!
)
required_illah = (
    "belongs_to_typed_domain",
    "belongs_to_residual_class",  # Type-specific!
)
output_candidate_type = "ResidualCodePoint"
```

## التغييرات الرئيسية (Key Changes)

### 1. في `typed_codepoint_rules.py`
- حُذفت `TYPED_CODEPOINT_CLASSIFICATION` العامة
- أُضيفت 5 قواعد canonical محددة
- كل قاعدة تطلب wasf/illah خاصين بنوعها

### 2. في `typed_codepoint_adapter.py`
- أُضيفت دالة `select_rule_for_codepoint(codepoint: int) -> QiyasRule`
- لم تعد `build_request_for_classification` تنشئ قاعدة ديناميكية
- بدلاً من ذلك، تختار القاعدة المناسبة من القواعد الخمس الموجودة

### 3. في `rules/__init__.py`
- تم تحديث exports لتصدير القواعد الخمس الجديدة

### 4. في `test_typed_codepoint_classification.py`
- أُضيفت اختبارات للتأكد من أن كل قاعدة تطلب wasf/illah الخاصين بها
- **اختباران حرجان جديدان:**
  - `test_letter_rule_blocks_when_specific_letter_wasf_missing`
  - `test_haraka_rule_blocks_when_specific_haraka_wasf_missing`

## الاختبارات الحرجة (Critical Tests)

الاختبارات الحرجة تثبت أن `QiyasKernel` **يرفض** الطلب إذا كان الدليل يفتقد للوصف النوعي:

```python
def test_letter_rule_blocks_when_specific_letter_wasf_missing():
    # Build evidence WITHOUT wasf:is_arabic_letter
    proves = [
        "wasf:is_classifiable_codepoint:evidenced",  # Generic only
        "illah:belongs_to_letter_class:verified",
        # MISSING: wasf:is_arabic_letter!
    ]

    request = QiyasRequest(
        rule=LETTER_CODEPOINT_CLASSIFICATION,  # Requires is_arabic_letter
        evidence=evidence,
        ...
    )

    result = kernel.apply(request)

    # Should be BLOCKED, not accepted!
    assert len(result.accepted) == 0
    assert len(result.blocked) > 0
```

هذا يثبت أن النوع ليس مجرد قرار من adapter، بل هو **متطلب مفروض من القاعدة نفسها**.

## الفرق الجبري (Algebraic Difference)

### قبل PR #24 (غير صحيح):
```text
adapter decides LetterCodePoint
+ generic rule (no type-specific requirements)
+ evidence contains type-specific wasf/illah (extra, not required)
→ LetterCodePoint
```

النوع كان قرارًا خارجيًا من adapter.

### بعد PR #24 (صحيح):
```text
UnicodeCandidate
+ Rule(LetterCodePoint) that REQUIRES is_arabic_letter
+ Evidence proves is_arabic_letter
→ CandidateSet[LetterCodePoint]
```

النوع الآن **مطلوب من القاعدة نفسها**.

## النتائج (Results)

- ✅ 49 اختبارًا في `test_typed_codepoint_classification.py` (جميعها تنجح)
- ✅ 63 اختبارًا إجماليًا في `tests/qiyas_core/` (جميعها تنجح)
- ✅ النوع المحدد الآن مطلوب من القاعدة، لا من adapter
- ✅ QiyasKernel يحجب الطلب إذا غاب الوصف النوعي
- ✅ لا إنشاء قواعد ديناميكية
- ✅ 5 قواعد canonical واضحة وصريحة

## الخلاصة (Conclusion)

PR #24 أغلق الفجوة الدستورية الأخيرة في طبقة TypedCodePoint. الآن:

```text
Raw Unicode
→ UnicodeCandidate (PR #20)
→ TypedCodePoint (PR #23 + PR #24)
```

البرهان الجبري **كامل ومحكم**.

الخطوة التالية: بناء `HarakaFunctionCarrier` كأول طبقة وظيفية.
