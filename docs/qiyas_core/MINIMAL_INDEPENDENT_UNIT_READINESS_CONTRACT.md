# MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> *minimal independent unit readiness* layer. No code, no tests, no
> implementation are changed by this PR.
>
> **Authority basis:**
> `CLAUDE.md` §0 / §3 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `RESET_CONSTITUTION.md` §1 / §3 / §4,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §6 / §7 / §10 /
> §11 / §12,
> `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3 / §9 / §11 / §12,
> `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §1 / §2 / §6 / §9 /
> §10 / §11,
> `PR_SCHEDULING_POLICY.md` §1.1 / §5 / §8,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4,
> the existing data registry
> `src/qiyas_core/data/arabic_articulation_registry.json`.
>
> **Governing one-liners:**
>
> ```
> Geometric validity is not functional independence.
> Functional readiness is not meaning.
> ```
>
> ```
> الصحة الهندسية ليست الاستقلال الوظيفي.
> والجاهزية الوظيفية ليست المعنى.
> ```

---

## 0. Phase-1 and Phase-2 Status — Settled

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

The single admissible Phase-2 output type is `SlotGeometryCandidate`
with `length` and `construction_mode` recorded on `trace_ids` —
never on `identity_ids`, and never as a separate candidate type.

This contract opens a **strictly later** layer on top of that
foundation. Three non-negotiable statements bind this PR's scope:

```text
The single-slot pipeline is not open work in this PR.
This PR does not revisit, reopen, refactor, or repair the Phase-1
or Phase-2 Batch 1 layers.
This PR only defines the next controlling contract for the
Minimal Independent Unit (MIU) readiness layer.
```

Three identity statements that this contract takes as **given** and
must hold across every readiness step:

```text
SlotGeometryCandidate(length = 1) is the completed output of
Phase-2 Batch 1.

SlotGeometryCandidate(length = 1) is geometrically valid.

SlotGeometryCandidate(length = 1) is not, by itself, a minimal
independent functional unit.
```

This document does **not** implement `MinimalIndependentUnitReadinessQiyas`,
does **not** implement `MinimalCompleteClosureEvidence` as a runtime
type, does **not** modify any source file or test, and does **not**
modify any existing constitutional document. It only fixes the
contract that any future implementation must satisfy *before* an
implementation PR may be opened.

---

## 1. The Principle

The MIU readiness layer answers exactly one question, and refuses
to answer any other:

```text
Question (admissible):
  Which SlotGeometryCandidate(length = 1) is eligible to function
  later as a minimal independent functional unit?

Question (inadmissible — strictly later concerns):
  What does this unit mean?
  Does this unit discharge a لفظ?
  Does this unit licence a Dalalah?
  Does this unit licence a Hukm?
  Does this unit licence a RealityClaim?
```

The output of MIU readiness is **not** meaning, **not** a لفظ, **not**
a dalalah, **not** a hukm, **not** a reality claim. It is a
candidate-only signal that a particular `SlotGeometryCandidate(length
= 1)` *may be considered* by a strictly later layer as a minimal
independent functional unit. The signal carries no semantic content.

The two governing one-liners restated:

```text
Geometric validity is not functional independence.
Functional readiness is not meaning.
```

```text
الصحة الهندسية ليست الاستقلال الوظيفي.
والجاهزية الوظيفية ليست المعنى.
```

`SlotGeometry` proves that a single slot is geometrically licensed.
**MIU readiness** proves that *this same* single slot is, additionally,
*eligible* to be considered as a minimal independent functional unit
under a layer-specific eligibility predicate. But even MIU readiness
remains `CandidateOnly`.

---

## 2. Closed Consumption Surface

`MinimalIndependentUnitReadinessQiyas` consumes exactly three input
types — and **only** these three. The consumption surface is closed
by constitutional ratification of this contract:

```text
admissible inputs:

  1. SlotGeometryCandidate(length = 1)
       — the geometrically-valid single-slot geometry.

  2. ArabicArticulationRegistry metadata
       — the per-entry metadata signal
         can_function_as_minimal_independent_unit (boolean),
         consulted as metadata only; never as a licensing claim.

  3. MinimalCompleteClosureEvidence
       — the closure readiness signal produced by the
         minimal-complete-closure predicate (per §1 / §3 of
         MINIMAL_COMPLETE_CLOSURE_CONTRACT.md) applied to the
         SlotGeometryCandidate(length = 1).
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
BoundaryCodePoint
ResidualCodePoint
SlotCandidate                           (must come via SlotGeometryQiyas)
SlotGeometryCandidate(length > 1)       (multi-slot geometries are
                                         not minimal-unit candidates)
WordCandidate                           (higher layer)
LafzCandidate                           (higher layer)
SentenceCandidate                       (higher layer)
ParagraphCandidate                      (higher layer)
DalalahCandidate                        (strictly later)
FinalMeaning                            (forbidden output anywhere)
HukmCandidate                           (forbidden output anywhere)
RealityClaim                            (forbidden output anywhere)
FinalCaseJudgment                       (forbidden output anywhere)
```

This rule is the load-bearing constitutional invariant of this
contract. Any future implementation PR that opens a direct path from
a non-`SlotGeometryCandidate(length = 1)` input into the readiness
layer is in violation of this contract and must be rejected at
review.

In particular: **`SlotGeometryCandidate(length > 1)` is not an
admissible input.** A multi-slot geometry is, by construction, not a
minimal-unit candidate at this layer; its functional question
belongs to strictly later (word- and sentence-) layers under
their own contracts. The MIU readiness layer answers about
`length == 1` geometries only.

---

## 3. The Governing Law

For a candidate `S = SlotGeometryCandidate(length = 1)`, an
`ArabicArticulationRegistry` metadata witness `M`, and a closure
evidence `E = MinimalCompleteClosureEvidence`:

```text
Admit(S, M, E) := True
  iff

    S satisfies §4.1 (length=1, mode=seed, geometric integrity);
    M.can_function_as_minimal_independent_unit == True;
    E witnesses minimal complete closure of S;
    every §6 invariant of this contract holds.
```

```text
S
  + ArabicArticulationRegistry metadata for S's symbol(s)
  + MinimalCompleteClosureEvidence for S
  → MinimalUnitReadinessCandidate

with:
  output_flags ⊇ {CandidateOnly}
  output_flags ∩ {HukmCandidate, RealityClaim, FinalMeaning,
                  FinalCaseJudgment, DalalahCandidate} = ∅
  identity_ids preserved from S
  identity_ids ∩ trace_ids = ∅
  rank = meet(S.rank, M-bearing-evidence.rank, E.rank, rule.rank_ceiling)
```

If any of the three conjuncts of `Admit` fails, the readiness layer
**must not** produce a `MinimalUnitReadinessCandidate`. It must
produce a blocked or deferred candidate (carrying the residuals that
witness the failure) or no candidate at all. The constitutional
default is to **refuse readiness silently**: lack of readiness is
not itself a candidate output and never escalates into another
candidate type.

`Admit` is **observation**, not promotion. It does not lift
`CandidateOnly`. It does not produce meaning, lafz, dalalah, hukm,
or reality. It does not transform `S` into anything other than what
`S` already is at the slot-geometry layer; it only attaches a
readiness witness *to* `S`.

---

## 4. Required Witnesses

### 4.1 The consumed `SlotGeometryCandidate(length = 1)`

Every `S` admitted into the readiness layer must satisfy the
following structural conditions (all read off the geometry layer's
own output per `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §6 / §9):

```text
S.candidate_type      == "SlotGeometryCandidate"
S.layer               == "SlotGeometryQiyas"
S.source_rule_id      ∈ {"slot_geometry.seed"}             (length=1 ⇒ seed only)
trace_ids carry       length = 1
trace_ids carry       construction_mode = "seed"
S.output_flags        ⊇ {CandidateOnly}
S.output_flags        ∩ {HukmCandidate, RealityClaim, FinalMeaning,
                         FinalCaseJudgment, DalalahCandidate} = ∅
S.identity_ids        non-empty
S.identity_ids ∩ S.trace_ids == ∅
S.rank                ≠ NO_EVIDENCE
S.status              == ACCEPTED                          (not blocked / deferred)
```

If any condition fails, `S` is **rejected** at the consumption
boundary; the readiness layer does not produce a
`MinimalUnitReadinessCandidate` for it. Rejection is recorded as a
residual on the readiness-layer request so the audit trail survives.

### 4.2 The `ArabicArticulationRegistry` metadata witness

A registry metadata witness `M` is the entry (or entries) returned
by the existing `ArabicArticulationRegistry` reader
(`get_articulations_by_symbol` / `get_primary_articulation`) for the
symbol(s) carried in `S.identity_ids` (specifically the
`identity:codepoint:*` entries that name the letter and the haraka
of the slot).

The registry's payload contains, for each entry:

```text
can_function_as_minimal_independent_unit  : Boolean
independent_unit_kind                     : str | None
independent_unit_requires                 : list[str]
notes                                     : str
```

The readiness layer reads only those four fields. It **must not** read
any other field from the registry, and **must not** use the registry
to substitute for any qiyas-layer transition. The registry is
metadata only (per the registry's own
`constitutional_role: "external_data_registry_only"`); it produces
no `Candidate` and licenses no algebraic transition by itself.

For the readiness layer to admit `S`, the metadata witness must
satisfy:

```text
can_function_as_minimal_independent_unit == True
```

For symbols whose registry returns multiple variants (e.g. `و` and
`ي` each carry both a `_madd` and a `_non_madd` entry), the
readiness layer must rely on `get_primary_articulation(symbol)` —
which the registry deliberately returns as `None` for ambiguous
symbols — and admit only those for which a single primary entry
exists *and* its `can_function_as_minimal_independent_unit` is
`True`. The constitutional discipline is: ambiguity at the metadata
layer is not resolved here; the readiness layer refuses to choose
between variants without evidence (mirroring the registry's own
`get_primary_articulation` discipline).

### 4.3 The `MinimalCompleteClosureEvidence` witness

`MinimalCompleteClosureEvidence` is the closure-readiness signal
produced by applying the **minimal complete closure predicate**
(per `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3) to the
`SlotGeometryCandidate(length = 1)`. For the slot-geometry layer
this means the eight conjunctive conditions of §3.1–§3.8 of the
closure contract, instantiated for the slot-geometry layer per
`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §8:

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

For `S` with `length = 1`, "licensed beginning" and "licensed
ending" coincide in the degenerate `Seed` case
(`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §3.1); "all internal
bindings" is vacuously satisfied (no `Extend` step); the remaining
conditions are checked structurally on `S`'s fields.

`MinimalCompleteClosureEvidence` is the runtime carrier of the
result of that predicate. This contract defines it as a **contract
concept only**; it does not implement it. A later contract PR will
fix its runtime shape and its production rule. Until then, the
readiness layer must treat it as a required input whose absence
blocks the readiness step.

`MinimalCompleteClosureEvidence` is **not portable** between
layers. A word-layer or sentence-layer closure evidence is a
distinct type and must not substitute here.

---

## 5. The Output — `MinimalUnitReadinessCandidate`

The single admissible output type is `MinimalUnitReadinessCandidate`.

Naming discipline — the chosen name is:

```text
MinimalUnitReadinessCandidate
```

The name `MinimalIndependentMeaningCandidate` is **forbidden**. The
output is a readiness signal, never a meaning claim; using "Meaning"
in the type name would imply semantic finality and is therefore
constitutionally inadmissible. The shorter `MinimalUnitReadiness`
form is preferred over `MinimalIndependentUnitReadiness` to keep
the type name compact while leaving the *contract* name
(`MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT`) explicit about the
domain.

The candidate's structural shape (read off the kernel's standard
`_make_candidate_set` machinery; see `RECURSIVE_LICENSED_EXTENSION_
CONTRACT.md` §10):

```text
candidate_type    == "MinimalUnitReadinessCandidate"
layer             == "MinimalIndependentUnitReadinessQiyas"
source_rule_id    == "minimal_unit_readiness.admit"        (reserved name)
output_flags      ⊇ {CandidateOnly}
output_flags      ∩ {HukmCandidate, RealityClaim, FinalMeaning,
                     FinalCaseJudgment, DalalahCandidate} = ∅
identity_ids      ⊇ S.identity_ids
identity_ids ∩ trace_ids == ∅
rank              ≤ rule.rank_ceiling
                    and = meet(S.rank, M-evidence.rank, E.rank, rule.rank_ceiling)
trace_ids         carry an `is_minimal_unit_ready: true` marker
                  (metadata-on-trace, never identity)
trace_ids         carry the symbol of the admitted unit
                  (for audit display, not for licensing)
residuals         ⊇ S.residuals  (preserved end-to-end)
```

`is_minimal_unit_ready` is a **metadata marker on `trace_ids`** —
not an identity entry, not a final-judgment flag, and not a
semantic claim. It carries no entailment beyond the readiness
question of §1.

`MinimalUnitReadinessCandidate` is still `CandidateOnly`. It is
admissible **only** as a consumable for whatever strictly later
layer the constitution eventually ratifies above it (a word layer,
a lafz layer, or a Dalalah-prerequisite layer). It is **not** a
WordCandidate, **not** a LafzCandidate, **not** a DalalahCandidate.
Crossing into any of those types is a strictly later concern under
its own contract.

---

## 6. Invariants Preserved by Every `Admit` Step

Every invocation of the readiness layer's `Admit` step must
preserve the §4 invariants of `CLAUDE.md` and the §6 invariants of
`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`, augmented by the
readiness-specific witnesses:

```text
identity preservation         (CLAUDE.md §4 invariant 4)
trace separation              (CLAUDE.md §4 invariants 1–3)
rank meet semantics           (CLAUDE.md §4 invariant 6)
residual preservation         (CLAUDE.md §4 invariant 7)
blocking difference annihilation
                              (CLAUDE.md §4 invariant 5)
CandidateOnly safety          (CLAUDE.md §4 invariant 9)
no skipped layers             (CLAUDE.md §4 invariant 10)
no final meaning              (CLAUDE.md §4 invariant 10)
no hukm                       (CLAUDE.md §4 invariant 10)
no reality claim              (CLAUDE.md §4 invariant 10)
no dalalah                    (extension specific to this contract)
no lafz                       (extension specific to this contract)
no word                       (extension specific to this contract)
```

The rank-meet formula at this layer:

```text
rank_out =
    rank(S)
  ∧ rank(M-bearing-evidence)
  ∧ rank(E)
  ∧ rank(rule)
```

If any contributing rank is `NO_EVIDENCE`, the meet collapses to
`NO_EVIDENCE` and the resulting candidate fails the
`rank ≠ NO_EVIDENCE` admission check; no
`MinimalUnitReadinessCandidate` is produced.

Only the canonical six rank names of `TERMINOLOGY_MAP.md` §2 may be
used (`NO_EVIDENCE … MASS_TRANSMISSION`). Only the canonical six
gate names of `TERMINOLOGY_MAP.md` §3 may be used
(`CAUSE … NULLITY`). The public English claim prefixes
(`base: / branch: / attribute: / effective_cause: / difference: /
gate:`) fixed by `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §9 / §9.1
appear in documentation; the canonical Arabic-rooted claim grammar
(`اصل: / فرع: / وصف: / علة: / فارق: / وادي:`) fixed by
`TERMINOLOGY_MAP.md` §4 remains the kernel-consumed grammar. No new
claim prefix, no new rank, and no new gate is introduced by this
document.

---

## 7. Eligibility Sets (Initial Reading)

Per the maintainer's ratified reading, the initial eligibility list
of letters whose registry entry carries
`can_function_as_minimal_independent_unit = True` is — and must be —
exactly the eight entries already present in
`src/qiyas_core/data/arabic_articulation_registry.json`'s
`minimal_independent_unit_policy.core_independent_letters`:

```text
و، ف، ب، ك، ل، س، أ، ت
```

Letters whose registry entry carries
`can_function_as_minimal_independent_unit = False` — and which the
readiness layer must therefore **reject** as non-ready — include
(non-exhaustively):

```text
ض، ص، ر، ق, م، ن، ه، ا
```

For symbols carrying *multiple* variants
(`و` has `_madd` and `_non_madd`; `ي` has `_madd` and `_non_madd`),
the readiness layer follows the registry's own discipline: it
consults `get_primary_articulation(symbol)`. When that returns
`None` (ambiguity), the readiness layer **refuses to admit** the
candidate — the constitutional default is to defer rather than
silently choose a variant. The same discipline rejects any
`SlotGeometryCandidate(length = 1)` whose underlying symbol the
registry does not recognise.

This eligibility set is read **at construction time of the
readiness rule**, not hard-coded by symbol. The readiness layer
*does not* maintain a parallel list of eligible letters; it
consults the registry through the existing reader API. If the
registry is later amended (under its own `PR_SCHEDULING_POLICY.md`
§1.4 Data Registry PR), the readiness layer's behaviour follows
the amendment without code change.

This contract does **not** add any letter to the eligibility set,
remove any letter from it, or amend the registry. Amendments are
strictly later concerns under their own contract / PR.

---

## 8. Forbidden Outputs

`MinimalIndependentUnitReadinessQiyas`, when implemented in a later
PR, must declare the following types in its `forbidden_outputs`:

```text
HukmCandidate                            (CONSTITUTIONAL_BASE)
RealityClaim                             (CONSTITUTIONAL_BASE)
FinalMeaning                             (CONSTITUTIONAL_BASE)
FinalCaseJudgment

DalalahCandidate
WordCandidate
LafzCandidate
SentenceCandidate
ParagraphCandidate
DiscourseGeometryCandidate
TextGeometryCandidate

MinimalIndependentMeaningCandidate       (forbidden by §5 of this
                                          contract — readiness is not
                                          meaning)
```

It may produce **only** the following output candidate type:

```text
MinimalUnitReadinessCandidate
```

No second admissible output is reserved by this contract.

---

## 9. Relationship to `SlotGeometryQiyas`

`SlotGeometryQiyas` (Phase-2 Batch 1) proves that a single slot —
or a sequence of slots — is geometrically licensed under the
recursive `Seed`/`Extend` law. It answers:

```text
Is this sequence of slots geometrically ordered and bound under a
licensed binding?
```

`MinimalIndependentUnitReadinessQiyas` (this contract) does **not**
re-answer that question. It strictly consumes the `length = 1`
output of `SlotGeometryQiyas` and answers a different question:

```text
Is this geometrically-valid single slot eligible to be considered
later as a minimal independent functional unit?
```

The two questions compose:

| Question                                                              | Law                                                                | Operator                                  |
| --------------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------- |
| Is the slot geometrically licensed?                                   | `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`                        | `seed_geometry / extend_geometry`         |
| Is the geometrically-valid length-1 slot eligible as minimal unit?    | this contract                                                      | `Admit(S, M, E)`                          |
| What does the unit *mean*?                                            | strictly later contract                                            | not authorised by this document           |

The readiness layer **must not** call back into the slot-geometry
layer to re-prove `S`. It also **must not** consume any
`SlotGeometryCandidate(length > 1)`; multi-slot geometries are not
minimal-unit candidates at this layer (cf. §2). A `length = 3`
geometry like `ضَرَبَ` is a perfectly licensed slot-geometry but
falls outside MIU readiness by construction.

The non-identity statements:

```text
SlotGeometryCandidate(length = 1)        ≠  MinimalUnitReadinessCandidate
SlotGeometryCandidate(length = 1)        ≠  WordCandidate
SlotGeometryCandidate(length = 1)        ≠  LafzCandidate
SlotGeometryCandidate(length = 1)        ≠  DalalahCandidate
MinimalUnitReadinessCandidate            ≠  WordCandidate
MinimalUnitReadinessCandidate            ≠  LafzCandidate
MinimalUnitReadinessCandidate            ≠  DalalahCandidate
MinimalUnitReadinessCandidate            ≠  FinalMeaning
MinimalUnitReadinessCandidate            ≠  HukmCandidate
MinimalUnitReadinessCandidate            ≠  RealityClaim
```

---

## 10. Relationship to `ArabicArticulationRegistry`

The Arabic articulation registry
(`src/qiyas_core/data/arabic_articulation_registry.json`) is an
**external data registry** per `PR_SCHEDULING_POLICY.md` §1.4 and
its own self-declared
`constitutional_role: "external_data_registry_only"`. The registry:

```text
does_not_produce_Candidate
does_not_use_QiyasRule
does_not_use_QiyasKernel
does_not_produce_SlotCandidate
does_not_produce_SlotGeometry
does_not_produce_DalalahCandidate
does_not_produce_FinalMeaning
does_not_produce_HukmCandidate
does_not_produce_RealityClaim
metadata_may_support_later_evidence_only
```

The readiness layer reads the registry **as metadata only**. The
truth value of `can_function_as_minimal_independent_unit` is a
*necessary* witness for admission but is **not sufficient**: it
must be combined with a valid `SlotGeometryCandidate(length = 1)`
and a valid `MinimalCompleteClosureEvidence`. The registry alone
licenses no algebraic transition; it carries no rule, no gate, no
identity, and no candidate output.

The registry's `independent_unit_requires` field (already present
on every entry whose
`can_function_as_minimal_independent_unit == True`) names exactly
the strictly-later proofs that must be discharged before any
algebraic admission. The current entries name three:

```text
licensed_slot                  — discharged by SlotGeometryQiyas
minimal_complete_closure       — discharged by MinimalCompleteClosure
                                 evidence applied to the geometry
later_dalalah_evidence         — strictly later, not in scope here
```

The readiness layer discharges the first two via its inputs (§2 and
§4). The third — `later_dalalah_evidence` — remains a strictly
later concern under its own contract; the readiness layer **must
not** discharge it, **must not** consume it, and **must not** treat
its absence as a non-readiness condition. The readiness predicate
answers only readiness — *not* dalalah.

The non-identities:

```text
ArabicArticulationEntry                            ≠  MinimalUnitReadinessCandidate
can_function_as_minimal_independent_unit (boolean) ≠  Admit(S, M, E)
ArabicArticulationRegistry                         ≠  MinimalIndependentUnitReadinessQiyas
```

---

## 11. Relationship to Strictly Later Layers

This contract does **not** define:

```text
WordCandidate
LafzCandidate
SentenceCandidate
ParagraphCandidate
DalalahCandidate
FinalMeaning
HukmCandidate
RealityClaim
FinalCaseJudgment
SentenceGeometryCandidate
DiscourseGeometryCandidate
TextGeometryCandidate
```

When those higher layers are eventually contracted and implemented,
they will inherit the recursive-extension growth law of
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1, the closure
predicate of `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3, and
the input-type closure of *their* immediate predecessor — never
short-circuited to a lower layer's licensed output, and never
licensed to skip a layer.

A `MinimalUnitReadinessCandidate` is admissible *only* as a
consumable for the strictly next licensed layer's own admission
contract — and that admission contract does not yet exist. Until
it is ratified, a `MinimalUnitReadinessCandidate` has no further
licensed destination, and that is constitutionally correct.

In particular: this contract does **not** authorise the connection
of segments. The Phase-1 / Phase-2 demonstrated behaviour for
`ضَرَبَ وَ قَتَلَ` — three independent per-segment geometries with
no cross-segment binding — is maintained verbatim. The MIU
readiness layer operates at most on *one* `length = 1` geometry per
step; it does not aggregate, sequence, or bind across geometries.

---

## 12. Forbidden Jumps

The following jumps are constitutional violations and must be
rejected by the gate policy of any future implementation contract:

```text
SlotGeometryCandidate(length = 1)        →  WordCandidate
SlotGeometryCandidate(length = 1)        →  LafzCandidate
SlotGeometryCandidate(length = 1)        →  SentenceCandidate
SlotGeometryCandidate(length = 1)        →  DalalahCandidate
SlotGeometryCandidate(length = 1)        →  FinalMeaning
SlotGeometryCandidate(length = 1)        →  HukmCandidate
SlotGeometryCandidate(length = 1)        →  RealityClaim
SlotGeometryCandidate(length = 1)        →  FinalCaseJudgment

SlotGeometryCandidate(length > 1)        →  MinimalUnitReadinessCandidate

ArabicArticulationEntry                  →  MinimalUnitReadinessCandidate
                                          (registry alone is metadata only)
ArabicArticulationRegistry               →  MinimalUnitReadinessCandidate
                                          (registry alone licenses nothing)

raw text                                 →  MinimalUnitReadinessCandidate
SequenceContextTokenizer markers         →  MinimalUnitReadinessCandidate
SlotCandidate                            →  MinimalUnitReadinessCandidate
                                          (must come via SlotGeometryQiyas)

MinimalUnitReadinessCandidate            →  WordCandidate
MinimalUnitReadinessCandidate            →  LafzCandidate
MinimalUnitReadinessCandidate            →  DalalahCandidate
MinimalUnitReadinessCandidate            →  FinalMeaning
MinimalUnitReadinessCandidate            →  HukmCandidate
MinimalUnitReadinessCandidate            →  RealityClaim
MinimalUnitReadinessCandidate            →  FinalCaseJudgment
MinimalUnitReadinessCandidate            →  SlotGeometryCandidate(length > 1)
                                          (readiness does not licence
                                           geometry growth)

MinimalUnitReadinessCandidate            →  MinimalIndependentMeaningCandidate
                                          (the latter name is forbidden;
                                           §5 of this contract)
```

In full:

```text
A MinimalUnitReadinessCandidate is still CandidateOnly.
A MinimalUnitReadinessCandidate is not a higher-layer typed unit.
A MinimalUnitReadinessCandidate is not semantic finality.
A MinimalUnitReadinessCandidate is not a hukm.
A MinimalUnitReadinessCandidate is not a reality claim.
A MinimalUnitReadinessCandidate is not a dalalah.
Geometric validity is not functional independence.
Functional readiness is not meaning.
```

This list extends — does not replace — §11 of
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`, §11 of
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md`, and §11 of
`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`. All four lists are
binding simultaneously.

---

## 13. Worked Examples

The following examples illustrate the readiness predicate's
intended behaviour. They are documentation, not specification: the
canonical predicate is the one defined in §1 / §3.

### 13.1 `بِ` — admissible (subject to closure)

```text
Phase 1            : raw text "بِ" → SlotCandidate (ب + kasra)
Phase 2 Batch 1    : SlotCandidate → SlotGeometryCandidate(length = 1,
                                                          construction_mode = "seed")
ArabicArticulationRegistry:
                     get_articulations_by_symbol("ب")     → [lips_ba]
                     lips_ba.can_function_as_minimal_independent_unit
                                                          == True
MinimalCompleteClosureEvidence:
                     applied to the geometry, holds.
Admit(S, M, E)     : True
Output             : MinimalUnitReadinessCandidate
                     (trace_ids carry `is_minimal_unit_ready: true`
                      and the symbol `ب`; output_flags ⊇ {CandidateOnly};
                      identity preserved; no meaning, no dalalah,
                      no hukm, no reality claim.)
```

### 13.2 `ضَ` — geometrically valid, readiness rejected

```text
Phase 1            : raw text "ضَ" → SlotCandidate (ض + fatha)
Phase 2 Batch 1    : SlotCandidate → SlotGeometryCandidate(length = 1,
                                                          construction_mode = "seed")
ArabicArticulationRegistry:
                     get_articulations_by_symbol("ض")    → [tongue_dad]
                     tongue_dad.can_function_as_minimal_independent_unit
                                                         == False
Admit(S, M, E)     : False  (registry metadata witness fails)
Output             : no MinimalUnitReadinessCandidate is produced.
                     The slot-geometry S remains a perfectly licensed
                     SlotGeometryCandidate(length = 1) — geometric
                     validity is preserved; only readiness is denied.
                     The denial is recorded as a residual on the
                     readiness-layer request so the audit trail
                     survives.
```

### 13.3 `وَ` (non-madd waw) — admissible (subject to closure)

```text
Phase 1            : raw text "وَ" → SlotCandidate (و + fatha)
Phase 2 Batch 1    : SlotCandidate → SlotGeometryCandidate(length = 1,
                                                          construction_mode = "seed")
ArabicArticulationRegistry:
                     get_articulations_by_symbol("و")    → [jawf_waw_madd,
                                                            lips_waw_non_madd]
                     get_primary_articulation("و")       == None
                                                         (two variants)
                     → admissibility under the non-madd variant requires
                       per-context evidence the readiness layer must
                       consult; until that evidence is supplied, the
                       readiness layer DEFERS rather than admits.
                     For the demonstrated non-madd case backed by
                     evidence, lips_waw_non_madd
                       .can_function_as_minimal_independent_unit
                                                         == True
MinimalCompleteClosureEvidence:
                     applied to the geometry, holds.
Admit(S, M, E)     : True (non-madd variant licensed)
                   | Deferred (variant evidence absent)
                   | False (madd variant intended — non-eligible)
Output             : MinimalUnitReadinessCandidate (admitted)
                   | Deferred candidate (variant evidence missing)
                   | no MinimalUnitReadinessCandidate (rejected)
                     In none of the three cases is meaning,
                     dalalah, hukm, or reality produced.
```

### 13.4 `ضَرَبَ` — geometrically valid `length = 3`, not in scope

```text
Phase 1            : raw text "ضَرَبَ" → three SlotCandidates
Phase 2 Batch 1    : seed + extend + extend
                     → SlotGeometryCandidate(length = 3,
                                            construction_mode = "extension")
Admit(S, M, E)     : not applicable
Output             : the MIU readiness layer does NOT consume
                     SlotGeometryCandidate(length > 1).
                     The length=3 geometry is a perfectly licensed
                     Phase-2 output but it is not a minimal-unit
                     candidate. Its readiness question — if any —
                     belongs to a strictly later (word- / lafz-)
                     layer under that layer's own contract.
```

### 13.5 `ضَرَبَ وَ قَتَلَ` — three independent geometries

```text
Phase 1 / Phase 2 Batch 1:
                     three independent SlotGeometryCandidates,
                     one per tokenizer segment:
                       ضَرَبَ      length = 3, construction_mode = "extension"
                       وَ          length = 1, construction_mode = "seed"
                       قَتَلَ      length = 3, construction_mode = "extension"
                     no cross-segment binding (Phase-2 Batch 1 §5).
MIU readiness layer:
                     Considers ONLY the length = 1 geometry وَ.
                     The length = 3 geometries (ضَرَبَ, قَتَلَ) are
                     NOT inputs to this layer.
                     Output: at most one MinimalUnitReadinessCandidate
                     (for the وَ geometry, subject to §4.2 / §4.3).
                     No segment linking. No DalalahCandidate. No
                     WordCandidate. No meaning.
```

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the readiness predicate it fixes is binding
  on every future MIU implementation PR;
- **pre-implementation** — no `MinimalIndependentUnitReadinessQiyas`,
  no `MinimalCompleteClosureEvidence` runtime type, no readiness
  adapter, and no readiness rule is implemented at the time of
  merge;
- **slot-geometry-layer-strict** — the law applies *only* to
  `SlotGeometryCandidate(length = 1)`; multi-slot geometries are
  outside scope by construction.

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes a `MinimalIndependentUnitReadinessQiyas`
  adapter;
- any future PR that proposes a `MinimalCompleteClosureEvidence`
  runtime type;
- any future PR that proposes a readiness rule, beginning rule, or
  ending rule for the readiness layer;
- any future review that asks whether a proposed readiness
  consumption is licensed.

It supersedes nothing prior; it specialises the general
recursive-extension growth law and the general minimal-complete-
closure termination law to the per-symbol eligibility predicate
of the readiness layer.

It does **not** authorise the implementation of
`MinimalIndependentUnitReadinessQiyas` or of any of the layers,
evidences, rules, or catalogues it describes. Each must continue
to be ratified by its own contract PR under
`PR_SCHEDULING_POLICY.md` §1.1 before any implementation PR may be
opened under §1.3.

---

## 16. Non-Goals

This document does **not**:

- modify any file under `src/qiyas_core/`,
- modify any file under `tests/qiyas_core/`,
- modify `run_qiyas.py`,
- modify any file under `experimental/`,
- modify any other constitutional document,
- modify the `ArabicArticulationRegistry` (`data/sources/*.csv`,
  `src/qiyas_core/data/*.json`, `src/qiyas_core/arabic_articulation_registry.py`),
- modify `src/qiyas_core/slot_geometry_adapter.py` or
  `src/qiyas_core/rules/slot_geometry_rules.py`,
- introduce any new CI check, hook, bot, or automation,
- define any new candidate type beyond the single
  `MinimalUnitReadinessCandidate` admissible output (§5);
  `MinimalIndependentMeaningCandidate` is explicitly forbidden,
- introduce any new evidence shape, rule, or rank,
- introduce any new claim prefix beyond the public English names
  fixed in `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §9, with the
  Arabic correspondence already documented in `TERMINOLOGY_MAP.md`
  §4,
- introduce any new gate beyond the six canonical gates,
- produce `WordCandidate`, `LafzCandidate`, `SentenceCandidate`,
  `ParagraphCandidate`, `DiscourseGeometryCandidate`, or
  `TextGeometryCandidate`,
- produce `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`,
  `RealityClaim`, or `FinalCaseJudgment`,
- treat `SlotGeometryCandidate(length = 1)` as meaning,
- link tokenizer segments — `ضَرَبَ + وَ + قَتَلَ` remains three
  independent per-segment geometries; the readiness layer operates
  on at most one `length = 1` geometry per step,
- amend the registry's eligibility list (`و، ف، ب، ك، ل، س، أ، ت`)
  or its rejection list (`ض، ص، ر، ق، م، ن، ه، ا`),
- authorise any implementation, runtime, adapter, kernel surface,
  or test.

---

## 17. Glossary

| Term                                          | Meaning |
| --------------------------------------------- | --- |
| `MinimalIndependentUnitReadinessQiyas`        | The next-layer Qiyas adapter that produces `MinimalUnitReadinessCandidate`. Not implemented at the time of this document; reserved public name. |
| `MinimalUnitReadinessCandidate`               | The single licensed output of the readiness layer (§5). Carries `output_flags ⊇ {CandidateOnly}`, the slot-geometry's identities, and an `is_minimal_unit_ready: true` metadata marker on `trace_ids`. Still `CandidateOnly` regardless of the truth of `is_minimal_unit_ready`. |
| `MinimalIndependentMeaningCandidate`          | **Forbidden** type name (§5, §12). Readiness is not meaning. |
| `is_minimal_unit_ready`                       | Metadata marker on `trace_ids` of an admitted `MinimalUnitReadinessCandidate`. Never on `identity_ids`. Never a semantic claim. |
| `Admit(S, M, E)`                              | The readiness predicate `(SlotGeometryCandidate(length = 1), ArabicArticulationRegistry metadata, MinimalCompleteClosureEvidence) → Bool`. Observation only; not a producer. |
| `ArabicArticulationRegistry` metadata witness | The registry entry (or entries) for the symbol carried in `S.identity_ids`. Consulted via the existing reader API; metadata only, no licensing claim. |
| `MinimalCompleteClosureEvidence`              | Contract concept: the closure-readiness signal produced by `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md`'s eight-condition predicate applied to the slot-geometry layer (per `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §8). Runtime shape deferred to a strictly later contract. Not portable between layers. |
| eligibility set                               | Per §7: `و، ف، ب، ك، ل، س، أ، ت` initially. Read at construction time from the existing registry; not hard-coded by symbol. |
| rejection set (initial)                       | `ض، ص، ر، ق، م، ن، ه، ا` per §7. Read at construction time. |
| non-readiness                                 | The state of a `SlotGeometryCandidate(length = 1)` for which `Admit(S, M, E) == False`. Recorded as a residual on the readiness-layer request; does *not* produce a candidate of any type. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
