"""Constitutional tests for evidence rank invariants."""

import pytest

from qiyas_core.enums import EvidenceRank
from qiyas_core.kernel import QiyasKernel
from tests.qiyas_core.constitutional_helpers import (
    assert_rank_ceiling,
    assert_rank_is_minimum,
)
from tests.qiyas_core.fixtures.candidates import make_candidate_with_rank
from tests.qiyas_core.fixtures.nodes import make_unicode_node, make_haraka_node
from tests.qiyas_core.fixtures.requests import make_qiyas_request
from tests.qiyas_core.fixtures.rules import make_minimal_rule


@pytest.mark.rank
@pytest.mark.constitution
class TestRankInvariants:
    """Test that candidate ranks follow constitutional invariants."""

    def test_output_rank_never_exceeds_rule_ceiling(self):
        """Candidate rank must not exceed rule.rank_ceiling"""
        candidate = make_candidate_with_rank(EvidenceRank.FORMAL_STRUCTURE)
        assert_rank_ceiling(candidate, EvidenceRank.FORMAL_STRUCTURE)
        assert_rank_ceiling(candidate, EvidenceRank.ANALOGICAL)  # Higher ceiling is OK

    def test_rank_ceiling_violation_detected(self):
        """Helper detects when rank exceeds ceiling"""
        candidate = make_candidate_with_rank(EvidenceRank.ANALOGICAL)

        with pytest.raises(AssertionError, match="exceeds ceiling"):
            assert_rank_ceiling(candidate, EvidenceRank.FORMAL_STRUCTURE)

    def test_rank_is_minimum_of_all_inputs(self):
        """Candidate rank = min(rule, asl, far, evidence)"""
        rule = make_minimal_rule(rank_ceiling=EvidenceRank.ANALOGICAL)
        asl = make_unicode_node(rank=EvidenceRank.FORMAL_STRUCTURE)
        far = make_haraka_node(rank=EvidenceRank.PATTERN)

        request = make_qiyas_request(rule=rule, asl=asl, far=far)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]

        # Expected: min(QIYAS, FORM, PATTERN, QIYAS) = FORM
        assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE

        assert_rank_is_minimum(
            candidate,
            rule_ceiling=rule.rank_ceiling,
            asl_rank=asl.rank,
            far_rank=far.rank,
            evidence_rank=EvidenceRank.ANALOGICAL,
        )

    def test_low_asl_rank_limits_output(self):
        """Low asl rank limits output rank"""
        rule = make_minimal_rule(rank_ceiling=EvidenceRank.ANALOGICAL)
        asl = make_unicode_node(rank=EvidenceRank.FORMAL_STRUCTURE)  # Low rank
        far = make_haraka_node(rank=EvidenceRank.ANALOGICAL)  # High rank

        request = make_qiyas_request(rule=rule, asl=asl, far=far)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        # Should be limited by asl's FORM rank
        assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE

    def test_low_far_rank_limits_output(self):
        """Low far rank limits output rank"""
        rule = make_minimal_rule(rank_ceiling=EvidenceRank.ANALOGICAL)
        asl = make_unicode_node(rank=EvidenceRank.ANALOGICAL)  # High rank
        far = make_haraka_node(rank=EvidenceRank.FORMAL_STRUCTURE)  # Low rank

        request = make_qiyas_request(rule=rule, asl=asl, far=far)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        # Should be limited by far's FORM rank
        assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE

    def test_low_rule_ceiling_limits_output(self):
        """Low rule ceiling limits output rank"""
        rule = make_minimal_rule(rank_ceiling=EvidenceRank.FORMAL_STRUCTURE)  # Low ceiling
        asl = make_unicode_node(rank=EvidenceRank.ANALOGICAL)
        far = make_haraka_node(rank=EvidenceRank.ANALOGICAL)

        request = make_qiyas_request(rule=rule, asl=asl, far=far)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        # Should be limited by rule ceiling
        assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE

    def test_all_high_ranks_produces_high_output(self):
        """When all inputs are high rank, output is high"""
        rule = make_minimal_rule(rank_ceiling=EvidenceRank.ANALOGICAL)
        asl = make_unicode_node(rank=EvidenceRank.ANALOGICAL)
        far = make_haraka_node(rank=EvidenceRank.ANALOGICAL)

        request = make_qiyas_request(rule=rule, asl=asl, far=far)

        kernel = QiyasKernel()
        result = kernel.apply(request)

        candidate = result.candidates[0]
        assert candidate.rank == EvidenceRank.ANALOGICAL

    def test_rank_minimum_assertion_detects_wrong_rank(self):
        """Helper detects when rank is not minimum of inputs"""
        # Create candidate with wrong rank
        candidate = make_candidate_with_rank(EvidenceRank.ANALOGICAL)

        # Claim it should be FORM (minimum of inputs)
        with pytest.raises(AssertionError, match="should be"):
            assert_rank_is_minimum(
                candidate,
                rule_ceiling=EvidenceRank.ANALOGICAL,
                asl_rank=EvidenceRank.FORMAL_STRUCTURE,  # Minimum
                far_rank=EvidenceRank.ANALOGICAL,
                evidence_rank=EvidenceRank.ANALOGICAL,
            )

    def test_form_rank_ceiling_respected(self):
        """FORM rank ceiling is respected"""
        candidate = make_candidate_with_rank(EvidenceRank.FORMAL_STRUCTURE)
        # Should pass FORM ceiling
        assert_rank_ceiling(candidate, EvidenceRank.FORMAL_STRUCTURE)

        # Should also pass higher ceilings
        assert_rank_ceiling(candidate, EvidenceRank.PATTERN)
        assert_rank_ceiling(candidate, EvidenceRank.ANALOGICAL)

    def test_pattern_rank_ceiling_respected(self):
        """PATTERN rank ceiling is respected"""
        candidate = make_candidate_with_rank(EvidenceRank.PATTERN)

        # Should fail FORM ceiling (PATTERN > FORM)
        with pytest.raises(AssertionError):
            assert_rank_ceiling(candidate, EvidenceRank.FORMAL_STRUCTURE)

        # Should pass PATTERN ceiling
        assert_rank_ceiling(candidate, EvidenceRank.PATTERN)
