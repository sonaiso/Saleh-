from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_evidence, build_nodes, build_request, build_rule


def test_kernel_rank_ceiling():
    rule = build_rule(rank_ceiling=EvidenceRank.INDIVIDUAL_REPORT)
    asl, far = build_nodes(asl_rank=EvidenceRank.DIRECT_HEARING, far_rank=EvidenceRank.FORMAL_STRUCTURE)
    evidence = build_evidence(
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
        ),
        rank=EvidenceRank.MASS_TRANSMISSION,
    )

    result = QiyasKernel().apply(build_request(rule=rule, asl=asl, far=far, evidence=evidence))

    assert result.candidates[0].status == CandidateStatus.ACCEPTED
    assert result.candidates[0].rank == EvidenceRank.FORMAL_STRUCTURE
