"""
Tests for HarakaRoleSpectrumLayerAdapter — Γ_haraka (Gamma-haraka) spectrum opener.

Constitutional contract: docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md

Required tests (from CLAUDE.md § 17 adapted for HarakaRoleSpectrum):
  1. test_fatha_produces_hypotheses_not_judgments
  2. test_identity_preservation
  3. test_rank_ceiling_is_analogical
  4. test_all_hypotheses_start_with_possible
  5. test_non_phonological_require_lambda
  6. test_all_hypotheses_declare_forbidden_outputs
  7. test_forbidden_output_enforcement
  8. test_different_haraka_types_produce_different_spectra
  9. test_optional_geometry_context
 10. test_blocking_conditions
"""

import uuid

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.haraka_role_spectrum import HarakaRoleSpectrum
from qiyas_core.haraka_role_spectrum_adapter import HarakaRoleSpectrumLayerAdapter
from qiyas_core.kernel import QiyasKernel
from qiyas_core.rules.haraka_role_spectrum_rules import FORBIDDEN_HARAKA_ROLE_SPECTRUM


def _kernel() -> QiyasKernel:
    return QiyasKernel()


def _adapter() -> HarakaRoleSpectrumLayerAdapter:
    return HarakaRoleSpectrumLayerAdapter(kernel=_kernel())


def _make_slot_candidate(
    haraka_name: str,
    haraka_codepoint: str,
    position_terminal: bool = False,
) -> Candidate:
    """
    Build a minimal SlotCandidate for spectrum generation tests.

    Args:
        haraka_name: e.g., "fatha", "damma", "kasra", "sukun"
        haraka_codepoint: e.g., "064e", "064f", "0650", "0652"
        position_terminal: whether the position is terminal
    """
    position_id = "identity:position:terminal" if position_terminal else "identity:position:P0"

    return Candidate(
        candidate_id=f"slot:{haraka_name}:{uuid.uuid4().hex[:8]}",
        candidate_type="SlotCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id="slot.composition",
        asl_id="اصل:slot_composition_domain",
        far_id=f"فرع:slot_{haraka_name}",
        identity_ids=(
            f"identity:codepoint:{haraka_codepoint}",
            f"identity:haraka:{haraka_name}",
            "identity:letter:baa",  # Example letter
            position_id,
        ),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(
            f"trace:haraka_function:{haraka_name}",
            "trace:carrier_binding:valid",
            "trace:alignment:evidenced",
        ),
        output_flags=frozenset(),
    )


def _make_geometry_context() -> Candidate:
    """Build a minimal SlotGeometryCandidate for optional context tests."""
    return Candidate(
        candidate_id=f"geometry:{uuid.uuid4().hex[:8]}",
        candidate_type="SlotGeometryCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SlotGeometryQiyas",
        source_rule_id="slot_geometry.build",
        asl_id="اصل:slot_geometry_domain",
        far_id="فرع:geometry",
        identity_ids=("identity:geometry:length_3",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(
            "trace:geometry_length:3",
            "trace:segment_transition:present",
        ),
        output_flags=frozenset(),
    )


# ---------------------------------------------------------------------------
# Test 1: FATHA produces hypotheses, not judgments
# ---------------------------------------------------------------------------


def test_fatha_produces_hypotheses_not_judgments():
    """
    Constitutional test: FATHA → multiple "possible_*" hypotheses.

    Must NOT produce:
    - Iʿrab (CaseEffect, Irab, FinalCaseJudgment)
    - Wazn (WeightCandidate, FinalPattern)
    - Hukm (HukmCandidate, RealityClaim, FinalMeaning)
    """
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Verify output type
    assert isinstance(spectrum, HarakaRoleSpectrum)

    # Verify hypotheses exist
    assert len(spectrum.hypotheses) > 0, "FATHA must produce hypotheses"

    # Verify all hypotheses start with "possible_"
    for hyp in spectrum.hypotheses:
        assert hyp.role_name.startswith("possible_"), (
            f"Hypothesis {hyp.role_name} does not start with 'possible_'"
        )

    # Verify spectrum does NOT claim final judgments
    # (this is structural - the spectrum object itself is not a judgment)
    assert spectrum.rank_ceiling == EvidenceRank.ANALOGICAL


def test_fatha_does_not_produce_irab():
    """Constitutional test: FATHA spectrum forbids I'rab outputs."""
    slot = _make_slot_candidate("fatha", "064e", position_terminal=True)
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # All hypotheses must forbid I'rab outputs
    for hyp in spectrum.hypotheses:
        forbidden = set(hyp.forbidden_outputs)
        assert "CaseEffect" in forbidden, f"{hyp.role_name} must forbid CaseEffect"
        assert "Irab" in forbidden, f"{hyp.role_name} must forbid Irab"
        assert "HukmCandidate" in forbidden, f"{hyp.role_name} must forbid HukmCandidate"


def test_fatha_does_not_produce_wazn():
    """Constitutional test: FATHA spectrum forbids Wazn outputs."""
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # All hypotheses must forbid Wazn outputs
    for hyp in spectrum.hypotheses:
        forbidden = set(hyp.forbidden_outputs)
        assert "WeightCandidate" in forbidden, f"{hyp.role_name} must forbid WeightCandidate"


def test_fatha_does_not_produce_hukm():
    """Constitutional test: FATHA spectrum forbids Hukm outputs."""
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # All hypotheses must forbid Hukm outputs
    for hyp in spectrum.hypotheses:
        forbidden = set(hyp.forbidden_outputs)
        assert "HukmCandidate" in forbidden
        assert "RealityClaim" in forbidden
        assert "FinalMeaning" in forbidden


# ---------------------------------------------------------------------------
# Test 2: Identity preservation
# ---------------------------------------------------------------------------


def test_identity_preservation():
    """
    Constitutional test (§ 3.5): source_identity must equal input identity_ids.
    """
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Source identity must be preserved
    assert spectrum.source_identity == slot.identity_ids, (
        f"Source identity not preserved.\n"
        f"Expected: {slot.identity_ids}\n"
        f"Got: {spectrum.source_identity}"
    )


def test_haraka_identity_subset_of_source():
    """
    Constitutional test (§ 3.5): haraka_identity ⊆ source_identity.
    """
    slot = _make_slot_candidate("damma", "064f")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    haraka_ids = set(spectrum.haraka_identity)
    source_ids = set(spectrum.source_identity)

    assert haraka_ids.issubset(source_ids), (
        f"Haraka identity not subset of source identity.\n"
        f"Haraka IDs: {haraka_ids}\n"
        f"Source IDs: {source_ids}\n"
        f"Difference: {haraka_ids - source_ids}"
    )


# ---------------------------------------------------------------------------
# Test 3: Rank ceiling is ANALOGICAL
# ---------------------------------------------------------------------------


def test_rank_ceiling_is_analogical():
    """
    Constitutional test (§ 2.2): rank_ceiling must be EvidenceRank.ANALOGICAL.

    Γ_haraka produces qiyas-based (analogical) hypotheses only.
    """
    slot = _make_slot_candidate("kasra", "0650")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    assert spectrum.rank_ceiling == EvidenceRank.ANALOGICAL, (
        f"Rank ceiling must be ANALOGICAL, got {spectrum.rank_ceiling}"
    )


# ---------------------------------------------------------------------------
# Test 4: All hypotheses start with "possible_"
# ---------------------------------------------------------------------------


def test_all_hypotheses_start_with_possible():
    """
    Constitutional test (§ 3.7): All hypotheses must have role_name starting
    with "possible_".
    """
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    assert len(spectrum.hypotheses) > 0, "Must have at least one hypothesis"

    for hyp in spectrum.hypotheses:
        assert hyp.role_name.startswith("possible_"), (
            f"Hypothesis role_name '{hyp.role_name}' does not start with 'possible_'"
        )


# ---------------------------------------------------------------------------
# Test 5: Non-phonological hypotheses require lambda context
# ---------------------------------------------------------------------------


def test_non_phonological_require_lambda():
    """
    Constitutional test (§ 3.8): Non-phonological hypotheses must declare
    "requires_lambda_context".
    """
    slot = _make_slot_candidate("fatha", "064e", position_terminal=True)
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    for hyp in spectrum.hypotheses:
        if hyp.role_genus in (
            "morphosyntactic",
            "morphological_pattern",
            "prosodic",
            "syllabic",
            "syntactic",
            "morphological",
        ):
            assert "requires_lambda_context" in hyp.required_context, (
                f"Non-phonological hypothesis {hyp.role_name} "
                f"(genus={hyp.role_genus}) must require lambda context"
            )


def test_phonological_does_not_require_lambda():
    """
    Constitutional test: Phonological hypotheses do NOT require lambda context.

    Phonological function is already established by HarakaFunctionCarrier.
    """
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Find phonological hypothesis
    phonological_hyps = [h for h in spectrum.hypotheses if h.role_genus == "phonological"]

    assert len(phonological_hyps) > 0, "Must have at least one phonological hypothesis"

    for hyp in phonological_hyps:
        assert "requires_lambda_context" not in hyp.required_context, (
            f"Phonological hypothesis {hyp.role_name} must NOT require lambda context"
        )


# ---------------------------------------------------------------------------
# Test 6: All hypotheses declare forbidden outputs
# ---------------------------------------------------------------------------


def test_all_hypotheses_declare_forbidden_outputs():
    """
    Constitutional test (§ 3.6): All hypotheses must declare forbidden_outputs.
    """
    slot = _make_slot_candidate("damma", "064f")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    for hyp in spectrum.hypotheses:
        assert len(hyp.forbidden_outputs) > 0, (
            f"Hypothesis {hyp.role_name} has no forbidden outputs"
        )

        # All hypotheses must forbid the base set
        forbidden = set(hyp.forbidden_outputs)
        assert "HukmCandidate" in forbidden
        assert "RealityClaim" in forbidden
        assert "FinalMeaning" in forbidden


# ---------------------------------------------------------------------------
# Test 7: Forbidden output enforcement
# ---------------------------------------------------------------------------


def test_forbidden_output_enforcement():
    """
    Constitutional test: Verify FORBIDDEN_HARAKA_ROLE_SPECTRUM constant.
    """
    forbidden = set(FORBIDDEN_HARAKA_ROLE_SPECTRUM)

    # Must forbid all final judgments
    assert "WeightCandidate" in forbidden
    assert "CaseEffect" in forbidden
    assert "Irab" in forbidden
    assert "ArudCandidate" in forbidden
    assert "FinalFunction" in forbidden
    assert "FinalMeaning" in forbidden
    assert "HukmCandidate" in forbidden
    assert "RealityClaim" in forbidden
    assert "SelectedRole" in forbidden
    assert "DeterminedFunction" in forbidden


# ---------------------------------------------------------------------------
# Test 8: Different haraka types produce different spectra
# ---------------------------------------------------------------------------


def test_fatha_spectrum():
    """Test FATHA produces opening hypotheses."""
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    role_names = [h.role_name for h in spectrum.hypotheses]

    # Must include phonological opening
    assert any("opening" in name for name in role_names), (
        f"FATHA must include opening hypothesis, got: {role_names}"
    )


def test_damma_spectrum():
    """Test DAMMA produces rounding hypotheses."""
    slot = _make_slot_candidate("damma", "064f")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    role_names = [h.role_name for h in spectrum.hypotheses]

    # Must include phonological rounding
    assert any("rounding" in name for name in role_names), (
        f"DAMMA must include rounding hypothesis, got: {role_names}"
    )


def test_kasra_spectrum():
    """Test KASRA produces fronting hypotheses."""
    slot = _make_slot_candidate("kasra", "0650")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    role_names = [h.role_name for h in spectrum.hypotheses]

    # Must include phonological fronting
    assert any("fronting" in name for name in role_names), (
        f"KASRA must include fronting hypothesis, got: {role_names}"
    )


def test_sukun_spectrum():
    """Test SUKUN produces closure hypotheses."""
    slot = _make_slot_candidate("sukun", "0652")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    role_names = [h.role_name for h in spectrum.hypotheses]

    # Must include phonological closure
    assert any("closure" in name or "boundary" in name for name in role_names), (
        f"SUKUN must include closure/boundary hypothesis, got: {role_names}"
    )


def test_terminal_position_generates_case_marker_hypothesis():
    """Test terminal position generates case marker hypothesis."""
    slot = _make_slot_candidate("fatha", "064e", position_terminal=True)
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Find case marker hypothesis
    case_hyps = [
        h for h in spectrum.hypotheses
        if h.role_genus == "morphosyntactic" and "case_marker" in h.role_name
    ]

    assert len(case_hyps) > 0, (
        "Terminal position should generate case marker hypothesis"
    )


def test_non_terminal_position_may_skip_case_marker():
    """Test non-terminal position may not generate case marker hypothesis."""
    slot = _make_slot_candidate("fatha", "064e", position_terminal=False)
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Non-terminal may or may not have case marker hypothesis
    # (implementation choice based on constitutional constraints)
    # This test just verifies it doesn't crash
    assert len(spectrum.hypotheses) > 0


# ---------------------------------------------------------------------------
# Test 9: Optional geometry context
# ---------------------------------------------------------------------------


def test_optional_geometry_context_accepted():
    """Test geometry context is accepted and traced."""
    slot = _make_slot_candidate("fatha", "064e")
    geometry = _make_geometry_context()

    spectrum = _adapter().open_haraka_role_spectrum(slot, geometry_context=geometry)

    # Geometry trace should be captured
    assert len(spectrum.geometry_context_trace) > 0, (
        "Geometry context should be traced"
    )


def test_without_geometry_context_empty_trace():
    """Test without geometry context, geometry_context_trace is empty."""
    slot = _make_slot_candidate("fatha", "064e")

    spectrum = _adapter().open_haraka_role_spectrum(slot, geometry_context=None)

    # Without geometry, trace should be empty
    assert spectrum.geometry_context_trace == (), (
        "Without geometry, geometry_context_trace should be empty"
    )


# ---------------------------------------------------------------------------
# Test 10: Blocking conditions
# ---------------------------------------------------------------------------


def test_missing_haraka_function_produces_residual():
    """Test missing haraka function produces deferred residual."""
    # Create slot without haraka identity
    slot = Candidate(
        candidate_id=f"slot:no_haraka:{uuid.uuid4().hex[:8]}",
        candidate_type="SlotCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id="slot.composition",
        asl_id="اصل:slot_composition_domain",
        far_id="فرع:slot_no_haraka",
        identity_ids=(
            "identity:letter:baa",
            "identity:position:P0",
        ),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=("trace:test",),
        output_flags=frozenset(),
    )

    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Should produce residual
    assert len(spectrum.residuals) > 0, (
        "Missing haraka function should produce residual"
    )

    # Check for defer residual
    defer_residuals = [
        r for r in spectrum.residuals
        if "defer" in r.residual_type or "missing_haraka" in r.residual_type
    ]
    assert len(defer_residuals) > 0, (
        "Should have defer residual for missing haraka function"
    )


def test_alignment_trace_captured():
    """Test alignment trace IDs are captured in spectrum."""
    slot = _make_slot_candidate("fatha", "064e")
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Alignment trace should be captured
    assert len(spectrum.alignment_trace_ids) > 0, (
        "Alignment trace should be captured"
    )


def test_position_identity_captured():
    """Test position identity is captured in spectrum."""
    slot = _make_slot_candidate("fatha", "064e", position_terminal=True)
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    # Position identity should be captured
    assert len(spectrum.position_identity) > 0, (
        "Position identity should be captured"
    )

    # Should contain position reference
    position_found = any(
        "position" in pid.lower()
        for pid in spectrum.position_identity
    )
    assert position_found, (
        f"Position identity should contain 'position', got: {spectrum.position_identity}"
    )


# ---------------------------------------------------------------------------
# Test 11: Spectrum contains multiple hypotheses
# ---------------------------------------------------------------------------


def test_spectrum_contains_multiple_hypotheses():
    """
    Test that Γ_haraka produces multiple hypotheses (spectrum opening).

    A spectrum should have at least:
    - 1 phonological hypothesis
    - 1+ non-phonological hypotheses (pattern, syllabic, prosodic, etc.)
    """
    slot = _make_slot_candidate("fatha", "064e", position_terminal=True)
    spectrum = _adapter().open_haraka_role_spectrum(slot)

    assert len(spectrum.hypotheses) >= 2, (
        f"Spectrum should have multiple hypotheses, got {len(spectrum.hypotheses)}"
    )

    # Count by genus
    genera = [h.role_genus for h in spectrum.hypotheses]
    unique_genera = set(genera)

    assert len(unique_genera) >= 2, (
        f"Spectrum should have multiple genera, got: {unique_genera}"
    )

    # Must have phonological
    assert "phonological" in unique_genera, (
        "Spectrum must have phonological hypothesis"
    )
