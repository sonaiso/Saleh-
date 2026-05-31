"""
Tests for AtomicUnitLayerAdapter.

These tests verify that the AtomicUnitLayerAdapter correctly:
1. Accepts valid bindings of Arabic letter + haraka/diacritic
2. Blocks invalid bindings (non-Arabic carrier, Latin letter, digit)
3. Maintains separate identity_ids and trace_ids for all candidates
4. Uses ATOMIC_UNIT_BINDING rule exclusively
5. Produces only AtomicUnitCandidate, never higher-level candidates
6. Respects the constitutional boundaries
"""
from qiyas_core.atomic_unit_adapter import AtomicUnitLayerAdapter, is_arabic_letter
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel


def test_ba_plus_fatha_produces_accepted_candidate():
    """Test that Arabic letter Ba + Fatha produces an accepted AtomicUnitCandidate."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+064E is Arabic Fatha (َ )
    result = adapter.process_binding(0x0628, 0x064E)

    assert len(result.accepted) == 1
    assert len(result.blocked) == 0
    assert len(result.deferred) == 0

    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert candidate.rank == EvidenceRank.FORM
    assert candidate.layer == "AtomicUnitQiyas"
    assert candidate.source_rule_id == "atomic_unit.binding"


def test_ba_plus_damma_produces_accepted_candidate():
    """Test that Arabic letter Ba + Damma produces an accepted AtomicUnitCandidate."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+064F is Arabic Damma (ُ )
    result = adapter.process_binding(0x0628, 0x064F)

    assert len(result.accepted) == 1
    assert len(result.blocked) == 0
    assert len(result.deferred) == 0

    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert candidate.rank == EvidenceRank.FORM


def test_ba_plus_kasra_produces_accepted_candidate():
    """Test that Arabic letter Ba + Kasra produces an accepted AtomicUnitCandidate."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0650 is Arabic Kasra (ِ )
    result = adapter.process_binding(0x0628, 0x0650)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "AtomicUnitCandidate"


def test_ba_plus_sukun_produces_accepted_candidate():
    """Test that Arabic letter Ba + Sukun produces an accepted AtomicUnitCandidate."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0652 is Arabic Sukun (ْ )
    result = adapter.process_binding(0x0628, 0x0652)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "AtomicUnitCandidate"


def test_ba_plus_shadda_produces_accepted_candidate():
    """Test that Arabic letter Ba + Shadda produces an accepted AtomicUnitCandidate."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0651 is Arabic Shadda (ّ )
    result = adapter.process_binding(0x0628, 0x0651)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "AtomicUnitCandidate"


def test_shadda_evidence_distinct():
    """Test that Shadda binding includes specific evidence for gemination."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0651 is Arabic Shadda (ّ )
    request = adapter.build_request_for_binding(0x0628, 0x0651)

    # Verify evidence is established
    assert request.evidence.proves("asl:established")
    assert request.evidence.proves("far:determined")
    assert request.evidence.proves("wasf:carrier_accepts_mark:evidenced")
    assert request.evidence.proves("illah:licensed_atomic_binding:verified")


def test_latin_carrier_plus_fatha_blocked():
    """Test that Latin letter + Fatha is blocked."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0041 is Latin capital letter A
    # U+064E is Arabic Fatha (َ )
    result = adapter.process_binding(0x0041, 0x064E)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0
    assert len(result.deferred) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about carrier not being Arabic letter
    assert len(candidate.residuals) > 0
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_arabic_digit_plus_fatha_blocked():
    """Test that Arabic digit + Fatha is blocked."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0660 is Arabic-Indic digit zero
    # U+064E is Arabic Fatha (َ )
    result = adapter.process_binding(0x0660, 0x064E)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.rank == EvidenceRank.ZERO


def test_additional_diacritic_not_treated_as_core_haraka():
    """
    Test that additional diacritics are accepted but remain distinct from core haraka.

    This test ensures constitutional compliance: additional diacritics like maddah
    can bind to carriers, but they maintain their distinct classification.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0653 is Maddah above (additional diacritic, not core haraka)
    result = adapter.process_binding(0x0628, 0x0653)

    # The binding should be accepted (valid carrier + valid mark)
    assert len(result.accepted) == 1
    candidate = result.accepted[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "AtomicUnitCandidate"


def test_identity_and_trace_ids_are_disjoint():
    """Test that all AtomicUnitCandidate maintain separate identity_ids and trace_ids."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Test with both valid and invalid bindings
    test_cases = [
        (0x0628, 0x064E),  # Ba + Fatha (valid)
        (0x0628, 0x064F),  # Ba + Damma (valid)
        (0x0041, 0x064E),  # Latin A + Fatha (invalid)
        (0x0660, 0x064E),  # Arabic digit + Fatha (invalid)
    ]

    for carrier, mark in test_cases:
        result = adapter.process_binding(carrier, mark)

        # Get the single candidate
        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        # Verify identity_ids and trace_ids are disjoint
        identity_set = set(candidate.identity_ids)
        trace_set = set(candidate.trace_ids)
        assert not (identity_set & trace_set), (
            f"Binding {carrier:04x}+{mark:04x}: identity_ids and trace_ids overlap: "
            f"{identity_set & trace_set}"
        )


def test_all_requests_use_atomic_unit_binding_rule():
    """Test that all processing uses the ATOMIC_UNIT_BINDING rule."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    test_cases = [
        (0x0628, 0x064E),  # Ba + Fatha
        (0x0628, 0x064F),  # Ba + Damma
        (0x0041, 0x064E),  # Latin A + Fatha (blocked)
    ]

    for carrier, mark in test_cases:
        result = adapter.process_binding(carrier, mark)

        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        assert candidate.source_rule_id == "atomic_unit.binding"
        assert candidate.layer == "AtomicUnitQiyas"


def test_no_higher_level_candidates():
    """
    Test that AtomicUnitLayerAdapter never produces higher-level candidates.

    Constitutional boundary: AtomicUnitQiyas produces only AtomicUnitCandidate,
    never SyllableCandidate, PronunciationCandidate, DalCandidate, etc.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Test various valid bindings
    test_cases = [
        (0x0628, 0x064E),  # Ba + Fatha
        (0x0628, 0x064F),  # Ba + Damma
        (0x0628, 0x0650),  # Ba + Kasra
        (0x0628, 0x0651),  # Ba + Shadda
        (0x0628, 0x0652),  # Ba + Sukun
    ]

    forbidden_types = [
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ]

    for carrier, mark in test_cases:
        result = adapter.process_binding(carrier, mark)

        all_candidates = result.accepted + result.blocked + result.deferred
        assert len(all_candidates) == 1
        candidate = all_candidates[0]

        # Should only produce AtomicUnitCandidate
        assert candidate.candidate_type == "AtomicUnitCandidate"
        for forbidden_type in forbidden_types:
            assert forbidden_type not in candidate.output_flags, (
                f"Binding {carrier:04x}+{mark:04x} should not have {forbidden_type} in output_flags"
            )


def test_is_arabic_letter_function():
    """Test the is_arabic_letter helper function."""
    # Arabic letters
    assert is_arabic_letter(0x0621)  # Hamza
    assert is_arabic_letter(0x0628)  # Ba
    assert is_arabic_letter(0x062A)  # Ta
    assert is_arabic_letter(0x064A)  # Ya

    # Not Arabic letters
    assert not is_arabic_letter(0x0041)  # Latin A
    assert not is_arabic_letter(0x0660)  # Arabic-Indic digit zero
    assert not is_arabic_letter(0x064E)  # Fatha (combining mark)
    assert not is_arabic_letter(0x0020)  # Space


def test_constitutional_boundary_no_syllable():
    """
    Constitutional test: AtomicUnitQiyas does not produce SyllableCandidate.

    This test ensures that even valid bindings do not produce syllable-level
    candidates. AtomicUnit is strictly carrier+mark, not CV/CVC/CVV.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Ba + Fatha is a valid atomic unit
    result = adapter.process_binding(0x0628, 0x064E)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]

    # Verify it's AtomicUnitCandidate, not SyllableCandidate
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert "SyllableCandidate" not in candidate.output_flags


def test_constitutional_boundary_no_pronunciation():
    """
    Constitutional test: AtomicUnitQiyas does not produce PronunciationCandidate.

    AtomicUnit is orthographic binding, not phonetic realization.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Ba + Sukun is a valid atomic unit
    result = adapter.process_binding(0x0628, 0x0652)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]

    # Verify it's AtomicUnitCandidate, not PronunciationCandidate
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert "PronunciationCandidate" not in candidate.output_flags


def test_constitutional_boundary_no_dal():
    """
    Constitutional test: AtomicUnitQiyas does not produce DalCandidate.

    AtomicUnit is form-level binding, not semantic reference.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Ba + Fatha is a valid atomic unit
    result = adapter.process_binding(0x0628, 0x064E)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]

    # Verify it's AtomicUnitCandidate, not DalCandidate
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert "DalCandidate" not in candidate.output_flags


def test_constitutional_boundary_no_meaning():
    """
    Constitutional test: AtomicUnitQiyas does not produce MeaningCandidate.

    AtomicUnit has no semantic content.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Ba + Kasra is a valid atomic unit
    result = adapter.process_binding(0x0628, 0x0650)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]

    # Verify it's AtomicUnitCandidate, not MeaningCandidate
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert "MeaningCandidate" not in candidate.output_flags


def test_constitutional_boundary_no_hukm():
    """
    Constitutional test: AtomicUnitQiyas does not produce HukmCandidate.

    AtomicUnit has no legal or normative judgment.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Ba + Shadda is a valid atomic unit
    result = adapter.process_binding(0x0628, 0x0651)

    assert len(result.accepted) == 1
    candidate = result.accepted[0]

    # Verify it's AtomicUnitCandidate, not HukmCandidate
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert "HukmCandidate" not in candidate.output_flags


def test_rank_ceiling_is_form():
    """Test that all AtomicUnitCandidate have rank ceiling of FORM."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Test valid bindings
    test_cases = [
        (0x0628, 0x064E),  # Ba + Fatha
        (0x0628, 0x064F),  # Ba + Damma
        (0x0628, 0x0650),  # Ba + Kasra
    ]

    for carrier, mark in test_cases:
        result = adapter.process_binding(carrier, mark)

        assert len(result.accepted) == 1
        candidate = result.accepted[0]

        # Rank must not exceed FORM
        assert candidate.rank == EvidenceRank.FORM, (
            f"Binding {carrier:04x}+{mark:04x} has rank {candidate.rank}, expected FORM"
        )


def test_evidence_claims_for_valid_binding():
    """Test that valid bindings produce all required evidence claims."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Ba + Fatha
    request = adapter.build_request_for_binding(0x0628, 0x064E)

    # Verify all required claims are present
    assert request.evidence.proves("asl:established")
    assert request.evidence.proves("far:determined")
    assert request.evidence.proves("wasf:carrier_accepts_mark:evidenced")
    assert request.evidence.proves("illah:licensed_atomic_binding:verified")
    assert request.evidence.proves("wadi:sabab:established")
    assert request.evidence.proves("wadi:shart:satisfied")
    assert request.evidence.proves("wadi:mani:absent")
    assert request.evidence.proves("wadi:sihha:valid")
    assert request.evidence.proves("wadi:fasad:absent")
    assert request.evidence.proves("wadi:butlan:absent")


def test_evidence_claims_for_invalid_binding():
    """Test that invalid bindings have clean blocking residuals."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Latin A + Fatha (invalid carrier)
    result = adapter.process_binding(0x0041, 0x064E)

    assert len(result.blocked) == 1
    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED

    # Get all residual types
    residual_types = [r.residual_type for r in candidate.residuals]

    # Should have fariq blocking
    assert "blocking_fariq_present" in residual_types

    # Should have wasf and illah missing
    assert "effective_wasf_missing" in residual_types
    assert "shared_illah_missing" in residual_types

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
            f"Did not expect {wadi_failure} in residuals for invalid carrier. "
            f"Blocking should be clean: only due to fariq/wasf/illah, not wadi failures."
        )


def test_multiple_arabic_letters_with_same_mark():
    """Test that different Arabic letters can all bind with the same mark."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Test multiple Arabic letters with Fatha
    arabic_letters = [
        0x0621,  # Hamza
        0x0628,  # Ba
        0x062A,  # Ta
        0x062B,  # Tha
        0x062C,  # Jim
    ]

    for letter in arabic_letters:
        result = adapter.process_binding(letter, 0x064E)  # Fatha

        assert len(result.accepted) == 1, f"Letter {letter:04x} + Fatha should be accepted"
        candidate = result.accepted[0]
        assert candidate.status == CandidateStatus.ACCEPTED
        assert candidate.candidate_type == "AtomicUnitCandidate"


def test_ba_plus_latin_a_blocked():
    """Test that Arabic letter Ba + Latin A is blocked (mark is not a diacritic)."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0041 is Latin capital letter A (not a diacritic)
    result = adapter.process_binding(0x0628, 0x0041)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0
    assert len(result.deferred) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "AtomicUnitCandidate"
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about mark not being a diacritic
    assert len(candidate.residuals) > 0
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_ba_plus_arabic_letter_blocked():
    """Test that Arabic letter Ba + Arabic letter Ya is blocked (mark is not a diacritic)."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+064A is Arabic letter Ya (ي) - not a diacritic
    result = adapter.process_binding(0x0628, 0x064A)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about mark not being a diacritic
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_ba_plus_arabic_digit_blocked():
    """Test that Arabic letter Ba + Arabic digit is blocked (mark is not a diacritic)."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0660 is Arabic-Indic digit zero (not a diacritic)
    result = adapter.process_binding(0x0628, 0x0660)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about mark not being a diacritic
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_ba_plus_non_diacritic_codepoint_blocked():
    """Test that Arabic letter Ba + non-diacritic codepoint is blocked."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0020 is space (not a diacritic)
    result = adapter.process_binding(0x0628, 0x0020)

    assert len(result.blocked) == 1
    assert len(result.accepted) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.rank == EvidenceRank.ZERO

    # Should have a residual about mark not being a diacritic
    residual_types = [r.residual_type for r in candidate.residuals]
    assert "blocking_fariq_present" in residual_types


def test_invalid_mark_blocked_residuals_are_clean():
    """
    Test that invalid marks have clean blocking residuals.

    Invalid marks should be blocked due to:
    - blocking_fariq_present (the fariq: mark_is_not_arabic_diacritic)
    - effective_wasf_missing (wasf not evidenced for non-diacritic)
    - shared_illah_missing (illah not verified for non-diacritic)

    But NOT due to wadi failures, since wadi conditions are satisfied.
    """
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # U+0628 is Arabic letter Ba (ب)
    # U+0041 is Latin A (not a diacritic)
    result = adapter.process_binding(0x0628, 0x0041)

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
            f"Did not expect {wadi_failure} in residuals for invalid mark. "
            f"Blocking should be clean: only due to fariq/wasf/illah, not wadi failures."
        )


def test_same_letter_with_different_marks():

    """Test that the same Arabic letter can bind with different marks."""
    adapter = AtomicUnitLayerAdapter(kernel=QiyasKernel())

    # Test Ba with different marks
    marks = [
        0x064E,  # Fatha
        0x064F,  # Damma
        0x0650,  # Kasra
        0x0651,  # Shadda
        0x0652,  # Sukun
    ]

    for mark in marks:
        result = adapter.process_binding(0x0628, mark)  # Ba

        assert len(result.accepted) == 1, f"Ba + mark {mark:04x} should be accepted"
        candidate = result.accepted[0]
        assert candidate.status == CandidateStatus.ACCEPTED
        assert candidate.candidate_type == "AtomicUnitCandidate"
