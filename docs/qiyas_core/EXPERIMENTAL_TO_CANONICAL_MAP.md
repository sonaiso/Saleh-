# EXPERIMENTAL TO CANONICAL MAP

> **Purpose:** Prevent accidental revival of pre-constitutional experimental components.
>
> **Authority:** This document maps experimental/ components to their canonical replacements or status.

---

## Overview

After PR #17 (Path A isolation), all pre-constitutional code was moved to `experimental/`. This document tracks:
1. What exists in experimental/
2. What canonical component replaced it (if any)
3. Whether it can be revived (and under what conditions)
4. What action to take when encountering it

---

## Mapping Table

| Experimental Component | Location | Canonical Replacement | Status | Action |
|----------------------|----------|---------------------|---------|---------|
| **AtomicUnitQiyas** | experimental/qiyas_core/atomic_unit_adapter.py | SlotCandidate (after alignment) | Replaced | ❌ Do NOT revive |
| **Old HarakaQiyas** | experimental/qiyas_core/haraka_adapter.py (old version) | HarakaFunctionCarrier | Rebuilt constitutionally | ❌ Do NOT copy old version |
| **CarrierFunctionQiyas** | experimental/qiyas_core/carrier_function_adapter.py | SlotCandidate composition | Replaced | ❌ Do NOT revive |
| **MarkFunctionQiyas** | experimental/qiyas_core/mark_function_adapter.py | SlotCandidate composition | Replaced | ❌ Do NOT revive |
| **PhonoFunctionalUnitQiyas** | experimental/qiyas_core/phono_functional_unit_adapter.py | SlotCandidate composition | Replaced | ❌ Do NOT revive |
| **SyllableReadinessQiyas** | experimental/qiyas_core/syllable_readiness_adapter.py | Future SyllableCandidate | Not canonical | ⚠️ Requires constitutional planning |
| **SlotGeometry Protocol** | experimental/qiyas_core/slot/geometry.py | None (deferred) | Not canonical | ⚠️ Requires constitutional validation |
| **SlotSpec** | experimental/qiyas_core/slot/spec.py | None (deferred) | Part of SlotGeometry | ⚠️ Requires constitutional validation |
| **SlotCapability** | experimental/qiyas_core/slot/capability.py | AlignmentEvidence / CarrierBindingCandidate | Replaced | ❌ Do NOT revive |
| **SlotDemand** | experimental/qiyas_core/slot/demand.py | AlignmentEvidence / CarrierBindingCandidate | Replaced | ❌ Do NOT revive |
| **SlotRoles** | experimental/qiyas_core/slot/roles.py | None (part of SlotGeometry) | Not canonical | ⚠️ Requires constitutional validation |
| **Slot Policies** | experimental/qiyas_core/slot/policies/*.py | Partially absorbed in QiyasKernel | Mixed | ⚠️ Selective extraction only |
| **LeftDemandQiyas** | experimental/qiyas_core/left_demand_adapter.py | AlignmentEvidence | Replaced | ❌ Do NOT revive |
| **RightCapabilityQiyas** | experimental/qiyas_core/right_capability_adapter.py | AlignmentEvidence | Replaced | ❌ Do NOT revive |
| **ClosureReadinessQiyas** | experimental/qiyas_core/closure_readiness_adapter.py | Future closure layer | Not canonical | ⚠️ Defer concept needs constitutional definition |
| **SyllableOrderEquilibriumQiyas** | experimental/qiyas_core/syllable_order_equilibrium_adapter.py | Future syllable layer | Not canonical | ⚠️ Equilibrium concept needs definition |
| **LafzInternalClosureReadinessQiyas** | experimental/qiyas_core/lafz_internal_closure_readiness_adapter.py | Future lafz layer | Not canonical | ⚠️ Lafz concept not defined |
| **LafzMinimalCompletionReadinessQiyas** | experimental/qiyas_core/lafz_minimal_completion_readiness_adapter.py | Future lafz layer | Not canonical | ⚠️ Lafz concept not defined |
| **MabniMurabClosureReadinessQiyas** | experimental/qiyas_core/mabni_murab_closure_readiness_adapter.py | Future grammatical layer | Not canonical | ⚠️ Grammatical concepts need grounding |
| **PhonotacticEconomyReadinessQiyas** | experimental/qiyas_core/phonotactic_economy_readiness_adapter.py | Future phonotactic layer | Not canonical | ⚠️ Economy principle needs definition |
| **WordInternalClosureReadinessQiyas** | experimental/qiyas_core/word_internal_closure_readiness_adapter.py | Future word layer | Not canonical | ⚠️ Word architecture not validated |
| **WordMinimalCompletionReadinessQiyas** | experimental/qiyas_core/word_minimal_completion_readiness_adapter.py | Future word layer | Not canonical | ⚠️ Word architecture not validated |
| **Constitutional helpers (PR #14)** | experimental/tests/qiyas_core/constitutional_helpers.py | Patterns extracted to constitutional docs | Reference only | ⚠️ Evidence grammar patterns valid, but test-before-constitution violates order |
| **Test fixtures (PR #14)** | experimental/tests/qiyas_core/fixtures/*.py | Rebuild with canonical layers | Deprecated | ❌ Do NOT copy (built on unconstitutional assumptions) |
| **Helpers (PR #14)** | experimental/tests/qiyas_core/helpers.py | Rebuild with canonical layers | Deprecated | ❌ Do NOT copy |

---

## Status Legend

| Symbol | Status | Meaning |
|--------|--------|---------|
| ❌ | Replaced / Deprecated | Do NOT revive. Canonical replacement exists. |
| ⚠️ | Deferred / Requires Validation | Do NOT use without constitutional planning/validation. |
| ✅ | Valid Reference | Can extract patterns after constitutional validation. |
| 🔄 | Partial Replacement | Some functionality replaced, some deferred. |

---

## Detailed Component Analysis

### AtomicUnitQiyas → SlotCandidate

**What it was:** Carrier + Mark binding layer.

**Why replaced:** Pre-constitutional architecture made assumptions about slot formation without separate letter identity, haraka function, position, and alignment proofs.

**Canonical replacement:** SlotCandidate after Layer 2A+2B+2C+2D composition.

**Action:** ❌ Do NOT revive AtomicUnitQiyas. Use SlotCandidate formation instead.

**Key difference:**
```python
# OLD (experimental):
AtomicUnitCandidate = carrier + mark

# NEW (canonical):
SlotCandidate = LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier + AlignmentEvidence
```

### PhonoFunctionalReadiness → Simpler Composition

**What it was:** Four-layer sublayer architecture (CarrierFunction, MarkFunction, PhonoFunctionalUnit, SyllableReadiness).

**Why replaced:** Over-engineered. The parallel proof architecture (Layer 2A/2B/2C/2D) is simpler and more constitutional.

**Canonical replacement:** SlotCandidate composition.

**Action:** ❌ Do NOT revive PhonoFunctionalReadiness sublayers.

**Key insight:** Atomic proofs (letter identity, haraka function) don't need intermediate "function" layers. They are already atomic.

### SlotGeometry → Deferred

**What it was:** Protocol-based slot abstraction (SlotGeometry, SlotSpec, policies, demand/capability).

**Why deferred:** Significant architectural commitment made before constitutional foundation. RESET_CONSTITUTION.md §7 explicitly prohibits adopting SlotGeometry before constitutional validation.

**Canonical replacement:** None yet. Deferred pending constitutional validation.

**Action:** ⚠️ Requires constitutional validation before canonical adoption. Do NOT copy to src/.

**Validation criteria (if/when evaluated):**
1. Does SlotGeometry align with layer sovereignty?
2. Does the protocol add constitutional value or complexity?
3. Can simpler slot formation achieve the same goals?
4. Does it preserve identity/trace separation?
5. Does it enforce forbidden outputs?

### Demand/Capability → AlignmentEvidence

**What it was:** Demand (left slot requirements) + Capability (right slot offerings) matching architecture.

**Why replaced:** Over-engineered. Alignment and carrier binding evidence are sufficient.

**Canonical replacement:** AlignmentEvidence / CarrierBindingCandidate in ConditionedTypedSequence.

**Action:** ❌ Do NOT revive demand/capability architecture.

**Key simplification:**
```python
# OLD (experimental):
LeftDemand.matches(RightCapability) → binding decision

# NEW (canonical):
CarrierBindingCandidate(letter_ref, haraka_ref, evidence, residuals, trace)
```

### Constitutional Helpers → Extract Patterns

**What it was:** PR #14 assertion helpers for evidence grammar, WadiGates, forbidden_outputs, rank, identity/trace.

**Why reference only:** Built testing framework BEFORE constitution (reversed construction order per RESET_CONSTITUTION.md §1).

**Valid patterns to extract:**
- Evidence claim grammar (اصل:, فرع:, وصف:, علة:, فارق:, وادي:)
- WadiGate completeness checking (all 6 gates required)
- Forbidden outputs discipline
- Rank meet semantics
- Identity/trace disjointness

**Action:** ✅ Extract patterns to constitutional documents, ❌ Do NOT copy helpers directly.

### Test Fixtures → Rebuild

**What it was:** PR #14 reusable test fixtures (candidates, evidence, nodes, requests, rules).

**Why deprecated:** Built on unconstitutional assumptions. PR #14's 13 test failures indicate fixture/schema inconsistency.

**Action:** ❌ Do NOT copy fixtures. Rebuild with canonical layers following constitutional patterns.

---

## Revival Decision Flow

When encountering an experimental component, use this flow:

```
1. Check this map: Is there a canonical replacement?
   → YES: Use canonical replacement. Do NOT revive experimental.
   → NO: Continue to 2.

2. Is the component marked "Replaced" or "Deprecated"?
   → YES: Do NOT revive. Architecture superseded.
   → NO: Continue to 3.

3. Is the component marked "Deferred" or "Requires Validation"?
   → YES: Requires constitutional planning before use.
           Open constitutional planning PR first.
   → NO: Continue to 4.

4. Is the component a pattern (not code)?
   → YES: Extract pattern after constitutional validation.
   → NO: Continue to 5.

5. Can the functionality be achieved by extending existing canonical layers?
   → YES: Extend canonical layer. Do NOT revive experimental.
   → NO: Continue to 6.

6. Is there constitutional basis for this layer?
   → YES: Rebuild constitutionally. Do NOT copy experimental.
   → NO: Propose constitutional amendment first.
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: "AtomicUnit looked good, let me copy it"

**Problem:** AtomicUnit was pre-constitutional. It made assumptions that violate current architecture.

**Correct action:** Use SlotCandidate formation from Layer 2 composition. Do NOT copy AtomicUnit.

### ❌ Mistake 2: "SlotGeometry protocol is well-designed, let me use it"

**Problem:** RESET_CONSTITUTION.md §7 explicitly prohibits adopting SlotGeometry before constitutional validation.

**Correct action:** Defer SlotGeometry. Use simpler slot formation for now. Propose constitutional validation PR if needed.

### ❌ Mistake 3: "Test fixtures exist, let me reuse them"

**Problem:** PR #14 fixtures were built on unconstitutional assumptions (13 test failures evidence).

**Correct action:** Rebuild fixtures with canonical layers. Do NOT copy experimental fixtures.

### ❌ Mistake 4: "Constitutional helpers have useful assertions"

**Problem:** Helpers are correct patterns but built in wrong order (tests before constitution).

**Correct action:** Extract patterns to constitutional documents. Do NOT copy helper code directly.

### ❌ Mistake 5: "Readiness concept seems useful"

**Problem:** "Readiness" was pre-constitutional concept. Not defined in LAYER_CONTRACT_CONSTITUTION.md.

**Correct action:** Define "readiness" constitutionally first, THEN implement. Do NOT revive experimental readiness layers.

---

## Pattern Extraction Guidelines

**When extracting patterns from experimental/, follow these rules:**

### ✅ Allowed Extraction (with validation):
1. Evidence claim grammar patterns (after constitutional validation)
2. Forbidden outputs discipline (architectural pattern)
3. WadiGate completeness checking (kernel requirement)
4. Identity/trace disjointness enforcement (algebraic invariant)
5. Rank meet semantics (meet = minimum, constitutional principle)

### ❌ Forbidden Extraction (architectural assumptions):
1. AtomicUnit architecture (replaced by SlotCandidate)
2. PhonoFunctionalReadiness sublayers (replaced by simpler composition)
3. Demand/capability matching (replaced by alignment evidence)
4. SlotGeometry protocol (requires constitutional validation)
5. Test fixtures (built on unconstitutional assumptions)

### ⚠️ Conditional Extraction (requires constitutional planning):
1. Readiness concepts (need constitutional definition first)
2. Closure concepts (need constitutional definition first)
3. Syllable concepts (need constitutional planning first)
4. Lafz/Word concepts (need constitutional architecture first)

---

## Integration with Other Documents

**CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 4:** This document implements the Experimental → Canonical Mapping section.

**LAYER_REGISTRY.md:** This document explains why experimental components are not in the canonical registry.

**NEXT_LAYER_DECISION_TREE.md:** This document informs decision point 6.7 (duplicate check).

**AGENT_PR_CHECKLIST.md:** This document supports checklist item "experimental boundary."

---

## Maintenance

**When an experimental component is promoted to canonical:**
1. Update this map: change status from "Deferred"/"Requires Validation" to "Rebuilt"
2. Document new canonical location
3. Update LAYER_REGISTRY.md with new canonical entry
4. Update CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 1.1
5. Do NOT delete experimental version (preserve historical record)

**When a new experimental component is added:**
1. Add entry to this map with "Experimental" status
2. Document why it is experimental (pre-constitutional, needs validation, exploratory)
3. Document what canonical component would replace it (if known)
4. Do NOT import in canonical code

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Active reference
