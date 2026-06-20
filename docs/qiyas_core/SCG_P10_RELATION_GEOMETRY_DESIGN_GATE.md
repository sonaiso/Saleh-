# SCG-P10 RelationGeometry Design Gate

> **Type:** Descriptive **design-gate note** — *not* a constitution. It introduces
> no new layer, no new theory name, and does not rename the framework. It is
> **subordinate** to `RELATION_GEOMETRY_CONSTITUTION.md`, the canonical P10
> `LayerSpec` (`master_registry_seed.py`), `SENTENCE_GEOMETRY_CONSTITUTION.md`,
> and the P9 design gate/resolution. **Where this note and the canonical
> spec/code differ, the canonical spec/code wins.**

## 1. Status

- **P10 is not implemented.** No `RelationGeometryLayer` adapter, rule, or runtime
  exists; the P10 `LayerSpec` carries `status=LayerStatus.PLANNED` in the seed and
  reaches only `SPECIFIED` via `build_p10_specified_registry`.
- **P10–P12 remain SPECIFIED-only.** Implemented phases stop at P9
  (`build_p9_implemented_registry`). There is no `build_p10_implemented_registry`.
- **Freeze remains ACTIVE above P9.** No phase beyond SCG-P9 is `IMPLEMENTED`;
  registry count stays **19**.
- This note is **descriptive and subordinate** to the documents named above. It
  invents nothing.
- This note **authorizes no runtime, registry, schema, or test change**, and emits
  no P10 candidate. **A separate explicit authorization is required before any
  P10 implementation work.**

## 2. Boundary Question

What keeps `RelationGeometryCandidate` **structural relation geometry only** — the
geometric *possibility* of internal dependency among sentence components — and
prevents it from becoming i‘rab, case assignment, semantic relation, dalālah,
hukm, reality, or final interpretation?

## 3. Existing Answer from the P10 Specification

Summarized strictly from the existing `LayerSpec` (`master_registry_seed.py` §P10)
and `RELATION_GEOMETRY_CONSTITUTION.md`; nothing added:

- **Expected input:** direct origin `P9_SENTENCE_GEOMETRY` → `SentenceGeometryCandidate`.
  Required upstream conditions `sentence_geometry_established`, `relation_scope_closed`;
  minimum required fields `sentence_geometry_ref`, `relation_type_evidence`,
  `dependency_scope_evidence`.
- **Expected output name:** `RelationGeometryCandidate` — and nothing else
  (candidate-only; "إمكان هندسة علاقات", not a parse).
- **What P10 may open (if specified):** `target_boundary_opens = (irab_geometry_candidates,)`
  — opened as a **prior for SCG-P11**, never produced. It also
  `target_boundary_closes = (relation_geometry_candidates,)` — i.e., it closes the
  prior that P9 opened.
- **What P10 must not emit:** `forbidden_outputs = _ABSOLUTE_FORBIDDEN +
  (IrabCandidate, CaseJudgment, IfadahCandidate, IrabGeometryCandidate)`;
  `forbidden_changes = (assign_irab, assign_case, assign_ifadah)`;
  `forbidden_direct_next_layer_ids = (P12_IFADAH_SPEECH_FORCE,)`.
- **Forbidden outputs that already exist:** `_ABSOLUTE_FORBIDDEN =
  (HukmCandidate, RealityClaim, FinalMeaning)`, plus the P10-local guards above.
  `relation_type_conflict` is the invalidating difference; `relation_structure_blocked`
  is the blocker.

This note adds **no missing commitments** beyond what the spec states.

## 4. Permitted Inputs

P10 permitted inputs, narrowly (per the spec):

- accepted **P9 `SentenceGeometryCandidate`** traces (the only upstream path: `P9 → P10`);
- **preserved multi-unit identity** carried from P9 (`preserves_ids = sentence_geometry_identity`);
- **structural relation-geometry evidence only** — relation-type and dependency-scope
  evidence (تبعية، عطف، إبدال، توكيد as *geometric possibility*);
- ordering / adjacency / boundary evidence carried in the P9 trace;
- **residuals** carried forward explicitly (nothing hidden).

P10 must **not consume**: lexical meaning, semantic interpretation, i‘rab
assignment, case judgment, hukm, reality facts, or final syntax labels treated as
claims.

## 5. Permitted Output

The only permitted output is **`RelationGeometryCandidate`** (the canonical P10
output). It must be:

- candidate-only, potential-only ("إمكان", never a judgment);
- identity-preserving (`sentence_geometry_identity` preserved, not consumed);
- trace-separated (relation evidence lives in trace `T(c)`, never in identity `I(c)`);
- residual-preserving (underdetermination surfaced, not discarded);
- proof-relevant and **non-final**.

It must **not** be: i‘rab, case, semantic relation, dalālah, hukm, reality, or
final interpretation. Relations are *mapped* (`allowed_changes = map_internal_relations`);
no parse is closed.

## 6. Must-Not-Emit List

Exact canonical forbidden names already present in the P10 spec
(`forbidden_outputs` / `forbidden_changes`):

- `IrabGeometryCandidate` (SCG-P11)
- `IfadahCandidate` (SCG-P12)
- `IrabCandidate`
- `CaseJudgment`
- `HukmCandidate`
- `RealityClaim`
- `FinalMeaning`
- `assign_irab`, `assign_case`, `assign_ifadah` (forbidden changes)

Additionally requested as forbidden boundary targets but **not yet named as
constants in the P10 spec** — to be **confirmed against canonical spec before any
implementation**: `MeaningCandidate`, `DalalahCandidate` / dalālah judgment, and
"final syntax labels" as claims. The spec covers these in prose (§6 "no final
syntactic judgment", "no meaning"), but the exact constants must be confirmed
canonically before they are referenced. **None of this is added to code;
design-only.**

## 7. ACCEPT / DEFER / BLOCK Discipline

Applying the P3–P9 information-gain discipline at the **design level only**:

- **ACCEPT** — the structural relation geometry is sufficient to **open only the
  next licensed structural prior** (`irab_geometry_candidates`), and nothing more.
- **DEFER** — the relation geometry is admissible but **underdetermined**; preserve
  the residual and open **no** unsafe downstream commitment.
- **BLOCK** — the relation geometry **contradicts required structural preconditions**
  (`relation_structure_blocked`) or attempts forbidden leakage (`relation_type_conflict`).

Stress (the core P10 boundary):
ACCEPT is **not** i‘rab. ACCEPT is **not** case. ACCEPT is **not** meaning.
ACCEPT is **not** hukm. ACCEPT is **not** final syntax. **ACCEPT only licenses the
next structural question** (the i‘rab-geometry prior for P11) — it asserts no
ruling. This mirrors P9, where ACCEPT opened only `relation_geometry_candidates`
and emitted no semantic/i‘rab object.

## 8. Kernel and Governance Enforcement

The boundary must be enforced the same way P3–P9 enforce theirs (no new machinery):

- **candidate-only marker** on every output (`CandidateOnly`);
- **preserved identity `I(c)`** = union of upstream identities
  (`sentence_geometry_identity`), never reconstructed from trace;
- **trace `T(c)` strictly separate** from identity (kernel's identity∩trace = ∅ check);
- **forbidden-output set** routed through the kernel's `فارق`/blocking machinery
  and the layer `forbidden_outputs`;
- **Freeze guard above P9 in the current state:** no `build_p10_implemented_registry`
  exists while P10 remains SPECIFIED-only. At any future P10 implementation gate,
  this guard must shift to no `build_p11_implemented_registry`, with P11–P12
  remaining SPECIFIED-only. Registry count fixed at 19; governance tests (REC-2,
  freeze-status, responsibility matrix, `test_master_registry_p10_specified.py`)
  hold the line;
- **no downstream candidate leakage** (no P11/P12 emission; P10 may only *open* the
  i‘rab-geometry prior);
- **no semantic / i‘rab / hukm / reality / final objects** anywhere in output or trace.

## 9. Open Design Questions

Design questions only — not implementation tasks:

1. What exact structural relation evidence is sufficient for P10 **ACCEPT** (and how
   is `relation_scope_closed` evidenced)?
2. What conditions should P10 **DEFER** rather than **BLOCK** (underdetermined
   relation scope vs. contradicted precondition)?
3. Does P10 require **at least one accepted P9 `SentenceGeometryCandidate`**, or
   multiple relation-bearing substructures, to ACCEPT?
4. How does P10 **preserve multi-unit identity** carried from P9 without collapsing
   it into a single relation identity?
5. What **residuals** must P10 emit for underdetermined relation geometry (naming
   consistent with the P9 `deferred_*` pattern)?
6. What exact **priors** may P10 open (`irab_geometry_candidates` only?) without
   crossing into i‘rab or meaning?
7. Which **forbidden-output constants** must be referenced explicitly (and must
   `MeaningCandidate` / `DalalahCandidate` be canonically added first)?
8. What **tests** will prove P10 emits no P11/P12 and no i‘rab/case/meaning/hukm/reality
   object?

## 10. Non-Authorization Clause

**This design gate does not authorize implementation.** A separate explicit
authorization is required before any of:

- registry changes
- runtime changes
- schema changes
- tests
- P10 candidate emission
- any PR that implements P10 behavior
