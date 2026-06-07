# Source Discrepancy Reporting Contract

> **Status**: docs-only constitutional contract.
> **Authority**: extends `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) and binds `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96), `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103), `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4, and `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12.1.
> **Scope**: defines how `source_data_discrepancy` and `true_source_discrepancy` cases discovered by any read-only external-source prototype are *reported, tracked, and escalated*, **without** correcting source data inside Saleh.
> **Non-Authority**: does NOT modify any external source file, does NOT admit any discrepant row into Saleh, does NOT silently correct discrepancies, does NOT create runtime, registry, or fixtures.

---

## 1. Purpose

This contract codifies the workflow Saleh follows when a read-only external-source prototype (e.g. `/tmp/source_preview_runner.py`) detects a *discrepancy* between (a) what an external source row claims at its `Operator` (or analogous surface) cell and (b) what the same source row demonstrates at its `Example_Vocalized` (or analogous example) cell.

The contract exists to make three things explicit:

1. **What counts as a discrepancy.** The taxonomy of warning sub-classes that the read-only prototype already emits (`linkage_vowel_difference`, `partial_vocalization`, `true_source_discrepancy`) is canonicalised here, with the conditions under which each is raised.
2. **What Saleh records about each discrepancy.** A discrepancy is a *fact about the external source*, not a fact about Saleh's runtime. Saleh records the discrepancy in its documentation corpus only, never in its registries, fixtures, or runtime data.
3. **The boundary between *report* and *fix*.** This contract is about *reporting*. The maintainer of `new_arabic_analyzer/` (the upstream) is the only authority that may *fix* source-side data. Saleh never silently corrects a discrepancy. The workflow has Saleh on the *report* side and the upstream on the *fix* side; the boundary is not crossable.

This contract is **docs-only**. It does **not** create a runtime layer, an adapter, a producer, a carrier, a rule, a registry, an evidence type, a candidate type, a test fixture, or any data file. It does not change any existing contract. It does not amend `new_arabic_analyzer/`. It is a *workflow contract*, not a *transformation contract*.

## 2. Relationship to Existing Source Contracts

This contract sits *on top of* the four predecessor contracts named below; it does not redefine, weaken, or override any of them. Where a sentence in this contract could be read as conflicting with any predecessor, the predecessor controls.

| document | role | how this contract uses it |
|---|---|---|
| `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) | normalization rules + `source_data_discrepancy` workflow stub (§ 12) + five reserved snapshot forms (§ 15) | this contract is the *workflow detail* PR #97 § 12 reserved by name |
| `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) | inventory of the two external corpora at `new_arabic_analyzer/data/` | this contract uses the inventory as the *upstream pointer* — the `source_path` field in every report points back at a row of the inventory |
| `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) | snapshot policy; § 13 forbids "silent source-side correction" | this contract is the *positive workflow* corresponding to PR #103 § 13's negation |
| `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 | `Example_Vocalized` is descriptive only; forbidden as runtime fixture / i'rāb proof / role proof | this contract reproduces the discipline verbatim in § 7 (Evidence Required) and § 9 (What Saleh Must Not Do) |
| `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline (`surface_form_vocalized` is identity; `مِنْ ≠ مَنْ`) | this contract preserves identity discipline in every discrepancy report — never collapses by stripped form |

## 3. Discrepancy Types

A *discrepancy* is a contradiction between the `Operator` cell of an external-source row and the same row's `Example_Vocalized` cell, on the shared consonant skeleton. This contract canonicalises three sub-classes already emitted by the read-only prototype, plus a fourth class for *prose-label* rows that the prototype's heuristics also catch.

### 3.1 `linkage_vowel_difference`

- **Severity**: `info`.
- **Definition**: The `Operator` and the matched span of `Example_Vocalized` share the same consonant skeleton and the same number of haraka slots, but the haraka *values* differ.
- **Cause (most often)**: Arabic *wasla* / connected-speech vocalization shift. The classical example is `مِنْ` (with sukun on the final noon, when in isolation) becoming `مِنَ` (with fatha) before a definite article `الـ`.
- **Workflow effect**: documented in the report, no upstream fix requested, no Saleh-side action.

### 3.2 `partial_vocalization`

- **Severity**: `warning`.
- **Definition**: The `Operator` and the matched span of `Example_Vocalized` share the same consonant skeleton, but `Operator` carries *fewer harakat* than the example. Operator is *under-specified* relative to the example.
- **Cause (most often)**: the source row's `Operator` cell was entered partially-vocalized or unvocalized while the `Example_Vocalized` cell carries full vocalization. The prototype found 25 such rows.
- **Workflow effect**: documented; upstream-side vocalization completion advisable; no Saleh-side correction.

### 3.3 `true_source_discrepancy`

- **Severity**: `block`.
- **Definition**: The `Operator` cell's unvocalized form is **not a substring** of `Example_Vocalized`'s unvocalized form. The consonant skeletons disagree.
- **Cause (most often)**: the `Operator` cell is *not the operator*, or is a *different morphological form* of the operator that does not literally appear in the example sentence.
- **Workflow effect**: blocks admission in any future snapshot or source-table contract until the upstream is asked to clarify. Saleh records the report but **does not** decide which of the two cells is correct.

### 3.4 `prose_label_in_operator_cell` (recognised by the prototype as a sub-pattern of `true_source_discrepancy`)

- **Severity**: `block`.
- **Definition**: The `Operator` cell contains *descriptive prose* (an Arabic *name* for the operator, often multi-token) rather than the operator's literal *surface form*. This is detected when (a) the `Operator` cell's NFC string is multi-token or contains a space, and (b) it does not appear as a substring of `Example_Vocalized`.
- **Cause (most often)**: a source-side editing convention that labels the operator by its grammatical name (e.g. `لام الأمر` — "the laam of command") rather than by its surface form (`لِـ`).
- **Workflow effect**: same as § 3.3 — blocking, reported, never auto-corrected.

A single row may carry **at most one** primary sub-class in any single report. A row that exhibits both `partial_vocalization` and `linkage_vowel_difference` is reported as `partial_vocalization` (the stronger signal). A row that exhibits `true_source_discrepancy` is reported as such and never as the weaker classes.

## 4. Known Prototype Findings

These are the *two* `true_source_discrepancy` rows the read-only prototype found in the current snapshot of `operators_catalog_split_vocalized.csv`. They are recorded here **as findings**, **not as corrections**. This contract does not fix either case.

### 4.1 Finding R-001

- **Source path**: `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`
- **Source row**: 42 (at prototype run time)
- **Operator cell (verbatim)**: `لام الأمر`
- **Example_Vocalized (verbatim)**: `لِيَنْصُرْ`
- **Sub-class**: `true_source_discrepancy` (sub-pattern: `prose_label_in_operator_cell`).
- **Diagnostic summary**: the `Operator` cell is the Arabic *name* of the operator ("the laam of command"), not its literal surface form. The operator's actual surface in the example is the single character `لـ` (U+0644) carrying KASRA, prefixed to a jussive verb.
- **Saleh-side action**: none beyond this report. The row is **excluded** from SNAP-001 (PR #104 § 7 verified that excluded class) and from any future snapshot until the upstream clarifies.
- **Upstream report recommendation**: ask the upstream whether the `Operator` cell should carry `لِـ` (surface form) and a separate `Name` column should carry `لام الأمر`. This contract does not adjudicate the answer.

### 4.2 Finding R-002

- **Source path**: `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`
- **Source row**: 56 (at prototype run time)
- **Operator cell (verbatim)**: `عشرة`
- **Example_Vocalized (verbatim)**: `رَأَيْتُ أَحَدَ عَشَرَ كَوْكَبًا`
- **Sub-class**: `true_source_discrepancy`.
- **Diagnostic summary**: `Operator` is the *feminine* form of "ten" (4 letters: `ع ش ر ة`). The `Example_Vocalized` demonstrates *eleven* (`أَحَدَ عَشَرَ`), which contains the *masculine* form `عَشَرَ` (3 letters: `ع ش ر`). The two consonant skeletons disagree by the final `ة`. The example does not contain the cell's stated form.
- **Saleh-side action**: none beyond this report. The row is **excluded** from SNAP-001 (PR #104 § 7 verified that excluded class) and from any future snapshot until the upstream clarifies.
- **Upstream report recommendation**: ask the upstream whether (a) the row was intended to be about the *masculine* `عَشَرَ` and the `Operator` cell mistakenly carries the *feminine* `عشرة`, or (b) the row was intended to be about *both* compound-number constituents and the `Example_Vocalized` should be reduced to a single-constituent example. This contract does not adjudicate the answer.

Each finding above must be re-verified before any snapshot or source-table PR cites it. § 11 codifies the re-inspection rules.

## 5. Reporting Workflow

Every detected discrepancy follows this workflow. The workflow is **single-direction**: a discrepancy moves from `detected` → `triaged` → `reported_upstream` → `awaiting_upstream` → `resolved_upstream_fixed` or `resolved_no_action_required`. There is no path that ends with Saleh modifying source data.

```
[detected]  ── read-only prototype emits warning_code in
              /tmp/source_preview_validation_warnings.csv
        │
        ▼
[triaged]   ── maintainer reads the warning, classifies the sub-class
              under § 3, and records the finding ID (e.g. R-001, R-002)
              in a new section of THIS contract (next amendment PR) or
              in a follow-up snapshot PR's exclusion list.
        │
        ▼
[reported_upstream]  ── maintainer sends a self-contained
                       report to the upstream (see § 7).
                       The report MUST include source_path, source row
                       number, Operator cell verbatim, Example_Vocalized
                       cell verbatim, sub-class, and diagnostic summary.
        │
        ▼
[awaiting_upstream]  ── no Saleh-side action. The finding remains in
                       any snapshot's exclusion list until upstream
                       responds.
        │
        ├──[resolved_upstream_fixed]  ── upstream amends the source
        │                                CSV / JSON; maintainer re-runs
        │                                the prototype (§ 11); the
        │                                finding's status is updated
        │                                in the next contract amendment
        │                                PR; if the row now passes
        │                                inclusion, it may be admitted
        │                                in a *new* snapshot ID.
        │                                NEVER retroactively included
        │                                in a previous snapshot.
        │
        └──[resolved_no_action_required] ── after upstream review, the
                                           finding is closed without
                                           source-side change (e.g.
                                           classification disagreement,
                                           or contract amendment to
                                           accept the form as-is). The
                                           finding's status is updated.
```

The workflow has **no automation in Saleh runtime**. Every transition is a *maintainer action*, recorded in a *docs-only* PR.

## 6. Severity Levels

Severity assignments follow the read-only prototype's emitted vocabulary verbatim:

| severity | meaning | example |
|---|---|---|
| `info` | linguistically expected; no upstream action required | `linkage_vowel_difference` (wasla) |
| `warning` | source-side completion or review advisable; not blocking | `partial_vocalization`, `weak_provenance`, `title_used_as_surface_candidate`, `collision_same_unvocalized_key`, `exact_duplicate_surface` |
| `block` | blocks admission to any snapshot or source-table until upstream clarifies | `true_source_discrepancy`, `prose_label_in_operator_cell`, `descriptive_not_surface`, `no_surface_candidate` |

**`block` severity** does *not* mean Saleh's runtime is blocked — Saleh runtime never consumes these rows in the first place. It means the row is **excluded from any docs-only snapshot or source-table contract** until upstream action.

## 7. Evidence Required

A reportable discrepancy must carry **all** of the following evidence fields in its triage record. Reports lacking any of these are not actionable.

1. **`source_path`** — absolute path to the source file (e.g. `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`).
2. **`source_size_bytes`** — byte size of the source file at prototype-run time.
3. **`source_mtime_utc`** — file modification time in ISO-8601 UTC.
4. **`source_sha256`** — SHA-256 of the source file at prototype-run time.
5. **`source_row_number`** — row position at prototype-run time (CSV) or `(file, entry_index, entry_id)` triple (JSON).
6. **`operator_cell_verbatim`** — NFC string, harakat preserved.
7. **`example_vocalized_verbatim`** — NFC string, harakat preserved.
8. **`sub_class`** — one of `linkage_vowel_difference`, `partial_vocalization`, `true_source_discrepancy`, `prose_label_in_operator_cell`.
9. **`diagnostic_summary`** — one-paragraph human-readable summary of why the sub-class fires.
10. **`prototype_run_id`** — pointer to the prototype script + invocation time (so the finding is reproducible).
11. **`finding_id`** — assigned at triage (e.g. `R-001`, `R-002`).

**`Example_Vocalized` discipline reaffirmation** (PR #98 § 12.4): the verbatim `example_vocalized_verbatim` field is recorded **as descriptive evidence of the source's own representation**, **never** as proof, fixture, runtime input, i'rāb evidence, Amil-effect evidence, role proof, or hukm / dalalah / meaning derivation. This is the same discipline as in PR #103 § 9 and PR #104 § 9.

## 8. What Saleh May Record

Saleh may record the following, **inside its documentation corpus only**:

- A new section of this contract (in a future docs-only amendment PR), listing additional triaged findings under the same § 4 template (`R-003`, `R-004`, …).
- The finding's identifier in the exclusion list of any future snapshot PR (e.g. a future SNAP-002 PR may cite `R-001` and `R-002` as reasons for excluding rows 42 and 56).
- A short citation in the report body of any future source-table contract PR (e.g. a future *Awamil detailed source table* contract may carry an "Excluded findings" section that lists `R-001` and `R-002`).
- A pointer (path, byte size, SHA-256) to the upstream report that was sent — never the report content embedded in Saleh.

Each of these recordings is **docs-only**. None creates a runtime layer, registry, fixture, or data file.

## 9. What Saleh Must Not Do

Saleh must NOT, under any reading of this contract:

- **Modify the external source.** Saleh has zero write access to `new_arabic_analyzer/`. This contract reaffirms that boundary.
- **Silently correct the discrepancy.** No row of any external source is ever re-vocalized, re-classified, or re-shaped by Saleh's own code, docs, or maintainer-side intervention. A row that is wrong stays wrong until the upstream maintainer fixes it; only at the next prototype run does Saleh observe the change.
- **Promote source-side taxonomy to Saleh canonical.** Any classification or fix the upstream makes is *source-side* news, not Saleh-canonical truth. PR #103 § 7(5) controls.
- **Consume `Example_Vocalized` as runtime input.** PR #98 § 12.4 controls.
- **Use a finding to license a runtime adapter / carrier / producer / rule / evidence / candidate.** Findings are *documentation facts*, not runtime authorisations.
- **Treat the upstream report as a fixture.** The report is a one-way message to the upstream maintainer; it is not a Saleh test fixture and is not reproduced verbatim in `tests/`.
- **Adjudicate which cell is correct** (`Operator` vs `Example_Vocalized`). The maintainer (Saleh side) may *recommend* a direction in the upstream report, but that recommendation is non-binding; only the upstream maintainer of `new_arabic_analyzer/` may fix the source.
- **Bundle a finding's resolution with any other PR.** Each finding-resolution lands in its own docs-only amendment PR; never bundled with snapshot work, source-table work, or runtime work.

## 10. Upstream Correction Workflow

The upstream side of the workflow has zero Saleh-side automation. The protocol is:

1. **Saleh maintainer sends** an upstream report. The report is a self-contained Markdown document (typically `/tmp/upstream_report_R-NNN.md`) carrying the seven evidence fields of § 7 plus a recommended question or recommended fix. The path is `/tmp` because the report is *external correspondence*, not a Saleh artefact.
2. **Upstream maintainer receives** the report and decides:
   - (a) accept the recommendation and fix the source file; or
   - (b) reject the recommendation and explain why; or
   - (c) request more evidence.
3. **Saleh maintainer re-runs** the read-only prototype after the upstream confirms a fix or a non-fix decision (§ 11).
4. **Saleh maintainer opens** a docs-only amendment PR to *this contract* updating the finding's status:
   - `resolved_upstream_fixed` — upstream changed the source; the next prototype run no longer emits the warning; the finding's status is closed; future snapshots may admit the (now-clean) row.
   - `resolved_no_action_required` — upstream rejected the recommendation or amended a sibling contract to accept the form; the finding's status is closed without source-side change.
5. **No retroactive snapshot inclusion.** A finding that flips to `resolved_upstream_fixed` does **not** retroactively appear in any earlier snapshot. The clean row may appear in a *new* snapshot ID; earlier snapshots remain frozen at the source state they cited.

This protocol holds regardless of how the upstream maintainer is reached (email, chat, issue tracker, in-person). The boundary is: Saleh reports, upstream fixes, Saleh re-inspects.

## 11. Re-Inspection Rules

After any upstream action (fix or non-fix), the Saleh maintainer must re-inspect under the following rules before updating any finding's status:

1. **Re-run the prototype** against the current upstream source. Re-running means executing the *same prototype script* at the same prototype-run-id-bound invocation. The current canonical prototype is `/tmp/source_preview_runner.py`.
2. **Compare provenance**. If `source_size_bytes`, `source_mtime_utc`, or `source_sha256` has changed, the prototype's outputs are a *new* run and bear a new `prototype_run_id`. The finding's status update must cite the new `prototype_run_id`.
3. **Compare warnings ledger**. If the warning row corresponding to the finding is *gone* from the new run's `/tmp/source_preview_validation_warnings.csv`, the finding flips to `resolved_upstream_fixed`. If the warning is still present but the upstream has confirmed no-action, the finding flips to `resolved_no_action_required`. If the warning has *changed sub-class* (e.g. `true_source_discrepancy` → `partial_vocalization`), this is a *new finding*; a new ID is assigned and the old finding is closed as `resolved_upstream_fixed`.
4. **Never assume the warning is gone** based on memory or a partial inspection. The prototype's outputs are the binary-precise reference.
5. **Snapshot re-issuance.** If the re-inspection shows that a previously-excluded row now passes inclusion, the row may be admitted in a *new* snapshot ID under PR #103 § 14's future-snapshot reservation. The row is **not** retroactively added to any prior snapshot file in `docs/qiyas_core/snapshots/`. PR #103 § 12 explicitly forbids snapshot in-place mutation.

## 12. Non-Goals

This contract explicitly does NOT:

- correct or alter any external source file;
- create any runtime layer, adapter, producer, carrier, rule, evidence type, or candidate type;
- create any registry under `src/qiyas_core/registries/`;
- create any test under `tests/`, any fixture, or any data file under `data/`;
- amend any predecessor contract (PR #86 / PR #96 / PR #97 / PR #98 / PR #103);
- amend `new_arabic_analyzer/` in any way;
- start `AmilEffectEvidence`, `I'rabEffectEvidence`, `WordCandidate`, `LafzCandidate`, `DalalahCandidate`, `Meaning`, `Hukm`, `RealityClaim`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, or `OperatorGeometry`;
- start `Amil` runtime or `I'rāb` runtime;
- start `GlyphClassificationEvidence` runtime, `GlyphClassificationGate` runtime, or `SifatVector` runtime;
- amend `letter_name_registry.py` or `letter_role_registry.py`;
- use `Example_Vocalized` as runtime input, fixture, i'rāb evidence, Amil-effect evidence, role proof, or hukm / dalalah / meaning derivation (PR #98 § 12.4 controls);
- promote the source's grammatical taxonomy to Saleh-canonical (PR #103 § 7(5) controls);
- adjudicate which side of a discrepancy is correct;
- bundle this contract's amendments with snapshot work, source-table work, or runtime work;
- open SNAP-002, SNAP-003, mabniyat pilot snapshot, or any source-table contract — those are A4 / A5 / A6 / A2 / A3 of the next-tracks schema and each has its own PR;
- open Track B (runtime evidence-layer extensions), Track C (resolver / MIU extensions), or Track D (maintainer-side follow-ups);
- engage PR #99 or any other unrelated PR;
- adjudicate `حَاشَا` / `عَدَا` / `خَلَا` exception-preposition classification (PR #103 § 10.3 controls).

## 13. Future Work

Each future step is its own docs-only PR. None implies the next.

1. **Amendment PRs for additional findings.** As future prototype runs detect new discrepancies, each new finding (R-003, R-004, …) is recorded by a *new* docs-only PR that adds a new sub-section under § 4 of this contract. The contract grows; it is never silently rewritten.
2. **Amendment PRs for finding-status transitions.** A finding flipping to `resolved_upstream_fixed` or `resolved_no_action_required` is recorded by a *new* docs-only PR that updates the finding's status sub-section. The full history is preserved.
3. **Sibling contract: detailed awamil source-table contract** (Track A2). Will cite this contract by name when listing per-row exclusions.
4. **Sibling contract: detailed mabniyat source-table contract** (Track A3). Same.
5. **SNAP-002 collision-class operators PR** (Track A4). Will cite `R-001` / `R-002` in its exclusion list; will NOT include any block-severity finding.
6. **Future snapshot PRs** (A5, A6, …) — same citation pattern.

None of the above implies opening runtime work. No PR opened under this contract creates code.

## 14. Summary Table

| Question | Answer |
|---|---|
| Does this contract create runtime? | **No** |
| Does it create a registry? | **No** |
| Does it modify external source files? | **No** |
| Does it silently fix discrepancies? | **No** |
| What does it create? | A workflow for reporting discrepancies + a record of known findings |
| Number of `true_source_discrepancy` findings recorded? | **2** (R-001, R-002) |
| Are findings runtime data? | **No** — documentation only |
| Are findings test fixtures? | **No** |
| Does Saleh write to `new_arabic_analyzer/`? | **No** |
| Who fixes the source data? | The upstream maintainer of `new_arabic_analyzer/`, not Saleh |
| What happens to a previously-excluded row that the upstream fixes? | Eligible for a *new* snapshot ID under PR #103 § 14; never retroactively added to an old snapshot |
| Is `Example_Vocalized` consumed as runtime input? | **No** (PR #98 § 12.4 controls) |
| Approval status of this contract? | Docs-only constitutional contract; opened under Track A1 of the post-PR-#104 next-tracks schema |

End of contract.
