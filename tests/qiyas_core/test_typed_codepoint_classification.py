"""
Comprehensive tests for TypedCodePoint classification layer.

This layer classifies UnicodeCandidate into typed codepoints:
- LetterCodePoint
- HarakaCodePoint
- BoundaryCodePoint
- PunctuationCodePoint
- ResidualCodePoint

Constitutional requirements:
1. Classification is disjoint (exactly one type per codepoint)
2. Unicode identity is preserved through classification
3. Classification uses QiyasKernel.apply()
4. Classification returns CandidateSet
5. Classification has evidence, rank, residuals, trace
6. Classification forbids higher-level outputs (root, weight, meaning, hukm, etc.)
7. Type-specific wasf and illah are proven in evidence (PR #23)
8. invalidating_differences enforce disjoint union (PR #23)
"""

from unittest.mock import MagicMock, patch

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.rules.typed_codepoint_rules import TYPED_CODEPOINT_CLASSIFICATION
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter


def test_classify_baa_returns_letter_codepoint():
    """Test that Arabic letter Ba (ب) classifies as LetterCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)  # ب

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "LetterCodePoint"
    assert candidate.rank == EvidenceRank.FORM


def test_classify_fatha_returns_haraka_codepoint():
    """Test that Fatha (َ) classifies as HarakaCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x064E)  # َ

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCodePoint"
    assert candidate.rank == EvidenceRank.FORM


def test_classify_space_returns_boundary_codepoint():
    """Test that space classifies as BoundaryCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0020)  # Space

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "BoundaryCodePoint"
    assert candidate.rank == EvidenceRank.FORM


def test_classify_arabic_comma_returns_punctuation_codepoint():
    """Test that Arabic comma (،) classifies as PunctuationCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x060C)  # ،

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "PunctuationCodePoint"
    assert candidate.rank == EvidenceRank.FORM


def test_classify_unknown_returns_residual_codepoint():
    """Test that unknown/unclassified codepoint becomes ResidualCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0058)  # Latin X

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "ResidualCodePoint"
    assert candidate.rank == EvidenceRank.FORM


def test_classification_preserves_unicode_identity():
    """Test that classification preserves the original unicode identity."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)  # ب

    candidate = result.accepted[0]
    assert "identity:codepoint:0628" in candidate.identity_ids


def test_letter_codepoint_is_not_haraka():
    """Test disjoint classification: letter is not haraka."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)  # ب

    candidate = result.accepted[0]
    assert candidate.candidate_type == "LetterCodePoint"
    assert candidate.candidate_type != "HarakaCodePoint"
    assert candidate.candidate_type != "BoundaryCodePoint"
    assert candidate.candidate_type != "PunctuationCodePoint"
    assert candidate.candidate_type != "ResidualCodePoint"


def test_haraka_codepoint_is_not_letter():
    """Test disjoint classification: haraka is not letter."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x064E)  # َ

    candidate = result.accepted[0]
    assert candidate.candidate_type == "HarakaCodePoint"
    assert candidate.candidate_type != "LetterCodePoint"
    assert candidate.candidate_type != "BoundaryCodePoint"
    assert candidate.candidate_type != "PunctuationCodePoint"
    assert candidate.candidate_type != "ResidualCodePoint"


def test_boundary_codepoint_is_not_punctuation():
    """Test disjoint classification: boundary is not punctuation."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0020)  # Space

    candidate = result.accepted[0]
    assert candidate.candidate_type == "BoundaryCodePoint"
    assert candidate.candidate_type != "LetterCodePoint"
    assert candidate.candidate_type != "HarakaCodePoint"
    assert candidate.candidate_type != "PunctuationCodePoint"
    assert candidate.candidate_type != "ResidualCodePoint"


def test_classification_returns_candidate_set():
    """Test that classification returns CandidateSet, not raw object."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)

    from qiyas_core.candidate import CandidateSet
    assert isinstance(result, CandidateSet)


def test_classification_has_evidence():
    """Test that classified candidate has evidence."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)

    candidate = result.accepted[0]
    # Candidate has evidence trace through its creation
    assert len(candidate.trace_ids) > 0


def test_classification_has_rank():
    """Test that classified candidate has rank."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)

    candidate = result.accepted[0]
    assert candidate.rank == EvidenceRank.FORM


def test_classification_has_residuals():
    """Test that classified candidate has residuals field (may be empty)."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)

    candidate = result.accepted[0]
    assert hasattr(candidate, 'residuals')
    assert isinstance(candidate.residuals, tuple)


def test_classification_has_trace():
    """Test that classified candidate has trace IDs."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)

    candidate = result.accepted[0]
    assert len(candidate.trace_ids) > 0


def test_typed_codepoint_rule_forbids_atomic_unit():
    """Test that TypedCodePoint rule forbids AtomicUnitCandidate output."""
    assert "AtomicUnitCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_syllable():
    """Test that TypedCodePoint rule forbids SyllableCandidate output."""
    assert "SyllableCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_root():
    """Test that TypedCodePoint rule forbids RootCandidate output."""
    assert "RootCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_weight():
    """Test that TypedCodePoint rule forbids WeightCandidate output."""
    assert "WeightCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_meaning():
    """Test that TypedCodePoint rule forbids MeaningCandidate output."""
    assert "MeaningCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_dalalah():
    """Test that TypedCodePoint rule forbids DalalahCandidate output."""
    assert "DalalahCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_ifadah():
    """Test that TypedCodePoint rule forbids IfadahCandidate output."""
    assert "IfadahCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_hukm():
    """Test that TypedCodePoint rule forbids HukmCandidate output."""
    assert "HukmCandidate" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_reality_claim():
    """Test that TypedCodePoint rule forbids RealityClaim output."""
    assert "RealityClaim" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_typed_codepoint_rule_forbids_final_meaning():
    """Test that TypedCodePoint rule forbids FinalMeaning output."""
    assert "FinalMeaning" in TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs


def test_classification_multiple_letters():
    """Test classification of multiple Arabic letters."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())

    # Test a few different letters
    letters = [0x0621, 0x0628, 0x062A, 0x062B, 0x062C, 0x064A]  # ء ب ت ث ج ي
    for codepoint in letters:
        result = adapter.classify_codepoint(codepoint)
        assert len(result.accepted) == 1
        assert result.accepted[0].candidate_type == "LetterCodePoint"


def test_classification_multiple_harakat():
    """Test classification of multiple harakat."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())

    # Test various harakat
    harakat = [0x064B, 0x064C, 0x064D, 0x064E, 0x064F, 0x0650, 0x0651, 0x0652]
    for codepoint in harakat:
        result = adapter.classify_codepoint(codepoint)
        assert len(result.accepted) == 1
        assert result.accepted[0].candidate_type == "HarakaCodePoint"


def test_classification_identity_preservation_across_types():
    """Test that identity is preserved for all classified types."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())

    test_cases = [
        (0x0628, "LetterCodePoint"),      # ب
        (0x064E, "HarakaCodePoint"),      # َ
        (0x0020, "BoundaryCodePoint"),    # Space
        (0x060C, "PunctuationCodePoint"), # ،
        (0x0058, "ResidualCodePoint"),    # X
    ]

    for codepoint, expected_type in test_cases:
        result = adapter.classify_codepoint(codepoint)
        candidate = result.accepted[0]
        assert candidate.candidate_type == expected_type
        assert f"identity:codepoint:{codepoint:04x}" in candidate.identity_ids


def test_classification_uses_qiyas_kernel():
    """Test that classification goes through QiyasKernel.apply()."""
    # This is verified by the fact that the adapter calls kernel.apply()
    # and returns a CandidateSet with proper structure
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)

    # If it went through kernel, it will have proper CandidateSet structure
    assert hasattr(result, 'accepted')
    assert hasattr(result, 'deferred')
    assert hasattr(result, 'blocked')
    assert len(result.accepted) == 1


def test_letter_codepoint_has_same_codepoint_identity():
    """Test that LetterCodePoint preserves exact unicode identity."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    codepoint = 0x0628  # ب
    result = adapter.classify_codepoint(codepoint)

    candidate = result.accepted[0]
    expected_identity = f"identity:codepoint:{codepoint:04x}"
    assert expected_identity in candidate.identity_ids


def test_haraka_codepoint_has_same_codepoint_identity():
    """Test that HarakaCodePoint preserves exact unicode identity."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    codepoint = 0x064E  # َ
    result = adapter.classify_codepoint(codepoint)

    candidate = result.accepted[0]
    expected_identity = f"identity:codepoint:{codepoint:04x}"
    assert expected_identity in candidate.identity_ids


# PR #23: Tests for hardened algebraic proof


def test_letter_classification_proves_type_specific_wasf():
    """Test that LetterCodePoint classification proves is_arabic_letter wasf."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    codepoint = 0x0628  # ب

    # Get the request that would be sent to kernel
    unicode_candidate = Candidate(
        candidate_id=f"unicode:{codepoint:04x}",
        candidate_type="UnicodeCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="UnicodeQiyas",
        source_rule_id="unicode.arabic.membership",
        asl_id="asl:arabic_unicode_block",
        far_id=f"far:{codepoint:04x}",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        rank=EvidenceRank.FORM,
        residuals=(),
        trace_ids=(f"test:unicode:{codepoint:04x}",),
        output_flags=frozenset(),
    )

    request = adapter.build_request_for_classification(unicode_candidate)

    # Check that evidence proves type-specific wasf
    evidence_proves = set()
    for evidence in request.evidence.items:
        evidence_proves.update(evidence.proves)

    assert "wasf:is_arabic_letter:evidenced" in evidence_proves


def test_haraka_classification_proves_type_specific_illah():
    """Test that HarakaCodePoint classification proves belongs_to_haraka_class illah."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    codepoint = 0x064E  # َ

    unicode_candidate = Candidate(
        candidate_id=f"unicode:{codepoint:04x}",
        candidate_type="UnicodeCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="UnicodeQiyas",
        source_rule_id="unicode.arabic.membership",
        asl_id="asl:arabic_unicode_block",
        far_id=f"far:{codepoint:04x}",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        rank=EvidenceRank.FORM,
        residuals=(),
        trace_ids=(f"test:unicode:{codepoint:04x}",),
        output_flags=frozenset(),
    )

    request = adapter.build_request_for_classification(unicode_candidate)

    evidence_proves = set()
    for evidence in request.evidence.items:
        evidence_proves.update(evidence.proves)

    assert "illah:belongs_to_haraka_class:verified" in evidence_proves


def test_boundary_classification_proves_type_specific_wasf_and_illah():
    """Test that BoundaryCodePoint proves both specific wasf and illah."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    codepoint = 0x0020  # Space

    unicode_candidate = Candidate(
        candidate_id=f"unicode:{codepoint:04x}",
        candidate_type="UnicodeCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="UnicodeQiyas",
        source_rule_id="unicode.arabic.membership",
        asl_id="asl:arabic_unicode_block",
        far_id=f"far:{codepoint:04x}",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        rank=EvidenceRank.FORM,
        residuals=(),
        trace_ids=(f"test:unicode:{codepoint:04x}",),
        output_flags=frozenset(),
    )

    request = adapter.build_request_for_classification(unicode_candidate)

    evidence_proves = set()
    for evidence in request.evidence.items:
        evidence_proves.update(evidence.proves)

    assert "wasf:is_whitespace_boundary:evidenced" in evidence_proves
    assert "illah:belongs_to_boundary_class:verified" in evidence_proves


def test_classification_uses_kernel_apply_verifiably():
    """Test that classification actually calls kernel.apply() (not just returning structure)."""
    mock_kernel = MagicMock(spec=QiyasKernel)
    # Make mock return a realistic CandidateSet
    from qiyas_core.candidate import CandidateSet
    mock_kernel.apply.return_value = CandidateSet(
        set_id="mock_set",
        layer="TypedCodePointClassificationQiyas",
        candidates=(),
        residuals=(),
        trace_ids=()
    )

    adapter = TypedCodePointLayerAdapter(kernel=mock_kernel)
    adapter.classify_codepoint(0x0628)  # ب

    # Verify kernel.apply was called exactly once
    assert mock_kernel.apply.call_count == 1


def test_typed_codepoint_rule_has_disjoint_union_invalidations():
    """Test that rule defines invalidating_differences for disjoint union proof."""
    assert len(TYPED_CODEPOINT_CLASSIFICATION.invalidating_differences) > 0
    assert "multiple_classes_claimed" in TYPED_CODEPOINT_CLASSIFICATION.invalidating_differences
    assert "letter_haraka_overlap" in TYPED_CODEPOINT_CLASSIFICATION.invalidating_differences


def test_letter_candidate_has_no_forbidden_output_flags():
    """Test that LetterCodePoint candidate has no forbidden output_flags."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)  # ب

    candidate = result.accepted[0]
    # output_flags should be frozenset (empty or with allowed flags only)
    assert isinstance(candidate.output_flags, frozenset)
    # No forbidden flag names should appear
    forbidden_types = {
        "AtomicUnitCandidate", "SyllableCandidate", "RootCandidate",
        "WeightCandidate", "MeaningCandidate", "HukmCandidate",
        "RealityClaim", "FinalMeaning"
    }
    # Convert flags to strings if they exist and check
    flag_strings = {str(flag) for flag in candidate.output_flags}
    assert not any(forbidden in flag for flag in flag_strings for forbidden in forbidden_types)


def test_all_classification_types_prove_specific_evidence():
    """Test that all classification types (Letter/Haraka/Boundary/Punctuation/Residual) prove their specific evidence."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())

    test_cases = [
        (0x0628, "is_arabic_letter", "belongs_to_letter_class"),      # ب
        (0x064E, "is_arabic_haraka", "belongs_to_haraka_class"),      # َ
        (0x0020, "is_whitespace_boundary", "belongs_to_boundary_class"),  # Space
        (0x060C, "is_arabic_punctuation", "belongs_to_punctuation_class"),  # ،
        (0x0058, "is_unclassified_codepoint", "belongs_to_residual_class"),  # X
    ]

    for codepoint, expected_wasf, expected_illah in test_cases:
        unicode_candidate = Candidate(
            candidate_id=f"unicode:{codepoint:04x}",
            candidate_type="UnicodeCandidate",
            status=CandidateStatus.ACCEPTED,
            layer="UnicodeQiyas",
            source_rule_id="unicode.arabic.membership",
            asl_id="asl:arabic_unicode_block",
            far_id=f"far:{codepoint:04x}",
            identity_ids=(f"identity:codepoint:{codepoint:04x}",),
            rank=EvidenceRank.FORM,
            residuals=(),
            trace_ids=(f"test:unicode:{codepoint:04x}",),
            output_flags=frozenset(),
        )

        request = adapter.build_request_for_classification(unicode_candidate)

        evidence_proves = set()
        for evidence in request.evidence.items:
            evidence_proves.update(evidence.proves)

        assert f"wasf:{expected_wasf}:evidenced" in evidence_proves, \
            f"Codepoint {codepoint:04x} should prove wasf:{expected_wasf}"
        assert f"illah:{expected_illah}:verified" in evidence_proves, \
            f"Codepoint {codepoint:04x} should prove illah:{expected_illah}"

