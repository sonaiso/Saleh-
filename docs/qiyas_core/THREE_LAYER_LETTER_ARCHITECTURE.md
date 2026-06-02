# Three-Layer Arabic Letter Architecture (Option C)

## Constitutional Decision

Following the architectural critique, we implement a **three-layer** structure that separates identity proof from coordinate enrichment:

```
LetterCodePoint
  ↓ Φ_identity
LetterIdentityCarrier
  ↓ Φ_coordinates
ArabicLetterCoordinateCarrier
  ↓ Φ_slot (with HarakaFunctionCarrier + PositionCarrier + AlignmentCarrier)
SlotCandidate
```

## Layer 1: LetterIdentityCarrier

**Purpose**: Answer the question "Which letter is this?"

**Contains ONLY pure identity:**
- `unicode_identity`: U+0628
- `script_identity`: ARABIC_LETTER_BAA
- `name_identity`: "BAA" (Latin) / "باء" (Arabic)
- `specific_letter_identity`: "letter:baa"
- `identity_ids`: tuple of identity markers
- `evidence`: EvidenceSet proving identity
- `rank`: EvidenceRank.FORM
- `trace_ids`: proof trace
- `residuals`: audit of what's missing

**Does NOT contain:**
- sound_identity (moves to Layer 2)
- makhraj (moves to Layer 2)
- sifat (moves to Layer 2)
- abjad numeric value (moves to Layer 2)
- phonetic proxy (moves to Layer 2)

**Constitutional Rules:**
```python
Φ_identity:
  LetterCodePoint × EvidenceSet
  ⇀ LetterIdentityCarrier

Required evidence:
  - wasf:has_unicode_identity:{codepoint}:evidenced
  - wasf:has_script_identity:{letter_name}:evidenced
  - illah:letter_identity_is:{letter_name}:verified
```

## Layer 2: ArabicLetterCoordinateCarrier

**Purpose**: Answer the question "What are this letter's coordinates within representation systems?"

**Contains coordinate enrichment:**
1. **Conventional Coordinates:**
   - `abjad_coordinate`: AbjadCoordinate | None
     - system: "ABJAD"
     - numeric_value: 2 (for baa)
     - semantic_force: "FORBIDDEN" ⚠️
     - evidence_source: "abjad_convention"

2. **Phonetic Physics Coordinates:**
   - `phonetic_proxy`: "/b/" (IPA representation)
   - `makhraj_coordinate`: MakhrajGeometry
     - spatial_source: "BILABIAL"
     - articulation_point: "LIPS_CLOSURE"
   - `sifat_profile`: SifatGeometry
     - voicing: "VOICED"
     - manner: "STOP"
     - nasal: False
     - fricative: False
     - emphasis: "NON_EMPHATIC"

3. **Invalidating Differences (FariqSet):**
   - `fariq_set`: tuple[str, ...]
   - Example for BAA:
     - "baa_vs_meem_nasality"
     - "baa_vs_faa_frication"
     - "baa_vs_taa_makhraj"

**Constitutional Rules:**
```python
Φ_coordinates:
  LetterIdentityCarrier × RepresentationContract × EvidenceSet
  ⇀ ArabicLetterCoordinateCarrier

Required evidence:
  - wasf:has_phonetic_proxy:/b/:evidenced
  - wasf:has_makhraj:bilabial:evidenced
  - wasf:has_voicing:voiced:evidenced
  - wasf:has_manner:stop:evidenced
  - wasf:has_nasal:false:evidenced
  - wasf:has_abjad_value:2:evidenced (if applicable)
  - فارق:{difference}:absent (for each invalidating difference)
```

**Critical Constraint:**
```python
# Abjad values are CONVENTIONAL ONLY
assert abjad_coordinate.semantic_force == "FORBIDDEN"

# Allowed:
Abjad(ب) = 2  ✓

# Forbidden:
Meaning(ب) = 2  ✗
Hukm(ب) = 2  ✗
```

## Layer 3: SlotCandidate

**Purpose**: Prove that an enriched letter enters a licensed slot with haraka, position, and alignment.

**Input Requirements:**
```python
Φ_slot:
  ArabicLetterCoordinateCarrier
  × HarakaFunctionCarrier
  × PositionCarrier
  × AlignmentCarrier
  × EvidenceSet
  ⇀ SlotCandidate
```

**Why SlotCandidate needs coordinates, not just identity:**

If slot building requires phonetic information (e.g., for syllable structure, vowel harmony, or phonotactic constraints), then it MUST consume `ArabicLetterCoordinateCarrier`, not bare `LetterIdentityCarrier`.

Otherwise, the slot would be built on an incomplete letter representation.

## No-Leap Constitutional Tests

### For LetterIdentityCarrier:
```python
# LetterIdentityCarrier CANNOT produce:
forbidden_outputs = (
    "ArabicLetterCoordinateCarrier",  # Next layer
    "SlotCandidate",
    "SyllableCandidate",
    "MeaningCandidate",
    "HukmCandidate",
    "RealityClaim",
)
```

### For ArabicLetterCoordinateCarrier:
```python
# ArabicLetterCoordinateCarrier CANNOT produce:
forbidden_outputs = (
    "SlotCandidate",           # Next layer (requires composition)
    "SyllableCandidate",
    "MeaningCandidate",
    "HukmCandidate",
    "RealityClaim",
    "IfadahCandidate",
    "DalalahCandidate",
)

# ArabicLetterCoordinateCarrier CANNOT derive meaning from numeric coordinates:
test_abjad_numeric_has_no_semantic_force()
test_abjad_cannot_prove_meaning()
test_abjad_cannot_prove_hukm()
```

## Why NOT Option A or B?

### Option A (Keep current minimal, defer enrichment):
❌ **Problem**: If SlotCandidate needs phonetic/coordinate geometry, it would build on a bare `LetterIdentityCarrier`, creating an incomplete foundation.

### Option B (Merge everything into LetterIdentityCarrier):
❌ **Problem**: Violates separation of concerns. Identity proof should not carry phonetic coordinates, Abjad values, or fariq sets.

### Option C (Three layers) ✓:
✅ **Identity first**: Pure identity proof
✅ **Coordinates second**: Enrichment with conventional and phonetic coordinates
✅ **Slot third**: Compositional slot building with full letter representation

## Implementation Checklist

- [x] Create Abjad numeric coordinate system
- [ ] Refactor LetterIdentityCarrier to pure identity
- [ ] Remove sound_identity/makhraj from LetterIdentityCarrier rules
- [ ] Create ArabicLetterCoordinateCarrier layer
- [ ] Create letter_coordinate_adapter.py
- [ ] Create letter_coordinate_rules.py
- [ ] Add constitutional no-leap tests
- [ ] Update existing tests for three-layer architecture
- [ ] Run full test suite

## Final Judgment

```
LetterIdentityCarrier proves: This is BAA.
ArabicLetterCoordinateCarrier proves: This BAA has coordinates (unicode, script, name, abjad=2, /b/, bilabial, voiced+stop).
SlotCandidate proves: This enriched BAA enters a licensed slot with haraka, position, and alignment.
```

**No meaning. No hukm. No contextual realization. Only licensed geometric proof.**
