# REPOSITORY_RESPONSIBILITY_MATRIX — مصفوفة مسؤولية المستودعات

> **Type:** Constitutional governance document — **REC-1** of the corrective queue
> (`PROJECT_RECOVERY_CANONICAL_MAP.md` §7).
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §2, promoted into this
> standalone document per the queue item REC-1; maintainer instruction
> (2026-06-10): *"REC-1: Repository Responsibility Matrix Enforcement —
> لكن ليس كوثيقة كلامية فقط. يجب أن يحوّل الحدود إلى اختبارات."*
>
> **Enforcement:** `tests/qiyas_core/test_repository_responsibility_matrix.py`
> (REC1-\* tests). This matrix is therefore not file evidence only — it is
> file evidence + test enforcement.
>
> **Cross-repository basis:** `CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md` §3–§6.

---

## 1. The Matrix — المصفوفة

| Repository | Responsibility (الحد) | Explicitly NOT responsible for |
| --- | --- | --- |
| `Binary-` | Encoding / Unicode / WrittenSurface / SyllableBridgeExport **فقط** | أي طبقة عربية: حركة، إعراب، جذر، وزن، مقطع، عروض، صرف، صوتيات |
| `Saleh-` | `qiyas_core` (kernel, adapters, rules) + `slot_geometry_core` (MasterLayerRegistry, LayerSpec, Gamma, TargetBoundary, MinimumCompletion, IdentityInheritance) — العمود الفقري الجبري | حمل أصوات/ترميز ثنائي (هذا حد Binary-)؛ الطبقات العربية الدلالية النهائية قبل تأسيسها دستوريًا |
| Arabic (future package/repo — لم يبدأ دستوريًا) | الدال وحده، المدلول اللفظي، المدلول الوضعي، الكلمة، التركيب، المنطوق، المفهوم | البدء قبل اكتمال هذه الخريطة + Canonical Registry + YAML schema |

**Status judgment (recorded as maintainer ruling, verbatim):**

```text
Binary-  : قريب من الإغلاق كـ Foundation — لكنه يجب ألا يحمل العربية.
Saleh-   : يملك نواة جيدة — لكنه يحتاج تصحيح خريطة وتسميات.
Arabic   : لم يبدأ دستوريًا — ويجب ألا يبدأ قبل Canonical Map + YAML.
```

---

## 2. Cross-Repository Law — قانون ما بين المستودعات

```text
القراءة المتبادلة مسموحة.
الكتابة المتبادلة ممنوعة.
النقل البرمجي أو الدستوري لا يتم إلا بسجل نقل معرفة.
```

- Knowledge moves between repositories **read-only**
  (`CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md` §3 — ReadOnlyKnowledgeBridge).
- Cross-writing is forbidden: FORBIDDEN-01 … FORBIDDEN-08
  (same document §4, lines 92–107).
- Any PR that uses knowledge from the other repository must embed a
  **Knowledge Transfer Record** (same document §5, line 111).
- No runtime dependency, no shared kernel, no shared dataclass
  (FORBIDDEN-05, FORBIDDEN-06, FORBIDDEN-07).

---

## 3. Enforcement in Saleh- — تحويل الحدود إلى اختبارات

Per the maintainer ruling, the boundaries above are converted into tests in
`tests/qiyas_core/test_repository_responsibility_matrix.py`:

| Test group | What it proves |
| --- | --- |
| `REC1-MAP-*` | `PROJECT_RECOVERY_CANONICAL_MAP.md` exists, declares the freeze (§1), the corrective queue and its rejection law (§7), the release condition, and the `HarakaFunctionCarrier` suspension (§6.1). |
| `REC1-FREEZE-*` | The freeze holds in the working tree, not only in the document: no `src/qiyas_core/slot_geometry_yaml/` runtime package, no `examples/` tree, no Lambert W machinery in `src/`, no metrics package beyond the merged logarithmic measurement carriers, and no registry builder advances any P1 layer beyond `SPECIFIED`. **REC-5 narrow lift:** `schemas/slot_geometry/` is admitted as the validated LayerSpec source (YAML files only); no other `schemas/*` subtree and no runtime YAML loader are permitted. |
| `REC1-BOUNDARY-*` | `Saleh-` does not attempt to modify or absorb `Binary-`: no `binary_core` import in `src/` or `tests/`, no `src/binary_core/` package hosted here, no sibling `Binary-` working-tree path references, no dependency declaration on `Binary-`. |
| `REC1-KTR-*` | Any cross-repository knowledge requires a Knowledge Transfer Record: the bridge document exists, declares cross-read allowed / cross-write forbidden, enumerates FORBIDDEN-01 … FORBIDDEN-08, and defines the required KTR fields. |
| `REC1-MATRIX-*` | This document exists, matches the map §2 boundaries, is cross-linked from `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` §12 and `LAYER_REGISTRY.md`, and does not lift the freeze. |

### Binary--side enforcement is NOT performed here

The matrix obligations inside `Binary-` (the foundation export must not export
Arabic-domain symbols; the extended Arabic modules must not appear in the
foundation `__init__`; the foundation boundary is L04 only) are **REC-4**
scope, executed **in `Binary-` by the maintainer only**. Cross-write from
`Saleh-` is FORBIDDEN (`CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md` §4,
FORBIDDEN-04 / FORBIDDEN-08; `PROJECT_RECOVERY_CANONICAL_MAP.md` §5, §7
REC-4).

---

## 4. Freeze Preservation — هذه الوثيقة لا ترفع التجميد

This document **does not lift the freeze**. PROJECT FREEZE remains in effect
(`PROJECT_RECOVERY_CANONICAL_MAP.md` §1): the freeze lifts only by explicit
maintainer instruction after REC-1 … REC-4 are merged.

```text
REC-0   : DONE — merged as PR #122 (governance map only).
REC-1   : DONE — this document + the REC1-* enforcement tests (PR #134).
REC-2   : DONE — Canonical Layer Registry alignment, SCG- phase prefixes
          + §3 origin notes (PR #136).
REC-3   : DONE — Naming Correction Plan, HarakaFunctionCarrier →
          HarakaMarkIdentityCarrier (PR #137).
REC-4   : PENDING — Binary- boundary enforcement, executed inside Binary-
          by the maintainer only (cross-write from Saleh- is FORBIDDEN);
          recorded on the Saleh- side, no Saleh- implementation required.
REC-5   : DONE — validated LayerSpec schema merged under the REC-5 narrow
          freeze lift (PR #138); a runtime YAML loader remains forbidden.
REC-6   : BLOCKED — Runtime resumption, layer-by-layer, only by explicit
          maintainer authorization after REC-1 … REC-5.
YAML runtime / Runtime / Metrics / Lambert W / P1 : BLOCKED.
The global REC freeze remains ACTIVE; REC-3 and REC-5 being complete does not
lift it. Layer 5+ remains blocked pending a separate maintainer authorization.
```

### 4.1 Narrow Layer 4 authorization (2026-06-13)

Maintainer Hussein Hiyassat explicitly authorized **Layer 4
`LicensedSyllableCandidate` runtime as a potential-only slice**, ahead of
the full REC-1 … REC-5 sequence (`src/qiyas_core/licensed_syllable.py`).
This is a single explicit per-layer narrow authorization — it is not a
global REC freeze release.

```text
Authorized narrowly:
  * Layer 4 LicensedSyllableCandidate runtime (potential-only)
  * BoundaryEvidence consumption by Layer 4 (read-only from
    qiyas_core.analysis_trace; not promoted to a standalone runtime layer)
  * SyllableShapeEvidence / PhoneticEconomyEvidence /
    SyllableInvalidationEvidence (Layer 4 evidence types, potential-only)

Still BLOCKED (no narrow exception granted):
  * Layer 5 and above
  * semantic runtime
  * meaning / hukm / i'rab / dalalah / tafsir / reality claim
  * WordCandidate / LafzCandidate / DalalahCandidate / HukmCandidate /
    FinalMeaning / RealityClaim
  * source importer
  * registry admission outside Layer 4
  * YAML / Lambert W / metrics / global P1 runtime advancement
  * Binary- writes from Saleh-
  * global REC freeze release until REC-1 … REC-4 merged
```

Layer 4 candidates carry `runtime_status="potential_only_not_semantic_runtime"`
and the analysis bundle records
`meaning_status=hukm_status=irab_status=reality_status="not_introduced"`.

---

## 5. Non-Goals — ما لا تفعله هذه الوثيقة

```text
This document does not change the master registry.
This document does not rename any layer (the HarakaFunction rename is REC-3).
This document does not re-prefix any phase string (re-prefixing is REC-2).
This document does not add runtime implementation, YAML, metrics, or Lambert W.
This document does not edit Binary- (REC-4 is maintainer-only, inside Binary-).
This document does not lift the freeze.
```

---

**Document Version:** 1.0
**Authority:** Constitutional governance document (REC-1)
**Last Updated:** 2026-06-13
