from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_evidence, build_nodes, build_request


def test_kernel_blocks_identity_trace_conflict():
    asl, far = build_nodes(far_trace=("id:asl",))
    request = build_request(
        asl=asl,
        far=far,
        evidence=build_evidence(
            proves=(
                "asl:established",
                "far:determined",
                "wasf:shared_wasf:evidenced",
                "illah:shared_illah:verified",
                "wadi:sabab:established",
            )
        ),
    )

    result = QiyasKernel().apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "identity_trace_conflict" for r in result.residuals)
