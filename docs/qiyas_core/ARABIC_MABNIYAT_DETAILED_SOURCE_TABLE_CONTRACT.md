# Arabic Mabniyat Detailed Source Table Contract

> **Status**: docs-only constitutional contract — *source-review discipline only*.
> **Authority**: extends `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97), `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103), `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105), and `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #106). Binds `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 5 (Mabniyat Scope) + § 12 / § 12.1 (Vocalized Source Identity Discipline), `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96), and `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 (`Example_Vocalized` discipline).
> **Scope**: defines the per-entry *source-review discipline* for the mabniyat / indeclinable-forms corpus at `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/`. Covers source-file inventory, source-class taxonomy, surface-field priority review, `title_used_as_surface_candidate` handling, `weak_provenance` handling, per-entry evidence requirements, identity discipline, `Example_Vocalized` discipline, discrepancy integration, the Saleh-side / upstream-side boundary, and inclusion / exclusion rules for any future *mabniyat pilot snapshot* cycle citing this contract.
> **Non-Authority**: this contract is **source-review discipline only**. It does **NOT** instantiate a mabniyat pilot snapshot, does **NOT** modify any external source file, does **NOT** admit any mabniyat entry into Saleh runtime / registry / tests / fixtures / data, does **NOT** silently correct any discrepancy, does **NOT** create runtime / registry / test / fixture / data file, does **NOT** promote source-side classification to Saleh-canonical, does **NOT** amend any predecessor contract, and does **NOT** open `SNAP-002` / `SNAP-003` / mabniyat pilot snapshot instantiation.

---

## 1. Purpose

This contract codifies the per-entry **source-review discipline** for the Arabic *mabniyat* (indeclinable-forms) corpus. It is the structural sibling of PR #106's `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` for the *awamil/operators* corpus — but the mabniyat corpus has fundamentally different schema heterogeneity (29 distinct JSON files, 9 candidate surface fields, multiple file classes with no concrete Arabic surface form at all), so A3 cannot be a copy-paste of A2.

This contract exists to make four things explicit:

1. **How a mabniyat entry's surface form is selected from heterogeneous source fields.** § 5 codifies the 9-way *surface-field priority review*. § 6 maps source fields to normalized review fields per file class. § 7 and § 8 codify the two mabniyat-specific warning classes (`title_used_as_surface_candidate` and `weak_provenance`) that the awamil contract did not need.
2. **How identity, `Example_Vocalized`, and discrepancy disciplines specialise to mabniyat.** § 10 / § 11 / § 12 re-bind the predecessor disciplines verbatim and specialise them to mabniyat's per-file heterogeneity.
3. **What evidence a future mabniyat pilot snapshot cycle must record per entry.** § 9 enumerates the required evidence fields. § 14 and § 15 specialise PR #103's inclusion / exclusion rules to mabniyat.
4. **The boundary between *source review* and *runtime*.** This contract is **source review**. It does not admit any entry into Saleh runtime, registry, fixture, or data. It does not perform a mabniyat pilot snapshot instantiation. § 16 reserves the forward hooks. § 17 enumerates the non-goals.

This contract is **docs-only**. It is **source-review discipline only**. It does NOT create a runtime layer, an adapter, a producer, a carrier, a rule, a registry, an evidence type, a candidate type, a test fixture, or any data file. It does NOT change any existing contract. It does NOT amend `new_arabic_analyzer/`. It is a *review-schema contract*, not a *transformation contract*.

This contract **does not claim** that mabniyat rows are proven grammatical facts. It does not claim that Saleh "solves" Arabic mabniyat. It says: when a future mabniyat pilot cycle is opened, *these* are the review rules it must follow.

## 2. Relationship to Predecessor Contracts

This contract sits *on top of* the predecessors below; it does not redefine, weaken, or override any of them. Where a sentence in this contract could be read as conflicting with a predecessor, the predecessor controls.

| document | role | how this contract uses it |
|---|---|---|
| `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 5 / § 12 / § 12.1 | Mabniyat Scope (the classical seed); Vocalized Source Identity Discipline | § 10 of this contract re-binds PR #86 § 12.1 verbatim; § 4 of this contract cites PR #86 § 5's source-class sketch as the *seed*, not the final taxonomy |
| `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) | inventory of the two external corpora at `new_arabic_analyzer/data/` | this contract uses the inventory as the canonical *source-path pointer* — § 3 below cites the mabniyat directory path verbatim from the inventory |
| `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) § 15 | the five reserved snapshot forms; the source-review normalization boundary | § 6 of this contract specialises PR #97's general normalization boundary to mabniyat's per-file heterogeneity |
| `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 | `Example_Vocalized` is descriptive only; forbidden as runtime fixture / i'rāb proof / role proof | § 11 of this contract re-binds PR #98 § 12.4 verbatim |
| `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) § 5 / § 6 / § 7 / § 8 / § 9 / § 12 / § 13 / § 14 | snapshot policy: inclusion / exclusion / identity / warning / `Example_Vocalized` / provenance / forbidden / future-PR-shape | § 14 / § 15 of this contract specialise PR #103's general rules to the mabniyat schema |
| `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) | discrepancy workflow + recorded findings R-001 / R-002 (awamil findings) | § 12 of this contract binds PR #105 verbatim; mabniyat findings, when discovered, will get the next-available `R-NNN` IDs (e.g. R-003, R-004, …) under PR #105's amendment workflow first, then mirrored here |
| `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #106) | sibling pattern for the *awamil* corpus | this contract follows the same 17-section structural pattern as A2 but specialises every section to mabniyat's per-file heterogeneity; it explicitly does NOT copy A2's row-level schema, because mabniyat is not one CSV with one schema |

**A3 is a sibling to A2, not a replacement and not a copy-paste clone.** A2 handles awamil (one CSV, one schema, one identity column). A3 handles mabniyat (29 JSON files, multiple surface-field candidates per file, weak-provenance file classes, title-fallback semantics). A3 inherits the shared *source-review* discipline (identity, `Example_Vocalized`, discrepancy, boundary, snapshot eligibility) from A2 verbatim, but adds three new sections (§ 5 Surface-Field Priority Review, § 7 `title_used_as_surface_candidate` Handling, § 8 `weak_provenance` Handling) that A2 did not need.

This contract does **not** amend any predecessor. Where a sentence could be read as conflicting with any predecessor, the predecessor controls.

## 3. Source Path and File Inventory

### 3.1 Source path

The mabniyat corpus this contract describes is the directory:

```
/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/
```

This path is **outside** Saleh's git working tree. Saleh has *zero write access* to it (PR #105 § 9). This contract cites the path by string; it does not copy, mirror, read for content, or import any byte of any file at that path into Saleh.

The contract is allowed to consult `/tmp/source_preview_mabniyat.csv` — the read-only prototype's normalized preview output — for source-file inventory facts. Such consultation is *prototype-derived metadata only*, never source-data import.

### 3.2 File inventory discipline

Any future mabniyat snapshot cycle citing this contract must, before admitting any entry, enumerate each JSON source file with the following inventory record:

| field | meaning |
|---|---|
| `source_file_name` | the JSON file's basename (e.g. `built_in_adverbs.json`) |
| `source_file_path` | absolute path: the directory above, plus the file basename |
| `source_file_size_bytes` | byte size at inspection time |
| `source_file_mtime_utc` | mtime at inspection time |
| `source_file_sha256` | SHA-256 at inspection time |
| `entry_count` | number of entries parsed from the file (typically the `data[]` list length) |
| `source_class_label` | the source-class label assigned per § 4 |
| `inspection_timestamp_utc` | UTC ISO-8601 timestamp when the inventory record was taken |
| `prototype_run_id` | pointer to the prototype script + invocation that produced the inventory |

### 3.3 The 29 source files

As of the prototype run at `/tmp/source_preview_mabniyat.csv` (mtime `Jun 7 00:10`), the corpus contains **29 JSON files** with the following inventory (this list is *descriptive of the prototype's observation*, not a normative invention; future review must re-enumerate against the live source):

| file | entry count (prototype) | source-class label (§ 4) |
|---|---:|---|
| `building_regulations.json` | 4 | rule/case-description |
| `built_in_adverbs.json` | 21 | adverbial/circumstantial fixed forms |
| `compound_number_details.json` | 4 | numerals or composite fixed forms |
| `compound_numbers.json` | 8 | numerals or composite fixed forms |
| `conditional_letters_tools.json` | 21 | conditional forms |
| `coordinating_conjunctions.json` | 23 | particles / fixed expressions |
| `copulative_particle.json` | 7 | particles / fixed expressions |
| `demonstrative_pronouns.json` | 53 | demonstratives |
| `estimated_parsing_indeclinables.json` | 4 | rule/case-description |
| `functional_indeclinable_substitutes.json` | 7 | rule/case-description |
| `grammatical_construction_cases.json` | 55 | rule/case-description |
| `hidden_pronouns.json` | 11 | pronouns |
| `imperative_verb_building.json` | 10 | rule/case-description |
| `indeclinable_discourse_roles.json` | 5 | rule/case-description |
| `interrogative_letters_tools.json` | 6 | interrogatives |
| `interrogative_tools_categories.json` | 17 | interrogatives |
| `jazm_tools.json` | 20 | particles / fixed expressions |
| `kinaya_names.json` | 9 | other mabni categories pending review |
| `letters_answers.json` | 10 | particles / fixed expressions |
| `past_tense_conjugation_rules.json` | 11 | rule/case-description |
| `preposition_meanings.json` | 56 | particles / fixed expressions |
| `present_naseb_tools.json` | 10 | particles / fixed expressions |
| `present_tense_building_cases.json` | 3 | rule/case-description |
| `pronouns_classification.json` | 43 | pronouns |
| `relative_pronouns.json` | 48 | relative pronouns |
| `types_of_i3rab.json` | 3 | rule/case-description |
| `verb_building_rules.json` | 10 | rule/case-description |
| `verb_name.json` | 57 | other mabni categories pending review |
| `vocative_particles.json` | 9 | particles / fixed expressions |

Total: **545 entries** across **29 files**. Of these, the prototype's normalization preview classified roughly **406** as `normalized_row_ready=yes`, **11** as `needs_review`, and **128** as blocked (`no`).

### 3.4 Boundary

Saleh does not read the JSON content of any file in `02_mabniyat/` by any means other than the read-only prototype. The prototype's outputs at `/tmp/source_preview_mabniyat.csv` (and similar) are the canonical mediated view. The source path appears only as a string in any Saleh document under this contract; the bytes at that path are never copied into Saleh.

## 4. Mabniyat Source Classes

These are **source-review classes**, not a final grammar ontology. They are the labels under which the prototype-observed files are grouped for review purposes; they do not constitute a normative claim about classical Arabic mabniyat taxonomy.

| source-class label | source-side examples | review notes |
|---|---|---|
| **particles / fixed expressions** | `coordinating_conjunctions.json`, `copulative_particle.json`, `jazm_tools.json`, `letters_answers.json`, `preposition_meanings.json`, `present_naseb_tools.json`, `vocative_particles.json` | typically expose a single concrete Arabic surface field; usually high-provenance |
| **pronouns** | `pronouns_classification.json`, `hidden_pronouns.json` | concrete surface fields; some `form` fields rather than `name` |
| **demonstratives** | `demonstrative_pronouns.json` | typically `name` field carries the surface form (e.g. `هَذَا`) |
| **relative pronouns** | `relative_pronouns.json` | typically `name` field |
| **interrogatives** | `interrogative_letters_tools.json`, `interrogative_tools_categories.json` | typically `tool` field |
| **conditional forms** | `conditional_letters_tools.json` | typically `particle` field |
| **adverbial / circumstantial fixed forms** | `built_in_adverbs.json` | typically `adverb` field |
| **numerals or composite fixed forms** | `compound_numbers.json`, `compound_number_details.json` | review-only — the source files describe composite *numerical-formation rules*, not standalone surface forms |
| **rule/case-description** | `building_regulations.json`, `estimated_parsing_indeclinables.json`, `functional_indeclinable_substitutes.json`, `grammatical_construction_cases.json`, `imperative_verb_building.json`, `indeclinable_discourse_roles.json`, `past_tense_conjugation_rules.json`, `present_tense_building_cases.json`, `types_of_i3rab.json`, `verb_building_rules.json` | source-side *prose* describing rules / cases / taxonomies; typically *no* concrete Arabic surface field; flagged `weak_provenance` per § 8 |
| **other mabni categories pending review** | `kinaya_names.json`, `verb_name.json` | needs explicit category-by-category review before any pilot admission |

These nine labels are the **source-review classes**, not a final linguistic taxonomy. They are *useful for grouping files under review*, not *authoritative grammatical claims*. A future mabniyat pilot snapshot cycle is free to refine or re-group these labels under its own explicit review.

## 5. Surface-Field Priority Review

This is the central A3 section. The mabniyat corpus does not have a single uniform "Operator" column the way the awamil CSV does. Different JSON files expose different field names for the entry's surface form. § 5 codifies the priority review under which any future mabniyat pilot snapshot cycle selects a single surface candidate per entry.

### 5.1 The 9-way ordered priority

When reviewing a candidate surface form for a mabniyat entry, the reviewer (or any future prototype run mirroring this discipline) checks the entry's fields **in this exact priority order** and admits the first non-empty candidate. The priority order is descending in *evidence strength*:

| priority class | description | typical source-side fields |
|---|---|---|
| **1. explicit vocalized surface field** | A field that directly carries the entry's Arabic surface form with harakat preserved | `name`, `letter`, `preposition`, `particle`, `adverb`, `pronoun`, `form`, `tool`, `copulative_particle` (when any of these carries a fully voweled Arabic string) |
| **2. explicit unvocalized surface field plus vocalization evidence** | Same priority-1 fields when the candidate value is consonant-only but a sibling vocalization field or note disambiguates | priority-1 fields plus an `example` / `notes` field that vocalizes the surface |
| **3. title field used as surface candidate** | The entry exposes only a `title` field as a candidate surface — flagged `title_used_as_surface_candidate` per § 7 | `title` |
| **4. key field used as surface candidate** | The entry exposes only an identifier / lookup `key` as a candidate — typically a non-Arabic short string | `key`, `id`, `slug` (if present) |
| **5. example-derived candidate, review-only** | The entry has no priority-1..4 candidate but an `example` field contains an Arabic example sentence — a reviewer must inspect to decide whether to extract a single surface form (review-only; never auto-admit) | `example`, `example_sentence`, `examples` |
| **6. category-label-only row, blocked** | The entry exposes only a category label (e.g. `category`, `type`, `case_type`) — blocked from any surface-form admission | `category`, `type`, `case_type` |
| **7. prose-description-only row, blocked** | The entry exposes only descriptive prose (e.g. `description`, `definition`, `explanation`) — blocked from any surface-form admission | `description`, `definition`, `explanation` |
| **8. multi-surface row requiring split review** | The entry's primary field carries multiple surface forms joined (e.g. `هَذَا / هَذِهِ`, slash-separated, or comma-separated) — requires explicit split review before any pilot admission | priority-1 field whose value contains a separator |
| **9. missing-surface row, blocked** | None of the above applies — no candidate surface form recoverable from the entry — block, flagged `no_surface_candidate` | n/a |

### 5.2 Per-class disposition

For each priority class, the table below defines whether the resulting row may become `ready`, must be `needs_review`, or is `blocked`; whether it may enter a future mabniyat pilot snapshot; and whether it may enter runtime.

| priority class | may become `ready`? | review status when no other warning | future-snapshot eligibility | runtime eligibility |
|---|:---:|---|---|---|
| 1. explicit vocalized surface field | **yes** | `ready` | eligible (subject to all of § 14) | **NO — always** |
| 2. explicit unvocalized + vocalization evidence | yes (with reviewer note) | `needs_review` | eligible after reviewer note resolves the vocalization | **NO — always** |
| 3. title field used as surface candidate | no | `needs_review` (flagged `title_used_as_surface_candidate`) | **not eligible** unless a future mabniyat pilot policy explicitly admits title-as-surface (it should not) | **NO — always** |
| 4. key field used as surface candidate | no | `needs_review` | not eligible | **NO — always** |
| 5. example-derived candidate, review-only | no | `needs_review` (flagged `example_derived_candidate`) | not eligible without further source confirmation | **NO — always** |
| 6. category-label-only row, blocked | no | `no` | not eligible | **NO — always** |
| 7. prose-description-only row, blocked | no | `no` | not eligible | **NO — always** |
| 8. multi-surface row requiring split review | no | `needs_review` (flagged `multi_surface_requires_split_review`) | not eligible until split | **NO — always** |
| 9. missing-surface row, blocked | no | `no` (flagged `no_surface_candidate`) | not eligible | **NO — always** |

**Runtime eligibility is always `NO` under this contract.** This contract does not admit *any* mabniyat entry into Saleh runtime, registry, fixture, or data, regardless of priority class. The "runtime eligibility" column in the table above exists to make that boundary terminal-visible.

### 5.3 Worked illustrations (descriptive, source-side)

Three concrete mabniyat surface forms from the prototype's observation (verbatim from `/tmp/source_preview_mabniyat.csv`), illustrating priority class 1:

- **`حَيْثُ`** — from `built_in_adverbs.json`, source field `adverb`, source class *adverbial / circumstantial fixed forms*. Priority 1: explicit vocalized surface field.
- **`هَذَا`** — from `demonstrative_pronouns.json`, source field `name`, source class *demonstratives*. Priority 1: explicit vocalized surface field.
- **`لَمْ`** — from `jazm_tools.json`, source field `tool`, source class *particles / fixed expressions*. Priority 1: explicit vocalized surface field.

These are *worked illustrations of the priority review*, not *normative grammatical claims*. The forms appear in the source under the file/field/class shown; that source observation is recorded; nothing is claimed about Saleh's runtime interpretation of these forms.

## 6. Field-Name Mapping Per File Class

A future mabniyat pilot snapshot cycle, or any subsequent docs-only review cycle citing A3, will produce a per-entry normalized review row carrying the following normalized review fields. These names are **review metadata only**; they are *not* Saleh-canonical runtime types.

| normalized review field | meaning |
|---|---|
| `source_file` | the source JSON file basename |
| `source_entry_id` | the entry's stable identifier within the file (typically `id` when present) |
| `source_entry_index` | the entry's positional index within the file's `data[]` array (provenance fallback) |
| `source_class_label` | one of the source-class labels enumerated in § 4 |
| `surface_form_vocalized` | the candidate surface form selected per § 5, in NFC, harakat preserved (PR #86 § 12.1) |
| `surface_form_unvocalized_key` | the candidate surface form with harakat stripped — **diagnostic only**, never identity (PR #86 § 12.1, PR #103 § 7) |
| `surface_candidate_source_field` | the source-side field name from which the surface candidate was taken (e.g. `name`, `tool`, `title`, `adverb`) |
| `surface_priority_class` | which of the 9 priority classes (§ 5.1) the candidate is assigned to (1–9) |
| `example_vocalized` | the source-side `example` / `example_sentence` / `examples` value where present — **descriptive only**, never proof (PR #98 § 12.4) |
| `normalization_status` | one of `unique_identity` / `exact_duplicate` / `collision_member` / `source_data_discrepancy` |
| `review_status` | one of `ready` / `needs_review` / `no` |
| `provenance_strength` | one of `strong` (priority class 1) / `moderate` (class 2) / `weak` (classes 3–5, 8) / `blocked` (classes 6, 7, 9) |
| `discrepancy_status` | one of `none` / `awaiting_upstream` / `resolved_upstream_fixed` / `resolved_no_action_required` (per PR #105 § 5 workflow) |
| `snapshot_eligibility` | computed; one of `eligible` / `pending_review` / `not_eligible` (per § 14 / § 15) |
| `review_notes` | free-text reviewer notes (descriptive only) |
| `upstream_report_id` | the PR #105 finding identifier (e.g. `R-003`) if the row has triggered an upstream discrepancy report; empty otherwise |

These fields are **source-review metadata only**. None of them is consumed by Saleh runtime. None of them is part of any Saleh-canonical Candidate / Evidence / Carrier type. They exist purely so that a future mabniyat pilot snapshot cycle can record per-entry review evidence in a normalized form.

## 7. `title_used_as_surface_candidate` Handling

### 7.1 What this warning means

The `title` field, when present in a mabniyat JSON entry, is typically a *human-readable label* — often a multi-token Arabic phrase or descriptive heading — **not** a guaranteed lexical surface form for the mabni token. A surface form derived from a `title` field is at best an *approximation* of the entry's mabni surface; at worst it is descriptive prose with no surface-form interpretation.

### 7.2 Disposition under this contract

A mabniyat entry whose surface candidate comes from the `title` field (i.e. priority class 3 per § 5):

1. Must carry the warning code **`title_used_as_surface_candidate`** at severity **`warning`** in `warning_codes`.
2. Must be at least `needs_review` in `review_status`. It **may not be auto-promoted to `ready`** unless a future source-specific or pilot-specific rule explicitly proves the title-field's identity in that file/class.
3. Is **not eligible** for admission to any future mabniyat pilot snapshot, unless that future pilot policy explicitly permits title-as-surface — which this contract recommends against, but does not foreclose.
4. **Is never eligible for runtime admission**, regardless of any future pilot policy. This contract's runtime boundary (§ 13) is unconditional.

### 7.3 Prototype-observed scale

The prototype at `/tmp/source_preview_mabniyat.csv` flagged **23 entries** under `title_used_as_surface_candidate` across the rule/case-description and rare-category files. These entries are the canonical population this contract describes.

### 7.4 Why this is a *source-review caution*, not an error

A `title_used_as_surface_candidate` flag is **not** a claim that the source data is wrong. Many of the affected files (e.g. `types_of_i3rab.json`, `building_regulations.json`) genuinely describe *taxonomies* or *rules* where no single mabni surface is the entry's subject. Recording the `title` as a candidate surface — and flagging the substitution — is the *source-review-correct* response: it preserves traceability without overclaiming.

## 8. `weak_provenance` Handling

### 8.1 What this warning means

`weak_provenance` flags an entry whose surface candidate is **not derivable from an explicit, content-identifying source field at high confidence**. Examples of weak-provenance derivations:

- surface candidate derived from the source file's filename rather than from any field within the entry;
- surface candidate derived from a `title` field (also flagged separately under § 7);
- surface candidate derived from a `category` / `type` / `case_type` label;
- surface candidate derived from an `example` sentence (text-extracted by reviewer or prototype, never authoritative);
- surface candidate inferred by script (regex / heuristic) rather than read from an explicit source field.

### 8.2 Disposition under this contract

A mabniyat entry whose surface candidate carries the `weak_provenance` flag:

1. Must carry the warning code **`weak_provenance`** at severity **`warning`** in `warning_codes`.
2. Must be at least `needs_review` in `review_status`. It **must not be silently promoted to `ready`**. Promotion to `ready` requires an explicit reviewer note documenting why the weak-provenance derivation is defensible for this specific entry.
3. Is **not eligible** for admission to any future mabniyat pilot snapshot. The mabniyat pilot snapshot cycle will admit only entries whose `provenance_strength` is `strong` (priority class 1) or `moderate` (priority class 2 with reviewer note).
4. **Is never eligible for runtime admission.**

### 8.3 `weak_provenance` is a source-review caution, not a linguistic error

A `weak_provenance` flag is **not** a claim that the source data is wrong. Many mabniyat source files are organised around *grammatical rules*, *case taxonomies*, or *building procedures* — domains where no single mabni surface form is the entry's primary subject. The weak-provenance flag is the *source-review-correct* response: it records the *strength* of the surface-form attribution, not a verdict on the underlying linguistic content.

### 8.4 Prototype-observed scale

The prototype flagged **124 entries** under `weak_provenance` across roughly 10 files (the rule/case-description class enumerated in § 4). These are the canonical population this contract describes.

## 9. Per-Entry Evidence Requirements

For every mabniyat entry a future mabniyat pilot snapshot cycle admits under this contract, the following evidence must be recorded at snapshot time:

| field | role |
|---|---|
| `source_file` | the JSON file basename (provenance) |
| `source_entry_id` | the entry's stable identifier within the file (provenance) |
| `source_entry_index` | the entry's positional index (provenance fallback) |
| `source_class_label` | one of the labels from § 4 |
| `selected_surface_candidate` | the value chosen per § 5 |
| `surface_candidate_source_field` | which source-side field the candidate came from |
| `vocalization_evidence` | source-side citation for the candidate's harakat — `null` for priority class 1, a sibling-field reference for priority class 2 |
| `surface_priority_class` | one of 1–9 per § 5.1 |
| `provenance_strength` | one of `strong` / `moderate` / `weak` / `blocked` |
| `review_status` | one of `ready` / `needs_review` / `no` |
| `discrepancy_status` | one of `none` / `awaiting_upstream` / `resolved_upstream_fixed` / `resolved_no_action_required` |
| `reason_for_inclusion_or_exclusion` | one-line human-readable summary referencing the relevant § |
| `reviewer_note` | free text where applicable |
| `prototype_run_id` | pointer to the prototype script + invocation |
| `snapshot_id` | the mabniyat pilot snapshot's identifier, assigned at admission time |

**Evidence here is source-review evidence only.** It is **not** proof of meaning, *i'rāb*, *Amil* behaviour, hukm, dalalah, reality, or any other higher-layer claim. The evidence carrier defined here does **not** instantiate any Saleh-canonical Candidate or Evidence type; it lives purely in the documentation snapshot's body or frontmatter.

## 10. Identity Discipline

This contract re-binds PR #86 § 12.1 verbatim, plus the policy additions of PR #103 § 7:

1. **`surface_form_vocalized` is the identity carrier when present.** Two mabniyat entries have the same identity *as a surface form* if and only if their NFC `surface_form_vocalized` strings are codepoint-equal.
2. **Harakat must be preserved.** NFC normalization is mandatory at any review point; harakat are identity-relevant; a mabniyat review never strips harakat to compress identity.
3. **`surface_form_unvocalized_key` is diagnostic only.** It MAY appear in review tables for human readability (it makes collision patterns visible). It MUST NEVER be used as identity, lookup key, or comparison basis for admitting or merging entries. Unvocalized keys may *group* candidates for reviewer attention; they cannot *authorize* equality.
4. **Do not collapse vocalized distinctions.** Even where mabniyat entries share an unvocalized skeleton, the vocalized surfaces remain distinct identities. The classical illustrations from PR #103 / PR #105 / PR #106 apply equally here:
   - `مِنْ` (preposition, U+0645 U+0650 U+0646 U+0652) ≠ `مَنْ` (conditional, U+0645 U+064E U+0646 U+0652)
   - `إِنَّ` (emphasis) ≠ `إِنْ` (conditional)
   - `أَنَّ` (emphasis) ≠ `أَنْ` (infinitival)
   These collision pairs appear in the *awamil* corpus; they are cited here as *illustrations of the general identity rule*, not as mabniyat content. Equivalent vocalized distinctions within the mabniyat corpus (e.g. `هَذَا` masculine vs `هَذِهِ` feminine, both demonstratives) are governed by the same rule.
5. **Length and class labels are not identity.** `length_bucket` and `source_class_label` are diagnostic; two entries with the same length bucket or the same class label may be distinct identities; identity is `surface_form_vocalized` only.

## 11. `Example_Vocalized` Discipline

This contract re-binds PR #98 § 12.4 verbatim, reaffirmed by PR #103 § 9, PR #104 § 9, PR #105 § 9, and PR #106 § 8.

The `Example_Vocalized` field (and the source-side `example` / `example_sentence` / `examples` fields in general) is **descriptive only**. It may appear in a future mabniyat pilot snapshot's table for human review. It MUST NEVER be:

- proof of anything;
- a test fixture (without a separate, explicitly-authorised fixture contract that does not yet exist and is not opened here);
- runtime input to any Saleh layer;
- a substitute for the entry's source surface (priority class 5 captures the case where an example is consulted *only as a review aid*);
- *i'rāb* evidence;
- *Amil*-effect evidence;
- role proof;
- hukm / dalalah / meaning derivation evidence;
- identity. A mabniyat entry whose surface is derived only from an example sentence is `needs_review` (priority class 5); the example may help the reviewer choose a candidate, but the example itself does **not** become the entry's identity.

If a future mabniyat pilot snapshot cycle wishes to admit example-derived surfaces, it must do so via an explicit additional rule that:

- requires manual reviewer confirmation per entry;
- records the reviewer name + date + the extraction reasoning;
- never auto-admits;
- never treats the example sentence as Saleh-canonical evidence.

This contract does not open that future rule.

## 12. Discrepancy Integration

This contract binds `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) by citation. Detected discrepancies in the mabniyat corpus follow PR #105's reporting workflow (PR #105 § 5).

Specifically (re-binding from PR #105 § 9):

1. Saleh does **not** correct upstream source data, ever.
2. Mabniyat entries flagged with `true_source_discrepancy`, `descriptive_not_surface`, or `no_surface_candidate` are **blocked or `awaiting_upstream`** until PR #105's upstream resolution closes the finding.
3. Mabniyat entries with **weak but non-contradictory provenance** (e.g. only `weak_provenance` flagged, no `true_source_discrepancy`) are **`needs_review`** — they are not blocked, but they require explicit reviewer confirmation before any pilot snapshot admission.
4. New mabniyat findings (when discovered by subsequent prototype runs) will be assigned the next-available `R-NNN` identifier under PR #105's amendment workflow first (e.g. `R-003`, `R-004`, …), then mirrored into this contract via a future A3-amendment PR. This contract is never silently rewritten.

At the time of writing, the prototype found **no `true_source_discrepancy` rows in the mabniyat corpus** (R-001 and R-002 are *awamil* findings, owned by PR #106 § 13). The blocked-severity mabniyat warnings already present (`no_surface_candidate` ×101 and `descriptive_not_surface` ×27) are *not* discrepancies — they are *source-review observations* about file/entry structure, governed by §§ 5, 7, 8, 15 rather than PR #105.

## 13. Saleh-Side / Upstream-Side Boundary

This contract reaffirms PR #105 § 9 verbatim:

> Saleh has zero write access to `new_arabic_analyzer/`. A row that is wrong stays wrong until the upstream maintainer fixes it; only at the next prototype run does Saleh observe the change. The maintainer of `new_arabic_analyzer/` (the upstream) is the only authority that may *fix* source-side data. Saleh never silently corrects a discrepancy. The boundary is not crossable.

Specifically for mabniyat:

1. **Saleh records, reports, re-inspects.** Saleh never modifies upstream.
2. **No JSON file from `02_mabniyat/`** is copied into Saleh by this contract.
3. **No JSON entry from `02_mabniyat/`** is admitted into Saleh runtime / registry / tests / fixtures / data by this contract.
4. **No corrected local copy** of any mabniyat source file is created by this contract.
5. **The path `02_mabniyat/...` appears only as a string** in any Saleh document under this contract; the bytes at that path are never copied into Saleh.
6. This contract **only defines review discipline**. It does not perform review; it does not perform admission; it does not perform snapshot instantiation.

## 14. Inclusion Rules

A mabniyat entry is eligible for admission to a future mabniyat pilot snapshot cycle under this contract if and only if **all** of the following hold:

1. `source_file` and `source_entry_id` (or `source_entry_index` as fallback) are known and recorded.
2. The entry's `source_class_label` is one of the labels enumerated in § 4 (not `null`).
3. The entry's surface candidate is selected via § 5's priority review and is in **priority class 1** (explicit vocalized surface field). Priority class 2 (explicit unvocalized + vocalization evidence) is also admissible *with* a documented reviewer note. Priority classes 3–9 are not admissible without a future explicit pilot rule that has not been written.
4. `surface_form_vocalized` is NFC and harakat-preserving. The vocalization came from the source field directly (priority class 1) or from a documented reviewer note (priority class 2).
5. `provenance_strength` is `strong` (priority class 1) or `moderate` (priority class 2 with reviewer note). `weak` and `blocked` are not eligible.
6. `normalization_status` is `unique_identity`. (`exact_duplicate`, `collision_member`, `source_data_discrepancy` are excluded per § 15.)
7. `warning_codes` is **empty** — zero warnings of any severity, including `info`-severity `linkage_vowel_difference` (mirroring PR #103 § 5).
8. The entry is **not** flagged `title_used_as_surface_candidate` (§ 7) or `weak_provenance` (§ 8) — those flags are excluded by point 7 above, listed here for emphasis.
9. The entry has **no `Example_Vocalized` dependency for proof, fixture, runtime input, or evidence** (per § 11).
10. The entry has **no unresolved discrepancy**. Its `discrepancy_status` is `none` (no finding has been raised) or `resolved_upstream_fixed` (an earlier finding has been closed by upstream). `awaiting_upstream` and `resolved_no_action_required` (where the resolution did not change the source surface) are not admissible.
11. The entry's review status is `ready` (not `needs_review`, not `no`).
12. The provenance fields enumerated in § 9 are all recorded and verifiable.

**Runtime eligibility is always `NO`**, regardless of any of the above. This contract is the *source-review eligibility* contract; the *runtime eligibility* contract does not exist and is not opened by this PR. A future runtime cycle, if ever opened, would require its own constitutional review under the standing § 9 non-goals of the living handoff.

## 15. Exclusion Rules

The following entry classes are explicitly excluded from any future mabniyat pilot snapshot admission under this contract. Each excluded class has its own forward path (§ 16).

- **`missing-surface` rows (priority class 9)** — `no_surface_candidate` flag; blocked.
- **`prose-description-only` rows (priority class 7)** — `descriptive_not_surface` flag; blocked.
- **`category-label-only` rows (priority class 6)** — blocked.
- **`title-only` surface without explicit review (priority class 3)** — `title_used_as_surface_candidate` flag; blocked from auto-admission per § 7.
- **`example-only` surface without confirmation (priority class 5)** — review-only; blocked from auto-admission per § 11.
- **`weak_provenance` rows unresolved (§ 8)** — blocked until reviewer note resolves.
- **Multi-surface rows requiring split review (priority class 8)** — blocked until split.
- **Unresolved source discrepancies** — blocked or `awaiting_upstream` per PR #105 / § 12.
- **Rows where source correction is needed** — Saleh does not correct upstream; blocked until upstream resolves (PR #105 § 10).
- **Rows requiring runtime interpretation** — no mabniyat entry is admitted into runtime under this contract.
- **Any row whose interpretation would require `Word` / `Lafz` / `Dalalah` / `Meaning` / `Hukm` / `Reality` / `Amil` / `I'rāb` runtime** — out of scope of this contract; explicitly forbidden by § 17.
- **`collision_member` rows** — reserved for the SNAP-002 sibling cycle's collision-handling sub-contract (PR #106 § 14.1).
- **`exact_duplicate` rows** — reserved for the SNAP-003 sibling cycle.
- **`info`-severity-only rows (e.g. only `linkage_vowel_difference`)** — excluded from any zero-warnings admission, mirroring PR #103 § 5 and PR #106 § 12.
- **All `length_6_plus` rows** — info-severity, excluded from the zero-warnings admission for consistency with PR #103 § 5.
- **All `unknown_length` rows** — warning-severity, excluded.
- **All awamil rows** — covered by PR #106's A2 contract; out of scope for A3.

Exclusion is *deferral*, not *rejection*. Each excluded class has its own forward-reservation hook in § 16.

## 16. Forward-Reservation Hooks

This contract reserves the following future docs-only sibling contracts by name. **Each requires its own separately-authorised PR cycle. None is opened by this contract.**

1. **Mabniyat pilot snapshot policy** — a docs-only sub-contract (or amendment to PR #103) that specialises PR #103's general snapshot policy to the mabniyat corpus, including any explicit per-class admission rule needed to admit priority classes beyond 1.
2. **Mabniyat pilot snapshot instantiation** — a docs-only snapshot PR opened *after* the mabniyat pilot snapshot policy lands; cites this contract and the pilot policy; admits a small pilot subset of mabniyat entries that satisfy § 14. Mirrors the PR #103 → PR #104 SNAP-001 cadence.
3. **Duplicate / multi-surface handling sub-contract** — covers priority class 8 (multi-surface requires split review) and the broader cross-corpus exact-duplicate / multi-role concern. Sibling to the SNAP-003 hook already reserved by PR #106 § 14.3.
4. **Fixture contract** — *only if ever authorised*. A future docs-only contract that would permit specific mabniyat surfaces to become test fixtures under named restrictions. PR #98 § 12.4 controls; this hook is reserved for completeness but recommended against opening without strong cause.
5. **Source discrepancy report package** — a docs-only sibling contract that bundles outgoing upstream reports (one per PR #105 finding) into a coherent communication artefact. Not currently needed (the prototype found 0 mabniyat discrepancies), but reserved for the case where mabniyat findings accumulate.
6. **Bridge to runtime** — *only after explicit future carrier and producer contracts*. This is **not** a reservation to open a mabniyat runtime; it is a *hook* recording that any future runtime work would require its own carrier-then-producer cadence (mirroring the variant-resolver runtime built across PR #78 / #79 / #80 / #81 / #82 / #83 / #84). The standing § 9 non-goals of the living handoff govern; runtime opens only after constitutional amendment.

**Do not start any of these cycles in this PR.** This contract is the *source-review discipline* layer; subsequent cycles are *separate* PRs under their own explicit triggers.

## 17. Non-Goals

This contract explicitly does NOT:

- **modify the external source corpus** — Saleh has zero write access to `new_arabic_analyzer/02_mabniyat/`.
- **silently correct any discrepancy** — PR #105 controls; reaffirmed in § 12 / § 13.
- **adjudicate which cell or field is correct** in any discrepancy.
- **promote source-side classification to Saleh-canonical** — the § 4 source-class labels are *review labels*, not Saleh-canonical grammatical labels.
- **create any runtime layer**, adapter, producer, carrier, rule, evidence type, or candidate type derived from any mabniyat entry.
- **create any registry** under `src/qiyas_core/registries/` — no `ArabicMabniRegistry`, `ArabicAmilRegistry`, `ArabicMabniyatRegistry`, etc.
- **create any test or fixture** under `tests/`.
- **import any data** — no JSON file is copied from `new_arabic_analyzer/` into Saleh.
- **create any data file** under `data/`.
- **use `Example_Vocalized` as proof or runtime input** — PR #98 § 12.4 controls; reaffirmed in § 11.
- **instantiate a mabniyat pilot snapshot** — § 16 reserves the hooks but does not exercise them.
- **open `SNAP-002`** (collision-handling sub-contract or instantiation).
- **open `SNAP-003`** (duplicate-handling sub-contract or instantiation).
- **open Track B** — no `GlyphClassificationEvidence` runtime contract / carrier / producer; no `SifatVector` runtime.
- **open Track C** — no `يَ` admission; no madd-variant admission; no alif (`ا`) variant semantics.
- **open Track D** — no maintainer-side runtime follow-up to PR #99.
- **introduce `WordCandidate`**, `LafzCandidate`, `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`, `RealityClaim`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, or `OperatorGeometry`.
- **introduce `Amil` runtime, `I'rāb` runtime, `AmilEffectEvidence`, or `I'rabEffectEvidence`**.
- **introduce `Glyph` runtime, `SifatVector` runtime, or any higher-layer runtime**.
- **perform source correction** (Saleh-side).
- **write to the upstream corpus** — Saleh has zero write access, reaffirmed in § 13.
- **amend any predecessor contract** (PR #86 / PR #96 / PR #97 / PR #98 / PR #103 / PR #105 / PR #106).
- **edit `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md`** — PR #104's snapshot is frozen.
- **engage PR #99** or any other unrelated PR.
- **claim that mabniyat rows are proven grammatical facts**. Mabniyat entries are *source observations under review*; no Saleh-canonical grammatical truth is claimed.
- **claim that Saleh solves Arabic mabniyat**.

## 18. Summary Table

| concept | status in A3 | may affect future snapshot? | may affect runtime? | notes |
|---|---|---|---|---|
| mabniyat source file | inventoried by § 3; 29 files at prototype run time | yes — eligibility computed at admission time | **no** — never | inventory record per file required at snapshot time |
| source entry | per-entry review record per § 9 | yes — under § 14 / § 15 | **no** — never | entry id + entry index required |
| `surface_form_vocalized` | **identity carrier** (PR #86 § 12.1) | yes — must be NFC, harakat preserved | **no** — never consumed by runtime | the only identity field |
| `surface_form_unvocalized_key` | **diagnostic only** | yes — display / collision-visibility aid | **no** — never identity, never lookup | must never be used to authorize equality |
| surface priority class | computed per § 5.1; one of 1–9 | yes — only classes 1 and 2 are admissible without future explicit policy | **no** — never | the central A3 review discipline |
| `title_used_as_surface_candidate` | warning flag per § 7; severity `warning` | **not admissible** without explicit future rule | **no** — never | 23 entries flagged by prototype |
| `weak_provenance` | warning flag per § 8; severity `warning` | **not admissible** until reviewer note resolves | **no** — never | 124 entries flagged by prototype |
| `Example_Vocalized` | **descriptive only** (PR #98 § 12.4) | yes — display aid in snapshot tables | **no** — never proof / fixture / runtime input | reaffirmed in § 11 |
| true source discrepancy | flagged by PR #105 workflow; severity `block` | **not admissible** until upstream resolution | **no** — never | no mabniyat true_source_discrepancy at prototype run time |
| `ready` row | per § 14; priority class 1, no warnings, no discrepancy, NFC vocalized identity | **yes** — eligible for mabniyat pilot snapshot | **no** — never | runtime boundary unconditional |
| `blocked` row | per § 15; multiple disjoint causes | **no** — not eligible | **no** — never | excluded with explicit reason |
| mabniyat pilot | reserved future cycle per § 16.1 / § 16.2 | n/a — the pilot itself is the snapshot | **no** — never | not opened by this PR |
| runtime registry | **explicitly excluded** | n/a | **no** — never | § 17 controls; standing § 9 non-goals also apply |

End of contract.
