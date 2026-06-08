# Arabic Awamil Detailed Source Table Contract

> **Status**: docs-only constitutional contract.
> **Authority**: extends `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97), `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103), and `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105). Binds `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 (Vocalized Source Identity Discipline), `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) (source-path inventory), `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 (`Example_Vocalized` discipline), and `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) (the first instantiation under PR #103).
> **Scope**: defines the per-row *detailed source-table contract* for the awamil/operators corpus at `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`. Covers source-column inventory, normalized field-name mapping, per-row evidence requirements, identity discipline, `Example_Vocalized` discipline, discrepancy integration, the Saleh-side / upstream-side boundary, inclusion / exclusion rules for any future `SNAP-NNN` cycle citing this contract, reserved findings, and forward-reservation hooks.
> **Non-Authority**: this contract does **NOT** modify any external source file, does **NOT** admit any source row into Saleh runtime / registry / tests / fixtures / data, does **NOT** silently correct any discrepancy, does **NOT** create runtime / registry / test / fixture / data file, does **NOT** promote source-side taxonomy to Saleh-canonical, does **NOT** amend any predecessor contract, and does **NOT** open `SNAP-002` / `SNAP-003` / mabniyat pilot snapshot.

---

## 1. Purpose

This contract codifies the per-row detailed source-table shape for the awamil/operators corpus. It is the structural-contract counterpart to:

- `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) — the *policy* under which a future `SNAP-NNN` may admit a subset of source rows;
- `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) — the first 13-row *instantiation* under PR #103;
- `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) — the *discrepancy workflow* for rows where the `Operator` cell and the `Example_Vocalized` cell disagree.

A future `SNAP-002` (collision-class operators), `SNAP-003` (exact-duplicate / multi-role operators), or any subsequent group-N snapshot cycle will cite *this* contract by name for its per-row schema. Conversely, no `SNAP-NNN` instantiation is opened by this contract; § 14 reserves the forward hooks but does not exercise them.

This contract is **docs-only**. It does NOT create a runtime layer, an adapter, a producer, a carrier, a rule, a registry, an evidence type, a candidate type, a test fixture, or any data file. It does NOT change any existing contract. It does NOT amend `new_arabic_analyzer/`. It is a *schema contract*, not a *transformation contract*.

## 2. Relationship to Predecessor Contracts

| document | role | how this contract uses it |
|---|---|---|
| `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) | normalization rules + the five reserved snapshot forms in § 15 | this contract specialises PR #97's general normalization shape to the awamil/operators CSV specifically; it does not redefine any PR #97 rule |
| `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) | inventory of the two external corpora at `new_arabic_analyzer/data/` | this contract uses the inventory as the canonical *source-path pointer* — § 3 below cites the awamil CSV path verbatim from the inventory |
| `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) | snapshot policy: § 5 inclusion / § 6 exclusion / § 7 identity / § 8 warning / § 9 `Example_Vocalized` / § 10 risks / § 11 manual review / § 12 provenance / § 13 forbidden / § 14 future PR shape | this contract *inherits* every rule from PR #103 § 5–§ 13; § 11 and § 12 of this contract specialise PR #103's general inclusion / exclusion rules to the awamil schema |
| `snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) | first instantiation under PR #103: 13 manually-approved group-1 rows | this contract uses PR #104 as the *worked example*: § 5 below recovers the same normalized field schema PR #104's table reproduced; § 11 below names PR #104 as the proof-of-concept instantiation; this contract *does not edit* PR #104 |
| `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) | discrepancy workflow + recorded findings R-001 / R-002 | this contract's § 9 binds PR #105 verbatim; § 13 cites R-001 and R-002 by ID with their PR #105 status; this contract does NOT adjudicate the findings |
| `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline (`surface_form_vocalized` is identity; `surface_form_unvocalized_key` is diagnostic; `مِنْ ≠ مَنْ`) | this contract's § 7 binds PR #86 § 12.1 verbatim |
| `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 | `Example_Vocalized` is future fixture material; forbidden as runtime input / i'rāb proof / role proof / fixture today | this contract's § 8 binds PR #98 § 12.4 verbatim |

This contract does **not** amend any predecessor. Where a sentence in this contract could be read as conflicting with any predecessor, the predecessor controls.

## 3. Source Path and Provenance

The corpus this contract describes is the file:

```
/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv
```

This path is **outside** Saleh's git working tree. Saleh has *zero write access* to it (PR #105 § 9). This contract cites the path by string; it does not copy, mirror, or import any byte of the file into Saleh.

Provenance fields any future `SNAP-NNN` PR citing this contract must record at snapshot time (inherited from PR #103 § 12; reproduced here for self-containment):

| field | role |
|---|---|
| `source_path` | absolute path string (verbatim copy of the path above) |
| `source_size_bytes` | byte size at prototype-run time |
| `source_mtime_utc` | file modification time, ISO-8601 UTC |
| `source_sha256` | SHA-256 of the source file at prototype-run time |
| `prototype_run_id` | pointer to the read-only prototype script + invocation time (e.g. `/tmp/source_preview_runner.py`) |
| `snapshot_taken_at_utc` | UTC ISO-8601 timestamp at snapshot time |
| `snapshot_form` | one of the five PR #97 § 15-reserved forms (PR #103 § 4 chose `normalized-table` for `SNAP-001`) |

A snapshot is *frozen*; the source-CSV drift policy of PR #103 § 12 applies — if the upstream CSV later changes, the next snapshot bears a new ID; the previous snapshot remains frozen.

## 4. Source Column Inventory

The source CSV carries **8 columns** at the time of writing (verified at prototype-run time). For each column, this contract states its **role**, its **identity-relevance**, whether it is **diagnostic-only**, and whether it is **descriptive-only**.

| # | column name | role | identity-relevant? | diagnostic-only? | descriptive-only? |
|---|---|---|:---:|:---:|:---:|
| 1 | `Group Number` | source-side grouping integer (1..N) | no | yes — *source-side classification only* (PR #103 § 7(5)) | no |
| 2 | `Arabic Group Name` | Arabic name of the source-side group | no | yes — *source-side classification only* | no |
| 3 | `English Group Name` | English name of the source-side group | no | yes — *source-side classification only* | no |
| 4 | `Operator` | the operator's surface form (Arabic, NFC, harakat preserved when present) | **YES — identity** under PR #86 § 12.1 | no | no |
| 5 | `Purpose/Usage` | Arabic prose describing the operator's grammatical purpose | no | no | **YES** — descriptive |
| 6 | `Example` | Arabic example sentence, unvocalized | no | no | **YES** — descriptive (NOT proof) |
| 7 | `Note` | Arabic prose with the source's own i'rāb-style analysis of the example | no | no | **YES** — descriptive (NOT proof / NOT i'rāb evidence) |
| 8 | `Example_Vocalized` | Arabic example sentence, fully voweled | no | no | **YES — descriptive only**, per PR #98 § 12.4 |

The identity-relevant column is `Operator` only. All other columns are either diagnostic (source-side classification) or descriptive (source-side prose / example).

## 5. Normalized Field-Name Mapping

The read-only prototype at `/tmp/source_preview_runner.py` already produces a normalized representation of each source row. This contract **describes** the prototype's existing schema; it does NOT invent a new normative schema, and it does NOT replace the prototype's output.

| source column | → | normalized field | identity / diagnostic / descriptive |
|---|---|---|---|
| (n/a; constant) | → | `source_kind` (always `"operators_csv"`) | descriptive |
| (CSV row position) | → | `source_row_number` | diagnostic (provenance) |
| `Group Number` | → | `group_number` | diagnostic (source-side) |
| `Arabic Group Name` | → | `arabic_group_name` | diagnostic (source-side) |
| `English Group Name` | → | `english_group_name` | diagnostic (source-side) |
| `Operator` | → | `surface_form_vocalized` (NFC) | **IDENTITY** (PR #86 § 12.1) |
| (derived from `Operator`) | → | `surface_form_unvocalized_key` (NFC + harakat stripped) | **diagnostic only** (PR #86 § 12.1, PR #103 § 7) |
| (derived from `Operator`) | → | `surface_form_codepoints` (per-codepoint expansion) | descriptive (review aid) |
| `Purpose/Usage` | → | `purpose_usage` | descriptive |
| `Example` | → | `example_unvocalized` | descriptive |
| `Example_Vocalized` | → | `example_vocalized` | **descriptive only** (PR #98 § 12.4) |
| `Note` | → | `note` | descriptive |
| (computed by prototype) | → | `identity_status` (one of `unique_identity` / `exact_duplicate` / `collision_member` / `source_data_discrepancy`) | computed classification |
| (computed by prototype) | → | `warning_codes` (semicolon-separated subset of the 11 codes in PR #103 § 8) | computed classification |
| (computed by prototype) | → | `normalized_row_ready` (one of `yes` / `needs_review` / `no`) | computed classification |
| (computed at snapshot time) | → | `snapshot_id` (e.g. `SNAP-001`) — present only on rows actually admitted to a snapshot | provenance |

This table is **descriptive of the prototype's existing schema**, not a normative invention. The prototype already emits these fields; PR #104 § 10 already reproduces a subset of them. This contract does not change the schema; it merely names and binds it for future `SNAP-NNN` cycles.

## 6. Per-Row Evidence Requirements

For every row a future `SNAP-NNN` cycle admits under this contract, the following evidence must be recorded at snapshot time (in the snapshot's table or frontmatter):

1. `source_path` — absolute path to the source CSV (see § 3).
2. `source_size_bytes` — byte size at snapshot time.
3. `source_mtime_utc` — file modification time at snapshot time.
4. `source_sha256` — SHA-256 at snapshot time.
5. `source_row_number` — the row's position in the source CSV at snapshot time.
6. `surface_form_vocalized` — NFC, harakat preserved.
7. `surface_form_unvocalized_key` — NFC + harakat stripped (diagnostic display only).
8. `surface_form_codepoints` — per-codepoint expansion (e.g. `U+0625 U+0650 U+0644 U+064E U+0649`).
9. `identity_status` — one of the four computed classifications.
10. `warning_codes` — must be empty for any admitted row (per PR #103 § 5 / § 6).
11. `normalized_row_ready` — must be `"yes"` for any admitted row.
12. `prototype_run_id` — pointer to the prototype script + invocation.
13. `snapshot_id` — assigned at the cycle's frontmatter.

Rows that fail any of these evidence requirements (e.g. unknown `source_sha256`, computed `warning_codes` non-empty, computed `normalized_row_ready` not `"yes"`) are *not* admissible under this contract.

## 7. Identity Discipline

This contract binds PR #86 § 12.1 verbatim, plus the policy additions of PR #103 § 7. All bindings are *re-stated* here, not amended:

1. **`surface_form_vocalized` is identity.** Two rows are the same identity if and only if their NFC `surface_form_vocalized` strings are codepoint-equal.
2. **`surface_form_unvocalized_key` is diagnostic only.** It MAY appear in tables for human readability; it MUST NEVER be used as identity, lookup key, or comparison basis.
3. **NFC normalization is mandatory** at snapshot time.
4. **Harakat are identity-relevant.** A snapshot NEVER strips harakat to compress identity.
5. **`مِنْ ≠ مَنْ`.** The preposition `مِنْ` (U+0645 U+0650 U+0646 U+0652) is a *distinct* identity from the conditional `مَنْ` (U+0645 U+064E U+0646 U+0652); they collide on the unvocalized skeleton `من` but are preserved as separate identities. Snapshot tables NEVER merge them.
6. **`إِنَّ ≠ إِنْ`.** The emphasis particle `إِنَّ` is distinct from the conditional `إِنْ`.
7. **`أَنَّ ≠ أَنْ`.** The emphasis particle `أَنَّ` is distinct from the infinitival `أَنْ`.
8. **Source taxonomy is source-side, not Saleh-canonical** (PR #103 § 7(5)). The `Group Number` / `Arabic Group Name` / `English Group Name` columns are recorded verbatim as *the source's own classification*; they are NEVER promoted to Saleh-canonical grammatical labels.

## 8. `Example_Vocalized` Discipline

This contract binds PR #98 § 12.4 verbatim, reaffirmed by PR #103 § 9 and PR #104 § 9 and PR #105 § 9.

`Example_Vocalized` cells are **descriptive only**. They MAY appear in a snapshot's optional reference table for human review. They MUST NEVER be:

- proof of anything;
- a test fixture;
- runtime input to any Saleh layer;
- i'rāb evidence;
- `Amil`-effect evidence;
- role proof (e.g. morphological-role classification);
- hukm / dalalah / meaning derivation evidence.

Additionally, the `Note` column (PR #104 § 10 reproduces some `Note` values verbatim) contains *the source's own i'rāb-style analysis* of its example sentence. This contract reaffirms: such `Note` analysis is *the source's own classification*, recorded verbatim where included, and NEVER consumed as Saleh-canonical i'rāb evidence by any Saleh layer.

## 9. Discrepancy Integration

This contract binds `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) by name and citation. Detected discrepancies follow PR #105's reporting workflow (PR #105 § 5).

Saleh's role in any discrepancy is **report**, not **fix**. Specifically (re-binding from PR #105 § 9):

- This contract does NOT adjudicate which cell (`Operator` vs `Example_Vocalized`) is correct in any discrepancy.
- This contract does NOT silently correct any row.
- Rows flagged `true_source_discrepancy` (or its sub-pattern `prose_label_in_operator_cell`) by the read-only prototype are **excluded** from any `SNAP-NNN` admission under this contract until PR #105's upstream resolution (PR #105 § 10 / § 11) closes the finding.
- The reverse is also true: a finding closed `resolved_upstream_fixed` makes the (now-clean) row eligible for a *new* `SNAP-NNN` ID; it does NOT retroactively appear in any earlier snapshot (PR #103 § 12, PR #105 § 11).

## 10. Saleh-Side / Upstream-Side Boundary

This contract reaffirms PR #105 § 9 verbatim:

> Saleh has zero write access to `new_arabic_analyzer/`. A row that is wrong stays wrong until the upstream maintainer fixes it; only at the next prototype run does Saleh observe the change. The maintainer of `new_arabic_analyzer/` (the upstream) is the only authority that may *fix* source-side data. Saleh never silently corrects a discrepancy. The boundary is not crossable.

Specifically:

1. **Saleh records, reports, re-inspects.** Saleh never modifies upstream.
2. **No row is copied into Saleh** by this contract. Rows are *cited* (by row number, by codepoints, by surface form) in `SNAP-NNN` tables under PR #103; they are NEVER stored as Saleh-canonical data.
3. **No file under `data/`** is created by this contract. Saleh's `data/` directory remains outside the scope of this contract.
4. **The path `new_arabic_analyzer/...` appears only as a string** in any Saleh document under this contract; the bytes at that path are never copied into Saleh.

## 11. Inclusion Rules

A row is eligible for admission to a future `SNAP-NNN` under this contract if and only if **all** of the following hold (specialised from PR #103 § 5):

1. `source_kind == "operators_csv"`.
2. The row appears in the read-only normalization prototype's output for the current source-CSV snapshot.
3. `normalized_row_ready == "yes"`.
4. `identity_status == "unique_identity"`.
5. `warning_codes` is **empty** — zero warnings of any severity, including `info`-severity `linkage_vowel_difference`.
6. No dependency on `Example_Vocalized` for proof, fixture, runtime input, or evidence (per § 8).
7. Not referenced by any PR #105 finding currently in `awaiting_upstream` or `block`-severity state (currently `R-001`, `R-002` — see § 13).
8. The source-CSV provenance fields (§ 3) are recorded and verifiable.

`SNAP-001` (PR #104) demonstrated the inclusion rule on its 13 group-1 rows (`إِلَى`, `فِي`, `تَ`, `لِ`, `رُبَّ`, `عَلَى`, `كَ`, `مُذْ`, `مُنْذُ`, `حَتَّى`, `حَاشَا`, `عَدَا`, `خَلَا`); this contract reaffirms that those 13 rows were correctly admitted and remain admitted.

## 12. Exclusion Rules

Deliberately excluded from any `SNAP-NNN` cycle under this contract:

- **`collision_member` rows** — `مِنْ` / `مَنْ`, `إِنَّ` / `إِنْ`, `أَنَّ` / `أَنْ`, and any other row whose `surface_form_unvocalized_key` collides with another row's. **Reserved for `SNAP-002`** under explicit collision-handling rules (a future docs-only sub-contract; see § 14).
- **`exact_duplicate` rows** — same `surface_form_vocalized` on more than one source row. **Reserved for `SNAP-003`** under explicit duplicate-handling rules.
- **`partial_vocalization` rows** — `Operator` cell under-specified relative to `Example_Vocalized`. Defer until source-side completion (PR #105 § 5 workflow).
- **`linkage_vowel_difference` rows** — info-severity wasla-style vocalization shift. Excluded from any zero-warnings `SNAP-NNN` admission under this contract.
- **`source_data_discrepancy` / `true_source_discrepancy` rows** — covered by PR #105; rows are excluded until upstream resolution.
- **`prose_label_in_operator_cell` rows** — sub-pattern of `true_source_discrepancy` (PR #105 § 3.4). The R-001 finding (see § 13) is the canonical example.
- **All mabniyat rows** — out of scope of this contract; covered by a separate future `A3 Arabic mabniyat detailed source-table contract`.
- **Rows requiring runtime interpretation** — none of the operators corpus admits runtime interpretation under this contract.

Exclusion is *deferral*, not *rejection*. Each excluded class has its own forward path in § 14.

## 13. Reserved Findings

This contract cites the two `true_source_discrepancy` findings recorded in `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) by ID with their current status. **Neither finding is corrected by this contract.**

### R-001

- **Source row**: 42 (at prototype run time).
- **`Operator` cell (verbatim)**: `لام الأمر` (the Arabic *name* "the laam of command", multi-token prose).
- **`Example_Vocalized` cell (verbatim)**: `لِيَنْصُرْ` (operator's literal surface form: `لـ` + KASRA + jussive verb `يَنْصُرْ`).
- **Sub-class**: `true_source_discrepancy` (sub-pattern: `prose_label_in_operator_cell`).
- **Current status**: `awaiting_upstream` (per PR #105 § 4.1).
- **A2 treatment**: **excluded** from any `SNAP-NNN` admission under this contract per § 12. Not corrected. Not adjudicated. Reported under PR #105's workflow.

### R-002

- **Source row**: 56 (at prototype run time).
- **`Operator` cell (verbatim)**: `عشرة` (feminine "ten", 4 letters: `ع ش ر ة`).
- **`Example_Vocalized` cell (verbatim)**: `رَأَيْتُ أَحَدَ عَشَرَ كَوْكَبًا` (containing masculine `عَشَرَ`, 3 letters: `ع ش ر`).
- **Sub-class**: `true_source_discrepancy` (consonant-skeleton mismatch on final `ة`).
- **Current status**: `awaiting_upstream` (per PR #105 § 4.2).
- **A2 treatment**: **excluded** from any `SNAP-NNN` admission under this contract per § 12. Not corrected. Not adjudicated. Reported under PR #105's workflow.

Future findings (`R-003`, `R-004`, …) discovered by subsequent prototype runs will be cited under amendments to PR #105 first, then mirrored into this contract's § 13 by an A2-amendment PR. This contract is never silently rewritten.

## 14. Forward-Reservation Hooks

This contract reserves the following future docs-only sibling contracts by name. Each requires its own separately-authorised PR cycle. None is opened by this contract.

1. **SNAP-002 collision-handling rules sub-contract** — a docs-only sub-contract (or amendment to PR #103) that defines, in advance of SNAP-002 itself, the constitutional shape under which collision-class rows (`مِنْ` / `مَنْ`, `إِنَّ` / `إِنْ`, `أَنَّ` / `أَنْ`, etc.) may be admitted as **distinct** identities. The handling rules must specify how distinct vocalized forms sharing a single unvocalized skeleton get linked at the table level without collapsing to the skeleton.
2. **SNAP-002 instantiation** — a docs-only snapshot PR opened *after* the collision-handling sub-contract lands; cites both this contract and the collision-handling sub-contract; admits the collision-class rows under the new handling.
3. **SNAP-003 exact-duplicate / multi-role sub-contract + instantiation** — same two-step pattern: rules first, snapshot second.
4. **A3 Arabic mabniyat detailed source-table contract** — sibling to *this* contract for the mabniyat corpus (`new_arabic_analyzer/data/02_mabniyat/`). Will require its own surface-field priority review (the `title_used_as_surface_candidate` and `weak_provenance` classes are mabniyat-only concerns).
5. **Mabniyat pilot snapshot cycle** — follows A3, mirrors the PR #103 + PR #104 SNAP-001 cadence for the mabniyat corpus.

Each future cycle:
- is its own PR;
- is docs-only;
- does NOT modify any predecessor contract;
- does NOT import any source data into Saleh;
- requires the explicit-trigger discipline used throughout this corpus.

This contract is the **stable schema baseline** for the awamil corpus; subsequent cycles cite it, do not replace it.

## 15. Non-Goals

This contract explicitly does NOT:

- **modify the external source CSV** — Saleh has zero write access to `new_arabic_analyzer/`.
- **silently correct R-001 or R-002** — both remain `awaiting_upstream` per PR #105.
- **adjudicate which cell is correct** in any discrepancy.
- **create any runtime layer**, adapter, producer, carrier, rule, evidence type, or candidate type derived from any source row.
- **create any registry** under `src/qiyas_core/registries/` — no `ArabicOperatorRegistry`, `ArabicAmilRegistry`, `ArabicPrepositionRegistry`, `ArabicMabniRegistry`, etc.
- **create any test or fixture** under `tests/`.
- **import any data** — no CSV or JSON file is copied from `new_arabic_analyzer/` into Saleh.
- **use `Example_Vocalized` as proof or runtime input** — PR #98 § 12.4 controls; reaffirmed in § 8.
- **introduce `AmilEffectEvidence`, `I'rabEffectEvidence`, `WordCandidate`, `LafzCandidate`, `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`, `RealityClaim`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, or `OperatorGeometry`**.
- **start `Amil` runtime, `I'rāb` runtime, `ArabicAmilRegistry` runtime, or `ArabicMabniRegistry` runtime**.
- **start `GlyphClassificationEvidence` runtime, `GlyphClassificationGate` runtime, or `SifatVector` runtime** — those are Track B.
- **start Track C** (`يَ` admission, `madd`-variant admission, alif (`ا`) variant semantics) — those require constitutional amendment of standing § 9 non-goals.
- **start Track D** (maintainer-side runtime follow-up to PR #99's `PhoneticCandidate` / `OrthographicEvidence` / `EvidenceBridge` contract).
- **amend `letter_name_registry.py`** or `letter_role_registry.py`.
- **promote source-side taxonomy** (`Group Number` / `Arabic Group Name`) to Saleh-canonical (PR #103 § 7(5) controls).
- **open SNAP-002 / SNAP-003 / mabniyat pilot snapshot** — § 14 reserves the hooks but does not exercise them.
- **amend any predecessor contract** (PR #86 / PR #96 / PR #97 / PR #98 / PR #103 / PR #104 / PR #105).
- **edit `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md`** — PR #104's snapshot is frozen.
- **engage PR #99** or any other unrelated PR.

## 16. Summary Table

| Question | Answer |
|---|---|
| Does this contract create runtime? | **No** |
| Does it create a registry? | **No** |
| Does it modify the external source CSV? | **No** |
| Does it admit any source row into Saleh? | **No** (the contract is per-row schema; admission is a `SNAP-NNN` cycle's job) |
| What does it create? | A per-row schema contract for the awamil/operators source corpus + reserved exclusion / inclusion / discrepancy / boundary rules |
| What source columns does it inventory? | 8 (Group Number, Arabic Group Name, English Group Name, Operator, Purpose/Usage, Example, Note, Example_Vocalized) |
| What normalized fields does it bind? | 15 (`source_kind`, `source_row_number`, `group_number`, `arabic_group_name`, `english_group_name`, `surface_form_vocalized`, `surface_form_unvocalized_key`, `surface_form_codepoints`, `purpose_usage`, `example_unvocalized`, `example_vocalized`, `note`, `identity_status`, `warning_codes`, `normalized_row_ready`) |
| What is the identity key? | `surface_form_vocalized` (NFC, harakat preserved) |
| What is the stripped key? | `surface_form_unvocalized_key` (diagnostic only) |
| Are `مِنْ` / `مَنْ` distinct identities? | **Yes** — and excluded from any SNAP-NNN under this contract until collision-handling lands |
| Is `Example_Vocalized` proof? | **No** (PR #98 § 12.4 controls) |
| How many reserved findings? | 2 (R-001, R-002) — both `awaiting_upstream` |
| Does this contract correct R-001 or R-002? | **No** — both remain `awaiting_upstream` per PR #105 |
| What is the proof-of-concept instantiation? | SNAP-001 (PR #104) — 13 group-1 prepositions |
| What is forward-reserved? | SNAP-002 collision-handling sub-contract + SNAP-002 instantiation, SNAP-003 sub-contract + instantiation, A3 mabniyat source-table, mabniyat pilot snapshot |
| Approval status of this contract? | Docs-only constitutional contract; opened under Track A2 of the post-PR-#105 next-tracks schema |

End of contract.
