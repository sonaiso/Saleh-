# Letter Transliteration Naming Contract

> **Type:** Docs-only constitutional contract (canonicalisation discipline).
>
> **Status:** Ratifies `src/qiyas_core/registries/letter_name_registry.py` as the **single canonical source** for Latin-transliteration letter names of Arabic codepoints. Documents the current naming inconsistencies surfaced by PR #94's alphabet-coordinate enrichment tests. Does **not** fix any module, does **not** modify the registry, does **not** change runtime, does **not** repair PR #94 failures.
>
> **Authority basis (read-only citation):**
>
> - `SOURCE_OF_TRUTH_REGISTRY.md` — the meta-contract for single-source-of-truth discipline ("No operational truth without a single source"). This contract extends that discipline to a specific truth-kind: Latin-transliteration letter names.
> - `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md`
> - `MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md` (cited only for the established evidence-build pattern referenced in §9)
> - `MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md` (same)
> - `CLAUDE.md` §0 / §2 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20 / §21

---

## 1. Purpose

This contract defines a single constitutional policy for Latin-transliteration letter names used inside Saleh/Qiyas.

It exists because PR #94's alphabet-coordinate enrichment tests surfaced 5 failures whose proximate cause for at least 2 letters is **inconsistent Latin spelling across modules** that should agree on a single canonical name per Arabic codepoint.

The contract:

- **Ratifies** `src/qiyas_core/registries/letter_name_registry.py` as the single canonical source for Latin-transliteration letter names.
- **Documents** the current observed inconsistencies verbatim, codepoint by codepoint, module by module.
- **Defines** the future-PR alignment rule.
- **Forbids** specific shortcuts (test-only patching; per-module aliases; silent multi-spelling acceptance).

It does **not**:

- modify any module,
- modify the registry,
- change runtime behaviour,
- repair the PR #94 failures (the fix belongs to a strictly later, separately-triggered PR — see §12),
- create a new registry,
- create an Evidence carrier,
- create a `Candidate` of any type,
- introduce a new claim, label, gate, rule, or producer,
- decide *i'rāb*, meaning, *dalālah*, *hukm*, or reality,
- amend `SOURCE_OF_TRUTH_REGISTRY.md` (cites only),
- amend `letter_name_registry.py` (ratifies its current values as canonical).

This contract is a **constitutional precursor** to a future small code PR that aligns the inconsistent modules. The code PR is **not** opened by or implied by this contract.

---

## 2. Problem Statement

PR #94 (full Arabic alphabet coordinate enrichment for 26 core letters; merged at commit `c0f6653`) added a parameterised test file `tests/qiyas_core/test_full_alphabet_coordinates.py` whose expectations include a `letter_name` value per codepoint. The expectations match `src/qiyas_core/registries/letter_name_registry.py` exactly.

5 of the 26 parameterised cases currently fail in the canonical suite. The investigation at `/tmp/pr94_alphabet_coordinate_failure_investigation.md` characterises two root-cause patterns:

- **For ذ (U+0630) and ظ (U+0638)** — *naming inconsistency across modules*: at least one of the modules contributing to the kernel's identity match uses a different Latin spelling than the canonical name in `letter_name_registry.py`. When `ArabicLetterCoordinateQiyas` composes identity from the identity rule and tries to match the coordinate rule against the registry-canonical expectation, the spellings disagree and the kernel rejects the candidate.

- **For ه (U+0647)** — *primarily an evidence-build issue*: the registry, identity rule, coordinate rule, abjad system, and test all agree on `haa_final` (one module, `phonetics/profiles.py`, uses a different name — see §4 — but that module is not on the kernel's identity-composition path for the failing tests). The kernel still returns an empty `accepted` set, which under Saleh's established evidence-build discipline means a missing structured wasf claim or an unsatisfied Wadi gate. **The ه failures are NOT primarily a naming problem.** This contract documents that distinction but does not address the evidence build.

The contract's scope is therefore: **ratify a single source for Latin names; document the inconsistencies; defer all repair**.

---

## 3. Source of Truth

The single canonical source for Latin-transliteration letter names of Arabic codepoints is:

```
src/qiyas_core/registries/letter_name_registry.py
```

Under this contract:

- **Any module** that names an Arabic letter by a Latin transliteration MUST take that name from `letter_name_registry.py` (by import, by lookup, or by exact-string match against the registry's current value).
- **No module** may invent a per-module spelling.
- **Test expectations** that name letters MUST track the registry. A test asserting a Latin name that disagrees with the registry is a contract violation by the test, not by the implementation.
- **The registry itself** is the only place this contract authorises the values to be edited. Edits to the registry are a separate concern (a registry-amendment PR) and are outside the scope of this contract.

This extends the meta-discipline of `SOURCE_OF_TRUTH_REGISTRY.md` (§0 "Why Source-of-Truth Registry?") to the specific truth-kind: **letter Latin transliteration name**. The registry already declares the canonical values; this contract gives them constitutional standing.

---

## 4. Current Observed Inconsistencies

The following values are recorded **verbatim from the files** at the time of writing. Lines cited are exact. **Do not infer from memory; the values below are what the files currently contain.**

### 4.1 U+0630 ذ (canonical Latin name: `thaal`)

| Source | File | Line | Latin name found |
|---|---|---:|---|
| **Canonical** | `src/qiyas_core/registries/letter_name_registry.py` | 62 | `"thaal"` |
| ✓ agrees | `src/qiyas_core/rules/letter_coordinate_rules.py` | 253 | `letter_name="thaal"` (PR #94) |
| ✓ agrees | `tests/qiyas_core/test_full_alphabet_coordinates.py` | 34 | `"thaal"` |
| ✗ disagrees | `src/qiyas_core/rules/letter_identity_rules.py` | 170 | `"dhal"` |
| ✗ disagrees | `src/qiyas_core/abjad_system.py` | 97 | `"dhal"` |
| ✗ disagrees | `src/qiyas_core/phonetics/profiles.py` | 396 | `arabic_name="dhaal"` |

**Three distinct Latin spellings present for the same codepoint** (`thaal` / `dhal` / `dhaal`).

The most directly load-bearing mismatch (per the failing test's traceback at `test_full_alphabet_coordinates.py:86`) is between `letter_identity_rules.py`'s `"dhal"` and the registry's canonical `"thaal"`:

```
AssertionError: assert 'letter_identity.dhal' == 'letter_identity.thaal'
```

The kernel composes the identity claim from `letter_identity_rules.py`, producing `letter_identity.dhal`; the coordinate rule expects `letter_identity.thaal` (matching the registry); the match fails; the kernel rejects the coordinate Candidate; the test's `len(accepted) == 1` assertion fails.

### 4.2 U+0638 ظ (canonical Latin name: `dhaa`)

| Source | File | Line | Latin name found |
|---|---|---:|---|
| **Canonical** | `src/qiyas_core/registries/letter_name_registry.py` | 70 | `"dhaa"` |
| ✓ agrees | `src/qiyas_core/rules/letter_identity_rules.py` | 202 | `"dhaa"` |
| ✓ agrees | `src/qiyas_core/abjad_system.py` | 105 | `"dhaa"` |
| ✓ agrees | `tests/qiyas_core/test_full_alphabet_coordinates.py` | 42 | `"dhaa"` |
| ✗ disagrees | `src/qiyas_core/rules/letter_coordinate_rules.py` | 349 | `letter_name="dhaa_emphatic"` (PR #94) |
| ✗ disagrees | `src/qiyas_core/phonetics/profiles.py` | 525 | `arabic_name="dhaa_emphatic"` |

**Two distinct Latin spellings present for the same codepoint** (`dhaa` / `dhaa_emphatic`). The newer PR #94 file uses the suffixed variant; four older modules and the test use the canonical bare variant.

### 4.3 U+0647 ه (canonical Latin name: `haa_final`)

| Source | File | Line | Latin name found |
|---|---|---:|---|
| **Canonical** | `src/qiyas_core/registries/letter_name_registry.py` | 80 | `"haa_final"` |
| ✓ agrees | `src/qiyas_core/rules/letter_identity_rules.py` | 242 | `"haa_final"` |
| ✓ agrees | `src/qiyas_core/rules/letter_coordinate_rules.py` | 457 | `letter_name="haa_final"` (PR #94) |
| ✓ agrees | `src/qiyas_core/abjad_system.py` | 114 | `"haa_final"` |
| ✓ agrees | `tests/qiyas_core/test_full_alphabet_coordinates.py` | 51 | `"haa_final"` |
| ✗ disagrees | `src/qiyas_core/phonetics/profiles.py` | 668 | `arabic_name="haa_glottal"` |

**Two distinct Latin spellings present for the same codepoint** (`haa_final` / `haa_glottal`).

However, the failing tests for ه (Failures 3, 4, 5 per the investigation) fail with `len(accepted) == 0`, not with a name-comparison assertion. The kernel's identity match for ه completes (all five identity-path modules agree), but the kernel still rejects the Candidate — pointing to an evidence-build shortfall (missing `effective_wasf` claim / unsatisfied Wadi gate / structurally-unrecorded `SAALATAMUUNIIHA` annotation; see §9). **The phonetics-side `haa_glottal` mismatch is recorded here for completeness but is NOT the proximate cause of the ه test failures.**

### 4.4 Inconsistency summary (codepoint × module)

| Codepoint | Registry | identity_rules | coordinate_rules (PR #94) | abjad_system | phonetics/profiles | test expects |
|---|---|---|---|---|---|---|
| ذ U+0630 | `thaal` | **dhal** ✗ | `thaal` ✓ | **dhal** ✗ | **dhaal** ✗ | `thaal` ✓ |
| ظ U+0638 | `dhaa` | `dhaa` ✓ | **dhaa_emphatic** ✗ | `dhaa` ✓ | **dhaa_emphatic** ✗ | `dhaa` ✓ |
| ه U+0647 | `haa_final` | `haa_final` ✓ | `haa_final` ✓ | `haa_final` ✓ | **haa_glottal** ✗ | `haa_final` ✓ |

✗ marks each module whose Latin spelling currently disagrees with the registry-canonical value.

The remaining 23 letters of the 26-letter alphabet are not enumerated here; this contract does not assume their consistency. A future audit may extend the table.

---

## 5. Canonical Name Resolution Rule

The constitutional rule for any future code that names an Arabic letter by Latin transliteration:

```
canonical_latin_name(letter)  :=  value from letter_name_registry.py
                                  at the entry keyed by the letter's
                                  Arabic-letter Unicode codepoint
```

### 5.1 Allowed implementations

- Import the value (or a helper) from `letter_name_registry.py` and use it directly.
- Hold a per-module local reference whose value is **exactly** the registry's current value and is unit-tested against the registry.
- Receive the name as an argument from a layer that already obtained it from the registry.

### 5.2 Forbidden implementations

- Per-module local Latin transliteration that is not derived from `letter_name_registry.py`.
- Ad-hoc spelling variants not present in the registry.
- Test-only expected names that differ from the registry (a test failure caused by such a discrepancy is a test bug under this contract, not an implementation bug; the test is to be updated to track the registry).
- Phonetics-only or coordinate-only names that override the registry within the kernel's identity-composition path.
- Aliasing: defining a per-module alias (e.g., `dhal = "thaal"`) that creates a second canonical-feeling name. Aliases at the module level dilute the single-source discipline; they MUST NOT be introduced as a workaround.

### 5.3 What this rule does NOT decide

- Which specific Latin spelling the registry SHOULD use. The registry's current values are ratified verbatim as canonical by §3; any change to a registry value is a separate registry-amendment PR.
- Arabic-name fields like `phonetics/profiles.py::arabic_name` may carry phonetic-context-specific labels (e.g., `"haa_glottal"` for U+0647) for descriptive purposes, **provided** that the kernel's identity composition does not depend on those labels. If a phonetic-context label appears on the identity-composition path, it MUST equal the registry's canonical Latin name.

---

## 6. Affected Letters

The PR #94 alphabet-coordinate failures involve three codepoints. Under this contract:

- **ذ (U+0630)** — affected; three distinct Latin spellings observed; primary fix is to align `letter_identity_rules.py` and `abjad_system.py` (and the phonetics surface where applicable) to the registry's `thaal`.
- **ظ (U+0638)** — affected; two distinct Latin spellings observed; primary fix is to align `letter_coordinate_rules.py` and the phonetics surface where applicable to the registry's `dhaa`.
- **ه (U+0647)** — included only because PR #94's test failures include it. Its issue is **NOT** primarily a naming inconsistency (4 of 5 modules and the test agree on `haa_final`). Its issue is **likely** an evidence-build issue at the coordinate rule (see §9). One naming inconsistency in `phonetics/profiles.py` (`haa_glottal`) is documented here for completeness but is not on the identity-composition path of the failing tests.

A future audit may extend the affected-letters set as additional codepoints are inspected. Such an extension is outside this contract.

---

## 7. Future Code Alignment Requirements

Any later PR proposing to fix the PR #94 alphabet-coordinate failures' **naming-related** root causes MUST:

- **Read or match** `letter_name_registry.py` as the single source for Latin names.
- **Unify** ذ and ظ across `letter_identity_rules.py`, `letter_coordinate_rules.py`, `abjad_system.py`, and the phonetics surface (where it appears on the identity path), to the registry's canonical values.
- **Not change** any letter's semantic role (identity, articulation, function).
- **Not add** meaning, *dalālah*, *i'rāb*, *hukm*, or reality.
- **Not introduce** a new runtime layer.
- **Not expand** alphabet coordinates beyond the codepoint set already in PR #94.
- **Not weaken** any existing invariant in the variant-resolution → MIU layer (the 17-test focused suite must remain green).
- **Not bundle** the ه evidence-build fix with the naming alignment if doing so makes the PR's surface harder to review; the evidence-build fix MAY be in the same PR if scoped cleanly, otherwise it belongs in a separate PR.

Constants whose **name** (the Python identifier, not the `letter_name` field value) is currently misaligned (e.g., `DHAAL_COORDINATE_RULE` referring to ذ in a file that emits `letter_name="thaal"`) are a separate, cosmetic concern. Aligning constant names to the registry's Latin names is RECOMMENDED but not REQUIRED by this contract — what matters under §3 is the value emitted onto the identity-composition path, not the constant identifier.

---

## 8. Relationship to PR #94 Failures

- This contract **prepares** the constitutional ground for fixing the ذ and ظ naming-related failures. It does NOT itself fix them.
- The ه failures (Failures 3, 4, 5) need additional non-naming work (likely an `effective_wasf` claim added to the rule's `required_effective_wasf` tuple, plus a corresponding structured wasf emission in the rule's `_build_evidence` body — see §9). That work belongs to a strictly separate PR or to a separately-scoped section of the same future fix PR.
- The full canonical suite **MAY remain non-green** after this docs-only contract merges. PR #94's 5 failures (currently `1081 passed, 5 failed, 4 skipped`) are not addressed by this contract.
- The focused variant-resolution → MIU test (`tests/qiyas_core/test_variant_resolver_miu_integration.py`) is the appropriate **non-blocking smoke check** for this docs-only PR. It remains green under this contract.
- A separate read-only investigation report at `/tmp/pr94_alphabet_coordinate_failure_investigation.md` (outside this repository, not committed) characterises the failures in detail and enumerates fix options. The recommended path is "this contract first, then a small code PR".

---

## 9. Relationship to Evidence Claims

Naming consistency is a **necessary condition** for the kernel's identity match to succeed. It is **not a sufficient condition** for the coordinate Candidate to reach the kernel's `accepted` set.

For ذ and ظ, naming alignment (per §7) is the primary blocker; fixing the names is expected to unblock the kernel's identity match and let the rest of the rule's evidence build pass.

For ه, all four identity-path modules and the test already agree on `haa_final`, so naming is not the blocker. The likely missing piece is a structured wasf claim corresponding to the `SAALATAMUUNIIHA` annotation. The investigation report notes that the implementation carries `SAALATAMUUNIIHA` in a comment but the rule may not emit it as a `وصف:` claim that the rule's `required_effective_wasf` tuple lists. **This contract does not define that wasf claim.** It is recorded here only to make explicit that fixing naming alone will not fix ه.

This contract follows the established Saleh discipline (cf. PR #71 / #72 / #73 / #80 / #81 patterns) that an Evidence-build shortfall surfaces as an empty `accepted` set with structurally-present `trace_ids` — but the design of the missing wasf belongs to a separate future PR, not to this one.

---

## 10. Forbidden Shortcuts

Under this contract, the following are explicitly forbidden in any future fix attempt:

- **Changing tests only to pass.** Updating a test's expected Latin name to match an implementation's misaligned spelling (instead of aligning the implementation to the registry) violates §3 — the registry is the source of truth, not the implementation.
- **Adding aliases without a contract.** Defining a per-module alias such as `dhal = "thaal"` to silently bridge the inconsistency dilutes the single-source discipline. If aliases ever become necessary they require their own constitutional amendment.
- **Silently accepting multiple canonical spellings.** Treating both `thaal` and `dhal` (or both `dhaa` and `dhaa_emphatic`) as "valid for ذ / ظ" violates §3.
- **Changing letter identity semantics.** Renaming the canonical Latin name in the registry to a different transliteration solely to match the implementation (rather than vice-versa) is forbidden unless ratified by a registry-amendment PR with its own constitutional review.
- **Changing the Arabic articulation registry** as a workaround.
- **Changing the glyph classification registry** as a workaround.
- **Changing `SifatVector`** as a workaround.
- **Changing MIU adapter / rule** as a workaround.
- **Adding `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment` / `MinimalIndependentMeaningCandidate`** — these have nothing to do with the failure and are standing non-goals.

---

## 11. Non-Goals

This PR is **docs-only** and explicitly does not include, propose, or imply:

- no code (no `src/` change)
- no tests (no `tests/` change)
- no registry change (no edit to `letter_name_registry.py` or any other registry)
- no runtime (no Evidence carrier, no `Candidate`, no rule, no gate, no producer)
- no fix to PR #94 failures
- no alphabet-coordinate-enrichment behaviour change
- no Evidence-carrier creation
- no `ArabicVariantResolver` change
- no `GlyphClassificationGate` contract change / no Glyph runtime
- no `SifatVector` runtime
- no `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`
- no `SentenceCandidate` / `ParagraphCandidate` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate` / `MinimalIndependentMeaningCandidate`
- no `Amil` layer runtime / no `I'rab` runtime / no `OperatorGeometry`
- no amendment to `SOURCE_OF_TRUTH_REGISTRY.md` (cites only)
- no amendment to `ARABIC_AWAMIL_MABNIYAT_SOURCE_CONTRACT.md`, `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md`, `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md`, or any other merged contract
- no `__init__.py` change
- no `run_qiyas.py` change
- no `experimental/` change
- no second PR

---

## 12. Future Work

Safe future PRs (each requires its own explicit trigger; each must pass its own preflight; each must respect all standing non-goals):

1. **`fix(qiyas_core): align full alphabet coordinate naming with letter registry`** — the small code PR that aligns `letter_identity_rules.py`, `letter_coordinate_rules.py`, `abjad_system.py`, and the phonetics surface where applicable, to `letter_name_registry.py`'s canonical values for ذ and ظ. Touches `src/` and may also need a test-expectation tweak where the test asserts a wrong Latin spelling against the now-canonical registry (the test currently agrees, so no test change is expected for ذ / ظ).

2. **`fix(qiyas_core): add missing structured evidence claim for haa_final coordinate enrichment`** — the small code PR that introduces the `SAALATAMUUNIIHA`-aligned `وصف:` wasf claim into `HAA_FINAL_COORDINATE_RULE`'s `_build_evidence` body and adds it to the rule's `required_effective_wasf` tuple. May share a PR with item 1 if the surface is small.

3. **Optional**: `test(qiyas_core): add transliteration source-of-truth regression coverage` — a tests-only PR that adds an AST/import audit asserting no module other than `letter_name_registry.py` defines a per-codepoint Latin name string. Prevents future drift.

4. **Future fixture material — out of scope of THIS contract**: the external operators CSV at `/Users/husseinhiyassat/fractal/new_arabic_analyzer/data/operators_catalog_split_vocalized.csv` carries an `Example_Vocalized` column with fully voweled Arabic example sentences (e.g., `مَرَرْتُ بِزَيْدٍ`, `سِرْتُ مِنَ الْبَيْتِ`). These vocalized examples exist as **external source material**, are recorded as descriptive cells per `EXTERNAL_AWAMIL_MABNIYAT_SOURCE_INVENTORY.md` (PR #96) and `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` §11 (PR #97 — `Example_Vocalized → example_vocalized` descriptive), and **MUST NOT** be used as runtime test fixtures, *i'rāb* evidence, operator-role proof, or input to any new runtime layer at this time. A separate **`docs(qiyas_core): define external vocalized example fixture contract`** future PR is required before any fixture-derived tests of any kind may be written against these example sentences. This item is named here only to forward-cite the boundary; **this naming contract does not consume, register, or test any vocalized example**, and the future fixture contract is strictly out of scope of the PR #94 fix cycle (Steps 1–3 above) — its trigger is independent.

What is **NOT** future work and must not be recommended next:

- runtime carriers / producers / registries for any of the above,
- `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`,
- `Amil` runtime / `I'rab` runtime,
- bundling either fix PR with any of the four `EXTERNAL_SOURCE_NORMALIZATION_CONTRACT.md` §19 follow-ups (source-table contracts; discrepancy-reporting contract; snapshot policy),
- introducing a new alphabet expansion beyond PR #94's 26-letter set.

**This contract does not start any of the items above.** Each requires its own explicit trigger.

---

## 13. Summary Table

| Question | Answer |
|---|---|
| Is this runtime? | No. Docs-only canonicalisation contract. |
| Does it fix PR #94? | No. It prepares the ground for a future fix. |
| What is the source of truth? | `src/qiyas_core/registries/letter_name_registry.py`. |
| What is the main naming issue? | ذ (3 distinct spellings: `thaal` / `dhal` / `dhaal`) and ظ (2 distinct spellings: `dhaa` / `dhaa_emphatic`). |
| Is ه a naming issue? | Mostly no. 4 of 5 modules + the test agree on `haa_final`; one phonetics-side spelling (`haa_glottal`) differs but is not on the identity-composition path of the failing tests. The ه failures are primarily an evidence-build issue, not a naming issue. |
| What is the next code step? | A separate fix PR (per §12 item 1), explicitly triggered by the maintainer. |
| Does this contract amend the registry? | No. It ratifies the registry's current values as canonical. |
| Does this contract change `SOURCE_OF_TRUTH_REGISTRY.md`? | No. It cites that meta-contract and extends it to a specific truth-kind. |
| Does this contract introduce Word / Dalalah / Meaning / Hukm / Reality? | No. |
| Does this contract address the 5 PR #94 failures? | No. They remain unresolved until the future fix PR. |

---

**Document version:** 1.1
**Last updated:** 2026-06-06 (added §12 item 4 — forward-cite of vocalized-example fixture material as out of scope of this contract)
**Status:** Letter transliteration naming contract (docs-only).
**Authority:** Subordinate to `SOURCE_OF_TRUTH_REGISTRY.md`, to `letter_name_registry.py` (whose current values it ratifies), and to `CLAUDE.md` §0–§21. Does not amend any of them.
