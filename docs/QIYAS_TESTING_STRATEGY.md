# Qiyas Testing Strategy

## Constitutional Testing Framework

This document describes the pytest-based constitutional testing framework for qiyas_core. The framework ensures that all layers, adapters, and rules follow constitutional principles through automated tests.

## Test Markers

Use the following pytest markers to categorize tests:

- `@pytest.mark.constitution` - Constitutional invariant tests
- `@pytest.mark.kernel` - QiyasKernel execution tests
- `@pytest.mark.rule` - QiyasRule validation tests
- `@pytest.mark.adapter` - Adapter contract tests
- `@pytest.mark.slot_geometry` - SlotGeometry protocol tests
- `@pytest.mark.evidence_claims` - Evidence claim grammar tests
- `@pytest.mark.rank` - Evidence rank invariant tests
- `@pytest.mark.identity_trace` - Identity and trace invariant tests
- `@pytest.mark.no_higher_outputs` - Candidate boundary tests
- `@pytest.mark.golden` - Golden path tests
- `@pytest.mark.integration` - Cross-layer integration tests
- `@pytest.mark.regression` - Regression tests for fixed bugs

## Evidence Claim Grammar

### Allowed Claims

The following evidence claim patterns are constitutionally valid:

- `asl:established` - asl candidate established
- `far:determined` - far candidate determined
- `wasf:*:evidenced` - wasf evidence proven (e.g., `wasf:carrier_accepts_mark:evidenced`)
- `illah:*:verified` - illah verified (e.g., `illah:licensed_atomic_binding:verified`)
- `wadi:{gate}:{state}` - wadi gate states:
  - `wadi:sabab:established`
  - `wadi:shart:satisfied`
  - `wadi:mani:absent`
  - `wadi:sihha:valid`
  - `wadi:fasad:absent`
  - `wadi:butlan:absent`
- `fariq:*:present` - invalidating difference detected (e.g., `fariq:carrier_is_not_arabic_letter:present`)
- `defer:*:present` - deferral condition detected (e.g., `defer:murab_closure_deferred:present`)

### Forbidden Claims

The following evidence claim patterns violate constitutional grammar:

- `diff:*` - old difference format (use `fariq:*:present` instead)
- `residual:*` - residuals are not evidence claims
- `hukm:*` - hukm claims not allowed in evidence layer
- `meaning:*:final` - final meaning not evidence-level
- `reality:*:claim` - reality claims not evidence-level
- `final:*` - final claims not evidence-level

## Constitutional Invariants

### 1. WadiGate Completeness

Every QiyasRule must require exactly 6 WadiGates (no more, no fewer):
- `WadiGate.SABAB`
- `WadiGate.SHART`
- `WadiGate.MANI`
- `WadiGate.SIHHA`
- `WadiGate.FASAD`
- `WadiGate.BUTLAN`

**Violation Examples:**
- Missing any gate → constitutional failure
- Extra gates beyond the six → constitutional failure

### 2. Forbidden Outputs Discipline

Qiyas and readiness layer rules must have **non-empty** `forbidden_outputs` listing all architecturally higher candidate types.

**Examples:**
- `AtomicUnitQiyas` must forbid: `SyllableCandidate`, `WordCandidate`, `MeaningCandidate`, etc.
- `PhonoFunctionalReadiness` layers must forbid: `SyllableCandidate`, `PronunciationCandidate`, etc.

**Violation Example:**
```python
# WRONG: empty forbidden_outputs in qiyas layer
forbidden_outputs=()
```

### 3. Evidence Claim Grammar

All evidence claims must follow allowed grammar patterns. Claims using forbidden patterns must be rejected.

**Violation Examples:**
- Using `diff:carrier_mismatch:detected` instead of `fariq:carrier_mismatch:present`
- Using `residual:unprocessed:present` as evidence claim

### 4. Defer and Fariq Status

Evidence claims must produce correct candidate statuses:
- `defer:*:present` → `CandidateStatus.DEFERRED`
- `fariq:*:present` → `CandidateStatus.BLOCKED` with `blocking_fariq_present`

**Violation Examples:**
- `defer:*:present` producing `ACCEPTED` status
- `fariq:*:present` not setting `blocking_fariq_present`

### 5. Rank Ceiling

Candidate rank must never exceed the minimum of all inputs:

```
candidate.rank ≤ min(
    rule.rank_ceiling,
    asl.rank,
    far.rank,
    evidence.rank
)
```

**Layer-Specific Rank Ceilings:**
- Form-level layers (AtomicUnit, Haraka) cannot produce rank > `EvidenceRank.FORM`
- Phonological layers cannot exceed `EvidenceRank.PATTERN`

**Violation Example:**
- AtomicUnit producing candidate with `EvidenceRank.MEANING`

### 6. Identity and Trace Disjointness

For every candidate:
```
identity_ids ∩ trace_ids = ∅
```

A candidate's own identity must not appear in its trace.

**Violation Example:**
```python
# WRONG: identity overlaps with trace
identity_ids=("id:abc",)
trace_ids=("id:abc", "id:xyz")  # "id:abc" appears in both
```

### 7. Candidate Boundaries

Each layer produces **only** its declared `output_candidate_type`. No layer produces types in its `forbidden_outputs`.

**Examples:**
- `AtomicUnitAdapter` produces only `AtomicUnitCandidate`
- `HarakaAdapter` produces only `HarakaCandidate`
- `PhonoFunctionalUnit` layers never produce `SyllableCandidate`

**Violation Example:**
- AtomicUnitAdapter producing `SyllableCandidate`

### 8. SlotGeometry Protocol

`SlotGeometry.slots_for()` must:
- Return sequence of `SlotSpec` only
- NOT call `QiyasKernel`
- NOT produce `CandidateSet`

SlotGeometry is a **declarative specification**, not an execution engine.

**Violation Examples:**
- SlotGeometry calling `kernel.apply()`
- `slots_for()` returning `CandidateSet`

### 9. SlotPolicy Consistency

`SlotDifferencePolicy` categories must be mutually disjoint:
- `invalidating_differences ∩ blocking_differences = ∅`
- `invalidating_differences ∩ non_blocking_differences = ∅`
- `blocking_differences ∩ non_blocking_differences = ∅`
- `invalidating_differences ∩ deferring_differences = ∅`

**Violation Example:**
```python
# WRONG: same difference in multiple categories
invalidating_differences=("diff_a",)
blocking_differences=("diff_a", "diff_b")  # diff_a appears in both
```

### 10. Adapter Validation Rigor

Adapters must validate **actual attributes**, not just ID presence.

**Violation Example:**
```python
# WRONG: treating non-empty ID as validation
if candidate.candidate_id:
    claims.add("wasf:valid:evidenced")  # No actual validation!
```

**Correct Approach:**
```python
# RIGHT: validate actual attributes
if is_arabic_letter(candidate.value):
    claims.add("wasf:carrier_is_arabic:evidenced")
```

## Running Constitutional Tests

### Run All Constitutional Tests
```bash
PYTHONPATH=src python -m pytest -m constitution
```

### Run Specific Constitutional Test Categories
```bash
# Evidence claim grammar
PYTHONPATH=src python -m pytest -m evidence_claims

# Rank invariants
PYTHONPATH=src python -m pytest -m rank

# Identity and trace
PYTHONPATH=src python -m pytest -m identity_trace

# Candidate boundaries
PYTHONPATH=src python -m pytest -m no_higher_outputs

# SlotGeometry protocol
PYTHONPATH=src python -m pytest -m slot_geometry
```

### Run Constitutional Tests for Specific Component
```bash
# Kernel constitutional tests
PYTHONPATH=src python -m pytest -m "constitution and kernel"

# Adapter constitutional tests
PYTHONPATH=src python -m pytest -m "constitution and adapter"

# Rule constitutional tests
PYTHONPATH=src python -m pytest -m "constitution and rule"
```

## Test Fixtures

Constitutional tests use shared fixtures from `tests/qiyas_core/fixtures/`:

- `nodes.py` - Node factories (`make_unicode_node`, `make_haraka_node`, etc.)
- `evidence.py` - Evidence factories (`make_evidence_set`, `make_wasf_evidence`, etc.)
- `rules.py` - Rule factories (`make_minimal_rule`, `make_rule_missing_wadi`, etc.)
- `candidates.py` - Candidate factories (`make_unicode_candidate`, etc.)
- `requests.py` - Request factories (`make_qiyas_request`, etc.)

## Constitutional Helpers

Helper functions in `tests/qiyas_core/constitutional_helpers.py` provide assertion utilities:

- `assert_evidence_claim_grammar(claim)` - validates claim follows allowed grammar
- `assert_forbidden_claim(claim)` - ensures claim is in forbidden list
- `assert_disjoint_ids(candidate)` - checks `identity_ids ∩ trace_ids = ∅`
- `assert_rank_ceiling(candidate, max_rank)` - validates rank doesn't exceed ceiling
- `assert_wadi_gates_complete(rule)` - all 6 gates present, no extras
- `assert_forbidden_outputs_present(rule)` - `forbidden_outputs` not empty for qiyas layers
- `assert_no_higher_outputs(candidates, forbidden_types)` - no candidates of forbidden types produced
- `assert_slot_policy_disjoint(policy)` - `SlotDifferencePolicy` categories don't overlap

## Adding New Constitutional Tests

When adding new constitutional tests:

1. **Use appropriate markers** - Tag with `@pytest.mark.constitution` and specific category markers
2. **Use shared fixtures** - Import from `tests/qiyas_core/fixtures/`
3. **Use constitutional helpers** - Import from `tests/qiyas_core/constitutional_helpers.py`
4. **Document the invariant** - Add clear docstring explaining what's being tested
5. **Include positive and negative cases** - Test both valid and invalid scenarios

Example:
```python
import pytest
from tests.qiyas_core.constitutional_helpers import assert_wadi_gates_complete
from tests.qiyas_core.fixtures.rules import make_minimal_rule, make_rule_missing_wadi

@pytest.mark.constitution
@pytest.mark.rule
class TestRuleConstitution:
    def test_all_six_wadi_gates_required(self):
        """Rules must have exactly 6 WadiGates"""
        rule = make_minimal_rule()
        assert_wadi_gates_complete(rule)  # Should pass

    def test_missing_wadi_gate_fails(self):
        """Rules missing any WadiGate must fail"""
        rule = make_rule_missing_wadi("sabab")
        with pytest.raises(AssertionError):
            assert_wadi_gates_complete(rule)
```

## What This Framework Prevents

The constitutional testing framework prevents:

1. **Evidence grammar violations** - `diff:*` or `residual:*` claims
2. **Status mapping errors** - `defer:*` not producing DEFERRED
3. **Rank inflation** - Candidates exceeding architectural rank ceilings
4. **Boundary violations** - Layers producing forbidden output types
5. **Identity conflicts** - Identity and trace ID overlap
6. **Policy contradictions** - Same difference in multiple policy categories
7. **Superficial validation** - Accepting candidates based on ID alone
8. **WadiGate violations** - Missing or extra gates
9. **Empty forbidden outputs** - Qiyas layers without output restrictions
10. **SlotGeometry execution** - Geometry calling kernel or producing candidates

## Success Criteria

The constitutional framework succeeds when:

- All 14 known constitutional violations have corresponding failing tests
- All current valid adapters/rules pass constitutional tests
- Pytest markers work correctly and prevent typos
- Fixtures eliminate test duplication
- Documentation clearly explains testing strategy
- Constitutional test coverage > 95%

## Next Steps

After establishing this framework:

1. Apply constitutional tests to harden existing PRs (e.g., PR #12 evidence issues)
2. Require constitutional compliance for new adapters/layers
3. Use constitutional tests to validate SlotGeometry adoption
4. Expand framework as new constitutional principles emerge
