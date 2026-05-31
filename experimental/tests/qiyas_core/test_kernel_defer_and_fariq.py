"""Constitutional tests for kernel defer and fariq handling."""

import pytest

from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.fixtures.requests import make_request_with_evidence
from tests.qiyas_core.fixtures.rules import make_minimal_rule


@pytest.mark.kernel
@pytest.mark.constitution
class TestKernelDeferAndFariq:
    """Test that kernel correctly handles defer and fariq evidence claims."""

    def test_defer_claim_produces_deferred_status(self):
        """defer:*:present evidence must produce CandidateStatus.DEFERRED"""
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "defer:murab_closure_deferred:present",  # Deferral claim
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        assert len(result.candidates) == 1
        candidate = result.candidates[0]
        assert candidate.status == CandidateStatus.DEFERRED

    def test_fariq_claim_produces_blocked_status(self):
        """fariq:*:present evidence must produce CandidateStatus.BLOCKED"""
        rule = make_minimal_rule()
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "fariq:test_diff:present",  # Blocking difference (matches rule.invalidating_differences)
            rule=rule,
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        assert len(result.candidates) == 1
        candidate = result.candidates[0]
        assert candidate.status == CandidateStatus.BLOCKED

    def test_fariq_sets_blocking_fariq_present_residual(self):
        """fariq:*:present must produce blocking_fariq_present residual"""
        rule = make_minimal_rule()
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "fariq:test_diff:present",
            rule=rule,
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        assert candidate.status == CandidateStatus.BLOCKED

        # Check that blocking_fariq_present residual exists
        residual_types = [r.residual_type for r in candidate.residuals]
        assert "blocking_fariq_present" in residual_types

    def test_multiple_defer_claims_all_recorded(self):
        """Multiple defer claims must all be recorded in deferral_states"""
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "defer:first_reason:present",
            "defer:second_reason:present",
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        assert candidate.status == CandidateStatus.DEFERRED

        # Check that both defer reasons are in residuals
        residual_types = [r.residual_type for r in candidate.residuals]
        assert "deferred_first_reason" in residual_types
        assert "deferred_second_reason" in residual_types

    def test_multiple_fariq_claims_produce_blocked(self):
        """Multiple fariq claims must produce BLOCKED status"""
        rule = make_minimal_rule(
            invalidating_differences=("diff_a", "diff_b"),
        )
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "fariq:diff_a:present",
            "fariq:diff_b:present",
            rule=rule,
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        assert candidate.status == CandidateStatus.BLOCKED

        # Both fariq should be recorded
        residual_types = [r.residual_type for r in candidate.residuals]
        assert residual_types.count("blocking_fariq_present") == 2

    def test_fariq_overrides_acceptance(self):
        """fariq:*:present blocks even if wasf/illah present"""
        rule = make_minimal_rule()
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",  # Valid wasf
            "illah:test_illah:verified",  # Valid illah
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "fariq:test_diff:present",  # But has blocking difference
            rule=rule,
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        # Despite having valid wasf/illah, fariq blocks
        assert candidate.status == CandidateStatus.BLOCKED

    def test_defer_produces_deferred_not_accepted(self):
        """defer:*:present must produce DEFERRED, not ACCEPTED"""
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            "defer:closure_pending:present",
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        # Must be DEFERRED, not ACCEPTED
        assert candidate.status != CandidateStatus.ACCEPTED
        assert candidate.status == CandidateStatus.DEFERRED

    def test_no_defer_or_fariq_produces_accepted(self):
        """Without defer or fariq claims, candidate is ACCEPTED"""
        request = make_request_with_evidence(
            "asl:established",
            "far:determined",
            "wasf:test_wasf:evidenced",
            "illah:test_illah:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
            # No defer:* or fariq:* claims
        )

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        assert candidate.status == CandidateStatus.ACCEPTED
