# AGENT PR CHECKLIST — Mandatory Pre-Implementation

> **Purpose:** Ensure constitutional compliance BEFORE writing implementation code.
>
> **Authority:** Every agent must complete this checklist before creating any layer, adapter, rule, or component PR.

---

## When to Use This Checklist

**MANDATORY for:**
- Creating new layer
- Creating new adapter
- Creating new rule
- Creating new component in src/qiyas_core/
- Extending existing canonical layer
- Rebuilding from experimental/

**OPTIONAL for:**
- Bug fixes in existing code (unless architecture changes)
- Documentation-only PRs
- Test-only PRs for existing layers

**If uncertain whether checklist is required:** Complete it anyway. Better safe than rejected.

---

## Checklist

**Copy this checklist into your PR description BEFORE writing code.**

```markdown
## Agent Pre-Implementation Checklist

### 1. Constitutional Reading (MANDATORY)

- [ ] I have read CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
- [ ] I have read LAYER_REGISTRY.md
- [ ] I have read LAYER_CONTRACT_CONSTITUTION.md relevant sections
- [ ] I have read EXPERIMENTAL_TO_CANONICAL_MAP.md
- [ ] I have read NEXT_LAYER_DECISION_TREE.md

### 2. Duplicate Prevention (MANDATORY)

- [ ] I have checked CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 Duplicate Prevention Table
- [ ] I have checked LAYER_REGISTRY.md for existing layers
- [ ] I have searched src/qiyas_core/ for similar components
- [ ] I have checked EXPERIMENTAL_TO_CANONICAL_MAP.md for replaced components
- [ ] I have used NEXT_LAYER_DECISION_TREE.md and reached decision point [7]

**Duplicate Check Result:**
- [ ] NO duplicate found — this is a genuinely new layer/component
- [ ] OR: This extends existing layer: _______________

### 3. Layer Decision (REQUIRED for new layers)

**Layer Name:** _______________

**Proof Obligation:** (What EXACT question does this layer answer?)
_______________

**Input Type:** _______________

**Output Type:** _______________

**Layer Type:**
- [ ] New canonical layer (requires constitutional planning)
- [ ] Enrichment/extension of existing layer: _______________
- [ ] Bug fix in existing layer: _______________

**Architecture Type:**
- [ ] Atomic proof (parallel, independent of other Layer 2 proofs)
- [ ] Sequential proof (depends on previous layer outputs)
- [ ] Compositional proof (combines multiple parallel proofs)

**Dependencies:** (Which canonical layers must exist first?)
_______________

### 4. Canonical vs Experimental (MANDATORY)

**Status:**
- [ ] Canonical (meets all constitutional requirements)
- [ ] Experimental (exploratory, goes to experimental/)

**If canonical:**
- [ ] Constitutional basis documented: LAYER_CONTRACT_CONSTITUTION.md § ___
- [ ] Follows constitutional layer sequence
- [ ] Does NOT skip prerequisite layers

**If experimental:**
- [ ] Will be placed in experimental/, NOT src/
- [ ] Will NOT be imported by canonical code
- [ ] Marked as reference only

### 5. Experimental Boundary (MANDATORY)

- [ ] I have NOT imported from experimental/
- [ ] I have NOT copied code from experimental/ without validation
- [ ] If using patterns from experimental/, I have validated them against constitutional principles

**If similar to experimental component:**

**Experimental component:** _______________

**Why not using experimental version:** (Check ONE)
- [ ] Experimental version was replaced by canonical component: _______________
- [ ] Experimental version requires constitutional validation first
- [ ] Rebuilding with constitutional compliance, not copying

### 6. Required Documentation (MANDATORY)

**Forbidden Outputs:** (List at least 5)
1. _______________
2. _______________
3. _______________
4. _______________
5. _______________

**Evidence Claims Required:**

**Wasf (effective attributes):**
- وصف:_______________:evidenced
- (list all)

**Illah (licensing causes):**
- علة:_______________:verified
- (list all)

**Wadi Gates (if applicable):**
- وادي:_______________:_______________
- (list all)

**Invalidating Differences:**
- fariq:_______________:present blocks when _______________
- (list all)

**Residual Behavior:**

**Deferral conditions:**
- defer:_______________:present when _______________
- (list all)

**Blocking conditions:**
- fariq:_______________:present when _______________
- (list all)

### 7. Architectural Compliance (MANDATORY)

**Parallel Proof Architecture:**
- [ ] If Layer 2, this is an atomic proof (identity or function)
- [ ] Atomic identity proofs do NOT depend on sequence conditioning
- [ ] Atomic function proofs do NOT depend on sequence conditioning
- [ ] If ConditionedTypedSequence, outputs are evidence/alignment, NOT identity

**Slot Formation (if applicable):**
- [ ] SlotCandidate requires LetterIdentityCarrier
- [ ] SlotCandidate requires HarakaFunctionCarrier
- [ ] SlotCandidate requires PositionCarrier
- [ ] SlotCandidate requires AlignmentEvidence
- [ ] NO SlotCandidate without all four ingredients

**Forbidden Architecture:**
- [ ] NOT creating linear chain: TypedCodePoint → ConditionedTypedSequence → LetterIdentityCarrier
- [ ] NOT making atomic identity depend on sequence conditioning
- [ ] NOT producing identity from sequence conditioning layer

### 8. Naming (MANDATORY)

**Layer/Component Name:** _______________

- [ ] Name follows canonical naming conventions (see TERMINOLOGY_MAP.md)
- [ ] Name does NOT duplicate existing canonical name
- [ ] Name is registered in LAYER_REGISTRY.md (or will be in this PR)
- [ ] Name is descriptive and specific (not generic like "Processor" or "Handler")

### 9. Tests (MANDATORY for implementation PRs)

**Test Coverage:**
- [ ] Test proves layer does NOT produce forbidden outputs
- [ ] Test proves layer does NOT jump to later layers
- [ ] Test proves layer does NOT duplicate existing layer functionality
- [ ] Test proves identity preservation (if applicable)
- [ ] Test proves trace preservation
- [ ] Test proves rank meet semantics
- [ ] Test proves residual handling (defer/fariq)

**Test Scope:**
- [ ] Tests written AFTER implementation (correct construction order)
- [ ] Tests validate constitutional compliance, not just functionality

### 10. Non-Goals (MANDATORY)

**This PR explicitly does NOT:**
- [ ] Does NOT implement _______________
- [ ] Does NOT produce _______________
- [ ] Does NOT derive _______________ (e.g., meaning from numeric coordinates)
- [ ] Does NOT jump to layer _______________

(List at least 3 non-goals to prevent scope creep)

### 11. Constitutional Invariants (MANDATORY)

**Invariants Preserved:**
- [ ] Identity is not trace
- [ ] Trace is not identity
- [ ] Evidence may add trace but must not consume identity
- [ ] Candidate identity preserves source identities
- [ ] Invalidating difference blocks licensing
- [ ] Rank is computed by meet semantics
- [ ] Residuals are not hidden or silently discarded
- [ ] Boundary and alignment evidence not collapsed into identity
- [ ] Potential candidates do not become final judgments
- [ ] No layer produces final output of later layer without required gate and evidence

### 12. Affected Files (MANDATORY)

**Canonical files added/modified:**
- src/qiyas_core/_______________
- src/qiyas_core/rules/_______________
- (list all)

**Test files added/modified:**
- tests/qiyas_core/_______________
- (list all)

**Documentation files added/modified:**
- docs/qiyas_core/_______________
- (list all)

**Experimental files (if any):**
- [ ] NO experimental files modified (canonical PR)
- [ ] OR: Experimental files modified because _______________ (must justify)

### 13. Final Verification (MANDATORY)

- [ ] All above sections completed
- [ ] All checkboxes checked or justified
- [ ] No placeholders (_______________) remaining
- [ ] Ready for maintainer review

---

## For Planning PRs Only

If this is a constitutional planning PR (BEFORE implementation):

- [ ] This is a planning PR, NOT implementation PR
- [ ] No src/ code changes included
- [ ] Documents constitutional basis for proposed layer
- [ ] Includes Layer Proposal template (see NEXT_LAYER_DECISION_TREE.md)
- [ ] Awaiting maintainer approval before implementation

---

## For Extension PRs Only

If extending an existing canonical layer:

**Existing Layer:** _______________

**Extension Type:**
- [ ] Adding new evidence type
- [ ] Adding new rule
- [ ] Adding new data (e.g., letter mappings)
- [ ] Adding new test coverage
- [ ] Bug fix

**Why extension, not new layer:**
_______________

**Compatibility:**
- [ ] Extension preserves existing layer semantics
- [ ] Extension does NOT change existing forbidden outputs
- [ ] Extension does NOT change layer input/output types
- [ ] Extension adds capability, does NOT replace functionality
```

---

## Rejection Criteria

**A PR will be REJECTED if:**

1. **Checklist not completed** — All sections must be filled out
2. **Duplicates existing layer** — Check CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2
3. **Copies experimental/ without validation** — Experimental code is NOT canonical
4. **Skips NEXT_LAYER_DECISION_TREE.md** — Must use decision tree first
5. **Violates parallel proof architecture** — Atomic proofs cannot depend on sequence conditioning
6. **Missing forbidden outputs** — Must list at least 5
7. **Missing evidence requirements** — Must specify wasf/illah/wadi/fariq
8. **Missing residual behavior** — Must specify defer/fariq conditions
9. **Violates constitutional invariants** — See § 11 of checklist
10. **No constitutional basis** — Must cite LAYER_CONTRACT_CONSTITUTION.md section

**Even if code is correct and tests pass, PR is rejected if checklist fails.**

**Constitutional compliance > code quality.**

---

## Approval Flow

### Step 1: Agent Completes Checklist

Agent fills out this checklist BEFORE writing implementation code.

### Step 2: Agent Self-Review

Agent reviews checklist for:
- All checkboxes checked or justified
- No placeholders remaining
- All questions answered
- Constitutional compliance verified

**If ANY item is uncertain, STOP and ask maintainer before proceeding.**

### Step 3: Implementation (if checklist passes)

Agent writes implementation code following checklist commitments.

### Step 4: PR Creation

Agent creates PR with:
- Completed checklist in PR description
- Implementation code matching checklist
- Tests validating checklist claims
- Documentation updates

### Step 5: Maintainer Review

Maintainer reviews:
1. Checklist completeness
2. Constitutional compliance
3. Duplicate check accuracy
4. Architectural conformance
5. Implementation matching checklist

**Maintainer may reject based on checklist alone, before reviewing code.**

---

## Checklist Templates by PR Type

### Template 1: New Canonical Layer

Use full checklist above, emphasizing:
- § 3 Layer Decision
- § 4 Canonical vs Experimental (canonical)
- § 6 Required Documentation
- § 7 Architectural Compliance

### Template 2: Extension of Existing Layer

Use full checklist, plus "For Extension PRs Only" section.

Focus on:
- Why extension, not new layer
- Compatibility preservation

### Template 3: Planning PR (Before Implementation)

Use "For Planning PRs Only" section.

Do NOT include implementation code.

Wait for maintainer approval.

### Template 4: Experimental Exploration

Use full checklist with:
- § 4 Canonical vs Experimental (experimental)
- § 5 Experimental Boundary
- Target: experimental/ NOT src/

---

## Common Mistakes

### ❌ Mistake 1: "I'll fill out checklist after writing code"

**Problem:** Checklist guides implementation. Filling it out after defeats its purpose.

**Correct:** Complete checklist BEFORE writing code.

### ❌ Mistake 2: "I'll skip sections that don't apply"

**Problem:** All sections apply unless explicitly exempted (e.g., bug fixes).

**Correct:** Complete all sections or justify exemption.

### ❌ Mistake 3: "I checked LAYER_REGISTRY.md, no need for Duplicate Prevention Table"

**Problem:** Multiple sources must be checked to catch all duplicates.

**Correct:** Check ALL sources listed in § 2.

### ❌ Mistake 4: "Tests passing means checklist is correct"

**Problem:** Tests validate functionality, not constitutional compliance.

**Correct:** Checklist validates constitutional compliance first, tests second.

### ❌ Mistake 5: "I'll update LAYER_REGISTRY.md later"

**Problem:** Registry update is part of checklist (§ 8 Naming).

**Correct:** Update registry in same PR or mark as "will be in this PR."

---

## Integration with Other Documents

**CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 7:** This document implements the Agent PR Checklist section.

**NEXT_LAYER_DECISION_TREE.md:** Use decision tree BEFORE this checklist.

**LAYER_REGISTRY.md:** Update registry as part of checklist (§ 8).

**EXPERIMENTAL_TO_CANONICAL_MAP.md:** Consult for § 5 Experimental Boundary.

---

## Example Completed Checklist

See `docs/qiyas_core/examples/` directory for example completed checklists (if available).

Or review recent constitutional PRs (#20, #23, #26, #27, #28) for checklist examples.

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Mandatory enforcement
**Enforcement:** All PRs must include completed checklist
