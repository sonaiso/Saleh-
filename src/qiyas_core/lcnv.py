"""Layered Compressed Numeric Value (LCNV) — Minimal Isolated Runtime

Constitutional law (PR #52):
  Unpack(Pack(c)) ≠ Candidate(c)
  Unpack(Pack(c)) = EncodedStateProjection(c)

CandidateAuthority requires:
  Validate(EncodedStateProjection + CandidateStore + EvidenceStore + TraceStore + ResidualStore)

Forbidden:
  - LCNV producing CandidateAuthority
  - LCNV producing Meaning/Ifadah/Hukm
  - LCNV producing RealityClaim
  - LCNV integration with SlotGeometry (Track A)
  - LCNV integration with LogarithmicMeasurement (Track C)
  - semantic_force ≠ FORBIDDEN

Governing principle:
  الرقم لا ينتج معرفة
  (Number does not produce knowledge)

  Candidate هو مصدر السلطة.
  LCNV أثر مضغوط.
  الأثر لا يصبح أصلًا.

  (Candidate is the source of authority.
   LCNV is compressed trace.
   Trace does not become origin.)

Track: LCNV (Track B)
See: docs/qiyas_core/LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


class LCNVError(ValueError):
    """Raised when LCNV operations violate constitutional constraints."""


# Gate state indicators
CLOSED = "CLOSED"  # Gate not opened (CLOSED ≠ 0)
GateState = Literal["CLOSED"] | int


@dataclass(frozen=True)
class GateStateBundle:
    """
    Gate state encoding from LCNV unpacking.

    NOT a Candidate.
    NOT authoritative without validation + stores.

    Constitutional law:
      GateStateBundle is state projection, NOT epistemological authority.
    """

    # Signifier-only layer (MCLO block)
    mclo_state: GateState

    # Future layers (reserved, all CLOSED in minimal runtime)
    lexical_state: GateState = CLOSED
    meaning_state: GateState = CLOSED
    binding_state: GateState = CLOSED
    mutabaqah_state: GateState = CLOSED
    tadammun_state: GateState = CLOSED
    iltizam_state: GateState = CLOSED

    # Rank and residuals (must be preserved)
    rank_ceiling: int | None = None
    residual_count: int = 0
    has_blocking_residuals: bool = False

    def __post_init__(self) -> None:
        """Validate constitutional constraints."""
        # CLOSED ≠ 0
        if self.mclo_state == 0:
            raise LCNVError(
                "MCLO state cannot be 0 (CLOSED ≠ 0). "
                "Use CLOSED constant for unopened gates."
            )


@dataclass(frozen=True)
class EncodedStateProjection:
    """
    Encoded state projection recovered from LCNV unpacking.

    NOT a Candidate.
    NOT authoritative.

    Constitutional requirement:
      Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)

    For authoritative restoration:
      CandidateAuthority = Validate(
          EncodedStateProjection,
          CandidateStore,
          EvidenceStore,
          TraceStore,
          ResidualStore
      )
    """

    gate_states: GateStateBundle
    source_layer_id: str
    encoding_format: str  # e.g., "mclo_only_v1"

    # Trace reference (NOT full trace, only reference)
    trace_ref: str | None = None

    def __post_init__(self) -> None:
        """Validate projection constraints."""
        if not self.source_layer_id:
            raise LCNVError("EncodedStateProjection requires source_layer_id")

        if not self.encoding_format:
            raise LCNVError("EncodedStateProjection requires encoding_format")


@dataclass(frozen=True)
class LCNV:
    """
    Layered Compressed Numeric Value.

    Reversible gate-aware numeric encoding of licensed qiyas layer state.

    Constitutional laws:
      1. LCNV is NOT a source of truth (Candidate is)
      2. LCNV is NOT a meaning derivation system
      3. LCNV is NOT a hukm inference system
      4. semantic_force = FORBIDDEN
      5. Unpack(Pack(c)) = EncodedStateProjection, NOT Candidate

    LCNV encodes state.
    LCNV does NOT create state.
    LCNV does NOT create authority.
    """

    # Numeric blocks (layered encoding)
    mclo_block: int | Literal["CLOSED"]
    lexical_block: int | Literal["CLOSED"] = CLOSED
    meaning_block: int | Literal["CLOSED"] = CLOSED
    binding_block: int | Literal["CLOSED"] = CLOSED
    mutabaqah_block: int | Literal["CLOSED"] = CLOSED
    tadammun_block: int | Literal["CLOSED"] = CLOSED
    iltizam_block: int | Literal["CLOSED"] = CLOSED

    # Rank and residual encoding (must preserve)
    rank_block: int | None = None
    residual_block: int = 0

    # Metadata
    encoding_version: str = "mclo_only_v1"
    source_layer: str | None = None

    def __post_init__(self) -> None:
        """Validate LCNV constitutional constraints."""
        # CLOSED ≠ 0 validation
        if self.mclo_block == 0:
            raise LCNVError(
                "MCLO block cannot be 0 (CLOSED ≠ 0). "
                "Use CLOSED constant for unopened gates."
            )

        # Block ordering dependency: no higher layers before binding
        if self.binding_block == CLOSED:
            if self.mutabaqah_block != CLOSED:
                raise LCNVError(
                    "Cannot have Mutabaqah block without Binding block "
                    "(Law 5: Block Ordering Dependency)"
                )
            if self.tadammun_block != CLOSED:
                raise LCNVError(
                    "Cannot have Tadammun block without Binding block "
                    "(Law 5: Block Ordering Dependency)"
                )
            if self.iltizam_block != CLOSED:
                raise LCNVError(
                    "Cannot have Iltizam block without Binding block "
                    "(Law 5: Block Ordering Dependency)"
                )

    def to_compact_int(self) -> int:
        """
        Serialize LCNV to compact integer representation.

        WARNING: This is lossy for minimal runtime (only MCLO block).
        Full implementation would pack all blocks.

        Returns:
            Compact integer encoding (current: MCLO block only)
        """
        if self.mclo_block == CLOSED:
            raise LCNVError("Cannot serialize LCNV with CLOSED MCLO block")

        # Minimal runtime: pack only MCLO block
        # Full runtime would pack all layers with bit shifting
        return int(self.mclo_block)

    @classmethod
    def from_compact_int(
        cls,
        value: int,
        encoding_version: str = "mclo_only_v1",
        source_layer: str | None = None,
    ) -> LCNV:
        """
        Deserialize LCNV from compact integer.

        WARNING: Minimal runtime implementation (MCLO only).

        Args:
            value: Compact integer encoding
            encoding_version: Encoding format identifier
            source_layer: Optional source layer identifier

        Returns:
            LCNV instance with MCLO block filled, others CLOSED
        """
        if value <= 0:
            raise LCNVError(
                f"Invalid LCNV compact value {value}. "
                "Must be positive integer (CLOSED ≠ 0)."
            )

        # Minimal runtime: unpack only MCLO block
        return cls(
            mclo_block=value,
            encoding_version=encoding_version,
            source_layer=source_layer,
        )


def pack(
    mclo_value: int,
    source_layer_id: str,
    rank_ceiling: int | None = None,
    residual_count: int = 0,
    has_blocking_residuals: bool = False,
) -> LCNV:
    """
    Pack licensed state into LCNV encoding.

    Minimal runtime: packs MCLO (signifier-only) block only.

    Constitutional constraint:
      pack() accepts licensed state AFTER qiyas transition,
      NOT as source of truth creation.

    Args:
        mclo_value: MCLO (signifier-only) numeric encoding
        source_layer_id: Layer that produced this state
        rank_ceiling: Optional rank ceiling (meet semantics)
        residual_count: Number of residuals
        has_blocking_residuals: Whether blocking residuals exist

    Returns:
        LCNV instance

    Raises:
        LCNVError: If mclo_value violates constraints
    """
    if mclo_value <= 0:
        raise LCNVError(
            f"Invalid MCLO value {mclo_value}. "
            "Must be positive integer (CLOSED ≠ 0)."
        )

    if not source_layer_id:
        raise LCNVError("pack() requires source_layer_id")

    return LCNV(
        mclo_block=mclo_value,
        rank_block=rank_ceiling,
        residual_block=residual_count,
        source_layer=source_layer_id,
    )


def unpack(lcnv: LCNV) -> EncodedStateProjection:
    """
    Unpack LCNV to EncodedStateProjection.

    Constitutional law (PR #52):
      Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)

    Unpack does NOT restore:
      - CandidateAuthority
      - Evidence
      - Full Trace
      - Meaning
      - Ifadah
      - Hukm

    Unpack ONLY restores:
      - GateStateBundle (gate state encoding)
      - Trace reference (not full trace)

    For authoritative restoration:
      CandidateAuthority = Validate(
          unpack(lcnv),
          CandidateStore,
          EvidenceStore,
          TraceStore,
          ResidualStore
      )

    Args:
        lcnv: LCNV instance to unpack

    Returns:
        EncodedStateProjection (NOT Candidate)
    """
    # Extract gate states
    gate_states = GateStateBundle(
        mclo_state=lcnv.mclo_block,
        lexical_state=lcnv.lexical_block,
        meaning_state=lcnv.meaning_block,
        binding_state=lcnv.binding_block,
        mutabaqah_state=lcnv.mutabaqah_block,
        tadammun_state=lcnv.tadammun_block,
        iltizam_state=lcnv.iltizam_block,
        rank_ceiling=lcnv.rank_block,
        residual_count=lcnv.residual_block,
        has_blocking_residuals=False,  # Future: decode from residual_block
    )

    # Build trace reference (not full trace)
    trace_ref = None
    if lcnv.source_layer:
        trace_ref = f"lcnv_trace:{lcnv.source_layer}:{lcnv.mclo_block}"

    # Return EncodedStateProjection, NOT Candidate
    return EncodedStateProjection(
        gate_states=gate_states,
        source_layer_id=lcnv.source_layer or "unknown",
        encoding_format=lcnv.encoding_version,
        trace_ref=trace_ref,
    )


# Constitutional export
__all__ = [
    "LCNV",
    "EncodedStateProjection",
    "GateStateBundle",
    "pack",
    "unpack",
    "LCNVError",
    "CLOSED",
]
