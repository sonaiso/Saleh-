# LAYERED COMPRESSED NUMERIC VALUE ARCHITECTURE

> **النظام العددي الطبقي القابل للفك**
>
> **Layered Compressed Numeric Value (LCNV) System**

---

## 0. Constitutional Authority

**This document establishes constitutional constraints on numeric encoding of qiyas layer state.**

**Authority:**
- Below: PROJECT_MATHEMATICAL_FOUNDATION.md (defines algebraic qiyas system)
- Below: CANONICAL_ARCHITECTURE_CONTROL_FRAME.md (defines layer architecture)
- Above: All runtime numeric encoding implementations

**Purpose:**
- Define what numeric encoding IS permitted (reversible state compression)
- Define what numeric encoding is FORBIDDEN (semantic derivation, meaning extraction, hukm production)

**Why this document exists NOW:**

After PR #43, Layer 2 coordinate slice has proper glyph gate and specific residuals. This makes it safe to define how numeric values may compress layer state **without creating semantic meaning**.

**The risk this prevents:**
```
❌ MCLO → Meaning
❌ AbjadValue → SemanticRoot
❌ LogScore → Hukm
❌ NumericBlock → RankUpgrade
❌ CompressedValue replacing Candidate as source-of-truth
```

---

## 1. Core Definition

### 1.1 What LCNV Is

**LCNV (Layered Compressed Numeric Value) is:**

> A reversible, gate-aware, rank-aware, residual-aware numeric encoding of a licensed qiyas layer state.

**Formal definition:**

```
LCNV(u) =
  [MCLO]
  [LexicalOnly]
  [MeaningOnly]
  [Binding]
  [Mutabaqah]
  [Tadammun]
  [Iltizam]
  [RankResidual]

where each block is:
- either CLOSED (gate not opened)
- or contains numeric encoding of that layer's licensed state
```

### 1.2 What LCNV Is NOT

**LCNV is NOT:**
- ❌ A source of truth (Candidate is source of truth)
- ❌ A meaning derivation system
- ❌ A hukm inference system
- ❌ A rank elevation mechanism
- ❌ A semantic interpretation of numbers
- ❌ A replacement for evidence-based qiyas
- ❌ A final value (it is always candidate/potential)

---

## 2. Fundamental Laws

### Law 1: Inverse Law (EncodedStateProjection, NOT Candidate)

```
LCNV inverse law:

Unpack(Pack(c)) ≠ Candidate(c)

Unpack(Pack(c)) = EncodedStateProjection(c)
```

**More precise formulation:**

```
Pack(c) does not compress the full authoritative Candidate,
but compresses a licensed projection of its state.

Unpack(Pack(c)) does not restore Candidate,
but restores EncodedStateProjection(c).

CandidateAuthority is NOT restored through unpacking alone,
but only through:
  EncodedStateProjection
  + CandidateStore
  + EvidenceStore
  + TraceStore
  + ResidualStore
  + Validation
```

**Algebraic formulation:**

```
CandidateAuthority(c)
≠ Unpack(Pack(c))

CandidateAuthority(c)
= Validate(
    EncodedStateProjection(c),
    CandidateStore,
    EvidenceStore,
    TraceStore,
    ResidualStore
  )
```

**Constitutional principle:**

```
LCNV is reversible within projection bounds,
NOT reversible within epistemological authority bounds.
```

**In Arabic:**

```
العكس في LCNV يفكّ ترميز حالة مرخّصة،
ولا يستردّ المرشح بوصفه أصلًا أو حجة أو مصدر حقيقة.
```

**Translation:**

```
Inverse in LCNV unpacks licensed state encoding,
and does NOT restore the Candidate as origin, proof, or source of truth.
```

**Reason:** If unpacking produced authoritative Candidate, numeric encoding would become a source of truth, violating Candidate primacy. LCNV encodes state; it does NOT create epistemological authority.

**Implication:** LCNV is reversible for state reconstruction but requires validation and store reunification for authority restoration.

### Law 2: Candidate Primacy

```
Candidate = source of truth
LCNV = reversible encoding of licensed state

Candidate.identity_ids ≠ LCNV(Candidate)
Candidate.evidence ≠ LCNV(Candidate)
Candidate.rank ≠ LCNV(Candidate)
Candidate.residuals ≠ LCNV(Candidate)

LCNV encodes state.
LCNV does NOT create state.
```

**Implication:** LCNV may only exist AFTER a Candidate has been licensed through qiyas. LCNV cannot produce a Candidate.

### Law 3: Gate Awareness

```
Closed block = gate not opened
Closed block ≠ zero meaning
Closed block ≠ absence of value

If Gate(layer) is not opened:
  LCNV[layer] = CLOSED

If Gate(layer) is opened and licensed:
  LCNV[layer] = Encode(licensed_state)
```

**Example:**

```
Input: LetterIdentityCarrier(BAA) with no lexical licensing yet

LCNV(BAA) =
  [MCLO(BAA:2)]        ← SignifierOnly block filled
  [CLOSED]             ← LexicalOnly block not opened
  [CLOSED]             ← MeaningOnly block not opened
  [CLOSED]             ← Binding block not opened
  [CLOSED]             ← Mutabaqah block not opened
  [CLOSED]             ← Tadammun block not opened
  [CLOSED]             ← Iltizam block not opened
  [RANK(CERTAIN)]      ← Rank encoded
```

**CRITICAL:** CLOSED ≠ 0. CLOSED means "this gate has not been opened, no licensed transition exists yet."

### Law 4: Semantic Force Prohibition

```
semantic_force = FORBIDDEN

∀ numeric block in LCNV:
  Block.semantic_force = FORBIDDEN

No numeric block may produce:
- MeaningCandidate
- IfadahCandidate
- HukmCandidate
- DalalahVector
- RealityClaim
- RankUpgrade
```

**Specifically forbidden:**

```
❌ Abjad(ب) = 2 → "ب means duality"
❌ Abjad(ب) = 2 → "ب is second in importance"
❌ MCLO(ب) = X → "ب has semantic value X"
❌ MCLO(ب) = X → Root(ب) without lexical qiyas
❌ LowCost(candidate) → higher rank
❌ HighCost(candidate) → blocked candidate
```

**Only permitted:**

```
✓ Abjad(ب) = 2 (conventional coordinate)
✓ MCLO(ب) = X (reversible signifier-only encoding)
✓ LowCost(candidate) → tarjih hint WITHIN same rank
✓ HighCost(candidate) → residual penalty measure
```

### Law 5: Block Ordering Dependency

```
No Mutabaqah/Tadammun/Iltizam before Binding.

LCNV[Mutabaqah] requires LCNV[Binding] ≠ CLOSED
LCNV[Tadammun] requires LCNV[Binding] ≠ CLOSED
LCNV[Iltizam] requires LCNV[Binding] ≠ CLOSED

Reason:
  Correspondence/inclusion/entailment relationships
  require licensed compositional binding first.
```

### Law 6: Rank-Residual Preservation

```
LCNV[RankResidual] must encode:
- Rank ceiling (meet semantics)
- Residual count
- Blocking vs non-blocking residuals

LCNV does NOT:
- Eliminate residuals
- Hide blocking residuals
- Upgrade rank by numeric manipulation
```

### Law 7: Forbidden Derivations from Unpack(LCNV)

**Explicitly forbidden derivations:**

```
Unpack(LCNV) ⇏ CandidateAuthority
Unpack(LCNV) ⇏ Meaning
Unpack(LCNV) ⇏ Ifadah
Unpack(LCNV) ⇏ Hukm
Unpack(LCNV) ⇏ RealityClaim
Unpack(LCNV) ⇏ Evidence
Unpack(LCNV) ⇏ Trace
```

**The ONLY permitted derivation:**

```
Unpack(LCNV) → EncodedStateProjection
EncodedStateProjection → GateStateBundle
```

**For authoritative restoration:**

```
GateStateBundle
+ Stores
+ Validation
→ CandidateAuthority
```

**The governing principle:**

```
Candidate هو مصدر السلطة.
LCNV أثر مضغوط.
الأثر لا يصبح أصلًا.
والرقم لا ينتج معرفة.
```

**Translation:**

```
Candidate is the source of authority.
LCNV is compressed trace.
Trace does not become origin.
Number does not produce knowledge.
```

---

## 3. LCNV Block Specification

### 3.1 MCLO (Signifier-Only Coordinate Numeric License)

**What it is:**
```
MCLO = numeric encoding of signifier identity
     = conventional coordinate (e.g., Abjad value)
     + positional coordinate (if applicable)
     + script variant coordinate (if applicable)
```

**What it contains:**
- Letter identity coordinate (e.g., Abjad value)
- Haraka function coordinate
- Position coordinate
- Alignment coordinate
- **NO lexical meaning**
- **NO semantic derivation**

**Constitutional constraint:**
```
MCLO fills SignifierOnly block ONLY.

MCLO.semantic_force = FORBIDDEN
MCLO.layer = SIGNIFIER_ONLY
MCLO.meaning_force = CLOSED
```

**Critical law:**

```
MCLO لا يحسب قيمة لدال لم يعبر glyph gate.

(MCLO must not compute a value for a signifier
 that has not crossed the glyph gate.)
```

**Example:**

```python
# ALLOWED:
MCLO(ب) = conventional_coordinate(2, "ABJAD")

# FORBIDDEN:
MCLO(ب) → Root(ب)
MCLO(ب) → Meaning(ب)
MCLO(ب) → Hukm based on numeric value
```

### 3.2 LexicalOnly Block

**What it is:**
```
LexicalOnly = numeric encoding of lexical attestation state
            = root/form licensing state (not final meaning)
```

**Gate requirement:**
```
Requires: LexicalAttestationGate opened
Requires: RootWeightAlgebra licensing
Requires: WordFormCandidate exists
```

**Does NOT contain:**
- Final meaning
- Compositional meaning
- Hukm

**Contains:**
- Root identity encoding
- Weight pattern encoding
- Lexical attestation level

### 3.3 MeaningOnly Block

**What it is:**
```
MeaningOnly = numeric encoding of lexical signified state
            = mutabaqah/tadammun/iltizam potential
            = polysemy/metaphor/transfer state
```

**Gate requirement:**
```
Requires: WadhScopeGate opened
Requires: DalalahTypeGate opened
Requires: LexicalMadlulCandidate exists
```

**Does NOT contain:**
- Compositional ifadah
- Hukm
- Truth value

**Contains:**
- Lexical meaning coordinate
- Polysemy residual encoding
- Metaphor/transfer licensing state

### 3.4 Binding Block

**What it is:**
```
Binding = numeric encoding of compositional binding state
        = amil/maamul licensing
        = agreement/reference licensing
```

**Gate requirement:**
```
Requires: CompositionGate opened
Requires: BindingEvidence exists
Requires: SlotGeometry licensed
```

**Contains:**
- Binding relationship encoding
- Agreement pattern encoding
- Reference closure state

### 3.5 Mutabaqah/Tadammun/Iltizam Blocks

**What they are:**
```
Mutabaqah = correspondence relationship encoding
Tadammun = inclusion relationship encoding
Iltizam = entailment relationship encoding
```

**Gate requirement:**
```
Requires: Binding block ≠ CLOSED
Requires: DalalahVector licensed
```

**Constitutional constraint:**
```
These blocks remain CLOSED until licensed Binding exists.

No mutabaqah before composition.
No tadammun before composition.
No iltizam before composition.
```

### 3.6 RankResidual Block

**What it is:**
```
RankResidual = encoding of:
  - Rank ceiling (CERTAIN, STRONG, WEAK, HYPOTHETICAL)
  - Residual count
  - Blocking residual flag
  - Deferred state count
```

**Does NOT:**
- Eliminate residuals
- Hide blocking residuals
- Allow rank upgrade by numeric manipulation

**Contains:**
```
rank_value: int (4=CERTAIN, 3=STRONG, 2=WEAK, 1=HYPOTHETICAL)
residual_count: int
blocking_count: int
deferred_count: int
```

---

## 4. Pack/Unpack Specification

### 4.1 Pack Operation

```python
def pack(candidate: Candidate) -> LCNV:
    """
    Encode candidate state into LCNV.

    Preconditions:
    - candidate must be licensed through qiyas
    - candidate must have identity_ids
    - candidate must have evidence
    - candidate must have rank

    Returns:
    - Reversible numeric encoding of layer state

    Guarantees:
    - Unpack(Pack(c)) = c
    - semantic_force = FORBIDDEN for all blocks
    - CLOSED blocks where gates not opened
    """
    return LCNV(
        mclo=encode_signifier(candidate) if has_signifier_gate(candidate) else CLOSED,
        lexical=encode_lexical(candidate) if has_lexical_gate(candidate) else CLOSED,
        meaning=encode_meaning(candidate) if has_meaning_gate(candidate) else CLOSED,
        binding=encode_binding(candidate) if has_binding_gate(candidate) else CLOSED,
        mutabaqah=encode_mutabaqah(candidate) if has_binding_gate(candidate) else CLOSED,
        tadammun=encode_tadammun(candidate) if has_binding_gate(candidate) else CLOSED,
        iltizam=encode_iltizam(candidate) if has_binding_gate(candidate) else CLOSED,
        rank_residual=encode_rank_residual(candidate),
    )
```

### 4.2 Unpack Operation

```python
def unpack(lcnv: LCNV) -> EncodedStateProjection:
    """
    Decode LCNV to EncodedStateProjection (NOT full Candidate).

    Preconditions:
    - lcnv must have been produced by pack()
    - lcnv must preserve structure

    Returns:
    - EncodedStateProjection with:
      - Gate state bundle
      - Encoded layer states
      - Rank/residual encoding
      - NOT: CandidateAuthority
      - NOT: Full evidence
      - NOT: Full trace
      - NOT: Source-of-truth status

    Guarantees:
    - Unpack(Pack(c)) = EncodedStateProjection(c)
    - Unpack(Pack(c)) ≠ Candidate(c)
    - Layer structure preserved
    - State reconstruction possible
    - Authority NOT restored
    """
    return EncodedStateProjection(
        gate_state_bundle=decode_gate_states(lcnv),
        signifier=decode_signifier(lcnv.mclo) if lcnv.mclo != CLOSED else None,
        lexical=decode_lexical(lcnv.lexical) if lcnv.lexical != CLOSED else None,
        meaning=decode_meaning(lcnv.meaning) if lcnv.meaning != CLOSED else None,
        binding=decode_binding(lcnv.binding) if lcnv.binding != CLOSED else None,
        mutabaqah=decode_mutabaqah(lcnv.mutabaqah) if lcnv.mutabaqah != CLOSED else None,
        tadammun=decode_tadammun(lcnv.tadammun) if lcnv.tadammun != CLOSED else None,
        iltizam=decode_iltizam(lcnv.iltizam) if lcnv.iltizam != CLOSED else None,
        rank_residual=decode_rank_residual(lcnv.rank_residual),
    )
```

### 4.3 Authoritative Restoration

```python
def restore_candidate_authority(
    projection: EncodedStateProjection,
    candidate_store: CandidateStore,
    evidence_store: EvidenceStore,
    trace_store: TraceStore,
    residual_store: ResidualStore,
) -> Candidate:
    """
    Restore CandidateAuthority from EncodedStateProjection + Stores.

    This is the ONLY way to restore Candidate from LCNV.
    Unpack alone does NOT produce Candidate.

    Preconditions:
    - projection from unpack(lcnv)
    - stores contain original candidate data
    - validation passes

    Returns:
    - Full authoritative Candidate with:
      - identity_ids (from store)
      - evidence (from evidence_store)
      - trace_ids (from trace_store)
      - residuals (from residual_store)
      - rank (from projection + validation)
      - source-of-truth status

    Formula:
      CandidateAuthority(c) = Validate(
          EncodedStateProjection(c),
          CandidateStore,
          EvidenceStore,
          TraceStore,
          ResidualStore
      )
    """
    validate_projection(projection)

    return Candidate(
        identity_ids=candidate_store.get_identity_ids(projection.ref),
        evidence=evidence_store.get_evidence(projection.ref),
        trace_ids=trace_store.get_trace(projection.ref),
        residuals=residual_store.get_residuals(projection.ref),
        rank=validate_rank(projection.rank_residual),
        status=validate_status(projection.gate_state_bundle),
    )
```

---

## 5. Use Cases (Permitted)

### 5.1 State Compression for Search

```
Use case: Compress candidate state for efficient search

ALLOWED:
- Pack(candidate) → LCNV
- Store LCNV in search index
- Compare LCNV values for ordering
- Unpack(LCNV) → candidate when needed

FORBIDDEN:
- Derive meaning from LCNV directly
- Use LCNV as source of truth
- Skip qiyas by using LCNV
```

### 5.2 Ambiguity Cost Measurement

```
Use case: Measure cost of resolving ambiguity

ALLOWED:
- CandidateSet → ambiguity_count
- EvidenceSet → evidence_cost
- ResidualSet → residual_penalty
- FariqPresent → blocking_cost (infinite)

FORBIDDEN:
- LowCost → Meaning
- LowCost → Hukm
- LowCost → RankUpgrade
- HighCost → Candidate rejection (only residual)
```

### 5.3 Tarjih (Preference) Within Same Rank

```
Use case: Prefer lower-cost candidate within same rank

ALLOWED:
- rank(c1) = rank(c2) = STRONG
- cost(c1) < cost(c2)
- prefer c1 for tarjih within STRONG rank

FORBIDDEN:
- rank(c1) = WEAK, rank(c2) = STRONG
- cost(c1) < cost(c2)
- upgrade c1 to STRONG (rank elevation forbidden)
```

### 5.4 Inverse Extraction Complexity

```
Use case: Measure complexity of extracting possible source

ALLOWED:
- InverseCandidates → extraction_cost
- Multiple paths → measure cost of each
- Prefer lower-cost extraction within same rank

FORBIDDEN:
- LowExtractionCost → certain source
- HighExtractionCost → impossible source
```

---

## 6. Anti-Patterns (Forbidden)

### 6.1 Numeric Semantic Derivation

```
❌ FORBIDDEN:

def derive_meaning_from_abjad(letter: str) -> str:
    abjad_value = get_abjad(letter)
    if abjad_value == 2:
        return "duality"
    elif abjad_value == 3:
        return "trinity"
    # ... semantic derivation from number
```

**Why forbidden:** Abjad values are conventional coordinates with `semantic_force=FORBIDDEN`. They do NOT carry intrinsic meaning.

### 6.2 MCLO as Meaning Source

```
❌ FORBIDDEN:

def get_root_from_mclo(mclo_value: int) -> Root:
    # Extract root from numeric encoding
    # without lexical qiyas
    return Root(...)
```

**Why forbidden:** MCLO is SignifierOnly. Root requires LexicalAttestationGate and RootWeightAlgebra licensing.

### 6.3 Cost-Based Rank Elevation

```
❌ FORBIDDEN:

def upgrade_rank_if_low_cost(candidate: Candidate) -> Candidate:
    if cost(candidate) < threshold:
        candidate.rank = upgrade(candidate.rank)
    return candidate
```

**Why forbidden:** Rank is determined by meet semantics (ceiling of input ranks), NOT by cost. Low cost may guide tarjih WITHIN rank, but cannot elevate rank.

### 6.4 Closed Block as Zero

```
❌ FORBIDDEN:

if lcnv.lexical == CLOSED:
    meaning = "no meaning"
    # treat as absence of value
```

**Why forbidden:** CLOSED means "gate not opened yet", NOT "zero meaning" or "meaningless". The layer may be licensed later.

**Correct:**

```
✓ ALLOWED:

if lcnv.lexical == CLOSED:
    # Lexical gate not opened yet
    # Cannot derive lexical meaning
    # Must wait for LexicalAttestationGate
```

### 6.5 LCNV Replacing Candidate

```
❌ FORBIDDEN:

# Store only LCNV, discard Candidate
database.store(lcnv)
candidate = None  # ← FORBIDDEN

# Later try to use LCNV as source
meaning = derive_from_lcnv(lcnv)  # ← FORBIDDEN
```

**Why forbidden:** Candidate is source of truth. LCNV is reversible encoding. If Candidate is discarded, structure is lost.

**Correct:**

```
✓ ALLOWED:

# Store LCNV for efficiency
database.store_compressed(lcnv)

# But preserve ability to reconstruct
candidate = unpack(lcnv)

# Use Candidate as source of truth
meaning = derive_from_candidate(candidate)  # through qiyas
```

---

## 7. Integration with Existing Architecture

### 7.1 Relationship to QiyasKernel

```
QiyasKernel:
  - Produces Candidate through qiyas proof
  - Validates evidence
  - Enforces rank meet semantics
  - Preserves identity/trace
  - Produces residuals on failure

LCNV:
  - Encodes Candidate state (after qiyas)
  - Does NOT replace qiyas
  - Does NOT produce Candidate
  - Does NOT validate evidence
  - Does NOT determine rank
```

**LCNV is downstream from QiyasKernel, not parallel to it.**

### 7.2 Relationship to AbjadSystem

```
AbjadSystem:
  - Source of truth for Abjad conventional coordinates
  - get_abjad_coordinate(letter) → AbjadCoordinate
  - AbjadCoordinate.semantic_force = FORBIDDEN

MCLO (LCNV signifier block):
  - May include Abjad coordinate
  - Inherits semantic_force = FORBIDDEN
  - May combine with other signifier coordinates
  - Still does NOT produce meaning
```

### 7.3 Relationship to Layer 2 Coordinates

```
After PR #43:
  - Glyph gate enforces classification before coordinates
  - Specific residuals for each failure type
  - Safe to define numeric encoding

LCNV:
  - Encodes glyph-gated coordinate state
  - Preserves glyph classification evidence
  - Preserves specific residuals
  - Does NOT bypass glyph gate
```

---

## 8. Implementation Constraints

### 8.1 When to Implement

**DO NOT implement LCNV runtime yet.**

**Required before implementation:**
1. ✓ PR #43 merged (glyph gate + specific residuals)
2. ✓ This document (PR #44) merged
3. ⚠️ PR #45 merged (inverse + logarithmic measurement law)
4. ⚠️ PR #46 merged (Full SifatVector structure)
5. ⚠️ PR #47 merged (source-of-truth registries)
6. ⚠️ PR #48 merged (full coordinate coverage)

**Only THEN:**
7. PR #50: SignifierOnlyValue / MCLO prototype

**Reason:** LCNV implementation requires:
- Complete sifat axes (to encode all distinctions)
- Source-of-truth registries (to prevent duplication)
- Full coordinate coverage (to encode all letters)
- Inverse/logarithmic laws (to constrain cost measurement)

### 8.2 What Runtime Implementation Must Include

**When implementing (PR #50), MUST include:**

1. **Pack/Unpack functions with tests:**
   ```python
   test_inverse_law():
       candidate = create_test_candidate()
       lcnv = pack(candidate)
       projection = unpack(lcnv)
       # Unpack produces EncodedStateProjection, NOT Candidate
       assert isinstance(projection, EncodedStateProjection)
       assert projection != candidate

   test_authority_restoration():
       candidate = create_test_candidate()
       lcnv = pack(candidate)
       projection = unpack(lcnv)
       restored = restore_candidate_authority(
           projection,
           candidate_store,
           evidence_store,
           trace_store,
           residual_store,
       )
       # Only after store reunification + validation is Candidate restored
       assert restored == candidate
   ```

2. **Semantic force enforcement:**
   ```python
   assert lcnv.mclo.semantic_force == "FORBIDDEN"
   assert lcnv.lexical.semantic_force == "FORBIDDEN"
   # ... for all blocks
   ```

3. **Gate closure tests:**
   ```python
   test_closed_blocks():
       candidate = LetterIdentityCarrier(...)
       lcnv = pack(candidate)
       assert lcnv.mclo != CLOSED  # signifier gate opened
       assert lcnv.lexical == CLOSED  # lexical gate not opened
   ```

4. **Forbidden output tests:**
   ```python
   test_no_candidate_from_unpack():
       lcnv = pack(candidate)
       projection = unpack(lcnv)
       assert not isinstance(projection, Candidate)
       assert isinstance(projection, EncodedStateProjection)

   test_no_meaning_from_mclo():
       with pytest.raises(ForbiddenOutputError):
           derive_meaning_from_mclo(mclo_value)

   test_no_authority_from_unpack():
       with pytest.raises(ForbiddenOutputError):
           # Unpack alone cannot produce CandidateAuthority
           unpack(lcnv).get_authority()
   ```

5. **Residual preservation tests:**
   ```python
   test_residual_preservation():
       candidate_with_residuals = ...
       lcnv = pack(candidate_with_residuals)
       projection = unpack(lcnv)
       restored = restore_candidate_authority(projection, stores...)
       assert restored.residuals == candidate_with_residuals.residuals
   ```

### 8.3 What Runtime Implementation Must NOT Include

**FORBIDDEN in PR #50:**
- ❌ Meaning derivation from MCLO
- ❌ Hukm derivation from any LCNV block
- ❌ Rank elevation from cost
- ❌ Semantic interpretation of Abjad values
- ❌ Root extraction without LexicalAttestationGate
- ❌ Bypassing qiyas through numeric encoding
- ❌ Treating CLOSED as zero/absence
- ❌ Discarding Candidate in favor of LCNV

---

## 9. Governing Laws Summary

**Place at top of any LCNV implementation file:**

```python
"""
LCNV Governing Laws:

1. Inverse Law: Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)
2. Candidate Primacy: Candidate = source of truth, LCNV = encoding
3. Gate Awareness: CLOSED = gate not opened (not zero)
4. Semantic Force: semantic_force = FORBIDDEN for all blocks
5. Block Ordering: No Mutabaqah/Tadammun/Iltizam before Binding
6. Rank-Residual: Preserve rank ceiling and all residuals
7. Forbidden Derivations: Unpack(LCNV) ⇏ CandidateAuthority/Meaning/Hukm/Evidence/Trace

Authority Restoration Formula:
  CandidateAuthority(c) = Validate(
      EncodedStateProjection(c),
      CandidateStore,
      EvidenceStore,
      TraceStore,
      ResidualStore
  )

Constitutional Principle:
  LCNV is reversible within projection bounds,
  NOT reversible within epistemological authority bounds.

Forbidden:
- Unpack(LCNV) → CandidateAuthority (requires stores + validation)
- MCLO → Meaning
- AbjadValue → SemanticRoot
- LogScore → Hukm
- NumericBlock → RankUpgrade
- LCNV replacing Candidate
- Closed block as zero
- Meaning from number
- Certainty from low cost

Governing Principle:
  Candidate هو مصدر السلطة.
  LCNV أثر مضغوط.
  الأثر لا يصبح أصلًا.
  والرقم لا ينتج معرفة.

  (Candidate is source of authority.
   LCNV is compressed trace.
   Trace does not become origin.
   Number does not produce knowledge.)
"""
```

---

## 10. Cross-References

**Constitutional Foundation:**
- PROJECT_MATHEMATICAL_FOUNDATION.md — algebraic qiyas system
- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md — layer architecture

**Coordinate Systems:**
- abjad_system.py — conventional Abjad coordinates with semantic_force=FORBIDDEN
- Layer 2 coordinate adapters — glyph-gated coordinate production

**Future Documents:**
- INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md (PR #45)
- SIFAT_VECTOR_CONTRACT.md (extended by PR #46)

**Related Memories:**
- numeric coordinate derivation (makhraj + branch + degree + system + evidence + rank, semantic_force=FORBIDDEN)
- GARA constitutional foundation (no Arabic identity before ArabicDomainBridge gate)
- layer contract invariants (no layer produces next layer output without gate)

---

## 11. Authority

**This document has constitutional authority over:**
- All numeric encoding implementations
- All cost/complexity measurement systems
- All MCLO/SignifierOnlyValue implementations
- All compression/decompression functions

**This document enforces:**

```
لا رقم قبل بوابة.
لا دلالة من رقم.
لا معنى من دال.
لا مطابقة قبل Binding.
لا يقين بلا رتبة.
ولا إغلاق بلا بقايا محسوبة.
```

**Translation:**
```
No number before gate.
No semantics from number.
No meaning from signifier.
No mutabaqah before Binding.
No certainty without rank.
No closure without computed residuals.
```

**PRs that violate these laws are REJECTED.**

---

**Document Version:** 2.0
**Last Updated:** 2026-06-03
**Status:** Constitutional constraint document (LCNV Inverse Law corrected)
**Authority:** Governs all numeric encoding of qiyas layer state
**Critical Change:** Law 1 corrected - Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)
**Next Document:** INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md (PR #45)
