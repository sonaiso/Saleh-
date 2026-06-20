# SCG-P11 IrabGeometry Design Resolution

> **Type:** Design-resolution note — answers the §9 open questions of
> `SCG_P11_IRAB_GEOMETRY_DESIGN_GATE.md`. It is **subordinate** to
> `IRAB_GEOMETRY_CONSTITUTION.md`, the canonical P11 `LayerSpec`
> (`master_registry_seed.py`), `RELATION_GEOMETRY_CONSTITUTION.md`,
> `SCG_P11_IRAB_GEOMETRY_DESIGN_GATE.md`, and the P10 design/implementation
> materials. **`[CANON]`** = already present in canonical spec/constitution.
> **`[DESIGN]`** = proposed design only, not ratified as runtime behavior.
> **Where this note and canonical spec/code differ, the canonical spec/code wins.**

## 1. Status

- **P11 is not implemented.** The P11 `LayerSpec` is `PLANNED` in the seed,
  reaching only `SPECIFIED` via `build_p11_specified_registry`.
- **P11–P12 remain SPECIFIED-only.** Implemented phases stop at P10.
- **Freeze remains ACTIVE above P10.** No `build_p11_implemented_registry`;
  registry count stays **19**.
- This note is **descriptive and subordinate** to the canonical spec/constitution.
- All new decisions are **`[DESIGN]` only** unless already **`[CANON]`**.
- This note **authorizes no runtime, registry, schema, or test change**.

## 2. Resolution Summary

This note resolves the §9 open questions of the P11 design gate while keeping
`IrabGeometryCandidate` **structural, candidate-only, potential-only, and
non-final**. It maps the P9/P10 information-gain pattern onto P11's canonical spine
(origin P10 `RelationGeometryCandidate` → `IrabGeometryCandidate`, opens only
`ifadah_speech_force_candidates`, closes `irab_geometry_candidates`).

**Stress:** `IrabGeometryCandidate` is the geometry of *possible i‘rab positions*
(إمكانات المواضع الإعرابية) — **not** an i‘rab judgment. It names *where* i‘rab
could fall and *what* it could be; it never declares a token *is*
marfū‘/manṣūb/majrūr/majzūm.

## 3. Q1 — ACCEPT Evidence

**Proposed `[DESIGN]` position** (no canonical contradiction). P11 **ACCEPT**
requires:

- at least one **accepted P10 `RelationGeometryCandidate`** `[CANON]` (origin);
- preserved **`relation_geometry_identity`** from P10 `[CANON]` (`preserves_ids`);
- **`irab_context_closed`** evidence `[CANON]` (condition);
- **`irab_position_evidence`** present as *structural position possibility only*
  `[CANON]` (required field);
- **`case_marker_evidence`** present as *marker-geometry evidence only* `[CANON]`
  (required field);
- **`waqf_readiness_evidence`** present `[CANON]` (required field);
- the `relation_geometry_established` condition met `[CANON]`;
- **no forbidden i‘rab-verdict / case-decision / ifādah / hukm / reality / meaning /
  final evidence consumed** `[DESIGN]` (boundary discipline).

**Stress:** `case_marker_evidence` is **not** `CaseJudgment` (it is the geometry of
a possible marker, not a decided case). `irab_position_evidence` is **not**
`IrabFinalDecision` (it is a candidate locus, not a verdict).

## 4. Q2 — DEFER vs BLOCK

**DEFER** — i‘rab geometry admissible but underdetermined:

| Reason | Marking |
| --- | --- |
| `irab_context_underspecified` | `[DESIGN]` |
| `irab_position_underspecified` | `[DESIGN]` |
| `case_marker_underspecified` | `[DESIGN]` |
| `waqf_readiness_underspecified` | `[DESIGN]` |
| `carried_relation_geometry_residuals` | `[DESIGN]` |
| `irab_identity_underspecified` | `[DESIGN]` |

**BLOCK** — structural contradiction or forbidden leakage:

| Reason | Marking |
| --- | --- |
| `irab_context_blocked` | `[CANON]` (spec `blockers`) |
| `irab_position_conflict` | `[CANON]` (spec `invalidating_differences`) |
| `identity_collapse_blocked` | `[DESIGN]` (mirrors P9/P10 guard) |
| `forbidden_output_attempted` | `[DESIGN]` (mirrors P9/P10 guard) |

Verdict precedence follows P9/P10: BLOCK (forbidden → position-conflict →
context/identity-collapse) before DEFER (underspecified reasons) before ACCEPT.

## 5. Q3 — Upstream Reachability (honest)

- P11 requires an **accepted P10 `RelationGeometryCandidate`** `[CANON]`.
- Implemented P10 ACCEPT currently arises **only from verb-sequence structures**
  (the P6 `VerbalSignified` gate admits verbs, not nouns → only verb units reach
  P8→P9→P10). So P11 should initially be tested **only on those structures** (e.g.
  `ضَرَبَ كَتَبَ`, `ضَرَبَ كَتَبَ فَعَلَ`).
- **Do not force** noun-subject examples (e.g. `كَتَبَ زَيْدٌ`) to pass: they never
  reach accepted P10 today, and P11 **must not fabricate i‘rab geometry from
  ordinary nouns** that never reached accepted P10.
- This is an honest upstream limit (P6 VerbalSignified scope), **independent of
  P11** — flagged, not forced.

## 6. Q4 — Identity Preservation

- `I(c)` preserves **`relation_geometry_identity`** from P10 `[CANON]`.
- P11 must preserve the **transitive P9 sentence/multi-unit identity** beneath P10
  `[DESIGN]` — the ordered units are **not** collapsed into a single i‘rab identity.
- I‘rab evidence (position / case-marker / waqf-readiness) lives strictly in
  **trace `T(c)`**, never identity `I(c)` `[CANON principle]`.
- `I(c)` and `T(c)` remain **disjoint** (kernel `identity ∩ trace = ∅`)
  `[CANON principle]`.
- Optional `[DESIGN]`: `T(c)` may include `irab_position_trace`, `case_marker_trace`,
  `waqf_readiness_trace` for auditability (trace-only; never identity).

## 7. Q5 — Residuals

Use canonical names verbatim where they exist; the following are **`[DESIGN]`
proposals** consistent with the P9/P10 `deferred_*` / kernel `blocking_*`
convention:

**Proposed DEFER residuals `[DESIGN]`:**

- `deferred_irab_context_underspecified`
- `deferred_irab_position_underspecified`
- `deferred_case_marker_underspecified`
- `deferred_waqf_readiness_underspecified`
- `deferred_carried_relation_geometry_residuals`
- `deferred_irab_identity_underspecified`

**Proposed BLOCK residuals:**

- `blocking_irab_context_blocked` (wraps `[CANON]` `irab_context_blocked`)
- `blocking_irab_position_conflict` (wraps `[CANON]` `irab_position_conflict`)
- `blocking_identity_collapse_blocked` `[DESIGN]`
- `blocking_forbidden_output_attempted` `[DESIGN]`

Note: as in P9/P10, the kernel surfaces blocks as `blocking_fariq_present` with the
specific `[CANON]` token (`irab_context_blocked` / `irab_position_conflict`) driving
the `فارق` machinery; the `blocking_*` names above are the proposed surfaced
residual labels.

## 8. Q6 — Licensed Priors

- P11 may open **only `ifadah_speech_force_candidates`** `[CANON]`
  (`target_boundary_opens`), and **only on ACCEPT**.
- P11 must **not emit `IfadahCandidate`** itself `[CANON]` (`forbidden_outputs`).
- P11 must **not emit P12 candidates** `[CANON]`.
- P11 must **not emit** `CaseJudgment`, `IrabFinalDecision`, hukm, reality, meaning,
  dalālah, or final interpretation `[CANON]`.
- P11 also **closes** `irab_geometry_candidates` `[CANON]`
  (`target_boundary_closes`) — the prior P10 opened.

**Stress:** opening `ifadah_speech_force_candidates` is **not** ifādah assignment and
**not** a speech-force judgment; it is only a downstream **structural prior**
licensing P12's later question.

## 9. Q7 — Forbidden Outputs

**Keep the canonical P11 forbidden list exactly `[CANON]`:**

- `IfadahCandidate` (P12) · `CaseJudgment` · `IrabFinalDecision` · `HukmCandidate`
  · `RealityClaim` · `FinalMeaning`
- forbidden changes: `assign_case_judgment` · `assign_ifadah` · `assign_hukm`

**Defense-in-depth hardening `[DESIGN]` — future implementation consideration
only** (confirm canonically before referencing; the constitution covers them in
prose, not yet as constants):

- `MeaningCandidate`
- `DalalahCandidate` / dalālah judgment
- "final syntax labels" as claims
- explicit i‘rab-verdict strings (e.g. a token asserted *as*
  marfū‘/manṣūb/majrūr/majzūm) as claims

No implementation change required here; flagged for the future implementation gate.

## 10. Q8 — Required Proof Tests for Future Implementation

**Design-only list (no tests authored now):**

- P11 registry-implemented test, *if later authorized* (`build_p11_implemented_registry`).
- P12 still SPECIFIED-only test.
- Freeze ACTIVE above P11 test.
- No `build_p12_implemented_registry` test (the guard shifts up one phase at the P11
  gate).
- P11 **ACCEPT** from accepted P10 `RelationGeometryCandidate` with
  `irab_context_closed` + `irab_position_evidence` + `case_marker_evidence` +
  `waqf_readiness_evidence`.
- P11 **DEFER** tests, one per underdetermined residual (§7).
- P11 **BLOCK** tests: `irab_context_blocked`, `irab_position_conflict`, identity
  collapse, forbidden-output attempt.
- Identity-preservation test P10 → P11 (`relation_geometry_identity` + transitive
  multi-unit identity preserved, not collapsed).
- Trace/identity separation test (`I ∩ T = ∅`).
- No-leakage test: no `IfadahCandidate`, no P12, no `CaseJudgment`, no
  `IrabFinalDecision`, no i‘rab verdict, no case decision, no ifādah, no meaning, no
  dalālah, no hukm, no reality, no final interpretation.
- `run_qiyas` integration test: P11 opens **only** behind an accepted P10 and does
  **not** open P12.

## 11. Summary of Proposed `[DESIGN]` Constants

| Aspect | Value | Marking |
| --- | --- | --- |
| ACCEPT threshold | ≥1 accepted P10 `RelationGeometryCandidate` + `irab_context_closed` + `irab_position_evidence` + `case_marker_evidence` + `waqf_readiness_evidence`; no forbidden evidence | inputs `[CANON]`; no-forbidden clause `[DESIGN]` |
| DEFER residuals | `deferred_irab_context_underspecified`, `deferred_irab_position_underspecified`, `deferred_case_marker_underspecified`, `deferred_waqf_readiness_underspecified`, `deferred_carried_relation_geometry_residuals`, `deferred_irab_identity_underspecified` | `[DESIGN]` |
| BLOCK residuals | `irab_context_blocked`, `irab_position_conflict` | `[CANON]` |
| BLOCK residuals (added) | `identity_collapse_blocked`, `forbidden_output_attempted` | `[DESIGN]` |
| Identity representation | preserve `relation_geometry_identity` + transitive multi-unit identity; i‘rab evidence trace-only; `I ∩ T = ∅` | id `[CANON]`; multi-unit-preservation `[DESIGN]` |
| Licensed prior | open **only** `ifadah_speech_force_candidates` (ACCEPT only); close `irab_geometry_candidates` | `[CANON]` |
| Forbidden-output hardening (optional) | `MeaningCandidate`, `DalalahCandidate`/dalālah judgment, final syntax labels, explicit i‘rab-verdict strings | `[DESIGN]` (future gate) |

## 12. Non-Authorization Clause

**This design-resolution note does not authorize implementation.** A separate
explicit authorization is required before any of:

- registry changes
- runtime changes
- schema changes
- tests
- P11 candidate emission
- any PR that implements P11 behavior

**P11 remains SPECIFIED-only. P11–P12 remain SPECIFIED-only. Freeze remains ACTIVE
above P10.**
