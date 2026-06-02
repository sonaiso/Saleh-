# SOURCE OF TRUTH REGISTRY

> **Core Law:** No operational truth without a single source. No source without evidence. No evidence without rank. No rank without preserved trace. No transition without identity preservation. No failure without residuals.
>
> **بالعربية:** لا حقيقة تشغيلية بلا مصدر واحد. لا مصدر بلا دليل. لا دليل بلا رتبة. لا رتبة بلا أثر محفوظ. لا انتقال بلا حفظ هوية. لا فشل بلا بقايا.

---

## 0. Constitutional Foundation

### Identity Preservation Law

```
Identity is preserved only through evidence grounded in the declared reality
of controlled vocalized Arabic.
```

**بالعربية:**

```
لا تُحفظ الهوية إلا بدليل مطابق لواقع العربية المشكولة المنضبطة ضمن المجال المصرح.
```

### Why Source-of-Truth Registry?

**Problem:** If a layer takes information from multiple sources, identity breaks.

**Example of identity breakage:**

```python
# abjad_system.py says:
ب = 2

# letter_coordinate_rules.py says:
ب = 2

# adapter.py says:
ب = 2
```

**Today:** Aligned.

**Tomorrow:** If they diverge, failure becomes ambiguous:
```
❌ effective_wasf_missing (unclear cause)
```

Instead of clear:
```
✓ source_of_truth_conflict: abjad_value
```

**Solution:** SourceOfTruthRegistry — not luxury, but **identity preservation requirement**.

---

## 1. Controlled Vocalized Arabic Domain

**The declared domain is NOT all Arabic in general.**

**The declared domain NOW is:**

```
Controlled Vocalized Arabic Domain
```

**Meaning:**

- Known Arabic symbols
- Classified letters
- Visible harakaat (vocalization marks)
- Visible boundaries
- Visible punctuation
- No estimation without evidence
- No deletion without trace
- No phonological change without gate
- No meaning without layer

**This domain allows us to say:**

```
✓ This letter is BAA by digital/orthographic evidence
✓ This haraka is FATHA by symbolic evidence
✓ This position is initial/medial by contextual evidence
✓ This alignment is valid by prior evidence
```

**This domain does NOT allow us to say prematurely:**

```
❌ This is a root
❌ This is a weight
❌ This is a meaning
❌ This is a hukm
```

---

## 2. Four Types of Truths

### A. Identity Truths

**Source location:** One canonical source per truth.

**Examples:**

| Truth | Source File | Example |
|-------|-------------|---------|
| Unicode codepoint | `unicode_constants.py` | `identity:codepoint:0628` |
| Script identity | `script_identity_registry.py` | `identity:script:arabic_letter_baa` |
| Letter name | `letter_name_registry.py` | `identity:name:baa` |
| Letter identity | `letter_identity_registry.py` | `identity:letter:baa` |
| Standalone form | `letter_forms_registry.py` | `identity:form:standalone` |
| Typed class | `typed_codepoint_registry.py` | `identity:type:letter` |

**Law:**

```
One identity truth = One canonical source
No duplication in adapter/rules/tests
All components import from same source
```

### B. Coordinate Truths

**Source location:** Coordinate systems with evidence and rank.

**Examples:**

| Coordinate | Source File | Constraint |
|------------|-------------|------------|
| Makhraj | `makhraj_coordinate_registry.py` | Phonetic origin coordinate |
| Sifat | `sifat_vector_registry.py` | 6-axis phonetic discrimination |
| Phonetic proxy | `phonetic_proxy_registry.py` | IPA approximation |
| Abjad value | `abjad_system.py` | Numeric coordinate with `semantic_force=FORBIDDEN` |
| Morpho role | `letter_role_taxonomy.py` | Role potential, not final role |
| Glyph class | `glyph_classification_registry.py` | Core letter vs hamza seat vs madd vs tatweel |

**Critical constraints:**

```python
# Abjad numeric coordinate:
assert abjad_coordinate.semantic_force == "FORBIDDEN"
# Meaning: No meaning derivation from numeric value

# Morpho role:
assert morpho_role.status == "POTENTIAL"
# Meaning: Role potential, requires RoleDisambiguationGate
```

### C. Operation Truths

**Source location:** Functional operation definitions.

**Examples:**

| Operation | Source File | Definition |
|-----------|-------------|------------|
| Haraka function | `haraka_function_registry.py` | Opening/closing/neutral classification |
| Short vowel operation | `vowel_operation_registry.py` | Vocalic operator type |
| Sukun closure | `sukun_operation_registry.py` | Closure/pause operation |
| Shadda compression | `shadda_operation_registry.py` | Consonant compression |
| Madd extension | `madd_operation_registry.py` | Vowel extension |

### D. Prohibition Truths

**Source location:** Forbidden output enforcement.

**Examples:**

| Prohibition | Source File | Enforcement |
|-------------|-------------|-------------|
| No meaning from Abjad | `abjad_system.py` | `semantic_force=FORBIDDEN` |
| No root from Unicode | `letter_identity_rules.py` | `forbidden_outputs` includes RootCandidate |
| No Slot without Alignment | `slot_candidate_rules.py` | Requires AlignmentEvidence |
| No Syllable from one Slot | `syllable_candidate_rules.py` | Requires adjacency evidence |
| No Weight without StemMatterTensor | `root_weight_rules.py` | Requires StemMatterTensor input |

---

## 3. Registry Structure

### Format

Every source-of-truth entry follows:

```python
@dataclass(frozen=True)
class SourceOfTruthEntry:
    """Single source of truth for one type of information."""

    truth_type: str  # "identity" | "coordinate" | "operation" | "prohibition"
    truth_name: str  # e.g., "letter_name", "abjad_value", "haraka_function"

    canonical_source: str  # File path to single source
    source_type: str  # "registry" | "system" | "taxonomy" | "rules"

    evidence_rank: EvidenceRank  # Minimum rank for this truth
    domain: str  # "controlled_vocalized_arabic" | etc.

    consuming_components: list[str]  # Components that import this truth

    forbidden_duplicates: list[str]  # Where this truth MUST NOT be redefined

    validation_rule: str  # How to verify single-source compliance
```

### Example Entry

```python
SourceOfTruthEntry(
    truth_type="coordinate",
    truth_name="abjad_numeric_value",

    canonical_source="src/qiyas_core/abjad_system.py",
    source_type="system",

    evidence_rank=EvidenceRank.FORMAL_STRUCTURE,
    domain="controlled_vocalized_arabic",

    consuming_components=[
        "src/qiyas_core/letter_coordinate_adapter.py",
        "src/qiyas_core/rules/letter_coordinate_rules.py",
        "tests/qiyas_core/test_letter_coordinate_carrier.py",
    ],

    forbidden_duplicates=[
        "src/qiyas_core/letter_identity_adapter.py",  # Identity layer doesn't define coordinates
        "src/qiyas_core/slot_candidate_adapter.py",   # Slot layer doesn't redefine Abjad
        "tests/qiyas_core/conftest.py",               # Tests import, not redefine
    ],

    validation_rule="assert all_components_import_from_canonical_source()"
)
```

---

## 4. Current Canonical Sources (Layer 0-3)

### Layer 0: Unicode Membership

| Truth | Canonical Source | Status |
|-------|-----------------|--------|
| Arabic Unicode ranges | `src/qiyas_core/unicode_constants.py` | ⚠️ Needs creation |
| Unicode validation | `src/qiyas_core/unicode_adapter.py` | ✓ Canonical |

### Layer 1: TypedCodePoint Classification

| Truth | Canonical Source | Status |
|-------|-----------------|--------|
| Typed classification rules | `src/qiyas_core/rules/typed_codepoint_rules.py` | ✓ Canonical |
| Letter class definition | `src/qiyas_core/registries/letter_class_registry.py` | ⚠️ Needs creation |
| Haraka class definition | `src/qiyas_core/registries/haraka_class_registry.py` | ⚠️ Needs creation |
| Boundary class definition | `src/qiyas_core/registries/boundary_class_registry.py` | ⚠️ Needs creation |

### Layer 2A: Letter Identity

| Truth | Canonical Source | Status |
|-------|-----------------|--------|
| Letter name mapping | `src/qiyas_core/registries/letter_name_registry.py` | ⚠️ Needs creation |
| Script identity | `src/qiyas_core/registries/script_identity_registry.py` | ⚠️ Needs creation |
| Letter identity rules | `src/qiyas_core/rules/letter_identity_rules.py` | ✓ Canonical |

### Layer 2B: Haraka Function

| Truth | Canonical Source | Status |
|-------|-----------------|--------|
| Haraka function taxonomy | `src/qiyas_core/registries/haraka_function_registry.py` | ⚠️ Needs creation |
| Opening/closing classification | `src/qiyas_core/rules/haraka_function_rules.py` | ✓ Canonical (partial) |

### Layer 2X: Arabic Letter Coordinates (Partial)

| Truth | Canonical Source | Status |
|-------|-----------------|--------|
| Makhraj coordinates | `src/qiyas_core/systems/makhraj_coordinate_system.py` | ⚠️ Needs creation |
| Sifat vectors | `src/qiyas_core/systems/sifat_vector_system.py` | ⚠️ Needs creation |
| Abjad system | `src/qiyas_core/abjad_system.py` | ✓ Canonical (complete: 28 letters) |
| Phonetic proxy | `src/qiyas_core/systems/phonetic_proxy_system.py` | ⚠️ Needs creation |

**Note on Abjad:** The source-of-truth in `abjad_system.py` defines complete Abjad values for all 28 traditional Arabic letters. Current Layer 2X consumption (ArabicLetterCoordinateCarrier) uses only BAA/TAA/SEEN/KAF as a minimal slice. To expand coordinate coverage, extend consumption in `letter_coordinate_adapter.py`, not the Abjad source.
| Glyph classification | `src/qiyas_core/gates/glyph_classification_gate.py` | ❌ Not implemented |
| Letter role taxonomy | `src/qiyas_core/taxonomies/letter_role_taxonomy.py` | ❌ Not implemented |

### Layer 3: Slot Candidate

| Truth | Canonical Source | Status |
|-------|-----------------|--------|
| Slot formation rules | `src/qiyas_core/rules/slot_rules.py` | ✓ Canonical (partial) |
| Alignment evidence | `src/qiyas_core/rules/conditioned_typed_sequence_rules.py` | ✓ Canonical |

---

## 5. Required Source Files (To Be Created)

### Priority 1: Identity Foundation

```
src/qiyas_core/registries/
  ├── unicode_constants.py          # Arabic Unicode ranges
  ├── letter_name_registry.py       # Letter name → identity mapping
  ├── script_identity_registry.py   # Script identity taxonomy
  ├── letter_class_registry.py      # Letter classification
  ├── haraka_class_registry.py      # Haraka classification
  └── boundary_class_registry.py    # Boundary classification
```

### Priority 2: Coordinate Systems

```
src/qiyas_core/
  ├── abjad_system.py               # ✓ Exists at root, complete 28 letters
src/qiyas_core/systems/              # (planned directory for future systems)
  ├── makhraj_coordinate_system.py  # ⚠️ Planned: Makhraj origin coordinates
  ├── sifat_vector_system.py        # ⚠️ Planned: 6-axis sifat discrimination
  └── phonetic_proxy_system.py      # ⚠️ Planned: IPA phonetic approximations
```

**CRITICAL:** Do NOT create `src/qiyas_core/systems/abjad_system.py`. The canonical Abjad source is `src/qiyas_core/abjad_system.py` (at root level, not under systems/).

### Priority 3: Classification Gates

```
src/qiyas_core/gates/
  ├── glyph_classification_gate.py  # Core letter vs hamza vs madd vs tatweel
  └── role_disambiguation_gate.py   # Future: stem vs augment vs particle
```

### Priority 4: Taxonomies

```
src/qiyas_core/taxonomies/
  ├── haraka_function_taxonomy.py   # Opening/closing/neutral/compression/extension
  ├── letter_role_taxonomy.py       # Carrier/operator/extension potential
  └── morpho_role_taxonomy.py       # Future: stem/augment/particle potential
```

---

## 6. Source-of-Truth Validation

### Validation Rules

**Every layer adapter MUST:**

1. Import truths from canonical source
2. NOT redefine truths locally
3. NOT duplicate truth definitions in tests
4. Cite source in evidence claims

**Example (Correct):**

```python
# letter_coordinate_adapter.py (example using current API)

from qiyas_core.abjad_system import get_abjad_coordinate
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.enums import EvidenceRank

class ArabicLetterCoordinateAdapter:
    def add_abjad_coordinate(self, letter_identity: LetterIdentityCarrier):
        # Use canonical source, not local definition
        abjad_coord = get_abjad_coordinate(letter_identity.codepoint)

        if abjad_coord:
            # Current Evidence API (not .add_claim helper)
            evidence_item = Evidence(
                evidence_id=f"abjad_{letter_identity.name_identity}_{abjad_coord.numeric_value}",
                source_layer="abjad_system.py",
                proves=(
                    f"coordinate:abjad:{letter_identity.name_identity}:{abjad_coord.numeric_value}:evidenced",
                ),
                rank=EvidenceRank.FORMAL_STRUCTURE,
                trace_ids=(letter_identity.codepoint,)
            )
            evidence_set = EvidenceSet(items=(evidence_item,))
```

**Example (Forbidden):**

```python
# letter_coordinate_adapter.py

class ArabicLetterCoordinateAdapter:
    # ❌ FORBIDDEN: Local redefinition of Abjad values
    ABJAD_VALUES = {
        "BAA": 2,
        "TAA": 400,
        # ...
    }
```

### Conflict Detection

```python
def detect_source_conflicts():
    """Detect when same truth is defined in multiple sources."""

    for truth_name in all_truths:
        sources = find_all_definitions(truth_name)

        if len(sources) > 1:
            raise SourceOfTruthConflict(
                truth=truth_name,
                sources=sources,
                resolution=f"Consolidate to canonical source: {canonical_source(truth_name)}"
            )
```

---

## 7. Identity Preservation Through Evidence

### What "Identity Preservation" Means Operationally

Every transition MUST declare:

```python
# Input identity:
identity_in = "identity:codepoint:0628"

# Established identity:
identity_established = "identity:letter:baa"

# Added coordinates:
coordinates_added = [
    "coordinate:makhraj:bilabial",
    "coordinate:sifat:voiced_stop_non_nasal",
    "coordinate:abjad:baa:2",
]

# NOT established (forbidden outputs):
not_established = [
    "identity:root",        # ❌ Root identity
    "identity:weight",      # ❌ Weight identity
    "identity:meaning",     # ❌ Meaning identity
    "identity:hukm",        # ❌ Hukm identity
]
```

**Never conflate:**

```
✓ identity (what it IS)
✓ coordinate (where it is in a system)
✓ role potential (what it CAN be)
❌ meaning (what it SIGNIFIES) — requires higher layers
❌ hukm (what JUDGMENT applies) — requires evidence domain + tanzil
```

---

## 8. Enforcement Mechanisms

### A. Import Validation

```python
def validate_imports(adapter_file: str):
    """Ensure adapter imports from canonical sources."""

    imports = extract_imports(adapter_file)
    required_sources = get_required_sources(adapter_file)

    for source in required_sources:
        if source not in imports:
            raise MissingCanonicalImport(
                adapter=adapter_file,
                missing_source=source,
                error="Adapter must import from canonical source"
            )
```

### B. Duplication Detection

```python
def detect_truth_duplication(codebase: Path):
    """Detect prohibited truth redefinition."""

    for truth in registered_truths:
        canonical = truth.canonical_source
        duplicates = find_redefinitions(truth.truth_name)

        forbidden = set(duplicates) & set(truth.forbidden_duplicates)

        if forbidden:
            raise ProhibitedDuplication(
                truth=truth.truth_name,
                canonical_source=canonical,
                prohibited_duplicates=forbidden
            )
```

### C. Evidence Citation Validation

```python
def validate_evidence_citations(evidence_set: EvidenceSet):
    """Ensure evidence cites canonical sources."""

    for item in evidence_set.items:
        source_layer = item.source_layer
        for claim in item.proves:
            if claim.startswith("coordinate:") or claim.startswith("identity:"):
                if "source=" not in claim and not source_layer:
                    raise MissingSourceCitation(
                        claim=claim,
                        error="Coordinate/identity claims must cite source"
                    )
```

---

## 9. Transition Plan

### Phase 1: Document Current State (This PR)

- [ ] SOURCE_OF_TRUTH_REGISTRY.md (this document)
- [ ] Identify all current truths
- [ ] Document current sources (canonical vs duplicated)
- [ ] List required source files

### Phase 2: Create Missing Registries

- [ ] Create `src/qiyas_core/registries/` directory
- [ ] Implement unicode_constants.py
- [ ] Implement letter_name_registry.py
- [ ] Implement script_identity_registry.py
- [ ] Implement letter_class_registry.py
- [ ] Implement haraka_class_registry.py
- [ ] Implement boundary_class_registry.py

### Phase 3: Create Coordinate Systems

- [ ] Expand `letter_coordinate_adapter.py` consumption to use full Abjad alphabet (source already complete)
- [ ] Create `src/qiyas_core/systems/makhraj_coordinate_system.py`
- [ ] Create `src/qiyas_core/systems/sifat_vector_system.py` (6 axes)
- [ ] Create `src/qiyas_core/systems/phonetic_proxy_system.py`

### Phase 4: Create Classification Gates

- [ ] Implement glyph_classification_gate.py
- [ ] Implement role_disambiguation_gate.py (future)

### Phase 5: Consolidate Duplicates

- [ ] Find all truth duplications in adapters/rules/tests
- [ ] Migrate to canonical sources
- [ ] Add import validation
- [ ] Add conflict detection

### Phase 6: Validation Enforcement

- [ ] Add pre-commit hook for source-of-truth validation
- [ ] Add CI check for duplication detection
- [ ] Add evidence citation validation in QiyasKernel

---

## 10. Integration with Governance

**This document implements:**
- PROJECT_MATHEMATICAL_FOUNDATION.md § 9 (Source-of-Truth Principle)
- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 12 (Source-of-truth Registry)

**This document is referenced by:**
- FULL_LAYER_2_PLAN.md (coordinate source specification)
- SIFAT_VECTOR_CONTRACT.md (sifat registry requirement)
- GLYPH_CLASSIFICATION_GATE_PLAN.md (glyph classification source)

---

## 12. Doc-Code Consistency Self-Audit

**This governance framework has been checked against current code paths, dataclass fields, and executable claim prefixes.**

### Path Verification
- ✅ `src/qiyas_core/abjad_system.py` exists (complete, 28 letters)
- ✅ `src/qiyas_core/evidence.py` exists (EvidenceSet.items, Evidence.source_layer/proves/rank/trace_ids)
- ❌ `src/qiyas_core/systems/` directory does NOT exist yet (planned for future)
- ❌ `AbjadSystem` class does NOT exist (use `get_abjad_coordinate` function instead)

### API Verification
- ✅ `get_abjad_coordinate(codepoint: int) -> AbjadCoordinate | None` is the canonical API
- ✅ `EvidenceSet` has `.items` field (tuple of Evidence), NOT `.claims` or `.source`
- ✅ `Evidence` has `.source_layer`, `.proves`, `.rank`, `.trace_ids` fields
- ❌ `evidence.add_claim()` helper method does NOT exist (construct Evidence directly)

### Executable Claim Prefix Verification
- ✅ QiyasKernel expects Arabic-prefixed claims: `فارق:`, `وصف:`, `علة:`, `اصل:`, `فرع:`, `وادي:`, `defer:`
- ✅ English word "fariq" may appear in prose, but executable claims use `فارق:{diff}:present`
- ✅ All pseudo-code examples in this document use current Evidence API

### Planned Files Marked
- ⚠️ All files under `src/qiyas_core/systems/` (except abjad_system.py) are marked "planned" and must NOT be created as duplicates
- ⚠️ All files under `src/qiyas_core/registries/` are marked "planned"
- ⚠️ All files under `src/qiyas_core/gates/` are marked "planned"

**Remaining planned files are clearly marked and must not be created as duplicates of existing canonical files.**

---

## 13. Summary

### Core Principle

```
حفظ الهوية عن دليل مطابق لواقع العربية المشكولة المنضبطة
هو قلب المشروع.

Identity preservation through evidence grounded in the declared reality
of controlled vocalized Arabic is the heart of the project.
```

### Before Next Layer

```
قبل الطبقة التالية: نثبت مصادر الحقائق.
قبل التشغيل: نثبت الهوية.
قبل الهوية: نثبت الدليل.
قبل النجاح: نثبت الرتبة والأثر.
وعند العجز: نخرج بقايا لا صمتًا.

Before next layer: Establish truth sources.
Before operation: Establish identity.
Before identity: Establish evidence.
Before success: Establish rank and trace.
On failure: Produce residuals, not silence.
```

---

**Document Version:** 1.1
**Last Updated:** 2026-06-02
**Status:** Constitutional requirement for Layer 2 completion
**Authority:** Implements PROJECT_MATHEMATICAL_FOUNDATION.md § 9
**Doc-Code Audit:** Completed 2026-06-02
