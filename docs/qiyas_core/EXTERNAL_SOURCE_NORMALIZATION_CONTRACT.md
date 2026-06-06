# External Source Normalization Contract

> **Type:** Docs-only constitutional contract (normalization boundary).
>
> **Status:** Defines the rules under which future docs-only **source-table contracts** may translate external Arabic source corpora into normalized source-table rows. Does **not** itself perform normalization, copy data, create a registry, or introduce a runtime.
>
> **Authority basis (read-only citation):**
>
> - `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) — especially §12 and §12.1 (Vocalized Source Identity Discipline)
> - `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) — the inventory this contract presupposes
> - `MIU_VARIANT_RESOLUTION_USAGE_NOTE.md` (PR #84)
> - `GLYPH_CLASSIFICATION_GATE_CONTRACT.md` (PR #85)
> - `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` (PR #71)
> - `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` (PR #72)
> - `SOURCE_OF_TRUTH_REGISTRY.md`
> - `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`
> - `CLAUDE.md` §0 / §2 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20 / §21

---

## 1. Purpose

This contract defines **how** external Arabic source corpora **may be normalized** into future source-table rows **without changing runtime behaviour**. It is a documentation/data-preparation boundary — it fixes the rules of the normalization step but does not perform it.

Two known external corpora are scoped (per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md`):

```
/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/
/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv
```

The contract states explicitly:

- **Source normalization is a documentation / data-preparation boundary.** It produces *future source-table rows*, nothing else.
- **It is not runtime.** No `Candidate`, no Evidence carrier, no rule, no gate, no producer is created.
- **It is not registry admission.** A normalized row is not licensed for runtime use by appearing in a source table; an additional, separate constitutional step is required.
- **It is not proof of grammatical operation.** A normalized row records what an external source says; it does not assert *i'rāb*, meaning, *dalālah*, *hukm*, or reality.

This contract is the **third** docs-only artifact in the awamil/mabniyat external-source cycle, after PR #86 (source contract) and PR #96 (inventory). It is preparatory for, but does not start, the detailed source-table contracts of §19.

---

## 2. Relationship to Existing Contracts

This contract subordinates itself to and **refines** (does not amend) the following existing contracts:

- **`ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86)** — the binding source-corpus seed contract.
  - **§12 (What May Be Recorded)** — reserves the field set for future source-table rows.
  - **§12.1 (Vocalized Source Identity Discipline)** — fixes the identity-carrier rule and the six binding rules around `collision` / `exact_duplicate` / `source_data_discrepancy`.

- **`EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96)** — records the two external paths, the per-corpus shape and gaps, and applies §12.1 to the observed external operators CSV.

Terms reused **verbatim** from §12 / §12.1 and from the inventory (this contract does not introduce new vocabulary):

```text
surface_form_vocalized        (identity carrier, NFC, includes harakat)
surface_form_unvocalized_key  (diagnostic only, NFC, harakat stripped)
collision                     (same unvocalized_key, different vocalized_form)
exact_duplicate               (same vocalized_form, >1 rows)
source_data_discrepancy       (row-internal contradiction between fields)
verification_status           (pending / verified_one_source / verified_multiple_sources / etc.)
```

This contract **does not amend** §12 / §12.1 or the inventory; it cites them. Anything in this contract that would conflict with PR #86 §12 / §12.1 is to be read as **superseded by PR #86**.

---

## 3. Normalization Boundary

The **only allowed** future operation that this contract licenses (subject to the detailed source-table contracts of §19):

```text
external source row  →  normalized source-table row
```

The following are **explicitly forbidden** even after normalization — see §16 for the exhaustive list, restated here briefly:

```text
external source row  →  runtime registry              ❌
external source row  →  AmilEffectEvidence            ❌
external source row  →  I'rabEffectEvidence           ❌
external source row  →  WordCandidate                 ❌
external source row  →  LafzCandidate                 ❌
external source row  →  DalalahCandidate              ❌
external source row  →  FinalMeaning                  ❌
external source row  →  HukmCandidate                 ❌
external source row  →  RealityClaim                  ❌
external source row  →  ArabicVariantResolver result  ❌
external source row  →  GlyphClassificationGate result ❌
external source row  →  SifatVector value             ❌
external source row  →  MIU acceptance                ❌
```

Normalization produces **rows in a documentary table**. It does not produce evidence, candidates, or runtime admissions.

---

## 4. Identity Discipline

Re-stated as binding, verbatim from PR #86 §12.1:

```text
surface_form_vocalized        = identity carrier
surface_form_unvocalized_key  = diagnostic only
```

**Harakat MUST NOT be stripped for identity.** The identity key is `surface_form_vocalized`.

Examples (codepoint-level distinctions that any future normalization MUST preserve):

```text
مِنْ   (preposition; codepoints U+0645 U+0650 U+0646 U+0652)
       ≠
مَنْ   (conditional / interrogative noun; codepoints U+0645 U+064E U+0646 U+0652)

إِنَّ   (mushabbihah — emphasis particle)
       ≠
إِنْ   (conditional jussive particle)

أَنَّ   (mushabbihah — emphasis particle)
       ≠
أَنْ   (maṣdariyyah — sub-clause introducer)
```

Any future normalization step that would merge a pair on either side of an `≠` above is **constitutionally invalid**.

---

## 5. Unicode and Normalization Rules

Future source-normalization MUST follow these rules. They are stated here as **rules to be applied later**, not as operations to be applied now.

- **Use Unicode NFC** for the stored `surface_form_vocalized`.
- **Preserve harakat in identity.** Do not strip them.
- **Preserve** shadda (U+0651), sukun (U+0652), tanwin (U+064B–U+064D), maddah (U+0653), hamza marks (U+0654–U+0655), alif khanjariya (U+0670), and any other letter-modifying combining marks present in the source.
- **Do not silently normalize away distinctions** (e.g., do not collapse alif-hamza-above `أ` U+0623 onto bare alif `ا` U+0627; do not collapse alif maqsurah `ى` U+0649 onto ya `ي` U+064A; do not collapse taa marbuta `ة` U+0629 onto haa `ه` U+0647). Such collapses, if ever desired for a *diagnostic key*, may live only on `surface_form_unvocalized_key`, never on identity.
- **Record the original raw cell** alongside the normalized cell when they differ. The normalized form does not replace the raw form; it complements it.
- **Record codepoints** for any audited discrepancy (e.g., when raw and NFC differ, when a row carries doubled diacritics, when a codepoint outside the expected Arabic ranges appears).

**These rules are to be applied by a future source-table contract.** This contract does not implement them now.

---

## 6. Diagnostic Keys

`surface_form_unvocalized_key` is a **diagnostic key**, never an identity.

**Allowed uses (future):**

- indexing,
- collision detection,
- search across vocalized variants,
- grouping for human-readable reports,
- audit reports that surface unvocalized-key collisions explicitly.

**Forbidden uses (any time):**

- identity (forbidden by PR #86 §12.1 rule 3),
- deduplication based on the diagnostic key (forbidden — would merge distinct identities),
- registry keys,
- runtime admission of any kind,
- automatic merging across vocalized forms.

If a future system needs a stable identifier, it MUST use `surface_form_vocalized` as the primary key.

---

## 7. Collision Handling

```text
collision  =  same surface_form_unvocalized_key  +  different surface_form_vocalized
```

**Required future behaviour** when normalization encounters a collision:

- **Preserve each vocalized form as a distinct row.**
- **Surface the collision explicitly** (e.g., in a diagnostic report or as a marker field on each colliding row).
- **Do not merge** the rows.
- **Do not choose one vocalization as canonical** for the collision; both are canonical at their own identities.
- **Require source citation and `verification_status`** on each row independently.

Known collision pairs observed in the external operators CSV (per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` §8):

```text
إِنَّ  ≠  إِنْ      (unvocalized key: إن)
أَنَّ  ≠  أَنْ      (unvocalized key: أن)
مَا   ≠  ما        (unvocalized key: ما)
أي    ≠  أيَّ      (unvocalized key: أي)
إِذًا  ≠  إذا      (unvocalized key: إذا)
```

Any future normalization that would silently collapse a pair above is a violation of this contract.

---

## 8. Exact Duplicate Handling

```text
exact_duplicate  =  same surface_form_vocalized  appearing in  >1 source row
```

**Required future behaviour:**

- **Keep rows separate** if `Purpose/Usage`, traditional group, or source row id differs.
- **Do not collapse** multi-role operators into a single multi-purpose row **unless** a strictly later contract authorises a multi-role aggregation shape (with its own constitutional review).
- **Record distinct source purposes** verbatim on each row.

Known genuine exact-vocalized multi-role forms observed in the external operators CSV (per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` §8):

```text
بِ   (مرور-قرب  /  قسم)        — 2 rows
وَ   (قسم  /  تقليل  /  معية)    — 3 rows
لَا  (نفي  /  نهي)              — 2 rows
```

For `مِنْ`, the binding rule (per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` §9 and §10): **`مِنْ` is excluded from the genuine multi-role list** because one of the two `مِنْ`-coded rows in the external CSV is a known `source_data_discrepancy` (the `Operator` cell carries `مِنْ` while the same row's `Example_Vocalized` uses `مَنْ`). Until the upstream corpus is corrected, that row cannot count as evidence of multi-role status for either `مِنْ` or `مَنْ`.

---

## 9. Source Data Discrepancy Handling

```text
source_data_discrepancy  =  source-internal contradiction between fields
                            of the same row
```

**Canonical example** (the `مِنْ` / `مَنْ` row in the operators CSV — see `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` §9):

```text
Operator cell        :  مِنْ
Example_Vocalized    :  مَنْ يَرْحَمْ يُرْحَمْ
Purpose/Usage        :  للشرط
English Group Name   :  Conditional (Jussive Only)
Classification       :  source_data_discrepancy
```

**Required future behaviour:**

- **Flag the row** as `source_data_discrepancy` in the normalized table.
- **Do not correct silently.** Saleh/Qiyas does not write to the external source.
- **Do not choose one field as canonical.** Neither the `Operator` cell nor the `Example_Vocalized` field is privileged over the other inside Saleh/Qiyas without an upstream correction.
- **Do not use the discrepant row as evidence of multi-role status** (rule 6 of §12.1 binds).
- **Refer back to the upstream maintainer or require an explicit correction PR in the external corpus** before a discrepant row may reach any non-`pending` `verification_status` (see §12).

The classical distinction `مِنْ` (preposition of ابتداء الغاية) vs `مَنْ` (conditional / interrogative noun) **remains binding under PR #86** regardless of the upstream-CSV state.

---

## 10. Mabniyat JSON Normalization

For the future normalization of the mabniyat JSON corpus at `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/`, the per-file surface-form field MAY map to `surface_form_vocalized` **only when** the field actually contains the surface form.

Variable surface-form field names observed in the inventory (per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` §5):

```text
name
letter
preposition
particle
adverb
pronoun
form
tool
title
copulative_particle
```

Mapping rule (binding for any future source-table PR):

```text
mabniyat external field  →  surface_form_vocalized
   (IF AND ONLY IF the field actually contains the surface form
    AND not a meta-title, descriptive label, or section header)
```

The field name `title` is the canonical example of a **meta-title** that is **not** a surface form (e.g., entries in `building_regulations.json` use `title` to record a chapter heading like "الأحكام الخاصة بالمبنيات", not a *mabnī* lexical surface). Such fields **MUST NOT** be treated as a surface identity.

The future source-table PR MUST decide per file (and per row, where necessary) whether a given field is a surface form or a meta-title, and MUST record that decision verbatim.

---

## 11. Operators CSV Normalization

For the future normalization of the operators CSV at `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`, the binding field mapping is:

| CSV field | Future normalized field | Note |
|---|---|---|
| `Operator` | `surface_form_vocalized` | identity carrier |
| stripped `Operator` (computed) | `surface_form_unvocalized_key` | diagnostic only |
| `Group Number` | `source_group_number` | descriptive |
| `Arabic Group Name` | `traditional_group` | descriptive |
| `English Group Name` | `traditional_group_en` | descriptive |
| `Purpose/Usage` | `source_purpose_note` | descriptive |
| `Example` | `example_unvocalized` | descriptive |
| `Example_Vocalized` | `example_vocalized` | descriptive; also the row-internal signal for `source_data_discrepancy` detection (§9) |
| `Note` | `source_parse_note` | descriptive |

**Important note on the `Note` field:** the source CSV's `Note` column may carry classical *i'rāb*-style prose (e.g., "الباء: حرف جر، زيد: اسم مجرور"). This is recorded as a descriptive `source_parse_note` — it does **NOT** create structured `I'rabEffectEvidence`, does NOT license any runtime *i'rāb* claim, and does NOT translate into runtime semantics. The `Note` field is a citation of what the external source records, not an evidence carrier.

---

## 12. Verification Status

Reserved future values for the `verification_status` field on normalized rows (refining PR #86 §12's three-value set):

```text
pending
verified_one_source
verified_multiple_sources
source_data_discrepancy
rejected
needs_upstream_correction
```

**Rules:**

- A row carrying `source_data_discrepancy` **cannot** be `verified_*`. It must be `source_data_discrepancy` or `needs_upstream_correction` until the upstream corpus is corrected.
- A row with only one weak provenance anchor (e.g., the `al_bab_althani_id` single-chapter reference observed in the mabniyat corpus per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` §13) **should remain conservative** — typically `pending` or `verified_one_source`, never `verified_multiple_sources`.
- **External appearance does not equal canonical admission.** A row reaching `verified_multiple_sources` in the normalized table does **NOT** thereby become a Saleh/Qiyas registry entry or a runtime input. Admission to runtime requires a strictly later, separately-authorised constitutional step.

The `needs_upstream_correction` value is the operational sibling of `source_data_discrepancy`: the discrepancy is the classification; the upstream-correction request is the action item.

---

## 13. Provenance Requirements

Future normalized source rows MUST preserve the following provenance fields (no actual data is added by this contract):

```text
external_path                 — verbatim path of the external file
source_file                   — basename of the file inside that path
source_row_number             — for CSVs, the 1-based line number
source_entry_id               — for JSONs, the file-local `id`
source_field_name             — which external field contributed
                                 the surface form / the parse note / etc.
raw_value                     — the cell content verbatim before any
                                 normalization
normalized_value              — the NFC-normalized value (when different)
source_reference              — citation anchor present in the source
                                 (e.g., `al_bab_althani_id`); recorded
                                 verbatim with no upgrading of provenance
                                 strength
inspection_timestamp          — when the external file was inspected
                                 OR
snapshot_reference            — an upstream commit SHA / file checksum
                                 / pinned snapshot identifier; whichever
                                 §15 settles on
verification_status           — one of the §12 values
```

**No actual data is added now.** This contract reserves the field names and discipline; the detailed source-table contracts of §19 populate them.

---

## 14. Length Bucket Discipline

`length_bucket` is a **diagnostic partitioning**, never an identity statement (per PR #86 §6 and §12.1 effect note).

**Rules:**

- `length_bucket` MAY ignore harakat for counting Arabic letter-glyph codepoints (range `0x0621–0x064A`).
- `length_bucket` MUST NOT override identity. Two distinct `surface_form_vocalized` identities MAY fall into the same `length_bucket`.
- `length_bucket` MUST NOT imply MIU acceptance. A surface form being recorded at `length_1` does NOT license MIU to admit it.
- **`length > 1` remains incompatible with the MIU `length == 1` gate** (per `MIU_VARIANT_RESOLUTION_USAGE_NOTE.md` and `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`) unless a strictly later non-MIU layer consumes it.
- `length_bucket` MUST NOT prove wordhood or operatorhood. It is a structural index into the source corpus, nothing else.

PR #86 §6 partitions the *mabniyat* source corpus by length buckets 1–5; the inventory §6 records that 61 entries fall at `length_6+` (outside the initial scope). A future source-table PR may decide whether `length_6+` is admitted into the source table or held aside for a separate scope-widening amendment of PR #86; this contract does **not** decide.

---

## 15. Source Snapshot Discipline

Because both external paths live **outside** Saleh/Qiyas (under `~/fractal/new_arabic_analyzer/`), future inventory/source-table PRs MUST declare which form of source reference they are using. The five reservable forms:

1. **Live external path reference** — the PR cites the path verbatim; consuming the data later re-reads whatever is at that path. Cheapest; most fragile.
2. **Snapshot hash** — the PR records a content hash (e.g., SHA-256) of the external file at inspection time. Robust to upstream mutation but does not preserve the data.
3. **Copied source fixture** — the PR copies the external file (in part or in full) into a fixture directory inside Saleh. **This option requires its own constitutional amendment** because it involves data import — see §17 non-goals.
4. **Upstream commit SHA** — if and when the external sources are themselves under git, the PR records the upstream repo and commit SHA. Strong provenance; depends on the upstream being a git repo.
5. **Manual transcription** — the PR transcribes the entries verbatim into the contract document itself. Slow; readable; preserves data inside Saleh as text rather than as a data file.

**This contract does NOT choose one** of the five forms. It reserves the menu so that a future source-table PR can declare a single choice and be held to it.

---

## 16. Forbidden Jumps

Explicitly forbidden under this contract — at the normalization layer, the source-table layer, and the citation layer:

```text
normalized source row  →  runtime registry                      ❌
normalized source row  →  MIU acceptance                        ❌
normalized source row  →  AmilEffectEvidence                    ❌
normalized source row  →  I'rabEffectEvidence                   ❌
normalized source row  →  WordCandidate                         ❌
normalized source row  →  LafzCandidate                         ❌
normalized source row  →  SentenceCandidate                     ❌
normalized source row  →  DalalahCandidate                      ❌
normalized source row  →  FinalMeaning                          ❌
normalized source row  →  HukmCandidate                         ❌
normalized source row  →  RealityClaim                          ❌
normalized source row  →  FinalCaseJudgment                     ❌
normalized source row  →  ArabicVariantResolver decision        ❌
normalized source row  →  GlyphClassificationGate output        ❌
normalized source row  →  SifatVector output                    ❌
normalized source row  →  MinimalIndependentMeaningCandidate    ❌
unvocalized_key collision  →  merged single identity            ❌
exact_duplicate row pair   →  collapsed multi-purpose row       ❌
source_data_discrepancy    →  silent correction                 ❌
weak-provenance row        →  verified_multiple_sources         ❌
```

A normalized source row is a documentary artifact, not an operational one.

---

## 17. Non-Goals

This PR is **docs-only** and explicitly does not include, propose, or imply:

- no code (no `src/` change)
- no tests (no `tests/` change)
- no data copy from `new_arabic_analyzer/`
- no `data/` directory addition or modification
- no registry (no `ArabicAmilRegistry` / `ArabicMabniRegistry` / new registry module of any kind)
- no runtime (no Evidence carrier, no `Candidate`, no rule, no gate, no producer)
- no source-table creation in this PR (the source tables are §19 follow-ups)
- no source-normalization execution in this PR (this contract is rules-only)
- no external CSV correction
- no external JSON correction
- no PR #94 alphabet-coordinate test-failure fix
- no `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`
- no `SentenceCandidate` / `ParagraphCandidate` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate` / `MinimalIndependentMeaningCandidate`
- no `Composition` / `Style` / `Ifādah` / `Tanzīl` runtime
- no `Amil` layer runtime / no `I'rab` runtime
- no `ArabicVariantResolver` expansion
- no MIU adapter amendment
- no `GlyphClassificationGate` contract amendment / no Glyph runtime
- no `SIFAT_VECTOR_CONTRACT.md` amendment / no `SifatVector` runtime
- no `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` amendment (cites only)
- no `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` amendment (cites only)
- no `__init__.py` change
- no `run_qiyas.py` change
- no `experimental/` change
- no second PR

---

## 18. Relationship to PR #94 Failures

The full canonical Saleh test suite currently reports **1081 passed, 5 failed, 4 skipped**. All 5 failures are isolated to `tests/qiyas_core/test_full_alphabet_coordinates.py` (PR #94 — alphabet coordinate enrichment for codepoints `ذ` U+0630, `ظ` U+0638, `ه` U+0647).

This contract states:

- **The 5 PR #94 failures are out of scope** of this docs-only normalization contract.
- **This contract does not fix or worsen them.** It is docs-only and touches no test, no runtime, no registry.
- **The full suite MAY remain non-green** until PR #94 failures are addressed in a strictly separate PR.
- **The focused variant/MIU test** (`tests/qiyas_core/test_variant_resolver_miu_integration.py`) remains the **appropriate non-blocking smoke check** for this docs-only PR — it pins the layer that PR #86 / #96 / this contract belong to, and remains green under all merges in this cycle.

A separate read-only investigation note has been written at `/tmp/pr94_alphabet_coordinate_failure_investigation.md` (outside this repository, not committed). The fix, if pursued, will be a strictly separate PR; its title and shape are recommended at the end of that note.

---

## 19. Future Work

Safe future PRs (each requires its own explicit trigger; each must pass its own preflight; each must respect all standing non-goals):

1. **`docs(qiyas_core): define Arabic awamil detailed source table contract`** — per-entry constitutional table for the 98 lafẓī + 2 ma‘nawī under strict citation discipline, applying the §11 mapping verbatim.
2. **`docs(qiyas_core): define Arabic mabniyat detailed source table contract`** — per-entry constitutional table for the *mabniyat* corpus, applying the §10 mapping discipline.
3. **`docs(qiyas_core): define source discrepancy reporting contract`** — formalises the `source_data_discrepancy` flag's machine-readable shape and the maintainer-reporting workflow.
4. **`docs(qiyas_core): define external source snapshot policy`** — chooses among the five §15 forms (live path / hash / fixture / upstream SHA / transcription) and binds the project to a single discipline.

What is **NOT** future work and **MUST NOT** be recommended next:

- runtime carriers / producers / registries for any of the above,
- `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`,
- `Amil` runtime / `I'rab` runtime / `OperatorGeometry` runtime,
- `MinimalIndependentMeaningCandidate` / `SentenceCandidate` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate`,
- bundling the PR #94 fix with any of the above,
- any direct data copy from external paths into Saleh/Qiyas without going through the §15 snapshot-policy decision first.

---

## 20. Summary Table

| Question | Answer |
|---|---|
| Is this runtime? | No. Docs-only normalization contract. |
| Does it copy data? | No. |
| Does it normalize data now? | No. Defines the rules; execution is a §19 follow-up. |
| Does it create a registry? | No. |
| What is the identity key? | `surface_form_vocalized` (per PR #86 §12.1). |
| What is the stripped key? | Diagnostic only (per PR #86 §12.1 rule 3). |
| What about `مِنْ` / `مَنْ`? | Distinct identities (codepoints `U+0650` vs `U+064E` at position 2). |
| What about source contradictions? | `source_data_discrepancy` (per PR #86 §12.1 rule 6); flagged, not silently corrected. |
| What about PR #94 failures? | Out of scope of this docs-only PR; separate investigation at `/tmp/pr94_alphabet_coordinate_failure_investigation.md`; future fix would be a separate PR. |
| What is next? | Detailed source-table docs (§19 item 1 or 2) / discrepancy reporting (§19 item 3) / snapshot policy (§19 item 4). |

---

**Document version:** 1.0
**Last updated:** 2026-06-06
**Status:** External source normalization contract (docs-only).
**Authority:** Subordinate to `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` §12 / §12.1 and to `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md`. Does not amend either. Records the normalization rules that govern future docs-only source-table contracts.
