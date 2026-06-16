# RELATION_GEOMETRY_CONSTITUTION — SCG-P10 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P10 layer.
> Authored under the **narrow SCG-P8–P12 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no actual i‘rab
> judgment, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p10_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `SENTENCE_GEOMETRY_CONSTITUTION.md` (SCG-P9, immediate predecessor);
> the SCG-P8–P12 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P10_RELATION_GEOMETRY` |
| LayerSpec name | `RelationGeometryLayer` |
| Phase | `SCG-P10` |
| Output type | `RelationGeometryCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p10_specified_registry`); P11–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — internal relation geometry, not a syntactic verdict

SCG-P10 maps the **internal relations between sentence components** — تبعية،
عطف، إبدال، توكيد — as a **candidate-only** structural geometry
(إمكان هندسة علاقات). It opens an internal-dependency hypothesis; it does
**not** deliver a final syntactic judgment, assign i‘rab, or assert ifadah.

```
شرط التفريع: قابلية الهندسة الجملية لتحديد علاقات المكونات داخل الجملة هندسيًا.
```

**Boundary note.** Dependency/relation mapping here is *geometric possibility*
over component candidates — never a final parse, never a grammatical ruling.

## 3. Required upstream evidence (consumed)

SCG-P10's **direct input is `SentenceGeometryCandidate`** (origin =
`P9_SENTENCE_GEOMETRY`). Required evidence:

- `SentenceGeometryCandidate` (direct input from SCG-P9)
- preserved identity (P10 preserves `sentence_geometry_identity`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **relation-type + dependency-scope evidence** (conditions:
  `sentence_geometry_established`, `relation_scope_closed`)

`minimum_required_fields = (sentence_geometry_ref, relation_type_evidence, dependency_scope_evidence)`

## 4. Allowed output

- **`RelationGeometryCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · IrabCandidate · CaseJudgment
```

## 6. What P10 must NOT do (structural-only discipline — the key P10 boundary)

P10 is **specification of required evidence + prohibitions only**. It must NOT:

- assign **i‘rab** or **judge a case** (`IrabCandidate` / `CaseJudgment` forbidden)
- assert **ifadah** / speech force (`IfadahCandidate` forbidden)
- emit any **final syntactic judgment**, `RealityClaim`, `FinalMeaning`, `HukmCandidate`
- (`forbidden_changes = assign_irab / assign_case / assign_ifadah`)

The spec may only define **what evidence a future `RelationGeometryCandidate`
would require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = SentenceGeometryCandidate` (SCG-P9) — the **only** upstream path is
  `P9 → P10`. Any skip into P11+ is structurally impossible.
- `target_boundary_opens = (irab_geometry_candidates,)` — **opened as a prior
  for SCG-P11**, never **produced** by P10.
- `forbidden_direct_next_layer_ids = (SCG-P12,)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = sentence_geometry_identity`.
- **Explicit residuals / no silent failure:** `blockers = (relation_structure_blocked,)`;
  `invalidating_differences = (relation_type_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; relations mapped, no parse closed.
- **No i‘rab / no case / no ifadah / no hukm:** §5 + §6.

## 9. Status discipline

- `build_p10_specified_registry` advances **only P10** `PLANNED → SPECIFIED`
  (building on `build_p9_specified_registry`); P11–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p10_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p10_specified.py` (`P10-SPEC-*`).
