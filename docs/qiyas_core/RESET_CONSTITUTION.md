# qiyas_core Reset Constitution

## 0. Reset Declaration

**PR #14 is merged but non-authoritative.**

The repository is not constitutionally clean after PR #14.

PR #14 introduced a pytest constitutional inspection framework with test results showing 344/357 tests passing and 80/93 constitutional tests passing. While merged into main, this PR is **not accepted as the constitutional foundation** for qiyas_core.

The fundamental architectural error was building a testing framework before establishing the constitutional foundation itself. This reverses the proper order of construction.

## 1. Supreme Construction Order

The correct and only acceptable order of construction is:

1. **Constitution** — Establish constitutional principles and rules
2. **Audit** — Examine current repository state against constitution
3. **Classification** — Categorize existing code by constitutional status
4. **Rebuild/Isolation** — Either rebuild from clean foundation or isolate non-constitutional code
5. **Tests** — Create tests that validate constitutional compliance
6. **Implementation** — Build implementation layers

Any deviation from this order violates constitutional integrity.

## 2. Current Repository Status

**The current qiyas_core state is under audit.**

All existing code, tests, fixtures, helpers, adapters, and framework components must be audited against this Reset Constitution before:
- Being accepted as canonical
- Being used as foundation for new work
- Being referenced as architectural authority

## 3. No-Authority Rule

**No previous test/helper/fixture/framework is constitutional merely because it is merged.**

Merged status ≠ Constitutional authority
Passing tests ≠ Constitutional validity
Framework existence ≠ Architectural correctness

All merged code from PR #14 and earlier must prove constitutional compliance through audit, not assume it through merge history.

## 4. Experimental Isolation Rule

**Anything not proven constitutional must be moved to experimental or ignored during rebuild.**

Code classification after audit:
- **canonical** — Proven constitutionally compliant, forms foundation
- **experimental** — May be useful but not constitutional, isolated for reference
- **deprecated** — Must not be used, scheduled for removal
- **rebuild-required** — Must be reconstructed from constitutional principles

Until audit completes, all existing qiyas_core implementation is presumed experimental.

## 5. Clean PR-1 Rebuild Option

**If audit fails, rebuild qiyas_core from PR-1 clean kernel.**

If the audit determines that existing code cannot be salvaged or constitutionally classified without excessive remediation, the repository retains the option to:

1. Isolate all post-PR-1 code as `experimental/`
2. Rebuild qiyas_core from the clean kernel foundation (PR #1)
3. Re-implement each layer with constitutional compliance from inception

This is not failure; this is constitutional discipline.

## 6. Audit Categories

The post-constitution audit must classify every file, function, test, and helper into exactly one category:

### canonical
Code that is:
- Constitutionally compliant in structure and intent
- Properly documented with constitutional reasoning
- Tested with constitutional validation
- Safe to use as foundation for future work

### experimental
Code that is:
- Potentially useful but not constitutionally validated
- Kept for reference or future constitutional redesign
- Isolated from canonical implementation paths
- Not imported or depended upon by canonical code

### deprecated
Code that is:
- Constitutionally incompatible
- Not salvageable through refactoring
- Scheduled for removal after audit
- Prohibited from use in any new work

### rebuild-required
Code that:
- Implements necessary functionality
- Uses unconstitutional architecture
- Must be rebuilt from scratch with constitutional design
- Serves as functional reference only

## 7. Prohibited Next Steps

**Before audit completes, the following actions are prohibited:**

- ❌ Adding adapters to qiyas_core
- ❌ Adopting SlotGeometry or any multi-slot architecture
- ❌ Building new qiyas layers (SyllableQiyas, PronunciationQiyas, etc.)
- ❌ Fixing PR #14 test failures
- ❌ Expanding test fixtures or helpers
- ❌ Implementing new rules or validators
- ❌ Refactoring existing qiyas_core code
- ❌ Assuming any previous work is canonical

## 8. Required Next Step

**Open repository audit issue or PR after this document.**

The immediate next action is to create a comprehensive audit that:

1. Reviews all existing qiyas_core code against constitutional principles
2. Classifies each component into: canonical, experimental, deprecated, or rebuild-required
3. Produces an audit report (not implementation code)
4. Recommends either:
   - Path A: Isolate experimental work and rebuild from clean foundation
   - Path B: Salvage and remediate constitutional violations in existing code

Only after audit completion and path decision can implementation resume.

## 9. Constitutional Principles (Summary)

The constitution itself must be defined, but key principles include:

- **Layer sovereignty** — Each qiyas layer has clear boundaries and responsibilities
- **Evidence-based validation** — All claims require explicit evidence chains
- **Forbidden outputs** — Each layer prohibits outputs beyond its responsibility
- **Deferred states** — Incomplete validation emits deferral, not failure
- **Canonical kernel** — QiyasKernel is the authoritative validator

These principles must be expanded into full constitutional documentation in subsequent work.

## 10. Relationship to PR #14

PR #14 status: `merged but non-authoritative inspection framework`

PR #14 is now classified as:
- Audit subject (not audit authority)
- Post-merge review target (not foundation)
- Framework experiment (not constitutional framework)

PR #14's test results (80/93 constitutional tests passing with 13 failures) indicate that the framework itself was built on unconstitutional assumptions about fixtures, helpers, and layer architecture.

Do not fix PR #14. Audit it.

---

## Summary

**No implementation work continues until:**
1. This Reset Constitution is accepted
2. Repository audit is completed
3. Code is classified (canonical/experimental/deprecated/rebuild)
4. Clean rebuild path is chosen (if necessary)

**The constitution comes first. Always.**

---

**Document Status:** Reset Constitution
**Authority Level:** Supreme (governs all qiyas_core work)
**Next Action Required:** Comprehensive repository audit
