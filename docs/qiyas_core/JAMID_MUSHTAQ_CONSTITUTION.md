# JAMID_MUSHTAQ_CONSTITUTION — SCG-P4 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P4 layer.
> Authored under the **narrow SCG-P4–P7 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no root extraction, no
> wazn assignment, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p4_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `ROOT_STEM_CLOSURE_CONSTITUTION.md` (SCG-P3, immediate predecessor);
> the SCG-P4–P7 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P4_JAMID_MUSHTAQ` |
| LayerSpec name | `JamidMushtaqLayer` |
| Phase | `SCG-P4` |
| Output type | `JamidMushtaqCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p4_specified_registry`); P5–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — structural classification possibility, not extraction

SCG-P4 **classifies a root/stem possibility as جامد (non-derived) or مشتق
(derived)** — as a **candidate-only** structural classification (إمكان تصنيف).
It opens a derivation-class hypothesis; it does **not** extract a root, decide a
wazn, or assert a final word-type judgment.

```
شرط التفريع: قابلية إمكان الجذر للتصنيف إلى جامد أو مشتق بناءً على دليل النمط.
```

**This is الأصل الثاني (structure), not الأصل الثالث (lexical/morphological
derivation).** "Jamid/Mushtaq" here is a *structural classification over a root
candidate* — **not** a morphological derivation, **not** a wazn, **not** a
lexical meaning.

## 3. Required upstream evidence (consumed)

Per §8 (a layer consumes only its immediate predecessor's licensed output),
SCG-P4's **direct input is `RootStemCandidate`** (origin =
`P3_ROOT_STEM_CLOSURE`). Required evidence:

- `RootStemCandidate` (direct input from SCG-P3)
- preserved identity-carrier references (P4 preserves
  `root_stem_candidate_identity`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **derivation-pattern evidence** showing *why* a jamid/mushtaq class is opened
  (condition: `root_stem_candidate_established`)

P4 does **not** re-derive any P1/P2/P3 identity; it consumes the root/stem
candidate and preserves its identity.

`minimum_required_fields = (root_stem_ref, derivation_class_evidence, pattern_evidence)`

## 4. Allowed output

- **`JamidMushtaqCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

P4 must NOT produce any downstream output type (no-jump), nor any final
semantic/judgment artifact:

```text
MufradWordCandidate            (SCG-P5)
VerbalSignifiedCandidate       (SCG-P6)
CompositionReadinessCandidate  (SCG-P7)
AmilMamulCandidate             (SCG-P8)
SentenceGeometryCandidate      (SCG-P9)
RelationGeometryCandidate      (SCG-P10)
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · WordTypeJudgment · MeaningCandidate · IrabCandidate
```

## 6. What P4 must NOT do (structural-only discipline — the key P4 boundary)

P4 is **specification of required evidence + prohibitions only**. It must NOT:

- **extract or infer a root** (no root extraction runtime)
- **assign a wazn** (وزن) — no morphological pattern decision
- emit a **final word-type judgment** (`WordTypeJudgment`)
- claim **lexical meaning**, **dalalah**, **grammar**, **i'rab judgment**,
  **hukm**, semantic runtime, `RealityClaim`, `FinalMeaning`
- (`forbidden_changes = assign_meaning / assign_irab / assign_case`)

The spec may only define **what evidence a future `JamidMushtaqCandidate` would
require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = RootStemCandidate` (SCG-P3) — the **only** upstream path is
  `P3 RootStemCandidate → P4 JamidMushtaqCandidate`. Any skip into P5+ is
  structurally impossible.
- `target_boundary_opens = (word_type_candidates,)` — **opened as a prior for
  SCG-P5**, never **produced** by P4.
- `forbidden_direct_next_layer_ids = (SCG-P8, SCG-P9, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = root_stem_candidate_identity`.
- **Explicit residuals / no silent failure:** `blockers = (derivation_pattern_blocked,)`;
  `invalidating_differences = (derivation_classification_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; no final classification judgment.
- **No root extraction / no wazn / no meaning / no i'rab:** §5 + §6.

## 9. Status discipline

- `build_p4_specified_registry` advances **only P4** `PLANNED → SPECIFIED`
  (building on `build_p3_specified_registry`); P5–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p4_implemented_registry`.** `IMPLEMENTED` is **not** authorized
  while the global REC freeze is ACTIVE; advancing P4 to `IMPLEMENTED` requires
  a separate, explicit, narrow authorization.

Enforced by `tests/qiyas_core/test_master_registry_p4_specified.py` (`P4-SPEC-*`).
