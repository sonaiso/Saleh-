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
- `فارق:non_arabic_codepoint:present` (blocks non-Arabic codepoints)

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
- `فارق:multiple_classes_claimed:present`
- `فارق:ambiguous_classification:present`
- `فارق:letter_haraka_overlap:present`
- `فارق:boundary_punctuation_overlap:present`

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
- Invalidating difference → `فارق:{difference}:present`

**Forbidden Outputs:**
- SlotGeometry (not canonical, experimental only)
- SyllableCandidate (next layer, not implemented)
- MeaningCandidate
- HukmCandidate
- RealityClaim

**Note:** SlotCandidate is a POTENTIAL slot, not a final slot. It remains candidate/potential only. It does NOT produce SlotGeometry directly.

**Constitutional Requirement:** No SlotCandidate may be produced unless ALL FOUR ingredients are present. Partial slots are not licensed.

---

## Layer X: Coordinate Enrichment (Consonantal Core Complete)

### Layer X: ArabicLetterCoordinateCarrier

**Input:** LetterIdentityCarrier
**Output:** ArabicLetterCoordinateCarrier
**Status:** canonical (full consonantal coverage)
**Source PR:** #27 (initial), expanded to full alphabet
**Coverage:** 26 core consonantal Arabic letters (ء ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه)
**Missing:** Weak letters (و ي ا) — deliberately gated by GlyphClassificationGate pending RoleDisambiguationGate (future layer); Hamza-seat glyphs (أ إ ؤ ئ) similarly gated

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

3. **Phonetic Physics Coordinates (SifatGeometry — 5 axes):**
   - phonetic_proxy: str (e.g., "/b/" IPA) via `src/qiyas_core/phonetics/profiles.py`
   - makhraj_coordinate: MakhrajGeometry
     - spatial_source: str (e.g., "BILABIAL")
     - articulation_point: str (e.g., "LIPS_CLOSURE")
   - sifat_profile: SifatGeometry
     - voicing: str (VOICED / VOICELESS)
     - manner: str (STOP / FRICATIVE / NASAL / LATERAL / TRILL / APPROXIMANT / AFFRICATE)
     - airflow: str (PULMONIC — all Arabic consonants)
     - duration: str (SHORT / LONG)
     - emphasis: str (EMPHATIC / NON_EMPHATIC)

4. **Invalidating Differences (FariqSet):**
   - fariq_set: tuple[str, ...] (e.g., for BAA: "baa_vs_meem_nasality", "baa_vs_faa_frication")

5. **GlyphClassificationGate:**
   - Implemented in `src/qiyas_core/registries/glyph_classification_registry.py`
   - Classifies glyphs before coordinate assignment: CORE_ARABIC_LETTER / STANDALONE_HAMZA / HAMZA_SEAT_GLYPH / WEAK_LETTER_GLYPH / TATWEEL_GLYPH / COMPLEX_GLYPH
   - Weak letters (و ي ا) produce DEFERRED residual (role ambiguity, not coordinate error)
   - Hamza-seat glyphs (أ إ ؤ ئ) produce DEFERRED residual (decomposition required)

**Evidence Required:**
- `وصف:has_phonetic_proxy:/b/:evidenced`
- `وصف:has_makhraj:bilabial:evidenced`
- `وصف:has_voicing:voiced:evidenced`
- `وصف:has_manner:stop:evidenced`
- `وصف:has_duration:short:evidenced`
- `وصف:has_emphasis:non_emphatic:evidenced`
- `وصف:has_abjad_value:2:evidenced` (if applicable)
- `فارق:{difference}:absent` (for each invalidating difference)

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

**Note:** 26 consonantal letters are fully implemented with GlyphClassificationGate, SifatGeometry (5 axes), and complete FariqSet. Weak letters (و ي ا) are constitutionally deferred — they have multiple potential roles (consonant/long-vowel/glide) that require a future RoleDisambiguationGate; this is correct architectural behaviour, not a gap.

**Implementation files:**
- `src/qiyas_core/letter_coordinate_adapter.py` — adapter logic
- `src/qiyas_core/rules/letter_coordinate_rules.py` — 26-letter rule map
- `src/qiyas_core/phonetics/profiles.py` — full LETTER_PHONETIC_PROFILES (all 26 letters)
- `src/qiyas_core/registries/glyph_classification_registry.py` — GlyphClassificationGate
- `tests/qiyas_core/test_full_alphabet_coordinates.py` — 45 tests covering all 26 letters

**Architectural Decision:** This layer is OPTIONAL for slot formation if slots do not require phonetic coordinates. If SlotCandidate requires phonetic information, it must consume ArabicLetterCoordinateCarrier, not bare LetterIdentityCarrier.

---

## Layer Γ: Haraka Role Spectrum (Canonical — Spectrum-Opening Phase Complete)

### Layer Γ: HarakaRoleSpectrum

**Input:** SlotCandidate × Option[SlotGeometryCandidate]
**Output:** HarakaRoleSpectrum
**Status:** canonical (Phase 2+3 complete — spectrum-opening function implemented)
**Source PR:** #89
**Coverage:** Full spectrum-opening (Γ function): phonological, pattern, case_marker, syllabic, prosodic hypotheses for all harakāt; rank_ceiling=ANALOGICAL; Λ selectors are future layers

**Proof Obligation:** What are the POTENTIAL roles of this haraka in different linguistic domains?

**Mathematical Function:**
```
Γ_haraka: SlotCandidate × Option[SlotGeometryCandidate] → HarakaRoleSpectrum

Γ_haraka(x, E, D, G) → RoleSpectrumCandidate

where:
  x = HarakaFunctionCarrier (from Phase 1)
  E = EvidenceSet (PositionCarrier + AlignmentEvidence)
  D = HarakaRoleDomain (new domain)
  G = Option[SlotGeometryCandidate] (optional geometric context)
```

**Output Structure:**
```python
HarakaRoleSpectrum = {
  source_identity: tuple[str, ...],           # from SlotCandidate
  haraka_identity: tuple[str, ...],           # haraka-specific identity
  position_identity: tuple[str, ...],         # from PositionCarrier
  alignment_trace_ids: tuple[str, ...],       # from AlignmentEvidence
  geometry_context_trace: tuple[str, ...],    # from SlotGeometry (optional)
  hypotheses: tuple[HarakaRoleHypothesis, ...], # THE SPECTRUM
  rank_ceiling: EvidenceRank.CANDIDATE,       # CANDIDATE only
  residuals: tuple[Residual, ...],
}

HarakaRoleHypothesis = {
  role_name: str,                             # e.g., "possible_case_marker_candidate"
  role_genus: str,                            # e.g., "morphosyntactic"
  evidence_claims: tuple[str, ...],
  required_context: tuple[str, ...],          # e.g., "requires_lambda_context"
  invalidating_differences: tuple[str, ...],
  forbidden_outputs: tuple[str, ...],         # e.g., ("Wazn", "Iʿrab")
}
```

**Constitutional Principle:**
```
Γ ≠ Λ

Γ = Spectrum opener (hypothesis generator)
Λ = Selector (context-dependent chooser, FUTURE)

Γ produces POTENTIAL roles ("possible_*").
Γ does NOT produce SELECTED roles.
Γ does NOT produce FINAL judgments.
```

**Example Hypotheses (Fatha):**
1. `possible_phonological_opening` (genus: phonological)
2. `possible_pattern_vowel` (genus: morphological_pattern)
3. `possible_case_marker_candidate` (genus: morphosyntactic)
4. `possible_syllabic_vowel` (genus: syllabic)
5. `possible_arud_relevance` (genus: prosodic)

**SlotGeometry Integration:**
- SlotGeometry is OPTIONAL context input
- When provided: adds geometry-aware hypotheses (geometry_length, position_in_geometry, boundaries)
- When absent: produces basic hypotheses only
- SlotGeometry does NOT produce HarakaRoleSpectrum
- Γ_haraka does NOT modify SlotGeometry

**Forbidden Outputs (Layer-Level):**
- WeightCandidate (Wazn)
- CaseEffect / Irab (Iʿrab)
- ArudCandidate (ʿArūḍ)
- FinalFunction / SelectedRole / DeterminedRole
- SyllableCandidate (Λ_syllable output, not Γ output)
- MeaningCandidate
- HukmCandidate
- RealityClaim

**Forbidden Outputs (Hypothesis-Level):**
Each hypothesis MUST declare forbidden outputs including at minimum:
- All hypotheses: `("HukmCandidate", "RealityClaim", "FinalMeaning")`
- Morphosyntactic: + `("CaseEffect", "Irab", "FinalCaseJudgment")`
- Pattern: + `("WeightCandidate", "FinalPattern")`
- Prosodic: + `("ArudCandidate", "FinalMeterJudgment")`

**Acceptance Law (8 Conditions):**
1. HasCarrier(x) — HarakaFunctionCarrier present
2. HasPosition(x) — PositionCarrier present
3. HasAlignment(x) — AlignmentEvidence present
4. HasDomainDeclaration(x) — HarakaRoleDomain declared
5. PreservesIdentity(x) — source identities preserved
6. DeclaresForbiddenOutputs(x) — every hypothesis declares forbidden outputs
7. ProducesOnlySpectrum(x) — all role_names start with "possible_"
8. DeclaresContextRequirement(x) — non-phonological hypotheses require lambda

**Relationship to Future Λ (Lambda):**
```
Γ_haraka (NOW, this layer):
  Opens spectrum of possible roles
  Produces: HarakaRoleSpectrum

Λ_syllable (FUTURE):
  Selects syllabic role from spectrum
  Consumes: HarakaRoleSpectrum
  Produces: SyllableConstituent | Residual

Λ_pattern (FUTURE):
  Selects pattern role from spectrum
  Consumes: HarakaRoleSpectrum
  Produces: PatternVowel | Residual

Λ_composition (FUTURE):
  Selects case role from spectrum
  Consumes: HarakaRoleSpectrum
  Produces: CaseMarkerCandidate | Residual
```

**Implementation Phases:**
- Phase 1 (Complete): Constitutional contract document (`HARAKA_ROLE_SPECTRUM_CONTRACT.md`)
- Phase 2 (Complete): Data structures (`HarakaRoleHypothesis`, `HarakaRoleSpectrum` dataclasses) in `src/qiyas_core/haraka_role_spectrum.py`
- Phase 3 (Complete): Adapter and rules implementation in `src/qiyas_core/haraka_role_spectrum_adapter.py` (516 lines) + `src/qiyas_core/rules/haraka_role_spectrum_rules.py` (92 lines) + `tests/qiyas_core/test_haraka_role_spectrum_adapter.py` (575 lines)

**Constitutional Document:** `docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md`

**Note:** This is a WEAK LINK layer that generates hypotheses only, per LAYER_CONTRACT_CONSTITUTION.md. It does NOT select roles, does NOT produce final judgments, and does NOT cross domain boundaries without explicit Λ gates.

---

## Layer 4: Licensed Syllable (Constitutional Contract Phase)

### Layer 4: LicensedSyllableCandidate

**Input:** tuple[IntegratedLinguisticCandidate, ...] + BoundaryEvidence + NeighborRelation + SyllableEconomyBridge
**Output:** LicensedSyllableCandidate
**Status:** constitutional_contract_only (Phase 1)
**Source PR:** #TBD (constitutional document established 2026-06-08)
**Coverage:** None (documentation only)

**Proof Obligation:** Can this sequence of integrated linguistic units form a licensed syllable under phonetic economy law?

**Constitutional Document:** `docs/qiyas_core/LICENSED_SYLLABLE_CONSTITUTION.md`

**Core Principle — Phonetic Economy Law:**
```
لا مقطع بلا ترتيب.
لا ترتيب بلا جوار.
لا جوار بلا حركة مرخّصة.
لا ترخيص بلا اقتصاد صوتي.

(No syllable without sequence. No sequence without adjacency.
No adjacency without licensed haraka. No licensing without phonetic economy.)
```

**Licensed Syllable Patterns (phonetic only, NOT prosodic/metrical):**
- CV (carrier + short vowel)
- CVC (carrier + short vowel + closure)
- CVV (carrier + long vowel)
- CVVC (carrier + long vowel + closure)

**Economy Principle:**
```
اختر أصغر مقطع مكتمل مرخّص
ولا توسّع المقطع إلا إذا منعته بقايا أو حدّ أو سكون أو مدّ.

(Choose the smallest complete licensed syllable.
Do not expand unless blocked by residuals, boundary, sukun, or madd.)
```

**Evidence Required:**
- `وصف:has_valid_sequence:evidenced` (sequence admissibility)
- `وصف:has_left_boundary:evidenced` (left boundary preserved)
- `وصف:has_right_boundary:evidenced` (right boundary preserved)
- `وصف:has_adjacency:evidenced` (neighbor relations)
- `علة:minimal_complete_syllable:verified` (economy law satisfied)
- `وصف:pattern_is_{CV|CVC|CVV|CVVC}:evidenced` (pattern identified)

**Invalidating Differences:**
- `فارق:incomplete_syllable:present` (missing carrier or nucleus)
- `فارق:economy_violation:present` (unnecessary expansion)
- `فارق:boundary_violation:present` (crosses required boundary)
- `فارق:neighbor_violation:present` (adjacency violated)
- `فارق:pattern_invalid:present` (not in licensed pattern set)

**Deferral Conditions:**
- `defer:incomplete_sequence:present` (more constituents needed)
- `defer:boundary_unknown:present` (cannot determine boundaries)
- `defer:economy_ambiguous:present` (multiple valid solutions)
- `defer:neighbor_pending:present` (neighbor relations pending)

**Forbidden Outputs (CRITICAL — No jumps to these layers):**
- WaznCandidate (morphological weight, future layer)
- IrabCandidate (case marking, future layer)
- ArudCandidate (prosodic meter, future layer)
- MorphologyCandidate (morphological analysis, future layer)
- MeaningCandidate
- HukmCandidate
- RealityClaim
- FinalMeaning
- FinalPattern
- FinalWeight

**CRITICAL ARCHITECTURAL PROHIBITION:**
```
❌ FORBIDDEN:
IntegratedLinguisticCandidate → Wazn (direct jump)
IntegratedLinguisticCandidate → I'rab (direct jump)
IntegratedLinguisticCandidate → Arud (direct jump)
LicensedSyllableCandidate → MeaningCandidate (direct jump)

✓ REQUIRED:
IntegratedLinguisticCandidate+ → LicensedSyllableCandidate
LicensedSyllableCandidate+ → StemMatterTensor (future)
StemMatterTensor → RootWeightAlgebra (future)
```

**Mathematical Bridge Role:**

LicensedSyllableCandidate serves as the mathematical bridge between:
- **Input domain:** Atomic units, integrated positions, alignment evidence
- **Future domains:** Morphological analysis (Wazn), Syntactic analysis (I'rab), Prosodic analysis (Arud)

**Critical Distinction:**
```
✓ CV as phonetic syllable candidate
✗ CV as metrical unit (Arud judgment)
✗ CV as morphological pattern element (Wazn judgment)
✗ CV as meaning carrier (semantic judgment)
```

**Implementation Phases:**
- Phase 1 (Current): Constitutional contract document (`LICENSED_SYLLABLE_CONSTITUTION.md`)
- Phase 2 (Next): Data structures (`LicensedSyllableCandidate`, `SyllableEconomyEvidence` dataclasses)
- Phase 3 (Future): Adapter and rules implementation

**Note:** This is the REQUIRED next layer after IntegratedLinguisticCandidate (PR #50). Do NOT jump to Wazn/I'rab/Arud before implementing this layer. Syllable is not built from a single element but from a sequence under phonetic economy law.

---

## Not Implemented Layers (Constitutional Contracts Exist)

**These layers have constitutional gates in LAYER_CONTRACT_CONSTITUTION.md but no canonical implementation.**

### Future Layer: StemMatterTensor

**Status:** not_implemented
**Constitutional Gate:** §7.4 LexicalPathGate
**Input:** LicensedSyllableCandidate* (sequence of syllables)
**Output:** StemMatterTensor
**Coverage:** None

**Note:** Requires LicensedSyllableCandidate to be implemented first. Do NOT build before syllable layer exists.

### Future Layer: RootWeightAlgebra

**Status:** not_implemented
**Constitutional Gate:** §7.4 LexicalPathGate
**Input:** StemMatterTensor
**Output:** RootCandidate, FormCandidate, WaznCandidate
**Coverage:** None

**Note:** Do NOT build Root/Weight before LicensedSyllableCandidate and StemMatterTensor exist. Weight operates on licensed matter, not raw letters.

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

## Canonical Phase Prefixes & Origin Traceability (REC-2)

**Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §3 / §4.1 / §4.2 — executed
by REC-2 of the corrective queue (§7). Scope: phase-string prefixes and
per-layer origin notes only. No new layers, no status advancement.

### Phase-prefix disambiguation (§4.1, binding)

```text
BF0    = Binary Foundation            (Binary- repository: L00…L04)
SCG-P0 = SlotGeometry Core phase 0    (Saleh- repository: Unicode/TypedCodePoint/Glyph)
AR-P0  = Arabic Voice/Verbal Origin   (future Arabic package/repo)

Declared: Binary-P0 ≠ Arabic-SCG-P0.
```

### Canonical phase strings (§4.2)

The `LayerSpec.phase` strings in
`src/qiyas_core/slot_geometry_core/master_registry_seed.py` carry the
canonical `SCG-` prefix. Conversion table (former → canonical):

| Former phase string | Canonical phase string (REC-2) |
| --- | --- |
| `P0_BINARY_FOUNDATION` | `SCG-P0` (renamed away from "BINARY_FOUNDATION" wording — §6.2 collision with BF0) |
| `P1_DAL_ALONE_ATOMIC` | `SCG-P1` |
| `P2_REGISTRY_PROJECTION` | `SCG-P2` |
| `P3_ROOT_STEM_CLOSURE` | `SCG-P3` |
| `P4_JAMID_MUSHTAQ` | `SCG-P4` |
| `P5_MUFRAD_WORD_CONTRACTS` | `SCG-P5` |
| `P6_VERBAL_SIGNIFIED_ALONE` | `SCG-P6` |
| `P7_COMPOSITION_READINESS` | `SCG-P7` |
| `P8_AMIL_MAMUL` | `SCG-P8` |
| `P9_SENTENCE_GEOMETRY` | `SCG-P9` |
| `P10_RELATION_GEOMETRY` | `SCG-P10` |
| `P11_IRAB_GEOMETRY` | `SCG-P11` |
| `P12_IFADAH_SPEECH_FORCE` | `SCG-P12` |

Layer IDs (`LAYER_ID_*` constants) are unchanged: they identify layers, not
phases, and renaming them is outside REC-2 scope.

Enforced by `tests/qiyas_core/test_canonical_phase_prefixes.py` (`REC2-*`).

### Origin traceability (§3, registry-binding)

**Tracing rule (قانون الإسناد):**

```text
كل طبقة بلا أصل من هذه الأصول الثلاثة = خارج المشروع أو تجريبية.
No layer without one of the three origins.
```

The three Foundational Origins:

| Origin | Served by | Notes |
| --- | --- | --- |
| الأصل الأول — صوت بشري عربي محفوظ الأثر (preserved sound trace) | `Binary-` (BF0) carries the written/encoded trace; future `AR-P0` carries the sound origin itself | not seeded in Saleh- |
| الأصل الثاني — نظام لفظي عربي يحفظ انتقالات الصوت (verbal system preserving transitions) | `Saleh-` algebraic spine (SCG phases) | **all 19 seeded layers** |
| الأصل الثالث — مدلول وضعي (conventional signified) | future Arabic package/repo only | not seeded in Saleh- |

All 19 layers registered in `build_master_registry_seed()` belong to `SCG-`
phases and trace to **الأصل الثاني**. The machine-checkable assignment is
`master_registry_seed.LAYER_ORIGIN_NOTES` (one entry per registered layer ID),
enforced by `REC2-ORIGIN-*` tests.

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
- REPOSITORY_RESPONSIBILITY_MATRIX.md — repository responsibility matrix (REC-1 boundary enforcement)
- PROJECT_RECOVERY_CANONICAL_MAP.md — recovery map (§3 origins, §4 canonical phases; REC-2 authority)

---

**Document Version:** 1.2
**Last Updated:** 2026-06-10
**Status:** Authoritative registry
