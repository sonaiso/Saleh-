# SNAP-001 Operators Group 1 Pilot Snapshot

> **Type**: documentation snapshot only.
> **Status**: manually approved pilot subset.
> **Authority**: `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103).
> **Non-Authority**: this file is NOT runtime, NOT registry, NOT data, NOT fixture. It does NOT admit any row into Saleh runtime, registries, tests, fixtures, or data files.

---

## 1. Purpose

`SNAP-001` records the first approved pilot snapshot candidate derived from the external operators source preview at `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`. It exists to make three things explicit:

1. The 13 rows that the read-only normalization prototype recommended and the maintainer manually approved as the first SNAP-001 pilot subset.
2. The constitutional shape under which these rows are admitted to the Saleh documentation corpus — strictly docs-only, strictly identity-preserving, strictly subordinate to the policies named in § 3.
3. The boundary of what this snapshot does and does not authorise — so future readers cannot mistake the snapshot for a runtime authorisation, a registry, or a data import.

This snapshot is **docs-only**. It is **not runtime**. It is **not registry**. It does **not** create or license any `Amil` / `I'rāb` / `Word` / `Lafz` / `Dalalah` / `Meaning` / `Hukm` / `Reality` / `SentenceGeometry` / `DiscourseGeometry` / `TextGeometry` / `OperatorGeometry` / `AmilEffectEvidence` / `I'rabEffectEvidence` artefact, runtime layer, evidence, candidate, registry, or test fixture. A future runtime layer that wishes to consume operator data would have to be opened in a separate, explicitly-authorised PR cycle under its own constitutional review; it would not be implied by, nor licensed by, this snapshot.

## 2. Snapshot Status

| field | value |
|---|---|
| `snapshot_id` | `SNAP-001` |
| `source_kind` | `operators_csv` |
| `scope` | group 1 operators pilot subset (`الجر فقط الدلالية` — Prepositions Only — Semantic) |
| `row_count` | **13** |
| `approval_status` | **manually approved by Hussein** |
| `data_status` | documentation snapshot only |
| `runtime_status` | **none** |

## 3. Policy Authority

This snapshot is admitted under, and bound by, the following documents in their merged form on `main`. It does not amend any of them.

| document | role |
|---|---|
| `docs/qiyas_core/EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) | snapshot policy — § 5 inclusion, § 6 exclusion, § 7 identity, § 8 warning, § 9 Example_Vocalized, § 10 risks, § 11 manual review, § 12 provenance, § 13 forbidden actions, § 14 future PR shape |
| `docs/qiyas_core/EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) | normalization rules, the five reserved snapshot forms, collision / exact-duplicate / source-data-discrepancy workflow |
| `docs/qiyas_core/EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) | inventory of the external corpora at `new_arabic_analyzer/data/`, including the operators CSV path cited as this snapshot's source |
| `docs/qiyas_core/ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline — `surface_form_vocalized` is identity, `surface_form_unvocalized_key` is diagnostic, `مِنْ ≠ مَنْ` |

This snapshot inherits all rules from the above verbatim. Where a sentence in this document could be read as conflicting with any of the above, the policy controls.

## 4. Source Prototype Inputs

The 13 rows below were derived from prototype outputs in `/tmp/`. **These `/tmp/` files are working aids only.** They are not committed to the Saleh repository. They are not runtime assets. They have no constitutional standing beyond being the source from which a maintainer-led manual-review pass derived this snapshot.

| `/tmp/` artefact | role |
|---|---|
| `/tmp/first_snapshot_subset_preview.csv` | normalized preview of the 13 candidate rows; the `surface_form_vocalized` and `surface_form_codepoints` values reproduced in this snapshot are taken verbatim from this file |
| `/tmp/snap001_terminal_review.md` | terminal review dashboard produced from the preview CSV; used during the manual-review pass |
| `/tmp/snap001_approval_checklist.md` | 11-confirmation + 13-row checklist that the maintainer read during the manual-review pass |

The source CSV itself (`/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`) was not copied into Saleh by this snapshot. The maintainer's `new_arabic_analyzer/` working tree was not modified by this snapshot.

## 5. Manual Approval

Hussein manually reviewed `/tmp/snap001_approval_checklist.md` and approved all 13 rows as the SNAP-001 pilot subset.

Nothing more is claimed. The manual-review pass was: read the checklist, read the terminal review pack, return the directive "APPROVED: all 13 rows are approved as the SNAP-001 pilot subset." No transitive approval of any other snapshot, any runtime work, any registry, any test, any fixture, any `Example_Vocalized` use, any source-table contract, or any future PR is implied by this approval.

## 6. Inclusion Rule

A row is included in SNAP-001 if and only if **all** of the following hold:

1. `source_kind == "operators_csv"`.
2. The row appears in the read-only normalization prototype's recommended SNAP-001 pilot subset (`/tmp/first_snapshot_subset_preview.csv`).
3. `normalized_row_ready == "yes"`.
4. `identity_status == "unique_identity"`.
5. `warning_codes` is empty (zero warnings of any severity, including `info`-severity `linkage_vowel_difference`).
6. No `source_data_discrepancy` (any sub-class).
7. No `collision_same_unvocalized_key`.
8. No `exact_duplicate_surface`.
9. No `partial_vocalization`.
10. No `linkage_vowel_difference`.
11. No dependency on `Example_Vocalized` as proof, fixture, or runtime input.

Rows that satisfy all of the above in the current source CSV: **13**.

## 7. Exclusion Rule

The following classes are explicitly excluded from SNAP-001 and are reserved for *later* snapshots under their own explicitly-named handling policies (§ 13):

- `مِنْ` (preposition, U+0645 U+0650 U+0646 U+0652) / `مَنْ` (conditional, U+0645 U+064E U+0646 U+0652) collision class — both are real, distinct, constitutional identities per PR #86 § 12.1; both are deferred to SNAP-002 (collision handling).
- Exact-duplicate operator rows (e.g., the `بِ` row if it appears on more than one row of group 1) — deferred until source-side review.
- Any `source_data_discrepancy` (any sub-class) — including any row whose `Operator` cell contradicts its own `Example_Vocalized` at the consonant skeleton level. Deferred until the source-side correction or, separately, the source discrepancy reporting workflow.
- `partial_vocalization` rows — Operator cell under-specified relative to the example.
- `linkage_vowel_difference` rows — info-severity vocalization shift, excluded from the *first* snapshot to keep it at "zero warnings of any kind".
- All `mabniyat_json` entries (all 29 files / ~545 entries) — mabniyat snapshots are a separate cycle.
- All rows requiring manual source-side correction.
- All rows with runtime interpretation needs.

Exclusion is deferral, not rejection. Excluded classes have their own forward path through the future snapshot reservation in § 13.

## 8. Identity Discipline

This snapshot is bound verbatim by the identity discipline of PR #86 § 12.1 / PR #97 / PR #98 § 12.4 / PR #103 § 7.

- **`surface_form_vocalized` is identity.** It is the only identity carrier. Two rows are the same identity if and only if their NFC `surface_form_vocalized` strings are codepoint-equal.
- **`surface_form_unvocalized_key` is diagnostic only.** It appears in the table of § 10 for human readability. It MUST NOT be used as an identity key, lookup key, or comparison basis. It MUST NOT be the basis for collapsing two rows.
- **Do not collapse by stripped form.** Two rows with the same `unvocalized_key` but different `surface_form_vocalized` are *distinct* identities, never merged. `مِنْ ≠ مَنْ`. `إِنَّ ≠ إِنْ`. `أَنَّ ≠ أَنْ`.
- **NFC normalization is mandatory.** The `surface_form_vocalized` values below are NFC-normalized.
- **Harakat are preserved.** Harakat are identity-relevant; this snapshot never strips them.

## 9. `Example_Vocalized` Discipline

This snapshot is bound verbatim by PR #98 § 12.4.

- `Example_Vocalized` from the source CSV is **descriptive only**.
- It is **not proof**.
- It is **not a test fixture**.
- It is **not runtime input**.
- It is **not i'rāb evidence**.
- It is **not Amil effect evidence**.
- It is **not role proof** (e.g., for morphological-role classification).
- It is **not hukm / dalalah / meaning derivation** evidence of any kind.

The `Example_Vocalized` column from the source CSV is intentionally NOT reproduced in this snapshot. Readers wishing to inspect the source's example sentences may consult the source CSV directly at its `new_arabic_analyzer/` path; doing so does not produce evidence consumable by any Saleh layer.

## 10. Approved Rows

The 13 approved rows of SNAP-001. All `surface_form_vocalized` and `surface_form_unvocalized_key` values are taken **verbatim** from `/tmp/first_snapshot_subset_preview.csv`. Source row numbers are the row positions in the source CSV at preview time (header is row 1; data rows start at row 2). Source-side category labels are recorded verbatim as the source's own classification, never promoted to Saleh-canonical.

| Snapshot ID | `surface_form_vocalized` | `surface_form_unvocalized_key` (diagnostic) | Source row / group | Source-side category | Note / caveat |
|---|---|---|---|---|---|
| SNAP-001-001 | `إِلَى` | `إلى` (diagnostic) | row 4, group 1 | حرف جر دلالي — preposition of end-of-temporal-goal | approved |
| SNAP-001-002 | `فِي` | `في` (diagnostic) | row 5, group 1 | حرف جر دلالي — locative preposition | approved |
| SNAP-001-003 | `تَ` | `ت` (diagnostic) | row 9, group 1 | تاء القسم — oath particle | single-letter caveat |
| SNAP-001-004 | `لِ` | `ل` (diagnostic) | row 10, group 1 | لام الجر — possession | single-letter caveat |
| SNAP-001-005 | `رُبَّ` | `رب` (diagnostic) | row 11, group 1 | حرف جر للتقليل — preposition of rarity / frequency | approved |
| SNAP-001-006 | `عَلَى` | `على` (diagnostic) | row 13, group 1 | حرف جر دلالي — superposition preposition | approved |
| SNAP-001-007 | `كَ` | `ك` (diagnostic) | row 14, group 1 | كاف التشبيه — simile | single-letter caveat |
| SNAP-001-008 | `مُذْ` | `مذ` (diagnostic) | row 15, group 1 | حرف جر زمني — temporal (short form) | approved |
| SNAP-001-009 | `مُنْذُ` | `منذ` (diagnostic) | row 16, group 1 | حرف جر زمني — temporal (full form) | approved |
| SNAP-001-010 | `حَتَّى` | `حتى` (diagnostic) | row 17, group 1 | حرف جر وغاية — terminal limit preposition | approved |
| SNAP-001-011 | `حَاشَا` | `حاشا` (diagnostic) | row 18, group 1 | حرف جر واستثناء — exception preposition | manual-review caveat (see § 11) |
| SNAP-001-012 | `عَدَا` | `عدا` (diagnostic) | row 19, group 1 | حرف جر واستثناء — exception preposition | manual-review caveat (see § 11) |
| SNAP-001-013 | `خَلَا` | `خلا` (diagnostic) | row 20, group 1 | حرف جر واستثناء — exception preposition | manual-review caveat (see § 11) |

The Unicode codepoint sequences for each `surface_form_vocalized` are recorded in `/tmp/first_snapshot_subset_preview.csv` (column `surface_form_codepoints`). They are not reproduced in this table to keep it readable; the CSV is the binary-precise reference.

A note on the source row numbers for SNAP-001-003 and SNAP-001-004: the approval brief's draft table showed rows 8 and 9 for `تَ` and `لِ` respectively. The actual source CSV (and the `/tmp/first_snapshot_subset_preview.csv` derived from it) places them at rows **9 and 10**. The values in this snapshot's table are taken verbatim from the CSV per the brief's explicit instruction "Do not invent or correct forms from memory."

## 11. Risk Notes

- **Single-letter operators `تَ` / `لِ` / `كَ` are identity-safe but downstream context-ambiguous.** Their vocalized identity is unique by codepoints. Their consonant skeletons coincide with verb prefixes / noun suffixes in connected speech. Disambiguation belongs to higher layers; it is out of scope of any snapshot. PR #103 § 10.1.
- **`حَاشَا` / `عَدَا` / `خَلَا` have an exception-preposition classification caveat.** Classical Arabic grammar admits multiple classifications (preposition vs verb taking accusative object); some contexts vocalize the following noun in `جر`, others in `نصب`. The source CSV places them under group 1 (preposition of meaning) per its own taxonomy; this snapshot records that classification verbatim. **Any future runtime work or structured source-table that wishes to use these rows must perform an explicit additional manual review before doing so.** PR #103 § 10.3.
- **Source taxonomy is not Saleh canonical taxonomy.** The source's `Group Number = 1` and `Arabic Group Name = الجر فقط الدلالية` are recorded *as the source's classification*, not as Saleh-canonical grammatical labels. PR #103 § 7(5).
- **`مِنْ` / `مَنْ` are deliberately excluded** from SNAP-001 until collision-class handling is separately approved. Both rows exist in the source CSV at distinct vocalized identities; both will appear in SNAP-002 under explicit collision-handling rules (see § 13). PR #103 § 6, § 10.2.

## 12. What This Snapshot Does Not Authorize

This snapshot explicitly does **not** authorise any of the following. Each remains forbidden until a separate, explicitly-named future PR opens it.

- **no runtime** — no runtime layer, adapter, producer, carrier, rule, or evidence type derived from any row in this snapshot.
- **no registry** — no `ArabicOperatorRegistry`, `ArabicPrepositionRegistry`, `ArabicAmilRegistry`, `ArabicMabniRegistry`, or any other registry derived from any row in this snapshot.
- **no tests** — no test under `tests/` consumes a snapshot row.
- **no CSV import** — no CSV file is copied from `new_arabic_analyzer/` into Saleh.
- **no JSON import** — no JSON file is copied from `new_arabic_analyzer/02_mabniyat/` into Saleh.
- **no source-table runtime** — no runtime adapter consumes a normalized source table that this or any future snapshot might produce.
- **no `AmilEffectEvidence`** runtime carrier.
- **no `I'rabEffectEvidence`** runtime carrier.
- **no `WordCandidate`** or any other word-level candidate type.
- **no `DalalahCandidate`** or any other dalalah-level candidate type.
- **no `Meaning`** layer.
- **no `Hukm`** layer.
- **no `RealityClaim`** layer.
- **no sentence / discourse / text layer.**
- **no use of `Example_Vocalized` as proof** — neither as fixture, nor as i'rāb evidence, nor as role proof, nor as runtime input.
- **no automatic consumption** of snapshot rows by `MIU`, `ArabicVariantResolver`, `GlyphClassificationGate`, `SifatVector`, or any other existing Saleh runtime component.
- **no promotion** of the source's taxonomy labels to Saleh-canonical labels.
- **no amendment** of any policy document (PR #86 / PR #97 / PR #98 / PR #103) under which this snapshot is admitted.
- **no modification** of `new_arabic_analyzer/`.

If any of the above seems desirable in a downstream conversation, the answer is the same: open a separate PR for it, name it explicitly, and gate it on its own constitutional review. This snapshot is not a transitive license.

## 13. Future Work

Safe future steps only. Each requires its own separately-authorised PR cycle.

1. **SNAP-002** — collision-class operators, especially the `مِنْ` / `مَنْ` pair (`من`-skeleton), under explicit collision-handling rules. The handling rules themselves would be defined either as an amendment to PR #103 or as a sibling policy document; SNAP-002 would not invent them inline.
2. **SNAP-003** — exact-duplicate / multi-role operator rows. Includes any row where the same `surface_form_vocalized` appears in more than one source group (e.g., `بِ` if duplicated), and any row classifiable in more than one source-side category.
3. **Mabniyat pilot snapshot** — a separate cycle. Only after explicit review of (a) the mabniyat surface-field priority order (already documented by the read-only prototype's `SURFACE_PRIORITY`), (b) the `title_used_as_surface_candidate` and `weak_provenance` warning classes, and (c) the per-file selection order.
4. **Source discrepancy reporting workflow** — formalizes how the `source_data_discrepancy` and `true_source_discrepancy` cases (e.g., the prose-label `لام الأمر` row and the `عشرة` vs `عشر` row found by the prototype) are reported back to the upstream maintainer of `new_arabic_analyzer/`.

This snapshot does **not** recommend opening any runtime, registry, fixture, or test work. The four items above are docs / data-snapshot work only.

## 14. Summary Table

| Question | Answer |
|---|---|
| Is this runtime? | **No** |
| Does it create registry data? | **No** |
| Does it copy CSV into Saleh? | **No** |
| How many rows? | **13** |
| Source kind? | `operators_csv` |
| Identity key? | `surface_form_vocalized` |
| Stripped key? | **diagnostic only** |
| Are `مِنْ` / `مَنْ` included? | **No** |
| Is `Example_Vocalized` proof? | **No** |
| Approval status? | **Manually approved pilot subset** |

End of snapshot.
