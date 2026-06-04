# ARABIC_VARIANT_SELECTION_RULES_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> *selection-rule admissibility predicates* that any future
> `ArabicVariantResolver` must satisfy when emitting an
> `ArabicVariantResolutionEvidence` (PR #78). No code, no tests, no
> registry change, no runtime, no implementation are changed by this
> PR.
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
> `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §1 / §2 / §3.1 / §4 / §5 /
> §6.1 / §7 / §10 / §12,
> `PR_SCHEDULING_POLICY.md` §1.1 / §5 / §8,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4,
> the existing data registry
> `src/qiyas_core/data/arabic_articulation_registry.json`.
>
> **Governing one-liners:**
>
> ```
> Selection rules license; they do not coerce.
> Selection rules do not produce candidates.
> Selection rules do not produce meaning.
> Selection rules do not equate to MIU acceptance.
> Absence of a licensed basis is DEFER, never BLOCK.
> ```
>
> ```
> قواعد الاختيار ترخّص، ولا تُلزم.
> ولا تنتج مرشّحًا، ولا معنى.
> ولا تساوي قبول MIU.
> وغياب الأساس المرخّص تأجيلٌ، لا منعٌ.
> ```

---

## 0. Phase Status — Settled

Phases 1, 2 Batch 1, the closure-evidence runtime, the closure check
implementation, the MIU readiness contract, the MIU readiness
implementation, and the **Arabic Variant Resolution Contract**
(PR #78) are all **complete on `main`**. The end-to-end chain
operates:

```text
raw text
  → SequenceContextTokenizer
  → SlotCandidate                         (Phase 1)
  → SlotGeometryCandidate                 (Phase 2 Batch 1)
  → MinimalCompleteClosureEvidence | None (closure check; PR #73)
  → MinimalUnitReadinessCandidate         (MIU readiness; PR #75)
       ACCEPTED | BLOCKED | DEFERRED
                ⇡
                ArabicVariantResolutionEvidence | None
                (runtime shape ratified in PR #78;
                 NOT yet implemented;
                 selection rules ratified by THIS PR)
```

The variant-resolution contract (PR #78) fixed:

- the **runtime shape** of `ArabicVariantResolutionEvidence` (Evidence
  carrier, never a `Candidate`),
- the **sole reserved producer name** (`ArabicVariantResolver`),
- the **closed consumption surface** (`SlotGeometryCandidate(length =
  1)` + registry metadata + local context drawn ONLY from preserved
  trace / identity),
- the **scope** (`و` and `ي` in this PR; `ا` future extensibility),
- the **failure-mode discipline** (absence ⇒ DEFER, never BLOCK),
- the **necessary-but-not-sufficient** relationship to MIU admission,
- the **seven reserved `selection_basis` labels**.

It deliberately **did NOT** specify which `selection_basis` label
licenses which variant for which symbol. That decision was
explicitly deferred to a strictly later contract — **this one**.

This document **only** fixes the admissibility predicates: which
`(symbol, variant, basis)` tuples a future `ArabicVariantResolver`
implementation may emit. It does **not** authorise implementation
of any runtime, any resolver, any registry change, any MIU adapter
amendment, any test, or any Candidate-producing layer.

Three non-negotiable statements bind this PR's scope:

```text
The contract from PR #78 is settled.
This PR fixes the selection-rule admissibility predicates — nothing
more, nothing less.
Selection rules license; they do not coerce. They do not produce
candidates. They do not produce meaning, لفظ, dalalah, hukm, or
reality.
```

This document does **not** modify any source file or test, does
**not** modify `run_qiyas.py`, the `ArabicArticulationRegistry`,
`slot_geometry_adapter.py`, `slot_geometry_rules.py`,
`slot_geometry_closure_check.py`, `minimal_unit_readiness_adapter.py`,
`minimal_unit_readiness_rules.py`, or `experimental/`, and does
**not** amend any existing constitutional document.

---

## 1. The Principle

Selection rules are **admissibility predicates**, not algorithms.

This contract fixes, for each `(symbol, variant)` pair within scope,
the **subset of `selection_basis` labels** that a future
`ArabicVariantResolver` **may** use to license the resolution.

It does **not** fix:

- which basis the resolver should try first,
- whether the resolver should try multiple bases and combine them,
- how the resolver should weigh conflicting bases,
- whether the resolver should defer when only a "weak" basis applies,
- the precise lexical / phonological conditions under which a given
  basis evaluates to True for a given input (that is elementary
  Arabic, codified in the registry's entries; this contract works at
  the layer above).

These remain implementation-level decisions, fixed by a strictly
later implementation contract under `PR_SCHEDULING_POLICY.md` §1.3.

Constitutionally, every selection rule below is of the form:

```text
For symbol S and variant V, basis B is admissible iff:
  B is one of the seven reserved labels in §3 of this contract;
  B's witness — read EXCLUSIVELY from the consumed
  SlotGeometryCandidate's preserved trace / identity, per the
  consumption-surface closure of variant-resolution contract §4 —
  is documented in a future implementation contract as constitutive
  evidence for V on S.
```

The contract's claim is therefore narrow:

```text
The following (symbol, variant, basis) tuples are CONSTITUTIONALLY
LICENSABLE. The contract does NOT claim that every implementation
MUST license them. It only claims that NO implementation MAY
license tuples OUTSIDE this list.
```

---

## 2. Constitutional Decision — Admissibility, Not Algorithm

The single load-bearing decision this contract fixes is:

```text
This contract enumerates admissible (symbol, variant, basis) tuples.
This contract does NOT enumerate selection algorithms.
```

### 2.1 Why admissibility, not algorithm

Implementation algorithms evolve. A future resolver may add a
confidence threshold, a basis-priority ordering, a multi-basis
combinator, or a debate framework over witnesses. Each of those
choices is reversible at the implementation layer without
constitutional cost — *provided the underlying admissibility
predicate is fixed*. By constitutionalising only the admissibility
predicate, this contract:

- locks the *space of licensable resolutions* (no implementation may
  emit a resolution outside this space),
- frees the *selection algorithm* (any implementation strategy that
  stays within the space is constitutionally licit),
- preserves the closure-evidence runtime contract §2.2 Evidence-
  carrier discipline (the carrier's `selection_basis` field is bound
  by the admissible label set, but the *order* and *weighting* of
  bases are implementation choices).

### 2.2 What this decision rules out

- **Not an enumeration of selection algorithms.** Future
  implementation contracts pick algorithms; this contract picks the
  legal space they may operate in.
- **Not a confidence model.** This contract has no concept of
  probability, weighting, or threshold. Admissibility is a Boolean
  predicate.
- **Not a registry amendment.** The registry's entries continue to
  declare what the variants ARE (e.g., `lips_waw_non_madd`,
  `jawf_waw_madd`); this contract declares which bases MAY license
  the resolver's selection of one such entry.
- **Not a candidate-producing layer.** No `Candidate` is emitted by
  any selection rule. No `MinimalUnitReadinessCandidate`,
  `WordCandidate`, `DalalahCandidate`, `FinalMeaning`,
  `HukmCandidate`, `RealityClaim`, `FinalCaseJudgment`, or
  higher-layer type is produced or proposed for production.

---

## 3. The Seven Reserved `selection_basis` Labels

This contract uses **only** the seven `selection_basis` labels
reserved by `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §6.1 — no
extensions. Restated for convenience:

```text
haraka_function_before     the previous slot's haraka licensed the
                             resolution
haraka_function_self       the slot's own haraka licensed the
                             resolution
haraka_function_after      the next slot's haraka licensed the
                             resolution
preceding_letter_identity  the previous letter's identity
                             disambiguated
following_letter_identity  the next letter's identity disambiguated
registry_default           a registry-level default applied (the
                             registry would need a future
                             `default_variant` field; not amended
                             here — reserved-but-unavailable)
intra_utterance_position   the slot's INITIAL / MEDIAL / FINAL /
                             ISOLATED position resolved the
                             ambiguity
```

A future amendment may extend this label set; **no rule below
introduces a new label**.

Three operational facts about the labels, fixed by PR #78 §4 and
carried verbatim here:

1. **Local-only.** Every basis reads its witness **EXCLUSIVELY**
   from the consumed `SlotGeometryCandidate`'s preserved trace /
   identity. The resolver does NOT re-read raw text, re-tokenise, or
   cross tokenizer segments. The previous/next slot context is
   admissible **only if** the geometry's trace/identity already
   preserves it (e.g., via a sibling-slot trace entry written by the
   slot-composition pipeline; how that trace gets there is a
   strictly later concern).
2. **`registry_default` is currently unavailable.** The current
   `ArabicArticulationRegistry` carries no per-symbol
   `default_variant` field. This contract does NOT amend the
   registry. The `registry_default` basis is reserved-by-name but
   **may not** be used by any rule below until a strictly later
   Data Registry PR amends the registry to carry a default field.
3. **No basis licenses madd from a bare symbol.** This is the
   constitutional consequence of "local-only + length-1": for a
   length-1 `SlotGeometryCandidate` with no preceding-slot context
   in its preserved trace, no `haraka_function_before` /
   `preceding_letter_identity` witness exists. The slot remains
   DEFERRED. This is constitutionally correct (absence ⇒ DEFER,
   per PR #78 §7) and is restated explicitly in §4 and §5 below.

---

## 4. Variant Selection Rules for `و`

### 4.1 و non_madd — admissible bases

```text
(symbol = "و", variant = "non_madd") MAY be licensed by ANY of:

  haraka_function_self
      The slot's own haraka witness is constitutive evidence that
      the و carries an active haraka (and is therefore consonantal /
      particle), not a sukun-bearing madd extension. This is the
      canonical Arabic discipline: the madd reading requires the
      letter to be SUKUN-bearing; an active haraka rules out madd.

  intra_utterance_position
      The slot's geometric position witness (per
      SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md §4 — ISOLATED /
      INITIAL / MEDIAL / FINAL) is constitutive evidence for the
      non_madd reading WHEN the position itself disambiguates
      (e.g., an ISOLATED waw with its own haraka in a single-segment
      utterance has no preceding letter to "follow with madd" and
      no following haraka context that could license madd). This
      basis is secondary: it does NOT license non_madd by itself;
      it CAN license non_madd in conjunction with haraka_function_self
      (the implementation may combine — but is not required to).
```

The four other reserved labels (`haraka_function_before`,
`haraka_function_after`, `preceding_letter_identity`,
`following_letter_identity`) are **NOT admissible** for
`(symbol = "و", variant = "non_madd")` in this contract. They are
reserved by PR #78 §6.1 but are not licensed for this
`(symbol, variant)` pair by this contract. A strictly later
amendment may add them.

`registry_default` is reserved-but-unavailable for this
`(symbol, variant)` pair (per §3 fact 2).

### 4.2 و madd — admissible bases

```text
(symbol = "و", variant = "madd") MAY be licensed ONLY by:

  haraka_function_before
      The preceding slot's haraka witness is constitutive evidence
      for the madd reading IFF the preceding letter's haraka is the
      "matching" haraka for waw-madd (canonically: damma on the
      preceding letter, combined with a sukun-bearing waw). The
      precise haraka-matching condition is documented in the
      registry's `jawf_waw_madd` entry and in elementary Arabic;
      this contract does NOT restate it.
```

The six other reserved labels are **NOT admissible** for
`(symbol = "و", variant = "madd")` in this contract.

In particular: `haraka_function_self` is **NOT admissible** for madd
on `و`. The madd reading on `و` requires the letter to be sukun-bearing;
an active self-haraka rules out madd. A resolver that emits
`(symbol = "و", variant = "madd", selection_basis = ("haraka_function_self",))`
is in violation of this contract and must be rejected at review.

`registry_default` is reserved-but-unavailable.

### 4.3 و — what this contract does NOT specify

This contract does **not** specify:

- which specific haraka values (fatha / damma / kasra / shadda /
  tanwin) trigger `haraka_function_self`-licensed non_madd (the
  registry's entry semantics + elementary Arabic suffice);
- which specific preceding-letter haraka triggers
  `haraka_function_before`-licensed madd beyond the canonical
  damma-matching pattern;
- which `intra_utterance_position` values constitute "ISOLATED-
  enough" for the secondary `intra_utterance_position` basis;
- the implementation's policy when both `haraka_function_self` and
  `intra_utterance_position` witnesses are available (combine?
  prefer one?);
- the implementation's policy when `haraka_function_self` is
  available but the resolver chooses to defer anyway (conservative
  threshold);
- whether the registry should later be amended to carry a
  `default_variant` field for `و`.

All five questions are strictly later concerns.

### 4.4 Bare و standalone — DEFERRED

When the consumed `SlotGeometryCandidate(length = 1)` for `و`
carries:

- no `haraka_function_self` witness (the slot has no haraka — but
  this is structurally impossible for a Phase-1 SlotCandidate, which
  by §2.1 of the slot-composition rule requires a haraka pillar),
  **and**
- no `haraka_function_before` witness (no preceding-slot context
  preserved on the geometry's trace),

then no licensed basis exists, and the resolver returns `None`
per PR #78 §7. The MIU readiness layer continues to DEFER with
`deferred_variant_ambiguity` — exactly as it does today.

This is the constitutional default: **bare و with no licensed
basis is DEFERRED, not BLOCKED**.

The first case (no `haraka_function_self`) cannot arise from a
real Phase-1 slot — the slot composition rule requires a haraka.
It is recorded for completeness only.

---

## 5. Variant Selection Rules for `ي`

### 5.1 ي non_madd — admissible bases

```text
(symbol = "ي", variant = "non_madd") MAY be licensed by ANY of:

  haraka_function_self
      The slot's own haraka witness is constitutive evidence that
      the ي carries an active haraka and is therefore consonantal
      (per registry entry tongue_ya_non_madd), not a sukun-bearing
      madd extension.

  intra_utterance_position
      Secondary basis with the same discipline as §4.1: licenses
      non_madd ONLY in conjunction with haraka_function_self.
```

The four other reserved labels (`haraka_function_before`,
`haraka_function_after`, `preceding_letter_identity`,
`following_letter_identity`) are **NOT admissible**.

`registry_default` is reserved-but-unavailable.

### 5.2 ي madd — admissible bases

```text
(symbol = "ي", variant = "madd") MAY be licensed ONLY by:

  haraka_function_before
      The preceding slot's haraka witness is constitutive evidence
      for the madd reading IFF the preceding letter's haraka is the
      "matching" haraka for ya-madd (canonically: kasra on the
      preceding letter, combined with a sukun-bearing ya). The
      precise haraka-matching condition is documented in the
      registry's `jawf_ya_madd` entry and in elementary Arabic;
      this contract does NOT restate it.
```

The six other reserved labels are **NOT admissible**.

In particular: `haraka_function_self` is **NOT admissible** for madd
on `ي`, by the same reasoning as §4.2.

`registry_default` is reserved-but-unavailable.

### 5.3 ي — what this contract does NOT specify

The same list as §4.3 applies, with `ي` substituted for `و` and
`jawf_ya_madd` / `tongue_ya_non_madd` substituted for the
corresponding waw entries.

### 5.4 Bare ي standalone — DEFERRED

When the consumed `SlotGeometryCandidate(length = 1)` for `ي`
carries no licensed basis, the resolver returns `None` and the MIU
readiness layer continues to DEFER. **Bare ي with no licensed basis
is DEFERRED, not BLOCKED.**

The constitutional discipline mirrors §4.4 verbatim.

---

## 6. `ا` — Future Extensibility Only

This contract names `ا` as a possible future symbol whose variant
semantics a later constitutional amendment may introduce. It does
**not** define `ا`-specific variant labels, admissible bases, registry
entry ids, or selection rules here.

Specifically, this contract makes **no claim** about:

- whether `ا` should be treated as a multi-variant symbol;
- whether orthographic / functional / hamza-seat / writing-function
  distinctions are constitutional concerns of the variant resolver;
- whether the current single registry entry for `ا`
  (`jawf_alif_madd`) should be split into multiple entries;
- which `selection_basis` labels (if any) would license such a
  split.

All four questions are explicitly **open questions** for a strictly
later constitutional amendment. Until such an amendment merges,
`ا`-headed slots remain at the existing MIU readiness behaviour:
single registry entry, `can_function_as_minimal_independent_unit ==
False`, BLOCKED at the MIU eligibility predicate independent of any
variant resolution. This pre-existing behaviour is preserved
verbatim.

The reserved producer `ArabicVariantResolver` MUST return `None`
for any `ا`-headed slot under this contract, since no
`(symbol = "ا", variant, basis)` tuple is admissible. A resolver that
emits `ArabicVariantResolutionEvidence` for `ا` is in violation of
this contract.

---

## 7. Conflict and Absence Behavior

This section fixes the constitutional behavior for five enumerated
edge cases.

### 7.1 Evidence pointing to a non-existent registry variant

```text
Case:
  The resolver-emitted ArabicVariantResolutionEvidence carries a
  selected_variant or selected_entry_id that does NOT match any
  ArabicArticulationEntry returned by get_articulation_by_id.

Rule:
  The evidence is INVALID and must be DISCARDED by the consumer
  (the future MIU adapter amendment). Discarded evidence behaves
  identically to ABSENT evidence.

  The MIU readiness layer continues to DEFER with
  deferred_variant_ambiguity. No BLOCK is recorded for the
  malformed evidence; the absence-⇒-DEFER discipline from PR #78
  §7 is preserved.
```

### 7.2 No licensed basis available

```text
Case:
  None of the bases admissible for (symbol, variant) per §§4–5
  has a witness on the consumed geometry's preserved trace /
  identity. The resolver cannot license any variant.

Rule:
  The resolver returns None. The MIU readiness layer DEFERS.
  No BLOCK. No silent guess.
```

### 7.3 Evidence contradicts registry metadata

```text
Case:
  The resolver-emitted evidence selects a variant (e.g., "madd"),
  but the registry's entry for that variant
  (e.g., jawf_waw_madd.can_function_as_minimal_independent_unit)
  combined with the readiness layer's eligibility predicate would
  produce a BLOCK.

Rule:
  This is NOT a contradiction; it is a valid downstream consequence.
  The resolver's role is to identify the variant. The MIU
  readiness layer's role is to apply the eligibility predicate on
  the resolved variant. A "madd" resolution that leads to a MIU
  BLOCK is constitutionally correct (per PR #78 §7 / §10.1).

  In particular: a valid madd resolution for وَ or يَ MAY cause
  MIU BLOCK ONLY because the resolved registry entry's
  can_function_as_minimal_independent_unit == False. The BLOCK is
  the eligibility predicate firing — not a contradiction.
```

### 7.4 Multiple bases give conflicting results

```text
Case:
  Two or more admissible bases (per §§4–5) have witnesses on the
  consumed geometry, but they license DIFFERENT variants (e.g.,
  haraka_function_self → non_madd; haraka_function_before → madd).

Rule:
  This contract does NOT specify a tie-breaking algorithm. The
  resolver MAY:

    (a) return None (treat the conflict as ambiguity);
    (b) follow a strictly-later implementation contract that
        specifies a deterministic tie-breaking algorithm.

  This contract REQUIRES that:

    (a) the resolver MUST NOT silently emit a "majority vote" or
        any heuristic combinator without a strictly later
        constitutional amendment that ratifies the combinator;
    (b) the default (in the absence of a ratified combinator) is
        None;
    (c) None is treated by the MIU readiness layer as ABSENT
        evidence (DEFER, not BLOCK).

  This is the constitutional default: CONFLICT ⇒ DEFER.
```

### 7.5 Evidence carries an invalid trace

```text
Case:
  The resolver-emitted ArabicVariantResolutionEvidence carries:

    - selection_basis labels NOT in the seven reserved set (§3), OR
    - audit_trace_ids that VIOLATE the §6.2 schema of PR #78, OR
    - identity_ids that intersect trace_ids
      (identity/trace separation violation), OR
    - geometry_candidate_id / geometry_layer / geometry_length
      values that contradict the consumed geometry.

Rule:
  The evidence is INVALID and must be DISCARDED. Discarded evidence
  behaves identically to ABSENT evidence. The MIU readiness layer
  DEFERS. No BLOCK.

  This is the constitutional default: MALFORMED ⇒ DISCARD ⇒ DEFER.
```

### 7.6 Summary of the absence / conflict / malformed regime

| Resolver outcome | MIU effect | Rationale |
|---|---|---|
| Valid `ArabicVariantResolutionEvidence` resolving non_madd | `variant_ambiguity` removed; MIU re-evaluates eligibility on the resolved entry | PR #78 §7 / §10.1 |
| Valid `ArabicVariantResolutionEvidence` resolving madd | `variant_ambiguity` removed; MIU eligibility predicate fires on madd entry → BLOCK | PR #78 §7 / §10.1 |
| `None` (no licensed basis) | DEFER (`deferred_variant_ambiguity` preserved) | PR #78 §7 |
| `None` (conflict between bases) | DEFER | §7.4 |
| Invalid evidence (variant / entry / trace malformed) | DISCARD, then DEFER | §7.1, §7.5 |

The universal constitutional invariant:

```text
Absence of LICENSED, VALID variant resolution at the readiness
layer is ALWAYS a DEFER, NEVER a BLOCK.
```

---

## 8. The License-Not-Require Discipline

A selection rule says what a resolver **MAY** emit, not what it
**MUST** emit. A resolver is constitutionally licit even when:

- it conservatively returns `None` despite a licensed basis being
  available (e.g., the implementation applies a higher confidence
  threshold not specified by this contract);
- it consults only a subset of the admissible bases for a given
  `(symbol, variant)` pair;
- it consults bases in a particular order;
- it caches resolutions across calls;
- it emits audit_trace_ids in a format compatible with the §6.2
  recommended schema of PR #78 but more verbose.

A resolver is constitutionally **illicit** when:

- it emits an `ArabicVariantResolutionEvidence` whose
  `(symbol, variant, selection_basis)` tuple is not licensed by
  §§4–5 of this contract;
- it emits a `selection_basis` label outside the seven reserved
  labels (§3);
- it emits evidence whose audit_trace_ids fail the §6.2 schema in
  ways that make the resolution unauditable;
- it consults raw text, re-tokenises, or crosses tokenizer
  segments (forbidden by PR #78 §4);
- it produces a `Candidate` of any type (forbidden by PR #78 §2);
- it amends the registry (forbidden by §8 below).

This is the same "license, not require" discipline established by
prior contracts; it is restated here for the selection-rule layer
because the difference is constitutionally load-bearing.

---

## 9. Forbidden Jumps

The following jumps are constitutional violations and must be
rejected by any future implementation contract or implementation
PR:

```text
ArabicVariantSelectionRule          →  MinimalUnitReadinessCandidate
                                       (rules license resolutions,
                                        not admissions)
selection_basis                     →  MIU acceptance
                                       (a basis is a witness, not
                                        an admission)
non_madd evidence                   →  MIU acceptance
                                       (resolution removes only
                                        variant_ambiguity; MIU
                                        applies its own predicate)
madd evidence                       →  meaning
                                       (madd resolution is variant
                                        selection, never meaning)
ArabicVariantSelectionRule          →  WordCandidate
ArabicVariantSelectionRule          →  LafzCandidate
ArabicVariantSelectionRule          →  SentenceCandidate
ArabicVariantSelectionRule          →  ParagraphCandidate
ArabicVariantSelectionRule          →  DalalahCandidate
ArabicVariantSelectionRule          →  FinalMeaning
ArabicVariantSelectionRule          →  HukmCandidate
ArabicVariantSelectionRule          →  RealityClaim
ArabicVariantSelectionRule          →  FinalCaseJudgment
ArabicVariantSelectionRule          →  DiscourseGeometryCandidate
ArabicVariantSelectionRule          →  TextGeometryCandidate

variant selection                   →  ArabicArticulationRegistry mutation
                                       (selection rules NEVER amend
                                        the registry; the registry
                                        is metadata only)

bare و                              →  non_madd resolution
                                       (no licensed basis without
                                        a haraka or position witness;
                                        bare-symbol resolution is
                                        forbidden)
bare ي                              →  non_madd resolution
                                       (same)
bare و                              →  madd resolution
                                       (no licensed basis without a
                                        preceding-haraka witness)
bare ي                              →  madd resolution
                                       (same)

(و, madd, haraka_function_self)     →  resolution
                                       (constitutional contradiction:
                                        self-haraka rules out madd)
(ي, madd, haraka_function_self)     →  resolution
                                       (same)

(ا, ANY variant, ANY basis)         →  resolution
                                       (out of scope of this PR;
                                        no admissible tuple)

selection_basis ∉ the seven         →  resolution
                                       (label discipline of §3)

multiple conflicting bases          →  silent majority/heuristic combinator
                                       (default is None — conflict ⇒
                                        DEFER, per §7.4)

invalid trace                       →  resolution
                                       (malformed ⇒ DISCARD ⇒ DEFER,
                                        per §7.5)
```

In full:

```text
Selection rules license, they do not coerce.
Selection rules do not produce candidates.
Selection rules do not produce meaning, لفظ, dalalah, hukm, or
reality.
Selection rules do not equate to MIU acceptance.
Absence of a licensed basis is DEFER, never BLOCK.
Conflict between bases is DEFER, never silent combination.
Malformed evidence is DISCARD, never silent admission.
```

This list extends — does not replace — the forbidden-jump lists in
§11 of the recursive-extension contract, §11 of the closure
contract, §11 of the slot-geometry alignment-trace contract, §12 of
the MIU readiness contract, §11 of the closure-evidence runtime
contract, and §12 of the variant-resolution contract (PR #78). All
seven lists are binding simultaneously.

---

## 10. Relationship to `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` (PR #78)

This contract is **subordinate** to PR #78. Every decision PR #78
fixed is preserved verbatim here:

| PR #78 decision | Preserved here? |
|---|---|
| `ArabicVariantResolutionEvidence` is an Evidence carrier, not a Candidate (§2) | ✅ This contract emits no Candidate. |
| `ArabicVariantResolver` is the sole reserved producer name (§3.1) | ✅ This contract introduces no new producer name. |
| Closed consumption surface to `SlotGeometryCandidate(length = 1)` + preserved local context (§4) | ✅ Every rule below operates on the same surface. |
| Scope: `و` / `ي` in scope; `ا` future extensibility (§5) | ✅ §§4–5 cover و / ي; §6 covers ا as future only. |
| Failure mode: absence ⇒ DEFER, never BLOCK (§7) | ✅ §§4.4 / 5.4 / 7 restate verbatim. |
| Necessary but not sufficient (§7 / §10) | ✅ §1 / §7.3 / §11 restate. |
| Seven reserved `selection_basis` labels (§6.1) | ✅ §3 cites the labels with no extensions. |
| Carrier structural shape (§6.1 fields) | ✅ This contract does not amend the carrier shape. |
| Recommended audit trace schema (§6.2) | ✅ This contract does not amend the schema. |
| Layer specificity / non-portability (§9) | ✅ §11 of this contract preserves. |

This contract does **not** amend PR #78. If any rule below conflicts
with PR #78, PR #78 wins.

---

## 11. Relationship to MIU Readiness

This contract has the same relationship to the MIU readiness layer
that PR #78 fixed: **necessary but not sufficient**, restated
verbatim:

```text
Resolution evidence  ⇏  MIU admission.
Resolution evidence  ⇏  meaning, لفظ, dalalah, hukm, reality.
Resolution evidence's role is narrow: remove the variant_ambiguity
defer reason from a single slot's readiness evaluation, where the
basis used is licensed by §§4–5 of this contract.
```

A resolved `non_madd` reading on وَ does NOT by itself license MIU
admission. The MIU readiness layer's `Admit(S, M, E, V?)` predicate
still applies all other §6 invariants of the MIU contract:

- `S` (`SlotGeometryCandidate(length = 1, construction_mode = "seed")`)
  must satisfy §4.1 structural conditions;
- `E` (`MinimalCompleteClosureEvidence`) must be present and
  well-formed;
- the registry entry's
  `can_function_as_minimal_independent_unit` (for the resolved
  variant) must be `True`;
- every CLAUDE.md §4 invariant must hold.

A resolved `madd` reading on وَ similarly does NOT license meaning,
لفظ, dalalah, hukm, or reality. The MIU readiness layer applies
its eligibility predicate on the resolved entry; per the current
registry, `jawf_waw_madd.can_function_as_minimal_independent_unit
== False`, so MIU BLOCKS. The BLOCK is the eligibility predicate
firing — not a contradiction or a side effect of this contract.

This contract does **not** amend the MIU readiness layer's
adapter or rule. The MIU adapter amendment that would consume
`ArabicVariantResolutionEvidence` as a fourth optional witness
(per PR #78 §10.3) is **out of scope** for this PR; it must come
under its own controlling implementation contract.

---

## 12. Worked Examples

### 12.1 `وَ` — without evidence

```text
Phase 1 / Phase 2 / Closure / MIU readiness without resolver
evidence:
  → MinimalUnitReadinessCandidate DEFERRED
    residual: deferred_variant_ambiguity

This contract changes nothing here. The MIU readiness layer's
existing behaviour is preserved verbatim.
```

### 12.2 `وَ` — with valid `(symbol = "و", variant = "non_madd", selection_basis = ("haraka_function_self",))` evidence

```text
The basis is admissible per §4.1 (haraka_function_self is in the
two-basis admissible set for و non_madd).

The MIU readiness layer (assuming the future MIU adapter amendment):
  variant_ambiguity removed
  → MIU re-evaluates eligibility on the lips_waw_non_madd registry
    entry
  → lips_waw_non_madd.can_function_as_minimal_independent_unit
    == True
  → IF every other MIU §6 invariant also holds:
       MinimalUnitReadinessCandidate ACCEPTED
     ELSE:
       MinimalUnitReadinessCandidate BLOCKED on the failing
       invariant (NOT on variant_ambiguity).

Constitutional reminder: the resolution did NOT itself admit the
slot. The MIU eligibility predicate did.
```

### 12.3 `وَ` — with valid `(symbol = "و", variant = "madd", selection_basis = ("haraka_function_before",))` evidence

```text
For this evidence to be valid, the consumed geometry's preserved
trace must carry a witness that the preceding slot's haraka
satisfies the canonical madd-matching condition (damma on the
preceding letter). For an isolated wَ in a single-slot test
fixture without preceding context, this basis is NOT available,
so the resolver should return None (case §4.4 / §7.2 — DEFER).

For a hypothetical real input where the preceding context IS
preserved (e.g., a Phase-1 pipeline produces a length-1 و slot
whose preserved trace carries a sibling-slot reference and the
sibling slot's haraka is damma — a future implementation question
of how trace is structured), the basis IS available:
  variant_ambiguity removed
  → MIU re-evaluates eligibility on the jawf_waw_madd registry
    entry
  → jawf_waw_madd.can_function_as_minimal_independent_unit
    == False
  → MinimalUnitReadinessCandidate BLOCKED on the
    symbol_not_eligible_for_minimal_unit fariq.

Constitutional reminder: the BLOCK is the eligibility predicate
firing on the resolved madd entry. It is constitutionally correct.
The resolver did its job (identified the variant); the MIU layer
did its job (rejected an ineligible entry).
```

### 12.4 `بِ` — no variant ambiguity

```text
The registry returns a single entry (lips_ba) for "ب" with
can_function_as_minimal_independent_unit == True. No variant
ambiguity. The resolver is NOT invoked.

This contract does NOT change بِ's behaviour. MIU continues to
admit it under existing conditions.
```

### 12.5 `يَ` — same shape as `وَ`

```text
Without evidence: DEFERRED (variant_ambiguity).

With valid (symbol = "ي", variant = "non_madd",
            selection_basis = ("haraka_function_self",)) evidence:
  → variant_ambiguity removed
  → MIU re-evaluates eligibility on the tongue_ya_non_madd
    registry entry
  → tongue_ya_non_madd.can_function_as_minimal_independent_unit
    == True (per the current registry)
  → ACCEPTED IF every other MIU §6 invariant also holds.

With valid (symbol = "ي", variant = "madd",
            selection_basis = ("haraka_function_before",)) evidence
where the preceding context is preserved:
  → variant_ambiguity removed
  → MIU re-evaluates eligibility on the jawf_ya_madd registry
    entry
  → jawf_ya_madd.can_function_as_minimal_independent_unit == False
  → BLOCKED on symbol_not_eligible_for_minimal_unit.

Bare ي without licensed basis: DEFERRED.
```

### 12.6 `ا` — future extensibility only

```text
This contract does NOT define alif variant resolution. The MIU
readiness layer continues to BLOCK alif-headed slots at its existing
eligibility predicate (jawf_alif_madd.
can_function_as_minimal_independent_unit == False).

The resolver MUST return None for any "ا"-headed slot under this
contract. A resolver that emits ArabicVariantResolutionEvidence
for "ا" is in violation; see §6.
```

---

## 13. Summary Table — `(symbol, variant, basis)` Admissibility

For the convenience of any reviewer or future implementation
contract reader, this table restates the contract's admissibility
predicates in a single view.

| Symbol | Variant | Admissible bases | Forbidden bases | Resolution licenses |
|---|---|---|---|---|
| `و` | `non_madd` | `haraka_function_self`; `intra_utterance_position` (secondary, with `haraka_function_self`) | `haraka_function_before`, `haraka_function_after`, `preceding_letter_identity`, `following_letter_identity`, `registry_default` (unavailable) | removal of `variant_ambiguity`; MIU re-evaluates on `lips_waw_non_madd` |
| `و` | `madd` | `haraka_function_before` (canonical: damma on preceding letter + sukun-bearing waw) | `haraka_function_self` (CONSTITUTIONAL CONTRADICTION — self-haraka rules out madd); `haraka_function_after`, `preceding_letter_identity`, `following_letter_identity`, `intra_utterance_position`, `registry_default` (unavailable) | removal of `variant_ambiguity`; MIU re-evaluates on `jawf_waw_madd` (likely BLOCK due to ineligibility) |
| `ي` | `non_madd` | `haraka_function_self`; `intra_utterance_position` (secondary, with `haraka_function_self`) | `haraka_function_before`, `haraka_function_after`, `preceding_letter_identity`, `following_letter_identity`, `registry_default` (unavailable) | removal of `variant_ambiguity`; MIU re-evaluates on `tongue_ya_non_madd` |
| `ي` | `madd` | `haraka_function_before` (canonical: kasra on preceding letter + sukun-bearing ya) | `haraka_function_self` (CONSTITUTIONAL CONTRADICTION); `haraka_function_after`, `preceding_letter_identity`, `following_letter_identity`, `intra_utterance_position`, `registry_default` (unavailable) | removal of `variant_ambiguity`; MIU re-evaluates on `jawf_ya_madd` (likely BLOCK due to ineligibility) |
| `ا` | any | **NONE** — out of scope of this contract | all seven labels | n/a; resolver MUST return `None` for `ا` |
| any other symbol | any | **NONE** — resolver MUST return `None` if `get_primary_articulation(symbol) ≠ None` (single-entry symbol) | all seven labels | n/a; single-entry symbols do not invoke the resolver |

For every row except the last two, the resolver MAY (but is not
required to) emit a resolution when an admissible basis has a
witness on the consumed geometry. For the last two rows, the
resolver MUST return `None`.

---

## 14. Status Classification

This document is classified as:

- **constitutional** — the selection-rule admissibility predicates
  are binding on every future variant-resolution implementation PR;
- **pre-implementation** — no resolver runtime, no MIU adapter
  amendment, no registry change is authorised at the time of merge;
- **subordinate-to-PR-#78** — every decision PR #78 fixed is
  preserved verbatim (§10);
- **strictly-scoped** — covers `و` and `ي` only; `ا` and all other
  symbols are out of scope.

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 15. Authority

Once merged, this document is the constitutional reference for:

- any future PR that proposes an `ArabicVariantResolver`
  implementation (which must restrict its emitted resolutions to
  the admissibility predicates of §§4–5);
- any future PR that proposes a MIU adapter amendment consuming
  variant resolution evidence (which must enforce §7's
  discard / defer / block discipline);
- any future PR that proposes to extend the seven reserved
  `selection_basis` labels (which must amend PR #78 first);
- any future PR that proposes to extend selection rules to `ا` or
  any other symbol (which must amend §5 / §6 of PR #78 first);
- any future PR that proposes a tie-breaking algorithm for
  conflicting bases (which must amend §7.4 of this contract first);
- any future review that asks whether a proposed variant resolution
  is constitutionally licensable.

It supersedes nothing prior; it specialises the
variant-resolution contract (PR #78) by fixing the admissibility
predicates that PR #78 deliberately left to a strictly later
contract.

It does **not** authorise the implementation of
`ArabicVariantResolutionEvidence`, `ArabicVariantResolver`, the
reserved module path, the MIU readiness layer's resolver-aware
admission path, or any consumer. Each must continue to be ratified
by its own contract / implementation PR under
`PR_SCHEDULING_POLICY.md` §1.1 / §1.3 before any implementation PR
may be opened.

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
- modify `slot_geometry_adapter.py`, `slot_geometry_rules.py`,
  `slot_geometry_closure_check.py`,
  `minimal_unit_readiness_adapter.py`, or
  `minimal_unit_readiness_rules.py`,
- implement `ArabicVariantResolutionEvidence` as a runtime type,
- implement `ArabicVariantResolver`,
- create the module `src/qiyas_core/arabic_variant_resolver.py`,
- amend the MIU readiness layer's adapter or rule to consume
  variant resolution evidence,
- introduce any new CI check, hook, bot, or automation,
- define new `selection_basis` labels (the seven of §3 are the
  full set),
- define `ا`-specific variant labels, basis labels, or registry
  entry ids,
- amend the registry to carry a `default_variant` field (the
  `registry_default` basis remains reserved-but-unavailable),
- introduce any new claim prefix beyond the public English names
  fixed in `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §9,
- introduce any new gate beyond the six canonical gates of
  `TERMINOLOGY_MAP.md` §3,
- introduce any new rank beyond the six canonical ranks of
  `TERMINOLOGY_MAP.md` §2,
- produce `Candidate` of any type (no `WordCandidate`,
  `LafzCandidate`, `SentenceCandidate`, `ParagraphCandidate`,
  `DiscourseGeometryCandidate`, `TextGeometryCandidate`,
  `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`,
  `RealityClaim`, `FinalCaseJudgment`,
  `MinimalUnitReadinessCandidate`,
  `MinimalCompleteClosureCandidate`,
  `MinimalIndependentMeaningCandidate`,
  `ArabicVariantResolutionCandidate`),
- accept `و` or `ي` by bare symbol alone,
- claim that `selection_basis` equals truth,
- claim that variant resolution equals readiness,
- claim that variant resolution equals meaning,
- specify a tie-breaking algorithm for conflicting bases,
- specify which haraka values (fatha / damma / kasra / shadda /
  tanwin) trigger which basis (registry + elementary Arabic
  suffice),
- authorise the implementation of any consumer, runtime, adapter,
  kernel surface, or test.

---

## 17. Glossary

| Term | Meaning |
| --- | --- |
| selection rule | An admissibility predicate of the form `(symbol, variant, basis) → admissible | inadmissible`, fixed in §§4–5 / §13 of this contract. |
| admissibility predicate | A Boolean rule that says which `(symbol, variant, basis)` tuples a future resolver MAY use. Distinct from a selection algorithm (which an implementation contract picks). |
| selection algorithm | The implementation-level policy a resolver uses to choose among admissible tuples and decide when to defer. Out of scope of this contract. |
| license, not require | The constitutional discipline (§8): selection rules say what a resolver MAY emit, not what it MUST emit. |
| `registry_default` | Reserved `selection_basis` label that is **currently unavailable** because the `ArabicArticulationRegistry` carries no `default_variant` field. May not be used by any rule under this contract until a future Data Registry PR amends the registry. |
| reserved-but-unavailable | The status of `registry_default` under this contract. The label is reserved by PR #78 §6.1 but is forbidden for use until a registry amendment is ratified. |
| bare symbol | A `SlotGeometryCandidate(length = 1)` whose preserved trace / identity carries no `haraka_function_before` and no `preceding_letter_identity` witnesses. The contract REQUIRES that no resolution be emitted for a bare و or ي with no licensed basis (§§4.4 / 5.4); the resolver returns `None`, and MIU DEFERS. |
| constitutional contradiction | The status of `(و, madd, haraka_function_self)` and `(ي, madd, haraka_function_self)` — internally inconsistent: madd requires sukun, but self-haraka is non-sukun. A resolver emitting such a tuple is in violation of this contract. |
| conflict | The case of §7.4: two or more admissible bases give different variants. The constitutional default is DEFER. |
| malformed | The case of §7.5: the evidence's variant / entry id / selection_basis / trace fields are invalid in some way. The constitutional default is DISCARD ⇒ DEFER. |
| `(symbol, variant, basis)` tuple | The atomic unit of admissibility. A resolver's emitted evidence corresponds to a (symbol, set-of-bases) selection of a variant; this contract fixes which (symbol, variant, basis) tuples may appear. |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
