# ARCHITECTURE LEVELS — Saleh/Qiyas

> **مستويات المعمار — الفصل الرباعي**
>
> **Purpose:** fix, once, the separation of four distinct levels so that the
> project never confuses them again. This is the *map*; every other governance
> document is *derived from* it.
>
> **The four levels are not interchangeable:**
>
> ```
> Theory  ≠  Constitution  ≠  Specification  ≠  Implementation
> ```
>
> **The biggest risk this prevents:**
> - a **Theory** degrading into a *fields file*, and
> - a **Constitution** degrading into *code*.
>
> **Status:** governance map only. No code, no technical fields, no behavior
> change. It introduces no layer and no registry change (registry stays 19, no
> P13, P12 terminal).

---

## 1. The four levels

| Level | Question it answers | What it MUST NOT become |
|-------|--------------------|--------------------------|
| **1 — Theory** | *Why does the idea exist?* | a fields file / a data schema |
| **2 — Constitution** | *What are the governing rules?* | code / a list of struct fields |
| **3 — Specification** | *What is the published technical contract (the fields)?* | a re-statement of theory or rules |
| **4 — Implementation** | *How is it realized in code?* | a source of new rules or new theory |

Flow of authority is top-down; a lower level **applies** a higher one, it never
**redefines** it:

```
Theory          →  applied by  →  Constitution
Constitution    →  applied by  →  Specification
Specification   →  realized by →  Implementation
```

> **بالعربية:** النظرية تقول لماذا؛ والدستور يقول ما القواعد؛ والـ Specification يقول
> ما الحقول التقنية المنشورة؛ والـ Implementation يحقّق ذلك في الكود. كل مستوى
> **يطبّق** الأعلى ولا **يعيد تعريفه**.

---

## 2. Level responsibilities

### Level 1 — Theory
Defines *what the project IS* (an identity-preserving proof algebra of licensed
qiyas transitions). It owns the mathematical invariants and the supreme law —
*DO NOT CREATE NAMES. PROVE TRANSITIONS.* It is **system-independent**: it does
not name files, fields, repos, or versions.

### Level 2 — Constitution
Applies the theory to a **specific system** as governing rules (what is allowed,
forbidden, gated; how identity/rank/trace/residuals must be treated). A
constitution is **not part of the theory** and **does not define fields**.

### Level 3 — Specification
The **published technical contract**: the concrete fields, types, and versioned
schema that cross a boundary between systems. A Specification is the only level
that lists fields. It is **versioned** (`v1`, `v2`, …) and is the *stable* artifact:
even a full rewrite of an implementation must keep an older Specification valid
(or publish a new version), without changing the theory.

### Level 4 — Implementation
The **code** of each system. It realizes a Specification and obeys its
Constitution and the Theory. It is **never** a source of new rules or new theory.

---

## 3. File mapping (locked)

| Level | Artifact | Lives in |
|-------|----------|----------|
| **1 Theory** | `PROJECT_MATHEMATICAL_FOUNDATION.md` | Qiyas (this repo) |
| **2 Qiyas Constitution** | `PROJECT_CONSTITUTION.md` | Qiyas |
| **2 Boundary Constitution** | `BOUNDARY_CONSTITUTION.md` *(to be drafted)* | Qiyas |
| **3 Boundary Specification** | `LICENSED_BOUNDARY_SPECIFICATION_v1.md` *(later)* | Qiyas (published) |
| **2 Consumer Constitution** | `CONSUMER_CONSTITUTION.md` *(later)* | **the consumer repo** (e.g. `hussein-root-2-sentence`), **not** Qiyas |
| **4 Implementations** | source code | `Qiyas`, `hussein-root-2-sentence`, future syntax / semantics … |

Notes:
- `PROJECT_CONSTITUTION.md` is the **Qiyas Constitution** — **not** the Theory.
  The Theory remains solely in `PROJECT_MATHEMATICAL_FOUNDATION.md`.
- `CONSUMER_CONSTITUTION.md` belongs to the **consumer**, so it is kept out of
  Qiyas and into the consuming project.

---

## 4. How systems relate (the published-boundary rule)

Just as **layers within a system never jump**, **systems never talk directly** —
they relate only through a **published, versioned Specification** of a boundary:

```
Internal Domain
        │
        ▼
Published Boundary Specification        (versioned: v1 → v2, theory unchanged)
        │
        ▼
Consumer Domain
```

- A **Domain** is a mathematical entity **inside the theory**. What is **published**
  between two systems is a **Specification**, not a Domain.
- The consuming system depends **only** on the Specification — never on the
  internal types of the producing system.
- This map applies to **any** Qiyas-derived project (morphology, syntax,
  semantics, …), not just one consumer.

---

## 5. Relationship to recorded decisions

This map is the parent of the handoff decisions already taken (kept here only as
pointers, not re-stated):

- **B-1** — a consumer inherits Qiyas's already-proved carriers; it does not
  re-derive them. (B-2 = explicit reconciliation, deferred.)
- **ADR-1 / ADR-2** — the boundary is an independent, versioned contract; no
  dependence on Qiyas internal types.
- **ADR-3 / ADR-4** — the published thing is a **Specification** (not a "Domain"
  and not a "Carrier"); four levels separated.
- **ADR-5** — the file mapping in §3.

The concrete fields of any boundary belong to **Level 3** (a Specification),
**never** here and **never** in a Constitution.

---

## 6. Derivation order

```
ARCHITECTURE_LEVELS.md   (this map — fix the split first)
        │
        ├── BOUNDARY_CONSTITUTION.md          (Level 2, next — rules only, no fields)
        │
        ├── LICENSED_BOUNDARY_SPECIFICATION_v1.md   (Level 3, later — the fields)
        │
        └── CONSUMER_CONSTITUTION.md          (Level 2, later — in the consumer repo)
```

---

**Document status:** governance map (Level 0 of organization, above all four
levels it describes). Subordinate to `PROJECT_MATHEMATICAL_FOUNDATION.md`.
**Behavioral effect:** none. No fields, no code, no registry change.
