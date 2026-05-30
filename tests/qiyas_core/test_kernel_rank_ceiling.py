from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_evidence, build_nodes, build_request, build_rule


def test_kernel_rank_ceiling():
    rule = build_rule(rank_ceiling=EvidenceRank.AHAD)
    asl, far = build_nodes(asl_rank=EvidenceRank.SAMA, far_rank=EvidenceRank.FORM)
    evidence = build_evidence(
        proves=(
            "asl:established",
            "far:determined",
            "wasf:shared_wasf:evidenced",
            "illah:shared_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
        ),
        rank=EvidenceRank.TAWATUR,
    )

    result = QiyasKernel().apply(build_request(rule=rule, asl=asl, far=far, evidence=evidence))

    assert result.candidates[0].status == CandidateStatus.ACCEPTED
    assert result.candidates[0].rank == EvidenceRank.FORM
