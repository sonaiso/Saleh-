# LAYER REGISTRY — Canonical Layer Documentation

> **Purpose:** Single source of truth for all qiyas layers, their status, inputs, outputs, and forbidden jumps.
>
> **Authority:** This registry is the authoritative reference for layer architecture. All agents must consult this before creating or modifying layers.

---

## Registry Format

Each layer entry follows this template:

```markdown
### Layer N: LayerName

**Input:** InputCandidateType
**Output:** OutputCandidateType
**Status:** canonical | partial | experimental | not_implemented
**Source PR:** #N (or #N + corrected by #M)
**Coverage:** Full | Partial (scope description)
**Missing:** (if partial) What components are not yet implemented

**Forbidden Outputs:** (list all forbidden jump targets)

**Note:** (critical constraints, warnings, or architectural decisions)
```

---

## Core Kernel (Foundation)

### Layer -1: QiyasKernel

**Type:** Algebraic kernel (not a layer adapter, but the foundation for all layers)
**Input:** QiyasRequest (asl, far, rule, evidence, context)
**Output:** CandidateSet (status, rank, residuals, trace)
**Status:** canonical
**Source PR:** #1
**Coverage:** Full

**Core Components:**
- Evidence validation (wasf, illah, wadi gates)
- Invalidating difference checking (fariq)
- Deferral state handling (defer)
- Identity preservation (neutral element)
- Rank ceiling enforcement (meet semantics)
- Trace preservation
- Residual collection
- Forbidden output enforcement

**Constitutional Gates Enforced:**
1. Asl (established source)
2. Far (determined target)
3. Wasf (effective attribute)
4. Illah (licensing cause)
5. Wadi (6 validity gates: cause, condition, obstacle, validity, corruption, nullity)
6. Fariq (invalidating differences)

**Note:** All layer adapters MUST use QiyasKernel. Direct function calls bypassing the kernel violate constitutional architecture.

---

## Layer 0: Unicode Membership

### Layer 0: UnicodeCandidate

**Input:** Raw codepoint (int or str)
**Output:** UnicodeCandidate
**Status:** canonical
**Source PR:** #1
**Coverage:** Full (Arabic Unicode blocks only)

**Proof Obligation:** Is this codepoint within Arabic Unicode range?

**Evidence Required:**
- `اصل:established` (Arabic Unicode block as source)
- `فرع:determined` (input codepoint as target)
- `وصف:is_in_arabic_range:evidenced`
- `علة:arabic_unicode_membership:verified`

**Invalidating Differences:**
- `fariq:non_arabic_codepoint:present` (blocks non-Arabic codepoints)

**Forbidden Outputs:**
- TypedCodePoint
- LetterCodePoint / HarakaCodePoint / BoundaryCodePoint / PunctuationCodePoint
- LetterIdentityCarrier
- HarakaFunctionCarrier
- SlotCandidate
- SyllableCandidate
- MeaningCandidate
- HukmCandidate
- RealityClaim

**Note:** First canonical layer, demonstrates complete constitutional compliance pattern.

---

## Layer 1: Typed CodePoint Classification

### Layer 1: TypedCodePoint

**Input:** UnicodeCandidate
**Output:** LetterCodePoint | HarakaCodePoint | BoundaryCodePoint | PunctuationCodePoint | ResidualCodePoint
**Status:** canonical
**Source PR:** #20 (initial), #23 (algebraic hardening)
**Coverage:** Full

**Proof Obligation:** Classify Unicode candidate into exactly one disjoint type.

**Evidence Required (General):**
- `وصف:is_classifiable_codepoint:evidenced` (all types)
- `علة:belongs_to_typed_domain:verified` (all types)

**Evidence Required (Type-Specific, PR #23):**
- Letter: `وصف:is_arabic_letter:evidenced`, `علة:belongs_to_letter_class:verified`
- Haraka: `وصف:is_arabic_haraka:evidenced`, `علة:belongs_to_haraka_class:verified`
- Boundary: `وصف:is_whitespace_boundary:evidenced`, `علة:belongs_to_boundary_class:verified`
- Punctuation: `وصف:is_arabic_punctuation:evidenced`, `علة:belongs_to_punctuation_class:verified`
- Residual: `وصف:is_unclassified_codepoint:evidenced`, `علة:belongs_to_residual_class:verified`

**Invalidating Differences (PR #23, disjoint union proof):**
- `fariq:multiple_classes_claimed:present`
- `fariq:ambiguous_classification:present`
- `fariq:letter_haraka_overlap:present`
- `fariq:boundary_punctuation_overlap:present`

**Forbidden Outputs:**
- AtomicUnitCandidate (old experimental name)
- LetterIdentityCarrier (next layer)
- HarakaFunctionCarrier (next layer)
- SlotCandidate
- SyllableCandidate
- MeaningCandidate

**Note:** Classification is proven within QiyasKernel via type-specific evidence, not just dynamic output_candidate_type assignment. This is the critical algebraic hardening from PR #23.

---

## Layer 2: Atomic Identity and Function Proofs (Parallel)

**Critical Architecture Note:** Layer 2 is NOT a linear chain. It consists of PARALLEL atomic proofs that are independent:

```
TypedCodePoint branches:
  → LetterIdentityCarrier (atomic identity proof, independent)
  → HarakaFunctionCarrier (atomic function proof, independent)

TypedCodePoint* (sequence):
  → ConditionedTypedSequence → AlignmentEvidence + PositionCarrier

These branches are INDEPENDENT and do NOT depend on each other.
```

### Layer 2A: LetterIdentityCarrier

**Input:** LetterCodePoint
**Output:** LetterIdentityCarrier
**Status:** canonical
**Source PR:** #26 (initial), #27 (corrected to pure identity)
**Coverage:** Full (pure identity only, no coordinates)

**Proof Obligation:** What is the identity of this letter? (NOT its coordinates)

**Contains:**
- unicode_identity: str (e.g., "U+0628")
- script_identity: str (e.g., "ARABIC_LETTER_BAA")
- name_identity: str (e.g., "BAA" / "باء")
- specific_letter_identity: str (e.g., "letter:baa")
- letter_class: str (e.g., "consonant")
- identity_ids: tuple[str, ...] (preserved from input)
- evidence: EvidenceSet
- rank: EvidenceRank
- trace_ids: tuple[str, ...]
- residuals: tuple[Residual, ...]

**Does NOT Contain (moved to Layer X):**
- sound_identity (moved to ArabicLetterCoordinateCarrier)
- makhraj (moved to ArabicLetterCoordinateCarrier)
- sifat (moved to ArabicLetterCoordinateCarrier)
- abjad_coordinate (moved to ArabicLetterCoordinateCarrier)
- phonetic_proxy (moved to ArabicLetterCoordinateCarrier)

**Evidence Required:**
- `وصف:has_unicode_identity:{codepoint}:evidenced`
- `وصف:has_script_identity:{letter_name}:evidenced`
- `علة:letter_identity_is:{letter_name}:verified`

**Invalidating Differences:**
- Invalid letter classification
- Identity ambiguity
- Non-letter codepoint

**Forbidden Outputs:**
- ArabicLetterCoordinateCarrier (next enrichment layer)
- HarakaFunctionCarrier (parallel proof, not output of letter layer)
- SlotCandidate (requires composition)
- SyllableCandidate
- MeaningCandidate
- HukmCandidate
- RealityClaim

**Note:** Pure identity only. No coordinates, no phonetics, no numeric values. This is the critical correction from PR #27 following the three-layer letter architecture.

**Constitutional Requirement:** LetterIdentityCarrier does NOT require ConditionedTypedSequence. It is an atomic proof independent of sequence context.

### Layer 2B: HarakaFunctionCarrier

**Input:** HarakaCodePoint
**Output:** HarakaFunctionCarrier
**Status:** canonical
**Source PR:** #25 (initial scope), #28 (corrected)
**Coverage:** Full

**Proof Obligation:** What is the functional role of this haraka?

**Contains:**
- unicode_identity: str (e.g., "U+064E")
- haraka_identity: str (e.g., "FATHA")
- functional_role: str (e.g., "OPENING", "CLOSING", "NEUTRAL")
- haraka_class: str (e.g., "short_vowel", "tanwin", "sukun", "shadda")
- identity_ids: tuple[str, ...]
- evidence: EvidenceSet
- rank: EvidenceRank
- trace_ids: tuple[str, ...]
- residuals: tuple[Residual, ...]

**Evidence Required:**
- `وصف:has_unicode_identity:{codepoint}:evidenced`
- `وصف:has_haraka_identity:{haraka_name}:evidenced`
- `وصف:has_functional_role:{role}:evidenced`
- `علة:haraka_function_is:{function}:verified`

**Invalidating Differences:**
- Invalid haraka classification
- Function role conflict
- Non-haraka codepoint

**Forbidden Outputs:**
- LetterIdentityCarrier (parallel proof, not output of haraka layer)
- SlotCandidate (requires composition)
- SyllableCandidate
- MeaningCandidate
- HukmCandidate

**Note:** Functional haraka classification (opening/closing/neutral), not just Unicode identity.

**Constitutional Requirement:** HarakaFunctionCarrier does NOT require ConditionedTypedSequence. It is an atomic proof independent of sequence context.

### Layer 2C: PositionCarrier

**Input:** ConditionedTypedSequence + index evidence
**Output:** PositionCarrier
**Status:** canonical
**Source PR:** #28
**Coverage:** Full

**Proof Obligation:** What is the position context of this element in the sequence?

**Contains:**
- position_index: int
- position_context: str (e.g., "P0", "P1", "terminal", "medial")
- sequence_ref: str (reference to parent ConditionedTypedSequence)
- identity_ids: tuple[str, ...]
- evidence: EvidenceSet
- rank: EvidenceRank
- trace_ids: tuple[str, ...]
- residuals: tuple[Residual, ...]

**Evidence Required:**
- `وصف:has_position_index:{index}:evidenced`
- `وصف:has_position_context:{context}:evidenced`
- `علة:position_is_valid:verified`

**Forbidden Outputs:**
- SlotCandidate (requires additional composition)
- SyllableCandidate
- MeaningCandidate

**Note:** Position evidence from sequence context, not independent atomic proof.

### Layer 2D: ConditionedTypedSequence + AlignmentEvidence

**Input:** TypedCodePoint* (sequence of typed codepoints)
**Output:** ConditionedTypedSequence, AlignmentEvidence, CarrierBindingCandidate, PositionEvidence, BoundaryEvidence, ResidualPreservationEvidence
**Status:** canonical
**Source PR:** #28
**Coverage:** Full

**Proof Obligation:** Is this typed codepoint sequence well-conditioned? Can marks be bound to carriers? Are boundaries preserved?

**CRITICAL: This layer does NOT produce:**
- ❌ LetterIdentityCarrier (separate atomic proof, Layer 2A)
- ❌ HarakaFunctionCarrier (separate atomic proof, Layer 2B)
- ❌ SlotCandidate (next layer, requires composition)

**This layer ONLY produces:**
- ✅ ConditionedTypedSequence (sequence admissibility proof)
- ✅ AlignmentEvidence (elements can be aligned)
- ✅ CarrierBindingCandidate (haraka has a carrier, with evidence)
- ✅ PositionEvidence (position context for each element)
- ✅ BoundaryEvidence (boundaries are preserved, not entered into slots)
- ✅ ResidualPreservationEvidence (residuals are tracked, not hidden)

**Evidence Produced:**
- Haraka has carrier: `CarrierBindingCandidate(letter_ref, haraka_ref, binding_evidence, residuals, trace)`
- Orphan haraka: `defer:haraka_without_carrier:present`
- Shadda requires carrier: `defer:shadda_without_carrier:present`
- Tanwin terminal sensitivity: `defer:tanwin_position_sensitive:present`
- Boundary preservation: `BoundaryEvidence(boundary_type, preserved=True)`
- Punctuation exclusion: evidence that punctuation does not enter slots

**Forbidden Outputs:**
- LetterIdentityCarrier (atomic proof, not sequence proof)
- HarakaFunctionCarrier (atomic proof, not sequence proof)
- SlotCandidate (requires Layer 2A + Layer 2B + Layer 2C + Layer 2D evidence)
- SyllableCandidate
- MeaningCandidate

**Note:** This is the critical architectural distinction. ConditionedTypedSequence produces ALIGNMENT and ADMISSIBILITY evidence, not identity proofs. It proves "this haraka CAN bind to this carrier" but does NOT prove "this is BAA" or "this is FATHA". Those are separate atomic obligations.

---

## Layer 3: Slot Candidate Formation

### Layer 3: SlotCandidate

**Input:** LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier + AlignmentEvidence
**Output:** SlotCandidate
**Status:** canonical
**Source PR:** #25 (initial), #28 (corrected to require all four ingredients)
**Coverage:** Full

**Proof Obligation:** Can this letter + haraka + position + alignment form a licensed slot?

**Required Ingredients (ALL FOUR MANDATORY):**
1. LetterIdentityCarrier (from Layer 2A)
2. HarakaFunctionCarrier (from Layer 2B)
3. PositionCarrier (from Layer 2C)
4. AlignmentEvidence (from Layer 2D)

**Formation Rule:**
```
SlotCandidate = LetterIdentityCarrier ⊗ HarakaFunctionCarrier ⊗ PositionCarrier ⊗ AlignmentEvidence
```

**Blocking Conditions:**
- Missing letter identity → `defer:letter_identity_missing:present`
- Missing haraka function → `defer:haraka_function_missing:present`
- Missing position → `defer:position_missing:present`
- Missing alignment → `defer:alignment_missing:present`
- Invalidating difference → `fariq:{difference}:present`

**Forbidden Outputs:**
- SlotGeometry (not canonical, experimental only)
- SyllableCandidate (next layer, not implemented)
- MeaningCandidate
- HukmCandidate
- RealityClaim

**Note:** SlotCandidate is a POTENTIAL slot, not a final slot. It remains candidate/potential only. It does NOT produce SlotGeometry directly.

**Constitutional Requirement:** No SlotCandidate may be produced unless ALL FOUR ingredients are present. Partial slots are not licensed.

---

## Layer X: Coordinate Enrichment (Partial)

### Layer X: ArabicLetterCoordinateCarrier

**Input:** LetterIdentityCarrier
**Output:** ArabicLetterCoordinateCarrier
**Status:** partial canonical slice
**Source PR:** #27
**Coverage:** BAA, TAA, SEEN, KAF only (minimal validation slice)
**Missing:** Full alphabet, GlyphClassificationGate, complete SifatVector

**Proof Obligation:** What are the coordinates of this letter within representation systems?

**Contains:**
1. **Identity (inherited from LetterIdentityCarrier):**
   - All identity fields preserved

2. **Conventional Coordinates:**
   - abjad_coordinate: AbjadCoordinate | None
     - system: "ABJAD"
     - numeric_value: int (e.g., 2 for BAA)
     - semantic_force: "FORBIDDEN" ⚠️ (CRITICAL)
     - evidence_source: "abjad_convention"

3. **Phonetic Physics Coordinates:**
   - phonetic_proxy: str (e.g., "/b/" IPA)
   - makhraj_coordinate: MakhrajGeometry
     - spatial_source: str (e.g., "BILABIAL")
     - articulation_point: str (e.g., "LIPS_CLOSURE")
   - sifat_profile: SifatGeometry
     - voicing: str (e.g., "VOICED")
     - manner: str (e.g., "STOP")
     - nasal: bool
     - fricative: bool
     - emphasis: str (e.g., "NON_EMPHATIC")

4. **Invalidating Differences (FariqSet):**
   - fariq_set: tuple[str, ...] (e.g., for BAA: "baa_vs_meem_nasality", "baa_vs_faa_frication")

**Evidence Required:**
- `وصف:has_phonetic_proxy:/b/:evidenced`
- `وصف:has_makhraj:bilabial:evidenced`
- `وصف:has_voicing:voiced:evidenced`
- `وصف:has_manner:stop:evidenced`
- `وصف:has_nasal:false:evidenced`
- `وصف:has_abjad_value:2:evidenced` (if applicable)
- `fariq:{difference}:absent` (for each invalidating difference)

**Forbidden Outputs:**
- SlotCandidate (requires composition with Haraka + Position + Alignment)
- SyllableCandidate
- MeaningCandidate
- HukmCandidate
- RealityClaim

**CRITICAL CONSTRAINT (Abjad Numeric Coordinates):**
```python
# Abjad values are CONVENTIONAL ONLY, NOT semantic
assert abjad_coordinate.semantic_force == "FORBIDDEN"

# ALLOWED:
Abjad(ب) = 2  ✓ (conventional coordinate)

# FORBIDDEN:
Meaning(ب) = 2  ✗ (semantic derivation)
Hukm(ب) = 2  ✗ (semantic derivation)
Root(ب) from numeric  ✗ (semantic derivation)
```

**Note:** This layer is a PARTIAL canonical slice. Full implementation requires:
1. Complete alphabet coverage (currently only 4 letters)
2. GlyphClassificationGate (not implemented)
3. Complete SifatVector for all letters
4. Constitutional validation of phonetic coordinate system

**Architectural Decision:** This layer is OPTIONAL for slot formation if slots do not require phonetic coordinates. If SlotCandidate requires phonetic information, it must consume ArabicLetterCoordinateCarrier, not bare LetterIdentityCarrier.

---

## Not Implemented Layers (Constitutional Contracts Exist)

**These layers have constitutional gates in LAYER_CONTRACT_CONSTITUTION.md but no canonical implementation.**

### Future Layer: SyllableCandidate

**Status:** not_implemented
**Constitutional Gate:** §7.3 LexicalAttestationGate (partial), future SyllableGate
**Input:** SlotCandidate* (sequence of slots)
**Output:** SyllableCandidate
**Coverage:** None

**Note:** Requires constitutional planning before implementation. Old experimental syllable readiness is NOT canonical.

### Future Layer: StemMatterTensor

**Status:** not_implemented
**Constitutional Gate:** §7.4 LexicalPathGate
**Input:** SyllableCandidate* or RootCandidate
**Output:** StemCandidate
**Coverage:** None

### Future Layer: RootWeightAlgebra

**Status:** not_implemented
**Constitutional Gate:** §7.4 LexicalPathGate
**Input:** RawLexCandidate or AttestedRoot
**Output:** RootCandidate, FormCandidate
**Coverage:** None

**Note:** Do NOT build Root/Weight before SyllableCandidate and StemMatterTensor.

### Future Layer: WordForm

**Status:** not_implemented
**Constitutional Gate:** §7.5 VerbalSignifiedGate
**Input:** FormCandidate
**Output:** VerbalSignifiedCandidate
**Coverage:** None

### Future Layer: Meaning / Wadh / Dalalah

**Status:** not_implemented
**Constitutional Gates:** §7.6 WadhScopeGate, §7.7 DalalahTypeGate
**Input:** VerbalSignifiedCandidate
**Output:** WadhCandidate, DalalahCandidate
**Coverage:** None

### Future Layer: Hukm / Tanzil

**Status:** not_implemented
**Constitutional Gates:** §7.11 EvidenceDomainGate, §7.12 TahqiqAlManatGate
**Input:** NormReadyCandidate
**Output:** HukmCandidate, TanzilCandidate
**Coverage:** None

---

## Deprecated / Experimental Layers

**These layers exist in experimental/ but are NOT canonical.**

### Experimental: Old AtomicUnitQiyas

**Status:** experimental (isolated in PR #17)
**Location:** experimental/qiyas_core/atomic_unit_adapter.py
**Canonical Replacement:** SlotCandidate (after Layer 2 composition)
**Action:** Do NOT revive. Use SlotCandidate instead.

### Experimental: Old PhonoFunctionalReadiness

**Status:** experimental (isolated in PR #17)
**Location:** experimental/qiyas_core/{carrier,mark,phono,syllable}_*_adapter.py
**Components:** CarrierFunction, MarkFunction, PhonoFunctionalUnit, SyllableReadiness
**Canonical Replacement:** SlotCandidate composition architecture
**Action:** Do NOT revive. Architecture replaced by simpler Layer 2A+2B+2C+2D composition.

### Experimental: Old SlotGeometry Protocol

**Status:** experimental (isolated in PR #17)
**Location:** experimental/qiyas_core/slot/
**Constitutional Status:** RESET_CONSTITUTION.md §7 explicitly prohibits adopting SlotGeometry before constitutional validation
**Action:** Requires constitutional validation before canonical adoption. Do NOT copy to src/.

### Experimental: Old Demand/Capability Architecture

**Status:** experimental (isolated in PR #17)
**Location:** experimental/qiyas_core/{left_demand,right_capability}_adapter.py
**Canonical Replacement:** Alignment/binding evidence in ConditionedTypedSequence
**Action:** Do NOT revive. Architecture replaced.

---

## Registry Maintenance Rules

**When adding a new canonical layer:**
1. Add full entry to this registry
2. Update CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 1.1
3. Update CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 Duplicate Prevention Table
4. Document constitutional basis
5. Specify forbidden outputs explicitly
6. Document evidence requirements
7. Specify blocking/deferral residuals

**When deprecating a layer:**
1. Move entry to "Deprecated / Experimental Layers" section
2. Document canonical replacement
3. Update Duplicate Prevention Table
4. Do NOT delete entry (preserve historical record)

**When updating layer coverage:**
1. Update Coverage field
2. Update Missing field
3. Document what changed in PR
4. Verify all cross-references are updated

---

## Cross-References

- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md — governing framework
- LAYER_CONTRACT_CONSTITUTION.md — constitutional gates for future layers
- EXPERIMENTAL_TO_CANONICAL_MAP.md — experimental component mapping
- TERMINOLOGY_MAP.md — canonical naming conventions
- THREE_LAYER_LETTER_ARCHITECTURE.md — letter layer architectural decision

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Authoritative registry
