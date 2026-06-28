# BOUNDARY CONSTITUTION — Saleh/Qiyas

> **دستور الحدود — قواعد نشر الحدود واستهلاكها**
>
> **Level:** 2 — Constitution (governing rules only). Governed by
> [`ARCHITECTURE_LEVELS.md`](ARCHITECTURE_LEVELS.md); subordinate to
> [`PROJECT_MATHEMATICAL_FOUNDATION.md`](PROJECT_MATHEMATICAL_FOUNDATION.md)
> (Theory) and consistent with [`PROJECT_CONSTITUTION.md`](PROJECT_CONSTITUTION.md)
> (Qiyas Constitution).
>
> **This document sets RULES ONLY.** It contains **no technical fields, no schema,
> no dataclass, no code, no runtime behavior.** Every concrete field, type, or
> version schema belongs to a **Level-3 Specification**
> (`LICENSED_BOUNDARY_SPECIFICATION_v1.md`, to be drafted later) — **never here**.
>
> **Scope:** how a **producer** **publishes** a boundary, and how a **consumer**
> **consumes** it. It introduces no layer and no registry change (registry stays
> 19, no P13, P12 terminal).
>
> **Producer-agnostic (ADR-6).** Throughout this document, **“the producer”**
> means *any implementation governed by Qiyas Theory that publishes a boundary*,
> and **“the consumer”** means *any system that consumes a published boundary*.
> **Qiyas is the first producer, not the only possible one.** This is a
> constitution for the **theory applied**, not for a single repository. It is a
> direct consequence of the theory principle *Internal Inference vs External
> Consumption* (`PROJECT_MATHEMATICAL_FOUNDATION.md` §26).

---

## §1 — Purpose and the published-boundary law

A **boundary** is the licensed relation between two independent systems. The
governing law, inherited from the Theory (`Layer = DomainBoundary`) and extended
to systems:

> **Just as layers within a system never jump, systems never communicate
> directly. A system may relate to another only through a published, versioned
> boundary — proved as a licensed transition, never as a raw data copy or a
> direct dependency on internal types.**

A boundary is **published by the producer** (Qiyas today; any Qiyas-governed
producer in general) and **consumed by a consumer** (any Qiyas-derived project).
Publishing is itself an act under qiyas: nothing crosses unless it is licensed.

---

## §2 — What the producer MAY publish

A producer may publish across a boundary **only**:

1. **Licensed, accepted candidates** — structural results the producer has
   already proved (ACCEPTED) under its own constitution.
2. **Preserved identity** — the inherited identity of the published unit.
3. **Inherited trace as evidence** — the proof trace, carried as evidence only.
4. **Rank** — the established evidence rank of the published unit.
5. **Residuals** — explicit, named residuals attached to the unit.
6. **Structural geometry evidence** — slot / cell / syllable / boundary /
   segmentation evidence, as **read-only inherited evidence**.
7. **Provenance markers** — safe source/version markers that let the consumer
   audit where the unit came from.

Everything publishable must already be **candidate-level and licensed**. The
producer publishes *what it has proved*, not *what it might mean*.

---

## §3 — What the producer MUST NOT publish

A producer must never publish across a boundary:

1. **Internal types** — no internal class/representation is exposed; the consumer
   must depend on the **Specification**, not on the producer's internals.
2. **Unaccepted results** — nothing `DEFERRED`, `BLOCKED`, suspicious,
   quarantined, rejected, or pending is published as if accepted.
3. **Final claims** — no final meaning, hukm, tafsir, truth/reality, or final
   case/i'rab judgment. (The producer's own constitution forbids these; the
   boundary cannot launder them.)
4. **Raw unlicensed surface as authority** — a raw string is not a boundary; a
   surface may appear only as a display attribute of a licensed unit, never as the
   identity and never as the scientific input.
5. **Ignored raw fields** — any field the producer treats as ignored evidence
   (e.g. external role/case/i'rab/meaning) is **not** promoted into a published
   field.
6. **Hidden residuals** — no failure may be published as success; residuals are
   never silently dropped (see §5).
7. **Mutable/unversioned payloads** — nothing is published outside a declared,
   versioned boundary (see §6).

---

## §4 — How identity, rank, and trace are preserved

The boundary must preserve the Theory's invariants across systems:

1. **Identity ≠ Trace.** Published identity and published trace remain disjoint;
   trace is evidence, never identity.
2. **Identity preservation.** The published unit's identity must contain the
   identities of its sources; publishing must not erase or rewrite identity.
3. **Trace is inherited as evidence.** The consumer reads the trace to audit and
   to compose new evidence — it may not treat inherited trace as its own identity.
4. **Rank is inherited and composes by meet.** A consumer may only lower rank by
   meet/min when adding its own evidence; it may never raise the rank above what
   the boundary published.
5. **Provenance is auditable.** Identity, rank, and trace must remain traceable
   back to the producing system through the published provenance markers.

How these are *encoded* (names, fields, formats) is a **Specification** concern,
not a constitutional one.

---

## §5 — How residuals are managed

1. **No silent success, no silent failure.** Every non-closure is published as an
   explicit, named residual.
2. **Residuals cross the boundary intact.** A consumer inherits the producer's
   residuals; it may add new residuals but may not delete or hide inherited ones.
3. **Ambiguity is residualized, not resolved silently.** Where the producer left
   ambiguity (e.g. multiple candidates), the boundary carries that ambiguity as a
   residual; the consumer must treat it as such.
4. **A residual is not a verdict.** Inherited residuals are inputs to the
   consumer's own qiyas — never a final judgment.

The catalogue of concrete residual names is a **Specification** matter.

---

## §6 — How versions are managed

1. **Every boundary is versioned.** A boundary is published under an explicit
   version (`v1`, `v2`, …). There is no unversioned boundary.
2. **A published version is immutable.** Once published, a version's meaning does
   not change; corrections are made by publishing a **new version**, not by
   mutating an old one.
3. **Theory does not move with versions.** Bumping a boundary version (`v1 → v2`)
   must not require any change to the Theory; the Theory is invariant under
   versioning.
4. **Producer rewrites do not break consumers.** A producer may rewrite its
   internals freely as long as it continues to honor (or supersede) the published
   version the consumer relies on.
5. **Deprecation is explicit.** Retiring a version is an announced, gated act, not
   a silent removal.

Concrete version numbers, schemas, and field-level compatibility live in the
**Specification**.

---

## §7 — How conformance is tested

1. **Both sides test against the boundary, not against each other's internals.**
   The producer proves it *emits* a conformant boundary; the consumer proves it
   *accepts only* a conformant boundary.
2. **Identity/trace disjointness is a conformance obligation.** A boundary
   instance that mixes identity and trace is non-conformant.
3. **Residual integrity is a conformance obligation.** Dropping or hiding an
   inherited residual is non-conformant.
4. **Rank monotonicity is a conformance obligation.** A consumer that raises rank
   above the published rank is non-conformant.
5. **Rejection of raw/unlicensed input is a conformance obligation.** A consumer
   that accepts a raw string (or any non-licensed input) in scientific/runtime
   mode is non-conformant.
6. **Version conformance.** A consumer must declare which boundary version it
   consumes and must reject inputs that do not match that version.

*How* these are exercised (golden cases, schema checks) is a Specification +
Implementation concern; *that* they must hold is constitutional.

---

## §8 — What a consumer MUST NOT re-prove

A consumer relates to a published boundary by a **licensed transition** and:

1. **Must not re-prove inherited legality.** Anything the producer already proved
   (e.g. Unicode membership, typed classification, letter/haraka identity, slot /
   cell / syllable / boundary legality, word-surface licensing, and any other
   accepted lower carrier) is **inherited, not re-derived**.
2. **May read, must not overwrite.** Inherited evidence is **read-only**. A
   consumer may inspect it; it may not mutate or silently replace it.
3. **Reconciliation is an explicit transition.** If a consumer needs to revisit an
   inherited proof, it must declare an explicit **reconciliation transition** that
   *compares* and *residualizes disagreement* — it never silently overrides the
   producer.
4. **Output stays candidate-level.** A consumer's results remain candidates; the
   boundary does not authorize any final meaning/root/hukm/truth.

---

## §9 — How the boundary prevents inter-system layer jump

1. **No direct internal access.** A consumer that reaches into producer internals
   (bypassing the published boundary) has performed an illegal **inter-system
   jump** and is rejected.
2. **No skipping the licensed transition.** Consumption must go through the
   licensed transition (Asl/Far/illah/wasf/fariq/evidence/rank/identity/residual);
   a raw function call or string pass is an illegal jump.
3. **No publishing across more than one boundary at once.** A producer may not
   expose a unit of layer `n` as if it were a unit of a far-downstream layer
   without the intermediate licensed boundaries — the system-level analogue of
   *no layer jump*.
4. **Every jump attempt is an explicit residual/BLOCK**, never a silent success.

---

## §10 — Relationship to other levels

- **Theory** (`PROJECT_MATHEMATICAL_FOUNDATION.md`) — supplies the invariants this
  document applies at the system boundary.
- **Qiyas Constitution** (`PROJECT_CONSTITUTION.md`) — governs Qiyas internals;
  this document governs what Qiyas may publish.
- **Specification** (`LICENSED_BOUNDARY_SPECIFICATION_v1.md`, later) — defines the
  concrete fields/types/version schema. **All fields live there, not here.**
- **Consumer Constitution** (later, **in the consumer repo**) — governs how a
  specific consumer obeys §8/§9 on its own side.

---

**Document status:** Level-2 governance (rules only). Subordinate to the Theory
and to `ARCHITECTURE_LEVELS.md`.
**Behavioral effect:** none. No fields, no schema, no code, no registry change.
**Next (not now, separate gate):** `LICENSED_BOUNDARY_SPECIFICATION_v1.md` —
the technical fields of the first published boundary.
