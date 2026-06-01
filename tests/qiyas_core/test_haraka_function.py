"""
Tests for HarakaFunctionCarrier layer — Gap #4 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Required tests (from contract):
  test_fatha_haraka_proves_fatha_function
  test_damma_haraka_proves_damma_function
  test_kasra_haraka_proves_kasra_function
  test_sukun_proves_closure_function
  test_shadda_proves_compression_function
  test_fatha_does_not_become_damma
  test_haraka_function_forbids_case_effect
"""

from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.kernel import QiyasKernel
from qiyas_core.phonetics import get_energy_profile


def _adapter() -> HarakaFunctionLayerAdapter:
    return HarakaFunctionLayerAdapter(kernel=QiyasKernel())


# ---------------------------------------------------------------------------
# Contract-required tests
# ---------------------------------------------------------------------------

def test_fatha_haraka_proves_fatha_function():
    """Contract test: HarakaCodePoint(FATHA) → HarakaFunctionCarrier(fatha)."""
    result = _adapter().prove_from_codepoint(0x064E)

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "HarakaFunctionCarrier"
    assert c.rank == EvidenceRank.FORM
    assert "fatha" in c.source_rule_id


def test_damma_haraka_proves_damma_function():
    """Contract test: HarakaCodePoint(DAMMA) → HarakaFunctionCarrier(damma)."""
    result = _adapter().prove_from_codepoint(0x064F)

    assert len(result.accepted) == 1
    assert "damma" in result.accepted[0].source_rule_id


def test_kasra_haraka_proves_kasra_function():
    """Contract test: HarakaCodePoint(KASRA) → HarakaFunctionCarrier(kasra)."""
    result = _adapter().prove_from_codepoint(0x0650)

    assert len(result.accepted) == 1
    assert "kasra" in result.accepted[0].source_rule_id


def test_sukun_proves_closure_function():
    """Contract test: HarakaCodePoint(SUKUN) → HarakaFunctionCarrier closure."""
    result = _adapter().prove_from_codepoint(0x0652)

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.candidate_type == "HarakaFunctionCarrier"
    assert "sukun" in c.source_rule_id


def test_shadda_proves_compression_function():
    """Contract test: HarakaCodePoint(SHADDA) → HarakaFunctionCarrier compression."""
    result = _adapter().prove_from_codepoint(0x0651)

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.candidate_type == "HarakaFunctionCarrier"
    assert "shadda" in c.source_rule_id


def test_fatha_does_not_become_damma():
    """
    Contract test: FATHA cannot prove DAMMA function.
    Each haraka maps to a distinct rule; adapter routes by codepoint.
    """
    adapter = _adapter()
    fatha_result = adapter.prove_from_codepoint(0x064E)
    damma_result = adapter.prove_from_codepoint(0x064F)

    assert "fatha" in fatha_result.accepted[0].source_rule_id
    assert "damma" in damma_result.accepted[0].source_rule_id
    assert fatha_result.accepted[0].source_rule_id != damma_result.accepted[0].source_rule_id


def test_haraka_function_forbids_case_effect():
    """
    Contract test: HarakaFunctionCarrier layer forbids CaseEffect.
    Verified by checking forbidden_outputs on the FATHA rule.
    """
    from qiyas_core.rules.haraka_function_rules import FATHA_FUNCTION_RULE

    assert "CaseEffect" in FATHA_FUNCTION_RULE.forbidden_outputs
    assert "Irab" in FATHA_FUNCTION_RULE.forbidden_outputs
    assert "HukmCandidate" in FATHA_FUNCTION_RULE.forbidden_outputs
    assert "RealityClaim" in FATHA_FUNCTION_RULE.forbidden_outputs
    assert "FinalMeaning" in FATHA_FUNCTION_RULE.forbidden_outputs


# ---------------------------------------------------------------------------
# Additional tests
# ---------------------------------------------------------------------------

def test_haraka_function_output_type():
    """Output candidate_type must be HarakaFunctionCarrier."""
    result = _adapter().prove_from_codepoint(0x064E)
    assert result.accepted[0].candidate_type == "HarakaFunctionCarrier"


def test_haraka_function_preserves_codepoint_identity():
    """Output must preserve the source haraka codepoint identity."""
    result = _adapter().prove_from_codepoint(0x064E)
    c = result.accepted[0]
    assert "identity:codepoint:064e" in set(c.identity_ids)


def test_haraka_function_trace_not_in_identity():
    """trace_ids and identity_ids must be disjoint."""
    result = _adapter().prove_from_codepoint(0x064E)
    c = result.accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_haraka_function_output_flags():
    """Output must have CandidateOnly flag."""
    result = _adapter().prove_from_codepoint(0x064E)
    assert "CandidateOnly" in result.accepted[0].output_flags


def test_tanwin_fath_proves_tanwin_function():
    """Tanwin fath (U+064B) proves tanwin function."""
    result = _adapter().prove_from_codepoint(0x064B)
    assert len(result.accepted) == 1
    assert "tanwin_fath" in result.accepted[0].source_rule_id


def test_tanwin_damm_proves_tanwin_function():
    """Tanwin damm (U+064C) proves tanwin function."""
    result = _adapter().prove_from_codepoint(0x064C)
    assert len(result.accepted) == 1
    assert "tanwin_damm" in result.accepted[0].source_rule_id


def test_tanwin_kasr_proves_tanwin_function():
    """Tanwin kasr (U+064D) proves tanwin function."""
    result = _adapter().prove_from_codepoint(0x064D)
    assert len(result.accepted) == 1
    assert "tanwin_kasr" in result.accepted[0].source_rule_id


def test_haraka_function_forbids_syllable():
    """HarakaFunctionCarrier must not produce SyllableCandidate."""
    from qiyas_core.rules.haraka_function_rules import FATHA_FUNCTION_RULE

    assert "SyllableCandidate" in FATHA_FUNCTION_RULE.forbidden_outputs


def test_energy_profile_fatha():
    """VocalicEnergyProfile for fatha has expected values."""
    profile = get_energy_profile(0x064E)
    assert profile is not None
    assert profile.arabic_name == "fatha"
    assert profile.vocalic_function == "OPENING_FUNCTION"
    assert profile.aperture == "OPEN"


def test_energy_profile_sukun():
    """VocalicEnergyProfile for sukun shows closure function."""
    profile = get_energy_profile(0x0652)
    assert profile is not None
    assert profile.vocalic_function == "CLOSURE_FUNCTION"
    assert profile.duration == "ZERO"


def test_fatha_invalidating_diff_blocks_haraka_transfer():
    """
    Injecting fariq:fatha_vs_damma:present blocks fatha function.
    """
    import uuid
    from qiyas_core.evidence import Evidence, EvidenceSet
    from qiyas_core.kernel import QiyasContext, QiyasKernel, QiyasRequest
    from qiyas_core.node import QiyasNodeRef
    from qiyas_core.rules.haraka_function_rules import FATHA_FUNCTION_RULE

    kernel = QiyasKernel()

    asl = QiyasNodeRef(
        node_id="asl:haraka_function_domain",
        node_type="HarakaFunctionDomain",
        identity_ids=("identity:haraka_function_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )
    far = QiyasNodeRef(
        node_id="far:haraka_codepoint:064e",
        node_type="HarakaCodePoint",
        identity_ids=("identity:codepoint:064e",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    proves = (
        "asl:established",
        "far:determined",
        "wasf:has_haraka_codepoint:evidenced",
        "wasf:has_unicode_identity:064e:evidenced",
        "wasf:has_vocalic_function:opening_function:evidenced",
        "illah:belongs_to_haraka_function_domain:verified",
        "illah:haraka_function_is:fatha:verified",
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
        # Invalidating difference — should block
        "fariq:fatha_vs_damma:present",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:fatha_damma_test:{uuid.uuid4().hex[:8]}",
            source_layer="HarakaFunctionQiyas",
            proves=proves,
            rank=EvidenceRank.FORM,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=FATHA_FUNCTION_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="HarakaFunctionQiyas"),
    )

    result = kernel.apply(request)
    assert len(result.blocked) == 1
    assert any(r.residual_type == "blocking_fariq_present" for r in result.residuals)
