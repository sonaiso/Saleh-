# HARAKA_ROLE_SPECTRUM_CONTRACT.md

**Constitutional Contract for Γ_haraka — The Haraka Role Spectrum Function**

---

## § 1. Constitutional Basis

This contract establishes **Γ_haraka (Gamma-haraka)**, a licensed spectrum-opening function that produces **role hypotheses** for haraka (diacritical mark) carriers within the Saleh/Qiyas algebraic framework.

**Governing Documents:**
- `PROJECT_MATHEMATICAL_FOUNDATION.md` — Layer = Domain boundary, Transition = Qiyas proof
- `LAYER_CONTRACT_CONSTITUTION.md` — Weak links generate hypotheses only
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` — No layer produces next layer's output
- `CLAUDE.md` § 4 (Absolute Invariants) — Potential candidates must not become final judgments

**Constitutional Principle:**

```
Γ ≠ Λ
Γ = Spectrum opener (hypothesis generator)
Λ = Selector (context-dependent chooser, future)

Γ produces POTENTIAL roles.
Γ does NOT produce SELECTED roles.
Γ does NOT produce FINAL judgments.
```

---

## § 2. Mathematical Definition of Γ_haraka

### § 2.1 Type Signature

```
Γ_haraka: SlotCandidate
        × Option[SlotGeometryCandidate]
        → HarakaRoleSpectrum
```

**Where:**
- `SlotCandidate` = the haraka-bearing slot (from Phase 1)
- `Option[SlotGeometryCandidate]` = optional geometric context (from Phase 2A)
- `HarakaRoleSpectrum` = the spectrum of potential roles (new candidate type)

### § 2.2 Mathematical Law

```
Γ_haraka(x, E, D, G) → RoleSpectrumCandidate

where:
  x = HarakaFunctionCarrier (licensed from Phase 1)
  E = EvidenceSet (from PositionCarrier + AlignmentEvidence)
  D = HarakaRoleDomain (new domain)
  G = Option[SlotGeometryCandidate] (optional context)
```

**Output:**

```
HarakaRoleSpectrum = {
  source_identity: tuple[str, ...],           # from SlotCandidate
  haraka_identity: tuple[str, ...],           # haraka-specific identity
  position_identity: tuple[str, ...],         # from PositionCarrier
  alignment_trace_ids: tuple[str, ...],       # from AlignmentEvidence
  geometry_context_trace: tuple[str, ...],    # from SlotGeometry (optional)
  hypotheses: tuple[HarakaRoleHypothesis, ...], # THE SPECTRUM
  rank_ceiling: EvidenceRank,                 # CANDIDATE only
  residuals: tuple[Residual, ...],            # blocking/deferred
}
```

### § 2.3 Hypothesis Structure

Each hypothesis in the spectrum:

```
HarakaRoleHypothesis = {
  role_name: str,                             # e.g., "possible_case_marker_candidate"
  role_genus: str,                            # e.g., "morphosyntactic"
  evidence_claims: tuple[str, ...],           # supporting evidence
  required_context: tuple[str, ...],          # e.g., "requires_lambda_context"
  invalidating_differences: tuple[str, ...],  # blocking fariq
  forbidden_outputs: tuple[str, ...],         # e.g., ("Wazn", "Iʿrab")
}
```

---

## § 3. Acceptance Law

Γ_haraka is constitutionally valid **if and only if** all eight conditions hold:

### § 3.1 Input Conditions

1. **HasCarrier(x)**
   ```
   ∃ HarakaFunctionCarrier ∈ x.identity_ids
   ```
   The input SlotCandidate MUST contain a licensed HarakaFunctionCarrier.

2. **HasPosition(x)**
   ```
   ∃ PositionCarrier ∈ x.trace_ids
   ```
   The input MUST have position context.

3. **HasAlignment(x)**
   ```
   ∃ AlignmentEvidence ∈ x.trace_ids
   ```
   The input MUST have alignment evidence from ConditionedTypedSequence.

4. **HasDomainDeclaration(x)**
   ```
   Domain(Γ_haraka) = "HarakaRoleDomain"
   ```
   The function MUST operate in a declared domain separate from phonological/morphological domains.

### § 3.2 Output Conditions

5. **PreservesIdentity(x)**
   ```
   HarakaRoleSpectrum.source_identity = SlotCandidate.identity_ids
   HarakaRoleSpectrum.haraka_identity ⊆ SlotCandidate.identity_ids
   ```
   All source identities MUST be preserved.

6. **DeclaresForbiddenOutputs(x)**
   ```
   ∀ h ∈ HarakaRoleSpectrum.hypotheses:
     h.forbidden_outputs ⊇ {
       "WeightCandidate",        # Wazn
       "CaseEffect",              # Iʿrab
       "Irab",
       "ArudCandidate",           # ʿArūḍ
       "FinalFunction",
       "FinalMeaning",
       "HukmCandidate",
       "RealityClaim"
     }
   ```
   Every hypothesis MUST declare forbidden outputs.

7. **ProducesOnlySpectrum(x)**
   ```
   output_candidate_type = "HarakaRoleSpectrum"
   ∀ h ∈ hypotheses: h.role_name starts with "possible_"
   ```
   Output MUST be spectrum only, with all roles marked as `possible_*`.

8. **DeclaresContextRequirement(x)**
   ```
   ∀ h ∈ hypotheses where h.role_genus ∈ {
     "morphosyntactic",
     "prosodic",
     "pattern"
   }:
     "requires_lambda_context" ∈ h.required_context
   ```
   Non-phonological hypotheses MUST declare lambda requirement.

---

## § 4. Failure Law

Γ_haraka **FAILS** (produces BLOCKED status) if any condition holds:

### § 4.1 Forbidden Output Violation

```
outputs ∩ {
  "WeightCandidate",      # Wazn
  "Irab",                 # Iʿrab
  "CaseEffect",
  "ArudCandidate",        # ʿArūḍ
  "FinalFunction",
  "FinalMeaning",
  "HukmCandidate",
  "RealityClaim",
  "SelectedRole",         # Final role selection
  "DeterminedFunction"    # Final function determination
} ≠ ∅
```

### § 4.2 Identity Loss

```
HarakaRoleSpectrum.source_identity ⊄ SlotCandidate.identity_ids
```

### § 4.3 Premature Selection

```
∃ h ∈ hypotheses: h.role_name does NOT start with "possible_"
```

### § 4.4 Domain Crossing Without Gate

```
∃ h ∈ hypotheses:
  h.role_genus ∈ {"morphosyntactic", "prosodic"}
  ∧ "requires_lambda_context" ∉ h.required_context
```

---

## § 5. Haraka Type Examples

### § 5.1 Fatha (U+064E) — الفتحة

**Input:**
```python
SlotCandidate(
  candidate_type="SlotCandidate",
  identity_ids=(
    "identity:codepoint:U+064E",
    "identity:haraka:fatha",
    "identity:letter:...",
  ),
  # HarakaFunctionCarrier: OPENING
  # PositionCarrier: terminal/medial
  # AlignmentEvidence: carrier_binding_valid
)
```

**Output Spectrum:**
```python
HarakaRoleSpectrum(
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_phonological_opening",
      role_genus="phonological",
      evidence_claims=(
        "وصف:haraka_class:short_vowel",
        "وصف:haraka_function:OPENING",
      ),
      required_context=(),
      invalidating_differences=(),
      forbidden_outputs=("WeightCandidate", "Irab", "HukmCandidate"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_pattern_vowel",
      role_genus="morphological_pattern",
      evidence_claims=(
        "وصف:haraka_opens_syllable",
        "وصف:position_medial_or_initial",
      ),
      required_context=("requires_lambda_context", "requires_pattern_template"),
      invalidating_differences=("فارق:pattern_mismatch:present",),
      forbidden_outputs=("WeightCandidate", "FinalPattern"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_case_marker_candidate",
      role_genus="morphosyntactic",
      evidence_claims=(
        "وصف:position_terminal",
        "وصف:haraka_marks_ending",
      ),
      required_context=("requires_lambda_context", "requires_composition_context"),
      invalidating_differences=(
        "فارق:non_terminal_position:present",
        "فارق:mabniyy_word:present",
      ),
      forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_syllabic_vowel",
      role_genus="syllabic",
      evidence_claims=(
        "وصف:haraka_opens",
        "وصف:can_form_syllable_nucleus",
      ),
      required_context=("requires_lambda_context", "requires_syllable_boundary"),
      invalidating_differences=(),
      forbidden_outputs=("FinalSyllable",),
    ),
    HarakaRoleHypothesis(
      role_name="possible_arud_relevance",
      role_genus="prosodic",
      evidence_claims=(
        "وصف:contributes_to_weight",
        "وصف:short_vowel_quantity",
      ),
      required_context=("requires_lambda_context", "requires_arud_meter"),
      invalidating_differences=(),
      forbidden_outputs=("ArudCandidate", "FinalMeterJudgment"),
    ),
  ),
  rank_ceiling=EvidenceRank.CANDIDATE,
)
```

### § 5.2 Damma (U+064F) — الضمة

**Output Spectrum:**
```python
HarakaRoleSpectrum(
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_rounding",
      role_genus="phonological",
      evidence_claims=(
        "وصف:haraka_class:short_vowel",
        "وصف:haraka_function:ROUNDING",
      ),
      required_context=(),
      invalidating_differences=(),
      forbidden_outputs=("WeightCandidate", "Irab", "HukmCandidate"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_pattern_vowel",
      role_genus="morphological_pattern",
      evidence_claims=("وصف:haraka_rounds", "وصف:pattern_position"),
      required_context=("requires_lambda_context", "requires_pattern_template"),
      invalidating_differences=("فارق:pattern_mismatch:present",),
      forbidden_outputs=("WeightCandidate", "FinalPattern"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_case_marker_candidate",
      role_genus="morphosyntactic",
      evidence_claims=("وصف:position_terminal", "وصف:nominative_marker_candidate"),
      required_context=("requires_lambda_context", "requires_composition_context"),
      invalidating_differences=(
        "فارق:non_terminal_position:present",
        "فارق:mabniyy_word:present",
      ),
      forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_pronominal_or_plural_relevance",
      role_genus="morphological",
      evidence_claims=("وصف:damma_on_suffix", "وصف:plural_or_pronoun_context"),
      required_context=("requires_lambda_context", "requires_morpheme_boundary"),
      invalidating_differences=(),
      forbidden_outputs=("FinalMorphologicalJudgment",),
    ),
  ),
  rank_ceiling=EvidenceRank.CANDIDATE,
)
```

### § 5.3 Kasra (U+0650) — الكسرة

**Output Spectrum:**
```python
HarakaRoleSpectrum(
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_fronting",
      role_genus="phonological",
      evidence_claims=(
        "وصف:haraka_class:short_vowel",
        "وصف:haraka_function:FRONTING",
      ),
      required_context=(),
      invalidating_differences=(),
      forbidden_outputs=("WeightCandidate", "Irab", "HukmCandidate"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_pattern_vowel",
      role_genus="morphological_pattern",
      evidence_claims=("وصف:haraka_fronts", "وصف:pattern_position"),
      required_context=("requires_lambda_context", "requires_pattern_template"),
      invalidating_differences=("فارق:pattern_mismatch:present",),
      forbidden_outputs=("WeightCandidate", "FinalPattern"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_case_marker_candidate",
      role_genus="morphosyntactic",
      evidence_claims=("وصف:position_terminal", "وصف:genitive_marker_candidate"),
      required_context=("requires_lambda_context", "requires_composition_context"),
      invalidating_differences=(
        "فارق:non_terminal_position:present",
        "فارق:mabniyy_word:present",
      ),
      forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_idafa_relevance",
      role_genus="syntactic",
      evidence_claims=("وصف:kasra_terminal", "وصف:potential_mudaf_ilayh"),
      required_context=("requires_lambda_context", "requires_idafa_context"),
      invalidating_differences=(),
      forbidden_outputs=("FinalIdafaJudgment",),
    ),
  ),
  rank_ceiling=EvidenceRank.CANDIDATE,
)
```

### § 5.4 Sukun (U+0652) — السكون

**Output Spectrum:**
```python
HarakaRoleSpectrum(
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_closure",
      role_genus="phonological",
      evidence_claims=(
        "وصف:haraka_class:sukun",
        "وصف:haraka_function:CLOSURE",
      ),
      required_context=(),
      invalidating_differences=(),
      forbidden_outputs=("WeightCandidate", "Irab", "HukmCandidate"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_syllable_boundary_relevance",
      role_genus="syllabic",
      evidence_claims=("وصف:sukun_closes_syllable", "وصف:boundary_marker"),
      required_context=("requires_lambda_context", "requires_syllable_template"),
      invalidating_differences=(),
      forbidden_outputs=("FinalSyllable",),
    ),
    HarakaRoleHypothesis(
      role_name="possible_jazm_candidate",
      role_genus="morphosyntactic",
      evidence_claims=("وصف:sukun_terminal", "وصف:jazm_marker_candidate"),
      required_context=("requires_lambda_context", "requires_verb_context"),
      invalidating_differences=(
        "فارق:non_verb_context:present",
        "فارق:mabniyy_word:present",
      ),
      forbidden_outputs=("CaseEffect", "Irab", "FinalJazmJudgment"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_waqf_relevance",
      role_genus="phonological_boundary",
      evidence_claims=("وصف:sukun_final", "وصف:pause_marker_candidate"),
      required_context=("requires_lambda_context", "requires_waqf_pattern"),
      invalidating_differences=(),
      forbidden_outputs=("FinalWaqfJudgment",),
    ),
  ),
  rank_ceiling=EvidenceRank.CANDIDATE,
)
```

### § 5.5 Shadda (U+0651) — الشدة

**Output Spectrum:**
```python
HarakaRoleSpectrum(
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_compression",
      role_genus="phonological",
      evidence_claims=(
        "وصف:haraka_class:shadda",
        "وصف:haraka_function:COMPRESSION",
      ),
      required_context=(),
      invalidating_differences=(),
      forbidden_outputs=("WeightCandidate", "Irab", "HukmCandidate"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_gemination_candidate",
      role_genus="phonological",
      evidence_claims=("وصف:shadda_doubles_consonant", "وصف:gemination_marker"),
      required_context=("requires_lambda_context",),
      invalidating_differences=(),
      forbidden_outputs=("FinalGeminationJudgment",),
    ),
    HarakaRoleHypothesis(
      role_name="possible_morphological_intensification_relevance",
      role_genus="morphological",
      evidence_claims=("وصف:shadda_intensifies", "وصف:taʿdid_marker"),
      required_context=("requires_lambda_context", "requires_pattern_context"),
      invalidating_differences=(),
      forbidden_outputs=("FinalMorphologicalJudgment",),
    ),
    HarakaRoleHypothesis(
      role_name="possible_arud_weight_relevance",
      role_genus="prosodic",
      evidence_claims=("وصف:shadda_heavy_weight", "وصف:contributes_double_weight"),
      required_context=("requires_lambda_context", "requires_arud_meter"),
      invalidating_differences=(),
      forbidden_outputs=("ArudCandidate", "FinalMeterJudgment"),
    ),
  ),
  rank_ceiling=EvidenceRank.CANDIDATE,
)
```

### § 5.6 Tanwin (U+064B/U+064C/U+064D) — التنوين

**Output Spectrum:**
```python
HarakaRoleSpectrum(
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_nunation",
      role_genus="phonological",
      evidence_claims=(
        "وصف:haraka_class:tanwin",
        "وصف:haraka_adds_nun_sound",
      ),
      required_context=(),
      invalidating_differences=(),
      forbidden_outputs=("WeightCandidate", "Irab", "HukmCandidate"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_indefiniteness_marker_candidate",
      role_genus="morphosyntactic",
      evidence_claims=("وصف:tanwin_marks_indefinite", "وصف:nakira_marker"),
      required_context=("requires_lambda_context", "requires_noun_context"),
      invalidating_differences=(
        "فارق:definite_article_present:present",
        "فارق:mabniyy_word:present",
      ),
      forbidden_outputs=("FinalIndefiniteJudgment",),
    ),
    HarakaRoleHypothesis(
      role_name="possible_case_marker_candidate",
      role_genus="morphosyntactic",
      evidence_claims=("وصف:position_terminal", "وصف:tanwin_case_marker"),
      required_context=("requires_lambda_context", "requires_composition_context"),
      invalidating_differences=(
        "فارق:non_terminal_position:present",
        "فارق:mabniyy_word:present",
      ),
      forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_waqf_transformation_relevance",
      role_genus="phonological_boundary",
      evidence_claims=("وصف:tanwin_drops_at_waqf", "وصف:waqf_sensitive"),
      required_context=("requires_lambda_context", "requires_waqf_pattern"),
      invalidating_differences=(),
      forbidden_outputs=("FinalWaqfJudgment",),
    ),
  ),
  rank_ceiling=EvidenceRank.CANDIDATE,
)
```

---

## § 6. SlotGeometry as Optional Context

### § 6.1 Integration Law

```
Γ_haraka(SlotCandidate, None)
  → HarakaRoleSpectrum(basic_hypotheses)

Γ_haraka(SlotCandidate, Some(SlotGeometryCandidate))
  → HarakaRoleSpectrum(basic_hypotheses + context_aware_hypotheses)
```

### § 6.2 Geometric Context Evidence

When `SlotGeometryCandidate` is provided, Γ_haraka MAY extract:

```python
geometry_length: int              # from SlotGeometry.trace_ids
position_in_geometry: str         # "geometry_initial" | "geometry_medial" | "geometry_terminal"
adjacent_boundaries: bool         # from SlotBindingEvidence
licensed_distance: int            # from SlotBindingEvidence
segment_transition: bool          # from SlotBindingEvidence
```

### § 6.3 Context-Aware Hypothesis Examples

**With geometry_length ≥ 2:**
```python
HarakaRoleHypothesis(
  role_name="possible_arud_weight_contributor",
  role_genus="prosodic",
  evidence_claims=(
    "وصف:geometry_length:>=2",
    "وصف:haraka_in_multi_slot_geometry",
  ),
  required_context=("requires_lambda_context", "requires_arud_pattern"),
  invalidating_differences=(),
  forbidden_outputs=("ArudCandidate", "FinalMeterJudgment"),
)
```

**With position_in_geometry == "geometry_terminal":**
```python
HarakaRoleHypothesis(
  role_name="possible_case_marker_candidate",
  role_genus="morphosyntactic",
  evidence_claims=(
    "وصف:position:geometry_terminal",
    "وصف:haraka_marks_ending",
  ),
  required_context=("requires_lambda_context", "requires_composition_context"),
  invalidating_differences=("فارق:non_terminal_case:present",),
  forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
)
```

**With adjacent_boundaries == true:**
```python
HarakaRoleHypothesis(
  role_name="possible_waqf_relevance",
  role_genus="phonological_boundary",
  evidence_claims=(
    "وصف:boundary_after_slot",
    "وصف:whitespace_or_punctuation_present",
  ),
  required_context=("requires_lambda_context", "requires_waqf_pattern"),
  invalidating_differences=(),
  forbidden_outputs=("FinalWaqfJudgment",),
)
```

### § 6.4 Constitutional Constraints

**SlotGeometry is:**
- ✅ Optional context input to Γ_haraka
- ✅ Source of geometric metadata
- ✅ Evidence provider for context-aware hypotheses

**SlotGeometry is NOT:**
- ❌ Producer of HarakaRoleSpectrum
- ❌ Modified by Γ_haraka
- ❌ Direct output of Γ_haraka
- ❌ Gate to Wazn/Iʿrab/Arud layers

---

## § 7. Relationship to Future Λ (Lambda)

### § 7.1 Division of Labor

```
Γ_haraka (NOW):
  - Opens spectrum of possible roles
  - Generates hypotheses
  - Preserves all potentials
  - Rank: CANDIDATE
  - Output: HarakaRoleSpectrum

Λ_syllable (FUTURE):
  - Selects syllabic role from spectrum
  - Consumes: HarakaRoleSpectrum
  - Produces: SyllableConstituent | Residual
  - Rank: depends on evidence

Λ_pattern (FUTURE):
  - Selects pattern role from spectrum
  - Consumes: HarakaRoleSpectrum
  - Produces: PatternVowel | Residual
  - Rank: depends on evidence

Λ_composition (FUTURE):
  - Selects case role from spectrum
  - Consumes: HarakaRoleSpectrum
  - Produces: CaseMarkerCandidate | Residual
  - Rank: depends on evidence
```

### § 7.2 Lambda Requirements

Each future Λ function MUST:

1. **Consume HarakaRoleSpectrum** (not SlotCandidate directly)
2. **Select ONE hypothesis** from the spectrum
3. **Provide context evidence** (syllable template, pattern template, composition tree)
4. **Validate invalidating_differences** before selection
5. **Respect forbidden_outputs** from the hypothesis
6. **Produce residuals** for non-selected hypotheses
7. **Preserve trace** linking back to the spectrum

### § 7.3 Forbidden Λ Behaviors

❌ Λ MUST NOT:
- Select multiple roles simultaneously (without explicit conjunction proof)
- Produce outputs forbidden by the hypothesis
- Bypass Γ_haraka and work directly on SlotCandidate
- Turn a `possible_*` hypothesis into a `final_*` judgment

---

## § 8. Forbidden Outputs

### § 8.1 Layer-Level Forbidden Outputs

`HarakaRoleSpectrum` (the Γ_haraka output) MUST NOT produce:

```python
FORBIDDEN_HARAKA_ROLE_SPECTRUM: tuple[str, ...] = (
    # Constitutional base
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",

    # Weight/Pattern layer
    "WeightCandidate",
    "RootCandidate",
    "PatternCandidate",
    "MorphemeCandidate",

    # Case/Composition layer
    "CaseEffect",
    "Irab",
    "CaseJudgment",
    "CompositionCandidate",

    # Prosody layer
    "ArudCandidate",
    "MeterJudgment",

    # Selection outputs
    "SelectedRole",
    "FinalFunction",
    "DeterminedRole",

    # Syllable layer (Λ_syllable output)
    "SyllableCandidate",
    "SyllableConstituent",

    # Higher layers
    "WordCandidate",
    "MeaningCandidate",
    "IfadahCandidate",
)
```

### § 8.2 Hypothesis-Level Forbidden Outputs

Every `HarakaRoleHypothesis` MUST declare its forbidden outputs in its `forbidden_outputs` field, including at minimum:

```python
# For all hypotheses
("HukmCandidate", "RealityClaim", "FinalMeaning")

# For morphosyntactic hypotheses
+ ("CaseEffect", "Irab", "FinalCaseJudgment")

# For pattern hypotheses
+ ("WeightCandidate", "FinalPattern")

# For prosodic hypotheses
+ ("ArudCandidate", "FinalMeterJudgment")
```

---

## § 9. Non-Goals (Explicit)

This contract **explicitly does NOT**:

1. ❌ Implement Λ (selection mechanism)
2. ❌ Implement Wazn (weight/pattern layer)
3. ❌ Implement Iʿrab (case/composition layer)
4. ❌ Implement ʿArūḍ (prosody layer)
5. ❌ Implement Syllable (syllable layer)
6. ❌ Select a final role from the spectrum
7. ❌ Produce FinalFunction/DeterminedRole
8. ❌ Modify SlotGeometry
9. ❌ Produce SlotGeometry
10. ❌ Cross domain boundaries without explicit gates

---

## § 10. Implementation Phases

### Phase 1 (This PR): Constitutional Document
- ✅ This file: `HARAKA_ROLE_SPECTRUM_CONTRACT.md`
- ✅ Zero code
- ✅ Zero tests
- ✅ Documentation only

### Phase 2 (Next PR): Data Structures
- `src/qiyas_core/haraka_role_spectrum.py`
  - `HarakaRoleHypothesis` dataclass
  - `HarakaRoleSpectrum` dataclass
- `src/qiyas_core/forbidden_outputs.py`
  - `FORBIDDEN_HARAKA_ROLE_SPECTRUM` constant
- Zero adapters
- Zero rules
- Zero integration tests

### Phase 3 (Later PR): Adapter Implementation
- `src/qiyas_core/haraka_role_spectrum_adapter.py`
  - `HarakaRoleSpectrumLayerAdapter` class
- `src/qiyas_core/rules/haraka_role_spectrum_rules.py`
  - Γ_haraka rules for each haraka type
- Integration tests
- Constitutional validation tests

---

## § 11. Version Control

**Version:** 1.0.0
**Status:** Constitutional (Phase 1)
**Date:** 2026-06-05
**Maintainer:** @sonaiso
**Dependencies:**
- `PROJECT_MATHEMATICAL_FOUNDATION.md`
- `LAYER_CONTRACT_CONSTITUTION.md`
- `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` (for optional context)
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md`

---

## Appendix A: Governing Principles Summary

```
1. Γ ≠ Λ
   Gamma opens spectrum, Lambda selects.

2. Candidate هو مصدر السلطة
   Candidates are the source of authority, not numbers or projections.

3. لا طبقة تنتج مخرج الطبقة التالية
   No layer produces the next layer's output.

4. الروابط الضعيفة تولّد فرضيات
   Weak links generate hypotheses only.

5. الأثر لا يصبح أصلًا
   Trace does not become identity.

6. الرقم لا ينتج معرفة
   Numbers do not produce knowledge.

7. كل مرشح يحتاج بوابة
   Every candidate requires a gate.

8. لا تنزيل بلا تحقيق مناط
   No application without verifying the condition.
```

---

**END OF CONTRACT**
