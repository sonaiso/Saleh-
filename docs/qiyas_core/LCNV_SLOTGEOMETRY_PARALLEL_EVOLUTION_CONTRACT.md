# LCNV-SLOTGEOMETRY PARALLEL EVOLUTION CONTRACT

> **عقد التطور المتوازي بين LCNV و SlotGeometry**
>
> **Parallel Evolution Contract Between LCNV and SlotGeometry**

---

## 0. Constitutional Authority

**This document establishes the constitutional framework for parallel evolution of LCNV (Track B) and SlotGeometry (Path B of Track A) while maintaining complete separation.**

**Authority:**
- Below: PROJECT_MATHEMATICAL_FOUNDATION.md (defines algebraic qiyas system)
- Below: CANONICAL_ARCHITECTURE_CONTROL_FRAME.md (defines layer architecture)
- Below: DUAL_PATH_CONSTITUTIONAL_ARCHITECTURE.md (defines dual-path governance)
- Below: LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md (defines LCNV laws)
- Below: LCNV_MINIMAL_RUNTIME_STABILIZATION_CLOSURE.md (closes LCNV for stabilization)
- Above: All future LCNV expansion proposals
- Above: All LCNV-SlotGeometry integration proposals

**Purpose:**
- Define how LCNV can evolve in parallel with SlotGeometry progress
- Prevent integration while allowing comparison
- Establish constitutional boundaries for parallel development
- Document conditions for opening deferred LCNV capabilities

**Why this document exists NOW:**

SlotGeometry is advancing (multi-slot construction, closure checks, MIU detection). LCNV is stable but minimal (MCLO-only encoding). This document establishes **how LCNV may evolve to encode SlotGeometry state WITHOUT integrating with SlotGeometry or becoming a source of truth**.

**The risk this prevents:**
```
❌ LCNV → SlotGeometry production (instead of encoding)
❌ SlotGeometry → LCNV dependency
❌ Track mixing/integration without approval
❌ LCNV becoming source instead of projection
❌ Unauthorized LCNV expansion
```

---

## 1. Supreme Principle

### المبدأ السامي

```
LCNV و SlotGeometry مساران منفصلان تحت دستور واحد.
التطور متوازٍ، ليس متكاملًا.
المقارنة مسموحة، التكامل ممنوع.
الدستور له كل السلطة.
```

**Translation:**

```
LCNV and SlotGeometry are separate paths under one constitution.
Evolution is parallel, not integrated.
Comparison is permitted, integration is forbidden.
The Constitution has all authority.
```

### Algebraic Formulation

```
SlotGeometry ≠ LCNV
SlotGeometry ∩ LCNV = ∅  (no shared runtime dependencies)
SlotGeometry ∥ LCNV      (parallel evolution)
Compare(SlotGeometry, LCNV) = ALLOWED
Integrate(SlotGeometry, LCNV) = FORBIDDEN (without explicit approval)
```

---

## 2. What "Parallel Evolution" Means

### Definition

**"Parallel Evolution" means:**

1. **LCNV develops capability to encode state AFTER SlotGeometry produces it**
   - SlotGeometry creates SlotCandidate → LCNV can encode that state
   - SlotGeometry creates SlotGeometry → LCNV can encode that state (if approved)
   - SlotGeometry creates MIU → LCNV can encode that state (if approved)

2. **LCNV does NOT produce SlotGeometry results itself**
   - LCNV does NOT create SlotCandidate
   - LCNV does NOT build SlotGeometry
   - LCNV does NOT determine closure
   - LCNV does NOT detect MIU

3. **Both paths preserve the same 10 invariants**
   - Identity ≠ trace
   - Candidate primacy
   - Rank meet semantics
   - Residual preservation
   - Gate-based licensing
   - No layer jumps
   - Potential-only candidates
   - Evidence-based transitions
   - Domain boundaries
   - Invalidating difference blocking

4. **Both paths use the same QiyasKernel**
   - Same evidence validation
   - Same rank calculation
   - Same residual handling
   - Same forbidden outputs
   - Same constitutional laws

### What "Parallel Evolution" Does NOT Mean

**"Parallel Evolution" does NOT mean:**

- ❌ LCNV replaces SlotGeometry
- ❌ LCNV integrates with SlotGeometry
- ❌ LCNV becomes source of truth for SlotGeometry
- ❌ SlotGeometry depends on LCNV
- ❌ Code sharing between paths
- ❌ Unified pipeline mixing both approaches
- ❌ LCNV → SlotGeometry production
- ❌ SlotGeometry → LCNV encoding requirement

---

## 3. Parallel Evolution Roadmap

### Current State (as of 2026-06-06)

| Component | SlotGeometry Status | LCNV Encoding Capability | Integration |
|-----------|-------------------|------------------------|-------------|
| **TypedCodePoint** | ✅ Implemented | ✅ Can encode (MCLO block) | ❌ Forbidden |
| **SlotCandidate** | ✅ Implemented | ✅ Can encode (MCLO block) | ❌ Forbidden |
| **SlotGeometry** | ✅ Implemented (seed/extend modes) | ⏸️ **Deferred** | ❌ Forbidden |
| **Closure Checks** | ✅ Implemented | ⏸️ **Deferred** | ❌ Forbidden |
| **MIU Detection** | ✅ Implemented | ⏸️ **Deferred** | ❌ Forbidden |
| **Syllable Geometry** | 📋 **Future** | 📋 **Future** | ❌ Forbidden |
| **Word Geometry** | 📋 **Future** | 📋 **Future** | ❌ Forbidden |

### Deferred Capabilities

**The following LCNV capabilities are DEFERRED pending maintainer approval:**

#### 1. Geometry State Encoding (Deferred)

**What it would encode:**
```python
# IF APPROVED:
geometry_state: GateState = CLOSED  # or positive int

# Encoding:
- slot_count: number of slots in geometry
- construction_mode: seed vs extend
- geometry_length: sequence length
- closure_readiness: boolean state

# NOT encoding:
- The actual SlotGeometry object
- Authority to produce SlotGeometry
- Geometric construction logic
```

**Opening conditions:**
1. ✅ SlotGeometry must be stable
2. ⏳ Maintainer explicit approval required
3. ⏳ Constitutional review required
4. ⏳ Track isolation verification required
5. ⏳ Forbidden operation audit required

**Tests required (if approved):**
```python
def test_geometry_encoding_does_not_produce_geometry():
    """Encoding geometry state does NOT produce SlotGeometry."""
    geometry = build_slot_geometry([slot1, slot2, slot3])  # Track A
    lcnv = pack_from_geometry(geometry)  # Track B encoding
    projection = unpack(lcnv)

    # Projection contains state, NOT SlotGeometry
    assert isinstance(projection, EncodedStateProjection)
    assert projection.geometry_state.slot_count == 3

    # FORBIDDEN: producing SlotGeometry from LCNV
    with pytest.raises(ForbiddenOutputError):
        projection.to_slot_geometry()

def test_cannot_encode_geometry_without_source():
    """Cannot encode geometry state without SlotGeometry source."""
    # This would be wrong:
    with pytest.raises(LCNVError):
        lcnv = pack_geometry_state(slot_count=3)  # no source

    # Must come from actual SlotGeometry:
    geometry = SlotGeometry(...)  # from Track A
    lcnv = pack_from_geometry(geometry)  # encode after production
```

#### 2. Closure State Encoding (Deferred)

**What it would encode:**
```python
# IF APPROVED:
closure_state: GateState = CLOSED  # or positive int

# Encoding:
- is_miu_ready: boolean
- closure_type: murab/mabni/waqf/continuation
- pending_dependencies: count

# NOT encoding:
- The actual closure determination
- Authority to declare closure
- MIU detection logic
```

**Opening conditions:**
1. ✅ MinimalIndependentUnitReadiness stable
2. ⏳ Constitutional boundary documented
3. ⏳ No integration with SlotGeometry
4. ⏳ Projection-only encoding verified
5. ⏳ Maintainer approval required

#### 3. Syllable/Word State Encoding (Future)

**Not planned until:**
- SlotGeometry extends to syllable/word levels
- Constitutional review complete
- Maintainer declares readiness
- Track isolation maintained

---

## 4. Constitutional Boundaries

### 4.1 Permanent Prohibitions

**LCNV is PERMANENTLY FORBIDDEN from:**

```
❌ LCNV → SlotGeometry production
❌ LCNV → SlotCandidate creation
❌ LCNV → Closure determination
❌ LCNV → MIU detection
❌ LCNV → Geometric construction
❌ LCNV replacing SlotGeometry as source
❌ SlotGeometry → LCNV runtime dependency
❌ Code imports between LCNV and SlotGeometry
❌ Shared state between tracks
❌ Integration without maintainer approval
```

**Reason:** LCNV is encoding/projection, NOT production/authority.

### 4.2 Permitted Operations

**LCNV is PERMITTED to:**

```
✅ Encode state AFTER SlotGeometry produces it
✅ Create EncodedStateProjection (not Candidate)
✅ Preserve gate/block structure
✅ Document parallel evolution
✅ Compare results with SlotGeometry (testing)
✅ Reference SlotGeometry in documentation
✅ Evolve independently within Track B
```

**Condition:** Must maintain track isolation.

### 4.3 SlotGeometry Independence

**SlotGeometry is INDEPENDENT and can:**

```
✅ Evolve freely without LCNV
✅ Add new construction modes
✅ Extend closure checks
✅ Implement syllable/word geometry
✅ Optimize performance
✅ Add new geometric proofs
✅ Never import LCNV
✅ Never depend on LCNV encoding
```

**SlotGeometry does NOT need LCNV approval or coordination.**

---

## 5. Track Isolation Laws

### Law 1: No Runtime Dependencies

```python
# src/qiyas_core/lcnv.py
# FORBIDDEN:
from qiyas_core.slot_geometry_adapter import SlotGeometry  # ❌

# ALLOWED:
# (no imports from slot_geometry_* files)
```

```python
# src/qiyas_core/slot_geometry_adapter.py
# FORBIDDEN:
from qiyas_core.lcnv import LCNV  # ❌

# ALLOWED:
# (no imports from lcnv.py)
```

**Enforcement:** Import guards in both files.

### Law 2: No Shared State

```
LCNV state ∩ SlotGeometry state = ∅

LCNV operates on EncodedStateProjection.
SlotGeometry operates on Candidate.
No shared mutable state.
```

### Law 3: Comparison-Only Testing

**Permitted:**
```python
# tests/qiyas_core/test_path_comparison.py

def test_compare_slot_geometry_vs_lcnv():
    """Compare SlotGeometry output with LCNV encoding (if implemented)."""

    # Path A (SlotGeometry): produces geometry
    geometry = build_slot_geometry([slot1, slot2, slot3])

    # Path B (LCNV): encodes geometry state (IF APPROVED)
    lcnv = pack_from_geometry(geometry)
    projection = unpack(lcnv)

    # Compare characteristics:
    assert geometry.slot_count == 3
    assert projection.geometry_state.slot_count == 3  # if implemented

    # CRITICAL: Projection ≠ Geometry
    assert projection != geometry
    assert not isinstance(projection, SlotGeometry)
```

**Forbidden:**
```python
# ❌ Integration test (forbidden):
def test_lcnv_produces_geometry():
    """FORBIDDEN: LCNV cannot produce SlotGeometry."""
    lcnv = create_lcnv(slot_count=3)
    geometry = lcnv.to_slot_geometry()  # ❌ FORBIDDEN
```

### Law 4: Documentation Cross-Reference Only

**Permitted:**
- Documenting that both paths exist
- Comparing architectural approaches
- Referencing constitutional boundaries
- Explaining track isolation

**Forbidden:**
- Recommending integration
- Suggesting one path replaces the other
- Claiming equivalence
- Mixing implementation guides

---

## 6. Opening Deferred Capabilities

### Constitutional Process

**To open any deferred LCNV capability:**

#### Phase 1: Prerequisites
1. ✅ Corresponding SlotGeometry feature must be stable
2. ✅ LCNV minimal runtime must remain stable
3. ✅ Track isolation must be verified
4. ✅ No integration proposals pending

#### Phase 2: Documentation
1. ⏳ Create constitutional contract document for new capability
2. ⏳ Document what it encodes vs. what it produces
3. ⏳ List forbidden operations explicitly
4. ⏳ Define opening conditions
5. ⏳ Submit docs-only PR for review

#### Phase 3: Maintainer Review
1. ⏳ Maintainer reviews constitutional contract
2. ⏳ Maintainer verifies track isolation
3. ⏳ Maintainer approves or defers
4. ⏳ If approved: proceed to implementation

#### Phase 4: Implementation (if approved)
1. ⏳ Implement encoding capability only
2. ⏳ Add forbidden operation guards
3. ⏳ Add constitutional tests
4. ⏳ Verify no SlotGeometry imports
5. ⏳ Submit implementation PR

#### Phase 5: Audit
1. ⏳ Verify track isolation maintained
2. ⏳ Verify no authority restoration
3. ⏳ Verify forbidden operations blocked
4. ⏳ Merge if all checks pass

### Example: Opening Geometry State Encoding

**IF maintainer approves geometry state encoding:**

```python
# STEP 1: Document contract (docs-only PR)
docs/qiyas_core/LCNV_GEOMETRY_STATE_ENCODING_CONTRACT.md

# STEP 2: Implement encoding (implementation PR)
# src/qiyas_core/lcnv.py

@dataclass(frozen=True)
class GateStateBundle:
    mclo: GateState = CLOSED
    lexical_only: GateState = CLOSED
    meaning_only: GateState = CLOSED
    binding: GateState = CLOSED
    mutabaqah: GateState = CLOSED
    tadammun: GateState = CLOSED
    iltizam: GateState = CLOSED
    rank_residual: GateState = CLOSED
    geometry_state: GateState = CLOSED  # NEW (if approved)
    semantic_force: str = field(default="FORBIDDEN", init=False)

# STEP 3: Add encoding function
def pack_from_geometry(geometry: SlotGeometry) -> LCNV:
    """
    Encode SlotGeometry state into LCNV.

    CRITICAL: This encodes STATE, not AUTHORITY.
    Unpack(Pack(geometry)) ≠ SlotGeometry
    Unpack(Pack(geometry)) = EncodedStateProjection
    """
    return LCNV(
        mclo=encode_slots(geometry.slots),
        geometry_state=encode_geometry_metadata(geometry),  # NEW
        rank_residual=encode_rank_residual(geometry),
    )

def encode_geometry_metadata(geometry: SlotGeometry) -> int:
    """Encode geometry metadata (slot count, mode, length)."""
    # Implementation details...
    return packed_metadata_int

# STEP 4: Add forbidden operation guard
@dataclass(frozen=True)
class EncodedStateProjection:
    geometry_state: Optional[GeometryStateProjection] = None

    def to_slot_geometry(self) -> Never:
        """FORBIDDEN: EncodedStateProjection cannot produce SlotGeometry."""
        raise ForbiddenOutputError(
            "EncodedStateProjection is state projection, not authority. "
            "Cannot produce SlotGeometry from LCNV encoding. "
            "SlotGeometry must be created through qiyas proof, not unpacking."
        )

# STEP 5: Add constitutional tests
def test_geometry_encoding_forbidden_operations():
    """Verify geometry encoding does not violate constitutional boundaries."""
    geometry = SlotGeometry(...)
    lcnv = pack_from_geometry(geometry)
    projection = unpack(lcnv)

    # Cannot produce SlotGeometry
    with pytest.raises(ForbiddenOutputError):
        projection.to_slot_geometry()

    # Cannot restore authority
    with pytest.raises(ForbiddenOutputError):
        projection.get_candidate_authority()

    # Projection ≠ Geometry
    assert projection != geometry
    assert not isinstance(projection, SlotGeometry)
```

---

## 7. Comparison Framework (Permitted)

### Architectural Comparison

**What can be compared:**

| Aspect | SlotGeometry (Track A) | LCNV (Track B) | Integration |
|--------|----------------------|----------------|-------------|
| **Purpose** | Geometric construction | State encoding | ❌ None |
| **Input** | TypedCodePoint/SlotCandidate | Candidate (any layer) | ❌ None |
| **Output** | SlotGeometry candidate | EncodedStateProjection | ❌ None |
| **Authority** | Full candidate authority | Projection only | ❌ None |
| **Source of truth** | Yes (creates structure) | No (encodes structure) | ❌ None |
| **Meaning production** | No (potential only) | No (forbidden) | ❌ None |
| **Track** | Track A Path B | Track B | ❌ Isolated |
| **QiyasKernel** | ✅ Uses | ✅ Uses | ✅ Shared |
| **Invariants** | ✅ All 10 | ✅ All 10 | ✅ Shared |
| **Dependencies** | Independent | Independent | ❌ None |

### Philosophical Comparison

**SlotGeometry approach:**
```
"Build geometric structure from atomic slots,
 license multi-slot sequences through construction modes,
 verify closure through readiness checks."
```

**LCNV approach:**
```
"Encode licensed layer state into reversible numeric form,
 preserve gate/block structure,
 enable state projection recovery (not authority restoration)."
```

**Relationship:**
```
SlotGeometry creates → LCNV may encode (if approved)
LCNV encodes → does NOT create SlotGeometry
Both preserve → same constitutional laws
Neither integrates → parallel evolution only
```

---

## 8. Maintainer Decision Framework

### Questions to Ask Before Opening LCNV Capability

**For maintainer review:**

1. **Is the SlotGeometry feature stable?**
   - ✅ Yes → can proceed to question 2
   - ❌ No → defer until stable

2. **Does LCNV encoding add value?**
   - What problem does encoding solve?
   - Is state projection needed for this feature?
   - Or is this premature optimization?

3. **Can track isolation be maintained?**
   - ✅ No runtime imports → can proceed
   - ❌ Requires imports → reject

4. **Is authority boundary clear?**
   - ✅ Encoding only, no production → can proceed
   - ❌ Might produce candidates → reject

5. **Are forbidden operations explicitly blocked?**
   - ✅ Guards in place → can proceed
   - ❌ No guards → require guards first

6. **Is there a valid use case?**
   - ✅ Specific need identified → can proceed
   - ❌ Speculative/premature → defer

7. **Is this the right time?**
   - Are other priorities more urgent?
   - Is LCNV expansion necessary now?
   - Or can it wait?

### Decision Tree

```
Is SlotGeometry stable?
  ├─ NO → DEFER
  └─ YES → Does encoding add value?
      ├─ NO → REJECT
      └─ YES → Can track isolation be maintained?
          ├─ NO → REJECT
          └─ YES → Is authority boundary clear?
              ├─ NO → REJECT
              └─ YES → Are forbidden operations blocked?
                  ├─ NO → REQUIRE GUARDS FIRST
                  └─ YES → Is there valid use case?
                      ├─ NO → DEFER
                      └─ YES → Is this the right time?
                          ├─ NO → DEFER
                          └─ YES → APPROVE with conditions
```

---

## 9. Forbidden Integration Patterns

### Pattern 1: LCNV → SlotGeometry Production

**FORBIDDEN:**
```python
def create_geometry_from_lcnv(lcnv: LCNV) -> SlotGeometry:
    """❌ FORBIDDEN: LCNV cannot produce SlotGeometry."""
    projection = unpack(lcnv)
    # ... somehow create SlotGeometry from projection
    return SlotGeometry(...)  # ❌ FORBIDDEN
```

**Why:** LCNV is projection, not source. SlotGeometry must come from qiyas proof.

### Pattern 2: SlotGeometry → LCNV Dependency

**FORBIDDEN:**
```python
# src/qiyas_core/slot_geometry_adapter.py
from qiyas_core.lcnv import LCNV  # ❌

class SlotGeometry:
    def encode(self) -> LCNV:  # ❌
        """❌ FORBIDDEN: SlotGeometry should not depend on LCNV."""
        return pack_from_geometry(self)
```

**Why:** SlotGeometry is independent. Must not depend on LCNV.

### Pattern 3: Unified Pipeline

**FORBIDDEN:**
```python
def process_input(text: str, use_lcnv: bool = False):
    """❌ FORBIDDEN: mixing tracks in one pipeline."""
    if use_lcnv:
        return lcnv_path(text)  # Track B
    else:
        return slot_geometry_path(text)  # Track A
```

**Why:** Tracks are parallel, not alternative implementations.

### Pattern 4: LCNV Authority Restoration

**FORBIDDEN:**
```python
def restore_geometry_from_lcnv(lcnv: LCNV) -> SlotGeometry:
    """❌ FORBIDDEN: LCNV cannot restore SlotGeometry authority."""
    projection = unpack(lcnv)
    # ... somehow restore full authority
    return authoritative_geometry  # ❌ FORBIDDEN
```

**Why:** Authority requires stores + validation, not just unpacking.

### Pattern 5: Track Optimization Through Mixing

**FORBIDDEN:**
```python
def optimize_with_lcnv(geometry: SlotGeometry) -> SlotGeometry:
    """❌ FORBIDDEN: using LCNV to optimize SlotGeometry."""
    lcnv = pack_from_geometry(geometry)
    # ... do some optimization on numeric encoding
    optimized = unpack_and_reconstruct(lcnv)  # ❌
    return optimized  # ❌ FORBIDDEN
```

**Why:** Each track must optimize independently.

---

## 10. Permitted Comparison Patterns

### Pattern 1: Test Comparison

**PERMITTED:**
```python
def test_compare_tracks():
    """✅ Compare SlotGeometry and LCNV characteristics."""

    # Track A produces geometry
    geometry = build_slot_geometry([slot1, slot2, slot3])

    # Track B encodes (if approved)
    lcnv = pack_from_geometry(geometry)
    projection = unpack(lcnv)

    # Compare metadata
    assert geometry.slot_count == projection.geometry_state.slot_count

    # Verify non-equivalence
    assert projection != geometry
```

### Pattern 2: Documentation Comparison

**PERMITTED:**
```markdown
## SlotGeometry vs LCNV

SlotGeometry creates geometric structure.
LCNV encodes state projection.

Both are canonical.
Both preserve invariants.
Neither integrates with the other.
```

### Pattern 3: Architectural Review

**PERMITTED:**
```python
def audit_track_isolation():
    """✅ Verify tracks remain isolated."""

    # Check no imports
    lcnv_imports = get_imports("src/qiyas_core/lcnv.py")
    assert "slot_geometry" not in lcnv_imports

    geometry_imports = get_imports("src/qiyas_core/slot_geometry_adapter.py")
    assert "lcnv" not in geometry_imports

    # Passes → tracks are isolated
```

---

## 11. Governance Summary

### Core Laws

```
1. LCNV and SlotGeometry are separate tracks under one constitution
2. Parallel evolution is permitted
3. Integration is forbidden (without explicit approval)
4. Track isolation must be maintained
5. LCNV encodes state, does not produce authority
6. SlotGeometry is independent of LCNV
7. Comparison is permitted, mixing is forbidden
8. Maintainer approval required for opening deferred capabilities
9. Constitutional review required for all expansions
10. Both tracks preserve all 10 invariants
```

### In Arabic

```
1. LCNV و SlotGeometry مساران منفصلان تحت دستور واحد
2. التطور المتوازي مسموح
3. التكامل ممنوع (بدون موافقة صريحة)
4. عزل المسارات واجب
5. LCNV يرمّز الحالة، لا ينتج السلطة
6. SlotGeometry مستقل عن LCNV
7. المقارنة مسموحة، الخلط ممنوع
8. موافقة المشرف مطلوبة لفتح القدرات المؤجلة
9. المراجعة الدستورية مطلوبة لكل توسع
10. كلا المسارين يحفظان الثوابت العشرة
```

---

## 12. Future Evolution Scenarios

### Scenario A: LCNV Remains Minimal

**If maintainer decides LCNV encoding is not needed:**

- ✅ LCNV stays at minimal runtime (MCLO-only)
- ✅ SlotGeometry continues evolving independently
- ✅ No geometry state encoding added
- ✅ Track isolation maintained automatically
- ✅ No constitutional risk

**Outcome:** Minimal maintenance, maximum simplicity.

### Scenario B: LCNV Expands Gradually

**If maintainer approves selective encoding:**

- ✅ Open geometry state encoding (Phase 1)
- ⏳ Wait for stability (Phase 2)
- ⏳ Open closure state encoding (Phase 3)
- ⏳ Wait for stability (Phase 4)
- ⏳ Evaluate syllable/word encoding (Phase 5)

**Outcome:** Gradual parallel evolution with checkpoints.

### Scenario C: LCNV Expansion Deferred Indefinitely

**If maintainer decides timing is not right:**

- ✅ LCNV remains closed for stabilization
- ✅ SlotGeometry evolves freely
- ✅ No geometry encoding implemented
- ✅ No timeline pressure on LCNV
- ✅ Reevaluate when conditions change

**Outcome:** SlotGeometry proceeds without LCNV dependency.

### Scenario D: Comparison Study

**If maintainer wants architectural comparison:**

- ✅ Document both approaches
- ✅ Compare characteristics (no code)
- ✅ Analyze trade-offs
- ✅ Make informed decision
- ✅ Proceed based on findings

**Outcome:** Evidence-based architectural decision.

---

## 13. Cross-References

### Constitutional Foundation
- `PROJECT_MATHEMATICAL_FOUNDATION.md` — algebraic qiyas system
- `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` — layer control
- `LAYER_REGISTRY.md` — single source of truth for layers

### Track-Specific Documents
- `DUAL_PATH_CONSTITUTIONAL_ARCHITECTURE.md` — dual-path governance
- `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md` — LCNV laws
- `LCNV_MINIMAL_RUNTIME_STABILIZATION_CLOSURE.md` — LCNV closure

### Implementation Files

**SlotGeometry (Track A):**
- `src/qiyas_core/slot_geometry_adapter.py`
- `src/qiyas_core/slot_geometry_closure_check.py`
- `src/qiyas_core/rules/slot_geometry_rules.py`
- `tests/qiyas_core/test_slot_geometry_*.py`

**LCNV (Track B):**
- `src/qiyas_core/lcnv.py`
- `tests/qiyas_core/test_lcnv_constitution.py`
- `tests/qiyas_core/test_lcnv_inverse_law_guard.py`

**No cross-imports permitted.**

---

## 14. Document Status

**Version:** 1.0
**Date:** 2026-06-06
**Status:** Constitutional contract document
**Authority:** Governs parallel evolution of LCNV and SlotGeometry

**Scope:**
- Defines parallel evolution framework
- Establishes track isolation laws
- Documents deferred capabilities
- Sets opening conditions
- Prevents unauthorized integration

**Changes from previous state:**
- NEW: Parallel evolution contract
- NEW: Opening conditions for deferred capabilities
- NEW: Forbidden integration patterns
- NEW: Maintainer decision framework
- NEW: Comparison framework

**Next steps:**
- Maintainer reviews contract
- Maintainer decides on deferred capabilities
- If approved: implement according to constitutional process
- If deferred: SlotGeometry continues independently

---

## 15. Final Law

```
التطور المتوازي مسموح.
التكامل ممنوع.
LCNV يرمّز، لا ينتج.
SlotGeometry ينتج، لا يرمّز.
العزل واجب.
الدستور حاكم.
```

**Translation:**

```
Parallel evolution is permitted.
Integration is forbidden.
LCNV encodes, does not produce.
SlotGeometry produces, does not encode.
Isolation is mandatory.
Constitution governs.
```

---

**الحمد لله رب العالمين**
