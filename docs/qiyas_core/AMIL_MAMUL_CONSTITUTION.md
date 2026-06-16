# AMIL_MAMUL_CONSTITUTION — SCG-P8 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P8 layer.
> Authored under the **narrow SCG-P8–P12 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no actual i‘rab
> judgment, no case assignment, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p8_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `COMPOSITION_READINESS_CONSTITUTION.md` (SCG-P7, immediate predecessor);
> the SCG-P8–P12 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P8_AMIL_MAMUL` |
| LayerSpec name | `AmilMamulLayer` |
| Phase | `SCG-P8` |
| Output type | `AmilMamulCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p8_specified_registry`); P9–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — operator–operand relation possibility, not case judgment

SCG-P8 proves an **عامل–معمول (operator–operand) relation as a possibility** —
إسناد / تقييد / توكيد — as a **candidate-only** structural relation
(إمكان علاقة عامل-معمول). It opens a governance-relation hypothesis; it does
**not** assign i‘rab, decide a case, or deliver any final grammatical judgment.

```
شرط التفريع: قابلية وحدتين مستعدتين للتركيب لتكوين علاقة عامل-معمول مرخّصة.
```

**Boundary note (critical — the case-governance tier begins here).** In Arabic
grammar an عامل *governs* a case on its معمول. SCG-P8 attests only that a
*relation candidate* exists between an operator and an operand — it must **never**
compute, assign, or judge the resulting case. Case/i‘rab judgment is downstream
(SCG-P11 maps i‘rab *geometry*, still as candidates), and a *final* case
decision is forbidden everywhere in Saleh-.

## 3. Required upstream evidence (consumed)

SCG-P8's **direct input is `CompositionReadinessCandidate`** (origin =
`P7_COMPOSITION_READINESS`). Required evidence:

- `CompositionReadinessCandidate` (direct input from SCG-P7)
- preserved identities (P8 preserves `composition_readiness_identities`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **relation-class + domain evidence** (conditions:
  `composition_readiness_established`, `amil_identified`, `mamul_identified`)

`minimum_required_fields = (amil_ref, mamul_ref, relation_class_evidence, domain_evidence)`

## 4. Allowed output

- **`AmilMamulCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
SentenceGeometryCandidate      (SCG-P9)
RelationGeometryCandidate      (SCG-P10)
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · IrabCandidate · CaseJudgment · SentenceCandidate
```

## 6. What P8 must NOT do (structural-only discipline — the key P8 boundary)

P8 is **specification of required evidence + prohibitions only**. It must NOT:

- **assign i‘rab** or **judge a case** (`CaseJudgment` / `IrabCandidate` forbidden)
- build a **sentence** or assign a **sentence type**
- emit any **final judgment**, `RealityClaim`, `FinalMeaning`, `HukmCandidate`
- (`forbidden_changes = assign_irab / assign_case / assign_sentence_type`)

The spec may only define **what evidence a future `AmilMamulCandidate` would
require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = CompositionReadinessCandidate` (SCG-P7) — the **only** upstream path
  is `P7 → P8`. Any skip into P9+ is structurally impossible.
- `target_boundary_opens = (sentence_geometry_candidates,)` — **opened as a
  prior for SCG-P9**, never **produced** by P8.
- `forbidden_direct_next_layer_ids = (SCG-P11, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = composition_readiness_identities`.
- **Explicit residuals / no silent failure:** `blockers = (amil_mamul_relation_blocked,)`;
  `invalidating_differences = (amil_class_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; relation proven, case never judged.
- **No i‘rab / no case / no sentence / no hukm:** §5 + §6.

## 9. Status discipline

- `build_p8_specified_registry` advances **only P8** `PLANNED → SPECIFIED`
  (building on `build_p7_specified_registry`); P9–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p8_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p8_specified.py` (`P8-SPEC-*`).
