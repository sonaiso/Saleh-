# ARABIC_VARIANT_RESOLUTION_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> **Arabic Variant Resolution Evidence** runtime shape. No code, no
> tests, no implementation are changed by this PR.
>
> **Authority basis:**
> `CLAUDE.md` §0 / §3 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `RESET_CONSTITUTION.md` §1 / §3 / §4,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C),
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §6 / §7 / §11 / §12,
> `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3 / §9 / §11 / §12,
> `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §1 / §6 / §9 / §11,
> `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` §2 / §3 / §4.2 /
> §7 / §13.3,
> `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` §2 / §3 /
> §6.1 / §10,
> `PR_SCHEDULING_POLICY.md` §1.1 / §5 / §8,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4,
> the existing data registry
> `src/qiyas_core/data/arabic_articulation_registry.json`.
>
> **Governing one-liners:**
>
> ```
> Variant resolution is evidence, not a candidate.
> Variant resolution removes ambiguity; it does not grant admission.
> Variant resolution is layer-specific and not portable.
> ```
>
> ```
> حلّ الـvariant دليل، لا مرشّح.
> ويُزيل الالتباس فقط، لا يمنح القبول.
> ويخصّ طبقته، ولا يُنقل إلى غيرها.
> ```

---

## 0. Phase Status — Settled

Phases 1, 2 Batch 1, the closure-evidence runtime, the MIU readiness
contract, and the MIU readiness implementation are **complete on
`main`**. The end-to-end chain operates:

```text
raw text
  → SequenceContextTokenizer
  → SlotCandidate                         (Phase 1)
  → SlotGeometryCandidate                 (Phase 2 Batch 1)
  → MinimalCompleteClosureEvidence | None (closure check; PR #73)
  → MinimalUnitReadinessCandidate         (MIU readiness; PR #75)
       ACCEPTED | BLOCKED | DEFERRED
```

The MIU readiness layer **defers** when the
`ArabicArticulationRegistry`'s `get_primary_articulation(symbol)`
returns `None` because of multi-variant symbols (`و` and `ي` each
carry `madd` + `non_madd`). The defer is constitutionally correct
under `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` §4.2 / §7 /
§13.3, but it leaves a real-world utility gap: the system can
neither admit `وَ` as a minimal independent unit nor explain why
not in operationally useful terms.

This contract fixes the **runtime shape** of the disambiguation
evidence that any future variant resolver must produce — the same
constitutional pattern the closure-evidence runtime contract
established for closure (PR #72). It does **not** implement a
resolver; it only fixes what any future implementation must satisfy
*before* an implementation PR may be opened.

Three non-negotiable statements bind this PR's scope:

```text
The phases above are settled.
This PR fixes the runtime shape of ArabicVariantResolutionEvidence —
nothing more, nothing less.
Variant resolution is NOT readiness. Variant resolution is NOT
meaning, لفظ, dalalah, hukm, or reality.
```

This document does **not** modify any source file or test, does
**not** modify `run_qiyas.py`, the `ArabicArticulationRegistry`,
`slot_geometry_adapter.py`, `slot_geometry_rules.py`,
`slot_geometry_closure_check.py`, `minimal_unit_readiness_adapter.py`,
`minimal_unit_readiness_rules.py`, or `experimental/`, and does
**not** amend any existing constitutional document.

---

## 1. The Principle

`ArabicVariantResolutionEvidence` answers exactly one question, and
refuses to answer any other:

```text
Question (admissible):
  For a SlotGeometryCandidate(length = 1) whose symbol carries
  multiple ArabicArticulationRegistry variants, which variant
  (e.g. "madd" or "non_madd") is licensed for THIS slot, under the
  context already preserved in the geometry's trace/identity?

Questions (inadmissible — strictly later concerns):
  Is this unit eligible as a minimal independent functional unit?
  What does this unit mean?
  Does this unit discharge a لفظ?
  Does this unit licence a Dalalah?
  Does this unit licence a Hukm?
  Does this unit licence a RealityClaim?
```

The output is **not** admission, **not** meaning, **not** a لفظ,
**not** a dalalah, **not** a hukm. It is a typed evidence carrier
that says: "for this specific slot, the licensed variant is `X`
(with provenance)" — and nothing more.

```text
Variant resolution is evidence, not a candidate.
Variant resolution removes ambiguity; it does not grant admission.
```

```text
حلّ الـvariant دليل، لا مرشّح.
ويُزيل الالتباس فقط، لا يمنح القبول.
```

---

## 2. Constitutional Decision — Evidence Carrier, Not Candidate

The single load-bearing decision this contract fixes is:

```text
ArabicVariantResolutionEvidence is an Evidence carrier
(an immutable, layer-specific, runtime-typed record).

ArabicVariantResolutionEvidence is NOT a Candidate.
```

### 2.1 Why an Evidence carrier

Variant resolution is **proof about an existing slot**, not the
production of a new textual entity. The `SlotGeometryCandidate(length
= 1)` already exists and is already licensed (Phase 2 Batch 1 §3 / §6).
The question "which variant applies for this slot?" yields a typed
answer with structured witnesses; it does **not** yield a new
candidate type, a new identity, or any algebraic transition.

Asking the kernel to treat variant resolution as a `Candidate` would
inflate the candidate namespace with a type that:

- carries no new identity beyond the slot's,
- carries no new layer beyond the slot's,
- carries no new linguistic content,
- carries only a typed variant label plus its provenance.

By construction, that is the shape of an `Evidence` carrier, not a
`Candidate`. The closure-evidence runtime contract (PR #72) set this
precedent for closure; the same shape applies here for variant
resolution.

### 2.2 What "Evidence carrier" means in this codebase

The same definition fixed by `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md`
§2.2 applies here verbatim. An Evidence carrier is:

1. constructed by a deterministic producer (per §3),
2. an immutable, frozen runtime record,
3. consumed by a downstream layer's request as auditable input,
4. **not** itself a `qiyas_core.candidate.Candidate`,
5. **not** itself a `qiyas_core.evidence.Evidence` (the kernel's
   claim-set primitive; the variant-resolution carrier is one
   structured layer above it).

### 2.3 What this decision rules out

- **Not a `Candidate` subclass.** No `candidate_type ==
  "ArabicVariantResolutionCandidate"` is reserved by this contract;
  the name `ArabicVariantResolutionCandidate` is **forbidden** by §8.
- **Not produced by a `QiyasRule`.** Variant resolution is not the
  output of any `output_candidate_type` declaration.
- **Not licensed by the six-gate predicate.** The gates
  (`CAUSE / CONDITION / OBSTACLE / VALIDITY / CORRUPTION / NULLITY`)
  apply to *rules* that consume evidence; the carrier itself is the
  input, not a kernel-licensed transition.
- **Not a Qiyas layer producing a Candidate.** Even if a future
  amendment introduces a Qiyas-shaped wrapper for ergonomics, the
  **output** of that wrapper must remain an Evidence carrier (or
  `None`), not a `Candidate` of any type. The non-binding note in
  §3.1 about a Qiyas-shaped alternative is subordinate to this
  rule.

---

## 3. Who Produces `ArabicVariantResolutionEvidence`?

A deterministic producer reads context preserved on a single
`SlotGeometryCandidate(length = 1)`, consults the registry's
multi-variant entries for the slot's symbol, and either returns a
fully-populated `ArabicVariantResolutionEvidence` (when the context
is sufficient to select one variant) or returns `None` (when the
context is insufficient — i.e., when ambiguity persists).

### 3.1 Reserved producer name

```text
ArabicVariantResolver           — reserved public name for the
                                    deterministic checker that
                                    evaluates variant evidence for a
                                    SlotGeometryCandidate and returns
                                    an ArabicVariantResolutionEvidence
                                    or None. Mirrors the
                                    SlotGeometryClosureCheck pattern
                                    (closure-evidence runtime
                                    contract §3).
```

`ArabicVariantResolver` is the **sole reserved producer name** under
this contract. It is **reserved-by-name only**; not implemented at
the time of this document's ratification.

#### Non-binding note on a Qiyas-shaped alternative

An earlier draft of this contract reserved a parallel name
`ArabicVariantResolutionQiyas` for a Qiyas-shaped wrapper. That
alternative is constitutionally awkward (a "Qiyas" producer whose
output is an Evidence carrier, not a `Candidate`, breaks the Qiyas
pattern's symmetry) and is **explicitly not reserved** by this
contract. If a strictly later constitutional amendment introduces a
Qiyas-shaped wrapper for ergonomic reasons, that amendment must
itself ratify the wrapper's name and re-affirm the §2.3 discipline
(the wrapper's output remains an Evidence carrier). The name
`ArabicVariantResolutionQiyas` is mentioned here only to record
that the alternative was considered and not adopted; it carries no
forward-binding force.

The reserved future module path is:

```text
src/qiyas_core/arabic_variant_resolver.py
  — reserved public path; not implemented. A future implementation
    contract may pick a different module path if it provides a
    justification; the reserved names of §3.1 are binding regardless.
```

### 3.2 The producer's discipline

The producer must satisfy:

```text
Input    : SlotGeometryCandidate(length = 1)
           + optional context drawn ONLY from already-preserved
             trace/identity on that geometry (per §4)
Output   : ArabicVariantResolutionEvidence  (variant selected with
                                              provenance)
         | None                              (insufficient context;
                                              ambiguity persists)

Observation only. The producer does not modify the input geometry.
The producer does not produce a Candidate. The producer is not a
QiyasRule (even if wrapped in a Qiyas-shaped adapter — see §2.3).
The producer does not invoke QiyasKernel.apply.

Construction is deterministic: given the same SlotGeometryCandidate
and the same registry state, the producer returns either the same
evidence (modulo nondeterministic identifiers like uuid) or None —
never one and then the other.
```

### 3.3 What the producer does NOT do

- **Does not modify the input geometry.** Observation only.
- **Does not produce a Candidate.** The `Candidate` namespace is
  unaffected.
- **Does not invoke `QiyasKernel.apply`.** No rule fires, no
  candidate set returns.
- **Does not re-read raw text.** All context comes from
  already-preserved trace/identity (per §4).
- **Does not re-tokenise.** The producer does not consult the
  `SequenceContextTokenizer` directly.
- **Does not call back into the closure-check or the MIU readiness
  adapter.** Variant resolution is layer-specific.
- **Does not consult higher-layer typed units.** No
  `WordCandidate` / `LafzCandidate` / `SentenceCandidate` /
  `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` /
  `RealityClaim` / `MinimalUnitReadinessCandidate` consumption.

---

## 4. Closed Consumption Surface

`ArabicVariantResolver` consumes exactly the following — and **only**
the following:

```text
admissible inputs:

  1. SlotGeometryCandidate(length = 1)
       — the single-slot geometry whose symbol the resolver is
         disambiguating.

  2. ArabicArticulationRegistry metadata
       — consulted read-only via the existing reader's public API
         (get_articulations_by_symbol / get_primary_articulation /
         load_arabic_articulation_registry); metadata only, no
         licensing claim.

  3. Local haraka/function context, drawn EXCLUSIVELY from
     already-preserved trace/identity on the consumed
     SlotGeometryCandidate (and, transitively, from the
     SlotCandidate's trace/identity that the geometry already
     preserves).
       — the haraka's identity (e.g. identity:codepoint:064E for
         fatha), the position type (INITIAL / MEDIAL / FINAL /
         ISOLATED — read from trace), and the carrier-binding
         witness (the slot's :alignment_ref: trace entry).

  4. Previous/next slot context, IF AND ONLY IF the previous/next
     SlotCandidate(s) live in the same SlotGeometry-construction
     history or the same INTRA_UTTERANCE tokenizer segment.
       — read via the geometry's preserved trace/identity; the
         resolver does NOT re-read the source text or re-tokenise.
       — for length=1 geometries this is the practical limit:
         neighbouring context must be supplied through the
         consumed geometry's trace/identity. The resolver does NOT
         independently fetch neighbours.
```

It must **not** directly consume any of the following:

```text
raw text
SequenceContextTokenizer markers (consumed directly)
UnicodeCandidate (consumed directly)
TypedCodePoint (consumed directly)
LetterIdentityCarrier (consumed directly)
HarakaFunctionCarrier (consumed directly)
PositionCarrier (consumed directly)
CarrierBindingCandidate (consumed directly)
ConditionedTypedSequence outputs (consumed directly)
SlotCandidate (consumed directly — must come via SlotGeometry)
SlotGeometryCandidate(length > 1)
MinimalCompleteClosureEvidence (orthogonal axis; not consumed here)
MinimalUnitReadinessCandidate
WordCandidate
LafzCandidate
SentenceCandidate
ParagraphCandidate
DalalahCandidate
FinalMeaning
HukmCandidate
RealityClaim
FinalCaseJudgment
```

In particular: the resolver does **not** consume
`SlotGeometryCandidate(length > 1)`. Multi-slot geometries are
outside this contract's scope; their variant questions, if any,
belong to strictly later (word- / sentence-) layers under their own
contracts.

The phrase "context preserved on the consumed geometry" means
exactly what `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §6.1 fixed
on the slot-geometry output: `identity_ids` carrying codepoint
identities, `trace_ids` carrying `:alignment_ref:` and the position
breadcrumbs, etc. The resolver reads these and nothing else.

---

## 5. Scope — Which Symbols

This contract fixes the variant-evidence shape for the symbols that
the existing `ArabicArticulationRegistry` reader reports as
multi-variant. As of the current registry state, that set is:

```text
in scope (current registry):
  و    — variants: {madd, non_madd}
  ي    — variants: {madd, non_madd}
```

For both `و` and `ي`, the registry's
`get_primary_articulation(symbol)` returns `None` because two
entries match (e.g. `jawf_waw_madd` and `lips_waw_non_madd` for `و`).
The MIU readiness layer correctly defers in this case. The resolver
exists to *attempt* to disambiguate, but **only** under the
restricted consumption surface of §4.

```text
future extensibility — NOT in scope of this PR:
  ا    — alif and any orthographic / functional variants future
         contracts may introduce. This contract NAMES alif as a
         possible future addition for clarity, but does NOT define
         its variant semantics. Any future variant-resolution
         coverage of alif requires its own constitutional
         amendment.

  (any other future symbol whose registry entry the project later
   amends to carry multiple variants).
```

The principle is clear: variant resolution is bounded by the
registry's own ambiguity declarations. If the registry resolves to
a single primary entry (as it does for `ب / ف / ك / ل / س / أ / ت`),
the resolver does **not** apply — no resolution evidence is needed
or produced, and the MIU readiness layer admits or rejects per its
existing predicate without consulting the resolver at all.

This contract does **not** define `ا`-specific variant semantics,
does **not** introduce new registry variants, and does **not**
amend the registry's `core_independent_letters` or
`contextual_or_bound_markers` lists.

---

## 6. The Evidence Carrier's Runtime Shape

`ArabicVariantResolutionEvidence` is a frozen, immutable runtime
record. Its field layout is fixed by this contract; future
implementation PRs may add audit metadata but must NOT remove
fields and must NOT add Candidate-shape fields (`candidate_type`,
`status`, `output_flags`).

### 6.1 Required fields

```text
symbol                   : str
    The Arabic letter symbol being disambiguated (e.g. "و", "ي").

selected_variant         : str
    The variant label chosen by the resolver. Reserved labels:
        "madd"      — the madd (vocalised-extension) variant
        "non_madd"  — the non-madd (consonantal / particle) variant
    Future contracts may extend the label set when ratifying new
    symbol coverage. This contract does NOT introduce additional
    labels. Implementation MUST validate the label against the
    registry's entry ids (e.g. lips_waw_non_madd vs
    jawf_waw_madd) — the resolver does not invent labels.

selected_entry_id        : str
    The ArabicArticulationEntry.id whose semantics the resolver
    selected (e.g. "lips_waw_non_madd"). This is the audit anchor
    back into the registry; a downstream consumer that needs the
    full registry entry calls
    get_articulation_by_id(selected_entry_id).

selection_basis          : tuple[str, ...]
    A tuple of zero or more BASIS-LABEL strings encoding which
    contextual witnesses drove the selection. Reserved basis labels:
        "haraka_function_before"     — the previous haraka licensed
                                         the non_madd reading
        "haraka_function_self"       — the slot's own haraka licensed
                                         the non_madd reading
        "haraka_function_after"      — the next haraka licensed the
                                         non_madd reading
        "preceding_letter_identity"  — the previous letter's identity
                                         disambiguated
        "following_letter_identity"  — the next letter's identity
                                         disambiguated
        "registry_default"           — the registry default applied
                                         (only when the registry
                                         itself carries a default
                                         field; not introduced here)
        "intra_utterance_position"   — the slot's INITIAL/MEDIAL/
                                         FINAL/ISOLATED position
                                         resolved the ambiguity
    Future implementation contracts may extend this label set when
    new context channels are ratified. This contract reserves only
    the labels above.

geometry_candidate_id    : str
    The consumed SlotGeometryCandidate's candidate_id (audit
    anchor).

geometry_layer           : str
    Fixed to "SlotGeometryQiyas" — the resolver operates on
    slot-geometry layer output.

geometry_length          : int
    Fixed to 1 — the resolver consumes only length=1 geometries.

geometry_construction_mode : str
    Fixed to "seed" — by length-1 implication.

geometry_identity_ids    : tuple[str, ...]
    The consumed geometry's identity_ids, preserved verbatim
    (NEVER rewritten, reordered, or downcast).

geometry_trace_ids       : tuple[str, ...]
    The consumed geometry's trace_ids, preserved verbatim.

evidence_id              : str
    Per-evidence unique identifier (uuid-style); never an identity.

audit_trace_ids          : tuple[str, ...]
    Auditable trace strings the resolver emits, per §6.2 schema.
    Disjoint from any identity field.
```

The carrier is constructed **only** when:

```text
selected_variant is non-empty,
selected_entry_id is non-empty and refers to a real registry entry,
selection_basis is non-empty (at least one BASIS-LABEL),
geometry_candidate_id, geometry_layer, geometry_length,
  geometry_construction_mode are all preserved correctly,
geometry_identity_ids and geometry_trace_ids are non-empty and
  preserved verbatim,
identity / trace separation invariant holds:
  set(geometry_identity_ids) ∩ set(audit_trace_ids) == ∅.
```

If any condition above is unmet, the resolver returns `None` rather
than building a half-true carrier.

### 6.2 Recommended `audit_trace_ids` schema (non-binding)

To mirror the closure-evidence runtime contract §6.1 pattern, this
contract **recommends** — but does **not** bind — the following
schema for the strings emitted into `audit_trace_ids`:

```text
trace:arabic_variant_resolution:symbol:<symbol>
trace:arabic_variant_resolution:selected_variant:<variant>
trace:arabic_variant_resolution:selected_entry_id:<entry_id>
trace:arabic_variant_resolution:basis:<basis-label>            (one per basis)
trace:arabic_variant_resolution:geometry_id:<geometry_candidate_id>
```

For an `evidence-built` outcome, the above six (or more, with one
trace per basis) appear in `audit_trace_ids`. For a `None` outcome,
the producer emits parallel `:no_variant_resolved:reason:<reason>`
strings on its own audit log (not on the carrier — there is no
carrier in the `None` case). The schema is **non-binding**; an
implementation contract may pick a different format if it preserves
reviewer legibility.

---

## 7. Failure Mode — Absence ≠ BLOCK

The producer's return type is two-valued:

```text
ArabicVariantResolutionEvidence  (when context resolves to a single
                                   variant with documented basis)
None                             (when context is insufficient OR
                                   not in scope OR not multi-variant)
```

When the producer returns `None`, the MIU readiness layer's
existing behaviour is preserved verbatim:

```text
MIU readiness reads:
  "no ArabicVariantResolutionEvidence supplied"
    → variant_ambiguity persists
    → defer:variant_ambiguity:present is emitted
    → kernel records deferred_variant_ambiguity residual
    → MinimalUnitReadinessCandidate is DEFERRED (not BLOCKED)
```

The constitutional invariant:

```text
Absence of variant resolution is NEVER a BLOCK at the readiness
layer. Absence is a DEFER.
```

Conversely, presence of variant resolution does **not** by itself
authorise admission:

```text
Presence of variant resolution removes the variant_ambiguity reason
for deferral, but ALL other MIU readiness conditions still apply:

  * SlotGeometryCandidate(length = 1) and construction_mode = "seed"
  * MinimalCompleteClosureEvidence present and complete
  * ArabicArticulationRegistry metadata for the resolved variant's
    entry must itself satisfy
    can_function_as_minimal_independent_unit == True
  * every CLAUDE.md §4 invariant of the readiness layer

If the resolved variant is "madd", and the registry's madd entry
has can_function_as_minimal_independent_unit == False, the MIU
readiness layer BLOCKS — not because of variant_ambiguity (which
has been resolved) but because of the underlying eligibility
predicate.
```

So:

```text
Resolution evidence  ⇏  MIU admission.
Resolution evidence  ⇏  meaning, لفظ, dalalah, hukm, reality.
Resolution evidence's role is narrow: remove the variant_ambiguity
defer reason from a single slot's readiness evaluation.
```

This is the same "necessary but not sufficient" pattern
`MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` §7 / §10
already fixed for closure evidence; the variant-resolution carrier
inherits the discipline.

---

## 8. Forbidden Outputs

`ArabicVariantResolver` (and any future Qiyas-shaped wrapper a
later constitutional amendment may introduce — see the non-binding
note in §3.1) must **never** produce — neither as its return value
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

ArabicVariantResolutionCandidate
                            (the carrier is Evidence, not a Candidate
                             — §2 of this contract)

MinimalCompleteClosureCandidate
                            (forbidden by the closure-evidence
                             runtime contract §8; reasserted here)

MinimalIndependentMeaningCandidate
                            (forbidden by MIU readiness §5 / §8;
                             reasserted here)

SlotCandidate
SlotGeometryCandidate
                            (the producer observes; it does not
                             produce candidates of any kind, not even
                             the candidate types it observes)
```

The single admissible *output* of `ArabicVariantResolver` is the
two-valued return:

```text
ArabicVariantResolutionEvidence  (when context resolves)
None                              (when context does not resolve)
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
re-tokenise raw text,
modify slot_geometry_adapter.py, slot_geometry_rules.py,
  slot_geometry_closure_check.py, minimal_unit_readiness_adapter.py,
  minimal_unit_readiness_rules.py, arabic_articulation_registry.py,
  or any other adapter/rule/registry.
```

---

## 9. Layer Specificity and Portability

`ArabicVariantResolutionEvidence` is **specifically** the
variant-resolution witness for a single
`SlotGeometryCandidate(length = 1)` at the `SlotGeometryQiyas` layer.

### 9.1 Layer-specific

The carrier's `geometry_layer` field is fixed to
`"SlotGeometryQiyas"`. The carrier's `geometry_length` is fixed to
`1`. The variant labels and basis labels are specific to single-slot
Arabic letter disambiguation.

### 9.2 Not portable upward

A `ArabicVariantResolutionEvidence` produced for one
`SlotGeometryCandidate(length = 1)` **must not** be reused as
variant evidence for any higher-layer typed unit. Higher layers
(word, sentence, paragraph) will, if they have variant-like
questions, need their own typed evidence types under their own
contracts. This non-portability mirrors `SlotBindingEvidence` and
the closure-evidence runtime contract's §9 discipline.

### 9.3 Not portable laterally

A `ArabicVariantResolutionEvidence` for symbol `و` must not be
reused as variant evidence for `ي`. The carrier records its
`symbol` and `selected_entry_id` for exactly this reason: each
carrier is bound to one slot, one symbol, one registry entry.
Sharing across slots is a forbidden side effect (§8.1).

---

## 10. Relationship to `MinimalUnitReadinessCandidate`

The variant-resolution carrier is consumed by the MIU readiness
layer as an **optional fourth witness**, added to the three already
fixed by `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` §2:

```text
Admit(S, M, E, V?) := True
  iff
    S (SlotGeometryCandidate(length = 1)) satisfies §4.1 conditions,
    M (registry metadata) satisfies §4.2 conditions
       — OR the registry returns variant ambiguity AND V is supplied
         AND V resolves the ambiguity to an eligible variant,
    E (MinimalCompleteClosureEvidence) is present and well-formed,
    every §6 invariant of the MIU contract holds.
```

### 10.1 The four cases (with and without V)

| Registry says | V supplied? | MIU outcome |
|---|---|---|
| single eligible variant | n/a | ACCEPTED (V irrelevant; never consulted) |
| single ineligible variant | n/a | BLOCKED (V irrelevant; never consulted) |
| multi-variant + variant_ambiguity | no | DEFERRED (per current MIU §4.2 / §7) |
| multi-variant + variant_ambiguity | yes, resolves to eligible variant | ACCEPTED subject to all other §6 invariants |
| multi-variant + variant_ambiguity | yes, resolves to ineligible variant | BLOCKED (eligibility check on the resolved variant) |
| multi-variant + variant_ambiguity | yes, returns `None` | DEFERRED (resolver failed; ambiguity persists) |

### 10.2 Non-identities

```text
ArabicVariantResolutionEvidence  ≠  MinimalUnitReadinessCandidate
ArabicVariantResolutionEvidence  ≠  Candidate (of any type)
ArabicVariantResolutionEvidence  ≠  MinimalCompleteClosureEvidence
                                     (orthogonal axis: closure asks
                                      "is the geometry closed?";
                                      resolution asks "which variant
                                      applies?")
ArabicVariantResolutionEvidence  ≠  meaning
ArabicVariantResolutionEvidence  ≠  word
ArabicVariantResolutionEvidence  ≠  lafz
ArabicVariantResolutionEvidence  ≠  dalalah
ArabicVariantResolutionEvidence  ≠  hukm
ArabicVariantResolutionEvidence  ≠  reality
```

### 10.3 The MIU layer's consumption discipline

When (and only when) the MIU layer encounters
`get_primary_articulation(symbol) == None`, it MAY consult an
`ArabicVariantResolutionEvidence` supplied by the caller. The MIU
layer does **not** independently invoke the resolver — the resolver
is, in implementation terms, a separate observation step driven by
the caller / pipeline. This mirrors the closure-evidence runtime
contract's eager-vs-lazy stance (§3 of that contract): the
implementation is free to compute eagerly or lazily; the contract
fixes the shape of what is consumed.

If the resolver evidence is present and admits an eligible variant,
the MIU layer's adapter:

1. records the resolved variant on its evidence chain (audit-only,
   never as identity);
2. proceeds with admission as if the registry had returned a single
   primary entry for the resolved variant;
3. enforces the remaining §6 invariants verbatim.

If the resolver evidence is absent or `None`, the MIU layer's
adapter:

1. emits `defer:variant_ambiguity:present` (existing behaviour);
2. records that no resolver evidence was supplied (audit only);
3. produces a DEFERRED `MinimalUnitReadinessCandidate` per
   `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` §13.3.

A future implementation PR for the MIU adapter's resolver-aware
admission path is **out of scope** for this contract; it must come
under its own controlling contract / PR.

---

## 11. Worked Examples

### 11.1 `وَ` — currently DEFERRED; resolution removes ambiguity (subject to eligibility)

```text
Phase 1 / Phase 2 / Closure / MIU readiness:
                      → MinimalUnitReadinessCandidate DEFERRED
                        residual: deferred_variant_ambiguity

With ArabicVariantResolutionEvidence supplied where:
    symbol = "و"
    selected_variant = "non_madd"
    selected_entry_id = "lips_waw_non_madd"
    selection_basis = ("haraka_function_self",)
    geometry_candidate_id = (the وَ geometry id)
  →
    Registry's lips_waw_non_madd:
        can_function_as_minimal_independent_unit == True
    MIU readiness re-evaluates:
        all other §6 invariants hold
        → MinimalUnitReadinessCandidate ACCEPTED

With ArabicVariantResolutionEvidence supplied where:
    selected_variant = "madd"
    selected_entry_id = "jawf_waw_madd"
  →
    Registry's jawf_waw_madd:
        can_function_as_minimal_independent_unit == False
    MIU readiness:
        eligibility predicate FAILS on the resolved variant
        → MinimalUnitReadinessCandidate BLOCKED

With ArabicVariantResolutionEvidence absent (resolver returned None):
  →
    Existing MIU behaviour is preserved:
        DEFERRED with deferred_variant_ambiguity.
```

In none of these cases does the variant-resolution carrier produce
meaning, لفظ, dalalah, hukm, reality, or any higher-layer typed
unit. The carrier resolves a typed ambiguity and stops.

### 11.2 `بِ` — no variant ambiguity, no resolver involvement

```text
Phase 1 / Phase 2 / Closure / MIU readiness:
                      → MinimalUnitReadinessCandidate ACCEPTED.

The registry returns a single entry (lips_ba) for "ب" with
can_function_as_minimal_independent_unit == True. No variant
ambiguity. The resolver is NOT invoked — and even if it were
invoked, it would return None (the symbol is single-variant, hence
out of scope per §5).
```

### 11.3 `يَ` — same shape as `وَ`, eligibility depends on resolved variant

```text
Default behaviour (no resolver):
                      → DEFERRED (variant_ambiguity).

With ArabicVariantResolutionEvidence supplied where:
    symbol = "ي"
    selected_variant = "non_madd"
    selected_entry_id = "tongue_ya_non_madd"
  →
    Registry's tongue_ya_non_madd:
        can_function_as_minimal_independent_unit == True
        (per the current registry entry for the non-madd ya)
    MIU readiness re-evaluates → ACCEPTED.

With selected_variant = "madd"
  →
    Registry's jawf_ya_madd:
        can_function_as_minimal_independent_unit == False
    MIU readiness → BLOCKED.
```

The constitutional discipline mirrors §11.1 exactly: resolution
narrows the registry to one variant, then the eligibility predicate
runs on that variant. Resolution does not bypass the predicate.

### 11.4 `ا` — future extensibility note only

This contract names `ا` as a possible future symbol whose variant
semantics a later constitutional amendment may introduce. It does
**not** define `ا`-specific variant labels, basis labels, or entry
ids here. Any future variant-resolution coverage of `ا` requires
its own constitutional amendment PR (which would specify, at
minimum, the variant label set and the registry's corresponding
entry ids). Until then, `ا` is out of scope of any
`ArabicVariantResolutionEvidence` produced under this contract.

The current registry entry for `ا` (`jawf_alif_madd`) is
single-entry with `can_function_as_minimal_independent_unit ==
False`, so `ا`-headed slots are BLOCKED at the MIU layer by the
existing eligibility predicate — independent of any variant
resolution. This pre-existing behaviour is preserved verbatim.

---

## 12. Forbidden Jumps

The following jumps are constitutional violations and must be
rejected by the gate policy of any future implementation contract:

```text
SlotGeometryCandidate                    →  ArabicVariantResolutionCandidate
                                            (forbidden — §2: variant
                                             resolution is Evidence,
                                             not a Candidate)

ArabicVariantResolutionEvidence          →  MinimalUnitReadinessCandidate
                                            (resolution evidence does
                                             not produce readiness;
                                             readiness applies its own
                                             admission predicate)

ArabicVariantResolutionEvidence          →  WordCandidate
ArabicVariantResolutionEvidence          →  LafzCandidate
ArabicVariantResolutionEvidence          →  SentenceCandidate
ArabicVariantResolutionEvidence          →  ParagraphCandidate
ArabicVariantResolutionEvidence          →  DalalahCandidate
ArabicVariantResolutionEvidence          →  FinalMeaning
ArabicVariantResolutionEvidence          →  HukmCandidate
ArabicVariantResolutionEvidence          →  RealityClaim
ArabicVariantResolutionEvidence          →  FinalCaseJudgment
ArabicVariantResolutionEvidence          →  SlotCandidate
ArabicVariantResolutionEvidence          →  SlotGeometryCandidate
                                            (resolution evidence
                                             licenses no growth,
                                             no extension, no new
                                             candidate of any kind)

raw text                                 →  ArabicVariantResolutionEvidence
SequenceContextTokenizer markers         →  ArabicVariantResolutionEvidence
UnicodeCandidate                         →  ArabicVariantResolutionEvidence
TypedCodePoint                           →  ArabicVariantResolutionEvidence
LetterIdentityCarrier                    →  ArabicVariantResolutionEvidence
HarakaFunctionCarrier                    →  ArabicVariantResolutionEvidence
PositionCarrier                          →  ArabicVariantResolutionEvidence
CarrierBindingCandidate                  →  ArabicVariantResolutionEvidence
ConditionedTypedSequence outputs         →  ArabicVariantResolutionEvidence
SlotCandidate                            →  ArabicVariantResolutionEvidence
                                            (resolution evidence is
                                             produced ONLY from a
                                             SlotGeometryCandidate)

SlotGeometryCandidate(length > 1)        →  ArabicVariantResolutionEvidence
                                            (resolver scope is
                                             length = 1 only — §4 / §5)

ArabicArticulationRegistry entry alone   →  ArabicVariantResolutionEvidence
ArabicArticulationRegistry alone         →  variant resolution
                                            (registry is metadata only
                                             and licenses no transition)

MinimalCompleteClosureEvidence           →  ArabicVariantResolutionEvidence
                                            (orthogonal axis; closure
                                             does not produce
                                             resolution)
```

In full:

```text
A variant resolution carrier is Evidence, not a Candidate.
It does not produce admission.
It does not produce meaning, لفظ, dalalah, hukm, reality, or any
higher-layer typed unit.
Its scope is single-slot, length-1, multi-variant symbols only.
Its inputs are restricted to the consumed geometry and its already-
preserved context.
```

This list extends — does not replace — the forbidden-jump lists in
§11 of the recursive-extension contract, §11 of the closure
contract, §11 of the slot-geometry alignment-trace contract, §12 of
the MIU readiness contract, and §11 of the closure-evidence runtime
contract. All six lists are binding simultaneously.

---

## 13. The 12 Answered Questions — Summary Table

For the convenience of any reviewer or future contract reader, this
section restates the contract's answers to the twelve questions
asked at the start of the maintainer's brief.

| # | Question | Answer (this contract) |
| - | --- | --- |
| 1 | What is `ArabicVariantResolutionEvidence`? | An immutable runtime carrier that records, for a single `SlotGeometryCandidate(length = 1)` whose symbol carries multiple registry variants, which variant is licensed and by what basis. Observation, not construction. |
| 2 | Is it a `Candidate` or an Evidence carrier only? | **Evidence carrier.** `ArabicVariantResolutionCandidate` is explicitly forbidden by name (§8). |
| 3 | Who produces it later? | A deterministic checker, reserved by the sole binding name `ArabicVariantResolver` (§3.1). Not implemented in this PR. A Qiyas-shaped wrapper was considered and explicitly NOT reserved; if a later amendment introduces one, its output must still be an Evidence carrier (§2.3). |
| 4 | Does it resolve `و` / `ي` / `ا`? | `و` and `ي` are in scope by default (single-letter, multi-variant per current registry). `ا` is named as a future extensibility note only; this PR does not define alif's variant semantics. |
| 5 | What is the difference between `madd` and `non_madd`? | Reserved variant labels (§6.1). `madd` denotes the vocalised-extension variant (e.g. `jawf_waw_madd`, `jawf_ya_madd`); `non_madd` denotes the consonantal / particle variant (e.g. `lips_waw_non_madd`, `tongue_ya_non_madd`). The labels are anchored to the registry's entry ids and must not be invented by the resolver. |
| 6 | Can `وَ` be admitted as a minimal unit if `non_madd` is proven? | **Subject to all other MIU conditions.** A `non_madd` resolution **removes** the `variant_ambiguity` defer reason. The MIU layer then re-evaluates the eligibility predicate on the resolved variant (`lips_waw_non_madd`); per the current registry that variant's `can_function_as_minimal_independent_unit == True`, so MIU may ACCEPT — provided every §6 MIU invariant also holds. Resolution alone is **not** admission. |
| 7 | Does `وَ` remain DEFERRED if no variant evidence is supplied? | **Yes.** Absence of `ArabicVariantResolutionEvidence` preserves the existing MIU readiness behaviour: `defer:variant_ambiguity:present` is emitted, the kernel records `deferred_variant_ambiguity`, and the candidate is DEFERRED. Absence never escalates to BLOCK (§7). |
| 8 | How does MIU readiness consume this evidence later? | When `get_primary_articulation(symbol) == None` AND a supplied `ArabicVariantResolutionEvidence` resolves the ambiguity, MIU re-evaluates the eligibility predicate on the resolved variant's registry entry, then admits / blocks accordingly. When the evidence is absent, MIU defers as today (§10.3). |
| 9 | Forbidden outputs? | Twelve type names listed in §8 (`HukmCandidate`, `RealityClaim`, `FinalMeaning`, `FinalCaseJudgment`, `DalalahCandidate`, `WordCandidate`, `LafzCandidate`, `SentenceCandidate`, `ParagraphCandidate`, `DiscourseGeometryCandidate`, `TextGeometryCandidate`, `MinimalUnitReadinessCandidate`, `ArabicVariantResolutionCandidate`, `MinimalCompleteClosureCandidate`, `MinimalIndependentMeaningCandidate`, `SlotCandidate`, `SlotGeometryCandidate`). The two-valued return shape (`ArabicVariantResolutionEvidence \| None`) is binding. |
| 10 | Non-goals? | Section §16 — no code, no test, no rule, no candidate, no kernel call, no registry amendment, no MIU implementation amendment, no `ا`-specific variant semantics, no claim that resolution = admission, no claim that resolution = meaning. |
| 11 | Failure mode — absence ⇒ DEFERRED, not BLOCKED? | **Yes.** Constitutional invariant §7: "Absence of variant resolution is NEVER a BLOCK at the readiness layer. Absence is a DEFER." A failed resolution attempt (resolver returns `None`) is treated identically to "no resolver attempt was made". |
| 12 | Does resolution evidence equal readiness? | **No.** Resolution evidence is necessary-but-not-sufficient for admission of an otherwise-ambiguous symbol. The MIU eligibility predicate runs on the resolved variant's registry entry; resolution does not bypass it. §7 and §10 fix this discipline. |

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the runtime shape it fixes is binding on
  every future variant-resolution implementation PR;
- **pre-implementation** — `ArabicVariantResolutionEvidence` as a
  runtime type, `ArabicVariantResolver` as the sole reserved
  producer name, the module
  `src/qiyas_core/arabic_variant_resolver.py`, and the MIU
  readiness layer's resolver-aware admission path are all
  reserved-by-name only; none is implemented at the time of merge;
- **slot-geometry-layer-strict** — the shape applies *only* to
  `SlotGeometryCandidate(length = 1)`; multi-slot geometries are
  outside scope by construction.

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes an `ArabicVariantResolutionEvidence`
  runtime type;
- any future PR that proposes an `ArabicVariantResolver` producer
  (or, by way of a separate constitutional amendment, a Qiyas-shaped
  wrapper — see the non-binding note in §3.1);
- any future PR that proposes a resolver-aware admission path in
  the MIU readiness layer's adapter or rule;
- any future PR that proposes to inline variant resolution into the
  MIU readiness layer (which this contract forbids by §4 / §10
  reasoning);
- any future PR that proposes a higher-layer variant-resolution
  evidence type (which this contract sets the precedent for but
  does not define);
- any future review that asks whether a proposed variant-resolution
  consumption is licensed.

It supersedes nothing prior; it fixes the runtime shape that the
MIU readiness contract reserved as a strictly later concern (per
its §4.2 / §7 / §13.3 deferral discipline), and it composes with —
does not amend — `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`
or any earlier contract.

It does **not** authorise the implementation of
`ArabicVariantResolutionEvidence`, `ArabicVariantResolver`, the
module at the reserved path, the MIU readiness layer's
resolver-aware admission path, or any consumer. Each must continue to be ratified by its own contract PR
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
- modify the `ArabicArticulationRegistry` (CSV source, JSON
  artifact, reader module),
- modify `src/qiyas_core/slot_geometry_adapter.py`,
  `src/qiyas_core/rules/slot_geometry_rules.py`,
  `src/qiyas_core/slot_geometry_closure_check.py`,
  `src/qiyas_core/minimal_unit_readiness_adapter.py`, or
  `src/qiyas_core/rules/minimal_unit_readiness_rules.py`,
- implement `ArabicVariantResolutionEvidence` as a runtime type,
- implement `ArabicVariantResolver`,
- create the module
  `src/qiyas_core/arabic_variant_resolver.py`,
- amend the MIU readiness layer's adapter or rule to consume
  variant resolution evidence,
- introduce any new CI check, hook, bot, or automation,
- define `WordLayerVariantResolutionEvidence`,
  `SentenceLayerVariantResolutionEvidence`, or any generic
  / parametric variant-resolution base type,
- define `ا`-specific variant labels or basis labels,
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
  `MinimalUnitReadinessCandidate`,
  `ArabicVariantResolutionCandidate`,
  `MinimalCompleteClosureCandidate`, or
  `MinimalIndependentMeaningCandidate`,
- claim that variant resolution is equivalent to MIU admission,
- claim that variant resolution licenses any algebraic transition
  by itself,
- authorise the implementation of any consumer, runtime, adapter,
  kernel surface, or test.

---

## 17. Glossary

| Term | Meaning |
| --- | --- |
| `ArabicVariantResolutionEvidence` | The slot-geometry-layer variant-resolution Evidence carrier (§1). Frozen, immutable. Carries the selected variant label, the registry entry id, the selection basis, and audit metadata. **Not** a `Candidate`. **Not** the kernel's `Evidence` primitive. |
| `ArabicVariantResolver` | Reserved public name for the deterministic producer of `ArabicVariantResolutionEvidence` (§3.1). Not a Qiyas layer. Not a rule. Does not invoke `QiyasKernel.apply`. Reserved-by-name only; not implemented at the time of this document. |
| `ArabicVariantResolutionQiyas` | Non-binding mention in §3.1 only; **not reserved** by this contract. A Qiyas-shaped wrapper was considered and explicitly not adopted because its asymmetry (Qiyas-shape producing Evidence, not a Candidate) breaks the Qiyas pattern. If a later constitutional amendment introduces such a wrapper, the amendment itself must ratify the name and re-affirm §2.3. |
| `src/qiyas_core/arabic_variant_resolver.py` | Reserved future module path for the producer (§3). Reserved-by-name only; not implemented. |
| `madd` | Reserved variant label (§6.1). Denotes the vocalised-extension variant. Anchored to the registry's `*_madd` entry ids. |
| `non_madd` | Reserved variant label (§6.1). Denotes the consonantal / particle variant. Anchored to the registry's `*_non_madd` entry ids. |
| `selection_basis` | Tuple of one or more reserved basis labels recording which contextual witnesses drove the resolver's selection (§6.1). |
| Evidence carrier | An immutable, frozen runtime record that carries typed witnesses about an existing candidate, consumed by a downstream layer's request. Distinct from both `Candidate` and the kernel's `Evidence` primitive. Same definition as the closure-evidence runtime contract §2.2. |
| variant ambiguity | The condition in which `get_primary_articulation(symbol)` returns `None` because the registry has multiple matching entries for the symbol. The MIU readiness layer DEFERS in this case; the resolver, if invoked and successful, removes the deferral reason. |
| necessary-but-not-sufficient | The variant-resolution / admission relationship (§7 / §10). Resolution removes a defer reason; it does not by itself license admission. |
| layer-specific (variant resolution) | The non-portability discipline (§9). Slot-geometry variant resolution is not reusable for word/sentence/paragraph layers. Higher layers define their own. |
| failure mode (absence ⇒ DEFER) | The constitutional invariant of §7. Absence of variant resolution is NEVER a BLOCK at the readiness layer; it preserves the existing DEFER behaviour. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
