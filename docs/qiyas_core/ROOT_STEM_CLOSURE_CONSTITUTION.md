# ROOT_STEM_CLOSURE_CONSTITUTION — SCG-P3 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P3 layer.
> Authored under the **narrow SCG-P3-only spec-authoring authorization
> (2026-06-15)**. SPEC ONLY — **no runtime, no adapter, no root extraction, no
> IMPLEMENTED status.** Transition authored: `PLANNED → SPECIFIED` via
> `build_p3_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `REGISTRY_PROJECTION_CONSTITUTION.md` (SCG-P2, immediate predecessor);
> the SCG-P3-only authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P3_ROOT_STEM_CLOSURE` |
| LayerSpec name | `RootStemClosureLayer` |
| Phase | `SCG-P3` |
| Output type | `RootStemCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p3_specified_registry`); P4–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه) — structural possibility, not extraction

SCG-P3 **closes a root/stem *possibility* (إمكان جذر/ساق)** from a sequence of
licensed slot candidates **via structural sequence-conditioning evidence**. It
is a **candidate-only** structural closure. It **opens** a root/stem hypothesis;
it does **not** extract, infer, or decide a root.

```
شرط التفريع: قابلية تسلسل مرشحات الخانات لتكوين إمكان جذر أو ساق مرخّص.
```

**This is الأصل الثاني (structure), not الأصل الثالث (lexical root/meaning).**
"Root/stem" here is a *geometric structural candidate over slots* — **not** a
lexical root, **not** a morphological derivation, **not** a wazn.

## 3. Required upstream evidence (consumed)

Per §8 (a layer consumes only its immediate predecessor's licensed output),
SCG-P3's **direct input is `RegistryProjectionCandidate`** (origin =
`P2_REGISTRY_PROJECTION`). Required evidence:

- `RegistryProjectionCandidate` (direct input from SCG-P2)
- preserved identity-carrier references (via the projection's preserved
  `slot_candidate_identity` chain — P3 preserves `slot_candidate_identities`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **projection evidence** showing *why* a root/stem hypothesis is opened
  (conditions: `registry_projection_established`, `slot_sequence_consistent`)

P3 does **not** re-derive any P1/P2 identity; it consumes the projection and
preserves the slot-candidate identities.

## 4. Allowed output

- **`RootStemCandidate` only** — a candidate (إمكان), never a judgment.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

P3 must NOT produce any downstream output type (no-jump), nor any final
semantic/judgment artifact:

```text
JamidMushtaqCandidate         (SCG-P4)
MufradWordCandidate           (SCG-P5)
VerbalSignifiedCandidate      (SCG-P6)
CompositionReadinessCandidate (SCG-P7)
AmilMamulCandidate            (SCG-P8)
SentenceGeometryCandidate     (SCG-P9)
RelationGeometryCandidate     (SCG-P10)
IrabGeometryCandidate         (SCG-P11)
IfadahCandidate               (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning · MeaningCandidate · WordTypeJudgment
```

## 6. What P3 must NOT do (structural-only discipline — the key P3 boundary)

P3 is **specification of required evidence + prohibitions only**. It must NOT:

- extract or infer a **root** (no root extraction runtime)
- emit a **final root judgment**
- assign **wazn** (وزن)
- perform any **morphology** runtime
- claim **wordhood**, **lexical meaning**, **grammar**, **i'rab judgment**,
  **dalalah**, **tafsir**, **hukm**, semantic runtime, `RealityClaim`,
  `FinalMeaning`
- (`forbidden_changes = assign_meaning / assign_irab / assign_case`)

The spec may only define **what evidence a future `RootStemCandidate` would
require** (`slot_sequence_refs`, `root_pattern_evidence`, `stem_boundary_evidence`)
and **what it must never claim**.

## 7. No-jump discipline

- `origin = RegistryProjectionCandidate` (SCG-P2) — the **only** upstream path
  is `P2 RegistryProjectionCandidate → P3 RootStemCandidate`. A direct
  `P1 → P3` (or any skip into P4+) is structurally impossible.
- `target_boundary_opens = (jamid_mushtaq_candidates, word_pattern_candidates)`
  — **opened as priors for SCG-P4**, never **produced** by P3.
- `forbidden_direct_next_layer_ids = (SCG-P8, SCG-P9, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = slot_candidate_identities`.
- **Explicit residuals / no silent failure:** `blockers = (root_pattern_blocked,)`;
  `invalidating_differences = (root_pattern_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes forbidden; no final root judgment.
- **No semantic / no root extraction / no wazn / no word / no i'rab:** §5 + §6.

## 9. Status discipline

- `build_p3_specified_registry` advances **only P3** `PLANNED → SPECIFIED`
  (building on `build_p2_specified_registry`); P4–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p3_implemented_registry`.** `IMPLEMENTED` is **not** authorized
  while the global REC freeze is ACTIVE; advancing P3 to `IMPLEMENTED` requires
  a separate, explicit, narrow authorization (and P1/P2 IMPLEMENTED first).

Enforced by `tests/qiyas_core/test_master_registry_p3_specified.py` (`P3-SPEC-*`).
