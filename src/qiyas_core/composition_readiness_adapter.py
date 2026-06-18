"""
CompositionReadinessLayerAdapter — SCG-P7 adapter.

Attests structural READINESS to enter composition from a
``VerbalSignifiedCandidate``, emitting a ``CompositionReadinessCandidate``
(COMPOSITION_READINESS_CONSTITUTION.md).

CANDIDATE-ONLY and READINESS-ONLY:
  - It attests readiness; it performs NO actual composition, NO syntax,
    NO amil/mamul relation, NO i'rab, NO meaning / dalalah / hukm.

Carried fields (on the output candidate's trace_ids, documented prefixes — they
are structural evidence, not identity):
  verbal_signified_candidate_ref:<id>             the consumed P6 candidate
  structural_composability_profile:<compsig...>    derived purely from geometry
  composition_readiness_evidence:structural         structural readiness marker
  slot_sequence_refs:<codepoints>                   structural slot-sequence refs
  opens_prior:amil_mamul_relation_priors / opens_prior:sentence_geometry_priors
      priors opened for SCG-P8/P9, NEVER produced here.

Identity: the output preserves the verbal-signified (and upstream) identities the
VerbalSignifiedCandidate carries (they ride on the far node).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.composition_readiness_rules import COMPOSITION_READINESS_RULE, OPENED_PRIORS

# Trace prefixes for the carried structural fields (read back by tests/tools).
VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX = "verbal_signified_candidate_ref:"
COMPOSABILITY_PROFILE_PREFIX = "structural_composability_profile:"
READINESS_EVIDENCE_PREFIX = "composition_readiness_evidence:"
SLOT_SEQUENCE_REFS_PREFIX = "slot_sequence_refs:"
OPENED_PRIOR_PREFIX = "opens_prior:"


def _codepoints(candidate: Candidate) -> list[str]:
    return sorted(
        iid[len("identity:codepoint:"):]
        for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )


def _structural_composability_profile(verbal_signified: Candidate) -> str:
    """Canonical STRUCTURAL composability profile, derived purely from the
    geometry (codepoint geometry). No syntax, no grammar, no meaning."""
    cps = _codepoints(verbal_signified)
    return "compsig:" + ("+".join(cps) if cps else "none")


@dataclass
class CompositionReadinessLayerAdapter:
    """Adapter that attests structural readiness to enter composition."""

    kernel: QiyasKernel

    def build_request(
        self,
        verbal_signified: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest attesting composition readiness from a
        VerbalSignifiedCandidate (candidate-only)."""
        signature = _structural_composability_profile(verbal_signified)
        slot_seq = "+".join(_codepoints(verbal_signified)) or "none"

        if not trace_prefix:
            trace_prefix = f"composition_readiness:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:composition_readiness_domain",
            node_type="CompositionReadinessDomain",
            identity_ids=("identity:composition_readiness_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The VerbalSignifiedCandidate rides on the far node — it preserves the
        # verbal-signified (and upstream) identities carried up from P6.
        far = QiyasNodeRef(
            node_id=f"فرع:verbal_signified_candidate:{verbal_signified.candidate_id}",
            node_type="VerbalSignifiedCandidate",
            identity_ids=verbal_signified.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=verbal_signified.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_verbal_signified_candidate:evidenced",
            "وصف:structural_composability_profile_derived:evidenced",
            "وصف:has_composition_readiness_evidence:evidenced",
            "وصف:has_slot_sequence_refs:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_composition_readiness_domain:verified",
            "علة:composition_readiness_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        carried_trace = [
            f"{VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX}{verbal_signified.candidate_id}",
            f"{COMPOSABILITY_PROFILE_PREFIX}{signature}",
            f"{READINESS_EVIDENCE_PREFIX}structural",
            f"{SLOT_SEQUENCE_REFS_PREFIX}{slot_seq}",
        ]
        carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:composition_readiness:{uuid.uuid4().hex[:8]}",
                    source_layer="CompositionReadinessQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=COMPOSITION_READINESS_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="CompositionReadinessQiyas"),
        )

    def attest(
        self,
        verbal_signified: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Attest composition readiness from a VerbalSignifiedCandidate."""
        return self.kernel.apply(self.build_request(verbal_signified, trace_prefix))
