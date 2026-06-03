# RECURSIVE_LICENSED_EXTENSION_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> *licensed recursive extension* law as a global algebraic pattern of
> the Qiyas algebra. No code, no tests, no implementation are changed
> by this PR.
>
> **Authority basis:**
> `CLAUDE.md` §0 / §3 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
> `RESET_CONSTITUTION.md` §1 / §3,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4.
>
> **Governing one-liner:**
>
> ```
> Licensed recursive extension is a global algebraic pattern,
> not a shortcut to meaning.
> ```
>
> ```
> الامتداد العودي المرخّص نمط جبري عام عبر الطبقات،
> وليس اختصارًا إلى المعنى.
> ```

---

## 0. Provenance

This contract generalises a pattern that already appears once in the
qiyas algebra — the formation of a geometric whole from licensed
candidates — and elevates it to a constitutional **law that applies
at every licensed layer of the system**.

The pattern is the same at the slot layer, at the word layer, at the
sentence layer, and at the paragraph layer; the *binding evidence*
that licenses each extension is **different at every layer**. This
document fixes that distinction.

This document does **not**:

- implement `SlotGeometryQiyas`,
- implement `SlotBindingEvidence`,
- implement `WordBindingEvidence`,
- implement `DiscourseBindingEvidence`,
- define `DalalahCandidate`,
- define `HukmCandidate`,
- modify any file under `src/qiyas_core/`,
- modify any file under `tests/qiyas_core/`,
- modify any file under `experimental/`,
- modify `run_qiyas.py`.

It only fixes the algebraic law that every future layer of that shape
must satisfy.

---

## 1. The General Law

For any licensed layer `L` of the Qiyas algebra, with candidate type
`LCandidate` and geometry candidate type `LGeometryCandidate`:

```text
LGeometryCandidate(1)
    = Seed(LCandidate₁)

LGeometryCandidate(n + 1)
    = Extend(
          LGeometryCandidate(n),
          LCandidateₙ₊₁,
          LBindingEvidenceₙ
      )
```

In words:

```
Every n+1-unit licensed geometry is a licensed n-unit geometry
extended by one further licensed unit, via a binding evidence
specific to that layer.
```

```
كل بنية من n+1 وحدة هي بنية مرخّصة من n وحدة،
مضافًا إليها وحدة مرخّصة واحدة عبر دليل ربط خاص بتلك الطبقة.
```

`Extend` is **not** free concatenation. It is a *licensed transition*
that:

1. consumes only the immediately previous layer's licensed output,
2. consumes a layer-specific `LBindingEvidence`,
3. preserves identity, trace, rank, and residuals (§8),
4. blocks on any invalidating difference (§8),
5. produces an `LGeometryCandidate`, never a final meaning.

A `Seed` is the degenerate case `n = 1`: a single `LCandidate`
admitted as a one-unit geometry without any extension step. The Seed
must already be a licensed `LCandidate` produced by its own layer —
it is never synthesised from raw text, tokenizer markers, or any
upstream layer that is not the immediate predecessor of `L`.

---

## 2. Slot Layer Application

The slot layer is the first place the law applies in the canonical
qiyas chain:

```text
SlotCandidate
    → SlotGeometryCandidate(length = 1)

SlotGeometryCandidate(length = n)
    + SlotCandidate
    + SlotBindingEvidence
    → SlotGeometryCandidate(length = n + 1)
```

The binding evidence is `SlotBindingEvidence`. Its context is
`INTRA_UTTERANCE`: it licenses geometric adjacency between slots that
belong to a single contiguous tokenizer segment.

It must be stated, in full:

```text
SlotGeometryCandidate does not denote meaning.
SlotGeometryCandidate does not denote DalalahCandidate.
SlotGeometryCandidate does not denote HukmCandidate.
SlotGeometryCandidate does not denote RealityClaim.
SlotGeometryCandidate is not FinalMeaning.
```

`SlotGeometryCandidate` answers exactly one question:

```
Is this sequence of slots geometrically ordered and bound under a
licensed binding?
```

```
هل الخانات مرتبة ومربوطة هندسيًا بشكل مرخّص؟
```

It does **not** answer:

```
Does this utterance discharge an independent verbal meaning?
```

```
هل هذا اللفظ يؤدي معنىً مستقلًا؟
```

That question belongs to a strictly later layer (`DalalahCandidate`
and above), which is **not** in scope of this contract.

---

## 3. Word Layer Application

The same recursive law extends to the composition of words inside a
sentence — but **not** as a jump from slots into meaning, and **not**
under `SlotBindingEvidence`.

```text
WordCandidate
    → SentenceGeometryCandidate(length = 1)

SentenceGeometryCandidate(length = n)
    + WordCandidate
    + WordBindingEvidence
    → SentenceGeometryCandidate(length = n + 1)
```

It must be stated, in full:

```text
WordBindingEvidence ≠ SlotBindingEvidence.
SentenceGeometryCandidate does not denote FinalMeaning.
SentenceGeometryCandidate does not denote HukmCandidate.
SentenceGeometryCandidate does not denote RealityClaim.
```

`WordBindingEvidence` may witness:

- linear word order under the segment's framing,
- syntactic compatibility between adjacent words (`base:` of the
  geometry compatible with `branch:` of the new candidate, under a
  layer-specific licensing gate),
- grammatical role and case-marking compatibility,
- positional licensing inside a syntactic frame,
- agreement, government, or other licensed syntactic relations.

It may **not** witness:

- final lexical meaning,
- final pragmatic intent,
- jurisprudential ruling (`hukm`),
- factual reference to reality.

A `SentenceGeometryCandidate` is still `CandidateOnly`. Its
production discharges no `DalalahCandidate`, no `HukmCandidate`, and
no `RealityClaim`.

---

## 4. Sentence Layer Application (Discourse)

Inside a paragraph or a discourse, sentences combine under the same
law, with **discourse-level** binding evidence:

```text
SentenceCandidate
    → DiscourseGeometryCandidate(length = 1)

DiscourseGeometryCandidate(length = n)
    + SentenceCandidate
    + DiscourseBindingEvidence
    → DiscourseGeometryCandidate(length = n + 1)
```

It must be stated, in full:

```text
DiscourseBindingEvidence operates in DISCOURSE_CONTEXT.
SlotBindingEvidence operates in INTRA_UTTERANCE.
DISCOURSE_CONTEXT and INTRA_UTTERANCE are not interchangeable.
SlotBindingEvidence is not admissible as binding evidence for
sentences or for discourse.
```

`DiscourseBindingEvidence` may witness:

- discourse-cohesion signals (continuation, contrast, causation,
  enumeration),
- topic continuity / referential anchoring across sentences,
- explicit framing markers permitted by the discourse layer's own
  licensing gate,
- macro-structural roles (e.g. premise vs. consequent placement)
  insofar as they are themselves licensed by a discourse rule.

It must not witness sentence-internal slot adjacency. That work is
already discharged at the slot layer; importing it here would be a
layer-skipping violation (CLAUDE.md §19).

---

## 5. Paragraph Layer Application (Text)

Paragraphs combine into a text under the same law, with **text-level**
binding evidence:

```text
ParagraphCandidate
    → TextGeometryCandidate(length = 1)

TextGeometryCandidate(length = n)
    + ParagraphCandidate
    + TextBindingEvidence
    → TextGeometryCandidate(length = n + 1)
```

`TextBindingEvidence` also operates in `DISCOURSE_CONTEXT` but at a
strictly higher granularity than `DiscourseBindingEvidence`. The two
must not be conflated: every layer's binding evidence has its own
admissibility predicate, its own claim grammar, and its own gate
policy.

`TextGeometryCandidate` is still `CandidateOnly`. It does not denote
`FinalMeaning`, `HukmCandidate`, `RealityClaim`, or
`FinalCaseJudgment`.

---

## 6. Binding Evidence Differs by Layer

The recursive **shape** is one. The binding evidence at each layer is
**different**, and it is **not portable** between layers.

| Layer            | Unit                | Geometry candidate              | Binding evidence            | Context                          |
| ---------------- | ------------------- | ------------------------------- | --------------------------- | -------------------------------- |
| Slot layer       | `SlotCandidate`     | `SlotGeometryCandidate`         | `SlotBindingEvidence`       | `INTRA_UTTERANCE`                |
| Word layer       | `WordCandidate`     | `SentenceGeometryCandidate`     | `WordBindingEvidence`       | `INTRA_UTTERANCE` / syntax       |
| Sentence layer   | `SentenceCandidate` | `DiscourseGeometryCandidate`    | `DiscourseBindingEvidence`  | `DISCOURSE_CONTEXT`              |
| Paragraph layer  | `ParagraphCandidate`| `TextGeometryCandidate`         | `TextBindingEvidence`       | `DISCOURSE_CONTEXT`              |

It must be stated, in full:

```text
The recursive shape is one.
The binding evidence is different at every layer.
Binding evidence is not portable between layers.
A layer may consume only the licensed outputs of its immediate
predecessor — nothing earlier, nothing later.
```

```text
الشكل العودي واحد.
لكن دليل الربط في كل طبقة مختلف.
لا يجوز نقل دليل ربط من طبقة إلى أخرى.
لا يجوز أن تستهلك طبقة مخرجات غير الطبقة السابقة مباشرة.
```

The **input-type closure** of each layer is therefore narrow by
construction:

- `SlotGeometryQiyas` consumes `SlotCandidate*` only.
- The word layer consumes `WordCandidate*` only.
- The sentence layer consumes `SentenceCandidate*` only.
- The paragraph layer consumes `ParagraphCandidate*` only.

Any other consumption is a forbidden jump (§11).

---

## 7. Invariants Preserved by Every `Extend`

For every layer `L`, every invocation of `Extend` must preserve the
canonical septet of `LAYER_CONTRACT_CONSTITUTION.md` §2.1:

```text
Candidate → Gate → Evidence → Domain → Rank → Residuals → Trace
```

Concretely, every `Extend` step at every layer must preserve:

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

In particular:

1. **Identity preservation.** The `identity_ids` of the input
   geometry candidate and of the new unit candidate are both
   represented in the output geometry candidate's `identity_ids`; no
   input identity is dropped or rewritten. (CLAUDE.md §4 invariant 4)

2. **Identity / trace separation.** The output's `identity_ids` and
   `trace_ids` remain disjoint. Evidence may add trace but must not
   consume identity. (CLAUDE.md §4 invariants 1–3)

3. **Residual preservation.** Every blocking or deferring residual
   on the inputs survives into the output's `residuals`; nothing is
   silently discarded. (CLAUDE.md §4 invariant 7)

4. **Blocking difference annihilation.** If any invalidating
   `difference:` claim is present in the binding evidence, the
   `Extend` is blocked and the output is a blocked candidate with
   the residual recorded — never an accepted geometry candidate of
   greater length. (CLAUDE.md §4 invariant 5)

5. **`CandidateOnly` safety.** The output carries
   `output_flags ⊇ {CandidateOnly}` and is free of any final-judgment
   flag (`HukmCandidate`, `RealityClaim`, `FinalMeaning`,
   `FinalCaseJudgment`). (CLAUDE.md §4 invariant 9)

6. **No skipped layers.** No `Extend` may produce, directly or
   indirectly, the licensed output of any layer beyond `L`.
   (CLAUDE.md §4 invariant 10)

---

## 8. Rank Meet Semantics

The output rank of every `Extend` is the *meet* of all participating
ranks. No `Extend` may raise the rank of its output above the
weakest contributing rank:

```text
rank_out =
    rank(previous_geometry)
  ∧ rank(new_candidate)
  ∧ rank(binding_evidence)
  ∧ rank(rule)
```

The rank lattice is the canonical finite chain fixed in
`TERMINOLOGY_MAP.md` §2. Only the following rank names may be used in
this contract and in any future contract that consumes it:

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
regardless. (CLAUDE.md §4 invariant 6; `TERMINOLOGY_MAP.md` §2.)

---

## 9. Licensing Gates and Claim Prefixes

Every `Extend` step must clear the conjunctive six-gate (وادي)
licensing predicate fixed in `TERMINOLOGY_MAP.md` §3. Only the
following gate names may be used:

```text
CAUSE
CONDITION
OBSTACLE
VALIDITY
CORRUPTION
NULLITY
```

The gates are conjunctive: the `Extend` is licensed iff **every**
declared gate holds. If any gate fails, the output is blocked with a
residual; the recursive geometry does not advance in length.

Claim grammar in this contract uses the public English claim
prefixes:

```text
base:               (the established source of the extension)
branch:             (the determined target of the extension)
attribute:          (the effective attribute of the new unit)
effective_cause:    (the licensing cause of the extension)
difference:         (the invalidating difference, if any)
gate:               (the validity-gate claim)
```

### 9.1 Correspondence with the canonical implementation grammar

This contract uses English public names for cross-layer documentation:
`base:`, `branch:`, `attribute:`, `effective_cause:`, `difference:`,
`gate:`.

This does **not** replace the canonical implementation claim grammar
already consumed by the kernel. Where the current implementation uses
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
introduced by this document. The English prefixes are
**documentation-side public names** intended for cross-layer prose
and the paper; the Arabic-rooted claim prefixes fixed in
`TERMINOLOGY_MAP.md` §4 remain the canonical claim grammar consumed
by `QiyasKernel`, and every evidence-producing instrument continues
to emit them verbatim.

### 9.2 Reserved gate-policy names

For gate-policy designation at the slot layer (and at any future
layer that adopts the same shape), this contract **reserves** the
following names:

```text
SlotGatePolicy
GATE_REQUIRED_CLAIMS
gate_policy
```

These are **reserved public names for future contracts**, not current
implementation symbols. No such name exists in `src/qiyas_core/` at
the time of this document's ratification, and this document does not
authorise their implementation. Any future implementation contract
for `SlotGeometryQiyas` (§12) must use these names verbatim once
ratified; until then, these names remain forward-binding
reservations only. No legacy gate-policy naming is admissible.

---

## 10. The `Extend` Transition — Required Shape

Every concrete `Extend` step, at every layer, must satisfy the
following docs-level signature:

```text
Extend(
    previous : LGeometryCandidate(length = n),
    new_unit : LCandidate,
    binding  : LBindingEvidence,
)
  → LGeometryCandidate(length = n + 1)    -- on success
  | BlockedGeometryCandidate(reason)      -- on blocking difference
                                          --   or failed gate
  | DeferredGeometryCandidate(reason)     -- on insufficient evidence
```

Required pre-conditions:

1. `previous.candidate_type == LGeometryCandidate`,
2. `new_unit.candidate_type == LCandidate`,
3. `binding.candidate_type == LBindingEvidence`,
4. `previous.layer == L` and `new_unit.layer == L`'s immediate
   predecessor (i.e. the layer that produces `LCandidate`),
5. `binding.layer == L` (binding evidence is produced *by* `L`,
   licensing the extension *within* `L`),
6. `previous`, `new_unit`, and `binding` all carry non-empty
   `identity_ids` disjoint from their `trace_ids`,
7. `binding` is in the licensed context of `L`
   (`INTRA_UTTERANCE` for slot/word, `DISCOURSE_CONTEXT` for
   sentence/paragraph; §6 table).

Required post-conditions:

1. `output.candidate_type == LGeometryCandidate`,
2. `output.layer == L`,
3. `output.identity_ids ⊇ previous.identity_ids ∪ new_unit.identity_ids`,
4. `output.trace_ids ⊇ previous.trace_ids ∪ new_unit.trace_ids ∪ binding.trace_ids`,
5. `output.identity_ids ∩ output.trace_ids == ∅`,
6. `output.rank == meet(previous.rank, new_unit.rank, binding.rank,
   rule.rank_ceiling)`,
7. `output.residuals ⊇ previous.residuals ∪ new_unit.residuals ∪
   binding.residuals` (preserved, possibly augmented by new residuals
   produced by the gate check itself),
8. `output.output_flags ⊇ {CandidateOnly}`,
9. `output.output_flags ∩ {HukmCandidate, RealityClaim,
   FinalMeaning, FinalCaseJudgment} == ∅`,
10. on any blocking `difference:` or failed `gate:`, the output is
    `Blocked`/`Deferred` and has length `n`, not `n + 1`.

Any concrete implementation of `Extend` for any layer must witness
these conditions in its own evidence set; this contract does not
implement the witnessing.

---

## 11. Forbidden Jumps

The following jumps are constitutional violations at every layer.
They must be rejected by the gate policy of any future implementation
contract, and must be enforced by the `forbidden_outputs` of any
future rule:

```text
raw text                            →  SlotGeometry
tokenizer markers                   →  SlotGeometry
UnicodeCandidate                    →  SlotGeometry
TypedCodePoint*                     →  SlotGeometry
LetterIdentityCarrier               →  SlotGeometry
HarakaFunctionCarrier               →  SlotGeometry
PositionCarrier                     →  SlotGeometry
CarrierBindingCandidate             →  SlotGeometry
ConditionedTypedSequence outputs    →  SlotGeometry
SlotCandidate*                      →  DalalahCandidate
SlotGeometryCandidate               →  FinalMeaning
WordCandidate*                      →  HukmCandidate
SentenceGeometryCandidate           →  RealityClaim
DiscourseGeometryCandidate          →  FinalCaseJudgment
```

In full:

```text
A geometry candidate is still CandidateOnly.
A geometry candidate is not semantic finality.
A geometry candidate is not a hukm.
A geometry candidate is not a reality claim.
```

This list is not exhaustive of all forbidden jumps in the system; it
is the *minimum* a future implementation contract for any
geometry-producing layer must reject.

---

## 12. Relationship to the upcoming SlotGeometry Alignment-Trace Contract

This contract **does not** implement `SlotGeometryQiyas`. It only
fixes the recursive law that `SlotGeometryQiyas` and every
analogously-shaped future layer must obey.

The next docs-only PR is reserved for the **SlotGeometry
alignment-trace contract**, which will fix the additional contract
that `SlotGeometryQiyas` must satisfy beyond §10 above. That contract
must declare, at minimum, that:

`SlotGeometryQiyas` may consume only:

```text
SlotCandidate*
```

Each `SlotCandidate` consumed by `SlotGeometryQiyas` must satisfy:

```text
candidate_type      == "SlotCandidate"
source_rule_id      == "slot.composition"
trace_ids           contain an alignment_ref entry
output_flags        contain CandidateOnly
output_flags        contain no forbidden final flags
                    ({HukmCandidate, RealityClaim, FinalMeaning,
                      FinalCaseJudgment})
identity_ids        are preserved and non-empty
identity_ids ∩ trace_ids == ∅
rank                ≠ NO_EVIDENCE
```

`SlotGeometryQiyas` must **not** consume directly:

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
```

This forward declaration is binding on the next docs-only PR. It is
not implemented here.

---

## 13. Relationship to Higher Layers (Dalalah, Hukm, etc.)

This contract does **not** define:

- `DalalahCandidate`,
- `HukmCandidate`,
- `RealityClaim`,
- `FinalMeaning`,
- `FinalCaseJudgment`.

It only fixes the *pattern* under which any future
geometry-producing layer must compose, so that — when those higher
layers are eventually contracted and implemented — they cannot
constitutionally arise from a geometry candidate without their own
licensed transition and their own binding evidence.

Any future layer that adopts the recursive shape introduced here
must continue to satisfy, *unweakened*:

```text
typed input only            (only the immediate predecessor's outputs)
licensed binding only       (a layer-specific binding evidence)
identity preservation       (CLAUDE.md §4 invariant 4)
trace separation            (CLAUDE.md §4 invariants 1–3)
rank meet                   (§8)
residual preservation       (§7 / CLAUDE.md §4 invariant 7)
CandidateOnly safety        (§7 / CLAUDE.md §4 invariant 9)
no skipped layers           (§7 / CLAUDE.md §4 invariant 10)
```

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the algebraic law it fixes is binding on every
  future geometry-producing PR;
- **pre-implementation** — no `SlotGeometryQiyas`, no
  `SlotBindingEvidence`, no `WordBindingEvidence`, and no
  `DiscourseBindingEvidence` exist at the time of merge;
- **layer-agnostic** — the law applies uniformly at the slot, word,
  sentence, and paragraph layers (and at any later layer of the same
  shape that may be ratified by future constitutional amendment).

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes a geometry-producing layer
  (`SlotGeometryQiyas`, the word-layer assembly, the sentence-layer
  assembly, the paragraph-layer assembly, or any layer adopting the
  same shape);
- any future binding-evidence contract
  (`SlotBindingEvidence`, `WordBindingEvidence`,
  `DiscourseBindingEvidence`, `TextBindingEvidence`);
- any future review that asks whether a proposed `Extend` step is
  algebraically licensed.

It supersedes nothing prior; it generalises the pattern that already
exists at the slot layer (`SLOT_COMPOSITION_RULE`) and elevates it to
a constitutional law for every analogous future layer.

It does **not** authorise the implementation of any of the layers it
describes. Each must be ratified by its own docs-only contract PR
before any implementation PR may be opened.

---

## 16. Glossary

| Term                          | Meaning |
| ----------------------------- | --- |
| licensed recursive extension  | The general algebraic pattern fixed in §1. |
| `Seed`                        | The degenerate `n = 1` case: a single `LCandidate` admitted as a one-unit geometry without an `Extend` step. |
| `Extend`                      | The licensed transition fixed in §10. Not free concatenation. |
| `LCandidate`                  | The licensed candidate produced by layer `L`'s predecessor (e.g. `SlotCandidate` for the slot geometry layer). |
| `LGeometryCandidate`          | The licensed geometry candidate produced by layer `L`. Still `CandidateOnly`. |
| `LBindingEvidence`            | The layer-specific binding evidence that licenses an `Extend` step at layer `L`. Not portable between layers. |
| `INTRA_UTTERANCE`             | The context of binding evidence that operates inside a single tokenizer segment (slot layer, word layer). |
| `DISCOURSE_CONTEXT`           | The context of binding evidence that operates across tokenizer segments / utterances (sentence layer, paragraph layer). |
| `CandidateOnly`               | The output flag asserting that the candidate is non-final; required on every `LGeometryCandidate` at every layer. |
| `SlotGatePolicy`              | Reserved public name for the slot layer's gate-policy declaration in a future contract; not a current implementation symbol. |
| `GATE_REQUIRED_CLAIMS`        | Reserved public name for the gate's required-claim list constant in a future contract; not a current implementation symbol. |
| `gate_policy`                 | Reserved public name for a layer's gate-policy reference in a future contract; not a current implementation symbol. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
