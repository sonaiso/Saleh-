# LAYER_CONTRACT_CONSTITUTION

> **PR #19 — Documentation only. Contract only. No implementation.**
>
> هذا الملف يُعرِّف **عقد الطبقات الناقصة والقفزات الممنوعة** في سلسلة قياس
> (Qiyas). لا يحتوي كودًا، ولا اختبارات، ولا تعديلات على `src/` أو
> `experimental/` أو `tests/` أو `.github/workflows/`. التنفيذ يأتي في PRs
> لاحقة، كلٌّ منها يفتح بوابة واحدة فقط بحدّ أدنى كافٍ.

---

## 0. الموقع الدستوري

| المرجع                                       | الوظيفة                                       |
| -------------------------------------------- | --------------------------------------------- |
| `RESET_CONSTITUTION.md` (PR #15)             | الدستور الأصلي وترتيب البناء                  |
| `AUDIT_AFTER_RESET_CONSTITUTION.md` (PR #16) | تدقيق ما بعد التصفير                          |
| `PATH_A_ISOLATION_RECORD.md` (PR #17)        | عزل المواد التجريبية                          |
| `CANONICAL_KERNEL_BOUNDARY_VERIFICATION.md` (PR #18) | تحقق حدّ النواة القانونية              |
| **`LAYER_CONTRACT_CONSTITUTION.md` (PR #19)**| **عقد الطبقات والبوابات — هذا الملف**         |
| PR #20+                                      | تنفيذ بوابة واحدة لكل PR بحدّ أدنى كافٍ       |

المبادئ الحاكمة الموروثة:

```
العقد قبل الطبقة.
والبوابة قبل التنفيذ.
والدستور قبل الاختبار.
```

ملاحظة: "الدستور قبل الاختبار" لا يعني أن الجبر بلا اختبار؛ بل يعني أن هذا
العقد يحدد **ما الذي سيُختبر** لاحقًا في كل PR تنفيذي.

---

## 1. النسخة المصححة النهائية للسلسلة (Canonical Chain — Final)

> هذه هي الصياغة الحاكمة لكامل سلسلة قياس بعد إغلاق القفزات. كل جملة في هذه
> الصياغة تمنع قفزة محددة، وكل بند منها له بوابة مقابلة في القسم 7.

```text
الجامد لا يثبت الموجود مباشرة،
بل يفتح مرشح موجود داخل نوع وجود ومجال ورتبة وبقايا.

والمشتق لا يعطي معرفة نهائية،
بل يفتح مرشح معرفة عن الموجود من جهة حدث أو صفة أو علاقة أو دور اشتقاقي.

والحد الأدنى الصوتي/المقطعي لا يثبت الاستعمال،
بل يرخّص إمكان المادة قبل فحص السماع أو المعجم أو المجال.

والوزن لا يعمل على كل لفظ،
بل يحوّل مادة مرخّصة، إذا سلكت مسار الجذر والوزن، إلى صيغة مرخصة.

والصيغة لا تعطي معنى،
بل تفتح مدلولًا لفظيًا مرشحًا.

والوضع، بنوعه ومجاله وشاهده وحدود استعماله،
يرخّص معنى معجميًا أو عرفيًا أو اصطلاحيًا.

والدلالة لا تكون واحدة،
بل تحدد نوع العلاقة بين الدال والمدلول: مطابقة أو تضمن أو التزام أو غيرها.

والإحالة لا تثبت المرجع،
بل تفتح مجال مرجع تضبطه القرائن والسياق.

والنسبة لا تنتج إفادة إلا إذا اكتملت شروط الإسناد أو الربط أو التقييد
بحسب نوع التركيب.

والقوة الخطابية تحدد هيئة الإفادة، لا حكمها النهائي.

والدليل المناسب، داخل مجال صحيح، مع الشروط وانتفاء الموانع،
ينتج حكمًا ذا رتبة وبقايا.

والحكم لا ينزل على واقعة إلا بتحقيق المناط.

والروابط الضعيفة تولّد فرضيات منخفضة الرتبة، ولا تنتج أحكامًا.

والروابط القوية لا ترخّص إلا انتقالًا محددًا داخل مجالها وطبقتها،
ولا تعبر إلى مجال آخر إلا ببوابة نقل.
```

---

## 2. القانون الحاكم (Governing Law)

### 2.1 الهيكل المعياري لكل طبقة

كل طبقة قياس، حالية أو مستقبلية، **يجب** أن تستوفي السلسلة التالية:

```
Candidate → Gate → Evidence → Domain → Rank → Residuals → Trace
مرشح   → بوابة → دليل   → مجال   → رتبة → بقايا   → أثر
```

أي:

1. لا تبدأ الطبقة بمخرج جاهز، بل بـ **Candidate** (مرشح).
2. لا يتحول المرشح إلى مخرج مرخّص إلا عبر **Gate** (بوابة) معرَّفة.
3. لا تفتح البوابة إلا بـ **Evidence** (دليل) من نوع متفق عليه.
4. الدليل لا يعمل خارج **Domain** (مجاله).
5. كل مخرج له **Rank** (رتبة) صريحة:
   `CANDIDATE` < `LICENSED` < `PROVEN` (وما يلحق بها داخل الطبقة).
6. كل قرار يَخلِّف **Residuals** (بقايا) لا يجوز إخفاؤها.
7. كل انتقال يحفظ **Trace** (أثرًا) يربط المخرج بمدخلاته وأدلته وبوابته.

### 2.2 المحظورات الستة (Six Prohibitions)

```
1. لا طبقة تنتج مخرج الطبقة التالية.
2. ولا مرشح يتحول إلى حكم.
3. ولا رابط يترقى بلا دليل.
4. ولا دليل يعمل خارج مجاله.
5. ولا تنزيل بلا تحقيق مناط.
6. ولا فرضية تتحول إلى معرفة إلا بعد اختبار.
```

أي خرق لهذه المحظورات في أي طبقة لاحقة يُعدّ خرقًا دستوريًا، ويوجب رفض الـPR
الذي يحتويه، بغض النظر عن جودة الكود.

### 2.3 علاقة هذا القانون بالنواة القائمة

النواة الحالية (`src/qiyas_core/kernel.py`) تطبّق جزءًا من هذا القانون
بالفعل عبر:

- `fariq:{difference}:present` — لإثبات الفروق المُبطلة (شكل مبكر من
  enforcement للبوابات).
- `defer:{reason}:present` — لتحويل الحالات غير المكتملة إلى `DEFERRED`
  بدلًا من ترقيتها إلى نتيجة (شكل مبكر من **Residuals**).
- `forbidden_outputs` في قواعد الطبقات (مثل `PhonoFunctionalUnit`) — تطبيق
  مباشر للمحظور الأول.

هذا العقد **لا يغيّر** هذه الآليات، بل يُعمِّمها ويفرض أن كل بوابة لاحقة
تتبعها.

---

## 3. تعريف المدلول اللفظي (VerbalSignified)

```
المدلول اللفظي = المرشح البنيوي الذي تفتحه الصيغة من جهة تركيبها وصورتها
ووظيفتها الصرفية أو البنائية، قبل ثبوت الوضع المعجمي أو العرفي أو
الاصطلاحي، وقبل تعيين المراد السياقي أو الحكم.
```

ينتج عن ذلك:

```
الصيغة → مدلول لفظي مرشح
لا   → معنى نهائي
لا   → مراد
لا   → حكم
```

مثال توضيحي (للعقد فقط، لا يُنفَّذ هنا):

- صيغة "فاعل" تفتح مدلولًا لفظيًا مرشحًا (جهة فاعلية / نسبة إلى حدث / صاحب
  فعل)، ولا تثبت معنى معجميًا نهائيًا ("كاتب" قد تعني الحرفة، أو الفعل
  الواقع، أو النسبة، أو الوظيفة).
- إثبات أيٍّ من هذه يقع في طبقات لاحقة عبر بواباتها (الوضع، الدلالة،
  الإحالة، السياق).

---

## 4. تعريف قوة الرابط (Link Strength)

### 4.1 القوة ليست كثرة الشواهد

```
قوة الرابط = محصلة دليل مرخّص داخل مجال،
            + انخفاض البقايا،
            + غياب مانع قاطع،
            + حفظ الأثر،
            + عدم تجاوز الطبقة.
```

### 4.2 شروط الرابط القوي (StrongLink — Seven Conditions)

```
StrongLink iff:
  1. DomainValid               (الدليل داخل مجاله)
  2. EvidenceSufficient        (كفاية الدليل)
  3. NoBlockingResidual        (لا بقايا مانعة)
  4. CounterEvidenceResolved   (الأدلة المعارضة حُلّت)
  5. TracePreserved            (الأثر محفوظ)
  6. Rank ≥ LICENSED           (الرتبة لا تقل عن مرخّصة)
  7. ScopeLimitedToLayer       (لا يتجاوز طبقته)
```

### 4.3 الرابط الضعيف (WeakLink)

```
WeakLink = HypothesisGenerator only
```

أي:

- يولّد **فرضية** فقط (rank = `CANDIDATE`، أو أدنى).
- **لا** يرخّص وضعًا.
- **لا** ينتج حكمًا.
- **لا** يرخّص تنزيلًا.
- **لا** ينتقل خارج طبقته.

مصادر الروابط الضعيفة لا تنحصر في التضمن والالتزام؛ تشمل أيضًا: تشابه وزني،
تشابه جذري، تقارب سياقي، قياس بعيد، استعارة، نقل اصطلاحي محتمل، رابط
تاريخي، رابط استعمالي نادر، رابط شبكي بين مجالين. كل هذه — حين تُعالَج —
تمر عبر `HypothesisGate` المعرَّفة في القسم 7.13.

---

## 5. جدول البوابات الأربع عشرة (14 Gates Overview)

| #  | الطبقة                       | البوابة المطلوبة          | القفزة الممنوعة                              |
| -- | ---------------------------- | ------------------------- | -------------------------------------------- |
| 1  | الجامد (Jamid)               | `RealityTypeGate`         | جامد → موجود خارجي قطعي                      |
| 2  | المشتق (Mushtaqq)            | `DerivationalRoleGate`    | مشتق → معرفة محددة                           |
| 3  | الصوتي/المقطعي (PhonoSyll.)  | `LexicalAttestationGate`  | ممكن صوتيًا → مستعمل عربيًا                  |
| 4  | الوزن (Wazn)                 | `LexicalPathGate`         | كل لفظ → جذر/وزن                             |
| 5  | الصيغة (Form)                | `VerbalSignifiedGate`     | مدلول لفظي → معنى معجمي نهائي                |
| 6  | الوضع (Wadh)                 | `WadhScopeGate`           | شاهد واحد → وضع عام                          |
| 7  | الدلالة (Dalalah)            | `DalalahTypeGate`         | علاقة دلالية → نوع علاقة محدد                |
| 8  | الإحالة + السياق (Reference) | `ReferenceResolutionGate` | ضمير/إشارة → مرجع نهائي                      |
| 9  | النسبة (Nisbah)              | `IfadahClosureGate`       | تركيب صحيح → إفادة تامة                      |
| 10 | القوة الخطابية (SpeechForce) | `DomainNormGate`          | أمر → وجوب، نهي → تحريم، خبر → صدق           |
| 11 | الحكم (Hukm)                 | `EvidenceDomainGate`      | حكم لغوي → حكم واقعي/شرعي                    |
| 12 | المناط (Manat)               | `TahqiqAlManatGate`       | مناط نظري → تنزيل على واقعة                  |
| 13 | الروابط الضعيفة (WeakLinks)  | `HypothesisGate`          | رابط ضعيف → حكم                              |
| 14 | الروابط القوية (StrongLinks) | `DomainTransferGuard`     | رابط قوي في مجال → نتيجة في مجال آخر         |

كل بوابة من هذه الأربع عشرة تُفصَّل في القسم 7 بقالب موحَّد، وتُنفَّذ كل
واحدة منها في PR مستقل لاحقًا (PR #20 وما بعده).

---

## 6. القالب الموحَّد لكل بوابة (Per-Gate Contract Template)

كل بوابة من البوابات الأربع عشرة في القسم 7 تتبع هذا القالب حرفيًا:

```
1. Input Candidate       — مرشح/مرشحات الإدخال (نوع candidate من طبقة سابقة)
2. Gate                  — اسم البوابة الرسمي + شرط فتحها
3. Output Candidate      — مرشح الإخراج (لا مخرج نهائي، إلا داخل الطبقة)
4. Forbidden Jump        — القفزة الممنوعة التي تغلقها هذه البوابة
5. Forbidden Outputs     — المخرجات التي لا يجوز للقواعد إنتاجها
6. Required Evidence     — أنواع الأدلة المطلوبة لفتح البوابة
7. Domain                — المجال/المجالات المسموح بها للدليل
8. Rank Policy           — كيف تُمنح الرتبة (CANDIDATE / LICENSED / PROVEN)
9. Residuals             — البقايا المعروفة وكيف تُمثَّل (defer/fariq/…)
10. Trace                — ما يجب حفظه للربط بالمدخلات والأدلة
```

ملاحظة تنفيذية مُلزِمة لكل PR مستقبلي يفتح بوابة:

- يجب أن تُضاف `forbidden_outputs` صراحة في قاعدة الطبقة (بنفس النمط الموجود
  في `src/qiyas_core/rules/*.py`).
- يجب أن تُترجَم البقايا إلى ادعاءات `defer:{reason}:present` أو
  `fariq:{difference}:present` بما يطابق ما تقبله النواة.
- يجب أن تُحفظ `Trace` في بنية المرشح المُخرَج.

---

## 7. عقود البوابات الأربع عشرة (The 14 Gate Contracts)

### 7.1 RealityTypeGate — بوابة نوع الوجود (الجامد)

1. **Input Candidate**: `JamidCandidate` (لفظ جامد مرشَّح، خارج من طبقة سابقة
   تثبت أنه ليس مشتقًّا ولا مبنى وظيفيًّا).
2. **Gate**: `RealityTypeGate` — تُفتح حين تتوفر دلائل تصنيف الموجود إلى أحد
   الأنواع: خارجي، ذهني، لفظي، اصطلاحي، مجازي، حكمي، تاريخي/أثري.
3. **Output Candidate**: `NamedEntityCandidate` ← `RealityTypeCandidate` ←
   `DomainScopedExistenceCandidate` (سلسلة داخل الطبقة، كلها مرشحات).
4. **Forbidden Jump**: جامد → موجود خارجي قطعي.
5. **Forbidden Outputs**: `RealityClaim`, `MeaningCandidate`, `HukmCandidate`,
   `FinalMeaning`, `DalCandidate`, `WordCandidate`.
6. **Required Evidence**: شواهد التصنيف الوجودي (سياقي/معجمي/عرفي/اصطلاحي).
7. **Domain**: مجالات الوجود السبعة المذكورة أعلاه؛ لا يُخلَط بينها.
8. **Rank Policy**:
   - `CANDIDATE` عند مجرد فتح المرشح.
   - `LICENSED` عند تطابق المجال + شاهد واحد قاطع.
   - لا يصل إلى `PROVEN` داخل هذه الطبقة وحدها.
9. **Residuals**:
   - `defer:reality_type_ambiguous:present` (احتمالان أو أكثر).
   - `defer:domain_unresolved:present` (لا يُعرف مجال الوجود).
   - `fariq:reality_type_conflict:present` (شواهد متعارضة).
10. **Trace**: `{jamid_token, candidate_reality_types[], chosen_domain, supporting_evidence_refs[]}`.

---

### 7.2 DerivationalRoleGate — بوابة الدور الاشتقاقي (المشتق)

1. **Input Candidate**: `MushtaqqCandidate` (لفظ مشتق مرشَّح، مع جذر مرشَّح).
2. **Gate**: `DerivationalRoleGate` — تُفتح حين يتعيَّن دور اشتقاقي محدد
   (فاعل، مفعول، مصدر، صفة مشبهة، اسم آلة، اسم مكان، اسم زمان، مبالغة،
   نسبة، حرفة، حالة، قابلية).
3. **Output Candidate**: `DerivationalRoleCandidate` ← `Event/Property/RelationCandidate`
   ← `ContextualRoleResolutionCandidate`.
4. **Forbidden Jump**: مشتق → معرفة معجمية محددة.
5. **Forbidden Outputs**: `MeaningCandidate`, `FinalMeaning`, `HukmCandidate`,
   `DalCandidate`, `WordCandidate`.
6. **Required Evidence**: قواعد صرفية + شواهد استعمال للدور المرشح.
7. **Domain**: الصرف + الاستعمال؛ لا يتجاوز إلى الحكم الدلالي النهائي.
8. **Rank Policy**:
   - `CANDIDATE` لكل دور صرفي ممكن.
   - `LICENSED` للدور المرجَّح بسياق أو شاهد.
   - لا `PROVEN` بلا طبقة وضع لاحقة.
9. **Residuals**:
   - `defer:derivational_role_ambiguous:present`.
   - `defer:role_context_missing:present`.
   - `fariq:role_conflict:present`.
10. **Trace**: `{form, candidate_roles[], chosen_role, contextual_signals[]}`.

---

### 7.3 LexicalAttestationGate — بوابة السماع والاستعمال (الصوتي/المقطعي)

1. **Input Candidate**: `PhonoSyllabicLicenseCandidate` (مادة مرخَّصة صوتيًا).
2. **Gate**: `LexicalAttestationGate` — تُفتح حين يَثبُت السماع المعجمي أو
   العرفي أو الاصطلاحي للمادة.
3. **Output Candidate**: `RootCandidate` ← `RootStatusCandidate`
   (`attested` | `productive` | `frozen` | `borrowed` | `unattested`).
4. **Forbidden Jump**: ممكن صوتيًا → مادة عربية مستعملة.
5. **Forbidden Outputs**: `FormCandidate`, `MeaningCandidate`, `WordCandidate`,
   `HukmCandidate`.
6. **Required Evidence**: شواهد السماع (معجمية/نقلية)، شواهد الاستعمال
   (نصوص/مدوّنات)، شواهد الإهمال.
7. **Domain**: المعجم + النقل + الاستعمال؛ لا يدخل المجال الدلالي.
8. **Rank Policy**:
   - `CANDIDATE` لمجرد الإمكان الصوتي.
   - `LICENSED` عند شاهد سماع أو استعمال موثَّق.
   - `PROVEN` يتطلب اتفاق مصدرين موثَّقين على الأقل (داخل الطبقة).
9. **Residuals**:
   - `defer:lexical_attestation_missing:present`.
   - `defer:root_status_unknown:present`.
   - `fariq:attestation_conflict:present`.
10. **Trace**: `{root_skeleton, attestation_sources[], status, productivity_indicators[]}`.

---

### 7.4 LexicalPathGate — بوابة المسار اللفظي (الوزن)

1. **Input Candidate**: `RootCandidate` أو `RawLexCandidate`.
2. **Gate**: `LexicalPathGate` — تختار **مسارًا واحدًا** من سبعة قبل تطبيق
   منطق الوزن:
   ```
   root_weight_path     — جذر + وزن (للمشتقات والأفعال).
   stem_pattern_path    — جذع بنمط محفوظ.
   mabni_operator_path  — مبني (ضمائر، أسماء إشارة، حروف معنى…).
   borrowed_path        — دخيل.
   proper_name_path     — علم.
   frozen_jamid_path    — جامد محفوظ.
   residual_path        — لا يطابق ما سبق (اسم صوت، اسم فعل، صيغة محفوظة).
   ```
3. **Output Candidate**: `LexicalPathCandidate` يحدد المسار المختار، يفتح
   بدوره `FormCandidate` فقط في مسار `root_weight_path` (و`stem_pattern_path`
   جزئيًا).
4. **Forbidden Jump**: لفظ عربي → جذر/وزن (دون المرور بهذه البوابة).
5. **Forbidden Outputs**: `FormCandidate` خارج المسارين المسموح لهما،
   `MeaningCandidate`, `HukmCandidate`.
6. **Required Evidence**: قواعد الاشتقاق + قواعد البناء + شواهد التصنيف.
7. **Domain**: الصرف + المعجم؛ لا يتجاوز إلى الدلالة.
8. **Rank Policy**:
   - `CANDIDATE` لكل مسار محتمل.
   - `LICENSED` للمسار المرجَّح بدليل.
   - `PROVEN` غالبًا غير ممكن داخل الطبقة وحدها.
9. **Residuals**:
   - `defer:lexical_path_ambiguous:present`.
   - `fariq:path_conflict:present`.
   - `defer:residual_path_unclassified:present`.
10. **Trace**: `{token, candidate_paths[], chosen_path, classification_evidence[]}`.

---

### 7.5 VerbalSignifiedGate — بوابة المدلول اللفظي (الصيغة)

1. **Input Candidate**: `FormCandidate` (صيغة مرخَّصة من 7.4).
2. **Gate**: `VerbalSignifiedGate` — تفتح **مدلولًا لفظيًا مرشحًا** فقط
   (بحسب التعريف في القسم 3).
3. **Output Candidate**: `VerbalSignifiedCandidate` (لا أكثر).
4. **Forbidden Jump**: مدلول لفظي → معنى معجمي نهائي/مراد/حكم.
5. **Forbidden Outputs**: `WadhCandidate` (مكان طبقة لاحقة), `MeaningCandidate`,
   `FinalMeaning`, `HukmCandidate`, `RealityClaim`.
6. **Required Evidence**: تركيب الصيغة + وظيفتها الصرفية + قواعد البناء.
7. **Domain**: الصرف + البناء فقط.
8. **Rank Policy**:
   - `CANDIDATE` افتراضيًا.
   - `LICENSED` عند توافق الصيغة مع قواعد الوظيفة دون معارض.
9. **Residuals**:
   - `defer:verbal_signified_underspecified:present`.
   - `fariq:form_function_conflict:present`.
10. **Trace**: `{form, structural_signals[], opened_signified_facets[]}`.

---

### 7.6 WadhScopeGate — بوابة نوع الوضع ومجاله (الوضع)

1. **Input Candidate**: `VerbalSignifiedCandidate` + شواهد استعمال.
2. **Gate**: `WadhScopeGate` — تحدد **نوع الوضع ومجاله** قبل ترخيص المعنى.
   الأنواع: لغوي، عرفي، شرعي، اصطلاحي، علمي، تقني، منقول، مجازي مستقر.
3. **Output Candidate**: `WadhCandidate` بحقول:
   ```
   { source_type, domain, attestation, usage_scope,
     historical_layer, rank, residuals }
   ```
4. **Forbidden Jump**: شاهد واحد → وضع عام؛ أو خلط الوضع اللغوي بالشرعي/
   الاصطلاحي في مجال مختلف.
5. **Forbidden Outputs**: `MeaningCandidate` خارج المجال المثبت، `HukmCandidate`,
   `FinalMeaning`.
6. **Required Evidence**: شواهد متعددة من نفس المجال؛ مصدر وضع موثَّق.
7. **Domain**: محدَّد بحقل `domain` نفسه؛ لا يتعدّاه.
8. **Rank Policy**:
   - `CANDIDATE` لكل نوع وضع مرشح.
   - `LICENSED` عند شاهد + مجال موافق.
   - `PROVEN` يتطلب اتفاق مصدرين على الأقل من نفس المجال.
9. **Residuals**:
   - `defer:wadh_scope_unresolved:present`.
   - `defer:domain_mismatch:present`.
   - `fariq:wadh_source_conflict:present`.
10. **Trace**: `{signified, candidate_wadh_types[], chosen_scope, domain_evidence[]}`.

---

### 7.7 DalalahTypeGate — بوابة نوع الدلالة (الدلالة)

1. **Input Candidate**: `WadhCandidate` (مرخَّص).
2. **Gate**: `DalalahTypeGate` — تحدد نوع العلاقة بين الدال والمدلول:
   ```
   mutabaqah   (مطابقة)
   tadammun    (تضمن)
   iltizam     (التزام)
   ishara      (إشارة)
   iqtidha     (اقتضاء)
   mafhum      (مفهوم موافقة/مخالفة)
   ```
3. **Output Candidate**: `DalalahCandidate` مع `relation_type` صريح.
4. **Forbidden Jump**: وجود علاقة دلالية → نوع دلالة محدد بلا فصل؛ خلط
   الدلالات الضعيفة (تضمن/التزام) بالقوية (مطابقة).
5. **Forbidden Outputs**: `IfadahCandidate` (طبقة لاحقة), `HukmCandidate`,
   `FinalMeaning`.
6. **Required Evidence**: قواعد الدلالة + شاهد للعلاقة المرشحة.
7. **Domain**: الوضع المثبت في 7.6 لا غيره.
8. **Rank Policy**:
   - `mutabaqah` يمكن أن تصل إلى `LICENSED`/`PROVEN` بشاهد قوي.
   - `tadammun` / `iltizam` تقف عند `CANDIDATE` افتراضيًا، ولا ترتقي إلا
     بشاهد إضافي + مرور عبر `HypothesisGate` إن لزم (7.13).
9. **Residuals**:
   - `defer:dalalah_type_ambiguous:present`.
   - `fariq:dalalah_relation_conflict:present`.
10. **Trace**: `{wadh, candidate_relations[], chosen_relation, justification[]}`.

---

### 7.8 ReferenceResolutionGate — بوابة حل الإحالة (الإحالة + السياق)

1. **Input Candidate**: `ReferenceCandidate` (ضمير، إشارة، موصول، علم سياقي).
2. **Gate**: `ReferenceResolutionGate` — تفصل **الإحالة** (من/ما المشار إليه؟)
   عن **السياق** (ما المحيط المرجِّح؟)، ولا تثبت مرجعًا نهائيًا بلا قرينة.
3. **Output Candidate**:
   `CandidateReferents` ← `ContextualSelectionCandidate` ← `ReferentRankCandidate`.
4. **Forbidden Jump**: ضمير/إشارة → مرجع نهائي بلا حل إحالة.
5. **Forbidden Outputs**: `MeaningCandidate` معتمد على مرجع غير محلول،
   `HukmCandidate`, `FinalMeaning`.
6. **Required Evidence**: قرائن سابقة (`antecedent`), قرائن سياقية (`deictic`),
   تطابق نحوي.
7. **Domain**: النص + السياق المباشر؛ لا يتجاوز إلى مجالات الحكم.
8. **Rank Policy**:
   - `CANDIDATE` لكل مرجع محتمل.
   - `LICENSED` للمرجع الراجح.
   - `PROVEN` يستلزم انعدام معارض.
9. **Residuals**:
   - `defer:antecedent_missing:present`.
   - `defer:deictic_context_missing:present`.
   - `fariq:multiple_candidate_referents:present`.
   - `fariq:agreement_conflict:present`.
10. **Trace**: `{reference_token, candidate_referents[], chosen_referent, contextual_signals[]}`.

---

### 7.9 IfadahClosureGate — بوابة تمام الإفادة (النسبة)

1. **Input Candidate**: `NisbahCandidate` (إسناد، عامل/معمول، إضافة، شرط/جواب،
   موصول/صلة…).
2. **Gate**: `IfadahClosureGate` — تتحقق من اكتمال شروط الإفادة **بحسب نوع
   التركيب**؛ ليس كل نسبة إفادة.
3. **Output Candidate**: `IfadahCandidate` بأحد الأنواع:
   ```
   إفادة اسمية | إفادة فعلية | إفادة شرطية | إفادة إنشائية
   إفادة ناقصة | إفادة مقيدة
   ```
4. **Forbidden Jump**: تركيب صحيح → إفادة تامة (مثل: "كتاب زيد" ليست إفادة
   حكمية تامة بمجردها).
5. **Forbidden Outputs**: `HukmCandidate`, `FinalMeaning`, `RealityClaim`.
6. **Required Evidence**: قواعد الإسناد لكل نوع تركيب + خلو من نواقص.
7. **Domain**: النحو + التركيب؛ لا يتعدّى إلى الحكم.
8. **Rank Policy**:
   - `CANDIDATE` افتراضيًا.
   - `LICENSED` عند اكتمال شروط الإسناد دون نقص.
9. **Residuals**:
   - `defer:ifadah_incomplete:present`.
   - `defer:nisbah_type_unresolved:present`.
   - `fariq:ifadah_type_conflict:present`.
10. **Trace**: `{nisbah_type, components[], completion_status, ifadah_subtype}`.

---

### 7.10 DomainNormGate — بوابة المعيار الخطابي (القوة الخطابية)

1. **Input Candidate**: `IfadahCandidate` + `SpeechForceCandidate` (خبر، أمر،
   نهي، استفهام، نداء، تمنٍّ، ترجٍّ، تعجب، شرط، قسم).
2. **Gate**: `DomainNormGate` — تفصل **هيئة الإفادة** عن **حكمها المعياري**؛
   تحدد فقط نوع الخطاب، لا الحكم اللاحق.
3. **Output Candidate**: `NormReadyCandidate` (مهيَّأ لـ `HukmEvidenceGate`).
4. **Forbidden Jumps**:
   ```
   أمر    → وجوب
   نهي    → تحريم
   خبر    → صدق
   استفهام → جهل المتكلم
   ```
5. **Forbidden Outputs**: `HukmCandidate` بلا مرور على `EvidenceDomainGate`،
   `FinalMeaning`, `RealityClaim`.
6. **Required Evidence**: قواعد القوة الخطابية + قرائن السياق.
7. **Domain**: التداولي/الخطابي؛ لا ينتقل لمجال الحكم النهائي.
8. **Rank Policy**:
   - `CANDIDATE` ابتدائيًا.
   - `LICENSED` عند تحديد القوة دون معارض.
9. **Residuals**:
   - `defer:speech_force_ambiguous:present`.
   - `fariq:speech_force_conflict:present`.
10. **Trace**: `{ifadah, candidate_forces[], chosen_force, pragmatic_signals[]}`.

---

### 7.11 EvidenceDomainGate — بوابة مجال الدليل (الحكم)

1. **Input Candidate**: `NormReadyCandidate` + `EvidenceBundle` (دليل + شروط
   + موانع).
2. **Gate**: `EvidenceDomainGate` — تتحقق أن:
   - الدليل من نوع يتوافق مع نوع الحكم المطلوب.
   - الشروط محققة.
   - الموانع منتفية.
   - الحكم لا يخرج عن مجاله (لغوي، صرفي، نحوي، دلالي، تداولي، واقعي،
     شرعي، برمجي، معماري).
3. **Output Candidate**: `HukmCandidate` بهيكل:
   ```
   { hukm_type, domain, claim, evidence, conditions, blockers,
     rank, residuals }
   ```
4. **Forbidden Jumps**:
   ```
   حكم لغوي   → حكم واقعي
   حكم تركيبي → حكم صدق
   حكم دلالي  → حكم شرعي
   ```
5. **Forbidden Outputs**: `TanzilCandidate` (طبقة 7.12 لاحقة)، `FinalMeaning`،
   `RealityClaim` خارج المجال.
6. **Required Evidence**: حِزَم دليل متخصصة بحسب `hukm_type`.
7. **Domain**: مُلزِم بأن يطابق `domain` الحقل في `HukmCandidate`.
8. **Rank Policy**:
   - `CANDIDATE` بمجرد توفر دليل ابتدائي.
   - `LICENSED` عند تحقق الشروط وانتفاء الموانع.
   - `PROVEN` يستلزم استيفاء كامل + انعدام معارض في المجال.
9. **Residuals**:
   - `defer:evidence_insufficient:present`.
   - `defer:conditions_unmet:present`.
   - `defer:blocker_present:present`.
   - `fariq:domain_mismatch:present`.
   - `fariq:evidence_conflict:present`.
10. **Trace**: `{norm_ready_id, evidence_refs[], conditions_satisfied[], blockers_absent[], hukm_type, domain}`.

---

### 7.12 TahqiqAlManatGate — بوابة تحقيق المناط (المناط/التنزيل)

1. **Input Candidate**: `HukmCandidate` عام + `ManatCandidate` (علة/محل/سبب
   الربط) + `IncidentCandidate` (الواقعة المراد التنزيل عليها).
2. **Gate**: `TahqiqAlManatGate` — لا تكتفي بوجود المناط، بل تشترط **تحققه**
   في الواقعة: تحقق الموضوع، تحقق الشروط، انتفاء الموانع، تعيين الواقعة،
   مطابقة المجال.
3. **Output Candidate**: `TanzilCandidate` (تنزيل مرشَّح، ليس حكمًا جديدًا).
4. **Forbidden Jump**: حكم عام + مناط نظري → تنزيل على واقعة.
5. **Forbidden Outputs**: `FinalMeaning`, حكم جديد خارج نطاق التنزيل،
   `RealityClaim` غير مرتبط.
6. **Required Evidence**: إثبات تحقق المناط في الواقعة عينًا.
7. **Domain**: مجال الحكم نفسه؛ لا يُنزَّل حكم مجال على واقعة مجال آخر.
8. **Rank Policy**:
   - `CANDIDATE` عند توفر مناط نظري فقط.
   - `LICENSED` عند تحقق المناط في الواقعة دون معارض.
   - `PROVEN` يستلزم استيفاء جميع شروط التحقق.
9. **Residuals**:
   - `defer:manat_unrealized:present`.
   - `defer:incident_unidentified:present`.
   - `fariq:manat_domain_mismatch:present`.
10. **Trace**: `{general_hukm, manat, incident, realization_evidence[], chosen_tanzil}`.

---

### 7.13 HypothesisGate — بوابة الفرضيات (الروابط الضعيفة)

1. **Input Candidate**: `WeakLinkCandidate` بهيكل:
   ```
   { source, target, link_type, similarity_basis, domain_distance,
     rank = CANDIDATE, residuals, forbidden_outputs }
   ```
   حيث `link_type` ∈ { تضمن، التزام، تشابه وزني، تشابه جذري، تقارب سياقي،
   قياس بعيد، استعارة، نقل اصطلاحي محتمل، رابط تاريخي، رابط استعمالي نادر،
   رابط شبكي بين مجالين }.
2. **Gate**: `HypothesisGate` — تقبل بإنتاج فرضية فقط؛ لا ترخّص ترقية إلى
   حكم.
3. **Output Candidate**: `HypothesisCandidate` (rank `CANDIDATE` فقط).
4. **Forbidden Jump**: رابط ضعيف → حكم أو وضع أو تنزيل.
5. **Forbidden Outputs**: `HukmCandidate`, `WadhCandidate` نهائي,
   `TanzilCandidate`, `FinalMeaning`.
6. **Required Evidence**: شاهد ضعيف واحد على الأقل + تصنيف نوع الرابط.
7. **Domain**: مقيَّد بمجال المصدر؛ ولا ينتقل إلا عبر `DomainTransferGuard`
   (7.14) **بعد** ترقيته إلى رابط قوي.
8. **Rank Policy**: لا يتعدّى `CANDIDATE` داخل هذه البوابة. الترقية إلى
   `LICENSED` تستلزم اختبارًا في طبقة لاحقة (PR تنفيذي مستقل).
9. **Residuals**:
   - `defer:hypothesis_untested:present` (افتراضيًا، حتى يثبت العكس).
   - `fariq:weak_link_conflict:present`.
10. **Trace**: `{source, target, link_type, similarity_basis, domain_distance, evidence_refs[]}`.

---

### 7.14 DomainTransferGuard — حارس انتقال المجال (الروابط القوية)

1. **Input Candidate**: `StrongLinkCandidate` مستوفٍ الشروط السبعة (القسم
   4.2) داخل **مجاله الأصلي**.
2. **Gate**: `DomainTransferGuard` — يمنع أي انتقال إلى مجال آخر إلا عبر
   إثبات إضافي ومخصص. الافتراض: **لا انتقال**.
3. **Output Candidate**: `CrossDomainLinkCandidate` فقط حين تتوفر:
   ```
   1. CrossDomainEvidence  (دليل صريح للانتقال).
   2. TargetDomainValidity (المجال المستهدف يقبل هذا النوع من الروابط).
   3. ResidualRetention    (البقايا تبقى مسجَّلة بعد الانتقال).
   4. RankDowngradePolicy  (الرتبة بعد الانتقال ≤ الرتبة قبله).
   ```
4. **Forbidden Jump**: رابط قوي صرفيًا → نتيجة دلالية نهائية؛ رابط قوي لغوي
   → حكم واقعي/شرعي؛ بشكل عام: استخدام رابط قوي خارج طبقته/مجاله.
5. **Forbidden Outputs**: `HukmCandidate` في مجال آخر، `FinalMeaning`,
   `TanzilCandidate` عابر للمجال.
6. **Required Evidence**: دليل انتقال صريح بنوع مقبول في المجال المستهدف.
7. **Domain**: يتطلب تحديد `source_domain` و`target_domain` كلاهما بصراحة.
8. **Rank Policy**:
   - الرتبة بعد الانتقال **لا تزيد** عن الرتبة قبله.
   - في الغالب: تنازل من `PROVEN` في المصدر إلى `LICENSED` في الهدف على
     الأكثر، ما لم يوجد دليل مستقل في المجال الهدف.
9. **Residuals**:
   - `defer:cross_domain_evidence_missing:present`.
   - `fariq:target_domain_rejects_link:present`.
   - `defer:rank_downgrade_required:present`.
10. **Trace**: `{strong_link, source_domain, target_domain, transfer_evidence[], rank_before, rank_after}`.

---

## 8. هوية النواة الجبرية (Algebraic Kernel Identity)

> **ملاحظة دستورية**: هذا القسم **توصيفيّ لا تنفيذيّ**. لا يضيف سلوكًا جديدًا
> إلى `QiyasKernel`، ولا يعدّل أي قاعدة قائمة. وظيفته توثيق الصيغة الجبرية
> التي تنفذها النواة فعلًا في `src/qiyas_core/` بحيث تُقرأ السلسلة الواردة
> في الأقسام 1–7 على أنها تطبيقات لهذا الجبر، لا قواعد منفصلة عنه.

### 8.1 الصيغة الجبرية الحاكمة

النواة `QiyasKernel` تنفذ عملية واحدة فقط، تُكتب جبريًا:

```
QiyasOperation(asl, far, rule, evidence, context)
  → CandidateSet(status, rank, residuals, trace_ids)
```

أي:

```
أصل + فرع + قاعدة + دليل + سياق  →  مرشح محكوم
```

وليست:

```
input  →  answer
```

هذا الفرق دستوريّ: كل بوابة من البوابات الأربع عشرة في القسم 7 يجب أن تُصاغ
كتخصيص لهذه العملية، لا كدالة `input → output` مستقلة.

### 8.2 أركان العملية الجبرية كما هي منفذة في النواة

| الركن الجبري       | تمثيله في `src/qiyas_core/`                                |
| ------------------ | ---------------------------------------------------------- |
| المجال (Domain)    | `QiyasContext.layer`, `QiyasRule.layer`                    |
| الأصل (Asl)        | `QiyasRequest.asl: QiyasNodeRef`                           |
| الفرع (Far`)       | `QiyasRequest.far: QiyasNodeRef`                           |
| القاعدة            | `QiyasRule`                                                |
| الوصف المؤثر       | `QiyasRule.required_effective_wasf`                        |
| العلة الجامعة      | `QiyasRule.required_illah`                                 |
| الشروط والموانع    | `QiyasRule.required_wadi_gates`                            |
| الفارق القادح      | `QiyasRule.invalidating_differences`                       |
| العنصر المحايد     | `QiyasRule.neutral_identity_domain` + حفظ `identity_ids`   |
| الدليل             | `EvidenceSet`                                              |
| الرتبة             | `EvidenceRank`, `rank_ceiling`, `minimum_rank()`           |
| البقايا            | `Residual`, `QiyasAudit`                                   |
| الأثر              | `trace_ids`                                                |
| المخرج             | `Candidate` / `CandidateSet`                               |
| منع القفز          | `QiyasRule.forbidden_outputs` + `Candidate.__post_init__`  |

سلسلة الفحوص الدستورية داخل `QiyasKernel.apply()` (راجع
`src/qiyas_core/kernel.py`) هي بالترتيب:

```
context layer
node types
asl established
far determined
effective wasf
illah
wadi gates
fariq
defer
identity
rank
forbidden outputs
```

هذه السلسلة هي الخوارزمية الجبرية نفسها؛ كل بوابة في القسم 7 تمر بها
بلا استثناء.

### 8.3 العنصر المحايد: حفظ الهوية (Neutral Identity Preservation)

في الجبر، **العنصر المحايد** هو ما يسمح بالعملية دون تغيير هوية الشيء.
في `qiyas_core` هذا العنصر **ليس صفرًا عدديًا** و**ليس "لا شيء"**، بل
هو حقل إلزامي على كل قاعدة:

```
QiyasRule.neutral_identity_domain: str   # إلزامي
```

و`QiyasRule.__post_init__` يرفض أي قاعدة بلا `neutral_identity_domain`.
معناه الجبري المحرَّر:

```
Id_domain(asl, far) = asl.identity ⊕ far.identity
```

أي أن القاعدة **لا يجوز** أن تقول:

```
أصل + فرع  →  شيء جديد يبتلع الأصل والفرع
```

بل **يجب** أن تحفظ الهوية:

```
identity(asl)  +  identity(far)   ⊆   identity(candidate)
```

ويظهر هذا الإنفاذ في موضعين متكاملين داخل النواة:

1. **عند الفحص** — `QiyasKernel._check_identity` يشترط وجود هويات على
   الأصل والفرع، ويمنع اختلاط `identity_ids` بـ`trace_ids` تحت اسم
   البقية `identity_trace_conflict`.
2. **عند البناء والتحقق** — عند صنع المرشح:

   ```
   identity_ids = request.asl.identity_ids + request.far.identity_ids
   ```

   ثم `QiyasKernel._validate_output` يرفض أي مرشح فقد هويات مصدره.

كذلك `QiyasNodeRef.__post_init__` و`Candidate.__post_init__` يرفضان
تقاطع `identity_ids` مع `trace_ids` بنيويًا، فلا يمكن إنشاء عقدة أو
مرشح ينتهك حفظ الهوية أصلًا.

**القانون التشغيلي:**

```
لا انتقال معتبر إذا فقد المرشح هوية الأصل والفرع،
ولا انتقال معتبر إذا اختلطت الهوية بالأثر.
```

### 8.4 الربط (Linkage) كعملية موزعة لا كصنف واحد

لا يوجد في `src/qiyas_core/` صنف باسم `Binding`. الربط الجبري **عقد موزع**
على أربعة مواضع:

1. **`QiyasRule`** — عقد الربط: `asl_type`, `far_type`,
   `required_effective_wasf`, `required_illah`, `neutral_identity_domain`.
2. **`EvidenceSet`** — يثبت `claims` التي ترخص الربط
   (`asl:established`, `far:determined`, `wasf:*:evidenced`,
   `illah:*:verified`, `wadi:*:...`)، ولكل دليل `proves`, `rank`,
   `trace_ids`.
3. **`QiyasKernel`** — يفحص أن هذا الربط لا يقفز: لا أصل بلا دليل،
   ولا فرع بلا تعيين، ولا وصف بلا `evidence`، ولا علة بلا `verification`،
   ولا رتبة فوق أضعف دليل.
4. **`Candidate`** — يحفظ الناتج كمرشح فقط (`CandidateOnly`)،
   ويمنع `FinalMeaning`/`RealityClaim`/`HukmCandidate` عبر
   `forbidden_outputs` و`__post_init__`.

### 8.5 معنى "جبر كامل كنواة"

تُقرأ عبارة "النواة الدستورية كاملة" بمعنى دقيق:

```
الجبر كامل كنواة قياس:
  - يحتوي كل أركان العملية الجبرية (راجع جدول 8.2).
  - يفرض العنصر المحايد بنيويًا (راجع 8.3).
  - يفرض المخرج الوحيد المسموح: CandidateSet.

والجبر العربي الكامل لم تُستأنف طبقاته canonical بعد:
  - المثالان الكنونيان الحاليان هما UnicodeLayerAdapter وTypedCodePointLayerAdapter (PR #20).
  - بقية الطبقات (Jamid, Mushtaqq, Wazn, Wadh, Dalalah, Ifadah,
    Hukm, Tanzil…) عقود في هذا الملف، لا تنفيذ canonical في src/.
```

هذا هو **التصحيح الدستوري**: الكمال هنا كمالُ نواة، لا كمالُ طبقات.

### 8.6 شكل التطبيق المُلزِم لكل طبقة لاحقة

أي طبقة تُنفَّذ مستقبلًا تحت أي بوابة من بوابات القسم 7 يجب أن تُصاغ
بهذه الصورة، بلا استثناء:

```
request = QiyasRequest(
    rule=RULE,                       # عقد الربط
    asl=asl_node,                    # أصل بهوية محفوظة
    far=far_node,                    # فرع بهوية محفوظة
    evidence=evidence_set,           # دليل بـ proves/rank/trace
    context=QiyasContext(layer=RULE.layer),
)

candidate_set = QiyasKernel().apply(request)
```

ويُمنع منعًا دستوريًا:

```
- كتابة دالة تعيد "meaning" أو "answer" مباشرة.
- إنتاج Hukm أو FinalMeaning أو RealityClaim من طبقة لا ترخصه.
- بناء قاعدة بلا neutral_identity_domain.
- بناء مرشح يتقاطع فيه identity_ids مع trace_ids.
- تجاوز سلسلة فحوص kernel أو الالتفاف عليها.
```

والمسموح الوحيد:

```
بناء Adapter يصوغ (أصل، فرع، دليل) ثم يُمرر الطلب إلى QiyasKernel،
ويترك للنواة قرار accepted / deferred / blocked.
```

### 8.7 الأمثلة الكنونية الحالية

#### 8.7.1 UnicodeLayerAdapter — طبقة الانتماء اليونيكودي

`UnicodeLayerAdapter` (في `src/qiyas_core/unicode_adapter.py`) هو
التطبيق الكنوني الأول لهذا الجبر: يبني الأصل
(`Arabic Unicode Block` بهوية `identity:arabic_unicode_block`) والفرع
(`InputCodepoint` بهوية `identity:codepoint:<hex>`)، ثم `EvidenceSet`،
ثم يمرر الطلب إلى `QiyasKernel`. عند `codepoint` غير عربي يضيف
`fariq:non_arabic_codepoint:present` فيمنع kernel النتيجة. هذا هو
المعنى الدقيق لـ "Arabic Unicode membership as Qiyas operation":

```
أصل + فرع + دليل + علة + شروط + لا مانع  →  مرشح انتماء
```

#### 8.7.2 TypedCodePointLayerAdapter — طبقة التصنيف الكودي (PR #20, hardened PR #23)

`TypedCodePointLayerAdapter` (في `src/qiyas_core/typed_codepoint_adapter.py`) هو
التطبيق الكنوني الثاني، ويُنفذ تصنيفًا disjoint على `UnicodeCandidate`:

```
UnicodeCandidate  →  TypedCodePoint
                      (Letter ⊔ Haraka ⊔ Boundary ⊔ Punctuation ⊔ Residual)
```

الأصل: `TypedCodePointClassificationDomain` (مجال التصنيف الكودي).
الفرع: `UnicodeCandidate` (بهوية محفوظة من طبقة Unicode).
الوصف المؤثر العام: `is_classifiable_codepoint` (لكل الأنواع).
**الوصف المؤثر الخاص** (PR #23): `is_arabic_letter`, `is_arabic_haraka`, `is_whitespace_boundary`, `is_arabic_punctuation`, `is_unclassified_codepoint`.
العلة العامة: `belongs_to_typed_domain` (لكل الأنواع).
**العلة الخاصة** (PR #23): `belongs_to_letter_class`, `belongs_to_haraka_class`, `belongs_to_boundary_class`, `belongs_to_punctuation_class`, `belongs_to_residual_class`.
المخرج: `LetterCodePoint` أو `HarakaCodePoint` أو `BoundaryCodePoint` أو
`PunctuationCodePoint` أو `ResidualCodePoint` (يتحدد ديناميكيًا بحسب الكود).

**الحفظ الجبري:**

- يحفظ `identity:codepoint:<hex>` من الفرع.
- يضيف `identity:typed_codepoint_domain` من الأصل.
- كل كود يُصنف إلى نوع **واحد فقط** (disjoint union).
- `forbidden_outputs` يمنع القفز إلى `AtomicUnitCandidate` أو طبقات أعلى.
- **PR #23**: كل تصنيف يثبت الوصف والعلة الخاصين داخل `EvidenceSet`.
- **PR #23**: `invalidating_differences` تثبت disjoint union جبريًا: `multiple_classes_claimed`, `ambiguous_classification`, `letter_haraka_overlap`, `boundary_punctuation_overlap`.

**الصيغة الجبرية:**

```
domain + unicode_candidate + evidence(is_classifiable + specific_wasf + specific_illah)
  →  typed_codepoint[LetterCodePoint | HarakaCodePoint | ...]
```

**القيد الدستوري** (PR #23):
`classify_codepoint()` مخصص للاختبارات فقط. المسار الإنتاجي الدستوري:
```
UnicodeLayerAdapter.process_codepoint()
  → UnicodeCandidate (accepted)
  → TypedCodePointLayerAdapter.classify_unicode_candidate()
  → TypedCodePoint
```

كل طبقة جديدة يجب أن تُحاكي هذا الشكل، لا أن تُخالفه.

### 8.8 الصياغة المعتمدة (Reference Statement)

تُعتمد الصياغتان التاليتان مرجعًا عند توثيق النواة للمبرمج:

```
qiyas_core is a complete algebraic kernel for governed qiyas:
it preserves identity as the neutral element,
uses evidence as licensed force,
residuals as blockers/deferments,
rank as transition ceiling,
and CandidateSet as the only allowed output.
```

```
qiyas_core نواة جبرية كاملة للقياس المحكوم:
العنصر المحايد فيها هو حفظ الهوية،
والدليل هو قوة الترخيص،
والبقايا هي موانع أو مؤجلات،
والرتبة سقف الانتقال،
والمخرج الوحيد هو مرشح لا حكم نهائي.
```

---

## 9. قاموس المصطلحات (Glossary — AR/EN)

| العربية                  | الإنجليزية              | تعريف موجز                                                                  |
| ------------------------ | ----------------------- | --------------------------------------------------------------------------- |
| مرشح                     | Candidate               | مخرج طبقة قبل الترخيص؛ لا يجوز معاملته كحكم.                                |
| بوابة                    | Gate                    | شرط بنيوي يحوّل مرشحًا إلى مرشح مرخّص داخل الطبقة.                          |
| دليل                     | Evidence                | شاهد من نوع متفق عليه يفتح بوابة محددة.                                     |
| مجال                     | Domain                  | نطاق صلاحية الدليل (لغوي، صرفي، نحوي، دلالي، تداولي، واقعي، شرعي…).         |
| رتبة                     | Rank                    | درجة الترخيص: `CANDIDATE` < `LICENSED` < `PROVEN`.                          |
| بقايا                    | Residuals               | ما لم يُحسم؛ يُمثَّل بـ `defer:*:present` أو `fariq:*:present`.             |
| أثر                      | Trace                   | بنية تربط المخرج بمدخلاته وأدلته وبوابته.                                   |
| مخرج ممنوع               | Forbidden Output        | نوع مخرج لا يُسمح للقاعدة بإنتاجه (يطابق `forbidden_outputs` في النواة).    |
| قفزة ممنوعة              | Forbidden Jump          | انتقال غير مرخَّص من طبقة إلى أعلى منها بلا بوابة.                          |
| كود يونيكود              | UnicodeCandidate        | مرشح انتماء يونيكودي عربي (خرج `UnicodeLayerAdapter`).                     |
| كود مُصنّف               | TypedCodePoint          | مرشح تصنيف كودي (حرف/حركة/حد/ترقيم/بقية)، خرج `TypedCodePointLayerAdapter`. |
| الجامد                   | Jamid                   | لفظ غير مشتق ولا مبنى وظيفي.                                                |
| المشتق                   | Mushtaqq                | لفظ صادر عن جذر بصيغة معروفة.                                               |
| المدلول اللفظي           | VerbalSignified         | المرشح البنيوي الذي تفتحه الصيغة قبل الوضع والمعنى والمراد والحكم.          |
| الوضع                    | Wadh                    | تخصيص اللفظ لمعنى داخل مجال (لغوي/عرفي/شرعي/اصطلاحي…).                      |
| الدلالة                  | Dalalah                 | علاقة الدال بالمدلول؛ أنواعها: مطابقة/تضمن/التزام/إشارة/اقتضاء/مفهوم.       |
| الإحالة                  | Reference               | الإشارة إلى مرجع نصي أو سياقي.                                              |
| النسبة                   | Nisbah                  | ربط طرفين في تركيب (إسناد، إضافة، شرط/جواب…).                               |
| الإفادة                  | Ifadah                  | اكتمال النسبة بحيث تحمل خبرًا أو إنشاءً.                                    |
| القوة الخطابية           | Speech Force            | نوع الفعل الكلامي (خبر/أمر/نهي/استفهام…).                                   |
| الحكم                    | Hukm                    | نتيجة مرخَّصة داخل مجال محدد بشروط ودليل.                                   |
| المناط                   | Manat                   | علة/محل/سبب ربط الحكم بالواقعة.                                             |
| تحقيق المناط             | TahqiqAlManat           | إثبات تحقق المناط في الواقعة المعينة.                                       |
| التنزيل                  | Tanzil                  | تطبيق الحكم العام على واقعة بعد تحقيق المناط.                               |
| رابط ضعيف                | WeakLink                | علاقة فرضية لا ترقى إلى حكم؛ تمر عبر `HypothesisGate`.                      |
| رابط قوي                 | StrongLink              | علاقة مستوفية لشروط القسم 4.2؛ لا تعبر مجالها إلا عبر `DomainTransferGuard`. |

---

## 10. تصريح ختامي (Non-Implementation Declaration)

```
هذا الملف عقدٌ، لا تنفيذٌ.
لا يضيف كودًا.
لا يضيف اختبارات.
لا يعدّل src/ ولا experimental/ ولا tests/ ولا .github/workflows/.
لا يفتح طبقة runtime جديدة.
لا يغيّر سلوك QiyasKernel.

كل بوابة من البوابات الأربع عشرة تُنفَّذ في PR مستقل لاحقًا، بحدّ أدنى كافٍ،
وفق الترتيب الذي يحدده صاحب القرار الدستوري، وبشرط:
  - احترام محظورات القسم 2.2.
  - استخدام forbidden_outputs بنفس نمط النواة القائمة.
  - تمثيل البقايا بـ defer:*:present و fariq:*:present فقط.
  - حفظ Trace قابل للتدقيق.

ولا تُفتح بوابة جديدة قبل إغلاق التي قبلها.
```
