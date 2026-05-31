from dataclasses import dataclass

from qiyas_core.enums import EvidenceRank


@dataclass(frozen=True)
class SlotEvidenceProfile:
    """Evidence requirements and policies for a slot.

    Defines what evidence is required, what ranks are acceptable,
    and how to merge evidence from multiple sources.
    """
    rank_floor: EvidenceRank
    rank_ceiling: EvidenceRank
    required_evidence_claims: tuple[str, ...]
    optional_evidence_claims: tuple[str, ...]
    evidence_merge_policy: str

    def __post_init__(self) -> None:
        if self.rank_floor.value > self.rank_ceiling.value:
            raise ValueError("rank_floor cannot exceed rank_ceiling")
        if not self.evidence_merge_policy:
            raise ValueError("evidence_merge_policy is required")


@dataclass(frozen=True)
class SlotRankPolicy:
    """Rank handling during slot operations.

    Specifies minimum required ranks, how to merge ranks from multiple
    sources, and what conditions degrade rank.
    """
    minimum_required_rank: EvidenceRank
    rank_merge_strategy: str
    rank_degradation_factors: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.rank_merge_strategy:
            raise ValueError("rank_merge_strategy is required")
