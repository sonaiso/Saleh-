"""
Tests for licensed logarithmic measurement runtime.

Constitutional law:
- log : LicensedMeasuredQuantity → LogMeasuredQuantity
- inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity

Forbidden:
- log(Candidate)
- log(LCNV)
- log(Meaning/Ifadah/Hukm)
- inverse_log → Candidate
"""

from decimal import Decimal

import pytest

from qiyas_core.logarithmic_measurement import (
    LicensedMeasuredQuantity,
    LogMeasuredQuantity,
    LogMeasurementError,
    inverse_log_quantity,
    log_quantity,
)


def test_log_roundtrip_for_licensed_quantity():
    """
    Verify logarithm roundtrip preserves quantity identity.

    Constitutional requirement:
    LicensedMeasuredQuantity → LogMeasuredQuantity → LicensedMeasuredQuantity
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:open-path-count",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:path-count",),
        residual_ids=("residual:non_blocking",),
    )

    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))
    restored = inverse_log_quantity(lq)

    assert isinstance(lq, LogMeasuredQuantity)
    assert isinstance(restored, LicensedMeasuredQuantity)
    assert restored.quantity_id == q.quantity_id
    assert restored.unit == q.unit
    assert restored.trace_ids == q.trace_ids
    assert restored.residual_ids == q.residual_ids
    assert restored.value == pytest.approx(q.value)


def test_log_rejects_closed_gate():
    """
    Verify logarithm rejects quantity with CLOSED gate.

    Constitutional requirement:
    log requires OPEN gate.
    """
    with pytest.raises(LogMeasurementError, match="log requires OPEN gate"):
        LicensedMeasuredQuantity(
            quantity_id="quantity:closed",
            value=Decimal("1"),
            unit="count",
            gate="CLOSED",  # type: ignore[arg-type]
            trace_ids=("trace:x",),
        )


def test_log_rejects_negative_quantity():
    """
    Verify logarithm rejects negative quantity.

    Constitutional requirement:
    log requires non-negative licensed quantity.
    """
    with pytest.raises(LogMeasurementError, match="log requires non-negative"):
        LicensedMeasuredQuantity(
            quantity_id="quantity:negative",
            value=Decimal("-1"),
            unit="count",
            gate="OPEN",
            trace_ids=("trace:x",),
        )


def test_log_rejects_invalid_base():
    """
    Verify logarithm rejects invalid bases.

    Constitutional requirement:
    base must be positive and ≠ 1.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:x",),
    )

    with pytest.raises(LogMeasurementError, match="base must be positive"):
        log_quantity(q, base=Decimal("1"))

    with pytest.raises(LogMeasurementError, match="base must be positive"):
        log_quantity(q, base=Decimal("0"))

    with pytest.raises(LogMeasurementError, match="base must be positive"):
        log_quantity(q, base=Decimal("-10"))


def test_log_rejects_unlicensed_input():
    """
    Verify logarithm rejects non-LicensedMeasuredQuantity input.

    Constitutional requirement:
    log only accepts LicensedMeasuredQuantity.
    """
    with pytest.raises(LogMeasurementError, match="log only accepts LicensedMeasuredQuantity"):
        log_quantity(object())  # type: ignore[arg-type]


def test_inverse_log_rejects_unlicensed_input():
    """
    Verify inverse_log rejects non-LogMeasuredQuantity input.

    Constitutional requirement:
    inverse_log only accepts LogMeasuredQuantity.
    """
    with pytest.raises(LogMeasurementError, match="inverse_log only accepts LogMeasuredQuantity"):
        inverse_log_quantity(object())  # type: ignore[arg-type]


def test_log_preserves_unit():
    """
    Verify logarithm preserves unit of measurement.

    Constitutional requirement:
    Unit must be preserved through log/inverse_log.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("99"),
        unit="meters",
        gate="OPEN",
        trace_ids=("trace:measurement",),
    )

    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))
    restored = inverse_log_quantity(lq)

    assert lq.unit == "meters"
    assert restored.unit == "meters"


def test_log_preserves_trace():
    """
    Verify logarithm preserves trace_ids.

    Constitutional requirement:
    Trace must be preserved through log/inverse_log.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas:1", "trace:qiyas:2"),
    )

    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))
    restored = inverse_log_quantity(lq)

    assert lq.trace_ids == ("trace:qiyas:1", "trace:qiyas:2")
    assert restored.trace_ids == ("trace:qiyas:1", "trace:qiyas:2")


def test_log_preserves_residuals():
    """
    Verify logarithm preserves residual_ids.

    Constitutional requirement:
    Residuals must be preserved through log/inverse_log.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas",),
        residual_ids=("residual:non_blocking_1", "residual:non_blocking_2"),
    )

    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))
    restored = inverse_log_quantity(lq)

    assert lq.residual_ids == ("residual:non_blocking_1", "residual:non_blocking_2")
    assert restored.residual_ids == ("residual:non_blocking_1", "residual:non_blocking_2")


def test_log_preserves_rank():
    """
    Verify logarithm preserves rank.

    Constitutional requirement:
    Rank must be preserved through log/inverse_log.
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("9"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:qiyas",),
        rank="STRONG",
    )

    lq = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))
    restored = inverse_log_quantity(lq)

    assert lq.rank == "STRONG"
    assert restored.rank == "STRONG"


def test_log_requires_declared_unit():
    """
    Verify logarithm rejects empty unit.

    Constitutional requirement:
    log requires declared unit.
    """
    with pytest.raises(LogMeasurementError, match="log requires declared unit"):
        LicensedMeasuredQuantity(
            quantity_id="quantity:no-unit",
            value=Decimal("9"),
            unit="",
            gate="OPEN",
            trace_ids=("trace:x",),
        )


def test_log_requires_trace_ids():
    """
    Verify logarithm rejects empty trace_ids.

    Constitutional requirement:
    log requires trace_ids.
    """
    with pytest.raises(LogMeasurementError, match="log requires trace_ids"):
        LicensedMeasuredQuantity(
            quantity_id="quantity:no-trace",
            value=Decimal("9"),
            unit="count",
            gate="OPEN",
            trace_ids=(),
        )


def test_log_with_different_bases():
    """
    Verify logarithm works with different bases.

    Allowed bases: e, 2, 10, etc. (positive, ≠ 1)
    """
    q = LicensedMeasuredQuantity(
        quantity_id="quantity:test",
        value=Decimal("7"),
        unit="count",
        gate="OPEN",
        trace_ids=("trace:x",),
    )

    # Base 2
    lq2 = log_quantity(q, base=Decimal("2"), shift=Decimal("1"))
    restored2 = inverse_log_quantity(lq2)
    assert restored2.value == pytest.approx(q.value)

    # Base e (approximately 2.71828)
    lqe = log_quantity(q, base=Decimal("2.71828"), shift=Decimal("1"))
    restorede = inverse_log_quantity(lqe)
    assert restorede.value == pytest.approx(q.value, abs=0.01)

    # Base 10
    lq10 = log_quantity(q, base=Decimal("10"), shift=Decimal("1"))
    restored10 = inverse_log_quantity(lq10)
    assert restored10.value == pytest.approx(q.value)
