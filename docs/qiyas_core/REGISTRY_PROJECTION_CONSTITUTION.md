# REGISTRY_PROJECTION_CONSTITUTION — SCG-P2 (specification only)

> **Status:** Constitutional **specification** for the canonical SCG-P2 layer.
> Authored under the **narrow SCG-P2-only spec-authoring authorization
> (2026-06-15)**. SPEC ONLY — **no runtime, no adapter, no IMPLEMENTED status.**
> Transition authored: `PLANNED → SPECIFIED` via `build_p2_specified_registry`.
>
> **SCG-P2 Semantic Fixation (2026-06-17, documentation only).** §§9–12 below fix
> the *structural* meaning of `registry_entry_ref` and `membership_prior_type`
> BEFORE any P2 runtime, so P2 is a real algebraic layer — "projection of slot
> geometry onto registry membership classes" — and not a name wrapper. Still
> SPEC/doc-only: no runtime, no `build_p2_implemented_registry`, no status change.
>
> **Authority:** `PROJECT_RECOVERY_CANONICAL_MAP.md` §4 (canonical phases) / §7
> (REC queue) / §8 (supreme law); `LAYER_REGISTRY.md`; the SCG-P2-only
> authorization. Canonical registry track only — **not** the runtime syllable
> track (`LicensedSyllableCandidate` etc., a different numbering — do not
> conflate runtime Layer N with SCG-Pn).

---

## 1. Identity

| Field | Value |
| --- | --- |
| Layer id | `P2_REGISTRY_PROJECTION` |
| LayerSpec name | `RegistryProjectionLayer` |
| Phase | `SCG-P2` |
| Output type | `RegistryProjectionCandidate` |
| Origin (الأصل) | الأصل الثاني — verbal-transition system (Saleh- algebraic spine) |
| Status | `SPECIFIED` (via `build_p2_specified_registry`); P3–P12 remain `PLANNED` |

## 2. Role (الفرع وسببه)

SCG-P2 **projects a licensed `SlotCandidate` onto the relevant phase registry
to OPEN potential morphological/syntactic priors** — *"Prior لا Judgment."* It
is a **candidate-only** projection. It opens hypotheses; it does not decide them.

```
شرط التفريع: قابلية مرشح الخانة للإسقاط على سجل ترخيص لفتح Prior لا Judgment.
```

## 3. Upstream evidence (consumed)

Per §8 ("a layer consumes only the licensed output of its immediate
predecessor"), SCG-P2's **direct input is `SlotCandidate`** (origin =
`P1_SLOT_CANDIDATE`). `SlotCandidate` is itself the licensed convergence of the
SCG-P1 atomic/sequence proofs, whose identities it preserves and which P2 may
reference only through it:

- `SlotCandidate` (direct input)
- `LetterIdentityCarrier` — via SlotCandidate's preserved identity refs
- `HarakaMarkIdentityCarrier` — via SlotCandidate's preserved identity refs
- `PositionCarrier` — via SlotCandidate
- `ConditionedTypedSequence` / `AlignmentEvidence` — via SlotCandidate
- residual / boundary evidence — as already preserved upstream

P2 does **not** re-derive any P1 identity; it consumes the converged
`SlotCandidate` and preserves `slot_candidate_identity`.

## 4. Allowed output

- **`RegistryProjectionCandidate` only.** Nothing else.

## 5. Forbidden outputs (exact downstream canonical names + absolutes)

P2 must NOT produce any downstream output type (no-jump), nor any final
semantic/judgment artifact:

```text
RootStemCandidate            (SCG-P3)
JamidMushtaqCandidate        (SCG-P4)
MufradWordCandidate          (SCG-P5)
VerbalSignifiedCandidate     (SCG-P6)
CompositionReadinessCandidate(SCG-P7)
AmilMamulCandidate           (SCG-P8)
SentenceGeometryCandidate    (SCG-P9)
RelationGeometryCandidate    (SCG-P10)
IrabGeometryCandidate        (SCG-P11)
IfadahCandidate              (SCG-P12)
HukmCandidate · RealityClaim · FinalMeaning   (absolute — every layer)
```

Also forbidden as *claims/changes*: meaning, dalalah, tafsir, i'rab judgment,
root, wazn, wordhood, grammar, hukm, semantic runtime (`forbidden_changes =
assign_root / assign_meaning / assign_irab`).

## 6. No-jump discipline

- `target_boundary_opens = (root_stem_candidates, word_type_priors)` — these are
  **opened as priors for SCG-P3**, never **produced** by P2.
- `forbidden_direct_next_layer_ids = (SCG-P6, SCG-P8, SCG-P12)`.
- Downstream output types are in `forbidden_outputs` (§5).
- P3 (`RootStemCandidate`) has `origin = RegistryProjectionCandidate`, so any
  `SCG-P1 → SCG-P3` path necessarily skips P2 and is structurally invalid.

## 7. Invariants preserved (spec level)

- **Identity ≠ trace; identity not consumed:** `preserves_ids =
  slot_candidate_identity`.
- **Explicit residuals / no silent failure:** `blockers =
  (slot_candidate_blocked,)`; `invalidating_differences =
  (registry_membership_conflict,)`.
- **Candidate-only, not final judgment:** output is a `…Candidate`; absolutes
  forbidden; "Prior لا Judgment."
- **No semantic / no root-wazn-word / no i'rab:** §5 forbidden outputs + changes.
- **Rank meet / potential-only:** no rank upgrade; nothing promoted.

## 8. Status discipline

- `build_p2_specified_registry` advances **only P2** `PLANNED → SPECIFIED`
  (building on `build_p1_specified_registry`); P3–P12 stay `PLANNED`; layer
  count stays **19**.
- **No `build_p2_implemented_registry`.** `IMPLEMENTED` is **not** authorized
  while the global REC freeze is ACTIVE; advancing P2 to `IMPLEMENTED` requires
  a separate, explicit, narrow authorization (and P1 IMPLEMENTED first).

Enforced by `tests/qiyas_core/test_master_registry_p2_specified.py` (`P2-SPEC-*`).

---

## 9. Structural semantics of `registry_entry_ref` and `membership_prior_type` (Semantic Fixation)

SCG-P2 answers exactly **one** question:

> **"To which registered *structural* membership class(es) could this geometry of
> `SlotCandidate`s belong?"**

It is a **projection of slot geometry onto registry membership classes** — nothing
more. The two carried fields are defined **structurally**, never linguistically:

### 9.1 `registry_entry_ref`
A reference to a **registered structural-class entry** whose membership
conditions the slot-sequence geometry satisfies. The match is computed **purely
from structure carried up through `SlotCandidate`** — never from a lexicon,
root table, or morphological pattern. A structural class is characterised by
**property dimensions only** (not by a coined name):

| Property dimension | Structural source (P0/P1) |
| --- | --- |
| **Slot count** | number of `SlotCandidate`s in the sequence |
| **CV signature** | the licensed cell shapes (CV / CVV / CVC / CVVC / CVCC / CVVCC) |
| **Boundary profile** | open vs closed final, tokenizer-segment framing |
| **Gemination profile** | shadda (U+0651) present / absent (trace-level if expanded) |
| **Long-vowel profile** | presence/position of long vowels (alif/waw/yaa as madd) |
| **Alignment profile** | carrier-binding evidence pattern across the sequence |

> **No registry of structural classes is established yet.** Therefore this
> document **coins NO class names** (no `CLASS_X`, no `CLASS_Y`). A `registry_entry_ref`
> points to *one or more registered structural classes whose membership
> conditions are stated as the property combination above* — the concrete
> registry is a later, separately-authorized artifact.

### 9.2 `membership_prior_type`
The **type/label of the structural-membership *prior*** opened by the projection
— a prior that *licenses* downstream root/stem and word-type **hypotheses**, never
a decision.

> **Hard constraint:** `membership_prior_type` **is NOT a linguistic category.
> It is a structural registry category.**
>
> - **Forbidden values:** `Verb`, `Noun`, `Particle`, `Derived`, `Jamid`,
>   `Root`, `Wazn`, or any morphological/lexical/grammatical label — these would
>   leak الأصل الثالث (root/word/meaning) into P2 prematurely.
> - **Allowed value-shapes (structural only):** e.g.
>   `StructuralMembershipClass`, `StructuralMembershipPrior`,
>   `GeometryMembershipClass` — labels that name a *geometry membership*, not a
>   linguistic identity.

## 10. Worked structural examples (conditions only — no class names, no root/wazn/meaning)

Each example states **only** the structural membership *conditions*; it assigns
no class name, no root, no wazn, no word, no meaning.

- **شَاذّ** → projects onto one or more registered structural classes whose
  membership conditions include: **gemination present** (U+0651, trace
  `شَاذّ → شَاذْذ`), **long-vowel present** (alif), **final closed boundary**
  (covering shape `CVVCC`), **slot count = 2**.
- **ضَرَبَ** → projects onto one or more registered structural classes whose
  membership conditions include: **no gemination**, **no long vowel**, **all-open
  CV cells** (`CV/CV/CV`), **slot count = 3**.
- **بَاب** → projects onto one or more registered structural classes whose
  membership conditions include: **no gemination**, **long-vowel present** (medial
  alif), **final closed boundary** (covering shape `CVVC`), **slot count = 1**.

In every case the output is a `RegistryProjectionCandidate` (candidate-only),
preserving `slot_candidate_identity`, opening `root_stem_candidates` /
`word_type_priors` as **priors**, and emitting **no** downstream candidate.

## 11. Non-goals of P2 (mandatory)

SCG-P2 does **NOT** answer any of the following:

```text
ما الجذر؟              (what is the root?)
ما الوزن؟              (what is the wazn / morphological pattern?)
هل الكلمة جامدة أم مشتقة؟ (is the word jamid or mushtaq?)
هل هي اسم أم فعل؟       (is it a noun or a verb?)
ما المعنى؟             (what is the meaning / dalalah?)
ما الإعراب؟            (what is the i'rab?)
ما الحكم؟              (what is the hukm?)
```

It answers **only**:

```text
ما هي العضويات البنيوية المحتملة التي يمكن أن تنتمي إليها
هذه الهندسة المكوّنة من SlotCandidates؟
(which potential STRUCTURAL memberships could this geometry of SlotCandidates belong to?)
```

Any value or output that answers a non-goal question is a constitutional
violation, regardless of tests.

## 12. Target tool output after P2 (`tools/qiyas_scg_ladder_state.py`)

When P2 is later implemented, the ladder tool must show (for شَاذّ):

```text
شَاذّ

LetterIdentityCarrier .......... 3
HarakaMarkIdentityCarrier ...... 2
ConditionedTypedSequence ....... OK
PositionCarrier ................ 3
SlotCandidate .................. 2

RegistryProjectionCandidate .... 1

Opened priors:
- root_stem_candidates
- word_type_priors

RootStemCandidate .............. not_introduced
JamidMushtaqCandidate .......... not_introduced
MufradWordCandidate ............ not_introduced
Meaning ........................ not_introduced
Hukm ........................... not_introduced
```

That is: P1 ladder counts, then **`RegistryProjectionCandidate` count + the
opened structural priors**, with `RootStemCandidate` and everything above still
**`not_introduced`** — the rising SCG candidate ladder, layer after layer,
without any early semantic/morphological leak.
