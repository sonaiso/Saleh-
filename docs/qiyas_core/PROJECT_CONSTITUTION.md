# PROJECT CONSTITUTION — Saleh/Qiyas

> **دستور المشروع — النظام القياسي الجبري الطبقي للغة العربية**
>
> **Canonical governance document.** It begins from the *theoretical foundation*
> (§0) and the *licensed-transition law* (§K), and only then derives the
> *scientific identity* (§A) and the operational constitutions (§B–§J).
>
> **Authority:** This document is **subordinate to**
> [`PROJECT_MATHEMATICAL_FOUNDATION.md`](PROJECT_MATHEMATICAL_FOUNDATION.md) (v1.0),
> which is the **supreme** authority and defines *what the project IS*. Where any
> wording here is narrower or unclear, the Mathematical Foundation governs.
>
> **Scope note:** This is documentation/governance only. It introduces **no code
> or behavior change**, **no new layer**, and **no registry change**. The canonical
> registry remains **19 (P0–P12)**; **there is no P13**; **P12 is terminal**.

---

## THE SUPREME LAW (pinned)

> # DO NOT CREATE NAMES. PROVE TRANSITIONS.
> # لا تنشئ أسماء. أثبت انتقالات.

Everything below is an elaboration of this single law. The *scientific identity*
of the project (§A) is **a consequence** of §0 and §K — never their origin.

---

## §0 — Theoretical Foundation / الأساس النظري للمشروع *(First Origin)*

1. **The project is NOT an NLP / linguistic pipeline.**
2. **The project IS** an **identity-preserving proof algebra** that **licenses the
   transition of linguistic objects across domains by qiyas** (analogical proof).
3. **Each domain runs partial algebraic operations** — operations that do not
   always succeed.
4. **Identity, rank, trace, and residuals must be preserved and reported** at
   every step.
5. **Failure is residual, not silent failure.** Non-closure is surfaced
   explicitly, never hidden or discarded.

> المشروع يثبت انتقال الكائن اللغوي من مجال إلى مجال بقياس محفوظ الهوية، ثم يشغّله
> داخل كل مجال بعمليات جبرية جزئية، ولا يسمح بالنجاح إلا بدليل ورتبة وأثر، ولا يسمح
> بالفشل الصامت بل يخرجه كبقايا.

### Governing equation

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

### The five founding laws

```
Layer       = DomainBoundary
Transition  = QiyasProof
Composition = PartialAlgebraicOperation
Failure     = ResidualSet
Success     = Candidate(identity_ids, rank, trace_ids, residuals)
```

### The supreme law — obligations for every new name

A new **name / adapter / rule / layer is FORBIDDEN** unless it answers all six:

1. **What is its domain?** (what boundary does it delimit)
2. **What is its qiyas?** (what transition does it prove)
3. **What is its partial algebraic operation?**
4. **What identity does it preserve?**
5. **What residuals are produced on failure?**
6. **What existing layer / domain boundary does it relate to** (extend or replace)?

> لا تنشئ أسماء. أثبت انتقالات. — كل اسم جديد ممنوع حتى يثبت: مجاله، قياسه، عمليته
> الجبرية، هويته المحفوظة، بقاياه عند الفشل، وعلاقته بالطبقات القائمة.

### Mathematical invariants

```
Identity ≠ Trace            :  Id(x) ≠ Trace(x)
Evidence monotonicity       :  Evidence adds Trace; it MUST NOT consume Identity
Source identity preservation:  Id(output) ⊇ Id(inputs)
Rank meet semantics         :  Rank(composition) = meet/min over component ranks
Residual non-concealment    :  every Failure → explicit Residual (never silent)
Boundary separation         :  BoundaryEvidence  ≠ Identity
Alignment separation        :  AlignmentEvidence ≠ Identity
Potential-only safety       :  Candidate ≠ FinalMeaning, ≠ Hukm, ≠ RealityClaim
No layer jump               :  Layer(n) MUST NOT produce Layer(n+k>1) output
                               without the intermediate licensed gates and evidence
```

---

## §K — Licensed Transition Constitution / دستور الانتقال المرخّص *(Second Origin)*

Every domain transition `A → B` MUST carry the full qiyas structure:

```
QiyasTransition(A → B) =
    Asl                    (established source)
  + Far                    (determined target)
  + SharedIllah            (licensing cause)
  + EffectiveWasf          (effective attribute)
  + FariqAudit             (invalidating-difference negation)
  + Evidence
  + Rank
  + IdentityPreservation
  + Residual
```

### Governing law

The **Far** may be attached to the **Asl** only when **all** of the following hold:

- a **shared illah** exists,
- an **effective wasf** is present,
- the **invalidating fariq** is negated,
- **evidence** exists,
- **identity** is preserved.

Otherwise the transition MUST produce **residual / DEFER / BLOCK**. **Never guess.**

### Canonical example (classification is qiyas, not assumption)

```
UnicodeCandidate(U+0628) → TypedCodePoint
  Asl   : typed Arabic codepoint domain
  Far   : codepoint U+0628
  Illah : belongs_to_typed_domain
  Wasf  : is_arabic_letter
  Fariq : NOT haraka, NOT digit, NOT boundary
  ⟹ LetterCodePoint   — by evidence, not assumption
```

### Partial operation example

```
BindSlot:
    LetterIdentityCarrier
  × HarakaFunctionCarrier
  × PositionCarrier
  × AlignmentEvidence
  ⇀ SlotCandidate            (⇀ partial: does not always succeed)
```

**Failure residuals include:**

```
defer:alignment_missing
defer:position_missing
fariq:incompatible_binding
defer:insufficient_evidence
fariq:{difference}
```

**Success requires:**

```
preserved identity
established rank
preserved trace
no blocking residuals
```

---

## §A — Scientific Identity *(a consequence of §0 and §K — not an origin)*

Because the project is an algebraic qiyas proof system (§0) that admits no
transition without a licensed qiyas (§K), it **follows** that Qiyas / **Slot
Geometry Algebra** is a **formal, proof-relevant, potential-type analysis
framework**. It produces **auditable structural candidates** with the verdicts
**ACCEPT / DEFER / BLOCK**.

It MUST NOT claim to:

- solve Arabic,
- understand all meaning,
- produce final truth,
- produce final hukm,
- produce final tafsir.

**DEFER is a valid, safe result** — it is exactly the §K case of *“a qiyas whose
licensing conditions are not (yet) met.”*

---

## §B — Registry Constitution

- The canonical registry remains **19**.
- **P0–P12 only.**
- **No P13.**
- **P12 `IfadahCandidate` is terminal and opens nothing.**
- P12 is **not** final meaning, truth, hukm, tafsir, or final speech-act.
- **P3.1** and **P5.1** are **auxiliary non-registry passes**.
- **`ClosedCategoryReachabilityQiyas`** is **audit/carrier only**, **not** a
  registered LayerSpec.

---

## §C — Naming Constitution

- **`SlotCandidate` / “slot”** terminology is reserved for the **lowest
  letter/haraka cell layer only**.
- Higher units MUST use **typed candidate / geometry** terms (not “word slots” or
  “sentence slots”).
- **ف ع ل are weight (mīzān) symbols, not root letters.**

---

## §D — Hussein Integration Constitution

- Hussein is **proposer only, never authority**.
- Runtime MUST NOT call the Hussein analyzer.
- Runtime MUST NOT use subprocess to invoke Hussein.
- Runtime MUST NOT read Stage A fixtures.
- Runtime MAY consume **only committed, reviewed, static snapshot data** under
  `data/external_snapshots/`.
- Stage A is **capture / test / provenance only**.
- Snapshot evidence MUST be **manually reviewed** and **explicitly allowed for the
  target layer** (`allowed_feed_targets`).
- **Suspicious / quarantined / rejected / pending rows MUST NOT create ACCEPT.**
- Raw Hussein fields such as **role / case / i'rab / meaning MUST remain ignored**.

---

## §E — P5.1 Constitution

P5.1 may consume **only**:

- `word_kind`
- `closed_category`
- `verb_tense`
- `is_closed_compound`
- safe provenance markers

P5.1 MUST NOT consume:

- `legacy_root`, `legacy_wazn`
- role, case, i'rab
- relation, event
- meaning, Q&A, tafsir
- hukm, truth/reality

P5.1 output is **readiness / candidate-level only**:

- `MabniReadinessCandidate`
- `Mu'rabReadinessCandidate`
- `InflectionalClosureCandidate`

**No final `MabniJudgment` or `MurabJudgment`.**

---

## §F — P3.1 Constitution

- P3.1 **WeightPattern** is auxiliary non-registry.
- P3.1 currently extracts/aligns weight patterns from Qiyas structures.
- **P3.1 MUST NOT be wired to the Hussein snapshot until Step D is separately
  authorized.**
- If Step D happens:
  - Hussein **root** is **audit metadata only**.
  - Hussein **wazn** may be a **proposal hint only**.
  - P3.1 MUST NOT rewrite identity.
  - P3.1 MUST NOT treat `legacy_root` as final root.
  - P3.1 MUST NOT leak final root/weight judgment.

---

## §G — Exact-Surface / Normalization Constitution

- Current snapshot matching is **exact-surface**.
- **No blind harakat-stripping.**
- Do **not** collapse `مَكْتُوب` into `مكتوب`.
- Do **not** equate `هو` and `هُوَ` unless a **governed normalization layer** is
  authorized.
- Any normalization MUST be **explicit, test-covered, and safety-gated**.

---

## §H — Pronoun / Reference Policy

**Current owner policy (recorded):** standalone pronouns such as **`هو` are NOT
runtime-consumable** from the Hussein P5.1 snapshot, even if raw Hussein produced
them.

**Reason:** a standalone pronoun is **referential / indexical**. It lacks the
currently licensed **`SharedIllah`** and **`EffectiveWasf`** required to treat it
as a **context-free closed-category unit** in P5.1. It requires a **separate
governed reference / anaphora qiyas**.

Therefore **PR #195 correctly quarantines `هو` as `out_of_scope_pronoun` while
preserving provenance** (the raw surface `هو` and its ISM_MABNI origin are kept).

This is a direct application of:

- the **Licensed Transition Constitution (§K)** — missing illah/wasf → residual,
- **Candidate ≠ FinalMeaning**,
- **no layer jump**,
- **failure/residual must be explicit**.

---

## §I — Demo Constitution

The customer demo MUST show, understandably:

- **input**
- **structural result**
- **accepted / deferred / not reached**
- **source**
- **safety note**

Avoid raw internal terms unless the customer is technical. **Do not show `هو` as
accepted from Hussein.**

Preferred customer demo tokens:

```
مِن · إلى · على · هذا · الذي · الذين
كَتَبَ · يَقُولُ · مَكْتُوب
بَاعَ · صَامَ · مكتوب
```

---

## §J — Workflow Constitution

- **One PR per layer/phase.**
- **One prompt per phase.**
- The prompt covers **planning, implementation, testing, and report**.
- **No repeated readiness gates** unless there is a real blocker.
- **Commit / PR / merge are separate explicit approval gates.**
- **Do not merge without explicit authorization.**
- **Do not start Step D without separate authorization.**
- Always report **exact files, commit, PR, tests, invariants, and next step**.

---

## Constitutional ordering (summary)

```
§0  Theoretical Foundation         ← First Origin
§K  Licensed Transition            ← Second Origin
§A  Scientific Identity            ← consequence of §0 + §K
§B  Registry        §C  Naming     §D  Hussein
§E  P5.1            §F  P3.1        §G  Exact-Surface
§H  Pronoun/Ref     §I  Demo        §J  Workflow
```

> The scientific identity is **not** the root. The root is the theoretical
> foundation and the licensed-transition law. Everything else is derived.

---

**Document status:** canonical governance, subordinate to
`PROJECT_MATHEMATICAL_FOUNDATION.md` (supreme).
**Behavioral effect:** none (documentation/governance only).
**Invariants restated:** registry 19 · no P13 · P12 terminal · P3.1/P5.1 auxiliary
non-registry · no Hussein analyzer/subprocess/Stage-A at runtime · exact-surface
discipline · potential-only safety.
