# SCG Structural Spine Completion Note: P0–P12

> **Type:** Paper-facing / status update note. Descriptive only — it introduces no
> new layer, no new theory name, and changes no constitution, registry, schema,
> runtime, or test. It is subordinate to the canonical SCG constitutions and
> LayerSpecs. Base: `main` HEAD `9f52261`.

## 1. Status

The Saleh/Qiyas **SCG structural spine** is now implemented end-to-end on `main`
(HEAD `9f52261`), from **P0 through P12**. The spine is a **potential-only cascade**
of **candidate-only layers**: each layer compiles formally delimited structural
evidence into a higher **proof-relevant**, **identity-preserving**,
**trace-separated** potential type. The cascade terminates at a **licensed
structural possibility** — it does not, at any layer, assert meaning, truth, hukm,
reality, or final interpretation.

This note describes the completion of an *implemented structural-potential spine*.
It makes no claim that the system understands, solves, or computes the meaning of
Arabic.

## 2. What Was Completed

- **P0–P12 implemented** — all thirteen phases of the canonical SCG spine reach
  `IMPLEMENTED` status on `main`.
- The **19-layer registry remains stable** (count unchanged at 19; no layers added
  or removed to reach completion).
- **P12 is terminal**: its `target_boundary_opens` is empty — it opens no successor
  phase.
- **No P13 exists** — there is no P13 layer id and no `build_p13_implemented_registry`.
- **Full tests and governance are green** (2689 passed, 2 skipped; 263 in the
  governance subset).

The implementation endpoint is **`IfadahCandidate`**, the terminal structural
candidate of the spine.

## 3. Scientific Meaning of Completion

"Completion" here means the **structural-potential spine is implemented** — not that
natural-language meaning or hukm has been solved.

The implemented cascade compiles formally delimited structural evidence into
progressively higher **proof-relevant potential types**: from raw Unicode codepoint
identity, through letter/haraka identity, slot geometry, word and verbal structure,
sentence/relation/i‘rab geometry, and finally into a terminal `IfadahCandidate`.
That terminal candidate records **licensed structural readiness** for speech-force /
ifādah **without asserting** truth, hukm, final meaning, or final interpretation.
Completion is of the *spine*, not of the language.

## 4. Boundary of IfadahCandidate

**`IfadahCandidate` means:**

- a *structural possibility* of ifādah / speech-force readiness;
- candidate-only;
- potential-only;
- trace-backed (every readiness flag is evidenced in trace);
- non-final.

**`IfadahCandidate` does NOT mean:**

- hukm;
- a reality claim;
- a truth judgment;
- final meaning;
- final interpretation;
- a final speech-force verdict;
- a semantic judgment;
- a theological or legal judgment.

This boundary is enforced, not merely stated: P12 opens nothing, closes the
`ifadah_candidates` prior, forbids the finality outputs (`HukmCandidate`,
`RealityClaim`, `RealityMapping`, `TruthJudgment`, `FinalMeaning`,
`IrabFinalDecision`), blocks the changes `assign_reality_claim` /
`assign_truth_value` / `assign_hukm`, and refuses any frontier crossing via a
`final_judgment_attempted` guard. The hukm/reality/finality frontier remains
**outside** the implemented SCG spine.

## 5. Identity and Trace Discipline

The spine maintains a strict separation throughout:

- Each layer **preserves identity** `I(c)` rather than collapsing it — upstream
  identities are carried forward (e.g. the ordered multi-unit identity established
  at P9 survives transitively through P10, P11, and P12 without being collapsed into
  a single higher-layer identity).
- **Higher evidence is carried in trace** `T(c)`, never in identity — speech-force
  readiness, i‘rab positions, relation geometry, and the like are trace facts, not
  identity.
- `I(c)` and `T(c)` **remain disjoint** (`I(c) ∩ T(c) = ∅`), enforced structurally
  at the candidate level.
- **Invalidating differences block or defer** rather than being overwritten — a
  contradicted precondition BLOCKs and an underdetermined one DEFERs with a
  preserved residual; nothing is silently resolved.

## 6. Current Empirical Validation

- Full suite: **2689 passed, 2 skipped, 0 failed**.
- Governance subset: **263 passed**.
- **No P13**; **no `build_p13_implemented_registry`**.
- **No hukm / reality / truth / final-meaning / final-interpretation /
  final-speech-force-verdict leakage** observed in pipeline probes (positive and
  negative).
- Schema, docs, and constitution **unchanged** during the P12 implementation.

## 7. Honest Limitation

Current positive P12 reachability is demonstrated only on structures that already
pass through the existing **verb-signified path** into an accepted P11 (e.g.
multi-verb sequences such as `ضَرَبَ كَتَبَ`). Ordinary **noun-subject** examples
such as `زيد` / `عمرو` still stop **upstream** — before accepted P11/P12 — because of
the current **P6/P7/P8 structural frontier** (the verbal-signified gate currently
admits verb units, not nouns). This is an **upstream structural-unit limitation**,
not a semantic claim and **not a failure of the P12 boundary**: the terminal
boundary holds regardless; what is currently narrow is the set of inputs that
structurally reach it.

## 8. Suggested Paper Insertion

> With the P12 implementation, the Saleh/Qiyas prototype now contains a complete
> 19-layer structural-potential spine, from raw Unicode codepoint identity through a
> terminal `IfadahCandidate`. This completion is deliberately bounded: the terminal
> candidate represents only *licensed structural readiness* for ifādah /
> speech-force, and does not assert meaning, hukm, truth, reality, or final
> interpretation. Every layer is candidate-only, identity-preserving, and
> trace-separated; higher evidence is carried in proof-relevant traces rather than
> collapsed into identity, and invalidating differences block or defer rather than
> being overwritten. The hukm/reality/finality frontier lies outside the implemented
> spine by construction — the algebra stops at licensed structural possibility.

## 9. Non-Claim Clause

This result should be read as the **completion of the implemented
structural-potential spine** — not as completion of Arabic understanding, semantic
interpretation, legal/theological judgment, or truth evaluation. Saleh/Qiyas builds
auditable, potential algebraic candidates over formally delimited structure; it
terminates at a licensed structural possibility and makes no claim beyond it.
