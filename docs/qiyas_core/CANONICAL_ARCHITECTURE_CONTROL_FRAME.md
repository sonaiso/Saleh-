# CANONICAL ARCHITECTURE CONTROL FRAME

> **Constitutional Authority:** This document implements the mathematical foundation and prevents layer duplication and architectural drift.
>
> **Purpose:** Maintain a single source of truth for what is canonical, what is experimental, what is deprecated, and what must not be rebuilt under a new name.
>
> **Foundation:** See PROJECT_MATHEMATICAL_FOUNDATION.md for the algebraic qiyas system definition that this document enforces.

---

## 0. Authority and Purpose

**This document sits below PROJECT_MATHEMATICAL_FOUNDATION.md and implements its principles:**

- PROJECT_MATHEMATICAL_FOUNDATION.md defines WHAT the project IS (algebraic qiyas system)
- This document defines HOW to implement it without drift (governance)

This document is the **governing frame** that prevents agents from reinventing existing layers under new names.

**The fundamental problem this solves:**

After PR #5–#31, the project passed through three overlapping phases:
1. Wide experimental exploration (PR #5–#14) before constitutional completion
2. Constitutional reset (PR #15–#18) establishing authority and isolating pre-constitutional work
3. Canonical rebuilding (PR #19–#31) re-implementing kernel, identity, TypedCodePoint, Layer 1/2, pre-slot alignment

**The current risk:**

A new agent sees old names in `experimental/` or old docs, then rebuilds the same concept with a new name, violating the prohibition against layer duplication.

**This document's function:**

- Map current canonical vs. experimental vs. deprecated status
- Prevent name proliferation through explicit duplicate-prevention tables
- Require every new PR to pass a layer-decision checklist before writing code
- Establish the canonical layer registry as the single source of architectural truth

---

## 1. Current Architectural State Map

### 1.1 Canonical Now (src/qiyas_core/)

**Core Kernel (PR #1, constitutional foundation):**
- `QiyasKernel` — algebraic kernel implementing all constitutional gates
- `Evidence` / `EvidenceSet` / `Residual` / `Candidate` / `CandidateSet`
- `QiyasRule` / `QiyasNodeRef` / `QiyasRegistry` / `QiyasAudit`
- `WadiGate` / `EvidenceRank` / `CandidateStatus` enums
- `QiyasKernelAdapter` base class
- `Validators` and formal laws

**Layer 0: Unicode Membership (PR #1):**
- `UnicodeLayerAdapter` — Arabic Unicode range validation
- `unicode_rules.py` — UNICODE_ARABIC_MEMBERSHIP rule

**Layer 1: TypedCodePoint Classification (PR #20, hardened PR #23):**
- `TypedCodePointLayerAdapter` — disjoint classification: Letter | Haraka | Boundary | Punctuation | Residual
- `typed_codepoint_rules.py` — type-specific wasf/illah, invalidating_differences for disjoint union proof

**Layer 2A: Letter Identity (PR #26, corrected PR #27):**
- `LetterIdentityCarrier` — pure identity only (unicode, script, name, letter class)
- `letter_identity_adapter.py` / `letter_identity_rules.py`
- **Does NOT contain:** makhraj, sifat, coordinates, abjad values

**Layer 2B: Haraka Function (PR #25, corrected PR #28):**
- `HarakaFunctionCarrier` — functional haraka classification (opening, closing, etc.)
- `haraka_function_adapter.py` / `haraka_function_rules.py`

**Layer 2C: Position Evidence (PR #28):**
- `PositionCarrier` — position context from ConditionedTypedSequence
- `position_adapter.py` / `position_rules.py`

**Layer 2D: Sequence Conditioning and Alignment (PR #28):**
- `ConditionedTypedSequence` — sequence-level admissibility
- `AlignmentEvidence` / `CarrierBindingCandidate`
- `conditioned_typed_sequence_adapter.py` / `conditioned_typed_sequence_rules.py`
- **Outputs alignment/binding/position/boundary evidence, NOT letter identity or slot candidates**

**Layer 3: Slot Candidate (PR #25, corrected PR #28):**
- `SlotCandidate` — requires LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier + AlignmentEvidence
- `slot_adapter.py` / `slot_rules.py`
- **No SlotGeometry, no SyllableCandidate**

**Layer X: Arabic Letter Coordinates (PR #27, partial canonical slice):**
- `ArabicLetterCoordinateCarrier` — enrichment with makhraj/sifat/abjad coordinates
- `letter_coordinate_adapter.py` / `letter_coordinate_rules.py`
- **Coverage:** BAA, TAA, SEEN, KAF only (minimal validation slice)
- **Missing:** full SifatVector, GlyphClassificationGate, complete letter coverage
- **Critical Constraint:** Abjad numeric coordinates have `semantic_force=FORBIDDEN`

**Specialized Systems:**
- `AbjadSystem` — conventional numeric coordinate system with semantic_force enforcement
- `RecursiveProofBuilder` — recursive proof construction
- `FormalLaws` — algebraic law enforcement
- `ForbiddenOutputs` — layer jump prevention

### 1.2 Minimal / Partial Canonical

Components that exist in canonical src/ but are incomplete:

| Component | Status | Coverage | Missing |
|-----------|--------|----------|---------|
| ArabicLetterCoordinateCarrier | Partial | BAA/TAA/SEEN/KAF | Full alphabet, GlyphClassificationGate, complete SifatVector |
| Phonetics module | Partial | Makhraj enum, basic sifat | Full phonology, universal sound algebra |

### 1.3 Experimental Only (experimental/)

**Pre-constitutional work isolated in PR #17:**
- Old AtomicUnit architecture
- Old PhonoFunctionalReadiness (CarrierFunction, MarkFunction, PhonoFunctionalUnit, SyllableReadiness)
- Old Syllable readiness framework
- Old SlotGeometry architecture (protocol, spec, policies, demand/capability)
- Old constitutional test framework copies
- All pre-constitutional adapters and rules (17 adapters, 17 rule files)

**Status:** Reference only, do NOT import in canonical code, do NOT copy without constitutional validation

### 1.4 Not Implemented (constitutional contracts exist, no canonical implementation)

**From LAYER_CONTRACT_CONSTITUTION.md:**
- UniversalSoundAlgebra
- LanguagePhonology
- ScriptAlgebra
- Full ArabicMorphophonology
- Full SifatVector with complete letter coverage
- GlyphClassificationGate
- SyllableCandidate
- StemMatterTensor
- RootWeightAlgebra
- WordForm
- Composition / Ifadah / Hukm layers

**Status:** Future layers, require constitutional planning before implementation

---

## 1.5 API Authority Principle

**Governance documents must align with executable code reality.**

### Authority Hierarchy for Names

**Architectural principles govern code meaning:**
- Layer boundaries, transition requirements, evidence obligations
- Identity preservation, trace separation, residual handling
- Algebraic composition rules, rank meet semantics

**Current canonical code governs API names:**
- File paths, module names, directory structure
- Class names, function names, dataclass field names
- Import paths, callable signatures

### The Rule

```
If governance docs and canonical code disagree on file/class/function names:
→ Update docs to match code
→ Do NOT create parallel APIs to satisfy stale docs

Exception: Explicit migration PR changes code after constitutional approval.
```

### Examples

**Correct:**
```
Doc says: src/qiyas_core/systems/abjad_system.py with AbjadSystem class
Reality: src/qiyas_core/abjad_system.py with get_abjad_coordinate function
→ Update doc to match reality: cite src/qiyas_core/abjad_system.py and get_abjad_coordinate
```

**Incorrect:**
```
Doc says: src/qiyas_core/systems/abjad_system.py with AbjadSystem class
Reality: src/qiyas_core/abjad_system.py with get_abjad_coordinate function
→ Create systems/abjad_system.py with AbjadSystem to match doc ❌ FORBIDDEN
```

### Rationale

Governance documents are prompts for AI agents. If docs reference non-existent APIs, agents may:
1. Create parallel implementations to match stale docs (layer duplication)
2. Use non-functional claim syntax (silent failures)
3. Misunderstand implementation status

**The correct sequence:**
1. Constitutional docs define architectural principles
2. Code implements those principles
3. Governance docs cite actual file paths, APIs, and field names from code
4. If migration needed, constitutional approval → code change → doc update

---

## 2. Duplicate Prevention Table

**This is the most critical section.**

Before creating ANY new layer, adapter, rule, or concept, check this table first.

| Need | DO NOT CREATE | USE / EXTEND INSTEAD |
|------|--------------|---------------------|
| Symbol classification | SymbolClassifier, UnicodeTypeLayer, CodePointType | TypedCodePointLayerAdapter |
| Letter identity | ArabicLetterIdentity, LetterProof, LetterRecognizer | LetterIdentityCarrier |
| Haraka function | VowelFunction, HarakaEnergy, MarkClassifier | HarakaFunctionCarrier |
| Position context | IndexCarrier, PositionProof, SequencePosition | PositionCarrier |
| Letter-haraka alignment | CompatibilityProof, SlotFit, BindingValidator | AlignmentEvidence / CarrierBindingCandidate |
| Slot formation | AtomicUnit, PhonoSlot, LetterHarakaUnit, PhonoFunctionalUnit | SlotCandidate |
| Phonetic coordinates | PhoneticLetterCarrier, SoundGeometry, ArticulationPoint | ArabicLetterCoordinateCarrier |
| Numeric values (Abjad) | NumberValue, AbjadMeaning, LetterNumerology | AbjadCoordinate via get_abjad_coordinate from abjad_system.py with semantic_force=FORBIDDEN |
| Sequence conditioning | SequenceValidator, ContextBuilder, TypedPair | ConditionedTypedSequence |
| Boundary handling | BoundaryProcessor, WhitespaceClassifier | TypedCodePoint (BoundaryCodePoint type) |
| Residual preservation | ErrorCollector, FailureHandler | Residual (from QiyasKernel) |
| Evidence collection | ProofBuilder, ClaimAssembler | EvidenceSet |
| Rank calculation | StrengthCalculator, ConfidenceRanker | EvidenceRank with minimum_rank() meet semantics |

**Law of Canonical Naming:**

```
If a concept is already represented by a canonical component,
then EXTEND that component or document why it is insufficient.

DO NOT create a parallel adapter/rule/carrier with a new name.
```

**Examples of FORBIDDEN duplication:**

```python
# FORBIDDEN: Creating parallel identity layer
class LetterRecognizer:  # ❌ LetterIdentityCarrier already exists
    ...

# FORBIDDEN: Creating parallel slot layer
class PhonoFunctionalUnit:  # ❌ SlotCandidate already exists
    ...

# FORBIDDEN: Creating parallel numeric system
class LetterNumerology:  # ❌ get_abjad_coordinate already exists in abjad_system.py
    def derive_meaning_from_number(self):  # ❌ Violates semantic_force=FORBIDDEN
        ...

# ALLOWED: Extending existing layer with new evidence
LetterIdentityRules.add_wasf("has_hamza_behavior")  # ✓

# ALLOWED: Creating genuinely new layer with constitutional basis
class SyllableCandidate:  # ✓ New layer, requires constitutional planning
    ...
```

---

## 3. Canonical Name Registration Law

**Every new PR must answer these questions BEFORE writing code:**

### 3.1 Layer Decision Checklist

```markdown
## Pre-Implementation Layer Decision

1. **Layer Name:** What is the canonical name of the layer I'm adding?

2. **Existing Layer Check:** Is there an existing canonical layer that performs this function?
   - If YES: Why is the existing layer insufficient? Document specific gaps.
   - If NO: Proceed to #3.

3. **Input Type:** What is the exact input candidate type?

4. **Output Type:** What is the exact output candidate type?

5. **Forbidden Outputs:** What outputs are explicitly forbidden? (List at least 3)

6. **Layer Type:**
   - [ ] New canonical layer (requires constitutional planning)
   - [ ] Enrichment of existing layer (requires compatibility proof)
   - [ ] Experimental exploration (must go to experimental/, not src/)

7. **Canonical vs Experimental:**
   - [ ] Canonical (meets all constitutional requirements)
   - [ ] Experimental (needs validation, goes to experimental/)

8. **Residual Behavior:** What residual is produced if the layer cannot complete?

9. **Constitutional Basis:** Which LAYER_CONTRACT_CONSTITUTION.md gate/section authorizes this?

10. **Duplicate Prevention Check:** Have I checked the Duplicate Prevention Table (§2)?
```

**Rejection Criteria:**

A PR is REJECTED if:
- It creates a new layer name when an existing canonical layer already performs that function
- It does not answer all 10 checklist questions
- It bypasses the Duplicate Prevention Table
- It copies experimental code to src/ without constitutional validation

---

## 4. Experimental → Canonical Mapping

**Purpose:** Prevent revival of experimental components without awareness.

| Experimental Component (experimental/) | Canonical Replacement (src/) | Status | Action |
|---------------------------------------|----------------------------|--------|--------|
| AtomicUnitQiyas | SlotCandidate after alignment | Replaced | Do NOT revive |
| Old HarakaQiyas | HarakaFunctionCarrier | Rebuilt constitutionally | Do NOT copy old version |
| Old SlotGeometry protocol | Deferred; forbidden after SlotCandidate for now | Not canonical | Requires constitutional validation |
| Old syllable readiness | Future SyllableCandidate path | Not canonical | Requires constitutional planning |
| Old constitutional helpers | Partial reference only | Patterns extracted | Do NOT copy tests before constitution |
| CarrierFunction / MarkFunction / PhonoFunctionalUnit | SlotCandidate composition | Replaced by simpler architecture | Do NOT revive |
| Old demand/capability architecture | Alignment/binding evidence | Replaced | Do NOT revive |
| 17 pre-constitutional adapters | Rebuilt selectively as needed | Isolated | Validate before canonical adoption |

**Critical Rule:**

```
experimental/ is NOT a source for copying, but a historical archive for comparison.

Before adopting ANY pattern from experimental/:
1. Verify it has constitutional basis
2. Check Duplicate Prevention Table (§2)
3. Validate against current canonical architecture
4. Rebuild with constitutional compliance, do NOT copy directly
```

---

## 5. Layer Registry (Single Source of Truth)

**This section is the authoritative reference for all layers.**

See `LAYER_REGISTRY.md` for detailed layer-by-layer documentation.

**Quick Reference:**

```
Layer 0: UnicodeCandidate (raw codepoint → Arabic Unicode membership)
Layer 1: TypedCodePoint (UnicodeCandidate → Letter|Haraka|Boundary|Punctuation|Residual)

Layer 2A: LetterIdentityCarrier (LetterCodePoint → pure letter identity)
Layer 2B: HarakaFunctionCarrier (HarakaCodePoint → haraka function)
Layer 2C: PositionCarrier (sequence index → position context)
Layer 2D: ConditionedTypedSequence + AlignmentEvidence (sequence → alignment/binding/admissibility)

Layer 3: SlotCandidate (Letter + Haraka + Position + Alignment → slot)

Layer X: ArabicLetterCoordinateCarrier (LetterIdentity → coordinates, partial)

Layers 4+: Not implemented (SyllableCandidate, Stem, Root/Weight, WordForm, Meaning, Hukm)
```

**Parallel Architecture (NOT linear chain):**

```
TypedCodePoint branches:
  → LetterIdentityCarrier (atomic identity proof)
  → HarakaFunctionCarrier (atomic function proof)

TypedCodePoint* (sequence):
  → ConditionedTypedSequence → AlignmentEvidence + PositionCarrier

Convergence:
  LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier + AlignmentEvidence
  → SlotCandidate
```

**FORBIDDEN Architecture (incorrect linear chain):**

```
❌ TypedCodePoint → ConditionedTypedSequence → LetterIdentityCarrier → SlotCandidate

This is WRONG because it makes atomic identity depend on sequence conditioning.
```

---

## 6. Next Layer Decision Tree

**Use this decision tree BEFORE proposing any new layer.**

### 6.1 Is the problem in an existing layer?

→ **YES:** Do NOT add a new layer. Add evidence/rule/test to the existing layer.

→ **NO:** Continue to 6.2

### 6.2 Is the problem missing data for an existing layer?

→ **YES:** Add source-of-truth data, NOT a new adapter.

→ **NO:** Continue to 6.3

### 6.3 Is the problem a silent failure?

→ **YES:** Add Residual with defer:{reason}:present, NOT a new layer.

→ **NO:** Continue to 6.4

### 6.4 Is the problem multiple possible roles?

→ **YES:** Add RoleDisambiguationGate or evidence-based role selection, NOT automatic assumption.

→ **NO:** Continue to 6.5

### 6.5 Is the problem after Slot formation?

→ **YES:** Do NOT build Root/Weight before SyllableCandidate and StemMatterTensor exist.

→ **NO:** Continue to 6.6

### 6.6 Is there a constitutional gate for this layer?

→ **YES:** Follow LAYER_CONTRACT_CONSTITUTION.md gate contract, create constitutional PR.

→ **NO:** STOP. Propose constitutional amendment first, then implement.

### 6.7 Does this duplicate an existing canonical layer?

→ **YES:** REJECT. Extend existing layer instead.

→ **NO:** Proceed with constitutional planning.

---

## 7. Agent PR Checklist (Mandatory Before Code)

**Every agent must complete this checklist BEFORE creating implementation code:**

```markdown
## Agent Pre-Implementation Checklist

### Constitutional Compliance
- [ ] I have read CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
- [ ] I have read LAYER_REGISTRY.md
- [ ] I have read LAYER_CONTRACT_CONSTITUTION.md relevant sections
- [ ] I have checked the Duplicate Prevention Table (§2)
- [ ] I have used the Next Layer Decision Tree (§6)

### Layer Decision
- [ ] This is a new canonical layer (not extension of existing)
  - OR: This extends an existing canonical layer: _______________
- [ ] This depends on canonical layer(s): _______________
- [ ] This is NOT similar to experimental component: _______________
  - OR: This IS similar to experimental component _______ but rebuilt with constitutional basis because: _______________

### Required Documentation
- [ ] Forbidden outputs are explicitly listed (minimum 3)
- [ ] Evidence claims are explicitly required
- [ ] Residual behavior on failure is documented
- [ ] Test proves no layer jump
- [ ] Test proves no duplicate layer

### Experimental Boundary
- [ ] I have NOT imported from experimental/
- [ ] I have NOT copied patterns from experimental/ without validation
- [ ] If this is experimental exploration, it will go to experimental/, not src/

### Naming
- [ ] The layer name does NOT duplicate an existing canonical name
- [ ] The layer name follows canonical naming conventions
- [ ] I have registered this layer in LAYER_REGISTRY.md

### Architectural Compliance
- [ ] This follows parallel proof architecture (NOT linear chain)
- [ ] Atomic identity proofs do NOT depend on sequence conditioning
- [ ] Sequence conditioning produces evidence, NOT identity
- [ ] SlotCandidate requires all four ingredients (Letter, Haraka, Position, Alignment)
```

**If ANY checkbox is unchecked or uncertain, STOP and ask the maintainer.**

---

## 8. Governing Rules for Agents

### 8.1 Absolute Prohibitions

**DO NOT:**
1. Invent new names for existing canonical layers
2. Copy experimental/ code to src/ without constitutional validation
3. Create linear chains where parallel proofs are required
4. Make atomic identity depend on sequence conditioning
5. Turn evidence into identity
6. Turn potential into final meaning
7. Build layers without checking Duplicate Prevention Table
8. Skip the Agent PR Checklist

### 8.2 Required Actions

**ALWAYS:**
1. Check LAYER_REGISTRY.md before proposing a new layer
2. Use Duplicate Prevention Table before creating any component
3. Complete Agent PR Checklist before writing implementation code
4. Ask maintainer when uncertain about architecture
5. Preserve parallel proof structure (identity + function proofs are independent)
6. Ensure ConditionedTypedSequence produces evidence, not identity
7. Require all four ingredients for SlotCandidate
8. Document constitutional basis for every new layer

### 8.3 When in Doubt

```
If you are uncertain whether a component already exists:
  → Check LAYER_REGISTRY.md
  → Check Duplicate Prevention Table
  → Search src/qiyas_core/ for similar names
  → Ask maintainer

If you are uncertain whether to extend or create new:
  → Default to EXTEND existing layer
  → Only create new if genuinely different proof obligation

If you are uncertain about constitutional basis:
  → Check LAYER_CONTRACT_CONSTITUTION.md
  → Ask maintainer before implementing

When uncertain, STOP and ask. Do NOT guess.
```

---

## 9. Terminology Stability

**Canonical naming is FIXED by TERMINOLOGY_MAP.md.**

Do NOT rename:
- `EvidenceRank` values: NO_EVIDENCE, FORMAL_STRUCTURE, ANALOGICAL, DIRECT_HEARING, INDIVIDUAL_REPORT, MASS_TRANSMISSION
- `WadiGate` values: CAUSE, CONDITION, OBSTACLE, VALIDITY, CORRUPTION, NULLITY
- Arabic claim prefixes: `اصل:`, `فرع:`, `وصف:`, `علة:`, `فارق:`, `وادي:`
- Core types: QiyasKernel, QiyasRule, QiyasNodeRef, Evidence, Candidate, Residual

Do NOT create synonyms:
- `StrengthCalculator` for `EvidenceRank` ❌
- `ProofBuilder` for `EvidenceSet` ❌
- `FailureHandler` for `Residual` ❌

---

## 10. Version Control and Updates

**This document evolves with the codebase.**

When a new canonical layer is added:
1. Update § 1.1 Current Architectural State Map
2. Update § 2 Duplicate Prevention Table
3. Add entry to LAYER_REGISTRY.md
4. Update § 5 Layer Registry quick reference

When experimental work is promoted to canonical:
1. Update § 4 Experimental → Canonical Mapping
2. Remove from experimental/ status
3. Add to § 1.1 as canonical
4. Document constitutional validation in PR

When a layer is deprecated:
1. Move from § 1.1 to § 1.3 or new § 1.5 Deprecated
2. Add to Duplicate Prevention Table with "Do NOT use" status
3. Document why deprecated

---

## 11. Enforcement

**This document has constitutional authority.**

PRs that violate this document's rules are REJECTED, even if:
- The code is high quality
- The tests pass
- The implementation is correct

**Constitutional compliance > code quality.**

A well-written duplicate layer is still a violation.

**Maintainer responsibility:**

The maintainer enforces this document by:
1. Requiring Agent PR Checklist completion before code review
2. Checking Duplicate Prevention Table during PR review
3. Verifying LAYER_REGISTRY.md is updated
4. Rejecting PRs that create duplicate layers under new names
5. Updating this document when architecture evolves

---

## 12. Cross-References

**Required reading for all agents:**
- LAYER_REGISTRY.md — detailed layer-by-layer documentation
- LAYER_CONTRACT_CONSTITUTION.md — constitutional gates and contracts
- EXPERIMENTAL_TO_CANONICAL_MAP.md — experimental component status
- NEXT_LAYER_DECISION_TREE.md — decision framework for new layers
- AGENT_PR_CHECKLIST.md — mandatory pre-implementation checklist
- TERMINOLOGY_MAP.md — fixed canonical naming
- RESET_CONSTITUTION.md — constitutional foundation
- AUDIT_AFTER_RESET_CONSTITUTION.md — constitutional audit evidence

---

## Final Statement

```
The purpose of this document is to prevent architectural drift
and layer proliferation through name changes.

Every concept has ONE canonical name.
Every layer has ONE canonical implementation.
Every function has ONE canonical location.

Duplication is architectural debt.
Renaming is not a solution to architectural problems.

When uncertain about whether a layer exists:
  Check LAYER_REGISTRY.md first.
  Check Duplicate Prevention Table second.
  Ask maintainer third.

Do NOT create new names for old concepts.
Do NOT reinvent layers that already exist.
Do NOT bypass this control frame.

Constitutional discipline > implementation speed.
```

---

**Document Version:** 1.0
**Authority:** Constitutional governance document
**Status:** Active enforcement
**Last Updated:** 2026-06-01
