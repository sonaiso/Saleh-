"""SCG-P4 JamidMushtaq — behavioral runtime tests (INFORMATION-GAIN layer).

SCG-P4 strengthening (2026-06-18). P4 is no longer a forwarding stamp: it READS
the upstream P3 verdict + structural geometry from the RootStemCandidate's trace
and discriminates the DERIVATION geometry into ACCEPT / DEFER / BLOCK, routed
through the kernel's ``defer:`` / ``فارق:`` machinery.

  ACCEPT : P3 ACCEPT and a consonantal skeleton (n_consonants >= 2).
  DEFER  : derivation skeleton too thin (n_consonants == 1) — e.g. مَا, which P3
           closes via its long vowel but whose single consonant under-specifies a
           derivation geometry.
  BLOCK  : P3 was DEFER/BLOCK (non-accepted upstream), or geometry conflicts.

Candidate-only and structural-only (JAMID_MUSHTAQ_CONSTITUTION.md): NOT a final
جامد/مشتق judgment (WordTypeJudgment forbidden), NOT wazn, NOT morphology, NOT
meaning. ``jamid_mushtaq_prior_type`` is a STRUCTURAL geometry class (selected
input-dependently), never a linguistic جامد/مشتق/اسم/فعل label.
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
from qiyas_core.root_stem_adapter import RootStemLayerAdapter, build_sequence_profile
from qiyas_core.jamid_mushtaq_adapter import (
    DERIVATION_GEOMETRY_EVIDENCE_PREFIX,
    DERIVATION_POSSIBILITY_PREFIX,
    JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX,
    OPENED_PRIOR_PREFIX,
    PATTERN_EVIDENCE_PREFIX,
    ROOT_STEM_CANDIDATE_REF_PREFIX,
    JamidMushtaqLayerAdapter,
)
from qiyas_core.rules.jamid_mushtaq_rules import (
    ALLOWED_DERIVATION_PRIOR_TYPES,
    DERIVATION_GEOMETRY_CLASS,
    DERIVATION_GEOMETRY_PRIOR,
    DERIVATION_UNDERSPECIFIED,
    JAMID_MUSHTAQ_RULE,
    OPENED_PRIORS,
    STRUCTURAL_DERIVATION_POSSIBILITY,
)

_LINGUISTIC_FORBIDDEN = {"Jamid", "Mushtaq", "Derived", "NonDerived", "Verb", "Noun",
                        "Particle", "Root", "Wazn", "اسم", "فعل"}

# Structural codepoint sequences (purely geometric).
_BARA = [0x0628, 0x064E, 0x0631, 0x064E]               # بَرَ -> CVCV  nC=2 (accept, Prior)
_SHADHTH = [0x0634, 0x064E, 0x0627, 0x0630, 0x0651]    # شَاذّ -> CVVCC nC=3 gem (accept, Possibility)
_DARABA = [0x0636, 0x064E, 0x0631, 0x064E, 0x0628, 0x064E]  # ضَرَبَ -> CVCVCV nC=3 (accept, Class)
_MAA = [0x0645, 0x064E, 0x0627]                        # مَا  -> CVV  nC=1 long-v (P3 accept, P4 defer)
_BA = [0x0628, 0x064E]                                 # بَ   -> CV   (P3 defer)


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


def _root_stem_set(profile_cps):
    """RootStemCandidate set for a given structural profile (status varies)."""
    return RootStemLayerAdapter(kernel=QiyasKernel()).close(
        _projection(), sequence_profile=build_sequence_profile(profile_cps)
    )


def _accepted_root_stem(profile_cps=_BARA):
    return _root_stem_set(profile_cps).accepted[0]


def _deferred_root_stem():
    return _root_stem_set(_BA).deferred[0]


def _classify(root_stem):
    return JamidMushtaqLayerAdapter(kernel=QiyasKernel()).classify(root_stem)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


def _has_trace(candidate, prefix):
    return any(t.startswith(prefix) for t in candidate.trace_ids)


# ─────────────────────────────────────────────────────────────────────────────
# P4-RUN-OUTPUT
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_RUN_01_root_stem_classifies_to_jamid_mushtaq_candidate():
    result = _classify(_accepted_root_stem())
    assert result.accepted
    assert result.accepted[0].candidate_type == "JamidMushtaqCandidate"


def test_P4_RUN_02_consumes_root_stem_far_type():
    assert JAMID_MUSHTAQ_RULE.far_type == "RootStemCandidate"
    assert JAMID_MUSHTAQ_RULE.output_candidate_type == "JamidMushtaqCandidate"


def test_P4_RUN_03_candidate_only():
    assert "CandidateOnly" in _classify(_accepted_root_stem()).accepted[0].output_flags


def test_P4_RUN_04_does_not_accept_every_root_stem_blindly():
    # Thin derivation skeleton (مَا: nC==1, P3-accepted via long vowel) -> NOT accepted.
    result = _classify(_accepted_root_stem(_MAA))
    assert not result.accepted


# ─────────────────────────────────────────────────────────────────────────────
# P4-VERDICT — reads P3 evidence; input-dependent verdict & prior_type
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_VERDICT_01_reads_p3_verdict_into_evidence():
    c = _classify(_accepted_root_stem(_SHADHTH)).accepted[0]
    ev = _trace_value(c, DERIVATION_GEOMETRY_EVIDENCE_PREFIX)
    assert ev is not None and "p3verdict=accept" in ev and "cv=CVVCC" in ev


def test_P4_VERDICT_02_prior_type_input_dependent():
    pt_gem = _trace_value(_classify(_accepted_root_stem(_SHADHTH)).accepted[0],
                          JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX)
    pt_full = _trace_value(_classify(_accepted_root_stem(_DARABA)).accepted[0],
                           JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX)
    pt_min = _trace_value(_classify(_accepted_root_stem(_BARA)).accepted[0],
                          JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX)
    assert pt_gem == STRUCTURAL_DERIVATION_POSSIBILITY   # gemination
    assert pt_full == DERIVATION_GEOMETRY_CLASS          # nC>=3
    assert pt_min == DERIVATION_GEOMETRY_PRIOR           # nC==2
    assert len({pt_gem, pt_full, pt_min}) == 3           # genuinely input-dependent


def test_P4_VERDICT_03_prior_type_is_structural_never_linguistic():
    for prof in (_SHADHTH, _DARABA, _BARA):
        pt = _trace_value(_classify(_accepted_root_stem(prof)).accepted[0],
                          JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX)
        assert pt in ALLOWED_DERIVATION_PRIOR_TYPES
        assert pt not in _LINGUISTIC_FORBIDDEN


# ─────────────────────────────────────────────────────────────────────────────
# P4-DEFER — thin derivation skeleton defers with a preserved residual
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_DEFER_01_thin_skeleton_defers():
    result = _classify(_accepted_root_stem(_MAA))   # nC==1
    assert result.deferred and not result.accepted and not result.blocked


def test_P4_DEFER_02_defer_residual_is_explicit():
    cand = _classify(_accepted_root_stem(_MAA)).deferred[0]
    types = {r.residual_type for r in cand.residuals}
    assert f"deferred_{DERIVATION_UNDERSPECIFIED}" in types


def test_P4_DEFER_03_defer_opens_no_priors_preserves_identity():
    rs = _accepted_root_stem(_MAA)
    cand = _classify(rs).deferred[0]
    assert not _has_trace(cand, OPENED_PRIOR_PREFIX)
    for iid in rs.identity_ids:
        assert iid in cand.identity_ids


# ─────────────────────────────────────────────────────────────────────────────
# P4-BLOCK — a non-accepted (deferred/blocked) P3 propagates to a P4 block
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_BLOCK_01_non_accepted_p3_blocks_p4():
    result = _classify(_deferred_root_stem())
    assert result.blocked and not result.accepted


def test_P4_BLOCK_02_block_preserves_identity():
    rs = _deferred_root_stem()
    cand = _classify(rs).blocked[0]
    for iid in rs.identity_ids:
        assert iid in cand.identity_ids


# ─────────────────────────────────────────────────────────────────────────────
# P4-IDENTITY / TRACE
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_IDENTITY_01_preserves_identities():
    rs = _accepted_root_stem()
    c = _classify(rs).accepted[0]
    for iid in rs.identity_ids:
        assert iid in c.identity_ids, iid


def test_P4_TRACE_01_identity_disjoint_from_trace():
    c = _classify(_accepted_root_stem()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


# ─────────────────────────────────────────────────────────────────────────────
# P4-STRUCTURAL — input-dependent derivation evidence; opens priors (ACCEPT)
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_STRUCTURAL_01_carries_structural_derivation_possibility():
    c = _classify(_accepted_root_stem(_SHADHTH)).accepted[0]
    sig = _trace_value(c, DERIVATION_POSSIBILITY_PREFIX)
    assert sig is not None and sig.startswith("derivsig:") and "CVVCC" in sig


def test_P4_STRUCTURAL_02_derivation_geometry_evidence_is_real_not_constant():
    e1 = _trace_value(_classify(_accepted_root_stem(_SHADHTH)).accepted[0],
                      DERIVATION_GEOMETRY_EVIDENCE_PREFIX)
    e2 = _trace_value(_classify(_accepted_root_stem(_DARABA)).accepted[0],
                      DERIVATION_GEOMETRY_EVIDENCE_PREFIX)
    assert e1 != e2 and "nC=3" in e1 and "gem=1" in e1


def test_P4_STRUCTURAL_03_carries_root_stem_ref_and_pattern_evidence():
    c = _classify(_accepted_root_stem()).accepted[0]
    assert _has_trace(c, ROOT_STEM_CANDIDATE_REF_PREFIX)
    assert _has_trace(c, PATTERN_EVIDENCE_PREFIX)


def test_P4_STRUCTURAL_04_opens_word_type_priors_on_accept():
    c = _classify(_accepted_root_stem()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"word_type_candidates"}


def test_P4_STRUCTURAL_05_does_not_emit_mufrad_word():
    c = _classify(_accepted_root_stem()).accepted[0]
    assert c.candidate_type != "MufradWordCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P4-FORBIDDEN — no final judgment / no wazn / no morphology / no meaning / no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_FORBIDDEN_01_no_final_judgment_no_wazn_no_word_no_meaning():
    forbidden = set(JAMID_MUSHTAQ_RULE.forbidden_outputs)
    for name in ("WordTypeJudgment", "WeightCandidate", "RootCandidate", "FormCandidate",
                 "WordCandidate", "MeaningCandidate", "DalalahCandidate", "IrabCandidate",
                 "CaseEffect", "Irab"):
        assert name in forbidden, name


def test_P4_FORBIDDEN_02_no_jump_to_p5_plus_or_absolutes():
    forbidden = set(JAMID_MUSHTAQ_RULE.forbidden_outputs)
    for name in ("MufradWordCandidate", "VerbalSignifiedCandidate", "IfadahCandidate",
                 "SlotGeometry", "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P4_FORBIDDEN_03_residual_diffs_explicit():
    assert JAMID_MUSHTAQ_RULE.invalidating_differences
