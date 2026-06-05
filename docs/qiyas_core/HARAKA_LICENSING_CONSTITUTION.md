# HARAKA_LICENSING_CONSTITUTION.md

**Constitutional Contract for Λ_haraka — The Haraka Role Licensing Function**

---

## § 0. Governing Law

```
Γ opens possibilities.
Λ licenses one role under context.
Λ does not produce the next layer's object.
```

**بالعربية:**

```
Γ يفتح الاحتمالات.
Λ يرخّص دورًا واحدًا تحت سياق.
Λ لا ينتج كائن الطبقة التالية.
```

---

## § 1. Constitutional Basis

This contract establishes **Λ_haraka (Lambda-haraka)**, a licensed role-selection function that operates on `HarakaRoleSpectrum` (the output of Γ_haraka) and produces **a single licensed role** under a specific linguistic context.

**Governing Documents:**
- `PROJECT_MATHEMATICAL_FOUNDATION.md` — Layer = Domain boundary, Transition = Qiyas proof
- `HARAKA_ROLE_SPECTRUM_CONTRACT.md` — Γ_haraka produces spectrum of possible roles
- `LAYER_CONTRACT_CONSTITUTION.md` — Gates and domain boundaries
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` — No layer produces next layer's output
- `CLAUDE.md` § 4 (Absolute Invariants) — Potential candidates must not become final judgments

**Constitutional Principle:**

```
Γ ≠ Λ

Γ_haraka = Spectrum opener (hypothesis generator)
Λ_haraka = Role selector (context-dependent license)

Γ produces POTENTIAL roles ("possible_*")
Λ produces LICENSED roles ("licensed_*")
Λ does NOT produce FINAL roles, DETERMINED functions, or next-layer objects
```

---

## § 2. Mathematical Definition of Λ_haraka

### § 2.1 Type Signature

```
Λ_haraka: HarakaRoleSpectrum
        × LicensingContext
        → LicensedHarakaRole | Residual
```

**Where:**
- `HarakaRoleSpectrum` = output from Γ_haraka (Phase 2B)
- `LicensingContext` = domain-specific context (syllable/pattern/composition/prosody)
- `LicensedHarakaRole` = ONE selected role with licensing evidence
- `Residual` = blocking/deferred when licensing fails

### § 2.2 Mathematical Law

```
Λ_haraka(Spectrum, Context, Evidence) → LicensedRole | Residual

where:
  Spectrum = HarakaRoleSpectrum (from Γ_haraka)
  Context = {
    SyllableContext       (for syllabic roles)
    | PatternContext      (for pattern roles)
    | CompositionContext  (for case marker roles)
    | ProsodyContext      (for arud roles)
  }
  Evidence = LicensingEvidence (context-specific proof)
```

**Output:**

```
LicensedHarakaRole = {
  source_spectrum_identity: tuple[str, ...],    # from HarakaRoleSpectrum
  selected_hypothesis: HarakaRoleHypothesis,    # ONE hypothesis from spectrum
  licensing_context: str,                       # which context licensed it
  licensing_evidence: EvidenceSet,              # proof of licensing
  licensed_role_name: str,                      # e.g., "licensed_case_marker_role"
  rank: EvidenceRank,                           # context-dependent
  trace_ids: tuple[str, ...],                   # preserved trace
  residuals: tuple[Residual, ...],              # non-selected hypotheses
}
```

---

## § 3. Acceptance Law

Λ_haraka is constitutionally valid **if and only if** all nine conditions hold:

### § 3.1 Input Conditions

1. **HasSpectrum(x)**
   ```
   ∃ HarakaRoleSpectrum ∈ input
   ```
   The input MUST be a valid HarakaRoleSpectrum from Γ_haraka.

2. **HasContext(x)**
   ```
   ∃ LicensingContext ∈ {
     SyllableContext,
     PatternContext,
     CompositionContext,
     ProsodyContext
   }
   ```
   A licensing context MUST be declared.

3. **HasEvidence(x)**
   ```
   ∃ LicensingEvidence with context-specific wasf/illah
   ```
   Licensing evidence MUST be provided.

4. **MatchesContextRequirement(x)**
   ```
   selected_hypothesis.required_context ⊆ provided_context
   ```
   The selected hypothesis MUST declare compatibility with the provided context.

### § 3.2 Selection Conditions

5. **SelectsExactlyOne(x)**
   ```
   |selected_hypotheses| = 1
   ```
   Exactly ONE hypothesis must be selected (not zero, not multiple).

6. **ValidatesInvalidatingDifferences(x)**
   ```
   ∀ fariq ∈ selected_hypothesis.invalidating_differences:
     fariq:absent is proven, NOT fariq:present
   ```
   All invalidating differences for the selected role MUST be negated.

### § 3.3 Output Conditions

7. **PreservesIdentity(x)**
   ```
   LicensedHarakaRole.source_spectrum_identity = HarakaRoleSpectrum.source_identity
   ```
   All source identities MUST be preserved.

8. **ProducesLicensedOnly(x)**
   ```
   output.licensed_role_name starts with "licensed_"
   output.licensed_role_name does NOT start with "final_" or "determined_"
   ```
   Output is licensed role, NOT final function or determined meaning.

9. **DeclaresNonSelectedResiduals(x)**
   ```
   ∀ h ∈ Spectrum.hypotheses where h ≠ selected_hypothesis:
     defer:non_selected_hypothesis:{h.role_name}:present ∈ residuals
   ```
   Non-selected hypotheses MUST be preserved as deferred residuals.

---

## § 4. Failure Law

Λ_haraka **FAILS** (produces BLOCKED status) if any condition holds:

### § 4.1 Forbidden Output Violation

```
outputs ∩ {
  "WeightCandidate",          # Wazn
  "Irab",                     # Iʿrab
  "IrabCandidate",
  "CaseEffect",
  "ArudCandidate",            # ʿArūḍ
  "SyllableCandidate",        # Next layer
  "SyllableConstituent",      # Next layer
  "PatternCandidate",         # Next layer
  "FinalFunction",            # Final determination
  "DeterminedRole",           # Final determination
  "FinalMeaning",             # Final determination
  "HukmCandidate",            # Hukm layer
  "RealityClaim"              # Reality layer
} ≠ ∅
```

### § 4.2 Multiple Selection

```
|selected_hypotheses| > 1
```
Selecting multiple roles simultaneously is FORBIDDEN without explicit conjunction proof.

### § 4.3 Context Mismatch

```
selected_hypothesis.required_context ⊈ provided_context
```
Cannot license a role whose context requirements are not met.

### § 4.4 Invalidating Difference Present

```
∃ fariq ∈ selected_hypothesis.invalidating_differences:
  فارق:{fariq}:present is proven
```
If an invalidating difference is present, licensing is BLOCKED.

### § 4.5 Identity Loss

```
LicensedHarakaRole.source_spectrum_identity ⊄ HarakaRoleSpectrum.source_identity
```
Source identities must be preserved.

### § 4.6 Premature Finalization

```
output.licensed_role_name starts with "final_" or "determined_"
```
Λ produces licensed roles, NOT final determinations.

---

## § 5. Licensing Contexts

### § 5.1 SyllableContext

**When:** Building syllable structure from slots.

**Provides:**
- Syllable template evidence (CV, CVC, CVV, etc.)
- Syllable boundary evidence
- Syllable nucleus/coda requirements
- Phonotactic constraints

**Licenses:**
- `possible_syllabic_vowel` → `licensed_syllabic_vowel`
- `possible_closure` (sukun) → `licensed_syllable_coda`
- `possible_phonological_opening` → `licensed_syllable_nucleus`

**Example:**

```python
LicensingContext(
  context_type="SyllableContext",
  syllable_template="CVC",
  position_in_syllable="nucleus",
  boundary_evidence="syllable_terminal:false",
)

Λ_haraka(
  HarakaRoleSpectrum(fatha_hypotheses),
  SyllableContext,
  SyllableTemplateEvidence
) → LicensedHarakaRole(
  licensed_role_name="licensed_syllabic_vowel",
  licensing_context="SyllableContext",
  licensing_evidence={
    "وصف:syllable_position:nucleus",
    "وصف:template_slot:vowel",
    "علة:syllable_structure_requires_vowel",
  },
)
```

**Forbidden Outputs:**
- `SyllableCandidate` (next layer)
- `CaseEffect` (wrong domain)
- `WeightCandidate` (wrong domain)

### § 5.2 PatternContext

**When:** Matching morphological pattern (وزن).

**Provides:**
- Pattern template evidence (فَعَلَ, فَعْلٌ, فِعْلٌ, etc.)
- Pattern slot position (first vowel, second vowel, etc.)
- Pattern slot occupancy requirements
- Root vs. augment evidence

**Licenses:**
- `possible_pattern_vowel` → `licensed_pattern_vowel`
- `possible_compression` (shadda) → `licensed_pattern_intensification`

**Example:**

```python
LicensingContext(
  context_type="PatternContext",
  pattern_template="فَعَلَ",
  pattern_position="first_vowel",
  expected_haraka="fatha",
)

Λ_haraka(
  HarakaRoleSpectrum(fatha_hypotheses),
  PatternContext,
  PatternTemplateEvidence
) → LicensedHarakaRole(
  licensed_role_name="licensed_pattern_vowel",
  licensing_context="PatternContext",
  licensing_evidence={
    "وصف:pattern_slot:first_vowel",
    "وصف:pattern_template:faʿala",
    "علة:pattern_requires_fatha",
  },
)
```

**Forbidden Outputs:**
- `WeightCandidate` (next layer)
- `PatternCandidate` (next layer)
- `CaseEffect` (wrong domain)
- `FinalPattern` (final determination)

### § 5.3 CompositionContext

**When:** Building syntactic composition (تركيب).

**Provides:**
- Compositional tree structure
- Syntactic role evidence (subject, object, etc.)
- Amil (عامل) evidence
- I'rab position evidence (terminal position)
- Definiteness evidence
- Mabniyy vs. mu'rab evidence

**Licenses:**
- `possible_case_marker_candidate` → `licensed_case_marker_role`
- `possible_indefiniteness_marker_candidate` (tanwin) → `licensed_indefiniteness_marker`
- `possible_jazm_candidate` (sukun) → `licensed_jazm_marker`

**Example:**

```python
LicensingContext(
  context_type="CompositionContext",
  syntactic_role="مفعول به",
  amil="فعل متعدي",
  position="terminal",
  definiteness="indefinite",
)

Λ_haraka(
  HarakaRoleSpectrum(fatha_hypotheses),
  CompositionContext,
  CompositionEvidence
) → LicensedHarakaRole(
  licensed_role_name="licensed_case_marker_role",
  licensing_context="CompositionContext",
  licensing_evidence={
    "وصف:position:terminal",
    "وصف:syntactic_role:object",
    "وصف:amil:transitive_verb",
    "علة:case_marking_licensed_by_amil",
  },
)
```

**Forbidden Outputs:**
- `CaseEffect` (next layer)
- `Irab` (next layer)
- `IrabCandidate` (next layer)
- `FinalCaseJudgment` (final determination)
- `CompositionCandidate` (next layer)

**CRITICAL:**
```
licensed_case_marker_role ≠ Nasb
licensed_case_marker_role ≠ CaseEffect

Λ_haraka licenses the ROLE.
A later layer (IrabCandidate) produces the case effect.
```

### § 5.4 ProsodyContext

**When:** Building prosodic meter (عروض).

**Provides:**
- Arud meter template
- Taf'ilah (تفعيلة) evidence
- Sabab/watad structure
- Weight contribution requirements

**Licenses:**
- `possible_arud_relevance` → `licensed_arud_weight_contributor`
- `possible_compression` (shadda) → `licensed_arud_heavy_weight`

**Example:**

```python
LicensingContext(
  context_type="ProsodyContext",
  meter="بحر الطويل",
  tafila="فعولن",
  position_in_tafila="second_position",
)

Λ_haraka(
  HarakaRoleSpectrum(fatha_hypotheses),
  ProsodyContext,
  ProsodyEvidence
) → LicensedHarakaRole(
  licensed_role_name="licensed_arud_weight_contributor",
  licensing_context="ProsodyContext",
  licensing_evidence={
    "وصف:meter:taweel",
    "وصف:tafila:faʿuulun",
    "علة:arud_weight_requirement",
  },
)
```

**Forbidden Outputs:**
- `ArudCandidate` (next layer)
- `MeterJudgment` (final determination)
- `FinalMeterJudgment` (final determination)

---

## § 6. Relationship to Γ_haraka and Next Layers

### § 6.1 Division of Labor

```
Γ_haraka (Phase 2B — DONE):
  Input: SlotCandidate × Option[SlotGeometry]
  Output: HarakaRoleSpectrum (multiple "possible_*" hypotheses)
  Rank: ANALOGICAL (candidate level)
  Status: Implemented (PR #89)

Λ_haraka (This Constitution — FUTURE):
  Input: HarakaRoleSpectrum × LicensingContext
  Output: LicensedHarakaRole (ONE "licensed_*" role)
  Rank: Depends on context evidence (ANALOGICAL to DIRECT_HEARING)
  Status: Constitutional document only

Next Layers (FUTURE, NOT Λ's responsibility):
  Λ_syllable → SyllableCandidate
  Λ_pattern → PatternCandidate / WeightCandidate
  Λ_composition → IrabCandidate / CaseEffect
  Λ_prosody → ArudCandidate
```

### § 6.2 Λ_haraka Does NOT Produce

❌ **Λ_haraka MUST NOT produce:**

1. **Syllable Layer:**
   - `SyllableCandidate`
   - `SyllableConstituent`
   - `SyllableStructure`

2. **Pattern/Weight Layer:**
   - `WeightCandidate`
   - `PatternCandidate`
   - `RootCandidate`
   - `Wazn`

3. **Case/Composition Layer:**
   - `IrabCandidate`
   - `CaseEffect`
   - `Irab`
   - `Nasb` / `Raf` / `Jarr` / `Jazm`
   - `CompositionCandidate`

4. **Prosody Layer:**
   - `ArudCandidate`
   - `MeterCandidate`
   - `TafilaCandidate`

5. **Final Determinations:**
   - `FinalFunction`
   - `DeterminedRole`
   - `FinalMeaning`
   - `HukmCandidate`
   - `RealityClaim`

✅ **Λ_haraka ONLY produces:**
- `LicensedHarakaRole` (licensed role with context)
- `Residual` (when licensing fails or hypotheses not selected)

---

## § 7. Examples

### § 7.1 Example 1: Syllable Context — Fatha as Syllabic Vowel

**Input Spectrum (from Γ_haraka):**
```python
HarakaRoleSpectrum(
  haraka_identity=("identity:haraka:fatha",),
  hypotheses=(
    HarakaRoleHypothesis(
      role_name="possible_phonological_opening",
      role_genus="phonological",
    ),
    HarakaRoleHypothesis(
      role_name="possible_pattern_vowel",
      role_genus="morphological_pattern",
      required_context=("requires_lambda_context", "requires_pattern_template"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_case_marker_candidate",
      role_genus="morphosyntactic",
      required_context=("requires_lambda_context", "requires_composition_context"),
    ),
    HarakaRoleHypothesis(
      role_name="possible_syllabic_vowel",
      role_genus="syllabic",
      required_context=("requires_lambda_context", "requires_syllable_boundary"),
    ),
  ),
)
```

**Licensing Context:**
```python
LicensingContext(
  context_type="SyllableContext",
  syllable_template="CVC",
  position_in_syllable="nucleus",
)
```

**Λ_haraka Selection:**
```python
LicensedHarakaRole(
  source_spectrum_identity=("identity:haraka:fatha",),
  selected_hypothesis=HarakaRoleHypothesis(
    role_name="possible_syllabic_vowel",
    role_genus="syllabic",
  ),
  licensing_context="SyllableContext",
  licensing_evidence=EvidenceSet(
    items=(
      Evidence(
        source_layer="SyllableContext",
        proves="وصف:syllable_position:nucleus:evidenced",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="SyllableContext",
        proves="علة:syllable_requires_vowel:verified",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="SyllableContext",
        proves="فارق:non_syllabic_context:absent",
        rank=EvidenceRank.ANALOGICAL,
      ),
    ),
  ),
  licensed_role_name="licensed_syllabic_vowel",
  rank=EvidenceRank.ANALOGICAL,
  residuals=(
    Residual(
      effect="defer:non_selected_hypothesis:possible_pattern_vowel:present",
      evidence=...,
    ),
    Residual(
      effect="defer:non_selected_hypothesis:possible_case_marker_candidate:present",
      evidence=...,
    ),
  ),
)
```

**Non-Selected Hypotheses → Residuals:**
- `possible_pattern_vowel` → `defer:non_selected_hypothesis:possible_pattern_vowel:present`
- `possible_case_marker_candidate` → `defer:non_selected_hypothesis:possible_case_marker_candidate:present`
- `possible_phonological_opening` → (absorbed into selected syllabic role, not deferred)

### § 7.2 Example 2: Composition Context — Fatha as Case Marker

**Input Spectrum:** (same as Example 1)

**Licensing Context:**
```python
LicensingContext(
  context_type="CompositionContext",
  syntactic_role="مفعول به",
  amil="فعل متعدي",
  position="terminal",
  definiteness="indefinite",
)
```

**Λ_haraka Selection:**
```python
LicensedHarakaRole(
  source_spectrum_identity=("identity:haraka:fatha",),
  selected_hypothesis=HarakaRoleHypothesis(
    role_name="possible_case_marker_candidate",
    role_genus="morphosyntactic",
  ),
  licensing_context="CompositionContext",
  licensing_evidence=EvidenceSet(
    items=(
      Evidence(
        source_layer="CompositionContext",
        proves="وصف:position:terminal:evidenced",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="CompositionContext",
        proves="وصف:syntactic_role:object:evidenced",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="CompositionContext",
        proves="علة:case_marking_licensed_by_amil:verified",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="CompositionContext",
        proves="فارق:mabniyy_word:absent",
        rank=EvidenceRank.ANALOGICAL,
      ),
    ),
  ),
  licensed_role_name="licensed_case_marker_role",
  rank=EvidenceRank.ANALOGICAL,
  residuals=(
    Residual(
      effect="defer:non_selected_hypothesis:possible_pattern_vowel:present",
      ...
    ),
    Residual(
      effect="defer:non_selected_hypothesis:possible_syllabic_vowel:present",
      ...
    ),
  ),
)
```

**CRITICAL:**
```python
# Λ_haraka produces:
licensed_role_name="licensed_case_marker_role"

# Λ_haraka does NOT produce:
case_effect="Nasb"  # ❌ FORBIDDEN
irab="منصوب"        # ❌ FORBIDDEN

# A LATER layer (IrabCandidate) will consume LicensedHarakaRole
# and produce CaseEffect/Irab
```

### § 7.3 Example 3: Pattern Context — Fatha as Pattern Vowel

**Input Spectrum:** (same as Example 1)

**Licensing Context:**
```python
LicensingContext(
  context_type="PatternContext",
  pattern_template="فَعَلَ",
  pattern_position="first_vowel",
  expected_haraka="fatha",
)
```

**Λ_haraka Selection:**
```python
LicensedHarakaRole(
  source_spectrum_identity=("identity:haraka:fatha",),
  selected_hypothesis=HarakaRoleHypothesis(
    role_name="possible_pattern_vowel",
    role_genus="morphological_pattern",
  ),
  licensing_context="PatternContext",
  licensing_evidence=EvidenceSet(
    items=(
      Evidence(
        source_layer="PatternContext",
        proves="وصف:pattern_slot:first_vowel:evidenced",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="PatternContext",
        proves="وصف:pattern_template:faʿala:evidenced",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="PatternContext",
        proves="علة:pattern_requires_fatha:verified",
        rank=EvidenceRank.ANALOGICAL,
      ),
      Evidence(
        source_layer="PatternContext",
        proves="فارق:pattern_mismatch:absent",
        rank=EvidenceRank.ANALOGICAL,
      ),
    ),
  ),
  licensed_role_name="licensed_pattern_vowel",
  rank=EvidenceRank.ANALOGICAL,
  residuals=(
    Residual(
      effect="defer:non_selected_hypothesis:possible_case_marker_candidate:present",
      ...
    ),
    Residual(
      effect="defer:non_selected_hypothesis:possible_syllabic_vowel:present",
      ...
    ),
  ),
)
```

**CRITICAL:**
```python
# Λ_haraka produces:
licensed_role_name="licensed_pattern_vowel"

# Λ_haraka does NOT produce:
wazn="فَعَلَ"           # ❌ FORBIDDEN
pattern_candidate=...  # ❌ FORBIDDEN
weight_candidate=...   # ❌ FORBIDDEN

# A LATER layer (PatternCandidate) will consume LicensedHarakaRole
# and produce Wazn/PatternCandidate
```

---

## § 8. Forbidden Outputs (Comprehensive)

### § 8.1 Layer-Level Forbidden Outputs

`LicensedHarakaRole` (the Λ_haraka output) MUST NOT produce:

```python
FORBIDDEN_LICENSED_HARAKA_ROLE: tuple[str, ...] = (
    # Constitutional base
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",

    # Syllable layer (next layer)
    "SyllableCandidate",
    "SyllableConstituent",
    "SyllableStructure",

    # Weight/Pattern layer (next layer)
    "WeightCandidate",
    "RootCandidate",
    "PatternCandidate",
    "Wazn",
    "FinalPattern",

    # Case/Composition layer (next layer)
    "CaseEffect",
    "Irab",
    "IrabCandidate",
    "Nasb",
    "Raf",
    "Jarr",
    "Jazm",
    "CompositionCandidate",
    "FinalCaseJudgment",

    # Prosody layer (next layer)
    "ArudCandidate",
    "MeterCandidate",
    "TafilaCandidate",
    "FinalMeterJudgment",

    # Final determinations
    "FinalFunction",
    "DeterminedRole",
    "SelectedFunction",

    # Higher layers
    "WordCandidate",
    "MeaningCandidate",
    "IfadahCandidate",
)
```

---

## § 9. Non-Goals (Explicit)

This constitution **explicitly does NOT**:

1. ❌ Implement Λ_haraka (this is constitutional document only)
2. ❌ Implement SyllableCandidate (next layer)
3. ❌ Implement PatternCandidate / WeightCandidate (next layer)
4. ❌ Implement IrabCandidate / CaseEffect (next layer)
5. ❌ Implement ArudCandidate (next layer)
6. ❌ Produce final determinations (FinalFunction, DeterminedRole)
7. ❌ Produce case effects (Nasb, Raf, Jarr, Jazm)
8. ❌ Produce weight/pattern (Wazn, PatternCandidate)
9. ❌ Produce syllables (SyllableCandidate, SyllableConstituent)
10. ❌ Produce prosodic meter (ArudCandidate, MeterJudgment)

**This constitution ONLY:**
- ✅ Defines the constitutional contract for Λ_haraka
- ✅ Specifies inputs, outputs, and forbidden behaviors
- ✅ Establishes licensing contexts
- ✅ Documents the relationship between Γ and Λ
- ✅ Provides examples of licensed role selection

---

## § 10. Implementation Phases

### Phase 1 (This PR): Constitutional Document
- ✅ This file: `HARAKA_LICENSING_CONSTITUTION.md`
- ✅ Zero code
- ✅ Zero tests
- ✅ Documentation only

### Phase 2 (Future PR): Data Structures
- `src/qiyas_core/licensed_haraka_role.py`
  - `LicensingContext` dataclass
  - `LicensedHarakaRole` dataclass
- `src/qiyas_core/forbidden_outputs.py`
  - `FORBIDDEN_LICENSED_HARAKA_ROLE` constant
- Zero adapters
- Zero rules
- Zero integration tests

### Phase 3 (Later PR): Adapter Implementation
- `src/qiyas_core/haraka_licensing_adapter.py`
  - Context-specific licensing adapters (Syllable, Pattern, Composition, Prosody)
- `src/qiyas_core/rules/haraka_licensing_rules.py`
  - Λ_haraka rules for each context type
- Integration tests
- Constitutional validation tests

---

## § 11. Governance Integration

### § 11.1 Layer Registry Update

When implementing Λ_haraka, add to `LAYER_REGISTRY.md`:

```markdown
### Layer Λ: HarakaRoleLicensing

**Input:** HarakaRoleSpectrum × LicensingContext
**Output:** LicensedHarakaRole | Residual
**Status:** constitutional_contract_only (Phase 1)
**Source PR:** #TBD
**Coverage:** None (documentation only)

**Proof Obligation:** Which role is licensed under this specific context?

**Constitutional Principle:**
Λ selects ONE hypothesis from Γ's spectrum under licensing context.
Λ does NOT produce next layer's object.
```

### § 11.2 Duplicate Prevention Table Update

When implementing Λ_haraka, add to `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` § 2:

| Need | DO NOT CREATE | USE / EXTEND INSTEAD |
|------|--------------|---------------------|
| License haraka role | HarakaRoleSelector, FinalHarakaFunction, DeterminedHaraka | Λ_haraka (LicensedHarakaRole) |
| Select from spectrum | SpectrumSelector, HypothesisChooser | Λ_haraka |

---

## § 12. Version Control

**Version:** 1.0.0
**Status:** Constitutional (Phase 1)
**Date:** 2026-06-05
**Maintainer:** @sonaiso
**Dependencies:**
- `PROJECT_MATHEMATICAL_FOUNDATION.md`
- `HARAKA_ROLE_SPECTRUM_CONTRACT.md` (Γ_haraka)
- `LAYER_CONTRACT_CONSTITUTION.md`
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md`

---

## Appendix A: Governing Principles Summary

```
1. Γ ≠ Λ
   Gamma opens spectrum, Lambda selects.

2. Λ يرخّص، لا يحدد
   Lambda licenses, does not determine finality.

3. licensed_* ≠ final_*
   Licensed roles are not final determinations.

4. لا طبقة تنتج مخرج الطبقة التالية
   No layer produces the next layer's output.

5. السياق يرخّص الدور
   Context licenses the role.

6. كل دور مرخّص يحتاج بينة من سياقه
   Every licensed role requires evidence from its context.

7. الفرضيات غير المختارة تصبح بقايا مؤجلة
   Non-selected hypotheses become deferred residuals.

8. الحركة المرخصة ≠ الإعراب
   Licensed haraka role ≠ Case effect (Iʿrab).

9. الحركة المرخصة ≠ الوزن
   Licensed haraka role ≠ Weight (Wazn).

10. لا تحديد نهائي بلا طبقة التحديد
    No final determination without the determination layer.
```

---

## Appendix B: Central Law (بالعربية والإنجليزية)

```
Γ opens possibilities.
Λ licenses one role under context.
Λ does not produce the next layer's object.

Γ يفتح الاحتمالات.
Λ يرخّص دورًا واحدًا تحت سياق.
Λ لا ينتج كائن الطبقة التالية.
```

**Formal Expression:**

```
Γ_haraka: Slot → Spectrum[possible_*]
Λ_haraka: Spectrum × Context → licensed_* | Residual

licensed_* ≠ final_*
licensed_* ≠ next_layer_object

Examples:
  licensed_case_marker_role ≠ Nasb
  licensed_pattern_vowel ≠ Wazn
  licensed_syllabic_vowel ≠ SyllableCandidate
  licensed_arud_weight_contributor ≠ ArudCandidate
```

---

**END OF CONSTITUTION**
