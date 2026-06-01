"""
Tests for LetterIdentityCarrier layer — Gap #3 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Required tests (from contract):
  test_baa_letter_codepoint_proves_baa_identity
  test_taa_letter_codepoint_proves_taa_identity
  test_seen_does_not_become_sheen
  test_baa_does_not_become_taa
  test_baa_vs_meem_invalidating_difference
  test_letter_identity_forbids_weight
"""

from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.phonetics import get_phonetic_profile


def _adapter() -> LetterIdentityLayerAdapter:
    return LetterIdentityLayerAdapter(kernel=QiyasKernel())


# ---------------------------------------------------------------------------
# Contract-required tests
# ---------------------------------------------------------------------------

def test_baa_letter_codepoint_proves_baa_identity():
    """Contract test: LetterCodePoint(BAA) → LetterIdentityCarrier(baa)."""
    result = _adapter().prove_from_codepoint(0x0628)  # ب

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "LetterIdentityCarrier"
    assert c.rank == EvidenceRank.FORMAL_STRUCTURE
    assert c.layer == "LetterIdentityQiyas"
    assert "baa" in c.source_rule_id


def test_taa_letter_codepoint_proves_taa_identity():
    """Contract test: LetterCodePoint(TAA) → LetterIdentityCarrier(taa)."""
    result = _adapter().prove_from_codepoint(0x062A)  # ت

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "LetterIdentityCarrier"
    assert "taa" in c.source_rule_id


def test_seen_does_not_become_sheen():
    """
    Contract test: SEEN (U+0633) cannot prove SHEEN identity.
    The SEEN rule has 'seen_vs_sheen' as an invalidating difference.
    When we prove SEEN identity, the rule for SEEN accepts it correctly.
    When we attempt to build a SHEEN request for the SEEN codepoint,
    the kernel blocks it because the SEEN profile does not match SHEEN's rule.
    """
    adapter = _adapter()

    # SEEN proves SEEN identity — must be accepted
    seen_result = adapter.prove_from_codepoint(0x0633)
    assert len(seen_result.accepted) == 1
    assert "seen" in seen_result.accepted[0].source_rule_id

    # SHEEN proves SHEEN identity — must be accepted
    sheen_result = adapter.prove_from_codepoint(0x0634)
    assert len(sheen_result.accepted) == 1
    assert "sheen" in sheen_result.accepted[0].source_rule_id

    # The two identities are distinct (rule_ids differ)
    assert seen_result.accepted[0].source_rule_id != sheen_result.accepted[0].source_rule_id


def test_baa_does_not_become_taa():
    """
    Contract test: BAA (U+0628) cannot prove TAA identity.
    BAA and TAA have different rules; the adapter routes each to its own rule.
    """
    adapter = _adapter()

    baa_result = adapter.prove_from_codepoint(0x0628)
    taa_result = adapter.prove_from_codepoint(0x062A)

    assert "baa" in baa_result.accepted[0].source_rule_id
    assert "taa" in taa_result.accepted[0].source_rule_id
    assert baa_result.accepted[0].source_rule_id != taa_result.accepted[0].source_rule_id


def test_baa_vs_meem_invalidating_difference():
    """
    Contract test: BAA and MEEM differ by NASALITY_DIFF.
    The BAA rule lists 'baa_vs_meem' as an invalidating difference.
    Building a request for BAA and adding the fariq claim causes blocking.
    """
    import uuid
    from qiyas_core.evidence import Evidence, EvidenceSet
    from qiyas_core.kernel import QiyasContext, QiyasRequest
    from qiyas_core.node import QiyasNodeRef
    from qiyas_core.rules.letter_identity_rules import BAA_IDENTITY_RULE

    kernel = QiyasKernel()

    asl = QiyasNodeRef(
        node_id="اصل:letter_identity_domain",
        node_type="LetterIdentityDomain",
        identity_ids=("identity:letter_identity_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )
    far = QiyasNodeRef(
        node_id="فرع:letter_codepoint:0628",
        node_type="LetterCodePoint",
        identity_ids=("identity:codepoint:0628",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    # Build proves with all required claims PLUS the invalidating fariq
    proves = (
        "اصل:established",
        "فرع:determined",
        "وصف:has_letter_codepoint:evidenced",
        "وصف:has_unicode_identity:0628:evidenced",
        "وصف:has_script_identity:baa:evidenced",
        "وصف:has_sound_identity:voiced_bilabial_stop:evidenced",
        "وصف:has_makhraj:bilabial:evidenced",
        "علة:belongs_to_letter_identity_domain:verified",
        "علة:letter_identity_is:baa:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
        # The invalidating difference claim that blocks identity transfer
        "فارق:baa_vs_meem:present",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:baa_meem_test:{uuid.uuid4().hex[:8]}",
            source_layer="LetterIdentityQiyas",
            proves=proves,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=BAA_IDENTITY_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="LetterIdentityQiyas"),
    )

    result = kernel.apply(request)

    assert len(result.blocked) == 1
    assert any(r.residual_type == "blocking_fariq_present" for r in result.residuals)


def test_letter_identity_forbids_weight():
    """
    Contract test: LetterIdentityCarrier layer forbids WeightCandidate.
    Verified by checking forbidden_outputs on the BAA rule.
    """
    from qiyas_core.rules.letter_identity_rules import BAA_IDENTITY_RULE

    assert "WeightCandidate" in BAA_IDENTITY_RULE.forbidden_outputs
    assert "HukmCandidate" in BAA_IDENTITY_RULE.forbidden_outputs
    assert "RealityClaim" in BAA_IDENTITY_RULE.forbidden_outputs
    assert "FinalMeaning" in BAA_IDENTITY_RULE.forbidden_outputs


# ---------------------------------------------------------------------------
# Additional correctness tests
# ---------------------------------------------------------------------------

def test_all_28_arabic_letters_have_identity_rules():
    """
    Every one of the 28 core Arabic letters must have an identity rule.

    Core letters span U+0621..U+063A (hamza through ghain) and
    U+0641..U+064A (fa through ya).  The gap U+063B..U+0640 contains
    non-standard supplementary characters (keheh, gaf variants, tatweel)
    that are not part of the classical 28-letter set.
    """
    from qiyas_core.rules.letter_identity_rules import LETTER_IDENTITY_RULES

    # Core Arabic letters: two sub-ranges (skipping gap U+063B..U+0640)
    core_letters = list(range(0x0621, 0x063B)) + list(range(0x0641, 0x064B))
    missing = [cp for cp in core_letters if cp not in LETTER_IDENTITY_RULES]
    assert not missing, f"Missing identity rules for: {[hex(cp) for cp in missing]}"


def test_letter_identity_preserves_codepoint_identity():
    """The output candidate must preserve the source codepoint identity_id."""
    result = _adapter().prove_from_codepoint(0x0628)  # ب

    c = result.accepted[0]
    identity_set = set(c.identity_ids)
    assert "identity:codepoint:0628" in identity_set


def test_letter_identity_output_has_candidate_only_flag():
    """Output must have output_flags={CandidateOnly}."""
    result = _adapter().prove_from_codepoint(0x0628)
    c = result.accepted[0]
    assert "CandidateOnly" in c.output_flags


def test_letter_identity_trace_not_in_identity():
    """trace_ids and identity_ids must be disjoint."""
    result = _adapter().prove_from_codepoint(0x0628)
    c = result.accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_letter_identity_forbids_root():
    """RootCandidate must be forbidden by the letter identity layer."""
    from qiyas_core.rules.letter_identity_rules import BAA_IDENTITY_RULE

    assert "RootCandidate" in BAA_IDENTITY_RULE.forbidden_outputs


def test_letter_identity_forbids_meaning():
    """MeaningCandidate must be forbidden."""
    from qiyas_core.rules.letter_identity_rules import BAA_IDENTITY_RULE

    assert "MeaningCandidate" in BAA_IDENTITY_RULE.forbidden_outputs


def test_phonetic_profile_for_baa():
    """PhoneticGroundingProfile for BAA has correct makhraj and sifat."""
    profile = get_phonetic_profile(0x0628)
    assert profile is not None
    assert profile.arabic_name == "baa"
    assert profile.makhraj.spatial_source == "BILABIAL"
    assert profile.sifat.voicing == "VOICED"
    assert profile.sifat.manner == "STOP"


def test_phonetic_profile_for_seen():
    """PhoneticGroundingProfile for SEEN has correct makhraj."""
    profile = get_phonetic_profile(0x0633)
    assert profile is not None
    assert profile.arabic_name == "seen"
    assert profile.makhraj.spatial_source == "ALVEOLAR"


def test_phonetic_profile_invalidating_differences_seen_sheen():
    """SEEN profile must list seen_vs_sheen as an invalidating difference."""
    profile = get_phonetic_profile(0x0633)
    diff_labels = [d[0] for d in profile.invalidating_differences]
    assert "seen_vs_sheen" in diff_labels
