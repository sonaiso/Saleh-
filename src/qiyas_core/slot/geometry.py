from typing import Any, Protocol

from .spec import SlotSpec


class SlotGeometry(Protocol):
    """Protocol defining the interface for slot-based operations.

    SlotGeometry is the foundational abstraction that defines how slots
    work across all layers of analysis. This is a generic protocol - specific
    layers will implement their own geometries:
    - LetterSlotGeometry (future)
    - WordSlotGeometry (future)
    - WeightSlotGeometry (future)
    - AmilSlotGeometry (future)
    - SentenceSlotGeometry (future)

    Key Principles:
    1. SlotGeometry does NOT call QiyasKernel
    2. SlotGeometry does NOT produce CandidateSet
    3. SlotGeometry does NOT judge acceptance
    4. SlotGeometry ONLY defines slot structure and provides slot specs

    The execution flow is:
    1. SlotGeometry provides SlotSpec instances
    2. Adapter uses SlotSpec to build QiyasRequest
    3. QiyasKernel judges the request
    4. Adapter produces CandidateSet based on kernel judgment

    This separation ensures:
    - Declarative slot definitions (SlotGeometry)
    - Separate from execution logic (Adapter)
    - Separate from judgment logic (Kernel)
    """

    def slots_for(self, context: dict[str, Any]) -> tuple[SlotSpec, ...]:
        """Return slot specifications for the given context.

        Args:
            context: Analysis context that may influence which slots are relevant

        Returns:
            Tuple of SlotSpec instances applicable to this context

        Note:
            This method returns specifications only. It does not execute
            analysis, build requests, or produce candidates.
        """
        ...
