# Mabniyat Pilot Snapshot Policy

> **Status**: docs-only constitutional policy — **eligibility policy only**.
> **Authority**: extends `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97), `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103), `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105), `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #106), and `ARABIC_MABNIYAT_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #107). Binds `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 (Vocalized Source Identity Discipline), `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96), `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 (`Example_Vocalized` discipline), and uses `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) as the *worked policy → instantiation precedent* for operators (NEVER editing it).
> **Scope**: defines the per-row *eligibility gate* under which a *future* mabniyat pilot snapshot instantiation PR may admit a small subset of mabniyat entries from `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/02_mabniyat/`. This policy specialises PR #103 for the mabniyat corpus, sitting *above* PR #107's per-row schema (A3) and *below* a future mabniyat pilot snapshot instantiation PR (analogous to PR #104 SNAP-001 but for mabniyat).
> **Non-Authority**: this policy is **eligibility policy only**. It does **NOT** instantiate a pilot snapshot, does **NOT** approve any row, does **NOT** approve any entry, does **NOT** list any row table, does **NOT** create any file under `docs/qiyas_core/snapshots/`, does **NOT** copy any source JSON into Saleh, does **NOT** create runtime / registry / test / fixture / data file, does **NOT** silently correct any discrepancy, does **NOT** promote source-side classification to Saleh-canonical, does **NOT** amend any predecessor contract, and does **NOT** open `SNAP-002` / `SNAP-003`.

---

## 1. Purpose

This policy codifies the per-row **eligibility gate** for a *future* mabniyat pilot snapshot. It is the mabniyat sibling of `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) for the operators/awamil corpus — and is **explicitly reserved by name** in `ARABIC_MABNIYAT_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #107) § 16.1:

> *"Mabniyat pilot snapshot policy — a docs-only sub-contract (or amendment to PR #103) that specialises PR #103's general snapshot policy to the mabniyat corpus, including any explicit per-class admission rule needed to admit priority classes beyond 1."*

This policy:

- defines under what conditions a mabniyat entry **may be considered eligible for review** under a future pilot snapshot cycle;
- maps PR #107's 9-way surface-field priority classes to eligibility verdicts;
- maps the 11-warning-class taxonomy (PR #103 § 8) to per-row eligibility decisions;
- specialises PR #107 § 14's inclusion rules to the *pilot* admission decision;
- specialises PR #107 § 15's exclusion rules to the same;
- describes (but does not build) a future `/tmp/` review pack and row-decision template;
- describes (but does not open) the future mabniyat pilot snapshot instantiation PR shape.

This policy is **docs-only**. It is **eligibility policy only**. It:

- does NOT instantiate any pilot snapshot;
- does NOT approve any row;
- does NOT approve any entry;
- does NOT contain an "Approved Rows" or "Approved Entries" table;
- does NOT copy or import any JSON file from `new_arabic_analyzer/02_mabniyat/`;
- does NOT create any file under `docs/qiyas_core/snapshots/`;
- does NOT create a runtime layer, an adapter, a producer, a carrier, a rule, a registry, an evidence type, a candidate type, a test fixture, or any data file;
- does NOT change any existing contract;
- does NOT amend `new_arabic_analyzer/`;
- does NOT claim that mabniyat rows are linguistically proven;
- does NOT claim that Saleh "solves" Arabic mabniyat.

## 2. Relationship to Predecessor Contracts

This policy sits *on top of* the predecessors below; it does not redefine, weaken, or override any of them. Where a sentence in this policy could be read as conflicting with a predecessor, the predecessor controls.

| document | role | how this policy uses it |
|---|---|---|
| `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline (`surface_form_vocalized` is identity; `مِنْ ≠ مَنْ`) | § 5 / § 6 of this policy re-bind the discipline verbatim; eligibility evaluation never collapses vocalized identities |
| `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) | inventory of the two external corpora at `new_arabic_analyzer/data/` | this policy points the future pilot review pack (§ 12) at the inventory's mabniyat path verbatim |
| `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) § 15 | the five reserved snapshot forms | this policy specialises PR #97's general normalization shape to the *mabniyat-pilot* admission decision; the future pilot snapshot will use the `normalized-table` form, mirroring PR #103's choice for operators |
| `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) | **the structural sibling** — general snapshot policy for the operators/awamil corpus; § 5 / § 6 / § 7 / § 8 / § 9 / § 12 / § 13 / § 14 | this policy specialises *every* PR #103 section to mabniyat: § 5 (inclusion) → § 4 / § 5 here; § 6 (exclusion) → § 10 here; § 7 (identity) → re-bound; § 8 (warning) → § 10 here as the warning-to-eligibility map; § 9 (`Example_Vocalized`) → § 9 here; § 12 (provenance) → § 6 here as the provenance-strength rules; § 13 (forbidden) → § 16 here; § 14 (future PR shape) → § 14 here |
| `snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) | **the worked policy → instantiation precedent** for the operators corpus: PR #103 (policy) → PR #104 (first instantiation under the policy) | this policy uses PR #104 as the *template* the future mabniyat pilot snapshot instantiation PR will mirror; this policy does NOT edit PR #104 |
| `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) | discrepancy reporting workflow | § 11 of this policy binds PR #105 verbatim; mabniyat findings, when discovered, will receive `R-NNN` IDs under PR #105's amendment workflow first, then propagate into this policy via a future amendment |
| `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #106) | awamil sibling of A3 — the per-row schema for the operators corpus | this policy is the mabniyat-side analogue of "what PR #103 was *for* PR #106"; it does not amend PR #106 |
| `ARABIC_MABNIYAT_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #107) | **the per-row schema layer this policy sits on top of**; § 4 / § 5 / § 7 / § 8 / § 14 / § 15 / § 16 | every section of this policy cites the corresponding A3 section: § 4 (eligibility concept) → A3 § 14 + A3 § 5.2; § 5 (priority classes) → A3 § 5 verbatim; § 6 (provenance strength) → A3 § 6 / § 9; § 7 (title rules) → A3 § 7; § 8 (weak provenance rules) → A3 § 8; § 10 (exclusion) → A3 § 15; § 11 (discrepancy) → A3 § 12 |

**Layering**: PR #107 (per-row schema) → **this policy** (per-row eligibility gate) → future mabniyat pilot snapshot instantiation PR (per-row admission, with row table). The schema layer says *what a mabniyat row looks like under review*; this policy layer says *which rows are eligible for the pilot snapshot*; the instantiation layer says *which rows are actually approved by the maintainer at instantiation time*. **This PR is the middle layer only.**

This policy does **not** amend any predecessor. Where a sentence could be read as conflicting with any predecessor, the predecessor controls.

## 3. Why This Is Not A Pilot Snapshot

This section is load-bearing and intentionally explicit. The constitutional difference between *policy* and *instantiation* must remain visible to every future reviewer.

This policy is **NOT**:

- **A pilot snapshot.** It does not instantiate any snapshot under `docs/qiyas_core/snapshots/`.
- **An approval.** It does not approve any row. It does not approve any entry.
- **A copy of source JSON.** It does not copy any byte from `new_arabic_analyzer/02_mabniyat/` into Saleh.
- **A source row table.** It does not contain a row table listing surface forms with provenance and approval verdicts.
- **A snapshot markdown file.** No file is created under `docs/qiyas_core/snapshots/` by this PR.
- **A fixture.** No fixture is created under `tests/` or anywhere else.
- **A runtime admission.** No runtime layer / adapter / producer / carrier / rule / evidence type / candidate type is created or licensed.
- **A registry.** No registry is created under `src/qiyas_core/registries/` or anywhere else.
- **A source correction.** No source-side data is changed; Saleh has zero write access to `new_arabic_analyzer/` (PR #105 § 9 reaffirmed).

The future mabniyat pilot snapshot **instantiation** PR (a *separate*, *later*, *explicitly-authorised* docs-only PR) will be the layer where:

- a small pilot subset of mabniyat entries is named;
- those entries are recorded in an "Approved Rows" / "Approved Entries" table under `docs/qiyas_core/snapshots/<file>.md`;
- the maintainer's manual review attestation is cited verbatim.

**That is not what this PR does.** This PR establishes the *rules* under which that future PR may operate. Mixing rules with instantiation in a single PR would conflate the policy layer with the admission layer — exactly the conflation that PR #103 → PR #104 successfully avoided for the operators corpus.

For a literal example of what an instantiation looks like and what this policy is *not* doing, see PR #104's `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` § 10 ("Approved Rows") — a table that this policy intentionally and constitutionally **omits**.

## 4. Pilot Eligibility Concept

This policy introduces the concept `pilot_eligible` as a **future review status only**. It is not a runtime status. It is not a registry status. It is not a Saleh-canonical Candidate / Evidence / Carrier flag.

A mabniyat entry is "**eligible for pilot review**" under this policy if and only if it satisfies all of the per-row eligibility tests in § 5 / § 6 / § 7 / § 8 / § 9 / § 10 / § 11. Even when eligible, the entry's actual admission to a future pilot snapshot requires a separate maintainer-led manual review pass (described in § 12 / § 13).

**Eligibility under this policy does NOT mean any of the following:**

- It does **not** mean the row is *linguistically proven* in classical Arabic grammar.
- It does **not** mean the row is *runtime valid*. Runtime eligibility is unconditionally `NO` under this policy.
- It does **not** mean the row is *registry valid*. This policy does not create a registry; no registry validation is implied.
- It does **not** mean the row carries any *meaning*, *hukm*, *reality*, *dalalah*, *amil effect*, or *i'rāb effect* claim. None of those higher-layer artefacts exists or is implied.
- It does **not** mean the row is *accepted into the Saleh source corpus permanently*. Snapshots are *frozen* (PR #103 § 12); a future re-snapshot under a new `snapshot_id` is the only path to update.
- It does **not** mean the source's classification of the entry is *Saleh-canonical*. Source taxonomy remains source-side under PR #103 § 7(5).

A `pilot_eligible` entry is *a candidate for the future pilot review pass*, nothing more.

## 5. Surface Priority Classes and Eligibility

This section specialises PR #107 § 5's 9-way ordered priority to per-class eligibility verdicts for the future mabniyat pilot snapshot.

| # | priority class (per PR #107 § 5.1) | default eligibility | required evidence | allowed in future pilot? | excluded? | requires reviewer note? | runtime eligibility |
|---:|---|---|---|---|---|---|---|
| 1 | explicit vocalized surface field | **`pilot_eligible`** | source field name + NFC harakat-preserving surface + provenance fields per § 6 | **yes** (under maintainer manual review) | no | no | **NO — always** |
| 2 | explicit unvocalized surface field plus vocalization evidence | **`pilot_eligible_with_reviewer_note`** | source field name + companion vocalization evidence (sibling field or example-mediated) + provenance fields + explicit reviewer note documenting the vocalization reasoning | **yes** (only with reviewer note) | no | **yes — mandatory** | **NO — always** |
| 3 | title field used as surface candidate | **`ineligible_pending_review`** | title value + explanation why title is plausibly a surface form + reviewer note + no contradictory priority-1/2 field + no unresolved discrepancy (§ 7) | no — not by default | flagged `title_used_as_surface_candidate` | **yes** | **NO — always** |
| 4 | key field used as surface candidate | **`ineligible_pending_review`** | key value + explanation why the key is plausibly a surface form + reviewer note | no — not by default | flagged warning | **yes** | **NO — always** |
| 5 | example-derived candidate, review-only | **`ineligible_pending_review`** | example sentence + explicit reviewer note documenting the source-confirmation rationale (§ 9) | no — not by default | flagged warning | **yes** | **NO — always** |
| 6 | category-label-only row | **`ineligible_blocked`** | n/a — no surface form recoverable | **no** | blocked | n/a | **NO — always** |
| 7 | prose-description-only row | **`ineligible_blocked`** | n/a — no surface form recoverable | **no** | blocked (`descriptive_not_surface`) | n/a | **NO — always** |
| 8 | multi-surface row requiring split review | **`ineligible_pending_split_review`** | per-surface split must be defined by a future split-review rules sub-contract | no — not until the split-review sub-contract lands | deferred | n/a (deferred) | **NO — always** |
| 9 | missing-surface row | **`ineligible_blocked`** | n/a — no surface form | **no** | blocked (`no_surface_candidate`) | n/a | **NO — always** |

**Runtime eligibility is unconditionally `NO`** for every class regardless of any other field. The "runtime eligibility" column exists to make that boundary terminal-visible at every row.

**No row is approved by this policy.** Classes 1 and 2 are *eligible for review*; the maintainer's review pass at the future instantiation PR is the moment any specific row becomes an approved row.

## 6. Provenance Strength Rules

Each mabniyat entry's `provenance_strength` is one of the following levels. This section maps each level to pilot eligibility, the reviewer-note requirement, discrepancy interaction, and the future snapshot boundary.

| `provenance_strength` | corresponding priority classes | pilot eligibility | reviewer note required? | discrepancy interaction | future snapshot boundary |
|---|---|---|---|---|---|
| **`strong_explicit_surface`** | class 1 | `pilot_eligible` | no | row admissible only if `discrepancy_status` is `none` or `resolved_upstream_fixed` | natural admission candidate for the first mabniyat pilot snapshot |
| **`explicit_surface_with_vocalization_support`** | class 2 | `pilot_eligible_with_reviewer_note` | **yes** — documenting the companion vocalization evidence | same as above | admissible with reviewer attestation; recorded in the future snapshot's frontmatter |
| **`title_candidate_review_required`** | class 3 | `ineligible_pending_review` | **yes** — documenting why the title is plausibly a surface form (per § 7) | row admissible only if no `awaiting_upstream` finding | deferred until reviewer promotion under § 7's rule |
| **`key_candidate_review_required`** | class 4 | `ineligible_pending_review` | **yes** — documenting why the key is plausibly a surface form | same as above | deferred |
| **`example_candidate_review_only`** | class 5 | `ineligible_pending_review` | **yes** — documenting the source-confirmation rationale (per § 9) | row admissible only if no `awaiting_upstream` finding | deferred until reviewer confirmation under § 9's rule |
| **`weak_provenance`** | classes 3, 4, 5, 8 (when also flagged `weak_provenance`) | `ineligible_pending_review` | **yes** — documenting the weak-provenance rationale (per § 8) | row admissible only if no `awaiting_upstream` finding | deferred until reviewer rationale resolves |
| **`missing_or_blocked`** | classes 6, 7, 9 | `ineligible_blocked` | n/a | n/a (blocked regardless of discrepancy status) | not eligible for any future mabniyat pilot snapshot; reserved exclusion |

**`provenance_strength = weak_provenance` is a source-review caution, not a linguistic error** (PR #107 § 8.3 reaffirmed). Promotion of a weak-provenance row to `pilot_eligible` is *never automatic* under this policy.

## 7. `title_used_as_surface_candidate` Rules

Title-derived surface candidates (priority class 3 per § 5) MUST satisfy **all** of the following before being considered for the future mabniyat pilot snapshot:

1. **`source_file` is recorded** (the JSON file basename).
2. **`source_entry_id` is recorded** (the entry's stable identifier within the file, or `source_entry_index` as fallback).
3. **The title value is recorded verbatim** in `surface_form_vocalized` if NFC-clean, OR with an explicit reviewer note explaining any normalization.
4. **An explanation is recorded** in `reviewer_note` describing why the title is *plausibly* the entry's surface form (rather than a descriptive heading). Plausible rationales include:
   - the file's source class (§ 4 of PR #107) is `particles / fixed expressions` and the title carries a single Arabic token;
   - the title's NFC string is a single mabni surface form, not multi-token prose;
   - the file lacks any priority-1 or priority-2 surface field for this entry.
5. **A reviewer note** is required and must be recorded verbatim — author name + UTC ISO-8601 timestamp + the plausibility rationale above.
6. **No contradictory surface field is present** in the same entry under priority classes 1–2. If such a field is present, the title is NOT the appropriate surface candidate; the entry should be re-evaluated under priority class 1 or 2 instead.
7. **No unresolved discrepancy** flags the row in PR #105's workflow.

**Default disposition**: `needs_review`. The row is NOT pilot-eligible by default.

**Promotion to `pilot_eligible`** requires that *every* condition above is satisfied AND the maintainer explicitly records the promotion decision in the future row-decision template (§ 13). Silent promotion is forbidden.

Title-derived candidates are NEVER runtime-eligible. Runtime eligibility is unconditionally `NO` for this class.

## 8. `weak_provenance` Rules

Weak-provenance candidates (any row flagged `weak_provenance` per PR #107 § 8) MUST satisfy **all** of the following before being considered for the future mabniyat pilot snapshot:

1. **A `provenance_explanation`** is recorded, describing the basis for the surface-form attribution (e.g. "surface derived from `title` field; no priority-1 surface field present in this entry").
2. **A `source_field_trace`** is recorded, listing every source-side field consulted during the surface-candidate selection (e.g. `[title, description, example]` if the reviewer inspected those three before settling on a candidate).
3. **A reviewer note** is required, with author + timestamp + the rationale for tolerating weak provenance in this specific entry under the pilot policy. The rationale must address: why no stronger provenance exists, why the chosen surface is plausible, and what would invalidate the choice.
4. **No unresolved discrepancy** flags the row in PR #105's workflow.
5. **An `explicit_pilot_tolerance_rationale`** is recorded, naming the reason this specific weak-provenance row should be tolerable in the pilot subset. Rationale categories include:
   - the source file is the *only* source for this mabni surface (no priority-1 alternative exists in the corpus);
   - the file's source class (per PR #107 § 4) is well-understood and the weak-provenance flag is purely structural (e.g. `weak_provenance` from file classification, not from per-entry ambiguity);
   - none of the rationale relies on Saleh runtime, on `Example_Vocalized` as proof, or on `Word`/`Lafz`/`Dalalah`/`Meaning`/`Hukm`/`Reality` derivation.

**`weak_provenance` is a source-review caution, not an automatic source error** (PR #107 § 8.3 verbatim).

**Default disposition**: `needs_review` (priority class 3, 4 weak-provenance variants) or `blocked` (where the weak provenance compounds with a `block`-severity exclusion from § 10).

**Promotion to `pilot_eligible`** requires every condition above AND the maintainer's explicit promotion decision. Silent promotion is forbidden.

Weak-provenance candidates are NEVER runtime-eligible.

## 9. Example-Derived Candidate Rules

Example-derived candidates (priority class 5 per § 5) are **review-only** under this policy. The `Example_Vocalized` discipline from PR #98 § 12.4, reaffirmed by PR #103 § 9 / PR #104 § 9 / PR #105 § 9 / PR #106 § 8 / PR #107 § 11, is re-bound here verbatim:

- **`Example_Vocalized` MAY NOT define identity.** Two mabniyat entries are the same identity if and only if their `surface_form_vocalized` strings are NFC-equal — never because their `Example_Vocalized` cells share content.
- **`Example_Vocalized` MAY NOT override the source surface.** If the source's surface field carries content X and the example sentence vocalizes X differently as Y, the identity remains X. The Y reading is a *source-review observation*, not a re-vocalization authority.
- **`Example_Vocalized` MAY NOT be proof.** Not of meaning, not of i'rāb, not of role, not of Amil effect, not of hukm / dalalah / reality.
- **`Example_Vocalized` MAY NOT be runtime input.** No Saleh runtime layer consumes `Example_Vocalized` as evidence.
- **`Example_Vocalized` MAY NOT be a fixture.** No test under `tests/` consumes `Example_Vocalized`. Future fixture admission would require a separate explicitly-authorised fixture contract that does not yet exist and is not opened here.

**Default disposition**: `needs_review`. Rows where the *only* source for the surface candidate is the example are NOT pilot-eligible by default.

**Promotion to `pilot_eligible`** requires:

1. **Additional explicit source confirmation** — a reviewer note documenting an *additional* source-side source for the candidate (e.g. a sibling field in the same entry, or a cross-entry corroboration in the same file). A row whose surface derives *solely* from an example sentence is not promotable.
2. **No `Example_Vocalized`-as-proof claim** anywhere in the row's review record.
3. **Maintainer explicit promotion decision** in the future row-decision template.

Example-derived candidates are NEVER runtime-eligible.

## 10. Exclusion Rules

The following classes of mabniyat entries are explicitly excluded from any future mabniyat pilot snapshot under this policy. Each exclusion has a forward path either to a future amendment (under this policy) or to a reserved sibling cycle (under PR #107 § 16).

### 10.1 By priority class (per § 5)

- **Missing-surface rows (class 9)** — `no_surface_candidate` flag; blocked.
- **Prose-description-only rows (class 7)** — `descriptive_not_surface` flag; blocked.
- **Category-label-only rows (class 6)** — blocked.
- **Multi-surface rows (class 8)** — `ineligible_pending_split_review`; deferred until a future split-review rules sub-contract lands (per PR #107 § 16.3).

### 10.2 By warning class (the warning-to-eligibility map)

The 11 warning codes from PR #103 § 8, mapped to eligibility verdicts under this policy:

| `warning_code` | severity (per PR #103 § 8) | eligibility verdict under this policy |
|---|---|---|
| `linkage_vowel_difference` | info | **`ineligible`** — excluded from any zero-warnings admission, mirroring PR #103 § 5 and PR #106 § 12 |
| `length_6_plus` | info | **`ineligible`** — excluded from any zero-warnings admission for consistency (PR #107 § 15) |
| `partial_vocalization` | warning | **`ineligible_pending_review`** — defer until source-side vocalization completion or explicit reviewer note |
| `collision_same_unvocalized_key` | warning | **`ineligible`** — reserved for SNAP-002 collision-handling sub-contract (PR #106 § 14.1, PR #107 § 16.3) |
| `exact_duplicate_surface` | warning | **`ineligible`** — reserved for SNAP-003 (PR #106 § 14.3) |
| `title_used_as_surface_candidate` | warning | **`ineligible_pending_review`** — per § 7 of this policy |
| `weak_provenance` | warning | **`ineligible_pending_review`** — per § 8 of this policy |
| `unknown_length` | warning | **`ineligible_pending_review`** — manual review required |
| `no_surface_candidate` | block | **`ineligible_blocked`** — per § 10.1 above |
| `descriptive_not_surface` | block | **`ineligible_blocked`** — per § 10.1 above |
| `true_source_discrepancy` | block | **`ineligible_blocked`** — reserved for PR #105's upstream resolution workflow (per § 11 below) |

### 10.3 By source-correction or runtime-interpretation need

- **Source correction required** — Saleh does not correct upstream; rows are deferred until PR #105's upstream resolution closes the finding.
- **Runtime interpretation required** — no mabniyat entry is admitted into runtime under this policy or any contract under this policy.
- **`Word` / `Lafz` / `Dalalah` / `Meaning` / `Hukm` / `Reality` interpretation** — any row whose interpretation would require these higher-layer artefacts is out of scope and explicitly forbidden by § 16.

Exclusion is **deferral**, not **rejection**. Excluded classes have their own forward path either to a future split-review sub-contract (multi-surface), a SNAP-002 collision-handling sub-contract (collisions), a SNAP-003 duplicate-handling sub-contract (duplicates), PR #105 upstream resolution (discrepancies), or amendment of this policy.

## 11. Discrepancy Integration

This policy binds `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) by citation. Discrepancies in the mabniyat corpus follow PR #105's reporting workflow (PR #105 § 5).

Specifically (re-binding from PR #105 § 9):

1. **Rows with `true_source_discrepancy` are blocked** from any pilot eligibility evaluation under this policy. They remain `ineligible_blocked` until PR #105's upstream workflow closes the finding.
2. **Mabniyat findings may be reported upstream** per PR #105 § 10. The upstream maintainer of `new_arabic_analyzer/` is the only authority that may fix source-side data.
3. **Cannot enter pilot until resolved OR until this policy explicitly documents why a flagged row is not a *true* discrepancy.** This policy does not currently document any such non-discrepancy carve-out; any future carve-out would require a separate policy amendment PR.
4. **No mabniyat findings exist at the time of writing** (R-001 and R-002 are *awamil* findings under PR #106 § 13, owned by the awamil corpus). When the first mabniyat finding is discovered, it will receive the next-available `R-NNN` identifier under PR #105's amendment workflow first, then propagate into this policy via a future amendment.
5. **Saleh does NOT correct upstream source data.** Saleh reports; upstream fixes; Saleh re-inspects. The boundary is not crossable.

## 12. Future `/tmp` Review Pack

Before any future mabniyat pilot snapshot instantiation PR is opened, a `/tmp/` review pack MUST be created by a separately-authorised read-only review turn. The pack is **review artefacts only** — none of these files enter the Saleh repository automatically; none is committed; none is part of this PR.

The expected pack contents (described, not built):

| `/tmp/` artefact | role |
|---|---|
| `/tmp/source_preview_mabniyat.csv` | the existing read-only normalization prototype output; already produced; cited by PR #107 § 3 |
| `/tmp/mabniyat_pilot_candidate_preview.csv` | a new prototype-derived preview restricted to rows that satisfy § 5 / § 6 of this policy; one row per *candidate* entry; carries the 14 normalized review fields per § 13 below |
| `/tmp/mabniyat_pilot_candidate_review.md` | a human-readable maintainer-facing review document (analogous to `/tmp/snap001_terminal_review.md` from the SNAP-001 cycle) listing the candidate entries with surface form, source file, source entry id, priority class, provenance strength, and pre-filled `pilot_eligibility` verdict |
| `/tmp/mabniyat_pilot_row_decisions_template.csv` | a blank CSV template (no row decisions) with the 14 columns from § 13 below, intended for the maintainer to fill out during review |
| `/tmp/mabniyat_pilot_eligibility_report.md` | a final report summarising eligibility counts by priority class, by warning code, by source file, and by source class; consumed by the future instantiation PR |

**These artefacts are produced by a separate read-only review turn, never by this PR.** This PR does not create, edit, or reference these files except by description. The review pack's authorisation is its own future explicit trigger, not this PR's merge.

## 13. Future Row-Decision Template

The future row-decision template (`/tmp/mabniyat_pilot_row_decisions_template.csv` per § 12) MUST carry the following 14 columns, in this order:

| column | role |
|---|---|
| `source_file` | the JSON file basename (provenance) |
| `source_entry_id` | the entry's stable identifier within the file |
| `source_class_label` | one of PR #107 § 4's labels |
| `surface_form_vocalized` | NFC, harakat-preserved (PR #86 § 12.1) |
| `surface_form_unvocalized_key` | NFC + harakat stripped (diagnostic only) |
| `surface_priority_class` | one of 1–9 per PR #107 § 5.1 |
| `provenance_strength` | one of the seven levels per § 6 |
| `review_status` | one of `ready` / `needs_review` / `no` (per PR #107 § 6) |
| `pilot_eligibility` | one of `pilot_eligible` / `pilot_eligible_with_reviewer_note` / `ineligible_pending_review` / `ineligible_pending_split_review` / `ineligible_blocked` |
| `discrepancy_status` | one of `none` / `awaiting_upstream` / `resolved_upstream_fixed` / `resolved_no_action_required` (per PR #105 § 5) |
| `reviewer_decision` | one of `approve` / `reject` / `defer` — **blank initially** until reviewer fills in |
| `reviewer_note` | free-text reviewer rationale (descriptive only) |
| `exclusion_reason` | citation to the § 10 / § 7 / § 8 / § 9 clause that triggers exclusion (empty if not excluded) |
| `upstream_report_id` | PR #105 finding ID (e.g. `R-003`) if the row has triggered an upstream report; empty otherwise |

**This policy does NOT include actual row content.** No row of any mabniyat JSON file is reproduced here, in the future template, or in any policy artefact under this PR. The template is *structurally described only*; the future review turn fills in entries for the candidate pool defined by § 5 / § 6 / § 7 / § 8 / § 9 / § 10 / § 11.

## 14. Future Pilot Snapshot PR Boundary

A future mabniyat pilot snapshot instantiation PR may be opened **only after all** of the following are true:

1. **The `/tmp/` review pack of § 12 has been created** in a separately-authorised read-only review turn.
2. **The candidate rows have been manually reviewed** by the maintainer (Hussein).
3. **Per-row decisions have been recorded** in `/tmp/mabniyat_pilot_row_decisions_template.csv` (the filled-in version), with `reviewer_decision` set to `approve`, `reject`, or `defer` for every candidate row.
4. **This policy is cited by name** in the future instantiation PR's authority chain (alongside PR #103, PR #107, PR #105).
5. **No unresolved blockers remain** — every `ineligible_blocked` and every `awaiting_upstream` row is excluded from the approved set.
6. **The maintainer's manual review attestation is recorded** verbatim in the future instantiation PR's snapshot file (mirroring PR #104 § 5).

The future instantiation PR shape (per PR #103 § 14 + PR #104 as worked example):

- **Title pattern**: `docs(qiyas_core): add MAB-001 mabniyat pilot snapshot` (or similar `MAB-NNN` identifier).
- **Single new file** under `docs/qiyas_core/snapshots/`, mirroring PR #104's structural template (14 mandatory sections including an Approved Rows table, Snapshot Status, Policy Authority, Source Prototype Inputs, Manual Approval, Inclusion Rule, Exclusion Rule, Identity Discipline, `Example_Vocalized` Discipline, Risk Notes, What This Snapshot Does Not Authorize, Future Work, Summary Table).
- **Cites THIS policy by name** plus PR #103, PR #107, PR #105, PR #86 § 12.1, PR #98 § 12.4.
- **Expected diff size**: ~150–300 lines (depends on pilot subset size — likely smaller than SNAP-001's 13-row pilot for the operators corpus, because mabniyat priority-class 1 entries are a smaller subset of A3 § 14-eligible entries).
- **Carries the Approved Rows / Approved Entries table** that this policy intentionally and constitutionally omits.
- **Explicit "Do not merge until Hussein explicitly asks" instruction** in the merge instruction section.
- **Opens ONLY after explicit per-PR authorisation** in a separate turn from this PR's merge.
- **Still docs-only.** No `src/`, no `tests/`, no `data/`, no registry, no runtime change.

**Runtime remains forbidden** at every layer above this policy. The future instantiation PR does not unlock runtime; only an explicit constitutional amendment of the standing § 9 non-goals in the living handoff could begin to discuss it.

## 15. Validation Expectations

Validation rules **for this PR** (i.e., the PR opening this policy):

- **Exactly one new file** at `docs/qiyas_core/MABNIYAT_PILOT_SNAPSHOT_POLICY.md`. No other path is changed.
- **No "Approved Rows" table** appears in the new file (other than as the explicit negative reference in § 3 / § 14 explaining what the future instantiation PR will contain that this policy does not).
- **No "Approved Entries" table** appears anywhere.
- **No file is created under `docs/qiyas_core/snapshots/`** by this PR.
- **No JSON source file is copied** from `new_arabic_analyzer/` into Saleh.
- **The current-state checker `/tmp/check_current_qiyas_state.py "بِ ضَ وَ يَ ضَرَبَ"` returns `CURRENT QIYAS STATE CHECK: PASS`** after the file is created and committed.
- **The MIU focused smoke test `tests/qiyas_core/test_variant_resolver_miu_integration.py` returns `17 passed`** before and after the commit.
- **All grep verifications hit at meaningful counts**: `pilot_eligible`, `title_used_as_surface_candidate`, `weak_provenance`, `Example_Vocalized`, `runtime` (all in negation contexts), `mabniyat pilot`.

If any validation differs, the PR is not safe to merge; the opening turn must stop and report.

Validation expectations **for the future mabniyat pilot snapshot instantiation PR** (i.e., the *next* PR after this one, when it opens) — described here for forward-binding, not exercised here:

- the `/tmp/` review pack of § 12 must exist;
- the maintainer's manual review pass must be complete;
- the per-row decisions CSV must be populated;
- the new snapshot file under `docs/qiyas_core/snapshots/` must mirror PR #104's structural template;
- the focused smoke test and full canonical suite must still pass on the post-merge HEAD.

## 16. Non-Goals

This policy explicitly does NOT:

- **instantiate a pilot snapshot** — § 3 controls.
- **approve any row** — § 1 / § 3 / § 4 control.
- **approve any entry** — same.
- **list any row table** — same.
- **copy any source JSON** into Saleh.
- **create any file under `docs/qiyas_core/snapshots/`** by this PR.
- **import source data** — no JSON file is copied from `new_arabic_analyzer/` into Saleh.
- **create any fixture** under `tests/`.
- **create any runtime layer**, adapter, producer, carrier, rule, evidence type, or candidate type.
- **create any registry** under `src/qiyas_core/registries/` — no `ArabicMabniRegistry`, `ArabicMabniyatPilotRegistry`, etc.
- **open `SNAP-002`** (collision-handling sub-contract or instantiation).
- **open `SNAP-003`** (duplicate-handling sub-contract or instantiation).
- **open Track B** — no `GlyphClassificationEvidence` runtime / carrier / producer; no `SifatVector` runtime.
- **open Track C** — no `يَ` admission; no madd-variant admission; no alif (`ا`) variant semantics.
- **open Track D** — no maintainer-side runtime follow-up to PR #99.
- **perform source-side correction** (Saleh-side).
- **write to the upstream corpus** — Saleh has zero write access, reaffirmed in § 11.
- **introduce `Amil` runtime, `I'rāb` runtime, `AmilEffectEvidence`, or `I'rabEffectEvidence`**.
- **introduce `WordCandidate`**, `LafzCandidate`, `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`, `RealityClaim`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, or `OperatorGeometry`.
- **introduce `Glyph` runtime or `SifatVector` runtime**.
- **amend any predecessor contract** (PR #86 / PR #96 / PR #97 / PR #98 / PR #103 / PR #104 / PR #105 / PR #106 / PR #107).
- **edit `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md`** — PR #104's snapshot is frozen; used here only as a worked example, never edited.
- **engage PR #99** or any other unrelated PR.
- **promote source-side classification to Saleh-canonical** — PR #103 § 7(5) controls.
- **claim that mabniyat rows are approved by this policy**.
- **claim that any specific row is pilot-included**.
- **claim that Saleh solves Arabic mabniyat**.

## 17. Summary Table

| concept | policy status | pilot eligible by default? | requires reviewer note? | may affect runtime? | notes |
|---|---|---|---|---|---|
| explicit vocalized surface | **`pilot_eligible`** | **yes** | no | **no — never** | priority class 1; the natural admission candidate for the first mabniyat pilot |
| explicit unvocalized + vocalization evidence | **`pilot_eligible_with_reviewer_note`** | yes (with note) | **yes** | **no — never** | priority class 2; reviewer documents the vocalization reasoning |
| `title_used_as_surface_candidate` | **`ineligible_pending_review`** | no | **yes** | **no — never** | priority class 3; 23 prototype-flagged entries; § 7 governs |
| `weak_provenance` | **`ineligible_pending_review`** | no | **yes** | **no — never** | 124 prototype-flagged entries; § 8 governs; caution not error |
| example-derived candidate | **`ineligible_pending_review`** | no | **yes** | **no — never** | priority class 5; § 9 governs; `Example_Vocalized` never proof |
| category-label-only row | **`ineligible_blocked`** | no | n/a | **no — never** | priority class 6; no surface form |
| prose-description-only row | **`ineligible_blocked`** | no | n/a | **no — never** | priority class 7; `descriptive_not_surface` flag |
| multi-surface row | **`ineligible_pending_split_review`** | no | n/a (deferred) | **no — never** | priority class 8; awaits future split-review sub-contract |
| missing-surface row | **`ineligible_blocked`** | no | n/a | **no — never** | priority class 9; `no_surface_candidate` flag |
| `true_source_discrepancy` row | **`ineligible_blocked`** | no | n/a | **no — never** | reserved for PR #105 upstream resolution |
| future `/tmp/` review pack | **described only** | n/a | n/a | **no — never** | created by a separately-authorised review turn; never by this PR |
| future mabniyat pilot snapshot | **described only** | n/a | n/a | **no — never** | opened by a *separate* future PR, not by this PR |
| runtime registry | **explicitly excluded** | n/a | n/a | **no — never** | § 16 controls; standing § 9 non-goals also apply |

End of policy.
