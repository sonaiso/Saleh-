# MINIMAL_COMPLETE_CLOSURE_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> *minimal complete closure* law as the termination companion to
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`. No code, no tests, no
> implementation are changed by this PR.
>
> **Authority basis:**
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §7 / §11,
> `CLAUDE.md` §0 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
> `RESET_CONSTITUTION.md` §1 / §3,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4.
>
> **Governing one-liner:**
>
> ```
> Recursive extension answers how a geometry grows.
> Minimal complete closure answers when a geometry may stop growing
> as a complete candidate within its layer.
> ```
>
> ```
> الامتداد العودي يجيب: كيف تنمو البنية.
> الإغلاق الأدنى الكامل يجيب: متى تتوقف البنية عن النمو بوصفها مرشحًا
> كاملًا داخل طبقتها.
> ```

---

## 0. Provenance

`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` fixes the *growth law*: the
licensed `Extend(LGeometryCandidate(n), LCandidateₙ₊₁,
LBindingEvidenceₙ) → LGeometryCandidate(n+1)` transition that
governs how a geometry candidate at any licensed layer `L` may add
one more licensed unit.

This document fixes the **termination law**: the predicate that
decides whether an `LGeometryCandidate(n)` is *minimally complete as
a candidate* inside its own layer — i.e., admissible as a finished
input for a strictly later, licensed layer — without ever being
promoted to meaning, ruling, or reality claim.

The two laws are *complementary*, not duplicative:

```text
Recursive Extension Contract   →   growth law      :  Extend(...)
Minimal Complete Closure       →   termination law :  IsMinimallyComplete(...)
```

A `length = n` geometry candidate is **not** automatically complete
merely by virtue of having `n` units. It is complete only when it
satisfies the eight conditions of §3. Completion never grants
membership in a later layer; it only certifies readiness for
*consideration* by the next licensed layer's own consumption
contract.

This document does **not**:

- implement `SlotGeometryQiyas` or any closure-checking adapter,
- introduce a new kernel primitive,
- introduce a new rank, gate, or claim prefix,
- define `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`,
  `RealityClaim`, or `FinalCaseJudgment`,
- modify any file under `src/qiyas_core/`,
  `tests/qiyas_core/`, `experimental/`, or `run_qiyas.py`,
- modify any other constitutional document.

---

## 1. The Principle

For any licensed layer `L` of the Qiyas algebra and any geometry
candidate produced by that layer, define a predicate
`IsMinimallyComplete : LGeometryCandidate → Bool` such that:

```text
IsMinimallyComplete(G) := True
  iff
    G satisfies all eight conditions of §3.
```

A `Seed(LCandidate₁)` (the `n = 1` degenerate case from §1 of the
recursive extension contract) **may** be minimally complete on its
own if and only if its single licensed beginning is *also* a
licensed ending under the layer's closure rule. Otherwise the layer
must extend before closure is admissible.

`IsMinimallyComplete` returns `True` or `False`. It does **not**
return meaning, ruling, or reality. It does not modify `G`; it only
classifies `G`.

A `G` for which `IsMinimallyComplete(G) == False` is a perfectly
licensed `LGeometryCandidate` — it simply remains a *non-terminal*
candidate, ready for further `Extend` steps within `L`.

A `G` for which `IsMinimallyComplete(G) == True` is a *terminal-by-
candidacy* geometry candidate inside `L`. Its only effect is to
become a licensed consumable for the strictly next layer's own
admission contract — never more.

```
Closure does not produce knowledge.
Closure produces readiness.
```

```
الإغلاق لا يُنتج معرفة.
الإغلاق يُنتج جاهزية.
```

---

## 2. Relationship to the Recursive Extension Contract

`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` answers:

```text
How does an LGeometryCandidate(n) become an LGeometryCandidate(n+1)?
```

This document answers:

```text
Given an LGeometryCandidate(n), may it stop growing inside L and
be offered to a later licensed layer as a finished candidate?
```

The two laws compose without conflict:

| Question                          | Law                | Operator                |
| --------------------------------- | ------------------ | ----------------------- |
| How does the geometry grow?       | Recursive Extension | `Extend(...)`           |
| When may the geometry stop?       | Minimal Closure     | `IsMinimallyComplete(...)` |
| What does the next layer consume? | Both, jointly       | A closed-by-candidacy `G` |

`IsMinimallyComplete` re-checks the §7 invariants of the recursive
extension contract (identity preservation, trace separation, rank
meet, residual preservation, blocking-difference annihilation,
`CandidateOnly` safety, no skipped layers) and adds the
beginning/ending/open-demand conditions specific to closure. It is
therefore a **strict super-set** of those invariants — every closure
condition is at least as strict, never weaker.

---

## 3. The Eight Closure Conditions

A geometry candidate `G : LGeometryCandidate(n)` is *minimally
complete* iff **all eight** of the following hold simultaneously:

### 3.1 Licensed beginning

```text
G has a licensed beginning under L's beginning rule.
```

There exists a layer-specific *beginning licensing* under which the
first unit of `G` is admissible as a start. The witness is a claim
of the form `gate:beginning:licensed` (public name; canonical
grammar carries the corresponding `وادي:` prefix per
`TERMINOLOGY_MAP.md` §4) on the seed's binding evidence, and an
`effective_cause:` claim identifying the layer's beginning cause.

### 3.2 Licensed ending

```text
G has a licensed ending under L's ending rule.
```

There exists a layer-specific *ending licensing* under which the
last unit of `G` is admissible as a terminus. The witness is a claim
of the form `gate:ending:licensed` on the most recent `Extend`'s
binding evidence, and an `effective_cause:` claim identifying the
layer's ending cause. Note: a beginning rule and an ending rule may
coincide in degenerate single-unit closures (cf. the `Seed` case in
§1).

### 3.3 All internal bindings are licensed

```text
For every Extend step that produced G, the binding was licensed
under L's per-extend gate policy.
```

For every `Extend` invocation in `G`'s construction history (read
off the canonical trace), the binding evidence satisfied the
conjunctive six-gate predicate with explicit gate states:
`CAUSE established ∧ CONDITION satisfied ∧ OBSTACLE absent ∧ VALIDITY valid ∧ CORRUPTION absent ∧ NULLITY absent` and produced an accepted (not
blocked, not deferred) extension. This condition is not new; it is
the running invariant of §7 of the recursive extension contract,
re-checked at closure time so that no historically-deferred binding
is silently admitted.

### 3.4 No open demand remains

```text
G carries no open demand on any of its units.
```

An *open demand* on a geometry is any unsatisfied admissibility
obligation that the layer's own contract requires before the
geometry may be offered to a later layer. Examples (illustrative,
not exhaustive — each layer fixes its own demand catalogue):

- a slot layer geometry may demand that no carrier-binding is left
  with an unresolved `effective_cause:` claim,
- a word layer geometry may demand that every required agreement
  marker has been licensed by a syntactic binding,
- a sentence layer geometry may demand that every anaphoric link
  recognised by a discourse marker has been resolved within the
  geometry.

Whatever the layer's catalogue is, **every** entry in it must be
discharged for `IsMinimallyComplete` to return `True`. An open
demand is *not* a blocking difference (§3.5) — it is a candidate
that the layer has admitted but not yet completed; closure is the
predicate that refuses to admit such candidates as terminal.

### 3.5 No blocking difference is present

```text
G carries no blocking difference:* claim on any of its units or on
any of its construction-history evidence sets.
```

A *blocking difference* is any `difference:` claim
(canonical Arabic-rooted grammar: `فارق:`) that invalidates a unit,
a binding, or the overall geometry under the layer's
invalidating-difference list. Closure is forbidden whenever any such
claim is present anywhere in the geometry's witnessable trace. This
condition is the closure-time enforcement of CLAUDE.md §4
invariant 5.

### 3.6 Residuals are preserved

```text
G.residuals ⊇ the union of all residuals on G's seed, on every
extension, and on every binding evidence used in the construction
history.
```

Closure may not be claimed by hiding a residual. Any blocking or
deferring residual produced during the geometry's construction must
survive into `G.residuals`. The kernel's `defer:` prefix and any
residual produced by gate failure are explicitly within scope. This
condition is the closure-time enforcement of CLAUDE.md §4
invariant 7.

### 3.7 Rank remains above NO_EVIDENCE

```text
G.rank > NO_EVIDENCE.
```

Closure requires that `G` has at least *some* evidentiary support.
The canonical rank lattice
(`NO_EVIDENCE < FORMAL_STRUCTURE < ANALOGICAL < DIRECT_HEARING <
INDIVIDUAL_REPORT < MASS_TRANSMISSION`, per `TERMINOLOGY_MAP.md`
§2) is finite and totally ordered; `G.rank` is the meet of all
participating ranks per §8 of the recursive extension contract. If
that meet collapses to `NO_EVIDENCE` for any reason — a zero-rank
binding evidence, a zero-rank rule, a zero-rank input — closure is
forbidden. A `length = n` geometry candidate at `rank ==
NO_EVIDENCE` is well-formed as a geometry but is not closed; it
must either gather more evidence (raising the meet) or remain a
non-terminal candidate.

### 3.8 Output remains CandidateOnly

```text
G.output_flags ⊇ {CandidateOnly} and
G.output_flags ∩ {HukmCandidate, RealityClaim, FinalMeaning,
                  FinalCaseJudgment} = ∅.
```

Closure does not lift `CandidateOnly`. A closed-by-candidacy
geometry is still a candidate; it is *not* a verdict. The output
flag set is checked at closure time so that no `Extend` history
leaked a final-judgment flag onto `G`. This condition is the
closure-time enforcement of CLAUDE.md §4 invariant 9.

---

## 4. What "Open Demand" Is and Is Not

Condition §3.4 is the only condition in §3 whose contents are
*layer-specific*. The other seven are universal: they apply
verbatim at every licensed layer. §3.4 requires every layer that
ratifies its own consumption contract to also publish its
**Demand Catalogue**: the finite list of admissibility obligations
that must be discharged before closure is admissible.

A demand is:

- declared by the layer's own contract (not by this document),
- discharged by a layer-specific licensed step that records an
  `effective_cause:demand_discharged:verified` claim (or its
  canonical Arabic-rooted equivalent under `TERMINOLOGY_MAP.md` §4),
- visible on the geometry's trace as either an open or a discharged
  entry — never silently dropped.

A demand is **not**:

- a blocking difference (those are §3.5),
- a residual (those are §3.6),
- a rank deficiency (that is §3.7),
- a missing closure (that is the absence of §3.1 or §3.2, not
  §3.4).

A geometry with an open demand is well-formed but non-terminal.
Closure simply refuses to admit it as ready for the next layer.

---

## 5. Slot Layer Instance

At the slot layer, `IsMinimallyComplete` applies to
`SlotGeometryCandidate(n)` (recursive extension contract §2):

```text
IsMinimallyComplete(SlotGeometry) :=
    licensed beginning under SlotBeginningRule       (§3.1)
  ∧ licensed ending    under SlotEndingRule          (§3.2)
  ∧ all SlotBindingEvidence on construction history
    are accepted under the slot layer's gate policy   (§3.3)
  ∧ Demand Catalogue (slot layer) discharged          (§3.4)
  ∧ no blocking difference on any slot or binding     (§3.5)
  ∧ residuals preserved                               (§3.6)
  ∧ rank > NO_EVIDENCE                                (§3.7)
  ∧ output_flags ⊇ {CandidateOnly} and clean of finals (§3.8)
```

A closed-by-candidacy `SlotGeometryCandidate` is admissible as a
consumable for the *next strictly later layer* (e.g., the word
layer's own admission contract — once that contract is ratified).
It is **not** admissible as:

- a `DalalahCandidate`,
- a `WordCandidate`,
- a `FinalMeaning`,
- a `HukmCandidate`,
- a `RealityClaim`.

Closure of a `SlotGeometryCandidate` only answers:

```
Is this sequence of slots terminated, in this layer, as a complete
candidate ready to be considered by the next licensed layer?
```

```
هل هذه الخانات منتهية، في هذه الطبقة، بوصفها مرشحًا كاملًا جاهزًا
للعرض على الطبقة المرخّصة التالية؟
```

It does **not** answer whether the closed geometry carries an
independent verbal meaning. That question belongs to a strictly
later layer's own contract.

---

## 6. Word Layer Instance

At the word layer, `IsMinimallyComplete` applies to
`WordGeometryCandidate(n)`:

```text
IsMinimallyComplete(WordGeometry) :=
    licensed beginning under WordBeginningRule
  ∧ licensed ending    under WordEndingRule
  ∧ all WordBindingEvidence accepted
  ∧ Demand Catalogue (word layer) discharged
  ∧ no blocking difference
  ∧ residuals preserved
  ∧ rank > NO_EVIDENCE
  ∧ output_flags ⊇ {CandidateOnly} and clean of finals
```

A closed-by-candidacy `WordGeometryCandidate` is admissible
only as a consumable for the strictly later sentence layer's own
admission contract. It is **not** admissible as `FinalMeaning`,
`HukmCandidate`, `RealityClaim`, or `FinalCaseJudgment`.

`WordBindingEvidence ≠ SlotBindingEvidence` (recursive extension
contract §6); the same non-portability holds at closure time. Each
layer's beginning rule, ending rule, and Demand Catalogue are its
own.

---

## 7. Sentence Layer Instance

At the sentence layer, `IsMinimallyComplete` applies to
`DiscourseGeometryCandidate(n)`:

```text
IsMinimallyComplete(DiscourseGeometry) :=
    licensed beginning under DiscourseBeginningRule
  ∧ licensed ending    under DiscourseEndingRule
  ∧ all DiscourseBindingEvidence accepted
  ∧ Demand Catalogue (sentence layer) discharged
  ∧ no blocking difference
  ∧ residuals preserved
  ∧ rank > NO_EVIDENCE
  ∧ output_flags ⊇ {CandidateOnly} and clean of finals
```

Closure operates strictly in `DISCOURSE_CONTEXT`. A closed
`DiscourseGeometryCandidate` is admissible only as a consumable for
the strictly later paragraph layer's own admission contract.

---

## 8. Paragraph Layer Instance

At the paragraph layer, `IsMinimallyComplete` applies to
`TextGeometryCandidate(n)`:

```text
IsMinimallyComplete(TextGeometry) :=
    licensed beginning under TextBeginningRule
  ∧ licensed ending    under TextEndingRule
  ∧ all TextBindingEvidence accepted
  ∧ Demand Catalogue (paragraph layer) discharged
  ∧ no blocking difference
  ∧ residuals preserved
  ∧ rank > NO_EVIDENCE
  ∧ output_flags ⊇ {CandidateOnly} and clean of finals
```

Closure operates strictly in `DISCOURSE_CONTEXT`. A closed
`TextGeometryCandidate` is admissible only as a consumable for
whatever strictly later layer the constitution later ratifies above
it. It is **not** admissible as `FinalMeaning`, `HukmCandidate`,
`RealityClaim`, or `FinalCaseJudgment`.

---

## 9. What Closure Does NOT Produce

`IsMinimallyComplete` never produces:

```text
DalalahCandidate
FinalMeaning
HukmCandidate
RealityClaim
FinalCaseJudgment
```

It also never produces, by side effect:

- a rank promotion (rank is fixed by the meet, per §8 of the
  recursive extension contract),
- an `output_flag` set lift (closure may not drop `CandidateOnly`
  or add any final-judgment flag),
- a residual deletion (closure may not silently drop residuals),
- a new identity, trace, or evidence claim (closure is a predicate,
  not a producer).

A closure check is *observation*, not *construction*. It does not
add to `G`; it classifies `G` as terminal-by-candidacy or
non-terminal.

---

## 10. What Closure DOES Produce — Readiness, Not Meaning

The single positive effect of closure is to certify:

```text
G is admissible as a consumable by the strictly next licensed
layer's own admission contract.
```

```text
G مرشّح كامل، جاهز لأن تنظر فيه الطبقة المرخّصة التالية وفق عقد
استهلاكها الخاص.
```

This admissibility is **conditional**: the next layer's contract
still owns the admission decision, and *that* contract may impose
further conditions beyond §3 — e.g., the SlotGeometry alignment-
trace contract (§11 below) imposes, on top of closure, additional
checks on `SlotCandidate`s consumed by `SlotGeometryQiyas`.

Closure therefore produces *readiness* but never *promotion*.
Crossing into the next layer is the responsibility of that layer's
own contract, not of this document.

---

## 11. Forbidden Jumps from Closure

The following jumps are constitutional violations at every layer
and must be rejected by every future implementation contract:

```text
IsMinimallyComplete(G) == True   ↛   DalalahCandidate
IsMinimallyComplete(G) == True   ↛   FinalMeaning
IsMinimallyComplete(G) == True   ↛   HukmCandidate
IsMinimallyComplete(G) == True   ↛   RealityClaim
IsMinimallyComplete(G) == True   ↛   FinalCaseJudgment

SlotGeometryCandidate closed       ↛   DalalahCandidate
SentenceGeometryCandidate closed   ↛   HukmCandidate
DiscourseGeometryCandidate closed  ↛   RealityClaim
TextGeometryCandidate closed       ↛   FinalCaseJudgment
```

In full:

```text
A closed geometry candidate is still CandidateOnly.
A closed geometry candidate is not meaning, ruling, or reality.
Closure produces readiness, never knowledge.
```

This list extends, not replaces, the forbidden-jumps list in §11 of
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`. Both lists are
binding simultaneously.

---

## 12. Relationship to the Upcoming SlotGeometry Alignment-Trace Contract

This contract **does not** implement `SlotGeometryQiyas`. It only
fixes the closure predicate that any future `SlotGeometryQiyas`
must obey *in addition to* the consumption contract reserved by
§12 of `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`.

Concretely: the upcoming SlotGeometry alignment-trace contract
(forthcoming, docs-only) must, at minimum, state that
`SlotGeometryQiyas`:

- consumes only `SlotCandidate*` (recursive extension contract §12),
- accepts each consumed `SlotCandidate` only if the alignment-trace
  conditions of that contract are met (recursive extension contract
  §12),
- admits a `SlotGeometryCandidate` as terminal only if
  `IsMinimallyComplete` is `True` under §3 of *this* document,
- does **not** produce `DalalahCandidate`, `FinalMeaning`,
  `HukmCandidate`, `RealityClaim`, or `FinalCaseJudgment` (§9 of
  this document and §11 of the recursive extension contract).

This forward declaration is binding on the upcoming SlotGeometry
alignment-trace contract PR. It is not implemented here.

---

## 13. Relationship to Higher Layers

This contract does **not** define:

- `DalalahCandidate`,
- `FinalMeaning`,
- `HukmCandidate`,
- `RealityClaim`,
- `FinalCaseJudgment`.

It only fixes the closure predicate that any future
geometry-producing layer must obey. When higher layers are
eventually contracted and implemented, they will inherit both this
predicate and the recursive extension growth law unweakened: a
geometry candidate from a lower layer is admissible to a higher
layer only as a *closed-by-candidacy* candidate, never as a
shortcut to meaning, ruling, or reality.

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the closure predicate it fixes is binding on
  every future geometry-producing PR;
- **pre-implementation** — no `IsMinimallyComplete` implementation,
  no demand-catalogue implementation, no `SlotBeginningRule` /
  `SlotEndingRule` adapter exists at the time of merge;
- **layer-agnostic** — the predicate applies uniformly at the slot,
  word, sentence, and paragraph layers (and at any later layer of
  the same shape).

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes a closure-checking adapter,
- any future PR that proposes a `BeginningRule` / `EndingRule` for a
  geometry-producing layer,
- any future PR that proposes a `Demand Catalogue` for a
  geometry-producing layer,
- any future review that asks whether a proposed geometry candidate
  is admissible as a finished consumable for a strictly later layer.

It supersedes nothing prior; it composes with — and is
strictly tighter than — the §7 invariants of
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`, by adding the
beginning, ending, open-demand, and rank-positivity conditions
specific to closure.

It does **not** authorise the implementation of any of the layers
or rules it describes. Each must be ratified by its own docs-only
contract PR before any implementation PR may be opened.

---

## 16. Glossary

| Term                          | Meaning |
| ----------------------------- | --- |
| minimal complete closure      | The termination law fixed in §1, with the eight conditions of §3. |
| `IsMinimallyComplete`         | The predicate `LGeometryCandidate → Bool` of §1. Observation only; not a producer. |
| licensed beginning            | The condition of §3.1: the seed unit is admissible under a layer-specific beginning rule. |
| licensed ending               | The condition of §3.2: the last extension's terminus is admissible under a layer-specific ending rule. |
| open demand                   | An unsatisfied admissibility obligation in the layer's own Demand Catalogue (§3.4). Not a residual, not a blocking difference. |
| Demand Catalogue              | The finite, layer-specific list of admissibility obligations a geometry must discharge before closure (§4). Layer-published. |
| closed-by-candidacy           | The state of an `LGeometryCandidate` for which `IsMinimallyComplete` returns `True`. Still `CandidateOnly`. |
| readiness                     | The single positive effect of closure (§10): admissibility as a consumable for the strictly next licensed layer. Not promotion. |
| terminal-by-candidacy         | Synonym for *closed-by-candidacy* — a closed geometry candidate is terminal *as a candidate*, not as a verdict. |
| `SlotBeginningRule` / `SlotEndingRule` | Reserved public names for the slot layer's beginning and ending rules in a future contract; not current implementation symbols. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
