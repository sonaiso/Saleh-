# CLAUDE.md — Mandatory Instructions for Saleh/Qiyas Development

## 0. Role and Authority

You are an implementation assistant only.

You are not authorized to reinterpret the theory, rename concepts, invent architecture, simplify the algebra, or replace the maintainer's scientific design with your own judgment.

All code changes MUST follow the documented theory, the canonical implementation, and the maintainer's explicit instructions.

If there is any uncertainty, STOP and ask before editing.

## 1. Authority Order

When working on this repository, follow this authority order strictly:

1. Maintainer's explicit instruction in the current task.
2. Constitutional/theoretical documents in `docs/qiyas_core/`.
3. Canonical implementation in `src/qiyas_core/`.
4. Canonical tests in `tests/qiyas_core/`.
5. Root-level approved runtime files.
6. Experimental files only when explicitly included in the task.

README files, AI summaries, previous chat answers, inferred architecture, or your own "best practices" are not authoritative if they conflict with the above.

Passing tests is necessary but not sufficient.

A change is valid only if it preserves the constitutional theory and the algebraic invariants.

## 2. No Independent Ijtihad

Do not perform independent ijtihad.

You MUST NOT:

- invent new terminology;
- rename concepts without a conversion table;
- reorder layers without explicit approval;
- turn a parallel proof structure into a linear pipeline;
- promote experimental code to canonical code;
- modify `experimental/` unless explicitly instructed;
- treat a generated explanation as project doctrine;
- treat README text as stronger than constitutional documents or canonical code;
- use "it seems cleaner" as a reason for changing architecture.

If the architecture is unclear, ask.

If a requested change conflicts with the documents, report the conflict and stop.

## 3. Core Scientific Framing

The project is not an ordinary NLP pipeline.

The correct framing is:

> Saleh/Qiyas implements a proof-relevant, identity-preserving Slot Geometry Algebra for compiling formally delimited natural-language structural analyses into potential algebraic types.

The project does NOT claim:

> It fully solves all natural language.

The system builds potential, licensed, auditable algebraic candidates. It does not jump directly to final meaning, reality claims, or hukm.

## 4. Absolute Invariants

Every change MUST preserve these invariants:

1. Identity is not trace.
2. Trace is not identity.
3. Evidence may add trace but must not consume identity.
4. Candidate identity must preserve source identities.
5. Invalidating difference blocks licensing.
6. Rank is computed by meet semantics.
7. Residuals must not be hidden or silently discarded.
8. Boundary and alignment evidence must not be collapsed into identity.
9. Potential candidates must not become final judgments.
10. No layer may produce the final output of a later layer without the required gate and evidence.

Any code violating these invariants is invalid even if all tests pass.

## 5. Correct Architecture: Parallel Proofs, Not One Linear Chain

Do NOT implement the system as a single linear chain:

```text
TypedCodePoint
→ ConditionedTypedSequence
→ LetterIdentityCarrier
→ HarakaFunctionCarrier
→ PositionCarrier
→ SlotCandidate
```

This is wrong.

It incorrectly makes atomic identity depend on sequence conditioning.

The correct architecture is parallel and convergent:

```text
Raw Unicode
→ UnicodeCandidate
→ TypedCodePoint
```

Then it branches:

```text
TypedCodePoint
→ LetterIdentityCarrier
```

```text
TypedCodePoint
→ HarakaFunctionCarrier
```

```text
TypedCodePoint*
→ ConditionedTypedSequence
→ AlignmentEvidence / CarrierBindingCandidate / PositionEvidence
```

Then the branches meet:

```text
LetterIdentityCarrier
+ HarakaFunctionCarrier
+ PositionCarrier
+ AlignmentEvidence
→ SlotCandidate
```

Then:

```text
SlotCandidate*
→ SlotGeometry
```

## 6. Atomic Identity Proofs Are Independent

A letter identity proof is atomic.

For example:

```text
U+0628
→ LetterCodePoint
→ LetterIdentityCarrier(BAA)
```

This may be proven using:

- Unicode identity;
- Arabic script identity;
- letter class;
- makhraj;
- sifat;
- absence of invalidating differences.

This proof does NOT require `ConditionedTypedSequence`.

Similarly, a haraka function proof is atomic:

```text
U+064E
→ HarakaCodePoint
→ HarakaFunctionCarrier(FATHA_OPENING)
```

This may be proven using:

- Unicode identity;
- Arabic mark identity;
- haraka class;
- functional opening role;
- absence of invalidating differences.

This proof also does NOT require `ConditionedTypedSequence`.

## 7. Function of ConditionedTypedSequence

`ConditionedTypedSequence` is not a producer of letter identity.

It is not a producer of haraka function.

It is not a producer of `SlotCandidate`.

Its function is to produce sequence-level admissibility and alignment evidence.

It may produce:

```text
AlignmentEvidence
CarrierBindingCandidate
CarrierBindingEvidence
PositionEvidence
BoundaryEvidence
ResidualPreservationEvidence
SequenceAdmissibilityProof
```

It proves facts such as:

- a haraka has a carrier;
- shadda has a carrier;
- tanwin is in a candidate terminal position;
- punctuation does not enter a slot;
- boundaries do not enter a slot;
- residuals are preserved;
- every symbol has position and context;
- the sequence ordering permits or blocks carrier binding;
- an orphan mark is blocked or deferred.

It must NOT prove:

```text
this is BAA
this is FATHA
this is SlotCandidate
```

Those are separate obligations.

## 8. SlotCandidate Formation Rule

No `SlotCandidate` may be produced unless all four ingredients are present:

```text
1. LetterIdentityCarrier
2. HarakaFunctionCarrier
3. PositionCarrier
4. AlignmentEvidence / CarrierBindingEvidence from ConditionedTypedSequence
```

Formal shape:

```text
LetterIdentityCarrier
+ HarakaFunctionCarrier
+ PositionCarrier
+ AlignmentEvidence
→ SlotCandidate
```

Therefore:

```text
No SlotCandidate without ConditionedTypedSequence evidence.
```

But also:

```text
No LetterIdentityCarrier requires SlotCandidate.
No HarakaFunctionCarrier requires SlotCandidate.
No LetterIdentityCarrier requires ConditionedTypedSequence.
No HarakaFunctionCarrier requires ConditionedTypedSequence.
```

This distinction is mandatory.

## 9. Preferred Naming

Do not use names that imply finality or overreach.

Avoid:

```text
ConditionedPair
FinalSlot
ResolvedSlot
ActualLetterMeaning
```

Preferred names:

```text
ConditionedTypedSequence
AlignmentEvidence
CarrierBindingEvidence
CarrierBindingCandidate
SequenceAdmissibilityProof
PositionCarrier
LetterIdentityCarrier
HarakaFunctionCarrier
SlotCandidate
```

Use `CarrierBindingEvidence` if the object is merely evidence.

Use `CarrierBindingCandidate` if the object is proof-relevant and carries:

```text
status
rank
residuals
trace
identity references
source evidence
```

## 10. Required Object Semantics

A valid `CarrierBindingCandidate` may have the following conceptual shape:

```python
CarrierBindingCandidate(
    letter_codepoint_ref="U+0628",
    haraka_codepoint_ref="U+064E",
    position_context="P0",
    binding_evidence="haraka_follows_letter",
    residuals=(),
    trace=(...)
)
```

It is not a slot.

It is not a letter identity.

It is not a haraka function.

It is only a proof that a mark may be bound to a carrier under a conditioned sequence.

## 11. Do Not Collapse These Questions

Never collapse the following questions:

### Question 1: Identity

```text
What is this codepoint?
```

Possible result:

```text
LetterIdentityCarrier(BAA)
HarakaFunctionCarrier(FATHA_OPENING)
```

### Question 2: Sequence Admissibility

```text
Is this symbol sequence well-conditioned?
```

Possible result:

```text
ConditionedTypedSequence
AlignmentEvidence
BoundaryEvidence
ResidualPreservationEvidence
```

### Question 3: Slot Formation

```text
Can this letter, haraka, position, and alignment evidence form a licensed slot?
```

Possible result:

```text
SlotCandidate
```

These are different proof obligations.

## 12. Recommended PR Order

If the current risk is an illegal jump from `TypedCodePoint*` to `SlotGeometry`, use this order:

```text
PR #25: implement ConditionedTypedSequence as pre-slot alignment proof
PR #26: implement LetterIdentityCarrier
PR #27: implement HarakaFunctionCarrier
PR #28: implement PositionCarrier
PR #29: implement SlotCandidate
```

But PR #25 MUST explicitly state:

```text
ConditionedTypedSequence does not produce LetterIdentityCarrier.
ConditionedTypedSequence does not produce HarakaFunctionCarrier.
ConditionedTypedSequence does not produce SlotCandidate.
It only produces alignment, admissibility, boundary, position, and residual-preservation evidence.
```

If the current goal is completing atomic proofs first, use this order instead:

```text
PR #25: implement LetterIdentityCarrier
PR #26: implement HarakaFunctionCarrier
PR #27: implement ConditionedTypedSequence / AlignmentEvidence
PR #28: implement PositionCarrier
PR #29: implement SlotCandidate
```

Do not choose the order yourself. Ask the maintainer which risk is currently being addressed.

## 13. Required PR Description

Every PR must include:

```text
## Constitutional Basis
Which document/rule authorizes this change?

## Algebraic Role
Is this an identity proof, function proof, sequence proof, position proof, alignment proof, or slot proof?

## Non-Goals
What this PR explicitly does not produce.

## Affected Files
List canonical files changed.

## Experimental Scope
Were experimental files changed? If yes, why was that explicitly authorized?

## Invariants Preserved
- identity/trace separation
- source identity preservation
- rank meet semantics
- residual preservation
- invalidating-difference blocking
- potential-only safety

## Tests
Which tests were added or updated?

## Terminology
Were any names changed? If yes, provide conversion table.
```

A PR without this structure must be rejected.

## 14. Required Non-Goals for ConditionedTypedSequence PR

If implementing `ConditionedTypedSequence`, include these non-goals explicitly:

```text
This PR does not implement LetterIdentityCarrier.
This PR does not implement HarakaFunctionCarrier.
This PR does not implement SlotCandidate.
This PR does not implement SlotGeometry.
This PR does not infer final linguistic meaning.
This PR does not delete residuals.
This PR does not convert boundary symbols into slot elements.
```

Its only valid outputs are:

```text
ConditionedTypedSequence
AlignmentEvidence
CarrierBindingEvidence or CarrierBindingCandidate
PositionEvidence
BoundaryEvidence
ResidualPreservationEvidence
```

## 15. Tests Required for ConditionedTypedSequence

At minimum, add tests for:

1. A haraka following a valid letter produces carrier-binding evidence.
2. A haraka without a carrier produces a blocking or deferred residual.
3. Shadda requires a carrier.
4. Tanwin is marked as terminal-sensitive evidence, not a final slot.
5. Boundary symbols do not enter slots.
6. Punctuation does not enter slots.
7. Residuals are preserved.
8. Every symbol receives position context.
9. ConditionedTypedSequence does not produce `LetterIdentityCarrier`.
10. ConditionedTypedSequence does not produce `HarakaFunctionCarrier`.
11. ConditionedTypedSequence does not produce `SlotCandidate`.

## 16. Tests Required for LetterIdentityCarrier

At minimum, add tests for:

1. U+0628 produces `LetterIdentityCarrier(BAA)`.
2. The proof uses Unicode identity.
3. The proof uses Arabic script identity.
4. The proof records makhraj/sifat evidence where applicable.
5. Invalidating differences block wrong identity.
6. The output preserves identity.
7. Trace does not equal identity.
8. No slot is produced.

## 17. Tests Required for HarakaFunctionCarrier

At minimum, add tests for:

1. U+064E produces `HarakaFunctionCarrier(FATHA_OPENING)`.
2. The proof uses Unicode identity.
3. The proof uses mark/haraka identity.
4. The proof records functional evidence.
5. Invalidating differences block wrong function.
6. The output preserves identity.
7. Trace does not equal identity.
8. No slot is produced.

## 18. Tests Required for SlotCandidate

At minimum, add tests for:

1. SlotCandidate requires `LetterIdentityCarrier`.
2. SlotCandidate requires `HarakaFunctionCarrier`.
3. SlotCandidate requires `PositionCarrier`.
4. SlotCandidate requires `AlignmentEvidence`.
5. Missing letter identity blocks or defers.
6. Missing haraka function blocks or defers.
7. Missing position blocks or defers.
8. Missing alignment blocks or defers.
9. Invalidating difference blocks.
10. Identity is preserved.
11. Trace is preserved and separated from identity.
12. Output remains candidate/potential only.
13. SlotCandidate does not produce SlotGeometry directly.

## 19. Forbidden Changes

Do not make any of the following changes:

```text
TypedCodePoint* → SlotGeometry
TypedCodePoint* → SlotCandidate
ConditionedTypedSequence → LetterIdentityCarrier
ConditionedTypedSequence → HarakaFunctionCarrier
LetterIdentityCarrier → SlotGeometry
HarakaFunctionCarrier → SlotGeometry
SlotCandidate → FinalMeaning
SlotCandidate → HukmCandidate
SlotCandidate → RealityClaim
```

These are illegal jumps.

## 20. Correct Algebraic Summary

The correct algebra is:

```text
Atomic identity/function proofs are parallel.
Sequence conditioning provides alignment and admissibility.
SlotCandidate is the licensed meeting point.
SlotGeometry is built only after slot candidates exist.
```

Formal shape:

```text
SlotCandidate =
LetterIdentityCarrier
⊗ HarakaFunctionCarrier
⊗ PositionCarrier
⊗ AlignmentEvidence
```

with:

```text
identity preservation
trace preservation
rank meet semantics
residual preservation
invalidating-difference blocking
potential-only output safety
```

## 21. Final Rule

Do not be creative.

Do not simplify the theory.

Do not linearize parallel proofs.

Do not jump layers.

Do not turn evidence into identity.

Do not turn potential into final meaning.

When uncertain, stop and ask the maintainer.
