from dataclasses import dataclass

from .enums import EvidenceRank


@dataclass(frozen=True)
class QiyasNodeRef:
    node_id: str
    node_type: str
    identity_ids: tuple[str, ...]
    trace_ids: tuple[str, ...]
    rank: EvidenceRank

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("node_id is required")
        if not self.node_type:
            raise ValueError("node_type is required")
        if set(self.identity_ids) & set(self.trace_ids):
            raise ValueError("identity_ids and trace_ids must be disjoint")
