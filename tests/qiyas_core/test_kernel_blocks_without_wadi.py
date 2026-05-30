from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_evidence, build_request


def test_kernel_blocks_without_wadi():
    request = build_request(
        evidence=build_evidence(
            proves=(
                "asl:established",
                "far:determined",
                "wasf:shared_wasf:evidenced",
                "illah:shared_illah:verified",
            )
        )
    )

    result = QiyasKernel().apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "wadi_sabab_failed" for r in result.residuals)
