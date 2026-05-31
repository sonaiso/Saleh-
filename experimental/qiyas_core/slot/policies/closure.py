from dataclasses import dataclass


@dataclass(frozen=True)
class SlotClosurePolicy:
    """Policy for when and how slots close.

    Defines the closure type (internal, external, deferred, contextual),
    what evidence is needed, and what conditions trigger different outcomes.
    """
    closure_type: str
    requires_evidence: tuple[str, ...]
    deferred_if: tuple[str, ...]
    blocked_if: tuple[str, ...]
    closes_on: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.closure_type:
            raise ValueError("closure_type is required")
