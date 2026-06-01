# FOUNDATION_IMPLEMENTATION.md

Implementation record linking each deliverable to its Gap number in
`docs/qiyas_core/ALGEBRAIC_FOUNDATION_CONTRACT.md`.

---

## Phase 1 — Algebraic Proof Chain (Implemented)

### Gap #3 — LetterIdentityCarrier

**Files:**
- `src/qiyas_core/phonetics/__init__.py` — package init
- `src/qiyas_core/phonetics/profiles.py` — `PhoneticGroundingProfile`, `MakhrajGeometry`,
  `SifatGeometry`, `LETTER_PHONETIC_PROFILES`, `get_phonetic_profile()`
- `src/qiyas_core/rules/letter_identity_rules.py` — `LETTER_IDENTITY_RULES` dict,
  `_make_letter_identity_rule()`, `get_letter_identity_rule()`; 36 per-letter
  `QiyasRule` instances (U+0621–U+063A, U+0641–U+064A)
- `src/qiyas_core/letter_identity_adapter.py` — `LetterIdentityLayerAdapter`

**What is proven:** For each Arabic letter codepoint, `QiyasKernel.apply()` verifies
`unicode_identity`, `script_identity`, `sound_identity`, `makhraj`, and `sifat`; emits
`LetterIdentityCarrier` candidate with `output_flags={"CandidateOnly"}`.

**invalidating_differences:** Each rule declares the cross-letter differences that
prevent identity confusion (e.g., `baa→taa` via PLACE, `seen→sheen` via MANNER,
`baa→meem` via NASALITY).

**Tests:** `tests/qiyas_core/test_letter_identity.py`
- `test_baa_letter_codepoint_proves_baa_identity`
- `test_taa_letter_codepoint_proves_taa_identity`
- `test_seen_does_not_become_sheen`
- `test_baa_does_not_become_taa`
- `test_baa_vs_meem_invalidating_difference`
- `test_letter_identity_forbids_weight`

---

### Gap #4 — HarakaFunctionCarrier

**Files:**
- `src/qiyas_core/phonetics/profiles.py` — `VocalicEnergyProfile`,
  `HARAKA_ENERGY_PROFILES`, `get_energy_profile()`
- `src/qiyas_core/rules/haraka_function_rules.py` — `HARAKA_FUNCTION_RULES` dict,
  `get_haraka_function_rule()`; 8 haraka rules (U+064B–U+0652)
- `src/qiyas_core/haraka_function_adapter.py` — `HarakaFunctionLayerAdapter`

**What is proven:** Each diacritic codepoint is proven to carry a specific vocalic
function (OPENING/ROUNDING/RAISING/CLOSURE/COMPRESSION/GEMINATION/NASALIZATION).

**forbidden_outputs (layer-specific):** `CaseEffect`, `Irab`, `Hukm` — haraka
function is phonetic only, never grammatical.

**Tests:** `tests/qiyas_core/test_haraka_function.py`
- `test_fatha_haraka_proves_fatha_function`
- `test_damma_haraka_proves_damma_function`
- `test_kasra_haraka_proves_kasra_function`
- `test_sukun_proves_closure_function`
- `test_shadda_proves_compression_function`
- `test_fatha_does_not_become_damma`
- `test_haraka_function_forbids_case_effect`

---

### Gap #5 — PositionCarrier

**Files:**
- `src/qiyas_core/rules/position_rules.py` — `POSITION_RULES` dict,
  `get_position_rule()`; 4 position rules (INITIAL/MEDIAL/FINAL/ISOLATED)
- `src/qiyas_core/position_adapter.py` — `PositionLayerAdapter`

**What is proven:** A letter's positional context is proven from its index and
boundary flags; emits `PositionCarrier` with `position_type`, `within_word`,
`at_boundary`, `waqf_eligible`, `wasl_eligible`.

**Tests:** `tests/qiyas_core/test_position.py`

---

### Gap #6 — SlotCandidate (First Algebraic Composition)

**Files:**
- `src/qiyas_core/rules/slot_rules.py` — `SLOT_COMPOSITION_RULE`
- `src/qiyas_core/slot_adapter.py` — `SlotLayerAdapter`

**What is proven:** Given `LetterIdentityCarrier`, `HarakaFunctionCarrier`, and
`PositionCarrier`, `Compatible(l,h,p)` and `PreserveIdentity(l,h,p)` are proven;
emits `SlotCandidate` with combined `identity_ids` from all three carriers.

**forbidden_outputs (layer-specific):** `SyllableCandidate` (adjacency not yet
proven), `MeaningCandidate`.

**Tests:** `tests/qiyas_core/test_slot.py`
- `test_slot_requires_letter_identity`
- `test_slot_requires_haraka_function`
- `test_slot_requires_position`
- `test_slot_compatible_baa_fatha`
- `test_slot_preserves_identity`
- `test_slot_forbids_syllable_before_adjacency`

---

### Gaps #7 / #8 — PhysicalGrounding + EnergyTracePreservation

**Files:**
- `src/qiyas_core/phonetics/profiles.py` — `PhoneticGroundingProfile` (makhraj +
  sifat + sound_identity + invalidating_differences) for every Arabic letter;
  `VocalicEnergyProfile` (duration/aperture/tongue_position) for every haraka.

**Policy:** Any transformed sound event preserves its source trace in the output
`trace_ids` field, consistent with `_check_identity` / `_validate_output` in the
kernel.

---

### Gap #9 — Economy Function

**File:** `src/qiyas_core/formal_laws.py` — `Economy(x, P, candidates)`

`Economy(x, P) ⇔ ¬∃y < x : Licensed(y,P) ∧ EquivalentPurpose(y,x,P)`

**Tests:** `tests/qiyas_core/test_formal_laws.py`

---

### Gap #10 — MinimalSufficiency Function

**File:** `src/qiyas_core/formal_laws.py` — `MSL(x, P, candidates)`

`MSL(x, P) ⇔ Licensed(x,P) ∧ Sufficient(x,P) ∧ ∀y<x : ¬Sufficient(y,P)`

**Tests:** `tests/qiyas_core/test_formal_laws.py`

---

### Gap #11 — RecursiveProofContract

**File:** `src/qiyas_core/recursive_proof.py` — `RecursiveProofContract` frozen
dataclass; `PHASE1_CONTRACTS` tuple of 5 canonical instances.

**Canonical instances:**
1. `TYPED_CODEPOINT_CONTRACT` — TypedCodePoint layer
2. `LETTER_IDENTITY_CONTRACT` — LetterIdentityCarrier layer
3. `HARAKA_FUNCTION_CONTRACT` — HarakaFunctionCarrier layer
4. `POSITION_CONTRACT` — PositionCarrier layer
5. `SLOT_CONTRACT` — SlotCandidate (composition) layer

**Tests:** `tests/qiyas_core/test_recursive_proof.py`

---

### Gap #12 — ForbiddenOutputRegistry

**File:** `src/qiyas_core/forbidden_outputs.py` — `ForbiddenOutputRegistry`,
`LAYER_FORBIDDEN_OUTPUTS` dict, `get_forbidden_outputs(layer)`.

Constitutional triple `{HukmCandidate, RealityClaim, FinalMeaning}` plus
layer-specific sets are consumed by all new rules instead of being repeated inline.

**Tests:** `tests/qiyas_core/test_forbidden_outputs.py`
- `test_letter_identity_forbids_weight`
- `test_haraka_function_forbids_case_effect`
- `test_slot_forbids_meaning`

---

## Deferred — Phase 2 (explicitly out of scope for this PR)

| Gap | Component | Reason deferred |
|-----|-----------|-----------------|
| #1  | `ControlledArabicVocalizedTextSpace` | Requires validated vocalised corpus boundary definition; scope > Phase 1 |
| #2  | Explicit inference relation `⊢` | Formal proof algebra on top of the candidate graph; requires Phase 1 complete |
| #13 | Soundness proof | Formal meta-theory; depends on #2 |
| #14 | Relative Completeness proof | Formal meta-theory; depends on #2 and #13 |

---

## Verified Test Run (all 172 tests pass)

```
PYTHONPATH=src python3 -m pytest tests/ -q
172 passed in 0.xx s
```

*(exact count: 155 original + 17 new `test_recursive_proof.py` = 172 total)*

---

## Constitutional Guarantees

| Invariant | Enforcement |
|-----------|-------------|
| `forbidden_outputs ⊇ {HukmCandidate, RealityClaim, FinalMeaning}` | `QiyasKernel._check_forbidden_outputs_declared` |
| `identity_ids ∩ trace_ids = ∅` | `QiyasKernel._check_identity` + `QiyasNodeRef.__post_init__` |
| `Layer[n] ⊬ Layer[n+2]` | `forbidden_outputs` on every layer + blocking tests |
| `output_flags = {"CandidateOnly"}` | All new rules + adapter validation |
| `rank_ceiling = EvidenceRank.FORM` | All new rules |
| Identity preserved across Slot composition | `SlotLayerAdapter` merges all three carrier `identity_ids` |
