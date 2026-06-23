# Legacy Proposal Snapshot Contract (Hussein Analyzer → Qiyas Proposal Evidence)

> **Type:** Constitutional **contract document** — docs-only. It introduces no new
> layer, no theory name, no rename, **no runtime code, no test, no data snapshot**.
> It is **subordinate** to `CLAUDE.md`, `PROJECT_MATHEMATICAL_FOUNDATION.md`,
> `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md`, `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md`,
> the canonical `LayerSpec` seed (`master_registry_seed.py`), and the landed P3.1/P5.1
> auxiliary passes + their test-side legacy feeds (PR #185/#186/#187/#188) and the P3.1
> runtime surface-binding fix (PR #190). **Where this contract and the canonical
> spec/code differ, the canonical spec/code wins.**
>
> **This contract authorizes no runtime wiring.** It is the **required bridge** that
> must exist *before* any future runtime consumption of legacy output. A separate
> explicit authorization is required for each subsequent step in §11.

## 0. Constitutional Statements (binding)

- The Hussein legacy analyzer is a **proposer, never a Qiyas authority**.
- Legacy output may only ever become **proposal evidence**.
- **Qiyas rules still decide** ACCEPT / DEFER / BLOCK.
- **`suspicious_defer` and `unsafe_final_looking` must never ACCEPT.**
- **No runtime wiring now.** No Stage A fixture read at runtime; no external analyzer
  call; no `subprocess` in Qiyas runtime.
- **No LayerSpec added.** Registry count **19**. **No P13.** **P0–P12 untouched.**
  **P12 terminal.** **P3.1 and P5.1 remain auxiliary non-registry.**
- **No final-judgment leakage** (no root/weight/word-kind/i'rab/case/relation/event/
  meaning/dalalah/ifadah/hukm/truth/reality output).

## 1. Snapshot Purpose

The snapshot is a **frozen, manually-reviewed, reproducible offline export** from the
Hussein analyzer, reproduced as a normalized table for archival + future proposal use.

It **is not**:
- the **live analyzer** (the analyzer is never invoked at Qiyas runtime);
- **Stage A fixture data** (`tests/qiyas_core/legacy_fixtures/` stays capture-only /
  test-only and is never read at runtime);
- a **Qiyas authority** (it never decides a verdict).

It **is**: a **proposal-evidence source only**, consumed — if ever — solely through the
landed P3.1/P5.1 adapters, which independently license, defer, or block.

## 2. Snapshot Location

Future governed path, **distinct from Stage A fixtures**:

```
data/external_snapshots/hussein_legacy_proposals/v1/
    snapshot.normalized-table.csv      # the reviewed rows (§3)
    MANIFEST.json                      # provenance + reproducibility (§9)
    REVIEW_LOG.md                      # per-row review status (§8)
```

It **must not** live under `tests/qiyas_core/legacy_fixtures/` — Stage A remains
capture-only/test-only, and the runtime provider (when later authorized) reads **only**
the `data/external_snapshots/...` path, never the Stage A path.

## 3. Required Row Schema (reserved `normalized-table` form)

One row per token / token-occurrence. Bound to `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md`
(NFC discipline) and `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` §12.1 vocalized-identity
discipline (`surface_form_vocalized` is identity; `مِنْ ≠ مَنْ`).

| column | role |
|---|---|
| `snapshot_version` | frozen version id; bumped only by a snapshot PR |
| `source_provenance` | free-text origin note (offline run, **not** a live call) |
| `analyzer_name` | constant `hussein` |
| `analyzer_version_or_commit` | analyzer build/commit identity |
| `offline_run_id` | id of the offline export run |
| `review_status` | one of §8 statuses |
| `reviewer` | reviewer identity |
| `reviewed_at` | review timestamp |
| `source_text_id` | corpus/text id the token came from |
| `token_index` | position within the source text |
| `surface_form_vocalized` | **identity** (NFC) |
| `surface_form_unvocalized_key` | diagnostic only |
| `normalized_surface_nfc` | NFC-normalized surface |
| `segmentation_hint` | structural segmentation note (not a decision) |
| `legacy_class` | analyzer word-class (closed-category hint for P5.1) |
| `legacy_subclass` | analyzer sub-type (hint only) |
| `legacy_verb_kind` | verb-kind signal (P5.1) |
| `legacy_verb_tense` | tense signal (P5.1 mabni/mu'rab lean) — kind, **not** i'rab |
| `legacy_root` | **audit metadata only** (P3.1) |
| `legacy_wazn` | weight hint (P3.1) |
| `morphology_ambiguity_tags` | weak/hollow/hamza/shadda/madd/deletion/assimilation (P3.1 defer hints) |
| `reliability_tag` | `proposal_evidence` \| `suspicious_defer` (gates trust) |
| `certainty_class` | legacy `Certificate` \| `Hypothesis` \| `Zero` (input hint only) |
| `unsafe_final_looking` | bool — flagged, never ACCEPT |
| `allowed_feed_targets` | subset of `{p3_1, p5_1}` this row may feed |
| `ignored_fields_summary` | which raw analyzer fields were dropped/quarantined |
| `quarantine_reason` | why a row/field is quarantined, if applicable |

## 4. Explicitly Forbidden Columns

The runtime snapshot **must not** contain any runtime-consumable column for:
grammatical **role**; **i'rab/case** strings (فاعل مرفوع / مفعول به منصوب / اسم مجرور;
marfū‘/manṣūb/majrūr/majzūm); **relations** (agent_of/patient_of/jawab_shart_of);
**events**; **speech-act**; **mood**; **resolution/anaphora**; **meaning graph**;
**reasoning/Q&A**; **tafsir-facing output**; **hukm**; **truth/reality**; **final
interpretation**.

If any of these exist in raw Hussein output, they are **omitted** from the runtime
snapshot, or retained **only** as ignored raw audit text (recorded in
`ignored_fields_summary` / `quarantine_reason`) — **never** as fed evidence.

## 5. P5.1 Feed Contract (future runtime)

**Allowed** into a future P5.1 runtime proposal feed (closed-category / inflectional-
closure readiness only):
- `legacy_class` as a **closed-category hint only**:
  - `HARF` → particle/harf hint;
  - `ISM_MAWSOOL` → relative hint;
  - `ISM_MABNI` → pronoun/demonstrative/closed-category hint;
  - `FIIL` past/imperative → **mabni-readiness** hint;
  - `FIIL` present → **mu'rab-readiness** hint;
- `legacy_verb_kind` / `legacy_verb_tense` (kind, **not** i'rab case);
- `reliability_tag`; `certainty_class`; `unsafe_final_looking` gate.

**Forbidden** for P5.1: `legacy_root`, `legacy_wazn`, role, case, relation, event,
meaning, Q&A, tafsir.

**P5.1 output only:** `InflectionalClosureCandidate`, `MabniReadinessCandidate`,
`Mu'rabReadinessCandidate`. **No** final `MabniJudgment` / `MurabJudgment`.

## 6. P3.1 Feed Contract (future runtime)

**Allowed** into a future P3.1 runtime proposal feed (weight/root structural proposal):
- `legacy_root` as **audit metadata only**;
- `legacy_wazn` as a **weight hint only**;
- `morphology_ambiguity_tags` for weak/hollow/hamza/shadda/madd/deletion/assimilation
  **defer hints**;
- `reliability_tag`; `certainty_class`; `unsafe_final_looking` gate.

**Forbidden** for P3.1: class / mabni-mu'rab / word-kind, role, case, relation, event,
meaning, Q&A, tafsir.

`legacy_root` must **never** be used as `external_root_letters`, as an identity rewrite,
or as a final root claim. **P3.1 aligns the preserved surface itself** (this is exactly
the discipline enforced by the landed test-side P3.1 feed and the PR #190 runtime
surface-binding fix).

**P3.1 output only:** `WeightPatternCandidate`. **No** `RootFinalJudgment` /
`WeightFinalJudgment`.

## 7. Reliability Policy

`reliability_tag` / `certainty_class` are **input hints**, never verdicts:

| tag | Qiyas behavior |
|---|---|
| `proposal_evidence` | ACCEPT-eligible **only if** the Qiyas adapter independently licenses it |
| `suspicious_defer` | **DEFER or quarantine — never ACCEPT** |
| `unsafe_final_looking` (true) | **ignore/quarantine — never ACCEPT** |
| unknown / missing | **DEFER** |
| contradiction | **BLOCK only if** Qiyas identity/fāriq logic independently blocks |

`certainty_class`: `Certificate` → ACCEPT-eligible (still subject to Qiyas licensing);
`Hypothesis` → normally DEFER; `Zero` → ignore/quarantine.

## 8. Review Policy

Every snapshot row is **manually reviewed before any runtime use**. Statuses:
`manually_reviewed`, `quarantined`, `rejected`, `pending_review`. **Only
`manually_reviewed` rows may be runtime-consumable**; all others are excluded from any
future feed.

## 9. Reproducibility Policy

The snapshot `MANIFEST.json` must record: **analyzer source**; **offline run command /
provenance**; **timestamp**; **source corpus/text id**; **snapshot version**; a
**checksum/digest** of the rows; and the aggregate **review status**. The runtime
**must never run the analyzer to refresh the snapshot** — refresh happens only via a new,
reviewed snapshot-version PR.

## 10. Test Matrix for Future Runtime Feed PRs

Required before *any* runtime feed implementation:
1. provider reads the **snapshot** path, asserted **not** Stage A fixtures;
2. **no subprocess / analyzer call** (AST import-graph guard on runtime modules);
3. **no forbidden field** (role/case/relation/event/meaning/Q&A/tafsir) reaches fed evidence;
4. **P5.1 ignores root/wazn**;
5. **P3.1 ignores class/mabni-mu'rab**;
6. **`suspicious_defer` never ACCEPTs**;
7. **`unsafe_final_looking` never ACCEPTs**;
8. **P3.1 root audit-only**, never `external_root_letters`;
9. **no final-judgment leakage** (output types ⊆ allowed candidate sets);
10. **registry count 19**; **no P13**; **P12 terminal**;
11. **P3.1 / P5.1 remain non-registry auxiliary**;
12. **runtime examples stable** (deterministic given a snapshot version);
13. **full suite green**.

## 11. Integration Roadmap (after this contract)

Intended sequence — **each a separate PR under separate explicit authorization**:

- **A. Docs-only Snapshot Contract PR** — *this document*.
- **B. Static snapshot data PR** — reviewed and committed under §2/§3/§8/§9; **no runtime
  use** (data-only).
- **C. P5.1 runtime provider PR** — reads the committed snapshot; honors §5 + §10.
- **D. P3.1 runtime provider PR** — reads the committed snapshot; honors §6 + §10.
- **E. Additional Hussein families** — only if **separately contracted**: derivation /
  jamid-mushtaq, roles, i'rab, relations, events, meaning graph.

**Hard boundary:** role / i'rab / relations / events / meaning each require **their own
future Qiyas layer contract** and **cannot be smuggled into P3.1 or P5.1**. P3.1 stays
weight-only; P5.1 stays inflectional-closure-only.

## 12. Confirmation

This is a **docs-only contract**. It makes **no** code, runtime, test, data-snapshot,
schema, or registry change; wires **no** legacy into `run_qiyas`; reads **no** Stage A
fixture at runtime; calls **no** external analyzer; uses **no** subprocess; adds **no**
LayerSpec. Registry count **19**, **no P13**, P0–P12 untouched, **P12 terminal**, P3.1 +
P5.1 auxiliary non-registry. Legacy output remains **proposal evidence only**.
