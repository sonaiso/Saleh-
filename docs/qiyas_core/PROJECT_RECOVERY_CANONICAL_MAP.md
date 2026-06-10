# PROJECT_RECOVERY_CANONICAL_MAP — خريطة الاسترداد القانونية للمشروع

> **Status:** Constitutional — governance only. This document contains **no
> implementation** (ولا تحتوي تنفيذًا). It is the single recovery reference
> that ends the state of "تشعب قبل تثبيت المرجعية الواحدة" (branching before
> fixing a single reference authority).
>
> **Evidence rule (قاعدة الدليل):** the word **PASS** is never used in this
> document without `file path + symbol + line` evidence. Claims about the
> `Binary-` repository are read-only knowledge transfers under
> `CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md` §3, taken at commit
> `ff472cdc8adc082a96598fef04b5c9c62943a0ff`. Claims about `Saleh-` are taken
> from the working tree at `main` ancestor `2243e9a`.

---

## 1. Freeze Declaration — إعلان التجميد

**PROJECT FREEZE is in effect** until this map and its corrective queue
(§7, items REC-1 … REC-4) are merged and approved by the maintainer.

While the freeze holds, the following are **forbidden** in both repositories:

```text
لا PR-D جديد.
لا P1 runtime.
لا YAML implementation.
لا Lambert W.
لا metrics.
لا HarakaFunction.
لا LetterIdentity runtime.
— حتى تكتمل الخريطة.
```

| Frozen item | Meaning | Current state (evidence) |
| --- | --- | --- |
| New PR-D | No new domain/feature PR streams | Open PRs: #121 (docs-only snapshot, explicitly "do not merge"), #120 (third-party draft). No other streams may open. |
| P1 runtime | No new runtime work on P1 layers | P1 layers are registry-status SPECIFIED only — `build_p1_specified_registry`, file: `src/qiyas_core/slot_geometry_core/master_registry_seed.py`, symbol: `build_p1_specified_registry`, line: 1238. They must not advance. |
| YAML implementation | No `slot_geometry_yaml` package, no schema runtime | PASS (absence verified): no `schemas/**` files, no `examples/**` files, no `src/qiyas_core/slot_geometry_yaml/` package exist on `main`; no open YAML PR (two PR searches returned 0 results). |
| Lambert W | No transcendental-function machinery | PASS (absence verified): `Lambert|lambert` matches only third-party `.venv` pygments builtins; zero matches in `src/`, `tests/`, `docs/`. |
| Metrics | No measurement/metrics expansion | No metrics package exists under `src/qiyas_core/` beyond the already-merged logarithmic measurement carriers (`src/qiyas_core/logarithmic_measurement.py`, symbol: `LicensedMeasuredQuantity`, line: 64). |
| HarakaFunction | The name and the layer are suspended (تُعلَّق) | file: `src/qiyas_core/slot_geometry_core/master_registry_seed.py`, symbol: `name="HarakaFunctionCarrierLayer"`, line: 283; file: `src/qiyas_core/haraka_function_adapter.py`, symbol: `class HarakaFunctionLayerAdapter`, line: 39. See §6. |
| LetterIdentity runtime | No further runtime work on letter identity | file: `src/qiyas_core/letter_identity_adapter.py`, symbol: `class LetterIdentityLayerAdapter`, line: 103 — frozen as-is until the map closes. |

**Freeze release condition:** the freeze lifts only by explicit maintainer
instruction after REC-1 … REC-4 of §7 are merged.

---

## 2. Repository Responsibility Matrix — مصفوفة مسؤولية المستودعات

| Repository | Responsibility (الحد) | Explicitly NOT responsible for |
| --- | --- | --- |
| `Binary-` | Encoding / Unicode / WrittenSurface / SyllableBridgeExport **فقط** | أي طبقة عربية: حركة، إعراب، جذر، وزن، مقطع، عروض، صرف، صوتيات |
| `Saleh-` | `qiyas_core` (kernel, adapters, rules) + `slot_geometry_core` (MasterLayerRegistry, LayerSpec, Gamma, TargetBoundary, MinimumCompletion, IdentityInheritance) — العمود الفقري الجبري | حمل أصوات/ترميز ثنائي (هذا حد Binary-)؛ الطبقات العربية الدلالية النهائية قبل تأسيسها دستوريًا |
| Arabic (future package/repo — لم يبدأ دستوريًا) | الدال وحده، المدلول اللفظي، المدلول الوضعي، الكلمة، التركيب، المنطوق، المفهوم | البدء قبل اكتمال هذه الخريطة + Canonical Registry + YAML schema |

**Cross-repository law:** knowledge moves between repositories **read-only**
(`docs/qiyas_core/CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md` §3); cross-writing is
forbidden (FORBIDDEN-01 … FORBIDDEN-08, same document §4, lines 92–107). Any
PR that uses knowledge from the other repository must embed a Knowledge
Transfer Record (§5, line 111).

**Status judgment (recorded as maintainer ruling):**

```text
Binary-  : قريب من الإغلاق كـ Foundation — لكنه يجب ألا يحمل العربية.
Saleh-   : يملك نواة جيدة — لكنه يحتاج تصحيح خريطة وتسميات.
Arabic   : لم يبدأ دستوريًا — ويجب ألا يبدأ قبل Canonical Map + YAML.
```

---

## 3. Three Foundational Origins — الأصول الثلاثة

Every layer in the whole project must trace to exactly one of these origins.
A layer that cannot be traced is **out of project** or **experimental**.

```text
الأصل الأول  : صوت بشري عربي محفوظ الأثر.
              (A human Arabic sound whose trace is preserved.)

الأصل الثاني : نظام لفظي عربي يحفظ انتقالات الصوت.
              (An Arabic verbal system that preserves the sound's transitions.)

الأصل الثالث : مدلول وضعي — ثبات كيان أو علاقة نُقل إلى لفظ.
              (A conventional signified — the stability of an entity or
               relation transferred into an utterance.)
```

**Tracing rule (قانون الإسناد):**

```text
كل طبقة بلا أصل من هذه الأصول الثلاثة = خارج المشروع أو تجريبية.
No layer without one of the three origins.
```

| Origin | Which repository serves it | Examples of layers it licenses |
| --- | --- | --- |
| الأصل الأول (preserved sound trace) | `Binary-` foundation carries only the *written/encoded trace*; the Arabic domain will carry the sound origin itself | BF0 encoding layers; future AR-P0 voice/verbal origin layers |
| الأصل الثاني (verbal system preserving transitions) | `Saleh-` algebraic spine (qiyas transitions, slot geometry) | SCG phases: TypedCodePoint…SlotCandidate ladders |
| الأصل الثالث (conventional signified) | Arabic future package/repo only | المدلول الوضعي، الكلمة، التركيب، المنطوق، المفهوم |

This section is registry-binding: the Canonical Layer Registry correction
(REC-2 in §7) must add an `origin` traceability note for every layer.

---

## 4. Canonical Layer Phases — الأطوار القانونية للطبقات

### 4.1 Phase-prefix disambiguation (fixing the P0 collision)

A naming collision exists today: `Saleh-` uses the phase string
`"P0_BINARY_FOUNDATION"` (file:
`src/qiyas_core/slot_geometry_core/master_registry_seed.py`, symbol:
`phase="P0_BINARY_FOUNDATION"`, lines: 107, 143, 191) while `Binary-` holds
the actual binary foundation as registry layers `L00…L04` (file:
`src/binary_core/slot_geometry_core.py`, symbol: `FOUNDATION_REGISTRY`,
read-only). Two different things share the name "binary foundation."

**Constitutional disambiguation (binding):**

```text
BF0    = Binary Foundation            (Binary- repository: L00…L04)
SCG-P0 = SlotGeometry Core phase 0    (Saleh- repository: Unicode/TypedCodePoint/Glyph)
AR-P0  = Arabic Voice/Verbal Origin   (future Arabic package/repo)

Declared: Binary-P0 ≠ Arabic-SCG-P0.
```

### 4.2 Canonical phase ladder (as currently seeded in Saleh-)

Single source: `src/qiyas_core/slot_geometry_core/master_registry_seed.py`
(layer-ID constants, symbol block `LAYER_ID_*`, lines 42–87; builder
`build_master_registry_seed`, line 1098). After REC-2, these phases carry the
`SCG-` prefix.

| Phase (current string) | Canonical prefix after REC-2 | Layers (name=, line) |
| --- | --- | --- |
| `P0_BINARY_FOUNDATION` | `SCG-P0` (renamed away from "BINARY_FOUNDATION" wording) | UnicodeCandidateLayer:106, TypedCodePointLayer:142, GlyphClassificationLayer:190 |
| `P1_DAL_ALONE_ATOMIC` | `SCG-P1` | LetterIdentityCarrierLayer:237, HarakaFunctionCarrierLayer:283 (suspended — §6), ConditionedTypedSequenceLayer:329, PositionCarrierLayer:378, SlotCandidateLayer:422 |
| `P2_REGISTRY_PROJECTION` | `SCG-P2` | RegistryProjectionLayer:494 |
| `P3_ROOT_STEM_CLOSURE` | `SCG-P3` | RootStemClosureLayer:551 |
| `P4_JAMID_MUSHTAQ` | `SCG-P4` | JamidMushtaqLayer:610 |
| `P5_MUFRAD_WORD_CONTRACTS` | `SCG-P5` | MufradWordContractsLayer:662 |
| `P6_VERBAL_SIGNIFIED_ALONE` | `SCG-P6` | VerbalSignifiedAloneLayer:720 |
| `P7_COMPOSITION_READINESS` | `SCG-P7` | CompositionReadinessLayer:774 |
| `P8_AMIL_MAMUL` | `SCG-P8` | AmilMamulLayer:829 |
| `P9_SENTENCE_GEOMETRY` | `SCG-P9` | SentenceGeometryLayer:886 |
| `P10_RELATION_GEOMETRY` | `SCG-P10` | RelationGeometryLayer:940 |
| `P11_IRAB_GEOMETRY` | `SCG-P11` | IrabGeometryLayer:993 |
| `P12_IFADAH_SPEECH_FORCE` | `SCG-P12` | IfadahSpeechForceLayer:1047 |

### 4.3 Phase/status discipline

Layer lifecycle is governed by `LayerStatus`
(file: `src/qiyas_core/slot_geometry_core/layer_spec.py`, symbol:
`class LayerStatus`, line: 23):

```text
PLANNED → SPECIFIED → IMPLEMENTED → AUDITED → CLOSED
```

Current registry truth:

- SCG-P0 layers are IMPLEMENTED via `build_p0_implemented_registry`
  (file: `src/qiyas_core/slot_geometry_core/master_registry_seed.py`,
  symbol: `build_p0_implemented_registry`, line: 1193) with implementation
  sources mapped in `_P0_IMPLEMENTATION_SOURCES` (lines 1184–1190).
- SCG-P1 layers are SPECIFIED only via `build_p1_specified_registry`
  (same file, line: 1238); its non-goals explicitly state
  "هذه الدالة لا تُنفِّذ HarakaFunctionCarrier runtime" (line: 1259).
- SCG-P2 … SCG-P12 layers are PLANNED in `build_master_registry_seed`
  (line: 1098).
- The absolute forbidden outputs remain registry-guarded:
  `_ABSOLUTE_FORBIDDEN = ("HukmCandidate", "RealityClaim", "FinalMeaning")`
  (same file, symbol: `_ABSOLUTE_FORBIDDEN`, line: 93).

---

## 5. Current Assets Inventory — جرد الأصول الحالية

> All PASS marks below satisfy the evidence rule:
> `file path + symbol + line`.

```text
Repository: Binary-
Role: Encoding / Unicode / WrittenSurface / SyllableBridgeExport foundation فقط.
Canonical boundary: FOUNDATION_BOUNDARY = "L04_SYLLABLE_BRIDGE_EXPORT"
  (file: src/binary_core/slot_geometry_core.py, symbol: FOUNDATION_BOUNDARY).
Implemented layers: exactly five, all LayerStatus.IMPLEMENTED, registered in
  FOUNDATION_REGISTRY (file: src/binary_core/slot_geometry_core.py):
    L00_BINARY                  → BinaryCarrier
    L01_BYTE_SEQUENCE           → ByteSequenceCarrier
    L02_UNICODE_CODEPOINT       → UnicodeCodePointCarrier
    L03_WRITTEN_SURFACE         → WrittenSurfaceCarrier
    L04_SYLLABLE_BRIDGE_EXPORT  → SyllableBridgeExportCarrier
      (L04 branch_reason: "Binary- foundation stops here; linguistic
       analysis belongs to external systems")
Out-of-scope layers: declared INTENTIONALLY UNREGISTERED beyond the boundary
  (same file, comment above FOUNDATION_BOUNDARY): GammaHaraka, LambdaHaraka,
  Integration, IrabCandidate, WaznCandidate, SyllableCandidate, ArudCandidate,
  PhonemCandidate, MorphologyCandidate.
Dangerous overlaps: 15 Arabic/linguistic modules live inside src/binary_core/
  although they are outside the foundation boundary:
    gamma_haraka.py, gamma_role_spectrum.py, haraka_carrier.py,
    haraka_operation.py, lambda_haraka.py, lambda_licensing.py,
    integration.py, irab_candidate.py, wazn_candidate.py, root_candidate.py,
    root_eligibility.py, morphology_candidate.py, phoneme_candidate.py,
    syllable_candidate.py, arud_candidate.py
  and src/binary_core/__init__.py exports Arabic-domain symbols
  (HarakaRoleHypothesis, HarakaRoleSpectrum, IntegratedLinguisticCandidate,
   IrabCandidate, IrabCandidateBridge, IrabHypothesis,
   LambdaHarakaLicensingBridge).
Required corrections: quarantine/relocate the 15 overlap modules out of the
  Binary- foundation surface (REC-4 in §7 — executed inside Binary- by the
  maintainer; cross-writing from Saleh- is FORBIDDEN per
  CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md §4). Binary- then closes as
  Foundation: BF0 = L00…L04 only.
```

```text
Repository: Saleh-
Role: algebraic spine — qiyas_core kernel + slot_geometry_core registry law.
Core packages:
  src/qiyas_core/                  — kernel + layer adapters + rules
    QiyasKernel                    (file: src/qiyas_core/kernel.py, symbol: class QiyasKernel, line: 70)
    UnicodeLayerAdapter            (file: src/qiyas_core/unicode_adapter.py, line: 33)
    TypedCodePointLayerAdapter     (file: src/qiyas_core/typed_codepoint_adapter.py, line: 154)
    GlyphClassification            (file: src/qiyas_core/registries/glyph_classification_registry.py, line: 94)
    LetterIdentityLayerAdapter     (file: src/qiyas_core/letter_identity_adapter.py, line: 103)
    HarakaFunctionLayerAdapter     (file: src/qiyas_core/haraka_function_adapter.py, line: 39) — suspended name, §6
    ConditionedTypedSequenceLayerAdapter (file: src/qiyas_core/conditioned_typed_sequence_adapter.py, line: 75)
    PositionLayerAdapter           (file: src/qiyas_core/position_adapter.py, line: 30)
    SlotLayerAdapter               (file: src/qiyas_core/slot_adapter.py, line: 117)
    SlotGeometryLayerAdapter       (file: src/qiyas_core/slot_geometry_adapter.py, line: 213)
    HarakaRoleSpectrumLayerAdapter (file: src/qiyas_core/haraka_role_spectrum_adapter.py, line: 301)
  src/qiyas_core/slot_geometry_core/ — constitutional contracts
    MasterLayerRegistry            (file: .../master_layer_registry.py, line: 26)
    LayerSpec                      (file: .../layer_spec.py, line: 69)
    LayerStatus                    (file: .../layer_spec.py, line: 23)
    GammaStatus / GammaResult      (file: .../gamma.py, lines: 27 / 45)
    TargetBoundary                 (file: .../target_boundary.py, line: 36)
    MinimumCompletionSpec          (file: .../minimum_completion.py, line: 37)
    IdentityInheritance            (file: .../identity_inheritance.py, line: 24)
    RegistryEntry                  (file: .../registry_entry.py, line: 45)
Master registries:
  build_master_registry_seed       (file: .../master_registry_seed.py, line: 1098) — 19 layers, SCG-P0…SCG-P12
  build_p0_implemented_registry    (same file, line: 1193) — P0 → IMPLEMENTED
  build_p1_specified_registry      (same file, line: 1238) — P1 → SPECIFIED only
Dangerous names:
  HarakaFunctionCarrierLayer       (file: .../master_registry_seed.py, line: 283)
  HarakaFunctionLayerAdapter       (file: src/qiyas_core/haraka_function_adapter.py, line: 39)
  phase="P0_BINARY_FOUNDATION"     (file: .../master_registry_seed.py, lines: 107, 143, 191) — collides with Binary- BF0
Required corrections: REC-1, REC-2, REC-3 in §7 (matrix doc, phase
  re-prefixing, HarakaFunction → HarakaMarkIdentity naming correction with
  TERMINOLOGY_MAP conversion table).
```

**Verified absences in Saleh- `main` (freeze-relevant):**

- PASS (absence): no YAML schema — glob `schemas/**` → no files; glob
  `examples/**` → no files; no `src/qiyas_core/slot_geometry_yaml/` package.
- PASS (absence): no Lambert W machinery — repository-wide grep matches only
  `.venv` pygments builtins.
- PASS (absence): no open YAML PR — PR searches for `slot_geometry_yaml` and
  `YAML` returned 0 results.

**Experimental holdings (not canonical, untouched by this map):**
`experimental/qiyas_core/` (17 adapters + `rules/` + `slot/` subpackage),
`experimental/data/sources/arabic_alphabet_makharij.csv`, root-level
`run_qiyas.py`. Governed by `RESET_CONSTITUTION.md` §7 — promotion forbidden.

---

## 6. Dangerous Names / Misbounded Layers — أسماء خطرة وطبقات خارج حدها

### 6.1 `HarakaFunctionCarrier` — suspended (معلَّقة)

**Ruling (verbatim):**

```text
الحركة أولًا علامة ذات هوية.
ثم لاحقًا قد تصير وظيفة، بعد Gate وسياق وتركيب.
```

The name "HarakaFunctionCarrier" asserts *function* at the atomic-identity
stage, which jumps a gate. The correct name at this stage is
**`HarakaMarkIdentityCarrier`** (mark identity first; function only later,
after gate + context + composition).

Occurrences that the corrective rename (REC-3) must cover, with a
TERMINOLOGY_MAP-style conversion table:

| Occurrence | file | symbol | line(s) |
| --- | --- | --- | --- |
| Registry layer | `src/qiyas_core/slot_geometry_core/master_registry_seed.py` | `name="HarakaFunctionCarrierLayer"` / `output_type="HarakaFunctionCarrier"` | 283 / 290; references also at 168, 261, 352, 402, 431, 1259 |
| Runtime adapter | `src/qiyas_core/haraka_function_adapter.py` | `class HarakaFunctionLayerAdapter` | 39 (refs at 2, 4, 9–11, 44, 70, 79, 113, 126) |
| Rules | `src/qiyas_core/rules/haraka_function_rules.py` | rule definitions | 13–19, 45, 47, 61, 129 |
| Guards | `src/qiyas_core/forbidden_outputs.py` | forbidden-output references | 59, 120, 126, 203 |
| Proof machinery | `src/qiyas_core/recursive_proof.py` | references | 9, 211, 238, 276 |
| Downstream refs | `src/qiyas_core/slot_adapter.py` (7, 123), `src/qiyas_core/letter_identity_adapter.py` (8, 111), `src/qiyas_core/haraka_role_spectrum_adapter.py` (10, 323, 418), `src/qiyas_core/conditioned_typed_sequence_adapter.py` (7, 17), `src/qiyas_core/phonetics/__init__.py` (3), `src/qiyas_core/rules/__init__.py` (71), `src/qiyas_core/rules/slot_rules.py` (5) | imports/claims | as listed |

Until REC-3 merges, the layer is **suspended**: no runtime work, no new
references, no status advancement.

### 6.2 `P0_BINARY_FOUNDATION` phase string — naming collision

`Saleh-` phase string `"P0_BINARY_FOUNDATION"` (master_registry_seed.py lines
107, 143, 191) collides with the true binary foundation in `Binary-`
(BF0 = L00…L04). Resolved by §4.1 prefixes (`BF0` / `SCG-P0` / `AR-P0`) via
REC-2. Declared now: **Binary-P0 ≠ Arabic-SCG-P0**.

### 6.3 Misbounded Arabic layers inside `Binary-`

The 15 modules listed in §5 (`gamma_haraka.py` … `arud_candidate.py`) are
Arabic/linguistic layers living inside the encoding repository. They are
already excluded from `FOUNDATION_REGISTRY` ("INTENTIONALLY UNREGISTERED"),
but their presence in `src/binary_core/` blurs the repository boundary:

```text
لو بقيت العربية كلها داخل Binary، سيفسد معنى Binary.
```

Correction is REC-4 (executed inside `Binary-` by the maintainer).

### 6.4 Names already guarded (no action needed)

`HukmCandidate`, `RealityClaim`, `FinalMeaning` are registry-forbidden —
file: `src/qiyas_core/slot_geometry_core/master_registry_seed.py`, symbol:
`_ABSOLUTE_FORBIDDEN`, line: 93. PASS (guard exists).

---

## 7. Corrective PR Queue — طابور التصحيحات

Ordered queue. Each item is docs/registry governance first; **no runtime
implementation enters the queue before REC-5 closes.** The mandated order is:

```text
1. Project Recovery Canonical Map   (this document — REC-0)
2. Repository Responsibility Matrix (REC-1)
3. Canonical Layer Registry         (REC-2)
4. Naming Correction Plan           (REC-3)
5. YAML Schema                      (REC-5)
6. Runtime                          (لاحقًا — after the above only)
```

| # | PR | Scope | Non-goals |
| --- | --- | --- | --- |
| REC-0 | This map | Adds `docs/qiyas_core/PROJECT_RECOVERY_CANONICAL_MAP.md` only | No code, no rename, no registry change |
| REC-1 | Responsibility Matrix doc + enforcement tests | Promote §2 into `REPOSITORY_RESPONSIBILITY_MATRIX.md`, cross-linked from `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` and `LAYER_REGISTRY.md`; convert the boundaries into tests (`tests/qiyas_core/test_repository_responsibility_matrix.py`, `REC1-*`) — maintainer ruling 2026-06-10: "ليس كوثيقة كلامية فقط. يجب أن يحوّل الحدود إلى اختبارات" | No runtime implementation, no registry change, no rename, no Binary- edits; the freeze is not lifted |
| REC-2 | Canonical Layer Registry alignment | Apply §4.1 prefixes (`BF0`/`SCG-P0`/`AR-P0`) to phase strings in `master_registry_seed.py` and `LAYER_REGISTRY.md`; add origin-traceability notes (§3) per layer | No new layers, no status advancement |
| REC-3 | Naming Correction Plan + rename | `HarakaFunctionCarrier` → `HarakaMarkIdentityCarrier` across the §6.1 occurrence table, with a TERMINOLOGY_MAP conversion table (per `TERMINOLOGY_MAP.md` policy); keep Arabic claim prefixes verbatim | No semantic change to gates/ranks; no new function claims |
| REC-4 | Binary- boundary enforcement | Recorded requirement only (this repo): quarantine/relocate the 15 overlap modules out of `src/binary_core/`; performed **in Binary- by the maintainer** — cross-write from Saleh- is FORBIDDEN (bridge §4) | Saleh- makes no edits to Binary- |
| REC-5 | YAML Schema | `slot_geometry` YAML schema as the validated source for LayerSpecs — only after REC-1…REC-4 | No runtime execution of YAML |
| REC-6 | Runtime resumption | Lift freeze items one layer at a time under §8 law | Nothing outside the single approved layer |

A PR not in this queue, or out of this order, is rejected while the freeze
holds.

**Queue status (recorded by REC-1, 2026-06-10, maintainer ruling):**

```text
REC-0 : DONE — merged as PR #122 (governance map only; not enforcement).
REC-1 : the only admissible next PR — matrix doc + REC1-* enforcement tests.
REC-2 : BLOCKED until REC-1 merges.
REC-3 : BLOCKED until REC-2 merges.
REC-4 : BLOCKED until REC-3 merges (maintainer-only, inside Binary-).
YAML / Runtime / Metrics / Lambert W / P1 : BLOCKED.
```

---

## 8. Future Execution Rule — قانون التنفيذ المستقبلي

**قانون التشغيل الأعلى (Supreme Operating Law):**

```text
لا تنفيذ قبل الخريطة.
لا خريطة بلا أصول.
لا طبقة بلا Origin/Branch.
لا Branch بلا قياس (Qiyas).
لا Qiyas بلا Boundary.
لا Boundary بلا MinimumCompletion.
لا Gamma بلا Target.
لا Runtime بلا YAML مصدّق.
لا PR بلا موقع في Master Registry.
```

**القانون الختامي (Final Law):**

```text
لا تبنِ طبقة جديدة حتى تعرف:
في أي مستودع؟      (which repository — §2)
تحت أي أصل؟        (which of the three origins — §3)
في أي Phase؟       (which canonical phase — §4)
بأي LayerSpec؟     (which registered LayerSpec — §5)
بأي YAML؟          (which validated schema — REC-5)
وبأي Gamma target؟ (which TargetBoundary — slot_geometry_core/target_boundary.py:36)
```

**Execution gate checklist** — every future layer PR must answer all six
questions above in its description, cite its `RegistryEntry`
(file: `src/qiyas_core/slot_geometry_core/registry_entry.py`, symbol:
`class RegistryEntry`, line: 45), and execute **one layer only**
(تنفيذ طبقة واحدة فقط). Anything else is rejected.
