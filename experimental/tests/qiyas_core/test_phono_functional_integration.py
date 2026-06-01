"""
Integration tests for the full PhonoFunctionalUnit layer stack.

Tests the complete flow:
AtomicUnitCandidate
  → CarrierFunctionCandidate
  → MarkFunctionCandidate
  → PhonoFunctionalUnitCandidate
  → SyllableReadinessCandidate

Validates constitutional boundaries are preserved at every layer.
"""
from qiyas_core.carrier_function_adapter import CarrierFunctionLayerAdapter
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.mark_function_adapter import MarkFunctionLayerAdapter
from qiyas_core.phono_functional_unit_adapter import PhonoFunctionalUnitLayerAdapter
from qiyas_core.syllable_readiness_adapter import SyllableReadinessLayerAdapter


def test_ba_fatha_full_stack():
    """Ba+Fatha flows through layers but is now blocked at syllable readiness awaiting order equilibrium."""
    kernel = QiyasKernel()

    # Layer 1: Carrier function
    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    carrier_result = carrier_adapter.process_carrier(0x0628)  # Ba
    assert len(carrier_result.accepted) == 1
    assert carrier_result.accepted[0].candidate_type == "CarrierFunctionCandidate"

    # Layer 2: Mark function
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    mark_result = mark_adapter.process_mark(0x064E)  # Fatha
    assert len(mark_result.accepted) == 1
    assert mark_result.accepted[0].candidate_type == "MarkFunctionCandidate"

    # Layer 3: Phono-functional unit
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    phono_result = phono_adapter.process_binding(0x0628, 0x064E)
    assert len(phono_result.accepted) == 1
    assert phono_result.accepted[0].candidate_type == "PhonoFunctionalUnitCandidate"

    # Layer 4: Syllable readiness (now requires order equilibrium evidence - PR #10)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x064E)
    # After PR #10, SyllableReadinessQiyas requires order equilibrium evidence
    assert len(syllable_result.blocked) == 1
    assert syllable_result.blocked[0].candidate_type == "SyllableReadinessCandidate"

    # Verify NO syllable candidate was produced
    assert syllable_result.blocked[0].candidate_type != "SyllableCandidate"


def test_ba_shadda_full_stack():
    """Ba+Shadda flows through layers but is now blocked at syllable readiness awaiting order equilibrium."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x0651)  # Shadda
    phono_result = phono_adapter.process_binding(0x0628, 0x0651)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x0651)

    # First three layers should accept
    assert len(carrier_result.accepted) == 1
    assert len(mark_result.accepted) == 1
    assert len(phono_result.accepted) == 1
    # After PR #10, syllable readiness is blocked awaiting order equilibrium
    assert len(syllable_result.blocked) == 1

    # Verify types at each layer
    assert carrier_result.accepted[0].candidate_type == "CarrierFunctionCandidate"
    assert mark_result.accepted[0].candidate_type == "MarkFunctionCandidate"
    assert phono_result.accepted[0].candidate_type == "PhonoFunctionalUnitCandidate"
    assert syllable_result.blocked[0].candidate_type == "SyllableReadinessCandidate"


def test_ba_sukun_initial_blocked_at_readiness():
    """Ba+Sukun at initial position should be blocked at syllable readiness layer."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    # First three layers should accept
    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x0652)  # Sukun
    phono_result = phono_adapter.process_binding(0x0628, 0x0652)

    assert len(carrier_result.accepted) == 1
    assert len(mark_result.accepted) == 1
    assert len(phono_result.accepted) == 1

    # Syllable readiness should block if initial
    syllable_result = syllable_adapter.process_validation(
        0x0628, 0x0652, is_initial_position=True
    )
    assert len(syllable_result.blocked) == 1
    assert len(syllable_result.accepted) == 0


def test_ba_additional_diacritic_blocked_at_readiness():
    """Ba+Additional diacritic should be blocked at syllable readiness."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    # First three layers should accept
    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x0653)  # Maddah
    phono_result = phono_adapter.process_binding(0x0628, 0x0653)

    assert len(carrier_result.accepted) == 1
    assert len(mark_result.accepted) == 1
    assert len(phono_result.accepted) == 1

    # Syllable readiness should block additional diacritic as vowel
    syllable_result = syllable_adapter.process_validation(0x0628, 0x0653)
    assert len(syllable_result.blocked) == 1
    assert len(syllable_result.accepted) == 0


def test_non_carrier_blocked_at_carrier_layer():
    """Non-carrier should be blocked at carrier function layer."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    carrier_result = carrier_adapter.process_carrier(0x0041)  # Latin A

    # Should be blocked at first layer
    assert len(carrier_result.blocked) == 1
    assert len(carrier_result.accepted) == 0
    assert carrier_result.blocked[0].status == CandidateStatus.BLOCKED


def test_all_layers_preserve_identity_trace_separation():
    """All layers must maintain identity/trace separation."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x064E)
    phono_result = phono_adapter.process_binding(0x0628, 0x064E)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x064E)

    # Check each layer
    for result in [carrier_result, mark_result, phono_result]:
        candidate = result.accepted[0]
        identity_set = set(candidate.identity_ids)
        trace_set = set(candidate.trace_ids)
        assert identity_set.isdisjoint(trace_set), \
            f"identity/trace overlap in {candidate.candidate_type}"

    # Check syllable layer (blocked after PR #10)
    candidate = syllable_result.blocked[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)
    assert identity_set.isdisjoint(trace_set), \
        f"identity/trace overlap in {candidate.candidate_type}"


def test_all_layers_preserve_rank_ceiling():
    """All layers must not exceed FORM rank."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x064E)
    phono_result = phono_adapter.process_binding(0x0628, 0x064E)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x064E)

    from qiyas_core.enums import EvidenceRank

    for result in [carrier_result, mark_result, phono_result]:
        candidate = result.accepted[0]
        assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE, \
            f"Rank ceiling violated in {candidate.candidate_type}"

    # Syllable layer is blocked after PR #10, rank is ZERO
    candidate = syllable_result.blocked[0]
    assert candidate.rank == EvidenceRank.NO_EVIDENCE


def test_all_layers_forbid_syllable_candidate():
    """All layers must forbid SyllableCandidate output."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x064E)
    phono_result = phono_adapter.process_binding(0x0628, 0x064E)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x064E)

    for result in [carrier_result, mark_result, phono_result]:
        candidate = result.accepted[0]
        assert "SyllableCandidate" not in candidate.output_flags, \
            f"SyllableCandidate produced by {candidate.candidate_type}"

    # Check blocked syllable layer
    candidate = syllable_result.blocked[0]
    assert "SyllableCandidate" not in candidate.output_flags, \
        f"SyllableCandidate produced by {candidate.candidate_type}"


def test_all_layers_forbid_pronunciation_candidate():
    """All layers must forbid PronunciationCandidate output."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x064E)
    phono_result = phono_adapter.process_binding(0x0628, 0x064E)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x064E)

    for result in [carrier_result, mark_result, phono_result]:
        candidate = result.accepted[0]
        assert "PronunciationCandidate" not in candidate.output_flags, \
            f"PronunciationCandidate produced by {candidate.candidate_type}"

    # Check blocked syllable layer
    candidate = syllable_result.blocked[0]
    assert "PronunciationCandidate" not in candidate.output_flags, \
        f"PronunciationCandidate produced by {candidate.candidate_type}"


def test_all_layers_forbid_dal_candidate():
    """All layers must forbid DalCandidate output."""
    kernel = QiyasKernel()

    carrier_adapter = CarrierFunctionLayerAdapter(kernel=kernel)
    mark_adapter = MarkFunctionLayerAdapter(kernel=kernel)
    phono_adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)
    syllable_adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    carrier_result = carrier_adapter.process_carrier(0x0628)
    mark_result = mark_adapter.process_mark(0x064E)
    phono_result = phono_adapter.process_binding(0x0628, 0x064E)
    syllable_result = syllable_adapter.process_validation(0x0628, 0x064E)

    for result in [carrier_result, mark_result, phono_result]:
        candidate = result.accepted[0]
        assert "DalCandidate" not in candidate.output_flags, \
            f"DalCandidate produced by {candidate.candidate_type}"

    # Check blocked syllable layer
    candidate = syllable_result.blocked[0]
    assert "DalCandidate" not in candidate.output_flags, \
        f"DalCandidate produced by {candidate.candidate_type}"
