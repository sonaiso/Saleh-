# COMPOSITION_READINESS_CONSTITUTION — SCG-P7 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P7 layer.
> Authored under the **narrow SCG-P4–P7 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no actual composition,
> no realized isnad, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p7_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `VERBAL_SIGNIFIED_CONSTITUTION.md` (SCG-P6, immediate predecessor);
> the SCG-P4–P7 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P7_COMPOSITION_READINESS` |
| LayerSpec name | `CompositionReadinessLayer` |
| Phase | `SCG-P7` |
| Output type | `CompositionReadinessCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p7_specified_registry`); P8–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — readiness gate, not composition itself

SCG-P7 proves that verbal units **satisfy the preconditions to enter a
composition (تركيب)** — manifest structure, possible isnad, closed boundaries —
as a **candidate-only** readiness gate (إمكان استعداد التركيب). It opens a
composition possibility; it does **not** form a composition, realize an isnad,
or relate an عامل to a معمول.

```
شرط التفريع: قابلية المدلول اللفظي للانضمام في تركيب نحوي عبر بوابة الاستعداد.
```

**Boundary note.** Readiness ≠ composition. P7 attests *eligibility* only.
Actual عامل–معمول relation is SCG-P8; sentence structure is SCG-P9. P7 must
never cross into either.

## 3. Required upstream evidence (consumed)

SCG-P7's **direct input is `VerbalSignifiedCandidate`** (origin =
`P6_VERBAL_SIGNIFIED_ALONE`). Required evidence:

- `VerbalSignifiedCandidate` (direct input from SCG-P6)
- preserved identities (P7 preserves `verbal_signified_candidate_identities`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **composition-boundary + isnad-readiness evidence** (conditions:
  `verbal_signified_established`, `composition_boundary_closed`)

`minimum_required_fields = (verbal_signified_refs, composition_boundary_evidence, isnad_readiness_evidence)`

## 4. Allowed output

- **`CompositionReadinessCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
AmilMamulCandidate             (SCG-P8)
SentenceGeometryCandidate      (SCG-P9)
RelationGeometryCandidate      (SCG-P10)
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · IrabCandidate · CaseEffect · SentenceCandidate
```

## 6. What P7 must NOT do (structural-only discipline — the key P7 boundary)

P7 is **specification of required evidence + prohibitions only**. It must NOT:

- form an **actual composition** or realize an **isnad** (only attest readiness)
- prove an **عامل–معمول** relation (that is SCG-P8)
- build a **sentence** or assign **i'rab** / **case**
- emit any **final judgment**, `RealityClaim`, `FinalMeaning`, `HukmCandidate`
- (`forbidden_changes = assign_irab / assign_case / assign_meaning`)

The spec may only define **what evidence a future `CompositionReadinessCandidate`
would require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = VerbalSignifiedCandidate` (SCG-P6) — the **only** upstream path is
  `P6 → P7`. Any skip into P8+ is structurally impossible.
- `target_boundary_opens = (amil_mamul_candidates,)` — **opened as a prior for
  SCG-P8**, never **produced** by P7.
- `forbidden_direct_next_layer_ids = (SCG-P11, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = verbal_signified_candidate_identities`.
- **Explicit residuals / no silent failure:** `blockers = (composition_precondition_blocked,)`;
  `invalidating_differences = (composition_readiness_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; readiness attested, never composition.
- **No actual composition / no isnad realized / no i'rab / no case:** §5 + §6.

## 9. Status discipline

- `build_p7_specified_registry` advances **only P7** `PLANNED → SPECIFIED`
  (building on `build_p6_specified_registry`); P8–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p7_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p7_specified.py` (`P7-SPEC-*`).
