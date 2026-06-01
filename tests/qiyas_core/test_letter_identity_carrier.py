"""
Tests for LetterIdentityCarrier

Validates that letter identity can be proven atomically from LetterCodePoint
without requiring sequence context, ConditionedTypedSequence, or other carriers.
"""

import pytest

from qiyas_core.candidate import Candidate
from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter


def test_baa_letter_codepoint_proves_baa_identity():
    """
    Test that LetterCodePoint(BAA) proves LetterIdentityCarrier(BAA).

    Constitutional requirement: atomic proof without sequence context.
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # BAA LetterCodePoint (U+0628)
    baa_codepoint = Candidate(
        candidate_id="test_baa",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x0628},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    # Process through adapter
    result = adapter.process_letter_codepoint(baa_codepoint)

    # Validate result
    assert len(result.candidates) == 1
    identity = result.candidates[0]

    assert identity.candidate_type == "LetterIdentityCarrier"
    assert identity.value["letter_name"] == "BAA"
    assert identity.value["unicode_identity"] == "U+0628"
    assert identity.value["script_identity"] == "ARABIC_LETTER_BAA"
    assert identity.value["sound_identity"] == "VOICED_BILABIAL_STOP"
    assert identity.value["codepoint"] == 0x0628

    # Validate evidence includes required wasf and illah
    evidence_keys = {e.claim_key for e in identity.evidence.claims}
    assert "has_baa_unicode_identity" in evidence_keys
    assert "has_baa_script_identity" in evidence_keys
    assert "has_baa_sound_identity" in evidence_keys
    assert "has_baa_makhraj_sifat" in evidence_keys


def test_taa_letter_codepoint_proves_taa_identity():
    """
    Test that LetterCodePoint(TAA) proves LetterIdentityCarrier(TAA).
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # TAA LetterCodePoint (U+062A)
    taa_codepoint = Candidate(
        candidate_id="test_taa",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x062A},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    result = adapter.process_letter_codepoint(taa_codepoint)

    assert len(result.candidates) == 1
    identity = result.candidates[0]

    assert identity.candidate_type == "LetterIdentityCarrier"
    assert identity.value["letter_name"] == "TAA"
    assert identity.value["sound_identity"] == "VOICELESS_ALVEOLAR_STOP"


def test_seen_does_not_become_sheen():
    """
    Test that SEEN identity is preserved and does not become SHEEN.

    Constitutional requirement: invalidating differences prevent confusion.
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # SEEN LetterCodePoint (U+0633)
    seen_codepoint = Candidate(
        candidate_id="test_seen",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x0633},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    result = adapter.process_letter_codepoint(seen_codepoint)

    assert len(result.candidates) == 1
    identity = result.candidates[0]

    assert identity.value["letter_name"] == "SEEN"
    assert identity.value["letter_name"] != "SHEEN"
    assert identity.value["sound_identity"] == "VOICELESS_ALVEOLAR_FRICATIVE"


def test_baa_does_not_become_taa():
    """
    Test that BAA identity is preserved and does not become TAA.

    Constitutional requirement: baa_vs_taa_voicing invalidating difference.
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    baa_codepoint = Candidate(
        candidate_id="test_baa",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x0628},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    result = adapter.process_letter_codepoint(baa_codepoint)

    assert len(result.candidates) == 1
    identity = result.candidates[0]

    assert identity.value["letter_name"] == "BAA"
    assert identity.value["letter_name"] != "TAA"
    assert "VOICED" in identity.value["sound_identity"]


def test_kaf_letter_codepoint_proves_kaf_identity():
    """
    Test that LetterCodePoint(KAF) proves LetterIdentityCarrier(KAF).
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # KAF LetterCodePoint (U+0643)
    kaf_codepoint = Candidate(
        candidate_id="test_kaf",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x0643},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    result = adapter.process_letter_codepoint(kaf_codepoint)

    assert len(result.candidates) == 1
    identity = result.candidates[0]

    assert identity.candidate_type == "LetterIdentityCarrier"
    assert identity.value["letter_name"] == "KAF"
    assert identity.value["sound_identity"] == "VOICELESS_VELAR_STOP"


def test_letter_identity_does_not_require_sequence():
    """
    Test that LetterIdentityCarrier can be proven from a single LetterCodePoint
    without requiring sequence context or ConditionedTypedSequence.

    This validates the parallel path architecture.
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Single letter, no sequence
    baa_codepoint = Candidate(
        candidate_id="isolated_baa",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x0628},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    # Should succeed without sequence context
    result = adapter.process_letter_codepoint(baa_codepoint)

    assert len(result.candidates) == 1
    assert result.candidates[0].candidate_type == "LetterIdentityCarrier"


def test_non_letter_codepoint_returns_empty():
    """
    Test that non-LetterCodePoint inputs return empty CandidateSet.
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # HarakaCodePoint should not produce LetterIdentityCarrier
    haraka_candidate = Candidate(
        candidate_id="test_haraka",
        candidate_type="HarakaCodePoint",
        value={"codepoint": 0x064E},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    result = adapter.process_letter_codepoint(haraka_candidate)

    assert len(result.candidates) == 0


def test_unmapped_letter_returns_empty():
    """
    Test that unmapped letters return empty (not yet in identity map).
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Use a valid Arabic letter not yet in our map (e.g., DAAL U+062F)
    daal_codepoint = Candidate(
        candidate_id="test_daal",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x062F},
        evidence=None,
        rank=None,
        trace_ids=(),
    )

    result = adapter.process_letter_codepoint(daal_codepoint)

    # Should return empty until DAAL is added to map
    assert len(result.candidates) == 0


def test_letter_identity_forbidden_outputs():
    """
    Test that LetterIdentityCarrier rules forbid compositional outputs.

    Constitutional requirement: LetterIdentityCarrier is atomic, not compositional.
    """
    from qiyas_core.rules.letter_identity_rules import BAA_LETTER_IDENTITY

    forbidden = BAA_LETTER_IDENTITY.forbidden_outputs

    # Must forbid compositional types
    assert "SlotCandidate" in forbidden
    assert "SlotGeometry" in forbidden
    assert "SyllableCandidate" in forbidden
    assert "HukmCandidate" in forbidden


def test_letter_identity_preserves_trace():
    """
    Test that LetterIdentityCarrier preserves trace from LetterCodePoint.
    """
    kernel = QiyasKernel()
    adapter = LetterIdentityLayerAdapter(kernel=kernel)

    baa_codepoint = Candidate(
        candidate_id="traced_baa",
        candidate_type="LetterCodePoint",
        value={"codepoint": 0x0628},
        evidence=None,
        rank=None,
        trace_ids=("parent_unicode", "parent_typed"),
    )

    result = adapter.process_letter_codepoint(baa_codepoint)

    assert len(result.candidates) == 1
    identity = result.candidates[0]

    # Trace should include parent traces + parent ID
    assert "parent_unicode" in identity.trace_ids
    assert "parent_typed" in identity.trace_ids
    assert "traced_baa" in identity.trace_ids
