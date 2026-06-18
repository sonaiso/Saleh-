"""
VerbalSignifiedLayerAdapter — SCG-P6 adapter.

Opens verbal-signified semantic POSSIBILITIES from a ``MufradWordCandidate``,
emitting a ``VerbalSignifiedCandidate`` (VERBAL_SIGNIFIED_CONSTITUTION.md).

CANDIDATE-ONLY and PRIORS-ONLY:
  - It OPENS meaning + dalalah PRIORS; it NEVER produces actual meaning
    (MeaningCandidate), dalalah (DalalahCandidate/DalalahJudgment), tafsir,
    hukm, or reality / final meaning.

Carried fields (on the output candidate's trace_ids, documented prefixes — they
are structural evidence, not identity):
  mufrad_word_candidate_ref:<id>                 the consumed P5 candidate
  structural_signified_evidence:<sigsig...>       derived purely from geometry
  opens_prior:meaning_priors / opens_prior:dalalah_priors
      semantic PRIORS opened downstream, NEVER produced here.

Identity: the output preserves the mufrad_word (and upstream) identities that the
MufradWordCandidate carries (they ride on the far node).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.verbal_signified_rules import OPENED_PRIORS, VERBAL_SIGNIFIED_RULE

# Trace prefixes for the carried structural fields (read back by tests/tools).
MUFRAD_WORD_CANDIDATE_REF_PREFIX = "mufrad_word_candidate_ref:"
SIGNIFIED_EVIDENCE_PREFIX = "structural_signified_evidence:"
OPENED_PRIOR_PREFIX = "opens_prior:"


def _structural_signified_signature(mufrad_word: Candidate) -> str:
    """Canonical STRUCTURAL signified-possibility signature, derived purely from
    the geometry (codepoint geometry). No lexicon, no meaning, no dalalah."""
    cps = sorted(
        iid[len("identity:codepoint:"):]
        for iid in mufrad_word.identity_ids
        if iid.startswith("identity:codepoint:")
    )
    return "sigsig:" + ("+".join(cps) if cps else "none")


@dataclass
class VerbalSignifiedLayerAdapter:
    """Adapter that opens verbal-signified semantic possibilities (priors only)."""

    kernel: QiyasKernel

    def build_request(
        self,
        mufrad_word: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest opening verbal-signified semantic possibilities
        from a MufradWordCandidate (candidate-only; priors only)."""
        signature = _structural_signified_signature(mufrad_word)

        if not trace_prefix:
            trace_prefix = f"verbal_signified:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:verbal_signified_domain",
            node_type="VerbalSignifiedDomain",
            identity_ids=("identity:verbal_signified_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The MufradWordCandidate rides on the far node — it preserves the
        # mufrad_word (and upstream) identities carried up from P5.
        far = QiyasNodeRef(
            node_id=f"فرع:mufrad_word_candidate:{mufrad_word.candidate_id}",
            node_type="MufradWordCandidate",
            identity_ids=mufrad_word.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=mufrad_word.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_mufrad_word_candidate:evidenced",
            "وصف:structural_signified_possibility_derived:evidenced",
            "وصف:opens_meaning_priors:evidenced",
            "وصف:opens_dalalah_priors:evidenced",
            "وصف:mufrad_word_identity_preserved:evidenced",
            "علة:belongs_to_verbal_signified_domain:verified",
            "علة:verbal_signified_opening_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        carried_trace = [
            f"{MUFRAD_WORD_CANDIDATE_REF_PREFIX}{mufrad_word.candidate_id}",
            f"{SIGNIFIED_EVIDENCE_PREFIX}{signature}",
        ]
        carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:verbal_signified:{uuid.uuid4().hex[:8]}",
                    source_layer="VerbalSignifiedQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=VERBAL_SIGNIFIED_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="VerbalSignifiedQiyas"),
        )

    def open(
        self,
        mufrad_word: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Open verbal-signified semantic possibilities from a MufradWordCandidate."""
        return self.kernel.apply(self.build_request(mufrad_word, trace_prefix))
