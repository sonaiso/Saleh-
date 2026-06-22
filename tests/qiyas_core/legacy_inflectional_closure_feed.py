"""Legacy → P5.1 proposal feed (TEST-SIDE bridge; audit-governed).

Converts the committed Stage A legacy fixtures into PROPOSAL EVIDENCE for the EXISTING
P5.1 InflectionalClosure adapter. It feeds ONLY class / closed-category / mabni-mu'rab /
safe-verb-kind evidence — never root, wazn, root-slot/added-letter alignment, weak/
shadda/hamza/madd morphology, grammatical role, case/i'rab, relations, events, meaning,
or reasoning.

CONSTITUTIONAL CONTRACT:
  - This module is TEST-SIDE. It is NOT under src/qiyas_core and is NOT wired into the
    live run_qiyas pipeline. Stage A stays capture-only; the runtime never calls the
    external analyzer and never reads these fixtures. (The Stage A guard
    test_LFH_10 — "no src/qiyas_core or run_qiyas reference to legacy" — stays green.)
  - It reads ONLY committed Stage A fixtures (via legacy_harness, fixture-only). No
    subprocess, no analyzer call.
  - The legacy analyzer PROPOSES; only the P5.1 Qiyas rules ACCEPT / DEFER / BLOCK.
    The certainty / reliability tag is an INPUT HINT, never a verdict:
      proposal_evidence (+ no suspicious family)  → ACCEPT-eligible
      suspicious_defer (any family)               → DEFER (never ACCEPT)
      unsafe_final_looking (role/case)            → ignored raw field only
  - root / wazn CONTENT is never fed; only the reliability TAG gates trust.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from qiyas_core.candidate import Candidate, CandidateSet
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.inflectional_closure_adapter import InflectionalClosureLayerAdapter

import legacy_harness as H

PROPOSAL_SOURCE = "legacy_stage_a_fixture"

# Mapped candidate hints (input hints to P5.1 — NOT verdicts).
MABNI_HINT = "mabni_hint"
MURAB_HINT = "murab_hint"
DEFER_HINT = "defer_hint"
IGNORE_HINT = "ignore_hint"

# Closed functional/pronominal compounds the legacy reports as HARF+enclitic.
_CLOSED_COMPOUND_SURFACES = {"عليه", "منه", "بكم", "فيه", "به", "له", "منهم", "عليهم", "بهم"}
# Detached-pronoun surfaces (legacy ISM_MABNI gives no finer sub-type).
_PRONOUN_SURFACES = {"هو", "هي", "هم", "هن", "أنا", "أنت", "أنتم", "نحن", "هما", "أنتِ"}

# Fields NEVER consumed by this feed (audit families held back for later governed PRs).
_ALWAYS_IGNORED = (
    "legacy_root", "legacy_wazn", "root_slot_alignment", "added_letter_alignment",
    "weak/shadda/hamza/madd morphology", "grammatical_role", "case/i'rab",
    "relations", "events", "speech_act", "resolution/anaphora", "meaning_graph",
    "reasoning/qa",
)


@dataclass(frozen=True)
class LegacyInflectionalClosureProposal:
    proposal_source: str
    raw_token: str
    raw_class_label: str | None
    raw_role_label: str | None
    raw_root: str | None            # present but ignored
    raw_wazn: str | None            # present but ignored
    reliability_tag: str            # the gating reliability (word_class / root_wazn)
    certainty_class: str | None     # legacy Certificate/Hypothesis/Zero if captured (not in morph capture)
    mapped_evidence_kind: str
    mapped_candidate_hint: str      # mabni_hint / murab_hint / defer_hint / ignore_hint
    unsafe_final_label: bool        # the L3 role/case is a committed (unsafe) i'rab
    consumed_fields: tuple = field(default_factory=tuple)
    ignored_fields: tuple = field(default_factory=tuple)
    # P5.1 evidence kwargs derived from the SAFE families only (closed-category / verb-kind).
    p5_1_evidence: dict = field(default_factory=dict)


def map_legacy_class_to_inflectional_closure_evidence(row):
    """Map a Stage A capability row to (p5_1_evidence, hint, evidence_kind, consumed).

    Gating: a token is ACCEPT-eligible only when its word_class is proposal_evidence AND
    no family is suspicious_defer. Suspicious entries → defer (no evidence fed). The
    role/case (always unsafe_final_looking) is never fed; for verbs the *tense* (a safe
    verb-kind signal, not i'rab) is the only role-derived field consumed.
    """
    cls = row.legacy_class
    role = row.legacy_role or ""
    surface = row.token
    rel = row.family_reliability
    wc = rel.get(H.FAMILY_WORD_CLASS)
    rw = rel.get(H.FAMILY_ROOT_WAZN)
    consumed: list[str] = []

    # Trust gate — suspicious class OR suspicious root/wazn tag → DEFER (never ACCEPT).
    # (root/wazn CONTENT is never used; only the audit tag gates trust.)
    if wc == H.SUSPICIOUS_DEFER or rw == H.SUSPICIOUS_DEFER:
        return {}, DEFER_HINT, "suspicious_class_or_morph_tag", consumed

    consumed.append("legacy_class")
    if cls == "HARF":
        if surface in _CLOSED_COMPOUND_SURFACES:
            return {"is_closed_compound": True}, MABNI_HINT, "closed_functional_compound", consumed
        return {"closed_category": "harf"}, MABNI_HINT, "closed_functional_particle", consumed
    if cls == "ISM_MAWSOOL":
        return {"closed_category": "relative"}, MABNI_HINT, "relative_noun", consumed
    if cls == "ISM_MABNI":
        if surface in _PRONOUN_SURFACES:
            return {"closed_category": "pronoun"}, MABNI_HINT, "pronoun", consumed
        return {"closed_category": "demonstrative"}, MABNI_HINT, "demonstrative_or_mabni_noun", consumed
    if cls == "FIIL":
        consumed.append("legacy_role:verb_tense")  # verb-kind, NOT i'rab case
        if "ماض" in role:
            return {"word_kind": "verbal", "verb_tense": "past"}, MABNI_HINT, "past_verb", consumed
        if "أمر" in role:
            return {"word_kind": "verbal", "verb_tense": "imperative"}, MABNI_HINT, "imperative_verb", consumed
        if "مضارع" in role:
            return {"word_kind": "verbal", "verb_tense": "present"}, MURAB_HINT, "present_verb_open", consumed
        return {}, DEFER_HINT, "verb_tense_underspecified", consumed
    if cls in ("ISM_MUARAB", "JAMID"):
        # inflectional-closure evidence (open declinable nominal); NOT a derivation label.
        return {"word_kind": "nominal"}, MURAB_HINT, "open_declinable_nominal", consumed
    # AALAM / JALALAH / SINGULAR_TERM / UNKNOWN — outside the safe mabni/mu'rab feed.
    return {}, IGNORE_HINT, "outside_inflectional_closure_scope", consumed


class LegacyInflectionalClosureProposalProvider:
    """Reads ONLY committed Stage A fixtures (fixture-only) and produces P5.1 proposals.
    Never calls the external analyzer / subprocess."""

    def proposals(self) -> list[LegacyInflectionalClosureProposal]:
        out = []
        for row in H.capability_rows():  # fixture-only source
            evidence, hint, kind, consumed = map_legacy_class_to_inflectional_closure_evidence(row)
            rel = row.family_reliability
            unsafe = rel.get(H.FAMILY_ROLE_CASE) == H.UNSAFE_FINAL_LOOKING
            ignored = list(_ALWAYS_IGNORED)
            if "legacy_role:verb_tense" not in consumed and row.legacy_role:
                ignored.append("legacy_role:i'rab_case")  # noun role = i'rab → ignored
            gating = (H.SUSPICIOUS_DEFER if (rel.get(H.FAMILY_WORD_CLASS) == H.SUSPICIOUS_DEFER
                      or rel.get(H.FAMILY_ROOT_WAZN) == H.SUSPICIOUS_DEFER)
                      else rel.get(H.FAMILY_WORD_CLASS))
            out.append(LegacyInflectionalClosureProposal(
                proposal_source=PROPOSAL_SOURCE,
                raw_token=row.token,
                raw_class_label=row.legacy_class,
                raw_role_label=row.legacy_role,
                raw_root=row.legacy_root,
                raw_wazn=row.legacy_wazn,
                reliability_tag=gating,
                certainty_class=None,  # not present in the morph+i3rab capture
                mapped_evidence_kind=kind,
                mapped_candidate_hint=hint,
                unsafe_final_label=unsafe,
                consumed_fields=tuple(consumed),
                ignored_fields=tuple(ignored),
                p5_1_evidence=evidence,
            ))
        return out

    def get(self, token: str) -> LegacyInflectionalClosureProposal:
        for p in self.proposals():
            if p.raw_token == token:
                return p
        raise KeyError(token)


# ── Feeding the EXISTING P5.1 adapter (Qiyas makes the verdict) ────────────────


def _synthetic_mufrad(surface: str) -> Candidate:
    """A minimal accepted P5 MufradWordCandidate carrier for the proposal's token."""
    return Candidate(
        candidate_id=f"accepted:MufradWordQiyas:{surface}",
        candidate_type="MufradWordCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="MufradWordQiyas",
        source_rule_id="mufrad_word.form",
        asl_id="اصل:mufrad_word_domain",
        far_id="فرع:jamid_mushtaq_candidate:x",
        identity_ids=(f"identity:codepoint:{ord(surface[0]):04x}", "identity:mufrad_word_domain"),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(),
        output_flags=frozenset({"CandidateOnly"}),
    )


def feed_proposal_to_p5_1(proposal: LegacyInflectionalClosureProposal,
                          kernel: QiyasKernel | None = None) -> CandidateSet:
    """Feed ONLY the safe mapped evidence into the existing P5.1 adapter. P5.1 decides.

    Crucially, root/wazn/role/case/relations/events/meaning are NEVER passed — only the
    closed-category / verb-kind evidence in `proposal.p5_1_evidence`."""
    adapter = InflectionalClosureLayerAdapter(kernel=kernel or QiyasKernel())
    return adapter.classify(
        _synthetic_mufrad(proposal.raw_token),
        token_surface=proposal.raw_token,
        **proposal.p5_1_evidence,
    )
