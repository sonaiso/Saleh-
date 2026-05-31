from dataclasses import dataclass


@dataclass(frozen=True)
class SlotWadiPolicy:
    """Wadi six-gate policy at the slot level.

    Aligns with the six-gate Wadi framework:
    - sabab: Causes/reasons for slot existence
    - shart: Conditions for slot validity
    - mani: Blockers that prevent slot operation
    - sihha: Correctness conditions
    - fasad: Corruption conditions
    - butlan: Nullification conditions
    """
    sabab_conditions: tuple[str, ...]
    shart_conditions: tuple[str, ...]
    mani_conditions: tuple[str, ...]
    sihha_conditions: tuple[str, ...]
    fasad_conditions: tuple[str, ...]
    butlan_conditions: tuple[str, ...]
