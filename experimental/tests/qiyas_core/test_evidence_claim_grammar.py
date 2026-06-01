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
        """اصل:established claim is allowed"""
        assert_evidence_claim_grammar("اصل:established")

    def test_far_determined_allowed(self):
        """فرع:determined claim is allowed"""
        assert_evidence_claim_grammar("فرع:determined")

    def test_wasf_claims_allowed(self):
        """وصف:*:evidenced claims are allowed"""
        assert_evidence_claim_grammar("وصف:carrier_accepts_mark:evidenced")
        assert_evidence_claim_grammar("وصف:valid_haraka:evidenced")
        assert_evidence_claim_grammar("وصف:anything:evidenced")

    def test_illah_claims_allowed(self):
        """علة:*:verified claims are allowed"""
        assert_evidence_claim_grammar("علة:licensed_atomic_binding:verified")
        assert_evidence_claim_grammar("علة:phonological_fit:verified")
        assert_evidence_claim_grammar("علة:anything:verified")

    def test_wadi_sabab_allowed(self):
        """وادي:cause:established claim is allowed"""
        assert_evidence_claim_grammar("وادي:cause:established")

    def test_wadi_shart_allowed(self):
        """وادي:condition:satisfied claim is allowed"""
        assert_evidence_claim_grammar("وادي:condition:satisfied")

    def test_wadi_mani_allowed(self):
        """وادي:obstacle:absent claim is allowed"""
        assert_evidence_claim_grammar("وادي:obstacle:absent")

    def test_wadi_sihha_allowed(self):
        """وادي:validity:valid claim is allowed"""
        assert_evidence_claim_grammar("وادي:validity:valid")

    def test_wadi_fasad_allowed(self):
        """وادي:corruption:absent claim is allowed"""
        assert_evidence_claim_grammar("وادي:corruption:absent")

    def test_wadi_butlan_allowed(self):
        """وادي:nullity:absent claim is allowed"""
        assert_evidence_claim_grammar("وادي:nullity:absent")

    def test_fariq_claims_allowed(self):
        """فارق:*:present claims are allowed"""
        assert_evidence_claim_grammar("فارق:carrier_is_not_arabic_letter:present")
        assert_evidence_claim_grammar("فارق:mark_is_not_arabic_diacritic:present")
        assert_evidence_claim_grammar("فارق:anything:present")

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
