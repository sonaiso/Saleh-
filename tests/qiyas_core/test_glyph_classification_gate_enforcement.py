"""
Tests for Glyph Classification Gate Enforcement

Constitutional requirement: No phonetic coordinates before glyph classification.

Validates that letter_coordinate_adapter enforces glyph classification gate:
  - CORE_ARABIC_LETTER → allows coordinate enrichment
  - TATWEEL_GLYPH → blocks coordinate enrichment (no phonetic coordinates)
  - HAMZA_SEAT_GLYPH → defers to decomposition
  - WEAK_LETTER_GLYPH → defers to role disambiguation
  - COMPLEX_GLYPH → defers to decomposition

Constitutional Law:
  لا إحداثيات صوتية قبل تصنيف glyph
  لا phonetic coordinates لمن لا يسمح بها glyph
  لا hamza-seat بلا decomposition
  لا weak-letter بلا role disambiguation
  كل منع أو تأجيل = residual صريح مخصوص (specific explicit residual)
"""

import pytest

from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.letter_coordinate_adapter import ArabicLetterCoordinateAdapter
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.registries.glyph_classification_registry import (
    classify_glyph,
    GlyphClass,
)


@pytest.fixture
def kernel():
    """Create QiyasKernel instance."""
    return QiyasKernel()


@pytest.fixture
def typed_codepoint_adapter(kernel):
    """Create TypedCodePointLayerAdapter."""
    return TypedCodePointLayerAdapter(kernel=kernel)


@pytest.fixture
def letter_identity_adapter(kernel):
    """Create LetterIdentityLayerAdapter."""
    return LetterIdentityLayerAdapter(kernel=kernel)


@pytest.fixture
def letter_coordinate_adapter(kernel):
    """Create ArabicLetterCoordinateAdapter."""
    return ArabicLetterCoordinateAdapter(kernel=kernel)


# Test 1: CORE_ARABIC_LETTER (ب BAA) passes through
def test_core_arabic_letter_passes_glyph_gate(
    typed_codepoint_adapter, letter_identity_adapter, letter_coordinate_adapter
):
    """
    Test that CORE_ARABIC_LETTER (ب) passes glyph classification gate.

    Constitutional rule: Core letters with direct phonetic mapping
    should receive coordinate enrichment.
    """
    # ب U+0628 BAA
    codepoint = 0x0628

    # Verify glyph classification
    classification = classify_glyph(codepoint)
    assert classification.glyph_class == GlyphClass.CORE_ARABIC_LETTER
    assert classification.allows_phonetic_coordinates is True
    assert classification.requires_decomposition is False
    assert classification.requires_role_disambiguation is False

    # Layer 0: TypedCodePoint
    typed_result = typed_codepoint_adapter.classify_codepoint(codepoint)
    assert typed_result.accepted, "TypedCodePoint should succeed for BAA"
    typed_candidate = typed_result.accepted[0]
    assert typed_candidate.candidate_type == "LetterCodePoint"

    # Layer 1: LetterIdentityCarrier
    identity_result = letter_identity_adapter.process_letter_codepoint(typed_candidate)
    assert identity_result.accepted, "LetterIdentity should succeed for BAA"
    identity_candidate = identity_result.accepted[0]
    assert identity_candidate.candidate_type == "LetterIdentityCarrier"

    # Layer 2: ArabicLetterCoordinateCarrier
    # This should PASS the glyph gate since BAA is CORE_ARABIC_LETTER
    coordinate_result = letter_coordinate_adapter.process_letter_identity(identity_candidate)
    assert coordinate_result.accepted, "Coordinate enrichment should succeed for BAA"
    coordinate_candidate = coordinate_result.accepted[0]
    assert coordinate_candidate.candidate_type == "ArabicLetterCoordinateCarrier"


# Test 2: TATWEEL (ـ) blocks - no phonetic coordinates
def test_tatweel_blocks_at_glyph_gate(
    typed_codepoint_adapter, letter_identity_adapter, letter_coordinate_adapter
):
    """
    Test that TATWEEL (ـ) is blocked by glyph classification gate with specific residual.

    Constitutional rule: Tatweel has no phonetic coordinates (spacing only).
    لا phonetic coordinates لـ TATWEEL

    Expected residual_type: "glyph_has_no_phonetic_coordinates"
    """
    # ـ U+0640 TATWEEL
    codepoint = 0x0640

    # Verify glyph classification
    classification = classify_glyph(codepoint)
    assert classification.glyph_class == GlyphClass.TATWEEL_GLYPH
    assert classification.allows_phonetic_coordinates is False  # BLOCKED
    assert classification.requires_decomposition is False
    assert classification.requires_role_disambiguation is False

    # Layer 0: TypedCodePoint
    typed_result = typed_codepoint_adapter.classify_codepoint(codepoint)
    if not typed_result.accepted:
        pytest.skip("Tatweel not yet classified at TypedCodePoint layer")

    typed_candidate = typed_result.accepted[0]
    if typed_candidate.candidate_type != "LetterCodePoint":
        pytest.skip("Tatweel not classified as LetterCodePoint")

    # Layer 1: LetterIdentityCarrier (might succeed if rule exists)
    identity_result = letter_identity_adapter.process_letter_codepoint(typed_candidate)
    if not identity_result.accepted:
        pytest.skip("Tatweel has no LetterIdentity - glyph gate not reached")

    identity_candidate = identity_result.accepted[0]

    # Layer 2: ArabicLetterCoordinateCarrier
    # This should be BLOCKED by glyph gate with specific residual
    result = letter_coordinate_adapter.process_letter_identity(identity_candidate)

    # Expected: No accepted candidates, specific residual emitted
    assert not result.accepted, "Tatweel should be blocked at glyph classification gate"
    assert result.residuals, "Tatweel block must emit residual"
    assert len(result.residuals) == 1

    residual = result.residuals[0]
    assert residual.residual_type == "glyph_has_no_phonetic_coordinates"
    assert residual.effect.name == "BLOCK"
    assert residual.severity.name == "BLOCKER"


# Test 3: HAMZA_SEAT_GLYPH (أ) defers to decomposition
def test_hamza_seat_defers_at_glyph_gate(
    typed_codepoint_adapter, letter_identity_adapter, letter_coordinate_adapter
):
    """
    Test that HAMZA_SEAT_GLYPH (أ) is deferred by glyph classification gate with specific residual.

    Constitutional rule: Hamza seats require decomposition before coordinates.
    لا hamza-seat بلا decomposition

    Expected residual_type: "glyph_decomposition_required"
    """
    # أ U+0623 ALIF WITH HAMZA ABOVE
    codepoint = 0x0623

    # Verify glyph classification
    classification = classify_glyph(codepoint)
    assert classification.glyph_class == GlyphClass.HAMZA_SEAT_GLYPH
    assert classification.requires_decomposition is True  # DEFERRED
    assert classification.allows_phonetic_coordinates is True  # After decomposition

    # Layer 0: TypedCodePoint
    typed_result = typed_codepoint_adapter.classify_codepoint(codepoint)
    if not typed_result.accepted:
        pytest.skip("Hamza seat not yet classified at TypedCodePoint layer")

    typed_candidate = typed_result.accepted[0]
    if typed_candidate.candidate_type != "LetterCodePoint":
        pytest.skip("Hamza seat not classified as LetterCodePoint")

    # Layer 1: LetterIdentityCarrier
    identity_result = letter_identity_adapter.process_letter_codepoint(typed_candidate)
    assert identity_result.accepted, (
        "Hamza seat must prove LetterIdentity (Arabic names in rules must match registry)"
    )

    identity_candidate = identity_result.accepted[0]

    # Layer 2: ArabicLetterCoordinateCarrier
    # Should be DEFERRED by glyph gate with specific residual
    result = letter_coordinate_adapter.process_letter_identity(identity_candidate)

    # Expected: No accepted candidates, specific residual emitted
    assert not result.accepted, "Hamza seat should be deferred at glyph classification gate"
    assert result.residuals, "Hamza seat defer must emit residual"
    assert len(result.residuals) == 1

    residual = result.residuals[0]
    assert residual.residual_type == "glyph_decomposition_required"
    assert residual.effect.name == "DEFER"
    assert residual.severity.name == "WARNING"


# Test 4: WEAK_LETTER_GLYPH (و) defers to role disambiguation
def test_weak_letter_defers_at_glyph_gate(
    typed_codepoint_adapter, letter_identity_adapter, letter_coordinate_adapter
):
    """
    Test that WEAK_LETTER_GLYPH (و) is deferred by glyph classification gate with specific residual.

    Constitutional rule: Weak letters need role disambiguation before coordinates.
    لا weak-letter بلا role disambiguation

    Expected residual_type: "glyph_role_disambiguation_required"
    """
    # و U+0648 WAW
    codepoint = 0x0648

    # Verify glyph classification
    classification = classify_glyph(codepoint)
    assert classification.glyph_class == GlyphClass.WEAK_LETTER_GLYPH
    assert classification.requires_role_disambiguation is True  # DEFERRED
    assert classification.allows_phonetic_coordinates is True  # Context-dependent

    # Layer 0: TypedCodePoint
    typed_result = typed_codepoint_adapter.classify_codepoint(codepoint)
    if not typed_result.accepted:
        pytest.skip("Waw not yet classified at TypedCodePoint layer")

    typed_candidate = typed_result.accepted[0]
    if typed_candidate.candidate_type != "LetterCodePoint":
        pytest.skip("Waw not classified as LetterCodePoint")

    # Layer 1: LetterIdentityCarrier
    identity_result = letter_identity_adapter.process_letter_codepoint(typed_candidate)
    if not identity_result.accepted:
        pytest.skip("Waw has no LetterIdentity - glyph gate not reached")

    identity_candidate = identity_result.accepted[0]

    # Layer 2: ArabicLetterCoordinateCarrier
    # Should be DEFERRED by glyph gate with specific residual
    result = letter_coordinate_adapter.process_letter_identity(identity_candidate)

    # Expected: No accepted candidates, specific residual emitted
    assert not result.accepted, "Weak letter should be deferred at glyph classification gate"
    assert result.residuals, "Weak letter defer must emit residual"
    assert len(result.residuals) == 1

    residual = result.residuals[0]
    assert residual.residual_type == "glyph_role_disambiguation_required"
    assert residual.effect.name == "DEFER"
    assert residual.severity.name == "WARNING"


# Test 5: COMPLEX_GLYPH (آ) defers to decomposition
def test_complex_glyph_defers_at_glyph_gate(
    typed_codepoint_adapter, letter_identity_adapter, letter_coordinate_adapter
):
    """
    Test that COMPLEX_GLYPH (آ) is deferred by glyph classification gate with specific residual.

    Constitutional rule: Complex glyphs require decomposition before coordinates.
    آ = alif + madda (madda = hamza + alif) → needs decomposition

    Expected residual_type: "glyph_decomposition_required"
    """
    # آ U+0622 ALIF WITH MADDA ABOVE
    codepoint = 0x0622

    # Verify glyph classification
    classification = classify_glyph(codepoint)
    assert classification.glyph_class == GlyphClass.COMPLEX_GLYPH
    assert classification.requires_decomposition is True  # DEFERRED
    assert classification.allows_phonetic_coordinates is True  # After decomposition

    # Layer 0: TypedCodePoint
    typed_result = typed_codepoint_adapter.classify_codepoint(codepoint)
    if not typed_result.accepted:
        pytest.skip("Complex glyph not yet classified at TypedCodePoint layer")

    typed_candidate = typed_result.accepted[0]
    if typed_candidate.candidate_type != "LetterCodePoint":
        pytest.skip("Complex glyph not classified as LetterCodePoint")

    # Layer 1: LetterIdentityCarrier
    identity_result = letter_identity_adapter.process_letter_codepoint(typed_candidate)
    assert identity_result.accepted, (
        "Complex glyph must prove LetterIdentity (Arabic names in rules must match registry)"
    )

    identity_candidate = identity_result.accepted[0]

    # Layer 2: ArabicLetterCoordinateCarrier
    # Should be DEFERRED by glyph gate with specific residual
    result = letter_coordinate_adapter.process_letter_identity(identity_candidate)

    # Expected: No accepted candidates, specific residual emitted
    assert not result.accepted, "Complex glyph should be deferred at glyph classification gate"
    assert result.residuals, "Complex glyph defer must emit residual"
    assert len(result.residuals) == 1

    residual = result.residuals[0]
    assert residual.residual_type == "glyph_decomposition_required"
    assert residual.effect.name == "DEFER"
    assert residual.severity.name == "WARNING"


# Test 6: Ensure no local glyph classification duplication
def test_no_local_glyph_classification_in_adapter():
    """
    Test that letter_coordinate_adapter does NOT contain local glyph classification.

    Constitutional requirement: Single source of truth = glyph_classification_registry
    Forbidden: Local GLYPH_CLASS dicts or classification logic in adapter
    """
    import inspect
    from qiyas_core import letter_coordinate_adapter

    source = inspect.getsource(letter_coordinate_adapter)

    # Should import classify_glyph from registry
    assert "from .registries.glyph_classification_registry import classify_glyph" in source

    # Should NOT contain local glyph classification sets/dicts
    # (Allow comments/strings but no actual data structures)
    forbidden_patterns = [
        "CORE_ARABIC_LETTERS =",
        "HAMZA_SEAT_GLYPHS =",
        "WEAK_LETTER_GLYPHS =",
        "TATWEEL_GLYPH =",
        "COMPLEX_GLYPHS =",
    ]

    for pattern in forbidden_patterns:
        assert pattern not in source, f"Adapter must NOT contain local glyph classification: {pattern}"
