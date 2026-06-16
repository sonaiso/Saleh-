# SENTENCE_GEOMETRY_CONSTITUTION — SCG-P9 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P9 layer.
> Authored under the **narrow SCG-P8–P12 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no actual i‘rab
> judgment, no ifadah, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p9_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `AMIL_MAMUL_CONSTITUTION.md` (SCG-P8, immediate predecessor);
> the SCG-P8–P12 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P9_SENTENCE_GEOMETRY` |
| LayerSpec name | `SentenceGeometryLayer` |
| Phase | `SCG-P9` |
| Output type | `SentenceGeometryCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p9_specified_registry`); P10–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — spatial organization of relations, not a grammatical verdict

SCG-P9 organizes عامل–معمول relations into a **sentence geometry** — a spatial
arrangement (إسناد، نعت، حال، معطوف، مفعولية) — as a **candidate-only**
structural composition (إمكان هندسة جملية). It opens a sentence-shape hypothesis;
it does **not** decide sentence *type* as a judgment, assign i‘rab, or assert
ifadah.

```
شرط التفريع: قابلية علاقات العامل-المعمول للتنظيم الهندسي ضمن بنية الجملة.
```

**Boundary note.** "Geometry" here is *structural arrangement of relation
candidates*, not a grammatical ruling about the sentence. Sentence-type evidence
is recorded as evidence, never closed into a verdict; i‘rab and ifadah remain
strictly downstream and candidate-only.

## 3. Required upstream evidence (consumed)

SCG-P9's **direct input is `AmilMamulCandidate`** (origin = `P8_AMIL_MAMUL`).
Required evidence:

- `AmilMamulCandidate` (direct input from SCG-P8)
- preserved identities (P9 preserves `amil_mamul_candidate_identities`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **sentence-type + isnad-boundary evidence** (conditions:
  `amil_mamul_candidates_ready`, `sentence_boundary_closed`)

`minimum_required_fields = (amil_mamul_refs, sentence_type_evidence, isnad_boundary_evidence)`

## 4. Allowed output

- **`SentenceGeometryCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
RelationGeometryCandidate      (SCG-P10)
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · IrabCandidate · CaseJudgment
```

## 6. What P9 must NOT do (structural-only discipline — the key P9 boundary)

P9 is **specification of required evidence + prohibitions only**. It must NOT:

- assign **i‘rab** or **judge a case** (`IrabCandidate` / `CaseJudgment` forbidden)
- assert **ifadah** / speech force (`IfadahCandidate` forbidden)
- emit any **final judgment**, `RealityClaim`, `FinalMeaning`, `HukmCandidate`
- (`forbidden_changes = assign_irab / assign_case / assign_ifadah`)

The spec may only define **what evidence a future `SentenceGeometryCandidate`
would require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = AmilMamulCandidate` (SCG-P8) — the **only** upstream path is
  `P8 → P9`. Any skip into P10+ is structurally impossible.
- `target_boundary_opens = (relation_geometry_candidates,)` — **opened as a
  prior for SCG-P10**, never **produced** by P9.
- `forbidden_direct_next_layer_ids = (SCG-P12,)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = amil_mamul_candidate_identities`.
- **Explicit residuals / no silent failure:** `blockers = (sentence_structure_blocked,)`;
  `invalidating_differences = (sentence_type_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; arrangement opened, no verdict closed.
- **No i‘rab / no case / no ifadah / no hukm:** §5 + §6.

## 9. Status discipline

- `build_p9_specified_registry` advances **only P9** `PLANNED → SPECIFIED`
  (building on `build_p8_specified_registry`); P10–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p9_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p9_specified.py` (`P9-SPEC-*`).
