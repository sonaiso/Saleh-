# MAB-001 Mabniyat Adverbial Fixed-Forms Snapshot

> **Type**: documentation snapshot only.
> **Status**: first mabniyat pilot subset — adverbial / circumstantial fixed forms; 16 included rows + 2 deferred entries; explicit Hussein manual decisions.
> **Authority**: `docs/qiyas_core/MABNIYAT_PILOT_SNAPSHOT_POLICY.md` (PR #108) + maintainer decisions file at `/tmp/mab001_manual_decisions_hussein_reviewed.csv`.
> **Non-Authority**: this file is **NOT** runtime, **NOT** registry, **NOT** data, **NOT** fixture, **NOT** source correction, **NOT** a general mabniyat solution. It does **NOT** admit any row into Saleh runtime, registries, tests, fixtures, or data files. It does **NOT** copy source JSON into Saleh. It does **NOT** modify `new_arabic_analyzer/`. It does **NOT** introduce semantic, hukm, reality, dalalah, amil-effect, or i'rāb-effect claims of any kind.

---

## 1. Purpose

`MAB-001` records the **first docs-only mabniyat pilot snapshot** under the eligibility policy defined by PR #108 (`MABNIYAT_PILOT_SNAPSHOT_POLICY.md`). It admits a small, coherent pilot family from a single source file (`built_in_adverbs.json`) under a single source class label (`adverbial / circumstantial fixed forms`). The 16 admitted rows derive **verbatim** from the maintainer-authored manual review decisions filed at `/tmp/mab001_manual_decisions_hussein_reviewed.csv`.

This snapshot is **docs-only**. It is **not runtime**. It is **not registry**. It is **not source correction**. It is **not a general mabniyat solution** — only the explicitly attested 16 rows from one source class are admitted; every other mabniyat entry remains out of scope of this snapshot. A future MAB-NNN cycle would be needed to admit additional rows under their own per-row attestation; this snapshot does not open or imply that cycle.

It exists to make three things explicit:

1. The **16 rows** (a subset of the 18-row prototype-recommended candidate pool) that the maintainer manually attested for MAB-001 admission via `/tmp/mab001_manual_decisions_hussein_reviewed.csv` (Hussein Hiyassat, 2026-06-09).
2. The constitutional shape under which the rows are admitted as **distinct vocalized identities** with harakat preserved, source classification recorded verbatim, and zero runtime/registry consumption.
3. The boundary of what this snapshot does and does not authorise — strictly docs-only, strictly identity-preserving, strictly subordinate to PR #108 and the predecessor policies it binds.

## 2. Authority Chain

This snapshot is admitted under, and bound by, the following documents in their merged form on `main`. It does not amend any of them.

| document | role |
|---|---|
| `docs/qiyas_core/ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline — `surface_form_vocalized` is identity carrier; `surface_form_unvocalized_key` is diagnostic only; harakat are identity-relevant |
| `docs/qiyas_core/EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) | inventory of the two external corpora at `new_arabic_analyzer/data/`, including the mabniyat path that this snapshot points at by description (no JSON copied) |
| `docs/qiyas_core/EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) § 15 | five reserved snapshot forms; this snapshot uses the `normalized-table` form, mirroring SNAP-001 / SNAP-002 |
| `docs/qiyas_core/EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) | external-source snapshot policy (operators sibling); identity discipline + `Example_Vocalized` discipline + source-side classification non-promotion (§ 7(5)) re-bound here verbatim |
| `docs/qiyas_core/SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) § 9 | Saleh-side / upstream-side zero-write boundary — Saleh reports, upstream fixes; the 2 deferred entries (§ 8 below) route through this workflow |
| `docs/qiyas_core/ARABIC_MABNIYAT_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #107) | per-row schema for the mabniyat corpus — § 5 priority classes, § 6 provenance strength, § 8 weak-provenance handling; this snapshot admits only priority class 1 / `strong_explicit_surface` rows, no exceptions |
| `docs/qiyas_core/MABNIYAT_PILOT_SNAPSHOT_POLICY.md` (PR #108) | eligibility policy this snapshot instantiates — § 5 priority class 1 → `pilot_eligible` default; § 6 `strong_explicit_surface` → admissible without reviewer-note requirement; § 14 future-PR shape; this snapshot is the first instantiation under § 14 |
| `/tmp/mab001_manual_decisions_hussein_reviewed.csv` | **verbatim maintainer decisions file** by Hussein Hiyassat (2026-06-09); 18 candidate rows; 16 marked `include_in_mab001`, 2 marked `needs_more_review` (entries 12 / 17). Preserved at `/tmp` for audit; **not committed to the Saleh repo** (mirrors the SNAP-001 / SNAP-002 convention that maintainer review artefacts live in `/tmp`, never in the repo) |

This snapshot inherits all rules from the above verbatim. Where a sentence in this document could be read as conflicting with any authority, the authority document controls.

## 3. Why This Snapshot Exists

PR #108 (the eligibility policy) defined under what conditions a mabniyat entry **may be considered eligible for review** under a future pilot snapshot cycle. It explicitly did **not** instantiate any snapshot, admit any row, or open the next step on its own — the future instantiation PR was reserved by name in PR #108 § 14 for a separate explicit cycle.

This snapshot **is** that next step, opened on Hussein's explicit directive after he authored the per-row manual decisions in `/tmp/mab001_manual_decisions_hussein_reviewed.csv`.

The pilot family is small, coherent, and deliberately conservative:

- **Source file**: `built_in_adverbs.json` (a single JSON file in the mabniyat corpus).
- **Source class label**: `adverbial / circumstantial fixed forms` (one of PR #107 § 4's labels).
- **Priority class**: 1 (`explicit_vocalized_surface` per PR #107 § 5) for every admitted row — no priority-2/3/4/5 admissions, no `weak_provenance`, no `title_used_as_surface_candidate`, no `example_candidate_review_only`, no exceptions.
- **Provenance strength**: `strong_explicit_surface` for every admitted row — no admission requires a reviewer-rationale note per PR #108 § 6.
- **Pilot eligibility verdict (prototype-output)**: `pilot_eligible_candidate` for every row in the candidate pool.
- **Discrepancy status**: `none` for every candidate row — no entry triggered a PR #105 `R-NNN` finding.

The constitutional purpose is to **prove that the mabniyat pilot pipeline can move from policy (PR #108) to instantiation (this PR) without crossing any of the standing red lines**: no runtime, no registry, no JSON import, no source correction, no `Example_Vocalized` as proof, no grammar/i'rāb/meaning/hukm/reality claim, no over-broad family admission, no silent inclusion of a `needs_more_review` row.

## 4. Identity Discipline

This snapshot is bound verbatim by PR #86 § 12.1 + PR #97 + PR #98 § 12.4 + PR #103 § 7 + PR #107 § 11 + PR #108 § 4.

- **`surface_form_vocalized` is the identity carrier.** Every admitted row's identity is its NFC `surface_form_vocalized` string. Two rows have the same identity if and only if their NFC `surface_form_vocalized` strings are codepoint-equal.
- **`surface_form_unvocalized_key` is diagnostic only.** It appears in § 6's table for human readability + cross-corpus collision diagnostics. It MUST NOT be used as identity, lookup, or comparison basis by any downstream consumer.
- **Harakat are not collapsed.** Every admitted row preserves its source-side harakat verbatim. A snapshot NEVER strips harakat to compress identity.
- **NFC normalization is mandatory.** Every `surface_form_vocalized` value below is NFC-normalized at admission time.
- **This file records potential-only source snapshot rows, NOT semantic / hukm / reality / dalalah / amil-effect / i'rāb-effect claims.** No row admits any role, function, grammar judgment, or meaning. PR #108 § 4: *"A `pilot_eligible` entry is a candidate for the future pilot review pass, nothing more."* This snapshot is one rung up from `pilot_eligible_candidate` — it is `maintainer_attested_admission_into_docs_only_snapshot`. Nothing more.
- **Source-side classification labels are recorded verbatim, never promoted to Saleh-canonical** per PR #103 § 7(5) + PR #108 § 4.

## 5. Manual Reviewer Decisions

The 16 rows below are admitted **because Hussein Hiyassat explicitly marked them `include_in_mab001`** in `/tmp/mab001_manual_decisions_hussein_reviewed.csv` (2026-06-09). The decisions file satisfies PR #108 § 14 manual-review-gate preconditions:

1. **Per-row decisions recorded** by the maintainer — every candidate row (18 of them) has a non-blank `reviewer_decision` field filled by Hussein.
2. **No silent inclusion** — every admitted row carries the verbatim reviewer note (preserved in `/tmp` and quoted in § 7 below).
3. **No `awaiting_upstream` blocker** — every admitted row has `discrepancy_status = none` in the source decisions file.
4. **Allowed `reviewer_decision` values only** — `include_in_mab001`, `needs_more_review`, `exclude_from_mab001`. No `approved` / `accepted` language anywhere in the decisions file (audited: 0 hits).
5. **Maintainer authored the decisions himself** — the assistant did NOT fill in any decision on the maintainer's behalf. The decisions file is the constitutional contrast with the rolled-back MAB-001 attempt earlier in this project's history, codified in PR #112 § 13.

**Entries 12 (`ثََمََّةَ`) and 17 (`أَيَّْنَ`) are deferred** as `needs_more_review` per the maintainer's instruction (§ 8 below); they are NOT admitted into MAB-001. Their deferral is **a hold for source-side recheck, not an exclusion**.

**No assistant approval is claimed.** Every `reviewer_decision: include_in_mab001` in § 6 traces back to a row Hussein himself marked in `/tmp/mab001_manual_decisions_hussein_reviewed.csv`. The audit file's content satisfies PR #108 § 14 conditions 2, 3, and 6 (maintainer review + per-row decisions + manual attestation recorded). The 7-line MAB-001 attestation lesson from PR #112 § 13 is honored: the assistant did not author any portion of the per-row decisions.

## 6. Snapshot Rows

The 16 admitted rows below derive verbatim from `/tmp/mab001_manual_decisions_hussein_reviewed.csv` — every column value preserved without paraphrase. `mab_id` is assigned in source-entry-id ascending order across the file.

| mab_id | source_file | source_entry_id | source_class_label | surface_form_vocalized | surface_form_unvocalized_key | surface_priority_class | provenance_strength | inclusion_basis | reviewer_decision | runtime_status | identity_note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MAB-001-001 | `built_in_adverbs.json` | 1 | adverbial / circumstantial fixed forms | `حَيْثُ` | حيث | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved per PR #86 § 12.1; fatha-sukun-damma sequence; identity is the vocalized form, never the bare skeleton |
| MAB-001-002 | `built_in_adverbs.json` | 2 | adverbial / circumstantial fixed forms | `مُنْذُ` | منذ | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; damma-sukun-damma sequence; sibling of operator-side `مُنْذُ` admitted in SNAP-001 (PR #104) — same surface form, distinct corpus (mabniyat), distinct snapshot ID |
| MAB-001-003 | `built_in_adverbs.json` | 3 | adverbial / circumstantial fixed forms | `قَطُّ` | قط | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; fatha + shadda + damma cluster on ط; identity preserves the shadda |
| MAB-001-004 | `built_in_adverbs.json` | 4 | adverbial / circumstantial fixed forms | `اَلآنَ` | الآن | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; the source's surface includes the alif-with-fatha + lam + alif-madda sequence verbatim |
| MAB-001-005 | `built_in_adverbs.json` | 5 | adverbial / circumstantial fixed forms | `غَدًا` | غدا | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; fatha + tanwin-fath + alif sequence; the tanwin-fath is identity-relevant |
| MAB-001-006 | `built_in_adverbs.json` | 8 | adverbial / circumstantial fixed forms | `أَيَّانَ` | أيان | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; fatha + ي + fatha + shadda + alif + fatha; the shadda on ي is identity-relevant |
| MAB-001-007 | `built_in_adverbs.json` | 9 | adverbial / circumstantial fixed forms | `هُنَاكَ` | هناك | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; damma + sukunless ن + fatha + alif + fatha on ك |
| MAB-001-008 | `built_in_adverbs.json` | 10 | adverbial / circumstantial fixed forms | `هُنَالِكَ` | هنالك | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; distinct from MAB-001-007 only by the medial ل + kasra cluster — identity-distinguishing |
| MAB-001-009 | `built_in_adverbs.json` | 13 | adverbial / circumstantial fixed forms | `إِذْ` | إذ | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; kasra-sukun on the alif-with-kasra + ذ pair |
| MAB-001-010 | `built_in_adverbs.json` | 14 | adverbial / circumstantial fixed forms | `مُذْ` | مذ | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; damma-sukun; sibling of operator-side `مُذْ` admitted in SNAP-001 — same surface form, distinct corpus, distinct snapshot ID |
| MAB-001-011 | `built_in_adverbs.json` | 15 | adverbial / circumstantial fixed forms | `لَدَى` | لدى | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; fatha + fatha + alif-maqsurah |
| MAB-001-012 | `built_in_adverbs.json` | 16 | adverbial / circumstantial fixed forms | `عِوَضُ` | عوض | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; kasra + fatha + damma sequence |
| MAB-001-013 | `built_in_adverbs.json` | 18 | adverbial / circumstantial fixed forms | `مَتَى` | متى | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; fatha + fatha + alif-maqsurah |
| MAB-001-014 | `built_in_adverbs.json` | 19 | adverbial / circumstantial fixed forms | `هُنَا` | هنا | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; damma + fatha + alif; shortest of the هنا / هناك / هنالك triad |
| MAB-001-015 | `built_in_adverbs.json` | 20 | adverbial / circumstantial fixed forms | `أَنَّى` | أنى | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; fatha + fatha + shadda + alif-maqsurah; the shadda is identity-relevant |
| MAB-001-016 | `built_in_adverbs.json` | 21 | adverbial / circumstantial fixed forms | `إِذَا` | إذا | 1_explicit_vocalized_surface | strong_explicit_surface | hussein_manual_decision | include_in_mab001 | not_runtime | NFC; harakat preserved; sibling skeleton `إذا` is the unvocalized member of the operator-side `إذا` collision group deferred from SNAP-002 (PR #113) per PR #112 § 6.2 — different corpus + different vocalization (mabniyat `إِذَا` with full harakat vs operator collision group's partial vocalization). The two are distinct constitutional identities per PR #86 § 12.1. |

**Per-row inclusion summary**: every row above is class 1 / `strong_explicit_surface` / `discrepancy_status = none` / `Hussein-marked include_in_mab001`. No row required a reviewer-rationale note per PR #108 § 6 (because every row sits at the strongest priority/provenance combination). The maintainer's note attached to every included row in `/tmp/mab001_manual_decisions_hussein_reviewed.csv` is the standard sentence:

> *"Explicit Hussein manual review: include in docs-only MAB-001 candidate set; no runtime, registry, fixture, or source correction authorized."*

This sentence appears as the `reviewer_note` field of all 16 rows in the audit file and is preserved verbatim there.

## 7. Row Notes

Concise observational notes per included row. **No grammar invention. No i'rāb. No meaning, hukm, reality, dalalah, amil-effect, or i'rāb-effect claim.** The notes are bookkeeping observations only — what fact about the source the snapshot records, and what fact the snapshot is silent on.

- **MAB-001-001 / `حَيْثُ`** — recorded as `built_in_adverbs.json` entry 1; identity-relevant harakat: kasra-sukun on ي + damma on ث. The snapshot is silent on syntactic role; PR #108 § 4 forbids that claim here.
- **MAB-001-002 / `مُنْذُ`** — recorded as entry 2; same surface form also admitted in operators corpus as SNAP-001-009 (PR #104). The mabniyat-corpus record and the operators-corpus record are **separate snapshot identities** even when their `surface_form_vocalized` strings coincide; each corpus has its own admission decision and provenance. No cross-corpus collapse.
- **MAB-001-003 / `قَطُّ`** — recorded as entry 3; the shadda on ط is recorded verbatim from the source.
- **MAB-001-004 / `اَلآنَ`** — recorded as entry 4; the wasla-headed alif + lam + alif-madda is recorded verbatim from the source. Any phonological observation about isolated-vs-prefix vocalization is reserved as source-side commentary, not a constitutional claim of the row.
- **MAB-001-005 / `غَدًا`** — recorded as entry 5; the tanwin-fath + alif sequence is the source's chosen surface; recorded verbatim.
- **MAB-001-006 / `أَيَّانَ`** — recorded as entry 8; distinguished from the deferred entry 17 `أَيَّْنَ` by the alif before the ن (this row carries it, entry 17 does not). The harakat layout on this row is consistent with the standard form; the entry 17 layout is the one flagged by the maintainer for recheck.
- **MAB-001-007 / `هُنَاكَ`** — recorded as entry 9; identity-distinct from MAB-001-008 / `هُنَالِكَ` and MAB-001-014 / `هُنَا`.
- **MAB-001-008 / `هُنَالِكَ`** — recorded as entry 10; the medial ل + kasra cluster differentiates this row from MAB-001-007. The two are recorded as **separate rows** with **separate identities**.
- **MAB-001-009 / `إِذْ`** — recorded as entry 13; sibling-vocalization of MAB-001-016 / `إِذَا` (same skeleton-prefix إذ but with sukun + ذ + sukun here vs ذ + fatha + alif in MAB-001-016). The two are distinct identities; no merge.
- **MAB-001-010 / `مُذْ`** — recorded as entry 14; same surface form also admitted in operators corpus as SNAP-001-008 (PR #104); same separation principle as MAB-001-002.
- **MAB-001-011 / `لَدَى`** — recorded as entry 15.
- **MAB-001-012 / `عِوَضُ`** — recorded as entry 16.
- **MAB-001-013 / `مَتَى`** — recorded as entry 18.
- **MAB-001-014 / `هُنَا`** — recorded as entry 19; shortest of the هنا / هناك / هنالك triad. Each is its own distinct identity.
- **MAB-001-015 / `أَنَّى`** — recorded as entry 20; the shadda on ن is identity-relevant and preserved.
- **MAB-001-016 / `إِذَا`** — recorded as entry 21; **important note**: the operator-side `إذا` collision group (`إِذًا` / `إذا`) was deferred from SNAP-002 (PR #113) per PR #112 § 6.2 because one member of that operator pair carried `partial_vocalization`. This mabniyat row is a **fully-voweled adverbial entry** in a **different source corpus** (mabniyat, not operators), with its own source-side classification. The two are distinct identities per PR #86 § 12.1; nothing in this snapshot collapses them.

The notes above describe *what the source records and what this snapshot preserves verbatim*. They do not adjudicate grammar, do not invent role assignments, do not produce i'rāb judgments, and do not claim semantic content. Higher-layer artefacts (Word / Lafz / Dalalah / Meaning / Hukm / Reality / Amil / I'rāb) are explicitly out of scope per § 11.

## 8. Deferred Rows

Two entries from the prototype-recommended candidate pool are **NOT admitted** by MAB-001. The maintainer marked them `needs_more_review` in `/tmp/mab001_manual_decisions_hussein_reviewed.csv`. They are recorded here for traceability; their omission is a **hold for source-side recheck under PR #105's discrepancy/completion workflow**, not a constitutional exclusion.

| source_file | source_entry_id | surface_form_vocalized | reviewer_decision | runtime_status | reason (verbatim reviewer note from decisions file) |
|---|---|---|---|---|---|
| `built_in_adverbs.json` | 12 | `ثََمََّةَ` | needs_more_review | not_runtime | *"Needs more review: vocalization appears malformed / over-marked; do not include in MAB-001 until source-side surface is rechecked."* |
| `built_in_adverbs.json` | 17 | `أَيَّْنَ` | needs_more_review | not_runtime | *"Needs more review: vocalization appears suspicious; do not include in MAB-001 until source-side surface is rechecked."* |

**Saleh does NOT "fix" these entries.** Per PR #105 § 9 + PR #112 § 12 + § 9 below, Saleh has zero write access to `new_arabic_analyzer/`. The deferred entries route through PR #105's upstream completion / discrepancy workflow if and when the maintainer escalates them. If the upstream maintainer of `new_arabic_analyzer/` adjusts the source surfaces and a future read-only prototype run shows them clean, a **separate, later, explicitly-authorised** MAB-NNN PR could admit them under their own per-row attestation; **MAB-001 itself remains frozen** per PR #103 § 12 and is never amended retroactively.

The deferral does **not** indicate that the source data is necessarily wrong — only that the maintainer's eye-pass found the harakat layout sufficiently unusual to merit a second look before admitting these rows into a docs-only snapshot. The PR #105 workflow is the only authorised channel for any source-side adjustment.

## 9. Source Discrepancy / Completion Boundary

This snapshot binds `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) verbatim.

The two deferred entries (§ 8) are **not** automatically classified as `true_source_discrepancy` findings. They are **`needs_more_review` holds** by the maintainer — a lighter-weight signal than a formal discrepancy under PR #105 § 3.1. If subsequent source-side inspection confirms a true discrepancy, a `R-NNN` finding may be opened under PR #105's amendment workflow; that step is a separate explicit cycle and is not initiated by this snapshot.

**Saleh-side / upstream-side boundary** (PR #105 § 9 + PR #108 § 11 verbatim):

> Saleh has zero write access to `new_arabic_analyzer/`. A row that is wrong stays wrong until the upstream maintainer fixes it. Saleh never silently corrects a discrepancy. The boundary is not crossable.

Specifically for MAB-001:

1. Saleh does **not** "fix" the deferred entries. Their source-side surface remains as the source has it; Saleh records the deferral, not a correction.
2. Saleh does **not** adjudicate the harakat layout of either deferred entry. The "appears malformed / over-marked" and "appears suspicious" observations are the maintainer's **eye-pass observations recorded verbatim**, never promoted to a Saleh constitutional finding about the source.
3. **No source-side data is modified.** No JSON file is copied or edited.
4. **No JSON or CSV file is copied into Saleh** by this snapshot. The 16 admitted rows are a normalized-table view per PR #97 § 15, drawn verbatim from `/tmp/mab001_manual_decisions_hussein_reviewed.csv` (which itself derives from a prior read-only prototype run; that file too is not committed to the Saleh repo).
5. Malformed-looking or suspicious vocalization remains **deferred, not corrected**. The 2 deferred entries are reserved for source-side recheck under the upstream maintainer's authority. Saleh reports; upstream completes; Saleh re-inspects on the next prototype cycle.

## 10. Runtime Boundary

This snapshot is **docs-only**. Explicitly:

- **no runtime admission** — no row above is a runtime input to any Saleh layer. The `runtime_status` column reads `not_runtime` for every admitted row (16/16).
- **no registry** — no `ArabicMabniRegistry`, `ArabicMabniyatRegistry`, `ArabicAdverbRegistry`, `ArabicMabniyatPilotRegistry`, or any other registry is created or modified by this snapshot.
- **no fixture** — no test fixture under `tests/` consumes any row above.
- **no MIU change** — no change to `tests/qiyas_core/test_variant_resolver_miu_integration.py` or to any other MIU-related test, registry, or rule.
- **no resolver change** — no change to `ArabicVariantResolver`, `GlyphClassificationGate`, `SifatVector`, or any other existing Saleh runtime component.
- **no semantic / hukm / reality / dalalah / amil-effect / i'rāb-effect claim** — no row admits any of those higher-layer artefacts; § 11 enumerates the forbidden types explicitly.

A future runtime layer wishing to consume mabniyat adverbial-fixed-form data must be opened in a separate, explicitly-authorised PR cycle under its own constitutional review. It is **not** implied by, nor licensed by, this snapshot.

## 11. Non-Goals

This snapshot explicitly does **NOT**:

- create any **general mabniyat registry** — `ArabicMabniyatRegistry` / `ArabicMabniRegistry` / `ArabicAdverbRegistry` are out of scope;
- introduce any **runtime layer**, adapter, producer, carrier, rule, evidence type, or candidate type;
- perform any **source correction** — Saleh has zero write access to `new_arabic_analyzer/` per PR #105 § 9 + PR #108 § 11;
- copy any **JSON file** from `new_arabic_analyzer/02_mabniyat/` into Saleh;
- open **MAB-002** — additional mabniyat admissions (other source files, other source classes, the deferred entries 12/17 if upstream resolves them, the `ثُمَّ`/`ثَمَّ` collision pair deferred from this cycle) all require their own future explicit MAB-NNN cycles;
- open **SNAP-003** (exact-duplicate-surface collision class, reserved by PR #107 § 16.3);
- open **Track B** (Glyph / SifatVector runtime), **Track C** (`يَ` admission / madd / alif variants), or **Track D** (PR #99 follow-up);
- introduce **`WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `SentenceGeometry` / `DiscourseGeometry` / `TextGeometry` / `OperatorGeometry`**;
- introduce **`Amil` runtime, `I'rāb` runtime, `AmilEffectEvidence`, `I'rabEffectEvidence`, `Glyph` runtime, or `SifatVector` runtime**;
- **amend** PR #86 / PR #96 / PR #97 / PR #98 / PR #103 / PR #104 / PR #105 / PR #106 / PR #107 / PR #108 / PR #112 / PR #113;
- **edit** any existing snapshot under `docs/qiyas_core/snapshots/` — SNAP-001 (PR #104) and SNAP-002 (PR #113) are frozen per PR #103 § 12;
- **modify** `new_arabic_analyzer/`;
- **promote** the source's class label (`adverbial / circumstantial fixed forms`) to Saleh-canonical per PR #103 § 7(5) + PR #108 § 4;
- claim that mabniyat are "solved" by Saleh;
- claim that pilot admission is a final grammatical adjudication;
- **license** any runtime consumption of the admitted rows by any future cycle.

## 12. Validation Expectations

The following validation commands are the expected baseline. **None are run by this snapshot** (docs-only); they are listed here as the validation contract for any future merge cycle of this PR.

**Expected validation commands and outcomes:**

```bash
git diff --name-only main...HEAD
# → docs/qiyas_core/snapshots/MAB-001_MABNIYAT_ADVERBIAL_FIXED_FORMS_SNAPSHOT.md   (single file)

PYTHONPATH=src:. python3 /tmp/check_current_qiyas_state.py "بِ ضَ وَ يَ ضَرَبَ"
# → CURRENT QIYAS STATE CHECK: PASS

PYTHONPATH=src:. python3 -m pytest tests/qiyas_core/test_variant_resolver_miu_integration.py -q
# → 17 passed

PYTHONPATH=src:. python3 -m pytest tests/qiyas_core -q
# → 1329 passed, 2 skipped  (post-PR-#119 baseline; no regression — this PR adds zero test/runtime impact)
```

**Expected grep checks** (all PASS):

- `grep -n "MAB-001-001"` → present (Row 1 in § 6 table)
- `grep -n "MAB-001-016"` → present (Row 16 in § 6 table)
- `grep -n "include_in_mab001"` → present (one per admitted row in § 6 + § 5 attestation summary + § 12 validation contract — multiple hits)
- `grep -n "needs_more_review"` → present **only in deferred context** (§ 5 mention of deferred entries + § 8 deferred-rows table)
- `grep -n "ثََمََّةَ"` → present **only in § 8 deferred row** (entry 12 record)
- `grep -n "أَيَّْنَ"` → present **only in § 8 deferred row** (entry 17 record)
- `grep -n "not_runtime"` → present (one per admitted row + § 8 deferred rows + § 10 + § 13)
- `grep -n "hussein_manual_decision"` → present (one per admitted row)

**Test impact**: zero — docs-only PR.

## 13. Summary

| question | answer |
|---|---|
| Snapshot ID | **MAB-001** |
| Authority | PR #108 (eligibility policy) + maintainer decisions file `/tmp/mab001_manual_decisions_hussein_reviewed.csv` (Hussein Hiyassat, 2026-06-09) |
| Source file | **1** (`built_in_adverbs.json`) |
| Source class label | **1** (`adverbial / circumstantial fixed forms`) |
| Included rows | **16** (mab_id MAB-001-001 through MAB-001-016) |
| Deferred entries (held for source-side recheck) | **2** (entry 12 `ثََمََّةَ`, entry 17 `أَيَّْنَ`) — both `needs_more_review`, both `not_runtime` |
| Source kind | mabniyat JSON (read-only via prototype output; NOT copied into Saleh) |
| Identity key | `surface_form_vocalized` |
| `surface_form_unvocalized_key` | diagnostic only — visible for cross-corpus collision diagnostics; **never** identity |
| Priority class | 1 (`explicit_vocalized_surface`) for every admitted row |
| Provenance strength | `strong_explicit_surface` for every admitted row |
| Approval status | **Manually attested per-row by Hussein Hiyassat on 2026-06-09** via `/tmp/mab001_manual_decisions_hussein_reviewed.csv` |
| `runtime_status` | **`not_runtime`** for every admitted row |
| `inclusion_basis` | **`hussein_manual_decision`** for every admitted row |
| `reviewer_decision` | **`include_in_mab001`** for every admitted row |
| Source correction performed? | **No** — Saleh has zero write access per PR #105 § 9 + PR #108 § 11 |
| Does this create a registry? | **No** |
| Does this create a runtime layer? | **No** |
| Does this create a test or fixture? | **No** |
| Does this import source data? | **No** — no JSON file copied from `new_arabic_analyzer/` |
| Does this open MAB-002 / SNAP-003 / Track B/C/D? | **No** — each remains a separate explicit cycle |
| Does this amend any predecessor contract? | **No** |
| Frozen? | **Yes** — MAB-001 is frozen at merge per PR #103 § 12; any future change produces a new MAB-NNN, not an amendment |
| Is `Example_Vocalized` proof anywhere? | **No** — PR #98 § 12.4 + PR #108 § 9 verbatim |

End of snapshot.
