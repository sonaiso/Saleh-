"""Constitutional tests for evidence claim grammar."""

import pytest

from tests.qiyas_core.constitutional_helpers import (
    assert_evidence_claim_grammar,
    assert_forbidden_claim,
)


@pytest.mark.evidence_claims
@pytest.mark.constitution
class TestEvidenceClaimGrammar:
    """Test that evidence claims follow constitutional grammar."""

    def test_asl_established_allowed(self):
        """asl:established claim is allowed"""
        assert_evidence_claim_grammar("asl:established")

    def test_far_determined_allowed(self):
        """far:determined claim is allowed"""
        assert_evidence_claim_grammar("far:determined")

    def test_wasf_claims_allowed(self):
        """wasf:*:evidenced claims are allowed"""
        assert_evidence_claim_grammar("wasf:carrier_accepts_mark:evidenced")
        assert_evidence_claim_grammar("wasf:valid_haraka:evidenced")
        assert_evidence_claim_grammar("wasf:anything:evidenced")

    def test_illah_claims_allowed(self):
        """illah:*:verified claims are allowed"""
        assert_evidence_claim_grammar("illah:licensed_atomic_binding:verified")
        assert_evidence_claim_grammar("illah:phonological_fit:verified")
        assert_evidence_claim_grammar("illah:anything:verified")

    def test_wadi_sabab_allowed(self):
        """wadi:sabab:established claim is allowed"""
        assert_evidence_claim_grammar("wadi:sabab:established")

    def test_wadi_shart_allowed(self):
        """wadi:shart:satisfied claim is allowed"""
        assert_evidence_claim_grammar("wadi:shart:satisfied")

    def test_wadi_mani_allowed(self):
        """wadi:mani:absent claim is allowed"""
        assert_evidence_claim_grammar("wadi:mani:absent")

    def test_wadi_sihha_allowed(self):
        """wadi:sihha:valid claim is allowed"""
        assert_evidence_claim_grammar("wadi:sihha:valid")

    def test_wadi_fasad_allowed(self):
        """wadi:fasad:absent claim is allowed"""
        assert_evidence_claim_grammar("wadi:fasad:absent")

    def test_wadi_butlan_allowed(self):
        """wadi:butlan:absent claim is allowed"""
        assert_evidence_claim_grammar("wadi:butlan:absent")

    def test_fariq_claims_allowed(self):
        """fariq:*:present claims are allowed"""
        assert_evidence_claim_grammar("fariq:carrier_is_not_arabic_letter:present")
        assert_evidence_claim_grammar("fariq:mark_is_not_arabic_diacritic:present")
        assert_evidence_claim_grammar("fariq:anything:present")

    def test_defer_claims_allowed(self):
        """defer:*:present claims are allowed"""
        assert_evidence_claim_grammar("defer:murab_closure_deferred:present")
        assert_evidence_claim_grammar("defer:unknown_closure_deferred:present")
        assert_evidence_claim_grammar("defer:anything:present")

    def test_diff_claims_forbidden(self):
        """diff:* claims must be rejected"""
        assert_forbidden_claim("diff:carrier_mismatch:detected")
        assert_forbidden_claim("diff:anything:detected")

    def test_residual_claims_forbidden(self):
        """residual:* claims must be rejected"""
        assert_forbidden_claim("residual:unprocessed:present")
        assert_forbidden_claim("residual:anything:something")

    def test_hukm_claims_forbidden(self):
        """hukm:* claims must be rejected"""
        assert_forbidden_claim("hukm:judgment:final")
        assert_forbidden_claim("hukm:anything:something")

    def test_meaning_final_claims_forbidden(self):
        """meaning:*:final claims must be rejected"""
        assert_forbidden_claim("meaning:semantic:final")
        assert_forbidden_claim("meaning:anything:final")

    def test_reality_claim_claims_forbidden(self):
        """reality:*:claim claims must be rejected"""
        assert_forbidden_claim("reality:ontological:claim")
        assert_forbidden_claim("reality:anything:claim")

    def test_final_claims_forbidden(self):
        """final:* claims must be rejected"""
        assert_forbidden_claim("final:output")
        assert_forbidden_claim("final:anything")

    def test_invalid_claim_rejected(self):
        """Claims not matching allowed patterns must be rejected"""
        with pytest.raises(AssertionError, match="does not match any allowed pattern"):
            assert_evidence_claim_grammar("invalid:claim:format")

    def test_diff_claim_not_allowed(self):
        """diff:* claims must not pass as allowed"""
        with pytest.raises(AssertionError, match="does not match any allowed pattern"):
            assert_evidence_claim_grammar("diff:something:detected")

    def test_residual_claim_not_allowed(self):
        """residual:* claims must not pass as allowed"""
        with pytest.raises(AssertionError, match="does not match any allowed pattern"):
            assert_evidence_claim_grammar("residual:something:present")
