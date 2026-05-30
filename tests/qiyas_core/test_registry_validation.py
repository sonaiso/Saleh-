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

    with pytest.raises(ValidationError, match="Rule must require exactly the six WadiGates"):
        registry.register(incomplete_rule)


def test_registry_rules_for_layer_returns_only_matching_layer():
    registry = QiyasRegistry()

    # Create rules for different layers
    from dataclasses import replace

    rule_layer1_a = build_rule()
    rule_layer1_b = replace(build_rule(), rule_id="rule:layer1_b")
    rule_layer2 = replace(build_rule(), rule_id="rule:layer2", layer="Layer2")
    rule_layer3 = replace(build_rule(), rule_id="rule:layer3", layer="Layer3")

    registry.register(rule_layer1_a)
    registry.register(rule_layer1_b)
    registry.register(rule_layer2)
    registry.register(rule_layer3)

    # Test filtering by layer
    layer1_rules = registry.rules_for_layer("KernelTest")
    assert len(layer1_rules) == 2
    assert set(r.rule_id for r in layer1_rules) == {"rule:test", "rule:layer1_b"}

    layer2_rules = registry.rules_for_layer("Layer2")
    assert len(layer2_rules) == 1
    assert layer2_rules[0].rule_id == "rule:layer2"

    layer3_rules = registry.rules_for_layer("Layer3")
    assert len(layer3_rules) == 1
    assert layer3_rules[0].rule_id == "rule:layer3"

    # Test non-existent layer
    nonexistent_rules = registry.rules_for_layer("NonExistent")
    assert len(nonexistent_rules) == 0
