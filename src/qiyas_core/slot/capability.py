from dataclasses import dataclass


@dataclass(frozen=True)
class SlotCapability:
    """Specifies what a slot provides when successfully filled.

    Capability represents what a slot contributes - what evidence it can
    provide and what demands it can satisfy.
    """
    capability_type: str
    provides_evidence: tuple[str, ...]
    satisfies_demands: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.capability_type:
            raise ValueError("capability_type is required")
