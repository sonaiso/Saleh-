# LICENSED SYLLABLE CONSTITUTION — Phonetic Economy Law

> **Constitutional Authority:** This document establishes the constitutional basis for `LicensedSyllableCandidate` as the mathematical bridge between integrated linguistic units and morphological/metrical analysis.
>
> **Foundation:** PROJECT_MATHEMATICAL_FOUNDATION.md § 14 (SyllableCandidate), LAYER_CONTRACT_CONSTITUTION.md
>
> **Status:** Constitutional contract (Phase 1 — documentation before implementation)

---

## 0. Authority and Purpose

**This document is NOT an implementation guide. It is a constitutional contract.**

**Purpose:**
- Define the constitutional basis for `LicensedSyllableCandidate`
- Establish the phonetic economy law (قانون الاقتصاد الصوتي)
- Prevent illegal jumps from `IntegratedLinguisticCandidate` to Wazn/I'rab/Arud
- Create the proper algebraic foundation for future morphological and metrical layers

**Authority Hierarchy:**
1. Maintainer's explicit instruction in architectural evaluation of PR #50
2. This constitutional document
3. PROJECT_MATHEMATICAL_FOUNDATION.md
4. CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
5. LAYER_REGISTRY.md

---

## 1. Core Constitutional Principle

### 1.1 Central Law (القانون المركزي)

```
لا مقطع بلا ترتيب.
لا ترتيب بلا جوار.
لا جوار بلا حركة مرخّصة.
لا ترخيص بلا اقتصاد صوتي.
```

**Translation:**
```
No syllable without sequence.
No sequence without adjacency.
No adjacency without licensed haraka.
No licensing without phonetic economy.
```

### 1.2 Governing Prohibition

**FORBIDDEN:**
```
IntegratedLinguisticCandidate → Wazn
IntegratedLinguisticCandidate → I'rab
IntegratedLinguisticCandidate → Arud
IntegratedLinguisticCandidate → Morphology (direct)
IntegratedLinguisticCandidate → Meaning
IntegratedLinguisticCandidate → Hukm
```

**REQUIRED:**
```
IntegratedLinguisticCandidate sequence
+ SyllableEconomyBridge
→ LicensedSyllableCandidate
```

### 1.3 Architectural Reasoning

**Why syllable comes before morphology:**

A syllable is NOT built from a single element, but from a sequence:

```
ما قبل + حامل + حركة + ما بعد
(before + carrier + haraka + after)
```

If `IntegratedLinguisticCandidate` represents only a single position, the next required layer is:

```
tuple[IntegratedLinguisticCandidate, ...]
+ SyllableEconomyBridge
→ LicensedSyllableCandidate
```

---

## 2. Phonetic Economy Law (قانون الاقتصاد الصوتي)

### 2.1 Economy Principle

```
اختر أصغر مقطع مكتمل مرخّص
ولا توسّع المقطع إلا إذا منعته بقايا أو حدّ أو سكون أو مدّ.
```

**Translation:**
```
Choose the smallest complete licensed syllable.
Do not expand the syllable unless blocked by:
  - residuals (بقايا)
  - boundary (حدّ)
  - sukun (سكون)
  - vowel lengthening (مدّ)
```

### 2.2 Economy Operation

**Formal definition:**

```
SyllableEconomy:
  IntegratedLinguisticCandidate+
  + BoundaryEvidence
  + NeighborRelation
  → MinimalCompleteLicensedSyllable | Residual
```

**Minimality condition:**

```
∀ syllable s, ∀ expansion e:
  if Complete(s) ∧ Licensed(s)
  then Expand(s, e) is FORBIDDEN
  unless Blocked(e) ∨ Required(e)
```

**Where:**
- `Complete(s)` = syllable has carrier + opening + potential closure
- `Licensed(s)` = syllable passes economy + boundary + neighbor checks
- `Blocked(e)` = residual/boundary/sukun/madd prevents expansion
- `Required(e)` = phonotactic law requires expansion

### 2.3 Licensed Syllable Patterns

**These are PHONETIC patterns only, NOT prosodic/metrical:**

```
CV    (carrier + short vowel)
CVC   (carrier + short vowel + closure)
CVV   (carrier + long vowel)
CVVC  (carrier + long vowel + closure)
```

**Critical distinction:**

```
✓ CV as phonetic syllable candidate
✗ CV as metrical unit (Arud)
✗ CV as morphological unit (Wazn)
✗ CV as meaning carrier
```

**Example:**

```
بَ = CV (phonetic syllable candidate)
≠ "light syllable" (metrical judgment, Arud)
≠ "فَعَ pattern element" (morphological judgment, Wazn)
≠ "meaning unit" (semantic judgment)
```

---

## 3. Layer Definition

### 3.1 Layer Name

**Canonical Name:** `LicensedSyllableCandidate`

**Alternative Names (FORBIDDEN):**
```
❌ SyllableUnit
❌ PhonoSyllable
❌ CompleteSyllable
❌ FinalSyllable
❌ SyllableGeometry
❌ ArudUnit
```

### 3.2 Proof Obligation

**Question this layer answers:**

```
Can this sequence of integrated linguistic units form a licensed syllable
under phonetic economy law?
```

**What this layer does NOT answer:**
```
❌ What is the metrical weight? (Arud layer, future)
❌ What is the morphological pattern? (Wazn layer, future)
❌ What is the case marker? (I'rab layer, future)
❌ What is the meaning? (Meaning layer, future)
```

### 3.3 Input

```
Input: tuple[IntegratedLinguisticCandidate, ...]
```

**Where `IntegratedLinguisticCandidate` contains:**
- Atomic letter identity
- Haraka function
- Position carrier
- Alignment evidence
- Integration evidence (from PR #50)

**Additional required inputs:**
- `BoundaryEvidence` — sequence boundaries preserved
- `NeighborRelation` — adjacency evidence
- `SyllableEconomyBridge` — economy constraints

### 3.4 Output

```
Output: LicensedSyllableCandidate
```

**Structure:**

```python
@dataclass(frozen=True)
class LicensedSyllableCandidate:
    """
    Licensed syllable candidate under phonetic economy law.

    This is NOT:
    - Metrical weight (Arud)
    - Morphological pattern (Wazn)
    - Case marker (I'rab)
    - Meaning unit
    """

    # Identity preservation
    identity_ids: tuple[str, ...]  # from source IntegratedLinguisticCandidates
    syllable_identity: str  # e.g., "syllable:baa_fatha_CV"

    # Structural evidence
    constituents: tuple[IntegratedLinguisticCandidate, ...]  # sequence
    syllable_pattern: str  # "CV" | "CVC" | "CVV" | "CVVC"

    # Boundary evidence
    onset: tuple[str, ...]  # carrier identities
    nucleus: tuple[str, ...]  # vowel/haraka identities
    coda: tuple[str, ...] | None  # optional closure identities

    # Neighbor evidence
    left_boundary: BoundaryEvidence
    right_boundary: BoundaryEvidence
    neighbor_relations: tuple[NeighborRelation, ...]

    # Economy evidence
    economy_evidence: SyllableEconomyEvidence
    minimality_proof: str  # why this is minimal complete licensed

    # Standard candidate fields
    evidence: EvidenceSet
    rank: EvidenceRank
    trace_ids: tuple[str, ...]
    residuals: tuple[Residual, ...]
```

### 3.5 Forbidden Outputs

**This layer MUST NOT produce:**

1. `WaznCandidate` — morphological weight (future layer)
2. `IrabCandidate` — case/i'rab marking (future layer)
3. `ArudCandidate` — prosodic meter (future layer)
4. `MorphologyCandidate` — morphological analysis (future layer)
5. `MeaningCandidate` — semantic meaning
6. `HukmCandidate` — normative judgment
7. `RealityClaim` — reality claim
8. `FinalMeaning` — final meaning
9. `FinalPattern` — final pattern
10. `FinalWeight` — final weight

**Forbidden transitions:**

```
❌ LicensedSyllableCandidate → WaznCandidate (direct jump)
❌ LicensedSyllableCandidate → IrabCandidate (direct jump)
❌ LicensedSyllableCandidate → ArudCandidate (direct jump)
❌ LicensedSyllableCandidate → MeaningCandidate (direct jump)
```

---

## 4. Evidence Requirements

### 4.1 Required Evidence Structure

**Every `LicensedSyllableCandidate` MUST prove:**

1. **Sequence Evidence (وصف:has_syllable_sequence)**
   ```
   وصف:has_valid_sequence:evidenced
   وصف:constituents_ordered:evidenced
   وصف:sequence_complete:evidenced
   ```

2. **Boundary Evidence (وصف:has_syllable_boundary)**
   ```
   وصف:has_left_boundary:evidenced
   وصف:has_right_boundary:evidenced
   وصف:boundary_preserved:evidenced
   ```

3. **Neighbor Evidence (وصف:has_neighbor_relations)**
   ```
   وصف:has_adjacency:evidenced
   وصف:neighbors_licensed:evidenced
   وصف:no_orphan_elements:evidenced
   ```

4. **Economy Evidence (علة:syllable_economy_satisfied)**
   ```
   علة:minimal_complete_syllable:verified
   علة:economy_law_satisfied:verified
   علة:no_unnecessary_expansion:verified
   ```

5. **Pattern Evidence (وصف:has_syllable_pattern)**
   ```
   وصف:pattern_is_CV:evidenced    (for CV)
   وصف:pattern_is_CVC:evidenced   (for CVC)
   وصف:pattern_is_CVV:evidenced   (for CVV)
   وصف:pattern_is_CVVC:evidenced  (for CVVC)
   ```

### 4.2 Invalidating Differences (فارق)

**Blocking conditions:**

```
فارق:incomplete_syllable:present
  → Missing required constituent (carrier or nucleus)

فارق:economy_violation:present
  → Unnecessary expansion beyond minimal complete

فارق:boundary_violation:present
  → Syllable crosses required boundary

فارق:neighbor_violation:present
  → Adjacency or neighbor constraint violated

فارق:pattern_mismatch:present
  → Claimed pattern does not match actual structure
```

### 4.3 Deferral Conditions (defer)

**When to defer:**

```
defer:incomplete_sequence:present
  → Sequence does not form complete syllable yet

defer:boundary_pending:present
  → Boundary evidence not yet available

defer:neighbor_pending:present
  → Neighbor relations not yet established

defer:economy_pending:present
  → Economy analysis requires more context

defer:ambiguous_pattern:present
  → Multiple valid patterns possible, needs disambiguation
```

---

## 5. Phonetic Economy Bridge

### 5.1 Purpose

`SyllableEconomyBridge` is NOT a separate layer. It is evidence produced during syllable formation.

**Function:**

```
SyllableEconomyBridge:
  Sequence → Minimality Analysis → Economy Evidence
```

### 5.2 Minimality Analysis

**For each candidate syllable:**

1. **Completeness check:**
   - Has carrier (C)?
   - Has vowel/nucleus (V)?
   - Has optional coda (C)?

2. **Minimality check:**
   - Can syllable be shorter while remaining complete?
   - If YES → NOT minimal (economy violation)
   - If NO → Continue

3. **Expansion check:**
   - Is there pressure to expand (sukun, madd, boundary)?
   - If YES → Expansion required
   - If NO → Current form is licensed

### 5.3 Economy Evidence Output

```python
@dataclass(frozen=True)
class SyllableEconomyEvidence:
    """Evidence that syllable satisfies phonetic economy law."""

    is_minimal: bool  # smallest complete form
    is_complete: bool  # has required constituents
    expansion_blocked: bool  # further expansion prevented
    expansion_reason: str | None  # why expansion blocked/required

    economy_claims: tuple[str, ...]  # economy evidence
    minimality_proof: str
```

---

## 6. Architectural Integration

### 6.1 Position in Layer Sequence

**BEFORE LicensedSyllableCandidate (must exist):**
```
Layer 0: UnicodeCandidate ✓
Layer 1: TypedCodePoint ✓
Layer 2A: LetterIdentityCarrier ✓
Layer 2B: HarakaFunctionCarrier ✓
Layer 2C: PositionCarrier ✓
Layer 2D: ConditionedTypedSequence + AlignmentEvidence ✓
Layer 3: SlotCandidate ✓
Layer X: IntegratedLinguisticCandidate ✓ (PR #50)
```

**AFTER LicensedSyllableCandidate (future, not now):**
```
Layer Y: StemMatterTensor (not implemented)
Layer Z: RootWeightAlgebra (not implemented)
Layer Wazn: MorphologicalPattern (not implemented)
Layer I'rab: CaseMarking (not implemented)
Layer Arud: ProsodyMeter (not implemented)
```

### 6.2 Transition Path

**Correct sequence:**

```
IntegratedLinguisticCandidate+
→ LicensedSyllableCandidate
→ StemMatterTensor (future)
→ RootWeightAlgebra (future)
→ MorphologicalPattern (future)
```

**Forbidden shortcuts:**

```
❌ IntegratedLinguisticCandidate → RootWeightAlgebra
❌ IntegratedLinguisticCandidate → MorphologicalPattern
❌ IntegratedLinguisticCandidate → IrabCandidate
❌ LicensedSyllableCandidate → MeaningCandidate
```

### 6.3 Mathematical Bridge Role

`LicensedSyllableCandidate` serves as the mathematical bridge between:

**Input domain:**
- Atomic units (letters, harakas)
- Integrated positions
- Alignment evidence

**Future domains (NOT NOW):**
- Morphological analysis (Wazn)
- Syntactic analysis (I'rab)
- Prosodic analysis (Arud)

**Bridge function:**

```
LicensedSyllableCandidate = Phonetic potential
≠ Morphological determination
≠ Syntactic determination
≠ Prosodic determination
```

---

## 7. Constitutional Invariants

### 7.1 All 10 Invariants Preserved

**This layer MUST preserve:**

1. **Identity ≠ Trace**
   ```
   Identity(syllable) = union of constituent identities
   Trace(syllable) = union of constituent traces + syllable formation trace
   Identity ≠ Trace
   ```

2. **Trace ≠ Identity**
   ```
   Trace includes formation process
   Identity is preserved content
   Never conflate
   ```

3. **Evidence adds trace, not consumes identity**
   ```
   Economy evidence → adds trace
   Economy evidence ≠ consumes constituent identity
   ```

4. **Source identity preservation**
   ```
   ∀ constituent ∈ syllable.constituents:
     constituent.identity ∈ syllable.identity_ids
   ```

5. **Invalidating difference blocks licensing**
   ```
   if فارق:economy_violation:present
   then status = BLOCKED
   ```

6. **Rank meet semantics**
   ```
   Rank(syllable) = min(Rank(constituent₁), ..., Rank(constituentₙ), Rank(economy))
   ```

7. **Residuals not hidden**
   ```
   ∀ constituent.residuals:
     residual preserved or explicitly handled
   ```

8. **Boundary ≠ Identity**
   ```
   BoundaryEvidence provides context
   BoundaryEvidence ≠ constituent identity
   ```

9. **Potential ≠ Final**
   ```
   LicensedSyllableCandidate = potential
   LicensedSyllableCandidate ≠ final metrical/morphological judgment
   ```

10. **No layer jump**
    ```
    LicensedSyllableCandidate MUST NOT produce Wazn/I'rab/Arud/Meaning
    without required intermediate gates
    ```

### 7.2 Identity Preservation Formula

```
Identity(LicensedSyllableCandidate) =
  { syllable:pattern:{pattern_id} }
  ∪ { onset identities }
  ∪ { nucleus identities }
  ∪ { coda identities }
  ∪ { constituent identity_ids }
```

### 7.3 Trace Preservation Formula

```
Trace(LicensedSyllableCandidate) =
  { trace:syllable_formation:{syllable_id} }
  ∪ { trace:economy_check:{check_id} }
  ∪ { trace:boundary_check:{boundary_id} }
  ∪ { constituent trace_ids }
```

### 7.4 Rank Computation

```
Rank(LicensedSyllableCandidate) = minimum(
  Rank(constituent₁),
  Rank(constituent₂),
  ...,
  Rank(constituentₙ),
  Rank(economy_evidence),
  Rank(boundary_evidence),
  Rank(neighbor_evidence)
)
```

---

## 8. Implementation Phases

### 8.1 Phase 1: Constitutional Contract (CURRENT)

**Status:** In progress
**Deliverable:** This document
**No code implementation yet**

**Actions:**
- Define constitutional basis
- Establish phonetic economy law
- Define forbidden outputs
- Define evidence requirements
- Update LAYER_REGISTRY.md

### 8.2 Phase 2: Data Structures (NEXT)

**Prerequisites:** Phase 1 approved by maintainer

**Deliverables:**
- `LicensedSyllableCandidate` dataclass
- `SyllableEconomyEvidence` dataclass
- `NeighborRelation` dataclass (if not exists)
- `BoundaryEvidence` extensions (if needed)

**Location:** `src/qiyas_core/candidates/syllable.py`

### 8.3 Phase 3: Adapter and Rules (FUTURE)

**Prerequisites:** Phase 2 complete

**Deliverables:**
- `LicensedSyllableAdapter`
- `syllable_rules.py` with economy rules
- Constitutional tests

**Location:**
- `src/qiyas_core/licensed_syllable_adapter.py`
- `src/qiyas_core/rules/syllable_rules.py`
- `tests/qiyas_core/test_licensed_syllable_adapter.py`

---

## 9. Examples

### 9.1 Simple CV Syllable

**Input:**
```
IntegratedLinguisticCandidate(
  letter_identity="BAA",
  haraka_function="FATHA_OPENING",
  ...
)
```

**Process:**
1. Sequence analysis: [BAA + FATHA]
2. Pattern recognition: CV
3. Economy check: Minimal complete? YES
4. Boundary check: Valid boundaries? YES
5. Neighbor check: Valid adjacency? YES

**Output:**
```
LicensedSyllableCandidate(
  identity_ids=("letter:baa", "haraka:fatha", "syllable:ba_CV"),
  syllable_pattern="CV",
  onset=("BAA",),
  nucleus=("FATHA",),
  coda=None,
  economy_evidence=SyllableEconomyEvidence(
    is_minimal=True,
    is_complete=True,
    expansion_blocked=False,
    minimality_proof="smallest_complete_cv"
  ),
  ...
)
```

### 9.2 CVC Syllable with Sukun

**Input:**
```
[
  IntegratedLinguisticCandidate(letter="BAA", haraka="FATHA"),
  IntegratedLinguisticCandidate(letter="TAA", haraka="SUKUN")
]
```

**Process:**
1. Sequence: [BAA+FATHA, TAA+SUKUN]
2. Pattern: CVC (sukun closes)
3. Economy: Minimal? NO (could be CV), but REQUIRED due to sukun
4. Expansion reason: sukun forces closure

**Output:**
```
LicensedSyllableCandidate(
  syllable_pattern="CVC",
  onset=("BAA",),
  nucleus=("FATHA",),
  coda=("TAA",),
  economy_evidence=SyllableEconomyEvidence(
    is_minimal=False,  # could be shorter
    is_complete=True,
    expansion_blocked=False,
    expansion_reason="sukun_requires_coda",
    minimality_proof="required_by_sukun"
  ),
  ...
)
```

### 9.3 CVV Long Vowel

**Input:**
```
[
  IntegratedLinguisticCandidate(letter="BAA", haraka="FATHA"),
  IntegratedLinguisticCandidate(letter="ALIF", haraka="MADD")
]
```

**Process:**
1. Sequence: [BAA+FATHA, ALIF+MADD]
2. Pattern: CVV (long vowel)
3. Economy: Required by madd

**Output:**
```
LicensedSyllableCandidate(
  syllable_pattern="CVV",
  onset=("BAA",),
  nucleus=("FATHA", "MADD"),
  coda=None,
  economy_evidence=SyllableEconomyEvidence(
    is_minimal=False,
    is_complete=True,
    expansion_reason="madd_requires_extension",
    ...
  ),
  ...
)
```

---

## 10. Rejection and Deferral Rules

### 10.1 Blocking Conditions

**Syllable formation BLOCKED when:**

```
فارق:incomplete_carrier:present
  → No valid carrier for onset

فارق:incomplete_nucleus:present
  → No valid vowel/nucleus

فارق:economy_violation:present
  → Unnecessary expansion beyond minimal

فارق:boundary_crossed:present
  → Syllable attempts to cross word/phrase boundary

فارق:pattern_invalid:present
  → Pattern not in licensed set {CV, CVC, CVV, CVVC}
```

### 10.2 Deferral Conditions

**Syllable formation DEFERRED when:**

```
defer:sequence_incomplete:present
  → More constituents needed to complete pattern

defer:boundary_unknown:present
  → Cannot determine syllable boundaries yet

defer:economy_ambiguous:present
  → Multiple valid economy solutions exist

defer:neighbor_pending:present
  → Neighbor relations not yet established

defer:context_required:present
  → Need more context to determine pattern
```

### 10.3 Residual Preservation

**When blocking or deferring:**

1. Preserve all constituent residuals
2. Add syllable-level residual with reason
3. Preserve all trace information
4. DO NOT discard any evidence
5. DO NOT hide any blocking reason

---

## 11. Future Extensions

### 11.1 Forbidden Now, Allowed Later

**After LicensedSyllableCandidate is established, FUTURE layers may:**

1. **Metrical Weight Analysis (Arud)**
   ```
   LicensedSyllableCandidate
   + ProsodyContext
   → ArudCandidate (future)
   ```

2. **Morphological Pattern Analysis (Wazn)**
   ```
   LicensedSyllableCandidate+
   + RootContext
   → WaznCandidate (future)
   ```

3. **Syntactic Case Analysis (I'rab)**
   ```
   LicensedSyllableCandidate+
   + SyntacticContext
   → IrabCandidate (future)
   ```

**But NEVER directly from IntegratedLinguisticCandidate.**

### 11.2 Layer Sequence Requirement

```
REQUIRED ORDER:

IntegratedLinguisticCandidate
→ LicensedSyllableCandidate (NOW)
→ StemMatterTensor (FUTURE)
→ RootWeightAlgebra (FUTURE)
→ WaznCandidate (FUTURE)
→ IrabCandidate (FUTURE)
→ ArudCandidate (FUTURE)
```

**FORBIDDEN:**
```
❌ Skip LicensedSyllableCandidate
❌ Jump directly to Wazn/I'rab/Arud
❌ Derive meaning from phonetic syllable alone
```

---

## 12. Testing Requirements

### 12.1 Constitutional Tests

**Minimum required tests:**

1. **Pattern Recognition**
   - CV syllable formation
   - CVC syllable formation
   - CVV syllable formation
   - CVVC syllable formation

2. **Economy Law**
   - Minimal complete syllable accepted
   - Unnecessary expansion blocked
   - Required expansion (sukun) accepted
   - Required expansion (madd) accepted

3. **Boundary Preservation**
   - Syllable respects word boundaries
   - Syllable respects phrase boundaries
   - Boundary crossing blocked

4. **Neighbor Relations**
   - Adjacent constituents licensed
   - Orphan elements deferred
   - Neighbor violations blocked

5. **Forbidden Outputs**
   - Does NOT produce WaznCandidate
   - Does NOT produce IrabCandidate
   - Does NOT produce ArudCandidate
   - Does NOT produce MeaningCandidate
   - Does NOT produce HukmCandidate

6. **Invariant Preservation**
   - Identity preservation verified
   - Trace separation verified
   - Rank meet semantics verified
   - Residual preservation verified

7. **Deferral Handling**
   - Incomplete sequence deferred
   - Ambiguous pattern deferred
   - Boundary pending deferred

### 12.2 Integration Tests

**Verify integration with:**
- IntegratedLinguisticCandidate (input)
- BoundaryEvidence
- NeighborRelation
- SyllableEconomyBridge

---

## 13. Checklist for Implementation PR

**When implementing Phase 2 or 3, include this checklist:**

### Constitutional Compliance
- [ ] Read this constitutional document
- [ ] Read LAYER_REGISTRY.md
- [ ] Read CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
- [ ] No duplicate layers created

### Evidence Requirements
- [ ] All required وصف claims implemented
- [ ] All required علة claims implemented
- [ ] All فارق blocking conditions implemented
- [ ] All defer deferral conditions implemented

### Forbidden Outputs
- [ ] Test proves NO WaznCandidate output
- [ ] Test proves NO IrabCandidate output
- [ ] Test proves NO ArudCandidate output
- [ ] Test proves NO MeaningCandidate output
- [ ] Test proves NO HukmCandidate output

### Invariants
- [ ] Identity ≠ Trace verified
- [ ] Source identity preserved
- [ ] Rank meet semantics implemented
- [ ] Residuals not hidden
- [ ] Potential candidates only (not final)

### Integration
- [ ] LAYER_REGISTRY.md updated
- [ ] CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 updated
- [ ] Constitutional tests added

---

## 14. Cross-References

**Foundation Documents:**
- PROJECT_MATHEMATICAL_FOUNDATION.md § 14 (SyllableCandidate)
- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
- LAYER_REGISTRY.md
- LAYER_CONTRACT_CONSTITUTION.md

**Related Layers:**
- IntegratedLinguisticCandidate (PR #50, input)
- SlotCandidate (Layer 3, predecessor)
- StemMatterTensor (future, successor)

**Governance:**
- NEXT_LAYER_DECISION_TREE.md
- AGENT_PR_CHECKLIST.md

---

## 15. Arabic Terminology

**Key Arabic terms:**

- **المقطع** (al-muqaṭṭaʿ) — syllable
- **المقطع المرخّص** (al-muqaṭṭaʿ al-murakhaṣ) — licensed syllable
- **الاقتصاد الصوتي** (al-iqtiṣād aṣ-ṣawtī) — phonetic economy
- **الوزن** (al-wazn) — morphological weight/pattern
- **الإعراب** (al-iʿrāb) — case marking
- **العروض** (al-ʿarūḍ) — prosody/meter
- **الحركة** (al-ḥaraka) — vowel/diacritic
- **الحامل** (al-ḥāmil) — carrier (consonant)
- **السكون** (as-sukūn) — sukun (absence of vowel)
- **المدّ** (al-madd) — vowel lengthening

---

## 16. Final Authority Statement

**This document has constitutional authority.**

**Any implementation of LicensedSyllableCandidate MUST:**
1. Follow this constitutional contract
2. Preserve all 10 invariants
3. Implement all evidence requirements
4. Enforce all forbidden outputs
5. Respect phonetic economy law
6. NOT jump to Wazn/I'rab/Arud/Meaning

**Implementation without constitutional compliance is REJECTED.**

**Phonetic syllable ≠ Morphological pattern ≠ Metrical unit ≠ Meaning carrier.**

---

**Document Version:** 1.0
**Last Updated:** 2026-06-08
**Status:** Constitutional contract (Phase 1)
**Authority:** Supreme for LicensedSyllableCandidate layer
**Next Phase:** Data structures (awaiting maintainer approval)
