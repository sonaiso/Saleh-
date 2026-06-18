"""SCG-P3 RootStemClosure — behavioral runtime tests (INFORMATION-GAIN layer).

SCG-P3 strengthening (2026-06-18). P3 is no longer a forwarding stamp: it
discriminates the token's slot-sequence geometry (a ``RootStemSequenceProfile``,
the constitutional ``slot_sequence_consistent`` evidence) into ACCEPT / DEFER /
BLOCK, routed through the kernel's ``defer:`` / ``فارق:`` machinery.

  ACCEPT : n_consonants >= 1 AND (slot_count >= 2 OR long-vowel OR gemination).
  DEFER  : lone CV with no long-vowel / gemination enrichment (underspecified).
  BLOCK  : no consonantal anchor (n_consonants == 0) -> root_pattern_conflict.

Candidate-only and structural-only (ROOT_STEM_CLOSURE_CONSTITUTION.md): NOT final
root extraction (RootCandidate forbidden), NOT wazn (WeightCandidate forbidden),
NOT morphology / wordhood / meaning / i'rab / hukm. Opens jamid/mushtaq +
word-pattern priors (ACCEPT only); emits no JamidMushtaqCandidate / downstream.
"""

from __future__ import annotations

from qiyas_core.kernel import QiyasKernel
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.conditioned_typed_sequence_adapter import ConditionedTypedSequenceLayerAdapter
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.slot_adapter import SlotLayerAdapter
from qiyas_core.registry_projection_adapter import RegistryProjectionLayerAdapter
from qiyas_core.root_stem_adapter import (
    OPENED_PRIOR_PREFIX,
    REGISTRY_PROJECTION_REF_PREFIX,
    ROOT_PATTERN_EVIDENCE_PREFIX,
    ROOT_STEM_SIGNATURE_PREFIX,
    SLOT_SEQUENCE_REFS_PREFIX,
    STEM_BOUNDARY_EVIDENCE_PREFIX,
    VERDICT_ACCEPT,
    VERDICT_BLOCK,
    VERDICT_DEFER,
    RootStemLayerAdapter,
    build_sequence_profile,
)
from qiyas_core.rules.root_stem_rules import (
    OPENED_PRIORS,
    ROOT_PATTERN_CONFLICT,
    ROOT_PATTERN_UNDERSPECIFIED,
    ROOT_STEM_RULE,
)

# Structural codepoint sequences (purely geometric).
_SHADHTH = [0x0634, 0x064E, 0x0627, 0x0630, 0x0651]   # شَاذّ -> CVVCC (2 slots, gem, long-v)
_DARABA = [0x0636, 0x064E, 0x0631, 0x064E, 0x0628, 0x064E]  # ضَرَبَ -> CVCVCV (3 slots)
_BAB = [0x0628, 0x064E, 0x0627, 0x0628]               # بَاب -> CVVC (1 slot, long-v)
_BA = [0x0628, 0x064E]                                # بَ -> CV (1 slot, bare)
_NO_CONSONANT = [0x064E, 0x064F]                       # harakat only -> VV (no anchor)

_ACCEPT_PROFILE = build_sequence_profile(_SHADHTH)
_DEFER_PROFILE = build_sequence_profile(_BA)
_BLOCK_PROFILE = build_sequence_profile(_NO_CONSONANT)


def _projection():
    """A real RegistryProjectionCandidate for بَ via the full P1->P2 chain."""
    k = QiyasKernel()
    typed = TypedCodePointLayerAdapter(kernel=k)
    lt = typed.classify_codepoint(0x0628).accepted[0]
    ht = typed.classify_codepoint(0x064E).accepted[0]
    letter = LetterIdentityLayerAdapter(kernel=k).process_letter_codepoint(lt).accepted[0]
    haraka = HarakaFunctionLayerAdapter(kernel=k).prove_from_codepoint(0x064E).accepted[0]
    cts = ConditionedTypedSequenceLayerAdapter(kernel=k)
    pe = cts.prove_letter_position(lt, index=0, sequence_length=2).accepted[0]
    pos = PositionLayerAdapter(kernel=k).prove_position(pe, index=0).accepted[0]
    cb = cts.prove_carrier_binding(haraka_typed=ht, carrier_letter_typed=lt, index=1, sequence_length=2).accepted[0]
    slot = SlotLayerAdapter(kernel=k).compose_slot(letter, haraka, pos, alignment_evidence=cb).accepted[0]
    return RegistryProjectionLayerAdapter(kernel=k).project(slot).accepted[0]


def _close(projection, profile=_ACCEPT_PROFILE):
    return RootStemLayerAdapter(kernel=QiyasKernel()).close(projection, sequence_profile=profile)


def _has_trace(candidate, prefix):
    return any(t.startswith(prefix) for t in candidate.trace_ids)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# P3-PROFILE — the structural CV profile is correct & input-dependent
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_PROFILE_01_cv_signatures_match_geometry():
    assert build_sequence_profile(_SHADHTH).cv_signature == "CVVCC"
    assert build_sequence_profile(_DARABA).cv_signature == "CVCVCV"
    assert build_sequence_profile(_BAB).cv_signature == "CVVC"
    assert build_sequence_profile(_BA).cv_signature == "CV"


def test_P3_PROFILE_02_slot_counts_and_flags():
    assert build_sequence_profile(_SHADHTH).slot_count == 2
    assert build_sequence_profile(_DARABA).slot_count == 3
    assert build_sequence_profile(_SHADHTH).has_gemination is True
    assert build_sequence_profile(_BAB).has_long_vowel is True
    assert build_sequence_profile(_BA).has_long_vowel is False


def test_P3_PROFILE_03_verdicts():
    assert build_sequence_profile(_SHADHTH).verdict == VERDICT_ACCEPT
    assert build_sequence_profile(_DARABA).verdict == VERDICT_ACCEPT
    assert build_sequence_profile(_BAB).verdict == VERDICT_ACCEPT      # long-vowel licenses 1-slot
    assert build_sequence_profile(_BA).verdict == VERDICT_DEFER        # bare CV underspecified
    assert build_sequence_profile(_NO_CONSONANT).verdict == VERDICT_BLOCK


# ─────────────────────────────────────────────────────────────────────────────
# P3-RUN — discriminating output (no longer blind accept)
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_RUN_01_sufficient_geometry_closes_to_root_stem_candidate():
    result = _close(_projection(), _ACCEPT_PROFILE)
    assert result.accepted
    assert result.accepted[0].candidate_type == "RootStemCandidate"


def test_P3_RUN_02_consumes_registry_projection_far_type():
    assert ROOT_STEM_RULE.far_type == "RegistryProjectionCandidate"
    assert ROOT_STEM_RULE.output_candidate_type == "RootStemCandidate"


def test_P3_RUN_03_candidate_only():
    assert "CandidateOnly" in _close(_projection(), _ACCEPT_PROFILE).accepted[0].output_flags


def test_P3_RUN_04_long_vowel_licenses_single_slot_closure():
    # بَاب-like geometry: 1 slot but a long vowel -> ACCEPT.
    result = _close(_projection(), build_sequence_profile(_BAB))
    assert result.accepted and not result.deferred and not result.blocked


def test_P3_RUN_05_does_not_accept_every_projection_blindly():
    # Same projection, underspecified profile -> NOT accepted.
    result = _close(_projection(), _DEFER_PROFILE)
    assert not result.accepted


# ─────────────────────────────────────────────────────────────────────────────
# P3-DEFER — underspecified geometry defers with a preserved residual
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_DEFER_01_single_cv_defers():
    result = _close(_projection(), _DEFER_PROFILE)
    assert result.deferred and not result.accepted and not result.blocked


def test_P3_DEFER_02_defer_residual_is_explicit():
    cand = _close(_projection(), _DEFER_PROFILE).deferred[0]
    types = {r.residual_type for r in cand.residuals}
    assert f"deferred_{ROOT_PATTERN_UNDERSPECIFIED}" in types


def test_P3_DEFER_03_defer_preserves_identity_and_opens_no_priors():
    proj = _projection()
    cand = _close(proj, _DEFER_PROFILE).deferred[0]
    for iid in proj.identity_ids:
        assert iid in cand.identity_ids
    assert not _has_trace(cand, OPENED_PRIOR_PREFIX)  # priors open only on ACCEPT


# ─────────────────────────────────────────────────────────────────────────────
# P3-BLOCK — contradictory geometry blocks with an invalidating difference
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_BLOCK_01_no_consonant_anchor_blocks():
    result = _close(_projection(), _BLOCK_PROFILE)
    assert result.blocked and not result.accepted


def test_P3_BLOCK_02_block_residual_is_root_pattern_conflict():
    cand = _close(_projection(), _BLOCK_PROFILE).blocked[0]
    assert any(ROOT_PATTERN_CONFLICT in r.message or r.residual_type == "blocking_fariq_present"
               for r in cand.residuals)
    assert ROOT_PATTERN_CONFLICT in ROOT_STEM_RULE.invalidating_differences


def test_P3_BLOCK_03_block_preserves_identity():
    proj = _projection()
    cand = _close(proj, _BLOCK_PROFILE).blocked[0]
    for iid in proj.identity_ids:
        assert iid in cand.identity_ids


# ─────────────────────────────────────────────────────────────────────────────
# P3-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_IDENTITY_01_preserves_slot_candidate_identities():
    proj = _projection()
    c = _close(proj, _ACCEPT_PROFILE).accepted[0]
    for iid in proj.identity_ids:
        assert iid in c.identity_ids, iid


def test_P3_TRACE_01_identity_disjoint_from_trace():
    c = _close(_projection(), _ACCEPT_PROFILE).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P3-STRUCTURAL — input-dependent evidence; opens priors (ACCEPT)
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_STRUCTURAL_01_signature_is_input_dependent():
    c1 = _close(_projection(), build_sequence_profile(_SHADHTH)).accepted[0]
    c2 = _close(_projection(), build_sequence_profile(_DARABA)).accepted[0]
    sig1 = _trace_value(c1, ROOT_STEM_SIGNATURE_PREFIX)
    sig2 = _trace_value(c2, ROOT_STEM_SIGNATURE_PREFIX)
    assert sig1 != sig2  # CVVCC vs CVCVCV — not a constant re-encoding
    assert "CVVCC" in sig1 and "CVCVCV" in sig2


def test_P3_STRUCTURAL_02_root_pattern_evidence_is_real_not_constant():
    e_accept = _trace_value(_close(_projection(), build_sequence_profile(_SHADHTH)).accepted[0],
                            ROOT_PATTERN_EVIDENCE_PREFIX)
    e_bab = _trace_value(_close(_projection(), build_sequence_profile(_BAB)).accepted[0],
                         ROOT_PATTERN_EVIDENCE_PREFIX)
    assert e_accept != "structural" and e_bab != e_accept
    assert "cv=CVVCC" in e_accept and "gem=1" in e_accept
    assert "lv=1" in e_bab


def test_P3_STRUCTURAL_03_stem_boundary_evidence_reflects_ending_profile():
    closed = _trace_value(_close(_projection(), build_sequence_profile(_SHADHTH)).accepted[0],
                          STEM_BOUNDARY_EVIDENCE_PREFIX)
    assert closed is not None and "ending=closed" in closed  # CVVCC ends in C


def test_P3_STRUCTURAL_04_carries_required_structural_evidence():
    c = _close(_projection(), _ACCEPT_PROFILE).accepted[0]
    assert _has_trace(c, REGISTRY_PROJECTION_REF_PREFIX)
    assert _has_trace(c, SLOT_SEQUENCE_REFS_PREFIX)
    assert _has_trace(c, ROOT_PATTERN_EVIDENCE_PREFIX)
    assert _has_trace(c, STEM_BOUNDARY_EVIDENCE_PREFIX)


def test_P3_STRUCTURAL_05_opens_jamid_mushtaq_and_word_pattern_priors():
    c = _close(_projection(), _ACCEPT_PROFILE).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"jamid_mushtaq_candidates", "word_pattern_candidates"}


def test_P3_STRUCTURAL_06_does_not_emit_jamid_mushtaq():
    c = _close(_projection(), _ACCEPT_PROFILE).accepted[0]
    assert c.candidate_type != "JamidMushtaqCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P3-FORBIDDEN — no final root / no wazn / no morphology / no meaning / no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_FORBIDDEN_01_no_final_root_no_wazn_no_word_no_meaning():
    forbidden = set(ROOT_STEM_RULE.forbidden_outputs)
    for name in ("RootCandidate", "WeightCandidate", "FormCandidate", "WordCandidate",
                 "MeaningCandidate", "DalalahCandidate", "Irab", "CaseEffect"):
        assert name in forbidden, name


def test_P3_FORBIDDEN_02_no_jump_to_p4_plus_or_absolutes():
    forbidden = set(ROOT_STEM_RULE.forbidden_outputs)
    for name in ("JamidMushtaqCandidate", "MufradWordCandidate", "VerbalSignifiedCandidate",
                 "IfadahCandidate", "SlotGeometry", "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P3_FORBIDDEN_03_root_stem_candidate_is_not_root_candidate():
    assert ROOT_STEM_RULE.output_candidate_type == "RootStemCandidate"
    assert "RootCandidate" in ROOT_STEM_RULE.forbidden_outputs


def test_P3_FORBIDDEN_04_residual_diffs_explicit():
    assert ROOT_STEM_RULE.invalidating_differences
