# SCG-P11 IrabGeometry Design Gate

> **Type:** Descriptive **design-gate note** — *not* a constitution. It introduces
> no new layer, no new theory name, and does not rename the framework. It is
> **subordinate** to `IRAB_GEOMETRY_CONSTITUTION.md`, the canonical P11
> `LayerSpec` (`master_registry_seed.py`), `RELATION_GEOMETRY_CONSTITUTION.md`
> (P10 predecessor), and the P9/P10 design-gate materials. **Where this note and
> the canonical spec/code differ, the canonical spec/code wins.**

## 1. Status

- **P11 is not implemented.** The P11 `LayerSpec` is `PLANNED` in the seed,
  reaching only `SPECIFIED` via `build_p11_specified_registry`.
- **P11–P12 remain SPECIFIED-only.** Implemented phases stop at P10
  (`build_p10_implemented_registry`, merge `cc94ac0`). There is no
  `build_p11_implemented_registry`.
- **Freeze remains ACTIVE above P10.** No phase beyond SCG-P10 is `IMPLEMENTED`;
  registry count stays **19**.
- This note is **descriptive and subordinate** to the documents named above. It
  invents nothing.
- This note **authorizes no runtime, registry, schema, or test change**, and emits
  no P11 candidate. **A separate explicit authorization is required before any
  P11 implementation work.**

## 2. Boundary Question

What keeps `IrabGeometryCandidate` the **geometry of i‘rab *positions and
possibilities*** (المواضع الإعرابية وإمكاناتها) — and prevents it from becoming an
**i‘rab judgment, a case decision, ifādah, hukm, reality, meaning, or final
interpretation**? This is the most judgment-adjacent layer in Saleh-: it names
*where* i‘rab could fall and *what* it could be, **never** that a token *is*
marfū‘/manṣūb/majrūr/majzūm as a verdict.

## 3. Existing Answer from the P11 Specification

Strictly from the `LayerSpec` (`master_registry_seed.py` §P11) and
`IRAB_GEOMETRY_CONSTITUTION.md`; nothing added:

- **Expected input:** origin `P10_RELATION_GEOMETRY` → `RelationGeometryCandidate`.
  Conditions `relation_geometry_established`, `irab_context_closed`; required fields
  `relation_geometry_ref`, `irab_position_evidence`, `case_marker_evidence`,
  `waqf_readiness_evidence`.
- **Expected output:** `IrabGeometryCandidate` only (candidate-only — "إمكان موضع
  إعرابي").
- **May open:** `target_boundary_opens = (ifadah_speech_force_candidates,)` —
  opened as a **prior for SCG-P12**, never produced. **Closes**
  `irab_geometry_candidates` (the prior P10 opened).
- **Must not emit:** `forbidden_outputs = _ABSOLUTE_FORBIDDEN + (CaseJudgment,
  IfadahCandidate, IrabFinalDecision)`; `forbidden_changes = (assign_case_judgment,
  assign_ifadah, assign_hukm)`. `forbidden_direct_next_layer_ids = ()` — P11→P12 is
  the single licensed forward edge.
- **Blocker / invalidating:** `irab_context_blocked` / `irab_position_conflict`.

## 4. Permitted Inputs

- accepted **P10 `RelationGeometryCandidate`** traces (only path: `P10 → P11`) `[CANON]`;
- preserved **`relation_geometry_identity`** (and, transitively, the P9
  sentence_geometry / multi-unit identity beneath it) `[CANON]`;
- **i‘rab-position, case-marker, waqf-readiness evidence** as *structural
  possibility only* `[CANON]`;
- carried residuals (nothing hidden).

P11 must **not consume**: semantic meaning, dalālah, a decided case, hukm, reality,
or any final interpretation.

## 5. Permitted Output

The only permitted output is **`IrabGeometryCandidate`** — candidate-only,
potential-only, identity-preserving (`relation_geometry_identity` preserved,
multi-unit structure not collapsed), trace-separated (`I∩T=∅`), residual-preserving,
proof-relevant, **non-final**. It must **not** be an i‘rab judgment, case decision,
ifādah, hukm, reality, meaning, or final syntax label. I‘rab positions are *mapped*
(`allowed_changes = map_irab_positions`); no case is decided.

## 6. Must-Not-Emit List

Canonical `[CANON]`: `IfadahCandidate` (P12) · `CaseJudgment` · `IrabFinalDecision`
· `HukmCandidate` · `RealityClaim` · `FinalMeaning`; forbidden changes
`assign_case_judgment` · `assign_ifadah` · `assign_hukm`. Defense-in-depth
`[DESIGN]` (confirm canonically before referencing): `MeaningCandidate`,
`DalalahCandidate`/dalālah judgment, "final syntax labels" as claims.

## 7. ACCEPT / DEFER / BLOCK Discipline

- **ACCEPT** — i‘rab-position geometry is sufficient to **open only**
  `ifadah_speech_force_candidates`, and nothing more.
- **DEFER** — i‘rab geometry admissible but underdetermined (position / case-marker
  / waqf-readiness underspecified, carried residuals, identity underspecified);
  preserve residual, open no unsafe downstream commitment.
- **BLOCK** — `irab_context_blocked` (no usable relation geometry / context not
  closed), `irab_position_conflict`, or a forbidden-output attempt.

**Stress:** ACCEPT is **not** an i‘rab verdict, **not** a case decision, **not**
ifādah, **not** hukm. ACCEPT only licenses the next structural question (the
ifādah/speech-force prior for P12). Mapping a *possible* marfū‘ position is
geometry; declaring a token *is* marfū‘ is a judgment — forbidden.

## 8. Kernel and Governance Enforcement

Same machinery as P3–P10 (no new mechanism): candidate-only marker; preserved
`I(c)` = `relation_geometry_identity` (multi-unit structure intact); `T(c)`
disjoint from identity; forbidden-output set via kernel `فارق:`/blocking; **freeze
guard above P10 in the current state — no `build_p11_implemented_registry` exists
while P11 remains SPECIFIED-only; at any future P11 implementation gate, this guard
must shift to no `build_p12_implemented_registry`, with P12 remaining
SPECIFIED-only**; registry count fixed at 19; governance tests (REC-2,
freeze-status, responsibility matrix, `test_master_registry_p11_specified.py`) hold
the line; no downstream (P12) candidate leakage; no judgment/case/ifādah/hukm/
reality/final objects in output or trace.

## 9. Open Design Questions

1. What exact `irab_position_evidence` + `case_marker_evidence` +
   `waqf_readiness_evidence` is sufficient for P11 **ACCEPT** (and how is
   `irab_context_closed` evidenced)?
2. What should P11 **DEFER** rather than **BLOCK** (underdetermined position vs.
   `irab_position_conflict`)?
3. Does the current pipeline produce enough structure for P11 to ACCEPT at all, or
   — like the P10/P6 limit — will only certain upstream shapes reach it? (honesty
   over forcing).
4. How does P11 preserve `relation_geometry_identity` + the P9-derived multi-unit
   identity without collapsing it into one i‘rab identity?
5. What residuals must P11 emit for underdetermined i‘rab geometry (P9/P10
   `deferred_*` naming convention)?
6. What priors may P11 open (`ifadah_speech_force_candidates` only) without crossing
   into a verdict?
7. Which forbidden-output constants must be referenced explicitly (and must
   `Meaning`/`Dalalah` be canonically confirmed first)?
8. What tests prove P11 emits no P12 object and **no i‘rab verdict / case decision /
   hukm / reality / final** — the judgment-adjacency guard?

## 10. Non-Authorization Clause

**This design gate does not authorize implementation.** A separate explicit
authorization is required before: registry changes · runtime changes · schema
changes · tests · P11 candidate emission · any PR that implements P11 behavior.
**P11 remains SPECIFIED-only. P11–P12 remain SPECIFIED-only. Freeze remains ACTIVE
above P10.**
