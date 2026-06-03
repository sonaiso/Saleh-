"""
Constitutional closure test for Logarithmic Measurement Phase 1.

This test verifies that Phase 1 closure document exists and contains
required closure and isolation guarantees.
"""

import re
from pathlib import Path


def test_phase1_closure_document_exists():
    """Verify Phase 1 closure document exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    assert doc_path.exists(), "Phase 1 closure document must exist"


def test_phase1_closure_document_contains_required_closure_phrases():
    """Verify Phase 1 closure document contains required closure phrases."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    required_phrases = [
        "Phase 1 is complete and isolated",
        "runtime exists and is isolated",
        "Blocking residuals prevent building",
        "Trace extends without mixing with identity",
        "No transition to Candidate",
    ]

    for phrase in required_phrases:
        assert phrase in content, f"Closure document must contain: {phrase}"


def test_phase1_closure_document_confirms_runtime_isolation():
    """Verify Phase 1 closure document confirms runtime isolation."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    isolation_confirmations = [
        "No imports from LCNV modules",
        "No imports from Candidate modules",
        "No imports from MCLO modules",
        "No imports from Pack/Unpack modules",
    ]

    for confirmation in isolation_confirmations:
        assert confirmation in content, f"Closure document must confirm: {confirmation}"


def test_phase1_closure_document_confirms_blocking_residual_validation():
    """Verify Phase 1 closure document confirms blocking residual validation."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    blocking_validations = [
        "residual:blocking:*",
        "*:blocking:*",
        "blocking:*",
        "log rejects blocking residuals",
    ]

    for validation in blocking_validations:
        # Use regex escape to handle special characters
        pattern = re.escape(validation)
        assert re.search(pattern, content), f"Closure document must confirm blocking validation: {validation}"


def test_phase1_closure_document_confirms_trace_extension():
    """Verify Phase 1 closure document confirms trace extension mechanism."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    trace_confirmations = [
        "trace:log_quantity:",
        "Trace is extended, not replaced",
        "Original trace is preserved",
        "Identity ≠ Trace",
    ]

    for confirmation in trace_confirmations:
        assert confirmation in content, f"Closure document must confirm trace extension: {confirmation}"


def test_phase1_closure_document_confirms_no_candidate_integration():
    """Verify Phase 1 closure document confirms no Candidate integration."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    no_candidate_confirmations = [
        "No Candidate Integration",
        "Accept Candidate as input",
        "Produce Candidate as output",
        "log(Candidate) ⇏",
    ]

    for confirmation in no_candidate_confirmations:
        assert confirmation in content, f"Closure document must confirm no Candidate integration: {confirmation}"


def test_phase1_closure_document_confirms_no_lcnv_integration():
    """Verify Phase 1 closure document confirms no LCNV integration."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    no_lcnv_confirmations = [
        "No LCNV Integration",
        "Accept LCNV as input",
        "Produce LCNV as output",
        "log(LCNV) ⇏",
    ]

    for confirmation in no_lcnv_confirmations:
        assert confirmation in content, f"Closure document must confirm no LCNV integration: {confirmation}"


def test_phase1_closure_document_confirms_no_mclo_integration():
    """Verify Phase 1 closure document confirms no MCLO integration."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    no_mclo_confirmations = [
        "No MCLO Integration",
        "Accept MCLO as input",
        "Produce MCLO as output",
    ]

    for confirmation in no_mclo_confirmations:
        assert confirmation in content, f"Closure document must confirm no MCLO integration: {confirmation}"


def test_phase1_closure_document_confirms_no_meaning_derivation():
    """Verify Phase 1 closure document confirms no meaning/ifadah/hukm derivation."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    no_meaning_confirmations = [
        "No Meaning/Ifadah/Hukm Derivation",
        "Derive meaning from logarithmic values",
        "log(Meaning) ⇏",
        "log(Ifadah) ⇏",
        "log(Hukm) ⇏",
    ]

    for confirmation in no_meaning_confirmations:
        assert confirmation in content, f"Closure document must confirm no meaning derivation: {confirmation}"


def test_phase1_closure_document_forbids_direct_integration():
    """Verify Phase 1 closure document forbids direct integration."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    forbidden_integrations = [
        "LogMeasuredQuantity → Candidate",
        "LogMeasuredQuantity → LCNV",
        "LogMeasuredQuantity → Meaning",
        "No direct integration",
    ]

    for forbidden in forbidden_integrations:
        assert forbidden in content, f"Closure document must forbid: {forbidden}"


def test_phase1_closure_document_specifies_next_phase():
    """Verify Phase 1 closure document specifies next phase requirements."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    next_phase_specifications = [
        "Bridge Specification",
        "Phase 2",
        "NOT direct integration",
        "LogMeasurementBridgeReadiness",
    ]

    for spec in next_phase_specifications:
        assert spec in content, f"Closure document must specify next phase: {spec}"


def test_phase1_closure_document_confirms_closure_status():
    """Verify Phase 1 closure document confirms closure status."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    closure_confirmations = [
        "is hereby closed",
        "This phase is complete",
        "Phase 1 closed, isolated, complete",
    ]

    for confirmation in closure_confirmations:
        assert confirmation in content, f"Closure document must confirm closure: {confirmation}"


def test_phase1_closure_document_contains_governing_law():
    """Verify Phase 1 closure document contains governing law in Arabic and English."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LOGARITHMIC_MEASUREMENT_PHASE1_CLOSURE.md"
    content = doc_path.read_text()

    governing_law_phrases = [
        "اللوغاريتم المرخّص لا ينتج مرشحًا ولا معنى",
        "Licensed logarithm does not produce Candidate or Meaning",
        "المرحلة الأولى مغلقة ومعزولة",
        "Phase 1 is closed and isolated",
    ]

    for phrase in governing_law_phrases:
        assert phrase in content, f"Closure document must contain governing law: {phrase}"
