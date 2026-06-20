# SCG-P10 RelationGeometry Design Resolution

> **Type:** Design-resolution note — answers the §9 open questions of
> `SCG_P10_RELATION_GEOMETRY_DESIGN_GATE.md`. It is **subordinate** to
> `RELATION_GEOMETRY_CONSTITUTION.md`, the canonical P10 `LayerSpec`
> (`master_registry_seed.py`), `SENTENCE_GEOMETRY_CONSTITUTION.md`, and the
> P9/P10 design-gate materials. **`[CANON]`** = already present in canonical
> spec/constitution. **`[DESIGN]`** = proposed design only, not ratified as
> runtime behavior. **Where this note and canonical spec/code differ, the
> canonical spec/code wins.**

## 1. Status

- **P10 is not implemented.** The P10 `LayerSpec` is `PLANNED` in the seed,
  reaching only `SPECIFIED` via `build_p10_specified_registry`.
- **P10–P12 remain SPECIFIED-only.** Implemented phases stop at P9.
- **Freeze remains ACTIVE above P9.** No `build_p10_implemented_registry`;
  registry count stays **19**.
- This note is **descriptive and subordinate** to the canonical spec/constitution.
- All new decisions are **`[DESIGN]` only** unless already **`[CANON]`**.
- This note **authorizes no runtime, registry, schema, or test change**.

## 2. Resolution Summary

This note resolves the §9 open questions of the P10 design gate while keeping
`RelationGeometryCandidate` **structural, candidate-only, potential-only, and
non-final**. It maps the P9 information-gain pattern onto P10's canonical spine
(origin P9 `SentenceGeometryCandidate` → `RelationGeometryCandidate`, opens only
the `irab_geometry_candidates` prior) and proposes — but does not ratify — the
residual/threshold constants a future implementation gate would need.

## 3. Q1 — ACCEPT Evidence

**Proposed `[DESIGN]` position** (no canonical contradiction found). P10 **ACCEPT**
requires:

- at least one **accepted P9 `SentenceGeometryCandidate`** `[CANON]` (origin);
- preserved **`sentence_geometry_identity`** from P9 `[CANON]` (`preserves_ids`);
- **`relation_scope_closed`** evidence `[CANON]` (condition);
- **`relation_type_evidence`** present as *structural relation possibility only*
  `[CANON]` (required field);
- **`dependency_scope_evidence`** present `[CANON]` (required field);
- the `sentence_geometry_established` condition met `[CANON]`;
- **no forbidden i‘rab/case/meaning/hukm/reality/final evidence consumed**
  `[DESIGN]` (boundary discipline).

**Stress:** `relation_type_evidence` is *structural* evidence (تبعية، عطف، إبدال،
توكيد as geometric possibility) — **not** a final syntax label and **not** a
semantic relation.

## 4. Q2 — DEFER vs BLOCK

**DEFER** — relation geometry admissible but underdetermined:

| Reason | Marking |
| --- | --- |
| `relation_scope_underspecified` | `[DESIGN]` |
| `relation_type_underspecified` | `[DESIGN]` |
| `dependency_scope_underspecified` | `[DESIGN]` |
| `carried_sentence_geometry_residuals` | `[DESIGN]` |
| `relation_identity_underspecified` | `[DESIGN]` |

**BLOCK** — structural contradiction or forbidden leakage:

| Reason | Marking |
| --- | --- |
| `relation_structure_blocked` | `[CANON]` (spec `blockers`) |
| `relation_type_conflict` | `[CANON]` (spec `invalidating_differences`) |
| `identity_collapse_blocked` | `[DESIGN]` (mirrors P9 adapter guard) |
| `forbidden_output_attempted` | `[DESIGN]` (mirrors P9 adapter guard) |

Verdict precedence would follow P9: BLOCK (forbidden → type-conflict →
structure/identity-collapse) before DEFER (underspecified reasons) before ACCEPT.

## 5. Q3 — Required Upstream Structure

**Recommended decision `[DESIGN]`:**

- P10 requires **at least one accepted P9 `SentenceGeometryCandidate`** `[CANON]`
  (single origin).
- P10 does **not** require multiple P9 candidates.
- The **multi-unit requirement is already enforced at P9** (≥2 distinct
  word/segment units to ACCEPT).
- P10 **refines relation geometry inside an accepted sentence geometry**; it does
  **not** re-prove sentencehood. No re-derivation of units; P10 reads P9's accepted
  multi-unit structure off the trace.

## 6. Q4 — Identity Preservation

- `I(c)` preserves **`sentence_geometry_identity`** from P9 `[CANON]`.
- Where P9 carries **ordered multi-unit identity structure**, P10 must **preserve
  it without collapsing it into a single relation identity** `[DESIGN]`.
- Relation evidence belongs in **trace `T(c)`**, never identity `I(c)`
  `[CANON principle]`.
- `I(c)` and `T(c)` remain **disjoint** (kernel `identity ∩ trace = ∅`)
  `[CANON principle]`.
- Optional `[DESIGN]`: `T(c)` may include `relation_scope_trace` and
  `dependency_scope_trace` for auditability (trace-only; never identity).

## 7. Q5 — Residuals

Use canonical names verbatim where they exist; the following are **`[DESIGN]`
proposals** consistent with the P9 `deferred_*` / kernel `blocking_*` convention:

**Proposed DEFER residuals `[DESIGN]`:**

- `deferred_relation_scope_underspecified`
- `deferred_relation_type_underspecified`
- `deferred_dependency_scope_underspecified`
- `deferred_carried_sentence_geometry_residuals`
- `deferred_relation_identity_underspecified`

**Proposed BLOCK residuals:**

- `blocking_relation_structure_blocked` (wraps `[CANON]` `relation_structure_blocked`)
- `blocking_relation_type_conflict` (wraps `[CANON]` `relation_type_conflict`)
- `blocking_identity_collapse_blocked` `[DESIGN]`
- `blocking_forbidden_output_attempted` `[DESIGN]`

Note: in P9 the kernel surfaced the block as `blocking_fariq_present`; the
canonical block tokens (`relation_structure_blocked`, `relation_type_conflict`)
drive the kernel `فارق` machinery, and the `blocking_*` names above are the
proposed surfaced residual labels.

## 8. Q6 — Licensed Priors

- P10 may open **only `irab_geometry_candidates`** `[CANON]`
  (`target_boundary_opens`), and **only on ACCEPT**.
- P10 must **not emit `IrabGeometryCandidate`** itself `[CANON]` (`forbidden_outputs`).
- P10 must **not emit P11/P12 candidates** `[CANON]` (forbidden outputs +
  `forbidden_direct_next_layer_ids = P12`).
- P10 must **not open** semantic, dalālah, hukm, reality, or final-meaning objects
  `[CANON principle]`.
- P10 also **closes** `relation_geometry_candidates` `[CANON]`
  (`target_boundary_closes`) — the prior P9 opened.

**Stress:** opening `irab_geometry_candidates` is **not i‘rab assignment**; it is
only a downstream **structural prior** licensing P11's later question.

## 9. Q7 — Forbidden Outputs

**Keep the canonical P10 forbidden list exactly `[CANON]`:**

- `IrabGeometryCandidate` (P11) · `IfadahCandidate` (P12) · `IrabCandidate` ·
  `CaseJudgment` · `HukmCandidate` · `RealityClaim` · `FinalMeaning`
- forbidden changes: `assign_irab` · `assign_case` · `assign_ifadah`

**Defense-in-depth hardening `[DESIGN]` — future implementation consideration
only** (must be confirmed canonically before being referenced; the constitution
covers them in prose, not yet as constants):

- `MeaningCandidate`
- `DalalahCandidate` / dalālah judgment
- "final syntax labels" as claims

No implementation change required here; flagged for the future implementation gate.

## 10. Q8 — Required Proof Tests for Future Implementation

**Design-only list (no tests authored now):**

- P10 registry-implemented test, *if later authorized* (`build_p10_implemented_registry`).
- P11–P12 still SPECIFIED-only test.
- Freeze ACTIVE above P10 test.
- No `build_p11_implemented_registry` test (the guard shifts up one phase at the
  P10 gate).
- P10 **ACCEPT** from accepted P9 `SentenceGeometryCandidate` with
  `relation_scope_closed` + `dependency_scope_evidence`.
- P10 **DEFER** tests, one per underdetermined residual (§7).
- P10 **BLOCK** tests: `relation_structure_blocked`, `relation_type_conflict`,
  identity collapse, forbidden-output attempt.
- Identity-preservation test P9 → P10 (`sentence_geometry_identity` preserved,
  multi-unit structure not collapsed).
- Trace/identity separation test (`I ∩ T = ∅`).
- No-leakage test: no `IrabGeometryCandidate`, no `IfadahCandidate`, no P11/P12,
  no i‘rab/case/meaning/dalālah/hukm/reality/final interpretation.
- `run_qiyas` integration test: P10 opens **only** behind an accepted P9 and does
  **not** open P11.

## 11. Summary of Proposed `[DESIGN]` Constants

| Aspect | Value | Marking |
| --- | --- | --- |
| ACCEPT threshold | ≥1 accepted P9 `SentenceGeometryCandidate` + `relation_scope_closed` + `relation_type_evidence` + `dependency_scope_evidence`; no forbidden evidence | inputs `[CANON]`; no-forbidden clause `[DESIGN]` |
| DEFER residuals | `deferred_relation_scope_underspecified`, `deferred_relation_type_underspecified`, `deferred_dependency_scope_underspecified`, `deferred_carried_sentence_geometry_residuals`, `deferred_relation_identity_underspecified` | `[DESIGN]` |
| BLOCK residuals | `relation_structure_blocked`, `relation_type_conflict` | `[CANON]` |
| BLOCK residuals (added) | `identity_collapse_blocked`, `forbidden_output_attempted` | `[DESIGN]` |
| Identity representation | preserve `sentence_geometry_identity` + ordered multi-unit structure; relation evidence trace-only; `I ∩ T = ∅` | id `[CANON]`; multi-unit-preservation `[DESIGN]` |
| Licensed prior | open **only** `irab_geometry_candidates` (ACCEPT only); close `relation_geometry_candidates` | `[CANON]` |
| Forbidden-output hardening (optional) | `MeaningCandidate`, `DalalahCandidate`/dalālah judgment, final syntax labels | `[DESIGN]` (future gate) |

## 12. Non-Authorization Clause

**This design-resolution note does not authorize implementation.** A separate
explicit authorization is required before any of:

- registry changes
- runtime changes
- schema changes
- tests
- P10 candidate emission
- any PR that implements P10 behavior

**P10 remains SPECIFIED-only. P10–P12 remain SPECIFIED-only. Freeze remains ACTIVE
above P9.**
