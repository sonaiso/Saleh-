# INVERSE EXTRACTION AND LOGARITHMIC MEASUREMENT LAW

> **قانون الاستخراج العكسي والقياس اللوغاريتمي**
>
> **Inverse Extraction and Logarithmic Measurement Law**

---

## 0. Constitutional Authority

**This document corrects and constrains PR #44 (LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md).**

**Authority:**
- Below: PROJECT_MATHEMATICAL_FOUNDATION.md (defines algebraic qiyas system)
- Below: CANONICAL_ARCHITECTURE_CONTROL_FRAME.md (defines layer architecture)
- Below: LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md (defines LCNV structure)
- Above: All LCNV runtime implementations
- Above: All logarithmic cost measurement implementations
- Above: All inverse extraction implementations

**Purpose:**
- Correct dangerous formulations in PR #44 before runtime implementation
- Define what logarithmic measurement IS permitted (cost within layer)
- Define what logarithmic measurement is FORBIDDEN (meaning derivation, rank elevation)
- Define what inverse extraction IS permitted (gate state reconstruction)
- Define what inverse extraction is FORBIDDEN (independent candidate authority)

**Why this document exists NOW:**

PR #44 successfully prevented numeric semantic derivation (`MCLO → Meaning`, `Number → Hukm`), but contains dangerous formulations that could become backdoors to meaning/rank/candidate independence during implementation.

**The risk this prevents:**
```
❌ Unpack(Pack(c)) = c (interpreted as: number reconstructs full Candidate independently)
❌ log(CLOSED) (treating gate state as quantity)
❌ LogScore(DalOnly) → MeaningOnly (logarithm opening higher layer)
❌ LowCost → RankUpgrade (cost elevating rank)
❌ LCNV⁻¹(n) → Meaning (inverse extraction producing semantic claims)
❌ LexicalOnly containing semantic meaning
❌ MeaningOnly computing Mutabaqah/Tadammun/Iltizam before Binding
```

---

## 1. Critical Correction: Unpack Does Not Return Full Candidate

### 1.1 The Dangerous Formulation in PR #44

PR #44 states (section 4.2):

```python
def unpack(lcnv: LCNV) -> Candidate:
    """
    Returns:
    - Original candidate with full:
      - identity_ids
      - evidence
      - rank
      - trace_ids
      - residuals
    """
```

**This is constitutionally dangerous.**

If implemented literally, this makes LCNV capable of reconstructing the full Candidate including evidence, which **contradicts the principle that Candidate is source of truth**.

### 1.2 The Constitutional Correction

**CORRECTED formulation:**

```python
def unpack(lcnv: LCNV) -> EncodedCandidateStateProjection:
    """
    Returns:
    - Encoded projection of candidate state
    - NOT independent candidate authority
    - NOT full evidence reconstruction

    Candidate reconstruction requires:
      EncodedCandidateStateProjection
      + CandidateStore
      + EvidenceStore
      + TraceStore
      → Candidate
    """
```

### 1.3 The Governing Law

```
LCNV reconstructs candidate state projection.
LCNV does NOT reconstruct independent evidential authority.
LCNV does NOT replace CandidateStore.
LCNV does NOT replace EvidenceStore.
LCNV does NOT replace TraceStore.

الرقم يفك إسقاط حالة المرشح.
ولا يعيد سلطة المرشح.
ولا يستقل بالدليل.
```

**Formal statement:**

```
Unpack(Pack(c)) = EncodedStateProjection(c)

NOT:
Unpack(Pack(c)) = c (as independent Candidate)

Candidate reconstruction:
EncodedStateProjection(c) + CandidateStore + EvidenceStore + TraceStore → c
```

**Reason:**

If the number can reconstruct full evidence independently, then:
1. LCNV becomes source of truth (violates Candidate primacy)
2. Evidence must be compressed into number (impractical or transforms number into database)
3. Number becomes substitute for qiyas proof (violates qiyas requirement)

**This is the most important correction in this document.**

---

## 2. Logarithmic Measurement Laws

### 2.1 Law 1: No Logarithm on CLOSED

```
log(CLOSED) = FORBIDDEN

Reason: CLOSED is gate state, not quantity.
```

**Detailed constraint:**

```
CLOSED ≠ 0
CLOSED ≠ value
CLOSED ≠ quantity
CLOSED = gate not opened

Therefore:
- log(CLOSED) is undefined
- CLOSED cannot participate in numeric measurement
- CLOSED must remain as distinct state in any encoding
```

**Test requirement:**

```python
def test_no_log_on_closed():
    with pytest.raises(ForbiddenOperationError):
        log_score(CLOSED)
```

### 2.2 Law 2: Logarithm Only on Positive Licensed Measure

```
log(x) permitted iff:
  x > 0
  ∧ x ∈ LicensedMeasuredQuantity
  ∧ Gate(x) = OPEN
```

**Permitted examples:**

```python
# Allowed: measuring ambiguity within licensed layer
log₁₀(1 + candidate_count)  # where candidates are licensed

# Allowed: information-theoretic cost
-log(p)  # where p is licensed probability from evidence

# Allowed: residual complexity
log₁₀(1 + residual_count)  # where residuals are computed

# Allowed: inverse extraction cost
log₁₀(1 + inverse_candidate_count)  # where inverses are licensed
```

**Forbidden examples:**

```python
# FORBIDDEN: logarithm on closed gate
log(CLOSED)

# FORBIDDEN: logarithm on meaning gate when closed
log(MeaningGateClosed)

# FORBIDDEN: semantic derivation from Abjad
log(AbjadValue) → meaning

# FORBIDDEN: semantic claim from MCLO
log(MCLO) → semantic_claim
```

**Constitutional constraint:**

```
Logarithm measures complexity/cost of licensed state.
Logarithm does NOT:
- Open gates
- Produce meaning
- Elevate rank
- Create candidates
- Replace evidence
```

### 2.3 Law 3: LogScore Measures Inside Layer Only

```
LogScore(layer) measures within that layer.
LogScore(layer) must NOT open higher layer.
```

**Specific prohibitions:**

```
LogScore(DalOnly) ↛ LexicalOnly
LogScore(LexicalOnly) ↛ MeaningOnly
LogScore(MeaningOnly) ↛ Binding
LogScore(Binding) ↛ Ifadah
LogScore(Ifadah) ↛ Hukm
```

**Permitted use:**

```
LogScore(DalOnly) → cost_of_signifier_ambiguity
  (within DalOnly layer, no semantic force)

LogScore(LexicalOnly) → cost_of_root_form_ambiguity
  (within LexicalOnly layer, requires LexicalGate opened)

LogScore(MeaningOnly) → cost_of_meaning_ambiguity
  (within MeaningOnly layer, requires MeaningGate opened, no ifadah/hukm)
```

**Test requirement:**

```python
def test_logscore_stays_in_layer():
    dal_score = log_score(dal_candidates)
    assert dal_score.layer == "DalOnly"
    assert dal_score.semantic_force == "FORBIDDEN"
    assert not opens_gate(dal_score, "LexicalOnly")
```

### 2.4 Law 4: Cost Guides Within Rank, Does Not Elevate Rank

**This law was stated in PR #44 but must be formalized here:**

```
LowCost → TarjihHintWithinRank

NOT:
LowCost → RankUpgrade
LowCost → Meaning
LowCost → Hukm
LowCost → Certainty
```

**Formal statement:**

```
Given:
  rank(c₁) = rank(c₂) = R
  cost(c₁) < cost(c₂)

Permitted:
  prefer(c₁) within rank R (tarjih hint)

Forbidden:
  upgrade(rank(c₁)) based on cost
  convert(cost(c₁)) to meaning
  derive(hukm) from cost(c₁)
```

**Example:**

```python
# ALLOWED:
c1 = Candidate(rank=STRONG, cost=5)
c2 = Candidate(rank=STRONG, cost=10)
preferred = tarjih_within_rank([c1, c2])  # returns c1 as hint

# FORBIDDEN:
c1 = Candidate(rank=WEAK, cost=5)
c2 = Candidate(rank=STRONG, cost=10)
# Cannot upgrade c1.rank to STRONG based on lower cost
```

**Reason:**

Rank is determined by **meet semantics** (ceiling of input ranks based on evidence strength), NOT by cost. Cost measures **complexity/ambiguity**, not **evidential strength**.

---

## 3. Inverse Extraction Laws

### 3.1 Law 5: Inverse Returns Gate State Bundle, Not Meaning

```
LCNV⁻¹(n) → GateStateBundle
LCNV⁻¹(n) → EncodedCandidateStateProjection

NOT:
LCNV⁻¹(n) → Meaning
LCNV⁻¹(n) → Hukm
LCNV⁻¹(n) → independent Candidate authority
```

**Formal specification:**

```python
def inverse_extract(lcnv: LCNV) -> GateStateBundle:
    """
    Extract gate state structure from LCNV.

    Returns:
    - GateStateBundle containing:
      - mclo_state: CLOSED | EncodedSignifierState
      - lexical_state: CLOSED | EncodedLexicalFormState
      - meaning_state: CLOSED | EncodedMeaningState
      - binding_state: CLOSED | EncodedBindingState
      - mutabaqah_state: CLOSED | EncodedMutabaqahPotential
      - tadammun_state: CLOSED | EncodedTadammunPotential
      - iltizam_state: CLOSED | EncodedIltizamPotential
      - rank_residual: EncodedRankResidualState

    Does NOT return:
    - Meaning
    - Hukm
    - Independent Candidate
    - Semantic claim
    - Truth value
    """
```

**Constitutional constraint:**

```
Inverse extraction reconstructs WHICH gates are open.
Inverse extraction reconstructs HOW MUCH state is encoded.
Inverse extraction does NOT reconstruct WHY (evidence).
Inverse extraction does NOT produce semantic meaning.
```

### 3.2 Inverse Extraction Use Cases

**Permitted:**

```python
# Inspect which gates are opened
gates = inverse_extract(lcnv)
if gates.mclo_state != CLOSED:
    print("Signifier gate opened")
if gates.lexical_state == CLOSED:
    print("Lexical gate not opened yet")

# Measure extraction complexity
complexity = log₁₀(1 + count_possible_sources(lcnv))

# Compare state structures
similarity = compare_gate_bundles(bundle1, bundle2)
```

**Forbidden:**

```python
# FORBIDDEN: derive meaning from inverse
meaning = inverse_extract(lcnv).derive_meaning()  # ❌

# FORBIDDEN: produce hukm from inverse
hukm = inverse_extract(lcnv).infer_hukm()  # ❌

# FORBIDDEN: bypass qiyas through inverse
candidate = inverse_extract(lcnv).to_candidate()  # ❌
# (Candidate reconstruction requires stores, not just LCNV)
```

---

## 4. Block-Specific Constraints

### 4.1 LexicalOnly Constraint

**PR #44 states:**

```
LexicalOnly = numeric encoding of lexical attestation state
            = root/form licensing state (not final meaning)
```

**DANGER:** The name "LexicalOnly" may be misunderstood as "lexical meaning."

**CONSTRAINT added by this document:**

```
LexicalOnly = LafziSignifiedOnly
OR
LexicalOnly = LexicalFormOnly

Definition:
  Lexical/morphological signified state
  NOT semantic meaning state

Laws:
  LexicalOnly.meaning_force = NOT_YET
  LexicalOnly.semantic_derivation = FORBIDDEN

Permitted outputs:
  root_identity
  form_pattern
  weight_encoding
  wordform_license
  morphological_analysis

Forbidden outputs:
  MeaningCandidate
  DalalahVector
  IfadahCandidate
  HukmCandidate
  SemanticClaim
```

**Reason:**

LexicalOnly encodes **المدلول اللفظي/الصرفي** (lexical/morphological signified), NOT **المدلول المعنوي** (semantic meaning).

Root and form are **linguistic structure**, not **semantic content**.

### 4.2 MeaningOnly Constraint

**PR #44 states:**

```
MeaningOnly = numeric encoding of lexical signified state
            = mutabaqah/tadammun/iltizam potential
            = polysemy/metaphor/transfer state
```

**DANGER:** The phrase "mutabaqah/tadammun/iltizam potential" could be misinterpreted as "compute PTI before Binding."

**CONSTRAINT added by this document:**

```
MeaningOnly = SingularLexicalMadlulCandidate
            = singular meaning candidate (no ifadah, no hukm)

Laws:
  MeaningOnly.PTI_force = POTENTIAL_ONLY
  MeaningOnly.PTI_computed = FORBIDDEN
  MeaningOnly.ifadah_force = FORBIDDEN
  MeaningOnly.hukm_force = FORBIDDEN

Permitted:
  MeaningOnly may contain analytical material for future DalalahVector
  (e.g., polysemy count, metaphor marker, transfer type)

Forbidden:
  MeaningOnly must NOT compute Mutabaqah value
  MeaningOnly must NOT compute Tadammun value
  MeaningOnly must NOT compute Iltizam value
  MeaningOnly must NOT produce Ifadah
  MeaningOnly must NOT produce Hukm
```

**Reason:**

PR #44 correctly states (section 3.5):

```
Mutabaqah/Tadammun/Iltizam blocks require:
- Binding block ≠ CLOSED
- DalalahVector licensed
```

Therefore, **MeaningOnly cannot compute PTI**, it can only carry **material** that will be **used later** after Binding is opened.

**Example:**

```python
# ALLOWED:
meaning_state = MeaningOnly(
    meaning_id="دَخَلَ_v1_enter",
    polysemy_count=3,  # analytical material
    metaphor_potential=True,  # marker for later analysis
    PTI_computed=False,  # explicitly NOT computed
)

# FORBIDDEN:
meaning_state = MeaningOnly(
    mutabaqah_value=0.8,  # ❌ computed PTI before Binding
    tadammun_value=0.6,   # ❌ computed PTI before Binding
)
```

### 4.3 MCLO Constraint

**PR #44 states:**

```
MCLO = numeric encoding of signifier identity
     = conventional coordinate (e.g., Abjad value)
     + positional coordinate
     + script variant coordinate
```

**INSUFFICIENCY:** The project has moved beyond Abjad. MCLO must be broader.

**CONSTRAINT added by this document:**

```
MCLO = SignifierOnlyValue
     = GlyphCoordinate
     + ScriptCoordinate
     + PhoneticCoordinate
     + HarakaFunctionCoordinate
     + PositionCoordinate
     + AlignmentCoordinate
     + OperationalSignifierCoordinate
     + OptionalConventionalCoordinate

Where:
  Abjad ⊂ MCLO (as OptionalConventionalCoordinate)

NOT:
  MCLO = Abjad
  MCLO ⊂ Abjad
```

**Three signifier layers:**

1. **GlyphCoordinate**: Glyph-gated classification state
2. **PhoneticCoordinate**: Phonetic/makhraj/sifat coordinate
3. **OperationalSignifierCoordinate**: Functional role in signifier algebra

**Abjad is:** OptionalConventionalCoordinate, not foundation.

**All components:**
```
semantic_force = FORBIDDEN
meaning_derivation = FORBIDDEN
hukm_production = FORBIDDEN
```

---

## 5. Governing Laws Summary

**Place at top of any LCNV inverse/logarithmic implementation:**

```python
"""
Inverse Extraction and Logarithmic Measurement Laws:

1. Unpack Correction:
   Unpack(Pack(c)) = EncodedStateProjection(c)
   Candidate reconstruction requires CandidateStore/EvidenceStore/TraceStore.

2. No log(CLOSED):
   CLOSED is gate state, not quantity.

3. Logarithm on licensed positive measures only:
   log(x) permitted iff x > 0 ∧ x ∈ LicensedMeasuredQuantity ∧ Gate(x)=OPEN

4. LogScore measures inside layer:
   LogScore(layer) ↛ open higher layer

5. Cost guides within rank:
   LowCost → TarjihHintWithinRank (NOT RankUpgrade)

6. Inverse returns gate state bundle:
   LCNV⁻¹(n) → GateStateBundle (NOT Meaning, NOT independent Candidate)

7. LexicalOnly = LafziSignifiedOnly:
   meaning_force=NOT_YET, semantic_derivation=FORBIDDEN

8. MeaningOnly constrained:
   PTI_force=POTENTIAL_ONLY, PTI_computed=FORBIDDEN,
   ifadah_force=FORBIDDEN, hukm_force=FORBIDDEN

9. MCLO = SignifierOnlyValue:
   GlyphCoordinate + PhoneticCoordinate + OperationalSignifierCoordinate
   + OptionalConventionalCoordinate (Abjad is subset)

Forbidden:
- Unpack → independent Candidate authority
- log(CLOSED)
- LogScore → open higher layer
- LowCost → RankUpgrade
- LCNV⁻¹ → Meaning/Hukm
- LexicalOnly → MeaningCandidate
- MeaningOnly → compute PTI before Binding
- MCLO as only Abjad
"""
```

---

## 6. Implementation Constraints

### 6.1 When to Implement

**DO NOT implement LCNV runtime yet.**

**This document (PR #45) is docs-only.**

**Required before LCNV runtime:**
1. ✓ PR #43 merged (glyph gate + specific residuals)
2. ✓ PR #44 merged (LCNV constitutional structure)
3. ✓ PR #45 merged (this document: inverse + logarithmic law)
4. ⚠️ PR #46 merged (Full SifatVector structure)
5. ⚠️ PR #47 merged (source-of-truth registries)
6. ⚠️ PR #48 merged (full coordinate coverage)

**Only THEN:**
7. PR #50: SignifierOnlyValue / MCLO prototype (with constraints from this document)

**Reason:**

Even with this document constraining inverse/logarithmic operations, runtime implementation requires:
- Complete sifat axes (to encode all phonetic distinctions)
- Source-of-truth registries (to prevent LCNV becoming source)
- Full coordinate coverage (to encode all letter coordinates)

### 6.2 Test Requirements for Future PR #50

**When implementing LCNV runtime (PR #50), MUST include:**

```python
# Test 1: Unpack returns projection, not independent candidate
def test_unpack_returns_projection_not_candidate():
    candidate = create_test_candidate()
    lcnv = pack(candidate)
    projection = unpack(lcnv)

    assert isinstance(projection, EncodedCandidateStateProjection)
    assert not isinstance(projection, Candidate)

    # Candidate reconstruction requires stores
    reconstructed = reconstruct_candidate(
        projection,
        candidate_store,
        evidence_store,
        trace_store
    )
    assert reconstructed == candidate

# Test 2: No log on CLOSED
def test_no_log_on_closed():
    with pytest.raises(ForbiddenOperationError):
        log_score(CLOSED)

# Test 3: Log only on positive licensed measure
def test_log_requires_positive_licensed_measure():
    with pytest.raises(ForbiddenOperationError):
        log_score(-5)  # negative

    with pytest.raises(ForbiddenOperationError):
        log_score(unlicensed_value)  # not licensed

    # Allowed
    score = log_score(licensed_positive_count)
    assert score > 0

# Test 4: LogScore stays in layer
def test_logscore_does_not_open_higher_layer():
    dal_candidates = create_dal_only_candidates()
    score = log_score(dal_candidates)

    assert score.layer == "DalOnly"
    assert score.semantic_force == "FORBIDDEN"
    assert not opens_gate(score, "LexicalOnly")

# Test 5: Cost does not elevate rank
def test_cost_does_not_elevate_rank():
    weak_low_cost = Candidate(rank=WEAK, cost=5)
    strong_high_cost = Candidate(rank=STRONG, cost=10)

    preferred = tarjih([weak_low_cost, strong_high_cost])

    # Strong rank preferred regardless of cost
    assert preferred.rank == STRONG
    assert preferred == strong_high_cost

# Test 6: Inverse returns gate bundle not meaning
def test_inverse_returns_gate_bundle_not_meaning():
    lcnv = pack(candidate)
    bundle = inverse_extract(lcnv)

    assert isinstance(bundle, GateStateBundle)
    assert not hasattr(bundle, 'meaning')
    assert not hasattr(bundle, 'hukm')

# Test 7: LexicalOnly forbidden outputs
def test_lexical_only_no_meaning_output():
    lexical_state = create_lexical_only_state()

    assert lexical_state.meaning_force == "NOT_YET"

    with pytest.raises(ForbiddenOutputError):
        lexical_state.derive_meaning()

# Test 8: MeaningOnly no PTI computation
def test_meaning_only_no_pti_computation():
    meaning_state = create_meaning_only_state()

    assert meaning_state.PTI_force == "POTENTIAL_ONLY"
    assert meaning_state.PTI_computed == False

    with pytest.raises(ForbiddenOperationError):
        meaning_state.compute_mutabaqah()

# Test 9: MCLO broader than Abjad
def test_mclo_broader_than_abjad():
    mclo = create_mclo_state()

    assert hasattr(mclo, 'glyph_coordinate')
    assert hasattr(mclo, 'phonetic_coordinate')
    assert hasattr(mclo, 'operational_coordinate')

    # Abjad is optional
    if mclo.has_conventional_coordinate:
        assert mclo.conventional_coordinate.type == "Abjad"
```

---

## 7. Cross-References

**Constitutional Foundation:**
- PROJECT_MATHEMATICAL_FOUNDATION.md — algebraic qiyas system
- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md — layer architecture
- LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md — LCNV structure (corrected by this document)

**Corrected Formulations:**
- Section 4.2 "Unpack Operation" in PR #44 → corrected by section 1 of this document
- Section 3.1 "MCLO" in PR #44 → constrained by section 4.3 of this document
- Section 3.2 "LexicalOnly Block" in PR #44 → constrained by section 4.1 of this document
- Section 3.3 "MeaningOnly Block" in PR #44 → constrained by section 4.2 of this document

**Future Documents:**
- SIFAT_VECTOR_CONTRACT.md (extended by PR #46)
- SOURCE_OF_TRUTH_REGISTRIES.md (PR #47)

**Related Memories:**
- LCNV constitutional architecture (updated by this document)
- numeric coordinate derivation (semantic_force=FORBIDDEN)
- layer contract invariants (no layer produces next layer output without gate)

---

## 8. Authority

**This document has constitutional authority over:**
- All LCNV inverse extraction implementations
- All logarithmic cost measurement implementations
- All Pack/Unpack implementations
- All MCLO/SignifierOnlyValue implementations
- PR #44 formulations that conflict with this document

**This document corrects PR #44:**

```
PR #44 stated: Unpack(Pack(x)) = x
This document corrects: Unpack(Pack(x)) = EncodedStateProjection(x)

PR #44 stated: Returns original candidate with full evidence
This document corrects: Returns projection, requires stores for reconstruction

PR #44 described: MCLO as conventional coordinate (e.g., Abjad)
This document constrains: MCLO = SignifierOnlyValue (Abjad is subset)

PR #44 described: MeaningOnly as PTI potential
This document constrains: PTI_force=POTENTIAL_ONLY, PTI_computed=FORBIDDEN
```

**This document enforces:**

```
لا رقم يعيد المرشح كاملًا.
لا لوغاريتم على بوابة مغلقة.
لا لوغاريتم يفتح طبقة أعلى.
لا كلفة ترفع الرتبة.
لا عكس ينتج معنى.
لا مدلول لفظي يُحسب معنىً.
لا مدلول معنوي يُحسب مطابقة قبل الربط.
```

**Translation:**
```
No number reconstructs full Candidate.
No logarithm on closed gate.
No logarithm opens higher layer.
No cost elevates rank.
No inverse produces meaning.
No lexical signified computed as semantic meaning.
No meaning signified computes mutabaqah before binding.
```

**PRs that violate these laws are REJECTED.**

---

**Document Version:** 1.0
**Last Updated:** 2026-06-02
**Status:** Constitutional constraint document (corrects PR #44)
**Authority:** Governs all inverse extraction and logarithmic measurement
**Corrects:** LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md (PR #44)
**Next Document:** SIFAT_VECTOR_CONTRACT.md (extended by PR #46)
