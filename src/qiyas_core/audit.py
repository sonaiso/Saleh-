from dataclasses import dataclass

from .enums import EvidenceRank, ResidualEffect
from .residual import Residual


@dataclass(frozen=True)
class QiyasAudit:
    blocked: bool
    deferred: bool
    residuals: tuple[Residual, ...]
    trace_ids: tuple[str, ...]
    rank_ceiling: EvidenceRank | None

    @staticmethod
    def empty() -> "QiyasAudit":
        return QiyasAudit(
            blocked=False,
            deferred=False,
            residuals=(),
            trace_ids=(),
            rank_ceiling=None,
        )

    def add_residual(self, residual: Residual) -> "QiyasAudit":
        return QiyasAudit(
            blocked=self.blocked or residual.effect == ResidualEffect.BLOCK,
            deferred=self.deferred or residual.effect == ResidualEffect.DEFER,
            residuals=self.residuals + (residual,),
            trace_ids=self.trace_ids + residual.trace_ids,
            rank_ceiling=self.rank_ceiling,
        )

    def with_rank_ceiling(self, rank: EvidenceRank) -> "QiyasAudit":
        return QiyasAudit(
            blocked=self.blocked,
            deferred=self.deferred,
            residuals=self.residuals,
            trace_ids=self.trace_ids,
            rank_ceiling=rank,
        )
