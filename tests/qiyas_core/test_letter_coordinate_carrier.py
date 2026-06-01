"""
Tests for ArabicLetterCoordinateCarrier layer (Layer 2) — coordinate enrichment.

Required tests:
  - BAA/TAA/SEEN/KAF coordinate enrichment
  - Fariq (invalidating differences) checking
  - Layer 1 vs Layer 2 evidence separation
  - Abjad semantic_force=FORBIDDEN validation
  - Residual generation for unsupported letters
"""

import uuid
from qiyas_core.candidate import CandidateSet
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel, QiyasContext, QiyasRequest
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.letter_coordinate_adapter import ArabicLetterCoordinateAdapter
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.node import QiyasNodeRef
from qiyas_core.rules.letter_coordinate_rules import BAA_COORDINATE_RULE


def _prove_coordinate_from_codepoint(codepoint: int) -> CandidateSet:
    """
    Helper to process a codepoint through the constitutional path to Layer 2.

    Constitutional path:
      codepoint → TypedCodePointLayerAdapter → LetterCodePoint →
      LetterIdentityLayerAdapter → LetterIdentityCarrier →
      ArabicLetterCoordinateAdapter → ArabicLetterCoordinateCarrier
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Get LetterCodePoint from TypedCodePointLayerAdapter
    typed_result = typed_adapter.classify_codepoint(codepoint)
    if not typed_result.accepted:
        return typed_result

    letter_codepoint = typed_result.accepted[0]

    # Get LetterIdentityCarrier from LetterIdentityLayerAdapter
    identity_result = letter_adapter.process_letter_codepoint(letter_codepoint)
    if not identity_result.accepted:
        return identity_result

    letter_identity = identity_result.accepted[0]

    # Get ArabicLetterCoordinateCarrier from ArabicLetterCoordinateAdapter
    return coordinate_adapter.process_letter_identity(letter_identity)


# ---------------------------------------------------------------------------
# Contract-required tests - Coordinate enrichment for BAA/TAA/SEEN/KAF
# ---------------------------------------------------------------------------

def test_baa_coordinate_enrichment():
    """BAA gets enriched with phonetic coordinates."""
    result = _prove_coordinate_from_codepoint(0x0628)  # ب

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "ArabicLetterCoordinateCarrier"
    assert c.rank == EvidenceRank.FORM
    assert c.layer == "ArabicLetterCoordinateQiyas"
    assert "baa" in c.source_rule_id


def test_taa_coordinate_enrichment():
    """TAA gets enriched with phonetic coordinates."""
    result = _prove_coordinate_from_codepoint(0x062A)  # ت

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "ArabicLetterCoordinateCarrier"
    assert "taa" in c.source_rule_id


def test_seen_coordinate_enrichment():
    """SEEN gets enriched with phonetic coordinates."""
    result = _prove_coordinate_from_codepoint(0x0633)  # س

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "ArabicLetterCoordinateCarrier"
    assert "seen" in c.source_rule_id


def test_kaf_coordinate_enrichment():
    """KAF gets enriched with phonetic coordinates."""
    result = _prove_coordinate_from_codepoint(0x0643)  # ك

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "ArabicLetterCoordinateCarrier"
    assert "kaf" in c.source_rule_id


# ---------------------------------------------------------------------------
# Fariq (invalidating differences) tests - MOVED FROM LAYER 1
# ---------------------------------------------------------------------------

def test_baa_vs_meem_invalidating_difference():
    """
    Layer 2 test: BAA and MEEM differ by NASALITY_DIFF.

    When we prove BAA coordinate with fariq:baa_vs_meem:present in evidence,
    the kernel blocks it because the rule has baa_vs_meem in invalidating_differences.
    """
    kernel = QiyasKernel()

    # Create asl node (letter coordinate domain)
    asl = QiyasNodeRef(
        node_id="asl:letter_coordinate_domain:baa",
        node_type="LetterCoordinateDomain",
        identity_ids=("identity:letter_coordinate_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )

    # Create far node (LetterIdentityCarrier for BAA)
    far = QiyasNodeRef(
        node_id="far:letter_identity:baa:0628",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:codepoint:0628", "identity:letter:baa"),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    # Build proves with all required claims PLUS the invalidating fariq
    proves = (
        "asl:established",
        "far:determined",
        # Layer 1 identity wasf
        "wasf:has_letter_codepoint:evidenced",
        "wasf:has_unicode_identity:0628:evidenced",
        "wasf:has_script_identity:baa:evidenced",
        "wasf:has_latin_name:baa:evidenced",
        # Layer 2 coordinate wasf
        "wasf:has_sound_identity:VOICED_BILABIAL_STOP:evidenced",
        "wasf:has_makhraj:BILABIAL:evidenced",
        "wasf:has_voicing:VOICED:evidenced",
        "wasf:has_manner:STOP:evidenced",
        "wasf:has_emphasis:NON_EMPHATIC:evidenced",
        "wasf:has_abjad_coordinate:evidenced",
        # Layer 1 illah
        "illah:belongs_to_letter_identity_domain:verified",
        "illah:letter_identity_is:baa:verified",
        # Layer 2 illah
        "illah:belongs_to_letter_coordinate_domain:verified",
        # Wadi gates
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
        # The invalidating difference claim that blocks coordinate transfer
        "fariq:baa_vs_meem:present",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:baa_meem_test:{uuid.uuid4().hex[:8]}",
            source_layer="ArabicLetterCoordinateQiyas",
            proves=proves,
            rank=EvidenceRank.FORM,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=BAA_COORDINATE_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="ArabicLetterCoordinateQiyas"),
    )

    result = kernel.apply(request)

    # Must be blocked due to fariq:baa_vs_meem:present
    assert len(result.blocked) == 1
    assert any(r.residual_type == "blocking_fariq_present" for r in result.residuals)


# ---------------------------------------------------------------------------
# Layer separation tests
# ---------------------------------------------------------------------------

def test_layer_1_has_no_phonetic_identity_ids():
    """
    Layer 1 (LetterIdentityCarrier) must not have phonetic identity_ids.
    It only proves pure identity (codepoint, script, name, letter).
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)

    # Get BAA LetterIdentityCarrier (Layer 1)
    typed_result = typed_adapter.classify_codepoint(0x0628)
    letter_codepoint = typed_result.accepted[0]
    identity_result = letter_adapter.process_letter_codepoint(letter_codepoint)
    layer1_candidate = identity_result.accepted[0]

    # Layer 1 identity_ids must include pure identity only
    identity_ids = layer1_candidate.identity_ids

    # Must have these
    assert any("identity:codepoint:" in id for id in identity_ids)
    assert any("identity:script:" in id or "identity:letter:" in id for id in identity_ids)

    # Must NOT have phonetic coordinates
    assert not any("phonetic" in id for id in identity_ids)
    assert not any("makhraj" in id for id in identity_ids)
    assert not any("abjad" in id for id in identity_ids)


def test_layer_2_produces_coordinate_carrier():
    """
    Layer 2 (ArabicLetterCoordinateCarrier) enriches with coordinates.
    """
    result = _prove_coordinate_from_codepoint(0x0628)  # BAA
    layer2_candidate = result.accepted[0]

    # Must be coordinate carrier type
    assert layer2_candidate.candidate_type == "ArabicLetterCoordinateCarrier"
    assert layer2_candidate.layer == "ArabicLetterCoordinateQiyas"


# ---------------------------------------------------------------------------
# Abjad semantic_force tests
# ---------------------------------------------------------------------------

def test_abjad_has_semantic_force_forbidden():
    """Abjad coordinate must have semantic_force=FORBIDDEN."""
    from qiyas_core.abjad_system import get_abjad_coordinate

    baa_abjad = get_abjad_coordinate(0x0628)
    assert baa_abjad is not None
    assert baa_abjad.semantic_force == "FORBIDDEN"


def test_abjad_cannot_produce_meaning_candidate():
    """
    Abjad coordinates cannot be used to produce MeaningCandidate.
    Verified by checking that ArabicLetterCoordinateCarrier forbids MeaningCandidate.
    """
    from qiyas_core.rules.letter_coordinate_rules import BAA_COORDINATE_RULE

    assert "MeaningCandidate" in BAA_COORDINATE_RULE.forbidden_outputs


def test_abjad_cannot_produce_hukm_candidate():
    """
    Abjad coordinates cannot be used to produce HukmCandidate.
    """
    from qiyas_core.rules.letter_coordinate_rules import BAA_COORDINATE_RULE

    assert "HukmCandidate" in BAA_COORDINATE_RULE.forbidden_outputs


# ---------------------------------------------------------------------------
# Residual generation tests
# ---------------------------------------------------------------------------

def test_unsupported_letter_returns_residuals():
    """
    Letters without coordinate rules must return DEFERRED with residuals.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    letter_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Get ALEF LetterIdentityCarrier (not in coordinate rules yet)
    typed_result = typed_adapter.classify_codepoint(0x0627)  # ا
    letter_codepoint = typed_result.accepted[0]
    identity_result = letter_adapter.process_letter_codepoint(letter_codepoint)
    letter_identity = identity_result.accepted[0]

    # Try to enrich with coordinates
    coordinate_result = coordinate_adapter.process_letter_identity(letter_identity)

    # Must have residuals, not empty
    assert len(coordinate_result.residuals) > 0
    residual_types = [r.residual_type for r in coordinate_result.residuals]
    assert "letter_coordinate_not_implemented" in residual_types or "phonetic_profile_missing" in residual_types


# ---------------------------------------------------------------------------
# Forbidden output tests
# ---------------------------------------------------------------------------

def test_layer_2_forbids_slot_candidate():
    """
    ArabicLetterCoordinateCarrier layer forbids SlotCandidate.
    """
    from qiyas_core.rules.letter_coordinate_rules import BAA_COORDINATE_RULE

    assert "SlotCandidate" in BAA_COORDINATE_RULE.forbidden_outputs
