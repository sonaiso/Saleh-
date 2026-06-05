# GlyphClassificationGate Contract

> **Type:** Producer-side constitutional contract (docs-only).
>
> **Status:** Reserves the future producer `GlyphClassificationGate` and
> its Evidence carrier `GlyphClassificationEvidence` over the existing
> `glyph_classification_registry.py` taxonomy. Does **not** introduce a
> parallel taxonomy, does **not** amend the registry, does **not**
> introduce any runtime.
>
> **Authority basis (read-only citation):**
>
> - `PROJECT_MATHEMATICAL_FOUNDATION.md` §11 (Full Layer 2)
> - `FULL_LAYER_2_PLAN.md` §3 (GlyphClassificationGate requirement)
> - `GLYPH_CLASSIFICATION_GATE_PLAN.md` (preparatory plan)
> - `SOURCE_OF_TRUTH_REGISTRY.md` §4 ("Glyph classification" canonical source)
> - `src/qiyas_core/registries/glyph_classification_registry.py` (canonical taxonomy module — read-only by this contract)
> - `SIFAT_VECTOR_CONTRACT.md` (existing sibling contract — not amended by this contract)
> - `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`
> - `ARABIC_VARIANT_RESOLUTION_CONTRACT.md`
> - `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md`
> - `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`
> - `CLAUDE.md` §0 / §2 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20 / §21

---

## 1. Purpose

This document defines a **producer-side constitutional contract** for a future `GlyphClassificationGate`. Its purpose is narrow:

- It **reserves** the producer name `GlyphClassificationGate` and the evidence carrier name `GlyphClassificationEvidence`.
- It **fixes** the closed consumption surface, allowed outputs, and failure discipline of the future producer.
- It **cites** the existing canonical taxonomy in `src/qiyas_core/registries/glyph_classification_registry.py` rather than restating it.

It is **not** a runtime artifact. It does **not**:

- introduce a new layer to runtime;
- introduce a new evidence carrier to runtime;
- introduce a new `Candidate` of any type;
- amend the existing glyph taxonomy registry;
- amend `ArabicVariantResolver`;
- amend the MIU readiness adapter;
- amend `SIFAT_VECTOR_CONTRACT.md` or any other merged contract;
- introduce any claim, label, gate, or rule into the Qiyas algebra.

The contract follows the docs-first precedent established by PRs #71, #72, #78, #79.

---

## 2. Layer Position

Per `PROJECT_MATHEMATICAL_FOUNDATION.md` §11, `GlyphClassificationGate` sits at **Layer 2 (Arabic Phonetic Completion)**, between `Layer 1 (TypedCodePoint classification)` and the future `Layer 2` completion pieces (`SifatVector`, `ArabicMorphophonology`, `RoleDisambiguationGate`).

```
Layer 0   UnicodeCandidate
Layer 1   TypedCodePoint
Layer 2   ← this contract is here
            GlyphClassificationGate
            SifatVector (separate contract — already merged)
            ArabicMorphophonology
            RoleDisambiguationGate
Layer 3   SlotCandidate
Layer 3.5 SlotGeometry
Layer 3.6 MinimalIndependentUnitReadiness
Layer 3.7 ArabicVariantResolver
Layer 4   Universal Phonetic Foundation
Layer 5   Arabic Phonetic Completion
Layer 6+  Syllable / Stem-Root / Word / Lexical / Composition / Style / Ifadah / Hukm / Truth-grounding
```

`GlyphClassificationGate` is **structurally below** `SlotCandidate` (Layer 3). It is far below `WordFormAlgebra` (Layer 8), `LexicalMadlulAlgebra` (Layer 9), and the eventual `HukmCandidate` (Layer 13). It is **not** a step toward Word, Dalalah, Meaning, Hukm, or Reality.

---

## 3. Existing Registry Authority

The canonical glyph-classification taxonomy already lives at:

```
src/qiyas_core/registries/glyph_classification_registry.py
```

That module is the **single canonical source** for the glyph taxonomy per `SOURCE_OF_TRUTH_REGISTRY.md` §4. It exports a `GlyphClass` enum, a `GlyphClassification` dataclass, and read-only public helpers (`classify_glyph`, `is_core_letter`, `requires_decomposition`). Its module docstring explicitly forbids parallel classification logic:

```
# DO NOT duplicate these classifications in adapters
# DO NOT create parallel glyph classification logic
```

This contract **honours that clause**. It does not duplicate, supersede, or contradict the registry taxonomy. The eight class labels in §6 below are the contract-friendly mapping of the registry's eight enum values, in PascalCase, for use in contract-side prose. The runtime authority remains the registry module.

This contract defines only the **producer-side constitutional shape** of the future `GlyphClassificationGate`: its consumption surface, its evidence-carrier output, its failure modes, and its forbidden outputs. The taxonomy itself is **not** restated here.

---

## 4. Producer Name

This contract **reserves** the following future runtime names:

```
GlyphClassificationGate        — reserved producer name. Not yet
                                  implemented. A future implementation
                                  PR may introduce the producer class
                                  under this name.
GlyphClassificationEvidence    — reserved Evidence carrier name. Not
                                  yet implemented. A future runtime PR
                                  may introduce a frozen-dataclass
                                  carrier under this name.
```

Both names are **reserved-by-name only**. Neither is implemented at the time of this document's ratification.

A future runtime PR introducing `GlyphClassificationEvidence` MUST follow the **Evidence-carrier-not-Candidate** pattern fixed by `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` (PR #72) and reaffirmed by `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §2:

```
GlyphClassificationEvidence is an Evidence carrier, NOT a Candidate.
It has no candidate_type, no status, no output_flags fields.
```

A future runtime PR introducing `GlyphClassificationGate` MUST follow the **observation-only producer** pattern fixed by `SlotGeometryClosureCheck` (PR #73) and `ArabicVariantResolver` (PR #81): a deterministic, frozen, stateless class with a `classify(codepoint, ...)` (or equivalent) method returning `GlyphClassificationEvidence | None`. It MUST NOT invoke `QiyasKernel.apply` and MUST NOT produce a `Candidate`.

The reserved future module path (non-binding suggestion) is:

```
src/qiyas_core/glyph_classification_gate.py
```

---

## 5. Closed Consumption Surface

When a future PR implements `GlyphClassificationGate`, it MUST consume **only** the following inputs:

**Admissible inputs:**

- `UnicodeCandidate` identity/trace already preserved by Layer 0;
- `TypedCodePoint` classification result already produced by Layer 1;
- the raw Unicode codepoint scalar value (read-only);
- `glyph_classification_registry.py` metadata (via its existing read-only public API: `classify_glyph`, `is_core_letter`, `requires_decomposition`);
- script-level metadata, IF already licensed by an existing lower-layer evidence carrier;
- local orthographic context, IF AND ONLY IF preserved by lower-layer evidence (e.g., a `TypedCodePoint`'s trace_ids that record adjacent codepoint identities) — the gate does NOT independently re-tokenise.

**Forbidden inputs (the gate MUST NOT directly consume any of these):**

- raw text strings (consumption must come via `UnicodeCandidate` / `TypedCodePoint`);
- `SequenceContextTokenizer` markers consumed directly;
- `LetterIdentityCarrier` (the gate runs strictly below identity carriers);
- `HarakaFunctionCarrier`;
- `PositionCarrier`;
- `CarrierBindingCandidate`;
- `ConditionedTypedSequence` outputs (the gate is per-codepoint, not per-sequence);
- `SlotCandidate`;
- `SlotGeometryCandidate`;
- `MinimalCompleteClosureEvidence`;
- `ArabicVariantResolutionEvidence`;
- `MinimalUnitReadinessCandidate`;
- `WordCandidate` / `LafzCandidate` / `SentenceCandidate` / `ParagraphCandidate`;
- `DalalahCandidate`;
- `FinalMeaning`;
- `HukmCandidate`;
- `RealityClaim`;
- `FinalCaseJudgment`;
- `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate`.

The gate operates **per codepoint** under the licensed Layer 0 / Layer 1 metadata. It does not consume any higher-layer typed unit.

---

## 6. Canonical Glyph Classes

Per §3, the canonical taxonomy is owned by `src/qiyas_core/registries/glyph_classification_registry.py`. The contract-friendly PascalCase labels — used in **prose only** within this contract — map 1:1 to the registry enum values:

| Contract label | Registry enum value | Notes |
|---|---|---|
| `CoreArabicLetter` | `CORE_ARABIC_LETTER` | Simple Arabic letters with direct 1:1 phonetic mapping. |
| `StandaloneHamza` | `STANDALONE_HAMZA` | Standalone hamza `ء` (U+0621). Not a seat glyph. |
| `HamzaSeatGlyph` | `HAMZA_SEAT_GLYPH` | Hamza on a seat (composite glyph). |
| `WeakLetterGlyph` | `WEAK_LETTER_GLYPH` | Letters with multiple potential roles (context-dependent). |
| `TatweelGlyph` | `TATWEEL_GLYPH` | Spacing/justification glyph, NOT a letter. |
| `OrthographicVariant` | `ORTHOGRAPHIC_VARIANT` | Orthographic form variants (e.g., alif maqsurah, taa marbuta). |
| `ComplexGlyph` | `COMPLEX_GLYPH` | Glyphs requiring decomposition before coordinates. |
| `Punctuation` | `PUNCTUATION` | Arabic punctuation marks. |

These **eight** are the canonical labels reserved by this contract. Any future amendment that proposes to add a class label MUST first amend the registry (a separate, explicitly-authorised PR) and only then update this contract.

The `GlyphClassificationGate` producer, when implemented, MUST emit only one of these eight class labels (or `None` per §10).

---

## 7. Deferred / Non-Canonical Labels

The following labels were proposed during contract drafting but are **NOT canonical** at the time of this document's ratification. Each requires a **separate registry-amendment PR** before it may be used in runtime or in any effective contract:

- `MaddGlyph` — currently subsumed under `WeakLetterGlyph` (the existing taxonomy treats madd as a *role* of weak letters, not a separate glyph class). Promoting `MaddGlyph` to a class requires a registry-amendment PR and a careful constitutional argument that distinguishes glyph-class from role.
- `Boundary` — whitespace and segment boundaries are currently handled at the tokenizer level (pre-qiyas). Their promotion to a canonical glyph class requires a registry-amendment PR.
- `Residual` — explicit residual handling at the glyph layer is currently encoded as `None` (the producer returns `None` for unclassifiable inputs per §10). Promoting `Residual` to a class label requires a registry-amendment PR.

Until those PRs exist:

- `GlyphClassificationGate` MUST NOT emit `MaddGlyph`, `Boundary`, or `Residual`.
- `GlyphClassificationEvidence.selected_glyph_class` MUST be drawn from the eight canonical labels in §6 only.
- Worked examples (§14) MUST NOT use these three labels.

This deferral is itself a non-goal of this PR (§16).

---

## 8. Evidence Shape

`GlyphClassificationEvidence` is reserved as the future Evidence carrier produced by `GlyphClassificationGate`. This contract fixes its **high-level constitutional shape** only. A future runtime PR will pin the precise field-level dataclass.

Conceptual field set (non-binding on field names, binding on intent):

```text
evidence_id           : str   — per-evidence unique identifier; never an identity
source_codepoint_id   : str   — audit anchor for the source codepoint (e.g.,
                                "identity:codepoint:0628")
selected_glyph_class  : str   — one of the eight canonical labels in §6
selection_basis       : tuple[str, ...] — basis-label tuple recording the
                                evidence the gate used (e.g., registry lookup,
                                Unicode block membership, decomposition
                                witness). Reserved basis labels are deferred
                                to the future runtime contract.
script_scope          : str   — script identity (e.g., "Arabic"); the gate's
                                contract is currently bounded to Arabic
                                Unicode blocks.
rank                  : EvidenceRank — at most FORMAL_STRUCTURE; the gate is
                                metadata-derived and may not exceed structural
                                rank.
identity_ids          : tuple[str, ...] — preserved verbatim from inputs
trace_ids             : tuple[str, ...] — preserved verbatim from inputs
                                + the gate's own audit trace entries
residuals             : tuple[Residual, ...] — empty when the gate emits
                                evidence; the gate emits None instead of
                                building a half-true carrier (per §10)
```

Field-level discipline (binding):

- The carrier is **frozen**.
- The carrier has **no** `candidate_type`, **no** `status`, **no** `output_flags` field — it is structurally NOT a `Candidate`-shape (per `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` §2 and `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` §2).
- The carrier preserves `identity_ids` verbatim and writes its own audit entries onto `trace_ids` only — never onto `identity_ids` (CLAUDE.md §4 invariant 3).

This contract does **not** specify the exact basis-label tuple; that is deferred to the future runtime contract.

---

## 9. Allowed Outputs

`GlyphClassificationGate`, when implemented, MUST return:

```
GlyphClassificationEvidence | None
```

It MUST NOT return any of the following — not as its return value, not as a side effect, not as part of an audit trail:

- `Candidate` of any type
- `SlotCandidate`
- `SlotGeometryCandidate`
- `MinimalCompleteClosureEvidence`
- `ArabicVariantResolutionEvidence`
- `MinimalUnitReadinessCandidate`
- `WordCandidate`
- `LafzCandidate`
- `SentenceCandidate`
- `ParagraphCandidate`
- `DalalahCandidate`
- `FinalMeaning`
- `HukmCandidate`
- `RealityClaim`
- `FinalCaseJudgment`
- `MinimalIndependentMeaningCandidate`
- `SentenceGeometry`
- `DiscourseGeometryCandidate`
- `TextGeometryCandidate`

---

## 10. Failure Discipline

The gate's failure discipline is fixed:

- **Absence** of admissible input ⇒ `None` (DEFER-equivalent). NEVER `BLOCK`.
- **Conflict** between competing classification witnesses ⇒ `None`. NEVER `BLOCK`.
- **Malformed** input ⇒ DISCARD ⇒ `None`. NEVER `BLOCK`.
- **Unlicensed context** (e.g., codepoint outside the Arabic script scope, or input shape not on the §5 consumption surface) ⇒ `None`. NEVER `BLOCK`.
- **No BLOCK at the glyph-classification layer.** This contract does not introduce a blocking diagnostic; a future amendment may do so only with an explicit constitutional argument.

This mirrors the §7 absence-≠-BLOCK discipline established by `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` and the conjunctive-build discipline of `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` (the carrier is constructed only when all preconditions hold; otherwise the producer returns `None` rather than building a half-true carrier).

---

## 11. Relationship to ArabicVariantResolver

- This contract **does not change** `ArabicVariantResolver` (PR #81).
- `ArabicVariantResolver` **does not consume** `GlyphClassificationEvidence` at the time of this document's ratification.
- This contract **does not change** the runtime behaviour of `وَ` or `يَ` documented in `MIU_VARIANT_RESOLUTION_USAGE_NOTE.md` (PR #84).
- A future runtime PR may use `GlyphClassificationEvidence` as part of stronger `ArabicVariantResolver` preconditions, but **not in this PR**. Any such future change is forward-looking and **not retroactive**.

---

## 12. Relationship to MIU

- This contract **does not change** `MinimalIndependentUnitReadinessLayerAdapter` (PRs #75 / #82).
- The MIU adapter **does not consume** `GlyphClassificationEvidence` at the time of this document's ratification.
- **No MIU adapter amendment** is implied or required by this contract.
- The merged ACCEPTED / BLOCKED / DEFERRED behaviour for بِ / ضَ / وَ / يَ / ضَرَبَ / foreign-evidence / invalid-evidence (documented in `MIU_VARIANT_RESOLUTION_USAGE_NOTE.md` §5 and locked by `tests/qiyas_core/test_variant_resolver_miu_integration.py`) is **unchanged** by this contract.

---

## 13. Relationship to SifatVector

- `SIFAT_VECTOR_CONTRACT.md` **already exists** in `docs/qiyas_core/`. It is a merged sibling contract.
- This contract **does not amend** `SIFAT_VECTOR_CONTRACT.md`.
- This contract **does not implement** `SifatVector` runtime.
- A future runtime PR for `SifatVector` MUST follow the existing `SIFAT_VECTOR_CONTRACT.md`. It will **not** be authorised to introduce a new SifatVector contract; that contract is already merged.
- `GlyphClassificationGate` may serve as a **prerequisite** for the eventual `SifatVector` runtime (a glyph must be classified before phonetic coordinates are assigned, per `GLYPH_CLASSIFICATION_GATE_PLAN.md` §0 and `SIFAT_VECTOR_CONTRACT.md` §0). The two contracts are **complementary**, not overlapping.

---

## 14. Worked Examples

Examples are illustrative under the canonical taxonomy of §6. They are **not** definitive runtime decisions and do **not** authorise any implementation. The "Notes" column records why classification at this layer carries no higher-layer semantic weight.

| Symbol / Glyph | Current canonical class | Notes |
|---|---|---|
| `ب` | `CoreArabicLetter` | no meaning claim, no morpho claim |
| `ت` | `CoreArabicLetter` | same — single mapping, no role decision |
| `ء` | `StandaloneHamza` | not a seat glyph; no word claim |
| `أ` | `HamzaSeatGlyph` or `OrthographicVariant` depending on registry entry — do not overdefine here |
| `إ` | `HamzaSeatGlyph` or `OrthographicVariant` depending on registry entry — do not overdefine here |
| `ؤ` | `HamzaSeatGlyph` — do not overdefine here |
| `ئ` | `HamzaSeatGlyph` — do not overdefine here |
| `و` | `WeakLetterGlyph` or `CoreArabicLetter` depending on current registry metadata; **no variant resolution at this layer** (variant resolution belongs to Layer 3.7 — `ArabicVariantResolver` — and remains unchanged by this contract) |
| `ي` | `WeakLetterGlyph` or `CoreArabicLetter` depending on current registry metadata; **no MIU admission at this layer** |
| `ـ` (U+0640) | `TatweelGlyph` | not a `SlotCandidate`; no phonetic coordinates |
| `آ` (U+0622) | `ComplexGlyph` | no decomposition runtime in this PR |
| `لا` (U+FEFB) | `ComplexGlyph` | composite ligature; no decomposition runtime here |
| `ى` (U+0649) | `OrthographicVariant` | terminal-position sensitivity is a registry concern, not a Glyph-gate concern |
| `ة` (U+0629) | `OrthographicVariant` | same |
| `،` (U+060C) | `Punctuation` | not a `SlotCandidate`; not a letter |
| `؛` (U+061B) | `Punctuation` | same |

**Explicit prohibitions on this table:**

- Whitespace is **NOT** classified as `Boundary` here. `Boundary` is a deferred non-canonical label per §7. Whitespace remains a tokenizer-level concern, pre-qiyas.
- Unknown / unclassifiable input is **NOT** classified as `Residual` here. `Residual` is a deferred non-canonical label per §7. Unknown input maps to `None` per §10.
- `و`, `ي`, and any future alif (`ا`) coverage **DO NOT** make final-role decisions here. Their role disambiguation belongs to `RoleDisambiguationGate` (a strictly later Layer 2 piece) and to `ArabicVariantResolver` (Layer 3.7).

---

## 15. Forbidden Jumps

The following transitions are **explicitly forbidden** under this contract — at the producer layer, at the evidence layer, and at the contract layer:

```
GlyphClassificationEvidence  →  SlotCandidate                     ❌
GlyphClassificationEvidence  →  SlotGeometryCandidate             ❌
GlyphClassificationEvidence  →  ArabicVariantResolutionEvidence   ❌
GlyphClassificationEvidence  →  MinimalCompleteClosureEvidence    ❌
GlyphClassificationEvidence  →  MinimalUnitReadinessCandidate     ❌
GlyphClassificationEvidence  →  WordCandidate                     ❌
GlyphClassificationEvidence  →  LafzCandidate                     ❌
GlyphClassificationEvidence  →  SentenceCandidate                 ❌
GlyphClassificationEvidence  →  DalalahCandidate                  ❌
GlyphClassificationEvidence  →  FinalMeaning                      ❌
GlyphClassificationEvidence  →  HukmCandidate                     ❌
GlyphClassificationEvidence  →  RealityClaim                      ❌
GlyphClassificationEvidence  →  FinalCaseJudgment                 ❌
GlyphClassificationEvidence  →  registry mutation                 ❌
glyph class                  →  meaning                           ❌
glyph class                  →  hukm                              ❌
glyph class                  →  wordhood                          ❌
glyph class                  →  MIU acceptance                    ❌
glyph class                  →  variant resolution                ❌
```

Glyph classification carries **no** higher-layer semantic weight. It records "this codepoint is of this glyph class under the registry's metadata" and nothing else.

---

## 16. Non-Goals

This PR is **docs-only** and explicitly does not include, propose, or imply:

- no code (no `src/` change)
- no tests (no `tests/` change)
- no runtime evidence carrier (`GlyphClassificationEvidence` is reserved-by-name only)
- no `GlyphClassificationGate` implementation
- no registry change (no `glyph_classification_registry.py` change)
- no registry amendment (no new enum value)
- no `SIFAT_VECTOR_CONTRACT.md` amendment
- no `SifatVector` runtime
- no `ArabicVariantResolver` expansion
- no MIU adapter amendment
- no `__init__.py` change
- no alif (`ا`) semantics
- no `MaddGlyph` canonicalization (deferred per §7)
- no `Boundary` canonicalization (deferred per §7)
- no `Residual` canonicalization (deferred per §7)
- no `WordCandidate`
- no `LafzCandidate`
- no `DalalahCandidate`
- no `FinalMeaning`
- no `HukmCandidate`
- no `RealityClaim`
- no `FinalCaseJudgment`
- no `SentenceCandidate` / `ParagraphCandidate` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate`
- no `MinimalIndependentMeaningCandidate`
- no `Amil` layer (no Jurjani 'awamil)
- no priority / tie-breaking algorithm
- no sibling-context pipeline amendment
- no caller-side auto-wiring above MIU
- no automatic integration layer above MIU
- no full Layer 2 implementation

---

## 17. Future Work

The following are **safe future PRs** that may be opened later, each under its own explicit trigger:

1. **`docs(qiyas_core): define GlyphClassificationEvidence runtime contract`** — pins the runtime field layout of the evidence carrier (closure-evidence runtime contract pattern, per PR #72), the audit-trace schema, and the reserved selection-basis labels.
2. **`feat(qiyas_core): add GlyphClassificationEvidence runtime carrier`** — introduces the frozen-dataclass carrier (carrier-only, mirrors PR #80).
3. **`feat(qiyas_core): implement GlyphClassificationGate`** — introduces the producer (producer-only, mirrors PR #81).
4. **Later — implement / use SifatVector according to the existing `SIFAT_VECTOR_CONTRACT.md`.** No new SifatVector contract is needed; the existing merged contract is the authority. A future runtime PR may follow the same docs-first → carrier → producer cadence under the existing contract's discipline.

The following are **explicitly NOT recommended next**:

- starting any of the rejected items in §16,
- amending the registry to add `MaddGlyph` / `Boundary` / `Residual`,
- amending the contract to widen the consumption surface,
- introducing an integration adapter above MIU,
- introducing `RoleDisambiguationGate` runtime before its own contract is merged,
- starting Layer 4+ (syllable, stem/root, word, lexical, composition, style, ifadah, hukm, truth/reality-grounding).

---

## 18. Summary Table

| Question | Answer |
|---|---|
| Is this runtime? | No. Docs-only contract. |
| Does it change MIU? | No. |
| Does it change `ArabicVariantResolver`? | No. |
| Does it change `glyph_classification_registry.py`? | No. |
| Does it amend `SIFAT_VECTOR_CONTRACT.md`? | No. |
| Does it produce `Candidate`? | No. Only `GlyphClassificationEvidence \| None` (when implemented). |
| Does it classify meaning? | No. |
| Does it start `WordCandidate` / `DalalahCandidate`? | No. |
| Does it touch alif semantics? | No. |
| What does it reserve? | `GlyphClassificationGate` (producer name); `GlyphClassificationEvidence` (carrier name). |
| What is the canonical taxonomy? | The existing `glyph_classification_registry.py` (8 enum values mapped 1:1 to the 8 PascalCase labels in §6). |
| What is deferred? | `MaddGlyph`, `Boundary`, `Residual` — each requires a separate registry-amendment PR. |
| What does absence mean? | `None` (DEFER-equivalent). Never `BLOCK`. |
| What is next? | A docs-only runtime contract for `GlyphClassificationEvidence` (see §17). |

---

**Document version:** 1.0
**Last updated:** 2026-06-05
**Status:** Producer-side constitutional contract (docs-only).
**Authority:** Subordinate to the registry in `src/qiyas_core/registries/glyph_classification_registry.py` for taxonomy, to `PROJECT_MATHEMATICAL_FOUNDATION.md` §11 for layer position, to the existing `SIFAT_VECTOR_CONTRACT.md` for phonetic-vector specifications, and to `CLAUDE.md` §0–§21 for the governing project discipline. Does not amend any of them.
