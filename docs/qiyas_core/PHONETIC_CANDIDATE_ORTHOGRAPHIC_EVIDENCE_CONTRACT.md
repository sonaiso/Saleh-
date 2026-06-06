# PhoneticCandidate ∥ OrthographicEvidence ∥ EvidenceBridge Contract

> **حالة الوثيقة:** دستور وثائقي فقط (documentation-only).
> **حالة التنفيذ:** لا runtime في هذا الـ PR. كل اسم جديد في هذه الوثيقة
> (`PhoneticCandidate`, `UnicodeGlyphCandidate`, `EvidenceBridge`,
> `BridgedLetterCandidate`, `OrthographicallyLicensedLetterCandidate`) هو
> **future runtime, not yet implemented**، تماشياً مع مذكرة
> *LCNV runtime implementation status* وقاعدة *constitutional PR sequencing*.
> **النطاق:** يُكمِّل GARA و `MakhrajAlgebra` ولا يلغي
> `DUAL_PATH_CONSTITUTIONAL_ARCHITECTURE.md` (Path A / Path B).

---

## § ١ — المبدأ الحاكم

1. `PhoneticCandidate ≠ LetterCandidate`.
   المرشّح الصوتي طبقة استدلالية مستقلة عن مرشّح الحرف، لا تساويه ولا تُنتجه
   بمفردها.
2. `Unicode = OrthographicEvidence`، لا `PhoneticIdentity` ولا
   `LetterIdentity`. نقطة الكود الموسومة شاهدٌ كتابي مرخّص، ليست أصلاً
   صوتياً ولا حكماً بالهوية الحرفية.
3. **لا حرفَ بشاهد واحد.** إنتاج `LetterCandidate` المركّب يلزمه
   **شاهدان مرخّصان** يجتمعان في بوابة معلَنة: شاهد صوتي (Phonetic) +
   شاهد كتابي (Orthographic).

هذه المبادئ الثلاثة مأخوذة من المقترح بعد تنقيته، وهي القوانين الوحيدة
المعتمدة دستورياً في هذه الوثيقة (انظر §١٠).

---

## § ٢ — تعريف `PhoneticCandidate`

`PhoneticCandidate` طبقةٌ استدلالية مستقلة، تجلس **بين**
`ArabicSoundCandidate` و `LetterIdentity` في سلسلة GARA المخزّنة:

```
HumanDigitalSound
  → UniversalPhoneticProbability
    → ArabicDomainBridge
      → ArabicSoundCandidate
        → PhoneticCandidate         ← الطبقة المُضافة دستورياً هنا
          → (EvidenceBridge)
            → LetterIdentity
```

### ٢-١ مصدر التوليد

- يُنتَج `PhoneticCandidate` **بعد** عبور `ArabicDomainBridge` وترخيص
  `ArabicSoundCandidate` فقط؛ لا يجوز توليده من إشارة صوتية لم تعبر
  بوابة المجال العربي.
- لا يُنتَج من Unicode، ولا من أي شاهد كتابي. أي اشتقاق
  `Unicode ⇒ PhoneticCandidate` ممنوع نصاً (§٦).

### ٢-٢ ما يجوز أن يحمله

- `makhraj_origin` — من `MakhrajAlgebra` U0.
- `branch_type` — من `MakhrajAlgebra` U1.
- `internal_degree` — من `MakhrajAlgebra` U2.
- `sifat_vector` — من `MakhrajAlgebra` U3.
- `rank_ceiling` — لا يتجاوز سقف الرتبة المرخّص لطبقة الاستدلال الصوتي
  (نظير `ANALOGICAL` في `Γ_haraka`؛ لا `CERTAIN` للحرف).
- `residuals` — أي بقايا غير محسومة على مستوى الصوت.
- `trace` — أثر الاستدلال الصوتي حصراً.

### ٢-٣ ما يُحرَّم حمله

ممنوع على `PhoneticCandidate` أن يحمل أيّاً مما يلي:

- `letter_identity`
- `unicode_codepoint` أو `glyph` أو أي شاهد كتابي
- `root` / `wazn`
- `meaning` / `ifadah`
- `hukm` / `irab`

أي حقل من هذه الحقول إن ظهر يُسقط رتبة المرشّح ويُحوّله إلى مرشّح غير
مرخّص (يُعامَل معاملة residual blocking وفق قاعدة Layer Contract).

### ٢-٤ صيغة الإنتاج

ينتج `PhoneticCandidate` حقولاً بصيغة `possible_*` فقط (طيف فرضيات)،
تماشياً مع نمط `Γ_haraka` (`HarakaRoleSpectrum.possible_*`). لا يُنتج
مرشّحاً منتخباً ولا حكماً.

---

## § ٣ — تعريف `UnicodeGlyphCandidate` (OrthographicEvidence)

`UnicodeGlyphCandidate` هو **الشاهد الكتابي** المرخّص، ورتبته الدستورية
`OrthographicEvidence` فقط، لا `PhoneticAuthority`.

### ٣-١ مصدر التوليد

- يُنتَج من `TypedCodePoint` (موجود في `src/qiyas_core/typed_codepoint_adapter.py`)
  **بعد** إثبات `is_arabic_letter` و `belongs_to_letter_class` وفق
  التصلّب الذي أضافه PR #23 (مذكرة *TypedCodePoint algebraic proof
  hardening*).
- لا يُولَّد من إشارة صوتية، ولا من `PhoneticCandidate`.

### ٣-٢ ما يجوز أن يحمله

- `codepoint`
- `glyph_class`
- `orthographic_identity`
- شواهد كتابية بصيغة `وصف:` و `علة:` فقط، متّسقة مع QiyasKernel
  (مذكرة *evidence*).

### ٣-٣ ما يُحرَّم حمله أو استنباطه

- `makhraj` أو `sifat` أو أي خصيصة صوتية.
- `phonetic_identity` بأي صورة.
- أي ادعاء بأنه أصل صوتي أو مصدر مخرج.

### ٣-٤ الرتبة

`UnicodeGlyphCandidate.rank = OrthographicEvidence`. هذه رتبة شاهد، لا
رتبة هوية صوتية ولا رتبة حكم.

---

## § ٤ — `EvidenceBridge` (بوابة العبور الصوتية/الكتابية)

`EvidenceBridge` بوابةٌ مرخّصة، نظيرة `ArabicDomainBridge` في وظيفتها
الحَكَمية، لكنها مخصّصة للجمع بين شاهدين من رتبتين مختلفتين
(صوتي + كتابي).

### ٤-١ المهمة

التحقّق من **التطابق** بين `RankedPhoneticCandidate` (مخرج §٢ بعد
ترتيبه) و `UnicodeGlyphCandidate` (مخرج §٣) **داخل نظام عبور معلَن**.

### ٤-٢ الشواهد المطلوبة

كل الشواهد تستخدم بادئات عربية وفق ما يقبله `QiyasKernel`
(مذكرة *evidence*، `src/qiyas_core/kernel.py`):

- `اصل:phonetic_candidate_licensed`
- `اصل:orthographic_candidate_licensed`
- `وصف:bridge_system_declared:{system_id}`
- `علة:phonetic_orthographic_correspondence_proven`
- `فارق:phonetic_orthographic_mismatch:absent`

النمط `فارق:…:absent` ملتزم بمذكرة *fariq constitutional semantics*:
يُثبَت غياب الفرق القادح في المسار الناجح، ولا يُرفع `:present` إلا عند
وجود تعارض قاطع.

### ٤-٣ المخرَج

- مخرج البوابة الوحيد المسموح هو `LetterCandidate` (بمسمى أدق:
  `BridgedLetterCandidate`، انظر §٥).
- **ممنوع** أن تُنتج البوابة `Letter` نهائياً، أو `Hukm`، أو
  `NumericCoordinate`، أو أي معنى/جذر/وزن.

---

## § ٥ — قانون التركيب (الصياغة الثلاثية)

```
LetterCandidate = Bridge(
    RankedPhoneticCandidate,
    UnicodeGlyphCandidate,
    BridgeSystem
)
```

### ٥-١ الممنوعات التركيبية

- **ممنوع** `Bridge(PhoneticOnly) → LetterCandidate`.
  لا يجوز إنتاج مرشّح حرف بشاهد صوتي وحده.
- **ممنوع** `Bridge(OrthographicOnly) → BridgedLetterCandidate`.
  لا يجوز إنتاج مرشّح حرف **مركّب** بشاهد كتابي وحده. (هذا قلبٌ صريح
  للنمط الذي كان يكتفي بـ `TypedCodePoint` وحده لاستخراج حرف.)

### ٥-٢ ملاحظة الانتقال

المرشّح الحرفي الحالي المبني من `TypedCodePoint` وحده **يبقى صالحاً**،
لكنه يُعاد تصنيفه دستورياً إلى:

- `OrthographicallyLicensedLetterCandidate` — رتبة أدنى، شاهد كتابي فقط.

ويُميَّز عن:

- `BridgedLetterCandidate` — رتبة أعلى، يلزمها شاهدان (صوتي + كتابي).

هذا التصنيف الثنائي يحفظ Path A القائم دون كسر، ويُضيف رتبة أعلى للحالة
المركّبة فقط.

### ٥-٣ سقوف الرتب

- `OrthographicallyLicensedLetterCandidate.rank_ceiling` لا يتجاوز ما
  يخوّله الشاهد الكتابي وحده (لا يدّعي يقيناً صوتياً).
- `BridgedLetterCandidate.rank_ceiling` لا يتجاوز ما يخوّله الأضعف من
  الشاهدين (مبدأ الأخذ بالأدنى)، ولا يصل إلى رتبة حكم نهائي.

---

## § ٦ — جدول الممنوعات الصريحة

| ممنوع | السبب الدستوري |
|---|---|
| `Unicode ⇏ PhoneticCandidate` | Unicode شاهد كتابي، لا أصل صوتي. |
| `PhoneticCandidate ⇏ LetterCandidate` (دون `EvidenceBridge`) | لا حرف بشاهد واحد. |
| `UnicodeGlyphCandidate ⇏ Makhraj` أو `Sifat` | لا استنباط صوتي من رمز كتابي. |
| `PhoneticCandidate ⇏ Root / Wazn / Meaning / Hukm / I'rab` | حظر القفز فوق الطبقات (Layer Contract). |
| `LetterCandidate ⇏ Final Letter` | المرشّح ليس حكماً (Layer Contract). |
| `EvidenceBridge ⇏ NumericCoordinate` | الإحداثيات تتطلب `ProjectionSystem` (مذكرة *numeric coordinate derivation*). |

كل بند في هذا الجدول قابل للفحص دستورياً إذا/حين يُنفَّذ runtime مستقبلي،
ويجب أن يُجرَّم بـ `فارق:…:present` أو `residual:blocking:…` وفق سياسة
QiyasKernel.

---

## § ٧ — تكامل مع الموجود (Doc-Code Alignment)

التزاماً بمذكرة *governance doc-code alignment*، يستشهد هذا الدستور
بالملفات الفعلية فقط في الـ repo الحالي:

- `src/qiyas_core/typed_codepoint_adapter.py` — المصدر المستقبلي
  لـ `UnicodeGlyphCandidate`.
- `src/qiyas_core/letter_identity_adapter.py` — المستهلك المستقبلي
  لـ `LetterCandidate` بنوعيه (Bridged / OrthographicallyLicensed).
- `src/qiyas_core/kernel.py` — مصدر اشتراط بادئات الشواهد العربية
  (`اصل:` / `وصف:` / `علة:` / `فارق:` …).
- `src/qiyas_core/evidence.py` — مرجع `EvidenceSet.items` والمطابقة
  الحرفية (exact match) دون normalization.

لا تخترع هذه الوثيقة أي API غير موجود. كل اسم جديد
(`PhoneticCandidate`, `UnicodeGlyphCandidate`, `EvidenceBridge`,
`BridgedLetterCandidate`, `OrthographicallyLicensedLetterCandidate`)
مُعلَّم صراحةً **"future runtime, not yet implemented"** في أعلى هذه
الوثيقة، وفق مذكرة *LCNV runtime implementation status*.

---

## § ٨ — الانسجام مع dual-path

استناداً إلى مذكرة *dual-path architecture* و
`docs/qiyas_core/DUAL_PATH_CONSTITUTIONAL_ARCHITECTURE.md`:

- **Path A** (`TypedCodePoint → LetterIdentity → HarakaFunction → Position
  → SlotCandidate`): يبقى مساراً دستورياً صالحاً، ومرشّح حرفه يُصنَّف
  `OrthographicallyLicensedLetterCandidate` دون أي كسر.
- **Path B** (`TypedCodePoint → SlotGeometry`): مستقل تماماً، ولا تمسّه
  هذه الوثيقة لا من قريب ولا من بعيد.
- **Path C** (محتمل مستقبلاً: `PhoneticCandidate + UnicodeGlyphCandidate
  → BridgedLetterCandidate`): **يُفتَح إمكانه** دستورياً بهذه الوثيقة،
  ولا يُلزَم تنفيذه. الدستور يحكم إن نُفِّذ، ولا يطلب تنفيذاً.

لا cross-dependency بين المسارات الثلاثة؛ المقارنة مسموحة، الدمج
الوظيفي ممنوع كما هو منصوص في الدستور المزدوج.

---

## § ٩ — حالة التنفيذ

- **حالة دستورية:** مُعلَنة بهذه الوثيقة.
- **حالة تنفيذية:** **لا runtime في هذا الـ PR**.

أي تنفيذ مستقبلي يجب أن:

1. يُفتَح في PR منفصل **بعد** دمج هذا الدستور
   (قاعدة *constitutional PR sequencing*).
2. يلتزم بسلسلة الطبقات: `Candidate → Gate → Evidence → Domain → Rank →
   Residuals → Trace` (مذكرة *layer contract invariants*).
3. لا يلامس Path A ولا Path B القائمين، ولا يُعدّل سلوكهما.
4. يستخدم بادئات الشواهد العربية حصراً (مذكرة *evidence*).
5. يحترم سقوف الرتب المذكورة في §٥-٣ ولا يدّعي يقيناً يفوق الشاهد
   الأضعف.

---

## § ١٠ — ملخص القوانين الثلاثة

هذه هي القوانين الثلاثة الوحيدة المُستخلَصة من المقترح الأصلي والمعتمدة
دستورياً في هذه الوثيقة:

1. **قانون الاستقلال الطبقي**
   `PhoneticCandidate` طبقة قائمة بذاتها، لا تساوي `LetterCandidate`،
   ولا تُستنبط من Unicode، ولا تُنتج معنى أو حكماً.

2. **قانون تخفيض Unicode**
   Unicode شاهد كتابي (`OrthographicEvidence`)، ليس هويةً صوتية ولا
   مصدراً للمخرج/الصفة، ورتبته شاهدية لا حكمية.

3. **قانون التركيب الثنائي للحرف**
   `LetterCandidate` المركّب (`BridgedLetterCandidate`) لا يتولّد إلا
   بعبور بوابة `EvidenceBridge` التي تجمع شاهداً صوتياً مرخّصاً وشاهداً
   كتابياً مرخّصاً ضمن نظام عبور معلَن.

---

## ملحق — ما استُبعد من المقترح الأصلي

للشفافية الدستورية، استُبعدت البنود التالية ولا تُعدّ جزءاً من هذا
الدستور:

- ❌ `ArticulatoryPossibility`, `MakhrajSpaceCarrier`,
  `MakhrajSlotGeometry` — مكرّرة أو متعارضة مع `MakhrajAlgebra` و
  `SlotGeometry` القائمين.
- ❌ `Γ_phonetic` / `Λ_phonetic` — تتعدّى على نمط `Γ_haraka` القائم
  بلا مسوّغ مستقل.
- ❌ "٥ فضاءات مخرج" — تخالف `ArabicMakhrajPlaceOrder` المخزّن
  (٨ مواضع داخل نظام معلَن).
- ❌ بند "Implementation requires future PRs" — يحوّل الدستور إلى
  خارطة طريق ملزمة، وهو مخالف لقاعدة تسلسل الدساتير
  (*constitutional PR sequencing*).
