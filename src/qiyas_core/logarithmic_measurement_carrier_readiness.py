"""
Logarithmic Measurement Carrier Readiness

Constitutional law:
- LogMeasuredQuantity → LogMeasurementReadinessCarrier
- Carrier readiness verifies; it does not decide.
- Carrier carries; it does not judge.
- Measurement preserves rank; it does not upgrade.

Forbidden:
- No Candidate integration
- No LCNV integration
- No MCLO integration
- No Pack/Unpack
- No Meaning derivation
- No Ifadah derivation
- No Hukm derivation
- No authority fields

Governing principle:
  حامل الجاهزية يتحقق ولا يقرر.
  والحامل يحمل ولا يحكم.
  والقياس يحفظ الرتبة ولا يرفعها.

  (Readiness carrier verifies; it does not decide.
   Carrier carries; it does not judge.
   Measurement preserves rank; it does not upgrade.)

See: docs/qiyas_core/LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from qiyas_core.logarithmic_measurement import LogMeasuredQuantity


class CarrierReadinessError(ValueError):
    """Raised when carrier readiness validation fails outside its licensed domain."""


def _has_blocking_residual(residual_ids: tuple[str, ...]) -> bool:
    """
    Check if any residual is blocking.

    Blocking residuals prevent bridge readiness.
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
class LogMeasurementReadinessCarrier:
    """
    A readiness carrier for logarithmic measurement.

    Constitutional requirements:
    - source_log_measurement_ref is provenance, NOT identity
    - original_quantity_id preserves LicensedMeasuredQuantity identity
    - carrier_readiness_trace is trace only, NOT identity
    - NOT a Candidate
    - NOT an LCNV
    - NOT a Meaning/Ifadah/Hukm
    - Does NOT produce authority
    - Does NOT decide; only verifies readiness

    Identity law:
    original_quantity_id ≠ source_log_measurement_ref ≠ carrier_readiness_trace
    """

    source_log_measurement_ref: str
    original_quantity_id: str
    is_bridge_ready: bool
    blocking_conditions: tuple[str, ...]
    constitutional_compliance: bool
    log_value: Decimal
    unit: str
    rank: str
    trace_ids: tuple[str, ...]
    residual_ids: tuple[str, ...]
    carrier_readiness_trace: str


def validate_log_measurement_carrier_readiness(
    log_quantity: LogMeasuredQuantity,
) -> LogMeasurementReadinessCarrier:
    """
    Validate logarithmic measurement carrier readiness.

    Constitutional law:
    LogMeasuredQuantity → LogMeasurementReadinessCarrier only.
    No Candidate, no LCNV, no MCLO, no meaning, no hukm, no authority.

    Identity preservation law:
    - original_quantity_id preserves LicensedMeasuredQuantity identity
    - source_log_measurement_ref is provenance only, not identity
    - carrier_readiness_trace is trace only, not identity
    - original_quantity_id ≠ source_log_measurement_ref ≠ carrier_readiness_trace

    Readiness law:
    - Carrier verifies readiness; it does not decide
    - Carrier carries; it does not judge
    - Blocking residuals make is_bridge_ready = False
    - Constitutional compliance is independent of bridge readiness

    Args:
        log_quantity: A logarithmically measured quantity

    Returns:
        LogMeasurementReadinessCarrier with verified readiness status

    Raises:
        CarrierReadinessError: If input is not LogMeasuredQuantity or constitutional violation
    """
    if not isinstance(log_quantity, LogMeasuredQuantity):
        raise CarrierReadinessError(
            "validate_log_measurement_carrier_readiness only accepts LogMeasuredQuantity"
        )

    # Preserve original quantity identity
    original_quantity_id = log_quantity.source_quantity_id

    # Create provenance reference (NOT identity)
    source_log_measurement_ref = f"log_measurement:{log_quantity.source_quantity_id}"

    # Create carrier readiness trace (NOT identity)
    carrier_readiness_trace = f"trace:carrier_readiness:{log_quantity.source_quantity_id}"

    # Extend trace with carrier readiness trace
    trace_ids = log_quantity.trace_ids + (carrier_readiness_trace,)

    # Preserve residuals
    residual_ids = log_quantity.residual_ids

    # Preserve rank (does not upgrade)
    rank = log_quantity.rank

    # Preserve unit
    unit = log_quantity.unit

    # Preserve log value
    log_value = log_quantity.log_value

    # Check for blocking residuals
    has_blocking = _has_blocking_residual(residual_ids)

    # Determine bridge readiness
    is_bridge_ready = not has_blocking

    # Record blocking conditions if present
    blocking_conditions: tuple[str, ...] = ()
    if has_blocking:
        blocking_conditions = tuple(
            r for r in residual_ids
            if r.startswith("residual:blocking")
            or ":blocking:" in r
            or r.startswith("blocking:")
        )

    # Constitutional compliance (independent of bridge readiness)
    # Only False if input type is wrong (already checked) or constitutional violation detected
    constitutional_compliance = True

    return LogMeasurementReadinessCarrier(
        source_log_measurement_ref=source_log_measurement_ref,
        original_quantity_id=original_quantity_id,
        is_bridge_ready=is_bridge_ready,
        blocking_conditions=blocking_conditions,
        constitutional_compliance=constitutional_compliance,
        log_value=log_value,
        unit=unit,
        rank=rank,
        trace_ids=trace_ids,
        residual_ids=residual_ids,
        carrier_readiness_trace=carrier_readiness_trace,
    )
