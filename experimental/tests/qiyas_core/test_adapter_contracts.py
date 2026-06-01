"""Constitutional tests for adapter contracts."""

import pytest

from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.constitutional_helpers import assert_no_higher_outputs
from tests.qiyas_core.fixtures.candidates import (
    make_unicode_candidate,
    make_haraka_candidate,
    make_atomic_unit_candidate,
)
from tests.qiyas_core.fixtures.requests import make_qiyas_request
from tests.qiyas_core.fixtures.rules import make_minimal_rule


@pytest.mark.adapter
@pytest.mark.constitution
class TestAdapterContracts:
    """Test that adapters follow constitutional contracts."""

    def test_adapter_produces_only_declared_output_type(self):
        """Adapter must produce only output_candidate_type from rule"""
        rule = make_minimal_rule(output_candidate_type="TestCandidate")
        request = make_qiyas_request(rule=rule)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        # All candidates must be TestCandidate type
        for candidate in result.candidates:
            assert candidate.candidate_type == "TestCandidate"

    def test_adapter_respects_forbidden_outputs(self):
        """Adapter must never produce types in rule.forbidden_outputs"""
        rule = make_minimal_rule(
            output_candidate_type="TestCandidate",
            forbidden_outputs=(
                "SyllableCandidate",
                "WordCandidate",
                "MeaningCandidate",
            ),
        )
        request = make_qiyas_request(rule=rule)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        # No forbidden types should be produced
        assert_no_higher_outputs(
            result.candidates,
            ["SyllableCandidate", "WordCandidate", "MeaningCandidate"],
        )

    def test_accepted_candidate_has_valid_evidence(self):
        """Accepted candidates must have valid wasf and illah evidence"""
        request = make_qiyas_request()

        kernel = QiyasKernel()
        result = kernel.apply(request)

        for candidate in result.accepted:
            # Accepted candidates must have status ACCEPTED
            assert candidate.status == CandidateStatus.ACCEPTED

    def test_blocked_candidate_has_blocking_evidence(self):
        """Blocked candidates must have blocking residual"""
        rule = make_minimal_rule()
        request = make_qiyas_request(rule=rule)

        # Modify to add blocking fariq
        from tests.qiyas_core.fixtures.evidence import make_evidence_set

        blocking_evidence = make_evidence_set(
            "اصل:established",
            "فرع:determined",
            "وصف:test_wasf:evidenced",
            "علة:test_illah:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
            "فارق:test_diff:present",  # Blocking
        )

        from qiyas_core.kernel import QiyasRequest, QiyasContext

        blocking_request = QiyasRequest(
            rule=rule,
            asl=request.asl,
            far=request.far,
            evidence=blocking_evidence,
            context=QiyasContext(layer=rule.layer),
        )

        kernel = QiyasKernel()
        result = kernel.apply(blocking_request)

        for candidate in result.blocked:
            assert candidate.status == CandidateStatus.BLOCKED
            # Must have at least one blocking residual
            assert len(candidate.residuals) > 0

    def test_deferred_candidate_has_defer_evidence(self):
        """Deferred candidates must have defer evidence"""
        rule = make_minimal_rule()

        from tests.qiyas_core.fixtures.evidence import make_evidence_set
        from qiyas_core.kernel import QiyasRequest, QiyasContext

        defer_evidence = make_evidence_set(
            "اصل:established",
            "فرع:determined",
            "وصف:test_wasf:evidenced",
            "علة:test_illah:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
            "defer:test_reason:present",  # Deferral
        )

        from tests.qiyas_core.fixtures.nodes import make_unicode_node, make_haraka_node

        defer_request = QiyasRequest(
            rule=rule,
            asl=make_unicode_node(),
            far=make_haraka_node(),
            evidence=defer_evidence,
            context=QiyasContext(layer=rule.layer),
        )

        kernel = QiyasKernel()
        result = kernel.apply(defer_request)

        for candidate in result.deferred:
            assert candidate.status == CandidateStatus.DEFERRED
            # Must have at least one deferral residual
            assert len(candidate.residuals) > 0

    def test_candidate_has_non_empty_layer(self):
        """All candidates must have non-empty layer"""
        candidates = [
            make_unicode_candidate(),
            make_haraka_candidate(),
            make_atomic_unit_candidate(),
        ]

        for candidate in candidates:
            assert candidate.layer
            assert len(candidate.layer) > 0

    def test_candidate_has_source_rule_id(self):
        """All candidates must have source_rule_id"""
        candidates = [
            make_unicode_candidate(),
            make_haraka_candidate(),
            make_atomic_unit_candidate(),
        ]

        for candidate in candidates:
            assert candidate.source_rule_id
            assert len(candidate.source_rule_id) > 0

    def test_candidate_has_asl_and_far_ids(self):
        """All candidates must have asl_id and far_id"""
        candidates = [
            make_unicode_candidate(),
            make_haraka_candidate(),
            make_atomic_unit_candidate(),
        ]

        for candidate in candidates:
            assert candidate.asl_id
            assert candidate.far_id
            assert len(candidate.asl_id) > 0
            assert len(candidate.far_id) > 0

    def test_output_flags_not_forbidden(self):
        """Candidate output_flags must not contain forbidden flags"""
        from qiyas_core.enums import EvidenceRank
        from qiyas_core.candidate import Candidate

        # Attempt to create candidate with forbidden flag should raise
        with pytest.raises(ValueError, match="forbidden output flags"):
            Candidate(
                candidate_id="test:1",
                candidate_type="TestCandidate",
                status=CandidateStatus.ACCEPTED,
                layer="TestLayer",
                source_rule_id="rule:test",
                asl_id="اصل:1",
                far_id="فرع:1",
                identity_ids=("id:1",),
                rank=EvidenceRank.ANALOGICAL,
                residuals=(),
                trace_ids=(),
                output_flags=frozenset(["HukmCandidate"]),  # Forbidden
            )
