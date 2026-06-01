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
            )
        ),
    )

    result = QiyasKernel().apply(request)

    assert result.candidates[0].status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "identity_trace_conflict" for r in result.residuals)


def test_blocked_candidate_from_identity_conflict_has_disjoint_ids():
    """Regression test: blocked candidates must have structurally valid disjoint identity_ids and trace_ids.

    The conflict is reported in residuals, not by violating the Candidate invariant.
    """
    asl, far = build_nodes(far_trace=("id:asl",))
    request = build_request(
        asl=asl,
        far=far,
        evidence=build_evidence(
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
            )
        ),
    )

    result = QiyasKernel().apply(request)
    candidate = result.candidates[0]

    # Verify the candidate is blocked due to conflict
    assert candidate.status == CandidateStatus.BLOCKED
    assert any(r.residual_type == "identity_trace_conflict" for r in result.residuals)

    # CRITICAL: Even though there's a conflict in the inputs,
    # the Candidate object itself must remain structurally valid
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)
    assert not (identity_set & trace_set), (
        f"Blocked candidate has overlapping identity_ids and trace_ids: {identity_set & trace_set}"
    )
