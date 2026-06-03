"""
Licensed Logarithmic Measurement

Constitutional law:
- log : LicensedMeasuredQuantity → LogMeasuredQuantity
- inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity

Forbidden:
- log(Candidate)
- log(LCNV)
- log(EncodedStateProjection)
- log(Meaning)
- log(Ifadah)
- log(Hukm)
- inverse_log(LogMeasuredQuantity) → Candidate

Governing principle:
  المقدار المرخّص فقط يدخل اللوغاريتم.
  واللوغاريتم لا ينتج مرشحًا ولا معنى ولا حكمًا.

  (Only LicensedMeasuredQuantity enters logarithm.
   Logarithm does not produce Candidate, Meaning, or Hukm.)

See: docs/qiyas_core/LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import log as _log, pow as _pow
from typing import Literal


class LogMeasurementError(ValueError):
    """Raised when logarithmic measurement is attempted outside its licensed domain."""


def _has_blocking_residual(residual_ids: tuple[str, ...]) -> bool:
    """
    Check if any residual is blocking.

    Blocking residuals prevent logarithmic operations.
    Patterns that indicate blocking:
    - residual:blocking:*
    - *:blocking:*
    - blocking:*

    Args:
        residual_ids: Tuple of residual identifier strings

    Returns:
        True if any residual is blocking, False otherwise
    """
    return any(
        r.startswith("residual:blocking")
        or ":blocking:" in r
        or r.startswith("blocking:")
        for r in residual_ids
    )


@dataclass(frozen=True)
class LicensedMeasuredQuantity:
    """
    A licensed measured quantity.

    Constitutional requirements:
    - gate must be OPEN
    - value must be non-negative
    - unit must be declared
    - trace_ids must be present
    - NOT a Candidate
    - NOT an LCNV
    - NOT a Meaning/Ifadah/Hukm
    """

    quantity_id: str
    value: Decimal
    unit: str
    gate: Literal["OPEN"]
    trace_ids: tuple[str, ...]
    residual_ids: tuple[str, ...] = ()
    rank: str = "CANDIDATE"

    def __post_init__(self) -> None:
        if self.gate != "OPEN":
            raise LogMeasurementError("log requires OPEN gate")
        if self.value < 0:
            raise LogMeasurementError("log requires non-negative licensed quantity")
        if not self.unit:
            raise LogMeasurementError("log requires declared unit")
        if not self.trace_ids:
            raise LogMeasurementError("log requires trace_ids")
        if _has_blocking_residual(self.residual_ids):
            raise LogMeasurementError("log rejects blocking residuals")


@dataclass(frozen=True)
class LogMeasuredQuantity:
    """
    A logarithmically measured quantity.

    Constitutional constraints:
    - NOT a Candidate
    - NOT an LCNV
    - NOT a Meaning/Ifadah/Hukm
    - Does NOT produce CandidateAuthority
    - Only reversible to LicensedMeasuredQuantity
    """

    source_quantity_id: str
    log_value: Decimal
    base: Decimal
    shift: Decimal
    unit: str
    trace_ids: tuple[str, ...]
    residual_ids: tuple[str, ...] = ()
    rank: str = "CANDIDATE"

    def __post_init__(self) -> None:
        if self.base <= 0 or self.base == 1:
            raise LogMeasurementError("invalid logarithm base")
        if self.shift <= 0:
            raise LogMeasurementError("shift must be positive")
        if not self.unit:
            raise LogMeasurementError("inverse log requires declared unit")
        if not self.trace_ids:
            raise LogMeasurementError("inverse log requires trace_ids")


def _validate_base(base: Decimal) -> None:
    if base <= 0 or base == 1:
        raise LogMeasurementError("base must be positive and not equal to 1")


def log_quantity(
    quantity: LicensedMeasuredQuantity,
    *,
    base: Decimal = Decimal("10"),
    shift: Decimal = Decimal("1"),
) -> LogMeasuredQuantity:
    """
    Licensed logarithmic measurement.

    Constitutional law:
    LicensedMeasuredQuantity → LogMeasuredQuantity only.
    No Candidate, no LCNV, no meaning, no hukm.

    Args:
        quantity: A licensed measured quantity with OPEN gate
        base: Logarithm base (must be positive and ≠ 1)
        shift: Shift value (must be positive)

    Returns:
        LogMeasuredQuantity with preserved unit, trace, residuals, and rank

    Raises:
        LogMeasurementError: If input is not LicensedMeasuredQuantity or constraints violated
    """
    if not isinstance(quantity, LicensedMeasuredQuantity):
        raise LogMeasurementError("log only accepts LicensedMeasuredQuantity")

    _validate_base(base)

    if shift <= 0:
        raise LogMeasurementError("shift must be positive")

    shifted_value = quantity.value + shift
    if shifted_value <= 0:
        raise LogMeasurementError("shifted value must be positive")

    result = Decimal(str(_log(float(shifted_value), float(base))))

    # Extend trace with log operation trace
    extended_trace = quantity.trace_ids + (f"trace:log_quantity:{quantity.quantity_id}",)

    return LogMeasuredQuantity(
        source_quantity_id=quantity.quantity_id,
        log_value=result,
        base=base,
        shift=shift,
        unit=quantity.unit,
        trace_ids=extended_trace,
        residual_ids=quantity.residual_ids,
        rank=quantity.rank,
    )


def inverse_log_quantity(log_quantity_value: LogMeasuredQuantity) -> LicensedMeasuredQuantity:
    """
    Inverse logarithmic measurement.

    Returns the licensed quantity only.
    Does NOT return Candidate, LCNV, Meaning, Ifadah, Hukm, Evidence, or Trace authority.

    Args:
        log_quantity_value: A logarithmically measured quantity

    Returns:
        LicensedMeasuredQuantity with restored value

    Raises:
        LogMeasurementError: If input is not LogMeasuredQuantity or inverse produces negative
    """
    if not isinstance(log_quantity_value, LogMeasuredQuantity):
        raise LogMeasurementError("inverse_log only accepts LogMeasuredQuantity")

    restored = Decimal(str(_pow(float(log_quantity_value.base), float(log_quantity_value.log_value)))) - log_quantity_value.shift

    if restored < 0:
        raise LogMeasurementError("inverse produced negative quantity")

    return LicensedMeasuredQuantity(
        quantity_id=log_quantity_value.source_quantity_id,
        value=restored,
        unit=log_quantity_value.unit,
        gate="OPEN",
        trace_ids=log_quantity_value.trace_ids,
        residual_ids=log_quantity_value.residual_ids,
        rank=log_quantity_value.rank,
    )
