"""
Tests for logarithmic measurement carrier readiness runtime.

Constitutional law:
- LogMeasuredQuantity → LogMeasurementReadinessCarrier
- Carrier readiness verifies; it does not decide
- Carrier carries; it does not judge
- Measurement preserves rank; it does not upgrade

Forbidden:
- No Candidate integration
- No LCNV integration
- No MCLO integration
- No Pack/Unpack
- No Meaning/Ifadah/Hukm derivation
- No authority fields
"""

from decimal import Decimal

import pytest

from qiyas_core.logarithmic_measurement import (
    LicensedMeasuredQuantity,
    LogMeasuredQuantity,
    log_quantity,
)
from qiyas_core.logarithmic_measurement_carrier_readiness import (
    CarrierReadinessError,
    LogMeasurementReadinessCarrier,
    validate_log_measurement_carrier_readiness,
)


def test_accepts_log_measured_quantity():
    """
    Verify carrier readiness accepts LogMeasuredQuantity.

    Constitutional requirement:
    validate_log_measurement_carrier_readiness only accepts LogMeasuredQuantity.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    assert isinstance(carrier, LogMeasurementReadinessCarrier)


def test_rejects_non_log_measured_quantity():
    """
    Verify carrier readiness rejects non-LogMeasuredQuantity input.

    Constitutional requirement:
    validate_log_measurement_carrier_readiness only accepts LogMeasuredQuantity.
    """
    with pytest.raises(
        CarrierReadinessError,
        match="validate_log_measurement_carrier_readiness only accepts LogMeasuredQuantity",
    ):
        validate_log_measurement_carrier_readiness(object())  # type: ignore[arg-type]


def test_preserves_original_quantity_id():
    """
    Verify carrier readiness preserves original quantity identity.

    Constitutional requirement:
    original_quantity_id preserves LicensedMeasuredQuantity identity.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:original",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    assert carrier.original_quantity_id == "quantity:original"
    assert carrier.original_quantity_id == lq.source_quantity_id


def test_source_log_measurement_ref_is_provenance_not_identity():
    """
    Verify source_log_measurement_ref is provenance, not identity.

    Constitutional requirement:
    source_log_measurement_ref is provenance only, not identity.
    original_quantity_id ≠ source_log_measurement_ref
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    # source_log_measurement_ref is NOT the same as original_quantity_id
    assert carrier.source_log_measurement_ref != carrier.original_quantity_id

    # source_log_measurement_ref is a provenance reference
    assert carrier.source_log_measurement_ref.startswith("log_measurement:")
    assert carrier.original_quantity_id in carrier.source_log_measurement_ref


def test_adds_carrier_readiness_trace():
    """
    Verify carrier readiness adds carrier_readiness_trace.

    Constitutional requirement:
    carrier_readiness_trace is trace only, not identity.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    # carrier_readiness_trace is created
    assert carrier.carrier_readiness_trace.startswith("trace:carrier_readiness:")

    # carrier_readiness_trace is NOT identity
    assert carrier.carrier_readiness_trace != carrier.original_quantity_id
    assert carrier.carrier_readiness_trace != carrier.source_log_measurement_ref


def test_trace_ids_preserve_existing_trace_and_append_readiness_trace():
    """
    Verify trace_ids preserve existing trace and append carrier_readiness_trace.

    Constitutional requirement:
    Trace must be preserved AND extended with carrier readiness trace.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1", "trace:qiyas:2"),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    # Original traces are preserved
    assert "trace:qiyas:1" in carrier.trace_ids
    assert "trace:qiyas:2" in carrier.trace_ids

    # Log operation trace is preserved
    assert any("trace:log_quantity:" in t for t in carrier.trace_ids)

    # Carrier readiness trace is added
    assert carrier.carrier_readiness_trace in carrier.trace_ids

    # Trace has more entries than log_quantity
    assert len(carrier.trace_ids) > len(lq.trace_ids)


def test_rank_is_preserved_not_upgraded():
    """
    Verify carrier readiness preserves rank without upgrading.

    Constitutional requirement:
    Measurement preserves rank; it does not upgrade.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
        rank="WEAK",
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    # Rank is preserved exactly
    assert carrier.rank == "WEAK"
    assert carrier.rank == lq.rank


def test_unit_is_preserved():
    """
    Verify carrier readiness preserves unit of measurement.

    Constitutional requirement:
    Unit must be preserved through carrier readiness.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="meters",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    assert carrier.unit == "meters"
    assert carrier.unit == lq.unit


def test_log_value_is_preserved():
    """
    Verify carrier readiness preserves log value.

    Constitutional requirement:
    Log value must be preserved through carrier readiness.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    assert carrier.log_value == lq.log_value


def test_residuals_are_preserved():
    """
    Verify carrier readiness preserves residuals.

    Constitutional requirement:
    Residuals must be preserved through carrier readiness.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
        residual_ids=("residual:non_blocking_1", "residual:non_blocking_2"),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    assert carrier.residual_ids == ("residual:non_blocking_1", "residual:non_blocking_2")
    assert carrier.residual_ids == lq.residual_ids


def test_blocking_residuals_make_bridge_ready_false():
    """
    Verify blocking residuals make is_bridge_ready = False.

    Constitutional requirement:
    Blocking residuals prevent bridge readiness.
    Carrier verifies; it does not decide to fail completely.
    """
    # Create a log quantity without blocking residuals
    q_clean = LicensedMeasuredQuantity(
        quantity_id="quantity:clean",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
        residual_ids=(),
    )
    lq_clean = log_quantity(q_clean, base=Decimal("10"), shift=Decimal("1"))

    # Manually construct a LogMeasuredQuantity with blocking residuals
    # (LicensedMeasuredQuantity would reject blocking residuals, but LogMeasuredQuantity may receive them)
    lq_blocked = LogMeasuredQuantity(
        source_quantity_id="quantity:blocked",
        log_value=Decimal("1"),
        base=Decimal("10"),
        shift=Decimal("1"),
        unit="count",
        trace_ids=("trace:qiyas:1",),
        residual_ids=("residual:blocking:issue",),
    )

    carrier_clean = validate_log_measurement_carrier_readiness(lq_clean)
    carrier_blocked = validate_log_measurement_carrier_readiness(lq_blocked)

    # Clean carrier is bridge ready
    assert carrier_clean.is_bridge_ready is True
    assert carrier_clean.blocking_conditions == ()

    # Blocked carrier is NOT bridge ready
    assert carrier_blocked.is_bridge_ready is False
    assert len(carrier_blocked.blocking_conditions) > 0


def test_blocking_conditions_are_recorded():
    """
    Verify blocking conditions are recorded when blocking residuals exist.

    Constitutional requirement:
    Blocking residuals are recorded in blocking_conditions.
    """
    lq_blocked = LogMeasuredQuantity(
        source_quantity_id="quantity:blocked",
        log_value=Decimal("1"),
        base=Decimal("10"),
        shift=Decimal("1"),
        unit="count",
        trace_ids=("trace:qiyas:1",),
        residual_ids=(
            "residual:blocking:issue1",
            "residual:non_blocking",
            "domain:blocking:issue2",
        ),
    )

    carrier = validate_log_measurement_carrier_readiness(lq_blocked)

    # blocking_conditions contains only blocking residuals
    assert "residual:blocking:issue1" in carrier.blocking_conditions
    assert "domain:blocking:issue2" in carrier.blocking_conditions
    assert "residual:non_blocking" not in carrier.blocking_conditions


def test_output_has_no_authority_fields():
    """
    Verify output has no authority fields.

    Constitutional requirement:
    LogMeasurementReadinessCarrier does NOT produce authority.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    # Verify no authority fields exist
    carrier_dict = carrier.__dict__
    assert "authority" not in carrier_dict
    assert "candidate_authority" not in carrier_dict
    assert "meaning" not in carrier_dict
    assert "ifadah" not in carrier_dict
    assert "hukm" not in carrier_dict


def test_no_candidate_lcnv_mclo_pack_meaning_ifadah_hukm_imports():
    """
    Verify no forbidden imports in logarithmic_measurement_carrier_readiness module.

    Constitutional requirement:
    No Candidate, LCNV, MCLO, Pack, Meaning, Ifadah, Hukm integration.
    """
    import inspect

    from qiyas_core import logarithmic_measurement_carrier_readiness

    source = inspect.getsource(logarithmic_measurement_carrier_readiness)

    # Check for forbidden import statements (actual code imports)
    forbidden_import_patterns = [
        "from qiyas_core.candidate import",
        "import candidate",
        "from qiyas_core.lcnv import",
        "from qiyas_core.mclo import",
        "from qiyas_core.meaning import",
        "from qiyas_core.ifadah import",
        "from qiyas_core.hukm import",
    ]

    for pattern in forbidden_import_patterns:
        assert pattern not in source, (
            f"Forbidden import pattern '{pattern}' found in module"
        )


def test_constitutional_compliance_is_true_for_valid_input():
    """
    Verify constitutional_compliance is True for valid input.

    Constitutional requirement:
    constitutional_compliance is independent of bridge readiness.
    Only False if constitutional violation detected.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    assert carrier.constitutional_compliance is True


def test_identity_separation_law():
    """
    Verify identity separation law is enforced.

    Constitutional requirement:
    original_quantity_id ≠ source_log_measurement_ref ≠ carrier_readiness_trace
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1",),
    )
    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))

    carrier = validate_log_measurement_carrier_readiness(lq)

    # All three must be different
    assert carrier.original_quantity_id != carrier.source_log_measurement_ref
    assert carrier.original_quantity_id != carrier.carrier_readiness_trace
    assert carrier.source_log_measurement_ref != carrier.carrier_readiness_trace

    # Verify they are actually distinct strings
    assert carrier.original_quantity_id == "quantity:test"
    assert carrier.source_log_measurement_ref == "log_measurement:quantity:test"
    assert carrier.carrier_readiness_trace == "trace:carrier_readiness:quantity:test"
