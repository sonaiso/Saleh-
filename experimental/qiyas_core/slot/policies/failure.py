from dataclasses import dataclass


@dataclass(frozen=True)
class SlotFailurePolicy:
    """Policy for handling slot failures.

    Defines what happens when a slot cannot be filled:
    - Block entire layer
    - Defer to later analysis
    - Try alternative slots
    - Cascade failure back to previous layer
    """
    failure_strategy: str
    fallback_slots: tuple[str, ...]
    propagate_failure: bool
    create_residual: bool

    def __post_init__(self) -> None:
        if not self.failure_strategy:
            raise ValueError("failure_strategy is required")
