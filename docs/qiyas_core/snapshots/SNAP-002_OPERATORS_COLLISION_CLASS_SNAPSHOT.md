# SNAP-002 Operators Collision-Class Snapshot

> **Type**: documentation snapshot only.
> **Status**: explicitly maintainer-attested collision-class subset (3 pairs / 6 rows).
> **Authority**: `docs/qiyas_core/SOURCE_SNAPSHOT_COLLISION_HANDLING_CONTRACT.md` (PR #112).
> **Non-Authority**: this file is **NOT** runtime, **NOT** registry, **NOT** data, **NOT** fixture, **NOT** a source correction. It does **NOT** admit any row into Saleh runtime, registries, tests, fixtures, or data files. It does **NOT** copy source CSV/JSON into Saleh. It does **NOT** modify `new_arabic_analyzer/`.

---

## 1. Purpose

`SNAP-002` records the **explicitly maintainer-attested** collision-class subset derived from the read-only normalization prototype at `/tmp/source_preview_operators.csv`. It is the positive admission path for the collision_member rows that PR #103 § 6 / § 10.2 reserved for "a separate later snapshot under explicit collision-handling rules" and that PR #104 SNAP-001 § 7 / § 11 explicitly excluded.

This snapshot exists to make three things explicit:

1. The **6 rows** (3 collision pairs) that the maintainer manually attested for SNAP-002 admission under PR #112 § 13 (verbatim attestation preserved at `/tmp/snap002_maintainer_attestation_2026-06-09.md`).
2. The constitutional shape under which collision pairs are admitted as **distinct** vocalized identities — both members admitted **together**, never silently merged on the shared unvocalized skeleton.
3. The boundary of what this snapshot does and does not authorise — strictly docs-only, strictly identity-preserving, strictly subordinate to PR #112 and the predecessor policies it binds.

This snapshot is **docs-only**. It is **not runtime**. It is **not registry**. It is **not** a source correction. It does **not** create or license any `Amil` / `I'rāb` / `Word` / `Lafz` / `Dalalah` / `Meaning` / `Hukm` / `Reality` / `SentenceGeometry` / `DiscourseGeometry` / `TextGeometry` / `OperatorGeometry` / `AmilEffectEvidence` / `I'rabEffectEvidence` artefact, runtime layer, evidence, candidate, registry, or test fixture. A future runtime layer wishing to consume operator collision data must be opened in a separate, explicitly-authorised PR cycle under its own constitutional review; it is **not** implied by, nor licensed by, this snapshot.

## 2. Authority Chain

This snapshot is admitted under, and bound by, the following documents in their merged form on `main`. It does not amend any of them.

| document | role |
|---|---|
| `docs/qiyas_core/ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md` (PR #86) § 12 / § 12.1 | Vocalized Source Identity Discipline — `surface_form_vocalized` is identity carrier; `surface_form_unvocalized_key` is diagnostic only; `مِنْ ≠ مَنْ`; `إِنَّ ≠ إِنْ`; `أَنَّ ≠ أَنْ` |
| `docs/qiyas_core/EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (PR #103) § 5 / § 6 / § 7 / § 10.2 | external-source snapshot policy; § 6 / § 10.2 reserved `collision_member` rows "for a separate later snapshot under explicit collision-handling rules" — SNAP-002 is that snapshot |
| `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` (PR #104) | first docs-only snapshot — the **worked precedent for exclusion** of these 3 pairs (see PR #104 § 7 / § 11 / § 13 item 1); SNAP-002 is the worked precedent for **admission** |
| `docs/qiyas_core/SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) | discrepancy reporting workflow — a collision pair is **not** a discrepancy; the 3 deferred `partial_vocalization` groups (§ 8 below) route through this workflow upstream |
| `docs/qiyas_core/SOURCE_SNAPSHOT_COLLISION_HANDLING_CONTRACT.md` (PR #112) | rules layer for collision-class admission — § 4 collision-class definition, § 6 per-pair handling rule, § 7 dual-row table format, § 8 forbidden actions, § 9 identity discipline, § 10 `Example_Vocalized` discipline, § 12 Saleh-side / upstream-side boundary, § 13 reviewer attestation requirements; SNAP-002 is the first instantiation under this contract |
| `/tmp/snap002_maintainer_attestation_2026-06-09.md` | verbatim maintainer attestation (Hussein Hiyassat, 2026-06-09); satisfies all 7 PR #112 § 13 attestation requirements; preserved at `/tmp` for audit, **not committed to the Saleh repo** |
| `/tmp/source_preview_operators.csv` | read-only prototype output from PR #97 normalization; each admitted row's `surface_form_vocalized` / codepoints / source row number / source-side classification / warning codes drawn verbatim from this file; **not committed to the Saleh repo** |

This snapshot inherits all rules from the above verbatim. Where a sentence in this document could be read as conflicting with any of the above, the authority document controls.

## 3. Why This Snapshot Exists

Classical Arabic is rich in homographs that differ only by harakat. The collision pairs admitted here — `مِنْ` / `مَنْ`, `إِنَّ` / `إِنْ`, `أَنَّ` / `أَنْ` — share an unvocalized diagnostic skeleton (`من`, `إن`, `أن` respectively) but carry **constitutionally distinct vocalized identities** per PR #86 § 12.1.

A collision pair is **not** an error. It is **not** a `true_source_discrepancy` (those are governed by PR #105). It is **not** an `exact_duplicate_surface` (those are reserved for SNAP-003). It is **not** a runtime ambiguity that Saleh must resolve. It is the vocalization-distinguished mabni surface inventory that PR #86 § 5 / § 12.1 catalogues.

Their exclusion from SNAP-001 was a **deliberate cycle-sequencing choice**, not a constitutional disqualification. PR #103 § 6 reserved them for "a separate later snapshot under explicit collision-handling rules". PR #112 wrote those rules. SNAP-002 is the first instantiation that admits the constitutionally-admissible subset.

The admission preserves both members **as separate rows forever**. The shared unvocalized skeleton appears in the `surface_form_unvocalized_key` column for diagnostic visibility per PR #112 § 7 / § 9.2 — never as identity, never as lookup, never as comparison basis.

## 4. Identity Discipline

This snapshot is bound verbatim by the identity discipline of PR #86 § 12.1 + PR #97 + PR #98 § 12.4 + PR #103 § 7 + PR #112 § 9.

- **`surface_form_vocalized` is the identity carrier.** It is the only identity carrier. Two rows are the same identity if and only if their NFC `surface_form_vocalized` strings are codepoint-equal.
- **`surface_form_unvocalized_key` is diagnostic only.** It appears in the table of § 6 for collision-class visibility — that visibility is the entire point of a collision-class snapshot per PR #112 § 7. It MUST NOT be used as identity, lookup, or comparison basis.
- **Shared unvocalized key does not collapse identity.** Two rows with the same `surface_form_unvocalized_key` but distinct `surface_form_vocalized` strings are *distinct* identities, never merged. This is the cardinal rule of collision-class admission per PR #112 § 8.1.
- **`مِنْ ≠ مَنْ`** — `مِنْ` (U+0645 U+0650 U+0646 U+0652) and `مَنْ` (U+0645 U+064E U+0646 U+0652) are distinct constitutional identities. The kasra-vs-fatha distinction on the م is identity-relevant.
- **`إِنَّ ≠ إِنْ`** — `إِنَّ` (U+0625 U+0650 U+0646 U+064E U+0651) and `إِنْ` (U+0625 U+0650 U+0646 U+0652) are distinct constitutional identities. The fatha+shadda-vs-sukun distinction on the ن is identity-relevant.
- **`أَنَّ ≠ أَنْ`** — `أَنَّ` (U+0623 U+064E U+0646 U+064E U+0651) and `أَنْ` (U+0623 U+064E U+0646 U+0652) are distinct constitutional identities. The fatha+shadda-vs-sukun distinction on the ن is identity-relevant.
- **NFC normalization is mandatory.** Every `surface_form_vocalized` value below is NFC-normalized at admission time.
- **Harakat are identity-relevant.** This snapshot never strips harakat to compress identity.
- **Source-side classification labels are not identity.** The source's `purpose_usage` field (e.g., "للتوكيد" vs "للشرط") is descriptive context, never the basis for distinguishing pair members. The distinction is the vocalization on the operator itself.

## 5. Maintainer Attestation

The 6 rows below are admitted because **Hussein Hiyassat explicitly attested the three pairs** in `/tmp/snap002_maintainer_attestation_2026-06-09.md` on **2026-06-09** under PR #112 § 13. The attestation satisfies all 7 of § 13's requirements (conformance verified in the audit file's "Conformance Check Against PR #112 § 13's 7 Requirements" table).

The attestation language for each admitted pair:

- **Pair 1 — `collision_group: من`** (`مِنْ` + `مَنْ`): *"I affirm that these are constitutionally distinct vocalized identities under PR #86 § 12.1. The shared unvocalized diagnostic key does not collapse identity. `surface_form_vocalized` remains the identity carrier, and `surface_form_unvocalized_key` remains diagnostic only."* — **Reviewer decision: `include_pair_in_snap002`**.
- **Pair 2 — `collision_group: إن`** (`إِنَّ` + `إِنْ`): same attestation language, same reviewer decision **`include_pair_in_snap002`**.
- **Pair 3 — `collision_group: أن`** (`أَنَّ` + `أَنْ`): same attestation language, same reviewer decision **`include_pair_in_snap002`**.

Each pair was **reviewed as a pair**, not member-by-member in isolation, per the attestation's opening clause: *"I explicitly review the following collision candidates as pairs, not as isolated member rows."*

No transitive approval is implied: the attestation explicitly says *"This attestation authorizes only a future docs-only SNAP-002 planning or instantiation step for the three listed fully vocalized operator pairs. It does not authorize runtime, registry, fixture creation, source correction, SNAP-003, MAB-001, Track B, Track C, or Track D."*

The verbatim attestation text is preserved at `/tmp/snap002_maintainer_attestation_2026-06-09.md` (8.8 KB). It is not reproduced inline here to keep this snapshot at readable length; the `/tmp` file is the binary-precise reference.

**No assistant approval is claimed.** The assistant did **not** approve any row. Every `reviewer_decision: include_pair_in_snap002` in § 6 derives from the maintainer's verbatim attestation, not from assistant judgment. This codifies the PR #112 § 13 lesson from the rolled-back MAB-001 attempt.

## 6. Snapshot Rows

The 6 admitted rows below derive **verbatim** from `/tmp/source_preview_operators.csv` (source row numbers refer to row positions in the source CSV: header is row 1; data rows start at row 2). The dual-row block format per PR #112 § 7 places each pair as two contiguous rows.

| snap_id | collision_group | surface_form_vocalized | surface_form_unvocalized_key | source_family | inclusion_basis | reviewer_decision | identity_note | runtime_status |
|---|---|---|---|---|---|---|---|---|
| SNAP-002-001 | `collision_group:من` | `مِنْ` | `من` (diagnostic) | source row 3, group 1 (الجر فقط الدلالية / Prepositions Only — Semantic); source `purpose_usage`: للدلالة على ابتداء الغاية الزمنية | maintainer_attested_pair | include_pair_in_snap002 | distinct vocalized identity per PR #86 § 12.1; kasra (U+0650) on م + sukun (U+0652) on ن; codepoints U+0645 U+0650 U+0646 U+0652; sibling is SNAP-002-002; **harakat preserved** | not_runtime |
| SNAP-002-002 | `collision_group:من` | `مَنْ` | `من` (diagnostic) | source row 45, group 7 (الشرط الجازمة فقط / Conditional — Jussive Only); source `purpose_usage`: للشرط | maintainer_attested_pair | include_pair_in_snap002 | distinct vocalized identity per PR #86 § 12.1; fatha (U+064E) on م + sukun (U+0652) on ن; codepoints U+0645 U+064E U+0646 U+0652; sibling is SNAP-002-001; **harakat preserved** | not_runtime |
| SNAP-002-003 | `collision_group:إن` | `إِنَّ` | `إن` (diagnostic) | source row 21, group 2 (التوكيد / Emphasis and Wishing — Grammatical); source `purpose_usage`: للتوكيد | maintainer_attested_pair | include_pair_in_snap002 | distinct vocalized identity per PR #86 § 12.1; kasra (U+0650) on إ + fatha (U+064E) + shadda (U+0651) on ن; codepoints U+0625 U+0650 U+0646 U+064E U+0651; sibling is SNAP-002-004; **harakat preserved** | not_runtime |
| SNAP-002-004 | `collision_group:إن` | `إِنْ` | `إن` (diagnostic) | source row 44, group 6 (الجزم فقط النافية والشرطية / Jussive Only — Negating and Conditional); source `purpose_usage`: للشرط | maintainer_attested_pair | include_pair_in_snap002 | distinct vocalized identity per PR #86 § 12.1; kasra (U+0650) on إ + sukun (U+0652) on ن; codepoints U+0625 U+0650 U+0646 U+0652; sibling is SNAP-002-003; **harakat preserved** | not_runtime |
| SNAP-002-005 | `collision_group:أن` | `أَنَّ` | `أن` (diagnostic) | source row 22, group 2 (التوكيد / Emphasis and Wishing — Grammatical); source `purpose_usage`: للتوكيد | maintainer_attested_pair | include_pair_in_snap002 | distinct vocalized identity per PR #86 § 12.1; fatha (U+064E) on أ + fatha (U+064E) + shadda (U+0651) on ن; codepoints U+0623 U+064E U+0646 U+064E U+0651; sibling is SNAP-002-006; **harakat preserved** | not_runtime |
| SNAP-002-006 | `collision_group:أن` | `أَنْ` | `أن` (diagnostic) | source row 36, group 5 (أداة نصب ومصدر / Accusative Only — Purposive and Negating); source `purpose_usage`: للمصدرية | maintainer_attested_pair | include_pair_in_snap002 | distinct vocalized identity per PR #86 § 12.1; fatha (U+064E) on أ + sukun (U+0652) on ن; codepoints U+0623 U+064E U+0646 U+0652; sibling is SNAP-002-005; **harakat preserved** | not_runtime |

**Per-pair admission summary**: 3 pairs × 2 members = 6 rows. No row admits in isolation; each pair is admitted together per PR #112 § 6.5. The `surface_form_unvocalized_key` column appears for diagnostic visibility per PR #112 § 7 / § 9.2 and **MUST NEVER** be used as identity by any downstream consumer.

**Per-row eligibility verification** against PR #112 § 6 (6 conditions × 3 pairs = 18 checks; all PASS): documented in `/tmp/snap002_review_pack.md` § 3 verbatim. Each pair satisfies § 6.1 (priority class 1, `strong_explicit_surface`, NFC), § 6.2 (neither member carries `partial_vocalization`), § 6.3 (neither carries a § 6.3-blocking warning), § 6.4 (neither referenced by an `awaiting_upstream` PR #105 finding), § 6.5 (both members admitted together), § 6.6 (reviewer attestation recorded per § 5 above).

## 7. Collision Pair Notes

One note per admitted pair.

### Pair 1 — `مِنْ` / `مَنْ` (`collision_group:من`)

The pair shares the diagnostic unvocalized skeleton `من` (U+0645 U+0646). Their `surface_form_vocalized` strings are distinct: `مِنْ` carries kasra (U+0650) on م and is the **preposition** (للدلالة على ابتداء الغاية الزمنية, per source row 3); `مَنْ` carries fatha (U+064E) on م and is the **conditional / relative / interrogative** particle (للشرط, per source row 45). Both readings are constitutionally licensed by PR #86 § 12.1 as distinct identities.

**Linkage-vowel note (source-side observation per PR #105 § 3.1)**: the source's `Example_Vocalized` cell for `مِنْ` shows `سِرْتُ مِنَ الْبَيْتِ` — the kasra-on-م shifts to fatha (`مِنَ`) before the wasla-headed `الْبَيْتِ`. This is the `linkage_vowel_difference` info-level warning recorded by the prototype on source row 3. It is **not** a blocking warning per PR #112 § 6.3, and the snapshot records it here as a **source-side observation, never as a constitutional claim about identity**. The identity of `مِنْ` remains its isolated NFC form (U+0645 U+0650 U+0646 U+0652); the wasla shift is a phonological observation of the source's example sentence, not part of the operator's identity. PR #105 § 3.1 governs.

### Pair 2 — `إِنَّ` / `إِنْ` (`collision_group:إن`)

The pair shares the diagnostic unvocalized skeleton `إن` (U+0625 U+0646). Their `surface_form_vocalized` strings are distinct: `إِنَّ` carries kasra (U+0650) on إ and fatha+shadda (U+064E U+0651) on ن and is the **emphasis particle** (للتوكيد, per source row 21, member of النواسخ); `إِنْ` carries kasra (U+0650) on إ and sukun (U+0652) on ن and is the **conditional particle** (للشرط, per source row 44, member of jussive-only particles). Both readings are constitutionally licensed by PR #86 § 12.1.

No `linkage_vowel_difference` warning is recorded on either member.

### Pair 3 — `أَنَّ` / `أَنْ` (`collision_group:أن`)

The pair shares the diagnostic unvocalized skeleton `أن` (U+0623 U+0646). Their `surface_form_vocalized` strings are distinct: `أَنَّ` carries fatha (U+064E) on أ and fatha+shadda (U+064E U+0651) on ن and is the **emphatic complementizer** (للتوكيد, per source row 22, member of النواسخ); `أَنْ` carries fatha (U+064E) on أ and sukun (U+0652) on ن and is the **infinitival complementizer / مصدرية** (للمصدرية, per source row 36, member of accusative-only particles). Both readings are constitutionally licensed by PR #86 § 12.1.

No `linkage_vowel_difference` warning is recorded on either member.

## 8. Deferred Collision Groups

The following collision groups detected by the read-only prototype are **NOT admitted** by SNAP-002 and remain reserved for source-side completion under PR #105's discrepancy / completion workflow. They appear here **only as deferred**.

| collision_group | members detected by prototype | reason for deferral |
|---|---|---|
| `ما` | source row 27 `مَا` (U+0645 U+064E U+0627) + source row 46 `ما` (U+0645 U+0627, no harakat) | PR #112 § 6.2 — row 46 carries `partial_vocalization`; the pair is NOT admissible until source-side vocalization completion |
| `أي` | source row 34 `أي` (U+0623 U+064A) + source row 47 `أيَّ` (U+0623 U+064A U+064E U+0651) | PR #112 § 6.2 — both members carry `partial_vocalization` (alif-maqsurah end is unvocalized in both); the pair is NOT admissible until source-side completion |
| `إذا` | source row 39 `إِذًا` (U+0625 U+0650 U+0630 U+064B U+0627) + source row 55 `إذا` (U+0625 U+0630 U+0627, no harakat) | PR #112 § 6.2 — row 55 carries `partial_vocalization`; the pair is NOT admissible until source-side vocalization completion |

The maintainer attestation explicitly excludes these three groups: *"I do not authorize admission of the deferred partial-vocalization groups: ما, أي, إذا. Those remain deferred to source-side completion / discrepancy workflow under PR #105 and the PR #112 collision-handling contract."*

Per PR #112 § 12.4: if the source CSV is later updated upstream to add the missing harakat in `new_arabic_analyzer/data/operators_catalog_split_vocalized.csv`, the next read-only prototype run will observe the change. A separate, new, explicitly-authorised future SNAP-NNN PR could then admit them under PR #112's rules. **SNAP-002 itself remains frozen and is never amended retroactively** per PR #103 § 12.

The deferred groups are listed here as bookkeeping artefacts only:

- `ما` — deferred (partial_vocalization in `ما` row 46)
- `أي` — deferred (partial_vocalization in both members)
- `إذا` — deferred (partial_vocalization in `إذا` row 55)

## 9. Source Discrepancy / Completion Boundary

This snapshot binds `SOURCE_DISCREPANCY_REPORTING_CONTRACT.md` (PR #105) verbatim.

A collision pair is **not** a discrepancy. PR #105 § 3.1's `true_source_discrepancy` covers the case where one source cell contradicts another at the consonant-skeleton level (e.g., R-001's `لام الأمر` prose label vs `لِيَنْصُرْ` literal). A collision pair is the opposite case: the source has *two correct rows*, each internally consistent, that happen to share an unvocalized skeleton.

**Saleh-side / upstream-side boundary** (PR #105 § 9 + PR #112 § 12 verbatim):

> Saleh has zero write access to `new_arabic_analyzer/`. A row that is wrong stays wrong until the upstream maintainer fixes it. Saleh never silently corrects a discrepancy. The boundary is not crossable.

Specifically for SNAP-002:

1. Saleh does **not** "fix" the collision. Both vocalized identities are admitted as distinct rows; the source's two rows remain as the source has them.
2. Saleh does **not** adjudicate which source-side classification (e.g., the source's "preposition" vs "conditional" label) is more accurate. Both classifications are recorded verbatim as source-side context, never promoted to Saleh-canonical per PR #103 § 7(5) + PR #112 § 8.6.
3. **No JSON or CSV file** is copied into Saleh by this snapshot. The 6 rows above are a normalized-table view per PR #97 § 15, not a copy of the source file.
4. **No source-side data is modified** by this snapshot. The 3 deferred `partial_vocalization` groups (§ 8) route through PR #105's upstream completion workflow — Saleh reports; upstream completes.
5. If a future PR #105 finding identifies an `R-NNN` issue on any of the 6 admitted rows, the stack-of-gates rule of PR #112 § 11 applies: the row must pass **both** the collision-handling gate (PR #112 § 6) AND the PR #105 discrepancy gate before continuing to count as cleanly admitted. If a finding lands, the row's admission status here is re-examined under PR #105 first.

## 10. Runtime Boundary

This snapshot is **docs-only**. Explicitly:

- **no runtime admission** — no row above is a runtime input to any Saleh layer.
- **no registry** — no `ArabicOperatorRegistry`, `ArabicPrepositionRegistry`, `ArabicCollisionRegistry`, `ArabicAmilRegistry`, `ArabicMabniRegistry`, or any other registry is created or modified by this snapshot.
- **no fixture** — no test fixture under `tests/` consumes any row above.
- **no MIU change** — no change to `tests/qiyas_core/test_variant_resolver_miu_integration.py` or to any other MIU-related test, registry, or rule.
- **no resolver change** — no change to `ArabicVariantResolver`, `GlyphClassificationGate`, `SifatVector`, or any other existing Saleh runtime component.
- **no semantic / hukm / reality / dalalah claim** — this snapshot does NOT introduce or license `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `SentenceGeometry` / `DiscourseGeometry` / `TextGeometry` / `OperatorGeometry` / `AmilEffectEvidence` / `I'rabEffectEvidence`.
- **no `Example_Vocalized` as proof** — the source-side `Example_Vocalized` field (and its linkage-vowel `مِنَ` shift on Pair 1) is descriptive observation only, never proof, never i'rāb evidence, never test fixture, never runtime input. PR #98 § 12.4 + PR #112 § 10 verbatim.
- **no automatic consumption** of snapshot rows by `MIU`, `ArabicVariantResolver`, `GlyphClassificationGate`, `SifatVector`, or any other existing Saleh runtime component.

A future runtime layer wishing to consume operator collision data must be opened in a separate, explicitly-authorised PR cycle under its own constitutional review. It is **not** implied by, nor licensed by, this snapshot.

## 11. Non-Goals

This snapshot explicitly does **NOT**:

- open **SNAP-003** (exact-duplicate-surface collision class, reserved by PR #107 § 16.3 — separate future cycle);
- open **MAB-001** (mabniyat pilot snapshot — still requires its own per-row attestation per PR #108 § 14);
- open **Track B** (Glyph / SifatVector runtime), **Track C** (`يَ` admission / madd / alif variants), or **Track D** (PR #99 follow-up);
- perform any **source correction** — Saleh has zero write access to `new_arabic_analyzer/` per PR #105 § 9;
- admit any **partial-vocalization** member of any collision group — § 8 lists `ما`, `أي`, `إذا` as deferred until source-side completion;
- create any **runtime layer**, adapter, producer, carrier, rule, evidence type, or candidate type;
- create any **registry** under `src/qiyas_core/registries/`;
- create or modify any **test** or **fixture** under `tests/`;
- introduce **`WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim`** or any sentence / discourse / text geometry layer;
- introduce **`Amil` / `I'rāb` / `Glyph` / `SifatVector` runtime**;
- **amend** PR #86 / PR #97 / PR #98 / PR #103 / PR #104 / PR #105 / PR #106 / PR #107 / PR #108 / PR #112;
- **edit** `docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md` — SNAP-001 is frozen per PR #103 § 12;
- **copy** `operators_catalog_split_vocalized.csv` or any other CSV / JSON from `new_arabic_analyzer/` into Saleh;
- **modify** `new_arabic_analyzer/` (Saleh has zero write access);
- **promote** the source's role labels ("preposition" / "conditional" / "emphasis" / "infinitival") to Saleh-canonical per PR #103 § 7(5) + PR #112 § 8.6;
- claim that homography is "solved" by Saleh;
- claim that collision admission is a final grammatical adjudication.

## 12. Validation Expectations

The following validation commands are the expected post-merge baseline. **None are run by this snapshot** (this is a docs-only snapshot); they are listed here as the validation contract for the merge cycle that will follow on a separate explicit directive.

**Expected validation commands and outcomes:**

```bash
git diff --name-only main...HEAD
# → docs/qiyas_core/snapshots/SNAP-002_OPERATORS_COLLISION_CLASS_SNAPSHOT.md   (single file)

PYTHONPATH=src:. python3 /tmp/check_current_qiyas_state.py "بِ ضَ وَ يَ ضَرَبَ"
# → CURRENT QIYAS STATE CHECK: PASS

PYTHONPATH=src:. python3 -m pytest tests/qiyas_core/test_variant_resolver_miu_integration.py -q
# → 17 passed

PYTHONPATH=src:. python3 -m pytest tests/qiyas_core -q
# → 1086 passed, 4 skipped   (matches the post-PR-#112 baseline; no regression — this PR adds zero test/runtime impact)
```

**Expected grep checks** (all PASS):

- `grep -n "مِنْ"` → present (Pair 1 member A + § 4 identity discipline mentions)
- `grep -n "مَنْ"` → present (Pair 1 member B)
- `grep -n "إِنَّ"` → present (Pair 2 member A)
- `grep -n "إِنْ"` → present (Pair 2 member B)
- `grep -n "أَنَّ"` → present (Pair 3 member A)
- `grep -n "أَنْ"` → present (Pair 3 member B)
- `grep -n "include_pair_in_snap002"` → present (6 hits, one per admitted row + § 5 attestation summary)
- `grep -n "not_runtime"` → present (6 hits, one per admitted row's `runtime_status`)
- `grep -n "ما"` → present **only in deferred context** (§ 8)
- `grep -n "أي"` → present **only in deferred context** (§ 8)
- `grep -n "إذا"` → present **only in deferred context** (§ 8)

**Test impact**: zero — docs-only PR.

## 13. Summary

| question | answer |
|---|---|
| Snapshot ID | **SNAP-002** |
| Authority | PR #112 (collision-handling contract) + maintainer attestation 2026-06-09 |
| Approved pairs | **3** (`مِنْ`/`مَنْ`, `إِنَّ`/`إِنْ`, `أَنَّ`/`أَنْ`) |
| Approved rows | **6** (3 pairs × 2 members; admitted together per PR #112 § 6.5) |
| Deferred groups | **3** (`ما`, `أي`, `إذا`) — all due to `partial_vocalization` (PR #112 § 6.2) |
| Source kind | `operators_csv` |
| Identity key | `surface_form_vocalized` |
| `surface_form_unvocalized_key` | diagnostic only — visible for collision-class clarity per PR #112 § 7; **never** identity |
| Approval status | **Manually attested per-pair by Hussein Hiyassat on 2026-06-09** (verbatim attestation at `/tmp/snap002_maintainer_attestation_2026-06-09.md`) |
| `runtime_status` | **`not_runtime`** for every admitted row |
| `inclusion_basis` | **`maintainer_attested_pair`** for every admitted row |
| `reviewer_decision` | **`include_pair_in_snap002`** for every admitted row |
| Source correction performed? | **No** — Saleh has zero write access to `new_arabic_analyzer/` per PR #105 § 9 + PR #112 § 12 |
| Is `Example_Vocalized` proof? | **No** — descriptive only per PR #98 § 12.4 + PR #112 § 10 |
| Does this create a registry? | **No** |
| Does this create a runtime layer? | **No** |
| Does this create a test or fixture? | **No** |
| Does this open SNAP-003 / MAB-001 / Track B/C/D? | **No** — each remains a separate explicit cycle |
| Does this amend any predecessor contract? | **No** |
| Frozen? | **Yes** — SNAP-002 is frozen at merge per PR #103 § 12; any future source-side change produces a new SNAP-NNN, not an amendment |

End of snapshot.
