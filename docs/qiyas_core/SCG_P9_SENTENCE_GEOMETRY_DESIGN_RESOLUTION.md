# SCG-P9 SentenceGeometry — Design Resolution (§9)

> **Descriptive design-resolution note — not a constitution.** Resolves the seven
> open questions from `SCG_P9_SENTENCE_GEOMETRY_DESIGN_GATE.md`. **Subordinate to**
> `SENTENCE_GEOMETRY_CONSTITUTION.md`, the SCG registry/spec entries, the P9 design
> gate, and freeze/forbidden-output governance. **Where this note and the canonical
> spec/code differ, the canonical spec/code wins.** It introduces no new layer,
> theory name, or framework rename. It **authorizes no runtime, registry, schema,
> or test change** and **no P9 implementation or candidate emission**. All new
> constants/thresholds are marked **[DESIGN]** only; nothing here is ratified for
> implementation until a separate P9 implementation gate.
>
> **Legend.** **[CANON]** = exact existing spec constant (authoritative, used
> verbatim at implementation). **[DESIGN]** = proposed addition, not yet in the
> spec; subordinate, ratified only at a future P9 implementation gate.

## Status

- **P9 is not implemented.** Status `SPECIFIED`; there is no
  `build_p9_implemented_registry`.
- **P9–P12 remain SPECIFIED-only.** Registry count stays **19**.
- **The freeze remains ACTIVE** for P9+.
- This note **authorizes no runtime, registry, schema, or test change**; a separate
  explicit authorization is required before any P9 implementation work.

## Q1 — Minimal evidence for P9 ACCEPT

P9 ACCEPT requires all of:

- **at least two** accepted P8 `AmilMamulCandidate` traces **[DESIGN]** — consistent
  with P9 being the first *multi-unit* layer and with the spec's plural
  `amil_mamul_refs` **[CANON]**; the spec does not mandate a count, so "≥2" is a
  design refinement, not a contradiction;
- preserved upstream identity for each trace — `amil_mamul_candidate_identities`
  **[CANON]**;
- **structurally licensed** adjacency/contiguity between units **[DESIGN]** (see Q3);
- a **closed sentence-geometry boundary** — `sentence_boundary_closed` /
  `isnad_boundary_evidence` **[CANON]**, with `amil_mamul_candidates_ready`
  **[CANON]**;
- **no** forbidden semantic/i‘rab/hukm/reality evidence consumed (see Q6/Q7).

The required-field backbone is the spec's
`minimum_required_fields = (amil_mamul_refs, sentence_type_evidence, isnad_boundary_evidence)`
**[CANON]**; sentence-type appears only as *evidence*, never a verdict.

## Q2 — DEFER vs BLOCK

- **DEFER** (structurally admissible but under-determined) **[DESIGN]** — incomplete
  boundary, weak adjacency, insufficient relation coverage, or unresolved carried
  residuals. The spec defines BLOCK reasons but **no** DEFER reason today, so the
  DEFER verdict is a design addition mirroring P3–P8.
- **BLOCK** (structural contradiction) — no accepted P8 traces; fewer than two
  units; identity collapse; contradictory ordering; forbidden downstream evidence;
  or attempted i‘rab/meaning/hukm/reality emission. Of these,
  `sentence_structure_blocked` **[CANON]** and `sentence_type_conflict` **[CANON]**
  are the existing spec blocker / invalidating-difference; the remaining BLOCK
  conditions are **[DESIGN]** additions (see Q5).

## Q3 — Adjacency

Use **structurally licensed adjacency [DESIGN]**, not raw textual adjacency.
Textual or normalized-token adjacency *may serve as evidence*, but **P9 ACCEPT
requires structural adjacency licensed by upstream trace/boundary evidence** —
consistent with the spec's framing of P9 as a "structural arrangement of relation
candidates," not a textual operation.

## Q4 — Identity preservation across multiple P8 traces

- **Identity `I(c)` = the union of upstream identity-sets [CANON-aligned]** — what
  the kernel preserves (`amil_mamul_candidate_identities`, union of `asl ∪ far`),
  satisfying identity preservation.
- **In addition, expose an *ordered tuple* of the upstream identity-sets in the
  trace `T(c)` [DESIGN]** — for trace readability / provenance of the multi-unit
  ordering.
- **Identity stays disjoint from trace [CANON]** — the ordered tuple lives in
  `T(c)`, never in `I(c)`; the union lives in `I(c)`.

## Q5 — Residuals

- **DEFER residuals [DESIGN]** must record one or more of:
  `adjacency_underspecified`, `sentence_boundary_underspecified`,
  `relation_coverage_underspecified`, `carried_upstream_residuals`,
  `identity_join_underspecified`.
- **BLOCK residuals** must record:
  `sentence_structure_blocked` **[CANON]**, `sentence_type_conflict` **[CANON]**,
  `identity_collapse_blocked` **[DESIGN]**, `forbidden_output_attempted`
  **[DESIGN]**.

All non-acceptance preserves an inspectable residual; carried-up P3–P8 residuals
are retained (`carried_upstream_residuals`), never discarded.

## Q6 — Licensed priors

- P9 may open **only** `relation_geometry_candidates` **[CANON]**
  (`target_boundary_opens`), and only on ACCEPT.
- P9 may **not** emit/open: `IrabCandidate`, `CaseJudgment`, `IfadahCandidate`,
  `HukmCandidate`, `RealityClaim`, `FinalMeaning` **[CANON]**, nor
  `MeaningCandidate`, `DalalahCandidate`, final syntax labels, `assign_irab`,
  `assign_case`, `assign_ifadah` (the last three are `forbidden_changes`
  **[CANON]**).

## Q7 — Forbidden-output constants

- **Keep the existing exact spec forbidden list [CANON]** as authoritative:
  `RelationGeometryCandidate`, `IrabGeometryCandidate`, `IfadahCandidate`,
  `HukmCandidate`, `RealityClaim`, `FinalMeaning`, `IrabCandidate`, `CaseJudgment`;
  plus `forbidden_changes = (assign_irab, assign_case, assign_ifadah)`.
- **Defense-in-depth additions** — `MeaningCandidate`, `DalalahCandidate`, final
  syntax labels — are **recommended only as a future implementation consideration
  [DESIGN]**, **not required** by this note. They are already excluded in effect
  (no SCG layer emits them; `FinalMeaning` covers final meaning), so adding them to
  the explicit tuple is optional hardening, deferred to the implementation gate.

## Summary of proposed [DESIGN] constants (none added here)

| Kind | Proposed constants (subordinate to spec; ratified only at the P9 implementation gate) |
|---|---|
| ACCEPT threshold | `≥2` accepted P8 traces; structurally-licensed adjacency requirement |
| Verdict | a **DEFER** verdict for P9 (the spec has BLOCK only) |
| DEFER residuals | `adjacency_underspecified`, `sentence_boundary_underspecified`, `relation_coverage_underspecified`, `carried_upstream_residuals`, `identity_join_underspecified` |
| Extra BLOCK residuals | `identity_collapse_blocked`, `forbidden_output_attempted` |
| Identity rep. | ordered-tuple of upstream identity-sets in `T(c)` (union remains `I(c)`) |
| Optional hardening | add `MeaningCandidate` / `DalalahCandidate` / final-syntax-labels to the P9 forbidden tuple |

Everything marked **[CANON]** is already in `SENTENCE_GEOMETRY_CONSTITUTION.md` /
the registry and is used verbatim. Everything marked **[DESIGN]** is a proposal
only.

## Non-authorization clause

This design-resolution note **does not authorize implementation.** A separate,
explicit authorization is required before any registry, runtime, schema, or test
change; before P9 candidate emission; or before any PR that implements P9
behavior. P9 remains **SPECIFIED-only**; the freeze remains **ACTIVE**.
