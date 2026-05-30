from dataclasses import dataclass

from .enums import CandidateStatus, EvidenceRank
from .residual import Residual


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    candidate_type: str
    status: CandidateStatus
    layer: str
    source_rule_id: str

    asl_id: str
    far_id: str

    identity_ids: tuple[str, ...]
    rank: EvidenceRank
    residuals: tuple[Residual, ...]
    trace_ids: tuple[str, ...]

    output_flags: frozenset[str]

    def __post_init__(self) -> None:
        forbidden_runtime_flags = {
            "HukmCandidate",
            "RealityClaim",
            "FinalMeaning",
            "FinalCaseJudgment",
        }
        if self.output_flags & forbidden_runtime_flags:
            raise ValueError(
                f"Candidate contains forbidden output flags: "
                f"{self.output_flags & forbidden_runtime_flags}"
            )


@dataclass(frozen=True)
class CandidateSet:
    set_id: str
    layer: str
    candidates: tuple[Candidate, ...]
    residuals: tuple[Residual, ...]
    trace_ids: tuple[str, ...]

    @property
    def accepted(self) -> tuple[Candidate, ...]:
        return tuple(c for c in self.candidates if c.status == CandidateStatus.ACCEPTED)

    @property
    def deferred(self) -> tuple[Candidate, ...]:
        return tuple(c for c in self.candidates if c.status == CandidateStatus.DEFERRED)

    @property
    def blocked(self) -> tuple[Candidate, ...]:
        return tuple(c for c in self.candidates if c.status == CandidateStatus.BLOCKED)
