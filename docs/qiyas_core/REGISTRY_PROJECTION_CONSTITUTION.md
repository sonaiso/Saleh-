# REGISTRY_PROJECTION_CONSTITUTION — SCG-P2 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P2 layer.
> Authored under the **narrow SCG-P2-only spec-authoring authorization
> (2026-06-15)**. SPEC ONLY — **no runtime, no adapter, no IMPLEMENTED status.**
> Transition authored: `PLANNED → SPECIFIED` via `build_p2_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 (canonical phases) / §7
> (REC queue) / §8 (supreme law); `LAYER_REGISTRY.md`; the SCG-P2-only
> authorization. Canonical registry track only — **not** the runtime syllable
> track (`LicensedSyllableCandidate` etc., a different numbering — do not
> conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P2_REGISTRY_PROJECTION` |
| LayerSpec name | `RegistryProjectionLayer` |
| Phase | `SCG-P2` |
| Output type | `RegistryProjectionCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p2_specified_registry`); P3–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه)

SCG-P2 **projects a licensed `SlotCandidate` onto the relevant phase registry
to OPEN potential morphological/syntactic priors** — *"Prior لا Judgment."* It
is a **candidate-only** projection. It opens hypotheses; it does not decide them.

```
شرط التفريع: قابلية مرشح الخانة للإسقاط على سجل ترخيص لفتح Prior لا Judgment.
```

## 3. Upstream evidence (consumed)

Per §8 ("a layer consumes only the licensed output of its immediate
predecessor"), SCG-P2's **direct input is `SlotCandidate`** (origin =
`P1_SLOT_CANDIDATE`). `SlotCandidate` is itself the licensed convergence of the
SCG-P1 atomic/sequence proofs, whose identities it preserves and which P2 may
reference only through it:

- `SlotCandidate` (direct input)
- `LetterIdentityCarrier` — via SlotCandidate's preserved identity refs
- `HarakaMarkIdentityCarrier` — via SlotCandidate's preserved identity refs
- `PositionCarrier` — via SlotCandidate
- `ConditionedTypedSequence` / `AlignmentEvidence` — via SlotCandidate
- residual / boundary evidence — as already preserved upstream

P2 does **not** re-derive any P1 identity; it consumes the converged
`SlotCandidate` and preserves `slot_candidate_identity`.

## 4. Allowed output

- **`RegistryProjectionCandidate` only.** Nothing else.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

P2 must NOT produce any downstream output type (no-jump), nor any final
semantic/judgment artifact:

```text
RootStemCandidate            (SCG-P3)
JamidMushtaqCandidate        (SCG-P4)
MufradWordCandidate          (SCG-P5)
VerbalSignifiedCandidate     (SCG-P6)
CompositionReadinessCandidate(SCG-P7)
AmilMamulCandidate           (SCG-P8)
SentenceGeometryCandidate    (SCG-P9)
RelationGeometryCandidate    (SCG-P10)
IrabGeometryCandidate        (SCG-P11)
IfadahCandidate              (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning   (absolute — every layer)
```

Also forbidden as *claims/changes*: meaning, dalalah, tafsir, i'rab judgment,
root, wazn, wordhood, grammar, hukm, semantic runtime (`forbidden_changes =
assign_root / assign_meaning / assign_irab`).

## 6. No-jump discipline

- `target_boundary_opens = (root_stem_candidates, word_type_priors)` — these are
  **opened as priors for SCG-P3**, never **produced** by P2.
- `forbidden_direct_next_layer_ids = (SCG-P6, SCG-P8, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).
- P3 (`RootStemCandidate`) has `origin = RegistryProjectionCandidate`, so any
  `SCG-P1 → SCG-P3` path necessarily skips P2 and is structurally invalid.

## 7. Invariants preserved (spec level)

- **Identity ≠ trace; identity not consumed:** `preserves_ids =
  slot_candidate_identity`.
- **Explicit residuals / no silent failure:** `blockers =
  (slot_candidate_blocked,)`; `invalidating_differences =
  (registry_membership_conflict,)`.
- **Candidate-only, not final judgment:** output is a `…Candidate`; absolutes
  forbidden; "Prior لا Judgment."
- **No semantic / no root-wazn-word / no i'rab:** §5 forbidden outputs + changes.
- **Rank meet / potential-only:** no rank upgrade; nothing promoted.

## 8. Status discipline

- `build_p2_specified_registry` advances **only P2** `PLANNED → SPECIFIED`
  (building on `build_p1_specified_registry`); P3–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p2_implemented_registry`.** `IMPLEMENTED` is **not** authorized
  while the global REC freeze is ACTIVE; advancing P2 to `IMPLEMENTED` requires
  a separate, explicit, narrow authorization (and P1 IMPLEMENTED first).

Enforced by `tests/qiyas_core/test_master_registry_p2_specified.py` (`P2-SPEC-*`).
