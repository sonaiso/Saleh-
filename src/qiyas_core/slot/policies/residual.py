from dataclasses import dataclass


@dataclass(frozen=True)
class SlotResidualPolicy:
    """Policy for how slots emit residuals.

    Distinguishes between residuals that:
    - Block: Prevent continuation
    - Defer: Require deferral
    - Rank: Lower rank
    - Open: Open other slots
    - Request evidence: Request additional evidence
    """
    blocking_residuals: tuple[str, ...]
    deferring_residuals: tuple[str, ...]
    ranking_residuals: tuple[str, ...]
    opening_residuals: tuple[str, ...]
    evidence_request_residuals: tuple[str, ...]
