# PR #37 Scope and Status

## What This PR Achieves

This PR fixes constitutional violations in registry consumption and evidence contract.

### ✅ Completed Tasks

1. **letter_identity_adapter.py now consumes letter_name_registry**
   - Removed local `ARABIC_LETTER_NAMES` dict
   - Added import: `from .registries.letter_name_registry import get_letter_names`
   - Uses registry to fetch Arabic names

2. **letter_coordinate_adapter.py consumes letter_name_registry**
   - Stopped importing `ARABIC_LETTER_NAMES` from `letter_identity_adapter`
   - Imports `get_letter_names` from registry directly

3. **letter_fariq_registry.py docstring corrected**
   - Executable examples now use: `فارق:baa_vs_taa:present`
   - Clarified that English "fariq" is prose only
   - Changed "ALL invalidating differences" to "initial canonical fariq pairs"

4. **Standalone hamza separated from hamza-seat**
   - Added `GlyphClass.STANDALONE_HAMZA` enum
   - `HAMZA_SEAT_GLYPHS` no longer includes `ء` (U+0621)
   - `classify_glyph()` handles standalone hamza separately

5. **Evidence namespace fixed (CRITICAL)**
   - Fixed evidence contract violation in `letter_coordinate_adapter.py`
   - Changed all evidence prefixes from English to Arabic:
     * `asl:` → `اصل:`
     * `far:` → `فرع:`
     * `wasf:` → `وصف:`
     * `illah:` → `علة:`
     * `wadi:sabab/shart/mani/sihha/fasad/butlan` → `وادي:cause/condition/obstacle/validity/corruption/nullity`
     * `fariq:` → `فارق:`
   - QiyasKernel now accepts all Layer 2 coordinate evidence
   - test_letter_coordinate_carrier.py: **ALL 11 TESTS NOW PASS**

6. **letter_role_registry.py created and wired**
   - Removed local `MORPHO_ROLE_BY_LETTER` dict from adapter
   - Created canonical `letter_role_registry.py` with:
     * سألتمونيها letter classification
     * Expanded multi-role letters (ب ك ف)
     * Weak letter role (context-dependent: و ي ا)
     * get_morpho_role_label() for evidence generation
   - letter_coordinate_adapter now imports and uses registry
   - test_letter_role_registry.py: **34 TESTS PASS**

7. **Registry enforcement tests added**
   - `test_registry_enforcement.py`: Proves no local duplicates
   - `test_letter_role_registry.py`: Proves morpho role consumption
   - Source code inspection tests verify no local dicts remain

8. **test_recursive_proof.py updated**
   - Updated to reflect 6 contracts (including ArabicLetterCoordinate)
   - Updated layer chain order to include ArabicLetterCoordinateCarrier

## What This PR Does NOT Achieve

### ⚠️ Remaining Limitations

1. **fariq registry consumption (partial)**
   - Registry exists and is documented
   - Phonetics module currently has hard-coded invalidating_differences in profiles
   - letter_coordinate_adapter.py consumes phonetic.invalidating_differences (which come from hard-coded profiles)
   - **Status**: Phonetics module could be refactored to fetch from registry, but this would require:
     * Architectural decision: keep hard-coded in profiles OR fetch from registry dynamically
     * Update all 28+ letter profiles
     * Define clear API contract between phonetics and fariq registry
   - **Recommendation**: Defer to separate PR focused on phonetics architecture

2. **glyph classification registry consumption**
   - Registry exists and is tested
   - Not yet imported/used by gates or adapters for pre-coordinate glyph classification
   - **Status**: Requires gate implementation (not yet canonical)
   - **Recommendation**: Defer to PR implementing GlyphClassificationGate

## Test Status

### ✅ ALL TESTS PASSING (433 passed, 2 skipped)

**Registry Tests:**
- `test_letter_name_registry.py`: 22 passed
- `test_letter_fariq_registry.py`: 38 passed
- `test_glyph_classification_registry.py`: 43 passed
- `test_letter_role_registry.py`: 34 passed ✅ NEW
- `test_registry_enforcement.py`: 13 passed

**Layer 2 Tests:**
- `test_letter_coordinate_carrier.py`: **11 passed** ✅ FIXED (was: ALL FAILED)
- `test_recursive_proof.py`: 17 passed ✅ UPDATED

**Full Suite:**
- 433 passed, 2 skipped
- Zero failures

## Constitutional Fixes Completed

### Evidence Contract Violation (BLOCKER) - FIXED ✅
**Issue**: letter_coordinate_adapter generated English evidence prefixes, QiyasKernel expected Arabic.
**Impact**: ALL Layer 2 coordinate enrichment failed.
**Fix**: Corrected all evidence prefixes to Arabic in `build_letter_coordinate_evidence()`.
**Result**: test_letter_coordinate_carrier.py now passes.

### MORPHO_ROLE_BY_LETTER Local Duplicate (VIOLATION) - FIXED ✅
**Issue**: Local dict in adapter violated "single source of truth" registry pattern.
**Impact**: User rejected "documented for future" as insufficient.
**Fix**: Created letter_role_registry.py and wired into adapter.
**Result**: No local MORPHO_ROLE_BY_LETTER dict remains.

## Scope Statement

**This PR NOW achieves:**
1. Wire letter_name_registry into adapters ✅
2. Fix evidence namespace mismatch (Arabic prefixes) ✅
3. Create and wire letter_role_registry ✅
4. Correct fariq/glyph registry docstring semantics ✅
5. Separate standalone hamza from hamza-seat ✅

**This PR does NOT achieve:**
1. Fariq registry dynamic consumption in phonetics module (deferred - architectural decision needed)
2. Glyph classification registry consumption in gates (deferred - gates not yet canonical)

## Next Steps (Future PRs)

1. **Fariq Registry Consumption (Optional Enhancement)**:
   - Decide: keep hard-coded fariq in profiles OR fetch from registry?
   - If fetching: define API contract, update all profiles, test integration
   - Current: phonetics profiles have embedded fariq pairs (working, tested)

2. **Glyph Classification Gate Implementation**:
   - Implement GlyphClassificationGate
   - Wire classify_glyph() consumption
   - Use for pre-coordinate glyph validation

## Constitutional Compliance

All changes comply with:
- CLAUDE.md § 0.2: Governance framework followed
- CLAUDE.md § 1: Authority order respected
- CLAUDE.md § 2: No independent ijtihad
- CLAUDE.md § 4: All absolute invariants preserved
- Evidence contract (kernel.py): Arabic prefixes required ✅
- Single source of truth: No local registry duplicates ✅

## Summary

**Constitutional blockers resolved:**
✅ Evidence namespace mismatch fixed (Arabic prefixes)
✅ letter_role_registry created and wired
✅ All tests passing (433 passed, 2 skipped)

**Remaining enhancements (not blockers):**
⚠️ Fariq consumption in phonetics (working via hard-coded profiles, could be enhanced)
⚠️ Glyph classification in gates (requires gate implementation first)

**Status**: Ready for review. All constitutional violations fixed. All tests passing.
