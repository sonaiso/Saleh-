"""
RootStemLayerAdapter — SCG-P3 adapter.

Closes a structural root/stem POSSIBILITY from a ``RegistryProjectionCandidate``,
emitting a ``RootStemCandidate`` (ROOT_STEM_CLOSURE_CONSTITUTION.md).

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT final root extraction / RootCandidate, NOT wazn / WeightCandidate,
    NOT morphology, NOT wordhood, NOT lexical meaning / dalalah / i'rab / hukm.

Carried fields (on the output candidate's trace_ids, with documented prefixes —
they are structural evidence, not identity):
  registry_projection_ref:<id>                 the consumed P2 candidate
  structural_root_stem_signature:<geomsig...>   derived purely from geometry
  slot_sequence_refs:<codepoints>               structural slot-sequence refs
  root_pattern_evidence:structural              structural pattern marker (no morphology)
  stem_boundary_evidence:structural             structural boundary marker
  opens_prior:jamid_mushtaq_candidates / opens_prior:word_pattern_candidates
      priors opened for SCG-P4, NEVER produced here.

Identity: the output preserves the slot_candidate identities that the
RegistryProjectionCandidate carries (they ride on the far node).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.root_stem_rules import OPENED_PRIORS, ROOT_STEM_RULE

# Trace prefixes for the carried structural fields (read back by tests/tools).
REGISTRY_PROJECTION_REF_PREFIX = "registry_projection_ref:"
ROOT_STEM_SIGNATURE_PREFIX = "structural_root_stem_signature:"
SLOT_SEQUENCE_REFS_PREFIX = "slot_sequence_refs:"
ROOT_PATTERN_EVIDENCE_PREFIX = "root_pattern_evidence:"
STEM_BOUNDARY_EVIDENCE_PREFIX = "stem_boundary_evidence:"
OPENED_PRIOR_PREFIX = "opens_prior:"


def _codepoints(candidate: Candidate) -> list[str]:
    return sorted(
        iid[len("identity:codepoint:"):]
        for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )


def _structural_root_stem_signature(projection: Candidate) -> str:
    """Canonical STRUCTURAL signature for the root/stem possibility, derived
    purely from the projection geometry (codepoint geometry). No lexicon, no
    morphology, no wazn, no coined root."""
    cps = _codepoints(projection)
    return "rootstemsig:" + ("+".join(cps) if cps else "none")


@dataclass
class RootStemLayerAdapter:
    """Adapter that closes a structural root/stem possibility from a projection."""

    kernel: QiyasKernel

    def build_request(
        self,
        projection: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest closing a structural root/stem possibility from a
        RegistryProjectionCandidate (candidate-only)."""
        signature = _structural_root_stem_signature(projection)
        slot_seq = "+".join(_codepoints(projection)) or "none"

        if not trace_prefix:
            trace_prefix = f"root_stem:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:root_stem_closure_domain",
            node_type="RootStemClosureDomain",
            identity_ids=("identity:root_stem_closure_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The RegistryProjectionCandidate rides on the far node — it preserves the
        # slot_candidate identities carried up from P2/P1.
        far = QiyasNodeRef(
            node_id=f"فرع:registry_projection_candidate:{projection.candidate_id}",
            node_type="RegistryProjectionCandidate",
            identity_ids=projection.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=projection.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_registry_projection:evidenced",
            "وصف:structural_root_stem_signature_derived:evidenced",
            "وصف:has_slot_sequence_refs:evidenced",
            "وصف:has_root_pattern_evidence:evidenced",
            "وصف:has_stem_boundary_evidence:evidenced",
            "وصف:slot_candidate_identities_preserved:evidenced",
            "علة:belongs_to_root_stem_closure_domain:verified",
            "علة:root_stem_closure_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Carried STRUCTURAL evidence + opened priors (evidence, not identity).
        carried_trace = [
            f"{REGISTRY_PROJECTION_REF_PREFIX}{projection.candidate_id}",
            f"{ROOT_STEM_SIGNATURE_PREFIX}{signature}",
            f"{SLOT_SEQUENCE_REFS_PREFIX}{slot_seq}",
            f"{ROOT_PATTERN_EVIDENCE_PREFIX}structural",
            f"{STEM_BOUNDARY_EVIDENCE_PREFIX}structural",
        ]
        carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:root_stem:{uuid.uuid4().hex[:8]}",
                    source_layer="RootStemQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=ROOT_STEM_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="RootStemQiyas"),
        )

    def close(
        self,
        projection: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Close a structural root/stem possibility from a RegistryProjectionCandidate."""
        return self.kernel.apply(self.build_request(projection, trace_prefix))
