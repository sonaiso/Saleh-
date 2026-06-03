"""
Constitutional compliance tests for Logarithmic Measurement Carrier Readiness Contract.

Tests verify that the contract document:
- Exists and is complete
- Contains required isolation phrases
- Confirms no Candidate integration
- Confirms no LCNV integration
- Confirms no MCLO integration
- Confirms no Pack/Unpack integration
- Confirms no Meaning/Ifadah/Hukm derivation
- Confirms isolated readiness carrier only
- Confirms no general Carrier adapter
- Confirms no authority derivation
"""

import pytest
from pathlib import Path


@pytest.fixture
def contract_doc_path():
    """Path to the Carrier Readiness Contract document."""
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_CARRIER_READINESS_CONTRACT.md"


@pytest.fixture
def contract_content(contract_doc_path):
    """Read contract document content."""
    assert contract_doc_path.exists(), f"Contract document not found: {contract_doc_path}"
    return contract_doc_path.read_text(encoding="utf-8")


def test_contract_document_exists(contract_doc_path):
    """Contract document must exist."""
    assert contract_doc_path.exists()


def test_contract_confirms_phase_3_scope(contract_content):
    """Contract must confirm Phase 3 Carrier Readiness scope."""
    required_phrases = [
        "Phase 3 Carrier Readiness Contract",
        "isolated implementation only",
        "Carrier readiness validation",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_isolated_dataclass(contract_content):
    """Contract must define isolated readiness carrier dataclass."""
    required_phrases = [
        "LogMeasurementReadinessCarrier",
        "isolated readiness carrier",
        "is not a general carrier",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_validation_function(contract_content):
    """Contract must define isolated validation function."""
    required_phrases = [
        "validate_log_measurement_carrier_readiness",
        "Bridge readiness verification",
        "Blocking condition detection",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_no_candidate_integration(contract_content):
    """Contract must confirm no Candidate integration."""
    required_phrases = [
        "Does Not Integrate with Candidate",
        "Candidate integration remains FORBIDDEN",
        "Direct integration with Candidate",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_no_lcnv_integration(contract_content):
    """Contract must confirm no LCNV integration."""
    required_phrases = [
        "Does Not Integrate with LCNV",
        "LCNV integration remains FORBIDDEN",
        "Direct integration with LCNV",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_no_mclo_integration(contract_content):
    """Contract must confirm no MCLO integration."""
    required_phrases = [
        "Does Not Integrate with MCLO",
        "MCLO integration remains FORBIDDEN",
        "Direct integration with MCLO",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_no_pack_unpack_integration(contract_content):
    """Contract must confirm no Pack/Unpack integration."""
    required_phrases = [
        "Does Not Integrate with Pack/Unpack",
        "Pack/Unpack integration remains FORBIDDEN",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_no_meaning_derivation(contract_content):
    """Contract must confirm no Meaning/Ifadah/Hukm derivation."""
    required_phrases = [
        "Does Not Derive Meaning, Ifadah, or Hukm",
        "Meaning/Ifadah/Hukm derivation remains FORBIDDEN",
        "Derive meaning from logarithmic values",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_readiness_not_authority(contract_content):
    """Contract must confirm readiness is not authority."""
    required_phrases = [
        "Carrier Readiness ≠ Carrier Authority",
        "is not Candidate authority",
        "NOT produce CandidateAuthority",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_no_general_carrier_adapter(contract_content):
    """Contract must confirm no general Carrier adapter."""
    required_phrases = [
        "Carrier Readiness ≠ General Carrier Adapter",
        "General Carrier adapter",
        "Isolated, specific readiness carrier",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_isolation_boundaries(contract_content):
    """Contract must define isolation boundaries."""
    required_phrases = [
        "Import Isolation",
        "No imports from Candidate modules",
        "No imports from LCNV modules",
        "No imports from MCLO modules",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_identity_preservation(contract_content):
    """Contract must confirm identity preservation."""
    required_phrases = [
        "Identity preservation is mandatory",
        "Preserved identity",
        "original_quantity_id",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_trace_extension(contract_content):
    """Contract must confirm trace extension (not replacement)."""
    required_phrases = [
        "Trace is extended (not replaced)",
        "Extended with carrier readiness trace",
        "trace:carrier_readiness:",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_rank_preservation(contract_content):
    """Contract must confirm rank preservation."""
    required_phrases = [
        "Rank is preserved (not upgraded)",
        "NOT upgraded",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_residual_preservation(contract_content):
    """Contract must confirm residual preservation."""
    required_phrases = [
        "Residuals are preserved (not hidden)",
        "NOT hidden",
        "NOT discarded",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_blocking_condition_detection(contract_content):
    """Contract must define blocking condition detection."""
    required_phrases = [
        "Blocking condition detection",
        "blocking_conditions",
        "is_bridge_ready",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_constitutional_compliance(contract_content):
    """Contract must define constitutional compliance verification."""
    required_phrases = [
        "Constitutional compliance verification",
        "constitutional_compliance",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_required_tests(contract_content):
    """Contract must define required tests."""
    required_phrases = [
        "Required Tests",
        "Bridge Readiness Verification Tests",
        "Isolation Tests",
        "Constitutional Compliance Tests",
        "Forbidden Output Tests",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_forbidden_operations(contract_content):
    """Contract must list forbidden operations."""
    required_phrases = [
        "What Remains Forbidden",
        "Direct integration with Candidate",
        "Direct integration with LCNV",
        "Direct integration with MCLO",
        "Meaning/Ifadah/Hukm derivation",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_future_deferral(contract_content):
    """Contract must define what is deferred to future phases."""
    required_phrases = [
        "What is Deferred to Future Phases",
        "requires separate constitutional authorization",
        "NOT part of Phase 3",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_implementation_scope(contract_content):
    """Contract must define implementation scope."""
    required_phrases = [
        "Implementation Scope for Phase 3",
        "What Phase 3 Implements",
        "What Phase 3 Does NOT Implement",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_confirms_governing_law_arabic(contract_content):
    """Contract must include governing law in Arabic."""
    required_phrases = [
        "حامل جاهزية القياس اللوغاريتمي",
        "ليس سلطة مرشح",
        "ممنوع",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required Arabic phrase: {phrase}"


def test_contract_confirms_governing_law_english(contract_content):
    """Contract must include governing law in English."""
    required_phrases = [
        "Readiness carrier is not Candidate authority",
        "Readiness verifies, does not produce",
        "Forbidden",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required English phrase: {phrase}"


def test_contract_forbids_prohibited_phrases(contract_content):
    """Contract must NOT contain phrases that imply forbidden integration."""
    # These phrases should NOT appear in affirmative context
    # (they may appear in "does NOT" or "forbidden" context)

    # Check document structure prevents misinterpretation
    prohibited_affirmative_patterns = [
        "Carrier readiness produces Candidate",
        "Carrier readiness derives authority",
        "Carrier readiness integrates with Candidate",
        "LogMeasurementReadinessCarrier → Candidate (permitted)",
    ]

    for pattern in prohibited_affirmative_patterns:
        assert pattern not in contract_content, f"Prohibited affirmative phrase found: {pattern}"


def test_contract_version_and_status(contract_content):
    """Contract must have version and status."""
    required_phrases = [
        "Document Version:",
        "Status:",
        "Phase 3 Carrier Readiness Contract",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required phrase: {phrase}"


def test_contract_constitutional_authority(contract_content):
    """Contract must reference constitutional authority."""
    required_phrases = [
        "Constitutional Authority",
        "PROJECT_MATHEMATICAL_FOUNDATION.md",
        "LOGARITHMIC_MEASUREMENT_BRIDGE_SPECIFICATION.md",
        "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md",
        "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md",
        "CANONICAL_ARCHITECTURE_CONTROL_FRAME.md",
    ]
    for phrase in required_phrases:
        assert phrase in contract_content, f"Missing required constitutional reference: {phrase}"
