from dataclasses import dataclass


@dataclass(frozen=True)
class SlotTracePolicy:
    """Policy for trace handling in slots.

    Defines how traces are preserved, merged, and propagated through
    slot operations.
    """
    preserve_input_trace: bool
    add_slot_trace: bool
    add_evidence_trace: bool
    add_residual_trace: bool
    trace_merge_strategy: str

    def __post_init__(self) -> None:
        if not self.trace_merge_strategy:
            raise ValueError("trace_merge_strategy is required")
