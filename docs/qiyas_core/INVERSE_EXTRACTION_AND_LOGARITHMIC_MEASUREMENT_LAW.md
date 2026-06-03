# INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md

## Document Authority

**Status**: CONSTITUTIONAL
**Authority**: MANDATORY
**Scope**: All LCNV operations, measurement operations, and Candidate reconstruction
**Effective**: Immediately upon merge
**Supersedes**: None (this is a NEW governing law)
**Amends**: `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md` § 2.1 (Reversibility Requirement)

---

## 0. Critical Constitutional Correction

### 0.1 The Danger in PR #44

PR #44 introduced LCNV architecture with this formulation:

```
Unpack(Pack(x)) = x

∀ candidate c:
  Unpack(LCNV(c)) = c
```

**This formulation is constitutionally UNSAFE.**

**Why it's unsafe:**

This formulation creates an **internal contradiction** with Candidate primacy:

1. **Candidate primacy** states: Candidate is the source of truth, LCNV is encoding only
2. **The dangerous formulation** states: `Unpack(LCNV(c)) = c` — meaning LCNV alone can reconstruct full Candidate `c`
3. **Contradiction**: If LCNV alone can produce full Candidate, then LCNV becomes source of truth, not Candidate

**What breaks:**

- Candidate primacy
- Evidence preservation requirement (Evidence is not in LCNV)
- Trace preservation requirement (Full trace is not in LCNV)
- Source identity preservation (Source references are not in LCNV)
- Separation of encoding from semantic authority

### 0.2 The Constitutional Correction

**SAFE formulation:**

```
Unpack(Pack(c)) = EncodedCandidateStateProjection(c)

Where:
  EncodedCandidateStateProjection(c) contains:
    - Decoded gate states from LCNV layers
    - Layer structure (which layers were encoded)
    - Rank/residual encoding from LCNV
    - References to required stores

  EncodedCandidateStateProjection(c) does NOT contain:
    - Independent semantic authority
    - Complete evidence reconstruction
    - Full trace reconstruction
    - Source identity reconstruction
```

**Full Candidate reconstruction requires:**

```python
projection = Unpack(LCNV(c))
candidate = ReconstructCandidate(
    projection,           # Gate states + structure from LCNV
    candidate_store,      # Source of truth for Candidates
    evidence_store,       # Source of truth for Evidence
    trace_store          # Source of truth for Trace
)
```

**Governing constraint:**

```
LCNV is NOT source of truth.
Candidate is source of truth.
LCNV is reversible ENCODING of gate states only.
Full reconstruction requires stores.
```

---

## 1. Inverse Extraction Law

### 1.1 Definition

**Inverse extraction** is the operation:

```
LCNV⁻¹: ℕ → GateStateBundle
```

Where:
- Input: Compressed numeric value (LCNV)
- Output: Bundle of decoded gate states

**NOT:**

```
LCNV⁻¹: ℕ → Meaning
LCNV⁻¹: ℕ → Hukm
LCNV⁻¹: ℕ → Candidate (with full authority)
```

### 1.2 GateStateBundle Structure

```python
@dataclass(frozen=True)
class GateStateBundle:
    """
    Result of inverse LCNV extraction.

    Contains ONLY decoded gate states, NOT semantic content.
    """
    mclo_state: int                    # MCLO block value
    lexical_only_state: int            # LexicalOnly block value
    meaning_only_state: int            # MeaningOnly block value
    binding_gate: GateState            # OPEN/CLOSED/BLOCK
    mutabaqah_gate: GateState          # OPEN/CLOSED/BLOCK
    tadammun_gate: GateState           # OPEN/CLOSED/BLOCK
    iltizam_gate: GateState            # OPEN/CLOSED/BLOCK
    rank_residual_state: int           # Rank/residual encoding

    # Required for full Candidate reconstruction:
    candidate_store_ref: Optional[CandidateStoreRef] = None
    evidence_store_ref: Optional[EvidenceStoreRef] = None
    trace_store_ref: Optional[TraceStoreRef] = None

    def requires_stores_for_candidate(self) -> bool:
        """Always returns True."""
        return True
```

### 1.3 Inverse Extraction Laws

**Law 1.1: Projection-Only Output**

```
∀ n ∈ LCNV:
  LCNV⁻¹(n) = GateStateBundle

GateStateBundle ≠ Candidate
GateStateBundle ≠ Meaning
GateStateBundle ≠ Hukm
```

**Law 1.2: Store Requirement**

```
∀ bundle ∈ GateStateBundle:
  ToCandidate(bundle) requires:
    - CandidateStore (source of truth for Candidates)
    - EvidenceStore (source of truth for Evidence)
    - TraceStore (source of truth for Trace)
```

**Law 1.3: No Independent Authority**

```
∀ bundle ∈ GateStateBundle:
  bundle.has_semantic_authority() = False
  bundle.is_source_of_truth() = False
  bundle.is_encoding_only() = True
```

**Law 1.4: Reversibility Constraint**

```
∀ c ∈ Candidate:
  projection = Unpack(Pack(c))
  projection ∈ EncodedCandidateStateProjection
  projection ≠ c

  ReconstructCandidate(projection, stores) = c
  where stores = (CandidateStore, EvidenceStore, TraceStore)
```

---

## 2. Logarithmic Measurement Law

### 2.1 Purpose

Logarithmic measurement converts multiplicative relationships into additive relationships for certain **licensed positive measured quantities**.

**NOT for:**
- Gate states (OPEN/CLOSED/BLOCK are not measured quantities)
- LCNV values (numeric encodings, not measured quantities)
- Blocked states (blocked = no measurement)
- Negative values (log undefined for ≤ 0)

### 2.2 Logarithmic Law Constraints

**Law 2.1: No Log of Gate States**

```
∀ gate ∈ {OPEN, CLOSED, BLOCK}:
  log(gate) is FORBIDDEN

Reason: Gates are not measured quantities.
```

**Law 2.2: No Log of LCNV**

```
∀ n ∈ LCNV:
  log(n) is FORBIDDEN unless n represents a licensed measured quantity

Reason: LCNV is an encoding, not a measured quantity.
```

**Law 2.3: No Log of CLOSED**

```
∀ quantity q where Gate(q) = CLOSED:
  log(q) is FORBIDDEN

Reason: CLOSED = no path = no measurement.
```

**Law 2.4: No Log of BLOCK**

```
∀ quantity q where Gate(q) = BLOCK:
  log(q) is FORBIDDEN

Reason: BLOCK = invalidating difference = no licensed measurement.
```

**Law 2.5: Log Only of Positive Licensed Quantities**

```
log(x) is PERMITTED only when:
  1. x > 0
  2. x ∈ LicensedMeasuredQuantity
  3. Gate(x) = OPEN
  4. x has evidence of measurement licensing

Common form:
  log(1 + x) where x ∈ ℝ⁺ and Gate(x) = OPEN
```

### 2.3 Examples

**FORBIDDEN:**

```python
# Gate states are not measurable
log(OPEN)       # FORBIDDEN
log(CLOSED)     # FORBIDDEN
log(BLOCK)      # FORBIDDEN

# LCNV is encoding, not measured quantity
lcnv_value = 12345
log(lcnv_value) # FORBIDDEN (unless explicitly licensed)

# Blocked quantities have no measurement
q = BlockedQuantity(...)
log(q)          # FORBIDDEN

# Closed gates have no path
if gate == CLOSED:
    log(quantity)  # FORBIDDEN
```

**PERMITTED:**

```python
# Licensed positive measured quantity with open gate
rank_measure = compute_rank_measure(candidate)  # returns ℝ⁺
if rank_measure.gate == OPEN and rank_measure > 0:
    log_rank = log(1 + rank_measure)  # PERMITTED

# Distance measure with licensing evidence
distance = compute_licensed_distance(c1, c2)
if distance.is_licensed() and distance.gate == OPEN:
    log_distance = log(1 + distance)  # PERMITTED
```

---

## 3. Block-Specific Constraints

### 3.1 LexicalOnly Block

**Constitutional Definition:**

```
LexicalOnly = LafziSignifiedOnly
```

**NOT:**

```
LexicalOnly ≠ SemanticMeaning
LexicalOnly ≠ ConceptualMeaning
LexicalOnly ≠ Hukm
```

**Constraint:**

```
LexicalOnly encodes:
  - Lexical signified (madlul lafzi)
  - Morphological structure
  - Root form
  - Pattern (wazn)
  - Lexical category

LexicalOnly does NOT encode:
  - Semantic meaning (ma'na)
  - Conceptual content
  - Hukm
  - Binding relationships (those are in gates)
  - Evidence (those are in EvidenceStore)
```

### 3.2 MeaningOnly Block

**Constitutional Definition:**

```
MeaningOnly = SingularLexicalMadlulCandidate
  where:
    PTI_force = POTENTIAL_ONLY
    PTI_computed = FORBIDDEN
```

**NOT:**

```
MeaningOnly ≠ FinalMeaning
MeaningOnly ≠ AuthoritativeMeaning
MeaningOnly ≠ Hukm
```

**Constraint:**

```
MeaningOnly encodes:
  - Singular lexical madlul candidate
  - Potential interpretation only
  - No computed PTI
  - No authoritative meaning claim

MeaningOnly does NOT encode:
  - Final meaning (meaning requires full Candidate + Evidence + context)
  - Hukm (hukm requires authorized legal reasoning)
  - Binding force (those are in gates)
  - Computed PTI (forbidden by PTI_computed = FORBIDDEN)
```

### 3.3 MCLO Block (SignifierOnlyValue)

**Constitutional Definition:**

```
MCLO = SignifierOnlyValue
```

**Broader than Abjad:**

```
SignifierOnlyValue may encode:
  - Abjad value (traditional)
  - Glyph numeric encoding
  - Unicode scalar value
  - Other signifier-level numeric representations

SignifierOnlyValue does NOT encode:
  - Meaning
  - Hukm
  - Evidence
  - Gate states (those are in separate layers)
```

**Constraint:**

```
MCLO block constraints:
  1. Must be reversible to signifier representation
  2. Must not encode semantic content
  3. Must not encode gate states
  4. Must preserve signifier identity
  5. May use various numeric encoding schemes (not limited to Abjad)
```

---

## 4. Implementation Constraints

### 4.1 Unpack Function Signature

**CORRECT:**

```python
def unpack(lcnv: LCNV) -> EncodedCandidateStateProjection:
    """
    Unpack LCNV into gate state projection.

    Returns:
        EncodedCandidateStateProjection containing:
          - Decoded gate states
          - Layer structure
          - Rank/residual encoding
          - Store references (if available)

    Does NOT return:
        - Independent Candidate with full authority
        - Complete evidence reconstruction
        - Full trace reconstruction
        - Semantic meaning

    For full Candidate reconstruction:
        projection = unpack(lcnv)
        candidate = reconstruct_candidate(
            projection,
            candidate_store,
            evidence_store,
            trace_store
        )
    """
    # Extract layers
    mclo = extract_mclo_block(lcnv)
    lexical_only = extract_lexical_only_block(lcnv)
    meaning_only = extract_meaning_only_block(lcnv)
    binding_gate = extract_binding_gate(lcnv)
    mutabaqah_gate = extract_mutabaqah_gate(lcnv)
    tadammun_gate = extract_tadammun_gate(lcnv)
    iltizam_gate = extract_iltizam_gate(lcnv)
    rank_residual = extract_rank_residual(lcnv)

    return EncodedCandidateStateProjection(
        mclo_state=mclo,
        lexical_only_state=lexical_only,
        meaning_only_state=meaning_only,
        binding_gate=binding_gate,
        mutabaqah_gate=mutabaqah_gate,
        tadammun_gate=tadammun_gate,
        iltizam_gate=iltizam_gate,
        rank_residual_state=rank_residual,
        requires_stores=True  # ALWAYS True
    )
```

**INCORRECT:**

```python
def unpack(lcnv: LCNV) -> Candidate:  # FORBIDDEN
    """This violates Candidate primacy."""
    pass
```

### 4.2 Reconstruct Candidate Function Signature

**CORRECT:**

```python
def reconstruct_candidate(
    projection: EncodedCandidateStateProjection,
    candidate_store: CandidateStore,
    evidence_store: EvidenceStore,
    trace_store: TraceStore
) -> Candidate:
    """
    Reconstruct full Candidate from projection + stores.

    Args:
        projection: Gate state projection from LCNV
        candidate_store: Source of truth for Candidates
        evidence_store: Source of truth for Evidence
        trace_store: Source of truth for Trace

    Returns:
        Full Candidate with:
          - Identity (from stores)
          - Evidence (from evidence_store)
          - Trace (from trace_store)
          - Gate states (from projection)
    """
    # Retrieve base candidate from store
    candidate_id = projection.get_candidate_ref()
    base_candidate = candidate_store.get(candidate_id)

    # Retrieve evidence
    evidence = evidence_store.get_for_candidate(candidate_id)

    # Retrieve trace
    trace = trace_store.get_for_candidate(candidate_id)

    # Reconstruct with gate states from projection
    return Candidate(
        identity=base_candidate.identity,
        evidence=evidence,
        trace=trace,
        binding_gate=projection.binding_gate,
        mutabaqah_gate=projection.mutabaqah_gate,
        tadammun_gate=projection.tadammun_gate,
        iltizam_gate=projection.iltizam_gate,
        rank=compute_rank_from_residual(projection.rank_residual_state),
        # ... other fields
    )
```

### 4.3 Logarithmic Measurement Guards

**CORRECT:**

```python
def compute_log_measure(quantity: MeasuredQuantity) -> Optional[float]:
    """
    Compute logarithmic measure with constitutional guards.

    Returns:
        log(1 + quantity) if licensed and permitted
        None if forbidden or blocked
    """
    # Guard 1: Check gate state
    if quantity.gate != GateState.OPEN:
        return None  # CLOSED or BLOCK = no log

    # Guard 2: Check licensing
    if not quantity.is_licensed():
        return None  # Unlicensed = no log

    # Guard 3: Check positivity
    if quantity.value <= 0:
        return None  # Non-positive = no log

    # Guard 4: Check type
    if not isinstance(quantity, LicensedMeasuredQuantity):
        return None  # Wrong type = no log

    # All guards passed: compute log
    return math.log(1 + quantity.value)
```

**INCORRECT:**

```python
def compute_log_measure_WRONG(lcnv: LCNV) -> float:
    """FORBIDDEN: taking log of encoding."""
    return math.log(lcnv)  # CONSTITUTIONAL VIOLATION
```

---

## 5. Governing Laws Summary

### 5.1 Inverse Extraction Laws

```
Law I.1: Unpack returns EncodedCandidateStateProjection, NOT Candidate
Law I.2: Full Candidate reconstruction requires stores
Law I.3: GateStateBundle has no independent semantic authority
Law I.4: LCNV is encoding only, NOT source of truth
Law I.5: Candidate is source of truth, NOT LCNV
```

### 5.2 Logarithmic Measurement Laws

```
Law L.1: log(gate_state) is FORBIDDEN
Law L.2: log(LCNV) is FORBIDDEN (unless explicitly licensed as measured quantity)
Law L.3: log(CLOSED) is FORBIDDEN
Law L.4: log(BLOCK) is FORBIDDEN
Law L.5: log(x) permitted only when x > 0 ∧ x ∈ LicensedMeasuredQuantity ∧ Gate(x) = OPEN
```

### 5.3 Block Constraint Laws

```
Law B.1: LexicalOnly = LafziSignifiedOnly (NOT semantic meaning)
Law B.2: MeaningOnly = SingularLexicalMadlulCandidate (PTI_force=POTENTIAL_ONLY, PTI_computed=FORBIDDEN)
Law B.3: MCLO = SignifierOnlyValue (broader than Abjad)
```

---

## 6. Cross-References

### 6.1 Amends

This document **AMENDS**:

- `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md` § 2.1
  - Replaces: `Unpack(Pack(x)) = x`
  - With: `Unpack(Pack(x)) = EncodedCandidateStateProjection(x)`

### 6.2 Depends On

This document **DEPENDS ON**:

- `PROJECT_MATHEMATICAL_FOUNDATION.md` (Candidate primacy, identity preservation)
- `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md` (LCNV structure)
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` (Layer separation, no layer jumping)

### 6.3 Required By

This document is **REQUIRED BY**:

- All LCNV runtime implementations
- All MCLO prototype implementations
- All measurement operations involving logarithms
- All Candidate reconstruction operations

---

## 7. Authority and Enforcement

### 7.1 Constitutional Status

This document has **CONSTITUTIONAL** status.

All code MUST comply with these laws.

**Enforcement:**

```
Any code that violates these laws is constitutionally invalid,
even if all tests pass.
```

### 7.2 Violation Examples

**VIOLATION 1: Direct Candidate from LCNV**

```python
# FORBIDDEN
def unpack(lcnv: LCNV) -> Candidate:
    return Candidate(...)  # CONSTITUTIONAL VIOLATION
```

**VIOLATION 2: Log of Gate State**

```python
# FORBIDDEN
log_value = math.log(GateState.OPEN)  # CONSTITUTIONAL VIOLATION
```

**VIOLATION 3: Log of LCNV without Licensing**

```python
# FORBIDDEN
lcnv_value = 12345
log_lcnv = math.log(lcnv_value)  # CONSTITUTIONAL VIOLATION
```

**VIOLATION 4: Log of CLOSED/BLOCK**

```python
# FORBIDDEN
if quantity.gate == GateState.CLOSED:
    log_q = math.log(quantity)  # CONSTITUTIONAL VIOLATION
```

### 7.3 Compliance Check

Before ANY LCNV runtime or MCLO prototype:

1. ✓ Does `unpack()` return `EncodedCandidateStateProjection`?
2. ✓ Does Candidate reconstruction require stores?
3. ✓ Are logarithms guarded against gates/encodings/blocks?
4. ✓ Is LexicalOnly = LafziSignifiedOnly (not semantic)?
5. ✓ Is MeaningOnly = SingularLexicalMadlulCandidate (potential only)?
6. ✓ Is MCLO = SignifierOnlyValue (broader than Abjad)?

**All must be YES before proceeding with runtime implementation.**

---

## 8. Rationale

### 8.1 Why This Correction Is Necessary

**The Problem:**

PR #44 introduced `Unpack(Pack(x)) = x`, which implies:
- LCNV alone can reconstruct full Candidate
- LCNV becomes source of truth
- Evidence, Trace, and source identity are somehow encoded in a single integer

This is **architecturally impossible** and **constitutionally invalid**.

**The Solution:**

Separate:
1. **Encoding** (LCNV) from **source of truth** (Candidate/Evidence/Trace stores)
2. **Gate state projection** (what LCNV can provide) from **full reconstruction** (requires stores)
3. **Measured quantities** (can have log) from **encodings/gates/blocks** (cannot have log)

### 8.2 Why Stores Are Required

**Candidate contains:**
- Identity (preserved from source)
- Evidence (proofs, not just states)
- Trace (full history, not just current state)
- Source references (where did this come from?)

**LCNV contains:**
- Gate states (OPEN/CLOSED/BLOCK)
- Layer block values (MCLO, LexicalOnly, MeaningOnly)
- Rank/residual encoding

**LCNV does NOT contain:**
- Full evidence chains
- Complete trace history
- Source identity references
- Semantic authority

Therefore: **Stores are mandatory for full reconstruction.**

### 8.3 Why Logarithm Guards Are Necessary

**Gates are not measured quantities.**

```
OPEN = path exists (not a measurement)
CLOSED = no path (not a measurement)
BLOCK = invalidating difference (not a measurement)
```

**LCNV is an encoding, not a measured quantity.**

```
LCNV = compressed numeric representation of gate states
LCNV ≠ distance, similarity, rank, or other measured property
```

**Logarithms apply only to licensed positive measured quantities with open gates.**

---

## 9. Migration Guide

### 9.1 For Existing Code (None Yet)

There is no existing LCNV runtime code to migrate.

This document establishes the **correct** formulation before any runtime is built.

### 9.2 For Future Implementation

When implementing LCNV runtime:

**Step 1: Implement EncodedCandidateStateProjection**

```python
@dataclass(frozen=True)
class EncodedCandidateStateProjection:
    mclo_state: int
    lexical_only_state: int
    meaning_only_state: int
    binding_gate: GateState
    mutabaqah_gate: GateState
    tadammun_gate: GateState
    iltizam_gate: GateState
    rank_residual_state: int
    candidate_store_ref: Optional[CandidateStoreRef] = None
    evidence_store_ref: Optional[EvidenceStoreRef] = None
    trace_store_ref: Optional[TraceStoreRef] = None
    requires_stores: bool = True  # ALWAYS True
```

**Step 2: Implement Stores**

```python
class CandidateStore:
    def get(self, candidate_id: CandidateID) -> Candidate: ...

class EvidenceStore:
    def get_for_candidate(self, candidate_id: CandidateID) -> Evidence: ...

class TraceStore:
    def get_for_candidate(self, candidate_id: CandidateID) -> Trace: ...
```

**Step 3: Implement Unpack (Projection Only)**

```python
def unpack(lcnv: LCNV) -> EncodedCandidateStateProjection:
    # Extract layers, return projection
    # Do NOT return Candidate
    pass
```

**Step 4: Implement Reconstruct (Projection + Stores → Candidate)**

```python
def reconstruct_candidate(
    projection: EncodedCandidateStateProjection,
    candidate_store: CandidateStore,
    evidence_store: EvidenceStore,
    trace_store: TraceStore
) -> Candidate:
    # Combine projection with stores
    # Return full Candidate
    pass
```

**Step 5: Implement Logarithmic Guards**

```python
def compute_log_measure(quantity: MeasuredQuantity) -> Optional[float]:
    if quantity.gate != GateState.OPEN:
        return None
    if not quantity.is_licensed():
        return None
    if quantity.value <= 0:
        return None
    return math.log(1 + quantity.value)
```

---

## 10. Constitutional Seal

**This document corrects a constitutional gap in PR #44.**

**Before this correction:**
- Risk: LCNV could be misinterpreted as source of truth
- Risk: Stores could be seen as optional
- Risk: Logarithms could be applied to gates/encodings/blocks

**After this correction:**
- LCNV is explicitly encoding only
- Stores are explicitly mandatory
- Logarithms are explicitly guarded

**Status:** MANDATORY before any LCNV runtime or MCLO prototype implementation.

**Authority:** This document amends `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md` and establishes new governing laws for inverse extraction and logarithmic measurement.

---

## End of Document

**Document ID:** `INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md`
**Version:** 1.0
**Date:** 2026-06-03
**Status:** CONSTITUTIONAL
**Authority:** MANDATORY
