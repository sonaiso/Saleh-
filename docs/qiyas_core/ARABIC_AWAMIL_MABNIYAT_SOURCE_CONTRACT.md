# Arabic Awamil and Mabniyat Source Contract

> **Type:** Source-corpus seed contract (docs-only).
>
> **Status:** Preserves the traditional Arabic *awamil* (Jurjani's hundred operators) and *mabniyat* (indeclinable forms) corpus as **future reference material only**. Reserves names. Sketches the length buckets 1–5. Does **not** create a registry, a runtime, an evidence carrier, a `Candidate`, an i'rāb engine, or any operator behaviour.
>
> **Authority basis (read-only citation):**
>
> - `PROJECT_MATHEMATICAL_FOUNDATION.md` §18 (`CompositionAlgebra` / `AmilGeometry`, Layer 10 — the eventual home of operator-related runtime)
> - `SOURCE_OF_TRUTH_REGISTRY.md` (single-source-of-truth discipline for any future registry)
> - `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` (registry/runtime separation discipline)
> - `MIU_VARIANT_RESOLUTION_USAGE_NOTE.md` (post-PR-#84 runtime baseline; this contract does not amend it)
> - `GLYPH_CLASSIFICATION_GATE_CONTRACT.md` (sibling Layer-2 contract; not amended)
> - `SIFAT_VECTOR_CONTRACT.md` (sibling phonetic contract; not amended)
> - `ARABIC_VARIANT_RESOLUTION_CONTRACT.md` + `ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md` (variant layer; not amended)
> - `CLAUDE.md` §0 / §2 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20 / §21

---

## 1. Purpose

This document preserves the classical Arabic *awamil* (governing operators) and *mabniyat* (indeclinable forms) corpus as a **source-corpus seed** for future Layer-10 work. Its purposes are narrow:

- **Record** the traditional taxonomy in a constitutional document so it cannot be lost or silently re-invented.
- **Reserve** the future names `ArabicAmilRegistry` and `ArabicMabniRegistry`.
- **Sketch** the length-bucket structure (1–5 letters) that the future detailed source tables will populate.
- **Forbid**, explicitly and verbosely, any jump from this material into runtime behaviour or higher-layer typed units.

It is **not** a runtime artifact. It does **not**:

- create a registry,
- create a runtime evidence carrier,
- create a `Candidate` of any type,
- introduce a `Qiyas` rule, gate, or wādī claim,
- amend any existing contract or registry,
- change MIU readiness, `ArabicVariantResolver`, `GlyphClassificationGate`, or `SifatVector`,
- decide *i'rāb* (case/mood) for any form,
- decide meaning, *dalālah*, *hukm*, or reality.

The contract follows the docs-first precedent of PRs #71, #72, #78, #79, #84, #85.

---

## 2. Current Project Boundary

After PR #85 merged, the runtime baseline is:

```
origin/main HEAD   = 405a040
PRs #78–#85         = MERGED
Open PR queue       = (this PR adds the only one)
Variant Resolution → MIU integration: complete (manual caller wiring)
GlyphClassificationGate: contract MERGED; runtime NOT implemented
SifatVector: contract MERGED (pre-existing); runtime NOT implemented
Word / Lafz / Dalalah / Meaning / Hukm / Reality: NOT started; standing non-goals
```

This contract sits **strictly inside** that boundary. It does not push the runtime forward by one line.

---

## 3. Source-Corpus Status

The *awamil*/*mabniyat* material recorded (and to-be-recorded) by this contract is **reference material only**. It is **not**:

- a registry runtime,
- a `Candidate` of any type,
- an Evidence carrier (no `AmilSourceEvidence`, no `MabniSourceEvidence` is created),
- a `Qiyas` rule, gate, or claim,
- an admissible input to the MIU readiness predicate,
- an admissible input to the Word/Lafz/Dalalah/Meaning/Hukm/Reality layers (none of which are started),
- an *i'rāb* engine.

A future PR (see §14 / §15 / §26) **may** promote the recorded material into a read-only registry following the precedent of `arabic_articulation_registry.py` and `glyph_classification_registry.py`. Until that PR merges, this document is **the only authority** on the boundary of what may and may not be inferred from the corpus, and the only authority is **negation**: the corpus implies nothing operational.

---

## 4. The One Hundred Awamil

The classical Jurjani split (per the established tradition of *al-Awāmil al-Mi'a*):

```
Total                       100
├─ Lafẓī (لفظية)             98
│   ├─ Samā‘ī (سماعية)        91   — heard / attested; particles and specific
│   │                              forms whose governing effect is fixed by
│   │                              traditional usage, not by analogy
│   └─ Qiyāsī (قياسية)         7   — analogical; categorial forms whose
│                                  governing effect derives from the form-class
└─ Ma‘nawī (معنوية)            2
    ├─ Ibtidā' (الابتداء)            — the operator of mubtada' (raising it
    │                              to nominative)
    └─ Tajarrud al-Muḍāri‘            — the operator of the bare imperfect
       (تجرد المضارع من الناصب         (raising it to indicative when free of
        والجازم)                    a nāṣib or jāzim)
```

**Caveat on names**: this contract reserves only the **structural split** above. It does **not** ratify a definitive enumerated list of the 98 lafẓī or the 7 qiyāsī under this PR. A separate `docs(qiyas_core): define Arabic awamil detailed source table contract` PR (per §26) will populate the detailed tables.

**Illustrative — non-canonical — examples** to make each bucket concrete (these are *not* a registry and may be reordered, renamed, or re-categorised by the detailed table contract):

- Lafẓī samā‘ī examples (illustrative only): `من`, `إلى`, `عن`, `على`, `في`, the *ba'* `ب`, the *kāf* `ك`, the *lām* `ل`, `إنّ`, `أنّ`, `كأنّ`, `لكنّ`, `ليت`, `لعلّ`, `ما`, `لا`, `قد`, `لم`, `لن`, `لو`, `كي`, `حتى`, `إذما`, …
- Lafẓī qiyāsī examples (illustrative only): الفعل، اسم الفاعل، اسم المفعول، الصفة المشبهة، المصدر، اسم التفضيل، اسم الفعل (with some traditional sources counting *al-ẓarf* in this seventh slot instead).
- Ma‘nawī (the two only): الابتداء، تجرّد المضارع من الناصب والجازم.

> **Examples are illustrative, not a canonical registry.** The detailed enumeration belongs to a strictly later contract.

---

## 5. Mabniyat Scope

The *mabniyat* in Arabic grammar are forms whose surface shape is **fixed** (indeclinable) — they do not exhibit *i'rāb* surface change under operator effect. The traditional classes include:

- *al-ḍamā'ir* (pronouns),
- *asmā' al-ishārah* (demonstratives),
- *al-asmā' al-mawṣūlah* (relative nouns),
- *asmā' al-shart wa-l-istifhām* (conditional/interrogative nouns),
- *asmā' al-af‘āl* (verbal nouns of action — e.g., `هَيهات`, `صَه`, `مَه`),
- *al-ḥurūf* (the particles, all of which are indeclinable by nature),
- *al-fi‘l al-māḍī* (the perfect verb, generally indeclinable; some accounts treat it as having a *maḥall* — a position taken in absentia),
- *fi‘l al-amr* (the imperative verb, indeclinable),
- some *fi‘l al-muḍāri‘* forms attached to specific suffixes (e.g., the nūn al-niswah, the heavy/light nūn al-tawkīd), under their traditional conditions.

This contract records the *mabniyat* corpus as a **source of fixed surface forms**, partitioned by length in §§7–11. It does **not**:

- claim that the system "knows i'rāb",
- claim that the system "knows binā'",
- assign any *maḥall* (governed position) to any form,
- declare that a recorded form is in scope for MIU,
- declare that a recorded form has a meaning, a *dalālah*, or a *hukm*.

---

## 6. Length Buckets

The corpus is partitioned into five buckets by **surface character count** (the count is over the raw Arabic letter-glyph code points, harakat excluded, tāʾ marbūṭah counted as one):

```
length_1   — single Arabic letter forms
length_2   — two-letter forms
length_3   — three-letter forms
length_4   — four-letter forms
length_5   — five-letter forms
```

Buckets larger than 5 are out of scope for this seed.

These buckets are **source-corpus-only**. They:

- do NOT alter `SlotGeometryCandidate.length`,
- do NOT alter MIU's `length == 1` admission gate,
- do NOT make `length > 1` admissible in MIU,
- do NOT introduce a new `Candidate` shape,
- do NOT introduce a new evidence carrier.

`length` here is a property of the recorded surface form in the **source corpus**, not a property of any runtime candidate.

---

## 7. One-Letter Forms (length_1)

**Scope**: single Arabic-letter forms — typically the most heavily-used *ḥurūf* and a small set of single-letter mabniyat.

**Illustrative — non-canonical — examples**:

| Surface | Traditional name | Possible category (non-binding) |
|---|---|---|
| `ب` | bā' al-jarr / bā' al-qasam / bā' al-ta‘diyah | lafẓī samā‘ī (jarr) |
| `ل` | lām al-jarr / lām al-amr / lām al-ibtidā' | lafẓī samā‘ī (multi-role) |
| `ك` | kāf al-tashbīh / kāf al-jarr | lafẓī samā‘ī (jarr) |
| `و` | wāw al-‘aṭf / wāw al-qasam / wāw al-ḥāl / wāw al-ma‘iyyah | lafẓī samā‘ī (multi-role); see §22 |
| `ف` | fā' al-‘aṭf / fā' al-sababiyyah | lafẓī samā‘ī |
| `ت` | tā' al-qasam | lafẓī samā‘ī |
| `أ` | hamzat al-istifhām | lafẓī samā‘ī |

**What may be recorded for each entry** (future fields, not implemented now):

- `surface_form`
- `normalized_form` (if licensed by a later normalization contract)
- `traditional_group`
- `possible_awamil_class` ∈ {`lafzi_samai`, `lafzi_qiyasi`, `manawi`, `not_amil`, `unknown`}
- `possible_mabni_category`
- `source_reference`
- `variant_notes`
- `ambiguity_notes`
- `verification_status`

**What must not be inferred from any length_1 entry**:

- no meaning,
- no *i'rāb* effect,
- no *hukm*,
- no `WordCandidate`,
- no `AmilEffectEvidence`,
- no runtime operator,
- no claim that a single letter ⇒ operator (see §13, §24).

A single letter being recorded here does NOT change its MIU status, its variant-resolution status, or its glyph-classification status.

---

## 8. Two-Letter Forms (length_2)

**Scope**: two-letter forms — the bulk of traditional *ḥurūf al-ma‘ānī* and a substantial set of mabniyat.

**Illustrative — non-canonical — examples**:

| Surface | Traditional name | Possible category (non-binding) |
|---|---|---|
| `من` | min al-jārrah | lafẓī samā‘ī (jarr) |
| `إن` | in al-sharṭiyyah | lafẓī samā‘ī (jazm) |
| `أن` | an al-maṣdariyyah | lafẓī samā‘ī (naṣb of muḍāri‘) |
| `لم` | lam al-jāzimah | lafẓī samā‘ī (jazm) |
| `لن` | lan al-nāṣibah | lafẓī samā‘ī (naṣb) |
| `لو` | law al-sharṭiyyah | lafẓī samā‘ī (non-jāzim conditional) |
| `ما` | mā (multi-role: nāfiyah, mawṣūlah, istifhāmiyyah, shartiyyah, …) | lafẓī samā‘ī (multi-role) |
| `لا` | lā al-nāfiyah / lā al-nāhiyah | lafẓī samā‘ī (multi-role) |
| `هل` | hal al-istifhāmiyyah | lafẓī samā‘ī |
| `قد` | qad (verbal particle) | lafẓī samā‘ī |
| `هو` / `هي` / `أنا` / `أنت` | core pronouns | mabnī (ḍamīr) |

**What may be recorded**: same field set as §7.

**What must not be inferred**:

- a two-letter surface form does NOT become a `WordCandidate`,
- does NOT acquire *i'rāb* effect at this layer,
- does NOT acquire `AmilEffectEvidence`,
- does NOT alter any MIU decision (MIU's gates remain unchanged — see §19),
- being attestable as multi-role (e.g., `ما`, `لا`) does NOT trigger a tie-breaking or priority algorithm at this layer; tie-breaking is forbidden by the variant-layer non-goals and that prohibition extends here.

---

## 9. Three-Letter Forms (length_3)

**Scope**: three-letter forms — including several *ḥurūf mushabbihah bi-l-fi‘l*, conditional particles, and a number of mabniyat.

**Illustrative — non-canonical — examples**:

| Surface | Traditional name | Possible category (non-binding) |
|---|---|---|
| `إنّ` | inna (mushabbihah bi-l-fi‘l) | lafẓī samā‘ī (naṣb of ism, raf‘ of khabar) |
| `أنّ` | anna (mushabbihah bi-l-fi‘l) | lafẓī samā‘ī |
| `ليس` | laysa (mā kāna wa-akhawātuhā) | lafẓī samā‘ī (raf‘ of ism, naṣb of khabar) |
| `كان` | kāna (mā kāna wa-akhawātuhā) | lafẓī samā‘ī |
| `هذا` / `هذه` / `ذاك` | demonstratives (some are three-letter) | mabnī (ism ishārah) |
| `الذي` | al-ladhī (relative — surface 4 letters with article; the bare form is `ذي`/`ذو` in some accounts) | mabnī (ism mawṣūl); see length_4 |
| `كلا` | kalā (deterrent particle) | lafẓī samā‘ī |
| `أين` | ayna (interrogative) | mabnī (ism istifhām) |

**What may be recorded**: same field set as §7.

**What must not be inferred**:

- a three-letter form being attested as an operator (e.g., `إنّ`) does NOT mean the runtime has any "inna operator" — no such operator exists in any layer below #85,
- attestability is not a proof of MIU acceptance or of any downstream effect.

---

## 10. Four-Letter Forms (length_4)

**Scope**: four-letter forms — including several mushabbihah, some conditional particles, and named mabniyat.

**Illustrative — non-canonical — examples**:

| Surface | Traditional name | Possible category (non-binding) |
|---|---|---|
| `لكنّ` | lākinna (mushabbihah) | lafẓī samā‘ī |
| `كأنّ` | ka'anna (mushabbihah) | lafẓī samā‘ī |
| `ليت` | layta (mushabbihah) | lafẓī samā‘ī |
| `لعلّ` | la‘alla (mushabbihah) | lafẓī samā‘ī (note: `لعل` is 3 letters, `لعلّ` with shaddah is structurally 4) |
| `الذي` | al-ladhī (relative noun, with definite article) | mabnī (ism mawṣūl) |
| `التي` | al-latī | mabnī (ism mawṣūl) |
| `إذما` | idhmā (sharṭiyyah) | lafẓī samā‘ī |
| `حيث` | ḥaythu (ẓarf makān) | mabnī (ẓarf) |

**What may be recorded**: same field set as §7.

**What must not be inferred**: same negations as §§7–9. In particular, a recorded *mushabbihah bi-l-fi‘l* in length_4 does NOT trigger any *i'rāb* assignment, does NOT change MIU behaviour, and is NOT an `AmilEffectEvidence` source.

---

## 11. Five-Letter Forms (length_5)

**Scope**: five-letter forms — generally rarer; includes some mushabbihah with affixed particles, some *asmā' al-af‘āl*, and some compound mabniyat.

**Illustrative — non-canonical — examples**:

| Surface | Traditional name | Possible category (non-binding) |
|---|---|---|
| `ليتما` | laytamā (layta + mā al-kāffah) | lafẓī samā‘ī; see notes |
| `لعلّما` | la‘allamā | lafẓī samā‘ī |
| `كأنّما` | ka'annamā | lafẓī samā‘ī |
| `إنّما` | innamā (inna + mā al-kāffah) | lafẓī samā‘ī |
| `أنّما` | annamā | lafẓī samā‘ī |
| `هَيهات` | hayhāta (ism fi‘l) | mabnī (ism fi‘l) |

**What may be recorded**: same field set as §7.

**What must not be inferred**: same negations as §§7–10. The mā al-kāffah affixed to a *mushabbihah* is a traditional grammatical fact; recording it as a five-letter surface form does NOT mean the runtime knows that the *mushabbihah* has been "neutralised" — that semantic claim is a downstream operator-layer question that is **not started**.

---

## 12. What May Be Recorded

The future detailed source tables (per §26 follow-up PRs) will admit the following field set per entry. This contract reserves the **field names**; it does **not** create the schema.

```text
source_id              : str   — stable identifier within the source table
surface_form           : str   — the Arabic surface form, normalized to NFC
length_bucket          : int   — 1..5 (per §6)
traditional_group      : str   — e.g., "ḥarf jarr", "mushabbihah",
                                 "ism ishārah", "ism mawṣūl", "ḍamīr",
                                 "fi‘l māḍī", …
awamil_class           : str   — one of:
                                   "lafzi_samai"   (91)
                                   "lafzi_qiyasi"  (7)
                                   "manawi"        (2)
                                   "not_amil"      (e.g., pure mabnī
                                                    without operator role)
                                   "unknown"       (pending verification)
mabni_category         : str | None — sub-classification within mabniyat
                                       if applicable; otherwise None
source_reference       : str   — citation placeholder (e.g.,
                                 "Jurjani — al-Awamil al-Mi'a §<n>")
variant_notes          : str   — surface variants, attested orthographies,
                                 dialectal notes if recorded
ambiguity_notes        : str   — multi-role notes (e.g., `ما` is mawṣūlah
                                 OR sharṭiyyah OR nāfiyah …); the note
                                 records the alternatives, NOT a decision
verification_status    : str   — one of:
                                   "pending"
                                   "verified_one_source"
                                   "verified_multiple_sources"
```

These fields are **conceptual reservations**. No runtime dataclass exists.

---

## 13. What Must Not Be Inferred

The following inferences are **forbidden** under this contract — from the source corpus, from any individual entry, and from any cross-cutting query:

- *form* ⇒ *word*
- *form* ⇒ *meaning*
- *form* ⇒ *i‘rāb effect*
- *form* ⇒ *hukm*
- *form* ⇒ *reality claim*
- *form* ⇒ *MIU acceptance*
- *form* ⇒ `AmilEffectEvidence`
- *form* ⇒ `I‘rabEffectEvidence`
- *source corpus* ⇒ *registry runtime*
- *traditional taxonomy* ⇒ *proof*

The corpus is **descriptive**, not **operational**. It records what tradition says exists; it does not authorise any system to act on it.

---

## 14. Future ArabicAmilRegistry

This contract **reserves** the future name:

```
ArabicAmilRegistry
```

`ArabicAmilRegistry` is **not implemented**. It is **not created** by this PR. It is **not** a source of runtime truth yet.

A strictly later docs-only contract MAY define its read-only schema, mirroring the precedent of `arabic_articulation_registry.py` (which is metadata-only and read-only). Even after such a registry exists, its outputs MUST remain metadata: they MAY support later evidence but MUST NOT license any algebraic transition by themselves.

The registry name is reserved-by-name; the eventual module path (non-binding) is:

```
src/qiyas_core/registries/arabic_amil_registry.py
```

---

## 15. Future ArabicMabniRegistry

This contract **reserves** the future name:

```
ArabicMabniRegistry
```

`ArabicMabniRegistry` is **not implemented**. It is **not created** by this PR.

The same discipline as §14 applies: read-only metadata only; no algebraic licensing by itself; reserved-by-name; non-binding eventual path:

```
src/qiyas_core/registries/arabic_mabni_registry.py
```

---

## 16. Future OperatorGeometry

Operator geometry — the eventual runtime layer that consumes operator-effect evidence and produces composition candidates — belongs to **Layer 10 (`CompositionAlgebra`)** per `PROJECT_MATHEMATICAL_FOUNDATION.md` §18.

This contract:

- does **not** define `OperatorGeometry`,
- does **not** start any Layer 10 work,
- does **not** authorise any operator runtime,
- explicitly defers operator runtime to a strictly later set of PRs that must each pass their own preflight review.

`OperatorGeometry` requires, as prerequisites, **all** of: WordFormAlgebra (Layer 8), LexicalMadlulAlgebra (Layer 9), and finally CompositionAlgebra itself. None of those layers have started. Trying to start operator geometry now would be a multi-layer jump and is forbidden by CLAUDE.md §4 invariant 10.

---

## 17. Future AmilEffectEvidence

This contract **reserves** the future name:

```
AmilEffectEvidence
```

`AmilEffectEvidence` is the eventual Evidence carrier that would record "operator `X` exerted effect `Y` on target `Z` under condition `C`". It is **not implemented**. It is **not created** by this PR.

When (much) later defined, it MUST follow the **Evidence-carrier-not-Candidate** pattern fixed by PR #72 / #80 / #85: frozen dataclass, no `candidate_type` / `status` / `output_flags` fields.

---

## 18. Future I‘rabEffectEvidence

This contract **reserves** the future name:

```
I‘rabEffectEvidence
```

`I‘rabEffectEvidence` is the eventual Evidence carrier that would record the case/mood outcome of operator application. It is **not implemented**. It is **not created** by this PR. The same Evidence-carrier-not-Candidate discipline applies.

The two carriers — `AmilEffectEvidence` and `I‘rabEffectEvidence` — are logically distinct:

- `AmilEffectEvidence` answers "did the operator apply?",
- `I‘rabEffectEvidence` answers "what is the resulting case/mood mark on the target?".

Both are deferred to strictly later contracts and PRs. Neither is operative anywhere in the current codebase.

---

## 19. Relationship to MIU

- The MIU readiness layer (`MinimalIndependentUnitReadinessLayerAdapter`, PRs #75 / #82) **does not change** as a result of this contract.
- All MIU gates remain in force: `length == 1`, `construction_mode == "seed"`, closure evidence present, registry eligibility, output flags ⊆ `{CandidateOnly}`.
- A surface form being recorded in §§7–11 does **not** alter its MIU status.
- `بِ` may already be ACCEPTED at MIU (single-variant, registry-eligible) — that does **not** mean the system "knows" `بِ` is a `ḥarf jarr` operator.
- `وَ` may already become ACCEPTED at MIU when a caller threads a valid resolver evidence (per PR #84 §5) — that does **not** mean the system "knows" `وَ` is `wāw al-‘aṭf` or `wāw al-qasam` or any other operator role.
- `ضَرَبَ` remains BLOCKED at MIU because `length > 1` and `construction_mode == "extension"`. That gate is **not** relaxed by recording `ضرب` as a verbal form in the source corpus.

The MIU output remains `MinimalUnitReadinessCandidate` with `output_flags == {CandidateOnly}` in every case. **No operator semantics leak into MIU.**

---

## 20. Relationship to GlyphClassificationGate

- The `GlyphClassificationGate` contract (PR #85) **does not change** as a result of this contract.
- Operators and mabniyat are **not** glyph classes. The eight canonical labels reserved by PR #85 §6 (`CoreArabicLetter`, `StandaloneHamza`, `HamzaSeatGlyph`, `WeakLetterGlyph`, `TatweelGlyph`, `OrthographicVariant`, `ComplexGlyph`, `Punctuation`) classify codepoints under script/orthography; this contract classifies surface forms under a separate, higher-level grammatical tradition.
- A future `GlyphClassificationEvidence` runtime carrier (when its docs-only contract lands) does NOT carry operator information and does NOT inform this corpus.
- This contract does NOT add `MaddGlyph` / `Boundary` / `Residual` (PR #85 §7 deferred) and does NOT touch the glyph registry.

---

## 21. Relationship to SifatVector

- `SIFAT_VECTOR_CONTRACT.md` (existing, merged) **does not change** as a result of this contract.
- Operators and mabniyat are **not** phonetic vectors. The 6-axis `SifatVector` classifies a *letter's* phonetic discrimination axes; this contract classifies *surface forms* under grammatical tradition.
- The two corpora may, **much later**, become composed at a higher layer (e.g., a *kāf* operator's phonetic identity informs morphophonological behaviour) — but that composition is a strictly later constitutional concern and is **not authorised by this contract**.

---

## 22. Relationship to ArabicVariantResolver

- `ArabicVariantResolver` (PR #81) **does not change** as a result of this contract.
- The variant-resolution layer answers "is this `و` a *madd* or a *non-madd*?" — a script/glyph-level question.
- The fact that a `و` surface form *may* appear in this corpus as `wāw al-‘aṭf`, `wāw al-qasam`, `wāw al-ḥāl`, `wāw al-ma‘iyyah`, etc. does **not** resolve the variant question. The variant question is a strictly lower-level discrimination (madd vs. non-madd) and its answer is independent of the operator role.
- This contract does **not** introduce a "wāw role" disambiguation. Such disambiguation would belong to a much-later `RoleDisambiguationGate` contract (per `PROJECT_MATHEMATICAL_FOUNDATION.md` §13) and is **not started**.

---

## 23. Relationship to Word / Dalalah / Meaning / Hukm / Reality

This contract **does not start**, **does not authorise**, **does not imply**, and **does not pave the way for**:

- `WordCandidate`,
- `LafzCandidate`,
- `DalalahCandidate`,
- `FinalMeaning`,
- `HukmCandidate`,
- `RealityClaim`,
- `FinalCaseJudgment`,
- `MinimalIndependentMeaningCandidate`,
- any `Sentence*` / `Discourse*` / `Text*` geometry,
- any `Composition*` / `Style*` / `Ifādah*` / `Tanzīl*` runtime.

Every traditional fact recorded in §§4–11 is a fact **about the source**, not a step toward word, meaning, or hukm. The traditional taxonomy is **not a proof**. A future PR proposing a runtime that consumes this corpus as proof of meaning would violate CLAUDE.md §4 invariants 6, 9, and 10 and would have to be rejected at preflight.

---

## 24. Forbidden Jumps

The following transitions are **explicitly forbidden** under this contract — at the source-entry level, at the corpus-query level, and at the contract-citation level:

```
AwamilSourceEntry      →  WordCandidate                       ❌
AwamilSourceEntry      →  LafzCandidate                       ❌
AwamilSourceEntry      →  DalalahCandidate                    ❌
AwamilSourceEntry      →  FinalMeaning                        ❌
AwamilSourceEntry      →  HukmCandidate                       ❌
AwamilSourceEntry      →  RealityClaim                        ❌
AwamilSourceEntry      →  FinalCaseJudgment                   ❌
AwamilSourceEntry      →  AmilEffectEvidence                  ❌
AwamilSourceEntry      →  I‘rabEffectEvidence                 ❌
MabniSourceEntry       →  WordCandidate                       ❌
MabniSourceEntry       →  I‘rabEffectEvidence                 ❌
MabniSourceEntry       →  any Candidate                       ❌
length bucket          →  MIU acceptance                      ❌
length_1 entry         →  operator runtime                    ❌
length_2 entry         →  operator runtime                    ❌
length_3 entry         →  operator runtime                    ❌
length_4 entry         →  operator runtime                    ❌
length_5 entry         →  operator runtime                    ❌
source corpus          →  runtime registry                    ❌
awamil class           →  i‘rāb effect                        ❌
mabni label            →  syntactic role decision             ❌
traditional name       →  proof                               ❌
source corpus          →  ArabicVariantResolver decision      ❌
source corpus          →  MIU decision                        ❌
source corpus          →  GlyphClassificationGate decision    ❌
```

The corpus is metadata about tradition. It is not, and cannot become, a source of operational truth without a separate explicit constitutional amendment.

---

## 25. Non-Goals

This PR is **docs-only** and explicitly does not include, propose, or imply:

- no code (no `src/` change)
- no tests (no `tests/` change)
- no runtime (no Evidence carrier, no `Candidate`, no rule, no gate)
- no registry (no `arabic_amil_registry.py`, no `arabic_mabni_registry.py`)
- no source module of any kind
- no `__init__.py` change
- no `run_qiyas.py` change
- no `experimental/` change
- no `ArabicAmilRegistry` implementation
- no `ArabicMabniRegistry` implementation
- no `OperatorGeometry` implementation
- no `AmilEffectEvidence` runtime
- no `I‘rabEffectEvidence` runtime
- no `WordCandidate` / `LafzCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`
- no `SentenceCandidate` / `ParagraphCandidate` / `SentenceGeometry` / `DiscourseGeometryCandidate` / `TextGeometryCandidate`
- no `MinimalIndependentMeaningCandidate`
- no `CompositionAlgebra` runtime
- no `Amil` layer runtime
- no change to MIU adapter or MIU rule
- no change to `ArabicVariantResolver`
- no change to `GlyphClassificationGate` contract
- no change to `SIFAT_VECTOR_CONTRACT.md`
- no change to `arabic_articulation_registry.py` or `glyph_classification_registry.py`
- no claim that traditional taxonomy is proof
- no claim that recording implies licensing
- no priority / tie-breaking algorithm at the awamil level
- no sibling-context pipeline amendment
- no alif semantics
- no `default_variant` field
- no detailed enumerated list of the 98 lafẓī or 7 qiyāsī (deferred to §26 follow-up)

---

## 26. Future Work

The following are **safe future PRs** that may be opened later, each under its own explicit trigger:

1. **`docs(qiyas_core): define Arabic awamil detailed source table contract`** — populates the per-entry table for the 98 lafẓī (91 samā‘ī + 7 qiyāsī) and the 2 ma‘nawī under a strict citation discipline.
2. **`docs(qiyas_core): define Arabic mabniyat detailed source table contract`** — populates the per-entry table for the mabniyat classes.
3. **`docs(qiyas_core): define Arabic operator geometry contract`** — only after Layer 6 (Syllable), Layer 7 (Stem/Root), Layer 8 (WordForm), and Layer 9 (LexicalMadlul) have at least their contracts merged; defines the eventual operator-runtime shape.
4. **`docs(qiyas_core): define AmilEffectEvidence contract`** — pins the Evidence carrier shape for the eventual operator-effect carrier.
5. **`docs(qiyas_core): define I‘rabEffectEvidence contract`** — same for the case/mood carrier.
6. **Much later only**: runtime carriers and producers under their own contracts.

What is **explicitly not** recommended next:

- starting any rejected item in §25,
- promoting the corpus into a runtime registry before the detailed source-table contracts merge,
- introducing operator runtime before its own contract is merged,
- introducing `WordCandidate` / `DalalahCandidate` / `FinalMeaning` / `HukmCandidate` / `RealityClaim` / `FinalCaseJudgment`,
- starting `CompositionAlgebra`, `StyleTemplateAlgebra`, `IfādahCandidate`, `HukmCandidate`, or `Truth/Evidence/Reality Grounding`.

---

## 27. Summary Table

| Question | Answer |
|---|---|
| Is this runtime? | No. Docs-only source-corpus seed. |
| Does it change MIU? | No. |
| Does it change `ArabicVariantResolver`? | No. |
| Does it change `GlyphClassificationGate` contract? | No. |
| Does it change `SIFAT_VECTOR_CONTRACT.md`? | No. |
| Does it create `ArabicAmilRegistry`? | No — reserved-by-name only. |
| Does it create `ArabicMabniRegistry`? | No — reserved-by-name only. |
| Does it create `AmilEffectEvidence` / `I‘rabEffectEvidence`? | No — reserved-by-name only. |
| Does it classify words? | No. |
| Does it produce meaning? | No. |
| Does it produce *i‘rāb* effect? | No. |
| Does it produce *hukm*? | No. |
| Does it start `WordCandidate` / `DalalahCandidate`? | No. |
| What does it preserve? | The source-corpus boundary: 91 lafẓī samā‘ī + 7 lafẓī qiyāsī + 2 ma‘nawī = 100 awamil; mabniyat by length 1–5. |
| What is next? | A docs-only detailed source-table contract (see §26 item 1). |

---

**Document version:** 1.0
**Last updated:** 2026-06-05
**Status:** Source-corpus seed contract (docs-only).
**Authority:** Subordinate to `PROJECT_MATHEMATICAL_FOUNDATION.md` §18 for layer position, to `RECURSIVE_LICENSED_EXTENSION_CONTRACT.md` and `SOURCE_OF_TRUTH_REGISTRY.md` for registry discipline, and to `CLAUDE.md` §0–§21 for the governing project discipline. Does not amend any of them.
