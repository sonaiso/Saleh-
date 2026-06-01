# GLYPH CLASSIFICATION GATE PLAN

> **Purpose:** Distinguish glyph types BEFORE assigning phonetic/morphological coordinates.
>
> **Critical:** Without this gate, agents may treat آ or ؤ as simple letters, breaking the algebraic chain.

---

## 0. Problem Statement

**Not all Arabic Unicode symbols are simple letters:**

```
ب (U+0628 BAA) = CoreArabicLetter
  → Has: makhraj, sifat, abjad, morpho role
  → Simple 1:1 mapping

أ (U+0623 ALIF_WITH_HAMZA_ABOVE) = HamzaSeatGlyph
  → Composite: Hamza + Alif seat
  → Requires decomposition

ا (U+0627 ALIF) = Context-Dependent
  → Can be: MaddGlyph | OrthographicVariant | HamzaSeat
  → Requires role disambiguation

ـ (U+0640 TATWEEL) = TatweelGlyph
  → NOT a letter
  → Spacing/justification glyph only
  → NO phonetic coordinates

آ (U+0622 ALIF_WITH_MADDA_ABOVE) = Complex
  → Madda = Hamza + Long Alif
  → Requires decomposition before coordinates
```

**Without GlyphClassificationGate:**

An agent sees `آ` → treats as simple letter → assigns wrong coordinates → breaks identity preservation.

**With GlyphClassificationGate:**

System sees `آ` → classifies as Complex → decomposes → assigns coordinates correctly → preserves identity.

---

## 1. Glyph Classification Taxonomy

### GlyphClass Enumeration

```python
from enum import Enum

class GlyphClass(Enum):
    """
    Glyph classification BEFORE coordinate assignment.
    """

    CORE_ARABIC_LETTER = "core_arabic_letter"
    # Simple Arabic letters with direct phonetic coordinates
    # Examples: ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه

    HAMZA_SEAT_GLYPH = "hamza_seat_glyph"
    # Hamza on a seat (alif, waw, yaa, or standalone)
    # Examples: أ إ ؤ ئ ء
    # Requires: Decomposition into hamza + seat

    MADD_GLYPH = "madd_glyph"
    # Long vowel / extension glyph
    # Examples: ا و ي (when functioning as madd)
    # Context-dependent classification

    WEAK_LETTER_GLYPH = "weak_letter_glyph"
    # Letters with multiple potential roles (carrier/operator/extension)
    # Examples: و ي ا
    # Requires: RoleDisambiguationGate

    TATWEEL_GLYPH = "tatweel_glyph"
    # Spacing/justification glyph, NOT a letter
    # Example: ـ (U+0640)
    # NO phonetic coordinates, NO morpho role

    ORTHOGRAPHIC_VARIANT = "orthographic_variant"
    # Orthographic form variants
    # Examples: ى (alif maqsurah), ة (taa marbutah)
    # Special coordinate handling

    COMPLEX_GLYPH = "complex_glyph"
    # Glyphs requiring decomposition
    # Examples: آ (alif with madda), لا (lam-alif ligature)
    # Requires: Decomposition gate

    PUNCTUATION = "punctuation"
    # Arabic punctuation marks
    # Examples: ، ؛ ؟
    # NO phonetic coordinates

    BOUNDARY = "boundary"
    # Whitespace, line breaks
    # NO phonetic coordinates

    RESIDUAL = "residual"
    # Unclassified or unknown glyph
```

---

## 2. Classification Rules

### Core Arabic Letter

**Criteria:**

```python
def is_core_arabic_letter(codepoint: str) -> bool:
    """
    Simple Arabic letters with direct 1:1 phonetic mapping.
    """
    CORE_LETTERS = {
        "U+0628",  # ب BAA
        "U+062A",  # ت TAA
        "U+062B",  # ث THAA
        "U+062C",  # ج JEEM
        "U+062D",  # ح HAA
        "U+062E",  # خ KHAA
        "U+062F",  # د DAL
        "U+0630",  # ذ THAAL
        "U+0631",  # ر RAA
        "U+0632",  # ز ZAAY
        "U+0633",  # س SEEN
        "U+0634",  # ش SHEEN
        "U+0635",  # ص SAAD
        "U+0636",  # ض DAAD
        "U+0637",  # ط TAA (emphatic)
        "U+0638",  # ظ ZAA (emphatic)
        "U+0639",  # ع AIN
        "U+063A",  # غ GHAIN
        "U+0641",  # ف FAA
        "U+0642",  # ق QAAF
        "U+0643",  # ك KAAF
        "U+0644",  # ل LAAM
        "U+0645",  # م MEEM
        "U+0646",  # ن NOON
        "U+0647",  # ه HAA
        # Note: و ي ا excluded (weak letters, context-dependent)
    }
    return codepoint in CORE_LETTERS
```

### Hamza Seat Glyph

**Criteria:**

```python
def is_hamza_seat_glyph(codepoint: str) -> bool:
    """
    Hamza on seat glyphs requiring decomposition.
    """
    HAMZA_SEAT_GLYPHS = {
        "U+0621",  # ء HAMZA (standalone)
        "U+0623",  # أ ALIF WITH HAMZA ABOVE
        "U+0624",  # ؤ WAW WITH HAMZA ABOVE
        "U+0625",  # إ ALIF WITH HAMZA BELOW
        "U+0626",  # ئ YAA WITH HAMZA ABOVE
    }
    return codepoint in HAMZA_SEAT_GLYPHS
```

**Decomposition requirement:**

```python
HamzaSeatDecomposition = {
    "U+0623": ("U+0621", "U+0627"),  # أ → hamza + alif
    "U+0624": ("U+0621", "U+0648"),  # ؤ → hamza + waw
    "U+0625": ("U+0621", "U+0627"),  # إ → hamza + alif (below)
    "U+0626": ("U+0621", "U+064A"),  # ئ → hamza + yaa
}
```

### Weak Letter Glyph

**Criteria:**

```python
def is_weak_letter_glyph(codepoint: str) -> bool:
    """
    Letters with multiple potential roles.
    """
    WEAK_LETTERS = {
        "U+0627",  # ا ALIF
        "U+0648",  # و WAW
        "U+064A",  # ي YAA
    }
    return codepoint in WEAK_LETTERS
```

**Role potential:**

```
ا can be:
  - MaddGlyph (long vowel /aa/)
  - OrthographicVariant (spelling alif)
  - HamzaSeat (in أ إ)
  - Carrier (in rare contexts)

و can be:
  - Carrier (consonant /w/)
  - MaddGlyph (long vowel /uu/)
  - Conjunction (particle)

ي can be:
  - Carrier (consonant /y/)
  - MaddGlyph (long vowel /ii/)
  - Morphological marker
```

### Tatweel Glyph

**Criteria:**

```python
def is_tatweel_glyph(codepoint: str) -> bool:
    """
    Spacing glyph, NOT a letter.
    """
    return codepoint == "U+0640"  # ـ TATWEEL
```

**Coordinate assignment:**

```
ـ (TATWEEL):
  makhraj_coordinate: None
  sifat_vector: None
  abjad_coordinate: None
  morpho_role_potential: None
  phonetic_proxy: None

  glyph_function: "spacing"
  forbidden_outputs: [all letter-related outputs]
```

### Complex Glyph

**Criteria:**

```python
def is_complex_glyph(codepoint: str) -> bool:
    """
    Glyphs requiring decomposition before coordinate assignment.
    """
    COMPLEX_GLYPHS = {
        "U+0622",  # آ ALIF WITH MADDA ABOVE
        "UFEFB",  # لا LAM-ALIF LIGATURE (isolated)
        "UFEFC",  # لا LAM-ALIF LIGATURE (final)
        # ... other ligatures
    }
    return codepoint in COMPLEX_GLYPHS
```

**Decomposition:**

```python
ComplexGlyphDecomposition = {
    "U+0622": ("U+0627", "MADDA"),  # آ → alif + madda (hamza + madd)
    "UFEFB": ("U+0644", "U+0627"),  # لا → lam + alif
}
```

### Orthographic Variant

**Criteria:**

```python
def is_orthographic_variant(codepoint: str) -> bool:
    """
    Orthographic form variants requiring special handling.
    """
    ORTHOGRAPHIC_VARIANTS = {
        "U+0629",  # ة TAA MARBUTAH
        "U+0649",  # ى ALIF MAQSURAH
    }
    return codepoint in ORTHOGRAPHIC_VARIANTS
```

---

## 3. GlyphClassificationGate Implementation

### Gate Operation

```python
class GlyphClassificationGate:
    """
    Classify glyph type BEFORE coordinate assignment.
    """

    def classify(
        self,
        letter_identity: LetterIdentityCarrier
    ) -> GlyphClassificationResult:
        """
        Classify glyph and determine coordinate assignment strategy.

        Returns:
            GlyphClassificationResult with:
              - glyph_class
              - coordinate_strategy
              - decomposition_required
              - residuals
        """

        codepoint = letter_identity.unicode_identity

        # Core Arabic letter (simple case)
        if is_core_arabic_letter(codepoint):
            return GlyphClassificationResult(
                glyph_class=GlyphClass.CORE_ARABIC_LETTER,
                coordinate_strategy="direct",
                decomposition_required=False,
                residuals=()
            )

        # Hamza seat (requires decomposition)
        if is_hamza_seat_glyph(codepoint):
            return GlyphClassificationResult(
                glyph_class=GlyphClass.HAMZA_SEAT_GLYPH,
                coordinate_strategy="decompose_then_coordinate",
                decomposition_required=True,
                decomposition=HamzaSeatDecomposition.get(codepoint),
                residuals=()
            )

        # Weak letter (context-dependent)
        if is_weak_letter_glyph(codepoint):
            return GlyphClassificationResult(
                glyph_class=GlyphClass.WEAK_LETTER_GLYPH,
                coordinate_strategy="role_disambiguation_required",
                decomposition_required=False,
                residuals=(
                    Residual(
                        effect="defer:role_potential_context_dependent:present",
                        scope="glyph_classification"
                    ),
                )
            )

        # Tatweel (no coordinates)
        if is_tatweel_glyph(codepoint):
            return GlyphClassificationResult(
                glyph_class=GlyphClass.TATWEEL_GLYPH,
                coordinate_strategy="no_coordinates",
                decomposition_required=False,
                residuals=()
            )

        # Complex glyph (decomposition required)
        if is_complex_glyph(codepoint):
            return GlyphClassificationResult(
                glyph_class=GlyphClass.COMPLEX_GLYPH,
                coordinate_strategy="decompose_then_coordinate",
                decomposition_required=True,
                decomposition=ComplexGlyphDecomposition.get(codepoint),
                residuals=()
            )

        # Orthographic variant (special handling)
        if is_orthographic_variant(codepoint):
            return GlyphClassificationResult(
                glyph_class=GlyphClass.ORTHOGRAPHIC_VARIANT,
                coordinate_strategy="variant_specific",
                decomposition_required=False,
                residuals=()
            )

        # Unclassified
        return GlyphClassificationResult(
            glyph_class=GlyphClass.RESIDUAL,
            coordinate_strategy="none",
            decomposition_required=False,
            residuals=(
                Residual(
                    effect="defer:glyph_class_unknown:present",
                    scope="glyph_classification"
                ),
            )
        )
```

---

## 4. Coordinate Assignment Strategy

### Strategy Mapping

| GlyphClass | CoordinateStrategy | Actions |
|------------|-------------------|---------|
| CORE_ARABIC_LETTER | direct | Assign all coordinates directly |
| HAMZA_SEAT_GLYPH | decompose_then_coordinate | Decompose, assign coordinates to components |
| WEAK_LETTER_GLYPH | role_disambiguation_required | Assign potential coordinates, defer final role |
| TATWEEL_GLYPH | no_coordinates | NO coordinates, mark as spacing glyph |
| COMPLEX_GLYPH | decompose_then_coordinate | Decompose, process components |
| ORTHOGRAPHIC_VARIANT | variant_specific | Special coordinate rules per variant |
| RESIDUAL | none | NO coordinates, produce residual |

### Example: Core Arabic Letter (ب)

```python
# Input: LetterIdentityCarrier(unicode_identity="U+0628", name_identity="BAA")

glyph_result = glyph_gate.classify(letter_identity)
# glyph_result.glyph_class = GlyphClass.CORE_ARABIC_LETTER
# glyph_result.coordinate_strategy = "direct"

# Proceed to coordinate assignment:
coordinates = {
    "makhraj": MakhrajCoordinate(spatial_source="BILABIAL", ...),
    "sifat": SifatVector(voicing=VOICED, manner=STOP, ...),
    "abjad": AbjadCoordinate(numeric_value=2, semantic_force="FORBIDDEN"),
    "phonetic_proxy": "/b/",
    "morpho_role_potential": MorphoRolePotential(carrier_potential=True, ...),
}
```

### Example: Hamza Seat Glyph (أ)

```python
# Input: LetterIdentityCarrier(unicode_identity="U+0623", name_identity="ALIF_WITH_HAMZA_ABOVE")

glyph_result = glyph_gate.classify(letter_identity)
# glyph_result.glyph_class = GlyphClass.HAMZA_SEAT_GLYPH
# glyph_result.decomposition = ("U+0621", "U+0627")

# Decompose into:
#   Component 1: Hamza (U+0621) → assign hamza coordinates
#   Component 2: Alif seat (U+0627) → assign alif coordinates (context: seat)

# Result: Composite coordinate set with preserved decomposition trace
```

### Example: Tatweel Glyph (ـ)

```python
# Input: LetterIdentityCarrier(unicode_identity="U+0640", name_identity="TATWEEL")

glyph_result = glyph_gate.classify(letter_identity)
# glyph_result.glyph_class = GlyphClass.TATWEEL_GLYPH
# glyph_result.coordinate_strategy = "no_coordinates"

# Result: NO ArabicLetterCoordinateCarrier produced
# Output: TatweelGlyph (spacing metadata only)
```

---

## 5. Integration with ArabicLetterCoordinateCarrier

### Updated Adapter Logic

```python
class ArabicLetterCoordinateAdapter(QiyasKernelAdapter):
    """
    Enrich LetterIdentityCarrier with coordinates.

    REQUIRES: GlyphClassificationGate
    """

    def __init__(self):
        self.glyph_gate = GlyphClassificationGate()
        # ... other systems

    def adapt(self, letter_identity: LetterIdentityCarrier) -> CandidateSet:
        # Step 1: Classify glyph
        glyph_result = self.glyph_gate.classify(letter_identity)

        # Step 2: Route by strategy
        if glyph_result.coordinate_strategy == "direct":
            return self._assign_direct_coordinates(letter_identity, glyph_result)

        elif glyph_result.coordinate_strategy == "decompose_then_coordinate":
            return self._decompose_and_coordinate(letter_identity, glyph_result)

        elif glyph_result.coordinate_strategy == "role_disambiguation_required":
            return self._assign_potential_coordinates(letter_identity, glyph_result)

        elif glyph_result.coordinate_strategy == "no_coordinates":
            return self._produce_spacing_glyph(letter_identity, glyph_result)

        else:  # none or residual
            return self._produce_residual(letter_identity, glyph_result)
```

---

## 6. Source-of-Truth

**Canonical source:**

```
src/qiyas_core/gates/glyph_classification_gate.py
```

**Contains:**

- GlyphClass enum
- Classification logic
- Decomposition mappings
- Coordinate strategy routing

**Imported by:**

- `arabic_letter_coordinate_adapter.py`
- `letter_coordinate_rules.py`
- Tests

**NOT duplicated in:**

- Rules (import only)
- Tests (import only)
- Other adapters

---

## 7. Residuals

### Glyph Classification Residuals

```
defer:glyph_class_unknown:present
  Cause: Glyph not in classification registry

defer:glyph_class_ambiguous:present
  Cause: Multiple possible classifications (context required)

defer:decomposition_required:present
  Cause: Complex glyph requires decomposition gate

defer:role_potential_context_dependent:present
  Cause: Weak letter requires role disambiguation
```

---

## 8. Implementation Priority

**Phase 1: Documentation (This PR)**
- [x] GLYPH_CLASSIFICATION_GATE_PLAN.md (this document)

**Phase 2: Registry Creation**
- [ ] Create `glyph_classification_registry.py`
- [ ] Document all glyph types (core, hamza, madd, weak, tatweel, etc.)
- [ ] Document decomposition mappings

**Phase 3: Gate Implementation**
- [ ] Implement `GlyphClassificationGate` class
- [ ] Implement classification logic
- [ ] Add decomposition support

**Phase 4: Integration**
- [ ] Update `ArabicLetterCoordinateAdapter` to use gate
- [ ] Add glyph_class field to `ArabicLetterCoordinateCarrier`
- [ ] Route coordinate assignment by strategy

**Phase 5: Testing**
- [ ] Test core letter classification
- [ ] Test hamza seat decomposition
- [ ] Test weak letter deferral
- [ ] Test tatweel exclusion
- [ ] Test residual production

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Planning document for Layer 2 completion
**Authority:** Required before coordinate expansion
