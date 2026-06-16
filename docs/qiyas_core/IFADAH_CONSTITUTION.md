# IFADAH_CONSTITUTION — SCG-P12 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P12 layer —
> the **terminal** phase of the canonical SCG spine. Authored under the **narrow
> SCG-P8–P12 spec-authoring authorization (2026-06-16)**. SPEC ONLY — **no
> runtime, no adapter, NO reality claim, NO truth value, NO hukm, no final
> meaning, no IMPLEMENTED status.** Transition authored:
> `PLANNED → SPECIFIED` via `build_p12_specified_registry`.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 / §7 / §8;
> `IRAB_GEOMETRY_CONSTITUTION.md` (SCG-P11, immediate predecessor);
> the SCG-P8–P12 authorization. Canonical SCG registry track only — **not**
> the runtime syllable track (do not conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P12_IFADAH_SPEECH_FORCE` |
| LayerSpec name | `IfadahSpeechForceLayer` |
| Phase | `SCG-P12` |
| Output type | `IfadahCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p12_specified_registry`); **terminal** — opens nothing |

## 2. Role (الفرع وسببه) — speech-force *possibility*, never a reality/truth claim

SCG-P12 builds an **ifadah (speech-force) possibility** — خبر / إنشاء / طلب —
as a **candidate-only** speech-force hypothesis (إمكان إفادة كلامية). It opens a
speech-force candidate for the مخاطب; it does **not** decide truth, map reality,
issue a hukm, or close a final meaning.

```
شرط التفريع: قابلية هندسة الإعراب المُغلَقة لحمل قوة كلامية محتملة تُفيد المخاطب.
```

**Boundary note (the hukm/reality frontier — the hardest boundary in Saleh-).**
"Ifadah" here is the *structural possibility* that an utterance carries a speech
force; it is the END of the structural spine, **not** the beginning of meaning,
truth, or ruling. A reality claim (`RealityMapping`/`RealityClaim`), a truth
value (`TruthJudgment`), a final i‘rab decision (`IrabFinalDecision`), and any
hukm (`HukmCandidate`) are all forbidden. `forbidden_changes` explicitly blocks
`assign_reality_claim`, `assign_truth_value`, and `assign_hukm`. Saleh- stops at
*licensed structural possibility* — it never crosses into reality, truth, or
hukm; that frontier belongs beyond this package, not here.

## 3. Required upstream evidence (consumed)

SCG-P12's **direct input is `IrabGeometryCandidate`** (origin =
`P11_IRAB_GEOMETRY`). Required evidence:

- `IrabGeometryCandidate` (direct input from SCG-P11)
- preserved identity (P12 preserves `irab_geometry_identity`)
- explicit **residual evidence** carried from upstream (nothing hidden)
- **speech-force + ifadah-boundary + mukhatab-context evidence** (conditions:
  `irab_geometry_established`, `ifadah_context_closed`)

`minimum_required_fields = (irab_geometry_ref, speech_force_evidence, ifadah_boundary_evidence, mukhatab_context_evidence)`

## 4. Allowed output

- **`IfadahCandidate` only** — a candidate (إمكان قوة كلامية), never a judgment,
  truth value, reality claim, or hukm.

## 5. Forbidden outputs (terminal — finality guards + absolutes)

P12 produces no downstream candidate (terminal). It must NOT produce any final
semantic/truth/reality artifact:

```text
HukmCandidate · RealityClaim · FinalMeaning · IrabFinalDecision · RealityMapping · TruthJudgment
```

## 6. What P12 must NOT do (structural-only discipline — the key P12 boundary)

P12 is **specification of required evidence + prohibitions only**. It must NOT:

- claim **reality** (`RealityMapping` / `RealityClaim`)
- assign a **truth value** (`TruthJudgment`)
- issue a **final i‘rab decision** (`IrabFinalDecision`) or any **hukm**
- close a **final meaning** (`FinalMeaning`) or perform tafsir
- (`forbidden_changes = assign_reality_claim / assign_truth_value / assign_hukm`)

The spec may only define **what evidence a future `IfadahCandidate` would
require** and **what it must never claim**.

## 7. No-jump discipline

- `origin = IrabGeometryCandidate` (SCG-P11) — the **only** upstream path is
  `P11 → P12`. Any skip is structurally impossible.
- `target_boundary_opens = ()` — **terminal**; P12 opens no successor phase.
- `forbidden_direct_next_layer_ids = ()` — there is no licensed forward edge.

## 8. Invariants preserved (spec level)

- **Identity ≠ trace; not consumed:** `preserves_ids = irab_geometry_identity`.
- **Explicit residuals / no silent failure:** `blockers = (ifadah_precondition_blocked,)`;
  `invalidating_differences = (speech_force_conflict,)`.
- **Candidate-only / potential-only:** output is a `…Candidate` ("إمكان");
  absolutes + reality/truth/final-decision guards forbidden; speech force as
  possibility, never as a reality/truth/hukm claim.
- **Structural spine ends here:** no meaning, no truth, no reality, no hukm.

## 9. Status discipline

- `build_p12_specified_registry` advances **only P12** `PLANNED → SPECIFIED`
  (building on `build_p11_specified_registry`). With this transition the
  canonical spine is **specification-complete**: P0 `IMPLEMENTED`,
  P1–P12 `SPECIFIED`; layer count stays **19**.
- **No `build_p12_implemented_registry`.** `IMPLEMENTED` is not authorized while
  the global REC freeze is ACTIVE; no layer beyond P0 is `IMPLEMENTED`.

Enforced by `tests/qiyas_core/test_master_registry_p12_specified.py` (`P12-SPEC-*`).
