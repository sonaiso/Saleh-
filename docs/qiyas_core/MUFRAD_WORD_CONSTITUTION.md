# MUFRAD_WORD_CONSTITUTION — SCG-P5 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P5 layer.
> Authored under the **narrow SCG-P4–P7 spec-authoring authorization
> (2026-06-16)**. SPEC ONLY — **no runtime, no adapter, no lexical-word claim,
> no word-meaning claim, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p5_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `JAMID_MUSHTAQ_CONSTITUTION.md` (SCG-P4, immediate predecessor);
> the SCG-P4–P7 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P5_MUFRAD_WORD_CONTRACTS` |
| LayerSpec name | `MufradWordContractsLayer` |
| Phase | `SCG-P5` |
| Output type | `MufradWordCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p5_specified_registry`); P6–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — single-word *contract* possibility, not lexical wordhood

SCG-P5 forms a **single-word (مفرد) structural contract** — a minimum-completion
possibility classifying a unit as اسم / فعل / حرف — as a **candidate-only**
structural closure (إمكان كلمة مفردة). It opens a word-shaped contract; it does
**not** assert lexical wordhood, dictionary identity, or meaning.

```
شرط التفريع: قابلية إمكان الجامد/المشتق للانضمام إلى عقد كلمة مفردة محددة النوع.
```

**Boundary note (critical).** Lexical wordhood and word *meaning* belong to
**الأصل الثالث (the future Arabic package)**, NOT to Saleh-. SCG-P5 produces only
a *structural* mufrad-word contract over the upstream candidate — **not** a
lexical entry, **not** a definition, **not** a meaning.

## 3. Required upstream evidence (consumed)

SCG-P5's **direct input is `JamidMushtaqCandidate`** (origin =
`P4_JAMID_MUSHTAQ`). Required evidence:

- `JamidMushtaqCandidate` (direct input from SCG-P4)
- preserved identity (P5 preserves `jamid_mushtaq_candidate_identity`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **word-class + word-boundary evidence** (conditions:
  `jamid_mushtaq_established`, `word_boundary_closed`)

`minimum_required_fields = (root_stem_ref, word_class_evidence, word_boundary_evidence)`

## 4. Allowed output

- **`MufradWordCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

```text
VerbalSignifiedCandidate       (SCG-P6)
CompositionReadinessCandidate  (SCG-P7)
AmilMamulCandidate             (SCG-P8)
SentenceGeometryCandidate      (SCG-P9)
RelationGeometryCandidate      (SCG-P10)
IrabGeometryCandidate          (SCG-P11)
IfadahCandidate                (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · IrabCandidate · CaseEffect · SentenceCandidate
```

## 6. What P5 must NOT do (structural-only discipline — the key P5 boundary)

P5 is **specification of required evidence + prohibitions only**. It must NOT:

- claim **lexical wordhood** or a **dictionary entry** (الأصل الثالث boundary)
- claim **word meaning** / **dalalah** / **tafsir**
- assign **i'rab**, **case**, or build a **sentence**
- emit any **final judgment**, `RealityClaim`, `FinalMeaning`, `HukmCandidate`
- (`forbidden_changes = assign_irab / assign_case / assign_meaning`)

The spec may only define **what evidence a future `MufradWordCandidate` would
require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = JamidMushtaqCandidate` (SCG-P4) — the **only** upstream path is
  `P4 → P5`. Any skip into P6+ is structurally impossible.
- `target_boundary_opens = (verbal_signified_candidates, composition_readiness_candidates)`
  — **opened as priors for SCG-P6/P7**, never **produced** by P5.
- `forbidden_direct_next_layer_ids = (SCG-P9, SCG-P11, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = jamid_mushtaq_candidate_identity`.
- **Explicit residuals / no silent failure:** `blockers = (word_type_ambiguity_blocking,)`;
  `invalidating_differences = (word_class_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; no final word judgment.
- **No lexical wordhood / no meaning / no i'rab / no case:** §5 + §6.

## 9. Status discipline

- `build_p5_specified_registry` advances **only P5** `PLANNED → SPECIFIED`
  (building on `build_p4_specified_registry`); P6–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p5_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE.

Enforced by `tests/qiyas_core/test_master_registry_p5_specified.py` (`P5-SPEC-*`).
