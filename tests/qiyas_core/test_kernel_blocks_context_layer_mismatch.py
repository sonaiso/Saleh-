from qiyas_core.kernel import QiyasKernel, QiyasContext
from qiyas_core.enums import CandidateStatus
from tests.qiyas_core.helpers import build_request


def test_kernel_blocks_context_layer_mismatch():
    kernel = QiyasKernel()
    request = build_request()

    # Change the context layer to be different from the rule layer
    request = build_request(
        rule=request.rule,
        asl=request.asl,
        far=request.far,
        evidence=request.evidence,
    )
    mismatched_context = QiyasContext(layer="DifferentLayer")
    mismatched_request = build_request(
        rule=request.rule,
        asl=request.asl,
        far=request.far,
        evidence=request.evidence,
    )
    # Override context
    from dataclasses import replace
    mismatched_request = replace(mismatched_request, context=mismatched_context)

    result = kernel.apply(mismatched_request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    residual_types = {r.residual_type for r in result.residuals}
    assert "context_layer_mismatch" in residual_types
