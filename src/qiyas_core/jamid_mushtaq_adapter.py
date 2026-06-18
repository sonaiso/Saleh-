"""
JamidMushtaqLayerAdapter — SCG-P4 adapter.

Opens a structural derivation-class POSSIBILITY from a ``RootStemCandidate``,
emitting a ``JamidMushtaqCandidate`` (JAMID_MUSHTAQ_CONSTITUTION.md).

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT a final jamid/mushtaq judgment (WordTypeJudgment forbidden), NOT wazn
    (WeightCandidate forbidden), NOT morphology, NOT wordhood, NOT lexical
    meaning / dalalah / i'rab / hukm.

Carried fields (on the output candidate's trace_ids, documented prefixes — they
are structural evidence, not identity):
  root_stem_candidate_ref:<id>                     the consumed P3 candidate
  structural_derivation_possibility:<derivsig...>   derived purely from geometry
  jamid_mushtaq_prior_type:<DerivationGeometryClass> STRUCTURAL category, never
      a linguistic جامد/مشتق label.
  pattern_evidence:structural                       structural pattern marker (no morphology)
  opens_prior:word_type_candidates                  prior opened for SCG-P5, NEVER produced.

Identity: the output preserves the root_stem (and thus slot) identities that the
RootStemCandidate carries (they ride on the far node).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.jamid_mushtaq_rules import (
    DERIVATION_GEOMETRY_CLASS,
    JAMID_MUSHTAQ_RULE,
    OPENED_PRIORS,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
ROOT_STEM_CANDIDATE_REF_PREFIX = "root_stem_candidate_ref:"
DERIVATION_POSSIBILITY_PREFIX = "structural_derivation_possibility:"
JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX = "jamid_mushtaq_prior_type:"
PATTERN_EVIDENCE_PREFIX = "pattern_evidence:"
OPENED_PRIOR_PREFIX = "opens_prior:"


def _structural_derivation_signature(root_stem: Candidate) -> str:
    """Canonical STRUCTURAL derivation-possibility signature, derived purely from
    the root/stem geometry (codepoint geometry). No lexicon, no morphology, no
    wazn, no جامد/مشتق judgment."""
    cps = sorted(
        iid[len("identity:codepoint:"):]
        for iid in root_stem.identity_ids
        if iid.startswith("identity:codepoint:")
    )
    return "derivsig:" + ("+".join(cps) if cps else "none")


@dataclass
class JamidMushtaqLayerAdapter:
    """Adapter that opens a structural derivation-class possibility from a root/stem."""

    kernel: QiyasKernel

    def build_request(
        self,
        root_stem: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest opening a structural derivation-class possibility
        from a RootStemCandidate (candidate-only)."""
        signature = _structural_derivation_signature(root_stem)
        prior_type = DERIVATION_GEOMETRY_CLASS  # structural category only

        if not trace_prefix:
            trace_prefix = f"jamid_mushtaq:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:jamid_mushtaq_domain",
            node_type="JamidMushtaqDomain",
            identity_ids=("identity:jamid_mushtaq_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The RootStemCandidate rides on the far node — it preserves the root/stem
        # (and slot) identities carried up from P3/P2/P1.
        far = QiyasNodeRef(
            node_id=f"فرع:root_stem_candidate:{root_stem.candidate_id}",
            node_type="RootStemCandidate",
            identity_ids=root_stem.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=root_stem.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_root_stem_candidate:evidenced",
            "وصف:structural_derivation_possibility_derived:evidenced",
            "وصف:has_jamid_mushtaq_prior_type:evidenced",
            "وصف:has_pattern_evidence:evidenced",
            "وصف:root_stem_candidate_identity_preserved:evidenced",
            "علة:belongs_to_jamid_mushtaq_domain:verified",
            "علة:jamid_mushtaq_classification_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        carried_trace = [
            f"{ROOT_STEM_CANDIDATE_REF_PREFIX}{root_stem.candidate_id}",
            f"{DERIVATION_POSSIBILITY_PREFIX}{signature}",
            f"{JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX}{prior_type}",
            f"{PATTERN_EVIDENCE_PREFIX}structural",
        ]
        carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:jamid_mushtaq:{uuid.uuid4().hex[:8]}",
                    source_layer="JamidMushtaqQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=JAMID_MUSHTAQ_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="JamidMushtaqQiyas"),
        )

    def classify(
        self,
        root_stem: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Open a structural derivation-class possibility from a RootStemCandidate."""
        return self.kernel.apply(self.build_request(root_stem, trace_prefix))
