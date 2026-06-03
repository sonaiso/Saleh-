# SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT

> **Status:** Constitutional. Docs-only ratification of the
> SlotGeometry closure and demand catalogue contract. No code, no tests,
> no implementation are changed by this PR.
>
> **Track:** SlotGeometry only (Track A).
>
> **Authority basis:**
> `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §3 / §6 / §8 / §9 / §11,
> `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §3 / §4 / §5 / §9 / §11 / §12,
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §1 / §7 / §11,
> `CLAUDE.md` §0 / §4 / §5 / §7 / §8 / §14 / §19 / §20,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `RESET_CONSTITUTION.md` §1 / §3,
> `TERMINOLOGY_MAP.md` §2 / §3 / §4.
>
> **Governing one-liner:**
>
> ```
> Closure readiness is NOT final meaning.
> Minimal completion is a stopping condition, NOT semantic authority.
> ```
>
> ```
> جاهزية الإغلاق ليست معنى نهائيًا.
> الاكتمال الأدنى شرط توقف، لا سلطة دلالية.
> ```

---

## 0. Constitutional Position

**This document defines closure for SlotGeometry layer ONLY.**

**Current state:**
- Phase-1 single-slot pipeline is complete (PR #1–#28)
- SlotCandidate is the completed Phase-1 output
- PR #63 defined SlotGeometry alignment-trace contract
- PR #64 implemented SlotGeometry seed + extend skeleton
- PR #65 centralized SlotGeometry forbidden outputs
- LCNV Track B is closed by PR #68 and must NOT be touched

**This PR scope:**
- Add `docs/qiyas_core/SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT.md` ONLY
- Define what makes a SlotGeometryCandidate minimally complete
- Define closure concept at SlotGeometry layer
- Define Demand Catalogue for SlotGeometry
- Distinguish extension from closure
- Distinguish SlotGeometryCandidate from MinimalCompletionReadinessCandidate

**This PR does NOT:**
- Modify `src/qiyas_core/`
- Modify `tests/qiyas_core/`
- Modify `run_qiyas.py`
- Modify LCNV
- Modify billing/product
- Modify Logarithmic Measurement
- Implement IsMinimallyComplete runtime
- Implement MinimalCompletionReadinessCandidate runtime
- Wire runtime execution
- Add DalalahCandidate / WordCandidate / Meaning / Ifadah / Hukm
- Add new claim prefix, rank, or gate (unless reserved as future work only)

---

## 1. The Governing Principle

**Recursive extension answers HOW a SlotGeometryCandidate grows.**
(Already defined in `SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` §3.)

**Minimal complete closure answers WHEN a SlotGeometryCandidate may STOP growing as a complete candidate within the slot-geometry layer.**

This document fixes the **termination law** for SlotGeometry layer.

### 1.1 The Complementary Laws

```text
Extension law (§3 of alignment-trace contract):
  Extend(Gₙ, Sₙ₊₁, SlotBindingEvidenceₙ) → Gₙ₊₁

Closure law (this document):
  IsMinimallyComplete(Gₙ) → Bool
```

These laws are complementary, not duplicative:

| Question | Law | Operator |
|----------|-----|----------|
| How does SlotGeometry grow? | Extension | Extend(...) |
| When may SlotGeometry stop? | Closure | IsMinimallyComplete(...) |
| What does the next layer consume? | Both, jointly | A closed-by-candidacy SlotGeometryCandidate |

### 1.2 What Closure Is

```text
Closure is a STOPPING CONDITION.
Closure is NOT semantic authority.
Closure is NOT final meaning.
Closure is NOT dalalah.
Closure is NOT word formation.
Closure is NOT hukm.
Closure is NOT reality claim.
```

**Closure produces READINESS, never KNOWLEDGE:**

```text
IsMinimallyComplete(G) = True
  →  G is ready for next layer's consideration
  →  G does NOT become DalalahCandidate
  →  G does NOT become WordCandidate
  →  G does NOT become FinalMeaning
  →  G does NOT become HukmCandidate
  →  G does NOT become RealityClaim
```

**بالعربية:**

```
الإغلاق لا يُنتج معرفة.
الإغلاق يُنتج جاهزية.

الإغلاق ليس دلالة.
الإغلاق ليس كلمة.
الإغلاق ليس معنى نهائي.
الإغلاق ليس حكم.
الإغلاق ليس ادعاء واقع.
```

---

## 2. Extension vs. Closure — The Critical Distinction

**Extension** and **closure** are DIFFERENT proof obligations:

### 2.1 Extension (Growth)

**Question:** Can I add one more SlotCandidate to this SlotGeometryCandidate?

**Answer:** Extension law (alignment-trace contract §3)

**Inputs:**
- Previous: SlotGeometryCandidate(length = n)
- New unit: SlotCandidate
- Binding: SlotBindingEvidence

**Output:**
- SlotGeometryCandidate(length = n+1) | BlockedSlotGeometryCandidate | DeferredSlotGeometryCandidate

**Gates checked:**
- Same INTRA_UTTERANCE segment
- ordered_after
- adjacent_or_licensed_distance
- no whitespace boundary crossing
- no punctuation boundary crossing
- previous geometry remains valid
- new slot satisfies SlotCandidate contract
- rank meet is valid
- identity preservation
- trace preservation
- residual preservation
- no blocking difference

### 2.2 Closure (Termination)

**Question:** Can this SlotGeometryCandidate STOP growing and become a minimally complete candidate within the slot-geometry layer?

**Answer:** Closure law (this document §3)

**Input:**
- SlotGeometryCandidate(length = n)

**Output:**
- Bool (True = minimally complete, False = must continue extending or remain non-terminal)

**Conditions checked (ALL EIGHT MANDATORY):**
1. Licensed beginning
2. Licensed ending
3. All internal bindings are licensed
4. No open demand remains (SlotGeometry Demand Catalogue)
5. No blocking difference is present
6. Residuals are preserved
7. Rank remains above NO_EVIDENCE
8. Output remains CandidateOnly

### 2.3 The Dependency

```text
Closure DEPENDS ON extension history.

You cannot check closure without first having:
  - A licensed Seed (extension base case)
  - Zero or more licensed Extend steps (extension growth)

Only AFTER extension produces a SlotGeometryCandidate(n)
can closure check whether it is minimally complete.

Extension is the CONSTRUCTION law.
Closure is the TERMINATION law.
```

**Critical non-identities:**

```text
SlotGeometryExtend ≠ IsMinimallyComplete
SlotBindingEvidence ≠ MinimalCompletionReadiness
Growing ≠ Stopping
n → n+1 ≠ "n is complete"
```

---

## 3. The Eight Closure Conditions for SlotGeometry

A `SlotGeometryCandidate(n)` is **minimally complete** iff **ALL EIGHT** of the following hold simultaneously:

### 3.1 Licensed beginning

```text
The first SlotCandidate in the geometry was admissible as a start
under a SlotGeometry beginning rule.
```

**For length = 1 (Seed case):**
- The single SlotCandidate was licensed as both beginning AND ending

**For length > 1:**
- The first SlotCandidate (position: initial) was licensed as a beginning under a SlotGeometry beginning rule
- The beginning rule must have produced evidence: `gate:beginning:licensed`

**Witness:**
- Claim shape: `gate:beginning:licensed` (public name)
- Canonical grammar: `وادي:beginning:licensed` (per TERMINOLOGY_MAP.md §4)
- Effective cause: `effective_cause:slot_geometry_beginning:{reason}:verified`

**This condition ensures:**
- No SlotGeometry starts arbitrarily
- Beginning must be explicitly licensed
- Seed step must produce beginning license (trivial witness when length = 1)

### 3.2 Licensed ending

```text
The last SlotCandidate in the geometry was admissible as a terminus
under a SlotGeometry ending rule.
```

**For length = 1 (Seed case):**
- The single SlotCandidate was licensed as both beginning AND ending

**For length > 1:**
- The last SlotCandidate (position: terminal) was licensed as an ending under a SlotGeometry ending rule
- The ending rule must have produced evidence: `gate:ending:licensed`

**Witness:**
- Claim shape: `gate:ending:licensed`
- Canonical grammar: `وادي:ending:licensed`
- Effective cause: `effective_cause:slot_geometry_ending:{reason}:verified`

**This condition ensures:**
- No SlotGeometry stops arbitrarily
- Ending must be explicitly licensed
- Terminal position alone is NOT sufficient for closure

**Note:** A beginning rule and an ending rule MAY coincide in degenerate single-unit closures (Seed case).

### 3.3 All internal bindings are licensed

```text
For every Extend step that produced this SlotGeometryCandidate,
the binding was licensed under SlotGeometry per-extend gate policy.
```

**Checked:**
- Every `Extend` invocation in construction history (read from canonical trace)
- The binding evidence satisfied the conjunctive six-gate predicate:
  - CAUSE ∧ CONDITION ∧ OBSTACLE ∧ VALIDITY ∧ CORRUPTION ∧ NULLITY
- Produced an accepted (not blocked, not deferred) extension

**This condition is inherited from:**
- Alignment-trace contract §6 / §7
- Recursive extension contract §7

**Re-checked at closure time to ensure:**
- No historically-deferred binding is silently admitted
- All extension steps remain valid at closure time

### 3.4 No open demand remains

```text
The SlotGeometryCandidate carries no open demand on any of its units.
```

**This is the ONLY layer-specific condition.**

**Definition:**
An *open demand* on a SlotGeometry is any unsatisfied admissibility obligation that the slot-geometry layer's own contract requires before the geometry may be offered to a later layer.

**The SlotGeometry Demand Catalogue** (§4 of this document) is the finite list of demands that must ALL be discharged.

**Every entry in the catalogue must be discharged for IsMinimallyComplete to return True.**

**Important distinctions:**
```text
Open demand ≠ blocking difference
  (Open demand is incomplete but not invalid)

Open demand ≠ deferral
  (Deferral blocks progress; open demand defers closure only)

Demand Catalogue ≠ final meaning
  (Catalogue is admissibility checklist, not semantic content)
```

### 3.5 No blocking difference is present

```text
The SlotGeometryCandidate carries no blocking difference:* claim
on any of its units or on any of its construction-history evidence sets.
```

**A blocking difference is:**
- Any `difference:` claim (canonical: `فارق:`) that invalidates:
  - A unit (SlotCandidate)
  - A binding (SlotBindingEvidence)
  - The overall geometry

**Checked:**
- Anywhere in the geometry's witnessable trace
- On any consumed SlotCandidate
- On any SlotBindingEvidence
- On the SlotGeometryCandidate itself

**Result:**
- Closure is FORBIDDEN whenever ANY blocking difference is present
- Even one `فارق:{diff}:present` blocks closure

**This condition enforces:**
- CLAUDE.md §4 invariant 5 (invalidating difference blocks licensing)
- Alignment-trace contract §6.4 (blocking difference annihilation)

### 3.6 Residuals are preserved

```text
SlotGeometryCandidate.residuals ⊇ union of all residuals from:
  - Seed SlotCandidate
  - Every Extend SlotCandidate
  - Every SlotBindingEvidence
  - Every construction step
```

**Enforces:**
- CLAUDE.md §4 invariant 7 (residuals must not be hidden or silently discarded)
- Alignment-trace contract §6.3 (residual preservation)
- Recursive extension contract §7.3

**Checked at closure:**
- No residual may be hidden to claim closure
- Any blocking or deferring residual produced during construction MUST survive into SlotGeometryCandidate.residuals
- Kernel's `defer:` prefix and any gate-failure residual are explicitly in scope

**Result:**
- Closure MAY NOT be claimed by hiding residuals
- All residuals remain auditable

### 3.7 Rank remains above NO_EVIDENCE

```text
SlotGeometryCandidate.rank > NO_EVIDENCE
```

**Rank lattice** (per TERMINOLOGY_MAP.md §2):
```text
NO_EVIDENCE
  < FORMAL_STRUCTURE
  < ANALOGICAL
  < DIRECT_HEARING
  < INDIVIDUAL_REPORT
  < MASS_TRANSMISSION
```

**Rank calculation** (per alignment-trace contract §6.2):
```text
rank_out = min(rank(inputs), rank(binding), rank(rule))
```

**Closure requirement:**
- The meet must produce rank > NO_EVIDENCE
- If ANY input, binding, or rule has rank = NO_EVIDENCE, closure is forbidden

**If rank = NO_EVIDENCE:**
- SlotGeometryCandidate is well-formed as a geometry
- SlotGeometryCandidate is NOT closed
- SlotGeometryCandidate must either:
  - Gather more evidence (raising the meet), OR
  - Remain a non-terminal candidate

### 3.8 Output remains CandidateOnly

```text
SlotGeometryCandidate.output_flags ⊇ {CandidateOnly}

AND

SlotGeometryCandidate.output_flags ∩ {HukmCandidate, RealityClaim,
  FinalMeaning, FinalCaseJudgment, DalalahCandidate, WordCandidate} = ∅
```

**Closure does NOT lift CandidateOnly:**
- A closed-by-candidacy SlotGeometry is STILL a candidate
- A closed SlotGeometry is NOT a verdict
- A closed SlotGeometry is NOT final meaning
- A closed SlotGeometry is NOT dalalah
- A closed SlotGeometry is NOT a word
- A closed SlotGeometry is NOT hukm
- A closed SlotGeometry is NOT reality claim

**Enforces:**
- CLAUDE.md §4 invariant 9 (potential candidates must not become final judgments)
- Alignment-trace contract §6.5 (CandidateOnly safety)
- Alignment-trace contract §9 (forbidden outputs)

**Checked at closure:**
- Output flag set is inspected
- No Extend history may have leaked a final-judgment flag onto SlotGeometryCandidate

---

## 4. SlotGeometry Demand Catalogue

**This is the layer-specific Demand Catalogue for SlotGeometry layer.**

**Status:** Initial catalogue. Future PRs may extend but NOT weaken.

### 4.1 What a Demand Is

Per `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §4:

```text
A demand is:
  - Declared by the layer's own contract (this document)
  - Discharged by a layer-specific licensed step that records an
    effective_cause:demand_discharged:verified claim
  - NOT a blocking difference (demand is incomplete, not invalid)
  - NOT a deferral (demand defers closure only, not extension)
  - Finite and enumerable
```

### 4.2 SlotGeometry Demands (Initial Catalogue)

**Demand 1: All carrier bindings are explicit**

```text
Every haraka in every SlotCandidate must have an explicit
CarrierBindingCandidate with binding evidence preserved in trace.
```

**Discharge witness:**
- `effective_cause:carrier_binding_explicit:verified`
- Presence of `alignment_ref` in trace_ids (per alignment-trace contract §2.2)

**Violation:**
- `defer:carrier_binding_implicit:present` (blocks closure)

**Rationale:**
- SlotGeometry cannot close with orphan harakas
- Carrier binding must be proven, not assumed

---

**Demand 2: No orphan marks**

```text
No haraka, shadda, tanwin, or other mark may be unbound to a carrier.
```

**Discharge witness:**
- `effective_cause:all_marks_bound:verified`
- Every mark has corresponding CarrierBindingCandidate

**Violation:**
- `defer:orphan_mark:present` (blocks closure)
- `defer:haraka_without_carrier:present`
- `defer:shadda_without_carrier:present`

**Rationale:**
- Orphan marks indicate incomplete slot structure
- SlotGeometry requires all marks to have licensed carriers

---

**Demand 3: Geometric positions are consistent**

```text
All geometric positions (isolated, initial, medial, terminal) must be
consistent with the geometry's length and construction history.
```

**Discharge witness:**
- `effective_cause:geometric_positions_consistent:verified`

**Violations:**
- `defer:position_inconsistency:present` (medial before initial)
- `defer:terminal_before_medial:present`
- `defer:isolated_in_multi_slot:present`

**Rationale:**
- Geometric positions are structural (per alignment-trace contract §4)
- Inconsistent positions indicate malformed geometry

---

**Demand 4: No unresolved boundary crossings**

```text
No SlotBindingEvidence may have deferred a boundary-crossing check
without resolution.
```

**Discharge witness:**
- `effective_cause:boundaries_resolved:verified`
- All boundary evidence from ConditionedTypedSequence is accounted for

**Violations:**
- `defer:boundary_crossing_unresolved:present`
- `defer:whitespace_boundary_deferred:present`
- `defer:punctuation_boundary_deferred:present`

**Rationale:**
- SlotGeometry operates in INTRA_UTTERANCE context
- Boundary crossings must be resolved before closure

---

**Demand 5: Residual preservation is complete**

```text
All residuals from construction history are preserved in
SlotGeometryCandidate.residuals.
```

**Discharge witness:**
- `effective_cause:residuals_complete:verified`
- Audit trail shows no residual was dropped

**Violation:**
- `defer:residual_dropped:present` (blocks closure)

**Rationale:**
- This overlaps with §3.6 but is explicitly catalogued
- Residual hiding is a constitutional violation

---

### 4.3 Catalogue Properties

**Finite:**
- The catalogue has exactly 5 demands initially
- Future PRs may add demands but NOT remove them without constitutional amendment

**Conjunctive:**
- ALL demands must be discharged
- Discharging 4 out of 5 is NOT sufficient

**Layer-specific:**
- This catalogue applies ONLY to SlotGeometry layer
- WordGeometry / SentenceGeometry / etc. will have their own catalogues

**Not portable:**
- SlotGeometry demands do NOT apply to higher layers
- Higher layers must define their own demand catalogues

### 4.4 Discharge Semantics

**Discharge is NOT automatic:**
- Demands must be explicitly checked
- Discharge must produce evidence claim
- Evidence must be preserved in trace

**Discharge is cumulative:**
- Once discharged, a demand stays discharged
- Re-extension does NOT re-open discharged demands (unless new violation introduced)

**Discharge is auditable:**
- Discharge evidence appears in trace
- Discharge can be verified by later layers

### 4.5 Demand vs. Blocking Difference

**Critical distinction:**

```text
Demand = incomplete but valid
  → Closure is deferred until discharge
  → Extension may continue
  → Geometry remains valid

Blocking difference = invalid
  → Extension is blocked
  → Closure is forbidden
  → Geometry is blocked/deferred
```

**Examples:**

```text
Open demand: "carrier binding not yet explicit"
  → Geometry is valid but incomplete
  → Closure deferred
  → Extension may provide missing binding

Blocking difference: "فارق:incompatible_binding:present"
  → Geometry is invalid
  → Closure forbidden
  → Extension blocked
```

---

## 5. Difference Between SlotGeometryCandidate and MinimalCompletionReadinessCandidate

**These are DIFFERENT concepts:**

### 5.1 SlotGeometryCandidate

**What it is:**
- The ONLY admissible output of SlotGeometryQiyas (per alignment-trace contract §9)
- Produced by Seed or Extend (per alignment-trace contract §3)
- Has length n (where n ≥ 1)
- Has construction_mode ∈ {"seed", "extension"}
- Carries identity_ids, trace_ids, rank, residuals, evidence
- Remains CandidateOnly always

**When it exists:**
- After ANY licensed Seed or Extend
- Does NOT require closure

**Status:**
- May be closed (IsMinimallyComplete = True)
- May be non-terminal (IsMinimallyComplete = False)
- Both are valid SlotGeometryCandidates

**Algebraic role:**
- SlotGeometryCandidate is the OUTPUT TYPE of SlotGeometryQiyas

### 5.2 MinimalCompletionReadinessCandidate

**What it is:**
- A FUTURE-RESERVED concept name ONLY (per alignment-trace contract §9)
- NOT an admissible output of SlotGeometryQiyas under current contract
- NOT implemented in this PR
- NOT authorized by this PR

**If it were to exist (future work):**
- It would represent a SlotGeometryCandidate for which IsMinimallyComplete = True
- It would carry additional closure evidence
- It would still be CandidateOnly (NOT final meaning)
- It would still NOT produce DalalahCandidate / WordCandidate / Hukm

**Status:**
- Reserved name only
- Requires separate constitutional contract PR before implementation
- May never be implemented if not needed

**Algebraic role (if implemented):**
- Would be a METADATA FLAG or EVIDENCE ANNOTATION on SlotGeometryCandidate
- Would NOT be a separate candidate type (unless future contract explicitly ratifies split)

### 5.3 The Relationship

```text
SlotGeometryCandidate is the geometry itself.

IsMinimallyComplete(SlotGeometryCandidate) is a PREDICATE over that geometry.

MinimalCompletionReadinessCandidate (future reserved) would be:
  - Either: a metadata flag on SlotGeometryCandidate, OR
  - Or: a separate type wrapping SlotGeometryCandidate with closure evidence

  But this is NOT decided yet and requires future contract.
```

**Current state:**

```text
SlotGeometryQiyas produces: SlotGeometryCandidate only

IsMinimallyComplete checks: SlotGeometryCandidate → Bool

MinimalCompletionReadinessCandidate: NOT IMPLEMENTED, reserved name only
```

### 5.4 Why This Distinction Matters

**Prevents confusion:**
- Extension produces SlotGeometryCandidate
- Closure checks SlotGeometryCandidate
- Closure does NOT produce a new type (unless future contract says so)

**Prevents overreach:**
- SlotGeometryCandidate is output type (fixed by alignment-trace contract §9)
- MinimalCompletionReadinessCandidate is future reserved concept (not output type yet)
- No implementation may create MinimalCompletionReadinessCandidate without constitutional amendment

**Preserves constitutional discipline:**
- Naming is controlled
- New types require contracts
- Future work is reserved but not authorized

---

## 6. Closure Does NOT Produce Dalalah, Word, Meaning, Ifadah, or Hukm

**These are constitutional prohibitions:**

### 6.1 What Closure Does NOT Produce

```text
IsMinimallyComplete(SlotGeometryCandidate) → Bool

It does NOT produce:
  ❌ DalalahCandidate
  ❌ WordCandidate
  ❌ LafzCandidate
  ❌ FinalMeaning
  ❌ MeaningCandidate
  ❌ IfadahCandidate
  ❌ HukmCandidate
  ❌ RealityClaim
  ❌ FinalCaseJudgment
  ❌ SentenceCandidate
  ❌ ParagraphCandidate
  ❌ DiscourseGeometryCandidate
  ❌ TextGeometryCandidate
```

### 6.2 What Closure DOES Produce

```text
IsMinimallyComplete(SlotGeometryCandidate) = True
  →  READINESS for next layer's consideration
  →  NOT promotion to next layer
  →  NOT semantic content
  →  NOT linguistic knowledge
  →  NOT meaning derivation
  →  NOT hukm inference
```

**The ONLY effect of closure:**

```text
A closed SlotGeometryCandidate becomes admissible as a consumable
for the strictly next licensed layer's own admission contract.
```

**What "next layer" means:**
- NOT yet defined (no contract exists)
- NOT WordCandidate directly (requires separate contract)
- NOT DalalahCandidate directly (requires separate contract)
- NOT any higher layer without its own consumption contract

### 6.3 Why This Prohibition Is Critical

**Prevents layer jumping:**
```text
SlotGeometry → Word (forbidden without intermediate contracts)
SlotGeometry → Meaning (forbidden)
SlotGeometry → Hukm (forbidden)
```

**Preserves algebraic discipline:**
```text
Every layer has its own admission contract.
No layer produces the output of a later layer.
Closure is NOT promotion.
```

**Enforces constitutional authority:**
```text
CLAUDE.md §4 invariant 10: No layer may produce the final output of a
later layer without the required gate and evidence.

CLAUDE.md §19 forbidden changes:
  SlotCandidate → FinalMeaning (forbidden)
  SlotCandidate → HukmCandidate (forbidden)
  SlotCandidate → RealityClaim (forbidden)

Same applies to SlotGeometryCandidate.
```

### 6.4 Closure Is a Stopping Condition, Not Semantic Authority

**Closure asks:**
```text
"Is this SlotGeometry structurally complete within its layer?"
```

**Closure does NOT ask:**
```text
"What does this SlotGeometry mean?"
"What word does this form?"
"What hukm does this imply?"
"What reality does this claim?"
```

**Those are DIFFERENT proof obligations for FUTURE layers.**

---

## 7. No LCNV Use in SlotGeometry Closure

**LCNV Track B is closed by PR #68.**

**SlotGeometry closure MUST NOT:**
- Import from `src/qiyas_core/lcnv.py`
- Use LCNV pack() / unpack()
- Use GateStateBundle
- Use EncodedStateProjection
- Integrate SlotGeometry with LCNV

**Rationale:**
- LCNV is Track B
- SlotGeometry is Track A
- PR #68 closed Track B temporarily
- No track mixing without explicit maintainer approval

**Per LCNV_MINIMAL_RUNTIME_STABILIZATION_CLOSURE.md:**

```text
This closure prevents:
  ❌ LCNV integration with SlotGeometry (Track A)
  ❌ Unauthorized LCNV expansion without explicit maintainer approval
```

**SlotGeometry closure is orthogonal to LCNV:**
- SlotGeometry closure uses IsMinimallyComplete predicate
- SlotGeometry closure uses Demand Catalogue
- SlotGeometry closure does NOT compress to numeric values
- SlotGeometry closure remains in qiyas algebraic domain

---

## 8. No Billing/Product Logic in qiyas_core

**Billing/product is a separate architectural layer.**

**SlotGeometry closure MUST NOT:**
- Import from `docs/product/` or any billing modules (if they exist in src/)
- Consult subscription tiers
- Alter closure based on payment status
- Integrate with commercial access logic

**Rationale:**
- qiyas_core is epistemological engine (truth-seeking)
- product/billing is commercial access layer
- Per billing constitutional separation (if documented):
  ```text
  الدفع يفتح الوصول، لكنه لا يغيّر الحقيقة
  (Payment opens access but does not alter truth)
  ```

**SlotGeometry closure must be:**
- Identical for all users with identical inputs
- Independent of subscription tier
- Independent of payment status
- Independent of commercial considerations

**Constitutional law:**
```text
Free and Enterprise tiers must produce identical IsMinimallyComplete
results for identical SlotGeometryCandidates.

Closure is analytical, not commercial.
```

---

## 9. Future Implementation Phases

**This contract authorizes ZERO implementation.**

**Future work (requires separate PRs with maintainer approval):**

### Phase 1: Beginning/Ending Rules (Not Authorized)

```text
Implement SlotGeometry beginning rule
Implement SlotGeometry ending rule
Add tests proving beginning/ending licensing
Update SlotGeometryQiyas to check §3.1 and §3.2
```

**Required before:**
- Any closure checking

**Blocked until:**
- This contract merges
- Maintainer approves beginning/ending rule PR

---

### Phase 2: Demand Catalogue Runtime (Not Authorized)

```text
Implement Demand Catalogue checker
Add tests for all 5 demands in §4.2
Add discharge evidence producers
Update SlotGeometryQiyas to check §3.4
```

**Required before:**
- Full closure checking

**Blocked until:**
- Phase 1 complete
- Maintainer approves demand catalogue PR

---

### Phase 3: IsMinimallyComplete Adapter (Not Authorized)

```text
Implement IsMinimallyComplete predicate
Check all 8 conditions from §3
Add constitutional tests (minimum 8, one per condition)
Wire to SlotGeometryQiyas
```

**Required before:**
- Any closure in runtime

**Blocked until:**
- Phase 1 and 2 complete
- Maintainer approves closure adapter PR

---

### Phase 4: Closure Integration (Not Authorized)

```text
Update run_qiyas.py to call IsMinimallyComplete
Add closure traces to output
Add closure evidence to candidates
Update documentation with runtime examples
```

**Required before:**
- Closure appears in user-visible output

**Blocked until:**
- Phase 1, 2, and 3 complete
- Maintainer approves closure integration PR

---

### Phase 5: MinimalCompletionReadinessCandidate (Not Authorized, May Never Happen)

```text
IF maintainer decides MinimalCompletionReadinessCandidate is needed:
  Open constitutional contract PR
  Decide if it's metadata flag or separate type
  Define what it adds beyond SlotGeometryCandidate
  Get constitutional approval
  THEN implement
```

**This is OPTIONAL future work:**
- May never be implemented
- Requires separate constitutional contract
- Not authorized by this PR

---

## 10. Forbidden Outputs

**SlotGeometry closure checking MUST declare these in forbidden_outputs:**

```text
DalalahCandidate
WordCandidate
LafzCandidate
FinalMeaning
MeaningCandidate
IfadahCandidate
HukmCandidate
RealityClaim
FinalCaseJudgment
SentenceCandidate
ParagraphCandidate
DiscourseGeometryCandidate
TextGeometryCandidate
MinimalCompletionReadinessCandidate (until constitutional contract ratifies it)
```

**Closure checking MAY produce:**
```text
Bool (IsMinimallyComplete result)
Evidence claims (discharge witnesses)
Trace entries (closure audit trail)
```

**Closure checking MUST NOT produce:**
```text
New candidate types
Promoted candidates
Semantic interpretations
Hukm inferences
Reality claims
```

---

## 11. Relationship to MINIMAL_COMPLETE_CLOSURE_CONTRACT.md

**This document is a SPECIALIZATION of the general closure law.**

**General closure contract defines:**
- The 8 universal conditions (§3)
- What closure is (§1)
- Relationship to extension (§2)
- What "open demand" means (§4)
- Forbidden outputs (§11)

**This SlotGeometry closure contract defines:**
- How the 8 conditions apply at SlotGeometry layer (§3)
- SlotGeometry-specific Demand Catalogue (§4)
- SlotGeometry-specific forbidden outputs (§10)
- SlotGeometry-specific future work (§9)

**Authority relationship:**

```text
MINIMAL_COMPLETE_CLOSURE_CONTRACT.md (general law)
  ↓ specializes
SLOT_GEOMETRY_CLOSURE_DEMAND_CONTRACT.md (this document, SlotGeometry instance)
```

**Both are binding:**
- General law provides framework
- This document provides layer-specific instance
- Future layers will need their own specialization documents

---

## 12. Relationship to SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md

**Alignment-trace contract (PR #63) defined:**
- Extension law (§3)
- SlotGeometryCandidate as output type (§9)
- Forbidden outputs (§9)
- Consumption surface (§1)
- Invariants (§6)

**This closure contract (PR #69) defines:**
- Termination law (§3)
- IsMinimallyComplete predicate (§1)
- Demand Catalogue (§4)
- Closure vs. extension distinction (§2)
- Future implementation phases (§9)

**Together they form:**
```text
Alignment-trace contract: HOW SlotGeometry grows
Closure contract: WHEN SlotGeometry stops

Both required for complete SlotGeometry behavior.
```

**Dependency:**
```text
This contract DEPENDS ON alignment-trace contract:
  - Consumes SlotGeometryCandidate (defined there)
  - Checks invariants (defined there)
  - Respects forbidden outputs (defined there)
  - Uses same claim grammar (defined there)
```

---

## 13. Glossary

| Term | Meaning |
|------|---------|
| Closure | The termination law; answers when a SlotGeometryCandidate may stop growing |
| Extension | The growth law; answers how a SlotGeometryCandidate grows |
| IsMinimallyComplete | The closure predicate; returns Bool |
| Demand Catalogue | The finite list of admissibility obligations that must be discharged before closure |
| Open demand | An unsatisfied admissibility obligation; defers closure but does not block extension |
| Discharge | Satisfying a demand with evidence claim |
| MinimalCompletionReadinessCandidate | Future-reserved concept name; not implemented; not authorized by this PR |
| Closed-by-candidacy | State of SlotGeometryCandidate for which IsMinimallyComplete = True; still CandidateOnly |
| Readiness | The single positive effect of closure; admissibility for next layer; NOT promotion |
| Licensed beginning | §3.1 condition; first slot must be admissible as start |
| Licensed ending | §3.2 condition; last slot must be admissible as terminus |
| Blocking difference | Invalidating فارق: claim; blocks closure (§3.5) |
| Residual preservation | §3.6 condition; all residuals from construction history preserved |
| Rank > NO_EVIDENCE | §3.7 condition; closure requires evidentiary support |
| CandidateOnly | §3.8 condition; closure does not lift this flag |

---

## 14. Status and Authority

**Document status:**
- Constitutional contract
- Docs-only (no implementation)
- SlotGeometry-specific
- Specializes MINIMAL_COMPLETE_CLOSURE_CONTRACT.md

**Authority:**
- Once merged, this is the constitutional reference for:
  - Any future SlotGeometry closure implementation
  - Any future IsMinimallyComplete adapter
  - Any future beginning/ending rules
  - Any future Demand Catalogue implementation

**Does NOT authorize:**
- Implementation of any component described here
- Creation of MinimalCompletionReadinessCandidate
- Integration with LCNV
- Integration with billing/product
- Any code/test/runtime changes

**Each implementation component requires:**
- Separate PR
- Maintainer approval
- Constitutional compliance check
- Tests proving all 8 conditions

---

## 15. Non-Goals

**This document does NOT:**

- Modify `src/qiyas_core/`
- Modify `tests/qiyas_core/`
- Modify `run_qiyas.py`
- Modify `experimental/`
- Modify LCNV
- Modify billing/product documentation
- Modify Logarithmic Measurement
- Implement IsMinimallyComplete runtime
- Implement beginning/ending rules
- Implement Demand Catalogue runtime
- Implement MinimalCompletionReadinessCandidate
- Wire any runtime execution
- Add DalalahCandidate, WordCandidate, Meaning, Ifadah, or Hukm concepts
- Add new claim prefix, rank, or gate (beyond what's already canonical)
- Authorize any future PR (each requires separate approval)
- Define next layer after SlotGeometry (requires separate contract)
- Define WordCandidate admission contract (requires separate contract)

---

## 16. Forbidden Jumps

**These jumps remain constitutional violations:**

```text
SlotGeometryCandidate → DalalahCandidate (forbidden)
SlotGeometryCandidate → WordCandidate (forbidden)
SlotGeometryCandidate → FinalMeaning (forbidden)
SlotGeometryCandidate → HukmCandidate (forbidden)
SlotGeometryCandidate → RealityClaim (forbidden)

IsMinimallyComplete(G) = True → DalalahCandidate (forbidden)
IsMinimallyComplete(G) = True → WordCandidate (forbidden)
IsMinimallyComplete(G) = True → FinalMeaning (forbidden)

Closure → Semantic authority (forbidden)
Closure → Promotion (forbidden)
Closure → Knowledge (forbidden)
```

**Closure produces ONLY:**
```text
Readiness (NOT promotion)
Bool (NOT meaning)
Evidence (NOT hukm)
```

---

**End of document.**

**This is a constitutional contract.**
**No implementation is authorized by this PR.**
**Track A only.**
**LCNV (Track B) must NOT be touched.**
