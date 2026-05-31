from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_request, build_rule


def test_kernel_forbidden_outputs():
    rule = build_rule(forbidden_outputs=("HukmCandidate", "RealityClaim"))

    result = QiyasKernel().apply(build_request(rule=rule))

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "forbidden_outputs_incomplete" for r in result.residuals)
