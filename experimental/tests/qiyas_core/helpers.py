from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.kernel import QiyasContext, QiyasRequest
from qiyas_core.node import QiyasNodeRef
from qiyas_core.rule import QiyasRule


def build_rule(*, forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"), rank_ceiling=EvidenceRank.ANALOGICAL):
    return QiyasRule(
        rule_id="rule:test",
        layer="KernelTest",
        pattern=QiyasPattern.ANALOGY,
        asl_type="AslType",
        far_type="FarType",
        required_effective_wasf=("shared_wasf",),
        required_illah=("shared_illah",),
        required_wadi_gates=(
            WadiGate.CAUSE,
            WadiGate.CONDITION,
            WadiGate.OBSTACLE,
            WadiGate.VALIDITY,
            WadiGate.CORRUPTION,
            WadiGate.NULLITY,
        ),
        invalidating_differences=("blocking_diff",),
        neutral_identity_domain="domain",
        output_candidate_type="KernelCandidate",
        forbidden_outputs=forbidden_outputs,
        rank_ceiling=rank_ceiling,
    )


def build_nodes(*, asl_identity=("id:asl",), far_identity=("id:far",), asl_trace=("trace:asl",), far_trace=("trace:far",), asl_rank=EvidenceRank.ANALOGICAL, far_rank=EvidenceRank.ANALOGICAL):
    asl = QiyasNodeRef(
        node_id="اصل:1",
        node_type="AslType",
        identity_ids=asl_identity,
        trace_ids=asl_trace,
        rank=asl_rank,
    )
    far = QiyasNodeRef(
        node_id="فرع:1",
        node_type="FarType",
        identity_ids=far_identity,
        trace_ids=far_trace,
        rank=far_rank,
    )
    return asl, far


def build_evidence(*, proves=(), rank=EvidenceRank.ANALOGICAL):
    return EvidenceSet(
        items=(
            Evidence(
                evidence_id="ev:1",
                source_layer="KernelTest",
                proves=proves,
                rank=rank,
                trace_ids=("trace:ev",),
            ),
        )
    )


def build_request(*, rule=None, asl=None, far=None, evidence=None):
    rule = rule or build_rule()
    asl, far = (asl, far) if asl and far else build_nodes()
    evidence = evidence or build_evidence(
        proves=(
            "اصل:established",
            "فرع:determined",
            "وصف:shared_wasf:evidenced",
            "علة:shared_illah:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        )
    )
    return QiyasRequest(
        rule=rule,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer=rule.layer),
    )
