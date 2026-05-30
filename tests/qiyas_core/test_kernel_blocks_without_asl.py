from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_evidence, build_request


def test_kernel_blocks_without_asl():
    request = build_request(
        evidence=build_evidence(
            proves=(
                "far:determined",
                "wasf:shared_wasf:evidenced",
                "illah:shared_illah:verified",
                "wadi:sabab:established",
            )
        )
    )

    result = QiyasKernel().apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "asl_not_established" for r in result.residuals)
