# VERBAL_SIGNIFIED_CONSTITUTION — SCG-P6 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P6 layer.
> Authored under the **narrow SCG-P4–P7 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no lexical meaning, no
> dalalah closure, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p6_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `MUFRAD_WORD_CONSTITUTION.md` (SCG-P5, immediate predecessor);
> the SCG-P4–P7 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P6_VERBAL_SIGNIFIED_ALONE` |
| LayerSpec name | `VerbalSignifiedAloneLayer` |
| Phase | `SCG-P6` |
| Output type | `VerbalSignifiedCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p6_specified_registry`); P7–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — verbal signified *alone*, never the meaning itself

SCG-P6 isolates the **verbal signified (المدلول اللفظي) *alone*** as a
**candidate-only** structural possibility — the *lafẓī* signified separated from
lexical meaning and grammatical judgment. It opens a signified possibility
(إمكان مدلول لفظي يُفيد إمكان المعنى دون إغلاقه); it does **not** close,
decide, or assert the meaning.

```
شرط التفريع: قابلية إمكان الكلمة المفردة لحمل مدلول لفظي يُفيد إمكان المعنى دون إغلاقه.
```

**Boundary note (critical — the most meaning-adjacent layer in PR A).** "Verbal
signified" is the *structural* carrier of signification possibility, **not**
dalalah, **not** lexical meaning, **not** tafsir. Meaning closure belongs to
**الأصل الثالث**, not Saleh-. The word "signified" here must never be read as a
meaning claim — it is structural possibility *opened*, never *closed*.

## 3. Required upstream evidence (consumed)

SCG-P6's **direct input is `MufradWordCandidate`** (origin =
`P5_MUFRAD_WORD_CONTRACTS`). Required evidence:

- `MufradWordCandidate` (direct input from SCG-P5)
- preserved identity (P6 preserves `mufrad_word_candidate_identity`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **signified-class + verbal-identity evidence** (condition:
  `mufrad_word_established`)

`minimum_required_fields = (mufrad_word_ref, signified_class_evidence, verbal_identity_evidence)`

## 4. Allowed output

- **`VerbalSignifiedCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
CompositionReadinessCandidate  (SCG-P7)
AmilMamulCandidate             (SCG-P8)
SentenceGeometryCandidate      (SCG-P9)
RelationGeometryCandidate      (SCG-P10)
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · IrabCandidate · CaseEffect · SentenceCandidate · MeaningJudgment
```

## 6. What P6 must NOT do (structural-only discipline — the key P6 boundary)

P6 is **specification of required evidence + prohibitions only**. It must NOT:

- **close lexical meaning** or produce `MeaningJudgment` / **dalalah** / **tafsir**
- assign **i'rab**, **case**, or build a **sentence**
- emit any **final judgment**, `RealityClaim`, `FinalMeaning`, `HukmCandidate`
- (`forbidden_changes = assign_meaning / assign_irab / assign_case`)

The spec may only define **what evidence a future `VerbalSignifiedCandidate`
would require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = MufradWordCandidate` (SCG-P5) — the **only** upstream path is
  `P5 → P6`. Any skip into P7+ is structurally impossible.
- `target_boundary_opens = (composition_readiness_candidates,)` — **opened as a
  prior for SCG-P7**, never **produced** by P6.
- `forbidden_direct_next_layer_ids = (SCG-P9, SCG-P11, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = mufrad_word_candidate_identity`.
- **Explicit residuals / no silent failure:** `blockers = (verbal_signified_ambiguity_blocking,)`;
  `invalidating_differences = (signified_class_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; meaning opened, never closed.
- **No meaning closure / no dalalah / no i'rab / no case:** §5 + §6.

## 9. Status discipline

- `build_p6_specified_registry` advances **only P6** `PLANNED → SPECIFIED`
  (building on `build_p5_specified_registry`); P7–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p6_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p6_specified.py` (`P6-SPEC-*`).
