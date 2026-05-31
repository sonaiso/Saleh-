"""Rule factories for constitutional tests."""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule


ALL_WADI_GATES = (
    WadiGate.SABAB,
    WadiGate.SHART,
    WadiGate.MANI,
    WadiGate.SIHHA,
    WadiGate.FASAD,
    WadiGate.BUTLAN,
)


def make_minimal_rule(
    rule_id: str = "rule:test:minimal",
    layer: str = "TestLayer",
    *,
    pattern: QiyasPattern = QiyasPattern.COMPOSITION_FIT,
    asl_type: str = "AslType",
    far_type: str = "FarType",
    output_candidate_type: str = "TestCandidate",
    forbidden_outputs: tuple[str, ...] = (
        "SyllableCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ),
    rank_ceiling: EvidenceRank = EvidenceRank.QIYAS,
) -> QiyasRule:
    """Create a constitutionally valid minimal rule.

    Args:
        rule_id: Unique rule identifier
        layer: Layer name
        pattern: QiyasPattern
        asl_type: Type of asl candidate
        far_type: Type of far candidate
        output_candidate_type: Type of output candidate
        forbidden_outputs: Forbidden output types
        rank_ceiling: Maximum evidence rank

    Returns:
        QiyasRule with all constitutional requirements satisfied
    """
    return QiyasRule(
        rule_id=rule_id,
        layer=layer,
        pattern=pattern,
        asl_type=asl_type,
        far_type=far_type,
        required_effective_wasf=("test_wasf",),
        required_illah=("test_illah",),
        required_wadi_gates=ALL_WADI_GATES,
        invalidating_differences=("test_diff",),
        neutral_identity_domain="test_domain",
        output_candidate_type=output_candidate_type,
        forbidden_outputs=forbidden_outputs,
        rank_ceiling=rank_ceiling,
    )


def make_rule_missing_wadi(
    missing_gate: str,
    rule_id: str = "rule:test:missing_wadi",
) -> QiyasRule:
    """Create a rule with a missing WadiGate (for negative tests).

    Args:
        missing_gate: Name of the gate to omit ("sabab", "shart", etc.)
        rule_id: Unique rule identifier

    Returns:
        QiyasRule missing one WadiGate (constitutionally invalid)
    """
    gate_map = {
        "sabab": WadiGate.SABAB,
        "shart": WadiGate.SHART,
        "mani": WadiGate.MANI,
        "sihha": WadiGate.SIHHA,
        "fasad": WadiGate.FASAD,
        "butlan": WadiGate.BUTLAN,
    }

    if missing_gate not in gate_map:
        raise ValueError(f"Unknown gate: {missing_gate}")

    gates = tuple(g for g in ALL_WADI_GATES if g != gate_map[missing_gate])

    return QiyasRule(
        rule_id=rule_id,
        layer="TestLayer",
        pattern=QiyasPattern.COMPOSITION_FIT,
        asl_type="AslType",
        far_type="FarType",
        required_effective_wasf=("test_wasf",),
        required_illah=("test_illah",),
        required_wadi_gates=gates,
        invalidating_differences=("test_diff",),
        neutral_identity_domain="test_domain",
        output_candidate_type="TestCandidate",
        forbidden_outputs=("HigherCandidate",),
        rank_ceiling=EvidenceRank.QIYAS,
    )


def make_rule_extra_wadi(
    rule_id: str = "rule:test:extra_wadi",
) -> QiyasRule:
    """Create a rule with an extra WadiGate (for negative tests).

    Args:
        rule_id: Unique rule identifier

    Returns:
        QiyasRule with 7 WadiGates (constitutionally invalid)

    Note:
        Since WadiGate enum only has 6 values, this will include
        a duplicate gate to simulate "extra" gate scenario.
    """
    # Duplicate one gate to create 7 gates
    gates = ALL_WADI_GATES + (WadiGate.SABAB,)

    return QiyasRule(
        rule_id=rule_id,
        layer="TestLayer",
        pattern=QiyasPattern.COMPOSITION_FIT,
        asl_type="AslType",
        far_type="FarType",
        required_effective_wasf=("test_wasf",),
        required_illah=("test_illah",),
        required_wadi_gates=gates,
        invalidating_differences=("test_diff",),
        neutral_identity_domain="test_domain",
        output_candidate_type="TestCandidate",
        forbidden_outputs=("HigherCandidate",),
        rank_ceiling=EvidenceRank.QIYAS,
    )


def make_rule_empty_forbidden(
    rule_id: str = "rule:test:empty_forbidden",
) -> QiyasRule:
    """Create a rule with empty forbidden_outputs (for negative tests).

    Args:
        rule_id: Unique rule identifier

    Returns:
        QiyasRule with empty forbidden_outputs (constitutionally invalid for qiyas layers)
    """
    return QiyasRule(
        rule_id=rule_id,
        layer="TestLayer",
        pattern=QiyasPattern.COMPOSITION_FIT,
        asl_type="AslType",
        far_type="FarType",
        required_effective_wasf=("test_wasf",),
        required_illah=("test_illah",),
        required_wadi_gates=ALL_WADI_GATES,
        invalidating_differences=("test_diff",),
        neutral_identity_domain="test_domain",
        output_candidate_type="TestCandidate",
        forbidden_outputs=(),  # Empty - constitutional violation
        rank_ceiling=EvidenceRank.QIYAS,
    )
