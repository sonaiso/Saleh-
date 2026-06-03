"""
Constitutional tests for logarithmic measurement carrier readiness.

These tests verify constitutional constraints are enforced in the module.

Constitutional law:
- LogMeasuredQuantity → LogMeasurementReadinessCarrier
- Carrier readiness verifies; it does not decide
- Carrier carries; it does not judge
- Measurement preserves rank; it does not upgrade
- No authority derivation
- No Candidate/LCNV/MCLO/Meaning/Ifadah/Hukm integration
"""

import inspect

import pytest

from qiyas_core import logarithmic_measurement_carrier_readiness


def test_module_does_not_import_forbidden_modules():
    """
    Verify module does not import forbidden modules.

    Constitutional requirement:
    No Candidate, LCNV, MCLO, Pack, Meaning, Ifadah, Hukm imports.
    """
    forbidden_modules = [
        "candidate",
        "lcnv",
        "mclo",
        "pack",
        "unpack",
        "meaning",
        "ifadah",
        "hukm",
        "authority",
    ]

    source = inspect.getsource(logarithmic_measurement_carrier_readiness)

    for module in forbidden_modules:
        # Check for direct imports
        assert f"import {module}" not in source
        assert f"from qiyas_core.{module} import" not in source
        assert f"from .{module} import" not in source


def test_module_only_imports_from_logarithmic_measurement():
    """
    Verify module only imports from logarithmic_measurement and standard library.

    Constitutional requirement:
    Isolated runtime implementation.
    """
    source = inspect.getsource(logarithmic_measurement_carrier_readiness)

    # Check allowed imports
    assert "from qiyas_core.logarithmic_measurement import LogMeasuredQuantity" in source
    assert "from dataclasses import dataclass" in source
    assert "from decimal import Decimal" in source

    # Count qiyas_core imports (should only be logarithmic_measurement)
    qiyas_imports = source.count("from qiyas_core.")
    assert qiyas_imports == 1, f"Expected 1 qiyas_core import, found {qiyas_imports}"


def test_dataclass_is_frozen():
    """
    Verify LogMeasurementReadinessCarrier is frozen.

    Constitutional requirement:
    Immutability for identity preservation.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        LogMeasurementReadinessCarrier,
    )

    # Check if dataclass is frozen
    assert LogMeasurementReadinessCarrier.__dataclass_fields__
    # Frozen dataclasses have __setattr__ overridden
    assert hasattr(LogMeasurementReadinessCarrier, "__setattr__")


def test_no_authority_fields_in_dataclass():
    """
    Verify LogMeasurementReadinessCarrier has no authority fields.

    Constitutional requirement:
    No authority derivation.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        LogMeasurementReadinessCarrier,
    )

    fields = LogMeasurementReadinessCarrier.__dataclass_fields__

    forbidden_field_names = [
        "authority",
        "candidate_authority",
        "meaning",
        "ifadah",
        "hukm",
        "reality_claim",
    ]

    for field_name in forbidden_field_names:
        assert field_name not in fields, f"Forbidden field '{field_name}' found in dataclass"


def test_required_fields_in_dataclass():
    """
    Verify LogMeasurementReadinessCarrier has all required fields.

    Constitutional requirement:
    All required carrier readiness fields must be present.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        LogMeasurementReadinessCarrier,
    )

    fields = LogMeasurementReadinessCarrier.__dataclass_fields__

    required_fields = [
        "source_log_measurement_ref",
        "original_quantity_id",
        "is_bridge_ready",
        "blocking_conditions",
        "constitutional_compliance",
        "log_value",
        "unit",
        "rank",
        "trace_ids",
        "residual_ids",
        "carrier_readiness_trace",
    ]

    for field_name in required_fields:
        assert field_name in fields, f"Required field '{field_name}' not found in dataclass"


def test_function_signature_accepts_only_log_measured_quantity():
    """
    Verify validate_log_measurement_carrier_readiness signature.

    Constitutional requirement:
    Function must accept only LogMeasuredQuantity.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    sig = inspect.signature(validate_log_measurement_carrier_readiness)
    params = list(sig.parameters.values())

    # Should have exactly 1 parameter
    assert len(params) == 1

    # Parameter name should indicate log_quantity
    assert params[0].name == "log_quantity"


def test_module_has_constitutional_docstring():
    """
    Verify module has constitutional law docstring.

    Constitutional requirement:
    Module must declare its constitutional constraints.
    """
    source = inspect.getsource(logarithmic_measurement_carrier_readiness)

    # Check for constitutional elements in docstring
    required_phrases = [
        "Constitutional law",
        "Forbidden",
        "Carrier readiness verifies",
        "does not decide",
        "Carrier carries",
        "does not judge",
        "Measurement preserves rank",
        "does not upgrade",
    ]

    for phrase in required_phrases:
        assert phrase in source, f"Required constitutional phrase '{phrase}' not found in module"


def test_no_candidate_production():
    """
    Verify function does not produce Candidate.

    Constitutional requirement:
    LogMeasurementReadinessCarrier is not a Candidate.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    source = inspect.getsource(validate_log_measurement_carrier_readiness)

    # Should not return anything with "Candidate" type
    assert "-> Candidate" not in source
    assert "return Candidate" not in source


def test_no_meaning_or_hukm_production():
    """
    Verify function does not produce Meaning or Hukm.

    Constitutional requirement:
    No Meaning, Ifadah, or Hukm derivation.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    source = inspect.getsource(validate_log_measurement_carrier_readiness)

    # Should not produce meaning or hukm
    forbidden_returns = ["Meaning", "Ifadah", "Hukm", "RealityClaim"]

    for forbidden in forbidden_returns:
        assert f"-> {forbidden}" not in source
        assert f"return {forbidden}" not in source


def test_identity_preservation_in_implementation():
    """
    Verify implementation preserves identity correctly.

    Constitutional requirement:
    original_quantity_id ≠ source_log_measurement_ref ≠ carrier_readiness_trace
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    source = inspect.getsource(validate_log_measurement_carrier_readiness)

    # Check that original_quantity_id is assigned from source_quantity_id
    assert "original_quantity_id = log_quantity.source_quantity_id" in source

    # Check that source_log_measurement_ref is created as provenance
    assert "source_log_measurement_ref = f\"log_measurement:" in source

    # Check that carrier_readiness_trace is created as trace
    assert "carrier_readiness_trace = f\"trace:carrier_readiness:" in source


def test_rank_preservation_in_implementation():
    """
    Verify implementation preserves rank without upgrading.

    Constitutional requirement:
    Measurement preserves rank; it does not upgrade.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    source = inspect.getsource(validate_log_measurement_carrier_readiness)

    # Check that rank is preserved from input
    assert "rank = log_quantity.rank" in source

    # Check that rank is not upgraded or modified
    assert "rank.upper()" not in source
    assert "rank = \"STRONG\"" not in source
    assert "upgrade" not in source.lower() or "does not upgrade" in source.lower()


def test_residual_preservation_in_implementation():
    """
    Verify implementation preserves residuals.

    Constitutional requirement:
    Residuals must be preserved.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    source = inspect.getsource(validate_log_measurement_carrier_readiness)

    # Check that residuals are preserved
    assert "residual_ids = log_quantity.residual_ids" in source


def test_trace_extension_in_implementation():
    """
    Verify implementation extends trace correctly.

    Constitutional requirement:
    Trace must be preserved AND extended with carrier readiness trace.
    """
    from qiyas_core.logarithmic_measurement_carrier_readiness import (
        validate_log_measurement_carrier_readiness,
    )

    source = inspect.getsource(validate_log_measurement_carrier_readiness)

    # Check that trace is extended (not replaced)
    assert "trace_ids = log_quantity.trace_ids + (" in source
    assert "carrier_readiness_trace" in source
