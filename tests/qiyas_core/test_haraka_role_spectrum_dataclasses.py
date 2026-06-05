"""
Tests for Γ_haraka spectrum dataclasses (Phase 2).

Constitutional contract: docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md

Phase 2 scope (this test):
  ✓ HarakaRoleDomain enum works
  ✓ HarakaRoleHypothesis dataclass instantiation
  ✓ HarakaRoleSpectrum dataclass instantiation
  ✓ FORBIDDEN_HARAKA_ROLE_SPECTRUM constant is correct
  ✓ Basic constitutional constraints (frozen, types)

Phase 3 scope (future test):
  ✗ No adapter testing (not implemented)
  ✗ No rule testing (not implemented)
  ✗ No QiyasKernel integration testing (not implemented)
  ✗ No Lambda testing (not implemented)
"""

import pytest

from qiyas_core.enums import EvidenceRank
from qiyas_core.forbidden_outputs import (
    CONSTITUTIONAL_BASE,
    FORBIDDEN_HARAKA_ROLE_SPECTRUM,
)
from qiyas_core.haraka_role_spectrum import (
    HarakaRoleDomain,
    HarakaRoleHypothesis,
    HarakaRoleSpectrum,
)


# ---------------------------------------------------------------------------
# § 1. HarakaRoleDomain enum tests
# ---------------------------------------------------------------------------


def test_haraka_role_domain_enum_exists():
    """HarakaRoleDomain enum exists and has HARAKA_ROLE_SPECTRUM value."""
    assert hasattr(HarakaRoleDomain, "HARAKA_ROLE_SPECTRUM")
    assert HarakaRoleDomain.HARAKA_ROLE_SPECTRUM.value == "haraka_role_spectrum"


def test_haraka_role_domain_is_string():
    """HarakaRoleDomain enum values are strings."""
    assert isinstance(HarakaRoleDomain.HARAKA_ROLE_SPECTRUM, str)
    assert isinstance(HarakaRoleDomain.HARAKA_ROLE_SPECTRUM.value, str)


# ---------------------------------------------------------------------------
# § 2. HarakaRoleHypothesis dataclass tests
# ---------------------------------------------------------------------------


def test_haraka_role_hypothesis_instantiation():
    """HarakaRoleHypothesis can be instantiated with all required fields."""
    hypothesis = HarakaRoleHypothesis(
        role_name="possible_phonological_opening",
        role_genus="phonological",
        evidence_claims=("وصف:haraka_function:opening", "وصف:haraka_class:short_vowel"),
        required_context=(),
        invalidating_differences=(),
        forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
    )

    assert hypothesis.role_name == "possible_phonological_opening"
    assert hypothesis.role_genus == "phonological"
    assert len(hypothesis.evidence_claims) == 2
    assert len(hypothesis.forbidden_outputs) == 3


def test_haraka_role_hypothesis_is_frozen():
    """HarakaRoleHypothesis is frozen (immutable)."""
    hypothesis = HarakaRoleHypothesis(
        role_name="possible_test",
        role_genus="test",
        evidence_claims=(),
        required_context=(),
        invalidating_differences=(),
        forbidden_outputs=("HukmCandidate",),
    )

    with pytest.raises(AttributeError):
        hypothesis.role_name = "changed"


def test_haraka_role_hypothesis_role_name_validation():
    """Role name starting with 'possible_' is valid (constitutional requirement)."""
    # This is a design constraint, but we test instantiation works
    hypothesis = HarakaRoleHypothesis(
        role_name="possible_case_marker_candidate",
        role_genus="morphosyntactic",
        evidence_claims=("وصف:position_terminal",),
        required_context=("requires_lambda_context",),
        invalidating_differences=(),
        forbidden_outputs=("CaseEffect", "Irab", "HukmCandidate"),
    )

    assert hypothesis.role_name.startswith("possible_")


def test_haraka_role_hypothesis_non_phonological_requires_lambda():
    """Non-phonological hypotheses should declare lambda requirement (design check)."""
    # Morphosyntactic hypothesis with lambda requirement
    hypothesis = HarakaRoleHypothesis(
        role_name="possible_case_marker_candidate",
        role_genus="morphosyntactic",
        evidence_claims=("وصف:position_terminal",),
        required_context=("requires_lambda_context", "requires_composition_context"),
        invalidating_differences=(),
        forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
    )

    assert "requires_lambda_context" in hypothesis.required_context


def test_haraka_role_hypothesis_forbidden_outputs_include_base():
    """Hypothesis forbidden outputs should include constitutional base (design check)."""
    hypothesis = HarakaRoleHypothesis(
        role_name="possible_pattern_vowel",
        role_genus="morphological_pattern",
        evidence_claims=("وصف:pattern_position",),
        required_context=("requires_lambda_context",),
        invalidating_differences=(),
        forbidden_outputs=(
            "HukmCandidate",
            "RealityClaim",
            "FinalMeaning",
            "WeightCandidate",
            "FinalPattern",
        ),
    )

    # Check constitutional base is present
    assert "HukmCandidate" in hypothesis.forbidden_outputs
    assert "RealityClaim" in hypothesis.forbidden_outputs
    assert "FinalMeaning" in hypothesis.forbidden_outputs


# ---------------------------------------------------------------------------
# § 3. HarakaRoleSpectrum dataclass tests
# ---------------------------------------------------------------------------


def test_haraka_role_spectrum_instantiation():
    """HarakaRoleSpectrum can be instantiated with all required fields."""
    hypothesis = HarakaRoleHypothesis(
        role_name="possible_phonological_opening",
        role_genus="phonological",
        evidence_claims=("وصف:haraka_function:opening",),
        required_context=(),
        invalidating_differences=(),
        forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
    )

    spectrum = HarakaRoleSpectrum(
        source_identity=("identity:codepoint:U+064E", "identity:haraka:fatha"),
        haraka_identity=("identity:haraka:fatha",),
        position_identity=("identity:position:P0",),
        alignment_trace_ids=("trace:carrier_binding:valid",),
        geometry_context_trace=(),
        hypotheses=(hypothesis,),
        rank_ceiling=EvidenceRank.ANALOGICAL,
        residuals=(),
    )

    assert len(spectrum.source_identity) == 2
    assert len(spectrum.hypotheses) == 1
    assert spectrum.rank_ceiling == EvidenceRank.ANALOGICAL


def test_haraka_role_spectrum_is_frozen():
    """HarakaRoleSpectrum is frozen (immutable)."""
    spectrum = HarakaRoleSpectrum(
        source_identity=(),
        haraka_identity=(),
        position_identity=(),
        alignment_trace_ids=(),
        geometry_context_trace=(),
        hypotheses=(),
        rank_ceiling=EvidenceRank.ANALOGICAL,
        residuals=(),
    )

    with pytest.raises(AttributeError):
        spectrum.source_identity = ("changed",)


def test_haraka_role_spectrum_rank_ceiling_must_be_candidate():
    """Rank ceiling MUST be CANDIDATE (constitutional requirement)."""
    spectrum = HarakaRoleSpectrum(
        source_identity=(),
        haraka_identity=(),
        position_identity=(),
        alignment_trace_ids=(),
        geometry_context_trace=(),
        hypotheses=(),
        rank_ceiling=EvidenceRank.ANALOGICAL,
        residuals=(),
    )

    assert spectrum.rank_ceiling == EvidenceRank.ANALOGICAL


def test_haraka_role_spectrum_multiple_hypotheses():
    """HarakaRoleSpectrum can contain multiple hypotheses (the spectrum)."""
    phonological_hypothesis = HarakaRoleHypothesis(
        role_name="possible_phonological_opening",
        role_genus="phonological",
        evidence_claims=("وصف:haraka_function:opening",),
        required_context=(),
        invalidating_differences=(),
        forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
    )

    morphosyntactic_hypothesis = HarakaRoleHypothesis(
        role_name="possible_case_marker_candidate",
        role_genus="morphosyntactic",
        evidence_claims=("وصف:position_terminal",),
        required_context=("requires_lambda_context",),
        invalidating_differences=(),
        forbidden_outputs=("CaseEffect", "Irab", "HukmCandidate"),
    )

    spectrum = HarakaRoleSpectrum(
        source_identity=("identity:codepoint:U+064E",),
        haraka_identity=("identity:haraka:fatha",),
        position_identity=("identity:position:terminal",),
        alignment_trace_ids=("trace:carrier_binding:valid",),
        geometry_context_trace=(),
        hypotheses=(phonological_hypothesis, morphosyntactic_hypothesis),
        rank_ceiling=EvidenceRank.ANALOGICAL,
        residuals=(),
    )

    assert len(spectrum.hypotheses) == 2
    assert spectrum.hypotheses[0].role_genus == "phonological"
    assert spectrum.hypotheses[1].role_genus == "morphosyntactic"


def test_haraka_role_spectrum_geometry_context_optional():
    """Geometry context trace is optional (empty tuple when not provided)."""
    spectrum_without_geometry = HarakaRoleSpectrum(
        source_identity=(),
        haraka_identity=(),
        position_identity=(),
        alignment_trace_ids=(),
        geometry_context_trace=(),  # Empty when SlotGeometry not provided
        hypotheses=(),
        rank_ceiling=EvidenceRank.ANALOGICAL,
        residuals=(),
    )

    spectrum_with_geometry = HarakaRoleSpectrum(
        source_identity=(),
        haraka_identity=(),
        position_identity=(),
        alignment_trace_ids=(),
        geometry_context_trace=(
            "trace:geometry_length:2",
            "trace:position_in_geometry:terminal",
        ),
        hypotheses=(),
        rank_ceiling=EvidenceRank.ANALOGICAL,
        residuals=(),
    )

    assert len(spectrum_without_geometry.geometry_context_trace) == 0
    assert len(spectrum_with_geometry.geometry_context_trace) == 2


# ---------------------------------------------------------------------------
# § 4. FORBIDDEN_HARAKA_ROLE_SPECTRUM constant tests
# ---------------------------------------------------------------------------


def test_forbidden_haraka_role_spectrum_exists():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM constant exists."""
    assert FORBIDDEN_HARAKA_ROLE_SPECTRUM is not None
    assert isinstance(FORBIDDEN_HARAKA_ROLE_SPECTRUM, tuple)


def test_forbidden_haraka_role_spectrum_includes_constitutional_base():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM includes constitutional base."""
    for base_item in CONSTITUTIONAL_BASE:
        assert base_item in FORBIDDEN_HARAKA_ROLE_SPECTRUM


def test_forbidden_haraka_role_spectrum_includes_wazn():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM forbids Wazn (weight/pattern) outputs."""
    assert "WeightCandidate" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "RootCandidate" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "PatternCandidate" in FORBIDDEN_HARAKA_ROLE_SPECTRUM


def test_forbidden_haraka_role_spectrum_includes_irab():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM forbids I'rab (case/composition) outputs."""
    assert "CaseEffect" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "Irab" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "CaseJudgment" in FORBIDDEN_HARAKA_ROLE_SPECTRUM


def test_forbidden_haraka_role_spectrum_includes_arud():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM forbids 'Arud (prosody) outputs."""
    assert "ArudCandidate" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "MeterJudgment" in FORBIDDEN_HARAKA_ROLE_SPECTRUM


def test_forbidden_haraka_role_spectrum_includes_lambda_outputs():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM forbids Lambda (selection) outputs."""
    assert "SelectedRole" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "FinalFunction" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "DeterminedRole" in FORBIDDEN_HARAKA_ROLE_SPECTRUM


def test_forbidden_haraka_role_spectrum_includes_syllable():
    """FORBIDDEN_HARAKA_ROLE_SPECTRUM forbids Syllable outputs (Lambda output)."""
    assert "SyllableCandidate" in FORBIDDEN_HARAKA_ROLE_SPECTRUM
    assert "SyllableConstituent" in FORBIDDEN_HARAKA_ROLE_SPECTRUM


# ---------------------------------------------------------------------------
# § 5. Constitutional principle tests (Γ ≠ Λ)
# ---------------------------------------------------------------------------


def test_gamma_not_lambda_principle_in_forbidden_outputs():
    """Γ ≠ Λ principle: Gamma opens spectrum, Lambda selects roles."""
    # Gamma (spectrum opener) MUST NOT produce Lambda (selector) outputs
    lambda_outputs = {"SelectedRole", "FinalFunction", "DeterminedRole"}

    for lambda_output in lambda_outputs:
        assert (
            lambda_output in FORBIDDEN_HARAKA_ROLE_SPECTRUM
        ), f"Γ must not produce Λ output: {lambda_output}"


def test_all_hypotheses_must_be_possible():
    """All role names in hypotheses MUST start with 'possible_' (design check)."""
    # Example spectrum with multiple hypotheses
    hypotheses = (
        HarakaRoleHypothesis(
            role_name="possible_phonological_opening",
            role_genus="phonological",
            evidence_claims=(),
            required_context=(),
            invalidating_differences=(),
            forbidden_outputs=("HukmCandidate",),
        ),
        HarakaRoleHypothesis(
            role_name="possible_case_marker_candidate",
            role_genus="morphosyntactic",
            evidence_claims=(),
            required_context=("requires_lambda_context",),
            invalidating_differences=(),
            forbidden_outputs=("CaseEffect", "Irab"),
        ),
    )

    for hypothesis in hypotheses:
        assert hypothesis.role_name.startswith(
            "possible_"
        ), f"Hypothesis role_name must start with 'possible_': {hypothesis.role_name}"
