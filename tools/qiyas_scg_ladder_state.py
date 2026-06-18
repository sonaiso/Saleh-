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
    build_p7_implemented_registry,
)

import run_qiyas  # official Phase-1 driver (repo-root module; needs `.` on path)

# Canonical SCG ladder candidate types surfaced now (P1..P7 implemented).
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
_COMPREADY = "CompositionReadinessCandidate"  # SCG-P7 (now implemented)

# Higher-layer / semantic outputs that MUST NOT appear yet (no-jump guard).
# P2..P7 are now IMPLEMENTED, so they are expected. SCG-P8 (AmilMamulCandidate)
# and above remain not_introduced.
_FORBIDDEN_HIGHER = (
    "AmilMamulCandidate", "SentenceGeometryCandidate",
    "RelationGeometryCandidate", "IrabGeometryCandidate", "IfadahCandidate",
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
    }


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
    lines.append("   SCG-P3 root/stem closure :")
    lines.append(f"       RootStemCandidate            = {counts[_ROOTSTEM]} (candidate-only)")
    lines.append(f"       final root judgment          = none (RootCandidate forbidden)")
    lines.append(f"       wazn                         = none (WeightCandidate forbidden)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p3_priors) if p3_priors else '—'}")
    p4_priors, _ = _opened_priors_and_types(steps, _JAMID)
    jm_types = sorted({t.split(":", 1)[1] for s in steps if s.candidate_type == _JAMID
                       for t in s.trace_ids if t.startswith("jamid_mushtaq_prior_type:")})
    lines.append("   SCG-P4 jamid/mushtaq :")
    lines.append(f"       JamidMushtaqCandidate        = {counts[_JAMID]} (candidate-only)")
    lines.append(f"       jamid_mushtaq_prior_type     = "
                 f"{', '.join(jm_types) if jm_types else '—'} (structural)")
    lines.append(f"       final jamid/mushtaq judgment = none (WordTypeJudgment forbidden)")
    lines.append(f"       wazn                         = none (WeightCandidate forbidden)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p4_priors) if p4_priors else '—'}")
    p5_priors, _ = _opened_priors_and_types(steps, _MUFRAD)
    lines.append("   SCG-P5 mufrad word :")
    lines.append(f"       MufradWordCandidate          = {counts[_MUFRAD]} (candidate-only)")
    lines.append(f"       final lexical word           = none (WordCandidate forbidden)")
    lines.append(f"       dictionary entry / morphology = none")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p5_priors) if p5_priors else '—'}")
    p6_priors, _ = _opened_priors_and_types(steps, _VERBAL)
    lines.append("   SCG-P6 verbal signified :")
    lines.append(f"       VerbalSignifiedCandidate     = {counts[_VERBAL]} (candidate-only)")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p6_priors) if p6_priors else '—'}")
    lines.append(f"       MeaningCandidate             = not_introduced")
    lines.append(f"       DalalahJudgment              = not_introduced")
    p7_priors, _ = _opened_priors_and_types(steps, _COMPREADY)
    lines.append("   SCG-P7 composition readiness :")
    lines.append(f"       CompositionReadinessCandidate= {counts[_COMPREADY]} (candidate-only)")
    lines.append(f"       actual composition / syntax  = none")
    lines.append(f"       amil/mamul / i'rab           = none")
    lines.append(f"       opened priors                = "
                 f"{', '.join(p7_priors) if p7_priors else '—'}")
    lines.append("   SCG-P8+ :")
    lines.append(f"       AmilMamulCandidate           = not_introduced")
    lines.append(f"       SentenceGeometryCandidate    = not_introduced")
    lines.append(f"       IrabGeometryCandidate        = not_introduced")
    lines.append(f"   higher-layer candidates present : "
                 f"{sorted(higher) if higher else 'none'}")
    lines.append(f"   semantic statuses      : meaning={v.meaning_status} hukm={v.hukm_status} "
                 f"irab={v.irab_status} dalalah={v.dalalah_status} reality={v.reality_status}")
    return "\n".join(lines), counts, higher


def render_registry_state() -> str:
    reg = build_p7_implemented_registry()
    by_phase: dict[str, list] = {}
    for s in reg.all_layers():
        by_phase.setdefault(s.phase, []).append(s.status)
    kp = lambda p: int(p.split("P")[1])
    impl = lambda ph: all(st is LayerStatus.IMPLEMENTED for st in by_phase.get(ph, []))
    p8_p12_spec = all(
        st is LayerStatus.SPECIFIED
        for ph, sts in by_phase.items()
        if ph not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6", "SCG-P7")
        for st in sts
    )
    count = sum(len(v) for v in by_phase.values())
    lines = ["── registry state (build_p7_implemented_registry)"]
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
    lines.append(f"   P8-P12 SPECIFIED              : {p8_p12_spec}")
    lines.append(f"   layer count                   : {count}")
    lines.append(f"   freeze ACTIVE for P8-P12      : {p8_p12_spec} "
                 f"(no P8+ layer is IMPLEMENTED)")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    text = args[0] if args else "شَاذّ عَدَّ بَ مَا مِن بَاب بَيت ض ضَرَبَ"
    tokens = text.split()

    print("=" * 72)
    print("SCG LADDER STATE — up to SCG-P7 (structural, potential-only)")
    print("=" * 72)

    all_higher: set = set()
    total_slots = 0
    total_projections = 0
    total_rootstems = 0
    total_jamid = 0
    total_mufrad = 0
    total_verbal = 0
    total_compready = 0
    residual_tokens = []
    for tok in tokens:
        block, counts, higher = render_token(tok)
        print(block)
        print()
        all_higher |= higher
        total_slots += counts[_SLOT]
        total_projections += counts[_PROJECTION]
        total_rootstems += counts[_ROOTSTEM]
        total_jamid += counts[_JAMID]
        total_mufrad += counts[_MUFRAD]
        total_verbal += counts[_VERBAL]
        total_compready += counts[_COMPREADY]
        if counts[_SLOT] == 0:
            residual_tokens.append(tok)

    print(render_registry_state())
    print()
    print("── aggregate")
    print(f"   total SlotCandidate count          : {total_slots}")
    print(f"   total RegistryProjectionCandidate  : {total_projections}")
    print(f"   total RootStemCandidate            : {total_rootstems} (candidate-only)")
    print(f"   total JamidMushtaqCandidate        : {total_jamid} (candidate-only)")
    print(f"   total MufradWordCandidate          : {total_mufrad} (candidate-only)")
    print(f"   total VerbalSignifiedCandidate     : {total_verbal} (candidate-only)")
    print(f"   total CompositionReadinessCandidate: {total_compready} (candidate-only)")
    print(f"   tokens with no SlotCandidate       : {residual_tokens or 'none'}")
    print(f"   P8+/semantic candidates seen       : {sorted(all_higher) if all_higher else 'none'}")
    print(f"   higher semantic statuses           : not_introduced "
          f"(constant: {NOT_INTRODUCED})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
