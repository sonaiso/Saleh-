from dataclasses import dataclass


@dataclass(frozen=True)
class SlotEffectSpec:
    """Specification for a single slot effect.

    Describes what happens when a slot transitions to a particular state.
    """
    effect_type: str
    target: str
    conditions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.effect_type:
            raise ValueError("effect_type is required")
        if not self.target:
            raise ValueError("target is required")


@dataclass(frozen=True)
class SlotEffectPolicy:
    """Policy for slot effects based on state.

    Defines what effects occur when a slot:
    - Succeeds (fills successfully)
    - Partially fills
    - Gets deferred
    """
    on_success: tuple[SlotEffectSpec, ...]
    on_partial: tuple[SlotEffectSpec, ...]
    on_deferred: tuple[SlotEffectSpec, ...]
