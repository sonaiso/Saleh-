# Dual-Path Constitutional Architecture

## بسم الله الرحمن الرحيم

## 0. Supreme Constitutional Principle

**الدستور له كل السلطة**
**The Constitution has all authority**

This project operates under a **unified constitutional framework** governing **two parallel, independent canonical paths**.

Both paths are:
- ✅ **Constitutionally licensed**
- ✅ **Canonical** (in src/qiyas_core/)
- ✅ **Governed by the same constitutional principles**
- ✅ **Subject to the same invariants and gates**

## 1. The Two Canonical Paths

### Path A: Atomic Layer Composition

**Architecture:**
```
TypedCodePoint
  → LetterIdentityCarrier (atomic proof)
  → HarakaFunctionCarrier (atomic proof)
  → PositionCarrier
  + AlignmentEvidence
  → SlotCandidate (meeting point of 4 ingredients)
  → Future: SyllableCandidate → ... (not yet implemented)
```

**Characteristics:**
- Parallel atomic identity proofs
- Explicit convergence at SlotCandidate
- Four required ingredients (LetterIdentity, HarakaFunction, Position, Alignment)
- Layer-by-layer composition
- Each layer proves its own domain transition

**Status:** Partially implemented (up to SlotCandidate)

**Location:**
- `src/qiyas_core/letter_identity_carrier.py`
- `src/qiyas_core/haraka_function_carrier.py`
- `src/qiyas_core/position_carrier.py`
- `src/qiyas_core/slot_adapter.py`

### Path B: SlotGeometry Construction

**Architecture:**
```
TypedCodePoint
  → SlotCandidate (single atomic slot)
  → SlotGeometry (geometric multi-slot sequence)
    - seed mode: initialize geometry from single slot
    - extend mode: grow geometry with binding evidence
  → SlotGeometryCandidate(length=n)
  → MinimalIndependentUnitReadiness (closure check)
```

**Characteristics:**
- Geometric sequence building
- Construction modes (seed/extend)
- Length-aware slot binding
- Explicit closure readiness checks
- Direct multi-slot modeling

**Status:** Implemented and tested

**Location:**
- `src/qiyas_core/slot_geometry_adapter.py`
- `src/qiyas_core/slot_geometry_closure_check.py`
- `src/qiyas_core/rules/slot_geometry_rules.py`

## 2. Constitutional Governance

Both paths are governed by the **same constitutional framework**:

### Shared Constitutional Documents
1. `PROJECT_MATHEMATICAL_FOUNDATION.md` - Mathematical invariants
2. `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` - Layer control
3. `LAYER_REGISTRY.md` - Single source of truth for all layers
4. `AGENT_PR_CHECKLIST.md` - Mandatory compliance checks

### Shared Invariants (from § 4 of CLAUDE.md)

Both paths MUST preserve:

1. Identity is not trace
2. Trace is not identity
3. Evidence may add trace but must not consume identity
4. Candidate identity must preserve source identities
5. Invalidating difference blocks licensing
6. Rank is computed by meet semantics
7. Residuals must not be hidden or silently discarded
8. Boundary and alignment evidence must not be collapsed into identity
9. Potential candidates must not become final judgments
10. No layer may produce the final output of a later layer without the required gate and evidence

### Shared Kernel

Both paths use the **same QiyasKernel** for validation:

```python
from qiyas_core.kernel import QiyasKernel

kernel = QiyasKernel()
result = kernel.validate(...)  # Same validation for both paths
```

The kernel enforces:
- Evidence-based validation (اصل، فرع، وصف، علة، وادي، فارق)
- Rank ceiling enforcement
- Forbidden output checking
- Residual preservation
- Trace/identity separation

## 3. Path Independence

### Separate Implementation Priorities

Each path has its own:
- Implementation roadmap
- Layer sequence
- Performance characteristics
- Use case optimization
- Testing strategy

### No Cross-Path Dependencies

```
❌ FORBIDDEN: Path A code depending on Path B implementation
❌ FORBIDDEN: Path B code depending on Path A implementation
✅ ALLOWED: Both paths depending on shared kernel/foundation
✅ ALLOWED: Comparative testing of results
```

### Comparison, Not Integration

**Allowed:**
```python
# Compare results from both paths
path_a_result = atomic_layer_pipeline(input)
path_b_result = slot_geometry_pipeline(input)

# Analyze differences
compare_results(path_a_result, path_b_result)
```

**Forbidden:**
```python
# Mixing paths in single pipeline
result = path_a_step1() + path_b_step2()  # ❌ FORBIDDEN
```

## 4. RESET_CONSTITUTION.md Clarification

**Previous Misinterpretation:**

RESET_CONSTITUTION.md § 7 was previously interpreted as:
> ❌ "SlotGeometry is prohibited and must be experimental-only"

**Correct Interpretation:**

RESET_CONSTITUTION.md § 7 means:
> ✅ "Before audit completes, do not adopt SlotGeometry **as the only canonical approach**"

The prohibition was against **abandoning the atomic layer approach** in favor of SlotGeometry, not against SlotGeometry itself.

**Resolution:**

Both approaches are canonical. The audit requirement is to:
1. Document both paths clearly ✅ (this document)
2. Ensure both are constitutional ✅ (same invariants, same kernel)
3. Prevent forced unification ✅ (independent paths)
4. Enable comparison ✅ (both produce comparable results)

## 5. Layer Registry Updates

### Path A Layers (LAYER_REGISTRY.md)

```
Layer 3.1: LetterIdentityCarrier (implemented)
Layer 3.2: HarakaFunctionCarrier (implemented)
Layer 3.3: PositionCarrier (implemented)
Layer 3.4: AlignmentEvidence (ConditionedTypedSequence)
Layer 3.5: SlotCandidate (meeting point)
```

### Path B Layers (LAYER_REGISTRY.md)

```
Layer 3: SlotCandidate (single atomic slot)
Layer 4-B: SlotGeometry (geometric multi-slot construction)
  - SlotGeometryCandidate(seed)
  - SlotGeometryCandidate(extend)
  - MinimalIndependentUnitReadiness (closure check)
```

Both registered in the same `LAYER_REGISTRY.md` under different branches.

## 6. Testing Strategy

### Independent Test Suites

**Path A Tests:**
- `test_letter_identity_carrier.py`
- `test_haraka_function.py`
- `test_position.py`
- `test_slot.py`

**Path B Tests:**
- `test_slot_geometry.py`
- `test_slot_geometry_closure_check.py`
- `test_slot_geometry_closure_contract.py`
- `test_slot_geometry_forbidden_outputs.py`

**Integration Tests:**
- `test_minimal_unit_readiness.py` (uses Path B for readiness checks)
- `test_variant_resolver_miu_integration.py` (uses Path B geometry)
- Future: `test_path_comparison.py` (compares Path A vs Path B results)

### Constitutional Tests

Both paths must pass:
- `test_forbidden_outputs.py`
- `test_formal_laws.py`
- `test_kernel_*.py` (all kernel enforcement tests)

## 7. Documentation Requirements

Every PR touching either path must declare:

```markdown
## Path Declaration
- [ ] Path A (atomic layer composition)
- [ ] Path B (SlotGeometry construction)
- [ ] Cross-path (affects both)
- [ ] Foundation (shared kernel/base)

## Constitutional Compliance
- [ ] Preserves all 10 invariants
- [ ] Uses QiyasKernel validation
- [ ] No cross-path dependencies
- [ ] Proper layer registration
```

## 8. Forbidden Actions

### ❌ Path Unification Without Approval

Do NOT:
- Force merge of Path A and Path B
- Declare one path "deprecated" without explicit maintainer approval
- Create hybrid layers mixing both approaches
- Remove either path from canonical status

### ❌ Path Hierarchy

Do NOT:
- Declare Path A "primary" and Path B "secondary"
- Declare Path B "experimental" and Path A "canonical"
- Prioritize one path's issues over the other's

### ❌ Cross-Path Coupling

Do NOT:
- Make Path A depend on Path B implementation
- Make Path B depend on Path A implementation
- Share mutable state between paths

## 9. Allowed Actions

### ✅ Independent Development

Each path may:
- Add new layers following its own sequence
- Optimize for its use cases
- Implement additional features
- Evolve its architecture independently

### ✅ Comparative Analysis

Developers may:
- Compare performance between paths
- Compare output quality between paths
- Study architectural trade-offs
- Recommend path choice for specific use cases

### ✅ Shared Foundation Enhancement

Both paths benefit from:
- QiyasKernel improvements
- Evidence system enhancements
- Rank computation refinements
- Registry system updates

## 10. Constitutional Authority Chain

```
Supreme: الدستور (Constitution)
  ├─ Shared: QiyasKernel, Evidence, Rank, Residual
  ├─ Path A: Atomic Layer Implementation
  └─ Path B: SlotGeometry Implementation

Both paths equal under constitution.
Neither path has authority over the other.
```

## 11. Future Evolution

### Path A Next Steps
- Complete ConditionedTypedSequence (AlignmentEvidence)
- Implement SyllableCandidate
- Build syllable composition layer
- Develop pronunciation layer

### Path B Next Steps
- Extend closure checks for complex geometries
- Add geometric transformation proofs
- Implement syllable-aware geometry
- Develop multi-word geometry sequences

### Convergence Points (Future)

Paths may converge at:
- **Syllable level** - both produce syllable candidates
- **Word level** - both produce word candidates
- **Meaning level** - both produce meaning candidates

But convergence is **optional**, not **mandatory**.

## 12. Maintainer Authority

Only the project maintainer (sonaiso) may:
- Declare one path deprecated
- Force path unification
- Change path priority
- Remove constitutional licensing from a path

Until such declaration, **both paths are equally canonical**.

---

## Summary

1. **Two paths, one constitution**
2. **Both canonical, both licensed**
3. **Independent implementation, shared governance**
4. **Comparison allowed, integration forbidden**
5. **الدستور له كل السلطة**

---

**Document Status:** Constitutional Architecture
**Authority Level:** Supreme (governs all qiyas_core paths)
**Effective Date:** 2026-06-06
**Supersedes:** Previous interpretations of RESET_CONSTITUTION.md § 7
