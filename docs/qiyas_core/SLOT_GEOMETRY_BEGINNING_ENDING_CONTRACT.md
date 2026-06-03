# SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT

> **Status:** Constitutional. Docs-only contract for SlotGeometry
> beginning and ending rule semantics. No code, no tests, no
> implementation are changed by this PR.
>
> **Track:** SlotGeometry only (Track A).
>
> **Authority basis:**
> `SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT.md` §3.1 / §3.2,
> `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §3 / §8,
> `CLAUDE.md` §0 / §4 / §5 / §7 / §8 / §19 / §20,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `RESET_CONSTITUTION.md` §1 / §3,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4.
>
> **Governing one-liner:**
>
> ```
> Beginning licenses where SlotGeometry may start.
> Ending licenses where SlotGeometry may stop.
> Neither produces meaning.
> ```
>
> ```
> البداية ترخّص أين قد يبدأ SlotGeometry.
> النهاية ترخّص أين قد يتوقف SlotGeometry.
> كلاهما لا ينتج معنى.
> ```

---

## 0. Constitutional Position

**This document defines beginning and ending rules for SlotGeometry layer ONLY.**

**Current state:**
- PR #63 defined SlotGeometry alignment-trace contract
- PR #64 implemented SlotGeometry seed + extend skeleton
- PR #65 centralized SlotGeometry forbidden outputs
- PR #68 closed LCNV Track B (must NOT be touched)
- PR #69 defined SlotGeometry closure and Demand Catalogue contract
- PR #70 added constitutional guard tests for closure contract
- Closure conditions §3.1 and §3.2 require "licensed beginning" and "licensed ending"

**This PR scope:**
- Add `docs/qiyas_core/SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md` ONLY
- Define SlotGeometryBeginningRule as contract concept
- Define SlotGeometryEndingRule as contract concept
- Define required evidence for licensed beginning
- Define required evidence for licensed ending
- Define blocking residuals for missing beginning/ending
- Define relationship to SlotGeometryCandidate trace_ids
- Define relationship to SequenceContextTokenizer boundaries
- Distinguish beginning/ending from meaning/dalalah/word formation

**This PR does NOT:**
- Modify `src/qiyas_core/`
- Modify `tests/qiyas_core/`
- Modify `run_qiyas.py`
- Modify LCNV
- Modify billing/product
- Modify Logarithmic Measurement
- Implement SlotGeometryBeginningRule runtime
- Implement SlotGeometryEndingRule runtime
- Implement IsMinimallyComplete runtime
- Implement MinimalCompletionReadinessCandidate runtime
- Wire runtime execution
- Add DalalahCandidate / WordCandidate / Meaning / Ifadah / Hukm
- Add new claim prefix, rank, or gate (unless reserved as future work only)

---

## 1. The Governing Principle

**Beginning and ending are CLOSURE CONDITIONS, not MEANING CONDITIONS.**

### 1.1 What Beginning Is

```text
Beginning answers: WHERE may a SlotGeometry start?

Beginning does NOT answer:
  - What does this SlotGeometry mean?
  - What word does this form?
  - What is the dalalah of this geometry?
  - What hukm does this imply?
```

**Beginning is a LICENSING GATE, not semantic authority:**

```text
SlotGeometryBeginningRule licenses:
  - This SlotCandidate MAY start a SlotGeometry

SlotGeometryBeginningRule does NOT produce:
  - DalalahCandidate
  - WordCandidate
  - FinalMeaning
  - HukmCandidate
  - RealityClaim
```

**بالعربية:**

```
البداية ترخيص موضعي، لا سلطة دلالية.

البداية تجيب: أين يجوز أن يبدأ SlotGeometry؟

البداية لا تجيب:
  - ما معنى هذا SlotGeometry؟
  - ما الكلمة التي يشكلها؟
  - ما دلالته؟
  - ما حكمه؟
```

### 1.2 What Ending Is

```text
Ending answers: WHERE may a SlotGeometry stop?

Ending does NOT answer:
  - What does this SlotGeometry mean?
  - Is this a complete word?
  - What is the final meaning?
  - Is this a valid utterance?
```

**Ending is a STOPPING CONDITION, not semantic finality:**

```text
SlotGeometryEndingRule licenses:
  - This SlotCandidate MAY terminate a SlotGeometry

SlotGeometryEndingRule does NOT produce:
  - DalalahCandidate
  - WordCandidate
  - FinalMeaning
  - HukmCandidate
  - RealityClaim
  - WordBoundaryCandidate
```

**بالعربية:**

```
النهاية شرط توقف، لا نهاية دلالية.

النهاية تجيب: أين يجوز أن يتوقف SlotGeometry؟

النهاية لا تجيب:
  - ما معنى هذا SlotGeometry؟
  - هل هذا كلمة كاملة؟
  - ما المعنى النهائي؟
  - هل هذا لفظ صحيح؟
```

### 1.3 The Critical Distinction

```text
Beginning/Ending = positional licensing
Meaning/Dalalah  = semantic content

Beginning/Ending = closure readiness conditions
Word formation   = later layer's obligation

Beginning/Ending = slot-geometry layer contract
Hukm             = much later layer's obligation
```

**These are DIFFERENT proof obligations:**

| Question | Obligation | Layer |
|----------|-----------|-------|
| Where can SlotGeometry start? | Beginning rule | SlotGeometry |
| Where can SlotGeometry stop? | Ending rule | SlotGeometry |
| What does it mean? | Dalalah proof | Future Dalalah layer |
| Is it a word? | Word formation | Future Word layer |
| What is the hukm? | Hukm derivation | Future Hukm layer |

---

## 2. SlotGeometryBeginningRule — Contract Definition

**SlotGeometryBeginningRule is a contract concept ONLY at this stage.**

**No runtime implementation is authorized by this PR.**

### 2.1 Purpose

```text
SlotGeometryBeginningRule proves:
  "This SlotCandidate is admissible as the FIRST unit of a SlotGeometry."
```

**It does NOT prove:**
- This is the first unit of a word
- This is the start of meaning
- This is a word boundary
- This is the beginning of dalalah
- This is the start of an utterance

### 2.2 Input

```text
Input: SlotCandidate
```

**Preconditions:**
- The SlotCandidate satisfies `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §2
- The SlotCandidate has `alignment_ref` in trace_ids
- The SlotCandidate has rank > NO_EVIDENCE
- The SlotCandidate is CandidateOnly

### 2.3 Output

```text
Output: Beginning evidence | Blocking residual
```

**On success:**
```text
Evidence claims:
  - gate:beginning:licensed (public name)
  - وادي:beginning:licensed (canonical implementation)
  - effective_cause:slot_geometry_beginning:{reason}:verified

where {reason} is one of:
  - segment_initial (first slot in INTRA_UTTERANCE segment)
  - post_boundary (follows whitespace/punctuation boundary preserved by tokenizer)
  - licensed_position (position admits beginning under slot-geometry policy)
```

**On failure (blocking):**
```text
Residual:
  - فارق:beginning_blocked:{reason}:present

where {reason} is one of:
  - mid_segment_orphan (slot appears mid-segment without licensing position)
  - boundary_violation (slot violates tokenizer boundary context)
  - position_conflict (slot position conflicts with beginning admissibility)
```

**On failure (deferral):**
```text
Residual:
  - defer:beginning_evidence_insufficient:present
```

### 2.4 Required Evidence

**A valid beginning license requires ALL of the following:**

1. **Position evidence from SequenceContextTokenizer:**
   - The SlotCandidate's source position is consistent with a beginning position
   - This is read from trace, NOT re-derived from raw text
   - Witness: `trace:position_context:{context}` where context ∈ {initial, isolated}

2. **Boundary evidence from SequenceContextTokenizer:**
   - No whitespace_boundary_marker forbids this position as beginning
   - No punctuation_boundary_marker forbids this position as beginning
   - Witness: `trace:boundary_context:beginning_admissible`

3. **Segment context from SequenceContextTokenizer:**
   - The SlotCandidate belongs to INTRA_UTTERANCE segment
   - Witness: `trace:segment_context:INTRA_UTTERANCE`

4. **No invalidating difference:**
   - No فارق: claim blocks beginning
   - Witness: absence of `فارق:beginning_blocked:*`

### 2.5 What Beginning Does NOT Require

**Beginning does NOT require:**
- Knowledge of what the SlotGeometry will mean
- Knowledge of whether it will form a word
- Knowledge of morphological role
- Knowledge of syntactic function
- Knowledge of semantic content
- Knowledge of dalalah
- Knowledge of hukm

**Beginning MAY be licensed without:**
- Complete word formation
- Lexical attestation
- Morphological analysis
- Syntactic parsing
- Semantic interpretation

### 2.6 Relationship to Seed

**For SlotGeometry length = 1 (Seed case):**

```text
The single SlotCandidate must be licensed as BOTH:
  - Beginning (via SlotGeometryBeginningRule), AND
  - Ending (via SlotGeometryEndingRule)

The Seed step produces both licenses simultaneously.
```

**Evidence shape for Seed:**
```text
gate:beginning:licensed
gate:ending:licensed
effective_cause:slot_geometry_seed:single_slot_complete:verified
```

**For SlotGeometry length > 1:**

```text
Only the FIRST SlotCandidate requires beginning license.
Subsequent units do NOT re-prove beginning.
Beginning evidence is inherited from Seed or first Extend.
```

---

## 3. SlotGeometryEndingRule — Contract Definition

**SlotGeometryEndingRule is a contract concept ONLY at this stage.**

**No runtime implementation is authorized by this PR.**

### 3.1 Purpose

```text
SlotGeometryEndingRule proves:
  "This SlotCandidate is admissible as the LAST unit of a SlotGeometry."
```

**It does NOT prove:**
- This is the last unit of a word
- This is the end of meaning
- This is a word boundary
- This is the ending of dalalah
- This is the end of an utterance
- This is complete semantic finality

### 3.2 Input

```text
Input: SlotCandidate
```

**Preconditions:**
- The SlotCandidate satisfies `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §2
- The SlotCandidate has `alignment_ref` in trace_ids
- The SlotCandidate has rank > NO_EVIDENCE
- The SlotCandidate is CandidateOnly

### 3.3 Output

```text
Output: Ending evidence | Blocking residual
```

**On success:**
```text
Evidence claims:
  - gate:ending:licensed (public name)
  - وادي:ending:licensed (canonical implementation)
  - effective_cause:slot_geometry_ending:{reason}:verified

where {reason} is one of:
  - segment_terminal (last slot in INTRA_UTTERANCE segment)
  - pre_boundary (precedes whitespace/punctuation boundary preserved by tokenizer)
  - licensed_position (position admits ending under slot-geometry policy)
```

**On failure (blocking):**
```text
Residual:
  - فارق:ending_blocked:{reason}:present

where {reason} is one of:
  - mid_segment_truncation (slot appears mid-segment without licensing termination)
  - boundary_violation (slot violates tokenizer boundary context)
  - position_conflict (slot position conflicts with ending admissibility)
```

**On failure (deferral):**
```text
Residual:
  - defer:ending_evidence_insufficient:present
```

### 3.4 Required Evidence

**A valid ending license requires ALL of the following:**

1. **Position evidence from SequenceContextTokenizer:**
   - The SlotCandidate's source position is consistent with an ending position
   - This is read from trace, NOT re-derived from raw text
   - Witness: `trace:position_context:{context}` where context ∈ {terminal, isolated}

2. **Boundary evidence from SequenceContextTokenizer:**
   - A whitespace_boundary_marker OR punctuation_boundary_marker follows this position
   - OR: this is the segment-terminal position
   - Witness: `trace:boundary_context:ending_admissible`

3. **Segment context from SequenceContextTokenizer:**
   - The SlotCandidate belongs to INTRA_UTTERANCE segment
   - Witness: `trace:segment_context:INTRA_UTTERANCE`

4. **No invalidating difference:**
   - No فارق: claim blocks ending
   - Witness: absence of `فارق:ending_blocked:*`

### 3.5 What Ending Does NOT Require

**Ending does NOT require:**
- Knowledge of what the SlotGeometry means
- Knowledge that it forms a complete word
- Knowledge of morphological completeness
- Knowledge of syntactic role
- Knowledge of semantic content
- Knowledge of dalalah
- Knowledge of hukm
- Lexical attestation
- Morphological closure
- Word formation closure

**Ending MAY be licensed without:**
- Complete word meaning
- Lexical entry match
- Morphological analysis completion
- Syntactic parsing
- Semantic interpretation

### 3.6 Relationship to Seed

**For SlotGeometry length = 1 (Seed case):**

```text
The single SlotCandidate must be licensed as BOTH:
  - Beginning (via SlotGeometryBeginningRule), AND
  - Ending (via SlotGeometryEndingRule)

The Seed step produces both licenses simultaneously.
```

**Evidence shape for Seed:**
```text
gate:beginning:licensed
gate:ending:licensed
effective_cause:slot_geometry_seed:single_slot_complete:verified
```

**For SlotGeometry length > 1:**

```text
Only the LAST SlotCandidate requires ending license.
Previous units do NOT prove ending.
Ending evidence is produced at final Extend or closure check.
```

---

## 4. Boundary Evidence Is Trace, Not Identity

**Critical principle:**

```text
Boundary evidence = provenance trace
Boundary evidence ≠ identity

Beginning license = admissibility gate
Beginning license ≠ meaning content

Ending license = stopping condition
Ending license ≠ semantic finality
```

### 4.1 What Boundary Evidence Is

**Boundary evidence records:**
- WHERE a tokenizer boundary exists (whitespace, punctuation)
- THAT a boundary was preserved (not crossed during binding)
- WHICH position context a slot has (initial, medial, terminal, isolated)

**Boundary evidence does NOT record:**
- WHAT the geometry means
- WHETHER it forms a word
- WHAT word it forms
- WHAT the dalalah is

### 4.2 CLAUDE.md §4 Invariant 8

**From CLAUDE.md:**

```text
Invariant 8: Boundary and alignment evidence must not be collapsed into identity.
```

**Application to beginning/ending:**

```text
gate:beginning:licensed is NOT identity
gate:ending:licensed is NOT identity

Both are TRACE/PROVENANCE evidence.
Neither produces MEANING or DALALAH.
```

**Forbidden conflations:**

```text
❌ Beginning license → Word beginning
❌ Ending license → Word ending
❌ Boundary position → Morphological boundary
❌ Segment terminal → Semantic finality
❌ Licensed ending → Complete meaning
```

**Allowed inferences:**

```text
✓ Beginning license → SlotGeometry may start here
✓ Ending license → SlotGeometry may stop here
✓ Boundary evidence → Position context is consistent
✓ Segment context → INTRA_UTTERANCE binding is valid
```

---

## 5. Relationship to SequenceContextTokenizer

**SlotGeometry beginning/ending rules DEPEND ON SequenceContextTokenizer evidence.**

**They do NOT re-tokenize.**

### 5.1 What Tokenizer Provides

**Per `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` Option C (adopted):**

```text
SequenceContextTokenizer provides:
  - INTRA_UTTERANCE segment boundaries
  - whitespace_boundary_marker stream
  - punctuation_boundary_marker stream
  - Position context for each codepoint (initial, medial, terminal, isolated)
```

**This evidence flows through:**
```text
SequenceContextTokenizer
  → TypedCodePoint (with position context trace)
  → ConditionedTypedSequence (with boundary preservation)
  → SlotCandidate (with alignment_ref and position trace)
  → SlotGeometryCandidate (inherits trace)
```

### 5.2 How Beginning/Ending Use Tokenizer Evidence

**Beginning rule checks:**
```text
1. Read position_context from SlotCandidate.trace_ids
2. Check position ∈ {initial, isolated}
3. Read boundary_context from trace
4. Verify no boundary violation
5. Read segment_context from trace
6. Verify INTRA_UTTERANCE
7. Produce gate:beginning:licensed
```

**Ending rule checks:**
```text
1. Read position_context from SlotCandidate.trace_ids
2. Check position ∈ {terminal, isolated}
3. Read boundary_context from trace
4. Verify boundary follows OR segment-terminal
5. Read segment_context from trace
6. Verify INTRA_UTTERANCE
7. Produce gate:ending:licensed
```

**FORBIDDEN:**
```text
❌ Re-tokenizing raw text
❌ Re-deriving position from codepoint index
❌ Re-computing boundaries from whitespace
❌ Bypassing SequenceContextTokenizer
```

**REQUIRED:**
```text
✓ Trust tokenizer evidence in trace
✓ Read position from trace_ids
✓ Respect boundary markers from tokenizer
✓ Preserve segment context from tokenizer
```

### 5.3 No Direct Text Access

**Beginning/Ending rules MUST NOT:**
- Access raw input text directly
- Re-scan for whitespace
- Re-classify boundaries
- Re-compute positions

**Beginning/Ending rules MUST:**
- Read ALL evidence from trace_ids
- Trust tokenizer's boundary analysis
- Preserve tokenizer's segment context
- Use tokenizer's position classification

---

## 6. Relationship to SlotGeometryCandidate trace_ids

**Every SlotGeometryCandidate inherits trace from its consumed SlotCandidates.**

### 6.1 Trace Inheritance

**For SlotGeometry length = 1 (Seed):**
```text
SlotGeometryCandidate.trace_ids ⊇ SlotCandidate.trace_ids

Required traces:
  - alignment_ref (from SlotCandidate)
  - position_context (from SequenceContextTokenizer)
  - boundary_context (from SequenceContextTokenizer)
  - segment_context (from SequenceContextTokenizer)
  - trace:beginning:licensed (from SlotGeometryBeginningRule)
  - trace:ending:licensed (from SlotGeometryEndingRule)
```

**For SlotGeometry length > 1 (Extended):**
```text
SlotGeometryCandidate.trace_ids ⊇
    SlotCandidate₁.trace_ids
  ∪ SlotCandidate₂.trace_ids
  ∪ ...
  ∪ SlotCandidateₙ.trace_ids
  ∪ SlotBindingEvidence₁.trace_ids
  ∪ ...
  ∪ SlotBindingEvidenceₙ₋₁.trace_ids

Required traces:
  - alignment_ref (from each SlotCandidate)
  - position_context (from each SlotCandidate's source)
  - boundary_context (from tokenizer)
  - segment_context (from tokenizer)
  - trace:beginning:licensed (from first SlotCandidate's beginning check)
  - trace:ending:licensed (from last SlotCandidate's ending check)
```

### 6.2 Beginning Trace Witness

**Beginning license must produce trace entry:**
```text
trace:beginning:{first_slot_identity}:licensed
```

**Example:**
```text
For SlotGeometry starting with BAA+FATHA:
  trace:beginning:slot_baa_fatha:licensed
```

**This trace entry is:**
- Added to SlotGeometryCandidate.trace_ids
- Preserved through all Extend steps
- Auditable at closure time
- NOT an identity (it's provenance)

### 6.3 Ending Trace Witness

**Ending license must produce trace entry:**
```text
trace:ending:{last_slot_identity}:licensed
```

**Example:**
```text
For SlotGeometry ending with MEEM+SUKUN:
  trace:ending:slot_meem_sukun:licensed
```

**This trace entry is:**
- Added to SlotGeometryCandidate.trace_ids
- Preserved at closure
- Auditable by later layers
- NOT an identity (it's provenance)

### 6.4 Trace Is Not Identity

**Per CLAUDE.md §4 invariants 1-3:**

```text
Identity is not trace.
Trace is not identity.
Evidence may add trace but must not consume identity.
```

**Application:**

```text
trace:beginning:licensed ∈ trace_ids ✓
trace:beginning:licensed ∉ identity_ids ✓

trace:ending:licensed ∈ trace_ids ✓
trace:ending:licensed ∉ identity_ids ✓

identity_ids ∩ trace_ids = ∅ (always)
```

**Forbidden:**
```text
❌ Treating beginning trace as identity
❌ Treating ending trace as identity
❌ Collapsing boundary evidence into identity
❌ Using trace to define meaning
```

---

## 7. Closure Integration

**Beginning and ending licenses are CLOSURE CONDITIONS.**

**Per `SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT.md` §3:**

### 7.1 Closure Condition §3.1: Licensed Beginning

```text
IsMinimallyComplete(SlotGeometryCandidate) requires:

  gate:beginning:licensed ∈ evidence claims
  OR
  trace:beginning:*:licensed ∈ trace_ids

If missing:
  IsMinimallyComplete = False
  Residual: defer:beginning_license_missing:present
```

### 7.2 Closure Condition §3.2: Licensed Ending

```text
IsMinimallyComplete(SlotGeometryCandidate) requires:

  gate:ending:licensed ∈ evidence claims
  OR
  trace:ending:*:licensed ∈ trace_ids

If missing:
  IsMinimallyComplete = False
  Residual: defer:ending_license_missing:present
```

### 7.3 Closure Does NOT Produce Meaning

**Even if both beginning and ending are licensed:**

```text
IsMinimallyComplete(G) = True
  → G is ready for next layer
  → G does NOT become WordCandidate
  → G does NOT become DalalahCandidate
  → G does NOT become FinalMeaning
```

**Beginning + Ending = READINESS, not MEANING:**

```text
Licensed beginning + Licensed ending + 6 other conditions
  = Minimal complete closure

Minimal complete closure ≠ Semantic finality
Minimal complete closure ≠ Word formation
Minimal complete closure ≠ Dalalah
Minimal complete closure ≠ Hukm
```

---

## 8. Forbidden Outputs

**SlotGeometryBeginningRule and SlotGeometryEndingRule MUST declare these in forbidden_outputs:**

```text
DalalahCandidate
WordCandidate
LafzCandidate
FinalMeaning
MeaningCandidate
IfadahCandidate
HukmCandidate
RealityClaim
FinalCaseJudgment
SentenceCandidate
ParagraphCandidate
DiscourseGeometryCandidate
TextGeometryCandidate
WordBoundaryCandidate
MorphologicalBoundaryCandidate
SemanticBoundaryCandidate
```

**Beginning/Ending MAY produce:**
```text
gate:beginning:licensed (evidence claim)
gate:ending:licensed (evidence claim)
trace:beginning:*:licensed (trace entry)
trace:ending:*:licensed (trace entry)
Blocking residual (فارق:beginning_blocked:* or فارق:ending_blocked:*)
Deferral residual (defer:beginning_evidence_insufficient or defer:ending_evidence_insufficient)
```

**Beginning/Ending MUST NOT produce:**
```text
New candidate types
Promoted candidates
Semantic interpretations
Word boundaries
Morphological boundaries
Dalalah content
Hukm inferences
Reality claims
```

---

## 9. Future Implementation Phases

**This contract authorizes ZERO implementation.**

**Future work (requires separate PRs with maintainer approval):**

### Phase 1: Beginning/Ending Rule Skeleton (Not Authorized)

```text
Implement SlotGeometryBeginningRule skeleton
Implement SlotGeometryEndingRule skeleton
Add minimal tests proving no forbidden outputs
Wire to SlotGeometryQiyas (if adapter exists)
```

**Required before:**
- Any closure checking involving beginning/ending

**Blocked until:**
- This contract merges
- Maintainer approves implementation PR

---

### Phase 2: Tokenizer Evidence Integration (Not Authorized)

```text
Read position_context from SlotCandidate.trace_ids
Read boundary_context from trace
Read segment_context from trace
Verify INTRA_UTTERANCE
Produce gate:beginning:licensed or gate:ending:licensed
Add constitutional tests (minimum 2: one for beginning, one for ending)
```

**Required before:**
- Beginning/Ending rules can license real geometries

**Blocked until:**
- Phase 1 complete
- Maintainer approves evidence integration PR

---

### Phase 3: Closure Integration (Not Authorized)

```text
Update IsMinimallyComplete to check §3.1 and §3.2
Add tests proving closure requires both beginning and ending
Add tests proving missing beginning blocks closure
Add tests proving missing ending blocks closure
Wire to SlotGeometryQiyas closure checking
```

**Required before:**
- Full closure checking

**Blocked until:**
- Phase 1 and 2 complete
- Maintainer approves closure integration PR

---

### Phase 4: Guard Tests for Constitutional Laws (Not Authorized)

```text
Test: Beginning does NOT produce WordCandidate
Test: Ending does NOT produce DalalahCandidate
Test: Beginning trace ∉ identity_ids
Test: Ending trace ∉ identity_ids
Test: Beginning reads tokenizer evidence, does NOT re-tokenize
Test: Ending reads tokenizer evidence, does NOT re-tokenize
Test: Seed produces both beginning AND ending licenses
Test: Extended geometry inherits beginning, produces new ending
Add to test_slot_geometry_beginning_ending_constitution.py
```

**Required before:**
- Constitutional compliance verification

**Blocked until:**
- Phase 1, 2, and 3 complete
- Maintainer approves guard test PR

---

## 10. Relationship to SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT.md

**This document is a DETAILING of closure conditions §3.1 and §3.2.**

**Closure contract defined:**
- §3.1 Licensed beginning (high-level requirement)
- §3.2 Licensed ending (high-level requirement)

**This document defines:**
- What "licensed beginning" means in detail (§2)
- What "licensed ending" means in detail (§3)
- Required evidence for beginning (§2.4)
- Required evidence for ending (§3.4)
- Relationship to tokenizer (§5)
- Relationship to trace (§6)
- Integration with closure (§7)

**Both are binding:**
- Closure contract provides framework
- This document provides detailed semantics
- Together they form complete beginning/ending law

---

## 11. Relationship to SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md

**Alignment-trace contract defined:**
- Seed and Extend operations (§3)
- SlotCandidate consumption contract (§2)
- Trace inheritance (§6.1)

**This document defines:**
- Beginning licensing for Seed (§2.6)
- Ending licensing for Seed (§3.6)
- Beginning requirement for first unit of Extend result (§2.6)
- Ending requirement for last unit of Extend result (§3.6)
- Trace entries for beginning/ending (§6)

**Together they form:**
```text
Alignment-trace: HOW SlotGeometry constructs
Beginning/Ending: WHERE SlotGeometry may start/stop
Closure: WHEN SlotGeometry is complete

All three required for complete SlotGeometry behavior.
```

---

## 12. No LCNV, Billing, or LogMeasurement Use

**LCNV Track B is closed by PR #68.**

**SlotGeometry beginning/ending MUST NOT:**
- Import from `src/qiyas_core/lcnv.py`
- Use LCNV pack() / unpack()
- Integrate with LogMeasurement
- Integrate with billing/product

**SlotGeometry beginning/ending is Track A only:**
- Pure qiyas algebraic layer
- No Track B integration
- No billing logic
- No logarithmic compression

**Per billing constitutional separation:**

```text
Payment opens access but does not alter truth.
Beginning/ending licenses must be identical for all users.
Subscription tier MUST NOT affect beginning/ending admissibility.
```

---

## 13. Glossary

| Term | Meaning |
|------|---------|
| SlotGeometryBeginningRule | Contract concept defining when a SlotCandidate may start a SlotGeometry; produces gate:beginning:licensed |
| SlotGeometryEndingRule | Contract concept defining when a SlotCandidate may terminate a SlotGeometry; produces gate:ending:licensed |
| Licensed beginning | Closure condition §3.1; requires gate:beginning:licensed in evidence or trace |
| Licensed ending | Closure condition §3.2; requires gate:ending:licensed in evidence or trace |
| Boundary evidence | Trace/provenance from SequenceContextTokenizer; NOT identity |
| Position context | Geometric position {initial, medial, terminal, isolated}; from tokenizer |
| Segment context | INTRA_UTTERANCE scope; from tokenizer |
| Beginning license | Admissibility gate; where SlotGeometry may start; NOT semantic content |
| Ending license | Stopping condition; where SlotGeometry may stop; NOT semantic finality |
| Seed case | SlotGeometry length = 1; requires BOTH beginning AND ending licenses |
| Extended case | SlotGeometry length > 1; beginning from first unit, ending from last unit |
| Readiness | Effect of closure; admissibility for next layer; NOT promotion to meaning |

---

## 14. Status and Authority

**Document status:**
- Constitutional contract
- Docs-only (no implementation)
- SlotGeometry-specific
- Details closure conditions §3.1 and §3.2

**Authority:**
- Once merged, this is the constitutional reference for:
  - Any future SlotGeometryBeginningRule implementation
  - Any future SlotGeometryEndingRule implementation
  - Any future beginning/ending evidence integration
  - Any future closure checking of beginning/ending conditions

**Does NOT authorize:**
- Implementation of SlotGeometryBeginningRule
- Implementation of SlotGeometryEndingRule
- Integration with IsMinimallyComplete runtime
- Any code/test/runtime changes

**Each implementation component requires:**
- Separate PR
- Maintainer approval
- Constitutional compliance check
- Tests proving all forbidden outputs

---

## 15. Non-Goals

**This document does NOT:**

- Modify `src/qiyas_core/`
- Modify `tests/qiyas_core/`
- Modify `run_qiyas.py`
- Modify `experimental/`
- Modify LCNV
- Modify billing/product documentation
- Modify Logarithmic Measurement
- Implement SlotGeometryBeginningRule runtime
- Implement SlotGeometryEndingRule runtime
- Implement IsMinimallyComplete runtime
- Implement MinimalCompletionReadinessCandidate
- Wire any runtime execution
- Add DalalahCandidate, WordCandidate, Meaning, Ifadah, or Hukm concepts
- Add new claim prefix, rank, or gate
- Authorize any future PR (each requires separate approval)
- Define WordBoundaryCandidate (forbidden)
- Define MorphologicalBoundaryCandidate (forbidden)
- Define SemanticBoundaryCandidate (forbidden)

---

## 16. Forbidden Jumps

**These jumps remain constitutional violations:**

```text
gate:beginning:licensed → WordCandidate (forbidden)
gate:ending:licensed → WordCandidate (forbidden)

Beginning license → Word beginning (forbidden)
Ending license → Word ending (forbidden)

Beginning license → Dalalah start (forbidden)
Ending license → Dalalah completion (forbidden)

Beginning license → Meaning start (forbidden)
Ending license → Semantic finality (forbidden)

Beginning + Ending → Word formation (forbidden)
Beginning + Ending → Complete meaning (forbidden)

Licensed beginning + Licensed ending → FinalMeaning (forbidden)
Licensed beginning + Licensed ending → HukmCandidate (forbidden)
```

**Beginning/Ending produce ONLY:**
```text
Readiness conditions (NOT semantic authority)
Licensing gates (NOT meaning content)
Trace evidence (NOT identity)
```

---

**End of document.**

**This is a constitutional contract.**
**No implementation is authorized by this PR.**
**Track A only.**
**LCNV (Track B) must NOT be touched.**
