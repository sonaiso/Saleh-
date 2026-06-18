# SCG_P3_P8_INFORMATION_GAIN_CASCADE — architecture note (descriptive)

> **Status:** **Descriptive architecture note**, not a constitution. It documents
> the *landed runtime behavior* of SCG layers P3–P8 after the information-gain
> campaign; it introduces **no new theory, no new layer, no new name**. Where it
> and a layer constitution disagree, the constitution + canonical code win.
>
> **Mainline baseline:** `main @ 38c1df5` — full suite **2528 passed / 2 skipped**;
> registry count **19**; IMPLEMENTED P0–P8; SPECIFIED P9–P12; freeze ACTIVE for P9+.
>
> **Authority:** subordinate to `PROJECT_MATHEMATICAL_FOUNDATION.md`,
> `CANONICAL_ARCHITECTURE_CONTROL_FRAME.md`, `LAYER_REGISTRY.md`, and each layer's
> own constitution (`ROOT_STEM_CLOSURE`, `JAMID_MUSHTAQ`, `MUFRAD_WORD`,
> `VERBAL_SIGNIFIED`, `COMPOSITION_READINESS`, `AMIL_MAMUL`).

---

## 1. What changed: forwarding → information-gain

A prior read-only audit found that SCG-P3…P7 (and the then-uncommitted P8) were
**forwarding layers**: every accepted upstream candidate produced exactly one
downstream candidate, the carried "signature" was a re-encoding of upstream
codepoints, evidence was a hardcoded all-pass, and **no input could ever be
deferred or blocked** (`NO_DISCRIMINATION_POWER`).

The P3–P8 information-gain campaign converted each of those layers into an
**information-gain layer**: a layer that **reads the prior layer's structural
evidence**, computes a small **structural sub-profile**, and emits one of three
verdicts — **ACCEPT / DEFER / BLOCK** — so the accepted-candidate stream **thins**
as geometry becomes insufficient. This preserves every constitutional invariant
(candidate-only, identity-preserving, no-jump, no semantic/hukm leakage) while
making each layer contribute genuine discrimination.

## 2. The shared mechanism

Every strengthened layer Pₙ (P4…P8) follows the same pattern:

1. **Read Pₙ₋₁'s evidence off the candidate it receives.** The upstream verdict
   and structural geometry ride on the candidate's `trace_ids` as a documented
   `…_evidence:` string (e.g. `cv=…;nC=…;…;verdict=…`). Pₙ parses it — it does not
   re-derive identity. (P3 reads a per-token structural profile computed once by
   `run_qiyas._segment_root_stem_profiles`; from P4 onward, no `run_qiyas` change
   was needed because the evidence travels on the candidate.)
2. **Compute a structural sub-profile** (CV signature, consonant count, vowel
   count, gemination, short-vowel cadence, ending/boundary) — **purely geometric**;
   no lexicon, morphology, wazn, or meaning.
3. **Emit a verdict via the kernel's existing residual machinery** — never
   hardcoded all-pass:
   - **ACCEPT** — prove the required waṣf/ʿilla/wādī and (only here) emit the
     `opens_prior:*` traces for the licensed downstream priors.
   - **DEFER** — emit `defer:<reason>:present` → the kernel returns a **DEFERRED**
     candidate with a preserved residual; opens **no** priors.
   - **BLOCK** — emit `فارق:<reason>:present` → the kernel returns a **BLOCKED**
     candidate with a residual; opens nothing. (A non-accepted upstream candidate
     also carries rank 0, which independently blocks downstream.)
4. **Select an input-dependent, structural `prior_type`** from that layer's
   allowed set — never a linguistic/grammatical/case label.
5. **Preserve identity** (`identity_ids = asl ∪ far`), keep `output_flags =
   {CandidateOnly}`, and keep identity disjoint from trace — for ACCEPT, DEFER,
   and BLOCK alike.

`run_qiyas.py` gates every layer on the prior's **accepted** output, so a
DEFER/BLOCK upstream simply stops the chain there (the count drop), and the
strengthened-layer evidence chain runs **downstream-reads-upstream**
(P4←P3, P5←P4, P6←P5, P7←P6, P8←P7).

## 3. Per-layer verdict rules

All signals are structural CV-geometry. `nC` = consonant count; `cadence` =
short-vowel alternation (`"VV"` absent from the CV signature, i.e. no long vowel).

### P3 — RootStemCandidate (root/stem closure)
- **ACCEPT** ⇔ `nC ≥ 1 AND (slot_count ≥ 2 OR long_vowel OR gemination)`
- **DEFER** ⇔ lone bare CV → `root_pattern_underspecified`
- **BLOCK** ⇔ `nC == 0` → `root_pattern_conflict`
- prior/evidence: input-dependent `structural_root_stem_signature`,
  `root_pattern_evidence` (cv, slots, gem, lv), `stem_boundary_evidence` (ending, nC).

### P4 — JamidMushtaqCandidate (derivation geometry)
- **BLOCK** ⇔ P3 verdict ≠ accept, or `nC == 0` → `derivation_classification_conflict`
- **ACCEPT** ⇔ `nC ≥ 2`
- **DEFER** ⇔ `nC == 1` (skeleton too thin, e.g. مَا) → `derivation_underspecified`
- `prior_type`: gemination → `StructuralDerivationPossibility`; `nC ≥ 3` →
  `DerivationGeometryClass`; else → `DerivationGeometryPrior`.

### P5 — MufradWordCandidate (isolated word-unit body)
- `word_unit_sufficient = (vowel_count ≥ 2 OR closed_ending OR gemination)`
- **BLOCK** ⇔ P4 ≠ accept, or `nC == 0`
- **ACCEPT** ⇔ `nC ≥ 2 AND word_unit_sufficient`
- **DEFER** ⇔ otherwise (e.g. compact `CCV`) → `word_unit_underspecified`
- `prior_type`: gemination → `WordUnitShapePossibility`; closed_ending →
  `IsolatedUnitBoundaryPrior`; `vowels ≥ 2` → `MufradUnitGeometryClass`; else →
  `StructuralWordUnitPrior`.

### P6 — VerbalSignifiedCandidate (verbal carrier)
- `verbal_carrier_sufficient = nC ≥ 2 AND ((nC ≥ 3 AND cadence) OR gemination)`
- **BLOCK** ⇔ P5 ≠ accept, or `nC == 0`, or `vowel_count == 0` → `signified_class_conflict`
- **ACCEPT** ⇔ `verbal_carrier_sufficient`
- **DEFER** ⇔ otherwise (long-vowel-only units بَاب/بَيت) → `verbal_carrier_underspecified`
- `prior_type`: gemination → `GeminatedCarrierPossibility`; `nC ≥ 3` + cadence →
  `ShortVowelCadencePrior`; `nC ≥ 3` → `VerbalCarrierGeometryClass`; else →
  `StructuralSignifiedCarrierPrior`.
- ACCEPT opens **only** `meaning_priors` + `dalalah_priors` — never a
  `MeaningCandidate` / `DalalahCandidate`.

### P7 — CompositionReadinessCandidate (readiness gate)
- `composition_ready = (cadence AND nC ≥ 3)` (a clean, unambiguous operand boundary)
- **BLOCK** ⇔ P6 ≠ accept, or `nC == 0` → `composition_precondition_blocked`
- **ACCEPT** ⇔ `composition_ready`
- **DEFER** ⇔ otherwise (boundary-ambiguous, e.g. geminated long-vowel شَاذّ) →
  `composition_readiness_underspecified`
- `prior_type`: closed + cadence → `CadenceBoundaryPrior`; `nC ≥ 3` + cadence →
  `CompositionReadinessGeometryClass`; gemination → `GeminatedReadinessPossibility`;
  else → `StructuralReadinessPrior`.
- ACCEPT opens **only** `amil_mamul_relation_priors` + `sentence_geometry_priors`.

### P8 — AmilMamulCandidate (operator–operand relation possibility)
- `relation_possible = (nC ≥ 3 AND cadence AND vowel_count ≥ 3)` — the most
  demanding layer: a richly-vocalised skeleton able to host a relation.
- **BLOCK** ⇔ P7 ≠ accept, or `nC == 0` → `amil_mamul_relation_blocked`
- **ACCEPT** ⇔ `relation_possible`
- **DEFER** ⇔ otherwise (compact / fewer-vowel operand, e.g. عَدَّ) →
  `relation_geometry_underspecified`
- `prior_type`: gemination → `CompactRelationPossibility`; `vowels ≥ 3` + cadence →
  `RelationCadenceGeometryClass`; `nC ≥ 3` + `vowels ≥ 2` → `RelationGeometryClass`;
  else → `StructuralRelationPrior`.
- ACCEPT opens **only** `grammatical_relation_priors` + `irab_priors` — it is a
  **relation possibility**, never an actual i'rab/case judgment.

## 4. The empirical cascade

Demo (`tools/qiyas_scg_ladder_state.py "شَاذّ عَدَّ بَ مَا مِن بَاب بَيت ض ضَرَبَ"`),
accepted counts thinning down the ladder:

```text
RootStem              10 accepted, 2 deferred   (P3)
JamidMushtaq           9 accepted, 1 deferred   (P4)
MufradWord             9 accepted               (P5)
VerbalSignified        7 accepted, 2 deferred   (P6)
CompositionReadiness   5 accepted, 2 deferred   (P7)
AmilMamul              3 accepted, 2 deferred   (P8)
```

Per-token — each token drops out at a **distinct** structural criterion:

```text
token   P3    P4    P5    P6    P7    P8     dropped at
شَاذّ   a2    a2    a2    a2    d2    -      P7 (no clean composition boundary)
عَدَّ   a2    a2    a2    a2    a2    d2     P8 (relation-thin: < 3 vowels)
بَ      d1    -     -     -     -     -      P3 (thin root/stem, bare CV)
مَا     a1    d1    -     -     -     -      P4 (1-consonant derivation skeleton)
مِن     d1    -     -     -     -     -      P3 (thin root/stem)
بَاب    a1    a1    a1    d1    -     -      P6 (long-vowel-only, no cadence)
بَيت    a1    a1    a1    d1    -     -      P6 (long-vowel-only, no cadence)
ض       -     -     -     -     -     -      residual (0 slots upstream)
ضَرَبَ  a3    a3    a3    a3    a3    a3     survives all eight gates
```

`a` = accepted, `d` = deferred. Only the richest triliteral-cadence geometry
(`ضَرَبَ`) survives the full ladder; the accepted stream strictly narrows.

## 5. Safety boundary (unchanged)

The landed P3–P8 stack is **candidate-only / potential-only**. It does **not**
emit final judgments for: root, wazn, word, jamid/mushtaq, verb, meaning,
dalalah, syntax, amil/mamul, i'rab, hukm, reality, final meaning. The following
remain **not introduced** anywhere in the pipeline output (verified):

```text
MeaningCandidate · DalalahCandidate · DalalahJudgment · IrabCandidate · Irab
HukmCandidate · RealityClaim · FinalMeaning · all P9+ candidates
```

Each layer's `FORBIDDEN_*` tuple forbids the exact downstream types + the
semantic/judgment absolutes; the kernel enforces the constitutional triple
(`HukmCandidate`/`RealityClaim`/`FinalMeaning`). Registry count stays **19**;
**freeze ACTIVE** for P9–P12 (no P9+ layer implemented).

## 6. Landing record

Merged to `main` bottom-up as a strict stacked chain (one PR per layer):

```text
#160  P3 RootStem                      merge e23bd93
#167  P4 JamidMushtaq                  merge f4dfc71   (supersedes #161)
#162  P5 MufradWord                    merge c7761ac
#163  P6 VerbalSignified               merge f0c984e
#164  P7 CompositionReadiness          merge 6cd824d
#165  P8 AmilMamul (impl + strengthen) merge f725f16
#166  ladder / demo reporting          merge 38c1df5
```

PR **#161** (original P4) was auto-closed when #160's base branch was deleted on
merge and was not reopenable; the identical P4 commit (`76f872e`) was recovered
non-destructively through **#167**. Final `main` HEAD: **`38c1df5`**.

## 7. What this is — and is not

SCG now has a **verified structural cascade** from `RootStemCandidate` through
`AmilMamulCandidate`: each layer reads the previous layer's structural evidence,
applies ACCEPT / DEFER / BLOCK discrimination, and opens only **licensed
downstream priors**. It is a **structural, proof-relevant, potential-only
information-gain pipeline** — not a semantic interpretation engine. It makes no
claim of final linguistic meaning, i'rab, or hukm. SCG-P9 (SentenceGeometry) and
beyond remain SPECIFIED-only and require their own narrow authorization (the
freeze is still ACTIVE).
