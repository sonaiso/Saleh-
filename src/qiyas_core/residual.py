from dataclasses import dataclass

from .enums import ResidualEffect, ResidualSeverity


@dataclass(frozen=True)
class Residual:
    residual_type: str
    severity: ResidualSeverity
    effect: ResidualEffect
    message: str
    source_rule_id: str
    layer: str
    trace_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.residual_type:
            raise ValueError("residual_type is required")
        if not self.source_rule_id:
            raise ValueError("source_rule_id is required")
        if not self.layer:
            raise ValueError("layer is required")
