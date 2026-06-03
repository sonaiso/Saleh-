# PR_SCHEDULING_POLICY

> **Status:** Constitutional. Docs-only ratification of the
> Saleh/Qiyas pull-request scheduling and batching policy. No code,
> no tests, no implementation are changed by this PR.
>
> **Authority basis:**
> `CLAUDE.md` §0 / §1 / §12 / §13 / §14 / §19,
> `RESET_CONSTITUTION.md` §1 / §3 / §4,
> `LAYER_CONTRACT_CONSTITUTION.md` §2.1 / §2.2,
> `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` §12 / §13,
> `MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` §1 / §12,
> `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` §6 / §8,
> `MICRO_PR_GOVERNANCE_FIX_SUMMARY.md`,
> `AGENT_PR_CHECKLIST.md`.
>
> **Governing one-liners:**
>
> ```
> One PR carries one constitutional purpose, not many.
> A PR is split when constitutional safety would otherwise blur.
> A PR is batched when one purpose would otherwise be fragmented.
> ```
>
> ```
> الـPR الواحد يحمل غرضًا دستوريًا واحدًا، لا أغراضًا متعددة.
> ويُقسَّم إذا كان دمج التغييرات يُذيب الأمان الدستوري.
> ويُجمَّع إذا كان تقسيم التغييرات يُفتت غرضًا واحدًا.
> ```

---

## 0. Purpose

This document fixes the policy by which Saleh/Qiyas contributions are
scheduled as pull requests. The policy answers three questions:

```text
1. Should this change be one PR or many?
2. If many, may any of them be stacked?
3. In what order may the PRs merge into main?
```

The policy exists because both extremes are unsafe:

- A **single mega-PR** that mixes a constitutional contract change
  with implementation changes with experimental cleanup makes review
  impossible and violates the "contract before implementation"
  principle of `RESET_CONSTITUTION.md` §1.
- A **fragmented avalanche** of one-line PRs for every micro-decision
  hides the constitutional intent behind the noise, breaks review
  context, and produces ambiguous merge order.

The policy below is the binding equilibrium between those two
extremes. Every PR opened against this repository must declare which
category it belongs to, satisfy that category's constraints, and
respect the merge-order rules of §8.

This document does **not** itself implement any scheduling tooling,
gating, CI check, or bot. It is a docs-only policy that humans and
human-supervised agents must follow.

---

## 1. PR Categories

Every PR opened against the Saleh/Qiyas repository must declare its
category. The categories are exhaustive: a PR that fits none of
them must be re-scoped until it fits one.

### 1.1 Constitutional Contract PR

**Definition.** A PR that adds or amends a constitutional document
under `docs/qiyas_core/` and changes nothing else.

**Inclusions.**

- A new `*_CONSTITUTION.md` or `*_CONTRACT.md` document.
- A scoped amendment to an existing constitutional document.
- A correspondence table or terminology pin (e.g., `TERMINOLOGY_MAP.md`).

**Exclusions.**

- Any change under `src/qiyas_core/`, `tests/qiyas_core/`,
  `experimental/`, or `run_qiyas.py`.
- Any new code symbol, new rule, new evidence claim, or new
  candidate type.

**Examples.** `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Z1),
`RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` (PR #48),
`MINIMAL_COMPLETE_CLOSURE_CONTRACT.md` (PR #50).

**Constraint.** Implementation may not begin until the controlling
contract PR is merged.

### 1.2 Micro Safety PR

**Definition.** A PR that closes exactly one narrowly-scoped
constitutional safety gap (declassification of dead code,
forbidden-output annotation, residual-preservation invariant, etc.)
inside a single canonical layer.

**Inclusions.**

- Editing at most ~10 small surfaces inside one layer's adapter,
  rules, and adjacent tests.
- Adding tests that pin the safety invariant being closed.

**Exclusions.**

- Any change in any other layer.
- Any new rule, candidate type, or evidence shape.
- Any wiring change in `run_qiyas.py`.

**Example.** Z4 (PR #46) — `chore(qiyas_core): declassify unreachable
BoundaryCodePoint paths` — six files in one layer family, no driver
change, no new rule.

**Constraint.** Must include a PR body that names the constitutional
basis (`CLAUDE.md` §, `*_CONSTITUTION.md` §) being closed and the
non-goals being preserved.

### 1.3 Batch Implementation PR

**Definition.** A PR that implements a single constitutional purpose
inside a single layer (or a strictly contiguous layer pair), bundling
all the changes that together constitute the purpose: adapter +
rules + tests + driver wiring if the purpose requires it.

**Inclusions.**

- All changes required by the single purpose, **with their tests
  in the same PR**.

**Exclusions.**

- A second, unrelated purpose in the same PR.
- A change to a layer whose contract has not yet been merged.
- A change that spans two layer boundaries.

**Example.** Z5 (PR #47) — `feat(run_qiyas): route whitespace and
boundary context through tokenizer` — driver wiring (`run_qiyas.py`)
plus all 13 new pipeline tests in `test_run_qiyas_pipeline.py`,
shipped together because they are one purpose.

**Constraint.** Tests are not a separate PR from the implementation
they validate.

### 1.4 Data Registry PR

**Definition.** A PR that introduces or amends an external data
registry — a JSON/CSV/TOML/etc. file consumed *as data* (not as
algebra) — plus its derived artifacts, its reader, and its tests,
all together.

**Inclusions.**

- Source data file (e.g., `data/arbic-alphabet.csv`).
- Derived registry artifact (e.g.,
  `data/arabic_articulation_registry.json`).
- Reader / loader module if the registry needs one.
- Tests pinning the registry schema and the non-Qiyas posture.

**Exclusions.**

- Any rule, adapter, or kernel surface that elevates the registry
  to a `Candidate` source.
- Any field that promotes registry metadata to identity, alignment,
  or licensing evidence inside the qiyas chain.

**Constraint.** The registry must declare its constitutional posture
in its own payload (see existing
`data/arabic_articulation_registry.json`'s
`constitutional_role: "external_data_registry_only"` and
`constitutional_constraints` block as the canonical pattern). The
registry produces no `Candidate`, uses no `QiyasRule`, and does not
license transitions by itself.

**Example.** The `data/arabic_articulation_registry.json` registry —
source CSV, derived JSON, and any reader/tests belong in **one PR**,
not three.

### 1.5 Stacked Dependency PR

**Definition.** A PR opened on top of another non-yet-merged PR, in
a strict linear chain where each PR is itself one of the categories
above, and each depends on its predecessor being merged first.

**Inclusions.**

- A clearly-stated base branch (`base:` field of the PR) pointing
  at the immediate predecessor.
- An explicit merge order in the PR body.

**Exclusions.**

- A branching stack (two PRs both stacked on the same base, both
  unmerged): forbidden, because no clean linear merge order exists.
- A stack whose predecessor is itself unscoped or speculative.

**Example.** Z1 → Z2 → Z3 → Z4 → Z5 (PRs #44/#45/#46/#47/#49 in
their final form). Each was itself either a Constitutional Contract
PR (Z1), a Micro Safety PR (Z4), or a Batch Implementation PR (Z2 /
Z3 / Z5).

**Constraint.** Stack depth must stay ≤ 3 unmerged PRs at any
time. Deeper stacks indicate that an earlier PR should have merged
already, or that the work was not actually a stack.

### 1.6 Experimental Cleanup PR

**Definition.** A PR that touches only files under `experimental/`,
intended to keep that tree internally coherent without affecting
the canonical pipeline.

**Inclusions.**

- Any rename, refactor, or documentation change inside
  `experimental/` only.
- Tests under `experimental/tests/` that remain non-canonical.

**Exclusions.**

- Any change under `src/qiyas_core/`, `tests/qiyas_core/`,
  `docs/qiyas_core/`, or `run_qiyas.py`.
- Any change that promotes experimental material into canonical
  status.

**Example.** A future PR that renames legacy fixtures inside
`experimental/qiyas_core/` for terminology consistency, with no
touch to canonical material.

**Constraint.** The PR body must explicitly state "no canonical
material is changed" and the reviewer must verify that statement
against the diff.

---

## 2. When to Split PRs

Split a PR when **any** of the following five triggers applies:

1. **Layer boundary crossing.** The change touches two or more
   layers (e.g., `TypedCodePointClassificationQiyas` *and*
   `ConditionedTypedSequenceQiyas`) for distinct reasons. Each
   layer's change is its own PR.

2. **Kernel invariants in play.** The change touches `QiyasKernel`,
   `EvidenceSet`, `CandidateSet`, `Residual`, `Trace`, or any
   septet primitive
   (`Candidate → Gate → Evidence → Domain → Rank → Residuals →
   Trace`, `LAYER_CONTRACT_CONSTITUTION.md` §2.1). Kernel changes
   are isolated by category.

3. **Candidate safety surface.** The change touches the
   `output_flags` machinery, the `CandidateOnly` invariant, or
   `forbidden_outputs` (`src/qiyas_core/forbidden_outputs.py`).
   Even small-looking edits to these surfaces are isolated, because
   they govern CLAUDE.md §4 invariants 9–10.

4. **Forbidden-outputs delta.** Adding to or removing from
   `FORBIDDEN_*` tuples is itself a constitutional-policy change.
   The forbidden-outputs delta is its own PR and may not be folded
   into a feature PR.

5. **Constitutional contract delta.** Any text change in a
   `*_CONSTITUTION.md` / `*_CONTRACT.md` document is a
   **Constitutional Contract PR** (§1.1) and may not be bundled
   with implementation.

The five triggers are conjunctive in effect, disjunctive in
detection: any one of them, by itself, forces a split. Triggers may
co-occur — in which case the split happens once, with each isolated
PR landing first.

---

## 3. When to Batch PRs

Batch a PR — i.e., keep changes together rather than splitting them
— when **all** of the following four conditions hold:

1. **Same purpose.** The changes serve one constitutional purpose
   that can be stated in a single sentence.
2. **Same layer (or strictly contiguous layer pair).** The changes
   are inside one canonical layer, or — in a Batch Implementation
   PR — the strictly contiguous adapter-and-driver pair required to
   wire that layer's contract through to `run_qiyas.py`.
3. **Low risk.** No change crosses a kernel invariant (§2 trigger 2),
   the Candidate safety surface (§2 trigger 3), or the forbidden-
   outputs delta (§2 trigger 4).
4. **Fully tested in the same PR.** The behavioural change and the
   tests pinning it ship together. Tests may **not** be deferred to
   a follow-up PR.

If any of the four conditions fails, the change is not eligible for
batching and must be re-scoped or split.

A data registry (§1.4) is the special case where the source data
file, the derived artifact, the reader, and its tests **must** ship
together, even if a literal reading of §2 would suggest splitting:
fragmenting a registry across PRs leaves the registry transiently
unusable and breaks review context.

---

## 4. When Stacked PRs Are Allowed

A stacked PR (§1.5) is allowed only when **all** of the following
four conditions hold:

1. **The stack is strictly linear.** Each PR has exactly one
   predecessor PR (its `base:` branch) and at most one successor.
2. **Each PR is itself a single category** (§1.1–§1.4 or §1.6).
3. **Each PR's body declares the merge order** and names its
   immediate predecessor.
4. **Stack depth at any moment is ≤ 3 unmerged PRs.**

Stacked PRs are the right shape for *constitutional dependency*:
when PR _B_ may not begin review until PR _A_ has merged, _B_ is
opened on top of _A_'s branch and its body says so. This is how
Z1→Z2→Z3→Z4→Z5 was scheduled.

Stacked PRs are **not** a substitute for batching. If two changes
share one purpose and one layer, they belong in **one** Batch
Implementation PR — not in two stacked PRs.

If a stack ever grows past depth 3 unmerged, an earlier PR must
either merge or be closed; depth-3 is the hard ceiling because
reviewer cognitive load scales superlinearly past it.

---

## 5. Forbidden PR Mixing

The following mixes are forbidden in a single PR:

1. **Constitutional contract + implementation** in the same PR,
   *unless* the contract being touched is purely a local-usage
   amendment to a contract that **already exists in `main`** and
   the implementation is the consumer of that already-merged
   contract.
2. **Implementation before contract.** A PR that implements a
   geometry-producing layer, a new gate, a new rule family, or a
   new binding-evidence type may not be opened before its
   controlling constitutional contract has merged into `main`.
3. **Canonical + experimental.** A PR that mixes a change under
   `src/qiyas_core/` (or `run_qiyas.py`, `tests/qiyas_core/`,
   `docs/qiyas_core/`) with a change under `experimental/`. Each
   tree is touched by its own category of PR.
4. **Multiple unrelated purposes.** A PR whose body cannot state
   its purpose in a single sentence is a mixed PR and must be
   split.
5. **Cross-layer micro-fixes.** A "small cleanup" PR that touches
   two layers' adapters or rules for two different reasons. The
   layers split; the cleanups land separately.
6. **Forbidden-outputs delta + feature.** A PR that modifies a
   `FORBIDDEN_*` tuple in
   `src/qiyas_core/forbidden_outputs.py` *and* adds a feature in
   the same diff. The constitutional delta is its own PR.
7. **Registry + algebra.** A PR that introduces a data registry
   (§1.4) and *also* introduces a rule, adapter, or kernel surface
   that consumes the registry as algebra (rather than as data) in
   the same diff. The data registry merges first; consumers come
   in a strictly later Batch Implementation PR.
8. **Documentation amendment + new principle.** A PR that both
   amends an existing constitutional document and introduces a
   new constitutional principle. Two amendments → two PRs, or one
   merged new contract → later amendments to peers.

Any PR violating a forbidden mix must be split before review.

---

## 6. Examples from this Project

### 6.1 Z1 → Z5 — A Valid Stacked Sequence

The single-character pipeline closure was scheduled as five PRs in a
strict linear stack:

| Step | Category | Purpose | Resulting PR |
| --- | --- | --- | --- |
| Z1 | Constitutional Contract (§1.1) | Ratify Option C and the pre-qiyas tokenizer model | (merged before this policy was written) |
| Z2 | Batch Implementation (§1.3) | Implement `SequenceContextTokenizer` | (merged) |
| Z3 | Batch Implementation (§1.3) | CTS consumes tokenizer evidence | PR #45 |
| Z4 | Micro Safety (§1.2) | Declassify `BoundaryCodePoint` paths | PR #46 |
| Z5 | Batch Implementation (§1.3) | Wire driver to tokenizer + 13 tests | PR #47 / PR #49 |

The stack satisfied §4: strictly linear, each PR was one category,
each PR's body declared its predecessor, and depth never exceeded 3
unmerged at any moment. The merge order was honoured: Z3 merged
first (PR #45 → main), then Z4+Z5 cascaded into their parent
branches (PRs #46, #47) and were brought into main via the final
bring-in PR #49.

The stack is the canonical example of how constitutional dependency
should be scheduled.

### 6.2 Experimental Terminology Cleanup — Separate from Canonical

A future PR that renames legacy fixtures inside
`experimental/qiyas_core/` for terminology consistency must be an
**Experimental Cleanup PR** (§1.6). It may not touch
`src/qiyas_core/`, `tests/qiyas_core/`, `run_qiyas.py`, or
`docs/qiyas_core/` even if the rename "would also be nice" in the
canonical tree. If the canonical tree needs the same rename, that
is a separate PR — typically a Constitutional Contract PR
(`TERMINOLOGY_MAP.md` amendment) followed by a Batch Implementation
PR after the amendment merges.

This is the canonical example of how **§5 trigger 3** ("canonical +
experimental mixing forbidden") is honoured in practice.

### 6.3 Arabic Articulation Registry — One Batch Data Registry PR

The Arabic articulation material lives in two files:

```text
data/arbic-alphabet.csv                  -- source data
data/arabic_articulation_registry.json   -- derived registry
```

The registry has 32 entries, declares its constitutional posture
inside its own payload (`constitutional_role:
"external_data_registry_only"`, plus a
`constitutional_constraints` list pinning *no Candidate, no
QiyasRule, no SlotCandidate, no SlotGeometry, no Dalalah, no
FinalMeaning, no Hukm, no RealityClaim*), and exposes a
`minimal_independent_unit_policy` whose
`required_later_proofs` list — `licensed_slot`,
`minimal_complete_closure`, `later_dalalah_evidence` — wires it
explicitly to the recursive extension contract (§12) and the
minimal complete closure contract (§12) without any direct
licensing claim.

Per §1.4 and §3, the **source CSV, the derived JSON, any reader,
and any registry-shape tests must ship as one PR**. Splitting the
data file, the reader, and the tests into three PRs would leave the
registry transiently unusable and would break review context. The
PR's body must:

- declare the **Data Registry** category,
- name the constitutional posture the registry asserts,
- explicitly state that the registry **does not produce
  `Candidate`** and **does not use `QiyasRule`**,
- list non-goals (no algebra consumer in this PR; no rule, no
  adapter, no kernel surface),
- declare which strictly-later PR will introduce any algebra
  consumer, and which constitutional contract authorises that
  consumer.

This is the canonical example of how **§3's data-registry exception
to splitting** is honoured.

---

## 7. Review Checklist

Every reviewer must verify the following for every PR. Failing
**any** item is grounds for requesting changes.

1. **Category declared.** The PR body states which §1 category the
   PR belongs to, and the diff is consistent with that category.
2. **Single purpose.** The PR body's summary fits in one sentence.
3. **Constitutional basis cited.** For Constitutional Contract,
   Micro Safety, and Batch Implementation PRs, the body cites the
   `CLAUDE.md` §, `*_CONSTITUTION.md` §, or `*_CONTRACT.md` §
   that authorises the change.
4. **Contract before implementation.** For any implementation PR,
   the controlling contract is already merged into `main`. If not,
   the implementation PR is blocked.
5. **Non-goals listed.** The PR body explicitly lists what it does
   *not* do (no SlotGeometry start, no kernel change, no new rule,
   no new candidate type, no final meaning / hukm / reality claim,
   no canonical+experimental mixing).
6. **Tests in the same PR.** For Batch Implementation and Data
   Registry PRs, the tests pinning the change are in the diff. A
   PR that says "tests in follow-up" is rejected.
7. **No forbidden mix** (§5). Reviewer reads the diff against the
   eight forbidden-mix conditions; any hit is grounds for a split
   request.
8. **Stack hygiene.** If stacked, the base branch is correct,
   merge order is declared, and stack depth is ≤ 3 unmerged.
9. **Forbidden outputs preserved.** Any change near the
   `FORBIDDEN_*` surface is explicitly reviewed against
   `forbidden_outputs.py` and against `CLAUDE.md` §19.
10. **Residual preservation.** Any layer change preserves the
    `Residual` chain end-to-end; no residual is silently dropped
    (CLAUDE.md §4 invariant 7).
11. **Identity / trace separation.** Any change touching evidence
    or candidate construction preserves the
    `identity_ids ∩ trace_ids == ∅` invariant
    (CLAUDE.md §4 invariants 1–3).
12. **Rank meet semantics.** Any change touching rank declares
    that `rank_out` is the meet of all participating ranks
    (CLAUDE.md §4 invariant 6, recursive extension contract §8).

This checklist composes with `AGENT_PR_CHECKLIST.md`; the items
above do not replace it, they reinforce it for the categories of
this policy.

---

## 8. Merge-Order Rules

The merge order of a set of PRs is fixed by the following rules,
in priority order:

### 8.1 Constitutional contracts merge first

A Constitutional Contract PR (§1.1) merges before any PR that
relies on the contract it ratifies. Implementation PRs whose
controlling contract is still open are blocked from merge until the
contract lands.

### 8.2 Stacks merge bottom-up, linearly

A stacked PR (§1.5) merges into its declared `base:` branch first,
then the next PR up the stack rebases / merges, and so on until
the top PR reaches `main`.

A common pattern in this project: Z3 → Z4 → Z5 merged each into
its predecessor (PRs #45, #46, #47), and a final **bring-in PR**
(#49, `feat/z5-tokenizer-driver → main`) carried Z4+Z5 into main
once Z3 was already there. Bring-in PRs of this shape are
legitimate: they add no new commits, they only redirect a
fully-reviewed top-of-stack branch into `main`.

### 8.3 Data registries merge before their algebra consumers

A Data Registry PR (§1.4) merges strictly before any Batch
Implementation PR that consumes the registry as data feeding into
algebra. The algebra consumer's PR body must cite the merged
registry's commit hash.

### 8.4 Micro Safety PRs merge in cumulative order

When several Micro Safety PRs are scheduled in parallel, each
closes one safety gap independently of the others; they may
therefore merge in any order, but each must rebase to the current
`main` immediately before merge so its tests run against the
cumulative state.

### 8.5 Experimental Cleanup PRs are independent

An Experimental Cleanup PR (§1.6) is independent of canonical
PRs and may merge at any time, in any order, without affecting
canonical merge scheduling.

### 8.6 No fast-forward over an unreviewed contract

A merge that would fast-forward `main` past a Constitutional
Contract PR which has not itself merged is forbidden. The contract
PR must land first, even if doing so requires waiting on review.

### 8.7 No PR merges into `main` with `CandidateOnly` violated

If a PR's diff would cause any canonical Candidate output flag to
diverge from `CandidateOnly` constraint, the PR is blocked from
merge regardless of test status. (CLAUDE.md §4 invariant 9.)

---

## 9. Policy — Binding Restatement

The following bullets restate the policy as binding rules. Every PR
opened against this repository is subject to them, and every
reviewer must enforce them.

- **Split** PRs when layer boundaries, kernel invariants, Candidate
  safety, forbidden outputs, or constitutional contracts are
  involved.
- **Batch** PRs when changes are same-purpose, same-layer (or
  strictly contiguous layer pair), low-risk, and fully tested.
- **Do not split** a data file, its reader, and its tests into
  separate PRs if they serve one registry.
- **Do not mix** `experimental/` with canonical `src/`.
- **Do not mix** a docs-constitutional change with implementation
  unless the contract already exists in `main` and the doc edit is
  only local-usage documentation.
- **Do not start** implementation before its controlling
  constitutional contract exists in `main`.
- **Do not stack** deeper than 3 unmerged PRs at any moment.
- **Do not defer tests** to a follow-up PR; tests ship with the
  change they pin.
- **Do not merge** any PR that mixes registry data with algebra
  consumers in one diff; the registry lands first.

---

## 10. Non-Goals

This document does **not**:

- modify any file under `src/qiyas_core/`,
- modify any file under `tests/qiyas_core/`,
- modify any file under `experimental/`,
- modify `run_qiyas.py`,
- modify any other constitutional document,
- introduce any new CI check, hook, bot, or automation,
- define any new layer, candidate type, evidence shape, rule, or
  rank,
- authorise the start of `SlotGeometryQiyas` or any binding-
  evidence layer,
- redefine `Candidate`, `Residual`, `Trace`, or any kernel
  primitive,
- replace `AGENT_PR_CHECKLIST.md`; this policy composes with it.

---

## 11. Status Classification

This document is classified as:

- **constitutional** — the scheduling policy is binding on every
  future PR;
- **process-only** — no code, no test, no rule, no candidate type;
- **layer-agnostic** — the policy applies to every PR regardless
  of which layer or contract it concerns;
- **complementary** — composes with `AGENT_PR_CHECKLIST.md`,
  `MICRO_PR_GOVERNANCE_FIX_SUMMARY.md`, and the constitutional
  contracts cited in the authority basis.

The classification persists until and unless a formal
constitutional amendment supersedes it.

---

## 12. Authority

Once merged, this document is the constitutional reference for:

- any future review of PR scope or batching,
- any future merge-order dispute,
- any future request to stack or split PRs,
- any future automation that schedules PRs (none is authorised by
  this document; this policy is human-enforced).

It supersedes nothing prior; it codifies the implicit practice that
was already followed for Z1 → Z5 and the recursive-extension /
closure contracts (PRs #44–#50) and binds it as policy going
forward.

It does **not** authorise the implementation of any layer, rule, or
adapter. Each must continue to be ratified by its own contract PR
under §1.1 before any implementation PR may be opened under §1.3.

---

## 13. Glossary

| Term                              | Meaning |
| --------------------------------- | --- |
| Constitutional Contract PR        | A docs-only PR that adds or amends a constitutional document (§1.1). |
| Micro Safety PR                   | A small, targeted PR closing one constitutional safety gap inside one layer (§1.2). |
| Batch Implementation PR           | A PR bundling one constitutional purpose's implementation, including tests, inside one layer (§1.3). |
| Data Registry PR                  | A PR introducing or amending an external data registry, with its derived artifacts, reader, and tests, all together (§1.4). |
| Stacked Dependency PR             | A PR opened on top of another non-yet-merged PR in a strict linear chain (§1.5). |
| Experimental Cleanup PR           | A PR touching only `experimental/` (§1.6). |
| Bring-in PR                       | A merge-only PR that flows a fully-reviewed top-of-stack branch into `main` without adding new commits (§8.2). |
| Stack depth                       | The number of unmerged PRs currently in a linear stack; bounded at 3 by §4. |
| Forbidden mix                     | Any of the eight combinations enumerated in §5. |
| Contract-before-implementation    | The principle that no implementation PR may be opened before its controlling constitutional contract has merged into `main` (`RESET_CONSTITUTION.md` §1; §5 trigger 2 of this document). |

---

**End of document.**

**Ratification PR is docs-only.**
**No implementation is authorised by this PR.**
