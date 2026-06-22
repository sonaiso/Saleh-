"""Legacy → P3.1 proposal feed (TEST-SIDE bridge; audit-governed).

Converts the committed Stage A legacy fixtures into PROPOSAL EVIDENCE for the EXISTING
P3.1 WeightPattern adapter. It feeds ONLY root / wazn / weight-alignment / weak-shadda-
hamza-madd ambiguity evidence — never mabni/mu'rab/word-kind class, grammatical role,
case/i'rab, relations, events, meaning, or reasoning (those are ignored raw context).

CONSTITUTIONAL CONTRACT (identical discipline to the P5.1 feed, PR #187):
  - TEST-SIDE only. NOT under src/qiyas_core, NOT wired into live run_qiyas. Stage A
    stays capture-only; the runtime never calls the analyzer and never reads fixtures
    (Stage A guard test_LFH_10 stays green).
  - Reads ONLY committed Stage A fixtures (fixture-only). No subprocess / analyzer call.
  - The legacy analyzer PROPOSES; only the P3.1 Qiyas rules ACCEPT / DEFER / BLOCK.
    Reliability tag is an INPUT HINT, never a verdict:
      root_wazn proposal_evidence → ACCEPT-eligible *iff* P3.1's own identity/alignment
                                    checks pass;
      root_wazn suspicious_defer (weak/hollow/hamza/shadda/madd/unvocalized) → DEFER —
                                    a suspicious entry is never promoted to ACCEPT;
      role/case unsafe_final_looking → ignored raw field only.
  - P3.1 aligns the SURFACE itself and never rewrites it. The legacy root is recorded
    only as audit metadata — never used to alter alignment or assert a final root/wazn.
    Hollow/weak/hamza/madd surfaces are therefore DEFERRED by P3.1's own discrimination,
    not blocked on a transformed underlying root letter.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.weight_pattern_adapter import WeightPatternLayerAdapter
from qiyas_core.rules.weight_pattern_rules import analyze_surface

import legacy_harness as H

PROPOSAL_SOURCE = "legacy_stage_a_fixture"

# Mapped candidate hints (input hints to P3.1 — NOT verdicts).
WEIGHT_PATTERN_HINT = "weight_pattern_hint"
ROOT_SLOT_ALIGNMENT_HINT = "root_slot_alignment_hint"
WEAK_LETTER_DEFER_HINT = "weak_letter_defer_hint"
SHADDA_DEFER_HINT = "shadda_defer_hint"
HAMZA_DEFER_HINT = "hamza_defer_hint"
MADD_DEFER_HINT = "madd_defer_hint"
INVALID_OR_IGNORE_HINT = "invalid_or_ignore_hint"

# Families NEVER consumed by THIS feed (held back / belong to the P5.1 feed).
_ALWAYS_IGNORED = (
    "legacy_class", "mabni_murab", "word_kind", "grammatical_role", "case/i'rab",
    "relations", "events", "speech_act", "resolution/anaphora", "meaning_graph",
    "reasoning/qa",
)


@dataclass(frozen=True)
class LegacyWeightPatternProposal:
    proposal_source: str
    raw_token: str
    raw_root: str | None
    raw_wazn: str | None
    raw_class_label: str | None     # present but ignored
    raw_role_label: str | None      # present but ignored
    reliability_tag: str            # the root_wazn reliability (gates P3.1 trust)
    certainty_class: str | None     # not present in the morph capture
    mapped_evidence_kind: str
    mapped_candidate_hint: str
    unsafe_final_label: bool
    consumed_fields: tuple = field(default_factory=tuple)
    ignored_fields: tuple = field(default_factory=tuple)
    p3_1_evidence: dict = field(default_factory=dict)


def _suspicious_defer_hint(surface: str) -> str:
    _base, sh, hz, md, wk = analyze_surface(surface)
    if sh:
        return SHADDA_DEFER_HINT
    if hz:
        return HAMZA_DEFER_HINT
    if md:
        return MADD_DEFER_HINT
    if wk:
        return WEAK_LETTER_DEFER_HINT
    return INVALID_OR_IGNORE_HINT


def map_legacy_root_wazn_to_weight_pattern_evidence(row):
    """Map a Stage A capability row to (p3_1_evidence, hint, kind, consumed)."""
    surface = row.token
    rw = row.family_reliability.get(H.FAMILY_ROOT_WAZN)
    consumed = ["legacy_root", "legacy_wazn", "surface"]
    root = row.legacy_root if row.legacy_root not in (None, "—") else None
    # P3.1 aligns the SURFACE itself and never rewrites it. The legacy root is recorded
    # as audit/cross-check metadata only — it is NOT used as a hard identity check,
    # because a hollow/weak/hamza root letter is legitimately transformed on the surface
    # (e.g. قَالَ ← root قول) and must NOT be treated as an identity violation. Suspicious
    # cases instead DEFER through P3.1's own weak/shadda/hamza/madd discrimination.
    evidence = {
        "surface": surface,
        "legacy_root_for_audit": root,  # recorded; never fed to alter alignment/identity
    }
    if rw == H.SUSPICIOUS_DEFER:
        return evidence, _suspicious_defer_hint(surface), "suspicious_root_wazn", consumed
    # proposal_evidence: sound surface — P3.1 will ACCEPT/DEFER on its own. Added-letter
    # forms (surface longer than a bare triliteral) carry alignment evidence.
    base, *_ = analyze_surface(surface)
    if len(base) > 3:
        return evidence, ROOT_SLOT_ALIGNMENT_HINT, "root_slot_and_added_letter_alignment", consumed
    return evidence, WEIGHT_PATTERN_HINT, "root_slot_alignment", consumed


class LegacyWeightPatternProposalProvider:
    """Reads ONLY committed Stage A fixtures (fixture-only). Never calls the analyzer."""

    def proposals(self) -> list[LegacyWeightPatternProposal]:
        out = []
        for row in H.capability_rows():
            evidence, hint, kind, consumed = map_legacy_root_wazn_to_weight_pattern_evidence(row)
            rel = row.family_reliability
            ignored = list(_ALWAYS_IGNORED)
            out.append(LegacyWeightPatternProposal(
                proposal_source=PROPOSAL_SOURCE,
                raw_token=row.token,
                raw_root=row.legacy_root,
                raw_wazn=row.legacy_wazn,
                raw_class_label=row.legacy_class,
                raw_role_label=row.legacy_role,
                reliability_tag=rel.get(H.FAMILY_ROOT_WAZN),
                certainty_class=None,
                mapped_evidence_kind=kind,
                mapped_candidate_hint=hint,
                unsafe_final_label=rel.get(H.FAMILY_ROLE_CASE) == H.UNSAFE_FINAL_LOOKING,
                consumed_fields=tuple(consumed),
                ignored_fields=tuple(ignored),
                p3_1_evidence=evidence,
            ))
        return out

    def get(self, token: str) -> LegacyWeightPatternProposal:
        for p in self.proposals():
            if p.raw_token == token:
                return p
        raise KeyError(token)


# ── Feeding the EXISTING P3.1 adapter (Qiyas makes the verdict) ────────────────


def _synthetic_root_stem(surface: str) -> Candidate:
    ids = tuple(f"identity:codepoint:{ord(c):04x}" for c in surface
                if 0x0621 <= ord(c) <= 0x064A) or ("identity:root_stem_domain",)
    return Candidate(
        candidate_id=f"accepted:RootStemQiyas:{surface}",
        candidate_type="RootStemCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="RootStemQiyas",
        source_rule_id="root_stem.close",
        asl_id="اصل:root_stem_domain",
        far_id="فرع:registry_projection_candidate:x",
        identity_ids=ids,
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=("root_pattern_evidence:cv=CVCVCV;slots=3",),
        output_flags=frozenset({"CandidateOnly"}),
    )


def feed_proposal_to_p3_1(proposal: LegacyWeightPatternProposal,
                          kernel: QiyasKernel | None = None):
    """Feed the SAFE evidence into the existing P3.1 adapter; apply the reliability gate.

    Returns (candidate_set, p3_1_raw_verdict, gated_verdict). The gate downgrades a P3.1
    ACCEPT to DEFER when the legacy proposal is suspicious_defer — a suspicious legacy
    entry is never promoted to ACCEPT. P3.1 still makes the structural decision."""
    adapter = WeightPatternLayerAdapter(kernel=kernel or QiyasKernel())
    cs = adapter.extract(
        _synthetic_root_stem(proposal.raw_token),
        surface=proposal.p3_1_evidence["surface"],
    )
    raw = "ACCEPT" if cs.accepted else ("DEFER" if cs.deferred else "BLOCK")
    if proposal.reliability_tag == H.SUSPICIOUS_DEFER and raw == "ACCEPT":
        gated = "DEFER"   # suspicious legacy entry must not ACCEPT
    else:
        gated = raw
    return cs, raw, gated
