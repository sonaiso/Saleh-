# PR #23: Hardening TypedCodePoint Algebraic Proof

## الملخص التنفيذي (Executive Summary)

PR #23 يقوي البرهان الجبري لطبقة `TypedCodePointClassification` التي أُنشئت في PR #20. بينما PR #20 أنشأ الجسر الأولي من `UnicodeCandidate` إلى `TypedCodePoint`، كان التصنيف النوعي (Letter/Haraka/Boundary/Punctuation/Residual) يُحسم **خارج** `QiyasKernel` ثم يُحقن كـ `output_candidate_type` ديناميكي.

PR #23 يُصلح هذه الفجوة الجبرية الدقيقة بجعل التصنيف النوعي **مُبرهنًا داخل النواة** عبر wasf/illah خاصين لكل نوع.

## المشكلة الأصلية (Original Problem)

في PR #20، كان الدليل يثبت فقط:
```
wasf:is_classifiable_codepoint:evidenced
illah:belongs_to_typed_domain:verified
```

ثم يتحدد النوع (Letter/Haraka/...) في adapter:
```python
candidate_type, wasf, illah = classify_codepoint(codepoint)
# ثم يُحقن في output_candidate_type
```

هذا يعني:
- النواة تثبت أن الرمز "قابل للتصنيف typed"
- لكنها **لا تثبت** أنه Letter لا Haraka
- النوع يُقرر خارج kernel، ثم يُمرَّر لها كمخرج ديناميكي

## الحل (Solution)

### 1. إضافة wasf/illah خاصين للدليل

الآن `EvidenceSet` يحتوي على:
```python
proves = [
    "asl:established",
    "far:determined",
    "wasf:is_classifiable_codepoint:evidenced",      # عام
    f"wasf:{wasf}:evidenced",                        # خاص: is_arabic_letter
    "illah:belongs_to_typed_domain:verified",        # عام
    f"illah:{illah}:verified",                       # خاص: belongs_to_letter_class
    "wadi:sabab:established",
    ...
]
```

الأنواع الخاصة:
- `wasf:is_arabic_letter:evidenced` + `illah:belongs_to_letter_class:verified`
- `wasf:is_arabic_haraka:evidenced` + `illah:belongs_to_haraka_class:verified`
- `wasf:is_whitespace_boundary:evidenced` + `illah:belongs_to_boundary_class:verified`
- `wasf:is_arabic_punctuation:evidenced` + `illah:belongs_to_punctuation_class:verified`
- `wasf:is_unclassified_codepoint:evidenced` + `illah:belongs_to_residual_class:verified`

### 2. إضافة invalidating_differences لبرهان الاتحاد المنفصل

```python
invalidating_differences=(
    "multiple_classes_claimed",
    "ambiguous_classification",
    "letter_haraka_overlap",
    "boundary_punctuation_overlap",
)
```

هذه تضمن جبريًا أن disjointness ليس فقط بترتيب if/elif، بل قانون داخل القاعدة.

### 3. توثيق `classify_codepoint()` كاختبار فقط

```python
"""
**WARNING: This is a testing/convenience method only.**

**NOT FOR PRODUCTION USE.** This method bypasses the constitutional
production path (UnicodeLayerAdapter.process_codepoint →
TypedCodePointLayerAdapter.classify_unicode_candidate).
...
"""
```

المسار الإنتاجي الدستوري:
```
UnicodeLayerAdapter.process_codepoint()
  → UnicodeCandidate (accepted, مُبرهن بعضوية Arabic Unicode)
  → TypedCodePointLayerAdapter.classify_unicode_candidate()
  → TypedCodePoint (مُصنف بوصف وعلة خاصين)
```

### 4. اختبارات شاملة

أُضيفت 7 اختبارات جديدة:
1. `test_letter_classification_proves_type_specific_wasf` — يثبت أن `LetterCodePoint` يحمل `wasf:is_arabic_letter:evidenced`
2. `test_haraka_classification_proves_type_specific_illah` — يثبت أن `HarakaCodePoint` يحمل `illah:belongs_to_haraka_class:verified`
3. `test_boundary_classification_proves_type_specific_wasf_and_illah` — كلاهما
4. `test_classification_uses_kernel_apply_verifiably` — mock/spy يثبت أن `kernel.apply()` يُستدعى فعليًا
5. `test_typed_codepoint_rule_has_disjoint_union_invalidations` — `invalidating_differences` موجودة
6. `test_letter_candidate_has_no_forbidden_output_flags` — لا أعلام ممنوعة
7. `test_all_classification_types_prove_specific_evidence` — الخمسة أنواع كلها

النتيجة: **37/37 tests pass**

### 5. تحديث الدستور

`docs/qiyas_core/LAYER_CONTRACT_CONSTITUTION.md` § 8.7.2 الآن يوثّق:
- الوصف المؤثر الخاص (PR #23)
- العلة الخاصة (PR #23)
- `invalidating_differences` (PR #23)
- القيد الدستوري على `classify_codepoint()` (PR #23)

## الحكم النهائي (Final Verdict)

### قبل PR #23:
```
التصنيف يُحسم خارج QiyasKernel،
النواة تقبل النتيجة كـ output_candidate_type ديناميكي.
```

### بعد PR #23:
```
التصنيف مُبرهن داخل QiyasKernel،
النوع ليس فقط مخرجًا ديناميكيًا، بل مُثبت بوصف وعلة خاصين في EvidenceSet.
```

الفجوة الجبرية الدقيقة **مُغلقة**.

PR #23 جاهز للمراجعة والدمج.

---

## الملفات المُعدَّلة (Modified Files)

1. `src/qiyas_core/typed_codepoint_adapter.py`
   - أضاف wasf/illah خاصين للدليل
   - وثّق `classify_codepoint()` كاختبار فقط

2. `src/qiyas_core/rules/typed_codepoint_rules.py`
   - أضاف `invalidating_differences` للبرهان الجبري

3. `tests/qiyas_core/test_typed_codepoint_classification.py`
   - أضاف 7 اختبارات جديدة (PR #23)
   - حدّث docstring

4. `docs/qiyas_core/LAYER_CONTRACT_CONSTITUTION.md`
   - حدّث § 8.7.2 بتوثيق PR #23

## الخطوة التالية (Next Step)

**لا تنتقل إلى `HarakaFunctionCarrier` بعد.**

الخطوة التالية حسب الحاجة:
- إما تقوية طبقة Unicode (ControlledArabicTextCodePointMembership)
- أو البدء في طبقات الجبر العربي (Jamid, Mushtaqq, Wazn, ...)
- أو معالجة مشكلة boundary/space vs Arabic Unicode block

ينتظر القرار الدستوري من @sonaiso.
