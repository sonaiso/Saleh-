# PRE_QIYAS_TOKENIZER_CONSTITUTION

> **Status:** Constitutional ratification of **Option C** from the
> whitespace/boundary admission Constitutional Review.
> **Authority:** Docs-only ratification. No code, no tests, no rules are
> changed by this PR. Implementation is deferred to PR Z2 and later.
> **Cross-references:**
> `RESET_CONSTITUTION.md` §7,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §5 / §7.7,
> `CLAUDE.md` §5 / §7,
> `ALGEBRAIC_FOUNDATION_CONTRACT.md`,
> `TERMINOLOGY_MAP.md`.

---

## 0. Provenance

This document records the constitutional decision reached after the
**Constitutional Review: whitespace / boundary admission** report. The
three options considered were:

| | Position | Verdict |
|---|---|---|
| Option A | Boundaries remain outside qiyas; declassify the unreachable `BoundaryCodePoint` path | rejected as insufficiently explicit |
| Option B | Admit boundaries through a new canonical `UNICODE_BOUNDARY_MEMBERSHIP` rule | rejected as constitutionally heavy — would force non-Arabic codepoints into the qiyas chain |
| **Option C** | **Pre-qiyas tokenizer: boundaries are structural framing, fed into CTS as evidence, never as candidates** | **adopted** |

This document ratifies Option C as binding.

---

## 1. The Decision

Whitespace and boundary characters are handled by a **pre-qiyas
tokenizer**.

They are **not qiyas candidates**.

Specifically:

- They **do not** enter `UnicodeQiyas` as `UnicodeCandidate`.
- They **do not** become `TypedCodePoint`.
- They **do not** become `LetterIdentityCarrier`, `HarakaFunctionCarrier`,
  `PositionCarrier`, `SlotCandidate`, or `SlotGeometry`.
- They produce **sequence-framing evidence** consumed by
  `ConditionedTypedSequence`.

This is the binding constitutional position. Any subsequent PR that
violates it must be rejected.

---

## 2. The `SequenceContextTokenizer`

The pre-qiyas component introduced by this decision is named
`SequenceContextTokenizer`. It is **non-qiyas by construction**.

It is **NOT**:

- a `QiyasRule`;
- driven by `QiyasKernel`;
- a producer of `Candidate`;
- subject to rank escalation (`CANDIDATE → LICENSED → PROVEN`);
- a producer of any final output
  (`HukmCandidate`, `RealityClaim`, `FinalMeaning`, `FinalCaseJudgment`).

It runs **before** any qiyas chain executes.

It operates on raw text only.

It produces structural markers that flow **alongside** (not through) the
qiyas chain.

Because it is not a qiyas layer, it is **not** subject to the
`Candidate → Gate → Evidence → Domain → Rank → Residuals → Trace`
septet of `LAYER_CONTRACT_CONSTITUTION.md` §2.1. That septet governs
qiyas layers. The tokenizer is pre-qiyas.

---

## 3. Allowed Outputs

The `SequenceContextTokenizer` is permitted to produce **only** the
following structural markers:

| Marker | Meaning |
|---|---|
| `boundary_before` | a sequence boundary precedes the position |
| `boundary_after` | a sequence boundary follows the position |
| `utterance_segment` | a contiguous span of qiyas-eligible codepoints between boundaries |
| `token_index` | position of the marker within the tokenizer's sequence |
| `intra_utterance_position_hint` | position-context hint within an utterance segment (e.g. start / middle / end) |
| `residual_preservation_marker` | an unclassified codepoint preserved at this position |
| `punctuation_boundary_marker` | Arabic punctuation acting as a sequence boundary |
| `whitespace_boundary_marker` | whitespace acting as a sequence boundary |

These markers are **not** `Candidate` objects. They are **structural
evidence**.

They reach downstream qiyas layers (specifically
`ConditionedTypedSequence`) either as `EvidenceItem.proves` claims (with
appropriate `وصف:` / `علة:` prefixes following
`TERMINOLOGY_MAP.md`) or as a sibling input channel to the CTS adapter.
The implementation detail is deferred to PR Z2 / Z3.

This list of eight markers is **exhaustive for ratification**. Adding
a new marker type requires a constitutional amendment, not a routine
PR.

---

## 4. Required Relation to `ConditionedTypedSequence`

`ConditionedTypedSequence` **may** consume `SequenceContextTokenizer`
evidence to perform the following functions:

1. **Block orphan marks.** A haraka whose `boundary_before` or
   `whitespace_boundary_marker` separates it from the preceding letter
   cannot bind to that letter as carrier; the kernel must block the
   `CarrierBindingCandidate` with the invalidating-difference
   `haraka_without_carrier`.
2. **Delimit carrier search.** The carrier-lookback for a haraka must
   not cross an `utterance_segment` boundary. The lookback terminates
   at the first preceding `boundary_before` or equivalent marker.
3. **Prevent cross-boundary binding.** No `CarrierBindingCandidate`
   may span a `boundary_before` / `boundary_after` /
   `punctuation_boundary_marker` / `whitespace_boundary_marker`.
4. **Preserve residuals.** Every `residual_preservation_marker`
   produced by the tokenizer becomes the basis for a
   `ResidualPreservationEvidence` admissibility claim in CTS.
5. **Derive `PositionEvidence`.** Sequence-position derivation in
   CTS — used to compute `intra_utterance_position_hint`-aware
   INITIAL / MEDIAL / FINAL / ISOLATED — consumes the tokenizer's
   `boundary_before` / `boundary_after` markers instead of computing
   positions ad-hoc from the raw text.

`ConditionedTypedSequence` **must not**:

- elevate tokenizer evidence to identity (tokenizer markers are not
  `identity_ids`);
- treat tokenizer markers as `Candidate` objects;
- bypass its own rule validation by trusting tokenizer markers
  verbatim without subjecting them to its standard six-`wadi`
  validation.

---

## 5. Forbidden Actions for `SequenceContextTokenizer`

The `SequenceContextTokenizer` **must not**:

- produce `SlotCandidate`;
- produce `SlotGeometry`;
- produce `LetterIdentityCarrier`, `HarakaFunctionCarrier`, or
  `PositionCarrier`;
- produce any `Candidate` of any `candidate_type`;
- create identity (`identity_ids` are produced by qiyas layers only;
  the tokenizer has no role in identity construction);
- consume identity (the tokenizer reads raw text, not upstream
  `Candidate` objects);
- replace `TypedCodePoint` (qiyas-eligible codepoints continue to flow
  through `UnicodeQiyas → TypedCodePointClassificationQiyas`
  unchanged);
- bypass `ConditionedTypedSequence` (tokenizer evidence reaches any
  downstream qiyas layer **only** via CTS).

These prohibitions are constitutional. Any future PR violating them
must be rejected at review.

---

## 6. Consequences for Existing Code

The following items are flagged for handling in subsequent PRs (Z3 / Z4).
**No code change happens in this PR.**

| Item | Disposition |
|---|---|
| `BOUNDARY_CODEPOINT_CLASSIFICATION` rule in `typed_codepoint_rules.py` | Dead code in canonical paths after Z2. To be declassified (testing-only annotation or removal) in PR Z4. |
| `BOUNDARY_EXCLUSION_PROOF` rule in `conditioned_typed_sequence_rules.py` | To be reframed as a tokenizer-consuming proof, OR declassified, in PR Z3 / Z4. |
| `BOUNDARY_CODEPOINTS` constant and `is_boundary` predicate in `typed_codepoint_adapter.py` | To be moved into the tokenizer (PR Z2) or marked testing-only (PR Z4). |
| `PUNCTUATION_EXCLUSION_PROOF` rule | Remains canonical. Consumes tokenizer evidence (`punctuation_boundary_marker`) rather than producing standalone `BoundaryEvidence` (PR Z3). |
| `_classify_position` in `run_qiyas.py` | Replaced by tokenizer-derived position context (PR Z5). |

The records above are forward-looking only. This PR introduces no
behavioural change.

---

## 7. Status Classification

This document classifies the pre-qiyas tokenizer as:

- **constitutional** — the architectural decision is ratified by this
  PR;
- **pre-canonical** — no implementation exists at the time this
  document is merged;
- **non-qiyas** — by design and by constitution, the tokenizer is not
  part of the qiyas chain and is not subject to qiyas-layer
  obligations.

The classification persists across future PRs until and unless a
formal constitutional amendment supersedes it.

---

## 8. Forward Plan

Implementation order. **No PR may skip its predecessor.**

| PR | Scope | Files touched |
|---|---|---|
| **Z1 (this PR)** | Constitutional ratification of Option C | `docs/qiyas_core/PRE_QIYAS_TOKENIZER_CONSTITUTION.md` |
| Z2 | Implement `SequenceContextTokenizer` (pre-qiyas, non-`QiyasRule`) | `src/qiyas_core/` (new file), `tests/qiyas_core/` |
| Z3 | Refactor CTS to consume tokenizer evidence | `src/qiyas_core/conditioned_typed_sequence_*` + tests |
| Z4 | Declassify unreachable `BoundaryCodePoint` paths | `src/qiyas_core/` + tests |
| Z5 | Route whitespace through tokenizer in `run_qiyas` | `run_qiyas.py` + regression tests |

After Z5, and only after Z5, may the project consider:

- the **SlotGeometry alignment-trace contract** (docs-only PR),
- the **`SlotGeometryQiyas` implementation** PR.

These two are explicitly **out of scope** for Z1 through Z5.

---

## 9. Authority

This document, once merged, is constitutional reference for:

- any future PR involving whitespace, boundary, punctuation, or
  sequence framing;
- any future Claude or human contributor reading `CLAUDE.md` or the
  `docs/` tree;
- any future `SlotGeometry` contract (which depends on a stable
  boundary model).

It supersedes the implicit boundary semantics that existed in PRs
#25–#31 prior to ratification.

`CLAUDE.md §5` (parallel proofs, not one linear chain) and `CLAUDE.md
§7` (function of `ConditionedTypedSequence`) remain authoritative; this
document narrows their scope by clarifying that whitespace/boundary
recognition is **not** a CTS responsibility — CTS *consumes* tokenizer
output, it does not *produce* boundary detection itself.

---

## 10. Glossary

| Term | Meaning |
|---|---|
| pre-qiyas | Operates before any `QiyasRule` is invoked; produces no `Candidate`. |
| qiyas-eligible codepoint | A codepoint that passes `UnicodeQiyas` (per current canonical chain, an Arabic Unicode block codepoint). |
| sequence-framing | Structural metadata about position, adjacency, and boundaries that does not assert anything about the identity of a codepoint. |
| utterance segment (`utterance_segment`) | A maximal contiguous run of qiyas-eligible codepoints delimited by boundary markers on either side. |
| structural marker | A non-`Candidate` data object produced by the tokenizer. |

---

**End of document. Ratification PR is docs-only.**
