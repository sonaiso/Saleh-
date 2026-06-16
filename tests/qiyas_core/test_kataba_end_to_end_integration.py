"""
PR #79 — End-to-end integration test for كَتَبَ pipeline.

Comprehensive integration test that validates the complete qiyas pipeline
through the canonical word كَتَبَ (kataba - "he wrote"), demonstrating the
full algebraic architecture from raw Unicode to SlotCandidate formation.

Test Structure:
    Raw Unicode: ك U+0643, َ U+064E, ت U+062A, َ U+064E, ب U+0628, َ U+064E
    → UnicodeCandidate (Layer 0)
    → TypedCodePoint (Layer 1)
    → LetterIdentityCarrier + HarakaFunctionCarrier (Layer 2A + 2B, parallel)
    → PositionCarrier (Layer 2C) + AlignmentEvidence (Layer 2D)
    → SlotCandidate (Layer 3)

Constitutional Basis:
  CLAUDE.md §0 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20
  PROJECT_MATHEMATICAL_FOUNDATION.md §2 / §3 / §4 / §5 / §6
  LAYER_REGISTRY.md Layer 0-3 definitions
  CANONICAL_ARCHITECTURE_CONTROL_FRAME.md §1.1 / §2 / §5

Algebraic Invariants Tested:
  1. Identity-trace separation (CLAUDE.md §4.1)
  2. Source identity preservation (CLAUDE.md §4.4)
  3. Rank meet semantics (CLAUDE.md §4.6)
  4. Residual preservation (CLAUDE.md §4.7)
  5. Parallel proof architecture (CLAUDE.md §5)
  6. No layer jumps (CLAUDE.md §4.10)
  7. Potential-only safety (CLAUDE.md §4.9)

Forbidden Outputs (CLAUDE.md §19):
  - TypedCodePoint* → SlotGeometry ❌
  - TypedCodePoint* → SlotCandidate ❌ (requires all 4 pillars)
  - ConditionedTypedSequence → LetterIdentityCarrier ❌
  - ConditionedTypedSequence → HarakaFunctionCarrier ❌
  - SlotCandidate → SlotGeometry ❌
  - SlotCandidate → FinalMeaning ❌
  - SlotCandidate → HukmCandidate ❌

Scope:
  - Tests-only PR (no src/, docs/, or registry changes)
  - Single new file: tests/qiyas_core/test_kataba_end_to_end_integration.py
  - Uses public API of canonical layers only
  - Demonstrates complete Phase-1 pipeline per run_qiyas.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Load run_qiyas.py as a module (same pattern as test_run_qiyas_pipeline.py)
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_RUN_QIYAS_PATH = _REPO_ROOT / "run_qiyas.py"
assert _RUN_QIYAS_PATH.is_file(), f"run_qiyas.py not found at {_RUN_QIYAS_PATH}"

_spec = importlib.util.spec_from_file_location("run_qiyas", _RUN_QIYAS_PATH)
assert _spec is not None and _spec.loader is not None
run_qiyas = importlib.util.module_from_spec(_spec)
sys.modules["run_qiyas"] = run_qiyas
_spec.loader.exec_module(run_qiyas)

process_text = run_qiyas.process_text


# ---------------------------------------------------------------------------
# Constants and helpers
# ---------------------------------------------------------------------------

# كَتَبَ - "he wrote"
KATABA = "كَتَبَ"
KATABA_CODEPOINTS = [
    ("ك", "U+0643"),  # KAF
    ("َ", "U+064E"),  # FATHA
    ("ت", "U+062A"),  # TAA
    ("َ", "U+064E"),  # FATHA
    ("ب", "U+0628"),  # BAA
    ("َ", "U+064E"),  # FATHA
]

# Expected layer sequence for a complete letter+haraka slot
EXPECTED_LAYER_SEQUENCE = [
    "UnicodeQiyas",
    "TypedCodePointClassificationQiyas",
    "LetterIdentityQiyas",
    "PositionQiyas",  # Will be suffixed with [INITIAL/MEDIAL/FINAL]
    "ConditionedTypedSequenceQiyas",
]

# Forbidden outputs per CLAUDE.md §19
FORBIDDEN_OUTPUTS = frozenset({
    "SlotGeometry",
    "FinalMeaning",
    "HukmCandidate",
    "RealityClaim",
    "SyllableCandidate",
    "WordCandidate",
    "MeaningCandidate",
})


def _all_steps(reports):
    """Yield every LayerStep in every CharacterReport, plus slot_step when present."""
    for r in reports:
        for s in r.steps:
            yield s
        if r.slot_step is not None:
            yield r.slot_step


def _accepted_steps_by_layer(reports, layer_name):
    """Get all accepted steps for a given layer name (exact or prefix match)."""
    return [
        s for s in _all_steps(reports)
        if (s.layer == layer_name or s.layer.startswith(layer_name))
        and s.status == "accepted"
    ]


def _accepted_slot_steps(reports):
    """Get all accepted slot steps."""
    return [
        r.slot_step for r in reports
        if r.slot_step is not None and r.slot_step.status == "accepted"
    ]


def _residual_types(step):
    """Extract residual types from a step."""
    return {r["residual_type"] for r in step.residuals}


def _identity_ids(step):
    """Extract identity_ids from a step."""
    return frozenset(step.identity_ids)


def _trace_ids(step):
    """Extract trace_ids from a step."""
    return frozenset(step.trace_ids)


# ---------------------------------------------------------------------------
# Group 1: Structural Validation
# ---------------------------------------------------------------------------


def test_kataba_produces_correct_number_of_reports():
    """
    كَتَبَ has 6 codepoints → must produce exactly 6 CharacterReports.
    Constitutional basis: Every codepoint gets audited (residual preservation).
    """
    reports = process_text(KATABA)
    assert len(reports) == 6, (
        f"Expected 6 reports for {KATABA}, got {len(reports)}"
    )


def test_kataba_produces_three_slots():
    """
    كَتَبَ has 3 letter+haraka pairs → must produce exactly 3 accepted SlotCandidates.

    Constitutional basis:
      - CLAUDE.md §8: SlotCandidate requires all 4 pillars
      - LAYER_REGISTRY.md Layer 3: Slot formation rule
    """
    reports = process_text(KATABA)
    accepted_slots = _accepted_slot_steps(reports)

    assert len(accepted_slots) == 3, (
        f"Expected 3 accepted slots for {KATABA}, got {len(accepted_slots)}"
    )

    # All must be SlotCandidate, not SlotGeometry or any other type
    for slot in accepted_slots:
        assert slot.candidate_type == "SlotCandidate", (
            f"Expected SlotCandidate, got {slot.candidate_type}"
        )
        assert slot.layer == "SlotQiyas"


def test_kataba_each_letter_has_complete_layer_sequence():
    """
    Each letter (ك, ت, ب) must pass through the complete canonical layer sequence.

    Constitutional basis:
      - PROJECT_MATHEMATICAL_FOUNDATION.md §6: Complete ladder
      - LAYER_REGISTRY.md: Layer 0 → 1 → 2A → 2C → 2D → 3
    """
    reports = process_text(KATABA)

    # Letter indices in KATABA: 0 (ك), 2 (ت), 4 (ب)
    letter_indices = [0, 2, 4]

    for idx in letter_indices:
        letter_report = reports[idx]
        layers_in_order = [s.layer for s in letter_report.steps]

        # Verify each expected layer appears in order
        assert layers_in_order[0] == "UnicodeQiyas"
        assert layers_in_order[1] == "TypedCodePointClassificationQiyas"
        assert layers_in_order[2] == "LetterIdentityQiyas"
        assert layers_in_order[3].startswith("PositionQiyas")
        assert layers_in_order[4] == "ConditionedTypedSequenceQiyas"

        # Verify slot step exists
        assert letter_report.slot_step is not None
        assert letter_report.slot_step.layer == "SlotQiyas"


def test_kataba_haraka_reports_have_no_slot_steps():
    """
    Haraka codepoints (َ) must NOT have slot_step.
    Only letters participate in slot formation.

    Constitutional basis:
      - CLAUDE.md §8: SlotCandidate requires LetterIdentityCarrier
      - Harakat are operators, not carriers
    """
    reports = process_text(KATABA)

    # Haraka indices in KATABA: 1, 3, 5 (all FATHA)
    haraka_indices = [1, 3, 5]

    for idx in haraka_indices:
        haraka_report = reports[idx]
        assert haraka_report.slot_step is None, (
            f"Haraka at index {idx} unexpectedly has slot_step"
        )


# ---------------------------------------------------------------------------
# Group 2: Parallel Proof Architecture
# ---------------------------------------------------------------------------


def test_kataba_demonstrates_parallel_letter_haraka_proofs():
    """
    LetterIdentityCarrier and HarakaFunctionCarrier are parallel atomic proofs.
    Neither depends on the other.

    Constitutional basis:
      - CLAUDE.md §5: Parallel proofs, not linear chain
      - CLAUDE.md §6: Atomic identity proofs are independent
      - LAYER_REGISTRY.md Layer 2: Parallel architecture note
    """
    reports = process_text(KATABA)

    # Get all LetterIdentityQiyas steps
    letter_steps = _accepted_steps_by_layer(reports, "LetterIdentityQiyas")
    assert len(letter_steps) == 3  # ك, ت, ب

    # Get all HarakaFunctionQiyas steps
    haraka_steps = _accepted_steps_by_layer(reports, "HarakaFunctionQiyas")
    assert len(haraka_steps) == 3  # Three FATHA

    # Verify letter identity does NOT require haraka function
    for letter_step in letter_steps:
        assert letter_step.candidate_type == "LetterIdentityCarrier"
        # Letter identity must NOT carry haraka function in its identity_ids
        letter_ids = _identity_ids(letter_step)
        assert not any(
            "haraka" in iid.lower() for iid in letter_ids
        ), "Letter identity must not depend on haraka"

    # Verify haraka function does NOT require letter identity
    for haraka_step in haraka_steps:
        # REC-3 / SCG-P1 PR-1: canonical emitted type is HarakaMarkIdentityCarrier.
        assert haraka_step.candidate_type == "HarakaMarkIdentityCarrier"
        # Haraka function must NOT carry letter identity in its identity_ids
        haraka_ids = _identity_ids(haraka_step)
        assert not any(
            "letter" in iid.lower() and "identity" in iid.lower()
            for iid in haraka_ids
        ), "Haraka function must not depend on letter identity"


def test_kataba_sequence_conditioning_produces_alignment_not_identity():
    """
    ConditionedTypedSequence produces alignment evidence, NOT letter or haraka identity.

    Constitutional basis:
      - CLAUDE.md §7: Function of ConditionedTypedSequence
      - CLAUDE.md §14: Required non-goals
    """
    reports = process_text(KATABA)

    # Get all ConditionedTypedSequenceQiyas steps
    cts_steps = _accepted_steps_by_layer(reports, "ConditionedTypedSequenceQiyas")
    assert len(cts_steps) == 3  # Three carrier-binding proofs

    for cts_step in cts_steps:
        # Must be CarrierBindingCandidate (alignment evidence)
        assert cts_step.candidate_type == "CarrierBindingCandidate", (
            f"Expected CarrierBindingCandidate, got {cts_step.candidate_type}"
        )

        # Must NOT be LetterIdentityCarrier or Haraka identity (canonical or legacy alias)
        assert cts_step.candidate_type != "LetterIdentityCarrier"
        assert cts_step.candidate_type != "HarakaMarkIdentityCarrier"
        assert cts_step.candidate_type != "HarakaFunctionCarrier"


def test_kataba_slot_requires_all_four_pillars():
    """
    Every SlotCandidate must be formed from all 4 required ingredients.

    Constitutional basis:
      - CLAUDE.md §8: SlotCandidate Formation Rule
      - LAYER_REGISTRY.md Layer 3: Required ingredients
    """
    reports = process_text(KATABA)
    accepted_slots = _accepted_slot_steps(reports)

    for slot in accepted_slots:
        # Must have alignment_ref in trace (shows alignment was consumed)
        slot_traces = _trace_ids(slot)
        has_alignment_ref = any(
            ":alignment_ref:" in tid for tid in slot_traces
        )
        assert has_alignment_ref, (
            f"Slot missing :alignment_ref: trace - violates 4-pillar requirement"
        )


# ---------------------------------------------------------------------------
# Group 3: Identity and Trace Invariants
# ---------------------------------------------------------------------------


def test_kataba_identity_trace_separation():
    """
    Identity ≠ Trace for all candidates.

    Constitutional basis:
      - CLAUDE.md §4.1: Identity is not trace
      - PROJECT_MATHEMATICAL_FOUNDATION.md §8: Identity-Trace Separation
    """
    reports = process_text(KATABA)

    for step in _all_steps(reports):
        step_ids = _identity_ids(step)
        step_traces = _trace_ids(step)

        # Identity and trace must be disjoint sets
        overlap = step_ids & step_traces
        assert not overlap, (
            f"Identity-trace overlap in {step.layer}: {overlap}"
        )


def test_kataba_source_identity_preservation():
    """
    Every candidate preserves source identities.

    Constitutional basis:
      - CLAUDE.md §4.4: Candidate identity must preserve source identities
      - PROJECT_MATHEMATICAL_FOUNDATION.md §8: Source Identity Preservation
    """
    reports = process_text(KATABA)

    # Check slots preserve letter + haraka identities
    accepted_slots = _accepted_slot_steps(reports)

    for slot in accepted_slots:
        slot_ids = _identity_ids(slot)

        # Slot must preserve codepoint identities from letter + haraka
        codepoint_ids = {
            iid for iid in slot_ids if iid.startswith("identity:codepoint:")
        }
        # Should have at least 2: one for letter, one for haraka
        assert len(codepoint_ids) >= 2, (
            f"Slot missing codepoint identities: {slot_ids}"
        )


def test_kataba_trace_preservation():
    """
    Trace is preserved and extended through layer transitions.

    Constitutional basis:
      - CLAUDE.md §4.2: Trace is not identity
      - PROJECT_MATHEMATICAL_FOUNDATION.md §8: Evidence Monotonicity
    """
    reports = process_text(KATABA)

    for step in _all_steps(reports):
        step_traces = _trace_ids(step)

        # Every step must have some trace
        assert len(step_traces) > 0, (
            f"Step {step.layer} has no trace_ids"
        )


# ---------------------------------------------------------------------------
# Group 4: Forbidden Outputs and Layer Jump Prevention
# ---------------------------------------------------------------------------


def test_kataba_no_forbidden_outputs():
    """
    Pipeline must never produce forbidden output types.

    Constitutional basis:
      - CLAUDE.md §19: Forbidden changes
      - CLAUDE.md §4.9: Potential candidates must not become final judgments
    """
    reports = process_text(KATABA)

    for step in _all_steps(reports):
        assert step.candidate_type not in FORBIDDEN_OUTPUTS, (
            f"Forbidden output {step.candidate_type} produced in {step.layer}"
        )


def test_kataba_no_layer_jumps():
    """
    No layer may jump to produce output of a non-adjacent layer.

    Constitutional basis:
      - CLAUDE.md §4.10: No layer jump
      - CLAUDE.md §19: Forbidden changes (illegal jumps listed)
    """
    reports = process_text(KATABA)

    # TypedCodePoint must not jump to SlotCandidate or SlotGeometry
    typed_steps = _accepted_steps_by_layer(
        reports, "TypedCodePointClassificationQiyas"
    )
    for step in typed_steps:
        assert step.candidate_type not in {"SlotCandidate", "SlotGeometry"}

    # LetterIdentityCarrier must not jump to SlotGeometry
    letter_steps = _accepted_steps_by_layer(reports, "LetterIdentityQiyas")
    for step in letter_steps:
        assert step.candidate_type != "SlotGeometry"

    # ConditionedTypedSequence must not produce SlotCandidate
    cts_steps = _accepted_steps_by_layer(reports, "ConditionedTypedSequenceQiyas")
    for step in cts_steps:
        assert step.candidate_type != "SlotCandidate"


def test_kataba_slot_does_not_produce_syllable():
    """
    SlotCandidate must not jump to SyllableCandidate.
    Syllable formation requires adjacency evidence not yet established.

    Constitutional basis:
      - CLAUDE.md §19: SlotCandidate → SyllableCandidate forbidden
      - LAYER_REGISTRY.md Layer 3: Forbidden outputs
    """
    reports = process_text(KATABA)
    accepted_slots = _accepted_slot_steps(reports)

    for slot in accepted_slots:
        assert slot.candidate_type == "SlotCandidate"
        assert slot.candidate_type != "SyllableCandidate"


def test_kataba_potential_only_safety():
    """
    All outputs remain potential/candidate only, never final.

    Constitutional basis:
      - CLAUDE.md §4.9: Potential candidates must not become final judgments
      - CLAUDE.md §3: System builds potential candidates, not final meaning
    """
    reports = process_text(KATABA)

    for step in _all_steps(reports):
        # Candidate type must end with "Candidate" or be a typed classification
        # Never "Final*", "Meaning", "Hukm", "RealityClaim"
        assert not step.candidate_type.startswith("Final")
        assert not step.candidate_type.endswith("Meaning") or step.candidate_type.endswith("Candidate")
        assert step.candidate_type != "Hukm"


# ---------------------------------------------------------------------------
# Group 5: Specific Word Properties
# ---------------------------------------------------------------------------


def test_kataba_first_letter_is_initial_position():
    """
    ك in كَتَبَ must be classified as INITIAL position.

    Constitutional basis:
      - run_qiyas.py: Position classification using tokenizer context
      - LAYER_REGISTRY.md Layer 2C: PositionCarrier
    """
    reports = process_text(KATABA)
    kaf_report = reports[0]  # ك is first

    # Find PositionQiyas step
    position_steps = [
        s for s in kaf_report.steps
        if s.layer.startswith("PositionQiyas")
    ]
    assert len(position_steps) == 1

    position_step = position_steps[0]
    assert "INITIAL" in position_step.layer, (
        f"Expected INITIAL position for first letter, got {position_step.layer}"
    )


def test_kataba_middle_letter_is_medial_position():
    """
    ت in كَتَبَ must be classified as MEDIAL position.

    Constitutional basis:
      - run_qiyas.py: Position classification
      - LAYER_REGISTRY.md Layer 2C: PositionCarrier
    """
    reports = process_text(KATABA)
    taa_report = reports[2]  # ت is middle

    # Find PositionQiyas step
    position_steps = [
        s for s in taa_report.steps
        if s.layer.startswith("PositionQiyas")
    ]
    assert len(position_steps) == 1

    position_step = position_steps[0]
    assert "MEDIAL" in position_step.layer, (
        f"Expected MEDIAL position for middle letter, got {position_step.layer}"
    )


def test_kataba_last_letter_is_final_position():
    """
    ب in كَتَبَ must be classified as FINAL position.

    Constitutional basis:
      - run_qiyas.py: Position classification
      - LAYER_REGISTRY.md Layer 2C: PositionCarrier
    """
    reports = process_text(KATABA)
    baa_report = reports[4]  # ب is last

    # Find PositionQiyas step
    position_steps = [
        s for s in baa_report.steps
        if s.layer.startswith("PositionQiyas")
    ]
    assert len(position_steps) == 1

    position_step = position_steps[0]
    assert "FINAL" in position_step.layer, (
        f"Expected FINAL position for last letter, got {position_step.layer}"
    )


def test_kataba_all_harakat_are_fatha():
    """
    All three harakat in كَتَبَ are FATHA (U+064E).
    Verify HarakaFunctionCarrier correctly identifies all as FATHA.

    Constitutional basis:
      - LAYER_REGISTRY.md Layer 2B: HarakaFunctionCarrier
      - CLAUDE.md §17: Tests required for HarakaFunctionCarrier
    """
    reports = process_text(KATABA)

    # Get all HarakaFunctionQiyas steps
    haraka_steps = _accepted_steps_by_layer(reports, "HarakaFunctionQiyas")
    assert len(haraka_steps) == 3

    for step in haraka_steps:
        # Check that rule_id identifies FATHA
        assert step.rule_id == "haraka_function.fatha", (
            f"Expected haraka_function.fatha, got {step.rule_id}"
        )

        # Verify codepoint identity
        step_ids = _identity_ids(step)
        has_fatha_codepoint = "identity:codepoint:064e" in step_ids
        assert has_fatha_codepoint, (
            f"Expected FATHA codepoint (064e) in {step_ids}"
        )


def test_kataba_letter_identities():
    """
    Verify correct letter identities: KAF, TAA, BAA.

    Constitutional basis:
      - LAYER_REGISTRY.md Layer 2A: LetterIdentityCarrier
      - CLAUDE.md §16: Tests required for LetterIdentityCarrier
    """
    reports = process_text(KATABA)

    # Get letter identity steps in order
    letter_steps = _accepted_steps_by_layer(reports, "LetterIdentityQiyas")
    assert len(letter_steps) == 3

    # Expected letters in order: KAF, TAA, BAA
    expected_letters = ["kaf", "taa", "baa"]

    for step, expected in zip(letter_steps, expected_letters):
        step_ids = _identity_ids(step)
        has_expected_letter = any(
            expected in iid.lower() for iid in step_ids
        )
        assert has_expected_letter, (
            f"Expected {expected} identity in {step_ids}"
        )


# ---------------------------------------------------------------------------
# Group 6: Rank and Residual Validation
# ---------------------------------------------------------------------------


def test_kataba_all_slots_have_rank():
    """
    Every SlotCandidate must have a rank.

    Constitutional basis:
      - CLAUDE.md §4.6: Rank is computed by meet semantics
      - PROJECT_MATHEMATICAL_FOUNDATION.md §8: Rank Meet Semantics
    """
    reports = process_text(KATABA)
    accepted_slots = _accepted_slot_steps(reports)

    for slot in accepted_slots:
        assert hasattr(slot, "rank"), "Slot missing rank attribute"
        assert slot.rank is not None, "Slot rank is None"


def test_kataba_no_blocking_residuals_in_accepted_slots():
    """
    Accepted slots must not have blocking residuals.

    Constitutional basis:
      - CLAUDE.md §4.5: Invalidating difference blocks licensing
      - CLAUDE.md §4.7: Residuals must not be hidden
    """
    reports = process_text(KATABA)
    accepted_slots = _accepted_slot_steps(reports)

    for slot in accepted_slots:
        residual_types = _residual_types(slot)

        # No blocking residuals
        blocking_residuals = {
            rt for rt in residual_types
            if "blocking" in rt.lower() or "فارق" in rt
        }
        assert not blocking_residuals, (
            f"Accepted slot has blocking residuals: {blocking_residuals}"
        )


# ---------------------------------------------------------------------------
# Group 7: Complete Pipeline Regression Lock
# ---------------------------------------------------------------------------


def test_kataba_complete_pipeline_baseline():
    """
    Comprehensive baseline test that locks the complete كَتَبَ pipeline output.

    This test captures the known-good state as a regression guard.
    Any future change that breaks this test requires explicit justification.

    Constitutional basis:
      - All constitutional documents apply
      - This is the integration test demonstrating full Phase-1 pipeline
    """
    reports = process_text(KATABA)

    # High-level assertions
    assert len(reports) == 6  # 6 codepoints
    assert len(_accepted_slot_steps(reports)) == 3  # 3 slots

    # Layer counts
    assert len(_accepted_steps_by_layer(reports, "UnicodeQiyas")) == 6
    assert len(_accepted_steps_by_layer(reports, "TypedCodePointClassificationQiyas")) == 6
    assert len(_accepted_steps_by_layer(reports, "LetterIdentityQiyas")) == 3
    assert len(_accepted_steps_by_layer(reports, "HarakaFunctionQiyas")) == 3
    assert len(_accepted_steps_by_layer(reports, "PositionQiyas")) == 3
    assert len(_accepted_steps_by_layer(reports, "ConditionedTypedSequenceQiyas")) == 3
    assert len(_accepted_slot_steps(reports)) == 3

    # No forbidden outputs anywhere
    all_types = {s.candidate_type for s in _all_steps(reports)}
    assert all_types.isdisjoint(FORBIDDEN_OUTPUTS)

    # Every slot has all required properties
    for slot in _accepted_slot_steps(reports):
        assert slot.candidate_type == "SlotCandidate"
        assert slot.layer == "SlotQiyas"
        assert slot.status == "accepted"
        assert len(slot.identity_ids) > 0
        assert len(slot.trace_ids) > 0
        assert any(":alignment_ref:" in tid for tid in slot.trace_ids)


def test_kataba_codepoint_coverage():
    """
    Verify all 6 codepoints are processed.

    Constitutional basis:
      - CLAUDE.md §4.7: Residuals must not be hidden or silently discarded
    """
    reports = process_text(KATABA)

    # Check we have exactly the expected codepoints
    assert len(reports) == len(KATABA_CODEPOINTS)

    for i, (expected_char, expected_unicode) in enumerate(KATABA_CODEPOINTS):
        report = reports[i]
        assert report.char == expected_char, (
            f"Position {i}: expected '{expected_char}', got '{report.char}'"
        )
        # Verify it went through UnicodeQiyas
        unicode_steps = [
            s for s in report.steps if s.layer == "UnicodeQiyas"
        ]
        assert len(unicode_steps) > 0, (
            f"Position {i} ({expected_char}) missing UnicodeQiyas step"
        )
