# MIU Variant Resolution Usage Note

> **Status:** Usage note. Not a contract. Documents the merged runtime
> behavior introduced by PRs #78–#83.
>
> **Authority basis (read-only citation):**
>
> - `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` (PR #78)
> - `ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md` (PR #79)
> - `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` (PR #71)
> - `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` (PR #72)
> - `CLAUDE.md` §0 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20

---

## 1. Purpose

This document is a **usage note** that records how the merged components from PRs #78–#83 fit together at runtime. It does **not**:

- define a new layer,
- define a new evidence carrier,
- amend any existing contract,
- change runtime behavior in any way,
- introduce a new claim, new label, new gate, or new rule.

It is a citation anchor for callers who want to wire `ArabicVariantResolver` into the readiness path correctly, and a reference for reviewers verifying that the runtime matches the constitutional contracts.

The note follows the precedent set by `LCNV_MINIMAL_RUNTIME_STABILIZATION_CLOSURE.md` and `LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md`: a closure document that names a settled state rather than proposing a next step.

---

## 2. Current Runtime Path

After PRs #78–#83, the runtime supports the following optional chain:

```text
ArabicVariantResolver
    → ArabicVariantResolutionEvidence | None
    → MinimalIndependentUnitReadinessLayerAdapter.admit(
          geometry,
          closure_evidence,
          variant_resolution_evidence=evidence,
      )
    → MinimalUnitReadinessCandidate (ACCEPTED / BLOCKED / DEFERRED)
```

The chain is **manual** at the caller side: there is no production adapter that automatically calls the resolver and threads its output into `admit(...)`. See §6.

The `variant_resolution_evidence` parameter is optional. Its presence is necessary-but-not-sufficient for any decision; see §4 and §7.

---

## 3. What the Resolver Does

`ArabicVariantResolver` is a **producer only** per `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §3:

- Input: a `SlotGeometryCandidate(length=1, construction_mode="seed")` on the `SlotGeometryQiyas` layer (the §4 closed consumption surface).
- Output: `ArabicVariantResolutionEvidence | None`.
- The resolver currently emits evidence only for the two in-scope multi-variant symbols `و` and `ي`, and only when the slot carries an **active (non-sukun) haraka** witness; the `selection_basis` it emits is always `("haraka_function_self",)`.
- It returns `None` for:
  - any symbol the registry resolves uniquely (e.g. `ب / ف / ك / ل / س / أ / ت`),
  - sukun-bearing `و` / `ي` (the `haraka_function_before` basis required for madd is not preserved on Phase-1 length=1 seeds — see `ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md` §4.4 / §5.4),
  - the alif `ا` (future extensibility only per `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §6),
  - any geometry that fails the surface gate (wrong `candidate_type`, wrong `layer`, `length != 1`, `construction_mode != "seed"`),
  - any malformed input.

It **does not**:

- decide MIU readiness,
- produce a `Candidate` of any type,
- invoke `QiyasKernel.apply`,
- consult or mutate the registry beyond read-only metadata lookup,
- consume any higher-layer typed unit.

---

## 4. What MIU Does With Evidence

`MinimalIndependentUnitReadinessLayerAdapter.admit(...)` accepts the optional `variant_resolution_evidence` per the PR #82 amendment to the MIU adapter. Its discipline:

- The argument is **optional**. Omitting it is the canonical path for single-variant symbols and is identical to passing `None`.
- For multi-variant symbols (`و` / `ي`) on length=1 seeds:
  - **Absent evidence** → MIU emits `defer:variant_ambiguity:present` → kernel records `deferred_variant_ambiguity` → DEFERRED.
  - **Invalid / foreign / mismatched evidence** is treated as absent: DEFERRED (never BLOCKED). Per `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §7, malformed evidence behaves like missing evidence — DEFER, not BLOCK.
  - **Valid evidence** removes the `variant_ambiguity` defer reason **only**.
- After ambiguity is removed (or never raised), all other MIU invariants still apply:
  - `length == 1`,
  - `construction_mode == "seed"`,
  - `MinimalCompleteClosureEvidence` present,
  - registry has metadata for the geometry's symbol,
  - the resolved entry's `can_function_as_minimal_independent_unit == True`,
  - `output_flags ⊇ {CandidateOnly}`.
- **Valid `madd` evidence** (which the current resolver does not emit but a future caller might supply synthetically) cannot ACCEPT: the registry entries `jawf_waw_madd` and `jawf_ya_madd` carry `can_function_as_minimal_independent_unit == False`, so the readiness layer BLOCKS via the eligibility predicate. It does **not** become "meaning" or "hukm".

Evidence validation inside `MIU._build_evidence` (via the private helper `_try_apply_variant_resolution`) requires five conjunctive conditions:

1. `evidence.symbol` matches the geometry's extracted symbol,
2. `evidence.geometry_candidate_id` matches the geometry's `candidate_id`,
3. `evidence.selected_variant` is one of the reserved labels (`madd` / `non_madd`),
4. `evidence.selected_entry_id` resolves to a real registry entry,
5. that entry's `symbol` and `variant` agree with the evidence.

Any failure of these conditions returns `None` (i.e., treats the evidence as absent) — `DEFER`, never `BLOCK`.

---

## 5. Canonical Examples

The matrix below records the merged runtime behavior. It is locked by `tests/qiyas_core/test_variant_resolver_miu_integration.py` (PR #83) and reflected by the diagnostic script `/tmp/check_miu_text.py` (see §9).

| Input | Resolver Evidence | MIU Result | Why |
|---|---|---|---|
| `بِ` (ب + kasra) | None | ACCEPTED | single-variant, registry-eligible |
| `ضَ` (ض + fatha) | None | BLOCKED | `can_function_as_minimal_independent_unit == False` |
| `وَ` without evidence | None | DEFERRED | `variant_ambiguity` (registry has two entries) |
| `وَ` with resolver evidence | `non_madd` / `lips_waw_non_madd` | ACCEPTED | ambiguity removed + entry eligible |
| `يَ` with resolver evidence | `non_madd` / `tongue_ya_non_madd` | BLOCKED | ambiguity removed but `tongue_ya_non_madd` not eligible |
| `ضَرَبَ` (length > 1) | irrelevant | BLOCKED | length gate + `construction_mode == "extension"` |
| `وَ` with foreign evidence (different geometry id) | rejected | DEFERRED | invalid evidence is treated as absent |
| `وَ` with synthetic `madd` evidence | `madd` / `jawf_waw_madd` | BLOCKED | resolved entry not eligible (no meaning, no hukm) |

The diagnostic script also reports the parsed letter/haraka codepoint pairs, the geometry length and `construction_mode`, whether closure evidence is present, the `selection_basis` tuple, the candidate's `output_flags`, the `residual_type` set, and the candidate type (always `MinimalUnitReadinessCandidate`).

---

## 6. Caller Responsibility

There is **no automatic caller-side wiring** in the merged codebase. The chain is entered manually at the call site:

```text
# Pseudo-code only. Not production code. Not committed anywhere
# inside `src/`. Provided here for documentation of the intended
# usage pattern at the integration boundary.

geometry = ...                  # SlotGeometryCandidate(length=1, seed)
closure = ...                   # MinimalCompleteClosureEvidence | None
evidence = ArabicVariantResolver().resolve(geometry)
result = miu.admit(
    geometry,
    closure,
    variant_resolution_evidence=evidence,
)
```

This is **intentional**. No runtime adapter "above MIU" exists yet. Any future PR that proposes to add one must:

- be a constitutional amendment (not a usage note), and
- preserve the necessary-but-not-sufficient discipline of §4.

The integration test file `tests/qiyas_core/test_variant_resolver_miu_integration.py` is the canonical reference for what the manual wiring looks like and what invariants must hold across it.

---

## 7. What This Does Not Mean

Evidence presence and ACCEPTED status carry strictly limited semantic weight. The following equations **never** hold under this baseline:

- `evidence is not None` ⟹ ACCEPTED — **false** (eligibility dominates).
- `selected_variant == "non_madd"` ⟹ ACCEPTED — **false** (see يَ).
- `selected_variant == "madd"` ⟹ meaning — **false** (BLOCK is the only honest outcome for current registry).
- `MinimalUnitReadinessCandidate` (ACCEPTED) ⟹ word — **false**.
- `MinimalUnitReadinessCandidate` (ACCEPTED) ⟹ dalalah — **false**.
- `MinimalUnitReadinessCandidate` (ACCEPTED) ⟹ hukm — **false**.
- `MinimalUnitReadinessCandidate` (ACCEPTED) ⟹ reality — **false**.

The MIU readiness layer marks a single Phase-1 slot as **ready to be considered as a minimal independent unit candidate** under the registry's eligibility metadata. It does not assert anything about meaning, lexical role, syntactic role, derivational role, or truth.

---

## 8. Scope Boundaries

This usage note is bounded by the same non-goals as the underlying contracts. The note **does not** introduce, license, or reference as operational:

- `WordCandidate`
- `LafzCandidate`
- `DalalahCandidate`
- `FinalMeaning`
- `HukmCandidate`
- `RealityClaim`
- `FinalCaseJudgment`
- `SentenceCandidate` / `ParagraphCandidate`
- `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate`
- `MinimalIndependentMeaningCandidate`
- Amil layer / عوامل الجرجاني
- any registry amendment (no `default_variant` field, no new variant labels, no flip of `can_function_as_minimal_independent_unit` on any entry)
- resolver expansion (no activation of the secondary `intra_utterance_position` basis, no `haraka_function_before` for madd, no `registry_default` consumption, no `preceding_letter_identity` / `following_letter_identity` / `haraka_function_after`)
- alif (`ا`) variant semantics
- any priority / tie-breaking algorithm over `selection_basis` labels
- any sibling-context pipeline amendment
- caller-side auto-wiring runtime adapter
- automatic integration layer above MIU
- `GlyphClassificationGate` runtime
- `SifatVector` runtime
- Full Layer 2 implementation

If any future PR proposes content that touches any of the above, it must merge **after** an explicit constitutional amendment and must not be back-justified by this note.

---

## 9. Relationship to Tests

The runtime behaviour documented here is **locked end-to-end** by:

```text
tests/qiyas_core/test_variant_resolver_miu_integration.py
```

That file is the regression source of truth. It pins:

- the seven canonical end-to-end cases enumerated in §5,
- the resolver↔registry agreement property (every emitted `selected_entry_id` is a real registry entry whose `symbol` and `variant` agree with the evidence),
- the MIU↔registry delegation property (`ACCEPTED` ⟹ resolved entry's `can_function_as_minimal_independent_unit == True`),
- the §7 absence-≠-BLOCK property for absent / foreign / malformed evidence,
- the AST guard that the test file imports nothing from any forbidden higher-layer module,
- the regression locks confirming no automatic caller-side wiring, only the primary `haraka_function_self` basis is currently emitted, and `ا` remains future-extensibility only.

A non-canonical diagnostic script lives at:

```text
/tmp/check_miu_text.py
```

It is **not** committed to the repository and is **not** part of the canonical surface. It mirrors the integration test's fixture pattern (codepoint scan → `SlotCandidate` fixture → `SlotGeometryLayerAdapter.seed_geometry` → optional resolver → `MIU.admit`) and exists only as a terminal aid for visual verification by maintainers. Do not depend on the `/tmp` path in any committed code.

---

## 10. Next Safe Steps

This note records a settled state. The safe next options after merging it are limited and intentionally conservative:

1. **Review and maintain the integration tests** (`tests/qiyas_core/test_variant_resolver_miu_integration.py`). They are the regression target for any future change that touches the resolver, the carrier, MIU, or the registry.
2. **Later, possibly a docs-only `GlyphClassificationGate` contract** — promoting the existing `GLYPH_CLASSIFICATION_GATE_PLAN.md` to a constitutional contract document, following the precedent set by PRs #71, #72, #78, #79. This is the next Layer 2 step per `PROJECT_MATHEMATICAL_FOUNDATION.md §11`. It is **docs-only** and structurally **below** SlotCandidate; it is not a step toward Word/Dalalah.
3. **Pause.** Pausing is a constitutionally valid action. The variant-resolution layer is fully specified, fully implemented, fully integrated with MIU, and now fully documented in usage form.

Explicitly **not** recommended:

- starting `WordCandidate`, `LafzCandidate`, `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`, `RealityClaim`, `FinalCaseJudgment`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, `MinimalIndependentMeaningCandidate`, or the Amil layer,
- amending the registry,
- expanding the resolver,
- introducing alif semantics,
- introducing `default_variant` or priority / tie-breaking,
- introducing sibling-context pipeline amendments,
- introducing caller-side auto-wiring.

Each of the above requires an explicit constitutional trigger that is **not** present.

---

**Document version:** 1.0
**Last updated:** 2026-06-05
**Status:** Usage note (post-PR-#83 baseline)
**Authority:** Subordinate to the contracts cited at the top of this document. Does not amend any of them.
