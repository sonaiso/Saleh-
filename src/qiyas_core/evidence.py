from dataclasses import dataclass

from .enums import EvidenceRank


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source_layer: str
    proves: tuple[str, ...]
    rank: EvidenceRank
    trace_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.evidence_id:
            raise ValueError("evidence_id is required")
        if not self.source_layer:
            raise ValueError("source_layer is required")
        if not self.proves:
            raise ValueError("evidence must prove at least one claim")
        if not self.trace_ids:
            raise ValueError("evidence must have trace_ids")


@dataclass(frozen=True)
class EvidenceSet:
    items: tuple[Evidence, ...]

    def proves(self, claim: str) -> bool:
        return any(claim in item.proves for item in self.items)

    def all_trace_ids(self) -> tuple[str, ...]:
        traces: list[str] = []
        for item in self.items:
            traces.extend(item.trace_ids)
        return tuple(traces)

    def minimum_rank(self) -> EvidenceRank:
        if not self.items:
            return EvidenceRank.NO_EVIDENCE
        return min((item.rank for item in self.items), key=lambda r: r.value)
