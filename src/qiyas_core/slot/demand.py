from dataclasses import dataclass


@dataclass(frozen=True)
class SlotDemand:
    """Specifies what a slot requires to be fulfilled.

    Demand represents the needs of a slot - what evidence, capabilities,
    and conditions must be satisfied for the slot to accept a candidate.
    """
    demand_type: str
    required_evidence: tuple[str, ...]
    required_capabilities: tuple[str, ...]
    optional_evidence: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.demand_type:
            raise ValueError("demand_type is required")
