"""qiyas_scg_ladder_state — terminal-visible SCG ladder state up to SCG-P1.

Read-only, potential-only renderer that shows what the system can produce now
that SCG-P1 is fully IMPLEMENTED (Letter, Haraka, ConditionedTypedSequence,
Position, Slot). It makes NO semantic / hukm / i'rab / dalalah / meaning /
reality claim, introduces NO P2+ layer, and changes NO verifier semantics.

It composes only OFFICIAL runtime paths:
  - qiyas_core.qiyas_structural_verification.verify_token_structure
      → structural status (covered_direct / covered_via_shadda_expansion /
        residual), identity preservation, shadda-expansion trace + CV cover.
  - run_qiyas.process_text  (the official Phase-1 driver)
      → the SCG-P1 ladder evidence per token (LetterIdentityCarrier,
        HarakaMarkIdentityCarrier, ConditionedTypedSequence evidence family,
        PositionCarrier, SlotCandidate).
  - qiyas_core.slot_geometry_core.build_p1_slot_implemented_registry
      → canonical registry state (P0 + all five P1 IMPLEMENTED; P2-P12 SPECIFIED).

Run:
    PYTHONPATH=src:. python3 tools/qiyas_scg_ladder_state.py "شَاذّ عَدَّ بَ مَا مِن بَاب بَيت ض ضَرَبَ"
"""

from __future__ import annotations

import os
import sys

# Allow `import run_qiyas` (repo-root Phase-1 driver) regardless of whether the
# caller put repo root on PYTHONPATH (e.g. `PYTHONPATH=src` vs `PYTHONPATH=src:.`).
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from qiyas_core.qiyas_structural_verification import (
    COVERED_DIRECT,
    COVERED_VIA_SHADDA_EXPANSION,
    NOT_INTRODUCED,
    verify_token_structure,
)
from qiyas_core.slot_geometry_core import (
    LayerStatus,
    build_p11_implemented_registry,
)

import run_qiyas  # official Phase-1 driver (repo-root module; needs `.` on path)

# Canonical SCG ladder candidate types surfaced now (P1..P8 implemented).
_LETTER = "LetterIdentityCarrier"
_HARAKA = "HarakaMarkIdentityCarrier"
_CTS_FAMILY = ("CarrierBindingCandidate", "PositionEvidence",
               "BoundaryEvidence", "ResidualPreservationEvidence")
_POSITION = "PositionCarrier"
_SLOT = "SlotCandidate"
_PROJECTION = "RegistryProjectionCandidate"  # SCG-P2 (implemented)
_ROOTSTEM = "RootStemCandidate"              # SCG-P3 (implemented)
_JAMID = "JamidMushtaqCandidate"             # SCG-P4 (implemented)
_MUFRAD = "MufradWordCandidate"              # SCG-P5 (implemented)
_VERBAL = "VerbalSignifiedCandidate"         # SCG-P6 (implemented)
_COMPREADY = "CompositionReadinessCandidate"  # SCG-P7 (implemented)
_AMIL = "AmilMamulCandidate"                 # SCG-P8 (now implemented)
_SG_EVIDENCE_PREFIX = "sentence_geometry_evidence:"  # SCG-P9 evidence trace marker
_RG_EVIDENCE_PREFIX = "relation_geometry_evidence:"  # SCG-P10 evidence trace marker
_IG_EVIDENCE_PREFIX = "irab_geometry_evidence:"      # SCG-P11 evidence trace marker

# Higher-layer / semantic outputs that MUST NOT appear yet (no-jump guard).
# P2..P11 are now IMPLEMENTED, so they are expected. SCG-P12 (IfadahCandidate)
# and above remain not_introduced.
_FORBIDDEN_HIGHER = (
    "IfadahCandidate", "CaseJudgment", "IrabFinalDecision",
    "SlotGeometry", "HukmCandidate", "RealityClaim", "FinalMeaning",
)


def _accepted_steps(reports):
    """All accepted LayerStep objects across a token's CharacterReports."""
    steps = []
    for r in reports:
        for s in r.steps:
            if s.status == "accepted":
                steps.append(s)
        if r.slot_step is not None and r.slot_step.status == "accepted":
            steps.append(r.slot_step)
    return steps


def _cover_str(shapes: tuple[tuple[str, ...], ...]) -> str:
    """Render covering shapes, e.g. (("CVVCC",),) -> 'CVVCC'; (("CVC","CV"),) -> 'CVC/CV'."""
    if not shapes:
        return "—"
    return " | ".join("/".join(cells) for cells in shapes)


def _ladder_counts(steps):
    types = [s.candidate_type for s in steps]
    return {
        _LETTER: types.count(_LETTER),
        _HARAKA: types.count(_HARAKA),
        "CTS(CarrierBinding)": types.count("CarrierBindingCandidate"),
        "CTS(PositionEvidence)": types.count("PositionEvidence"),
        _POSITION: types.count(_POSITION),
        _SLOT: types.count(_SLOT),
        _PROJECTION: types.count(_PROJECTION),
        _ROOTSTEM: types.count(_ROOTSTEM),
        _JAMID: types.count(_JAMID),
        _MUFRAD: types.count(_MUFRAD),
        _VERBAL: types.count(_VERBAL),
        _COMPREADY: types.count(_COMPREADY),
        _AMIL: types.count(_AMIL),
    }


def _rootstem_verdicts(reports):
    """SCG-P3 status breakdown (accepted/deferred/blocked) + CV signature + residuals
    across a token's RootStemQiyas steps (any status, not only accepted)."""
    acc = dfr = blk = 0
    cv = None
    residuals: set = set()
    for r in reports:
        for s in r.steps:
            if s.layer != "RootStemQiyas":
                continue
            if s.status == "accepted":
                acc += 1
            elif s.status == "deferred":
                dfr += 1
            elif s.status == "blocked":
                blk += 1
            for t in s.trace_ids:
                if t.startswith("root_pattern_evidence:") and "cv=" in t:
                    cv = t.split("cv=", 1)[1].split(";", 1)[0]
            for res in s.residuals:
                residuals.add(res["type"])
    return acc, dfr, blk, cv, sorted(residuals)


def _layer_status_breakdown(reports, layer):
    """(accepted, deferred, blocked, sorted residual types) across a layer's steps."""
    acc = dfr = blk = 0
    residuals: set = set()
    for r in reports:
        for s in r.steps:
            if s.layer != layer:
                continue
            if s.status == "accepted":
                acc += 1
            elif s.status == "deferred":
                dfr += 1
            elif s.status == "blocked":
                blk += 1
            for res in s.residuals:
                residuals.add(res["type"])
    return acc, dfr, blk, sorted(residuals)


def _opened_priors_and_types(steps, candidate_type):
    """Opened priors + membership_prior_type(s) carried by steps of a type."""
    priors: set = set()
    prior_types: set = set()
    for s in steps:
        if s.candidate_type != candidate_type:
            continue
        for t in s.trace_ids:
            if t.startswith("opens_prior:"):
                priors.add(t.split(":", 1)[1])
            elif t.startswith("membership_prior_type:"):
                prior_types.add(t.split(":", 1)[1])
    return sorted(priors), sorted(prior_types)


def render_token(token: str) -> tuple[str, dict, set]:
    v = verify_token_structure(token)
    reports = run_qiyas.process_text(token)
    steps = _accepted_steps(reports)
    counts = _ladder_counts(steps)
    seen_types = {s.candidate_type for s in steps}
    higher = seen_types & set(_FORBIDDEN_HIGHER)

    if v.final_status == COVERED_DIRECT:
        cover = _cover_str(v.direct_covering_shapes)
    elif v.final_status == COVERED_VIA_SHADDA_EXPANSION:
        cover = _cover_str(v.shadda_expansion_covering_shapes)
    else:
        cover = "—"

    lines = []
    lines.append(f"── token: {token}")
    lines.append(f"   structural_status      : {v.final_status}")
    lines.append(f"   identity_surface       : {v.identity_surface!r}")
    lines.append(f"   identity_codepoints    : {' '.join(v.identity_codepoints)}")
    lines.append(f"   identity_preserved     : {v.identity_preserved}")
    lines.append(f"   shadda_present (U+0651): {v.shadda_present}")
    if v.shadda_expansion_trace:
        lines.append(f"   shadda_expansion_trace : {token} -> {v.shadda_expansion_trace}  (trace only)")
    lines.append(f"   structural_cover (CV)  : {cover}")
    lines.append("   SCG-P1 ladder evidence :")
    lines.append(f"       LetterIdentityCarrier        = {counts[_LETTER]}")
    lines.append(f"       HarakaMarkIdentityCarrier    = {counts[_HARAKA]}")
    lines.append(f"       ConditionedTypedSequence     = "
                 f"CarrierBinding:{counts['CTS(CarrierBinding)']} "
                 f"PositionEvidence:{counts['CTS(PositionEvidence)']}")
    lines.append(f"       PositionCarrier              = {counts[_POSITION]}")
    lines.append(f"       SlotCandidate                = {counts[_SLOT]}")
    p2_priors, prior_types = _opened_priors_and_types(steps, _PROJECTION)
    lines.append("   SCG-P2 projection :")
    lines.append(f"       RegistryProjectionCandidate  = {counts[_PROJECTION]}")
    lines.append(f"       membership_prior_type        = "
                 f"{', '.join(prior_types) if prior_types else '—'} (structural)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p2_priors) if p2_priors else '—'}")
    p3_priors, _ = _opened_priors_and_types(steps, _ROOTSTEM)
    p3_acc, p3_dfr, p3_blk, p3_cv, p3_res = _rootstem_verdicts(reports)
    counts["_P3_DEFER"] = p3_dfr
    counts["_P3_BLOCK"] = p3_blk
    lines.append("   SCG-P3 root/stem closure (information-gain) :")
    lines.append(f"       RootStemCandidate (accepted) = {counts[_ROOTSTEM]} (candidate-only)")
    lines.append(f"       structural verdict           = "
                 f"accept:{p3_acc} defer:{p3_dfr} block:{p3_blk}")
    lines.append(f"       CV signature (structural)    = {p3_cv or '—'}")
    lines.append(f"       residuals                    = "
                 f"{', '.join(p3_res) if p3_res else 'none'}")
    lines.append(f"       final root judgment          = none (RootCandidate forbidden)")
    lines.append(f"       wazn                         = none (WeightCandidate forbidden)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p3_priors) if p3_priors else '—'} (ACCEPT only)")
    p4_priors, _ = _opened_priors_and_types(steps, _JAMID)
    jm_types = sorted({t.split(":", 1)[1] for s in steps if s.candidate_type == _JAMID
                       for t in s.trace_ids if t.startswith("jamid_mushtaq_prior_type:")})
    p4_acc, p4_dfr, p4_blk, p4_res = _layer_status_breakdown(reports, "JamidMushtaqQiyas")
    counts["_P4_DEFER"] = p4_dfr
    counts["_P4_BLOCK"] = p4_blk
    lines.append("   SCG-P4 jamid/mushtaq (information-gain) :")
    lines.append(f"       JamidMushtaqCandidate (accept)= {counts[_JAMID]} (candidate-only)")
    lines.append(f"       structural verdict           = "
                 f"accept:{p4_acc} defer:{p4_dfr} block:{p4_blk}")
    lines.append(f"       jamid_mushtaq_prior_type     = "
                 f"{', '.join(jm_types) if jm_types else '—'} (structural, input-dependent)")
    lines.append(f"       residuals                    = "
                 f"{', '.join(p4_res) if p4_res else 'none'}")
    lines.append(f"       final jamid/mushtaq judgment = none (WordTypeJudgment forbidden)")
    lines.append(f"       wazn                         = none (WeightCandidate forbidden)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p4_priors) if p4_priors else '—'} (ACCEPT only)")
    p5_priors, _ = _opened_priors_and_types(steps, _MUFRAD)
    p5_types = sorted({t.split(":", 1)[1] for s in steps if s.candidate_type == _MUFRAD
                       for t in s.trace_ids if t.startswith("mufrad_word_prior_type:")})
    p5_acc, p5_dfr, p5_blk, p5_res = _layer_status_breakdown(reports, "MufradWordQiyas")
    counts["_P5_DEFER"] = p5_dfr
    counts["_P5_BLOCK"] = p5_blk
    lines.append("   SCG-P5 mufrad word (information-gain) :")
    lines.append(f"       MufradWordCandidate (accept) = {counts[_MUFRAD]} (candidate-only)")
    lines.append(f"       structural verdict           = "
                 f"accept:{p5_acc} defer:{p5_dfr} block:{p5_blk}")
    lines.append(f"       mufrad_word_prior_type       = "
                 f"{', '.join(p5_types) if p5_types else '—'} (structural, input-dependent)")
    lines.append(f"       residuals                    = "
                 f"{', '.join(p5_res) if p5_res else 'none'}")
    lines.append(f"       final lexical word / مفرد    = none (WordCandidate forbidden)")
    lines.append(f"       dictionary entry / morphology = none")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p5_priors) if p5_priors else '—'} (ACCEPT only)")
    p6_priors, _ = _opened_priors_and_types(steps, _VERBAL)
    p6_types = sorted({t.split(":", 1)[1] for s in steps if s.candidate_type == _VERBAL
                       for t in s.trace_ids if t.startswith("verbal_signified_prior_type:")})
    p6_acc, p6_dfr, p6_blk, p6_res = _layer_status_breakdown(reports, "VerbalSignifiedQiyas")
    counts["_P6_DEFER"] = p6_dfr
    counts["_P6_BLOCK"] = p6_blk
    lines.append("   SCG-P6 verbal signified (information-gain) :")
    lines.append(f"       VerbalSignifiedCandidate(acc)= {counts[_VERBAL]} (candidate-only)")
    lines.append(f"       structural verdict           = "
                 f"accept:{p6_acc} defer:{p6_dfr} block:{p6_blk}")
    lines.append(f"       verbal_signified_prior_type  = "
                 f"{', '.join(p6_types) if p6_types else '—'} (structural, input-dependent)")
    lines.append(f"       residuals                    = "
                 f"{', '.join(p6_res) if p6_res else 'none'}")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p6_priors) if p6_priors else '—'} (ACCEPT only)")
    lines.append(f"       final فعل / verb / tense     = none (pre-semantic, structural)")
    lines.append(f"       MeaningCandidate             = not_introduced")
    lines.append(f"       DalalahJudgment              = not_introduced")
    p7_priors, _ = _opened_priors_and_types(steps, _COMPREADY)
    p7_types = sorted({t.split(":", 1)[1] for s in steps if s.candidate_type == _COMPREADY
                       for t in s.trace_ids if t.startswith("composition_readiness_prior_type:")})
    p7_acc, p7_dfr, p7_blk, p7_res = _layer_status_breakdown(reports, "CompositionReadinessQiyas")
    counts["_P7_DEFER"] = p7_dfr
    counts["_P7_BLOCK"] = p7_blk
    lines.append("   SCG-P7 composition readiness (information-gain) :")
    lines.append(f"       CompositionReadinessCand(acc)= {counts[_COMPREADY]} (candidate-only)")
    lines.append(f"       structural verdict           = "
                 f"accept:{p7_acc} defer:{p7_dfr} block:{p7_blk}")
    lines.append(f"       composition_readiness_prior  = "
                 f"{', '.join(p7_types) if p7_types else '—'} (structural, input-dependent)")
    lines.append(f"       residuals                    = "
                 f"{', '.join(p7_res) if p7_res else 'none'}")
    lines.append(f"       actual composition / syntax  = none (readiness gate only)")
    lines.append(f"       amil/mamul / i'rab           = none")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p7_priors) if p7_priors else '—'} (ACCEPT only)")
    p8_priors, _ = _opened_priors_and_types(steps, _AMIL)
    p8_types = sorted({t.split(":", 1)[1] for s in steps if s.candidate_type == _AMIL
                       for t in s.trace_ids if t.startswith("amil_mamul_prior_type:")})
    p8_acc, p8_dfr, p8_blk, p8_res = _layer_status_breakdown(reports, "AmilMamulQiyas")
    counts["_P8_DEFER"] = p8_dfr
    counts["_P8_BLOCK"] = p8_blk
    lines.append("   SCG-P8 amil/mamul (information-gain) :")
    lines.append(f"       AmilMamulCandidate (accept)  = {counts[_AMIL]} (candidate-only)")
    lines.append(f"       structural verdict           = "
                 f"accept:{p8_acc} defer:{p8_dfr} block:{p8_blk}")
    lines.append(f"       amil_mamul_prior_type        = "
                 f"{', '.join(p8_types) if p8_types else '—'} (structural, input-dependent)")
    lines.append(f"       residuals                    = "
                 f"{', '.join(p8_res) if p8_res else 'none'}")
    lines.append(f"       actual i'rab / case / amil   = none (relation-possibility only)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p8_priors) if p8_priors else '—'} (ACCEPT only)")
    lines.append(f"       IrabCandidate                = not_introduced")
    lines.append(f"       MeaningCandidate             = not_introduced")
    lines.append(f"       HukmCandidate                = not_introduced")
    lines.append("   SCG-P9 :")
    lines.append(f"       SentenceGeometryCandidate    = sentence-level "
                 f"(single word is one unit → see P9 section)")
    lines.append("   SCG-P10 :")
    lines.append(f"       RelationGeometryCandidate    = sentence-level "
                 f"(behind accepted P9 → see P10 section)")
    lines.append("   SCG-P11 :")
    lines.append(f"       IrabGeometryCandidate        = sentence-level "
                 f"(behind accepted P10 → see P11 section)")
    lines.append("   SCG-P12+ :")
    lines.append(f"       IfadahCandidate              = not_introduced")
    lines.append(f"   higher-layer candidates present : "
                 f"{sorted(higher) if higher else 'none'}")
    lines.append(f"   semantic statuses      : meaning={v.meaning_status} hukm={v.hukm_status} "
                 f"irab={v.irab_status} dalalah={v.dalalah_status} reality={v.reality_status}")
    return "\n".join(lines), counts, higher


def render_registry_state() -> str:
    reg = build_p11_implemented_registry()
    by_phase: dict[str, list] = {}
    for s in reg.all_layers():
        by_phase.setdefault(s.phase, []).append(s.status)
    kp = lambda p: int(p.split("P")[1])
    impl = lambda ph: all(st is LayerStatus.IMPLEMENTED for st in by_phase.get(ph, []))
    p12_spec = all(
        st is LayerStatus.SPECIFIED
        for ph, sts in by_phase.items()
        if ph not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4",
                      "SCG-P5", "SCG-P6", "SCG-P7", "SCG-P8", "SCG-P9", "SCG-P10",
                      "SCG-P11")
        for st in sts
    )
    count = sum(len(v) for v in by_phase.values())
    lines = ["── registry state (build_p11_implemented_registry)"]
    for ph in sorted(by_phase, key=kp):
        vals = sorted({st.value for st in by_phase[ph]})
        lines.append(f"   {ph:8} {','.join(vals)} ({len(by_phase[ph])})")
    lines.append(f"   P0 IMPLEMENTED               : {impl('SCG-P0')}")
    lines.append(f"   P1 all five IMPLEMENTED       : {impl('SCG-P1')}")
    lines.append(f"   P2 RegistryProjection IMPL    : {impl('SCG-P2')}")
    lines.append(f"   P3 RootStemClosure IMPL       : {impl('SCG-P3')}")
    lines.append(f"   P4 JamidMushtaq IMPL          : {impl('SCG-P4')}")
    lines.append(f"   P5 MufradWord IMPL            : {impl('SCG-P5')}")
    lines.append(f"   P6 VerbalSignified IMPL       : {impl('SCG-P6')}")
    lines.append(f"   P7 CompositionReadiness IMPL  : {impl('SCG-P7')}")
    lines.append(f"   P8 AmilMamul IMPL             : {impl('SCG-P8')}")
    lines.append(f"   P9 SentenceGeometry IMPL      : {impl('SCG-P9')}")
    lines.append(f"   P10 RelationGeometry IMPL     : {impl('SCG-P10')}")
    lines.append(f"   P11 IrabGeometry IMPL         : {impl('SCG-P11')}")
    lines.append(f"   P12 SPECIFIED                : {p12_spec}")
    lines.append(f"   layer count                   : {count}")
    lines.append(f"   freeze ACTIVE for P12         : {p12_spec} "
                 f"(no P12+ layer is IMPLEMENTED)")
    return "\n".join(lines)


def render_relation_geometry(text: str) -> str:
    """SCG-P10 refines a relation geometry from an accepted P9 sentence geometry.
    It appears ONLY behind an accepted P9 step; on ACCEPT it opens only
    irab_geometry_candidates and closes relation_geometry_candidates."""
    reports = run_qiyas.process_text(text)
    rg_steps = [
        s for r in reports for s in r.steps if s.layer == "RelationGeometryQiyas"
    ]
    lines = ["── SCG-P10 relation geometry (behind accepted P9 only)"]
    if not rg_steps:
        lines.append("   RelationGeometryCandidate    = not_introduced "
                     "(no accepted P9 sentence geometry to refine)")
        return "\n".join(lines)
    for s in rg_steps:
        scope = rtype = dep = verdict = "?"
        opened: list[str] = []
        closed: list[str] = []
        for t in s.trace_ids:
            if t.startswith(_RG_EVIDENCE_PREFIX):
                for kv in t.split(":", 1)[1].split(";"):
                    if kv.startswith("relation_scope_closed="):
                        scope = kv.split("=", 1)[1]
                    elif kv.startswith("relation_type="):
                        rtype = kv.split("=", 1)[1]
                    elif kv.startswith("dependency_scope="):
                        dep = kv.split("=", 1)[1]
                    elif kv.startswith("verdict="):
                        verdict = kv.split("=", 1)[1]
            elif t.startswith("opens_prior:"):
                opened.append(t.split(":", 1)[1])
            elif t.startswith("closes_prior:"):
                closed.append(t.split(":", 1)[1])
        residuals = sorted({res["type"] for res in s.residuals})
        lines.append(f"   RelationGeometryCandidate    = {s.status} "
                     f"(verdict={verdict})")
        lines.append(f"   relation scope closed        = {scope}")
        lines.append(f"   relation-type / dependency   = {rtype} / {dep}")
        lines.append(f"   opened priors                = {opened or 'none'} "
                     f"(P10 opens ONLY irab_geometry_candidates)")
        lines.append(f"   closed priors                = {closed or 'none'}")
        lines.append(f"   residual reasons             = {residuals or 'none'}")
    return "\n".join(lines)


def render_irab_geometry(text: str) -> str:
    """SCG-P11 refines an i'rab-position geometry from an accepted P10 relation
    geometry. It appears ONLY behind an accepted P10 step; on ACCEPT it opens only
    ifadah_speech_force_candidates and closes irab_geometry_candidates. It maps
    i'rab POSITIONS as possibilities — never an i'rab verdict."""
    reports = run_qiyas.process_text(text)
    ig_steps = [
        s for r in reports for s in r.steps if s.layer == "IrabGeometryQiyas"
    ]
    lines = ["── SCG-P11 i'rab geometry (positions, not verdict; behind accepted P10 only)"]
    if not ig_steps:
        lines.append("   IrabGeometryCandidate        = not_introduced "
                     "(no accepted P10 relation geometry to refine)")
        return "\n".join(lines)
    for s in ig_steps:
        ctx = pos = mark = waqf = verdict = "?"
        opened: list[str] = []
        closed: list[str] = []
        for t in s.trace_ids:
            if t.startswith(_IG_EVIDENCE_PREFIX):
                for kv in t.split(":", 1)[1].split(";"):
                    if kv.startswith("irab_context_closed="):
                        ctx = kv.split("=", 1)[1]
                    elif kv.startswith("irab_position="):
                        pos = kv.split("=", 1)[1]
                    elif kv.startswith("case_marker="):
                        mark = kv.split("=", 1)[1]
                    elif kv.startswith("waqf_readiness="):
                        waqf = kv.split("=", 1)[1]
                    elif kv.startswith("verdict="):
                        verdict = kv.split("=", 1)[1]
            elif t.startswith("opens_prior:"):
                opened.append(t.split(":", 1)[1])
            elif t.startswith("closes_prior:"):
                closed.append(t.split(":", 1)[1])
        residuals = sorted({res["type"] for res in s.residuals})
        lines.append(f"   IrabGeometryCandidate        = {s.status} "
                     f"(verdict={verdict})")
        lines.append(f"   irab context closed          = {ctx}")
        lines.append(f"   position / marker / waqf     = {pos} / {mark} / {waqf} "
                     f"(possibilities, NOT a verdict)")
        lines.append(f"   opened priors                = {opened or 'none'} "
                     f"(P11 opens ONLY ifadah_speech_force_candidates)")
        lines.append(f"   closed priors                = {closed or 'none'}")
        lines.append(f"   residual reasons             = {residuals or 'none'}")
    return "\n".join(lines)


def render_sentence_geometry(text: str) -> str:
    """SCG-P9 is a SENTENCE-level layer: it composes ≥2 distinct word/segment
    units, each carrying accepted P8 evidence. A single word is ONE unit and
    therefore BLOCKs (n_raw<2). This pass runs the whole phrase once and reports
    the single P9 SentenceGeometryQiyas step attached to reports[0]."""
    reports = run_qiyas.process_text(text)
    sg_steps = [
        s for r in reports for s in r.steps if s.layer == "SentenceGeometryQiyas"
    ]
    lines = ["── SCG-P9 sentence geometry (sentence-level; ≥2 distinct units)"]
    if not sg_steps:
        lines.append("   SentenceGeometryCandidate    = not_introduced "
                     "(no sentence-level step emitted)")
        return "\n".join(lines)
    for s in sg_steps:
        units = distinct = adjacency = boundary = verdict = "?"
        priors: list[str] = []
        for t in s.trace_ids:
            if t.startswith(_SG_EVIDENCE_PREFIX):
                body = t.split(":", 1)[1]
                for kv in body.split(";"):
                    if kv.startswith("units="):
                        units = kv.split("=", 1)[1]
                    elif kv.startswith("distinct="):
                        distinct = kv.split("=", 1)[1]
                    elif kv.startswith("adjacency="):
                        adjacency = kv.split("=", 1)[1]
                    elif kv.startswith("boundary="):
                        boundary = kv.split("=", 1)[1]
                    elif kv.startswith("verdict="):
                        verdict = kv.split("=", 1)[1]
            elif t.startswith("opens_prior:"):
                priors.append(t.split(":", 1)[1])
        residuals = sorted({res["type"] for res in s.residuals})
        lines.append(f"   SentenceGeometryCandidate    = {s.status} "
                     f"(verdict={verdict})")
        lines.append(f"   units (raw / distinct)       = {units} / {distinct}")
        lines.append(f"   adjacency contiguous         = {adjacency}")
        lines.append(f"   isnad boundary closed        = {boundary}")
        lines.append(f"   opened priors                = {priors or 'none'} "
                     f"(P9 opens ONLY relation_geometry_candidates)")
        lines.append(f"   residual reasons             = {residuals or 'none'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    text = args[0] if args else "شَاذّ عَدَّ بَ مَا مِن بَاب بَيت ض ضَرَبَ"
    tokens = text.split()

    print("=" * 72)
    print("SCG LADDER STATE — up to SCG-P11 (structural, potential-only)")
    print("=" * 72)

    all_higher: set = set()
    total_slots = 0
    total_projections = 0
    total_rootstems = 0
    total_rootstem_defer = 0
    total_rootstem_block = 0
    total_jamid = 0
    total_jamid_defer = 0
    total_jamid_block = 0
    total_mufrad = 0
    total_mufrad_defer = 0
    total_mufrad_block = 0
    total_verbal = 0
    total_verbal_defer = 0
    total_verbal_block = 0
    total_compready = 0
    total_compready_defer = 0
    total_compready_block = 0
    total_amil = 0
    total_amil_defer = 0
    total_amil_block = 0
    residual_tokens = []
    for tok in tokens:
        block, counts, higher = render_token(tok)
        print(block)
        print()
        all_higher |= higher
        total_slots += counts[_SLOT]
        total_projections += counts[_PROJECTION]
        total_rootstems += counts[_ROOTSTEM]
        total_rootstem_defer += counts.get("_P3_DEFER", 0)
        total_rootstem_block += counts.get("_P3_BLOCK", 0)
        total_jamid += counts[_JAMID]
        total_jamid_defer += counts.get("_P4_DEFER", 0)
        total_jamid_block += counts.get("_P4_BLOCK", 0)
        total_mufrad += counts[_MUFRAD]
        total_mufrad_defer += counts.get("_P5_DEFER", 0)
        total_mufrad_block += counts.get("_P5_BLOCK", 0)
        total_verbal += counts[_VERBAL]
        total_verbal_defer += counts.get("_P6_DEFER", 0)
        total_verbal_block += counts.get("_P6_BLOCK", 0)
        total_compready += counts[_COMPREADY]
        total_compready_defer += counts.get("_P7_DEFER", 0)
        total_compready_block += counts.get("_P7_BLOCK", 0)
        total_amil += counts[_AMIL]
        total_amil_defer += counts.get("_P8_DEFER", 0)
        total_amil_block += counts.get("_P8_BLOCK", 0)
        if counts[_SLOT] == 0:
            residual_tokens.append(tok)

    print(render_registry_state())
    print()
    print(render_sentence_geometry(text))
    print()
    print(render_relation_geometry(text))
    print()
    print(render_irab_geometry(text))
    print()
    print("── aggregate")
    print(f"   total SlotCandidate count          : {total_slots}")
    print(f"   total RegistryProjectionCandidate  : {total_projections}")
    print(f"   total RootStemCandidate (accepted) : {total_rootstems} (candidate-only)")
    print(f"   total RootStem deferred/blocked    : "
          f"defer={total_rootstem_defer} block={total_rootstem_block} (P3 discrimination)")
    print(f"   total JamidMushtaqCandidate (accept): {total_jamid} (candidate-only)")
    print(f"   total JamidMushtaq deferred/blocked: "
          f"defer={total_jamid_defer} block={total_jamid_block} (P4 discrimination)")
    print(f"   total MufradWordCandidate (accept) : {total_mufrad} (candidate-only)")
    print(f"   total MufradWord deferred/blocked  : "
          f"defer={total_mufrad_defer} block={total_mufrad_block} (P5 discrimination)")
    print(f"   total VerbalSignifiedCandidate(acc): {total_verbal} (candidate-only)")
    print(f"   total VerbalSignified def/blocked  : "
          f"defer={total_verbal_defer} block={total_verbal_block} (P6 discrimination)")
    print(f"   total CompositionReadinessCand(acc): {total_compready} (candidate-only)")
    print(f"   total CompositionReadiness def/blk : "
          f"defer={total_compready_defer} block={total_compready_block} (P7 discrimination)")
    print(f"   total AmilMamulCandidate (accept)  : {total_amil} (candidate-only)")
    print(f"   total AmilMamul deferred/blocked   : "
          f"defer={total_amil_defer} block={total_amil_block} (P8 discrimination)")
    print(f"   tokens with no SlotCandidate       : {residual_tokens or 'none'}")
    print(f"   P12+/semantic candidates seen      : {sorted(all_higher) if all_higher else 'none'}")
    print(f"   higher semantic statuses           : not_introduced "
          f"(constant: {NOT_INTRODUCED})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
