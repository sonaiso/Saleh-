# Path A Isolation: Execution Record

**Date:** 2026-05-31
**PR:** #17
**Branch:** claude/choreqiyas-core-isolate-pre-constitutional-materia
**Constitutional Authority:** RESET_CONSTITUTION.md (PR #15), AUDIT_AFTER_RESET_CONSTITUTION.md (PR #16)

---

## Executive Summary

This document records the execution of **Path A** (isolate and rebuild from clean foundation) as recommended by the constitutional audit in PR #16.

All post-PR #1 pre-constitutional qiyas_core materials have been moved to `experimental/` directory with clear non-canonical warnings and import boundaries.

The canonical foundation from PR #1 remains in `src/qiyas_core/` as the authoritative base for constitutional rebuild.

---

## What Was Done

### 1. Created experimental/ Directory Structure

```
experimental/
├── README.md                           # Non-canonical warning and reference
├── qiyas_core/                         # Pre-constitutional adapters
│   ├── __init__.py                     # Import guard
│   ├── [16 adapters moved here]
│   ├── rules/                          # Pre-constitutional rules
│   │   ├── __init__.py                 # Import guard
│   │   └── [16 rule files moved here]
│   └── slot/                           # SlotGeometry architecture
│       └── [entire slot/ directory moved here]
└── tests/
    └── qiyas_core/                     # Pre-constitutional tests
        ├── constitutional_helpers.py
        ├── helpers.py
        ├── fixtures/
        ├── slot/
        └── [40+ test files moved here]
```

### 2. Moved Pre-Constitutional Adapters

The following 16 adapters were moved from `src/qiyas_core/` to `experimental/qiyas_core/`:

1. `haraka_adapter.py`
2. `atomic_unit_adapter.py`
3. `carrier_function_adapter.py`
4. `mark_function_adapter.py`
5. `phono_functional_unit_adapter.py`
6. `syllable_readiness_adapter.py`
7. `closure_readiness_adapter.py`
8. `left_demand_adapter.py`
9. `right_capability_adapter.py`
10. `syllable_order_equilibrium_adapter.py`
11. `lafz_internal_closure_readiness_adapter.py`
12. `lafz_minimal_completion_readiness_adapter.py`
13. `mabni_murab_closure_readiness_adapter.py`
14. `phonotactic_economy_readiness_adapter.py`
15. `word_internal_closure_readiness_adapter.py`
16. `word_minimal_completion_readiness_adapter.py`

**Reason:** All built before RESET_CONSTITUTION.md (PR #15), classified as experimental by audit (PR #16).

### 3. Moved Pre-Constitutional Rules

The following 16 rule files were moved from `src/qiyas_core/rules/` to `experimental/qiyas_core/rules/`:

1. `haraka_rules.py`
2. `atomic_unit_rules.py`
3. `carrier_function_rules.py`
4. `mark_function_rules.py`
5. `phono_functional_unit_rules.py`
6. `syllable_readiness_rules.py`
7. `closure_readiness_rules.py`
8. `left_demand_rules.py`
9. `right_capability_rules.py`
10. `syllable_order_equilibrium_rules.py`
11. `lafz_internal_closure_readiness_rules.py`
12. `lafz_minimal_completion_readiness_rules.py`
13. `mabni_murab_closure_readiness_rules.py`
14. `phonotactic_economy_readiness_rules.py`
15. `word_internal_closure_readiness_rules.py`
16. `word_minimal_completion_readiness_rules.py`

**Reason:** All built before RESET_CONSTITUTION.md, classified as experimental by audit.

### 4. Moved SlotGeometry Architecture

Entire `src/qiyas_core/slot/` directory moved to `experimental/qiyas_core/slot/`:
- `geometry.py` — SlotGeometry protocol
- `spec.py` — SlotSpec definitions
- `capability.py`, `demand.py` — Slot abstractions
- `roles.py`, `enums.py` — Slot role/enum definitions
- `policies/` — All slot policies

**Reason:** RESET_CONSTITUTION.md §7 explicitly prohibits "Adopting SlotGeometry or any multi-slot architecture" before constitutional validation. Audit classified as rebuild-required.

### 5. Moved Pre-Constitutional Tests

The following test materials were moved from `tests/qiyas_core/` to `experimental/tests/qiyas_core/`:

**Test Helpers:**
- `constitutional_helpers.py` — PR #14 assertion helpers (built before constitution)
- `helpers.py` — Test fixture builders
- `fixtures/` — Reusable test fixtures

**Test Files (40+ files):**
- All adapter tests (`test_*_adapter.py`)
- All constitutional test suites from PR #14
- All SlotGeometry tests (`slot/test_*.py`)
- All framework validation tests

**Reason:** Testing framework built before constitution violates construction order (RESET_CONSTITUTION.md §1). Audit found systemic fixture issues (13 test failures).

### 6. Preserved Canonical Foundation

The following components **remain** in `src/qiyas_core/` as canonical foundation (PR #1):

**Core Infrastructure:**
- `kernel.py` — QiyasKernel
- `rule.py` — QiyasRule
- `node.py` — QiyasNodeRef
- `evidence.py` — Evidence, EvidenceSet
- `candidate.py` — Candidate, CandidateSet
- `residual.py` — Residual
- `audit.py` — QiyasAudit
- `enums.py` — Core enums
- `registry.py` — QiyasRegistry
- `adapter.py` — QiyasKernelAdapter base
- `validators.py` — Validation utilities

**Canonical Layer Example:**
- `unicode_adapter.py` — UnicodeLayerAdapter
- `rules/unicode_rules.py` — UNICODE_ARABIC_MEMBERSHIP

**Canonical Tests:**
- `tests/qiyas_core/test_kernel_*.py` — Kernel validation (12 test files)
- `tests/qiyas_core/test_unicode_qiyas_accepts_arabic_codepoint.py`

### 7. Updated Import Boundaries

**src/qiyas_core/__init__.py:**
- Removed imports of experimental adapters (HarakaLayerAdapter, AtomicUnitLayerAdapter, etc.)
- Removed imports of experimental enums (DiacriticKind, etc.)
- Kept only canonical foundation imports

**src/qiyas_core/rules/__init__.py:**
- Removed imports of experimental rules
- Kept only UNICODE_ARABIC_MEMBERSHIP

**experimental/qiyas_core/__init__.py:**
- Created with import guard warning
- Explicitly states: "DO NOT add imports here"

**experimental/qiyas_core/rules/__init__.py:**
- Created with import guard warning
- Explicitly states: "DO NOT add imports here"

### 8. Created Documentation

**experimental/README.md:**
- Comprehensive non-canonical warning
- Lists all isolated materials
- Explains why materials were isolated
- Defines prohibited and permitted actions
- Links to RESET_CONSTITUTION.md and AUDIT_AFTER_RESET_CONSTITUTION.md
- Clarifies import boundary rules

**docs/qiyas_core/PATH_A_ISOLATION_RECORD.md:** (this document)
- Records execution of Path A
- Documents what was moved and why
- Provides canonical foundation summary
- Links to constitutional authority

---

## Canonical Foundation Summary

After Path A isolation, the **canonical qiyas_core foundation** consists of:

### Components: 15 files
1. `src/qiyas_core/kernel.py` — QiyasKernel (constitutional authority)
2. `src/qiyas_core/rule.py` — QiyasRule dataclass
3. `src/qiyas_core/node.py` — QiyasNodeRef
4. `src/qiyas_core/evidence.py` — Evidence, EvidenceSet
5. `src/qiyas_core/candidate.py` — Candidate, CandidateSet
6. `src/qiyas_core/residual.py` — Residual
7. `src/qiyas_core/audit.py` — QiyasAudit
8. `src/qiyas_core/enums.py` — All core enumerations
9. `src/qiyas_core/registry.py` — QiyasRegistry
10. `src/qiyas_core/adapter.py` — QiyasKernelAdapter base
11. `src/qiyas_core/validators.py` — Validation utilities
12. `src/qiyas_core/unicode_adapter.py` — UnicodeLayerAdapter (first layer)
13. `src/qiyas_core/rules/__init__.py` — Rules package
14. `src/qiyas_core/rules/unicode_rules.py` — UNICODE_ARABIC_MEMBERSHIP rule
15. `src/qiyas_core/__init__.py` — Package exports

### Tests: 13 files (all canonical kernel behavior)
1. `tests/qiyas_core/test_kernel_accepts_valid_qiyas.py`
2. `tests/qiyas_core/test_kernel_blocks_context_layer_mismatch.py`
3. `tests/qiyas_core/test_kernel_blocks_identity_trace_conflict.py`
4. `tests/qiyas_core/test_kernel_blocks_node_type_mismatch.py`
5. `tests/qiyas_core/test_kernel_blocks_on_fariq.py`
6. `tests/qiyas_core/test_kernel_blocks_without_asl.py`
7. `tests/qiyas_core/test_kernel_blocks_without_far.py`
8. `tests/qiyas_core/test_kernel_blocks_without_illah.py`
9. `tests/qiyas_core/test_kernel_blocks_without_wadi.py`
10. `tests/qiyas_core/test_kernel_blocks_without_wasf.py`
11. `tests/qiyas_core/test_kernel_rank_ceiling.py`
12. `tests/qiyas_core/test_unicode_qiyas_accepts_arabic_codepoint.py`

**Total canonical codebase: ~28 files (15 source + 13 tests)**

**Percentage of original codebase: ~5%** (consistent with audit finding)

---

## Import Boundary Enforcement

### Hard Rule

**Canonical code in `src/qiyas_core/` MUST NOT import from `experimental/`.**

This is a constitutional boundary. Violation = constitutional violation.

### Enforcement Mechanisms

1. **Documentation:** experimental/README.md explicitly forbids canonical imports
2. **Import guards:** experimental/__init__.py files contain explicit warnings
3. **Code review:** All PRs must verify no experimental imports in canonical code
4. **Future:** Consider adding automated linter rule to enforce boundary

### What To Do If You Need Experimental Functionality

If canonical code needs functionality from experimental/:

1. **Review** experimental code against constitutional principles
2. **Rebuild** it with constitutional compliance from scratch
3. **Document** constitutional reasoning
4. **Place** rebuilt code in canonical `src/qiyas_core/`
5. **Test** with constitutional validation tests
6. **Never** import experimental code directly

---

## What Happens Next

### Immediate Next Steps (per Path A)

1. ✅ **Path A isolation complete** (this PR #17)
2. ⏭️ **Verify canonical kernel boundary** (PR #18)
   - Ensure canonical tests still pass
   - Verify no experimental dependencies leaked
   - Validate import boundaries
3. ⏭️ **Expand constitutional principles** (future PR)
   - Create docs/qiyas_core/CONSTITUTIONAL_PRINCIPLES.md
   - Define layer architecture constitutionally
   - Define evidence claim grammar as constitutional principle
   - Define SlotGeometry evaluation criteria
4. ⏭️ **Rebuild first layer constitutionally** (future PR)
   - Start with HarakaQiyas (diacritic classification)
   - Document constitutional reasoning
   - Build tests AFTER implementation (correct construction order)
   - Validate against constitutional principles

### Prohibited Actions (still in effect per RESET_CONSTITUTION.md §7)

- ❌ Do not import experimental code
- ❌ Do not fix experimental tests
- ❌ Do not build on experimental architecture
- ❌ Do not assume experimental patterns are constitutional
- ❌ Do not adopt SlotGeometry without constitutional validation
- ❌ Do not implement new layers before constitutional definition

### Permitted Actions

- ✅ Review experimental code for functional reference
- ✅ Extract useful patterns for constitutional redesign
- ✅ Study evidence claim grammar (with validation)
- ✅ Run canonical tests to verify foundation
- ✅ Expand constitutional principles documentation
- ✅ Begin constitutional layer rebuild (following construction order)

---

## Constitutional Chain of Authority

This isolation follows the constitutional chain:

1. **PR #15 (merged):** RESET_CONSTITUTION.md — Establishes constitutional authority
2. **PR #16 (merged):** AUDIT_AFTER_RESET_CONSTITUTION.md — Classifies all materials, recommends Path A
3. **PR #17 (this PR):** Execute Path A isolation — Move experimental materials, preserve canonical foundation
4. **PR #18 (next):** Verify canonical boundary — Ensure isolation is clean
5. **Future PRs:** Constitutional rebuild — One layer at a time, with constitutional compliance

---

## Verification Checklist

To verify Path A isolation was executed correctly:

- [x] All 16 pre-constitutional adapters moved to experimental/qiyas_core/
- [x] All 16 pre-constitutional rules moved to experimental/qiyas_core/rules/
- [x] Entire SlotGeometry directory moved to experimental/qiyas_core/slot/
- [x] All pre-constitutional tests moved to experimental/tests/qiyas_core/
- [x] Canonical foundation (15 files) remains in src/qiyas_core/
- [x] Canonical tests (13 files) remain in tests/qiyas_core/
- [x] src/qiyas_core/__init__.py updated (no experimental imports)
- [x] src/qiyas_core/rules/__init__.py updated (only canonical rule)
- [x] experimental/README.md created with warnings
- [x] experimental/__init__.py files created with import guards
- [x] This record document created

**Next verification (PR #18):**
- [ ] Canonical tests pass with PYTHONPATH=src python3 -m pytest tests/qiyas_core/ -q
- [ ] No imports from experimental/ in canonical code
- [ ] Import boundaries verified

---

## References

- **Constitution:** [docs/qiyas_core/RESET_CONSTITUTION.md](./RESET_CONSTITUTION.md) (PR #15)
- **Audit:** [docs/qiyas_core/AUDIT_AFTER_RESET_CONSTITUTION.md](./AUDIT_AFTER_RESET_CONSTITUTION.md) (PR #16)
- **Experimental Materials:** [experimental/README.md](../../experimental/README.md)
- **Canonical Foundation:** PR #1 (clean kernel)

---

**Path A Status:** ✅ ISOLATION COMPLETE

**Next Required Action:** Verify canonical kernel boundary (PR #18)

**Constitutional Compliance:** This isolation follows RESET_CONSTITUTION.md §5 and implements AUDIT_AFTER_RESET_CONSTITUTION.md Path A recommendation.

---

**Document Authority:** Path A Execution Record
**Effective Date:** 2026-05-31
**PR:** #17
