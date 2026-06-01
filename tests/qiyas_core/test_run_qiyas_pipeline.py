"""
PR #27b — Regression test for the run_qiyas driver pipeline.

Pins the canonical flow established by PR #27:

    TypedCodePoint
        → LetterIdentityCarrier
        → HarakaFunctionCarrier
        → PositionCarrier
        → ConditionedTypedSequenceQiyas / CarrierBindingCandidate
        → SlotCandidate

Verifies that:

  1. process_text("بَ") produces an accepted ConditionedTypedSequenceQiyas step.
  2. process_text("بَ") produces an accepted SlotQiyas step.
  3. SlotQiyas is only accepted when a CarrierBindingCandidate (or other
     alignment proof) is present in the same character's trace AND the
     SlotQiyas step carries an `:alignment_ref:` trace pointing at the
     consumed alignment candidate.
  4. process_text("بَتْ") produces two accepted ConditionedTypedSequenceQiyas.
  5. process_text("بَتْ") produces two accepted SlotQiyas.
  6. No step or slot produces SlotGeometry.
  7. No step or slot produces FinalMeaning.
  8. No step or slot produces HukmCandidate.
  9. No step or slot produces RealityClaim.

Scope per the maintainer's PR #27b brief: this file ONLY. No other
modifications under src/qiyas_core/, run_qiyas.py, docs/, or experimental/.
"""

import importlib.util
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Locate and load run_qiyas.py as a module without touching its source.
#
# The module must be registered in sys.modules *before* exec_module is
# called, because run_qiyas.py defines @dataclass classes that resolve
# their type hints by looking the owning module up in sys.modules. If
# the registration is missing, Python's dataclass machinery raises
# AttributeError on `sys.modules.get(cls.__module__).__dict__`.
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
# Forbidden final-output candidate types — never appear anywhere in the
# pipeline output (CLAUDE.md §0, §3, §4 invariant 10).
# ---------------------------------------------------------------------------

_FORBIDDEN_OUTPUTS = frozenset({
    "SlotGeometry",
    "FinalMeaning",
    "HukmCandidate",
    "RealityClaim",
})


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _all_steps(reports):
    """Yield every LayerStep in every CharacterReport, plus the slot_step
    when present."""
    for r in reports:
        for s in r.steps:
            yield s
        if r.slot_step is not None:
            yield r.slot_step


def _accepted_steps_by_layer(reports, layer_name):
    return [
        s for s in _all_steps(reports)
        if s.layer == layer_name and s.status == "accepted"
    ]


def _accepted_slot_steps(reports):
    return [
        r.slot_step for r in reports
        if r.slot_step is not None and r.slot_step.status == "accepted"
    ]


# ---------------------------------------------------------------------------
# 1. بَ → an accepted ConditionedTypedSequenceQiyas step.
# ---------------------------------------------------------------------------


def test_baa_fatha_produces_accepted_cts_step():
    reports = process_text("بَ")
    cts_accepted = _accepted_steps_by_layer(
        reports, "ConditionedTypedSequenceQiyas"
    )
    assert len(cts_accepted) == 1
    step = cts_accepted[0]
    assert step.candidate_type == "CarrierBindingCandidate"
    assert step.rule_id == "conditioned_typed_sequence.carrier_binding"


# ---------------------------------------------------------------------------
# 2. بَ → an accepted SlotQiyas step.
# ---------------------------------------------------------------------------


def test_baa_fatha_produces_accepted_slot_step():
    reports = process_text("بَ")
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 1
    slot = accepted_slots[0]
    assert slot.layer == "SlotQiyas"
    assert slot.candidate_type == "SlotCandidate"
    assert slot.rule_id == "slot.composition"


# ---------------------------------------------------------------------------
# 3. SlotQiyas is only accepted when a CarrierBindingCandidate / Alignment
#    is present in the same character's trace AND the SlotQiyas step
#    carries an :alignment_ref: trace pointing at that candidate.
# ---------------------------------------------------------------------------


def test_slot_accepted_implies_alignment_consumed_in_trace():
    """For every character whose slot_step is accepted, the corresponding
    report must contain an accepted ConditionedTypedSequenceQiyas step,
    AND the slot step's trace_ids must include an `:alignment_ref:`
    entry — the structural witness that the slot consumed an explicit
    alignment proof (SlotLayerAdapter writes this trace when the four
    pillars are present, see slot_adapter.py)."""

    for sample in ("بَ", "بَتْ"):
        reports = process_text(sample)
        for r in reports:
            if r.slot_step is None or r.slot_step.status != "accepted":
                continue

            cts_in_report = [
                s for s in r.steps
                if s.layer == "ConditionedTypedSequenceQiyas"
                and s.status == "accepted"
            ]
            assert cts_in_report, (
                f"sample={sample!r} char={r.char!r} index={r.index}: "
                "accepted Slot has no accepted CTS step in the same report"
            )

            alignment_refs = [
                t for t in r.slot_step.trace_ids if ":alignment_ref:" in t
            ]
            assert alignment_refs, (
                f"sample={sample!r} char={r.char!r} index={r.index}: "
                "accepted Slot is missing an :alignment_ref: trace; the "
                "slot adapter only writes this when an alignment proof "
                "is consumed."
            )


def test_isolated_letter_without_haraka_produces_no_slot():
    """A letter without an immediately-following haraka cannot form a
    slot in this driver (no carrier+mark adjacency). Therefore there is
    no CTS step and no Slot step for that letter."""
    reports = process_text("ب")  # just a baa, no haraka
    cts_accepted = _accepted_steps_by_layer(reports, "ConditionedTypedSequenceQiyas")
    accepted_slots = _accepted_slot_steps(reports)
    assert len(cts_accepted) == 0
    assert len(accepted_slots) == 0


# ---------------------------------------------------------------------------
# 4. بَتْ → two accepted CTS steps.
# ---------------------------------------------------------------------------


def test_baa_fatha_taa_sukun_produces_two_cts_accepted():
    reports = process_text("بَتْ")
    cts_accepted = _accepted_steps_by_layer(
        reports, "ConditionedTypedSequenceQiyas"
    )
    assert len(cts_accepted) == 2


# ---------------------------------------------------------------------------
# 5. بَتْ → two accepted Slot steps.
# ---------------------------------------------------------------------------


def test_baa_fatha_taa_sukun_produces_two_slot_accepted():
    reports = process_text("بَتْ")
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 2
    # Both must be SlotCandidate, not anything else (no jump to SlotGeometry).
    for slot in accepted_slots:
        assert slot.candidate_type == "SlotCandidate"


# ---------------------------------------------------------------------------
# 6, 7, 8, 9 — none of the forbidden final-output candidate types
# appear anywhere in the pipeline output.
# ---------------------------------------------------------------------------


def test_driver_never_emits_slot_geometry():
    for sample in ("بَ", "بَتْ", "اَكتب", "بَتَكُلَ"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "SlotGeometry", (
                f"sample={sample!r}: a step produced SlotGeometry"
            )


def test_driver_never_emits_final_meaning():
    for sample in ("بَ", "بَتْ", "اَكتب"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "FinalMeaning"


def test_driver_never_emits_hukm_candidate():
    for sample in ("بَ", "بَتْ", "اَكتب"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "HukmCandidate"


def test_driver_never_emits_reality_claim():
    for sample in ("بَ", "بَتْ", "اَكتب"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "RealityClaim"


def test_driver_emits_no_forbidden_outputs_at_all():
    """Single sweep that simultaneously checks all four forbidden
    final-output types across a wider sample, including non-Arabic
    characters that exercise the blocked path."""
    for sample in ("بَ", "بَتْ", "اَكتب hi", "كظضَرَسشسش"):
        reports = process_text(sample)
        produced = {s.candidate_type for s in _all_steps(reports)}
        assert produced.isdisjoint(_FORBIDDEN_OUTPUTS), (
            f"sample={sample!r}: forbidden output types appeared: "
            f"{produced & _FORBIDDEN_OUTPUTS}"
        )


# ---------------------------------------------------------------------------
# Bonus structural check — the canonical layer sequence appears in order
# for every letter that participates in a slot. This guards against
# accidental re-ordering of the parallel proofs in the driver.
# ---------------------------------------------------------------------------


def test_layer_sequence_for_letter_that_forms_a_slot():
    """For a letter that does form a slot in this driver, the steps in
    its CharacterReport must appear in the canonical order:

        UnicodeQiyas
        → TypedCodePointClassificationQiyas
        → LetterIdentityQiyas
        → PositionQiyas[*]
        → ConditionedTypedSequenceQiyas
        (then slot_step on the same report = SlotQiyas)
    """
    reports = process_text("بَ")
    letter_report = reports[0]
    layers_in_order = [s.layer for s in letter_report.steps]

    # PositionQiyas layer label is suffixed with [INITIAL/MEDIAL/...] in
    # the driver, so we match by prefix.
    assert layers_in_order[0] == "UnicodeQiyas"
    assert layers_in_order[1] == "TypedCodePointClassificationQiyas"
    assert layers_in_order[2] == "LetterIdentityQiyas"
    assert layers_in_order[3].startswith("PositionQiyas")
    assert layers_in_order[4] == "ConditionedTypedSequenceQiyas"
    assert letter_report.slot_step is not None
    assert letter_report.slot_step.layer == "SlotQiyas"
