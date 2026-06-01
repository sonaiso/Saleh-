"""
Tests for ForbiddenOutputRegistry — Gap #12 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Required tests (from contract):
  test_letter_identity_forbids_weight
  test_haraka_function_forbids_case_effect
  test_slot_forbids_meaning
"""

from qiyas_core.forbidden_outputs import (
    CONSTITUTIONAL_BASE,
    FORBIDDEN_LETTER_IDENTITY,
    FORBIDDEN_HARAKA_FUNCTION,
    FORBIDDEN_POSITION,
    FORBIDDEN_SLOT,
    FORBIDDEN_SYLLABLE,
    LAYER_FORBIDDEN_OUTPUTS,
    get_forbidden_outputs,
)


# ---------------------------------------------------------------------------
# Constitutional base invariant
# ---------------------------------------------------------------------------

def test_constitutional_base_contains_required_triple():
    """Every layer's forbidden_outputs must include the constitutional triple."""
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    assert required.issubset(set(CONSTITUTIONAL_BASE))


def test_all_layers_include_constitutional_base():
    """Every layer in the registry includes the constitutional triple."""
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    for layer, outputs in LAYER_FORBIDDEN_OUTPUTS.items():
        assert required.issubset(set(outputs)), (
            f"Layer {layer!r} missing constitutional forbidden outputs"
        )


# ---------------------------------------------------------------------------
# Contract-required tests
# ---------------------------------------------------------------------------

def test_letter_identity_forbids_weight():
    """Contract test: LetterIdentityCarrier layer forbids WeightCandidate."""
    assert "WeightCandidate" in FORBIDDEN_LETTER_IDENTITY


def test_haraka_function_forbids_case_effect():
    """Contract test: HarakaFunctionCarrier layer forbids CaseEffect."""
    assert "CaseEffect" in FORBIDDEN_HARAKA_FUNCTION
    assert "Irab" in FORBIDDEN_HARAKA_FUNCTION


def test_slot_forbids_meaning():
    """Contract test: SlotCandidate layer forbids MeaningCandidate."""
    assert "MeaningCandidate" in FORBIDDEN_SLOT


# ---------------------------------------------------------------------------
# Additional registry tests
# ---------------------------------------------------------------------------

def test_letter_identity_forbids_root():
    """LetterIdentityCarrier must forbid RootCandidate."""
    assert "RootCandidate" in FORBIDDEN_LETTER_IDENTITY


def test_haraka_function_forbids_syllable():
    """HarakaFunctionCarrier must forbid SyllableCandidate."""
    assert "SyllableCandidate" in FORBIDDEN_HARAKA_FUNCTION


def test_slot_forbids_syllable():
    """SlotCandidate must forbid SyllableCandidate (adjacency not yet established)."""
    assert "SyllableCandidate" in FORBIDDEN_SLOT


def test_position_forbids_case_effect():
    """PositionCarrier must forbid CaseEffect."""
    assert "CaseEffect" in FORBIDDEN_POSITION


def test_get_forbidden_outputs_returns_layer_specific():
    """get_forbidden_outputs returns correct tuple for known layers."""
    assert get_forbidden_outputs("LetterIdentityQiyas") is FORBIDDEN_LETTER_IDENTITY
    assert get_forbidden_outputs("HarakaFunctionQiyas") is FORBIDDEN_HARAKA_FUNCTION
    assert get_forbidden_outputs("PositionQiyas") is FORBIDDEN_POSITION
    assert get_forbidden_outputs("SlotQiyas") is FORBIDDEN_SLOT


def test_get_forbidden_outputs_defaults_to_constitutional_base():
    """Unknown layer returns the constitutional base tuple."""
    result = get_forbidden_outputs("UnknownLayer")
    assert result is CONSTITUTIONAL_BASE
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    assert required.issubset(set(result))


def test_syllable_layer_registered():
    """SyllableQiyas is registered in the forbidden outputs registry."""
    assert "SyllableQiyas" in LAYER_FORBIDDEN_OUTPUTS
    assert "MeaningCandidate" in LAYER_FORBIDDEN_OUTPUTS["SyllableQiyas"]
