# FULL LAYER 2 PLAN

> **Purpose:** Complete architectural planning for Layer 2 (Atomic Identity and Coordinates) before building higher layers.
>
> **Constraint:** No SyllableCandidate, RootWeightAlgebra, or higher layer until Layer 2 is fully planned and source-of-truth is established.

---

## 0. Layer 2 Completion Criteria

**Layer 2 is NOT complete until it answers:**

1. What does ArabicLetterCoordinateCarrier carry?
2. What does it NOT carry?
3. What is the source of each value?
4. What distinguishes core letter vs glyph vs hamza seat vs madd?
5. What distinguishes phonetic sifat vs abjad value vs morpho role?
6. What residuals are produced if proof fails?

**Minimum planning requirement:**

```
ArabicLetterCoordinateCarrier =
    LetterIdentity (from Layer 2A)
  + GlyphClass
  + MakhrajCoordinate
  + FullSifatVector (6 axes)
  + PhoneticProxy
  + AbjadCoordinate (semantic_force=FORBIDDEN)
  + MorphoRolePotential (NOT final role)
  + FariqSet (invalidating differences)
  + Evidence
  + Rank
  + Trace
  + Residual
```

**With absolute constraint:**

```
Nothing in this layer produces:
  ❌ Meaning
  ❌ Root
  ❌ Weight
  ❌ Hukm
```

---

## 1. Layer 2 Architecture (Parallel + Convergent)

### Current Canonical Structure

```
Layer 2A: LetterIdentityCarrier (atomic, parallel)
  Input: LetterCodePoint
  Output: LetterIdentityCarrier
  Proof: Pure identity (unicode, script, name, class)
  Status: ✓ Canonical
  Coverage: Full (all Unicode Arabic letters)

Layer 2B: HarakaFunctionCarrier (atomic, parallel)
  Input: HarakaCodePoint
  Output: HarakaFunctionCarrier
  Proof: Functional role (opening/closing/neutral)
  Status: ✓ Canonical
  Coverage: Full (all harakaat)

Layer 2C: PositionCarrier (sequential)
  Input: ConditionedTypedSequence + index
  Output: PositionCarrier
  Proof: Position context
  Status: ✓ Canonical
  Coverage: Full

Layer 2D: ConditionedTypedSequence + AlignmentEvidence (sequential)
  Input: TypedCodePoint*
  Output: AlignmentEvidence, CarrierBindingCandidate, PositionEvidence
  Proof: Sequence admissibility, carrier binding
  Status: ✓ Canonical
  Coverage: Full

Layer 2X: ArabicLetterCoordinateCarrier (enrichment, partial)
  Input: LetterIdentityCarrier
  Output: ArabicLetterCoordinateCarrier
  Proof: Coordinate enrichment (makhraj, sifat, abjad, phonetic, glyph)
  Status: ⚠️ Partial canonical (4 letters: BAA, TAA, SEEN, KAF)
  Coverage: Partial
  Missing: Full alphabet, Full SifatVector, GlyphClassificationGate
```

### Convergence Point

```
Layer 3: SlotCandidate
  Input: LetterIdentityCarrier (2A)
       + HarakaFunctionCarrier (2B)
       + PositionCarrier (2C)
       + AlignmentEvidence (2D)
  Output: SlotCandidate
  Status: ✓ Canonical
```

---

## 2. Layer 2X Completion Plan

### 2.1 What ArabicLetterCoordinateCarrier IS

**Purpose:** Enrich letter identity with coordinate systems for phonetic, numeric, and morphological positioning.

**NOT purpose:** Derive meaning, root, weight, or hukm.

### 2.2 Complete Component Specification

```python
@dataclass(frozen=True)
class ArabicLetterCoordinateCarrier:
    """
    Enrichment of LetterIdentityCarrier with coordinate systems.

    CRITICAL: This is coordinate positioning, NOT meaning derivation.
    """

    # === INHERITED FROM LetterIdentityCarrier ===
    unicode_identity: str           # e.g., "U+0628"
    script_identity: str            # e.g., "ARABIC_LETTER_BAA"
    name_identity: str              # e.g., "BAA" / "باء"
    specific_letter_identity: str   # e.g., "letter:baa"
    letter_class: str               # e.g., "consonant"

    # === GLYPH CLASSIFICATION (NEW) ===
    glyph_class: GlyphClass
    # GlyphClass = CoreArabicLetter | HamzaSeatGlyph | MaddGlyph
    #            | WeakLetterGlyph | TatweelGlyph | OrthographicVariant

    # === PHONETIC PHYSICS COORDINATES ===
    makhraj_coordinate: MakhrajCoordinate
    # MakhrajCoordinate:
    #   spatial_source: str     # e.g., "BILABIAL", "ALVEOLAR"
    #   articulation_point: str # e.g., "LIPS_CLOSURE", "TONGUE_RIDGE"
    #   makhraj_place_order: int  # Within ArabicMakhrajPlaceOrder system

    sifat_vector: SifatVector
    # SifatVector (6 axes, FULL):
    #   voicing_axis: VoicingValue      # VOICED | VOICELESS
    #   manner_axis: MannerValue        # STOP | FRICATIVE | NASAL | APPROXIMANT | LATERAL
    #   nasality_axis: NasalityValue    # NASAL | ORAL
    #   frication_axis: FricationValue  # FRICATIVE | NON_FRICATIVE
    #   continuancy_axis: ContinuancyValue  # CONTINUANT | NON_CONTINUANT
    #   emphasis_axis: EmphasisValue    # EMPHATIC | NON_EMPHATIC
    #   # Residual if classification incomplete

    phonetic_proxy: str
    # IPA phonetic approximation, e.g., "/b/", "/t/", "/s/"
    # NOTE: Approximation only, not authoritative phonetic identity

    # === CONVENTIONAL NUMERIC COORDINATE ===
    abjad_coordinate: AbjadCoordinate | None
    # AbjadCoordinate:
    #   system: "ABJAD"
    #   numeric_value: int             # e.g., 2 for BAA
    #   semantic_force: "FORBIDDEN"    # ⚠️ CRITICAL: No meaning derivation
    #   evidence_source: "abjad_convention"

    # === MORPHOLOGICAL ROLE POTENTIAL (NOT FINAL ROLE) ===
    morpho_role_potential: MorphoRolePotential | None
    # MorphoRolePotential:
    #   carrier_potential: bool        # Can act as consonantal carrier
    #   operator_potential: bool       # Can act as vocalic operator
    #   extension_potential: bool      # Can act as long vowel extension
    #   weak_letter: bool              # Subject to phonological changes
    #   # NOTE: Potential only, requires RoleDisambiguationGate

    # === INVALIDATING DIFFERENCES ===
    fariq_set: tuple[str, ...]
    # Exhaustive list of invalidating differences negated for this letter
    # e.g., for BAA: "baa_vs_meem_nasality", "baa_vs_faa_frication"

    # === QIYAS PROOF INFRASTRUCTURE ===
    identity_ids: tuple[str, ...]  # Preserved from LetterIdentityCarrier
    evidence: EvidenceSet
    rank: EvidenceRank
    trace_ids: tuple[str, ...]
    residuals: tuple[Residual, ...]
```

### 2.3 Source-of-Truth Mapping

| Field | Canonical Source | Status |
|-------|-----------------|--------|
| `glyph_class` | `glyph_classification_registry.py` | ❌ To be created |
| `makhraj_coordinate` | `makhraj_coordinate_system.py` | ❌ To be created |
| `sifat_vector` | `sifat_vector_system.py` | ❌ To be created |
| `phonetic_proxy` | `phonetic_proxy_system.py` | ❌ To be created |
| `abjad_coordinate` | `abjad_system.py` | ✓ Exists (4 letters, needs expansion) |
| `morpho_role_potential` | `letter_role_taxonomy.py` | ❌ To be created |
| `fariq_set` | `letter_fariq_registry.py` | ❌ To be created |

---

## 3. Glyph Classification Gate

**See:** GLYPH_CLASSIFICATION_GATE_PLAN.md

**Purpose:** Distinguish glyph types BEFORE assigning phonetic/morphological coordinates.

**Why critical:**

```
ب (BAA) = CoreArabicLetter
  → Full makhraj/sifat/abjad

أ (ALIF_WITH_HAMZA_ABOVE) = HamzaSeatGlyph
  → Hamza coordinates + Alif seat coordinates
  → NOT simple letter

ا (ALIF) = MaddGlyph | OrthographicVariant
  → Context-dependent classification
  → Requires role disambiguation

ـ (TATWEEL) = TatweelGlyph
  → NOT letter, spacing glyph only
  → NO phonetic coordinates

آ (ALIF_WITH_MADDA_ABOVE) = Complex
  → Madda + Hamza + Alif orthography
  → Requires decomposition gate
```

**Gate requirement:**

```python
def classify_glyph(letter_identity: LetterIdentityCarrier) -> GlyphClass:
    """
    Classify glyph type BEFORE coordinate assignment.

    Returns:
        CoreArabicLetter: Simple letter with full coordinates
        HamzaSeatGlyph: Hamza on seat (requires decomposition)
        MaddGlyph: Long vowel / extension glyph
        WeakLetterGlyph: و/ي/ا with multiple potential roles
        TatweelGlyph: Spacing glyph (no phonetic coordinates)
        OrthographicVariant: Alif maqsurah, etc.
        Residual: Unclassified
    """
```

---

## 4. Full Sifat Vector (6 Axes)

**See:** SIFAT_VECTOR_CONTRACT.md

**Current (Partial):** 3 axes (voicing, manner, emphasis)

**Required (Full):** 6 axes

### 4.1 Why 6 Axes?

**3 axes insufficient to distinguish:**

```
❌ Cannot distinguish:
  ب (BAA)     vs م (MEEM)    — both voiced stops, need NASALITY
  و (WAW)     vs ف (FAA)     — need FRICATION + CONTINUANCY
  س (SEEN)    vs ش (SHEEN)   — need FRICATION manner detail
  ت (TAA)     vs د (DAL)     — need VOICING
  ط (TAA_E)   vs ت (TAA)     — need EMPHASIS
  ظ (ZAA_E)   vs ذ (THAAL)   — need EMPHASIS + FRICATION
```

**6 axes sufficient:**

```
✓ Can distinguish all 28+ Arabic letters through:
  VoicingAxis × MannerAxis × NasalityAxis
  × FricationAxis × ContinuancyAxis × EmphasisAxis
```

### 4.2 Sifat Vector Specification

```python
@dataclass(frozen=True)
class SifatVector:
    """
    6-axis phonetic discrimination system.

    CRITICAL: This is phonetic coordinate ONLY, not meaning.
    Used to NEGATE invalidating differences (fariq).
    """

    voicing_axis: VoicingValue
    # VOICED: ب د ج ز etc.
    # VOICELESS: ت ك س ص etc.

    manner_axis: MannerValue
    # STOP: ب ت د ط ك ق
    # FRICATIVE: ف ث ذ س ص ش خ غ ح ع ه
    # NASAL: م ن
    # APPROXIMANT: و ي (when consonantal)
    # LATERAL: ل

    nasality_axis: NasalityValue
    # NASAL: م ن
    # ORAL: all others

    frication_axis: FricationValue
    # FRICATIVE: ف ث ذ س ص ش ز خ غ ح ع ه
    # NON_FRICATIVE: ب ت د ط ك ق م ن ل و ي

    continuancy_axis: ContinuancyValue
    # CONTINUANT: ف ث ذ س ص ش ز خ غ ح ع ه م ن ل و ي
    # NON_CONTINUANT: ب ت د ط ك ق ء

    emphasis_axis: EmphasisValue
    # EMPHATIC: ص ض ط ظ ق (tafkhim)
    # NON_EMPHATIC: all others

    residuals: tuple[Residual, ...]
    # If any axis cannot be determined
```

### 4.3 Source-of-Truth

```
Canonical source: src/qiyas_core/systems/sifat_vector_system.py

Contains:
  - SifatVector dataclass
  - Enum definitions for each axis
  - Complete mapping: letter → sifat vector
  - Fariq negation logic
  - Evidence generation for sifat claims
```

---

## 5. Abjad Coordinate System (Expansion)

**Current status:** 4 letters only (BAA, TAA, SEEN, KAF)

**Required:** Full Arabic alphabet

### 5.1 Abjad System Contract

```python
@dataclass(frozen=True)
class AbjadCoordinate:
    """
    Conventional numeric coordinate in Abjad system.

    CRITICAL CONSTRAINT: semantic_force = FORBIDDEN
    """

    system: str  # "ABJAD"
    numeric_value: int  # 1-1000
    semantic_force: str  # MUST be "FORBIDDEN"
    evidence_source: str  # "abjad_convention"

    # FORBIDDEN OPERATIONS:
    # ❌ derive_meaning_from_numeric_value()
    # ❌ derive_root_from_numeric_value()
    # ❌ derive_hukm_from_numeric_value()

    # ALLOWED OPERATIONS:
    # ✓ numeric_coordinate_position()
    # ✓ numeric_ordering()
    # ✓ coordinate_distance()
```

### 5.2 Required Expansion

| Letter | Current | Required | Source |
|--------|---------|----------|--------|
| ا | — | 1 | abjad_system.py |
| ب | ✓ 2 | 2 | abjad_system.py |
| ج | — | 3 | abjad_system.py |
| د | — | 4 | abjad_system.py |
| ... | ... | ... | ... |
| غ | — | 1000 | abjad_system.py |

**Total:** 28 letters + variants

---

## 6. Morphological Role Potential

**NOT final role assignment.**

**Potential only.**

### 6.1 Role Potential Specification

```python
@dataclass(frozen=True)
class MorphoRolePotential:
    """
    Morphological role POTENTIAL, not final role.

    Final role requires RoleDisambiguationGate.
    """

    carrier_potential: bool
    # Can act as consonantal carrier (stem matter)
    # True for: ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه
    # Context-dependent for: و ي ا (weak letters)

    operator_potential: bool
    # Can act as vocalic operator
    # True for: و ي (when not carrier)
    # False for: solid consonants

    extension_potential: bool
    # Can act as long vowel extension
    # True for: و ي ا (madd letters)
    # False for: solid consonants

    weak_letter: bool
    # Subject to phonological changes (إعلال)
    # True for: و ي ا
    # False for: solid consonants

    # CRITICAL: This is POTENTIAL, not final determination
    # Final role requires:
    #   - Context
    #   - Pattern demand
    #   - Lexical evidence
    #   - RoleDisambiguationGate
```

---

## 7. Forbidden Outputs (Explicit)

**ArabicLetterCoordinateCarrier MUST forbid:**

```python
forbidden_outputs = [
    "MeaningCandidate",       # No meaning from coordinates
    "RootCandidate",          # No root from letter identity
    "WeightCandidate",        # No weight from coordinates
    "StemMatterCandidate",    # Requires role disambiguation
    "WordFormCandidate",      # Requires higher layers
    "LexicalMadlulCandidate", # Meaning requires composition
    "HukmCandidate",          # Hukm requires evidence domain
    "RealityClaim",           # Truth requires correspondence check
]
```

**Evidence claims MUST include:**

```python
evidence.add_claim("forbidden:meaning_from_abjad:negated")
evidence.add_claim("forbidden:root_from_unicode:negated")
evidence.add_claim("forbidden:weight_from_coordinates:negated")
```

---

## 8. Residual Specifications

**See:** LAYER_2_RESIDUALS.md

**Categories:**

### 8.1 Identity Residuals

```
defer:letter_identity_ambiguous:present
  Cause: Multiple possible identities (e.g., context-dependent glyphs)

defer:script_identity_uncertain:present
  Cause: Non-standard Unicode sequence

فارق:letter_identity_conflict:present
  Cause: Invalidating difference detected
```

### 8.2 Coordinate Residuals

```
defer:makhraj_coordinate_unknown:present
  Cause: Letter not in makhraj registry

defer:sifat_vector_incomplete:present
  Cause: One or more sifat axes cannot be determined

defer:abjad_value_undefined:present
  Cause: Letter not in Abjad system (e.g., non-classical letters)

defer:glyph_class_ambiguous:present
  Cause: Glyph classification requires context
```

### 8.3 Role Potential Residuals

```
defer:role_potential_context_dependent:present
  Cause: Weak letter (و/ي/ا) requires context for role determination

defer:morpho_role_requires_disambiguation:present
  Cause: Multiple potential roles, requires RoleDisambiguationGate
```

---

## 9. Implementation Sequence

**DO NOT implement all at once.**

**Phased implementation:**

### Phase 1: Source-of-Truth Establishment (Documentation PR)

- [ ] SOURCE_OF_TRUTH_REGISTRY.md ✓ (this PR)
- [ ] FULL_LAYER_2_PLAN.md ✓ (this document)
- [ ] GLYPH_CLASSIFICATION_GATE_PLAN.md (this PR)
- [ ] SIFAT_VECTOR_CONTRACT.md (this PR)
- [ ] LAYER_2_RESIDUALS.md (this PR)

### Phase 2: Registry Creation

- [ ] Create `src/qiyas_core/registries/` directory structure
- [ ] Implement letter_name_registry.py
- [ ] Implement glyph_classification_registry.py
- [ ] Implement letter_fariq_registry.py

### Phase 3: System Creation

- [ ] Expand abjad_system.py to full alphabet
- [ ] Create makhraj_coordinate_system.py
- [ ] Create sifat_vector_system.py (6 axes)
- [ ] Create phonetic_proxy_system.py
- [ ] Create letter_role_taxonomy.py

### Phase 4: Gate Implementation

- [ ] Implement GlyphClassificationGate
- [ ] Add glyph classification to ArabicLetterCoordinateAdapter
- [ ] Add validation tests

### Phase 5: Coordinate Expansion

- [ ] Expand ArabicLetterCoordinateCarrier to include:
  - glyph_class
  - full sifat_vector (6 axes)
  - morpho_role_potential
  - fariq_set
- [ ] Update tests for expanded structure

### Phase 6: Full Alphabet Coverage

- [ ] Expand from 4 letters (BAA, TAA, SEEN, KAF) to full alphabet
- [ ] Add all 28+ classical Arabic letters
- [ ] Add variant forms where applicable
- [ ] Comprehensive test coverage

---

## 10. Success Criteria

**Layer 2 is COMPLETE when:**

1. ✓ All canonical sources created and documented
2. ✓ No truth duplication (single source per truth)
3. ✓ GlyphClassificationGate operational
4. ✓ Full SifatVector (6 axes) for all letters
5. ✓ Abjad system covers full alphabet
6. ✓ Morpho role potential documented (not final roles)
7. ✓ All forbidden outputs explicitly enforced
8. ✓ All residual categories documented
9. ✓ Full test coverage
10. ✓ No layer jump to meaning/root/weight/hukm

**ONLY THEN can we proceed to:**
- SyllableCandidate (Layer 4)
- ArabicMorphophonology (Layer 4-5)
- RoleDisambiguationGate (Layer 5)

---

## 11. Integration with Governance

**This plan implements:**
- PROJECT_MATHEMATICAL_FOUNDATION.md § 11 (Full Layer 2: SifatVector + GlyphClassificationGate)
- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md (governance before expansion)
- SOURCE_OF_TRUTH_REGISTRY.md (canonical source requirement)

**This plan feeds into:**
- GLYPH_CLASSIFICATION_GATE_PLAN.md (gate specification)
- SIFAT_VECTOR_CONTRACT.md (6-axis sifat contract)
- LAYER_2_RESIDUALS.md (residual specifications)

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Constitutional planning document
**Authority:** Required before Layer 3+ expansion
