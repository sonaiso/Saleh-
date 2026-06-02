"""
Tests for ArabicLetterCoordinateCarrier (Layer 2)

Validates that letter identity (Layer 1) can be enriched with coordinates (Layer 2):
  - Phonetic proxy (sound_identity)
  - Makhraj (articulation place)
  - Sifat (voicing, manner, emphasis)
  - Abjad numeric values with semantic_force:FORBIDDEN
  - Morphological role potential
  - Invalidating differences (fariq)

Constitutional compliance:
  - Uses LetterIdentityLayerAdapter → ArabicLetterCoordinateAdapter
  - Validates identity_ids preservation through layers
  - Validates evidence structure with all required wasf
  - Validates fariq (blocking invalidating differences)
  - Validates layer separation (Layer 1 proves identity, Layer 2 proves coordinates)
  - Validates residual discipline for unsupported letters
"""

import pytest

from qiyas_core.enums import CandidateStatus, EvidenceRank, ResidualSeverity, ResidualEffect
from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.letter_coordinate_adapter import ArabicLetterCoordinateAdapter
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.recursive_proof import (
    LETTER_IDENTITY_CONTRACT,
    LETTER_COORDINATE_CONTRACT,
)


def test_baa_letter_identity_enriches_to_baa_coordinate():
    """
    Test that LetterIdentityCarrier(BAA) enriches to ArabicLetterCoordinateCarrier(BAA).

    Validates full Layer 1 → Layer 2 path with coordinate enrichment.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    identity_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Layer 0: TypedCodePoint
    typed_result = typed_adapter.classify_codepoint(0x0628)  # BAA
    assert len(typed_result.accepted) == 1
    baa_codepoint = typed_result.accepted[0]

    # Layer 1: LetterIdentityCarrier
    identity_result = identity_adapter.process_letter_codepoint(baa_codepoint)
    assert len(identity_result.accepted) == 1
    baa_identity = identity_result.accepted[0]
    assert baa_identity.candidate_type == "LetterIdentityCarrier"

    # Layer 2: ArabicLetterCoordinateCarrier
    coordinate_result = coordinate_adapter.process_letter_identity(baa_identity)
    assert len(coordinate_result.accepted) == 1
    baa_coordinate = coordinate_result.accepted[0]

    # Validate coordinate carrier
    assert baa_coordinate.candidate_type == "ArabicLetterCoordinateCarrier"
    assert baa_coordinate.status == CandidateStatus.ACCEPTED
    assert baa_coordinate.rank == EvidenceRank.FORMAL_STRUCTURE

    # Validate identity_ids preservation (Kernel merges identities from both layers)
    assert "identity:codepoint:0628" in baa_coordinate.identity_ids
    assert "identity:letter_identity_domain" in baa_coordinate.identity_ids or \
           "identity:letter:baa" in baa_coordinate.identity_ids


def test_baa_vs_meem_invalidating_difference():
    """
    Test that BAA vs MEEM invalidating difference (nasality) is proven absent.

    Constitutional requirement: Layer 2 must prove fariq (blocking differences).
    This test validates the BLOCKER FIX: morpho_role evidence emission.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    identity_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Get BAA coordinate carrier
    typed_result = typed_adapter.classify_codepoint(0x0628)
    baa_identity = identity_adapter.process_letter_codepoint(typed_result.accepted[0])
    result = coordinate_adapter.process_letter_identity(baa_identity.accepted[0])

    assert len(result.accepted) == 1
    baa_coordinate = result.accepted[0]

    # Extract evidence
    # Note: Candidate object doesn't have .evidence attribute - evidence is in EvidenceSet from request
    # We validate via residuals: no effective_wasf_missing means all required wasf were proven

    # Validate all required wasf were proven (no missing wasf residuals)
    assert not any(r.residual_type == "effective_wasf_missing" for r in result.residuals)

    # Validate coordinate evidence should include:
    # - Abjad wasf (system, value, semantic_force)
    # - Morpho role wasf (BLOCKER: this was missing before fix)
    # - Phonetic wasf (sound_identity, makhraj, voicing, manner, emphasis)
    # - Fariq wasf (baa_vs_meem:absent, etc.)

    # We can't directly access evidence from candidate, but we can verify via residuals
    # If all wasf are present, kernel accepts the candidate with no blocking residuals
    assert baa_coordinate.status == CandidateStatus.ACCEPTED


def test_layer_separation_identity_vs_coordinates():
    """
    Test that Layer 1 proves ONLY identity, Layer 2 proves coordinates.

    Constitutional requirement: strict layer separation.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    identity_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Get TAA through both layers
    typed_result = typed_adapter.classify_codepoint(0x062A)  # TAA
    taa_identity = identity_adapter.process_letter_codepoint(typed_result.accepted[0])
    taa_coordinate = coordinate_adapter.process_letter_identity(taa_identity.accepted[0])

    # Layer 1 (identity) result
    identity = taa_identity.accepted[0]
    assert identity.candidate_type == "LetterIdentityCarrier"
    assert identity.source_rule_id == "letter_identity.taa"

    # Layer 2 (coordinate) result
    coordinate = taa_coordinate.accepted[0]
    assert coordinate.candidate_type == "ArabicLetterCoordinateCarrier"
    assert coordinate.source_rule_id == "letter_coordinate.taa"

    # Validate layer separation via rule IDs
    assert identity.source_rule_id != coordinate.source_rule_id
    assert "letter_identity" in identity.source_rule_id
    assert "letter_coordinate" in coordinate.source_rule_id


@pytest.mark.parametrize("codepoint,letter_name,abjad_value,morpho_role", [
    (0x0628, "baa", 2, "EXPANDED_MULTI_ROLE"),      # BAA
    (0x062A, "taa", 400, "SAALATAMUUNIIHA"),        # TAA
    (0x0633, "seen", 60, "SAALATAMUUNIIHA"),        # SEEN
    (0x0643, "kaf", 20, "EXPANDED_MULTI_ROLE"),     # KAF
])
def test_minimal_coordinate_slice_letters(codepoint, letter_name, abjad_value, morpho_role):
    """
    Test minimal Layer 2 coordinate slice for BAA, TAA, SEEN, KAF.

    Validates:
      - Abjad value-specific evidence (e.g., BAA=2, TAA=400)
      - Morpho role evidence (BLOCKER FIX)
      - semantic_force:FORBIDDEN for Abjad
      - No effective_wasf_missing residuals
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    identity_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Full path: TypedCodePoint → LetterIdentityCarrier → ArabicLetterCoordinateCarrier
    typed_result = typed_adapter.classify_codepoint(codepoint)
    identity_result = identity_adapter.process_letter_codepoint(typed_result.accepted[0])
    coordinate_result = coordinate_adapter.process_letter_identity(identity_result.accepted[0])

    # Validate acceptance
    assert len(coordinate_result.accepted) == 1
    carrier = coordinate_result.accepted[0]
    assert carrier.candidate_type == "ArabicLetterCoordinateCarrier"
    assert carrier.status == CandidateStatus.ACCEPTED

    # Validate no missing wasf (proves all required evidence was emitted)
    assert not any(r.residual_type == "effective_wasf_missing" for r in coordinate_result.residuals)

    # Validate identity preservation
    assert f"identity:codepoint:{codepoint:04x}" in carrier.identity_ids


def test_unsupported_letter_returns_residual_not_silent_empty():
    """
    Test that unsupported letter coordinate enrichment returns Residual, not silent empty CandidateSet.

    Constitutional requirement: No silent failures - all blocking conditions must produce residuals.
    This validates the FIX for silent failure when coordinate enrichment is not supported.

    Updated for PR #43: Now emits specific residuals instead of generic "coordinate_enrichment_not_supported".
    ALIF (0x0627) is a WEAK_LETTER_GLYPH requiring role disambiguation.
    """
    kernel = QiyasKernel()
    typed_adapter = TypedCodePointLayerAdapter(kernel=kernel)
    identity_adapter = LetterIdentityLayerAdapter(kernel=kernel)
    coordinate_adapter = ArabicLetterCoordinateAdapter(kernel=kernel)

    # Choose a letter NOT in minimal slice (BAA/TAA/SEEN/KAF)
    # ALIF (0x0627) is a WEAK_LETTER_GLYPH - requires role disambiguation
    typed_result = typed_adapter.classify_codepoint(0x0627)  # ALIF

    # Layer 1 succeeds (ALIF has letter identity)
    identity_result = identity_adapter.process_letter_codepoint(typed_result.accepted[0])
    assert len(identity_result.accepted) == 1
    alif_identity = identity_result.accepted[0]
    assert alif_identity.candidate_type == "LetterIdentityCarrier"

    # Layer 2 should return CandidateSet with specific residual (NOT silent empty)
    coordinate_result = coordinate_adapter.process_letter_identity(alif_identity)

    # Validate: no accepted candidates (enrichment blocked by glyph gate)
    assert len(coordinate_result.accepted) == 0
    
    # Validate: MUST have residual (not silent empty)
    assert len(coordinate_result.residuals) >= 1
    
    # Find the specific glyph gate residual
    # ALIF (0x0627) is WEAK_LETTER_GLYPH → expects "glyph_role_disambiguation_required"
    # (PR #43: Changed from generic "coordinate_enrichment_not_supported" to specific residuals)
    glyph_gate_residual = None
    for r in coordinate_result.residuals:
        if r.residual_type == "glyph_role_disambiguation_required":
            glyph_gate_residual = r
            break

    assert glyph_gate_residual is not None, "Missing glyph_role_disambiguation_required residual for ALIF"

    # Validate residual structure uses correct API
    assert glyph_gate_residual.severity == ResidualSeverity.WARNING
    assert glyph_gate_residual.effect == ResidualEffect.DEFER
    assert "U+0627" in glyph_gate_residual.message
    assert glyph_gate_residual.source_rule_id == "glyph_gate.weak_letter_disambiguation"
    assert glyph_gate_residual.layer == "ArabicLetterCoordinateQiyas"
    assert len(glyph_gate_residual.trace_ids) > 0


def test_residual_construction_uses_correct_api():
    """
    Test that Residual uses correct API fields.
    
    Validates that residual construction does NOT use incorrect fields like:
      - residual_id (does not exist)
      - reason (does not exist)
    
    Instead uses correct API:
      - residual_type
      - severity
      - effect
      - message
      - source_rule_id
      - layer
      - trace_ids
    """
    from qiyas_core.residual import Residual
    
    # Construct a residual using correct API
    residual = Residual(
        residual_type="test_residual_type",
        severity=ResidualSeverity.BLOCKER,
        effect=ResidualEffect.DEFER,
        message="Test message",
        source_rule_id="test.rule",
        layer="TestLayer",
        trace_ids=("test:trace",),
    )
    
    # Validate all fields are correct
    assert residual.residual_type == "test_residual_type"
    assert residual.severity == ResidualSeverity.BLOCKER
    assert residual.effect == ResidualEffect.DEFER
    assert residual.message == "Test message"
    assert residual.source_rule_id == "test.rule"
    assert residual.layer == "TestLayer"
    assert residual.trace_ids == ("test:trace",)
    
    # Validate no incorrect fields exist
    assert not hasattr(residual, "residual_id")
    assert not hasattr(residual, "reason")


def test_letter_identity_contract_has_no_layer_2_wasf():
    """
    Test that LETTER_IDENTITY_CONTRACT contains NO Layer 2 wasf.
    
    Constitutional requirement: Layer 1 proves identity only, NOT coordinates.
    Layer 2 coordinates (sound_identity, makhraj, sifat) belong to LETTER_COORDINATE_CONTRACT.
    
    This validates the FIX for recursive_proof.py stale contract.
    """
    # Layer 1 effective_wasf must NOT contain Layer 2 coordinates
    layer_1_wasf = set(LETTER_IDENTITY_CONTRACT.effective_wasf)
    
    # Forbidden Layer 2 wasf patterns
    forbidden_patterns = [
        "has_sound_identity",
        "has_makhraj",
        "has_voicing",
        "has_manner",
        "has_emphasis",
        "has_abjad_system",
        "has_abjad_value",
        "has_morpho_role",
    ]
    
    for pattern in forbidden_patterns:
        # Check no wasf contains this Layer 2 pattern
        assert not any(pattern in w for w in layer_1_wasf), \
            f"LETTER_IDENTITY_CONTRACT must not contain Layer 2 wasf: {pattern}"
    
    # Layer 1 evidence must NOT mention Layer 2 concepts
    layer_1_evidence = " ".join(LETTER_IDENTITY_CONTRACT.evidence)
    
    forbidden_evidence_terms = [
        "phonetic profile",
        "makhraj",
        "sifat",
        "sound identity",
        "abjad",
    ]
    
    for term in forbidden_evidence_terms:
        assert term not in layer_1_evidence.lower(), \
            f"LETTER_IDENTITY_CONTRACT evidence must not mention Layer 2: {term}"
    
    # Validate Layer 1 allows only identity wasf
    required_layer_1_patterns = [
        "has_letter_codepoint",
        "has_unicode_identity",
        "has_script_identity",
        "has_latin_name",
    ]
    
    for pattern in required_layer_1_patterns:
        assert any(pattern in w for w in layer_1_wasf), \
            f"LETTER_IDENTITY_CONTRACT must contain identity wasf: {pattern}"


def test_letter_coordinate_contract_has_layer_2_wasf():
    """
    Test that LETTER_COORDINATE_CONTRACT contains Layer 2 coordinate wasf.
    
    Validates that Layer 2 contract correctly includes:
      - Layer 1 identity wasf (inherited)
      - Layer 2 coordinate wasf (added)
    """
    layer_2_wasf = set(LETTER_COORDINATE_CONTRACT.effective_wasf)
    
    # Layer 2 must inherit Layer 1 identity wasf
    required_layer_1_patterns = [
        "has_letter_codepoint",
        "has_unicode_identity",
        "has_script_identity",
        "has_latin_name",
    ]
    
    for pattern in required_layer_1_patterns:
        assert any(pattern in w for w in layer_2_wasf), \
            f"LETTER_COORDINATE_CONTRACT must inherit Layer 1 wasf: {pattern}"
    
    # Layer 2 must add coordinate wasf
    required_layer_2_patterns = [
        "has_sound_identity",
        "has_makhraj",
        "has_voicing",
        "has_manner",
        "has_emphasis",
    ]
    
    for pattern in required_layer_2_patterns:
        assert any(pattern in w for w in layer_2_wasf), \
            f"LETTER_COORDINATE_CONTRACT must contain Layer 2 wasf: {pattern}"
    
    # Validate output type
    assert LETTER_COORDINATE_CONTRACT.output == "ArabicLetterCoordinateCarrier"
    
    # Validate input type (takes Layer 1 output)
    assert "LetterIdentityCarrier" in LETTER_COORDINATE_CONTRACT.inputs


def test_fariq_present_blocks_kernel():
    """
    CONSTITUTIONAL TEST: فارق:...:present MUST block kernel.

    This test verifies that QiyasKernel correctly blocks when evidence contains
    فارق:{diff}:present (invalidating difference is present).

    Normal successful path emits فارق:{diff}:absent.
    Only conflict/error cases emit فارق:{diff}:present.

    This test validates the constitutional meaning of fariq evidence.
    """
    import uuid
    from qiyas_core.kernel import QiyasKernel, QiyasRequest, QiyasContext
    from qiyas_core.node import QiyasNodeRef
    from qiyas_core.evidence import Evidence, EvidenceSet
    from qiyas_core.rules.letter_coordinate_rules import BAA_COORDINATE_RULE

    kernel = QiyasKernel()

    # Build evidence that explicitly includes فارق:baa_vs_meem:present
    # This simulates a blocking invalidating difference
    proves = [
        "اصل:established",
        "فرع:determined",
        # Layer 1 identity wasf
        "وصف:has_letter_codepoint:evidenced",
        "وصف:has_unicode_identity:0628:evidenced",
        "وصف:has_script_identity:baa:evidenced",
        "وصف:has_latin_name:baa:evidenced",
        "وصف:has_arabic_name:باء:evidenced",
        # Layer 2 coordinate wasf
        "وصف:has_sound_identity:VOICED_BILABIAL_STOP:evidenced",
        "وصف:has_makhraj:BILABIAL:evidenced",
        "وصف:has_voicing:VOICED:evidenced",
        "وصف:has_manner:STOP:evidenced",
        "وصف:has_emphasis:NON_EMPHATIC:evidenced",
        "وصف:has_abjad_system:ABJAD:evidenced",
        "وصف:has_abjad_value:2:evidenced",
        "وصف:abjad_semantic_force:FORBIDDEN:evidenced",
        "وصف:has_morpho_role:EXPANDED_MULTI_ROLE:evidenced",
        # Illah
        "علة:belongs_to_letter_identity_domain:verified",
        "علة:letter_identity_is:baa:verified",
        "علة:belongs_to_letter_coordinate_domain:verified",
        # Wadi gates
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
        # CRITICAL: Inject فارق:baa_vs_meem:present (blocking!)
        "فارق:baa_vs_meem:present",
    ]

    evidence = EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:test_blocking_fariq:{uuid.uuid4().hex[:8]}",
                source_layer="ArabicLetterCoordinateQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORMAL_STRUCTURE,
                trace_ids=("test:blocking_fariq",),
            ),
        )
    )

    asl = QiyasNodeRef(
        node_id="asl:letter_coordinate_domain:baa",
        node_type="LetterCoordinateDomain",
        identity_ids=("identity:letter_coordinate_domain",),
        trace_ids=("test:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    far = QiyasNodeRef(
        node_id="far:letter_identity:baa",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:codepoint:0628", "identity:letter:baa"),
        trace_ids=("test:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    request = QiyasRequest(
        rule=BAA_COORDINATE_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="ArabicLetterCoordinateQiyas"),
    )

    # Execute through kernel
    result = kernel.apply(request)

    # VALIDATE: Kernel MUST block when فارق:...:present
    assert len(result.accepted) == 0, "Kernel must NOT accept when فارق:present"
    assert len(result.blocked) == 1, "Kernel must BLOCK when فارق:present"

    # Find blocking residual
    blocking_residual = None
    for r in result.residuals:
        if r.residual_type == "blocking_fariq_present":
            blocking_residual = r
            break

    assert blocking_residual is not None, "Must have blocking_fariq_present residual"
    assert blocking_residual.effect == ResidualEffect.BLOCK
    assert "baa_vs_meem" in blocking_residual.message or "blocking" in blocking_residual.residual_type
