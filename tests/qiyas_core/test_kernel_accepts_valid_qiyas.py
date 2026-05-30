from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.helpers import build_request


def test_kernel_accepts_valid_qiyas():
    result = QiyasKernel().apply(build_request())

    assert len(result.accepted) == 1
    assert result.accepted[0].status == CandidateStatus.ACCEPTED
