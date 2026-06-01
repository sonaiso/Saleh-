from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_evidence, build_request


def test_kernel_blocks_without_asl():
    request = build_request(
        evidence=build_evidence(
            proves=(
                "فرع:determined",
                "وصف:shared_wasf:evidenced",
                "علة:shared_illah:verified",
                "وادي:cause:established",
            )
        )
    )

    result = QiyasKernel().apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "asl_not_established" for r in result.residuals)
