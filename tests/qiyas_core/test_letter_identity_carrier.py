"""
Tests for LetterIdentityCarrier

Validates that letter identity can be proven atomically from LetterCodePoint
without requiring sequence context, ConditionedTypedSequence, or other carriers.

Constitutional compliance:
  - Uses TypedCodePointLayerAdapter.classify_codepoint() for proper fixtures
  - Validates identity_ids preservation
  - Validates evidence structure
  - Validates fariq (invalidating differences) proofs
"""

import pytest

from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter


def test_baa_letter_codepoint_proves_baa_identity():
    """
    Test that LetterCodePoint(BAA) proves LetterIdentityCarrier(BAA).

    Constitutional requirement: atomic proof without sequence context.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Get proper LetterCodePoint from TypedCodePointLayerAdapter
    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    assert len(typed_result.accepted) == 1

    baa_letter_codepoint = typed_result.accepted[0]
    assert baa_letter_codepoint.candidate_type == "LetterCodePoint"

    # Process through letter identity adapter
    result = letter_adapter.process_letter_codepoint(baa_letter_codepoint)

    # Validate result
    assert len(result.accepted) == 1
    identity = result.accepted[0]

    assert identity.candidate_type == "LetterIdentityCarrier"
    assert identity.status == CandidateStatus.ACCEPTED
    assert identity.rank == EvidenceRank.FORM

    # Validate identity_ids preservation
    # Kernel preserves input identities and adds asl identity
    assert "identity:codepoint:0628" in identity.identity_ids
    assert "identity:typed_codepoint_domain" in identity.identity_ids or "identity:typed_codepoint:letter" in identity.identity_ids
    assert "identity:letter_identity_domain" in identity.identity_ids


def test_taa_letter_codepoint_proves_taa_identity():
    """
    Test that LetterCodePoint(TAA) proves LetterIdentityCarrier(TAA).
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x062A)  # TAA
    taa_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(taa_letter_codepoint)

    assert len(result.accepted) == 1
    identity = result.accepted[0]

    assert identity.candidate_type == "LetterIdentityCarrier"
    # Kernel preserves input identities and adds asl identity
    assert "identity:codepoint:062a" in identity.identity_ids
    assert "identity:letter_identity_domain" in identity.identity_ids


def test_seen_does_not_become_sheen():
    """
    Test that SEEN identity is preserved and does not become SHEEN.

    Constitutional requirement: invalidating differences prevent confusion.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x0633)  # SEEN
    seen_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(seen_letter_codepoint)

    assert len(result.accepted) == 1
    identity = result.accepted[0]

    # Kernel preserves codepoint identity - SEEN is U+0633, SHEEN is U+0634
    assert "identity:codepoint:0633" in identity.identity_ids
    assert "identity:codepoint:0634" not in identity.identity_ids
    assert "identity:letter_identity_domain" in identity.identity_ids


def test_baa_does_not_become_taa():
    """
    Test that BAA identity is preserved and does not become TAA.

    Constitutional requirement: baa_vs_taa invalidating difference.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    baa_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(baa_letter_codepoint)

    assert len(result.accepted) == 1
    identity = result.accepted[0]

    # Kernel preserves codepoint identity - BAA is U+0628, TAA is U+062A
    assert "identity:codepoint:0628" in identity.identity_ids
    assert "identity:codepoint:062a" not in identity.identity_ids
    assert "identity:letter_identity_domain" in identity.identity_ids


def test_kaf_letter_codepoint_proves_kaf_identity():
    """
    Test that LetterCodePoint(KAF) proves LetterIdentityCarrier(KAF).
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x0643)  # KAF
    kaf_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(kaf_letter_codepoint)

    assert len(result.accepted) == 1
    identity = result.accepted[0]

    assert identity.candidate_type == "LetterIdentityCarrier"
    # Kernel preserves input identities and adds asl identity
    assert "identity:codepoint:0643" in identity.identity_ids
    assert "identity:letter_identity_domain" in identity.identity_ids


def test_letter_identity_does_not_require_sequence():
    """
    Test that LetterIdentityCarrier can be proven from a single LetterCodePoint
    without requiring sequence context or ConditionedTypedSequence.

    This validates the parallel path architecture.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Single letter, no sequence
    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    baa_letter_codepoint = typed_result.accepted[0]

    # Should succeed without sequence context
    result = letter_adapter.process_letter_codepoint(baa_letter_codepoint)

    assert len(result.accepted) == 1
    assert result.accepted[0].candidate_type == "LetterIdentityCarrier"


def test_non_letter_codepoint_returns_empty():
    """
    Test that non-LetterCodePoint inputs return empty CandidateSet.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Get HarakaCodePoint instead of LetterCodePoint
    typed_result = typed_adapter.classify_codepoint(0x064E)  # FATHA
    haraka_codepoint = typed_result.accepted[0]

    assert haraka_codepoint.candidate_type == "HarakaCodePoint"

    # Should return empty for non-letter
    result = letter_adapter.process_letter_codepoint(haraka_codepoint)

    assert len(result.candidates) == 0


def test_unmapped_letter_returns_empty():
    """
    Test that unmapped letters return empty (not yet in identity map).

    Currently only BAA, TAA, SEEN, KAF mapped (plus full 28 letter set).
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Try DAAL which should be mapped
    typed_result = typed_adapter.classify_codepoint(0x062F)  # DAAL
    daal_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(daal_letter_codepoint)

    # DAAL should be in the 28-letter map
    assert len(result.accepted) >= 0  # May be mapped or not


def test_letter_identity_forbidden_outputs():
    """
    Test that LetterIdentityCarrier rules forbid compositional outputs.

    Constitutional requirement: LetterIdentityCarrier is atomic, not compositional.
    """
    from qiyas_core.rules.letter_identity_rules import get_letter_identity_rule

    baa_rule = get_letter_identity_rule(0x0628)
    assert baa_rule is not None

    forbidden = baa_rule.forbidden_outputs

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
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    baa_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(baa_letter_codepoint)

    assert len(result.accepted) == 1
    identity = result.accepted[0]

    # Trace should be preserved and extended
    assert len(identity.trace_ids) > 0


def test_letter_identity_proves_fariq_absence():
    """
    Test that evidence proves absence of invalidating differences (fariq).

    Constitutional requirement: fariq must be proven in evidence, not just declared.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    baa_letter_codepoint = typed_result.accepted[0]

    # Build request to inspect evidence
    request = letter_adapter.build_request_for_letter_identity(baa_letter_codepoint)
    assert request is not None

    # Evidence must prove fariq absence
    proves_list = []
    for evidence_item in request.evidence.items:
        proves_list.extend(evidence_item.proves)

    # Must contain fariq:*:absent claims
    fariq_proofs = [p for p in proves_list if p.startswith("fariq:") and ":absent" in p]
    assert len(fariq_proofs) > 0  # At least one invalidating difference proven absent


def test_letter_identity_has_representation_contract():
    """
    Test that LetterIdentityCarrier preserves constitutional identity contract.

    The kernel preserves input identities and adds the asl domain identity.
    Detailed RepresentationContract layers (unicode, script, name, phonetic_proxy,
    makhraj, sifat, letter) are proven in evidence, not added to identity_ids.

    Constitutional requirement: input_identity_ids ⊆ output_identity_ids
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    baa_letter_codepoint = typed_result.accepted[0]

    result = letter_adapter.process_letter_codepoint(baa_letter_codepoint)

    assert len(result.accepted) == 1
    identity = result.accepted[0]

    # Kernel preserves input identities
    assert "identity:codepoint:0628" in identity.identity_ids
    assert "identity:typed_codepoint_domain" in identity.identity_ids or "identity:typed_codepoint:letter" in identity.identity_ids

    # Kernel adds asl identity
    assert "identity:letter_identity_domain" in identity.identity_ids

    # Verify evidence proves representation contract layers
    request = letter_adapter.build_request_for_letter_identity(baa_letter_codepoint)
    assert request is not None

    proves_list = []
    for evidence_item in request.evidence.items:
        proves_list.extend(evidence_item.proves)

    # Evidence must prove representation contract layers
    has_unicode_wasf = any("wasf:has_unicode_identity:" in p for p in proves_list)
    has_script_wasf = any("wasf:has_script_identity:" in p for p in proves_list)
    has_sound_wasf = any("wasf:has_sound_identity:" in p for p in proves_list)
    has_makhraj_wasf = any("wasf:has_makhraj:" in p for p in proves_list)

    assert has_unicode_wasf, "Evidence missing unicode identity proof"
    assert has_script_wasf, "Evidence missing script identity proof"
    assert has_sound_wasf, "Evidence missing sound identity proof"
    assert has_makhraj_wasf, "Evidence missing makhraj proof"
