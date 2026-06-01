# NEXT LAYER DECISION TREE

> **Purpose:** Guide agents through systematic decision-making before proposing new layers.
>
> **Authority:** This decision tree enforces architectural discipline and prevents layer proliferation.

---

## Overview

**Use this decision tree BEFORE proposing any new layer, adapter, rule, or component.**

The tree guides you through 7 decision points to determine whether:
1. You need a new layer at all
2. An existing layer can be extended
3. The problem is actually missing data or evidence
4. Constitutional planning is required first

**If you skip this tree, your PR will be rejected.**

---

## Decision Tree

```
START: I have a problem or feature request
│
├─→ [1] Is the problem in an existing layer?
│   │
│   ├─→ YES: Do NOT add a new layer.
│   │         Add evidence/rule/test to the existing layer.
│   │         EXIT
│   │
│   └─→ NO: Continue to [2]
│
├─→ [2] Is the problem missing data for an existing layer?
│   │
│   ├─→ YES: Add source-of-truth data, NOT a new adapter.
│   │         Example: Add letter to makhraj mapping in phonetics/
│   │         Do NOT create a new layer for this.
│   │         EXIT
│   │
│   └─→ NO: Continue to [3]
│
├─→ [3] Is the problem a silent failure?
│   │
│   ├─→ YES: Add Residual with defer:{reason}:present.
│   │         Do NOT create a layer just to handle failures.
│   │         Example: defer:unknown_haraka:present
│   │         EXIT
│   │
│   └─→ NO: Continue to [4]
│
├─→ [4] Is the problem multiple possible roles?
│   │
│   ├─→ YES: Add RoleDisambiguationGate or evidence-based selection.
│   │         Do NOT make the symbol automatically decide its role.
│   │         Do NOT create separate layers for each role.
│   │         Example: Hamza can be carrier or mark → evidence decides
│   │         EXIT
│   │
│   └─→ NO: Continue to [5]
│
├─→ [5] Is the problem after Slot formation?
│   │
│   ├─→ YES: Do NOT build Root/Weight before SyllableCandidate exists.
│   │         Do NOT build Meaning before WordForm exists.
│   │         Follow constitutional layer sequence.
│   │         Check LAYER_CONTRACT_CONSTITUTION.md for proper order.
│   │         EXIT or propose constitutional sequence planning
│   │
│   └─→ NO: Continue to [6]
│
├─→ [6] Is there a constitutional gate for this layer?
│   │
│   ├─→ YES: Follow LAYER_CONTRACT_CONSTITUTION.md § 7 gate contract.
│   │         Complete AGENT_PR_CHECKLIST.md.
│   │         Create constitutional planning PR.
│   │         EXIT to planning phase
│   │
│   └─→ NO: Continue to [7]
│
└─→ [7] Does this duplicate an existing canonical layer?
    │
    ├─→ YES: REJECT. Extend existing layer instead.
    │         Check CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2
    │         Check LAYER_REGISTRY.md
    │         Use existing canonical component.
    │         EXIT
    │
    └─→ NO: This may be a genuinely new layer.
            Proceed to NEW LAYER PROTOCOL below.
```

---

## NEW LAYER PROTOCOL

**If you reached this point, you may have a genuinely new layer.**

**STOP. Do not write code yet.**

### Step 1: Answer These Questions

1. **Layer Name:** What is the canonical name?
2. **Proof Obligation:** What EXACT question does this layer answer?
3. **Input Type:** What is the exact input candidate type?
4. **Output Type:** What is the exact output candidate type?
5. **Parallel or Sequential:** Is this an atomic proof (parallel) or compositional (sequential)?
6. **Dependencies:** What canonical layers must exist first?
7. **Forbidden Outputs:** What outputs are explicitly forbidden? (List at least 5)
8. **Residual Behavior:** What defer:{reason}:present or fariq:{diff}:present claims are produced?
9. **Constitutional Basis:** Which LAYER_CONTRACT_CONSTITUTION.md section authorizes this?
10. **Duplicate Check:** Have you checked CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2?

### Step 2: Verify No Duplication

**Check these sources in order:**

1. LAYER_REGISTRY.md — Is this layer already listed?
2. CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 Duplicate Prevention Table — Is this concept already mapped?
3. src/qiyas_core/ directory — Does an adapter already exist for this?
4. EXPERIMENTAL_TO_CANONICAL_MAP.md — Was this in experimental/ and replaced?

**If ANY of these show a match, STOP. Use existing component instead.**

### Step 3: Constitutional Planning PR

**Before implementation, create a planning PR:**

```markdown
Title: docs(qiyas_core): plan Layer N — [LayerName]

Body:
## Layer Proposal

**Layer Name:** [LayerName]
**Proof Obligation:** [What question does this answer?]
**Input:** [InputCandidateType]
**Output:** [OutputCandidateType]

## Constitutional Basis

**Authorizing Gate:** LAYER_CONTRACT_CONSTITUTION.md § [section]
**Dependencies:** [List canonical layers this depends on]
**Forbidden Outputs:** [List at least 5]

## Duplicate Check

- [ ] Checked LAYER_REGISTRY.md: No match
- [ ] Checked Duplicate Prevention Table: No match
- [ ] Checked src/qiyas_core/: No match
- [ ] Checked experimental/: No match or validated for rebuild

## Evidence Requirements

**Required wasf:**
- [List]

**Required illah:**
- [List]

**Invalidating fariq:**
- [List]

## Residual Behavior

**Deferral conditions:**
- defer:[reason]:present when [condition]

## Open Questions

[List any uncertainties for maintainer review]
```

**Wait for maintainer approval before implementing.**

---

## Decision Point Details

### [1] Is the problem in an existing layer?

**Question:** Can this be solved by adding a rule, evidence type, or test to an existing canonical layer?

**Examples:**

✅ **Problem in existing layer:**
- "LetterIdentityCarrier doesn't handle hamza" → Add hamza recognition rule to LetterIdentityCarrier
- "Haraka classification missing sakta" → Add sakta to HarakaFunctionCarrier rules
- "Slot formation missing residual for orphan haraka" → Add defer:orphan_haraka:present to SlotCandidate

❌ **NOT in existing layer:**
- "Need to recognize syllable boundaries" → New layer (SyllableCandidate)
- "Need to match roots to patterns" → New layer (RootWeightAlgebra)

**Action if YES:** Add to existing layer, do NOT create new layer.

### [2] Is the problem missing data?

**Question:** Is this a data/knowledge problem, not an architectural problem?

**Examples:**

✅ **Missing data:**
- "Need makhraj coordinates for letter ض" → Add to phonetics/makhraj_map.py
- "Need abjad value for letter غ" → Add to abjad_system.py
- "Need sifat for letter ظ" → Add to phonetics/sifat_map.py

❌ **NOT missing data:**
- "Need to classify symbols" → TypedCodePoint layer already exists
- "Need to match haraka to carrier" → ConditionedTypedSequence already does this

**Action if YES:** Add data to source-of-truth, do NOT create adapter.

### [3] Is the problem a silent failure?

**Question:** Is the system failing silently when it should defer or block?

**Examples:**

✅ **Silent failure:**
- Unknown haraka encountered → Add defer:unknown_haraka:present
- Orphan shadda → Add defer:shadda_without_carrier:present
- Ambiguous letter identity → Add fariq:letter_identity_conflict:present

❌ **NOT silent failure:**
- Missing layer to process syllables → Requires new layer (SyllableCandidate)

**Action if YES:** Add Residual, do NOT create layer.

### [4] Is the problem multiple roles?

**Question:** Does a symbol have multiple possible interpretations that need disambiguation?

**Examples:**

✅ **Multiple roles:**
- Hamza can be carrier or mark → Add evidence-based role selection
- Alif can be long vowel or glottal → Add RoleDisambiguationGate
- Tanwin terminal vs. non-terminal → Add position-sensitive evidence

❌ **NOT multiple roles:**
- Each slot type has distinct function → Separate layers or slot types OK

**Action if YES:** Add disambiguation gate/evidence, do NOT create layer per role.

### [5] Is the problem after Slot?

**Question:** Are you trying to build a layer that should come after slot/syllable/stem but before those exist?

**Examples:**

❌ **Forbidden sequence violations:**
- Building RootWeightAlgebra before SyllableCandidate exists
- Building MeaningLayer before WordForm exists
- Building HukmLayer before Ifadah/Dalalah exist

✅ **Correct sequence:**
- Building SyllableCandidate after SlotCandidate exists
- Building StemMatterTensor after SyllableCandidate exists

**Action if YES:** STOP. Follow constitutional layer sequence. Build prerequisites first.

### [6] Is there a constitutional gate?

**Question:** Does LAYER_CONTRACT_CONSTITUTION.md define a gate for this layer?

**Check:** LAYER_CONTRACT_CONSTITUTION.md § 7 (14 gates)

**Examples:**

✅ **Has constitutional gate:**
- Jamid → § 7.1 RealityTypeGate
- Mushtaqq → § 7.2 DerivationalRoleGate
- Wadh → § 7.6 WadhScopeGate
- Hukm → § 7.11 EvidenceDomainGate

❌ **No constitutional gate:**
- Proprietary layer for specific use case → Propose constitutional amendment

**Action if YES:** Follow gate contract, create planning PR.
**Action if NO:** Propose constitutional amendment BEFORE implementing.

### [7] Does this duplicate existing?

**Question:** Is there already a canonical component that performs this function?

**Check in order:**
1. CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 Duplicate Prevention Table
2. LAYER_REGISTRY.md
3. src/qiyas_core/ directory listing
4. EXPERIMENTAL_TO_CANONICAL_MAP.md

**Examples:**

❌ **Duplicates:**
- SymbolClassifier → TypedCodePointLayerAdapter already exists
- LetterRecognizer → LetterIdentityCarrier already exists
- VowelFunction → HarakaFunctionCarrier already exists
- AtomicUnit → SlotCandidate already exists

✅ **Genuinely new:**
- SyllableCandidate (after slots, not yet implemented)
- RootWeightAlgebra (after syllables, not yet implemented)

**Action if YES (duplicates):** REJECT. Extend existing component.
**Action if NO:** Proceed to NEW LAYER PROTOCOL.

---

## Common Anti-Patterns

### Anti-Pattern 1: "I need X, so I'll create XLayer"

**Problem:** Assumes every feature needs a layer.

**Correct approach:** Use decision tree. Often X can be added to existing layer or as evidence.

### Anti-Pattern 2: "This layer is similar to experimental Y, let me revive Y"

**Problem:** Experimental components are pre-constitutional.

**Correct approach:** Check EXPERIMENTAL_TO_CANONICAL_MAP.md. Rebuild constitutionally, do NOT copy.

### Anti-Pattern 3: "I'll create a parallel layer for this edge case"

**Problem:** Creates layer proliferation.

**Correct approach:** Add RoleDisambiguationGate or evidence to existing layer.

### Anti-Pattern 4: "I'll rename existing layer to avoid duplication"

**Problem:** Renaming is not a solution. It IS duplication.

**Correct approach:** Extend existing layer or document why it's insufficient.

### Anti-Pattern 5: "I'll create a helper layer to bridge A and B"

**Problem:** Creates intermediate layers that violate proof structure.

**Correct approach:** Check if A and B should be parallel proofs, not sequential.

---

## Exit Strategies

### Exit 1: Add to Existing Layer

```python
# Example: Adding hamza support to LetterIdentityCarrier
# Do NOT create HamzaIdentityCarrier
# Do NOT create HamzaRecognizer

# CORRECT:
# Add to letter_identity_rules.py
add_letter_identity_rule("hamza", "U+0621", ...)
```

### Exit 2: Add Data

```python
# Example: Adding makhraj for ض
# Do NOT create DadMakhrajAdapter

# CORRECT:
# Add to phonetics/makhraj_map.py
MAKHRAJ_MAP = {
    ...
    "DAD": MakhrajCoordinate("ALVEOLAR", ...),
}
```

### Exit 3: Add Residual

```python
# Example: Unknown haraka encountered
# Do NOT create UnknownHarakaHandler

# CORRECT:
# Add defer claim in haraka_function_adapter.py
if haraka_class is None:
    residuals.append(Residual(
        effect="defer:unknown_haraka:present",
        ...
    ))
```

### Exit 4: Constitutional Planning

```markdown
# Example: Need syllable recognition
# Do NOT implement SyllableRecognizer directly

# CORRECT:
# Create planning PR first:
# docs(qiyas_core): plan Layer 4 — SyllableCandidate

# Wait for maintainer approval
# Then implement with constitutional compliance
```

---

## Quick Reference Card

```
Problem Type → Action

Bug in layer → Fix bug, not new layer
Missing data → Add data, not adapter
Silent fail → Add residual, not layer
Multiple roles → Add disambiguation, not layer per role
After Slot → Build prerequisites first
Has gate → Planning PR, wait for approval
Duplicate → Extend existing, REJECT new
New concept → NEW LAYER PROTOCOL
```

---

## Integration with Other Documents

**CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 6:** This document implements the Next Layer Decision Tree section.

**AGENT_PR_CHECKLIST.md:** Use this tree BEFORE completing checklist.

**LAYER_REGISTRY.md:** Consult registry at decision points [1], [6], [7].

**EXPERIMENTAL_TO_CANONICAL_MAP.md:** Consult map at decision point [7].

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Active decision framework
