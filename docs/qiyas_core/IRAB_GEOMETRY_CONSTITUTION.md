# IRAB_GEOMETRY_CONSTITUTION — SCG-P11 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P11 layer.
> Authored under the **narrow SCG-P8–P12 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, NO actual i‘rab
> judgment, NO final case decision, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p11_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `RELATION_GEOMETRY_CONSTITUTION.md` (SCG-P10, immediate predecessor);
> the SCG-P8–P12 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P11_IRAB_GEOMETRY` |
| LayerSpec name | `IrabGeometryLayer` |
| Phase | `SCG-P11` |
| Output type | `IrabGeometryCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p11_specified_registry`); P12 remains `PLANNED` |

## 2. Role (الفرع وسببه) — geometry of i‘rab *positions*, never an i‘rab judgment

SCG-P11 maps the **geometry of i‘rab** — the i‘rab *positions* and their
*possibilities* (المواضع الإعرابية وإمكاناتها) — as **candidates, not rulings**.
It opens i‘rab-position hypotheses based on operator / locus / marker evidence;
it does **not** issue an i‘rab judgment, decide a case, or finalize anything.

```
شرط التفريع: قابلية هندسة العلاقات لحمل إمكانات الإعراب بناءً على العامل والمحل والعلامة.
```

**Boundary note (the most judgment-adjacent layer in Saleh-).** This layer names
*where* i‘rab could fall and *what* it could be — as geometry of possibilities.
It must **never** assert that a token *is* marfū‘/manṣūb/majrūr/majzūm as a
verdict. A final i‘rab/case decision (`IrabFinalDecision`, `CaseJudgment`) and
any hukm are forbidden here and everywhere in Saleh-. `forbidden_changes`
explicitly blocks `assign_case_judgment`, `assign_ifadah`, and `assign_hukm`.

## 3. Required upstream evidence (consumed)

SCG-P11's **direct input is `RelationGeometryCandidate`** (origin =
`P10_RELATION_GEOMETRY`). Required evidence:

- `RelationGeometryCandidate` (direct input from SCG-P10)
- preserved identity (P11 preserves `relation_geometry_identity`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **i‘rab-position + case-marker + waqf-readiness evidence** (conditions:
  `relation_geometry_established`, `irab_context_closed`)

`minimum_required_fields = (relation_geometry_ref, irab_position_evidence, case_marker_evidence, waqf_readiness_evidence)`

## 4. Allowed output

- **`IrabGeometryCandidate` only** — a candidate (إمكان موضع إعرابي), never a
  judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · CaseJudgment · IrabFinalDecision
```

## 6. What P11 must NOT do (structural-only discipline — the key P11 boundary)

P11 is **specification of required evidence + prohibitions only**. It must NOT:

- issue an **i‘rab judgment** or a **final case decision**
  (`IrabFinalDecision` / `CaseJudgment` forbidden)
- assert **ifadah** / speech force (`IfadahCandidate` forbidden)
- emit any **hukm**, `RealityClaim`, `FinalMeaning`
- (`forbidden_changes = assign_case_judgment / assign_ifadah / assign_hukm`)

The spec may only define **what evidence a future `IrabGeometryCandidate` would
require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = RelationGeometryCandidate` (SCG-P10) — the **only** upstream path is
  `P10 → P11`. Any skip is structurally impossible.
- `target_boundary_opens = (ifadah_speech_force_candidates,)` — **opened as a
  prior for SCG-P12**, never **produced** by P11.
- `forbidden_direct_next_layer_ids = ()` — P11 → P12 is the single licensed
  forward edge; the downstream output `IfadahCandidate` is in `forbidden_outputs`.

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = relation_geometry_identity`.
- **Explicit residuals / no silent failure:** `blockers = (irab_context_blocked,)`;
  `invalidating_differences = (irab_position_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes + `IrabFinalDecision` forbidden; i‘rab geometry mapped, never judged.
- **No i‘rab judgment / no case decision / no ifadah / no hukm:** §5 + §6.

## 9. Status discipline

- `build_p11_specified_registry` advances **only P11** `PLANNED → SPECIFIED`
  (building on `build_p10_specified_registry`); P12 stays `PLANNED`; layer
  count stays **19**.
- **No `build_p11_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p11_specified.py` (`P11-SPEC-*`).
