import pytest

from qiyas_core.registry import QiyasRegistry
from qiyas_core.validators import ValidationError
from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule
from tests.qiyas_core.helpers import build_rule


def test_registry_rejects_duplicate_rule_id():
    registry = QiyasRegistry()
    rule = build_rule()

    registry.register(rule)

    with pytest.raises(ValueError, match="Duplicate rule_id"):
        registry.register(rule)


def test_registry_rejects_rule_missing_wadi_gates():
    registry = QiyasRegistry()
    incomplete_rule = QiyasRule(
        rule_id="rule:incomplete",
        layer="TestLayer",
        pattern=QiyasPattern.ANALOGY,
        asl_type="AslType",
        far_type="FarType",
        required_effective_wasf=("wasf",),
        required_illah=("illah",),
        required_wadi_gates=(WadiGate.SABAB,),  # Missing 5 gates
        invalidating_differences=("diff",),
        neutral_identity_domain="domain",
        output_candidate_type="Candidate",
        forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
        rank_ceiling=EvidenceRank.QIYAS,
    )

    with pytest.raises(ValidationError, match="Rule must require all six WadiGates"):
        registry.register(incomplete_rule)
