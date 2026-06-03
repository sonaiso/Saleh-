# PR_1_49_AUTHORITY_AUDIT.md

## Document Authority

**Status**: CONSTITUTIONAL
**Authority**: MANDATORY
**Scope**: All PRs #1-49 and future PR governance
**Effective**: Immediately upon merge
**Purpose**: Prevent unsynchronized constitutional/executable/planning authorities

---

## 0. The Systemic Problem Identified

### 0.1 The Pattern

Between PR #1 and PR #49, a dangerous pattern emerged multiple times:

1. **Constitutional documents** created with **binding authority** over future runtime
2. Documents reference **future PRs by number** (e.g., "PR #45 will...")
3. **Actual PRs diverge** from the documented plan
4. **No mechanism prevents** outdated constitutional text from remaining authoritative
5. **Result**: Constitutional documents with binding authority contain false promises and unsafe formulations

### 0.2 Historical Evidence

**PR #16-18: First Recognition**
- PR #16 acknowledged that **95% of code** was built **before constitutional foundation**
- Solution: Move all post-PR #1 code to `experimental/`
- This proves the project **already knew** this pattern was dangerous

**PR #44: Pattern Returned**
- Created constitutional LCNV document while Layer 2 still unstable (PR #42-43 were fixing glyph gate/residuals)
- Claimed binding authority over "all numeric encoding implementations"
- **Promised "PR #45 would constrain inverse/logarithmic law"**
- **Reality: PR #45 is actually "CTS consumes tokenizer evidence (Z3)"**
- Dangerous formulation `Unpack(Pack(x)) = x` remained uncorrected

### 0.3 The Three Unsynchronized Authorities

1. **QiyasKernel** (actual executable authority in `src/qiyas_core/`)
2. **Constitutional docs** (claimed binding authority in `docs/qiyas_core/`)
3. **PR sequencing** (promised future constraints, often unfulfilled)

When these diverge without guards, the system has no protection against:
- Outdated constitutional text remaining authoritative
- Future implementation following broken laws
- "Docs-only" PRs having runtime impact through binding authority

---

## 1. PR #1-49 Classification

### 1.1 Classification Categories

Each PR is classified as:

1. **Executable Canonical** — Code in `src/qiyas_core/`, merged, active
2. **Constitutional Binding** — Docs with binding authority over runtime
3. **Planning Only** — Docs without binding authority, speculative
4. **Experimental** — Code in `experimental/`, non-authoritative
5. **Superseded/Corrected** — Replaced by later PRs
6. **Mismatch/Needs Correction** — Authority claim doesn't match reality

### 1.2 Full PR Audit

**PR #1: QiyasKernel Foundation**
- **Classification**: Executable Canonical
- **Authority**: BINDING (defines kernel contract)
- **Status**: Active, correct
- **Note**: Established QiyasNodeRef, Evidence, Residual, QiyasRule, Candidate, CandidateSet, six wadi checks

**PR #2: Kernel Hardening**
- **Classification**: Executable Canonical
- **Authority**: BINDING (enforces six wadi gates, identity/trace separation)
- **Status**: Active, correct

**PR #3-14: Pre-Constitutional Expansion**
- **Classification**: Experimental (moved by PR #17)
- **Authority**: NON-BINDING (pre-dated constitutional foundation)
- **Status**: Correctly isolated to `experimental/`
- **Note**: Unicode, Haraka, AtomicUnit, SlotGeometry, test framework — all built before constitution

**PR #15: Constitutional Sequence Recognition**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (declared correct sequence: constitution → implementation → tests)
- **Status**: Active, correct
- **Danger Identified**: PR #14 was non-authoritative, implementation-before-constitution is forbidden

**PR #16: Authority Debt Audit**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (acknowledged 95% of code pre-dated constitution)
- **Status**: Active, correct
- **Critical Finding**: "95% of code built before constitutional foundation"
- **Decision**: Path A — isolate all post-PR #1 to `experimental/`

**PR #17: Isolation Execution**
- **Classification**: Executable Canonical
- **Authority**: BINDING (executed Path A isolation)
- **Status**: Active, correct
- **Result**: Moved 16 adapters, 16 rules, SlotGeometry, tests to `experimental/`

**PR #18: Boundary Verification**
- **Classification**: Executable Canonical
- **Authority**: BINDING (verified canonical kernel = 15 files only)
- **Status**: Active, correct

**PR #19: Kernel Identity Documentation**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (defined kernel as algebraic core, not complete Arabic layers)
- **Status**: Active, correct

**PR #20: (Not Found or Skipped)**
- **Classification**: N/A
- **Status**: N/A

**PR #21: Pytest Scope Constraint**
- **Classification**: Executable Canonical
- **Authority**: BINDING (restricts pytest to `tests/` only, excludes experimental)
- **Status**: Active, correct

**PR #22: TypedCodePoint Classification**
- **Classification**: Executable Canonical
- **Authority**: BINDING (rebuilt TypedCodePoint with constitutional compliance)
- **Status**: Active, correct

**PR #23: Type Proof Hardening**
- **Classification**: Executable Canonical
- **Authority**: BINDING (added wasf/illah/fariq to prove types within kernel)
- **Status**: Active, correct

**PR #24: Gap Documentation**
- **Classification**: Constitutional Binding
- **Authority**: PLANNING (697 lines, 16 gaps, Phase roadmap)
- **Status**: Speculative, non-binding
- **Note**: Large doc before implementation complete — early warning sign

**PR #25: Large Layer 2 Implementation**
- **Classification**: Executable Canonical
- **Authority**: BINDING (TypedCodePoint → LetterIdentity → HarakaFunction → Position → SlotCandidate)
- **Status**: Active, but...
- **Warning**: 4548 additions in 22 files — large implementation

**PR #26: Architecture Correction**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (corrected PR #25 to parallel proofs, not linear chain)
- **Status**: Active, correct
- **Critical**: Prevented illegal linearization of identity proofs

**PR #27: Layer 2 Minimal Slice Declaration**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (Layer 1 = pure identity, Layer 2 = coordinate enrichment, minimal slice only)
- **Status**: Active, correct
- **Warning**: Declared Layer 2 incomplete

**PR #28: CTS and Recursion**
- **Classification**: Executable Canonical
- **Authority**: BINDING (CTS, Slot alignment, recursion closure, run_qiyas wiring)
- **Status**: Active, correct
- **Note**: 4017 additions — large integration

**PR #29-30: (Not Found or Skipped)**
- **Classification**: N/A
- **Status**: N/A

**PR #31: Layer 2 Evidence Format Fix**
- **Classification**: Executable Canonical
- **Authority**: BINDING (fixed 7 Layer 2 test failures from PR #27)
- **Status**: Active, correct
- **Critical**: Layer 2 was still being fixed when PR #44 introduced LCNV

**PR #32: Massive Governance Documentation**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (12 docs, 7325 lines, including PROJECT_MATHEMATICAL_FOUNDATION)
- **Status**: Active, correct
- **Governing Law**: "DO NOT CREATE NAMES. PROVE TRANSITIONS."

**PR #33-34: Doc-Code Drift Correction**
- **Classification**: Executable Canonical
- **Authority**: BINDING (fixed non-existent paths, wrong APIs, Abjad status)
- **Status**: Active, correct
- **Critical Evidence**: Docs had drifted from code — proves docs need guards

**PR #35: (Not Found or Skipped)**
- **Classification**: N/A
- **Status**: N/A

**PR #36: Source-of-Truth Registries**
- **Classification**: Executable Canonical
- **Authority**: BINDING (letter, glyph, fariq registries)
- **Status**: Active, correct

**PR #37: Evidence Namespace Fix**
- **Classification**: Executable Canonical
- **Authority**: BINDING (fixed adapter to use Arabic evidence names)
- **Status**: Active, correct

**PR #38-39: Fariq Registry Integration**
- **Classification**: Executable Canonical
- **Authority**: BINDING (connected fariq to registry)
- **Status**: Active, correct

**PR #40-41: (Not Found or Skipped)**
- **Classification**: N/A
- **Status**: N/A

**PR #42: Glyph Classification Gate**
- **Classification**: Executable Canonical
- **Authority**: BINDING (glyph gate before coordinate enrichment)
- **Status**: Active, correct
- **Critical**: Layer 2 still being closed when PR #44 opened

**PR #43: Residual Glyph Failures**
- **Classification**: Executable Canonical
- **Authority**: BINDING (glyph failures produce residuals)
- **Status**: Active, correct
- **Critical**: Layer 2 stabilization ongoing

**PR #44: LCNV Architecture — BINDING BUT NEEDS CORRECTION**
- **Classification**: Constitutional Binding
- **Authority**: BINDING (claims authority over "all numeric encoding implementations")
- **Status**: **MISMATCH/NEEDS CORRECTION**
- **Dangerous Formulation**: `Unpack(Pack(x)) = x` and `Unpack(LCNV(c)) = c`
- **False Promise**: "PR #45 will constrain inverse/logarithmic law"
- **Reality**: PR #45 is actually CTS tokenizer evidence (Z3)
- **Constitutional Violation**: Creates internal contradiction with Candidate primacy
- **Timing Error**: Introduced while Layer 2 incomplete (PRs #42-43 still closing)
- **Correction Required**: See INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md

**PR #45: CTS Consumes Tokenizer Evidence (Z3) — NOT INVERSE LAW**
- **Classification**: Executable Canonical
- **Authority**: BINDING (CTS tokenizer integration)
- **Status**: Active, correct
- **Critical Mismatch**: PR #44 promised "PR #45 = inverse law" but reality = tokenizer
- **Governance Failure**: No mechanism prevented false future PR reference in #44

**PR #46-49: Tokenizer/Boundary Pipeline**
- **Classification**: Executable Canonical
- **Authority**: BINDING (Z4/Z5 tokenizer/boundary integration)
- **Status**: Active, correct
- **Note**: All in tokenizer/boundary track, none in LCNV/inverse track

---

## 2. Constitutional Violations Identified

### 2.1 Violation 1: Unguarded Constitutional Authority (PR #44)

**Document**: `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md`

**Claim**: "This document has constitutional authority over all numeric encoding implementations"

**Problem**: Document is "docs-only" but claims binding runtime authority

**Unsafe Formulation**:
```
Unpack(Pack(x)) = x
∀ candidate c: Unpack(LCNV(c)) = c
```

**Constitutional Conflict**: Violates Candidate primacy (Candidate = source of truth, LCNV = encoding only)

**No Guard**: No test prevents this formulation from remaining or returning

**Status**: **NEEDS CORRECTION** (see PR #50 component B)

### 2.2 Violation 2: False Future PR Reference (PR #44)

**Document**: `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md` § 10

**Claim**: References "INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md (PR #45)"

**Reality**: PR #45 = "CTS consumes tokenizer evidence (Z3)", not inverse law

**Problem**: Constitutional doc referenced non-existent future PR by number

**No Verification**: No mechanism checked whether PR #45 matched the promise

**Status**: **NEEDS CORRECTION** (see PR #50 component A)

### 2.3 Violation 3: Doc-Code Drift (PR #33-34)

**Evidence**: PR #33-34 had to fix:
- Non-existent file paths
- Wrong API names
- Incorrect status claims

**Problem**: Constitutional docs referenced APIs that didn't exist

**Pattern**: Same as PR #44 — docs with authority drifting from reality

**Status**: **FIXED** in PR #33-34, but **PATTERN RETURNED** in PR #44

---

## 3. Governing Laws to Prevent Recurrence

### 3.1 Law 1: No Authoritative Document Without Guard

**Arabic**: لا وثيقة سلطوية بلا حارس

**Rule**:
```
∀ document d where Authority(d) = BINDING:
  ∃ test t where Guards(t, d) = TRUE

Guard test must:
  1. Verify formulations are constitutionally safe
  2. Verify referenced files/APIs exist
  3. Verify referenced PRs match their claims
  4. Fail if dangerous patterns return
```

**Enforcement**: PR #50 adds `test_constitutional_doc_safety.py`

### 3.2 Law 2: No Future PR Reference Without Verification

**Rule**:
```
∀ document d, ∀ claim c in d:
  IF c = "PR #X will Y"
  THEN:
    - PR #X must be open OR
    - PR #X must be merged with title matching Y OR
    - Claim must be marked SPECULATIVE/NON-BINDING

FORBIDDEN:
  - "PR #45 will fix inverse law" when PR #45 doesn't exist yet
  - Leaving such claims after PR #45 merges with different content
```

**Enforcement**: This audit document + guard tests

### 3.3 Law 3: Separate Encoding Authority from Candidate Authority

**Rule**:
```
EncodedStateProjection ≠ CandidateAuthority

LCNV provides: EncodedCandidateStateProjection (gate states only)
Stores provide: CandidateAuthority (identity + evidence + trace)

FORBIDDEN:
  Unpack(LCNV(c)) = c  (implies LCNV has candidate authority)

REQUIRED:
  Unpack(LCNV(c)) = EncodedCandidateStateProjection(c)
  ReconstructCandidate(projection, stores) = c
```

**Enforcement**: PR #50 component B (INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md)

### 3.4 Law 4: Constitution Before Implementation

**Rule**:
```
∀ layer L:
  ConstitutionalContract(L) MUST precede ExecutableImplementation(L)

FORBIDDEN:
  - Implementation → Constitution (creates constitutional debt)
  - Implementation → Tests → Constitution (PR #15 violation)

REQUIRED:
  - Constitution → Implementation → Tests
```

**Historical Compliance**:
- ✗ PR #1-14: Implementation before constitution (corrected by PR #16-18)
- ✓ PR #19+: Constitution first
- ⚠ PR #44: Constitutional doc while Layer 2 incomplete

### 3.5 Law 5: Docs-Only ≠ Safe When Authority is Binding

**Rule**:
```
IF document.authority = BINDING
THEN document.safety ≠ guaranteed_by(docs_only_flag)

"Docs-only" means:
  - No runtime code changed

"Docs-only" does NOT mean:
  - No runtime impact
  - No constitutional authority
  - No need for guards

BINDING docs shape future runtime.
BINDING docs require guards even without current runtime.
```

**Application to PR #44**:
- ✓ PR #44 is docs-only (no code changed)
- ✗ PR #44 is NOT safe (claims binding authority, has unsafe formulation)
- ✗ PR #44 had NO guards (no tests prevent regression)

---

## 4. Required Corrections

### 4.1 Immediate (PR #50)

**A. Fix LCNV Inverse Law**
- Document: `INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md` (NEW)
- Action: Replace `Unpack(Pack(x)) = x` with projection formulation
- Action: Require stores for full Candidate reconstruction
- Action: Define logarithmic measurement constraints

**B. Amend LCNV Architecture**
- Document: `LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md`
- Action: Replace Law 1 with corrected formulation
- Action: Remove false "PR #45" reference
- Action: Add reference to governing law document

**C. Add Guard Tests**
- File: `tests/qiyas_core/test_constitutional_doc_safety.py` (NEW)
- Action: Test LCNV doc doesn't contain forbidden formulations
- Action: Test required safe formulations are present
- Action: Prevent regression

**D. This Audit Document**
- File: `PR_1_49_AUTHORITY_AUDIT.md` (THIS FILE)
- Action: Classify all PRs #1-49
- Action: Identify constitutional violations
- Action: Establish governing laws

### 4.2 Future (Post-PR #50)

**Before Any LCNV Runtime**:
1. ✓ PR #50 merged (constitutional correction)
2. ✓ Guard tests passing
3. ✓ Stores architecture defined (CandidateStore, EvidenceStore, TraceStore)
4. ✓ EncodedCandidateStateProjection implemented
5. ✓ GateStateBundle implemented
6. THEN: LCNV Pack/Unpack implementation permitted

**Before Any MCLO Prototype**:
1. ✓ All "Before LCNV Runtime" requirements
2. ✓ SignifierOnlyValue constraints verified
3. ✓ Abjad semantic_force=FORBIDDEN verified
4. THEN: MCLO prototype permitted

---

## 5. PR Classification Summary Table

| PR # | Type | Authority | Status | Notes |
|------|------|-----------|--------|-------|
| #1 | Executable | BINDING | ✓ Active | Kernel foundation |
| #2 | Executable | BINDING | ✓ Active | Kernel hardening |
| #3-14 | Experimental | NON-BINDING | ✓ Isolated | Pre-constitutional |
| #15 | Constitutional | BINDING | ✓ Active | Sequence law |
| #16 | Constitutional | BINDING | ✓ Active | 95% debt audit |
| #17 | Executable | BINDING | ✓ Active | Isolation execution |
| #18 | Executable | BINDING | ✓ Active | Boundary verification |
| #19 | Constitutional | BINDING | ✓ Active | Kernel identity |
| #21 | Executable | BINDING | ✓ Active | Pytest scope |
| #22-23 | Executable | BINDING | ✓ Active | TypedCodePoint |
| #24 | Constitutional | PLANNING | ~ Speculative | Gap doc |
| #25-28 | Executable | BINDING | ✓ Active | Layer 2 impl |
| #31 | Executable | BINDING | ✓ Active | Layer 2 fixes |
| #32 | Constitutional | BINDING | ✓ Active | Massive governance |
| #33-34 | Executable | BINDING | ✓ Active | Doc drift fix |
| #36-39 | Executable | BINDING | ✓ Active | Registries |
| #42-43 | Executable | BINDING | ✓ Active | Glyph gate/residuals |
| #44 | Constitutional | BINDING | **✗ NEEDS CORRECTION** | Unsafe LCNV formulation |
| #45 | Executable | BINDING | ✓ Active | CTS tokenizer (NOT inverse law) |
| #46-49 | Executable | BINDING | ✓ Active | Tokenizer/boundary |

---

## 6. Authority Control Framework

### 6.1 Document Authority Levels

**BINDING**:
- Claims authority over current or future runtime
- Violations are constitutional errors even if tests pass
- Requires guard tests
- Examples: LCNV architecture, kernel contract, layer laws

**PLANNING**:
- Speculative, non-binding
- May reference future work without authority claim
- Does not require guards
- Must be marked "PLANNING ONLY" explicitly

**EXPERIMENTAL**:
- In `experimental/` directory
- No canonical authority
- May contradict constitution (testing hypotheses)
- Must not be merged to canonical without constitutional review

### 6.2 PR Authority Declaration

Every PR with constitutional docs MUST declare:

```yaml
authority:
  level: BINDING | PLANNING | EXPERIMENTAL
  scope: "what this governs"
  guards: "which tests prevent regression"
  dependencies: "which PRs/docs this requires"
  supersedes: "which docs/PRs this replaces"
```

### 6.3 Guard Test Requirements

**For BINDING docs**:
```python
def test_doc_constitutional_safety():
    """Prevent unsafe formulations."""
    text = read_doc()
    for forbidden in FORBIDDEN_PATTERNS:
        assert forbidden not in text
    for required in REQUIRED_PATTERNS:
        assert required in text
```

**For Future PR References**:
```python
def test_doc_pr_references_valid():
    """Verify all PR references match reality."""
    for claim in extract_pr_claims(doc):
        pr_number = claim.pr_number
        pr_actual = get_pr_metadata(pr_number)
        assert claim.description matches pr_actual.title
```

---

## 7. Lessons Learned

### 7.1 What Worked

1. **PR #16-18 Recognition**: Project identified constitutional debt and isolated it
2. **PR #26 Correction**: Prevented illegal linearization of parallel proofs
3. **PR #32 Governance**: Massive constitutional foundation established
4. **PR #33-34 Drift Fix**: Corrected doc-code mismatches

### 7.2 What Failed

1. **PR #44 Timing**: Constitutional LCNV doc while Layer 2 incomplete
2. **PR #44 Formulation**: Unsafe `Unpack(Pack(x)) = x` with no guards
3. **PR #44 Future Reference**: False "PR #45 = inverse law" claim
4. **Pattern Recurrence**: Same debt pattern returned after PR #16 correction

### 7.3 Structural Weakness

**The system had NO mechanism to prevent**:
- Constitutional docs with binding authority but unsafe formulations
- Future PR references that don't match actual PRs
- Doc-code drift returning after correction
- "Docs-only" PRs claiming binding runtime authority without guards

**PR #50 fixes this** by adding:
- Guard tests for constitutional docs
- Authority audit (this document)
- Explicit governing laws
- Correction of unsafe LCNV formulation

---

## 8. Enforcement

### 8.1 This Document's Authority

**Status**: CONSTITUTIONAL
**Authority**: MANDATORY
**Scope**: All current and future PRs

### 8.2 Compliance Check

Before any PR with constitutional docs:

- [ ] Authority level declared (BINDING/PLANNING/EXPERIMENTAL)
- [ ] If BINDING: guard tests added
- [ ] If references future PRs: verification mechanism included
- [ ] If amends previous docs: supersession declared
- [ ] Doc-code consistency verified (no non-existent APIs)

### 8.3 Violation Consequences

**Any code/doc violating these laws is constitutionally invalid, even if tests pass.**

Examples of violations:
- BINDING doc without guards → Invalid
- Future PR reference without verification → Invalid
- `Unpack(LCNV(c)) = c` formulation → Invalid (violates Candidate primacy)
- Docs-only PR with binding authority but no guards → Invalid

---

## 9. Constitutional Seal

**This document establishes governance over PR authority synchronization.**

**Before PR #50**:
- Risk: Constitutional docs with false claims and unsafe formulations
- Risk: No guards prevent regression
- Risk: Future PR references go unverified

**After PR #50**:
- Constitutional docs require guards
- Unsafe formulations corrected and prevented
- Future PR references must be verified or marked speculative
- Authority levels explicitly declared

**Governing principle**:

```
لا وثيقة سلطوية بلا حارس
لا عكس بلا تحديد نوع المعاد
لا Pack/Unpack يعيد سلطة
لا رقم يسترد دليلًا
لا إسقاط يساوي مرشحًا
لا PR مستقبلي يصلح قانونًا إلا بعد أن يوجد فعلًا
```

**Translation**:
- No authoritative document without a guard
- No inverse without specifying return type
- No Pack/Unpack returns authority
- No number retrieves evidence
- No projection equals candidate
- No future PR fixes a law unless it actually exists

---

## End of Document

**Document ID**: `PR_1_49_AUTHORITY_AUDIT.md`
**Version**: 1.0
**Date**: 2026-06-03
**Status**: CONSTITUTIONAL
**Authority**: MANDATORY
**Corrects**: PR #44 authority mismatch, false PR #45 reference
**Establishes**: PR authority governance framework for all future PRs
