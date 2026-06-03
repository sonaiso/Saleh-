# MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the runtime
> shape of `MinimalCompleteClosureEvidence`. No code, no tests, no
> implementation are changed by this PR.
>
> **Authority basis:**
> `CLAUDE.md` §0 / §3 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `RESET_CONSTITUTION.md` §1 / §3 / §4,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §7 / §10 / §11 / §12,
> `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3 / §5 / §9 / §11 / §12,
> `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §1 / §6 / §8 / §9 / §11,
> `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` §2 / §3 / §4.3,
> `PR_SCHEDULING_POLICY.md` §1.1 / §5 / §8,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4.
>
> **Governing one-liners:**
>
> ```
> Closure is evidence, not a candidate.
> Closure evidence licenses no transition by itself.
> Closure evidence is layer-specific and not portable.
> ```
>
> ```
> الإغلاق دليل، لا مرشّح.
> ودليل الإغلاق لا يرخّص انتقالًا وحده.
> ودليل الإغلاق يخصّ طبقته، ولا يُنقل إلى غيرها.
> ```

---

## 0. Phase Status — Settled

Phase 1 — the single-slot pipeline — is **complete on `main`**:

```text
raw text
  → SequenceContextTokenizer
  → UnicodeQiyas
  → TypedCodePointClassificationQiyas
  → LetterIdentityQiyas / HarakaFunctionQiyas / PositionQiyas
  → ConditionedTypedSequenceQiyas
  → SlotQiyas
  → SlotCandidate
```

Phase-2 Batch 1 — `SlotGeometryQiyas` — is **complete on `main`**:

```text
SlotCandidate
  → SlotGeometryCandidate(length = 1, construction_mode = "seed")

SlotGeometryCandidate(length = n)
  + SlotCandidate
  + SlotBindingEvidence
  → SlotGeometryCandidate(length = n + 1, construction_mode = "extension")
```

The MIU readiness contract (`MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`)
is **complete on `main`**. It declares a closed consumption surface

```text
SlotGeometryCandidate(length = 1)
  + ArabicArticulationRegistry metadata
  + MinimalCompleteClosureEvidence
  → MinimalUnitReadinessCandidate
```

but defers the runtime shape of `MinimalCompleteClosureEvidence` to
*this* document (cf. MIU §4.3 — "contract concept only; later contract
PR will fix its runtime shape").

This document fixes that runtime shape. It does **not** implement
any runtime; it only constitutionally binds what any future
implementation must satisfy.

Four non-negotiable statements bind this PR's scope:

```text
Phase 1 is settled.
Phase-2 Batch 1 (SlotGeometryQiyas) is settled.
The MIU readiness contract is settled.
This PR fixes the runtime shape of MinimalCompleteClosureEvidence —
nothing more, nothing less.
```

This document does **not** modify any source file or test, does
**not** modify `run_qiyas.py`, the `ArabicArticulationRegistry`,
`slot_geometry_adapter.py`, `slot_geometry_rules.py`, or
`experimental/`, and does **not** amend any existing constitutional
document.

---

## 1. What is `MinimalCompleteClosureEvidence`?

`MinimalCompleteClosureEvidence` is the **runtime carrier** of the
witnesses required by the eight closure conditions of
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §3, instantiated for the
slot-geometry layer per `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`
§8.

In a single sentence:

```text
MinimalCompleteClosureEvidence is an immutable, layer-specific
evidence record that says: this SlotGeometryCandidate, at the
slot-geometry layer, has satisfied all eight closure conditions
and is admissible as a closure witness for a strictly later
licensed layer.
```

It is **observation**, not **construction**. It does not create a
new entity in the text. It does not produce a `Candidate`. It does
not license an algebraic transition by itself. It only certifies —
for a `SlotGeometryCandidate` that already exists and is already
licensed by Phase-2 Batch 1 — that closure holds.

Constitutionally:

```text
MinimalCompleteClosureEvidence is not meaning.
MinimalCompleteClosureEvidence is not a WordCandidate.
MinimalCompleteClosureEvidence is not a LafzCandidate.
MinimalCompleteClosureEvidence is not a DalalahCandidate.
MinimalCompleteClosureEvidence is not a HukmCandidate.
MinimalCompleteClosureEvidence is not a RealityClaim.
MinimalCompleteClosureEvidence is not a FinalMeaning.
MinimalCompleteClosureEvidence is not a FinalCaseJudgment.
MinimalCompleteClosureEvidence is not a MinimalUnitReadinessCandidate.
MinimalCompleteClosureEvidence does not produce readiness by itself.
```

It is consumed downstream — currently and exclusively — by the
forthcoming `MinimalIndependentUnitReadinessQiyas` layer (per MIU
contract §2 / §4.3), as one of three required witnesses, alongside
the `SlotGeometryCandidate(length = 1)` itself and the
`ArabicArticulationRegistry` metadata. **Closure evidence alone is
not sufficient for readiness**; readiness conjoins it with the other
two witnesses and applies the readiness predicate. This contract
fixes the closure side of that conjunction.

---

## 2. Constitutional Decision — Evidence Carrier, Not Candidate

The single most load-bearing decision this contract fixes is:

```text
MinimalCompleteClosureEvidence is an Evidence carrier
(an immutable, layer-specific, runtime-typed record).

MinimalCompleteClosureEvidence is NOT a Candidate.
```

### 2.1 Why an Evidence carrier

Closure is **proof about an existing candidate**, not the
production of a new one. The `SlotGeometryCandidate` already exists
and is already licensed (Phase-2 Batch 1 §3 / §6). The question
"does this geometry close minimally inside its layer?" yields a
yes/no answer with structured witnesses; it does **not** yield a new
textual entity, a new identity, or a new candidate type. Asking the
kernel to treat closure as a `Candidate` would inflate the candidate
namespace with a type that:

- carries no new identity beyond the geometry's,
- carries no new layer beyond the geometry's,
- carries no new linguistic content,
- carries only witnesses about the geometry's own internal state.

By construction, that is the shape of an `Evidence` carrier, not a
`Candidate`. The kernel's existing `Evidence` machinery
(`src/qiyas_core/evidence.py` per
`TERMINOLOGY_MAP.md` §4) handles claim-bearing immutable records
already. The closure carrier follows that pattern.

### 2.2 What "Evidence carrier" means in this codebase

For the purposes of this contract, **"Evidence carrier"** denotes
an immutable, frozen runtime record that:

1. is constructed by a deterministic producer (per §3),
2. carries explicit witnesses for each of the eight §6 closure
   conditions,
3. is consumed by a downstream layer's `QiyasRequest.evidence` (via
   a thin translation step that maps the carrier's fields into the
   canonical Arabic-rooted `EvidenceSet` claims the kernel reads),
4. is **not** itself a `qiyas_core.candidate.Candidate`,
5. is **not** itself a `qiyas_core.evidence.Evidence` either — the
   existing `Evidence` type is the kernel's claim-set primitive; a
   closure-evidence carrier is one structured layer above it, with
   typed fields that a producer translates into `Evidence` claims
   for the kernel.

The runtime shape is therefore closest to the pattern already
established by `SlotBindingEvidence`
(`src/qiyas_core/slot_geometry_adapter.py` —
`@dataclass(frozen=True)` with typed fields, consumed by the
adapter, never going through the kernel as a `Candidate`).

### 2.3 What this decision rules out

- **Not a `Candidate` subclass.** No `candidate_type ==
  "MinimalCompleteClosureCandidate"` is reserved by this contract;
  the name `MinimalCompleteClosureCandidate` is **forbidden** by §8.
- **Not produced by a `QiyasRule`.** Closure evidence is not the
  output of any `output_candidate_type` declaration; it has no
  `forbidden_outputs` of its own at the kernel level (those belong
  to the rule that *consumes* it).
- **Not licensed by gates.** Closure evidence is not subject to the
  six-gate (`CAUSE / CONDITION / OBSTACLE / VALIDITY / CORRUPTION /
  NULLITY`) licensing predicate at the kernel level. The gates apply
  to the *rule* that consumes it (e.g., the readiness rule); the
  closure carrier is the input.
- **Not a layer.** There is **no** `MinimalCompleteClosureQiyas`
  layer reserved by this contract. The carrier is produced by a
  deterministic checker (per §3), not by a Qiyas layer.

---

## 3. Who Produces `MinimalCompleteClosureEvidence`?

A deterministic producer reads the eight closure conditions off a
`SlotGeometryCandidate` and either returns a fully-populated
`MinimalCompleteClosureEvidence` (when all eight hold) or returns
`None` (when at least one fails).

### 3.1 Reserved producer name

```text
SlotGeometryClosureCheck     — reserved public name for the
                                deterministic checker that
                                evaluates the eight closure
                                conditions on a SlotGeometryCandidate
                                and returns an
                                MinimalCompleteClosureEvidence or
                                None. Not an implemented symbol at
                                the time of this document.
```

The name is reserved for the strictly later implementation contract
PR. No implementation is authorised here.

### 3.2 The producer's discipline

The producer must satisfy:

```text
Input    : SlotGeometryCandidate
Output   : MinimalCompleteClosureEvidence  (all eight conditions hold)
         | None                            (at least one fails)

Observation only. The producer does not modify the input geometry.
The producer does not produce a Candidate. The producer is not a
QiyasRule. The producer does not invoke QiyasKernel.

Construction is deterministic: given the same SlotGeometryCandidate,
the producer returns either the same evidence (modulo nondeterministic
identifiers like uuid) or None — never one and then the other.
```

### 3.3 Where the producer lives

The producer lives **outside** the `src/qiyas_core/rules/` tree
(it is not a rule) and **outside** the existing layer adapters
(`slot_adapter.py`, `slot_geometry_adapter.py`, etc.). The
reserved future module path is:

```text
src/qiyas_core/slot_geometry_closure_check.py
  — reserved public path; not implemented at the time of this
    document. A future implementation contract may pick a different
    module path if it provides a justification; the name
    SlotGeometryClosureCheck is binding regardless.
```

The producer **may** consult the existing `slot_geometry_adapter`
read-only helpers (`get_geometry_length`,
`get_construction_mode`) without modifying them. It **must not**
modify any existing adapter, rule, or kernel surface.

### 3.4 What the producer does NOT do

- **Does not modify the input geometry.** Observation only.
- **Does not produce a Candidate.** The `Candidate` namespace is
  unaffected.
- **Does not invoke `QiyasKernel.apply`.** No rule fires, no
  candidate set returns.
- **Does not consult `ArabicArticulationRegistry`.** Closure is
  layer-internal; registry metadata is a separate witness consumed
  by the readiness layer, not by closure.
- **Does not consult `SequenceContextTokenizer` markers or raw
  text.** Closure reads off the geometry's internal structure
  only.

---

## 4. Closed Consumption Surface

`SlotGeometryClosureCheck` consumes exactly one input type — and
**only** this one:

```text
admissible input:
  1. SlotGeometryCandidate   (any length, any construction_mode,
                              produced by SlotGeometryQiyas)
```

It must **not** directly consume any of the following:

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
SlotCandidate
ArabicArticulationRegistry metadata
WordCandidate
LafzCandidate
SentenceCandidate
ParagraphCandidate
DalalahCandidate
MinimalUnitReadinessCandidate
FinalMeaning
HukmCandidate
RealityClaim
```

The producer's input surface is therefore **strictly narrower** than
either Phase-2 Batch 1 (`SlotGeometryQiyas`, which consumes
`SlotCandidate*` and `SlotBindingEvidence`) or the MIU readiness
layer (which consumes `SlotGeometryCandidate(length = 1)` plus
registry plus closure evidence).

In particular, closure evidence **does not** consult the registry.
Registry metadata is a separate witness, layered at the readiness
layer, and constitutionally orthogonal to closure: closure asks
"does this geometry close internally?", registry asks "is this
symbol metadata-eligible as a minimal independent unit?". Conflating
them would dilute both.

---

## 5. Length Scope — Any Length, Not Only `length = 1`

`MinimalCompleteClosureEvidence` is constructible for **any**
`SlotGeometryCandidate`, regardless of `length` or
`construction_mode`:

```text
SlotGeometryCandidate(length = 1, construction_mode = "seed")
  → SlotGeometryClosureCheck → MinimalCompleteClosureEvidence | None

SlotGeometryCandidate(length = n, construction_mode = "extension")
  → SlotGeometryClosureCheck → MinimalCompleteClosureEvidence | None
```

### 5.1 Why not restrict to `length = 1`

The MIU readiness layer currently consumes only `length = 1`
geometries (MIU contract §2). But future layers (word-layer,
sentence-layer, paragraph-layer) will also need closure evidence on
their *own* geometries. Restricting closure to `length = 1` here
would force every later layer to invent its own closure carrier
shape, inflating the type namespace and breaking the single-source
discipline of `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1.

The cleaner reading: **closure conditions are length-agnostic** —
the eight conditions of `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §3
apply to any geometry candidate of any layer, with the slot-geometry
instance fixed in `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §8.
Restricting the producer's input to `length = 1` would over-fit to
the current downstream consumer (readiness), which is itself only
the *first* consumer of closure evidence, not the last.

### 5.2 How the readiness layer narrows the scope

The MIU readiness layer narrows the scope at its own admission
boundary (`MIU contract §2 / §4.1`):

```text
admission predicate of readiness:
    S.candidate_type        == "SlotGeometryCandidate"
    trace_ids carry length  == 1
    trace_ids carry mode    == "seed"
    closure_evidence_for(S) is not None
```

Closure evidence for a `length = 3` geometry (e.g., `ضَرَبَ`) is
**well-formed and producible**, but the readiness layer does not
admit it — readiness's input gate filters by length before
consulting closure. This is the constitutionally correct division of
labour: closure says "is the geometry internally closed?"; readiness
says "is this *length-1* closed geometry eligible as a minimal
unit?".

A future word-layer closure consumer (if it follows the same
pattern) would admit `length > 1` geometries and apply its own
admission predicate, but still consume the **same** closure
evidence shape produced by `SlotGeometryClosureCheck`.

### 5.3 The non-identity statements

```text
SlotGeometryClosureCheck(length = 1 geometry)   may produce evidence.
SlotGeometryClosureCheck(length = n geometry)   may produce evidence.

Closure evidence for length = 1   ≠   readiness candidate.
Closure evidence for length = n   ≠   word candidate.
Closure evidence for any length   ≠   meaning.
```

---

## 6. The Eight Closure Conditions, Carried Verbatim

`MinimalCompleteClosureEvidence` carries one witness per condition
of `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §3, instantiated for the
slot-geometry layer per `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`
§8. The eight fields are:

```text
1. licensed_beginning            : True | False
   — the geometry has a licensed beginning (Seed for length = 1
     is the trivial witness; for length > 1, the first Extend
     step's binding witnesses the beginning).

2. licensed_ending               : True | False
   — the geometry has a licensed ending (Seed is the trivial
     witness when length = 1; for length > 1, the last accepted
     Extend step witnesses the ending).

3. all_internal_bindings_licensed : True | False
   — every SlotBindingEvidence used in the geometry's construction
     history was accepted under the slot-geometry layer's gate
     policy (Phase-2 Batch 1 §5 + §3 of this contract).
     For length = 1, this is vacuously True (no Extend step).

4. no_open_demand                : True | False
   — the slot-geometry layer's own Demand Catalogue is fully
     discharged (MINIMAL_COMPLETE_CLOSURE_CONTRACT.md §3.4). The
     catalogue's initial contents are deferred to a strictly later
     contract; this evidence field is the layer's structural witness
     that no demand is open at evidence-construction time.

5. no_blocking_difference        : True | False
   — no `فارق:*:present` claim invalidates any slot or any binding
     in the construction history. Read off the geometry's residuals
     and the Phase-2 Batch 1 invalidating-difference list.

6. residuals_preserved           : True | False
   — every residual on the geometry's consumed inputs survives into
     the geometry's `residuals`. Structurally checked.

7. rank_above_no_evidence        : True | False
   — the geometry's `rank` field is strictly above `NO_EVIDENCE`
     (`TERMINOLOGY_MAP.md` §2 finite chain).

8. candidate_only_safety         : True | False
   — `output_flags ⊇ {CandidateOnly}` and
     `output_flags ∩ {HukmCandidate, RealityClaim, FinalMeaning,
                      FinalCaseJudgment, DalalahCandidate} = ∅`.
```

In addition to the eight booleans, the carrier records audit
metadata:

```text
geometry_candidate_id           : the consumed geometry's candidate_id
geometry_layer                  : "SlotGeometryQiyas"
geometry_length                 : the consumed geometry's length
geometry_construction_mode      : "seed" | "extension"
geometry_identity_ids           : tuple — preserved verbatim from the
                                  geometry (NEVER rewritten,
                                  reordered, or downcast)
geometry_trace_ids              : tuple — preserved verbatim from the
                                  geometry
geometry_rank                   : the meet rank of the geometry
evidence_id                     : per-evidence unique identifier
                                  (uuid-style; not an identity)
audit_trace_ids                 : tuple — additional auditable trace
                                  entries appended by the checker
                                  itself (must remain disjoint from
                                  identity_ids)
```

The eight booleans are conjunctive: the carrier is **only**
constructed when all eight are `True`. If any is `False`, the
producer returns `None` and records the failing witnesses as
residuals on the producer's audit log (the exact log shape is left
to the implementation contract).

`MinimalCompleteClosureEvidence` is a **frozen** dataclass —
immutable once constructed.

### 6.1 Recommended `audit_trace_ids` schema (non-binding)

The `audit_trace_ids` field of §6 is intentionally a tuple of
opaque strings; the kernel and downstream consumers treat its
contents as audit-only trace, never as identity (CLAUDE.md §4
invariants 1–3). To keep audit logs legible across implementations,
this contract **recommends** — but does **not** bind — the
following schema for the strings emitted into `audit_trace_ids`:

```text
trace:slot_geometry_closure:<condition_name>:passed
trace:slot_geometry_closure:<condition_name>:failed
```

with `<condition_name>` ranging over the eight §6 booleans:

```text
trace:slot_geometry_closure:licensed_beginning:passed
trace:slot_geometry_closure:licensed_ending:passed
trace:slot_geometry_closure:all_internal_bindings_licensed:passed
trace:slot_geometry_closure:no_open_demand:passed
trace:slot_geometry_closure:no_blocking_difference:passed
trace:slot_geometry_closure:residuals_preserved:passed
trace:slot_geometry_closure:rank_above_no_evidence:passed
trace:slot_geometry_closure:candidate_only_safety:passed
```

For a producer call that returns `MinimalCompleteClosureEvidence`,
all eight `:passed` entries appear in `audit_trace_ids`. For a
producer call that returns `None`, the implementation should emit
the corresponding `:failed` entries on the producer's audit log
(not on the carrier — there is no carrier in the `None` case). The
schema is **non-binding**: an implementation contract may pick a
different format if it provides a stable, layer-prefixed, status-
suffixed pattern. The intent is reviewer legibility, not lexical
prescription.

---

## 7. Does It Produce Readiness?

**No.** Closure evidence does not produce readiness, does not
produce a candidate of any kind, does not license an algebraic
transition, and does not produce any constitutional flag.

The relationship is:

```text
SlotGeometryClosureCheck(S)
  → MinimalCompleteClosureEvidence | None

         (the carrier is consumed by a later layer)

ReadinessLayer(S, M, E)
  where:
    S = SlotGeometryCandidate(length = 1)
    M = ArabicArticulationRegistry metadata for S's symbol(s)
    E = MinimalCompleteClosureEvidence for S
        (= SlotGeometryClosureCheck(S), if not None)
  → MinimalUnitReadinessCandidate
```

The two contracts compose strictly:

| Step                                       | Contract                                                       | Operator                            |
| ------------------------------------------ | -------------------------------------------------------------- | ----------------------------------- |
| produce closure evidence for a geometry    | this contract                                                  | `SlotGeometryClosureCheck(S)`       |
| admit a length-1 geometry as readiness     | `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`               | `Admit(S, M, E)`                    |

Closure evidence is a **necessary** but **not sufficient** witness
for readiness:

```text
Closure evidence True for S  ⇏  S is admissible as readiness candidate.
Closure evidence False for S ⇒  S is NOT admissible as readiness candidate.
```

Readiness additionally requires the registry metadata witness
(`MIU §4.2`) and the structural conditions on `S` (`MIU §4.1`).
Closure alone never produces readiness. The constitutional
discipline:

```text
Closure is evidence, not a candidate.
Closure evidence licenses no transition by itself.
```

```text
الإغلاق دليل، لا مرشّح.
ودليل الإغلاق لا يرخّص انتقالًا وحده.
```

---

## 8. Forbidden Outputs

`SlotGeometryClosureCheck`, when implemented in a later PR, must
**never** produce any of the following — neither as its return value
nor as a side effect:

```text
HukmCandidate
RealityClaim
FinalMeaning
FinalCaseJudgment

DalalahCandidate
WordCandidate
LafzCandidate
SentenceCandidate
ParagraphCandidate
DiscourseGeometryCandidate
TextGeometryCandidate

MinimalUnitReadinessCandidate
MinimalIndependentMeaningCandidate
                            (also forbidden by MIU §5 / §8)

MinimalCompleteClosureCandidate
                            (the carrier is Evidence, not a
                             Candidate — §2 of this contract)

SlotCandidate
SlotGeometryCandidate
                            (the producer observes; it does not
                             produce candidates of any kind, not
                             even the candidate types it observes)
```

The single admissible *output* of `SlotGeometryClosureCheck` is the
two-valued return:

```text
MinimalCompleteClosureEvidence   (when all eight conditions hold)
None                              (when any condition fails)
```

There is no third return type.

### 8.1 Forbidden side effects

The producer must not:

```text
mutate the input geometry,
push or pull from any external service,
write to disk (except for explicit audit logging that the
  implementation contract may authorise — outside the scope of this
  document),
invoke QiyasKernel.apply,
emit a Candidate to any layer,
consult the ArabicArticulationRegistry,
consult SequenceContextTokenizer markers or raw text,
modify slot_geometry_adapter.py, slot_geometry_rules.py, or any
  other adapter/rule.
```

### 8.2 What "forbidden output" means at this layer

For a `Candidate`-producing layer, `forbidden_outputs` is the
kernel-enforced tuple on the `QiyasRule`. For closure evidence —
which is **not** kernel-produced — the equivalent discipline is
that the **producer's return type is statically known and bounded**
to the two-valued shape above. A future implementation must enforce
this by type discipline (e.g., a typed `Optional[MinimalCompleteClosureEvidence]`
return annotation) plus tests that pin the constitutional non-output
of every name in the §8 list.

---

## 9. Layer Specificity and Portability

`MinimalCompleteClosureEvidence` as defined by this contract is the
**slot-geometry-layer** instance of a more general pattern.

### 9.1 Layer-specific

The carrier produced by `SlotGeometryClosureCheck` is **specifically**
the closure witness for a `SlotGeometryCandidate` at the
`SlotGeometryQiyas` layer. Its `geometry_layer` field is fixed to
`"SlotGeometryQiyas"`. Its eight booleans witness the eight
conditions **as instantiated for the slot-geometry layer** (per
`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §8).

### 9.2 Not portable upward

A `MinimalCompleteClosureEvidence` produced for a
`SlotGeometryCandidate` **must not** be reused as closure evidence
for any higher-layer candidate. Higher layers (word, sentence,
paragraph) will need their own closure-evidence types, produced by
their own layer-specific checkers, with their own field semantics:

```text
SlotGeometryClosureCheck         → MinimalCompleteClosureEvidence
                                   (slot-geometry layer)

WordLayerClosureCheck            → WordLayerClosureEvidence
                                   (word layer — reserved future
                                    name only; not defined here)

SentenceLayerClosureCheck        → SentenceLayerClosureEvidence
                                   (sentence layer — reserved future
                                    name only; not defined here)
```

The non-portability discipline mirrors `SlotBindingEvidence`'s
non-portability (Phase-2 Batch 1 §5.2): each layer's closure
evidence is its own type, with its own field semantics, and is not
accepted by any other layer.

### 9.3 Why fix only the slot-geometry instance now

Because that is the only instance currently demanded by an existing
constitutional contract (the MIU readiness contract). The
higher-layer closure-evidence shapes will be ratified by their own
contracts when those layers are themselves contracted.

This contract does **not**:

- define `WordLayerClosureEvidence`,
- define `SentenceLayerClosureEvidence`,
- define `ParagraphLayerClosureEvidence`,
- define any generic / parametric "ClosureEvidence" base type,
- authorise the implementation of any higher-layer closure check.

---

## 10. Relationship to `MinimalUnitReadinessCandidate`

The closure evidence carrier is the **third** of the three witnesses
required by the MIU readiness contract (§2):

```text
Admit(S, M, E) := True
  iff
    S.candidate_type        == "SlotGeometryCandidate"
    S satisfies MIU §4.1 structural conditions,
    M.can_function_as_minimal_independent_unit == True,
    E = SlotGeometryClosureCheck(S)  is not None,
    every MIU §6 invariant holds.
```

### 10.1 Hard non-identities

```text
MinimalCompleteClosureEvidence  ≠  MinimalUnitReadinessCandidate
MinimalCompleteClosureEvidence  ≠  Candidate (of any type)
MinimalCompleteClosureEvidence  ≠  Evidence (of the kernel's
                                              EvidenceSet shape)
MinimalCompleteClosureEvidence  ≠  meaning
MinimalCompleteClosureEvidence  ≠  word
MinimalCompleteClosureEvidence  ≠  lafz
MinimalCompleteClosureEvidence  ≠  dalalah
MinimalCompleteClosureEvidence  ≠  hukm
MinimalCompleteClosureEvidence  ≠  reality
```

### 10.2 What closure evidence licenses, in the readiness pipeline

```text
Closure evidence True   →  one of three readiness preconditions met.
Closure evidence False  →  readiness admission MUST be refused
                            (the registry-metadata witness and the
                             structural-conditions witness are
                             unaffected; closure is one of three).
Closure evidence absent →  the readiness layer MUST treat absence
                            as a deferred decision (the closure
                            check was not run); it must not silently
                            admit, and it must not silently reject.
```

This is the constitutional reading. A future implementation may
choose to *eagerly* compute closure evidence whenever readiness is
attempted, or to *lazily* require the caller to supply it; that
implementation choice is **out of scope** for this contract.

### 10.3 Why closure evidence cannot be inlined into readiness

A reviewer may ask: why not have the readiness layer's adapter
re-compute the eight closure conditions on the geometry directly,
without a separate closure-evidence carrier?

Answer: because closure is **layer-internal** to slot-geometry, and
readiness is **strictly later**. Inlining the closure check into
readiness would:

1. cause every higher layer that needs closure (word-layer,
   sentence-layer, etc.) to re-inline the same eight checks,
2. break the single-source discipline of
   `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3,
3. couple the readiness adapter to the slot-geometry internal
   structure, which the consumption-surface closure of
   `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` §2 explicitly
   forbids.

The Evidence-carrier shape preserves separation: the slot-geometry
layer owns the closure check; the readiness layer owns the
admission predicate; the closure evidence is the typed witness that
crosses the boundary.

---

## 11. Worked Examples

The following examples illustrate where closure evidence does and
does **not** intersect with the readiness layer. They are
documentation, not specification: the canonical contract is the
text of §1–§10.

### 11.1 `بِ` — closure evidence likely, readiness still subject to other witnesses

```text
Phase 1               : raw text "بِ" → SlotCandidate (ب + kasra)
Phase 2 Batch 1       : SlotCandidate → SlotGeometryCandidate
                                         (length = 1,
                                          construction_mode = "seed")
SlotGeometryClosureCheck:
                        evaluates the eight §6 conditions on the
                        length-1 seed geometry. For the canonical
                        run_qiyas.py-produced seed of "بِ", all
                        eight conditions hold (licensed beginning
                        and ending coincide trivially in Seed;
                        all internal bindings are vacuous; no open
                        demand; no blocking difference; residuals
                        preserved; rank = FORMAL_STRUCTURE; output
                        flags = {CandidateOnly}).
                        → produces a MinimalCompleteClosureEvidence.
Downstream (MIU)      : the readiness layer conjoins this closure
                        evidence with the registry metadata witness
                        for ب (lips_ba.can_function_as_minimal_
                        independent_unit == True) and with the
                        structural conditions on S. If all three
                        admit, readiness returns a
                        MinimalUnitReadinessCandidate.
What this contract    : closure evidence is produced. Closure does
says                    not produce readiness by itself. Closure
                        does not produce meaning. The readiness
                        decision is the readiness layer's, not
                        closure's.
```

### 11.2 `ضَ` — closure evidence likely, readiness rejected by registry metadata

```text
Phase 1               : raw text "ضَ" → SlotCandidate (ض + fatha)
Phase 2 Batch 1       : SlotCandidate → SlotGeometryCandidate
                                         (length = 1,
                                          construction_mode = "seed")
SlotGeometryClosureCheck:
                        evaluates the eight §6 conditions on the
                        length-1 seed geometry. Geometrically, the
                        Phase-2 Batch 1 seed of "ضَ" satisfies the
                        eight structural conditions just as "بِ"
                        does.
                        → produces a MinimalCompleteClosureEvidence.
Downstream (MIU)      : the readiness layer fetches the registry
                        metadata witness for ض. tongue_dad's
                        can_function_as_minimal_independent_unit
                        is False. Readiness REFUSES admission.
                        No MinimalUnitReadinessCandidate is
                        produced.
What this contract    : closure evidence existed; that did not
says                    license readiness. Closure is necessary
                        but not sufficient (§7 / §10.2). No meaning
                        is produced anywhere.
```

### 11.3 `ضَرَبَ` — closure evidence applies (length-agnostic), readiness layer does not consume it

```text
Phase 1 / Phase 2     : raw text "ضَرَبَ" → three SlotCandidates →
                        SlotGeometryCandidate(length = 3,
                                               construction_mode =
                                               "extension")
SlotGeometryClosureCheck:
                        evaluates the eight §6 conditions on the
                        length-3 geometry. Closure is length-
                        agnostic (§5), so this is a legitimate
                        producer call. If all eight conditions hold
                        for the multi-extend construction history,
                        → produces a MinimalCompleteClosureEvidence
                        for the length-3 geometry.
Downstream (MIU)      : the readiness layer does NOT consume this
                        evidence. Per MIU §2 / §4.1, readiness
                        admits only SlotGeometryCandidate(length =
                        1, construction_mode = "seed"). The length-3
                        geometry is outside readiness's input gate
                        regardless of whether closure evidence
                        exists for it.
What this contract    : closure evidence may exist for any length;
says                    readiness consumes only the length-1
                        subset. The two contracts decouple cleanly:
                        closure does not care about readiness's
                        length restriction, and readiness applies
                        its own gate before consulting closure
                        evidence at all.
```

The three examples together demonstrate why §2's Evidence-carrier
decision and §5's length-agnostic decision compose without
conflict: closure observes structural facts about any geometry;
readiness applies an admission predicate that conjoins closure
with two other witnesses and narrows by length. The two layers
do not see each other; they communicate only through the typed
closure evidence carrier.

---

## 12. Forbidden Jumps

The following jumps are constitutional violations and must be
rejected by the gate policy of any future implementation contract:

```text
SlotGeometryCandidate              →  MinimalCompleteClosureCandidate
                                       (forbidden — §2: closure is
                                        Evidence, not a Candidate)

MinimalCompleteClosureEvidence     →  MinimalUnitReadinessCandidate
                                       (closure evidence does not
                                        produce readiness; readiness
                                        conjoins it with the other
                                        two witnesses)

MinimalCompleteClosureEvidence     →  WordCandidate
MinimalCompleteClosureEvidence     →  LafzCandidate
MinimalCompleteClosureEvidence     →  SentenceCandidate
MinimalCompleteClosureEvidence     →  ParagraphCandidate
MinimalCompleteClosureEvidence     →  DalalahCandidate
MinimalCompleteClosureEvidence     →  FinalMeaning
MinimalCompleteClosureEvidence     →  HukmCandidate
MinimalCompleteClosureEvidence     →  RealityClaim
MinimalCompleteClosureEvidence     →  FinalCaseJudgment
MinimalCompleteClosureEvidence     →  SlotCandidate
MinimalCompleteClosureEvidence     →  SlotGeometryCandidate
                                       (closure evidence licenses
                                        no growth, no extension, no
                                        new candidate of any kind)

raw text                           →  MinimalCompleteClosureEvidence
SequenceContextTokenizer markers   →  MinimalCompleteClosureEvidence
UnicodeCandidate                   →  MinimalCompleteClosureEvidence
TypedCodePoint                     →  MinimalCompleteClosureEvidence
LetterIdentityCarrier              →  MinimalCompleteClosureEvidence
HarakaFunctionCarrier              →  MinimalCompleteClosureEvidence
PositionCarrier                    →  MinimalCompleteClosureEvidence
CarrierBindingCandidate            →  MinimalCompleteClosureEvidence
ConditionedTypedSequence outputs   →  MinimalCompleteClosureEvidence
SlotCandidate                      →  MinimalCompleteClosureEvidence
ArabicArticulationRegistry entry   →  MinimalCompleteClosureEvidence
                                       (closure evidence is produced
                                        ONLY from a
                                        SlotGeometryCandidate; never
                                        directly from any upstream
                                        layer's output)

ArabicArticulationRegistry         →  ClosureCheck
                                       (the registry is metadata
                                        only and licenses no
                                        algebraic transition;
                                        closure does not consult it)
```

In full:

```text
A MinimalCompleteClosureEvidence is an Evidence carrier.
It is not a Candidate.
It is not semantic.
It is not a hukm.
It is not a reality claim.
It is not a dalalah.
It is not readiness.
Closure is evidence, not a candidate.
```

This list extends — does not replace — the forbidden-jumps lists in
§11 of `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`, §11 of
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md`, §11 of
`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`, and §12 of
`MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`. All five lists are
binding simultaneously.

---

## 13. The 10 Answered Questions — Summary Table

For the convenience of any reviewer or future contract reader, this
section restates the contract's answers to the ten questions the
maintainer asked.

| # | Question                                                                                | Answer (this contract)                                                                                                                                                                                |
| - | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | What is `MinimalCompleteClosureEvidence`?                                               | An immutable runtime carrier of the eight slot-geometry closure-condition witnesses, plus audit metadata about the consumed geometry. Observation, not construction.                                  |
| 2 | Is it a `Candidate` or an Evidence carrier only?                                        | **Evidence carrier.** Not a `Candidate`. `MinimalCompleteClosureCandidate` is explicitly forbidden by name (§8).                                                                                       |
| 3 | Who produces it?                                                                        | A deterministic checker reserved as `SlotGeometryClosureCheck`. Not a Qiyas layer, not a rule, does not invoke `QiyasKernel.apply` (§3).                                                                |
| 4 | Does it consume `SlotGeometryCandidate`?                                                | **Yes — and only that.** Closed consumption surface to `SlotGeometryCandidate` only (§4).                                                                                                              |
| 5 | Does it work on `SlotGeometryCandidate(length = 1)` only or on every length?            | **Every length.** The eight closure conditions are length-agnostic. The MIU readiness layer narrows to `length = 1` at its own admission boundary (§5).                                                |
| 6 | What are its eight conditions?                                                          | Carried verbatim from `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §3 and `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §8 — one boolean field per condition, plus audit metadata (§6).                         |
| 7 | Does it produce readiness?                                                              | **No.** Closure evidence is a necessary-but-not-sufficient witness for readiness. Readiness conjoins it with the other two witnesses (registry metadata + structural conditions) per MIU §3 (§7).      |
| 8 | What are its forbidden outputs?                                                         | Twelve type names listed in §8 (CONSTITUTIONAL_BASE + the higher-layer typed-unit list + `MinimalUnitReadinessCandidate` + `MinimalCompleteClosureCandidate`). The single admissible return is the two-valued `MinimalCompleteClosureEvidence | None`. |
| 9 | Is it specific to `SlotGeometryQiyas` or portable?                                      | **Layer-specific.** Not portable upward; higher-layer closure-evidence shapes will be defined by their own future contracts (§9).                                                                       |
| 10| What is its relationship to `MinimalUnitReadinessCandidate`?                            | Closure evidence is the **third** of three required readiness witnesses. Closure True ⇏ readiness; closure False ⇒ readiness refused. Closure cannot be inlined into readiness (§10).                  |

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the runtime shape it fixes is binding on
  every future closure-evidence implementation PR;
- **pre-implementation** — `MinimalCompleteClosureEvidence` as a
  runtime type, `SlotGeometryClosureCheck` as a producer, and the
  module `src/qiyas_core/slot_geometry_closure_check.py` are all
  reserved-by-name only; none is implemented at the time of merge;
- **slot-geometry-layer-strict** — the shape applies *only* to
  closure evidence at the slot-geometry layer; higher-layer
  closure-evidence shapes will be defined by their own contracts.

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes a `MinimalCompleteClosureEvidence`
  runtime type;
- any future PR that proposes a `SlotGeometryClosureCheck` producer;
- any future PR that proposes to inline closure into the readiness
  layer (which this contract forbids);
- any future PR that proposes a higher-layer closure-evidence type
  (which this contract sets the precedent for but does not define);
- any future review that asks whether a proposed closure-evidence
  consumption is licensed.

It supersedes nothing prior; it fixes the runtime shape that the
MIU readiness contract deferred to a strictly later contract, and
it composes with — does not amend —
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md`.

It does **not** authorise the implementation of
`MinimalCompleteClosureEvidence`, `SlotGeometryClosureCheck`, the
module at the reserved path, or any consumer. Each must continue to
be ratified by its own contract PR under `PR_SCHEDULING_POLICY.md`
§1.1 before any implementation PR may be opened under §1.3.

---

## 16. Non-Goals

This document does **not**:

- modify any file under `src/qiyas_core/`,
- modify any file under `tests/qiyas_core/`,
- modify `run_qiyas.py`,
- modify any file under `experimental/`,
- modify any other constitutional document,
- modify the `ArabicArticulationRegistry` (CSV source, JSON
  artifact, reader module),
- modify `src/qiyas_core/slot_geometry_adapter.py` or
  `src/qiyas_core/rules/slot_geometry_rules.py`,
- implement `MinimalCompleteClosureEvidence` as a runtime type,
- implement `SlotGeometryClosureCheck` as a producer,
- create the module `src/qiyas_core/slot_geometry_closure_check.py`,
- introduce any new CI check, hook, bot, or automation,
- define `WordLayerClosureEvidence`, `SentenceLayerClosureEvidence`,
  `ParagraphLayerClosureEvidence`, or any generic `ClosureEvidence`
  base type,
- introduce any new claim prefix beyond the public English names
  fixed in `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §9,
- introduce any new gate beyond the six canonical gates of
  `TERMINOLOGY_MAP.md` §3,
- introduce any new rank beyond the six canonical ranks of
  `TERMINOLOGY_MAP.md` §2,
- produce `WordCandidate`, `LafzCandidate`, `SentenceCandidate`,
  `ParagraphCandidate`, `DiscourseGeometryCandidate`,
  `TextGeometryCandidate`, `DalalahCandidate`, `FinalMeaning`,
  `HukmCandidate`, `RealityClaim`, `FinalCaseJudgment`,
  `MinimalUnitReadinessCandidate`, or
  `MinimalCompleteClosureCandidate`,
- inline closure into the readiness layer,
- authorise the implementation of any consumer, runtime, adapter,
  kernel surface, or test.

---

## 17. Glossary

| Term                                          | Meaning |
| --------------------------------------------- | --- |
| `MinimalCompleteClosureEvidence`              | The slot-geometry-layer closure-evidence carrier (§1). Frozen, immutable. Carries one boolean witness per §6 condition plus audit metadata. **Not** a `Candidate`. **Not** the kernel's `Evidence` primitive. |
| `SlotGeometryClosureCheck`                    | Reserved public name for the deterministic producer of `MinimalCompleteClosureEvidence` (§3). Not a Qiyas layer. Not a rule. Does not invoke `QiyasKernel.apply`. Reserved-by-name only; not implemented at the time of this document. |
| `src/qiyas_core/slot_geometry_closure_check.py` | Reserved future module path for the producer (§3.3). Reserved-by-name only; not implemented. |
| Evidence carrier                              | An immutable, frozen runtime record that carries typed witnesses about an existing candidate, consumed by a downstream layer's request. Distinct from both `Candidate` and the kernel's `Evidence` primitive (§2.2). |
| closure observation                           | The producer's discipline (§3.2): no mutation, no kernel invocation, no candidate production. Closure is **observation**, not construction. |
| length-agnostic closure                       | The contract's position (§5): closure is constructible for any `SlotGeometryCandidate` length, not only `length = 1`. The MIU readiness layer narrows scope at its own admission boundary. |
| necessary-but-not-sufficient                  | The closure-readiness relationship (§7 / §10). Closure True ⇏ readiness; closure False ⇒ readiness refused. |
| layer-specific (closure)                      | The non-portability discipline (§9). Slot-geometry closure evidence is not reusable as word/sentence/paragraph closure evidence. Higher layers define their own. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
