# PR #37 Scope and Limitations

## What This PR Achieves

This PR wires `letter_name_registry` into adapters and fixes glyph/fariq registry semantics.

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

5. **Registry enforcement tests added** (`test_registry_enforcement.py`)
   - Proves adapters have NO local ARABIC_LETTER_NAMES
   - Proves adapters import get_letter_names from registry
   - Proves fariq registry uses فارق: in docstrings
   - Proves registry metadata forbids adapter duplication

## What This PR Does NOT Achieve

### ⚠️ Known Limitations

1. **MORPHO_ROLE_BY_LETTER remains local** (lines 41-47 in letter_coordinate_adapter.py)
   - Still defined as local dict
   - Needs future `letter_role_registry.py` or equivalent
   - Out of scope for this PR

2. **test_letter_coordinate_carrier.py fails** (pre-existing issue)
   - Evidence prefix mismatch: adapter uses English (`wasf:`, `illah:`, `wadi:`)
   - QiyasKernel expects Arabic (`وصف:`, `علة:`, `وادي:`)
   - This is a **pre-existing blocker** not introduced by this PR
   - Fixing requires Layer 2 coordinate adapter evidence overhaul
   - Out of scope for this PR (registry wiring only)

3. **fariq registry not fully consumed**
   - Registry exists and is tested
   - `letter_coordinate_adapter.py` and `letter_coordinate_rules.py` do NOT yet import/use `get_fariq_pairs()` or `has_invalidating_difference()`
   - Future PR needed to wire fariq consumption into coordinate layer

4. **glyph classification registry not fully wired**
   - Registry exists and is tested
   - Not yet consumed by adapters/gates
   - Future PR needed for actual consumption

## Test Status

### ✅ Passing Tests (116 total)
- `test_letter_name_registry.py`: 22 passed
- `test_letter_fariq_registry.py`: 38 passed
- `test_glyph_classification_registry.py`: 43 passed
- `test_registry_enforcement.py`: 13 passed (NEW)

### ❌ Pre-existing Failing Test
- `test_letter_coordinate_carrier.py`: BLOCKED
  - Cause: Arabic vs English evidence prefix mismatch
  - Status: Pre-existing issue (not caused by this PR)
  - Resolution: Requires separate PR to fix Layer 2 evidence generation

## Scope Statement

**This PR achieves:**
"Wire letter_name_registry into Layer 1/2 adapters and correct fariq/glyph registry docstring semantics"

**This PR does NOT achieve:**
"Full Layer 2 source-of-truth enforcement" or "Complete registry consumption for all Layer 2 truths"

## Next Steps (Future PRs)

1. **PR #38**: Fix Layer 2 coordinate adapter Arabic evidence prefix mismatch
   - Convert evidence from English to Arabic prefixes
   - Fix test_letter_coordinate_carrier.py failure

2. **PR #39**: Create letter_role_registry.py
   - Move MORPHO_ROLE_BY_LETTER to registry
   - Wire into letter_coordinate_adapter

3. **PR #40**: Wire fariq registry consumption
   - Import get_fariq_pairs() in coordinate adapter/rules
   - Use for invalidating difference validation

4. **PR #41**: Wire glyph classification registry consumption
   - Import classify_glyph() in gates/adapters
   - Use for pre-coordinate glyph classification

## Constitutional Compliance

All changes comply with:
- CLAUDE.md § 0.2 governance framework
- Authority Order (§ 1): constitutional docs → canonical code → tests
- No Independent Ijtihad (§ 2): no terminology invention
- Absolute Invariants (§ 4): all preserved

## Summary

This PR successfully transitions letter_name_registry from "created" to "consumed" and fixes critical registry documentation issues. However, it is **NOT** a complete Layer 2 source-of-truth enforcement. It is one step in a multi-PR journey toward full registry compliance.
