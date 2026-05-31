# experimental/

## ⚠️ NON-CANONICAL CODE - DO NOT IMPORT IN CANONICAL IMPLEMENTATIONS ⚠️

This directory contains **pre-constitutional qiyas_core materials** that were built before the establishment of the Reset Constitution (PR #15) and were classified as **experimental** or **rebuild-required** by the constitutional audit (PR #16).

## Status Classification

**All code in this directory is:**
- ❌ **Not canonical** — Does not serve as architectural authority
- ❌ **Not authoritative** — Cannot be cited as constitutional reference
- ❌ **Not for canonical imports** — Forbidden from import by canonical qiyas_core code
- ⚠️ **Pre-constitutional** — Built before constitutional foundation was established
- 📚 **Reference only** — May contain useful patterns but requires constitutional validation

## Constitutional Context

This isolation follows the **Path A** recommendation from the constitutional audit:

1. **Constitution established** (PR #15): docs/qiyas_core/RESET_CONSTITUTION.md
2. **Audit conducted** (PR #16): docs/qiyas_core/AUDIT_AFTER_RESET_CONSTITUTION.md
3. **Path A selected**: Isolate pre-constitutional materials and rebuild from canonical foundation
4. **This isolation** (PR #17): Move all post-PR #1 materials to experimental/

## What's Isolated Here

### Adapters (experimental/qiyas_core/)
All layer adapters except the canonical `unicode_adapter.py`:
- `haraka_adapter.py` — Diacritic classification
- `atomic_unit_adapter.py` — Carrier+mark binding
- `carrier_function_adapter.py` — Carrier function layer
- `mark_function_adapter.py` — Mark function layer
- `phono_functional_unit_adapter.py` — Phono-functional unit binding
- `syllable_readiness_adapter.py` — Syllable readiness validation
- `closure_readiness_adapter.py` — Closure readiness validation
- `left_demand_adapter.py` — Left demand (slot-based)
- `right_capability_adapter.py` — Right capability (slot-based)
- `syllable_order_equilibrium_adapter.py` — Syllable order equilibrium
- `lafz_internal_closure_readiness_adapter.py` — Lafz-level closure
- `lafz_minimal_completion_readiness_adapter.py` — Lafz-level completion
- `mabni_murab_closure_readiness_adapter.py` — Grammatical closure
- `phonotactic_economy_readiness_adapter.py` — Phonotactic economy
- `word_internal_closure_readiness_adapter.py` — Word-level closure
- `word_minimal_completion_readiness_adapter.py` — Word-level completion

### Rules (experimental/qiyas_core/rules/)
All rule definitions except the canonical `unicode_rules.py`:
- All corresponding `*_rules.py` files for the above adapters

### SlotGeometry Architecture (experimental/qiyas_core/slot/)
Complete slot-based abstraction framework (PR #13):
- `geometry.py` — SlotGeometry protocol
- `spec.py` — SlotSpec definitions
- `capability.py`, `demand.py` — Slot abstractions
- `roles.py`, `enums.py` — Slot role/enum definitions
- `policies/` — All slot policies (difference, closure, evidence, failure, residual, trace, wadi)

**Note:** RESET_CONSTITUTION.md §7 explicitly prohibits "Adopting SlotGeometry or any multi-slot architecture" before constitutional validation. SlotGeometry must be rebuilt from constitutional principles if approved.

### Tests (experimental/tests/qiyas_core/)
All test files except canonical kernel tests:
- `constitutional_helpers.py` — PR #14 assertion helpers (built before constitution)
- `helpers.py` — Test fixture builders
- `fixtures/` — Reusable test fixtures
- All adapter/layer test files
- All constitutional test suites from PR #14
- `slot/` — All SlotGeometry tests

## Canonical Foundation (Preserved in src/)

The following components remain in `src/qiyas_core/` as the **canonical foundation** from PR #1:

**Core Infrastructure:**
- `kernel.py` — QiyasKernel (constitutional authority)
- `rule.py` — QiyasRule dataclass
- `node.py` — QiyasNodeRef
- `evidence.py` — Evidence and EvidenceSet
- `candidate.py` — Candidate and CandidateSet
- `residual.py` — Residual effect model
- `audit.py` — QiyasAudit trail
- `enums.py` — Core enumerations
- `registry.py` — QiyasRegistry
- `adapter.py` — QiyasKernelAdapter base
- `validators.py` — Validation utilities

**Canonical Layer Example:**
- `unicode_adapter.py` — UnicodeLayerAdapter (first layer, PR #1)
- `rules/unicode_rules.py` — UNICODE_ARABIC_MEMBERSHIP rule

**Canonical Tests:**
- `tests/qiyas_core/test_kernel_*.py` — Kernel validation tests
- `tests/qiyas_core/test_unicode_qiyas_accepts_arabic_codepoint.py` — Unicode layer test

## Why These Materials Were Isolated

Per the constitutional audit findings:

1. **Construction order violation** — Code built before constitution established (Implementation → Tests → Constitution instead of Constitution → Audit → Implementation)
2. **Volume of pre-constitutional code** — 17 adapters + 17 rules + SlotGeometry + testing framework = ~95% of codebase
3. **SlotGeometry architectural assumption** — Significant architectural commitment made without constitutional validation
4. **PR #14 systemic issues** — 13 test failures indicate fixture assumptions inconsistent with implementation
5. **§7 violations** — Multiple prohibited actions occurred before constitution (adding adapters, building layers, expanding fixtures)

## What Happens Next

**Prohibited actions:**
- ❌ Do not import experimental code in canonical implementations
- ❌ Do not fix experimental tests or code
- ❌ Do not assume experimental patterns are constitutional
- ❌ Do not build on top of experimental architecture

**Permitted actions:**
- ✅ Review experimental code for functional reference
- ✅ Extract useful patterns for constitutional redesign
- ✅ Study evidence claim grammar patterns (with constitutional validation)
- ✅ Use as learning resource for what to avoid

**Next steps (per Path A):**
1. Expand constitutional principles (docs/qiyas_core/CONSTITUTIONAL_PRINCIPLES.md)
2. Rebuild layers one-by-one with constitutional compliance from inception
3. Document constitutional reasoning for each new layer
4. Build constitutional tests AFTER implementation (correct construction order)
5. Evaluate SlotGeometry constitutionally before re-adopting

## Import Boundary Guard

**All canonical qiyas_core code MUST NOT import from experimental/.**

This is a hard boundary. Violation of this boundary violates constitutional discipline.

If you need functionality from experimental/, you must:
1. Review it against constitutional principles
2. Rebuild it with constitutional compliance
3. Document constitutional reasoning
4. Place it in canonical src/qiyas_core/
5. Write constitutional validation tests

## References

- **Constitution:** docs/qiyas_core/RESET_CONSTITUTION.md (PR #15)
- **Audit Report:** docs/qiyas_core/AUDIT_AFTER_RESET_CONSTITUTION.md (PR #16)
- **Canonical Foundation:** PR #1 (clean kernel)
- **Path A Decision:** Audit §Final Recommendation

---

**This directory exists to preserve pre-constitutional work while ensuring it cannot contaminate the constitutional rebuild.**

**When in doubt, do not use experimental code. Rebuild constitutionally instead.**
