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


# ===========================================================================
# Z5 — driver routes whitespace and boundary context through
# `SequenceContextTokenizer`. Per `PRE_QIYAS_TOKENIZER_CONSTITUTION.md`
# (Option C, §1 / §5 / §6 / §8), whitespace and boundary characters are
# pre-qiyas sequence-framing markers. They must not become
# `UnicodeCandidate`, `TypedCodePoint`, or any other `Candidate`; they
# must not become identity; and they must not become slot material.
# Position context (INITIAL/MEDIAL/FINAL/ISOLATED) is derived from
# tokenizer segments rather than from `is_boundary`.
# ===========================================================================


def _all_typed_candidate_types(reports):
    """Every `candidate_type` produced by any step / slot, across reports."""
    return {s.candidate_type for s in _all_steps(reports)}


def _typed_candidate_types_for(reports, index):
    """Candidate types produced by the steps belonging to one character."""
    r = reports[index]
    types = {s.candidate_type for s in r.steps}
    if r.slot_step is not None:
        types.add(r.slot_step.candidate_type)
    return types


# ---------------------------------------------------------------------------
# 1. "بَ" — still produces exactly one accepted SlotQiyas step.
# ---------------------------------------------------------------------------


def test_run_qiyas_baa_fatha_still_accepts_one_slot():
    reports = process_text("بَ")
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 1
    assert accepted_slots[0].candidate_type == "SlotCandidate"


# ---------------------------------------------------------------------------
# 2. "بَتْ" — still produces exactly two accepted SlotQiyas steps.
# ---------------------------------------------------------------------------


def test_run_qiyas_baa_fatha_taa_sukun_still_accepts_two_slots():
    reports = process_text("بَتْ")
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 2
    for s in accepted_slots:
        assert s.candidate_type == "SlotCandidate"


# ---------------------------------------------------------------------------
# 3. "بَ تْ" — binds inside each tokenizer segment only; no cross-whitespace
#    binding.
# ---------------------------------------------------------------------------


def test_run_qiyas_does_not_bind_across_whitespace():
    reports = process_text("بَ تْ")
    # Two segments → two slots (one per بَ / تْ pair). Crucially, the
    # carriers stay within their own segments — there is no slot whose
    # alignment crosses the whitespace at index 2.
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 2

    # The whitespace character is at text index 2 — neither slot may be
    # reported on that index, and the whitespace report itself carries
    # no SlotQiyas step.
    space_report = reports[2]
    assert space_report.slot_step is None
    # Both slots belong to letter positions, not to the whitespace.
    slot_indices = {r.index for r in reports if r.slot_step is not None}
    assert 2 not in slot_indices
    assert slot_indices == {0, 3}


# ---------------------------------------------------------------------------
# 4. "ب،َ" — does not bind across Arabic punctuation.
# ---------------------------------------------------------------------------


def test_run_qiyas_does_not_bind_across_punctuation():
    # ب at 0, ، at 1, َ at 2. The fatha must not bind to the baa across
    # the punctuation boundary marker; therefore no SlotQiyas step is
    # produced for any character.
    reports = process_text("ب،َ")
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 0
    # No accepted ConditionedTypedSequenceQiyas step either, since
    # carrier-binding was never invoked.
    cts_accepted = _accepted_steps_by_layer(reports, "ConditionedTypedSequenceQiyas")
    assert len(cts_accepted) == 0


# ---------------------------------------------------------------------------
# 5. Whitespace appears as a tokenizer marker / context evidence, never as
#    an accepted UnicodeCandidate or TypedCodePoint.
# ---------------------------------------------------------------------------


def test_run_qiyas_whitespace_is_tokenizer_context_not_candidate():
    reports = process_text("بَ تْ")
    space_report = reports[2]
    assert space_report.char == " "

    # Tokenizer surfaces whitespace as a boundary marker on the report.
    tm = space_report.tokenizer_marker
    assert tm is not None
    assert tm["marker_type"] == "whitespace_boundary_marker"
    assert tm["segment_id"] is not None

    # UnicodeQiyas attempts and blocks the whitespace codepoint — there is
    # no accepted UnicodeCandidate for it, and no TypedCodePoint is ever
    # constructed.
    unicode_step = next(s for s in space_report.steps if s.layer == "UnicodeQiyas")
    assert unicode_step.status != "accepted"
    typed_steps = [
        s for s in space_report.steps
        if s.layer == "TypedCodePointClassificationQiyas"
    ]
    assert typed_steps == []

    # Specifically, no BoundaryCodePoint candidate is produced anywhere
    # in the canonical chain (Z4 declassification still holds in Z5).
    assert "BoundaryCodePoint" not in _all_typed_candidate_types(reports)


# ---------------------------------------------------------------------------
# 6. Punctuation appears as a tokenizer marker / context evidence, never as
#    slot material.
# ---------------------------------------------------------------------------


def test_run_qiyas_punctuation_is_tokenizer_context_not_slot_material():
    reports = process_text("ب،َ")
    comma_report = reports[1]
    assert comma_report.char == "،"

    # Tokenizer surfaces the comma as a punctuation boundary marker.
    tm = comma_report.tokenizer_marker
    assert tm is not None
    assert tm["marker_type"] == "punctuation_boundary_marker"

    # The punctuation IS a qiyas-eligible codepoint (it sits inside the
    # Arabic Unicode block) and so it survives `UnicodeQiyas`. The
    # constitutional non-promotion is: it must not become slot material.
    assert comma_report.slot_step is None
    types_for_comma = _typed_candidate_types_for(reports, 1)
    assert "SlotCandidate" not in types_for_comma
    assert "SlotGeometry" not in types_for_comma

    # And no slot anywhere uses the comma as alignment — there are no
    # accepted SlotQiyas / ConditionedTypedSequenceQiyas steps at all.
    assert _accepted_slot_steps(reports) == []
    assert _accepted_steps_by_layer(reports, "ConditionedTypedSequenceQiyas") == []


# ---------------------------------------------------------------------------
# 7. Residual symbols are preserved as auditable tokenizer markers — no
#    character is silently dropped.
# ---------------------------------------------------------------------------


def test_run_qiyas_preserves_residual_markers():
    # "بَXتْ" — the Latin 'X' is outside ARABIC_RANGES and therefore is
    # a `residual_preservation_marker` at the tokenizer level. It does
    # not enter UnicodeQiyas as an accepted candidate, but it must not
    # be silently dropped from the audit.
    reports = process_text("بَXتْ")
    # One report per character — nothing dropped.
    assert len(reports) == 5

    x_report = reports[2]
    assert x_report.char == "X"
    tm = x_report.tokenizer_marker
    assert tm is not None
    assert tm["marker_type"] == "residual_preservation_marker"
    # And — critically — the residual sits between two tokenizer
    # segments, so the surrounding letter+haraka pairs each form their
    # own slot.
    accepted_slots = _accepted_slot_steps(reports)
    assert len(accepted_slots) == 2


# ---------------------------------------------------------------------------
# 8. The driver never emits SlotGeometry (re-asserted post-Z5 wiring).
# ---------------------------------------------------------------------------


def test_run_qiyas_no_slot_geometry():
    for sample in ("بَ", "بَتْ", "بَ تْ", "ب،َ", "بَXتْ", "اَكتب"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "SlotGeometry", (
                f"sample={sample!r}: a step produced SlotGeometry"
            )


# ---------------------------------------------------------------------------
# 9. The driver never emits FinalMeaning.
# ---------------------------------------------------------------------------


def test_run_qiyas_no_final_meaning():
    for sample in ("بَ", "بَتْ", "بَ تْ", "ب،َ", "بَXتْ"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "FinalMeaning"


# ---------------------------------------------------------------------------
# 10. The driver never emits HukmCandidate.
# ---------------------------------------------------------------------------


def test_run_qiyas_no_hukm_candidate():
    for sample in ("بَ", "بَتْ", "بَ تْ", "ب،َ", "بَXتْ"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "HukmCandidate"


# ---------------------------------------------------------------------------
# 11. The driver never emits RealityClaim.
# ---------------------------------------------------------------------------


def test_run_qiyas_no_reality_claim():
    for sample in ("بَ", "بَتْ", "بَ تْ", "ب،َ", "بَXتْ"):
        reports = process_text(sample)
        for s in _all_steps(reports):
            assert s.candidate_type != "RealityClaim"


# ---------------------------------------------------------------------------
# Z5 structural guards — the driver does not import `is_boundary` and does
# not carry a comment that calls `BoundaryCodePoint` canonical.
# ---------------------------------------------------------------------------


def test_run_qiyas_does_not_import_is_boundary():
    """`is_boundary` is the Z4-declassified legacy helper. Per Z5, the
    driver must not import it as a callable name — boundary detection
    is a tokenizer responsibility."""
    # Verify against the parsed import graph rather than the source text,
    # so docstring mentions of `is_boundary` (allowed: they explain why
    # the import is gone) do not trigger a false positive.
    bound_names = set(vars(run_qiyas).keys())
    assert "is_boundary" not in bound_names, (
        "run_qiyas.py still binds `is_boundary` at module scope; the "
        "Z5 wiring must source boundary detection from "
        "`SequenceContextTokenizer`."
    )


def test_run_qiyas_has_no_canonical_boundary_codepoint_comment():
    """The legacy comment "BoundaryCodePoint / PunctuationCodePoint /
    ResidualCodePoint: the contract defines no further canonical layer
    …" implied BoundaryCodePoint was a canonical typed-codepoint output.
    Z5 must update or remove that wording."""
    import inspect
    source = inspect.getsource(run_qiyas)
    assert (
        "BoundaryCodePoint / PunctuationCodePoint / ResidualCodePoint"
        not in source
    )
