# Legacy Proposal Runtime Consumption — Design Gate

> **Type:** Descriptive **design-gate note** — *not* a constitution and *not* an
> authorization. It introduces no new layer, no new theory name, and renames nothing.
> It is **subordinate** to `CLAUDE.md`, `PROJECT_MATHEMATICAL_FOUNDATION.md`,
> `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md`, `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md`,
> the canonical `LayerSpec` seed (`master_registry_seed.py`), and the landed P3.1/P5.1
> auxiliary passes + their legacy feeds (PR #186/#185/#187/#188). **Where this note and
> the canonical spec/code differ, the canonical spec/code wins.**
>
> **This note authorizes no runtime, registry, schema, data, or test change.** It emits
> no candidate. A **separate explicit authorization** is required before any runtime
> legacy-feed implementation work.

## 0. Constitutional Statements (binding; restated in full below)

- The legacy analyzer is a **proposer, never a Qiyas authority**.
- Legacy evidence may only ever become **proposal evidence**.
- **Qiyas rules still decide** ACCEPT / DEFER / BLOCK — the legacy never decides.
- **`suspicious_defer` and `unsafe_final_looking` must never ACCEPT.**
- The **P3.1 legacy root remains audit metadata only** — never passed as
  `external_root_letters`, never used to rewrite identity / the surface.
- **P5.1 ignores root/wazn.**
- **P3.1 ignores class / mabni-mu'rab.**
- **Both feeds ignore** role / case / i'rab / relations / events / resolution /
  meaning graph / Q&A / tafsir-facing outputs.
- **Registry count remains 19.** **No P13.** **P0–P12 untouched.** **P12 terminal.**
- **P3.1 and P5.1 remain auxiliary non-registry.**
- **Runtime remains unwired now**; Stage A remains **capture-only**; both legacy feeds
  remain **test-side only**. No Stage A fixture read at runtime; no external analyzer
  call at runtime. **Option D rejected; Option B not implemented; Option C preferred
  later** under a governed static-snapshot data contract. If ever authorized, the
  **P5.1 runtime feed comes before the P3.1 runtime feed.**

## 1. Status (what exists today, main @ 39b04f7)

- Two legacy → Qiyas proposal feeds are **MERGED and test-side only**:
  - **Legacy → P5.1** InflectionalClosure (PR #187, `850fa20`) — consumes class /
    closed-category / safe-verb-kind.
  - **Legacy → P3.1** WeightPattern (PR #188, `39b04f7`) — consumes root / wazn /
    weight-alignment / weak-shadda-hamza-madd ambiguity.
- Both live under `tests/qiyas_core/`, read **only** committed Stage A fixtures, make
  **no** analyzer / subprocess call, and are **not** imported by `src/qiyas_core` or
  `run_qiyas`. The Stage A guard (`test_LFH_10`) and the P3.1-feed guard
  (`test_WF_GOV_02`) enforce this.
- **Safety property in force:** *"Stage A is capture-only; the runtime never consumes
  legacy output."* No code path in `run_qiyas` reads a legacy proposal.
- Invariants intact: registry count **19**, no P13, P0–P12 untouched, **P12 terminal**,
  P3.1 + P5.1 remain **auxiliary non-registry** (registered only in
  `LAYER_FORBIDDEN_OUTPUTS` as `WeightPatternQiyas` / `InflectionalClosureQiyas`).

## 2. The Gate Question

**Should `run_qiyas` ever consume a legacy proposal feed at runtime — and if so, from
what source — without ending the "Stage A capture-only" safety property by accident?**

The legacy analyzer is, by constitution (`CLAUDE.md` §0, §3; foundation doc), an
**external proposer**, never an authority. Any runtime consumption must keep the legacy
output as *proposal evidence into a Qiyas rule*, with the rule — not the legacy — making
every ACCEPT / DEFER / BLOCK decision, and with suspicious/unsafe entries unable to
ACCEPT.

## 3. Options Compared

### Option A — Keep both feeds test-side only, permanently
- **Pros:** Maximum safety; reproducibility absolute; no external-source surface in
  runtime; "Stage A capture-only" never at risk; zero new attack/leakage surface.
- **Cons:** The legacy analyzer's proposal value (root/wazn/class hints) never reaches a
  live analysis; the bridges remain a validation artifact only; no path to using the
  legacy as a *real* upstream proposer.

### Option B — Runtime reads the committed Stage A fixtures directly
- **Pros:** Reproducible (fixtures are committed, NFC-clean, reviewed); no analyzer
  call; small diff.
- **Cons:** **Directly ends "Stage A capture-only"** — Stage A fixtures were admitted as
  *capture-only test data*, not as a runtime data source. Conflates a test fixture with
  a runtime contract; the 34-token set is illustrative, not a maintained runtime corpus;
  silently re-purposing it violates the property it was granted under.

### Option C — Runtime reads a **governed static proposal snapshot** (committed, reviewed)
- A snapshot is generated *offline* from the legacy analyzer, **manually reviewed**,
  NFC-normalized, identity-verified, and committed as a frozen `docs/`- or `data/`-side
  artifact under the existing `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` discipline
  (reserved form: `normalized-table`). Runtime reads only this snapshot.
- **Pros:** Reproducible and auditable (frozen, versioned, diffable); **no analyzer /
  subprocess at runtime**; keeps the snapshot distinct from Stage A test fixtures, so
  "Stage A capture-only" stays true; inherits an *existing* governance contract instead
  of inventing one; every row is human-reviewed before it can influence a verdict.
- **Cons:** Requires a snapshot-contract PR first (schema, provenance, review workflow);
  snapshot can drift from the live analyzer (acceptable — reproducibility > freshness);
  more upfront governance work.

### Option D — Runtime calls the external legacy analyzer directly (subprocess / import)
- **Pros:** Always-fresh proposals; no snapshot maintenance.
- **Cons:** **Rejected.** Violates reproducibility (output depends on an external,
  unversioned binary), external-source discipline (`CLAUDE.md` §3; snapshot policy §3),
  and the hard constraint "do not call the external analyzer / no subprocess in
  `run_qiyas`." Non-deterministic, non-auditable, breaks headless/CI runs, and makes the
  Qiyas verdict depend on code outside the constitutional authority order.

## 4. Recommendation

**Now:** keep runtime **unwired** — *Option A holds in practice* until a governed static
snapshot contract exists. **Later (only under separate authorization):** prefer
**Option C**. **Reject Option D** outright. **Do not** use Option B (it spends the
"Stage A capture-only" property for a convenience that Option C provides safely).

Sequencing: **P5.1 live feed should be authorized before P3.1 live feed** — see §8.

## 5. Allowed Evidence Families — *future* P5.1 runtime feed (Option C)

Consumable (closed-category / inflectional-closure readiness only):
- legacy **word-class as a closed-category hint**: HARF → harf/particle; ISM_MAWSOOL →
  relative; ISM_MABNI → pronoun/demonstrative; closed functional compound;
- legacy **verb-kind / tense as a mabni-vs-mu'rab signal** (past/imperative → mabni-lean;
  present → mu'rab-lean) — *kind*, **not** i'rab case;
- the **reliability tag** (proposal_evidence vs suspicious_defer) as an **input hint**.

The Qiyas P5.1 rule still decides; suspicious_defer never ACCEPTs.

## 6. Allowed Evidence Families — *future* P3.1 runtime feed (Option C)

Consumable (weight/root structural proposal only):
- legacy **root** as **audit/cross-check metadata** (recorded; **never** passed as a hard
  identity check / `external_root_letters`; never used to rewrite the surface);
- legacy **wazn** as a **weight-pattern hint** (P3.1 still aligns the preserved surface
  itself);
- **weak / hollow / hamza / shadda / madd ambiguity tags** as **defer hints**;
- the **reliability tag** as an **input hint**.

The Qiyas P3.1 rule still decides; weak/hollow/hamza/shadda/madd and any suspicious_defer
DEFER unless P3.1 independently licenses, and never ACCEPT from legacy evidence alone.

## 7. Forbidden Evidence Families (both feeds, runtime or test)

Never consumed; ignored or quarantined as raw context only:
- grammatical **role**; **case / i'rab** strings (فاعل مرفوع / مفعول به منصوب / اسم مجرور;
  marfū‘ / manṣūb / majrūr / majzūm);
- **relations** (agent_of / patient_of / jawab_shart_of); **events / tense-as-event /
  mood / speech-act**; **resolution / anaphora**;
- **meaning graph**; **reasoning / Q&A**; **tafsir / interpretation-facing output**;
- any **final-looking** legacy output (final root judgment, final wazn judgment,
  word-kind decision, i'rab decision, meaning) — downgraded to proposal evidence or
  ignored, flagged `unsafe_final_looking`, and **never** ACCEPT.

Cross-feed isolation also holds: the P3.1 feed ignores class/mabni-mu'rab; the P5.1 feed
ignores root/wazn.

## 8. Sequencing — P5.1 before P3.1

Authorize the **P5.1** live feed first because:
- its consumed evidence (closed-category membership) is **categorical and stable** —
  closed classes (ḥarf, pronoun, relative, demonstrative) change slowly and map cleanly;
- it is **further from morphological ambiguity** than P3.1, whose weak/hollow/hamza
  cases require the careful DEFER discipline already proven test-side;
- it gives one governed precedent (snapshot contract + runtime guard tests) that the
  P3.1 live feed can reuse before taking on the harder morphology surface.

## 9. Proposed Static-Snapshot Data Contract (Option C)

Bind to `EXTERNAL_SOURCE_SNAPSHOT_POLICY.md` (reserved form **`normalized-table`**) and
`EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md`. A snapshot row is a **frozen, reviewed,
NFC-clean** record — e.g.:

```
legacy_proposal_snapshot_v1 (one row per reviewed token)
  snapshot_version            # frozen version id; bumped only by a snapshot PR
  source_provenance           # legacy analyzer id + offline-run note (NOT a live call)
  surface_form_vocalized      # identity (مِنْ ≠ مَنْ); NFC-normalized
  surface_form_unvocalized_key# diagnostic only
  legacy_class                # closed-category hint (P5.1)
  legacy_verb_kind / tense    # mabni/mu'rab signal (P5.1) — kind, not case
  legacy_root                 # audit metadata (P3.1) — never identity check
  legacy_wazn                 # weight hint (P3.1)
  morphology_ambiguity_tags   # weak/hollow/hamza/shadda/madd (P3.1 defer hints)
  reliability_tag             # proposal_evidence | suspicious_defer
  unsafe_final_looking        # bool — flagged, never ACCEPT
  review_status               # manually_reviewed (required before runtime use)
```

Excluded columns by contract: role, case/i'rab, relations, events, meaning, reasoning,
Q&A, tafsir. The snapshot lives **outside** `tests/qiyas_core/legacy_fixtures/` so it
does not re-purpose Stage A. A runtime provider reads only this committed snapshot.

## 10. Required Tests Before *Any* Runtime Feed PR

1. **No analyzer / subprocess at runtime** — AST import-graph check on `run_qiyas` and
   any new runtime provider: no `import subprocess`, no `subprocess.run`, no analyzer-dir
   path. (Extends `test_WF_10` / `test_LF_12` to runtime modules.)
2. **Source is the governed snapshot, not Stage A** — runtime provider reads the
   committed snapshot path; a guard asserts it does **not** read
   `tests/qiyas_core/legacy_fixtures/` (so "Stage A capture-only" survives).
3. **Suspicious_defer never ACCEPTs at runtime** — parametrized over the snapshot.
4. **unsafe_final_looking never ACCEPTs**, only flagged.
5. **Forbidden families absent** — role/case/relation/event/meaning/Q&A/tafsir never
   reach the fed evidence dict (per-feed).
6. **Cross-feed isolation** — P3.1 runtime feed ignores class/mabni-mu'rab; P5.1 runtime
   feed ignores root/wazn.
7. **Qiyas makes the verdict** — accepted candidates carry the P3.1/P5.1
   `source_rule_id`, not a legacy id.
8. **No final-judgment leakage** — emitted types ⊆ {WeightPatternCandidate} /
   {Mabni/Mu'rabReadinessCandidate}; none of RootFinalJudgment / WeightFinalJudgment /
   word-kind / i'rab / case / meaning / dalalah / ifadah / hukm / truth / reality.
9. **Governance unchanged** — registry count 19, no P13, P0–P12 untouched, P12 terminal,
   P3.1 + P5.1 still auxiliary non-registry.
10. **Reproducibility** — same snapshot version → identical proposals (determinism).
11. **Existing suites stay green** — P3.1, P5.1, Stage A harness, both test-side feeds,
    full suite.

## 11. Risks

- **Accidental end of "Stage A capture-only"** — mitigated by Option C (snapshot ≠ Stage
  A) + Test 2.
- **Snapshot drift** — accepted; reproducibility outranks freshness; refresh only via a
  reviewed snapshot-bump PR.
- **Scope creep into forbidden families** — mitigated by §7 + Tests 5/6/8.
- **External-source discipline erosion** — mitigated by rejecting Option D and binding to
  the existing snapshot policy.
- **Identity rewrite via legacy root** — mitigated by keeping the P3.1 legacy root as
  audit metadata only (already the landed design).

## 12. Confirmation

This is a **docs-only design-gate note**. It makes **no** code, runtime, registry,
schema, data, or test change; calls **no** external analyzer; adds **no** LayerSpec;
keeps registry count **19**, **no** P13, P0–P12 untouched, P12 terminal, P3.1 + P5.1
auxiliary non-registry. Legacy output remains **proposal evidence only**.

## 13. Next Recommended PR (if any)

A **docs-only** *Legacy Proposal Snapshot Contract* PR (subordinate to
`EXTERNAL_SOURCE_SNAPSHOT_POLICY.md`) that freezes the row schema of §9 and the test
matrix of §10 — **still no runtime code**. Only after that contract lands should a
**separate** PR implement the **P5.1** runtime feed against a committed snapshot, with
the P3.1 runtime feed following as its own later PR. Each step requires explicit
authorization.
