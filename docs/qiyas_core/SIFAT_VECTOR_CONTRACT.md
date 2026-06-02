# SIFAT VECTOR CONTRACT

> **Purpose:** 6-axis phonetic discrimination system for Arabic letters.
>
> **Constraint:** Full SifatVector is NOT optional decoration — it is the mechanism for negating invalidating differences (فارق/fariq).

---

## 0. Why 6 Axes Are Required

### Current (Partial): 3 Axes

```
voicing_axis: VOICED | VOICELESS
manner_axis: STOP | FRICATIVE | ...
emphasis_axis: EMPHATIC | NON_EMPHATIC
```

### Problem: Cannot Distinguish

```
❌ ب (BAA)  vs  م (MEEM)
   Both: VOICED + STOP + NON_EMPHATIC
   Difference: NASALITY

❌ و (WAW)  vs  ف (FAA)
   Need: FRICATION + CONTINUANCY distinction

❌ س (SEEN)  vs  ص (SAAD)  vs  ش (SHEEN)
   Need: EMPHASIS + detailed FRICATION

❌ ت (TAA)  vs  د (DAL)
   Difference: VOICING (already covered)
   But: Need NASALITY axis to exclude م/ن

❌ ط (TAA emphatic)  vs  ت (TAA plain)
   Difference: EMPHASIS (already covered)
   But: Need full discrimination for CONTINUANCY
```

### Solution: 6 Axes

```
✓ VoicingAxis: ب د vs ت ك
✓ MannerAxis: STOP vs FRICATIVE vs NASAL vs APPROXIMANT vs LATERAL
✓ NasalityAxis: م ن vs all others
✓ FricationAxis: ف ث ذ س ص ش خ غ ح ع ه vs others
✓ ContinuancyAxis: fricatives/nasals/liquids vs stops
✓ EmphasisAxis: ص ض ط ظ ق vs others
```

**With 6 axes, we can uniquely identify all 28+ Arabic letters through fariq negation.**

---

## 1. SifatVector Specification

### Complete Dataclass

```python
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class SifatVector:
    """
    6-axis phonetic discrimination system.

    PURPOSE: Negate invalidating differences (fariq) between letters.
    NOT PURPOSE: Derive meaning, root, or hukm.

    CRITICAL: This is coordinate positioning ONLY.
    """

    voicing_axis: VoicingValue
    manner_axis: MannerValue
    nasality_axis: NasalityValue
    frication_axis: FricationValue
    continuancy_axis: ContinuancyValue
    emphasis_axis: EmphasisValue

    residuals: tuple[Residual, ...]
    # If any axis cannot be determined

    # Qiyas proof infrastructure
    evidence: EvidenceSet
    rank: EvidenceRank
```

---

## 2. Axis Definitions

### Axis 1: VoicingAxis

```python
class VoicingValue(Enum):
    """Vocal fold vibration during articulation."""

    VOICED = "voiced"
    # Vocal folds vibrate
    # Arabic: مجهور
    # Examples: ب د ج ز ظ ذ ض غ

    VOICELESS = "voiceless"
    # Vocal folds do not vibrate
    # Arabic: مهموس
    # Examples: ت ك س ص ش ح خ ف ث ه ق ط
```

**Discrimination:**

| Letter | Voicing |
|--------|---------|
| ب | VOICED |
| ت | VOICELESS |
| د | VOICED |
| ك | VOICELESS |

### Axis 2: MannerAxis

```python
class MannerValue(Enum):
    """Manner of articulation."""

    STOP = "stop"
    # Complete closure, then release
    # Arabic: شديد
    # Examples: ب ت د ط ك ق ء

    FRICATIVE = "fricative"
    # Narrow constriction, turbulent airflow
    # Arabic: رخو
    # Examples: ف ث ذ س ص ش ز خ غ ح ع ه

    NASAL = "nasal"
    # Oral closure, nasal airflow
    # Arabic: غنّة
    # Examples: م ن

    APPROXIMANT = "approximant"
    # Narrow constriction, smooth airflow
    # Examples: و ي (when consonantal)

    LATERAL = "lateral"
    # Tongue center closure, side airflow
    # Example: ل
```

**Discrimination:**

| Letter | Manner |
|--------|--------|
| ب | STOP |
| ف | FRICATIVE |
| م | NASAL |
| ل | LATERAL |
| و | APPROXIMANT |

### Axis 3: NasalityAxis

```python
class NasalityValue(Enum):
    """Nasal vs oral airflow."""

    NASAL = "nasal"
    # Airflow through nose
    # Arabic: غنّة
    # Examples: م ن

    ORAL = "oral"
    # Airflow through mouth only
    # Examples: All others
```

**Critical discrimination:**

```
ب (BAA) vs م (MEEM):
  Both VOICED + STOP + NON_EMPHATIC
  Difference: ORAL vs NASAL ← CRITICAL

Fariq (invalidating difference) negation claim:
  فارق:baa_vs_meem_nasality:absent
```

### Axis 4: FricationAxis

```python
class FricationValue(Enum):
    """Fricative vs non-fricative."""

    FRICATIVE = "fricative"
    # Turbulent airflow through narrow constriction
    # Examples: ف ث ذ س ص ش ز خ غ ح ع ه

    NON_FRICATIVE = "non_fricative"
    # No turbulent frication
    # Examples: ب ت د ط ك ق م ن ل و ي
```

**Critical discrimination:**

```
و (WAW) vs ف (FAA):
  Need FRICATION distinction

Fariq (invalidating difference) negation claim:
  فارق:waw_vs_faa_frication:absent
```

### Axis 5: ContinuancyAxis

```python
class ContinuancyValue(Enum):
    """Continuous vs non-continuous airflow."""

    CONTINUANT = "continuant"
    # Airflow can continue
    # Examples: ف ث ذ س ص ش ز خ غ ح ع ه م ن ل و ي

    NON_CONTINUANT = "non_continuant"
    # Airflow interrupted (stops)
    # Examples: ب ت د ط ك ق ء
```

**Relation to manner:**

```
STOP → NON_CONTINUANT
FRICATIVE → CONTINUANT
NASAL → CONTINUANT
APPROXIMANT → CONTINUANT
LATERAL → CONTINUANT
```

### Axis 6: EmphasisAxis

```python
class EmphasisValue(Enum):
    """Pharyngealization (tafkhim) vs plain."""

    EMPHATIC = "emphatic"
    # Pharyngealized (back of tongue raised toward pharynx)
    # Arabic: مفخّم / إطباق
    # Examples: ص ض ط ظ ق

    NON_EMPHATIC = "non_emphatic"
    # Plain (no pharyngealization)
    # Arabic: مرقّق
    # Examples: All others
```

**Critical discrimination:**

```
ط (TAA emphatic) vs ت (TAA plain):
  Both VOICELESS + STOP + ORAL + NON_FRICATIVE + NON_CONTINUANT
  Difference: EMPHATIC vs NON_EMPHATIC ← CRITICAL

Fariq (invalidating difference) negation claim:
  فارق:taa_emphatic_vs_taa_plain_emphasis:absent
```

---

## 3. Complete Letter Mappings

**Source:** `sifat_vector_system.py`

### Sample Mappings

| Letter | Voicing | Manner | Nasality | Frication | Continuancy | Emphasis |
|--------|---------|--------|----------|-----------|-------------|----------|
| ب BAA | VOICED | STOP | ORAL | NON_FRICATIVE | NON_CONTINUANT | NON_EMPHATIC |
| ت TAA | VOICELESS | STOP | ORAL | NON_FRICATIVE | NON_CONTINUANT | NON_EMPHATIC |
| ث THAA | VOICELESS | FRICATIVE | ORAL | FRICATIVE | CONTINUANT | NON_EMPHATIC |
| ج JEEM | VOICED | STOP | ORAL | NON_FRICATIVE | NON_CONTINUANT | NON_EMPHATIC |
| م MEEM | VOICED | NASAL | NASAL | NON_FRICATIVE | CONTINUANT | NON_EMPHATIC |
| ن NOON | VOICED | NASAL | NASAL | NON_FRICATIVE | CONTINUANT | NON_EMPHATIC |
| ف FAA | VOICELESS | FRICATIVE | ORAL | FRICATIVE | CONTINUANT | NON_EMPHATIC |
| و WAW | VOICED | APPROXIMANT | ORAL | NON_FRICATIVE | CONTINUANT | NON_EMPHATIC |
| س SEEN | VOICELESS | FRICATIVE | ORAL | FRICATIVE | CONTINUANT | NON_EMPHATIC |
| ص SAAD | VOICELESS | FRICATIVE | ORAL | FRICATIVE | CONTINUANT | EMPHATIC |
| ش SHEEN | VOICELESS | FRICATIVE | ORAL | FRICATIVE | CONTINUANT | NON_EMPHATIC |
| ط TAA_E | VOICELESS | STOP | ORAL | NON_FRICATIVE | NON_CONTINUANT | EMPHATIC |

**Total:** 28+ letters, each with complete 6-axis sifat vector.

---

## 4. Fariq (Invalidating Difference) Negation

**Purpose of SifatVector: Enable fariq negation.**

### Example: ب vs م

```python
# Letter: ب (BAA)
sifat_baa = SifatVector(
    voicing_axis=VoicingValue.VOICED,
    manner_axis=MannerValue.STOP,
    nasality_axis=NasalityValue.ORAL,           # ← CRITICAL
    frication_axis=FricationValue.NON_FRICATIVE,
    continuancy_axis=ContinuancyValue.NON_CONTINUANT,
    emphasis_axis=EmphasisValue.NON_EMPHATIC,
)

# Letter: م (MEEM)
sifat_meem = SifatVector(
    voicing_axis=VoicingValue.VOICED,
    manner_axis=MannerValue.NASAL,
    nasality_axis=NasalityValue.NASAL,          # ← CRITICAL
    frication_axis=FricationValue.NON_FRICATIVE,
    continuancy_axis=ContinuancyValue.CONTINUANT,
    emphasis_axis=EmphasisValue.NON_EMPHATIC,
)

# Fariq between ب and م:
fariq_baa_vs_meem = [
    "baa_vs_meem_nasality",    # ORAL vs NASAL
    "baa_vs_meem_manner",      # STOP vs NASAL
    "baa_vs_meem_continuancy", # NON_CONTINUANT vs CONTINUANT
]

# Pseudo-code using proposed helper API (not yet implemented):
# evidence.add_claim("فارق:baa_vs_meem_nasality:absent")
# evidence.add_claim("فارق:baa_vs_meem_manner:absent")
# evidence.add_claim("فارق:baa_vs_meem_continuancy:absent")

# Current Evidence API:
evidence_items = [
    Evidence(
        evidence_id="fariq_baa_vs_meem_nasality_absent",
        source_layer="sifat_vector_system.py",
        proves=("فارق:baa_vs_meem_nasality:absent",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        trace_ids=("U+0628",)
    ),
    Evidence(
        evidence_id="fariq_baa_vs_meem_manner_absent",
        source_layer="sifat_vector_system.py",
        proves=("فارق:baa_vs_meem_manner:absent",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        trace_ids=("U+0628",)
    ),
    Evidence(
        evidence_id="fariq_baa_vs_meem_continuancy_absent",
        source_layer="sifat_vector_system.py",
        proves=("فارق:baa_vs_meem_continuancy:absent",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        trace_ids=("U+0628",)
    ),
]
evidence_set = EvidenceSet(items=tuple(evidence_items))
```

### Example: س vs ص

```python
# Letter: س (SEEN)
sifat_seen = SifatVector(
    voicing_axis=VoicingValue.VOICELESS,
    manner_axis=MannerValue.FRICATIVE,
    nasality_axis=NasalityValue.ORAL,
    frication_axis=FricationValue.FRICATIVE,
    continuancy_axis=ContinuancyValue.CONTINUANT,
    emphasis_axis=EmphasisValue.NON_EMPHATIC,    # ← CRITICAL
)

# Letter: ص (SAAD)
sifat_saad = SifatVector(
    voicing_axis=VoicingValue.VOICELESS,
    manner_axis=MannerValue.FRICATIVE,
    nasality_axis=NasalityValue.ORAL,
    frication_axis=FricationValue.FRICATIVE,
    continuancy_axis=ContinuancyValue.CONTINUANT,
    emphasis_axis=EmphasisValue.EMPHATIC,        # ← CRITICAL
)

# Fariq between س and ص:
fariq_seen_vs_saad = [
    "seen_vs_saad_emphasis",  # NON_EMPHATIC vs EMPHATIC
]

# Pseudo-code using proposed helper API (not yet implemented):
# evidence.add_claim("فارق:seen_vs_saad_emphasis:absent")

# Current Evidence API:
evidence_item = Evidence(
    evidence_id="fariq_seen_vs_saad_emphasis_absent",
    source_layer="sifat_vector_system.py",
    proves=("فارق:seen_vs_saad_emphasis:absent",),
    rank=EvidenceRank.FORMAL_STRUCTURE,
    trace_ids=("U+0633",)
)
evidence_set = EvidenceSet(items=(evidence_item,))
```

---

## 5. Source-of-Truth

**Canonical source:**

```
src/qiyas_core/systems/sifat_vector_system.py
```

**Contains:**

- SifatVector dataclass
- All 6 axis enums
- Complete letter → sifat mapping (28+ letters)
- Fariq negation logic
- Evidence generation

**Imported by:**

- `arabic_letter_coordinate_adapter.py`
- `letter_coordinate_rules.py`
- Tests

**NOT duplicated in:**

- Rules (import only)
- Tests (import only)
- Other adapters

---

## 6. Evidence Requirements

### Evidence Claims for Sifat

```python
# Pseudo-code using proposed helper API (not yet implemented):
# evidence.add_claim(f"وصف:has_voicing:{voicing.value}:evidenced")
# evidence.add_claim(f"وصف:has_manner:{manner.value}:evidenced")
# evidence.add_claim(f"وصف:has_nasality:{nasality.value}:evidenced")
# evidence.add_claim(f"وصف:has_frication:{frication.value}:evidenced")
# evidence.add_claim(f"وصف:has_continuancy:{continuancy.value}:evidenced")
# evidence.add_claim(f"وصف:has_emphasis:{emphasis.value}:evidenced")
# for fariq in fariq_set:
#     evidence.add_claim(f"فارق:{fariq}:absent")
# evidence.source = "sifat_vector_system.py"

# Current Evidence API:
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.enums import EvidenceRank

evidence_items = []

# For each sifat axis:
evidence_items.append(Evidence(
    evidence_id=f"sifat_voicing_{letter_name}",
    source_layer="sifat_vector_system.py",
    proves=(f"وصف:has_voicing:{voicing.value}:evidenced",),
    rank=EvidenceRank.FORMAL_STRUCTURE,
    trace_ids=(letter_codepoint,)
))
evidence_items.append(Evidence(
    evidence_id=f"sifat_manner_{letter_name}",
    source_layer="sifat_vector_system.py",
    proves=(f"وصف:has_manner:{manner.value}:evidenced",),
    rank=EvidenceRank.FORMAL_STRUCTURE,
    trace_ids=(letter_codepoint,)
))
# ... similar for nasality, frication, continuancy, emphasis

# Fariq negation:
for fariq in fariq_set:
    evidence_items.append(Evidence(
        evidence_id=f"fariq_{fariq}_absent",
        source_layer="sifat_vector_system.py",
        proves=(f"فارق:{fariq}:absent",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        trace_ids=(letter_codepoint,)
    ))

evidence_set = EvidenceSet(items=tuple(evidence_items))
```

### Rank

```python
rank = EvidenceRank.FORMAL_STRUCTURE
# Sifat classification is formal/conventional
```

---

## 7. Residuals

### Sifat Vector Residuals

```
defer:sifat_vector_incomplete:present
  Cause: One or more axes cannot be determined
  Example: Non-classical letter, ambiguous Unicode

defer:sifat_axis_ambiguous:{axis}:present
  Cause: Specific axis requires context
  Example: و (WAW) voicing context-dependent in some theories

فارق:sifat_conflict:present
  Cause: Sifat values conflict with letter identity
  Example: VOICED assigned to inherently voiceless letter
```

---

## 8. Forbidden Outputs

**SifatVector MUST forbid:**

```python
forbidden_outputs = [
    "MeaningCandidate",       # Sifat is phonetic coordinate, not meaning
    "RootCandidate",          # Sifat does not determine root
    "WeightCandidate",        # Sifat does not determine weight
    "HukmCandidate",          # Sifat does not determine hukm
]
```

**Evidence MUST include:**

```python
# Pseudo-code using proposed helper API (not yet implemented):
# evidence.add_claim("forbidden:meaning_from_sifat:negated")
# evidence.add_claim("forbidden:root_from_sifat:negated")

# Current Evidence API:
forbidden_evidence = [
    Evidence(
        evidence_id="forbidden_meaning_from_sifat",
        source_layer="sifat_vector_system.py",
        proves=("forbidden:meaning_from_sifat:negated",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        trace_ids=(letter_codepoint,)
    ),
    Evidence(
        evidence_id="forbidden_root_from_sifat",
        source_layer="sifat_vector_system.py",
        proves=("forbidden:root_from_sifat:negated",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        trace_ids=(letter_codepoint,)
    ),
]
```

---

## 9. Implementation Priority

**Phase 1: Documentation (This PR)**
- [x] SIFAT_VECTOR_CONTRACT.md (this document)

**Phase 2: System Creation**
- [ ] Create `sifat_vector_system.py`
- [ ] Define all 6 axis enums
- [ ] Define SifatVector dataclass
- [ ] Map all 28+ letters to complete sifat vectors

**Phase 3: Fariq Registry**
- [ ] Document all fariq pairs
- [ ] Implement fariq negation logic
- [ ] Add fariq_set to each letter

**Phase 4: Integration**
- [ ] Update `ArabicLetterCoordinateCarrier` to include `sifat_vector` field
- [ ] Update adapter to use sifat_vector_system
- [ ] Generate evidence with fariq negation

**Phase 5: Testing**
- [ ] Test all 28+ letters have complete vectors
- [ ] Test fariq negation (ب vs م, س vs ص, etc.)
- [ ] Test incomplete vector produces residual
- [ ] Test forbidden outputs enforced

---

## 10. Integration

**This contract implements:**
- PROJECT_MATHEMATICAL_FOUNDATION.md § 11 (Full SifatVector requirement)
- FULL_LAYER_2_PLAN.md § 4 (6-axis specification)
- SOURCE_OF_TRUTH_REGISTRY.md (sifat as coordinate truth)

**This contract is required by:**
- ArabicLetterCoordinateCarrier (sifat_vector field)
- GlyphClassificationGate (phonetic classification)
- Future ArabicMorphophonology (phonological rule conditions)

---

**Document Version:** 1.0
**Last Updated:** 2026-06-01
**Status:** Constitutional contract for Layer 2 completion
**Authority:** Required before coordinate expansion
