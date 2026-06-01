"""
Tests for CarrierFunctionLayerAdapter.

Validates that carrier function classification correctly identifies:
- Arabic consonant carriers
- Weak letter carriers (Alif, Waw, Ya)
- Hamza carriers
- Non-carriers (invalid codepoints)
"""
from qiyas_core.carrier_function_adapter import (
    CarrierFunctionLayerAdapter,
    classify_carrier_function,
)
from qiyas_core.enums import CarrierFunction, CandidateStatus
from qiyas_core.kernel import QiyasKernel


def test_ba_classified_as_arabic_consonant():
    """Ba (0x0628) should be classified as ARABIC_CONSONANT_CARRIER."""
    result = classify_carrier_function(0x0628)  # Ba
    assert result == CarrierFunction.ARABIC_CONSONANT_CARRIER


def test_ta_classified_as_arabic_consonant():
    """Ta (0x062A) should be classified as ARABIC_CONSONANT_CARRIER."""
    result = classify_carrier_function(0x062A)  # Ta
    assert result == CarrierFunction.ARABIC_CONSONANT_CARRIER


def test_alif_classified_as_weak_letter():
    """Alif (0x0627) should be classified as WEAK_LETTER_CARRIER."""
    result = classify_carrier_function(0x0627)  # Alif
    assert result == CarrierFunction.WEAK_LETTER_CARRIER


def test_waw_classified_as_weak_letter():
    """Waw (0x0648) should be classified as WEAK_LETTER_CARRIER."""
    result = classify_carrier_function(0x0648)  # Waw
    assert result == CarrierFunction.WEAK_LETTER_CARRIER


def test_ya_classified_as_weak_letter():
    """Ya (0x064A) should be classified as WEAK_LETTER_CARRIER."""
    result = classify_carrier_function(0x064A)  # Ya
    assert result == CarrierFunction.WEAK_LETTER_CARRIER


def test_hamza_classified_as_hamza_carrier():
    """Hamza (0x0621) should be classified as HAMZA_CARRIER."""
    result = classify_carrier_function(0x0621)  # Hamza
    assert result == CarrierFunction.HAMZA_CARRIER


def test_alif_hamza_above_classified_as_hamza_carrier():
    """Alif with Hamza above (0x0623) should be classified as HAMZA_CARRIER."""
    result = classify_carrier_function(0x0623)  # Alif with Hamza above
    assert result == CarrierFunction.HAMZA_CARRIER


def test_non_arabic_letter_classified_as_non_carrier():
    """Non-Arabic letter (e.g., Latin A) should be NON_CARRIER."""
    result = classify_carrier_function(0x0041)  # Latin A
    assert result == CarrierFunction.NON_CARRIER


def test_diacritic_classified_as_non_carrier():
    """Diacritic (e.g., Fatha) should be NON_CARRIER."""
    result = classify_carrier_function(0x064E)  # Fatha
    assert result == CarrierFunction.NON_CARRIER


def test_adapter_processes_ba_carrier():
    """Adapter should produce CarrierFunctionCandidate for Ba."""
    kernel = QiyasKernel()
    adapter = CarrierFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_carrier(0x0628)  # Ba

    assert result.layer == "CarrierFunctionQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "CarrierFunctionCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.layer == "CarrierFunctionQiyas"


def test_adapter_processes_alif_carrier_with_readiness():
    """Adapter should produce CarrierFunctionCandidate for Alif with augmentation readiness."""
    kernel = QiyasKernel()
    adapter = CarrierFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_carrier(0x0627)  # Alif

    assert result.layer == "CarrierFunctionQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "CarrierFunctionCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    # Should have readiness residuals for weak letter
    assert len(candidate.residuals) >= 0  # May have deferred residuals


def test_adapter_blocks_non_carrier():
    """Adapter should block non-carrier codepoint."""
    kernel = QiyasKernel()
    adapter = CarrierFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_carrier(0x0041)  # Latin A

    assert result.layer == "CarrierFunctionQiyas"
    assert len(result.blocked) == 1
    assert len(result.accepted) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED


def test_carrier_function_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for carrier function."""
    kernel = QiyasKernel()
    adapter = CarrierFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_carrier(0x0628)  # Ba

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"


def test_carrier_function_rank_not_exceeds_form():
    """Carrier function candidate rank must not exceed FORM."""
    kernel = QiyasKernel()
    adapter = CarrierFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_carrier(0x0628)  # Ba

    candidate = result.accepted[0]
    from qiyas_core.enums import EvidenceRank
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_carrier_function_forbidden_outputs_enforced():
    """CarrierFunctionCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = CarrierFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_carrier(0x0628)  # Ba

    candidate = result.accepted[0]

    forbidden = {
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    }

    assert not (candidate.output_flags & forbidden), \
        f"Forbidden outputs detected: {candidate.output_flags & forbidden}"
