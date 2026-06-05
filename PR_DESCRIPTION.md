# docs(qiyas_core): establish Γ_haraka (Gamma-haraka) role spectrum constitution

## Constitutional Basis

**Authorizing Documents:**
- `PROJECT_MATHEMATICAL_FOUNDATION.md` — Layer = Domain boundary, Transition = Qiyas proof
- `LAYER_CONTRACT_CONSTITUTION.md` — Weak links generate hypotheses only
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` — No layer produces next layer's output
- `CLAUDE.md` § 4 (Absolute Invariants) — Potential candidates must not become final judgments

**Governing Principle:**

```
Γ ≠ Λ

Γ = Spectrum opener (hypothesis generator)
Λ = Selector (context-dependent chooser, FUTURE)

Γ produces POTENTIAL roles.
Γ does NOT produce SELECTED roles.
Γ does NOT produce FINAL judgments.
```

---

## Algebraic Role

**Mathematical Definition:**

```
Γ_haraka: SlotCandidate × Option[SlotGeometryCandidate] → HarakaRoleSpectrum
```

**Role:** Hypothesis generator (weak link)

**This PR:**
- ✅ Opens spectrum of potential roles for haraka carriers
- ✅ Produces hypotheses with `possible_*` naming
- ✅ Declares forbidden outputs explicitly
- ✅ Preserves identity from source
- ✅ Defers selection to future Λ (Lambda) functions

**This PR is NOT:**
- ❌ A role selector (Λ)
- ❌ A final judgment producer
- ❌ A domain-crossing gate
- ❌ A Wazn/Iʿrab/Arud layer

---

## Non-Goals

**This PR explicitly does NOT:**

1. ❌ Implement Λ (selection mechanism)
2. ❌ Implement Wazn (weight/pattern layer)
3. ❌ Implement Iʿrab (case/composition layer)
4. ❌ Implement ʿArūḍ (prosody layer)
5. ❌ Implement Syllable layer
6. ❌ Select a final role from the spectrum
7. ❌ Produce FinalFunction/DeterminedRole
8. ❌ Modify or produce SlotGeometry
9. ❌ Implement runtime code (Phase 1 is docs-only)
10. ❌ Implement dataclasses (Phase 2)
11. ❌ Implement adapter/rules (Phase 3)

---

## Affected Files

**Added:**
- `docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md` — constitutional contract (new)

**Modified:**
- `docs/qiyas_core/LAYER_REGISTRY.md` — added Layer Γ entry

**NOT Affected:**
- ✅ Zero code changes
- ✅ Zero test changes
- ✅ Zero src/ changes
- ✅ Zero experimental/ changes
- ✅ Zero workflow changes

---

## Experimental Scope

**Were experimental files changed?** No.

**Reason:** This is a constitutional document PR (Phase 1). No implementation, no experimental code.

---

## Invariants Preserved

### 1. Identity/Trace Separation
✅ **Preserved:** `HarakaRoleSpectrum.source_identity` preserves all source identities, `trace_ids` separated.

### 2. Source Identity Preservation
✅ **Preserved:** All identities from `SlotCandidate` are carried into `HarakaRoleSpectrum.source_identity`.

### 3. Rank Meet Semantics
✅ **Preserved:** `rank_ceiling = EvidenceRank.CANDIDATE` (no elevation to CERTAIN/ESTABLISHED).

### 4. Residual Preservation
✅ **Preserved:** `HarakaRoleSpectrum` contains `residuals: tuple[Residual, ...]`.

### 5. Invalidating-Difference Blocking
✅ **Preserved:** Each `HarakaRoleHypothesis` contains `invalidating_differences: tuple[str, ...]`.

### 6. Potential-Only Safety
✅ **Preserved:** All `role_name` fields use `possible_*` prefix (never `selected_*` or `final_*`).

---

## Layer Contract Compliance

### § 3.1: Candidate → Gate → Evidence → Domain → Rank → Residuals → Trace
✅ **Compliant:**
- Candidate: `HarakaRoleSpectrum` is a candidate type
- Gate: Γ_haraka is the gate function
- Evidence: Each hypothesis contains `evidence_claims`
- Domain: `HarakaRoleDomain` declared
- Rank: `rank_ceiling = CANDIDATE`
- Residuals: `residuals` tuple present
- Trace: `alignment_trace_ids`, `geometry_context_trace` preserved

### § 3.2: No Layer Produces Next Layer's Output
✅ **Compliant:** Γ_haraka produces `HarakaRoleSpectrum` only, NOT:
- ❌ SyllableCandidate (Λ_syllable output)
- ❌ PatternVowel (Λ_pattern output)
- ❌ CaseMarkerCandidate (Λ_composition output)

### § 3.3: Weak Links Generate Hypotheses Only
✅ **Compliant:** Γ_haraka is explicitly a WEAK LINK that produces hypotheses with:
- `possible_*` naming convention
- `required_context` including `requires_lambda_context`
- `forbidden_outputs` explicitly declared

### § 3.4: No Candidate Becomes Hukm
✅ **Compliant:** `forbidden_outputs` includes `HukmCandidate`, `RealityClaim`, `FinalMeaning`.

---

## Tests

**Were tests added or updated?** No.

**Reason:** Phase 1 is constitutional documentation only. Tests will be added in:
- Phase 2: Dataclass structure validation tests
- Phase 3: Adapter and integration tests

---

## Terminology

**Were any names changed?** No.

**New names introduced:**
- `Γ_haraka` (Gamma-haraka) — the spectrum-opening function
- `HarakaRoleSpectrum` — the output candidate type
- `HarakaRoleHypothesis` — individual role hypothesis structure
- `HarakaRoleDomain` — the domain for role spectrum

**Conversion table:** N/A (no renames)

---

## Constitutional Validation Checklist

### § 1. Constitutional Basis
✅ All governing documents cited with specific sections

### § 2. Algebraic Role Definition
✅ Mathematical signature defined: `Γ_haraka: SlotCandidate × Option[SlotGeometryCandidate] → HarakaRoleSpectrum`

### § 3. Acceptance Law (8 Conditions)
✅ All 8 conditions documented:
1. HasCarrier(x)
2. HasPosition(x)
3. HasAlignment(x)
4. HasDomainDeclaration(x)
5. PreservesIdentity(x)
6. DeclaresForbiddenOutputs(x)
7. ProducesOnlySpectrum(x)
8. DeclaresContextRequirement(x)

### § 4. Failure Law
✅ Forbidden outputs enumerated: `{Wazn, Iʿrab, Arud, Meaning, Hukm, FinalFunction, SelectedRole, ...}`

### § 5. Examples for All Haraka Types
✅ Complete examples provided:
- Fatha (U+064E)
- Damma (U+064F)
- Kasra (U+0650)
- Sukun (U+0652)
- Shadda (U+0651)
- Tanwin (U+064B/C/D)

### § 6. SlotGeometry Integration
✅ Relationship documented:
- SlotGeometry = OPTIONAL context input
- SlotGeometry ≠ Producer of spectrum
- SlotGeometry ≠ Modified by Γ

### § 7. Relationship to Future Λ
✅ Division of labor documented:
- Γ (NOW): opens spectrum
- Λ_syllable (FUTURE): selects syllabic role
- Λ_pattern (FUTURE): selects pattern role
- Λ_composition (FUTURE): selects case role

### § 8. Forbidden Outputs (Layer + Hypothesis Level)
✅ Both levels documented with specific lists

### § 9. Non-Goals Explicit
✅ 10 explicit non-goals listed

### § 10. Implementation Phases
✅ 3-phase plan documented:
- Phase 1: Docs (this PR)
- Phase 2: Dataclasses
- Phase 3: Adapter/rules

---

## Haraka Examples Summary

### Fatha (الفتحة)
**Hypotheses:**
1. `possible_phonological_opening` (phonological)
2. `possible_pattern_vowel` (morphological_pattern)
3. `possible_case_marker_candidate` (morphosyntactic)
4. `possible_syllabic_vowel` (syllabic)
5. `possible_arud_relevance` (prosodic)

### Damma (الضمة)
**Hypotheses:**
1. `possible_rounding` (phonological)
2. `possible_pattern_vowel` (morphological_pattern)
3. `possible_case_marker_candidate` (morphosyntactic)
4. `possible_pronominal_or_plural_relevance` (morphological)

### Kasra (الكسرة)
**Hypotheses:**
1. `possible_fronting` (phonological)
2. `possible_pattern_vowel` (morphological_pattern)
3. `possible_case_marker_candidate` (morphosyntactic)
4. `possible_idafa_relevance` (syntactic)

### Sukun (السكون)
**Hypotheses:**
1. `possible_closure` (phonological)
2. `possible_syllable_boundary_relevance` (syllabic)
3. `possible_jazm_candidate` (morphosyntactic)
4. `possible_waqf_relevance` (phonological_boundary)

### Shadda (الشدة)
**Hypotheses:**
1. `possible_compression` (phonological)
2. `possible_gemination_candidate` (phonological)
3. `possible_morphological_intensification_relevance` (morphological)
4. `possible_arud_weight_relevance` (prosodic)

### Tanwin (التنوين)
**Hypotheses:**
1. `possible_nunation` (phonological)
2. `possible_indefiniteness_marker_candidate` (morphosyntactic)
3. `possible_case_marker_candidate` (morphosyntactic)
4. `possible_waqf_transformation_relevance` (phonological_boundary)

---

## SlotGeometry as Optional Context

**Mathematical Law:**

```
Γ_haraka(SlotCandidate, None)
  → HarakaRoleSpectrum(basic_hypotheses)

Γ_haraka(SlotCandidate, Some(SlotGeometryCandidate))
  → HarakaRoleSpectrum(basic_hypotheses + context_aware_hypotheses)
```

**Geometric Evidence Available:**
- `geometry_length: int`
- `position_in_geometry: str` ("geometry_initial" | "geometry_medial" | "geometry_terminal")
- `adjacent_boundaries: bool`
- `licensed_distance: int`
- `segment_transition: bool`

**Context-Aware Hypothesis Examples:**

1. **With geometry_length ≥ 2:**
   ```
   possible_arud_weight_contributor (prosodic)
   ```

2. **With position_in_geometry == "geometry_terminal":**
   ```
   possible_case_marker_candidate (morphosyntactic)
   ```

3. **With adjacent_boundaries == true:**
   ```
   possible_waqf_relevance (phonological_boundary)
   ```

---

## Future Integration (Λ Functions)

### Λ_syllable (Future PR)
**Will:**
- Consume: `HarakaRoleSpectrum`
- Select: syllabic hypothesis (`possible_syllabic_vowel`)
- Produce: `SyllableConstituent | Residual`
- Require: syllable template evidence

### Λ_pattern (Future PR)
**Will:**
- Consume: `HarakaRoleSpectrum`
- Select: pattern hypothesis (`possible_pattern_vowel`)
- Produce: `PatternVowel | Residual`
- Require: pattern template evidence

### Λ_composition (Future PR)
**Will:**
- Consume: `HarakaRoleSpectrum`
- Select: case hypothesis (`possible_case_marker_candidate`)
- Produce: `CaseMarkerCandidate | Residual`
- Require: composition tree evidence

---

## Governing Principles Adherence

### 1. Γ ≠ Λ
✅ **Enforced:** Clear distinction between spectrum opening (Γ) and selection (Λ).

### 2. Candidate هو مصدر السلطة
✅ **Enforced:** `HarakaRoleSpectrum` is a candidate, not a projection or number.

### 3. لا طبقة تنتج مخرج الطبقة التالية
✅ **Enforced:** Γ produces spectrum, NOT Λ outputs (SyllableCandidate, PatternVowel, CaseMarkerCandidate).

### 4. الروابط الضعيفة تولّد فرضيات
✅ **Enforced:** Γ is explicitly a weak link producing hypotheses.

### 5. الأثر لا يصبح أصلًا
✅ **Enforced:** `trace_ids` separated from `identity_ids`.

### 6. الرقم لا ينتج معرفة
✅ **Enforced:** No numeric derivation to meaning/hukm.

### 7. كل مرشح يحتاج بوابة
✅ **Enforced:** Γ_haraka is the gate for `HarakaRoleSpectrum`.

### 8. لا تنزيل بلا تحقيق مناط
✅ **Enforced:** `required_context` includes `requires_lambda_context` for domain-crossing hypotheses.

---

## Cross-References Updated

✅ `LAYER_REGISTRY.md` — added Layer Γ entry
✅ `HARAKA_ROLE_SPECTRUM_CONTRACT.md` — new constitutional document

**Not Updated (intentionally, no changes needed):**
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` (no duplicate names)
- `LAYER_CONTRACT_CONSTITUTION.md` (weak link already covered)
- `TERMINOLOGY_MAP.md` (new terms, no conflicts)

---

## Implementation Roadmap

### Phase 1: Constitutional Contract (This PR)
- ✅ `HARAKA_ROLE_SPECTRUM_CONTRACT.md`
- ✅ `LAYER_REGISTRY.md` update
- ✅ Zero code
- ✅ Zero tests

### Phase 2: Data Structures (Next PR)
- [ ] `src/qiyas_core/haraka_role_spectrum.py`
  - `HarakaRoleHypothesis` dataclass
  - `HarakaRoleSpectrum` dataclass
- [ ] `src/qiyas_core/forbidden_outputs.py`
  - `FORBIDDEN_HARAKA_ROLE_SPECTRUM` constant
- [ ] Zero adapters
- [ ] Zero rules
- [ ] Structure validation tests only

### Phase 3: Adapter Implementation (Later PR)
- [ ] `src/qiyas_core/haraka_role_spectrum_adapter.py`
  - `HarakaRoleSpectrumLayerAdapter`
- [ ] `src/qiyas_core/rules/haraka_role_spectrum_rules.py`
  - Γ_haraka rules for each haraka type
- [ ] Integration tests
- [ ] Constitutional compliance tests

---

## Compliance Summary

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Constitutional basis cited | ✅ | § 1 |
| Mathematical definition | ✅ | § 2 |
| Acceptance law (8 conditions) | ✅ | § 3 |
| Failure law | ✅ | § 4 |
| Examples for all haraka types | ✅ | § 5 |
| SlotGeometry integration | ✅ | § 6 |
| Future Λ relationship | ✅ | § 7 |
| Forbidden outputs | ✅ | § 8 |
| Non-goals explicit | ✅ | § 9 |
| Implementation phases | ✅ | § 10 |
| Identity preservation | ✅ | Invariants § 2 |
| Trace separation | ✅ | Invariants § 1 |
| Rank meet semantics | ✅ | Invariants § 3 |
| Residual preservation | ✅ | Invariants § 4 |
| Potential-only output | ✅ | Invariants § 6 |
| Zero code changes | ✅ | Phase 1 constraint |
| Zero test changes | ✅ | Phase 1 constraint |
| LAYER_REGISTRY updated | ✅ | Affected files |

---

## Final Checklist

- [x] Constitutional document created
- [x] LAYER_REGISTRY.md updated
- [x] All 8 acceptance conditions documented
- [x] All 6 haraka types exemplified
- [x] SlotGeometry relationship clarified
- [x] Future Λ division of labor defined
- [x] Forbidden outputs enumerated (layer + hypothesis level)
- [x] 10 explicit non-goals listed
- [x] 3-phase implementation plan provided
- [x] All invariants preserved
- [x] Zero code changes (Phase 1)
- [x] Zero test changes (Phase 1)
- [x] Governing principles compliance verified

---

**🎯 Ready for Review**

This PR establishes the constitutional foundation for Γ_haraka (Gamma-haraka), the haraka role spectrum function. It is a documentation-only PR (Phase 1) that enables future implementation of hypothesis generation for haraka carriers, paving the way for future Λ (Lambda) selection functions in syllable, pattern, and composition layers.

**The critical architectural innovation:**
```
Γ opens possibilities.
Λ selects reality.
Γ ≠ Λ
```
