"""
MufradWordLayerAdapter — SCG-P5 adapter.

Forms a candidate-only single-word POSSIBILITY from a ``JamidMushtaqCandidate``,
emitting a ``MufradWordCandidate`` (MUFRAD_WORD_CONSTITUTION.md).

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT a final lexical word (WordCandidate forbidden), NOT a dictionary entry,
    NOT morphology, NOT grammar, NOT lexical meaning / dalalah / i'rab / hukm.

Carried fields (on the output candidate's trace_ids, documented prefixes — they
are structural evidence, not identity):
  jamid_mushtaq_candidate_ref:<id>                 the consumed P4 candidate
  structural_wordhood_evidence:<wordsig...>         derived purely from geometry
  structural_word_boundary_evidence:structural      structural boundary marker
  slot_sequence_refs:<codepoints>                   structural slot-sequence refs
  opens_prior:verbal_signified_candidates / opens_prior:phrase_level_priors
      priors opened for SCG-P6, NEVER produced here.

Identity: the output preserves the upstream identities the JamidMushtaqCandidate
carries (root/stem/slot identities ride on the far node).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.mufrad_word_rules import MUFRAD_WORD_RULE, OPENED_PRIORS

# Trace prefixes for the carried structural fields (read back by tests/tools).
JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX = "jamid_mushtaq_candidate_ref:"
WORDHOOD_EVIDENCE_PREFIX = "structural_wordhood_evidence:"
WORD_BOUNDARY_EVIDENCE_PREFIX = "structural_word_boundary_evidence:"
SLOT_SEQUENCE_REFS_PREFIX = "slot_sequence_refs:"
OPENED_PRIOR_PREFIX = "opens_prior:"


def _codepoints(candidate: Candidate) -> list[str]:
    return sorted(
        iid[len("identity:codepoint:"):]
        for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )


def _structural_wordhood_signature(jamid_mushtaq: Candidate) -> str:
    """Canonical STRUCTURAL wordhood signature, derived purely from the geometry
    (codepoint geometry). No lexicon, no morphology, no dictionary, no meaning."""
    cps = _codepoints(jamid_mushtaq)
    return "wordsig:" + ("+".join(cps) if cps else "none")


@dataclass
class MufradWordLayerAdapter:
    """Adapter that forms a candidate-only single-word possibility."""

    kernel: QiyasKernel

    def build_request(
        self,
        jamid_mushtaq: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest forming a single-word possibility from a
        JamidMushtaqCandidate (candidate-only)."""
        signature = _structural_wordhood_signature(jamid_mushtaq)
        slot_seq = "+".join(_codepoints(jamid_mushtaq)) or "none"

        if not trace_prefix:
            trace_prefix = f"mufrad_word:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:mufrad_word_domain",
            node_type="MufradWordDomain",
            identity_ids=("identity:mufrad_word_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The JamidMushtaqCandidate rides on the far node — it preserves the
        # upstream (root/stem/slot) identities carried up from P4.
        far = QiyasNodeRef(
            node_id=f"فرع:jamid_mushtaq_candidate:{jamid_mushtaq.candidate_id}",
            node_type="JamidMushtaqCandidate",
            identity_ids=jamid_mushtaq.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=jamid_mushtaq.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_jamid_mushtaq_candidate:evidenced",
            "وصف:structural_wordhood_evidence_derived:evidenced",
            "وصف:has_structural_word_boundary_evidence:evidenced",
            "وصف:has_slot_sequence_refs:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_mufrad_word_domain:verified",
            "علة:mufrad_word_formation_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        carried_trace = [
            f"{JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX}{jamid_mushtaq.candidate_id}",
            f"{WORDHOOD_EVIDENCE_PREFIX}{signature}",
            f"{WORD_BOUNDARY_EVIDENCE_PREFIX}structural",
            f"{SLOT_SEQUENCE_REFS_PREFIX}{slot_seq}",
        ]
        carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:mufrad_word:{uuid.uuid4().hex[:8]}",
                    source_layer="MufradWordQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=MUFRAD_WORD_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="MufradWordQiyas"),
        )

    def form(
        self,
        jamid_mushtaq: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Form a single-word possibility from a JamidMushtaqCandidate."""
        return self.kernel.apply(self.build_request(jamid_mushtaq, trace_prefix))
