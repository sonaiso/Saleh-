# PROJECT MATHEMATICAL FOUNDATION

> **النظام القياسي الجبري الطبقي للغة العربية**
>
> **Layered Qiyas-Based Algebraic System for Arabic**

---

## 0. Foundational Principle

**This project is NOT a linguistic pipeline.**

**This project IS:**

> A proof-relevant, identity-preserving algebraic system that licenses transitions of linguistic objects across domains through qiyas (analogical proof), operating each domain with partial algebraic operations, preserving identity+rank+trace, and exposing non-closure as residuals.

**بالعربية:**

> المشروع يثبت انتقال الكائن اللغوي من مجال إلى مجال بقياس محفوظ الهوية،
> ثم يشغله داخل كل مجال بعمليات جبرية جزئية،
> ولا يسمح بالنجاح إلا بدليل ورتبة وأثر،
> ولا يسمح بالفشل الصامت بل يخرجه كبقايا.

---

## 1. Core Mathematical Definition

### Arabic Algebraic Qiyas System

```
ArabicAlgebraicQiyasSystem =
    Domains
  + Operations
  + QiyasTransitions
  + Evidence
  + Rank
  + Trace
  + Residuals
  + IdentityPreservation
```

### Foundational Laws

**Every layer is a domain.**
**Every transition is a qiyas proof.**
**Every composition is a partial algebraic operation.**
**Every failure is a residual set.**
**Every success is an identity-preserving candidate.**

**Formal notation:**

```
Layer = DomainBoundary
Transition = QiyasProof
Composition = PartialAlgebraicOperation
Failure = ResidualSet
Success = Candidate(identity_ids, rank, trace_ids, residuals)
```

**Critical constraint:**

```
No layer produces output merely because it is named "layer."
No operation exists without operating conditions.
No transition exists without qiyas proof.
```

---

## 2. Qiyas as Transition Proof

**Every domain transition MUST follow this structure:**

```
QiyasTransition(A → B) =
    Asl (established source)
  + Far (determined target)
  + SharedIllah (licensing cause)
  + EffectiveWasf (effective attribute)
  + FariqAudit (invalidating difference negation)
  + Evidence
  + Rank
  + IdentityPreservation
  + Residual
```

**Meaning:**

Transferring the branch (far) to the source (asl) occurs ONLY when:
- A shared cause (illah) exists
- An effective attribute (wasf) is present
- Invalidating differences (fariq) are negated
- Evidence is provided
- Identity is preserved

### Example: UnicodeCandidate → TypedCodePoint

This is NOT mere classification. This is qiyas:

```
Asl: Domain of classified Arabic symbols
Far: Input codepoint U+0628
Shared Illah: belongs_to_typed_domain
Effective Wasf: is_arabic_letter
Invalidating Fariq: NOT haraka, NOT digit, NOT boundary
Result: LetterCodePoint
```

**Proof obligation:** Prove this codepoint belongs to the letter domain through evidence, not assumption.

---

## 3. Algebra as Domain Operation

**Within each domain, qiyas alone is insufficient. We need operations.**

```
AlgebraicOperation =
    Inputs
  + Domain
  + Operator
  + Preconditions
  + OutputCandidate
  + Residuals
```

### Example: Slot Formation (Partial Operation)

```
BindSlot:
    LetterIdentityCarrier
  × HarakaFunctionCarrier
  × PositionCarrier
  × AlignmentEvidence
  ⇀ SlotCandidate
```

**This is a partial algebraic operation** because it does NOT always succeed.

**Failure conditions:**
- Missing alignment evidence → defer:alignment_missing:present
- Missing position → defer:position_missing:present
- Letter/haraka conflict → فارق:incompatible_binding:present
- Missing evidence → defer:insufficient_evidence:present
- Invalidating difference present → فارق:{difference}:present

**Success conditions:**
- identity_ids preserved
- Rank established
- Trace preserved
- No blocking residuals

---

## 4. Concept Formation Before Rule Formation

**Critical methodological principle:**

> Do NOT start with code. Start with conceptual analysis of the domain.

### Concept Formation Process

```
ConceptFormation(domain):
    1. Initial conceptualization of the domain
    2. Retrieve domain information
    3. Identify identity-preserving concept
    4. Match concept to Arabic implementation reality
    5. Extract effective attribute (wasf)
    6. Determine invalidating differences (fariq)
    7. Convert concept to rule
    8. Test rule through qiyas
```

**Questions to answer BEFORE coding:**

1. What is the domain?
2. What does identity preservation mean here?
3. What is the evidence?
4. What are the invalidating differences?
5. What are the residuals?

**THEN write the rule.**

### Example: Short Vowel Function

```
Concept: Short vowel is phonetic operator
Arabic Reality: Fatha/Damma/Kasra/Sukun are opening/closing/neutral operators
Effective Wasf: short_vocalic_operation
Shared Illah: belongs_to_haraka_function_domain
Invalidating Fariq: NOT long vowel, NOT consonant, NOT punctuation
Rule: HarakaFunctionRule
```

---

## 5. From Concept to Rule

**Every concept set matched to reality becomes a rule:**

```
ConceptSet + Evidence + IdentityPreservation → QiyasRule
```

**No rule exists without:**
- Domain delimitation
- Transition proof
- Algebraic operation specification
- Identity preservation mechanism
- Residual production specification

---

## 6. Project Scope (Full Ladder)

**This is the complete architectural ladder:**

### 0. Governance Layer (Current)
- Architecture Control Frame ✓
- Layer Registry ✓
- Experimental-to-Canonical Map ✓
- Source-of-Truth Registry (needed)

### 1. Foundation (Canonical Now)
- QiyasKernel ✓
- UnicodeCandidate ✓
- TypedCodePoint ✓

### 2. Atomic Identity/Function (Partial Canonical)
- LetterIdentityCarrier ✓
- HarakaFunctionCarrier ✓
- PositionCarrier ✓
- ConditionedTypedSequence + AlignmentEvidence ✓
- ArabicLetterCoordinateCarrier (partial: 4 letters) ✓

### 3. Slot (Canonical)
- SlotCandidate ✓

### 4. Universal Phonetic Foundation (Not Implemented)
- UniversalSoundAlgebra
- LanguagePhonology
- ScriptAlgebra

### 5. Arabic Phonetic Completion (Not Implemented)
- Full SifatVector (currently partial)
- GlyphClassificationGate
- ArabicMorphophonology
- RoleDisambiguationGate

### 6. Syllable (Not Implemented)
- SyllableCandidate

### 7. Stem/Root (Not Implemented)
- StemMatterTensor
- RootWeightAlgebra

### 8. Word (Not Implemented)
- WordFormAlgebra

### 9. Lexical Meaning (Not Implemented)
- LexicalMadlulAlgebra

### 10. Composition (Not Implemented)
- CompositionAlgebra

### 11. Style (Not Implemented)
- StyleTemplateAlgebra

### 12. Ifadah (Not Implemented)
- IfadahCandidate

### 13. Hukm (Not Implemented)
- HukmCandidate

### 14. Truth/Evidence/Reality (Not Implemented)
- Truth/Evidence/Reality Grounding

**CRITICAL: Implementation does NOT start from UniversalSound immediately.**

**Next priority: Complete governance, THEN Full Layer 2 (SifatVector + GlyphClassificationGate).**

---

## 7. Governing Law for All Agents

**Place this at the top of the repository:**

```
DO NOT CREATE NAMES. PROVE TRANSITIONS.
```

**A new class, adapter, or rule is FORBIDDEN unless it answers:**

1. What domain does it delimit?
2. What transition does it prove?
3. What algebraic operation does it perform?
4. What identity does it preserve?
5. What residual does it produce on failure?
6. What existing canonical layer does it extend or replace?

**بالعربية:**

```
لا تنشئ أسماء. أثبت انتقالات.
```

**كل اسم جديد ممنوع حتى يثبت:**
1. مجاله
2. قياسه
3. عمليته الجبرية
4. هويته المحفوظة
5. بقاياه عند الفشل
6. علاقته بالطبقات القائمة

---

## 8. Mathematical Invariants

**Every change MUST preserve these mathematical invariants:**

### Identity-Trace Separation
```
Id(x) ≠ Trace(x)
Trace(x) ≠ Id(x)
```

### Evidence Monotonicity
```
Evidence may add Trace
Evidence MUST NOT consume Identity
```

### Source Identity Preservation
```
Id(output) ⊇ Id(inputs)
∀ input_id ∈ inputs: input_id ∈ output.identity_ids
```

### Rank Meet Semantics
```
Rank(composition) = min(Rank(component₁), Rank(component₂), ..., Rank(componentₙ))
```

### Residual Non-Concealment
```
Residuals MUST NOT be hidden
Residuals MUST NOT be silently discarded
Every failure → explicit Residual
```

### Boundary Preservation
```
BoundaryEvidence ≠ Identity
AlignmentEvidence ≠ Identity
```

### Potential-Only Safety
```
Candidate ≠ FinalMeaning
Candidate ≠ Hukm
Candidate ≠ RealityClaim
```

### No Layer Jump
```
Layer(n) MUST NOT produce output of Layer(n+k) where k > 1
without required gates and evidence from intermediate layers
```

---

## 9. Source-of-Truth Principle

**Every value or classification MUST have ONE canonical source.**

### Examples

**Abjad values:**
```
source = abjad_system.py
Rules MUST import/derive, NOT duplicate
```

**Morphological role:**
```
source = letter_role_taxonomy.py
Adapter and rules MUST use same source
```

**Sifat values:**
```
source = sifat_vector_registry.py
```

**Glyph classes:**
```
source = glyph_classification_registry.py
```

**Layer names:**
```
source = LAYER_REGISTRY.md or layer_registry.py
```

**This prevents drift:**
```
❌ rule says BAA=2
❌ adapter says BAA=3
❌ test doesn't notice (only sees missing wasf)

✓ Single source: abjad_system.py says BAA=2
✓ All components import from same source
✓ Conflict is impossible
```

---

## 10. Next Implementation Priority

**DO NOT implement new layers before completing governance:**

### Required Before New Layers

1. **PR-A: Architecture Control Frame** ✓ (completed)
2. **PR-B: Layer Registry** ✓ (completed)
3. **PR-C: Experimental-to-Canonical Map** ✓ (completed)
4. **PR-D: Source-of-Truth Registry** (needed)
5. **PR-E: Full Layer 2 Constitutional Planning** (needed)

### Then (After Governance Complete)

6. **PR-F: Full SifatVector** (extend from partial)
7. **PR-G: GlyphClassificationGate** (new)
8. **PR-H: ArabicMorphophonology** (new)
9. **PR-I: RoleDisambiguationGate** (new)
10. **PR-J: SyllableCandidate** (new)

**Rationale:**

Current problem is NOT absence of layers.
Current problem is name proliferation through duplication.
Governance MUST be complete before adding complexity.

---

## 11. Full Layer 2: SifatVector + GlyphClassificationGate

**After governance stabilizes, complete Layer 2.**

### Full SifatVector

```
SifatVector =
    VoicingAxis
  + MannerAxis
  + NasalityAxis
  + FricationAxis
  + ContinuancyAxis
  + EmphasisAxis
  + Residual
```

**Insufficient (current partial):**
```
voicing + manner + emphasis
```

**Required (full discrimination):**
```
Must distinguish:
  باء / ميم / واو / فاء
  سين / صاد / شين / زاي
  تاء / دال / طاء / ثاء / ذال / ظاء
```

### GlyphClassificationGate

**Before claiming a symbol is consonantal carrier, long vowel, hamza, or orthographic, we need:**

```
GlyphClassificationGate =
    CoreArabicLetter
  | HamzaSeatGlyph
  | MaddGlyph
  | WeakLetterGlyph
  | TatweelGlyph
  | OrthographicVariant
  | Punctuation
  | Boundary
  | Residual
```

**This prevents conflation of:**
```
ا as long vowel
ا as alif orthography
أ as hamza-on-alif
آ as madd/hamza/orthography
ى as alif maqsurah
ـ as tatweel (NOT letter)
```

---

## 12. ArabicMorphophonology

**After Full Layer 2, enter morphophonology:**

### Law

```
Consonant = carrier by potential
Vowel = operator by potential
Madd = extension by potential
Multi-role letter = undecided before RoleDisambiguation
```

### Operation

```
ArabicMorphophonology:
    GlyphClass
  + SoundCoordinate
  + SifatVector
  + RolePotential
  ⇀ CarrierOperatorCandidate
```

### Outputs

```
ConsonantalCarrierCandidate
VocalicOperatorCandidate
LongVowelExtensionCandidate
GlottalClosureCandidate
MorphologicalOperatorCandidate
Residual
```

---

## 13. RoleDisambiguationGate

**Solves the problem of multi-role symbols:**

```
Examples:
  سألتمونيها (all roles active)
  ب ف ك (consonants with potential vowel role in some theories)
  ا و ي (long vowels vs consonants vs orthography)
  همزة (glottal vs orthographic)
  مبنيات (invariant forms)
  أدوات (particles)
```

### Law

```
Nothing is stem-matter or augment or madd or particle BY DEFAULT.
Everything requires RoleDisambiguation.
```

### Operation

```
RoleDisambiguation:
    CandidateSet
  + Context
  + PatternDemand
  + LexicalEvidence
  + FariqAudit
  ⇀ LicensedRole | Residual
```

---

## 14. SyllableCandidate

**DO NOT build Syllable before completing:**

```
SlotCandidate ✓
+ Adjacency evidence
+ Boundary evidence
+ Phonotactic economy evidence
+ Closure readiness evidence
```

### Operation

```
BuildSyllable:
    SlotCandidate⁺
  + AdjacencyEvidence
  + BoundaryEvidence
  + EconomyEvidence
  ⇀ SyllableCandidate
```

**NOT:**
```
❌ SlotCandidate → SyllableCandidate (direct jump forbidden)
```

---

## 15. StemMatterTensor

**After syllable, we need matter mass:**

```
StemMatterTensor =
    OrderedConsonantalCarriers
  + RoleLicense
  + WeakLetterAudit
  + ZiyadahAudit
  + Residual
```

**DO NOT assume:**
```
❌ Any three letters = root
```

**Correct:**
```
✓ Three licensed consonantal carriers MAY form StemMatterCandidate
```

---

## 16. RootWeightAlgebra

**Weight does NOT operate on Unicode or raw letters.**
**Weight operates on licensed matter:**

```
ApplyWeight:
    StemMatterTensor
  + WeightOperator
  + VocalicProgram
  + ZiyadahProgram
  + Evidence
  ⇀ WordFormCandidate
```

### Laws

```
No weight without matter
No matter without RoleDisambiguation
No augment without stem preservation
No weight without R-coordinates
No meaning transition from weight alone
```

---

## 17. WordForm → LexicalMadlul

**After WordFormCandidate, do NOT jump to final meaning.**
**Jump to lexical signified:**

```
LexicalMadlulAlgebra:
    WordFormCandidate
  + LexicalEvidence
  + UsageDomain
  + PolysemyResidual
  ⇀ LexicalMadlulCandidate
```

**Here enters:**
```
Mutabaqah (correspondence)
Tadammun (inclusion)
Iltizam (entailment)
Ishtarak (polysemy)
Naql (transfer)
Majaz (metaphor)
Residuals
```

---

## 18. CompositionAlgebra

**After lexical signified, no ifadah yet. Need composition:**

```
CompositionAlgebra =
    SlotGeometry
  + AmilGeometry
  + RelationGeometry
  + AgreementGeometry
  + ReferenceGeometry
  + BoundaryGeometry
  + ResidualAudit
```

### Laws

```
No composition without slots
No slots without roles
No roles without amil or relation
No relation without license
No reference without referent or residual
No estimation without evidence
```

---

## 19. StyleTemplateAlgebra

**After composition:**

```
StyleTemplate =
    KhabarTemplate (declarative)
  | InshaTemplate (performative)
```

**Khabar:**
```
Subject to truth/falsehood evaluation later
```

**Insha:**
```
NOT subject to truth/falsehood in same way
Has force: request/call/command/prohibition/interrogation
```

---

## 20. IfadahCandidate

**Ifadah opens ONLY after:**

```
WordForm closed
LexicalMadlul candidate
Composition closed
Style template closed
Residuals non-blocking
```

### Operation

```
IfadahCandidate =
    ClosedComposition
  + ClosedStyle
  + ReferenceClosure
  + BoundaryClosure
  + ResidualAudit
```

---

## 21. HukmCandidate

**Hukm after Ifadah, NOT before:**

```
HukmCandidate =
    IfadahCandidate
  + Domain
  + Evidence
  + CorrespondenceCheck
  + CounterEvidenceAudit
  + Rank
  + Residual
```

---

## 22. Truth/Evidence/Reality Grounding

**This is NOT at the beginning of the project. This is at the END.**

```
EpistemicTruth(claim, domain) =
    Correspondence(claim, domain)
  ∧ ValidEvidence(claim)
  ∧ PreservedTrace(claim)
  ∧ ScopeSufficiency(claim)
  ∧ NoBlockingCounterEvidence(claim)
```

---

## 23. Final Project Vision

### Complete Formulation

```
المشروع يبني جبرًا عربيًا طبقيًا،
يبدأ من الرمز الرقمي،
ولا يسمح له أن يصير صوتًا أو حرفًا أو خانة أو مقطعًا أو جذعًا أو وزنًا أو كلمة أو معنى أو حكمًا
إلا بقياس محفوظ الهوية.
```

**Translation:**

> The project builds a layered Arabic algebra,
> starting from digital symbol,
> and does NOT allow it to become sound or letter or slot or syllable or stem or weight or word or meaning or hukm
> except through identity-preserving qiyas.

### Core Principles

```
Every layer is a domain.
Every domain has identity-preserving concepts.
Every concept becomes a rule only with evidence matched to Arabic reality.
Every transition is qiyas.
Every composition is partial algebraic operation.
Every failure is residual.
Every success is identity+rank+trace preserving candidate.
```

---

## 24. Integration with Governance Documents

**This document sits ABOVE:**

1. CANONICAL_ARCHITECTURE_CONTROL_FRAME.md — implements mathematical principles
2. LAYER_REGISTRY.md — catalogs domains
3. EXPERIMENTAL_TO_CANONICAL_MAP.md — prevents drift
4. NEXT_LAYER_DECISION_TREE.md — enforces discipline
5. AGENT_PR_CHECKLIST.md — validates compliance

**This document defines:**

- **What the project IS** (algebraic qiyas system)
- **What layers ARE** (domain boundaries)
- **What transitions ARE** (qiyas proofs)
- **What operations ARE** (partial algebra)
- **What success IS** (identity-preserving candidate)
- **What failure IS** (residual)

**Governance documents enforce how to implement this vision without drift.**

---

## 25. Authority

**This document has constitutional authority.**

**Every new layer, adapter, rule, or component MUST answer:**

1. What domain does it delimit?
2. What qiyas transition does it prove?
3. What algebraic operation does it perform?
4. What identity does it preserve?
5. What residual does it produce?
6. How does it integrate with the mathematical foundation?

**PRs that create names without proving transitions are REJECTED.**

**Constitutional mathematical foundation > code implementation.**

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Foundational constitutional document
**Authority:** Supreme (defines what the project IS)
