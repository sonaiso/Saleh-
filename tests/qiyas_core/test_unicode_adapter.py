"""
Tests for UnicodeLayerAdapter.

These tests verify that the UnicodeLayerAdapter correctly:
1. Accepts Arabic codepoints (e.g., U+0628) as valid UnicodeCandidate
2. Blocks non-Arabic codepoints with appropriate residuals
3. Maintains separate identity_ids and trace_ids for all candidates
4. Uses UNICODE_ARABIC_MEMBERSHIP rule exclusively
"""
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.unicode_adapter import UnicodeLayerAdapter


def test_arabic_letter_ba_produces_accepted_candidate():
    """Test that Arabic letter Ba (U+0628) produces an accepted UnicodeCandidate."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    result = adapter.process_codepoint(0x0628)

    assert len(result.accepted) == 1
    assert len(result.blocked) == 0
    assert len(result.deferred) == 0

    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "UnicodeCandidate"
    assert candidate.rank == EvidenceRank.FORM
    assert candidate.layer == "UnicodeQiyas"
    assert candidate.source_rule_id == "unicode.arabic.membership"


def test_non_arabic_symbol_produces_blocked_candidate():
    """Test that non-Arabic symbols (e.g., Latin 'A') produce blocked candidates."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # U+0041 is Latin capital letter A
    result = adapter.process_codepoint(0x0041)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0
    assert len(result.deferred) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "UnicodeCandidate"
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about non-Arabic codepoint
    assert len(candidate.residuals) > 0
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_identity_and_trace_ids_are_disjoint():
    """Test that all candidates maintain separate identity_ids and trace_ids."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # Test with both Arabic and non-Arabic codepoints
    test_codepoints = [
        0x0628,  # Arabic Ba
        0x0041,  # Latin A
        0x0629,  # Arabic Ta Marbuta
    ]

    for codepoint in test_codepoints:
        result = adapter.process_codepoint(codepoint)

        # Get the single candidate
        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        # Verify identity_ids and trace_ids are disjoint
        identity_set = set(candidate.identity_ids)
        trace_set = set(candidate.trace_ids)
        assert not (identity_set & trace_set), (
            f"Codepoint {codepoint:04x}: identity_ids and trace_ids overlap: "
            f"{identity_set & trace_set}"
        )


def test_all_requests_use_unicode_arabic_membership_rule():
    """Test that all processing uses the UNICODE_ARABIC_MEMBERSHIP rule."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    test_codepoints = [0x0628, 0x0041, 0x062D, 0x0030]

    for codepoint in test_codepoints:
        result = adapter.process_codepoint(codepoint)

        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        assert candidate.source_rule_id == "unicode.arabic.membership"
        assert candidate.layer == "UnicodeQiyas"


def test_no_pronunciation_or_dal_candidates():
    """Test that UnicodeLayerAdapter never produces Pronunciation or Dal candidates."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # Test various codepoints
    test_codepoints = [0x0628, 0x0629, 0x062A, 0x062B, 0x0041]

    for codepoint in test_codepoints:
        result = adapter.process_codepoint(codepoint)

        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        # Should only produce UnicodeCandidate
        assert candidate.candidate_type == "UnicodeCandidate"
        assert "PronunciationCandidate" not in candidate.output_flags
        assert "DalCandidate" not in candidate.output_flags


def test_process_text_returns_multiple_candidates():
    """Test that process_text returns one CandidateSet per character."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # Mixed Arabic and non-Arabic text
    text = "بت"  # Arabic Ba and Ta
    results = adapter.process_text(text)

    assert len(results) == 2

    # Both should be accepted (both are Arabic)
    for result in results:
        assert len(result.accepted) == 1
        assert result.accepted[0].candidate_type == "UnicodeCandidate"


def test_arabic_supplement_range():
    """Test that Arabic Supplement range (0750-077F) is recognized."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # U+0750 is in Arabic Supplement
    result = adapter.process_codepoint(0x0750)

    assert len(result.accepted) == 1
    assert result.accepted[0].status == CandidateStatus.ACCEPTED


def test_control_character_may_be_blocked():
    """Test that control characters are handled (likely blocked)."""
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # U+0000 is NULL control character
    result = adapter.process_codepoint(0x0000)

    # Should be blocked since it's not in Arabic range
    assert len(result.blocked) == 1
    assert result.blocked[0].status == CandidateStatus.BLOCKED


def test_non_arabic_blocked_residuals_are_clean():
    """
    Test that non-Arabic codepoints have clean blocking residuals.

    Non-Arabic codepoints should be blocked due to:
    - blocking_fariq_present (the fariq: non_arabic_codepoint)
    - effective_wasf_missing (wasf not evidenced for non-Arabic)
    - shared_illah_missing (illah not verified for non-Arabic)

    But NOT due to wadi failures, since wadi conditions are satisfied
    even for non-Arabic codepoints (they just fail on domain mismatch).
    """
    adapter = UnicodeLayerAdapter(kernel=QiyasKernel())

    # U+0041 is Latin capital letter A
    result = adapter.process_codepoint(0x0041)

    assert len(result.blocked) == 1
    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED

    # Get all residual types
    residual_types = [r.residual_type for r in candidate.residuals]

    # Should have fariq blocking
    assert "blocking_fariq_present" in residual_types, (
        "Expected blocking_fariq_present in residuals"
    )

    # Should have wasf and illah missing (genuinely not applicable)
    assert "effective_wasf_missing" in residual_types, (
        "Expected effective_wasf_missing in residuals"
    )
    assert "shared_illah_missing" in residual_types, (
        "Expected shared_illah_missing in residuals"
    )

    # Should NOT have wadi failures (wadi conditions are satisfied)
    wadi_failure_types = [
        "wadi_sabab_failed",
        "wadi_shart_failed",
        "wadi_mani_failed",
        "wadi_sihha_failed",
        "wadi_fasad_failed",
        "wadi_butlan_failed",
    ]
    for wadi_failure in wadi_failure_types:
        assert wadi_failure not in residual_types, (
            f"Did not expect {wadi_failure} in residuals for non-Arabic codepoint. "
            f"Blocking should be clean: only due to fariq/wasf/illah, not wadi failures."
        )
