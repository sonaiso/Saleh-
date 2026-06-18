"""SCG-P8 AmilMamul — behavioral runtime tests (INFORMATION-GAIN layer).

SCG-P8 strengthening (2026-06-18). P8 is no longer a forwarding stamp: it READS
the upstream P7 verdict + composition geometry from the CompositionReadinessCandidate's
trace and discriminates the RELATION-possibility geometry into ACCEPT / DEFER /
BLOCK, routed through the kernel's ``defer:`` / ``فارق:`` machinery.

  ACCEPT : P7 ACCEPT and a richly-vocalised alternating skeleton able to host an
           operator–operand relation — nC >= 3 AND cadence AND vowel_count >= 3.
  DEFER  : P7-accepted operand whose relation geometry is too compact / fewer-
           vowel to host a relation — e.g. كَتَب (CVCVC, 2 vowels) or عَدَّ
           (geminated CVCVC) — emits ``defer:relation_geometry_underspecified:present``.
  BLOCK  : P7 was DEFER/BLOCK (non-accepted upstream), or no usable geometry.

CANDIDATE-ONLY and RELATION-POSSIBILITY-only (AMIL_MAMUL_CONSTITUTION.md): NOT an
actual i'rab/case judgment (IrabCandidate/CaseJudgment forbidden), NOT grammar,
NOT meaning/dalalah/hukm. ``amil_mamul_prior_type`` is a STRUCTURAL relation-
geometry class (input-dependent), never a grammatical/case label. Opens
grammatical-relation + i'rab PRIORS on ACCEPT only.
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
from qiyas_core.jamid_mushtaq_adapter import JamidMushtaqLayerAdapter
from qiyas_core.mufrad_word_adapter import MufradWordLayerAdapter
from qiyas_core.verbal_signified_adapter import VerbalSignifiedLayerAdapter
from qiyas_core.composition_readiness_adapter import CompositionReadinessLayerAdapter
from qiyas_core.amil_mamul_adapter import (
    AMIL_MAMUL_PRIOR_TYPE_PREFIX,
    COMPOSITION_READINESS_CANDIDATE_REF_PREFIX,
    OPENED_PRIOR_PREFIX,
    RELATION_GEOMETRY_EVIDENCE_PREFIX,
    RELATION_POSSIBILITY_PREFIX,
    AmilMamulLayerAdapter,
)
from qiyas_core.rules.amil_mamul_rules import (
    ALLOWED_AMIL_MAMUL_PRIOR_TYPES,
    AMIL_MAMUL_RULE,
    COMPACT_RELATION_POSSIBILITY,
    OPENED_PRIORS,
    RELATION_CADENCE_GEOMETRY_CLASS,
    RELATION_GEOMETRY_UNDERSPECIFIED,
)

# i'rab / case / grammatical labels that must NEVER be a P8 prior_type.
_GRAMMATICAL_FORBIDDEN = {"Amil", "Mamul", "Marfu", "Mansub", "Majrur", "Nominative",
                         "Accusative", "Genitive", "Subject", "Object", "Irab"}

# Structural codepoint sequences (purely geometric).
_DARABA = [0x0636, 0x064E, 0x0631, 0x064E, 0x0628, 0x064E]            # CVCVCV  vowels3 (P8 acc, cadence)
_SHADDAB = [0x0634, 0x064E, 0x062F, 0x0651, 0x064E, 0x0628, 0x064E]   # CVCCVCV vowels3 gem (P8 acc, compact)
_KATAB = [0x0643, 0x064E, 0x062A, 0x064E, 0x0628]                    # CVCVC   vowels2 (P7 acc; P8 DEFER)
_SHADHTH = [0x0634, 0x064E, 0x0627, 0x0630, 0x0651]                  # CVVCC   (P7 DEFER -> block)


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


def _verbal_signified(profile_cps):
    k = QiyasKernel()
    rs = RootStemLayerAdapter(kernel=k).close(
        _projection(), sequence_profile=build_sequence_profile(profile_cps)
    ).accepted[0]
    jm = JamidMushtaqLayerAdapter(kernel=k).classify(rs).accepted[0]
    mw = MufradWordLayerAdapter(kernel=k).form(jm).accepted[0]
    return VerbalSignifiedLayerAdapter(kernel=k).open(mw).accepted[0]


def _composition_readiness(profile_cps=_DARABA):
    """An accepted CompositionReadinessCandidate carrying P7 evidence for the profile."""
    vs = _verbal_signified(profile_cps)
    return CompositionReadinessLayerAdapter(kernel=QiyasKernel()).attest(vs).accepted[0]


def _deferred_composition_readiness():
    """A P7-DEFERRED CompositionReadinessCandidate (شَاذّ: ambiguous boundary)."""
    vs = _verbal_signified(_SHADHTH)
    return CompositionReadinessLayerAdapter(kernel=QiyasKernel()).attest(vs).deferred[0]


def _relate(cr):
    return AmilMamulLayerAdapter(kernel=QiyasKernel()).relate(cr)


def _has_trace(candidate, prefix):
    return any(t.startswith(prefix) for t in candidate.trace_ids)


def _trace_value(candidate, prefix):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 1. RUN
# ─────────────────────────────────────────────────────────────────────────────


def test_P8_RUN_01_composition_readiness_relates_to_amil_mamul_candidate():
    result = _relate(_composition_readiness())
    assert result.accepted
    assert result.accepted[0].candidate_type == "AmilMamulCandidate"


def test_P8_RUN_02_consumes_composition_readiness_far_type():
    assert AMIL_MAMUL_RULE.far_type == "CompositionReadinessCandidate"
    assert AMIL_MAMUL_RULE.output_candidate_type == "AmilMamulCandidate"


def test_P8_RUN_03_candidate_only():
    assert "CandidateOnly" in _relate(_composition_readiness()).accepted[0].output_flags


def test_P8_RUN_04_does_not_relate_every_operand_blindly():
    # كَتَب (CVCVC, 2 vowels): P7-accepted operand but relation-thin -> NOT accepted.
    assert not _relate(_composition_readiness(_KATAB)).accepted


# ─────────────────────────────────────────────────────────────────────────────
# 2. VERDICT
# ─────────────────────────────────────────────────────────────────────────────


def test_P8_VERDICT_01_accept_visible_in_evidence():
    c = _relate(_composition_readiness(_DARABA)).accepted[0]
    ev = _trace_value(c, RELATION_GEOMETRY_EVIDENCE_PREFIX)
    assert ev is not None and "verdict=accept" in ev and "p7verdict=accept" in ev


def test_P8_VERDICT_02_compact_operand_defers():
    result = _relate(_composition_readiness(_KATAB))  # 2 vowels — relation-thin
    assert result.deferred and not result.accepted and not result.blocked


def test_P8_VERDICT_03_non_accepted_p7_blocks():
    result = _relate(_deferred_composition_readiness())
    assert result.blocked and not result.accepted


# ─────────────────────────────────────────────────────────────────────────────
# 3. INFORMATION_GAIN
# ─────────────────────────────────────────────────────────────────────────────


def test_P8_INFOGAIN_01_p7_accepted_but_p8_deferred_exists():
    # كَتَب is ACCEPTED by P7 (clean composition operand) yet DEFERRED by P8
    # (relation geometry too thin): P8 accepted count < P7 accepted count.
    cr = _composition_readiness(_KATAB)
    assert cr.candidate_type == "CompositionReadinessCandidate"  # P7 accepted
    assert not _relate(cr).accepted                              # P8 does not accept


def test_P8_INFOGAIN_02_prior_type_is_input_dependent():
    pt_cadence = _trace_value(_relate(_composition_readiness(_DARABA)).accepted[0],
                              AMIL_MAMUL_PRIOR_TYPE_PREFIX)
    pt_gem = _trace_value(_relate(_composition_readiness(_SHADDAB)).accepted[0],
                          AMIL_MAMUL_PRIOR_TYPE_PREFIX)
    assert pt_cadence == RELATION_CADENCE_GEOMETRY_CLASS
    assert pt_gem == COMPACT_RELATION_POSSIBILITY
    assert pt_cadence != pt_gem


def test_P8_INFOGAIN_03_relation_evidence_is_real_not_constant():
    e1 = _trace_value(_relate(_composition_readiness(_DARABA)).accepted[0], RELATION_GEOMETRY_EVIDENCE_PREFIX)
    e2 = _trace_value(_relate(_composition_readiness(_SHADDAB)).accepted[0], RELATION_GEOMETRY_EVIDENCE_PREFIX)
    assert e1 != e2 and "vowels=3" in e1 and "gem=1" in e2


# ─────────────────────────────────────────────────────────────────────────────
# 4. STRUCTURAL_ONLY — relation possibility; prior type NEVER grammatical/case
# ─────────────────────────────────────────────────────────────────────────────


def test_P8_STRUCTURAL_01_carries_structural_relation_possibility():
    c = _relate(_composition_readiness(_DARABA)).accepted[0]
    sig = _trace_value(c, RELATION_POSSIBILITY_PREFIX)
    assert sig is not None and sig.startswith("relsig:")  # geometry signature, no syntax


def test_P8_STRUCTURAL_02_prior_type_is_structural_not_grammatical():
    for prof in (_DARABA, _SHADDAB):
        pt = _trace_value(_relate(_composition_readiness(prof)).accepted[0], AMIL_MAMUL_PRIOR_TYPE_PREFIX)
        assert pt in ALLOWED_AMIL_MAMUL_PRIOR_TYPES, pt
        assert pt not in _GRAMMATICAL_FORBIDDEN


def test_P8_STRUCTURAL_03_carries_composition_readiness_ref():
    c = _relate(_composition_readiness()).accepted[0]
    assert _has_trace(c, COMPOSITION_READINESS_CANDIDATE_REF_PREFIX)


def test_P8_STRUCTURAL_04_opens_grammatical_relation_and_irab_priors_on_accept_only():
    c = _relate(_composition_readiness()).accepted[0]
    opened = {t[len(OPENED_PRIOR_PREFIX):] for t in c.trace_ids if t.startswith(OPENED_PRIOR_PREFIX)}
    assert opened == set(OPENED_PRIORS) == {"grammatical_relation_priors", "irab_priors"}
    # deferred -> opens nothing
    d = _relate(_composition_readiness(_KATAB)).deferred[0]
    assert not _has_trace(d, OPENED_PRIOR_PREFIX)


def test_P8_STRUCTURAL_05_does_not_emit_sentence_geometry():
    c = _relate(_composition_readiness()).accepted[0]
    assert c.candidate_type == "AmilMamulCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# 5. IDENTITY_STABILITY
# ─────────────────────────────────────────────────────────────────────────────


def test_P8_IDENTITY_01_preserves_upstream_identities():
    cr = _composition_readiness()
    c = _relate(cr).accepted[0]
    for iid in cr.identity_ids:
        assert iid in c.identity_ids, iid


def test_P8_IDENTITY_02_defer_and_block_preserve_identity():
    cr_thin = _composition_readiness(_KATAB)
    d = _relate(cr_thin).deferred[0]
    for iid in cr_thin.identity_ids:
        assert iid in d.identity_ids
    cr_def = _deferred_composition_readiness()
    b = _relate(cr_def).blocked[0]
    for iid in cr_def.identity_ids:
        assert iid in b.identity_ids


def test_P8_IDENTITY_03_identity_disjoint_and_candidate_only():
    c = _relate(_composition_readiness()).accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))
    assert "CandidateOnly" in c.output_flags


def test_P8_DEFER_residual_is_explicit():
    d = _relate(_composition_readiness(_KATAB)).deferred[0]
    assert f"deferred_{RELATION_GEOMETRY_UNDERSPECIFIED}" in {r.residual_type for r in d.residuals}


# ─────────────────────────────────────────────────────────────────────────────
# 6. FORBIDDEN_DOWNSTREAM — no i'rab / case / meaning / hukm; no-jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P8_FORBIDDEN_01_no_irab_no_case_no_meaning_no_hukm():
    forbidden = set(AMIL_MAMUL_RULE.forbidden_outputs)
    for name in ("IrabCandidate", "IrabJudgment", "CaseEffect", "CaseJudgment", "Irab",
                 "MeaningCandidate", "DalalahCandidate", "DalalahJudgment", "TafsirCandidate",
                 "HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden, name


def test_P8_FORBIDDEN_02_no_jump_to_p9_plus():
    forbidden = set(AMIL_MAMUL_RULE.forbidden_outputs)
    for name in ("SentenceGeometryCandidate", "RelationGeometryCandidate",
                 "IrabGeometryCandidate", "IfadahCandidate"):
        assert name in forbidden, name


def test_P8_FORBIDDEN_03_output_always_amil_mamul():
    for prof in (_DARABA, _SHADDAB, _KATAB):
        for c in _relate(_composition_readiness(prof)).candidates:
            assert c.candidate_type == "AmilMamulCandidate"


def test_P8_FORBIDDEN_04_residual_diffs_explicit():
    assert AMIL_MAMUL_RULE.invalidating_differences
