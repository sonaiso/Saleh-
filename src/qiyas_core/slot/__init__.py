"""SlotGeometry foundation for adapter engineering.

This package provides the generic infrastructure for defining slots -
functional positions in linguistic analysis that have:
- Identity (slot_id, slot_family_id, slot_type)
- Domain and boundaries (layer, domain, boundary, direction)
- Roles (participants in slot operations)
- Demand and capability (what slot needs and provides)
- Policies (evidence, wadi, difference, closure, rank, residual, effect, failure, trace)
- Relationships (dependencies, composition, blocking)
- Context requirements
- Output constraints

SlotGeometry is declarative. It defines slot structure but does not:
- Call QiyasKernel
- Produce CandidateSet
- Judge acceptance

Adapters will use SlotGeometry to build QiyasRequest instances.
QiyasKernel remains the only judge.

Architecture:
    SlotGeometry → defines slots (this package)
    LayerAdapter → uses slots to build QiyasRequest
    QiyasKernel → judges requests
"""

from .capability import SlotCapability
from .demand import SlotDemand
from .enums import (
    SlotAmbiguityPolicy,
    SlotBoundary,
    SlotDirection,
    SlotMultiplicity,
    SlotState,
)
from .geometry import SlotGeometry
from .policies import (
    SlotClosurePolicy,
    SlotDifferencePolicy,
    SlotEffectPolicy,
    SlotEffectSpec,
    SlotEvidenceProfile,
    SlotFailurePolicy,
    SlotRankPolicy,
    SlotResidualPolicy,
    SlotTracePolicy,
    SlotWadiPolicy,
)
from .roles import SlotRoleSpec
from .spec import SlotSpec

__all__ = [
    # Enums
    "SlotAmbiguityPolicy",
    "SlotBoundary",
    "SlotDirection",
    "SlotMultiplicity",
    "SlotState",
    # Core structures
    "SlotCapability",
    "SlotDemand",
    "SlotRoleSpec",
    "SlotSpec",
    # Policies
    "SlotClosurePolicy",
    "SlotDifferencePolicy",
    "SlotEffectPolicy",
    "SlotEffectSpec",
    "SlotEvidenceProfile",
    "SlotFailurePolicy",
    "SlotRankPolicy",
    "SlotResidualPolicy",
    "SlotTracePolicy",
    "SlotWadiPolicy",
    # Protocol
    "SlotGeometry",
]
