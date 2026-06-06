# External Awamil and Mabniyat Source Inventory

> **Type:** External-source inventory note (docs-only).
>
> **Status:** Records the location, shape, and known issues of two external Arabic corpora living **outside** this repository. **No data is copied into Saleh/Qiyas by this document.** No registry is created. No runtime is introduced. No external entry is ratified as canonical.
>
> **Authority basis (read-only citation):**
>
> - `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) — especially §12 (What May Be Recorded) and §12.1 (Vocalized Source Identity Discipline) — the binding constitutional anchor for any future use of these corpora.
> - `SOURCE_OF_TRUTH_REGISTRY.md` — single-source-of-truth discipline.
> - `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` — registry/runtime separation.
> - `CLAUDE.md` §0 / §2 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20 / §21.

---

## 1. Purpose

This document is an **inventory** — a citation-shaped working record of two Arabic source corpora that exist on the maintainer's local filesystem, **outside** the Saleh/Qiyas repository.

Its purposes are narrow:

- **Cite** the two external paths verbatim so they can be referred to later without ambiguity.
- **Summarize** each corpus's observed shape (file counts, schemas, field families, length-bucket coverage) based on read-only inspections performed in prior sessions.
- **Apply** the binding identity discipline of `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12.1 to the external material as observed.
- **Record** a specific known source-data discrepancy in the operators CSV.
- **Map** the external field shapes to the field reservations of PR #86 §12.

This document does **NOT**:

- copy data into Saleh/Qiyas,
- create a registry,
- create a runtime,
- ratify external entries as canonical,
- amend any existing contract,
- introduce a new claim, label, gate, or rule,
- repair, correct, or modify the external sources,
- decide *i'rāb*, meaning, *dalālah*, or *hukm*.

---

## 2. External Paths

The two external sources documented by this inventory:

```
/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/
/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv
```

Both paths live under a sibling project (`new_arabic_analyzer`) that is maintained independently of Saleh/Qiyas. These paths are **not** referenced by any `src/`, `tests/`, or runtime code in Saleh/Qiyas. Any future PR proposing to consume them must:

- pass its own preflight review,
- cite this inventory's findings (or refresh them by re-inspection),
- honour `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12.1 (vocalized identity carrier),
- not embed external paths in committed runtime code without a separate constitutional amendment.

The maintainer may move, mutate, or rename these paths at any time without notice — this inventory captures the snapshot at the time of its writing.

---

## 3. Relationship to Arabic Awamil/Mabniyat Source Contract

The binding constitutional anchor for any handling of *awamil* / *mabniyat* material is:

```
docs/qiyas_core/ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md
```

Two of that contract's sections are load-bearing for this inventory:

- **§12 What May Be Recorded** — reserves the conceptual field set (`surface_form`, `traditional_group`, `awamil_class`, `mabni_category`, `source_reference`, `variant_notes`, `ambiguity_notes`, `verification_status`, etc.) for any later detailed source table. This inventory maps observed external fields to those reservations in §11 below.
- **§12.1 Vocalized Source Identity Discipline** — refines `surface_form` into `surface_form_vocalized` (identity carrier) and `surface_form_unvocalized_key` (diagnostic only); fixes the six binding rules around vocalization-as-identity, collisions, exact-duplicates, and `source_data_discrepancy`. This inventory applies §12.1 verbatim to the external operators CSV in §8 below.

Anything in this inventory that would conflict with §12 or §12.1 is to be read as **superseded by the contract**. The contract is binding; this inventory is descriptive.

---

## 4. Source A — Mabniyat Corpus Summary

`/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/` (read-only inspection):

- **29 JSON files**, flat layout (no subdirectories).
- **545 entries** in aggregate across the 29 files.
- Common envelope (every file):
  ```json
  { "status": "success", "data": [ … ] }
  ```
- A subset of files also carry `pagination` and timestamp fields (`created_at`, `updated_at`, `is_deleted`, `edited_by`) — the signature of a Laravel/REST database export, not a hand-curated corpus.
- **Length buckets 1–5 are populated** (counts in §6 below).
- **Length 6+ entries also exist** (61 entries) — multi-token / compound forms beyond the initial 1–5 scope of `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §6.
- Topical filename organization: pronouns (5 files), particles/tools (10 files), adverbs (1 file), verb forms (5 files), numbers (2 files), grammar-meta (6 files).
- **Schema is consistent within each file** but **not uniform across files** — surface-form field names vary by domain (see §5).
- **Not registry-ready** under Saleh's `arabic_articulation_registry.py` / `glyph_classification_registry.py` precedent: the database-export envelope, the per-file field-name variance, and the absence of an explicit `awamil_class` partitioning would all need normalization steps before promotion to a registry. **This inventory does NOT perform any such normalization.**

---

## 5. Mabniyat Apparent Schema

Field families observed across the 29 files (read-only inspection):

**Universal per-entry fields:**

- `id` — file-local integer.
- `example` — illustrative Arabic sentence (typically fully vocalized).
- `al_bab_althani_id` — citation anchor to "الباب الثاني — المبنيات" (Chapter II of the maintainer's reference work); appears as a string in most files and as an integer in a few.

**Surface-form field names (per-domain):**

- `name`
- `letter`
- `preposition`
- `particle`
- `adverb`
- `pronoun`
- `form`
- `tool`
- `title`
- `copulative_particle`

**Analytic descriptive fields (per-domain):**

- `gender`
- `number`
- `distance`
- `grammatical_status`
- `semantic_analysis`
- `contextual_analysis`
- `usages`
- `notes`
- `build_mark`
- `condition`
- `parse`
- `syntactic_function`
- `work_condition`

**These are external descriptive fields, not Saleh runtime fields.** Their inclusion in this inventory is purely citational. Any future Saleh-side mapping is governed by §11 below and by `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12. No external field name is canonicalized by appearing in this list.

---

## 6. Mabniyat Length Coverage

Surface-form length distribution by Arabic-letter codepoint count (harakat excluded — i.e., the **diagnostic** length per `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §6 / §12.1 rule 3):

| Bucket | Count | Status |
|---|---:|---|
| length_1 | 9 | populated |
| length_2 | 69 | populated |
| length_3 | 76 | populated |
| length_4 | 55 | populated |
| length_5 | 33 | populated |
| length_6+ | 61 | outside initial 1–5 scope |

**Counts are diagnostic, not canonical.** They are computed from observed surface-form fields using the same Arabic-letter range (`0x0621–0x064A`) that the contract's §6 uses. Length is **not** an identity; per §12.1 rule 3, two distinct `surface_form_vocalized` identities MAY fall into the same `length_bucket`. The 242 entries inside buckets 1–5 are directly addressable by any future detailed source-table contract for *mabniyat*; the 61 length_6+ entries are explicitly outside the initial scope of §6.

---

## 7. Source B — Operators CSV Summary

`/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv` (read-only inspection):

- **UTF-8 with BOM.**
- **102 data rows + 1 header row** = 103 file lines.
- **8 columns**:
  1. `Group Number`
  2. `Arabic Group Name`
  3. `English Group Name`
  4. `Operator`
  5. `Purpose/Usage`
  6. `Example`
  7. `Note`
  8. `Example_Vocalized`
- **13 numeric `Group Number` values** (1–13).
- **23 distinct `(Group Number, Arabic Group Name)` tuples** — the `Arabic Group Name` column subdivides some numeric groups (notably Group 2 splits into six emphasis/wishing sub-themes, and Group 4 splits into five vocative/exception sub-themes).
- **Zero missing values** across all 8 columns.
- **102 / 102 rows have a populated `Example_Vocalized`** field.

This shape is materially cleaner than Source A's database-export structure — the CSV is hand-shaped enough to be cited entry-by-entry, but is still not registry-ready under Saleh's discipline (no `awamil_class` field, single-anchor provenance via `Group Number` only, see §13).

---

## 8. Operators Identity Discipline

Per `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12.1, the identity discipline for any future handling of this CSV (and of Source A) is fixed as follows. This section re-states the discipline so that future PRs citing **this** inventory have the rules visible at a single anchor.

```text
surface_form_vocalized        = identity carrier
                                (the exact NFC-normalized vocalized Arabic
                                 surface form INCLUDING harakat)

surface_form_unvocalized_key  = diagnostic only
                                (the NFC-normalized form with harakat
                                 stripped — usable for collision detection
                                 and indexing; NEVER as identity)
```

Worked distinctions that the CSV preserves and that this inventory binds:

```text
مِنْ  (preposition; codepoints U+0645 U+0650 U+0646 U+0652)
      ≠
مَنْ  (conditional / interrogative noun; codepoints U+0645 U+064E U+0646 U+0652)

إِنَّ  (mushabbihah — emphasis particle)
      ≠
إِنْ  (conditional jussive particle)

أَنَّ  (mushabbihah — emphasis particle)
      ≠
أَنْ  (maṣdariyyah — sub-clause introducer)
```

Six binding rules (verbatim per §12.1):

1. **Harakat MUST NOT be stripped for identity.** The identity key is `surface_form_vocalized`.
2. `مِنْ` and `مَنْ` (and analogous pairs above) are **distinct identities** and MUST NOT be merged at any inventory or future-registry layer.
3. Harakat-stripped forms are **diagnostic only**. They MAY be carried as a secondary key for indexing or audit; they MUST NOT be the primary identity field.
4. *Same `surface_form_unvocalized_key`* + *different `surface_form_vocalized`* = **collision**. Each vocalized form is recorded as a separate identity with its own citation; the collision is surfaced explicitly, not silently merged.
5. *Same `surface_form_vocalized`* appearing in more than one row = **`exact_duplicate`**. Genuine multi-role operators appear here; both rows MUST be recorded with their distinct `Purpose/Usage`.
6. Disagreement between the `Operator` cell and the same row's `Example_Vocalized` field = **`source_data_discrepancy`**. Such rows MUST be referred back to the external corpus maintainer for correction. Saleh/Qiyas MUST NOT silently pick one vocalization as canonical, and MUST NOT use a discrepant row as evidence of multi-role status for either form.

Observed unvocalized-key collisions in the CSV (rule 4 cases — both vocalized identities are distinct and both are recorded):

- `{إِنَّ , إِنْ}` (unvocalized key `إن`)
- `{أَنَّ , أَنْ}` (unvocalized key `أن`)
- `{مَا , ما}` (unvocalized key `ما`)
- `{أي , أيَّ}` (unvocalized key `أي`)
- `{إِذًا , إذا}` (unvocalized key `إذا`)

Observed exact-vocalized duplicates in the CSV (rule 5 cases — same `surface_form_vocalized` appearing in multiple rows under distinct `Purpose/Usage`):

- `بِ` × 2 (مرور / قرب; قسم)
- `وَ` × 3 (قسم; تقليل; معية)
- `لَا` × 2 (نفي; نهي)

The `مِنْ` situation is special and is covered by §9 below.

---

## 9. Known Source Data Discrepancy

One inspected operators row in the external CSV carries a row-internal vocalization disagreement:

```text
Operator cell        : مِنْ
Example_Vocalized    : مَنْ يَرْحَمْ يُرْحَمْ
English Group Name   : Conditional (Jussive Only)
Purpose/Usage        : للشرط
```

Classification under §12.1 rule 6:

```text
source_data_discrepancy
```

Constitutional consequences:

- **This is not evidence that `مِنْ` carries a conditional role.** The CSV's `Operator` cell at this row is at odds with the same row's `Example_Vocalized`, and §12.1 binds: "Saleh/Qiyas MUST NOT silently pick one of the two vocalizations as canonical, and MUST NOT use the discrepant row as evidence of multi-role status for either form."
- **This inventory does not correct the external CSV.** Repair belongs to the external corpus maintainer, not to Saleh/Qiyas.
- **A future source-table PR must either consume the corrected upstream CSV or flag the row as `source_data_discrepancy`.** No middle path is licensed by §12.1 rule 6.
- **The classical distinction `مِنْ` (preposition of ابتداء الغاية) vs `مَنْ` (conditional / interrogative noun) remains binding** under `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md`. The discrepancy in the external CSV does not weaken or modify that distinction.

---

## 10. Duplicate and Collision Categories

The vocabulary used by this inventory (and binding for any future source-table PR that cites it):

- **`collision`** — same `surface_form_unvocalized_key` + different `surface_form_vocalized`. Both vocalized forms are distinct identities. They MUST NOT be merged. (See the five observed pairs in §8.)
- **`exact_duplicate`** — same `surface_form_vocalized` appearing in more than one row, with different `Purpose/Usage`. Genuine multi-role surface form. Both rows MUST be recorded. (See `بِ` / `وَ` / `لَا` in §8.)
- **`source_data_discrepancy`** — row-internal disagreement between the operator-cell vocalization and the example vocalization. The row MUST be flagged and referred back upstream. (See `مِنْ` / `مَنْ` situation in §9.)

Known genuine exact multi-role forms (from the CSV, at the time of inspection):

```text
بِ
وَ
لَا
```

For `مِنْ`, the relevant note:

> The earlier inspected duplicate is **not** accepted as validated multi-role evidence because one row is source-discrepant (§9). Under §12.1 rule 6, the discrepant row cannot count as evidence of multi-role status for `مِنْ`.

---

## 11. Mapping to PR #86 Reserved Fields

Mapping of observed external fields to the field reservations of `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12. The right column carries the binding name; the left columns name the external surface from which the data could later be drawn (by a future source-table PR that imports nothing into Saleh/Qiyas in this inventory itself).

| External field | PR #86 reserved field | Notes |
|---|---|---|
| `Operator` (CSV) | `surface_form_vocalized` | identity carrier (§12.1 rule 1) |
| stripped `Operator` (computed) | `surface_form_unvocalized_key` | diagnostic only (§12.1 rule 3) |
| `Arabic Group Name` (CSV) | `traditional_group` | external grouping |
| `English Group Name` (CSV) | `traditional_group_en` | descriptive |
| `Purpose/Usage` (CSV) | `source_purpose_note` | descriptive |
| `Example` (CSV) | `example_unvocalized` | descriptive |
| `Example_Vocalized` (CSV) | `example_vocalized` | descriptive; also the discrepancy-detection signal (§12.1 rule 6) |
| `Note` (CSV) | `source_parse_note` | descriptive |
| filename (mabniyat) | `traditional_group` / `mabni_category` | for the Source A corpus, where the surface-form field name varies and the topical group is encoded in the filename |
| `al_bab_althani_id` (mabniyat) | `source_reference` | **weak provenance anchor** — single chapter reference of the maintainer's own book; not a citation chain to classical literature; future source-table PR should enrich with classical-source references where possible |

This mapping does **not** import data. It documents how a future, separately-authorised PR would translate the external field surface into the contract's reserved vocabulary — and explicitly notes the `source_reference` provenance gap.

---

## 12. What This Inventory Does Not Do

Explicit non-actions of this PR:

- **does not copy data** from `new_arabic_analyzer/data/02_mabniyat/` into Saleh/Qiyas
- **does not copy data** from `new_arabic_analyzer/data/operators_catalog_split_vocalized.csv` into Saleh/Qiyas
- **does not make external sources canonical**
- **does not create a registry** (no `ArabicAmilRegistry`, no `ArabicMabniRegistry`)
- **does not create a runtime** (no Evidence carrier, no `Candidate`, no rule, no gate, no producer)
- **does not create `ArabicAmilRegistry`**
- **does not create `ArabicMabniRegistry`**
- **does not create `OperatorGeometry`**
- **does not create `AmilEffectEvidence`**
- **does not create `I'rabEffectEvidence`**
- **does not decide `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate` / `MinimalIndependentMeaningCandidate`**
- **does not modify MIU** (no `minimal_unit_readiness_adapter.py` change; no `MinimalUnitReadinessCandidate` change)
- **does not modify `ArabicVariantResolver`**
- **does not modify `GlyphClassificationGate`** contract or any future Glyph runtime
- **does not modify `SIFAT_VECTOR_CONTRACT.md`**
- **does not modify any other existing contract** (including `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` itself — this inventory cites it; it does not amend it)
- **does not address PR #94 coordinate test failures** (5 failures in `test_full_alphabet_coordinates.py` for ذ / ظ / ه are out of scope of this docs-only inventory; their resolution belongs to a separate PR)

---

## 13. Risks and Gaps

Honest enumeration of the risks and gaps that any future PR consuming this inventory must confront:

1. **External path coupling.** Both paths live under `/Users/husseinhiyassat/fractal/new_arabic_analyzer/` — a sibling project maintained independently. Either path may move, mutate, or be renamed without notice to Saleh/Qiyas. Inventory results are a snapshot.
2. **Database-export shape for mabniyat.** Source A's `{ "status": "success", "data": [...] }` envelope with `pagination` / `created_at` / `is_deleted` fields is a REST/Laravel-export shape, not a hand-shaped registry. Normalization would be required before any registry promotion.
3. **Uneven JSON schema across mabniyat files.** Per-file field-name variance for the surface form (`name` / `letter` / `preposition` / `particle` / `adverb` / `pronoun` / `form` / `tool` / `title`) means cross-file queries are non-mechanical.
4. **Weak provenance.** The single `al_bab_althani_id` anchor points to one chapter of the maintainer's own reference work; classical-source citations (Jurjani, Azhariyya, Alfiyya, etc.) are not present in machine-readable form.
5. **No JSON Schema.** No schema file enforces field consistency across the 29 mabniyat files; all files parse, but field shapes are de-facto, not declared.
6. **No dedup index across files.** Cross-file deduplication of mabniyat entries is by domain-role (which is structurally correct), but no explicit cross-reference is recorded.
7. **Possible diacritic normalization issues.** At least one observed mabniyat entry carries what appears to be doubled diacritics (`ثََمََّةَ`). NFC normalization is uneven.
8. **Known `مِنْ` / `مَنْ` source discrepancy (§9).** One operators-CSV row carries a row-internal vocalization disagreement; classified as `source_data_discrepancy` and must NOT be silently resolved.
9. **`length_6+` outside the initial 1–5 source-contract bucket scope.** 61 mabniyat entries fall beyond `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §6's bucket range; promoting them requires either widening the contract's scope (constitutional question) or excluding them (data-loss question).
10. **CSV group-granularity mismatch.** 13 numeric `Group Number` values vs 23 `(Group Number, Arabic Group Name)` tuples — the Arabic group-name column subdivides some numeric groups. A future source-table PR must decide which level is canonical for `traditional_group`.
11. **CSV is operator-effect organized, not exactly the Jurjani 91 / 7 / 2 split.** The CSV partitions by operator effect (jarr / naṣb / raf‘ / jazm / hybrid), which is complementary to but not the same as `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §4's lafẓī samā‘ī / lafẓī qiyāsī / ma‘nawī partition.
12. **The two ma‘nawī awamil are absent from the CSV by nature.** *al-Ibtidā'* and *Tajarrud al-muḍāri‘* have no surface form and thus cannot appear in a surface-form catalog.
13. **Global suite currently has 5 known failures from PR #94, unrelated to this docs-only inventory.** Acknowledged in §12 above as explicitly out of scope for this PR.

---

## 14. Future Work

Safe future PRs (each requires its own explicit trigger; each must pass its own preflight; each must respect the standing non-goals):

1. **`docs(qiyas_core): define external source normalization contract`** — pins the rules under which an external source may be folded into a registry (NFC normalization audit, schema unification, citation enrichment, dedup index requirements).
2. **`docs(qiyas_core): define Arabic awamil detailed source table contract`** — per-entry constitutional table for the 98 lafẓī + 2 ma‘nawī under strict citation discipline, with `awamil_class` partitioning.
3. **`docs(qiyas_core): define Arabic mabniyat detailed source table contract`** — per-entry constitutional table for the mabniyat classes, with per-domain analytic fields normalized to a uniform shape.
4. **`docs(qiyas_core): define source discrepancy reporting contract`** — formalises the `source_data_discrepancy` flag's machine-readable shape and the maintainer-reporting workflow.

What is **not** future work and **must not** be recommended next:

- runtime carriers / producers / registries for any of the above (each requires its own constitutional contract first, mirroring PR #71 / #72 / #80 / #81 / #85),
- `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`,
- `Amil` layer runtime / `OperatorGeometry` runtime / `AmilEffectEvidence` runtime / `I'rabEffectEvidence` runtime,
- `MinimalIndependentMeaningCandidate` / `SentenceCandidate` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate`,
- any direct data copy from external paths into Saleh/Qiyas without going through a normalization contract first.

---

## 15. Summary Table

| Question | Answer |
|---|---|
| Is this runtime? | No. Docs-only external-source inventory. |
| Does it copy data? | No. Cites paths only. |
| Does it make the CSV canonical? | No. The CSV is descriptive; it is not registry-ready. |
| Does it create a registry? | No. |
| What is the identity key? | `surface_form_vocalized` (per `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12.1 rule 1). |
| What is the stripped key? | Diagnostic only (per §12.1 rule 3); never an identity. |
| What about `مِنْ` / `مَنْ`? | Distinct identities (codepoints `U+0650` vs `U+064E` at position 2); the CSV's row-45-style `Operator`-cell vs `Example_Vocalized` disagreement is a **`source_data_discrepancy`** flagged per §9. |
| What about global test failures? | 5 failures in `test_full_alphabet_coordinates.py` are known **out-of-scope PR #94 failures**; this docs-only inventory neither addresses nor inherits them. |
| What is next? | Either pause, or a docs-only normalization / detailed source-table contract per §14. |

---

**Document version:** 1.0
**Last updated:** 2026-06-06
**Status:** External-source inventory note (docs-only).
**Authority:** Subordinate to `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12 / §12.1, to `SOURCE_OF_TRUTH_REGISTRY.md`, to `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`, and to `CLAUDE.md` §0–§21. Does not amend any of them. Records the external source state at the time of writing; the external sources may evolve independently.
