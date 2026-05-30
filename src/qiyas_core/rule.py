from dataclasses import dataclass

from .enums import EvidenceRank, QiyasPattern, WadiGate


@dataclass(frozen=True)
class QiyasRule:
    rule_id: str
    layer: str
    pattern: QiyasPattern

    asl_type: str
    far_type: str

    required_effective_wasf: tuple[str, ...]
    required_illah: tuple[str, ...]
    required_wadi_gates: tuple[WadiGate, ...]

    invalidating_differences: tuple[str, ...]

    neutral_identity_domain: str
    output_candidate_type: str
    forbidden_outputs: tuple[str, ...]

    rank_ceiling: EvidenceRank

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id is required")
        if not self.layer:
            raise ValueError("layer is required")
        if not self.asl_type:
            raise ValueError("asl_type is required")
        if not self.far_type:
            raise ValueError("far_type is required")
        if not self.required_effective_wasf:
            raise ValueError("required_effective_wasf is required")
        if not self.required_illah:
            raise ValueError("required_illah is required")
        if not self.required_wadi_gates:
            raise ValueError("required_wadi_gates is required")
        if not self.neutral_identity_domain:
            raise ValueError("neutral_identity_domain is required")
        if not self.output_candidate_type:
            raise ValueError("output_candidate_type is required")
        if not self.forbidden_outputs:
            raise ValueError("forbidden_outputs is required")
