from dataclasses import dataclass

from .capability import SlotCapability
from .demand import SlotDemand
from .enums import SlotBoundary, SlotDirection, SlotState
from .policies import (
    SlotClosurePolicy,
    SlotDifferencePolicy,
    SlotEffectPolicy,
    SlotEvidenceProfile,
    SlotFailurePolicy,
    SlotRankPolicy,
    SlotResidualPolicy,
    SlotTracePolicy,
    SlotWadiPolicy,
)
from .roles import SlotRoleSpec


@dataclass(frozen=True)
class SlotSpec:
    """Complete specification for a slot in the SlotGeometry system.

    This is the foundational data structure that defines a functional position
    (slot) in linguistic analysis. It aggregates all the policies, constraints,
    and metadata needed to precisely define what a slot is, what it requires,
    what it produces, and how it behaves.

    SlotSpec is declarative - it describes the slot but does not execute
    analysis. Adapters will use SlotSpec to build QiyasRequest instances,
    and QiyasKernel will judge those requests.

    Architecture:
    - SlotGeometry defines slots using SlotSpec
    - LayerAdapter uses SlotSpec to build QiyasRequest
    - QiyasKernel judges the requests

    This ensures:
    - No Adapter builds arbitrary requests
    - All slots follow structural discipline
    - Slot semantics are explicit and verifiable
    """

    # Identity and Classification
    slot_id: str
    slot_family_id: str
    slot_type: str
    layer: str
    domain: str
    subdomain: str | None

    # Geometry
    boundary: SlotBoundary
    direction: SlotDirection
    state: SlotState

    # Roles and Participants
    roles: tuple[SlotRoleSpec, ...]

    # Demand and Capability
    demand: SlotDemand
    capability: SlotCapability

    # Policies
    evidence_profile: SlotEvidenceProfile
    wadi_policy: SlotWadiPolicy
    difference_policy: SlotDifferencePolicy
    closure_policy: SlotClosurePolicy
    rank_policy: SlotRankPolicy
    residual_policy: SlotResidualPolicy
    effect_policy: SlotEffectPolicy
    failure_policy: SlotFailurePolicy
    trace_policy: SlotTracePolicy

    # Relationships with Other Slots
    depends_on_slots: tuple[str, ...]
    opens_slots: tuple[str, ...]
    blocks_slots: tuple[str, ...]
    composes_with: tuple[str, ...]

    # Context Requirements
    required_context_keys: tuple[str, ...]
    optional_context_keys: tuple[str, ...]

    # Outputs
    forbidden_outputs: tuple[str, ...]
    output_candidate_type: str

    def __post_init__(self) -> None:
        if not self.slot_id:
            raise ValueError("slot_id is required")
        if not self.slot_family_id:
            raise ValueError("slot_family_id is required")
        if not self.slot_type:
            raise ValueError("slot_type is required")
        if not self.layer:
            raise ValueError("layer is required")
        if not self.domain:
            raise ValueError("domain is required")
        if not self.roles:
            raise ValueError("At least one role is required")
        if not self.output_candidate_type:
            raise ValueError("output_candidate_type is required")
        if self.forbidden_outputs is None:
            raise ValueError("forbidden_outputs is required (use empty tuple if none)")
