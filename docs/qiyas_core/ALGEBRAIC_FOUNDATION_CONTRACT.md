# العقد التأسيسي للجبر: من الرمز إلى التركيب
# Algebraic Foundation Contract: From Symbol to Composition

## المبدأ الأساسي (Core Principle)

```
الحرف = أول هوية صوتية ممثلة كتابيًا ورقميًا
الحركة = أول وظيفة صوتية ممثلة كتابيًا ورقميًا
الموضع = شرط تعيين زمني/كتابي
الـ Slot = أول تركيب جبري لصوت صامت + وظيفة صائتة + موضع
```

## الوضع الحالي (Current State)

✅ **مكتمل (Completed)**:
```
Raw Unicode → UnicodeCandidate → TypedCodePoint
```

- PR #24: 5 قواعد canonical محددة النوع
- كل قاعدة تطلب `wasf`/`illah` خاصين بها
- البرهان الأساسي محكم

❌ **الناقص (Missing)**: البرهان من TypedCodePoint إلى Identity/Function/Position/Slot

---

## الفجوات الستة عشر (16 Foundation Gaps)

### المستوى الأول: المجال والاستنتاج (Domain & Inference)

#### 1. ControlledArabicVocalizedTextSpace
**الوضع**: غير موجود
**المطلوب**: فضاء السلسلة الكاملة، لا الرمز المفرد

```
𝔄₀ = ControlledArabicVocalizedTextSpace
   = Sequence[TypedCodePoint] with constraints

Constraints:
- هل الحركة لها حامل؟
- هل الشدة في موضع جائز؟
- هل التنوين طرفي؟
- هل هناك حرف بلا حركة؟
- هل هناك بقايا داخل النص؟
- هل الحدود محفوظة؟
```

**الناقص**:
- `TextSequenceValidator`
- `HarakaCarrierRule`
- `ShaddaPositionRule`
- `TanwinTerminalRule`
- `BoundaryPreservationRule`

#### 2. علاقة الاستنتاج (⊢ Inference Relation)
**الوضع**: نستخدم `operation() → CandidateSet`
**المطلوب**: علاقة استنتاج صريحة

```
Current (operational):
  classify(x) → CandidateSet

Required (inferential):
  Γ ⊢ x : Sort

Examples:
  Γ ⊢ c : UnicodeCandidate
  Γ ⊢ wasf:is_arabic_letter(c)
  Γ ⊢ illah:belongs_to_letter_class(c)
  ────────────────────────────────
  Γ ⊢ c : LetterCodePoint

  Γ ⊢ c : LetterCodePoint
  Γ ⊢ has_baa_unicode_identity(c)
  Γ ⊢ has_baa_script_identity(c)
  Γ ⊢ has_baa_sound_identity(c)
  Γ ⊢ has_baa_makhraj_sifat(c)
  ────────────────────────────────
  Γ ⊢ c : LetterIdentityCarrier(BAA)
```

**الناقص**:
- `InferenceContext` (Γ)
- `InferenceRule` registry
- `DerivationTrace`

---

### المستوى الثاني: الهوية والوظيفة (Identity & Function)

#### 3. LetterIdentityCarrier
**الوضع**: `LetterCodePoint` فقط (نوع عام)
**المطلوب**: هوية محددة (BAA, TAA, SEEN, ...)

```python
LetterIdentityCarrier(BAA) = {
    # Digital/Script Layer
    unicode_identity: "U+0628",
    script_identity: "ARABIC_LETTER_BAA",

    # Phonetic Layer (from PhoneticGroundingProfile)
    sound_identity: "VOICED_BILABIAL_STOP",
    makhraj_profile: {
        spatial_source: "BILABIAL",
        articulation_point: "LIPS_CLOSURE"
    },
    sifat_profile: {
        voicing: "VOICED",
        manner: "STOP",
        place: "BILABIAL"
    },

    # Algebraic Layer
    invalidating_differences: {
        "baa_vs_meem": "NASALITY_DIFF",
        "baa_vs_faa": "PLACE_DIFF",
        "baa_vs_taa": "VOICING_DIFF"
    },

    # Evidence/Proof
    evidence: EvidenceSet,
    rank: EvidenceRank.FORM,
    trace_ids: tuple[str, ...]
}
```

**الناقص**:
- `ArabicLetterIdentitySpace`
- `LetterIdentityRule`
- `MakhrajGeometry`
- `SifatGeometry`
- `PhonoDistinctionProfile`
- `InvalidatingDifferenceGeometry`

**الاختبارات المطلوبة**:
```python
test_baa_letter_codepoint_proves_baa_identity()
test_taa_letter_codepoint_proves_taa_identity()
test_seen_does_not_become_sheen()
test_baa_does_not_become_taa()
test_baa_vs_meem_invalidating_difference()
```

#### 4. HarakaFunctionCarrier
**الوضع**: `HarakaCodePoint` فقط (نوع عام)
**المطلوب**: وظيفة صوتية محددة

```python
HarakaFunctionCarrier(FATHA) = {
    # Digital/Script Layer
    unicode_identity: "U+064E",
    script_mark_identity: "ARABIC_FATHA",

    # Phonetic Layer
    vocalic_function: "OPENING_FUNCTION",
    acoustic_effect: "SHORT_LOW_FRONT_VOWEL",
    energy_profile: {
        duration: "SHORT",
        aperture: "OPEN",
        tongue_position: "LOW_FRONT"
    },

    # Constitutional Boundaries
    forbidden_outputs: {
        "CaseEffect",  # فتحة ≠ نصب
        "I'rab",
        "Hukm"
    }
}
```

**القانون الحاسم**:
```
HarakaFunctionCarrier ⊬ CaseEffect
HarakaFunctionCarrier ⊬ I'rab
HarakaFunctionCarrier ⊬ Hukm
```

**الناقص**:
- `ArabicHarakaFunctionSpace`
- `HarakaFunctionRule`
- `VocalicEnergyProfile`
- `HarakaInvalidatingDifferences`

**الاختبارات المطلوبة**:
```python
test_fatha_haraka_proves_fatha_function()
test_damma_haraka_proves_damma_function()
test_kasra_haraka_proves_kasra_function()
test_sukun_proves_closure_function()
test_shadda_proves_compression_function()
test_fatha_does_not_become_damma()
test_haraka_function_forbids_case_effect()
```

---

### المستوى الثالث: التركيب (Composition)

#### 5. PositionCarrier
**الوضع**: غير موجود
**المطلوب**: موضع كحامل، لا كرقم

```python
PositionCarrier = {
    # Sequence Position
    index: int,

    # Contextual Position
    position_type: {
        "INITIAL" | "MEDIAL" | "FINAL" | "ISOLATED"
    },

    # Structural Position
    within_word: bool,
    at_boundary: bool,

    # Functional Position
    accepts_haraka: bool,
    accepts_shadda: bool,
    accepts_tanwin: bool,
    waqf_eligible: bool,
    wasl_eligible: bool
}
```

**الناقص**:
- `PositionCarrier` type
- `PositionRule`
- `PositionCompatibilityCheck`

#### 6. SlotGeometry
**الوضع**: غير موجود
**المطلوب**: أول تركيب جبري

```
Γ ⊢ l : LetterIdentityCarrier
Γ ⊢ h : HarakaFunctionCarrier
Γ ⊢ p : PositionCarrier
Γ ⊢ Compatible(l,h,p)
Γ ⊢ PreserveIdentity(l,h,p)
────────────────────────────────
Γ ⊢ Slot(l,h,p)
```

**البنية الفيزيائية/الصوتية**:
```
Slot(بَ) = {
    consonantal_identity: LetterIdentity(BAA),
    vocalic_function: HarakaFunction(FATHA_OPENING),
    position: PositionCarrier,

    acoustic_sequence: [
        BILABIAL_STOP_BURST,
        SHORT_OPEN_VOWEL
    ],

    energy_profile: {
        total_energy: onset_energy + nucleus_energy,
        distribution: CONSONANT_DOMINANT
    }
}
```

**الناقص**:
- `SlotCandidate`
- `SlotCompatibilityRule`
- `SlotIdentityPreservation`
- `SlotResidualPolicy`
- `SlotForbiddenOutputs`

**الاختبارات المطلوبة**:
```python
test_slot_requires_letter_identity()
test_slot_requires_haraka_function()
test_slot_requires_position()
test_slot_compatible_baa_fatha()
test_slot_preserves_identity()
test_slot_forbids_syllable_before_adjacency()
```

---

### المستوى الرابع: التأسيس الفيزيائي (Phonetic Grounding)

#### 7. PhoneticGroundingProfile
**الوضع**: غير موجود
**المطلوب**: ربط الجبر بالواقع الفيزيائي/الصوتي

```python
@dataclass
class PhoneticGroundingProfile:
    """Physical/phonetic grounding for algebraic entities"""
    sound_event_type: SoundEventType
    makhraj: MakhrajProfile
    sifat: SifatProfile
    energy: EnergyProfile
    duration: DurationProfile
```

**MakhrajGeometry**:
```python
MakhrajSpace = {
    BILABIAL: {ب، م، و},
    DENTAL: {ث، ذ، ظ},
    ALVEOLAR: {ت، د، ط، ض، ل، ن، ر},
    PALATAL: {ج، ش، ي},
    VELAR: {ك، غ، خ},
    UVULAR: {ق},
    PHARYNGEAL: {ح، ع},
    GLOTTAL: {ء، هـ}
}
```

**SifatGeometry**:
```python
SifatProfile = {
    voicing: {VOICED, VOICELESS},
    manner: {STOP, FRICATIVE, NASAL, LIQUID, GLIDE},
    airflow: {ORAL, NASAL},
    duration: {SHORT, LONG, GEMINATED},
    emphasis: {PLAIN, EMPHATIC}
}
```

**EnergyTracePreservation**:
```
∀ sound event s:
  if transformed(s) then ∃ trace(s) in output

Examples:
- حذف(ن) → deletion_trace(ن) preserved
- إدغام(ن+ر→رّ) → assimilation_trace(ن) + gemination(ر)
- إبدال(و→ي) → substitution_trace(و) + output(ي)
```

**الناقص**:
- `PhoneticGroundingProfile`
- `SoundEventProfile`
- `MakhrajProfile`
- `SifatProfile`
- `EnergyProfile`
- `EnergyTracePreservation` policy

---

### المستوى الخامس: الفصل بين القابلية والتفعيل (Capability vs Activation)

#### 8. CapabilitySet Algebra
**الوضع**: غير موجود
**المطلوب**: فصل Identity عن Capability عن Activation

```
LetterIdentityCarrier(BAA)
  → CapabilitySet{Stem, Particle, ...}
    → SlotEligibility
      → ContextualActivation
```

**القانون**:
```
لا يجوز:
  LetterIdentityCarrier → Weak (مباشرة)
  LetterIdentityCarrier → Extra (مباشرة)

الصحيح:
  LetterIdentityCarrier → CapabilitySet
  CapabilitySet → activation conditions
  conditions met → activated capability
```

**CapabilitySet Structure**:
```python
CapabilitySet(letter) = {
    StemRadicalCapability?,
    WeakCapability?,
    MaddCapability?,
    ExtraCapability?,
    AffixCapability?,
    BuiltParticleCapability?,
    AssimilationCapability?,
    DeletionCapability?,
    SubstitutionCapability?
}
```

**الناقص**:
- `CapabilitySetAlgebra`
- `CapabilityCandidate`
- `CapabilityEvidence`
- `ActivationBoundary`

---

### المستوى السادس: القوانين الشكلية (Formal Laws)

#### 9. Economy Function
**الوضع**: مذكور لفظيًا
**المطلوب**: دالة رسمية قابلة للاختبار

```
Economy(x, P) ⇔
  ¬∃y < x : Licensed(y, P) ∧ EquivalentPurpose(y, x, P)

أي: لا توجد بنية أصغر مرخصة تحقق نفس الغرض
```

**الناقص**:
- `Order relation <`
- `Purpose P`
- `EquivalentPurpose predicate`

#### 10. MinimalSufficiency Function
**الوضع**: مذكور لفظيًا
**المطلوب**: دالة رسمية

```
MSL(x, P) ⇔
  Licensed(x, P) ∧ Sufficient(x, P) ∧ ∀y < x : ¬Sufficient(y, P)

أي: x مرخص وكافٍ، وكل ما هو أصغر منه غير كافٍ
```

**الناقص**:
- `Sufficient predicate`
- `License predicate`

---

### المستوى السابع: البنية التكرارية (Recursive Structure)

#### 11. RecursiveProofContract
**الوضع**: كل طبقة اختراع مستقل
**المطلوب**: قالب تكراري موحد

```python
RecursiveProofContract = {
    inputs: Input types,
    effective_wasf: Required wasf claims,
    jami_illah: Required illah claims,
    invalidating_فارق: Blocking differences,
    evidence: EvidenceSet,
    identity_preservation: Identity rules,
    economy: Economy check,
    minimal_sufficiency: MSL check,
    forbidden_outputs: Output boundaries,
    trace: Trace policy,
    output: CandidateSet[NewCarrier]
}
```

**الناقص**:
- `RecursiveProofContract` interface
- `RecursiveProofEngine`
- Layer-specific instantiations

---

### المستوى الثامن: الحدود الدستورية (Constitutional Boundaries)

#### 12. ForbiddenOutputRegistry
**الوضع**: موجود لكل طبقة بشكل مبعثر
**المطلوب**: registry مركزي مع اختبارات

```python
FORBIDDEN_OUTPUT_REGISTRY = {
    "TypedCodePoint": {
        "LetterIdentityCarrier",
        "HarakaFunctionCarrier",
        "SlotCandidate",
        ...
    },
    "LetterIdentityCarrier": {
        "RootCandidate",
        "WeightCandidate",
        "MeaningCandidate",
        "HukmCandidate"
    },
    "HarakaFunctionCarrier": {
        "CaseEffect",
        "I'rab",
        "Hukm"
    },
    "SlotCandidate": {
        "SyllableCandidate",  # before adjacency
        "MeaningCandidate"
    },
    "SyllableCandidate": {
        "WeightCandidate",  # before BuildClosure
        "MeaningCandidate"
    }
}
```

**الاختبارات المطلوبة**:
```python
test_letter_identity_forbids_weight()
test_haraka_function_forbids_case_effect()
test_slot_forbids_meaning()
test_syllable_forbids_weight_without_build()
```

---

### المستوى التاسع: البرهان الشكلي (Formal Proof)

#### 13. Soundness Theorem
**الوضع**: غير موجود
**المطلوب**: مبرهنة صحة

```
Soundness:
  If Γ ⊢ x : S, then M ⊨ x : S

أي: إذا استُنتج x من النوع S،
     فإن x مرخص في النموذج M

Example:
  If Γ ⊢ LetterIdentityCarrier(BAA)
  Then:
    - has Unicode identity U+0628
    - has script identity
    - has sound identity
    - has makhraj/sifat profile
    - has invalidating differences
    - preserves identity
```

**الناقص**:
- `Model M` definition
- `Satisfaction relation ⊨`
- Soundness proof per layer

#### 14. Relative Completeness
**الوضع**: غير موجود
**المطلوب**: اكتمال نسبي داخل مجال معلن

```
DeclaredDomain₀ = {
    Arabic letters: 28 core letters
    Core harakat: fatha, damma, kasra, sukun, shadda, tanwin
    Boundaries: space, newline
    Punctuation: Arabic punctuation marks
}

RelativeCompleteness(DeclaredDomain₀, Rules R):
  ∀ licensed case c ∈ DeclaredDomain₀:
    ∃ derivation or explained residual
```

**الناقص**:
- `DeclaredDomain` specification
- Coverage tests
- Residual policy

---

## خريطة الطريق (Roadmap)

### المرحلة 1: الحد الأدنى التأسيسي ⭐⭐⭐
```
TypedCodePoint → LetterIdentityCarrier → HarakaFunctionCarrier
→ PositionCarrier → SlotCandidate
```

**الأولوية القصوى**:
1. ✅ PR #24: TypedCodePoint rules (مكتمل)
2. ⏳ LetterIdentityCarrier + MakhrajGeometry + SifatGeometry
3. ⏳ HarakaFunctionCarrier + VocalicEnergyProfile
4. ⏳ PositionCarrier
5. ⏳ SlotGeometry

### المرحلة 2: البنية الشكلية
- Economy/MSL functions
- RecursiveProofContract
- ForbiddenOutputRegistry

### المرحلة 3: البرهان الرياضي
- Inference relation (⊢)
- Soundness theorem
- Relative completeness

### المرحلة 4: الطبقات اللاحقة
- SyllableGeometry
- BuildClosureGeometry
- WeightGeometry
- Mabni/Mu'rab
- Jamid/Mushtaq

---

## القوانين التأسيسية (Foundation Laws)

### 1. قانون حفظ الطاقة الجبري
```
∀ sound event s ∈ System:
  if transformed(s) then ∃ trace(s) in output
```

### 2. قانون الفصل بين الطبقات
```
Layer[n] ⊬ Layer[n+2]
```
لا طبقة تقفز فوق الطبقة التالية مباشرة

### 3. قانون الحد الأدنى
```
MSL(x, P) ⇔ Licensed(x, P) ∧ Sufficient(x, P) ∧ ∀y < x : ¬Sufficient(y, P)
```

### 4. قانون الاقتصاد
```
Economy(x, P) ⇔ ¬∃y < x : Licensed(y, P) ∧ EquivalentPurpose(y, x, P)
```

### 5. قانون الممنوعات
```
∀ layer L, ∀ output o:
  if o ∈ ForbiddenOutputs(L) then L ⊬ o
```

### 6. قانون حفظ الهوية
```
∀ transformation T(x → y):
  identity(x) ⊆ trace(y)
```

### 7. قانون الفصل بين القابلية والتفعيل
```
Identity → Capability → Eligibility → Activation
لا قفز من Identity إلى Activation مباشرة
```

---

## الخلاصة الدستورية (Constitutional Summary)

### ✅ ما اكتمل:
```
Raw Unicode → UnicodeCandidate → TypedCodePoint
```
- 5 قواعد canonical
- برهان محكم بـ wasf/illah نوعيين
- اختبارات حجب عند غياب الوصف النوعي

### ❌ ما ينقص لاكتمال التأسيس:
1. ControlledArabicVocalizedTextSpace
2. علاقة الاستنتاج (⊢)
3. LetterIdentityCarrier
4. HarakaFunctionCarrier
5. PositionCarrier
6. SlotGeometry
7. PhoneticGroundingProfile
8. MakhrajGeometry + SifatGeometry
9. CapabilitySet Algebra
10. Economy/MSL functions
11. RecursiveProofContract
12. ForbiddenOutputRegistry
13. Soundness theorem
14. Relative completeness
15. Test matrix
16. Inference rules

### 🎯 الهدف النهائي للتأسيس:
```
إذا وصلنا إلى:
  LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier + SlotCandidate

مع:
  - CandidateSet مبرهن
  - evidence/rank/residuals/trace محفوظة
  - forbidden outputs مفروضة
  - identity preservation مضمونة

فهنا نقول: تأسيس الجبر اكتمل
```

### 📋 التوصية الفورية:
**لا نبدأ أي طبقة جديدة حتى نوثق هذا العقد التأسيسي ونلتزم به**

هذا الملف = الدستور الجبري
كل PR لاحق يجب أن يُراجع على هذا الدستور

---

## المراجع (References)

- PR #24: TypedCodePoint type-specific rules
- docs/qiyas_core/PR_24_SUMMARY.md
- docs/qiyas_core/LAYER_CONTRACT_CONSTITUTION.md (if exists)

---

**تاريخ الإنشاء**: 2026-06-01
**الحالة**: Constitutional Specification
**الأولوية**: CRITICAL - Foundation Contract
