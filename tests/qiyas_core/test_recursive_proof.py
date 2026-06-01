"""
Tests for RecursiveProofContract — Gap #11 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Verifies that every Phase-1 layer has a valid RecursiveProofContract instance
that satisfies all constitutional invariants.
"""

from qiyas_core.recursive_proof import (
    RecursiveProofContract,
    PHASE1_CONTRACTS,
    TYPED_CODEPOINT_CONTRACT,
    LETTER_IDENTITY_CONTRACT,
    HARAKA_FUNCTION_CONTRACT,
    POSITION_CONTRACT,
    SLOT_CONTRACT,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _check_contract(contract: RecursiveProofContract) -> None:
    violations = contract.validate()
    assert violations == [], (
        f"Contract violations in {contract.layer_name!r}:\n"
        + "\n".join(f"  - {v}" for v in violations)
    )


# ---------------------------------------------------------------------------
# Individual contract validity tests
# ---------------------------------------------------------------------------

def test_typed_codepoint_contract_valid():
    _check_contract(TYPED_CODEPOINT_CONTRACT)


def test_letter_identity_contract_valid():
    _check_contract(LETTER_IDENTITY_CONTRACT)


def test_haraka_function_contract_valid():
    _check_contract(HARAKA_FUNCTION_CONTRACT)


def test_position_contract_valid():
    _check_contract(POSITION_CONTRACT)


def test_slot_contract_valid():
    _check_contract(SLOT_CONTRACT)


# ---------------------------------------------------------------------------
# Phase-1 contract set tests
# ---------------------------------------------------------------------------

def test_phase1_has_five_contracts():
    """Phase 1 must define exactly five contracts."""
    assert len(PHASE1_CONTRACTS) == 5


def test_all_phase1_contracts_valid():
    """All Phase-1 contracts must pass validate()."""
    for contract in PHASE1_CONTRACTS:
        _check_contract(contract)


def test_all_phase1_contracts_have_distinct_layers():
    """Each contract must have a unique layer_name."""
    names = [c.layer_name for c in PHASE1_CONTRACTS]
    assert len(names) == len(set(names)), "Duplicate layer names in PHASE1_CONTRACTS"


def test_all_phase1_contracts_have_constitutional_forbidden_outputs():
    """Every contract must include the constitutional triple in forbidden_outputs."""
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    for c in PHASE1_CONTRACTS:
        assert required.issubset(set(c.forbidden_outputs)), (
            f"[{c.layer_name}] Missing constitutional forbidden outputs"
        )


def test_all_phase1_contracts_have_inputs():
    """Every contract must list at least one input type."""
    for c in PHASE1_CONTRACTS:
        assert len(c.inputs) > 0, f"[{c.layer_name}] inputs must not be empty"


def test_all_phase1_contracts_have_outputs():
    """Every contract must declare an output type."""
    for c in PHASE1_CONTRACTS:
        assert c.output, f"[{c.layer_name}] output must not be empty"


def test_all_phase1_contracts_have_identity_preservation():
    """Every contract must declare at least one identity to preserve."""
    for c in PHASE1_CONTRACTS:
        assert len(c.identity_preservation) > 0, (
            f"[{c.layer_name}] identity_preservation must not be empty"
        )


def test_recursive_proof_contract_is_frozen():
    """RecursiveProofContract must be immutable (frozen dataclass)."""
    import pytest
    contract = TYPED_CODEPOINT_CONTRACT
    with pytest.raises(AttributeError):
        contract.output = "MutatedOutput"  # type: ignore


# ---------------------------------------------------------------------------
# Structural chain tests
# ---------------------------------------------------------------------------

def test_layer_chain_order():
    """
    The Phase-1 chain must follow the correct layer order:
    TypedCodePoint → LetterIdentity → HarakaFunction → Position → Slot
    """
    expected_outputs = [
        "LetterCodePoint",
        "LetterIdentityCarrier",
        "HarakaFunctionCarrier",
        "PositionCarrier",
        "SlotCandidate",
    ]
    actual_outputs = [c.output for c in PHASE1_CONTRACTS]
    assert actual_outputs == expected_outputs


def test_slot_contract_consumes_three_inputs():
    """SlotCandidate requires three input carrier types."""
    assert len(SLOT_CONTRACT.inputs) == 3
    assert "LetterIdentityCarrier" in SLOT_CONTRACT.inputs
    assert "HarakaFunctionCarrier" in SLOT_CONTRACT.inputs
    assert "PositionCarrier" in SLOT_CONTRACT.inputs


def test_haraka_function_contract_forbids_case_effect():
    """HarakaFunctionCarrier contract must forbid CaseEffect and Irab."""
    assert "CaseEffect" in HARAKA_FUNCTION_CONTRACT.forbidden_outputs
    assert "Irab" in HARAKA_FUNCTION_CONTRACT.forbidden_outputs


def test_slot_contract_forbids_syllable():
    """SlotCandidate contract must forbid SyllableCandidate."""
    assert "SyllableCandidate" in SLOT_CONTRACT.forbidden_outputs
