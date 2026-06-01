# LAYER 2 RESIDUALS

> **Purpose:** Exhaustive specification of residuals for Layer 2 (Atomic Identity and Coordinates).
>
> **Law:** No silent failure. Every blocking condition produces an explicit residual.

---

## 0. Residual Philosophy

**From PROJECT_MATHEMATICAL_FOUNDATION.md:**

```
Failure = ResidualSet

Every failure → explicit Residual
No silent failure
No hidden errors
No exceptions without trace
```

**From CLAUDE.md:**

```
Residuals must not be hidden or silently discarded.
```

**Layer 2 must produce residuals for:**

1. Identity proofs that cannot complete
2. Coordinate assignments that fail
3. Glyph classifications that are ambiguous
4. Evidence that is insufficient
5. Fariq (invalidating differences) that are present

---

## 1. Layer 2A: LetterIdentityCarrier Residuals

### Identity Residuals

```
defer:letter_identity_ambiguous:present
  Scope: letter_identity
  Cause: Multiple possible identities (context-dependent Unicode)
  Example: Hamza seat glyphs without context
  Resolution: Requires GlyphClassificationGate or context

defer:script_identity_uncertain:present
  Scope: letter_identity
  Cause: Non-standard Unicode sequence or non-Arabic script
  Example: Arabic presentation forms, compatibility characters
  Resolution: Normalize Unicode or defer

fariq:letter_identity_conflict:present
  Scope: letter_identity
  Cause: Invalidating difference detected (wrong letter claimed)
  Example: Claimed BAA but codepoint is TAA
  Resolution: Correct identity claim
```

### Classification Residuals

```
defer:letter_class_unknown:present
  Scope: letter_identity
  Cause: Letter class cannot be determined
  Example: Non-classical letter, loan word letter
  Resolution: Extend letter_class_registry.py

defer:letter_class_context_dependent:present
  Scope: letter_identity
  Cause: Weak letter (و/ي/ا) requires context for classification
  Example: ا can be madd, orthographic, or seat
  Resolution: Defer to GlyphClassificationGate
```

---

## 2. Layer 2B: HarakaFunctionCarrier Residuals

### Function Residuals

```
defer:haraka_function_unknown:present
  Scope: haraka_function
  Cause: Haraka function cannot be determined
  Example: Non-standard diacritic, rare mark
  Resolution: Extend haraka_function_registry.py

defer:haraka_function_context_dependent:present
  Scope: haraka_function
  Cause: Function depends on position or adjacent harakat
  Example: Sukun as closure vs pause
  Resolution: Requires sequence context from ConditionedTypedSequence

fariq:haraka_function_conflict:present
  Scope: haraka_function
  Cause: Claimed function contradicts Unicode identity
  Example: Claimed FATHA_OPENING but codepoint is DAMMA
  Resolution: Correct function claim
```

### Operation Residuals

```
defer:haraka_operation_requires_carrier:present
  Scope: haraka_function
  Cause: Haraka requires carrier but none present
  Example: Orphan haraka at sequence start
  Resolution: Deferred until ConditionedTypedSequence provides binding evidence
```

---

## 3. Layer 2C: PositionCarrier Residuals

### Position Residuals

```
defer:position_context_insufficient:present
  Scope: position
  Cause: Cannot determine position without sequence context
  Example: Isolated codepoint without sequence
  Resolution: Requires ConditionedTypedSequence

defer:position_boundary_ambiguous:present
  Scope: position
  Cause: Boundary position unclear (word-initial vs phrase-initial)
  Example: Alif after space (could be word boundary or emphasis space)
  Resolution: Requires higher-level boundary evidence
```

---

## 4. Layer 2D: ConditionedTypedSequence Residuals

### Alignment Residuals

```
defer:alignment_missing:present
  Scope: alignment
  Cause: Cannot align letter and haraka (no adjacency)
  Example: Letter followed by boundary, not haraka
  Resolution: Deferred until slot formation (may be sukun context)

defer:carrier_binding_incomplete:present
  Scope: alignment
  Cause: Carrier exists but binding evidence insufficient
  Example: Shadda without carrier
  Resolution: Block or defer slot formation

fariq:alignment_conflict:present
  Scope: alignment
  Cause: Letter-haraka combination forbidden
  Example: Hamza with tanwin in non-terminal position
  Resolution: Block slot formation
```

### Boundary Residuals

```
defer:boundary_preservation_required:present
  Scope: sequence_admissibility
  Cause: Boundary symbol encountered, must not enter slot
  Example: Whitespace in sequence
  Resolution: Preserve as boundary, do not enter slot

defer:punctuation_exclusion_required:present
  Scope: sequence_admissibility
  Cause: Punctuation symbol encountered
  Example: Arabic comma ،
  Resolution: Preserve as punctuation, do not enter slot
```

---

## 5. Layer 2X: ArabicLetterCoordinateCarrier Residuals

### Glyph Classification Residuals

```
defer:glyph_class_unknown:present
  Scope: glyph_classification
  Cause: Glyph not in classification registry
  Example: Unicode Arabic supplement characters
  Resolution: Extend glyph_classification_registry.py

defer:glyph_class_ambiguous:present
  Scope: glyph_classification
  Cause: Multiple possible glyph classes (context required)
  Example: ا (ALIF) as madd vs orthographic vs seat
  Resolution: Requires role disambiguation

defer:decomposition_required:present
  Scope: glyph_classification
  Cause: Complex glyph requires decomposition before coordinates
  Example: آ (ALIF_WITH_MADDA_ABOVE) = hamza + long alif
  Resolution: Apply decomposition gate, then coordinate components
```

### Makhraj Coordinate Residuals

```
defer:makhraj_coordinate_unknown:present
  Scope: makhraj_coordinate
  Cause: Letter not in makhraj registry
  Example: Non-classical letter, loan word
  Resolution: Extend makhraj_coordinate_system.py or defer

defer:makhraj_coordinate_ambiguous:present
  Scope: makhraj_coordinate
  Cause: Makhraj varies by dialect or context
  Example: ج (JEEM) as affricate vs fricative
  Resolution: Specify dialect system or defer

fariq:makhraj_coordinate_conflict:present
  Scope: makhraj_coordinate
  Cause: Assigned makhraj conflicts with letter identity
  Example: Bilabial makhraj claimed for alveolar letter
  Resolution: Correct makhraj assignment
```

### Sifat Vector Residuals

```
defer:sifat_vector_incomplete:present
  Scope: sifat_vector
  Cause: One or more sifat axes cannot be determined
  Example: Ambiguous voicing for weak letter in context
  Resolution: Complete missing axes or defer

defer:sifat_axis_ambiguous:{axis}:present
  Scope: sifat_vector
  Cause: Specific axis requires context or dialect specification
  Example: Emphasis for ر (RAA) context-dependent
  Resolution: Specify context or defer

fariq:sifat_conflict:present
  Scope: sifat_vector
  Cause: Sifat value contradicts letter identity
  Example: VOICED claimed for inherently voiceless letter
  Resolution: Correct sifat assignment
```

### Abjad Coordinate Residuals

```
defer:abjad_value_undefined:present
  Scope: abjad_coordinate
  Cause: Letter not in Abjad system
  Example: Non-classical letters, loan words
  Resolution: Extend abjad_system.py or assign None

defer:abjad_system_ambiguous:present
  Scope: abjad_coordinate
  Cause: Multiple Abjad numbering systems (eastern vs western)
  Example: ج = 3 (eastern) vs 5 (maghrebi)
  Resolution: Specify system or defer

fariq:abjad_semantic_force_violated:present
  Scope: abjad_coordinate
  Cause: Attempt to derive meaning from numeric value
  Example: Code tries to generate meaning from BAA=2
  Resolution: BLOCK — semantic_force=FORBIDDEN enforcement
```

### Morphological Role Potential Residuals

```
defer:role_potential_context_dependent:present
  Scope: morpho_role_potential
  Cause: Weak letter (و/ي/ا) role depends on context
  Example: و can be carrier, operator, or extension
  Resolution: Deferred until RoleDisambiguationGate

defer:morpho_role_requires_disambiguation:present
  Scope: morpho_role_potential
  Cause: Multiple potential roles, cannot determine without context
  Example: Hamza as carrier vs orthographic marker
  Resolution: Requires RoleDisambiguationGate
```

### Phonetic Proxy Residuals

```
defer:phonetic_proxy_unavailable:present
  Scope: phonetic_proxy
  Cause: IPA approximation not available for letter
  Example: Non-standard letters
  Resolution: Extend phonetic_proxy_system.py or defer

defer:phonetic_proxy_approximate_only:present
  Scope: phonetic_proxy
  Cause: IPA is approximation, not authoritative phonetic identity
  Note: Always present — phonetic proxy is convenience, not proof
  Resolution: Use for reference only, not identity
```

---

## 6. Fariq (Invalidating Difference) Residuals

### General Fariq Pattern

```
fariq:{letter1}_vs_{letter2}_{axis}:present
  Scope: fariq_negation
  Cause: Invalidating difference detected between claimed letter and alternative
  Example: fariq:baa_vs_meem_nasality:present
  Resolution: Identity claim is wrong, correct it
```

### Specific Fariq Examples

```
fariq:baa_vs_meem_nasality:present
  Cause: Claimed BAA but nasality axis shows NASAL (should be ORAL)
  Resolution: Correct to MEEM

fariq:seen_vs_saad_emphasis:present
  Cause: Claimed SEEN but emphasis axis shows EMPHATIC (should be NON_EMPHATIC)
  Resolution: Correct to SAAD

fariq:taa_vs_taa_emphatic_emphasis:present
  Cause: Claimed plain TAA but emphasis axis shows EMPHATIC
  Resolution: Correct to emphatic TAA (ط)

fariq:waw_vs_faa_frication:present
  Cause: Claimed WAW but frication axis shows FRICATIVE (should be NON_FRICATIVE)
  Resolution: Correct to FAA
```

---

## 7. Evidence Insufficiency Residuals

### General Evidence Pattern

```
defer:evidence_insufficient:{claim_type}:present
  Scope: evidence
  Cause: Required evidence claim missing or insufficient rank
  Resolution: Add evidence or increase rank
```

### Specific Evidence Residuals

```
defer:evidence_insufficient:wasf:present
  Cause: Effective attribute (wasf) claim missing
  Resolution: Add وصف: evidence claim

defer:evidence_insufficient:illah:present
  Cause: Licensing cause (illah) claim missing
  Resolution: Add علة: evidence claim

defer:evidence_insufficient:rank:present
  Cause: Evidence rank below required minimum
  Example: NO_EVIDENCE when FORMAL_STRUCTURE required
  Resolution: Strengthen evidence or defer

defer:evidence_source_missing:present
  Cause: Evidence claim lacks source citation
  Example: Coordinate claim without source="abjad_system.py"
  Resolution: Add source citation
```

---

## 8. Residual Handling Strategy

### Defer vs Block vs Fariq

**Defer (defer:*:present):**
- Cannot complete now, may complete later with more context
- Preserves residual for inspection
- Allows processing to continue (non-blocking)

**Block (implicit through absence of success):**
- Cannot proceed without required component
- No candidate produced
- Must be resolved before continuing

**Fariq (fariq:*:present):**
- Invalidating difference detected
- Identity claim is wrong
- BLOCKS candidate production
- Must be corrected

### Residual Preservation

```python
# ALL residuals MUST be preserved in output candidate

@dataclass(frozen=True)
class ArabicLetterCoordinateCarrier:
    # ... all fields ...

    residuals: tuple[Residual, ...]  # NEVER empty on partial success

# Example with residuals:
ArabicLetterCoordinateCarrier(
    unicode_identity="U+0627",  # ا ALIF
    name_identity="ALIF",
    glyph_class=GlyphClass.WEAK_LETTER_GLYPH,
    # ... some coordinates assigned ...
    residuals=(
        Residual(
            effect="defer:role_potential_context_dependent:present",
            scope="morpho_role_potential"
        ),
        Residual(
            effect="defer:glyph_class_ambiguous:present",
            scope="glyph_classification"
        ),
    )
)
```

---

## 9. Residual Documentation Requirements

**Every adapter MUST document:**

1. What residuals it produces
2. Under what conditions
3. What resolution is required
4. Whether defer (non-blocking) or fariq (blocking)

**Example adapter documentation:**

```python
class ArabicLetterCoordinateAdapter(QiyasKernelAdapter):
    """
    Enrich LetterIdentityCarrier with coordinates.

    RESIDUALS PRODUCED:
      defer:glyph_class_unknown:present
        Condition: Glyph not in registry
        Resolution: Extend registry or defer

      defer:sifat_vector_incomplete:present
        Condition: One or more axes unknown
        Resolution: Complete axes or defer

      fariq:{letter1}_vs_{letter2}_{axis}:present
        Condition: Invalidating difference detected
        Resolution: Correct identity claim (BLOCKING)

      defer:role_potential_context_dependent:present
        Condition: Weak letter role requires context
        Resolution: Defer to RoleDisambiguationGate
    """
```

---

## 10. Test Requirements

**Every Layer 2 component MUST have tests for:**

### Identity Layer Tests

- [ ] Letter identity success (canonical case)
- [ ] Letter identity with defer:letter_identity_ambiguous
- [ ] Letter identity with fariq:letter_identity_conflict (blocking)

### Coordinate Layer Tests

- [ ] Makhraj coordinate success
- [ ] Makhraj coordinate with defer:makhraj_coordinate_unknown
- [ ] Sifat vector success (6 axes complete)
- [ ] Sifat vector with defer:sifat_vector_incomplete
- [ ] Sifat vector with fariq:sifat_conflict (blocking)
- [ ] Abjad coordinate success with semantic_force=FORBIDDEN
- [ ] Abjad coordinate with defer:abjad_value_undefined
- [ ] Abjad coordinate blocking fariq:abjad_semantic_force_violated

### Glyph Classification Tests

- [ ] Core letter classification success
- [ ] Hamza seat with defer:decomposition_required
- [ ] Weak letter with defer:role_potential_context_dependent
- [ ] Tatweel with no coordinates
- [ ] Unknown glyph with defer:glyph_class_unknown

### Fariq Negation Tests

- [ ] fariq:baa_vs_meem_nasality correctly negated for BAA
- [ ] fariq:baa_vs_meem_nasality present blocks MEEM claim for BAA
- [ ] fariq:seen_vs_saad_emphasis correctly negated for SEEN
- [ ] All 28+ letters have complete fariq sets

---

## 11. Integration

**This document implements:**
- PROJECT_MATHEMATICAL_FOUNDATION.md § 8 (Mathematical Invariants: Residual Non-Concealment)
- FULL_LAYER_2_PLAN.md § 8 (Residual Specifications)
- SOURCE_OF_TRUTH_REGISTRY.md (residual as failure mode)

**This document is required by:**
- All Layer 2 adapters (must produce documented residuals)
- All Layer 2 tests (must test residual production)
- QiyasKernel (residual preservation enforcement)

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Constitutional requirement for Layer 2 completion
**Authority:** Implements residual non-concealment invariant
