"""
Tests for HarakaLayerAdapter.

These tests verify that the HarakaLayerAdapter correctly:
1. Accepts Arabic harakat (combining marks) as valid HarakaCandidate
2. Blocks non-harakat codepoints with appropriate residuals
3. Maintains separate identity_ids and trace_ids for all candidates
4. Uses HARAKA_ARABIC_DIACRITIC rule exclusively
"""
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.haraka_adapter import HarakaLayerAdapter
from qiyas_core.kernel import QiyasKernel


def test_fatha_produces_accepted_candidate():
    """Test that Fatha (U+064E) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+064E is Arabic Fatha (َ )
    result = adapter.process_codepoint(0x064E)

    assert len(result.accepted) == 1
    assert len(result.blocked) == 0
    assert len(result.deferred) == 0

    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCandidate"
    assert candidate.rank == EvidenceRank.FORM
    assert candidate.layer == "HarakaQiyas"
    assert candidate.source_rule_id == "haraka.arabic.diacritic"


def test_damma_produces_accepted_candidate():
    """Test that Damma (U+064F) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+064F is Arabic Damma (ُ )
    result = adapter.process_codepoint(0x064F)

    assert len(result.accepted) == 1
    assert len(result.blocked) == 0
    assert len(result.deferred) == 0

    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCandidate"
    assert candidate.rank == EvidenceRank.FORM


def test_kasra_produces_accepted_candidate():
    """Test that Kasra (U+0650) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+0650 is Arabic Kasra (ِ )
    result = adapter.process_codepoint(0x0650)

    assert len(result.accepted) == 1
    assert len(result.blocked) == 0
    assert len(result.deferred) == 0

    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCandidate"


def test_sukun_produces_accepted_candidate():
    """Test that Sukun (U+0652) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+0652 is Arabic Sukun (ْ )
    result = adapter.process_codepoint(0x0652)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCandidate"


def test_shadda_produces_accepted_candidate():
    """Test that Shadda (U+0651) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+0651 is Arabic Shadda (ّ )
    result = adapter.process_codepoint(0x0651)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCandidate"


def test_fathatan_produces_accepted_candidate():
    """Test that Fathatan/tanwin (U+064B) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+064B is Arabic Fathatan (ً )
    result = adapter.process_codepoint(0x064B)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "HarakaCandidate"


def test_dammatan_produces_accepted_candidate():
    """Test that Dammatan/tanwin (U+064C) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+064C is Arabic Dammatan (ٌ )
    result = adapter.process_codepoint(0x064C)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED


def test_kasratan_produces_accepted_candidate():
    """Test that Kasratan/tanwin (U+064D) produces an accepted HarakaCandidate."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+064D is Arabic Kasratan (ٍ )
    result = adapter.process_codepoint(0x064D)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED


def test_non_haraka_arabic_letter_produces_blocked_candidate():
    """Test that non-haraka codepoints (e.g., Arabic letter Ba) produce blocked candidates."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب) - not a haraka
    result = adapter.process_codepoint(0x0628)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0
    assert len(result.deferred) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "HarakaCandidate"
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about non-haraka codepoint
    assert len(candidate.residuals) > 0
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_latin_letter_produces_blocked_candidate():
    """Test that Latin letters produce blocked candidates."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+0041 is Latin capital letter A
    result = adapter.process_codepoint(0x0041)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0
    assert len(result.deferred) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.rank == EvidenceRank.ZERO


def test_identity_and_trace_ids_are_disjoint():
    """Test that all candidates maintain separate identity_ids and trace_ids."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # Test with both harakat and non-harakat codepoints
    test_codepoints = [
        0x064E,  # Fatha (haraka)
        0x0628,  # Arabic Ba (not haraka)
        0x064F,  # Damma (haraka)
        0x0041,  # Latin A (not haraka)
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


def test_all_requests_use_haraka_arabic_diacritic_rule():
    """Test that all processing uses the HARAKA_ARABIC_DIACRITIC rule."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    test_codepoints = [0x064E, 0x064F, 0x0650, 0x0628, 0x0041]

    for codepoint in test_codepoints:
        result = adapter.process_codepoint(codepoint)

        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        assert candidate.source_rule_id == "haraka.arabic.diacritic"
        assert candidate.layer == "HarakaQiyas"


def test_no_higher_level_candidates():
    """Test that HarakaLayerAdapter never produces higher-level candidates."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # Test various codepoints
    test_codepoints = [0x064E, 0x064F, 0x0650, 0x0651, 0x0652]

    forbidden_types = [
        "AtomicUnitCandidate",
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ]

    for codepoint in test_codepoints:
        result = adapter.process_codepoint(codepoint)

        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        # Should only produce HarakaCandidate
        assert candidate.candidate_type == "HarakaCandidate"
        for forbidden_type in forbidden_types:
            assert forbidden_type not in candidate.output_flags


def test_process_text_returns_multiple_candidates():
    """Test that process_text returns one CandidateSet per character."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # Text with multiple harakat
    # Note: using just the harakat marks without base letters
    text = "\u064E\u064F"  # Fatha + Damma
    results = adapter.process_text(text)

    assert len(results) == 2

    # Both should be accepted (both are harakat)
    for result in results:
        assert len(result.accepted) == 1
        assert result.accepted[0].candidate_type == "HarakaCandidate"


def test_harakat_range_boundaries():
    """Test the boundaries of the harakat Unicode range."""
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+064B is the start of harakat range
    result_start = adapter.process_codepoint(0x064B)
    assert len(result_start.accepted) == 1
    assert result_start.accepted[0].status == CandidateStatus.ACCEPTED

    # U+065F is the end of harakat range
    result_end = adapter.process_codepoint(0x065F)
    assert len(result_end.accepted) == 1
    assert result_end.accepted[0].status == CandidateStatus.ACCEPTED

    # U+064A is just before the range (Arabic letter Ya)
    result_before = adapter.process_codepoint(0x064A)
    assert len(result_before.blocked) == 1
    assert result_before.blocked[0].status == CandidateStatus.BLOCKED

    # U+0660 is just after the range (Arabic-Indic digit zero)
    result_after = adapter.process_codepoint(0x0660)
    assert len(result_after.blocked) == 1
    assert result_after.blocked[0].status == CandidateStatus.BLOCKED


def test_non_haraka_blocked_residuals_are_clean():
    """
    Test that non-haraka codepoints have clean blocking residuals.

    Non-haraka codepoints should be blocked due to:
    - blocking_fariq_present (the fariq: non_haraka_codepoint)
    - effective_wasf_missing (wasf not evidenced for non-haraka)
    - shared_illah_missing (illah not verified for non-haraka)

    But NOT due to wadi failures, since wadi conditions are satisfied
    even for non-haraka codepoints (they just fail on domain mismatch).
    """
    adapter = HarakaLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (not a haraka)
    result = adapter.process_codepoint(0x0628)

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
            f"Did not expect {wadi_failure} in residuals for non-haraka codepoint. "
            f"Blocking should be clean: only due to fariq/wasf/illah, not wadi failures."
        )
