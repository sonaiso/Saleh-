# SCG-P9 SentenceGeometry Design Gate

> **Descriptive design-gate note — not a constitution.** It introduces no new
> layer, theory name, or framework rename, and it changes no constitutional
> boundary. It is **subordinate to** `SENTENCE_GEOMETRY_CONSTITUTION.md` (SCG-P9
> specification), the SCG registry/spec entries, and the existing
> freeze/forbidden-output governance. **Where this note and the canonical
> spec/code differ, the canonical spec/code wins.** This note **authorizes no
> runtime, registry, schema, or test change**, and **no P9 implementation**.

## 1. Status

- **P9 is not implemented.** Its registry status is `SPECIFIED` (via
  `build_p9_specified_registry`); there is no `build_p9_implemented_registry`.
- **P9–P12 remain SPECIFIED-only.** Registry count stays **19**.
- **The freeze remains ACTIVE** for P9+ (no P9+ layer is IMPLEMENTED).
- This note is **descriptive** and subordinate to the existing constitutions/specs.
- This note **authorizes no runtime, registry, schema, or test change**, and a
  separate explicit authorization is required before any P9 implementation work.

## 2. Boundary question

> What keeps `SentenceGeometryCandidate` a **multi-unit structural geometry**
> candidate only, and prevents it from becoming **syntax, i‘rab, dalālah,
> meaning, hukm, reality, or final interpretation**?

## 3. Existing answer from the P9 specification

The boundary is already largely fixed by `SENTENCE_GEOMETRY_CONSTITUTION.md` and
the P9 registry spec; this design gate **consolidates**, it does not invent:

- P9 **consumes accepted P8 `AmilMamulCandidate`** (origin
  `P8_AMIL_MAMUL → AmilMamulCandidate`); it is the only upstream path (`P8 → P9`).
- P9 organizes عامل–معمول relation candidates into a **sentence geometry** — a
  *spatial arrangement* of relation candidates (إسناد، نعت، حال، معطوف، مفعولية)
  — explicitly defined as a "candidate-only structural composition
  (إمكان هندسة جملية)," **not a grammatical ruling**.
- P9's **only allowed output is `SentenceGeometryCandidate`** — "a candidate
  (إمكان), never a judgment."
- Sentence-*type* evidence is "recorded as evidence, never closed into a
  verdict"; **i‘rab and ifadah remain strictly downstream and candidate-only.**
- P9 **preserves `amil_mamul_candidate_identities`**, keeps explicit residuals
  (no silent failure), and **opens `relation_geometry_candidates` only as a
  prior** for SCG-P10 — never produced by P9.
- P9's spec already **forbids** `RelationGeometryCandidate`,
  `IrabGeometryCandidate`, `IfadahCandidate`, `HukmCandidate`, `RealityClaim`,
  `FinalMeaning`, `IrabCandidate`, `CaseJudgment`, with
  `forbidden_changes = (assign_irab, assign_case, assign_ifadah)`.

In short: the answer to §2 is *already present* — P9 is a candidate-only,
identity-preserving arrangement of P8 relation candidates that opens a downstream
prior and is explicitly barred from any i‘rab/ifadah/judgment object. The design
gate's task is to apply the P3–P8 information-gain discipline to it without
crossing that line.

## 4. Permitted inputs

P9 may consume only:

- accepted **P8 `AmilMamulCandidate`** traces (`amil_mamul_refs`);
- preserved upstream **identity sets** (`amil_mamul_candidate_identities`);
- **multi-unit structural adjacency** evidence across units;
- **boundary evidence** across units (per the spec's `isnad_boundary_evidence`,
  condition `sentence_boundary_closed`);
- **ordering / contiguity** evidence;
- **sentence-type *evidence*** (recorded as evidence only, never a type verdict;
  condition `amil_mamul_candidates_ready`);
- **residuals** carried from prior layers where relevant.

P9 **must not consume** (as inputs to its decision): lexical meaning; semantic
interpretation; i‘rab assignment; case judgment; syntactic role labels treated as
final claims; or external world/reality facts.

## 5. Permitted output

The only permitted output is **`SentenceGeometryCandidate`**, which must be:

- candidate-only;
- potential-only;
- identity-preserving (carries forward `amil_mamul_candidate_identities`);
- trace-separated (`I(c)` disjoint from `T(c)`);
- residual-preserving;
- proof-relevant;
- non-final.

It may open only the licensed structural prior **`relation_geometry_candidates`**
(toward SCG-P10) — never a final judgment, and never the P10 candidate itself.

## 6. Must-not-emit list

P9 must not emit (exact spec names first; broader sub-semantic exclusions follow):

- **From the P9 forbidden-output spec:** `IrabCandidate`, `CaseJudgment`,
  `IfadahCandidate`, `HukmCandidate`, `RealityClaim`, `FinalMeaning`,
  `RelationGeometryCandidate` (P10), `IrabGeometryCandidate` (P11).
- **Forbidden changes (spec):** `assign_irab`, `assign_case`, `assign_ifadah`.
- **Also excluded, consistent with the cascade's sub-semantic boundary** (no SCG
  layer emits these): `MeaningCandidate`, `DalalahCandidate` / dalālah judgment,
  final syntax labels, and any final interpretation object. (These are not in
  P9's explicit `forbidden_outputs` tuple today; whether to list them there
  explicitly is an open design question — see §9.7.)

## 7. ACCEPT / DEFER / BLOCK discipline (design level only)

Applying the P3–P8 information-gain discipline to P9, at design level:

- **ACCEPT** — the multi-unit structural geometry is *sufficient* to open the
  licensed sentence-geometry prior (`relation_geometry_candidates`).
- **DEFER** — the units are structurally admissible but **under-determined**;
  preserve the residual and open **no** downstream commitment. *(Note: the P9
  spec currently defines BLOCK reasons but no DEFER reason; a
  `sentence_geometry_underspecified`-style defer reason would be a design
  addition, mirroring P3–P8 — see §9.2 / §9.5.)*
- **BLOCK** — the multi-unit geometry contradicts the required structural
  preconditions; the spec already names these as `sentence_structure_blocked`
  (blocker) and `sentence_type_conflict` (invalidating difference).

Stressed boundary: **ACCEPT is not sentence meaning; not syntax; not i‘rab; not
hukm.** ACCEPT only *licenses the next structural question* (the relation-geometry
prior).

## 8. Kernel and governance enforcement

The boundary must be enforced structurally, exactly as for P3–P8:

- candidate-only output marker (`CandidateOnly`);
- preserved identity `I(c)` = union of upstream identities
  (`amil_mamul_candidate_identities`);
- trace `T(c)` kept disjoint from identity;
- a per-layer **forbidden-output set** checked by the kernel (including the
  constitutional `HukmCandidate` / `RealityClaim` / `FinalMeaning` triple plus the
  P9 list in §6);
- the **freeze guard** for P9+ (`IMPLEMENTED` not permitted while the freeze is
  ACTIVE; no `build_p9_implemented_registry`);
- no downstream-candidate leakage (only the `relation_geometry_candidates` prior
  is opened, never a P10+ candidate);
- no semantic / i‘rab / hukm / reality object, and no final-judgment object, under
  any verdict.

## 9. Open design questions (design only — not implementation tasks)

1. What is the **minimal multi-unit evidence** sufficient for a P9 ACCEPT (e.g.
   ≥2 accepted P8 traces + a closed isnad boundary)?
2. What structural condition should cause **DEFER rather than BLOCK**
   (under-determination vs. contradiction), and what defer reason name should
   carry it?
3. What counts as **adjacency** — textual adjacency, normalized-token adjacency,
   or *structurally licensed* adjacency derived from upstream evidence?
4. How should P9 **preserve identity across multiple upstream P8 traces** (union,
   ordered tuple, or set) while keeping identity disjoint from trace?
5. What **residuals** must P9 emit for under-determined sentence geometry, and how
   do they compose with carried-up P3–P8 residuals?
6. What **exact priors** may P9 open (the spec licenses
   `relation_geometry_candidates`) — and is that the complete licensed set, with
   nothing else opened?
7. Which **forbidden-output constants** must be referenced explicitly (e.g. adding
   `MeaningCandidate` / `DalalahCandidate` to the P9 forbidden tuple for
   defense-in-depth, vs. relying on the absolutes)?

## 10. Non-authorization clause

This design gate **does not authorize implementation.** A separate, explicit
authorization is required before any of:

- registry changes;
- runtime changes;
- schema changes;
- tests;
- P9 candidate emission;
- any PR that implements P9 behavior.
