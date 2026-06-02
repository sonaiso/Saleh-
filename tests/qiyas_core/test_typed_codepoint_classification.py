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
from qiyas_core.rules.typed_codepoint_rules import (
    LETTER_CODEPOINT_CLASSIFICATION,
    HARAKA_CODEPOINT_CLASSIFICATION,
    BOUNDARY_CODEPOINT_CLASSIFICATION,
    PUNCTUATION_CODEPOINT_CLASSIFICATION,
    RESIDUAL_CODEPOINT_CLASSIFICATION,
)
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter


def test_classify_baa_returns_letter_codepoint():
    """Test that Arabic letter Ba (ب) classifies as LetterCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0628)  # ب

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "LetterCodePoint"
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_classify_fatha_returns_haraka_codepoint():
    """Test that Fatha (َ) classifies as HarakaCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x064E)  # َ

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCodePoint"
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_classify_space_returns_boundary_codepoint():
    """Test that space classifies as BoundaryCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0020)  # Space

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "BoundaryCodePoint"
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_classify_arabic_comma_returns_punctuation_codepoint():
    """Test that Arabic comma (،) classifies as PunctuationCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x060C)  # ،

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "PunctuationCodePoint"
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_classify_unknown_returns_residual_codepoint():
    """Test that unknown/unclassified codepoint becomes ResidualCodePoint."""
    adapter = TypedCodePointLayerAdapter(kernel=QiyasKernel())
    result = adapter.classify_codepoint(0x0058)  # Latin X

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "ResidualCodePoint"
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


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
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


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
    """Test that TypedCodePoint rules forbid AtomicUnitCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "AtomicUnitCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_syllable():
    """Test that TypedCodePoint rules forbid SyllableCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "SyllableCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_root():
    """Test that TypedCodePoint rules forbid RootCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "RootCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_weight():
    """Test that TypedCodePoint rules forbid WeightCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "WeightCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_meaning():
    """Test that TypedCodePoint rules forbid MeaningCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "MeaningCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_dalalah():
    """Test that TypedCodePoint rules forbid DalalahCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "DalalahCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_ifadah():
    """Test that TypedCodePoint rules forbid IfadahCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "IfadahCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_hukm():
    """Test that TypedCodePoint rules forbid HukmCandidate output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "HukmCandidate" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_reality_claim():
    """Test that TypedCodePoint rules forbid RealityClaim output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "RealityClaim" in rule.forbidden_outputs


def test_typed_codepoint_rule_forbids_final_meaning():
    """Test that TypedCodePoint rules forbid FinalMeaning output."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert "FinalMeaning" in rule.forbidden_outputs


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
        asl_id="اصل:arabic_unicode_block",
        far_id=f"فرع:{codepoint:04x}",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(f"test:unicode:{codepoint:04x}",),
        output_flags=frozenset(),
    )

    request = adapter.build_request_for_classification(unicode_candidate)

    # Check that evidence proves type-specific wasf
    evidence_proves = set()
    for evidence in request.evidence.items:
        evidence_proves.update(evidence.proves)

    assert "وصف:is_arabic_letter:evidenced" in evidence_proves


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
        asl_id="اصل:arabic_unicode_block",
        far_id=f"فرع:{codepoint:04x}",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(f"test:unicode:{codepoint:04x}",),
        output_flags=frozenset(),
    )

    request = adapter.build_request_for_classification(unicode_candidate)

    evidence_proves = set()
    for evidence in request.evidence.items:
        evidence_proves.update(evidence.proves)

    assert "علة:belongs_to_haraka_class:verified" in evidence_proves


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
        asl_id="اصل:arabic_unicode_block",
        far_id=f"فرع:{codepoint:04x}",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(f"test:unicode:{codepoint:04x}",),
        output_flags=frozenset(),
    )

    request = adapter.build_request_for_classification(unicode_candidate)

    evidence_proves = set()
    for evidence in request.evidence.items:
        evidence_proves.update(evidence.proves)

    assert "وصف:is_whitespace_boundary:evidenced" in evidence_proves
    assert "علة:belongs_to_boundary_class:verified" in evidence_proves


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
    """Test that rules define invalidating_differences for disjoint union proof."""
    for rule in [LETTER_CODEPOINT_CLASSIFICATION, HARAKA_CODEPOINT_CLASSIFICATION,
                 BOUNDARY_CODEPOINT_CLASSIFICATION, PUNCTUATION_CODEPOINT_CLASSIFICATION,
                 RESIDUAL_CODEPOINT_CLASSIFICATION]:
        assert len(rule.invalidating_differences) > 0
        assert "multiple_classes_claimed" in rule.invalidating_differences

    # Letter and Haraka specifically check for overlap
    assert "letter_haraka_overlap" in LETTER_CODEPOINT_CLASSIFICATION.invalidating_differences
    assert "letter_haraka_overlap" in HARAKA_CODEPOINT_CLASSIFICATION.invalidating_differences


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
            asl_id="اصل:arabic_unicode_block",
            far_id=f"فرع:{codepoint:04x}",
            identity_ids=(f"identity:codepoint:{codepoint:04x}",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
            residuals=(),
            trace_ids=(f"test:unicode:{codepoint:04x}",),
            output_flags=frozenset(),
        )

        request = adapter.build_request_for_classification(unicode_candidate)

        evidence_proves = set()
        for evidence in request.evidence.items:
            evidence_proves.update(evidence.proves)

        assert f"وصف:{expected_wasf}:evidenced" in evidence_proves, \
            f"Codepoint {codepoint:04x} should prove wasf:{expected_wasf}"
        assert f"علة:{expected_illah}:verified" in evidence_proves, \
            f"Codepoint {codepoint:04x} should prove illah:{expected_illah}"


# PR #24: Failure tests - rule enforcement


def test_letter_rule_requires_is_arabic_letter_wasf():
    """Test that LETTER_CODEPOINT_CLASSIFICATION requires is_arabic_letter wasf."""
    assert "is_arabic_letter" in LETTER_CODEPOINT_CLASSIFICATION.required_effective_wasf


def test_letter_rule_requires_belongs_to_letter_class_illah():
    """Test that LETTER_CODEPOINT_CLASSIFICATION requires belongs_to_letter_class illah."""
    assert "belongs_to_letter_class" in LETTER_CODEPOINT_CLASSIFICATION.required_illah


def test_haraka_rule_requires_is_arabic_haraka_wasf():
    """Test that HARAKA_CODEPOINT_CLASSIFICATION requires is_arabic_haraka wasf."""
    assert "is_arabic_haraka" in HARAKA_CODEPOINT_CLASSIFICATION.required_effective_wasf


def test_haraka_rule_requires_belongs_to_haraka_class_illah():
    """Test that HARAKA_CODEPOINT_CLASSIFICATION requires belongs_to_haraka_class illah."""
    assert "belongs_to_haraka_class" in HARAKA_CODEPOINT_CLASSIFICATION.required_illah


def test_boundary_rule_requires_is_whitespace_boundary_wasf():
    """Test that BOUNDARY_CODEPOINT_CLASSIFICATION requires is_whitespace_boundary wasf."""
    assert "is_whitespace_boundary" in BOUNDARY_CODEPOINT_CLASSIFICATION.required_effective_wasf


def test_boundary_rule_requires_belongs_to_boundary_class_illah():
    """Test that BOUNDARY_CODEPOINT_CLASSIFICATION requires belongs_to_boundary_class illah."""
    assert "belongs_to_boundary_class" in BOUNDARY_CODEPOINT_CLASSIFICATION.required_illah


def test_punctuation_rule_requires_is_arabic_punctuation_wasf():
    """Test that PUNCTUATION_CODEPOINT_CLASSIFICATION requires is_arabic_punctuation wasf."""
    assert "is_arabic_punctuation" in PUNCTUATION_CODEPOINT_CLASSIFICATION.required_effective_wasf


def test_punctuation_rule_requires_belongs_to_punctuation_class_illah():
    """Test that PUNCTUATION_CODEPOINT_CLASSIFICATION requires belongs_to_punctuation_class illah."""
    assert "belongs_to_punctuation_class" in PUNCTUATION_CODEPOINT_CLASSIFICATION.required_illah


def test_residual_rule_requires_is_unclassified_codepoint_wasf():
    """Test that RESIDUAL_CODEPOINT_CLASSIFICATION requires is_unclassified_codepoint wasf."""
    assert "is_unclassified_codepoint" in RESIDUAL_CODEPOINT_CLASSIFICATION.required_effective_wasf


def test_residual_rule_requires_belongs_to_residual_class_illah():
    """Test that RESIDUAL_CODEPOINT_CLASSIFICATION requires belongs_to_residual_class illah."""
    assert "belongs_to_residual_class" in RESIDUAL_CODEPOINT_CLASSIFICATION.required_illah


def test_letter_rule_blocks_when_specific_letter_wasf_missing():
    """
    CRITICAL TEST: LetterCodePoint should NOT be produced if wasf:is_arabic_letter is missing.

    This tests that the rule requirement is enforced by QiyasKernel, not just that
    evidence happens to contain the wasf.
    """
    from qiyas_core.evidence import Evidence, EvidenceSet
    from qiyas_core.kernel import QiyasContext, QiyasRequest
    from qiyas_core.node import QiyasNodeRef
    import uuid

    kernel = QiyasKernel()
    codepoint = 0x0628  # ب (Arabic letter Ba)

    # Build evidence WITHOUT type-specific wasf:is_arabic_letter
    # Only include generic wasf:is_classifiable_codepoint
    proves = [
        "اصل:established",
        "فرع:determined",
        "وصف:is_classifiable_codepoint:evidenced",  # Generic only - MISSING is_arabic_letter!
        "علة:belongs_to_typed_domain:verified",
        "علة:belongs_to_letter_class:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    ]

    evidence = EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:test:{uuid.uuid4().hex[:8]}",
                source_layer="TypedCodePointClassificationQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORMAL_STRUCTURE,
                trace_ids=("test:missing_wasf",),
            ),
        )
    )

    asl = QiyasNodeRef(
        node_id="اصل:typed_codepoint_classification_domain",
        node_type="TypedCodePointClassificationDomain",
        identity_ids=("identity:typed_codepoint_domain",),
        trace_ids=("test:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    far = QiyasNodeRef(
        node_id=f"فرع:unicode_candidate:{codepoint:04x}",
        node_type="UnicodeCandidate",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        trace_ids=("test:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    request = QiyasRequest(
        rule=LETTER_CODEPOINT_CLASSIFICATION,  # Uses rule that REQUIRES is_arabic_letter
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="TypedCodePointClassificationQiyas"),
    )

    result = kernel.apply(request)

    # The request should be BLOCKED because wasf:is_arabic_letter is missing
    assert len(result.accepted) == 0, "LetterCodePoint should NOT be produced when is_arabic_letter wasf is missing"
    assert len(result.blocked) > 0, "Request should be blocked when required wasf is missing"


def test_haraka_rule_blocks_when_specific_haraka_wasf_missing():
    """
    CRITICAL TEST: HarakaCodePoint should NOT be produced if wasf:is_arabic_haraka is missing.
    """
    from qiyas_core.evidence import Evidence, EvidenceSet
    from qiyas_core.kernel import QiyasContext, QiyasRequest
    from qiyas_core.node import QiyasNodeRef
    import uuid

    kernel = QiyasKernel()
    codepoint = 0x064E  # Fatha

    proves = [
        "اصل:established",
        "فرع:determined",
        "وصف:is_classifiable_codepoint:evidenced",  # Generic only - MISSING is_arabic_haraka!
        "علة:belongs_to_typed_domain:verified",
        "علة:belongs_to_haraka_class:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    ]

    evidence = EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:test:{uuid.uuid4().hex[:8]}",
                source_layer="TypedCodePointClassificationQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORMAL_STRUCTURE,
                trace_ids=("test:missing_wasf",),
            ),
        )
    )

    asl = QiyasNodeRef(
        node_id="اصل:typed_codepoint_classification_domain",
        node_type="TypedCodePointClassificationDomain",
        identity_ids=("identity:typed_codepoint_domain",),
        trace_ids=("test:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    far = QiyasNodeRef(
        node_id=f"فرع:unicode_candidate:{codepoint:04x}",
        node_type="UnicodeCandidate",
        identity_ids=(f"identity:codepoint:{codepoint:04x}",),
        trace_ids=("test:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    request = QiyasRequest(
        rule=HARAKA_CODEPOINT_CLASSIFICATION,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="TypedCodePointClassificationQiyas"),
    )

    result = kernel.apply(request)

    assert len(result.accepted) == 0, "HarakaCodePoint should NOT be produced when is_arabic_haraka wasf is missing"
    assert len(result.blocked) > 0, "Request should be blocked when required wasf is missing"


# ---------------------------------------------------------------------------
# Z4 — Declassification of BoundaryCodePoint in the canonical path.
#
# Per PRE_QIYAS_TOKENIZER_CONSTITUTION (Option C, §6):
#   - whitespace must not enter UnicodeQiyas as UnicodeCandidate,
#   - whitespace must not become TypedCodePoint, and
#   - boundary context is sourced from SequenceContextTokenizer.
#
# UnicodeQiyas already rejects whitespace (outside ARABIC_RANGES), so
# the canonical Unicode → Typed chain cannot produce a BoundaryCodePoint
# for any whitespace input. The boundary branch in
# `typed_codepoint_adapter.classify_codepoint(int)` survives only for
# legacy unit fixtures that bypass UnicodeQiyas — those legacy tests
# remain above; the tests below assert the canonical-path declassification.
# ---------------------------------------------------------------------------


def test_canonical_path_rejects_whitespace_before_typed_layer():
    """U+0020 is blocked at UnicodeQiyas and therefore never reaches
    `TypedCodePointClassificationQiyas` in the canonical pipeline.

    This is the Z4 declassification witness for whitespace: it is
    constitutionally a tokenizer concern, not a TypedCodePoint concern.
    """
    from qiyas_core.unicode_adapter import UnicodeLayerAdapter

    kernel = QiyasKernel()
    unicode_layer = UnicodeLayerAdapter(kernel=kernel)

    for whitespace_cp in (0x0020, 0x0009, 0x000A, 0x000D):
        u_set = unicode_layer.process_codepoint(whitespace_cp)
        assert len(u_set.accepted) == 0, (
            f"UnicodeQiyas must reject whitespace U+{whitespace_cp:04X} "
            "so the canonical chain cannot reach BoundaryCodePoint classification"
        )


def test_canonical_typed_chain_does_not_emit_boundary_codepoint_for_whitespace():
    """The canonical Unicode → Typed chain produces no candidate at all
    for whitespace inputs — in particular, no `BoundaryCodePoint`."""
    from qiyas_core.unicode_adapter import UnicodeLayerAdapter

    kernel = QiyasKernel()
    unicode_layer = UnicodeLayerAdapter(kernel=kernel)
    typed_layer = TypedCodePointLayerAdapter(kernel=kernel)

    for whitespace_cp in (0x0020, 0x0009, 0x000A, 0x000D):
        u_set = unicode_layer.process_codepoint(whitespace_cp)
        # No accepted UnicodeCandidate ⇒ TypedCodePoint classification
        # is not invoked from the canonical driver. We do not bypass
        # UnicodeQiyas here; that bypass is the legacy fixture path.
        assert len(u_set.accepted) == 0
        # And the legacy bypass (kept only for fixtures) still classifies
        # whitespace as `BoundaryCodePoint`, which is the historic
        # behaviour the rule retains. That branch is legacy unreachable
        # from the canonical pipeline (asserted above).
        legacy_set = typed_layer.classify_codepoint(whitespace_cp)
        assert legacy_set.accepted[0].candidate_type == "BoundaryCodePoint"


def test_boundary_codepoint_classification_marked_legacy_unreachable():
    """The Z4 declassification annotation is present in the rule's source
    (a load-bearing comment, since the rule survives for legacy tests
    and external re-exports). This guards against silent re-promotion
    of the boundary rule into a canonical caller."""
    import inspect
    from qiyas_core.rules import typed_codepoint_rules

    source = inspect.getsource(typed_codepoint_rules)
    assert "Z4 declassification" in source
    assert "legacy unreachable" in source.lower()


def test_boundary_helpers_marked_legacy_in_adapter():
    """The Z4 declassification annotation is present in the adapter
    module — `is_boundary`, `BOUNDARY_CODEPOINTS`, and the boundary
    branches are reachable only from legacy fixtures or the deferred
    Z5 `run_qiyas._classify_position` import."""
    import inspect
    from qiyas_core import typed_codepoint_adapter

    source = inspect.getsource(typed_codepoint_adapter)
    assert "Z4 declassification" in source
    assert "legacy unreachable" in source.lower()
