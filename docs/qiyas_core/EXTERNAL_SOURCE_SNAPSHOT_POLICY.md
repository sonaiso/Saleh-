# External Source Snapshot Policy

> **Status**: docs-only constitutional policy.
> **Authority**: extends `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) and binds `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) §12.1 / `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) §12.4.
> **Scope**: defines how a *future* first snapshot from `new_arabic_analyzer/data/` would be admitted into Saleh's documentation corpus, with a 13-row pilot subset cited as an *illustrative candidate only*.
> **Non-Authority**: does NOT admit any row, identity, taxonomy, or example into Saleh runtime, registries, tests, fixtures, or data files.

---

## 1. Purpose

This document codifies the policy under which a *future* first external-source snapshot from
`/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`
may be admitted into Saleh's documentation corpus as a reserved snapshot form. It exists to make four things explicit:

1. The constitutional shape of the *first* snapshot — operators-only, group-bounded, identity-verified, manually reviewable.
2. The inclusion / exclusion rules that any candidate first-snapshot row must satisfy.
3. The identity, warning, and `Example_Vocalized` disciplines that any snapshot snapshot must inherit verbatim from PR #86 §12.1, PR #97, and PR #98 §12.4.
4. The boundary of this policy — what it does and does not authorise — so that future readers cannot mistake the policy for a runtime authorisation, a registry, or a data import.

This is a *policy* document. No code, no data, no test, no registry, no runtime change ride on top of it. The PR that opens this policy is docs-only. A future *separate* PR — and only that PR — could later perform the snapshot under this policy. Even that future PR would be docs-only / data-only and would not produce runtime code.

## 2. Relationship to External Source Normalization Contract

This policy is the *application* layer of `docs/qiyas_core/EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97). The normalization contract defines:

- NFC normalization,
- collision / exact-duplicate / source-data-discrepancy workflow,
- `verification_status` reservation,
- five reserved snapshot forms (§15 of PR #97): `raw`, `shadowed-with-overlays`, `normalized-table`, `vocalized-NFC-clean`, `curated-subset`.

This snapshot policy *chooses one* of those forms for the first snapshot — `normalized-table` — and binds it to the operators-only domain. It does NOT redefine, weaken, or override any rule of PR #97. Where a sentence in this document could be read as conflicting with PR #97, PR #97 controls.

It is also bound by `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) §12.1 (Vocalized Source Identity Discipline: `surface_form_vocalized` is identity, `surface_form_unvocalized_key` is diagnostic only, `مِنْ ≠ مَنْ`) and by `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) §12.4 (`Example_Vocalized` is future fixture material, forbidden as runtime input / i'rāb proof / role proof / fixture). Both bindings hold absolutely.

## 3. Snapshot Policy Boundary

This policy defines what would land in `docs/` if a future snapshot PR were opened. It explicitly does **not**:

- admit any row into `src/`, `tests/`, `data/`, or any registry under `src/qiyas_core/registries/`;
- create a runtime adapter, carrier, producer, or rule for any operator;
- produce evidence, candidates, residuals, or any kernel-touching artefact;
- assign Saleh-canonical taxonomy labels to source rows (the source's group labels are recorded *as the source's own classification*, never as Saleh's);
- license `Example_Vocalized` as fixture material in any form;
- authorise *any* runtime layer above Layer 1 (LetterIdentityCarrier) or Layer 2 (ArabicLetterCoordinateCarrier) to consume snapshot rows;
- authorise any `Word` / `Lafz` / `Dalalah` / `Meaning` / `Hukm` / `Reality` / `Amil` / `I'rāb` runtime work.

A snapshot under this policy is a **documentation snapshot**: a frozen, NFC-clean, traceable, manually-reviewed slice of the external corpus reproduced in Saleh's docs for archival and reference purposes. It is descriptive, not normative; documentary, not authoritative.

## 4. First Pilot Snapshot Candidate

The first pilot snapshot subset is **operators-only** and **group-bounded to group 1** (الجر فقط الدلالية — "Prepositions Only — Semantic") from the source CSV `operators_catalog_split_vocalized.csv`. A read-only normalization prototype produced under PR #97's discipline (`/tmp/source_preview_runner.py` and its five outputs in `/tmp/source_preview_*`) **recommended 13 rows** that meet every inclusion rule of § 5 below and trip no warning of any severity. Those 13 rows are cited *for illustration only* in the table of § 16. They are:

```
إِلَى ، فِي ، تَ ، لِ ، رُبَّ ، عَلَى ، كَ ، مُذْ ، مُنْذُ ، حَتَّى ، حَاشَا ، عَدَا ، خَلَا
```

The 13-row candidate set is documented in detail (with inclusion reasons, codepoints, identity status, and risks) at:

- `/tmp/first_snapshot_subset_recommendation.md`
- `/tmp/first_snapshot_subset_preview.csv`

Those `/tmp` artefacts are *prototype output*. They are not canonical data. They are not part of this docs PR. They are not licensed to be copied into Saleh by this PR. **Citation of the 13-row subset in this document is for policy illustration only and does not constitute data import, registry creation, or runtime authorisation.**

## 5. Inclusion Rules

A row from `operators_catalog_split_vocalized.csv` is *eligible* for the first pilot snapshot if and only if **all** of the following hold:

1. `source_kind == "operators_csv"` (excludes any future mabniyat or other-source rows).
2. `group_number == "1"` (the source CSV's column `Group Number`, value `1`, label `الجر فقط الدلالية`).
3. `identity_status == "unique_identity"` per the warnings ledger produced by the normalization prototype.
4. `normalized_row_ready == "yes"` per the same prototype.
5. `warning_codes` is empty for that row — **zero warnings of any severity**, including `info`-severity `linkage_vowel_difference`.
6. The row's `surface_form_vocalized` is NFC-normalized and fully voweled (every consonant carries its expected haraka; no missing harakat).
7. The row has no `partial_vocalization`, no `collision_same_unvocalized_key`, no `exact_duplicate_surface`, no `true_source_discrepancy`, no `linkage_vowel_difference`.

Eligibility per these rules in the current source CSV yields **13 rows**.

## 6. Exclusion Rules

The following rows are *deliberately* excluded from the first pilot snapshot, and the snapshot-PR description must record each exclusion class verbatim:

- Any row outside `operators_csv` (no mabniyat, no other source).
- Any row outside `group_number == "1"`.
- Any row with `identity_status` other than `unique_identity`. In particular:
  - **`collision_member`** — including `مِنْ` (preposition, U+0645 U+0650 U+0646 U+0652), which collides with `مَنْ` (conditional, U+0645 U+064E U+0646 U+0652) on the unvocalized skeleton `من`. **Both are real, distinct, constitutional identities** per PR #86 §12.1; both are reserved for a separate later snapshot under explicit collision-handling rules. They are NOT excluded because they are uncertain; they are excluded because the *first* snapshot deliberately defers the collision-handling shape.
  - **`exact_duplicate`** — including `بِ` if it appears twice. The first snapshot does not adjudicate whether duplication is intentional multi-group classification or a source-side merge candidate.
  - **`source_data_discrepancy`** (any sub-class) — including any row whose `Operator` cell contradicts its own `Example_Vocalized` at the consonant skeleton level (e.g., the prose-label `لام الأمر` row, or the `عشرة` vs `عشر` row found by the prototype).
- Any row with `partial_vocalization` — Operator cell is under-specified relative to the example.
- Any row with `linkage_vowel_difference` — even though `info`-severity, the first snapshot stays at "zero warnings of any kind".
- Any row with `title_used_as_surface_candidate` — N/A for operators but documented for completeness.
- Any row with `no_surface_candidate` — N/A for operators.
- Any row with `descriptive_not_surface` — including any row whose Operator cell contains descriptive prose rather than the operator's actual surface form.

Exclusion is not rejection. Excluded classes are reserved for *later* snapshots under explicitly-named handling policies (see § 14).

## 7. Identity Discipline

The following identity disciplines are inherited verbatim and bind every row in every snapshot under this policy:

1. **`surface_form_vocalized` is identity.** It is the only identity carrier. Two rows have the same identity if and only if their NFC `surface_form_vocalized` strings are codepoint-equal. (PR #86 §12.1, PR #98 §12.4.)
2. **`surface_form_unvocalized_key` is diagnostic only.** It MAY appear in snapshot tables for human readability but MUST NEVER be used as an identity key, lookup key, or comparison basis. (PR #86 §12.1.)
3. **NFC normalization is mandatory.** Every surface form in a snapshot is NFC-normalized at snapshot time. (PR #97.)
4. **Harakat are identity-relevant.** `مِنْ` (with KASRA) is NOT the same identity as `مَنْ` (with FATHA). `إِنَّ` ≠ `إِنْ`. `أَنَّ` ≠ `أَنْ`. Snapshots NEVER strip harakat to compress identity.
5. **The source CSV's taxonomy is the source's own classification, not Saleh's.** The `Group Number` and `Arabic Group Name` columns are recorded as the source's classification, preserved verbatim, and explicitly tagged as *source-side* in the snapshot. They do NOT become Saleh-canonical grammatical labels; they are not consumed by any Saleh runtime layer.
6. **`Example_Vocalized` is descriptive only.** It MAY appear in a snapshot as an illustrative example of how the source represents the operator in context. It MUST NEVER be used as a runtime fixture, i'rāb proof, operator-role proof, runtime input, or evidence claim. (PR #98 §12.4.) Snapshot tables may print it; runtime code may not consume it.
7. **`length_bucket` is diagnostic only**, not identity (PR #86 §12.1). This snapshot policy uses no length-based selection criterion; § 5 selects by group and identity status, not by length.

## 8. Warning Discipline

This policy adopts verbatim the 11 warning codes the read-only prototype produced and the severity assignments under which they were emitted. Snapshot-PR descriptions must use this exact vocabulary:

| warning_code | severity | meaning |
|---|---|---|
| `linkage_vowel_difference` | `info` | Operator's harakat differ from the Example_Vocalized harakat on the matched span; likely benign Arabic wasla/connected-speech vocalization shift. |
| `length_6_plus` | `info` | Surface has 6+ Arabic letters — multi-letter compound or extended form. Acceptable; not blocking. |
| `partial_vocalization` | `warning` | Operator cell is under-specified relative to Example_Vocalized; source-side completion advisable. |
| `collision_same_unvocalized_key` | `warning` | Unvocalized key maps to multiple distinct vocalized identities; preserved as distinct, never collapsed. |
| `exact_duplicate_surface` | `warning` | Same vocalized identity appears on multiple rows; manual review for intentional multi-group classification vs source-side merge candidate. |
| `title_used_as_surface_candidate` | `warning` | No priority surface field found; `title` used as a stand-in. (N/A to operators; reserved for mabniyat snapshots.) |
| `weak_provenance` | `warning` | Source file contains rule/case descriptions rather than concrete operator surfaces. |
| `unknown_length` | `warning` | Could not compute Arabic-letter count. |
| `no_surface_candidate` | `block` | Entry has no usable surface field across the configured priority list. |
| `descriptive_not_surface` | `block` | Candidate surface looks like descriptive prose, not an Arabic surface form. |
| `true_source_discrepancy` | `block` | Operator's unvocalized form not found in Example_Vocalized's unvocalized form — true consonant-skeleton mismatch; source-side correction required. |

The first pilot snapshot admits **only `unique_identity` rows with zero warnings**, so none of these codes apply to its 13 admitted rows. Their codification here is for future snapshots and for the snapshot-PR review checklist.

## 9. `Example_Vocalized` Discipline

`Example_Vocalized` cells in any snapshot are governed by these rules:

1. **Descriptive only.** They illustrate how the source represents the operator in a fully voweled example sentence.
2. **Not identity.** The snapshot's identity is its `surface_form_vocalized` column, never the `Example_Vocalized` column.
3. **Not a runtime fixture.** No test, evidence builder, adapter, or runtime layer may consume the `Example_Vocalized` column of any snapshot row. (PR #98 §12.4.)
4. **Not an i'rāb proof.** The grammatical analyses some source rows print in their `Note` column (e.g., `إلى: حرف جر، البيت: اسم مجرور`) are recorded verbatim as the source's own analysis and are NOT consumed as i'rāb evidence by any Saleh layer.
5. **Not a role proof.** Whether the source's `Example_Vocalized` shows an operator in subject, object, or oblique position has zero load-bearing effect on Saleh's morphological-role classification.
6. **Not a hukm / dalalah / meaning derivation.** None of the above.
7. **Wasla mention.** Where `Example_Vocalized` and `Operator` differ in the haraka on the operator's final consonant (e.g., `مِنْ` → `مِنَ` before `الـ`), the snapshot records the difference as a `linkage_vowel_difference` fact about the source's own examples, NEVER as a claim about Saleh's grammar.

## 10. Pilot Subset Risks

The 13-row pilot subset carries the following risks. Each must be explicitly acknowledged in the future snapshot-PR description:

1. **Single-letter operators (`تَ`, `لِ`, `كَ`) overlap downstream.** Their consonant skeletons coincide with verb prefixes / noun suffixes in connected speech. *Identity is safe* (the snapshot's vocalized identity is unique); *downstream context-ambiguity exists* (a higher layer must disambiguate by context — that disambiguation is out of scope of any snapshot). **`كَ` in particular is identity-safe but downstream context-ambiguous**: its identity `U+0643 U+064E` is unique, but its grammatical role in context can be comparison (كاف التشبيه), possessive pronoun, vocative, or address — disambiguation belongs to higher layers, NOT to this snapshot.
2. **`مِنْ` is excluded.** This well-known preposition does not appear in the first pilot snapshot because its skeleton `من` collides with the conditional `مَنْ`. **`مِنْ` / `مَنْ` collision rows are deliberately excluded from the first pilot snapshot**; they are reserved for a *later* collision-class snapshot under explicit collision-handling rules. Snapshot-PR reviewers MUST be alerted to this exclusion.
3. **Exception-prepositions `حَاشَا` / `عَدَا` / `خَلَا` are grammatically nuanced.** Classical Arabic grammar admits multiple classifications: some grammarians treat them as exception-prepositions of meaning; others classify them as exception-verbs taking accusative objects; some contexts vocalize the following noun in `جر` and others in `نصب`. The source CSV groups them under group 1 (preposition-of-meaning) per its own taxonomy; the snapshot records that classification verbatim. **These rows require manual review before any future data snapshot** to confirm that the source's group-1 placement is the policy-reviewer's preferred classification, and to record the classification disagreement in the snapshot's `note` column if so.
4. **The source's group-1 label is the maintainer's taxonomy, not Saleh's.** The snapshot binds the source's label as *source-side*, traceable but not authoritative.
5. **Source-CSV drift.** The maintainer may revise the upstream CSV. The snapshot fixates the source file's path, byte size, and SHA-256 at snapshot time (see § 12).
6. **`Example_Vocalized` wasla shifts.** Even though the snapshot admits only rows with zero warnings (no `linkage_vowel_difference`), the wasla phenomenon is a feature of Arabic, not a defect; future snapshots that include `info`-warning rows must explain the wasla mechanism to non-Arabic-speaking reviewers.

## 11. Manual Review Requirements

Before any future snapshot PR is opened, a maintainer-led manual review pass must:

1. **Read every row of the candidate subset by eye.** For the 13-row pilot, this is feasible in one sitting. Larger snapshots must be tabled into manageable batches before review.
2. **Confirm the source-CSV provenance.** Cite the absolute path, byte size, mtime, and SHA-256 of the source file at review time.
3. **Confirm each row's identity codepoints.** No row whose codepoints differ from this policy's documented values is admitted.
4. **Re-run the read-only normalization prototype.** If the run no longer produces the documented inclusion result, the policy must be re-evaluated, not silently bypassed.
5. **Confirm the warnings ledger.** Every excluded class (per § 6) must be present in the run's warnings CSV with the documented codes and severities.
6. **Confirm no source data has changed under the snapshot's feet.** If the source CSV has been edited since the previous prototype run, the snapshot PR must explicitly call out the changed rows.
7. **Confirm the exception-prepositions classification.** For `حَاشَا` / `عَدَا` / `خَلَا`, the reviewer must explicitly approve the source's group-1 placement.
8. **Confirm the `مِنْ` / `مَنْ` exclusion.** The reviewer must explicitly acknowledge the deliberate exclusion of the collision-class rows.

The review may be performed by the maintainer alone; this policy does NOT require multi-reviewer sign-off. But a single reviewer's sign-off must be recorded in the future snapshot PR's description, by name and date.

## 12. Provenance Requirements

Every snapshot under this policy must record, in the snapshot file's frontmatter or top section:

| field | example value |
|---|---|
| `source_path` | `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv` |
| `source_size_bytes` | `26799` |
| `source_mtime_utc` | `2026-06-06T07:20:00Z` (`source mtime at snapshot time`) |
| `source_sha256` | `<computed at snapshot time>` |
| `snapshot_form` | `normalized-table` (one of the five PR #97 §15-reserved forms) |
| `snapshot_id` | `SNAP-001` |
| `snapshot_taken_at_utc` | `<UTC ISO-8601 timestamp at snapshot time>` |
| `prototype_run` | `/tmp/source_preview_runner.py` |
| `prototype_outputs_referenced` | `/tmp/source_preview_*` and `/tmp/first_snapshot_subset_*` |
| `policy_authority` | `docs/qiyas_core/EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` |
| `reviewer` | (name) |
| `review_date_utc` | (date) |

The snapshot is *frozen*. If the source CSV later changes, the next snapshot is a *new* snapshot ID (`SNAP-002`, `SNAP-003`, …), never an update-in-place.

## 13. What This Does Not Authorize

This policy does NOT authorize any of the following actions. Each is **forbidden** until a separate, explicitly-named future PR opens it:

- **Copying the 13 rows into `src/` / `tests/` / `data/` / any registry.** No row of any source CSV is licensed by this policy to appear under those directories.
- **Building a runtime adapter, producer, carrier, rule, evidence type, or candidate type** for operators, prepositions, or any other surface category derived from a snapshot.
- **Creating an `ArabicOperatorRegistry`, `ArabicPrepositionRegistry`, `ArabicAmilRegistry`, `ArabicMabniRegistry`, or any other operator/role registry** under `src/qiyas_core/registries/` or anywhere else.
- **Producing runtime tests** that consume snapshot row data.
- **Producing fixtures** that derive from the `Example_Vocalized` cells of any snapshot row.
- **Inferring i'rāb / dalalah / meaning / hukm / reality / Word / Lafz / SentenceGeometry / DiscourseGeometry / TextGeometry / OperatorGeometry / AmilEffectEvidence / I'rāb runtime** from any snapshot row.
- **Promoting source-side taxonomy labels to Saleh-canonical labels.**
- **Treating any snapshot as a license to refactor the variant resolver, the MIU adapter, the GlyphClassificationGate, the SifatVector contract, the slot geometry, the LCNV, or any other Saleh runtime component.**
- **Modifying `new_arabic_analyzer`** to bring it into agreement with a snapshot, or vice versa.
- **Bundling a snapshot PR with any other PR.**

If any of the above seems desirable in a downstream conversation, the answer is the same: open a separate PR for it, name it explicitly, and gate it on its own constitutional review.

## 14. Future Snapshot PR Shape

A *future* PR opened under this policy would have the following shape:

- **Title**: `docs(qiyas_core): take first external operator snapshot (SNAP-001)` (or similar).
- **Type**: docs-only.
- **Files changed**: exactly one new file under `docs/qiyas_core/snapshots/`, e.g. `SNAP-001-operators-group1-prepositions.md` (or `.csv` if the snapshot is tabular and the docs-snapshot subdirectory accepts CSV).
- **Content**: provenance frontmatter per § 12; the 13 rows in a normalized table; explicit citation of this policy as the authority; explicit § 6 exclusions list; manual-review attestation per § 11; no other content.
- **Diff scope**: one new docs file. No `src/`, no `tests/`, no `data/`, no registry, no runtime change.
- **Test impact**: zero.
- **Authority**: this policy, plus the §11 manual review.

Subsequent snapshots (`SNAP-002`, `SNAP-003`, …) each get their own PR under the same template. Reserved subjects, in the order this policy expects them to be useful:

- **SNAP-002**: operators, group 1 collision-class rows (`مِنْ`, `بِ` if duplicated, etc.), under an explicit collision-handling rule appendix.
- **SNAP-003**: operators, group 2 (التوكيد — emphasis).
- **SNAP-004 +**: subsequent operator groups, one group per snapshot.
- **SNAP-0NN (later)**: mabniyat per-file, one or two files at a time, in the file priority order recorded by the read-only prototype's surface-field priority list.
- (No reservation is made for `Example_Vocalized` fixture snapshots; PR #98 §12.4 controls.)

Each future snapshot PR opens under this policy or under a successor policy. This policy is amendable by a docs PR that explicitly cites it as its predecessor.

## 15. Non-Goals

This policy explicitly does NOT:

- license `Example_Vocalized` as runtime fixture (PR #98 §12.4 controls);
- create or modify any runtime layer, carrier, producer, rule, or evidence type;
- create or modify any registry under `src/qiyas_core/registries/`;
- create or modify any test under `tests/`;
- create or modify any data file under `data/`;
- create or modify any other contract under `docs/qiyas_core/`;
- modify `new_arabic_analyzer/`;
- import any data from `new_arabic_analyzer/data/` into Saleh;
- copy the 13 illustrative rows of § 16 into Saleh as canonical data — they are illustrated for policy clarity only;
- adjudicate whether the source's group-1 classification matches Saleh's preferred classification;
- adjudicate the classical-grammar status of the exception-prepositions;
- adjudicate whether single-letter operators have a single grammatical function;
- adjudicate whether wasla-shifted vocalizations are bugs or features;
- adjudicate any morphological role, syntactic position, or semantic interpretation;
- start `Amil` runtime, `I'rāb` runtime, `Word`, `Lafz`, `Dalalah`, `Meaning`, `Hukm`, `Reality`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, or `OperatorGeometry`;
- engage with PR #99 or any other unrelated PR.

## 16. Summary Table

The 13-row pilot snapshot candidate, summarized below for policy illustration only. **This is not data import. This is not registry. This is not runtime authorisation. This is an illustrative table inside a docs-only policy file.**

| snapshot_candidate_id | surface_form_vocalized | unv_key (diagnostic) | codepoints | source-side classification |
|---|---|---|---|---|
| SNAP-001-001 | `إِلَى` | `إلى` | `U+0625 U+0650 U+0644 U+064E U+0649` | حرف جر دلالي — end-of-temporal-goal |
| SNAP-001-002 | `فِي` | `في` | `U+0641 U+0650 U+064A` | حرف جر دلالي — locative |
| SNAP-001-003 | `تَ` | `ت` | `U+062A U+064E` | تاء القسم — oath particle |
| SNAP-001-004 | `لِ` | `ل` | `U+0644 U+0650` | لام الجر — possession |
| SNAP-001-005 | `رُبَّ` | `رب` | `U+0631 U+064F U+0628 U+064E U+0651` | حرف جر للتقليل — rarity / frequency |
| SNAP-001-006 | `عَلَى` | `على` | `U+0639 U+064E U+0644 U+064E U+0649` | حرف جر دلالي — superposition |
| SNAP-001-007 | `كَ` | `ك` | `U+0643 U+064E` | كاف التشبيه — simile (identity-safe; downstream context-ambiguous) |
| SNAP-001-008 | `مُذْ` | `مذ` | `U+0645 U+064F U+0630 U+0652` | حرف جر زمني — temporal (short form) |
| SNAP-001-009 | `مُنْذُ` | `منذ` | `U+0645 U+064F U+0646 U+0652 U+0630 U+064F` | حرف جر زمني — temporal (full form) |
| SNAP-001-010 | `حَتَّى` | `حتى` | `U+062D U+064E U+062A U+064E U+0651 U+0649` | حرف جر وغاية — terminal limit |
| SNAP-001-011 | `حَاشَا` | `حاشا` | `U+062D U+064E U+0627 U+0634 U+064E U+0627` | حرف جر واستثناء — exception (manual review per § 10.3) |
| SNAP-001-012 | `عَدَا` | `عدا` | `U+0639 U+064E U+062F U+064E U+0627` | حرف جر واستثناء — exception (manual review per § 10.3) |
| SNAP-001-013 | `خَلَا` | `خلا` | `U+062E U+064E U+0644 U+064E U+0627` | حرف جر واستثناء — exception (manual review per § 10.3) |

Notes on the table:

- The `unv_key` column is **diagnostic only**, not identity. Including it in the table makes the collision-pattern visible to human reviewers; downstream consumers must NEVER read it as identity.
- The `source-side classification` column is the source CSV's own classification, recorded verbatim, **not** a Saleh-canonical taxonomy label.
- The `codepoints` column is the per-codepoint expansion of the NFC `surface_form_vocalized`. It exists to make the harakat visible to readers who cannot inspect the binary.
- The `Example_Vocalized` column from the source CSV is intentionally NOT reproduced in this policy's table. The full prototype output at `/tmp/first_snapshot_subset_preview.csv` does reproduce it for reference, but as a *prototype artefact*, not as canonical data.
- **No row of this table is copied into Saleh runtime, registries, or data files by this policy.** This is an illustrative summary inside a docs-only file.
- The classical *سألتمونيها* mnemonic and the group-1 *الجر فقط الدلالية* taxonomy are independent classification systems; this policy adjudicates neither.

End of policy.
