# Hussein Legacy Proposal Snapshot — v1 (MANIFEST)

> **Governed artifact** under `docs/qiyas_core/LEGACY_PROPOSAL_SNAPSHOT_CONTRACT.md`.
> As of **Step C** it is read at runtime **only** by the authorized
> `hussein_snapshot_provider` and **only** to feed P5.1 InflectionalClosure. It is **NOT
> a Qiyas authority** and is distinct from Stage A fixtures
> (`tests/qiyas_core/legacy_fixtures/`), which stay capture-only and are never read at
> runtime. The Hussein analyzer is a **proposer only**; Qiyas P3.1/P5.1 rules decide
> ACCEPT/DEFER/BLOCK. This snapshot is **proposal evidence only**.

## Provenance & reproducibility
- **analyzer_name:** hussein
- **analyzer_version_or_commit:** analyze_verse_v3.py (commit unknown; offline --morph --i3rab capture)
- **offline_run_id:** stage_a_capture/words_morph_i3rab
- **source_provenance:** captured from /Users/husseinhiyassat/fractal/hussein/clean_code/analyze_verse_v3.py --morph --i3rab (read-only, verbatim)
- **source_text_id:** stage_a/words_morph_i3rab.raw.txt
- **produced_by:** offline transform of the Stage A reviewed capture — **no live analyzer call**
- **reviewed_at:** 2026-06-24 · **reviewer:** maintainer (Stage A verbatim review)
- **snapshot_file:** `hussein_legacy_proposals_v1.csv`
- **sha256:** `e50498d20290537fee1fb92414bde691fb16aa065676a84c81d09b7e5e58ec97`
- Runtime must **never** run the analyzer to refresh this snapshot; a refresh is a new
  reviewed snapshot-version PR.

## Row counts
| metric | value |
|---|---|
| rows | 26 |
| manually_reviewed | 23 |
| quarantined | 3 |
| rejected | 0 |
| pending_review | 0 |
| P5.1-target rows | 23 |
| P3.1-target rows | 12 |
| suspicious_defer | 9 |
| unsafe_final_looking | 26 |

## Consumable columns by target (contract §5/§6)
- **P5_1_INFLECTIONAL_CLOSURE:** legacy_class, legacy_subclass, legacy_verb_kind,
  legacy_verb_tense, reliability_tag, certainty_class, unsafe_final_looking.
  *(never root/wazn)*
- **P3_1_WEIGHT_PATTERN:** legacy_root (**audit metadata only — never external_root_letters,
  never identity rewrite, never final root**), legacy_wazn (hint), morphology_ambiguity_tags,
  reliability_tag, certainty_class, unsafe_final_looking. *(never class/mabni-mu'rab/word-kind)*

## Policy notes
- **reliability_tag** is collapsed conservatively: `proposal_evidence` only when **every**
  consumed family (word_class for P5.1, root_wazn for P3.1) is reliable; otherwise
  `suspicious_defer`. `suspicious_defer` and `unsafe_final_looking` **never ACCEPT** —
  ACCEPT-eligibility requires the Qiyas adapter to license independently.
- **unsafe_final_looking = true** on every row flags the legacy i'rab/role output, which is
  recorded only in `ignored_fields_summary` and **never fed**. The safe fed families
  (class / root-audit / wazn) are explicitly safe after manual review.
- **Forbidden families** (role, i'rab/case, relations, events, speech-act, mood,
  resolution, meaning, Q&A, tafsir, hukm, truth/reality, final interpretation) appear in
  **no consumable column** — only inside `ignored_fields_summary` / `quarantine_reason`.
- **Quarantined rows** (empty allowed_feed_targets): بَاعَ, صَامَ (legacy misclassified the
  hollow verb as ISM_MUARAB), مكتوب (legacy root متوب is a misread of the unvocalized surface).
- **Seed spelling note:** committed fixture spellings are used verbatim — e.g. `هو` (not
  هُوَ), and both `مَكْتُوب` (vocalized) and `مكتوب` (unvocalized) appear as distinct rows.
- **list cells** use `|` as separator.

## Status
The CSV rows are immutable and byte-identical to the Step B (PR #192) commit (sha256
above unchanged). As of **Step C**, the snapshot is consumed at runtime by the authorized
`hussein_snapshot_provider` for **P5.1 only** (no LayerSpec, no `run_qiyas` registry/schema
change, no P3.1 wiring). Registry count 19; no P13; P12 terminal; P3.1/P5.1 auxiliary
non-registry. Stage A is never read at runtime.
Next step (separate authorization): **D — P3.1 runtime provider PR against this snapshot**.
