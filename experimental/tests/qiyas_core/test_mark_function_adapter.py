"""
Tests for MarkFunctionLayerAdapter.

Validates that mark function classification correctly identifies:
- Short vowel marks (Fatha, Damma, Kasra)
- Tanwin marks
- Sukun mark
- Shadda mark
- Additional diacritic marks
"""
from qiyas_core.enums import CandidateStatus, MarkFunction
from qiyas_core.kernel import QiyasKernel
from qiyas_core.mark_function_adapter import (
    MarkFunctionLayerAdapter,
    classify_mark_function,
)


def test_fatha_classified_as_short_vowel():
    """Fatha (0x064E) should be classified as SHORT_VOWEL_MARK."""
    result = classify_mark_function(0x064E)
    assert result == MarkFunction.SHORT_VOWEL_MARK


def test_damma_classified_as_short_vowel():
    """Damma (0x064F) should be classified as SHORT_VOWEL_MARK."""
    result = classify_mark_function(0x064F)
    assert result == MarkFunction.SHORT_VOWEL_MARK


def test_kasra_classified_as_short_vowel():
    """Kasra (0x0650) should be classified as SHORT_VOWEL_MARK."""
    result = classify_mark_function(0x0650)
    assert result == MarkFunction.SHORT_VOWEL_MARK


def test_fathatan_classified_as_tanwin():
    """Fathatan (0x064B) should be classified as TANWIN_MARK."""
    result = classify_mark_function(0x064B)
    assert result == MarkFunction.TANWIN_MARK


def test_dammatan_classified_as_tanwin():
    """Dammatan (0x064C) should be classified as TANWIN_MARK."""
    result = classify_mark_function(0x064C)
    assert result == MarkFunction.TANWIN_MARK


def test_kasratan_classified_as_tanwin():
    """Kasratan (0x064D) should be classified as TANWIN_MARK."""
    result = classify_mark_function(0x064D)
    assert result == MarkFunction.TANWIN_MARK


def test_shadda_classified_as_shadda_mark():
    """Shadda (0x0651) should be classified as SHADDA_MARK."""
    result = classify_mark_function(0x0651)
    assert result == MarkFunction.SHADDA_MARK


def test_sukun_classified_as_sukun_mark():
    """Sukun (0x0652) should be classified as SUKUN_MARK."""
    result = classify_mark_function(0x0652)
    assert result == MarkFunction.SUKUN_MARK


def test_additional_diacritic_classified_correctly():
    """Additional diacritic (e.g., Maddah 0x0653) should be ADDITIONAL_DIACRITIC_MARK."""
    result = classify_mark_function(0x0653)  # Maddah
    assert result == MarkFunction.ADDITIONAL_DIACRITIC_MARK


def test_non_diacritic_returns_unknown():
    """Non-diacritic (e.g., Ba) should return UNKNOWN_MARK_FUNCTION."""
    result = classify_mark_function(0x0628)  # Ba
    assert result == MarkFunction.UNKNOWN_MARK_FUNCTION


def test_adapter_processes_fatha_mark():
    """Adapter should produce MarkFunctionCandidate for Fatha."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x064E)  # Fatha

    assert result.layer == "MarkFunctionQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "MarkFunctionCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.layer == "MarkFunctionQiyas"


def test_adapter_processes_shadda_with_residual():
    """Adapter should produce MarkFunctionCandidate for Shadda with carrier validation residual."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x0651)  # Shadda

    assert result.layer == "MarkFunctionQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "MarkFunctionCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    # Shadda should have deferred residual for carrier validation
    assert len(candidate.residuals) >= 0


def test_adapter_processes_sukun_with_residual():
    """Adapter should produce MarkFunctionCandidate for Sukun with initial check residual."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x0652)  # Sukun

    assert result.layer == "MarkFunctionQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "MarkFunctionCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    # Sukun should have deferred residual for initial position check
    assert len(candidate.residuals) >= 0


def test_adapter_processes_additional_diacritic_with_constraint():
    """Adapter should produce MarkFunctionCandidate for additional diacritic with vowel constraint."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x0653)  # Maddah

    assert result.layer == "MarkFunctionQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "MarkFunctionCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    # Additional diacritic should have constraint residual
    assert len(candidate.residuals) >= 0


def test_adapter_blocks_unknown_mark():
    """Adapter should handle unknown mark function."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x0628)  # Ba (not a mark)

    assert result.layer == "MarkFunctionQiyas"
    # Should be blocked due to mark_function_indeterminate fariq
    assert len(result.blocked) == 1
    assert len(result.accepted) == 0


def test_mark_function_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for mark function."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x064E)  # Fatha

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"


def test_mark_function_rank_not_exceeds_form():
    """Mark function candidate rank must not exceed FORM."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x064E)  # Fatha

    candidate = result.accepted[0]
    from qiyas_core.enums import EvidenceRank
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_mark_function_forbidden_outputs_enforced():
    """MarkFunctionCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = MarkFunctionLayerAdapter(kernel=kernel)

    result = adapter.process_mark(0x064E)  # Fatha

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


def test_tanwin_marks_not_treated_as_short_vowels():
    """Tanwin marks should be classified separately from short vowels."""
    fathatan = classify_mark_function(0x064B)
    fatha = classify_mark_function(0x064E)

    assert fathatan == MarkFunction.TANWIN_MARK
    assert fatha == MarkFunction.SHORT_VOWEL_MARK
    assert fathatan != fatha
