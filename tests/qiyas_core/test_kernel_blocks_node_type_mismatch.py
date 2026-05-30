from qiyas_core.kernel import QiyasKernel
from qiyas_core.enums import CandidateStatus
from tests.qiyas_core.helpers import build_request, build_rule, build_nodes


def test_kernel_blocks_asl_type_mismatch():
    kernel = QiyasKernel()

    # Create nodes with correct type
    asl, far = build_nodes()

    # Create a rule that expects a different asl_type
    rule = build_rule()
    from dataclasses import replace
    rule = replace(rule, asl_type="DifferentAslType")

    request = build_request(rule=rule, asl=asl, far=far)
    result = kernel.apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    residual_types = {r.residual_type for r in result.residuals}
    assert "asl_type_mismatch" in residual_types


def test_kernel_blocks_far_type_mismatch():
    kernel = QiyasKernel()

    # Create nodes with correct type
    asl, far = build_nodes()

    # Create a rule that expects a different far_type
    rule = build_rule()
    from dataclasses import replace
    rule = replace(rule, far_type="DifferentFarType")

    request = build_request(rule=rule, asl=asl, far=far)
    result = kernel.apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    residual_types = {r.residual_type for r in result.residuals}
    assert "far_type_mismatch" in residual_types
