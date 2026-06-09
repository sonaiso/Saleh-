# Source Snapshot Collision Handling Contract

> **Status**: docs-only constitutional contract — **collision-class admission rules only**.
> **Authority**: extends `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) and binds `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97), `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105), `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #106), `ARABIC_MABNIYAT_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #107), `MABNIYAT_PILOT_SNAPSHOT_POLICY.md` (PR #108), `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 (Vocalized Source Identity Discipline), and `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 (`Example_Vocalized` discipline). Uses `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) as the worked precedent for how collision-class rows have been *excluded* until this contract lands.
> **Scope**: defines the constitutional shape under which a *future* `SNAP-NNN`-class instantiation PR may admit **collision-class rows** — rows whose `surface_form_unvocalized_key` collides with another row's but whose `surface_form_vocalized` identities are distinct. Reserved by PR #103 § 6, PR #103 § 10.2, PR #106 § 14.1, and PR #108 § 16.3 by name. Covers both the awamil/operators corpus (the 6 collision groups in `operators_catalog_split_vocalized.csv` excluded from SNAP-001) and any future mabniyat collision groups.
> **Non-Authority**: this contract is **rules only**. It does **NOT** instantiate any collision-class snapshot, does **NOT** admit any specific row, does **NOT** create an "Approved Rows" or "Approved Entries" table, does **NOT** create any file under `docs/qiyas_core/snapshots/`, does **NOT** modify any external source file, does **NOT** copy any source data into Saleh, does **NOT** create runtime / registry / test / fixture / data file, does **NOT** amend any predecessor contract, and does **NOT** open any specific `SNAP-NNN` instantiation PR.

---

## 1. Purpose

This contract codifies how a *future* docs-only snapshot PR may admit **collision-class rows** — rows that share an `unvocalized_key` with another row but carry **distinct `surface_form_vocalized` identities**. These rows were deliberately excluded from `SNAP-001` (PR #104 § 7) and from `MAB-001` (when the mabniyat pilot snapshot lands). PR #103 § 6 / § 10.2 explicitly reserved them for "a separate later snapshot under explicit collision-handling rules" — this contract is those rules.

The constitutional question is **not** whether collision-class rows are valid. PR #86 § 12.1 (Vocalized Source Identity Discipline) settles that: `مِنْ` (preposition, U+0645 U+0650 U+0646 U+0652) and `مَنْ` (conditional, U+0645 U+064E U+0646 U+0652) **are distinct constitutional identities** despite sharing the unvocalized skeleton `من`. The same applies to `إِنَّ` / `إِنْ`, `أَنَّ` / `أَنْ`, `ما` / `مَا`, `أي` / `أيَّ`, `إِذًا` / `إذا`, and to any future mabniyat collisions such as `ثُمَّ` / `ثَمَّ` (deferred from `MAB-001` per its § 7).

The constitutional question is *how* a snapshot admits both members of a collision pair as **distinct row entries** without ever collapsing them onto the shared unvocalized skeleton. This contract answers that question.

This contract is **docs-only**. It is **rules-only**. It does:

- NOT instantiate any snapshot;
- NOT admit any specific row;
- NOT create any "Approved Rows" table;
- NOT create any file under `docs/qiyas_core/snapshots/`;
- NOT copy or import any source data into Saleh;
- NOT create a runtime layer, adapter, producer, carrier, rule, evidence type, candidate type, registry, test, fixture, or data file;
- NOT change any existing contract;
- NOT modify `new_arabic_analyzer/`;
- NOT claim that collision-class rows are linguistically proven;
- NOT claim that Saleh "solves" Arabic homography.

## 2. Relationship to Predecessor Contracts

This contract sits *on top of* the predecessors below; it does not redefine, weaken, or override any of them.

| document | role | how this contract uses it |
|---|---|---|
| `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` (PR #97) § 15 | five reserved snapshot forms | this contract's future instantiations will use `normalized-table`, mirroring `SNAP-001` / `MAB-001` |
| `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) § 5 / § 6 / § 10.2 | inclusion rule that *excludes* `collision_member` rows; § 6 explicitly reserves them for "a separate later snapshot under explicit collision-handling rules" | this contract IS those rules |
| `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) | discrepancy reporting workflow | § 11 of this contract binds PR #105: a collision pair is NOT a discrepancy; it is a *legitimate distinct-identity case* |
| `ARABIC_AWAMIL_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #106) § 14.1 | awamil schema; § 14.1 explicitly reserves a SNAP-002 collision-handling sub-contract by name | this contract IS the sub-contract PR #106 § 14.1 named |
| `ARABIC_MABNIYAT_DETAILED_SOURCE_TABLE_CONTRACT.md` (PR #107) § 16.3 | mabniyat schema; § 16.3 reserves a duplicate/multi-surface handling sub-contract covering the broader cross-corpus collision concern | this contract covers the *collision* half of PR #107 § 16.3 (the *exact-duplicate / multi-role* half remains reserved for a future SNAP-003 sub-contract) |
| `MABNIYAT_PILOT_SNAPSHOT_POLICY.md` (PR #108) § 16.3 | mabniyat pilot policy; § 16.3 reserves the same cross-corpus collision concern | this contract is the cross-corpus answer; mabniyat collision groups discovered later (e.g. `ثُمَّ` / `ثَمَّ` deferred from MAB-001) admit under this contract's rules verbatim |
| `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline (`surface_form_vocalized` is identity; `مِنْ ≠ مَنْ`) | § 9 of this contract binds PR #86 § 12.1 verbatim; this contract is the *positive* admission path for collision pairs that PR #86 § 12.1 established as distinct identities |
| `LETTER_TRANSLITERATION_NAMING_CONTRACT.md` (PR #98) § 12.4 | `Example_Vocalized` is descriptive only | § 10 of this contract re-binds PR #98 § 12.4 verbatim |
| `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) | first docs-only snapshot under PR #103 | this contract uses PR #104 as the *worked precedent for exclusion* — § 7 / § 10 / § 11 of PR #104 list the collision pairs that were excluded; this contract is the positive admission path for those exclusions |

This contract does **not** amend any predecessor.

## 3. Why Collision-Class Rows Are Constitutional, Not Defective

This section is load-bearing. It must remain visible to every future reviewer.

A **collision-class row** is **not**:

- a defective source row;
- a `true_source_discrepancy` (those are governed by PR #105);
- an `exact_duplicate_surface` (those are reserved for SNAP-003);
- a `linkage_vowel_difference` (those are info-severity wasla shifts);
- a `partial_vocalization` (those need source-side completion);
- a runtime ambiguity that Saleh must resolve.

A **collision-class row** **is**:

- a row whose `surface_form_vocalized` is NFC and harakat-preserving;
- a row whose `surface_form_vocalized` is a **distinct constitutional identity** from every other row's `surface_form_vocalized` (per PR #86 § 12.1);
- a row that happens to **share an unvocalized skeleton** with at least one other row whose `surface_form_vocalized` is a *different* NFC string.

Classical Arabic is **rich in homographs that differ only by harakat**: `مِنْ` (preposition "from") vs `مَنْ` (interrogative / relative / conditional "who"); `إِنَّ` (emphatic particle) vs `إِنْ` (conditional particle); `أَنَّ` (emphatic complementizer) vs `أَنْ` (infinitival complementizer). These are *not* errors. They are the **vocalization-distinguished mabni surface inventory** that PR #86 § 5 / § 12.1 catalogues.

Their exclusion from `SNAP-001` was a **deliberate cycle-sequencing choice**, not a constitutional disqualification:

> *"They are NOT excluded because they are uncertain; they are excluded because the first snapshot deliberately defers the collision-handling shape."* — PR #103 § 6, second-to-last paragraph.

This contract opens that deferred shape.

## 4. Collision Class Definition

A row is a **collision-class member** if and only if **all** of the following hold:

1. The row's `identity_status` is `collision_member` (per PR #97 normalization output).
2. The row's `normalization_status` from the read-only prototype is `collision_member` (equivalently flagged with `collision_same_unvocalized_key` warning).
3. There exists at least one *other* row in the same source corpus (operators CSV or mabniyat JSON file) whose `surface_form_unvocalized_key` is NFC-equal to this row's AND whose `surface_form_vocalized` is NFC-distinct from this row's.
4. The row's own `surface_form_vocalized` is **unique** across the corpus (i.e., it is not also an `exact_duplicate_surface` — that case is reserved for SNAP-003).
5. The row is otherwise free of `block`-severity warnings: no `true_source_discrepancy`, no `descriptive_not_surface`, no `no_surface_candidate`, no `prose_label_in_operator_cell`.

A **collision pair** is the smallest collision group: two rows sharing an unvocalized skeleton with distinct vocalized identities. A **collision group** may have **three or more** members (e.g., a hypothetical future `أَنَّى` / `أَنَّا` / `أَنَّ` triple) — the rules below scale linearly.

## 5. Worked Examples — Descriptive Only

The following collision pairs were detected by the read-only prototype run that produced `/tmp/source_preview_operators.csv`. **These are descriptive observations from the source corpus, not admission decisions.** Listing them here cites *what the source contains*; it does not admit any specific row.

| `unvocalized_key` | member A (vocalized + codepoints) | member B (vocalized + codepoints) | source-side roles |
|---|---|---|---|
| `من` | `مِنْ` (U+0645 U+0650 U+0646 U+0652) | `مَنْ` (U+0645 U+064E U+0646 U+0652) | preposition (semantic) vs conditional/relative |
| `إن` | `إِنَّ` (U+0625 U+0650 U+0646 U+064E U+0651) | `إِنْ` (U+0625 U+0650 U+0646 U+0652) | emphasis vs conditional |
| `أن` | `أَنَّ` (U+0623 U+064E U+0646 U+064E U+0651) | `أَنْ` (U+0623 U+064E U+0646 U+0652) | emphasis vs infinitival |
| `ما` | `مَا` (U+0645 U+064E U+0627) | `ما` (U+0645 U+0627, no vocalization) | negation vs conditional |
| `أي` | `أيَّ` (U+0623 U+064A U+064E U+0651) | `أي` (U+0623 U+064A, no vocalization) | conditional vs vocative |
| `إذا` | `إِذًا` (U+0625 U+0650 U+0630 U+064B U+0627) | `إذا` (U+0625 U+0630 U+0627, no vocalization) | answer particle vs conditional |

Two of these pairs (`ما`, `أي`, `إذا`) include a member with **incomplete vocalization** at source (no harakat). Under this contract, a collision-class member with `partial_vocalization` is **NOT admissible** until source-side vocalization completion (per PR #103 § 8 / PR #108 § 10.2). Only collision pairs where *both* members carry full harakat at source qualify for admission.

A future mabniyat collision group `ثُمَّ` (conjunction "then", U+062B U+064F U+0645 U+0651 U+064E) vs `ثَمَّ` (adverb "there", U+062B U+064E U+0645 U+0651 U+064E), deferred from `MAB-001`, will admit under the same rules.

**These rows are NOT admitted by this contract.** A *separate*, *later*, *explicitly-authorised* `SNAP-NNN` instantiation PR (e.g. `SNAP-002`) is the place where specific rows are admitted, citing this contract as authority.

## 6. Per-Pair Handling Rule

A future `SNAP-NNN` instantiation PR opened under this contract admits a collision pair if and only if **all** of the following hold:

1. **Both members** of the pair are independently eligible per the relevant per-row schema contract (PR #106 § 14 for awamil; PR #107 § 14 for mabniyat). Specifically, each member must be priority class 1 (explicit vocalized surface field) AND `provenance_strength = strong_explicit_surface` AND have NFC harakat-preserving identity.
2. **Neither member** carries a `partial_vocalization` warning. A pair with one un-vocalized member is **NOT admissible** under this contract; defer until source-side completion.
3. **Neither member** carries `true_source_discrepancy`, `descriptive_not_surface`, `no_surface_candidate`, or `prose_label_in_operator_cell` warnings.
4. **Neither member** is referenced by an `awaiting_upstream` finding under PR #105.
5. **Both members** are admitted **together** in the same snapshot. A future `SNAP-NNN` MAY NOT admit one member of a pair without admitting the other (admitting only one would conceal the collision and risk downstream consumers treating the unvocalized skeleton as the identity).
6. **A reviewer attestation** is recorded in the snapshot's Manual Approval section (per § 12) explicitly acknowledging the collision pair as a pair, with both vocalized identities listed verbatim. Silent admission of a collision pair without attestation is forbidden.

If a collision **group** has three or more members, the rule is identical: all members are admitted together, or none.

## 7. Dual-Row Table Format

A future `SNAP-NNN` instantiation under this contract MUST present each collision pair as **a single block of two contiguous rows** in the snapshot's "Approved Rows" table, with the following column shape (specialised from PR #104 § 10 for the operators case; same shape for mabniyat):

| Snapshot ID | `surface_form_vocalized` | `unv_key` (diagnostic) | codepoints | source-side classification | collision group |
|---|---|---|---|---|---|
| SNAP-NNN-X | member A's vocalized form | shared unv_key | A's codepoints | A's source-side role | `collision_group:{unv_key}` |
| SNAP-NNN-X+1 | member B's vocalized form | shared unv_key | B's codepoints | B's source-side role | `collision_group:{unv_key}` |

The `collision group` column is **mandatory** for collision-class snapshots. It groups paired rows visually so a human reviewer cannot miss them. The column value is the literal string `collision_group:{unv_key}` — e.g., `collision_group:من` for the `مِنْ` / `مَنْ` pair.

The `unv_key` column appears in this format because diagnostic visibility is the entire point of a collision-class snapshot: human reviewers must see at a glance that two distinct vocalized identities share the same skeleton. Downstream consumers MUST NEVER use the `unv_key` column as identity (PR #86 § 12.1 verbatim).

Snapshot IDs MAY be assigned sequentially across collision groups (e.g., the `من` pair = SNAP-002-001 + SNAP-002-002; the `إن` pair = SNAP-002-003 + SNAP-002-004; etc.). The IDs are bookkeeping handles; identity remains `surface_form_vocalized`.

## 8. Forbidden Actions

A future `SNAP-NNN` instantiation under this contract MUST NOT:

1. **Merge two collision pair members into one row** by stripping harakat. This is the cardinal sin. The whole point of this contract is to admit both vocalized identities as distinct rows. A snapshot that lists `من` (no harakat) and claims it covers "both senses" is **constitutionally invalid**.
2. **Use `surface_form_unvocalized_key` as identity** at any level — not for de-duplication, not for grouping (other than the visual `collision_group:` column above), not for lookup. PR #86 § 12.1 verbatim.
3. **Admit only one member of a pair**. Both members admit together, or neither.
4. **Silently include a `partial_vocalization` collision member** without first cycling it through PR #105's upstream completion workflow.
5. **Treat the source's grammatical-purpose labels as identity-distinguishing.** The source's purpose column (e.g., "للتوكيد" vs "للشرط") is descriptive context, not constitutional identity. Identity remains `surface_form_vocalized`.
6. **Promote the source's role labels to Saleh-canonical** (per PR #103 § 7(5)). The source's "preposition" / "conditional" / "interrogative" labels are *source-side classification*, recorded verbatim, never promoted.
7. **Include an `Approved Rows` entry whose `surface_form_vocalized` lacks any harakat** (other than for rows where the source-side row genuinely has no harakat AND a reviewer attestation explicitly documents the un-vocalized status as the source's chosen surface form, which would be unusual for collision-class admission).
8. **Reorder collision pair members** between admission and re-snapshot. If `مِنْ` is SNAP-002-001 and `مَنْ` is SNAP-002-002, that ordering is frozen for the lifetime of SNAP-002.
9. **Bundle a collision-class snapshot with a non-collision snapshot** in a single PR.
10. **Open a future SNAP-NNN collision instantiation without citing this contract by name** in its Policy Authority section.

## 9. Identity Discipline

This contract re-binds PR #86 § 12.1 verbatim, plus PR #103 § 7 and PR #108 § 10:

1. **`surface_form_vocalized` is identity.** Two rows have the same identity if and only if their NFC `surface_form_vocalized` strings are codepoint-equal.
2. **`surface_form_unvocalized_key` is diagnostic only.** It MAY appear in collision snapshot tables (in fact, this contract makes its appearance mandatory for visibility) but MUST NEVER be used as identity, lookup, or comparison basis.
3. **Distinct vocalized identities sharing an unvocalized skeleton are *distinct*.** `مِنْ ≠ مَنْ`. `إِنَّ ≠ إِنْ`. `أَنَّ ≠ أَنْ`. `ثُمَّ ≠ ثَمَّ`. The constitutional treatment is: both admitted, both labelled `collision_group:{unv_key}`, both retained as separate rows forever.
4. **NFC normalization is mandatory** at admission time.
5. **Harakat are identity-relevant.** A snapshot NEVER strips harakat to compress identity.
6. **Length and source-side classification labels are not identity.** Two collision pair members may have the same Arabic-letter count; identity is `surface_form_vocalized`.

## 10. `Example_Vocalized` Discipline

This contract re-binds PR #98 § 12.4 verbatim. The source-side `Example_Vocalized` (operators) or `example_sentence` / `examples` (mabniyat) field is **descriptive only**. It MAY appear in a collision-class snapshot's reference column for human review (e.g., to show that `مِنْ` is illustrated by `سِرْتُ مِنَ الْبَيْتِ` and `مَنْ` by `مَنْ يَرْحَمْ يُرْحَمْ`). It MUST NEVER be:

- proof of anything;
- a test fixture (without a separate explicitly-authorised fixture contract);
- runtime input to any Saleh layer;
- i'rāb evidence;
- Amil-effect evidence;
- role proof;
- the basis for distinguishing collision pair members (the *vocalization on the operator itself* is the distinction; the example sentence is illustration);
- hukm / dalalah / meaning derivation evidence.

For collision-class snapshots specifically: where the source `Example_Vocalized` cells for two collision pair members exhibit a `linkage_vowel_difference` from the operator's isolated form (e.g., `مِنْ` becoming `مِنَ` before `الـ`), the snapshot records the difference as a *source-side observation*, never as a constitutional claim about the identity. PR #105 § 3.1 governs.

## 11. Discrepancy Integration

This contract binds `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) by citation.

A collision pair is **not** a discrepancy. PR #105's `true_source_discrepancy` covers the case where the source's `Operator` cell and `Example_Vocalized` cell contradict each other at the consonant-skeleton level (e.g., R-001's `لام الأمر` prose label vs `لِيَنْصُرْ` literal). A collision pair is the opposite case: the source has *two correct rows*, each with its own internally-consistent surface form, that happen to share an unvocalized skeleton.

If a collision pair member has *also* triggered a PR #105 finding (e.g., R-NNN where one cell contradicts itself), the member is **NOT admissible** under this contract until the PR #105 finding is closed via upstream resolution. The collision-handling rules and the discrepancy workflow stack: a row must pass both gates.

If new mabniyat collision groups generate `R-NNN` findings (because, e.g., one cell of the pair has a `true_source_discrepancy`), the finding is processed under PR #105 first; only the cleanly-classified rows feed into any future `SNAP-NNN` collision instantiation.

## 12. Saleh-Side / Upstream-Side Boundary

This contract reaffirms PR #105 § 9 verbatim:

> Saleh has zero write access to `new_arabic_analyzer/`. A row that is wrong stays wrong until the upstream maintainer fixes it. Saleh never silently corrects a discrepancy. The boundary is not crossable.

Specifically for collision-class admission:

1. **Saleh does not "fix" a collision** by editing the upstream source. The source's two rows remain as the source has them; Saleh admits both into the snapshot as distinct identities.
2. **Saleh does not adjudicate** which source-side classification (e.g., the source's "preposition" vs "conditional" label) is more accurate. Both classifications are recorded verbatim as source-side context, never as constitutional truth.
3. **No JSON or CSV file** is copied into Saleh by this contract or by any future `SNAP-NNN` instantiation under it. The future snapshot file (under `docs/qiyas_core/snapshots/`) contains a normalized-table view of the admitted rows, not the source file itself.
4. **No source-side data is modified.** If the source CSV is later updated upstream (e.g., the `ما` collision member's missing harakat get added), the next prototype run observes the change and a *new* `SNAP-NNN` ID becomes possible. The previous snapshot remains frozen (PR #103 § 12).

## 13. Reviewer Attestation Requirements

A future `SNAP-NNN` instantiation under this contract MUST include in its Manual Approval section (mirroring PR #104 § 5 for the SNAP-001 precedent) an explicit, verbatim attestation by the maintainer covering:

1. **Every collision pair** (or larger group) admitted, listed by `collision_group:{unv_key}` with both members' `surface_form_vocalized` written out verbatim.
2. **A statement that the maintainer reviewed each pair as a pair**, not member-by-member in isolation.
3. **A statement that the maintainer affirms the two (or more) members are distinct constitutional identities** per PR #86 § 12.1.
4. **A statement that no collision pair member is being silently merged with its sibling** by the snapshot.
5. **A timestamp and reviewer name** (`Hussein Hiyassat`, by default).
6. **A reference to the read-only prototype run** that produced the collision detection (e.g., `/tmp/source_preview_operators.csv` for awamil, `/tmp/source_preview_mabniyat.csv` for mabniyat).
7. **An explicit acknowledgement that this contract was cited as authority.**

The reviewer attestation cannot be filled in by an assistant on the maintainer's behalf. If the maintainer's per-pair affirmation is missing from the future SNAP-NNN PR body, the future PR is constitutionally invalid and must be rolled back.

## 14. Future SNAP-NNN Operators Instantiation PR Shape

A future operators-collision-class snapshot instantiation PR opened under this contract would have approximately the following shape (described, not opened):

- **Title pattern**: `docs(qiyas_core): add SNAP-002 operators collision-class snapshot`.
- **Single new file** under `docs/qiyas_core/snapshots/`, e.g. `SNAP-002_OPERATORS_COLLISION_CLASS_SNAPSHOT.md`.
- **Mirrors PR #104 SNAP-001 structural template** (14 mandatory sections) plus the dual-row table format of § 7 above plus the reviewer attestation requirements of § 13 above.
- **Cites this contract by name** plus PR #103, PR #106, PR #105, PR #86 § 12.1, PR #98 § 12.4, PR #104 (as the worked precedent for exclusion).
- **Admits the awamil collision pairs** that satisfy § 6 of this contract. From the read-only prototype run's 6 detected groups, the **constitutionally-admissible subset** (after the `partial_vocalization` exclusion of § 6.2) is the **3 fully-voweled pairs**: `مِنْ`/`مَنْ`, `إِنَّ`/`إِنْ`, `أَنَّ`/`أَنْ` (6 rows total). The remaining 3 detected groups (`ما`, `أي`, `إذا`) contain members with `partial_vocalization` and are **deferred to source-side completion**.
- **Carries the dual-row Approved Rows table** required by § 7.
- **Includes the per-pair reviewer attestation** required by § 13.
- **Estimated diff size**: ~200–350 lines.
- **Explicit "Do not merge until Hussein explicitly asks"** in the merge instruction.
- **Opens ONLY after explicit per-PR authorisation** in a separate turn.
- **Still docs-only**. No `src/`, no `tests/`, no `data/`, no registry, no runtime change.

This PR is NOT opened by this contract. The above is a forward-binding shape description, not an open action.

## 15. Future Mabniyat Collision Handling Hook

The same rules apply verbatim to any future mabniyat collision groups. The `ثُمَّ` / `ثَمَّ` pair deferred from `MAB-001` (when it lands) is the first known mabniyat collision candidate. A future mabniyat collision-class snapshot instantiation PR (e.g., MAB-002 or a dedicated `MAB_COLLISION_001`) opened under this contract would mirror the operators case:

- single new file under `docs/qiyas_core/snapshots/`;
- dual-row table per pair;
- reviewer attestation per pair;
- cites this contract + PR #107 + PR #108 + PR #105 + PR #86 § 12.1 + PR #98 § 12.4.

The expected first mabniyat collision admission is a single pair (`ثُمَّ`/`ثَمَّ` from `built_in_adverbs.json`), 2 rows total.

No mabniyat collision PR is opened by this contract.

## 16. Non-Goals

This contract explicitly does NOT:

- **instantiate any snapshot** — § 14 / § 15 describe future shapes; none is opened.
- **admit any specific row** — the worked examples in § 5 are descriptive observations of source content, not admission decisions.
- **create any file under `docs/qiyas_core/snapshots/`** — the future instantiation PRs do that.
- **create any "Approved Rows" or "Approved Entries" table** — none appears in this contract; the table shape of § 7 is a *specification*, not a populated table.
- **modify the external source corpus** — Saleh has zero write access.
- **silently correct any discrepancy** — PR #105 governs.
- **adjudicate which source-side classification is correct** in any collision pair.
- **promote source-side classification to Saleh-canonical**.
- **create any runtime layer**, adapter, producer, carrier, rule, evidence type, or candidate type.
- **create any registry** under `src/qiyas_core/registries/`.
- **create any test or fixture** under `tests/`.
- **import any data** — no source file is copied from `new_arabic_analyzer/` into Saleh.
- **use `Example_Vocalized` / `example_sentence` as proof or runtime input** — PR #98 § 12.4 / PR #108 § 9 control.
- **open Track B**, Track C, or Track D.
- **introduce `AmilEffectEvidence`**, `I'rabEffectEvidence`, `WordCandidate`, `LafzCandidate`, `DalalahCandidate`, `FinalMeaning`, `HukmCandidate`, `RealityClaim`, `SentenceGeometry`, `DiscourseGeometry`, `TextGeometry`, or `OperatorGeometry`.
- **introduce `Amil` runtime, `I'rāb` runtime, `Glyph` runtime, or `SifatVector` runtime**.
- **perform source-side correction**.
- **write to the upstream corpus**.
- **amend any predecessor contract**.
- **edit any existing snapshot under `docs/qiyas_core/snapshots/`** — SNAP-001 is frozen.
- **engage PR #99** or any other unrelated PR.
- **claim that homography is "solved" by Saleh**.
- **claim that collision admission is a final grammatical adjudication**.

## 17. Summary Table

| concept | status in this contract | may admit rows? | requires reviewer attestation per pair? | may affect runtime? | notes |
|---|---|---|---|---|---|
| collision-class definition | **rules only** | no | n/a | **no — never** | § 4 |
| collision pair | preserved as **two distinct rows** | not by this contract | yes (per § 13) | **no — never** | both members admit together or neither |
| collision group (3+ members) | same rules; all members admit together | not by this contract | yes | **no — never** | § 6 scales linearly |
| `unvocalized_key` | **diagnostic only** | n/a | n/a | **no — never** | mandatory display column in collision snapshots; never identity |
| `surface_form_vocalized` | **identity** | n/a (rules layer) | n/a | **no — never** | PR #86 § 12.1 binding |
| source-side classification | **source-side label, recorded verbatim** | n/a | n/a | **no — never** | never promoted to Saleh-canonical (PR #103 § 7(5)) |
| `Example_Vocalized` / `example_sentence` | **descriptive only** | n/a | n/a | **no — never** | PR #98 § 12.4 verbatim |
| `partial_vocalization` collision member | **NOT admissible** under § 6.2 | no | n/a | **no — never** | defer until source-side vocalization completion |
| `true_source_discrepancy` collision member | **NOT admissible** until PR #105 resolution | no | n/a | **no — never** | PR #105 stacks with this contract |
| future operators collision snapshot | **described in § 14** | not by this contract | yes | **no — never** | future PR; ~3 fully-voweled pairs admissible (مِنْ/مَنْ + إِنَّ/إِنْ + أَنَّ/أَنْ) |
| future mabniyat collision snapshot | **described in § 15** | not by this contract | yes | **no — never** | future PR; first known candidate: ثُمَّ/ثَمَّ from MAB-001 deferral |
| runtime registry | **explicitly excluded** | n/a | n/a | **no — never** | § 16 controls |

End of contract.
