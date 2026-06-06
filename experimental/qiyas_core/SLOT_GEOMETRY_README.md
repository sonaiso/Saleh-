# SlotGeometry - Experimental Code

**Constitutional Status:** PROHIBITED in canonical src/ per RESET_CONSTITUTION.md §7

## Files Moved to experimental/

The following files were moved from `src/qiyas_core/` to `experimental/qiyas_core/`:

- `slot_geometry_adapter.py`
- `slot_geometry_closure_check.py`
- `rules/slot_geometry_rules.py`

Related test files moved to `experimental/tests/qiyas_core/`:

- `test_slot_geometry.py`
- `test_slot_geometry_closure_check.py`
- `test_slot_geometry_closure_contract.py`
- `test_slot_geometry_forbidden_outputs.py`

## Constitutional Basis

From RESET_CONSTITUTION.md § 7:

```
## 7. Prohibited Next Steps

**Before audit completes, the following actions are prohibited:**

- ❌ Adopting SlotGeometry or any multi-slot architecture
```

From LAYER_REGISTRY.md:

```
### Experimental: Old SlotGeometry Protocol

**Status:** experimental (isolated in PR #17)
**Constitutional Status:** RESET_CONSTITUTION.md §7 explicitly prohibits adopting SlotGeometry before constitutional validation
**Action:** Requires constitutional validation before canonical adoption. Do NOT copy to src/.
```

## Reason for Move

SlotGeometry was implemented in canonical src/ without completing:

1. Full Layer 2 (SifatVector, GlyphClassificationGate)
2. SyllableCandidate (Layer 4)
3. Constitutional validation

This violates the documented layer order and the explicit prohibition in governance documents.

## Usage

Code that needs SlotGeometry functionality should:

1. Import from experimental path (see test files for example)
2. Add clear documentation that it depends on experimental code
3. Plan migration when SlotGeometry receives constitutional approval

## Future Path

SlotGeometry may return to canonical status if:

1. Constitutional audit is completed
2. Required intermediate layers are implemented
3. Formal approval is granted by project maintainer
4. Governance documents are updated accordingly
