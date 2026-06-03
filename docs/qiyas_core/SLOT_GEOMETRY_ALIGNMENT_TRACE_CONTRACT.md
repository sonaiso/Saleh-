# SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> `SlotGeometry` alignment-trace contract. No code, no tests, no
> implementation are changed by this PR.
>
> **Phase-1 status statement:**
>
> ```
> Phase 1 — single-slot pipeline is complete on main.
>
>     raw text
>     → SequenceContextTokenizer
>     → UnicodeQiyas
>     → TypedCodePointClassificationQiyas
>     → LetterIdentityQiyas / HarakaFunctionQiyas / PositionQiyas
>     → ConditionedTypedSequenceQiyas
>     → SlotQiyas
>     → SlotCandidate
>
> The single-slot phase is not open work in this PR.
> This PR does not revisit, reopen, refactor, or repair the Phase-1
> pipeline. This PR only defines the next controlling contract for
> SlotGeometry.
> ```
>
> **Authority basis:**
> `CLAUDE.md` §0 / §3 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `RESET_CONSTITUTION.md` §1 / §3 / §4,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §2 / §6 / §7 / §8 / §9 / §10 / §11 / §12,
> `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3 / §5 / §9 / §11 / §12,
> `PR_SCHEDULING_POLICY.md` §1.1 / §5 / §8,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4.
>
> **Governing one-liner:**
>
> ```
> SlotGeometryQiyas consumes only SlotCandidate*.
> ```
>
> ```
> SlotGeometryQiyas لا يستهلك إلا SlotCandidate*.
> ```

---

## 0. Phase-1 Status — Settled

Phase 1 — the single-slot pipeline — is **complete on `main`**:

```text
raw text
  → SequenceContextTokenizer            (Z2; merged)
  → UnicodeQiyas                        (canonical; merged)
  → TypedCodePointClassificationQiyas   (Z4 declassification; merged)
  → LetterIdentityQiyas
  | HarakaFunctionQiyas
  | PositionQiyas                       (parallel proofs; merged)
  → ConditionedTypedSequenceQiyas       (Z3; merged)
  → SlotQiyas                           (slot composition; merged)
  → SlotCandidate                       (Phase-1 output)
```

Phase 1 has been **constitutionally validated** under the
`PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`, and
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` discipline. The driver wiring
in `run_qiyas.py` is tokenizer-driven; whitespace and boundary
context flow as pre-qiyas tokenizer evidence; carrier-binding is
gated on segment context; `SlotQiyas` emits `SlotCandidate` only
through `slot.composition` with an `alignment_ref` trace.

Two non-negotiable statements:

```text
The single-slot phase is not open work in this PR.
This PR does not revisit, reopen, refactor, or repair the Phase-1
pipeline. This PR only defines the next controlling contract for
SlotGeometry.
```

Six identity statements that this contract takes as **given**:

```text
SlotCandidate is the completed output of Phase 1.
SlotCandidate is not SlotGeometry.
SlotCandidate is not DalalahCandidate.
SlotCandidate is not FinalMeaning.
SlotCandidate is not HukmCandidate.
SlotCandidate is not RealityClaim.
```

This document **does not** implement `SlotGeometryQiyas`, does
**not** implement `SlotBindingEvidence`, does **not** modify any
file under `src/qiyas_core/`, `tests/qiyas_core/`, `experimental/`,
or `run_qiyas.py`, and does **not** modify any existing
constitutional document. It only fixes the contract that
`SlotGeometryQiyas` must satisfy *before* any implementation PR may
be opened.

---

## 1. The Governing Law

`SlotGeometryQiyas` is a Phase-2 layer that consumes the licensed
output of the slot layer and produces a recursive geometry over it.
Its consumption surface is **closed**:

```text
SlotGeometryQiyas may consume only SlotCandidate*.
```

It may **not** directly consume any of the following — each of these
was the responsibility of a strictly earlier Phase-1 layer, and that
work is settled:

```text
raw text
SequenceContextTokenizer markers
UnicodeCandidate
TypedCodePoint
LetterIdentityCarrier
HarakaFunctionCarrier
PositionCarrier
CarrierBindingCandidate
ConditionedTypedSequence outputs
BoundaryCodePoint
ResidualCodePoint
```

In particular, `SlotGeometryQiyas` does **not** re-tokenise the
text, does **not** re-classify codepoints, does **not** re-prove
letter identity or haraka function, does **not** re-derive sequence
position, and does **not** re-prove carrier binding. All of that
work ended at the production of `SlotCandidate`; `SlotGeometryQiyas`
trusts and consumes only that licensed output, never anything
upstream of it.

This consumption rule is the load-bearing constitutional invariant
of this contract. Any future implementation PR that opens a path
from a non-`SlotCandidate` input directly into the slot-geometry
layer is in violation of this contract and must be rejected at
review.

---

## 2. The Consumed `SlotCandidate` Contract

Every `SlotCandidate` that enters `SlotGeometryQiyas` must satisfy
the following structural and provenance conditions. A
`SlotCandidate` failing any one of them must be rejected by
`SlotGeometryQiyas` — never silently consumed.

### 2.1 Required structural fields

```text
candidate_type      == "SlotCandidate"
source_rule_id      == "slot.composition"
output_flags        ⊇ {CandidateOnly}
output_flags        ∩ {HukmCandidate, RealityClaim, FinalMeaning,
                       FinalCaseJudgment, DalalahCandidate} = ∅
identity_ids        non-empty
identity_ids ∩ trace_ids == ∅
rank                ≠ NO_EVIDENCE
```

### 2.2 Required trace audit

The `trace_ids` must carry an `alignment_ref` entry — the
structural witness, written by `SlotLayerAdapter` only when an
explicit `CarrierBindingCandidate` / alignment evidence was
consumed — together with enough source-trace breadcrumbs to
reconstruct the four Phase-1 contributing proofs:

```text
trace_ids must contain alignment_ref
trace_ids must contain enough source trace to audit:
  - letter identity source        (LetterIdentityQiyas)
  - haraka function source        (HarakaFunctionQiyas)
  - position source               (PositionQiyas[*])
  - CTS / carrier-binding source  (ConditionedTypedSequenceQiyas)
```

The four breadcrumbs are independent: each is required, and the
absence of any one is sufficient to reject the `SlotCandidate` from
slot-geometry consumption.

### 2.3 Rejection discipline

A `SlotCandidate` failing §2.1 or §2.2 is **rejected**, not
quietly accepted with a residual. The rejection itself is recorded
as a residual on the geometry-level request so the trail is
auditable, but the rejected candidate may not enter any
`SlotGeometrySeed` or `SlotGeometryExtend` step.

In particular:

```text
A SlotCandidate without an alignment_ref entry in its trace_ids
is rejected.

A SlotCandidate whose source_rule_id is not "slot.composition" is
rejected.

A SlotCandidate whose output_flags contain any final-judgment flag
is rejected.

A SlotCandidate with empty identity_ids is rejected.

A SlotCandidate whose identity_ids ∩ trace_ids is non-empty is
rejected (identity/trace separation invariant; CLAUDE.md §4
invariants 1–3).

A SlotCandidate with rank == NO_EVIDENCE is rejected (§6 of this
document).
```

---

## 3. The Recursive Law — `Seed` and `Extend`

This contract is the slot-layer instance of the general law fixed
in `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §2 / §10. It
specialises that law for `SlotGeometryQiyas`:

### 3.1 `SlotGeometrySeed`

```text
SlotGeometrySeed

  Input  : SlotCandidate
  Output : SlotGeometryCandidate(length = 1)
```

Preconditions: the input satisfies §2 (the consumed `SlotCandidate`
contract).

Postconditions: the output is a `SlotGeometryCandidate` of length 1,
carrying the seed's identities and trace per §6 invariants, with
`output_flags ⊇ {CandidateOnly}`.

### 3.2 `SlotGeometryExtend`

```text
SlotGeometryExtend

  Input  : SlotGeometryCandidate(length = n)
           SlotCandidate                       (the new unit)
           SlotBindingEvidence                 (the licensing evidence)
  Output : SlotGeometryCandidate(length = n + 1)
         | BlockedSlotGeometryCandidate(reason)      (on blocking difference
                                                       or failed gate)
         | DeferredSlotGeometryCandidate(reason)     (on insufficient evidence)
```

Preconditions:

1. `previous.candidate_type == "SlotGeometryCandidate"`,
2. `new_unit` satisfies §2,
3. `binding.candidate_type == "SlotBindingEvidence"`,
4. `previous.layer == "SlotGeometryQiyas"`,
5. `new_unit.layer == "SlotQiyas"` (the immediate predecessor),
6. `binding` is in `INTRA_UTTERANCE` context (§5),
7. `previous`, `new_unit`, and `binding` all carry non-empty
   `identity_ids` disjoint from their `trace_ids`.

Postconditions are the §6 invariants.

### 3.3 The recursive formula

```text
G₁ = Seed(S₁)

Gₙ₊₁ = Extend(Gₙ, Sₙ₊₁, SlotBindingEvidenceₙ)
```

with

```text
Sᵢ = SlotCandidate
Gᵢ = SlotGeometryCandidate(length = i)
```

`Extend` is **not** free concatenation. It is a licensed transition
that consumes a layer-specific `SlotBindingEvidence` and preserves
the six invariants of §6.

---

## 4. Geometric Position Inside a `SlotGeometryCandidate`

Every `SlotCandidate` consumed by a `SlotGeometryQiyas` step occupies
a **geometric** position inside the resulting
`SlotGeometryCandidate`. The four geometric positions are:

```text
isolated  = no previous slot and no next slot
initial   = no previous slot and has next slot
medial    = has previous slot and has next slot
terminal  = has previous slot and no next slot
```

These positions are **geometric only**. They are not semantic; they
do not denote meaning, dalalah, hukm, or reality. They re-use the
discrimination that already exists at the Phase-1 `PositionQiyas`
layer (`POSITION_INITIAL / POSITION_MEDIAL / POSITION_FINAL /
POSITION_ISOLATED`) and re-state it at the slot-geometry level —
but they are an attribute of the geometry, not a new evidence claim.

The admissible geometry shapes by length:

```text
isolated SlotCandidate
  → may seed SlotGeometryCandidate(length = 1)

initial + terminal
  → may form SlotGeometryCandidate(length = 2)

initial + medial* + terminal
  → may form SlotGeometryCandidate(length = n), n ≥ 2
```

Each internal transition `medial → medial`, `initial → medial`,
`medial → terminal` requires a separate `SlotBindingEvidence`
licensing the extension. The geometry's length-1 seed requires no
binding evidence (the `Seed` case of §3.1), only a satisfying
`SlotCandidate`.

A geometric position is recorded as an `attribute:` claim on the
slot-geometry evidence set (per §7 grammar). It is **not** an
identity, **not** a licensing cause, and **not** a final
classification.

---

## 5. `SlotBindingEvidence`

`SlotBindingEvidence` is the layer-specific binding evidence that
licenses a `SlotGeometryExtend` step. It is defined here as a
**contract concept only** — this PR does not implement it as a
runtime type.

### 5.1 Required claims

A valid `SlotBindingEvidence` must witness all of the following:

```text
same INTRA_UTTERANCE segment
  (the previous geometry's tokenizer segment is the new slot's
   tokenizer segment; segment identity is read from the source
   trace, not re-derived from raw text)

ordered_after
  (the new slot's source position is strictly after the previous
   geometry's last consumed slot's source position)

adjacent_or_licensed_distance
  (the new slot is immediately adjacent to the previous geometry's
   last consumed slot, or the gap is licensed by a slot-geometry
   rule's own admissibility predicate)

no whitespace boundary crossing
  (the tokenizer's whitespace_boundary_marker stream contains no
   marker between the previous geometry's last source position and
   the new slot's source position)

no punctuation boundary crossing
  (same for punctuation_boundary_marker)

no tokenizer boundary between slots
  (the more general statement of the two above)

previous geometry remains valid
  (the previous SlotGeometryCandidate still satisfies §6's
   invariants at the time the extension is attempted)

new slot satisfies the SlotCandidate contract
  (the new SlotCandidate satisfies §2)

rank meet is valid
  (the result of the meet in §6.2 is ≠ NO_EVIDENCE; otherwise the
   extension is blocked at the gate, not at the binding evidence
   itself)

identity preservation
trace preservation
residual preservation
no blocking difference
  (the four standing invariants of §6 are all satisfied for the
   extension being proposed)
```

The conditions are conjunctive: every one of them must hold. The
failure of any one is sufficient to block the `Extend` and produce a
`BlockedSlotGeometryCandidate` (or a deferred candidate, depending
on whether the failure was definitive or pending evidence).

### 5.2 Non-portability

`SlotBindingEvidence` is **not portable** between layers.

```text
SlotBindingEvidence is not WordBindingEvidence.
SlotBindingEvidence is not SentenceBindingEvidence.
SlotBindingEvidence must not be reused above the slot layer.
```

A higher layer that needs binding evidence at its own scope must
produce its own (`WordBindingEvidence`, `DiscourseBindingEvidence`,
`TextBindingEvidence`, etc.) under that layer's own contract.
Importing `SlotBindingEvidence` upward is a forbidden cross-layer
binding-evidence reuse (`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`
§6).

### 5.3 Context

`SlotBindingEvidence` operates exclusively in the `INTRA_UTTERANCE`
context (per `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §6). It
must not cross into `DISCOURSE_CONTEXT` or any other higher-layer
context.

---

## 6. Invariants Preserved by Every `Seed` and `Extend`

Every `SlotGeometrySeed` and every `SlotGeometryExtend` must
preserve the canonical septet of `LAYER_CONTRACT_CONSTITUTION.md`
§2.1 and the §4 invariants of `CLAUDE.md`:

```text
identity preservation
trace separation
rank meet semantics
residual preservation
blocking difference annihilation
CandidateOnly safety
no skipped layers
no final meaning
no hukm
no reality claim
```

### 6.1 Identity / trace / residuals

1. **Identity preservation.** The `identity_ids` of every consumed
   `SlotCandidate` (and, in `Extend`, of the previous
   `SlotGeometryCandidate`) appear in the output's `identity_ids`.
   No identity is dropped, rewritten, or downcast. (CLAUDE.md §4
   invariant 4.)
2. **Identity / trace separation.** The output's
   `identity_ids ∩ trace_ids == ∅`. Evidence may add trace but
   must not consume identity. (CLAUDE.md §4 invariants 1–3.)
3. **Residual preservation.** Every blocking or deferring residual
   on the inputs survives into the output's `residuals`. Nothing
   is silently discarded. (CLAUDE.md §4 invariant 7;
   `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §7.3.)
4. **Blocking-difference annihilation.** If any invalidating
   `difference:` claim is present in the binding evidence or on
   any consumed input, the `Extend` is blocked and the output is a
   blocked candidate. The geometry's length does not advance.
5. **`CandidateOnly` safety.** Every output carries
   `output_flags ⊇ {CandidateOnly}` and is free of any
   final-judgment flag (`HukmCandidate`, `RealityClaim`,
   `FinalMeaning`, `FinalCaseJudgment`, `DalalahCandidate`).
6. **No skipped layers.** No `Seed` or `Extend` may produce,
   directly or indirectly, the licensed output of any layer beyond
   `SlotGeometryQiyas` itself.

### 6.2 Rank meet semantics

The output rank is the **meet** of all participating ranks. The
slot-geometry layer's `rank_ceiling` declared by its rule
participates in the meet; the output may not exceed it.

For `Extend`:

```text
rank_out =
    rank(previous_geometry)
  ∧ rank(new_slot)
  ∧ rank(binding_evidence)
  ∧ rank(rule)
```

For `Seed`:

```text
rank_out =
    rank(slot)
  ∧ rank(rule)
```

The rank lattice is the canonical six-name finite chain fixed in
`TERMINOLOGY_MAP.md` §2. Only the following rank names may be used
in this contract and in any future implementation contract that
consumes it:

```text
NO_EVIDENCE
FORMAL_STRUCTURE
ANALOGICAL
DIRECT_HEARING
INDIVIDUAL_REPORT
MASS_TRANSMISSION
```

No legacy or alternative rank naming is admissible. A rule that
declares a `rank_ceiling` higher than the meet of its inputs is
constitutionally invalid; the kernel clamps the output to the meet
regardless. (CLAUDE.md §4 invariant 6; recursive-extension contract
§8.)

If any of the meet's contributing ranks is `NO_EVIDENCE`, the
output rank collapses to `NO_EVIDENCE`, and the resulting
`SlotGeometryCandidate` fails §2.1's `rank ≠ NO_EVIDENCE`
requirement at the next downstream check. The geometry can be
formed structurally but cannot itself become an admissible input
for any later layer until the rank rises above `NO_EVIDENCE`.

---

## 7. Claim Prefixes and Gates

### 7.1 Claim grammar

Claim grammar in this contract uses the public English claim
prefixes fixed in `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §9 /
§9.1:

```text
base:               (the established source of the extension)
branch:             (the determined target of the extension)
attribute:          (the effective attribute of the new unit)
effective_cause:    (the licensing cause of the extension)
difference:         (the invalidating difference, if any)
gate:               (the validity-gate claim)
```

These are **public documentation names** for cross-layer prose. They
do not replace the canonical implementation claim grammar already
consumed by the kernel. Where the current implementation uses
Arabic-rooted claims, the correspondence is:

```text
base:            ↔ اصل:
branch:          ↔ فرع:
attribute:       ↔ وصف:
effective_cause: ↔ علة:
difference:      ↔ فارق:
gate:            ↔ وادي:
```

No new claim parser, claim prefix, or kernel evidence grammar is
introduced by this document. The Arabic-rooted claim prefixes
fixed in `TERMINOLOGY_MAP.md` §4 remain the canonical claim grammar
consumed by `QiyasKernel`, and every evidence-producing instrument
continues to emit them verbatim.

### 7.2 Licensing gates

Every `Seed` and every `Extend` must clear the conjunctive six-gate
(وادي) licensing predicate fixed in `TERMINOLOGY_MAP.md` §3. Only
the following gate names may be used:

```text
CAUSE
CONDITION
OBSTACLE
VALIDITY
CORRUPTION
NULLITY
```

The gates are conjunctive: the step is licensed iff **every**
declared gate holds. If any gate fails, the output is blocked with
a residual; the recursive geometry does not advance in length.

---

## 8. Minimal Complete Closure Principle

This section instantiates the general termination law of
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3 / §5 at the
slot-geometry layer.

```text
Recursive extension answers how SlotGeometry grows.

Minimal complete closure answers when a SlotGeometryCandidate may
stop growing as a complete candidate within the slot-geometry
layer.
```

A `SlotGeometryCandidate` is **minimally complete** iff **all eight**
of the following hold simultaneously:

```text
licensed beginning
licensed ending
all internal bindings are licensed
no open demand remains
no blocking difference is present
residuals are preserved
rank remains above NO_EVIDENCE
output remains CandidateOnly
```

Each of the eight conditions is an instance of its peer in
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §3:

| § of the closure contract | Slot-geometry reading |
| --- | --- |
| §3.1 licensed beginning | The seed `SlotCandidate` was admissible as a start under a slot-geometry beginning rule. The `Seed` case (§3.1 of this document) is the trivial witness when `length == 1`. |
| §3.2 licensed ending | The last `Extend` (or the seed, when `length == 1`) was admissible as a terminus under a slot-geometry ending rule. |
| §3.3 all internal bindings are licensed | Every `SlotBindingEvidence` used in the construction history of this `SlotGeometryCandidate` was accepted under §5 of this document and the six-gate predicate of §7.2. |
| §3.4 no open demand remains | The slot-geometry layer's own Demand Catalogue is fully discharged. (The Catalogue is layer-published; the implementation contract that follows this document will fix its initial contents.) |
| §3.5 no blocking difference is present | No `difference:` claim invalidates any slot or any binding in the construction history. |
| §3.6 residuals are preserved | Every residual on every consumed input survives into the geometry's `residuals`. |
| §3.7 rank > NO_EVIDENCE | The meet of §6.2 produced a rank strictly above `NO_EVIDENCE`. |
| §3.8 output remains CandidateOnly | `output_flags ⊇ {CandidateOnly}` and no final-judgment flag is present. |

Closure produces **readiness**, never knowledge:

```text
Minimal complete closure does not produce:
  - DalalahCandidate
  - FinalMeaning
  - HukmCandidate
  - RealityClaim
  - FinalCaseJudgment

Minimal complete closure produces only:
  - readiness for a later licensed layer.
```

A closed-by-candidacy `SlotGeometryCandidate` is admissible only as
a consumable for the strictly next licensed layer's own admission
contract. It is **not** admissible as a `WordCandidate`, a
`SentenceCandidate`, a `DiscourseGeometryCandidate`, a
`TextGeometryCandidate`, or any higher-layer typed unit; each of
those layers will own its own admission contract.

This contract does **not** implement closure for `SlotGeometryQiyas`.
The closure-checking adapter, the beginning rule, the ending rule,
and the Demand Catalogue are all out of scope of this PR and must
themselves be ratified by separate contract PRs before any
implementation is opened.

---

## 9. Forbidden Outputs

`SlotGeometryQiyas`, when implemented in a later PR, must declare
the following types in its `forbidden_outputs`:

```text
DalalahCandidate
FinalMeaning
HukmCandidate
RealityClaim
FinalCaseJudgment
WordCandidate
SentenceCandidate
DiscourseGeometryCandidate
TextGeometryCandidate
```

`SlotGeometryQiyas` may produce **only** the following output
candidate type:

```text
Admissible output:
  - SlotGeometryCandidate only.

With metadata:
  - length            : the integer length of the geometry (1, 2, …).
  - construction_mode : one of {"seed", "extension"}, identifying
                        which mode produced this geometry.
```

`Seed` and `Extend` (§3) are **construction modes**, not separate
candidate types. A length-1 geometry produced by a `Seed` step is a

```text
SlotGeometryCandidate(length = 1, construction_mode = "seed")
```

and a length-(n+1) geometry produced by an `Extend` step is a

```text
SlotGeometryCandidate(length = n+1, construction_mode = "extension")
```

The choice to unify the output type is constitutional, not an
implementation discretion: this contract **does not** reserve
`SlotGeometrySeedCandidate` or `SlotGeometryExtensionCandidate` as
independent output types. Introducing either as an independent
candidate type requires a strictly later contract PR that
explicitly reopens this decision and ratifies the split.

`MinimalCompletionReadinessCandidate` remains a **future-reserved
concept name only**. It is **not** an admissible output of
`SlotGeometryQiyas` under this contract; a later implementation
contract that proposes such a type must itself ratify the symbol
before any implementation may emit it.

Any later implementation PR that adds a new `SlotGeometryQiyas`
output type beyond `SlotGeometryCandidate` is in violation of this
contract and must be rejected at review.

---

## 10. Relationship to Higher Layers

`SlotGeometryCandidate` is **not** a higher-layer typed unit. The
following non-identities are constitutional:

```text
SlotGeometryCandidate ≠ WordCandidate
SlotGeometryCandidate ≠ LafzCandidate
SlotGeometryCandidate ≠ SentenceCandidate
SlotGeometryCandidate ≠ ParagraphCandidate
SlotGeometryCandidate ≠ DiscourseGeometryCandidate
SlotGeometryCandidate ≠ TextGeometryCandidate
```

Converting a `SlotGeometryCandidate` into any of those higher
typed units **requires its own separate constitutional contract
PR** that ratifies the conversion's binding evidence and licensing
gates. No such contract exists at the time of this document's
ratification; therefore no such conversion is authorised here.

### 10.1 Naming discipline — "slot" terminology is reserved

The word "slot" in this codebase is reserved for the **lowest
letter/haraka cell layer**. The following names are constitutionally
admissible for higher layers:

```text
WordCandidate / LafzCandidate          (word-layer typed unit)
SentenceCandidate                       (sentence-layer typed unit)
ParagraphCandidate                      (paragraph-layer typed unit)
SentenceGeometryCandidate               (word-layer geometry; per
                                         RECURSIVE_LICENSED_EXTENSION
                                         _CONTRACT.md §3)
DiscourseGeometryCandidate              (sentence-layer geometry)
TextGeometryCandidate                   (paragraph-layer geometry)
```

The following names are **forbidden**, because they would re-use the
"slot" terminology at a layer where it does not belong:

```text
WordSlot          ← forbidden
SentenceSlot      ← forbidden
ParagraphSlot     ← forbidden
```

Do not introduce a "word slot" or a "sentence slot" anywhere in this
codebase. The slot layer is Phase-1, complete, and singular.

---

## 11. Forbidden Jumps

The following jumps are constitutional violations and must be
rejected by the gate policy of any future implementation contract:

```text
raw text                            →  SlotGeometryCandidate
SequenceContextTokenizer markers    →  SlotGeometryCandidate
UnicodeCandidate                    →  SlotGeometryCandidate
TypedCodePoint*                     →  SlotGeometryCandidate
LetterIdentityCarrier               →  SlotGeometryCandidate
HarakaFunctionCarrier               →  SlotGeometryCandidate
PositionCarrier                     →  SlotGeometryCandidate
CarrierBindingCandidate             →  SlotGeometryCandidate
ConditionedTypedSequence outputs    →  SlotGeometryCandidate
BoundaryCodePoint                   →  SlotGeometryCandidate
ResidualCodePoint                   →  SlotGeometryCandidate

SlotGeometryCandidate               →  DalalahCandidate
SlotGeometryCandidate               →  FinalMeaning
SlotGeometryCandidate               →  HukmCandidate
SlotGeometryCandidate               →  RealityClaim
SlotGeometryCandidate               →  FinalCaseJudgment
SlotGeometryCandidate               →  WordCandidate
SlotGeometryCandidate               →  LafzCandidate
SlotGeometryCandidate               →  SentenceCandidate
SlotGeometryCandidate               →  DiscourseGeometryCandidate
SlotGeometryCandidate               →  TextGeometryCandidate
```

In full:

```text
A SlotGeometryCandidate is still CandidateOnly.
A SlotGeometryCandidate is not a higher-layer typed unit.
A SlotGeometryCandidate is not semantic finality.
A SlotGeometryCandidate is not a hukm.
A SlotGeometryCandidate is not a reality claim.
```

This list extends — does not replace — §11 of
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` and §11 of
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md`. All three lists are binding
simultaneously.

---

## 12. Relationship to the Arabic Articulation Registry

The Arabic articulation registry (`PR #60`, awaiting merge) is an
external data registry per `PR_SCHEDULING_POLICY.md` §1.4. It is
**not** an admissible input for `SlotGeometryQiyas`. The
non-identities are:

```text
ArabicArticulationEntry        ≠  SlotCandidate
ArabicArticulationRegistry     ≠  SlotBindingEvidence
can_function_as_minimal_independent_unit  ≠  IsMinimallyComplete
                                              (closure §3 of the
                                               minimal-closure
                                               contract)
```

The registry's own `minimal_independent_unit_policy` field already
declares that its `core_independent_letters` are metadata signals
of *possible* later minimal-completion readiness only, with
`required_later_proofs` naming `licensed_slot`,
`minimal_complete_closure`, and `later_dalalah_evidence` as
strictly-later obligations. This contract is the controlling
contract for the first of those three: **slot-geometry licensed
admission via §2 of this document**. The other two remain
strictly later concerns.

`SlotGeometryQiyas` does **not** consult
`ArabicArticulationRegistry`. The registry is metadata only and
licenses no algebraic transition by itself
(`PR_SCHEDULING_POLICY.md` §1.4; the registry's own
`constitutional_constraints`).

---

## 13. Relationship to Higher-Layer Concepts

This contract does **not** define:

```text
DalalahCandidate
FinalMeaning
HukmCandidate
RealityClaim
FinalCaseJudgment
WordCandidate
LafzCandidate
SentenceCandidate
ParagraphCandidate
WordBindingEvidence
DiscourseBindingEvidence
TextBindingEvidence
```

When those higher layers are eventually contracted and implemented,
they will inherit the recursive extension growth law (§1 of
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`), the closure predicate
(§1 / §3 of `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md`), and the
input-type closure of *their* immediate predecessor — never
short-circuited to a lower layer's licensed output, and never
licensed to skip a layer.

A `SlotGeometryCandidate` is admissible *only* as a consumable for
the strictly next licensed layer's own admission contract — and that
admission contract does not yet exist. Until it is ratified, a
closed-by-candidacy `SlotGeometryCandidate` has no further licensed
destination, and that is constitutionally correct.

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the alignment-trace contract it fixes is
  binding on every future `SlotGeometryQiyas` implementation PR;
- **pre-implementation** — no `SlotGeometryQiyas`, no
  `SlotBindingEvidence`, no `SlotGeometrySeed`, no
  `SlotGeometryExtend`, no closure-checking adapter, no
  beginning/ending rule, and no Demand Catalogue is implemented at
  the time of merge;
- **slot-layer-specialised** — the law it specialises (recursive
  extension + minimal complete closure) applies at every licensed
  layer; this document fixes the specialised reading at the
  slot-geometry layer only.

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes a `SlotGeometryQiyas` adapter,
- any future PR that proposes a `SlotBindingEvidence` runtime type,
- any future PR that proposes a slot-geometry beginning rule, an
  ending rule, or a Demand Catalogue entry,
- any future review that asks whether a proposed slot-geometry
  consumption is licensed.

It supersedes nothing prior; it specialises the general
recursive-extension growth law and the general minimal-complete-
closure termination law for the slot-geometry layer specifically.

It does **not** authorise the implementation of `SlotGeometryQiyas`
or of any of the layers, evidences, rules, or catalogues it
describes. Each must continue to be ratified by its own contract PR
under `PR_SCHEDULING_POLICY.md` §1.1 before any implementation PR
may be opened under §1.3.

---

## 16. Non-Goals

This document does **not**:

- modify any file under `src/qiyas_core/`,
- modify any file under `tests/qiyas_core/`,
- modify `run_qiyas.py`,
- modify any file under `experimental/`,
- modify any other constitutional document,
- modify the `ArabicArticulationRegistry` (`PR #60`),
- introduce any new CI check, hook, bot, or automation,
- define any new candidate type beyond the single
  `SlotGeometryCandidate` admissible output enumerated in §9
  (`MinimalCompletionReadinessCandidate` remains a
  future-reserved concept name only, not an admissible output of
  this contract),
- define any new evidence shape, rule, or rank,
- introduce any new claim prefix beyond the public English names
  fixed in `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §9, with the
  Arabic correspondence reproduced in §7.1 of this document,
- introduce any new gate beyond the six canonical gates,
- produce `WordCandidate`, `LafzCandidate`, `SentenceCandidate`,
  `ParagraphCandidate`, `DiscourseGeometryCandidate`, or
  `TextGeometryCandidate`,
- produce `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`,
  `RealityClaim`, or `FinalCaseJudgment`,
- authorise any implementation, runtime, adapter, kernel surface,
  or test.

---

## 17. Glossary

| Term                                  | Meaning |
| ------------------------------------- | --- |
| `SlotGeometryQiyas`                   | The Phase-2 layer that consumes `SlotCandidate*` and produces `SlotGeometryCandidate`. Not implemented at the time of this document. |
| `SlotGeometryCandidate`               | The single licensed output of the slot-geometry layer (§9). Carries a length `n`, a `construction_mode` ∈ {"seed", "extension"}, identity_ids and trace_ids per §6, and `output_flags ⊇ {CandidateOnly}`. Still `CandidateOnly` regardless of length or construction mode. |
| `construction_mode`                   | Metadata field on `SlotGeometryCandidate` (§9). `"seed"` for the length-1 base case (§3.1); `"extension"` for length-(n+1) results of `Extend` (§3.2). Construction mode is metadata, **not** a distinct candidate type. |
| `SlotBindingEvidence`                 | The layer-specific binding evidence that licenses a `SlotGeometryExtend` step. Defined as a contract concept here; not implemented. Not portable above the slot layer (§5.2). |
| `Seed(S₁)`                            | The licensed length-1 base case of the recursive law (§3.1). |
| `Extend(Gₙ, Sₙ₊₁, SlotBindingEvidenceₙ)` | The licensed transition from a length-n geometry to a length-(n+1) geometry (§3.2). Not free concatenation. |
| isolated / initial / medial / terminal | The four geometric positions a `SlotCandidate` may occupy inside a `SlotGeometryCandidate` (§4). Geometric only; not semantic. |
| `alignment_ref`                       | The structural trace entry written by `SlotLayerAdapter` only when an explicit alignment proof was consumed. A required `trace_ids` entry for every `SlotCandidate` admitted by `SlotGeometryQiyas` (§2.2). |
| `INTRA_UTTERANCE`                     | The context in which `SlotBindingEvidence` operates (§5.3; `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §6). |
| Demand Catalogue (slot layer)         | The finite, layer-specific list of admissibility obligations that `IsMinimallyComplete` checks at the slot-geometry layer (§8; `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §3.4). Catalogue contents are layer-published; this contract reserves the name and binds future contracts to declare it. |
| `MinimalCompletionReadinessCandidate` | Future-reserved concept name only (§9). **Not** an admissible output of `SlotGeometryQiyas` under this contract; a later implementation contract must itself ratify the symbol before any implementation may emit it. |
| `IsMinimallyComplete`                 | The closure predicate inherited from `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1. Applied at the slot-geometry layer per §8 of this document. |
| closed-by-candidacy                   | The state of a `SlotGeometryCandidate` for which `IsMinimallyComplete` returns `True`. Still `CandidateOnly`. |
| readiness                             | The single positive effect of closure (§8): admissibility as a consumable for the strictly next licensed layer. Never promotion. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
