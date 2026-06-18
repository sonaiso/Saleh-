"""
RegistryProjectionLayerAdapter — SCG-P2 adapter.

Projects a licensed ``SlotCandidate`` onto registry membership classes, emitting
a ``RegistryProjectionCandidate`` (REGISTRY_PROJECTION_CONSTITUTION.md §§9–12).

It answers ONLY: "to which registered STRUCTURAL membership class(es) could this
slot geometry belong?" — never root / wazn / word / meaning / i'rab / hukm.

Carried fields (exposed on the output candidate's trace_ids with documented
prefixes, since they are evidence, not identity):
  registry_entry_ref:<canonical structural signature>   — derived purely from the
      SlotCandidate geometry (codepoint geometry); NO coined class names.
  membership_prior_type:<GeometryMembershipClass|...>    — a STRUCTURAL registry
      category; never a linguistic category (Verb/Noun/Derived/Jamid/Root/Wazn).
  opens_prior:root_stem_candidates / opens_prior:word_type_priors — priors opened
      for SCG-P3, NEVER produced here.

Identity: the output preserves ``slot_candidate_identity`` (the SlotCandidate's
identity_ids ride on the far node); the codepoint stays structural identity.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.registry_projection_rules import (
    GEOMETRY_MEMBERSHIP_CLASS,
    OPENED_PRIORS,
    REGISTRY_PROJECTION_RULE,
)

# Trace prefixes for the carried projection fields (read back by tests/tools).
REGISTRY_ENTRY_REF_PREFIX = "registry_entry_ref:"
MEMBERSHIP_PRIOR_TYPE_PREFIX = "membership_prior_type:"
OPENED_PRIOR_PREFIX = "opens_prior:"


def _structural_signature(slot_candidate: Candidate) -> str:
    """Canonical STRUCTURAL signature derived purely from the SlotCandidate
    geometry — its codepoint identities, in canonical order. No lexicon, no
    morphology, no coined class name."""
    codepoints = sorted(
        iid[len("identity:codepoint:"):]
        for iid in slot_candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )
    return "geomsig:" + ("+".join(codepoints) if codepoints else "none")


@dataclass
class RegistryProjectionLayerAdapter:
    """Adapter that projects a SlotCandidate onto registry membership classes."""

    kernel: QiyasKernel

    def build_request(
        self,
        slot_candidate: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest projecting a SlotCandidate onto registry
        membership classes (candidate-only)."""
        signature = _structural_signature(slot_candidate)
        prior_type = GEOMETRY_MEMBERSHIP_CLASS  # structural category only

        if not trace_prefix:
            trace_prefix = f"registry_projection:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:registry_projection_domain",
            node_type="RegistryProjectionDomain",
            identity_ids=("identity:registry_projection_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The SlotCandidate rides on the far node — its identity is preserved.
        far = QiyasNodeRef(
            node_id=f"فرع:slot_candidate:{slot_candidate.candidate_id}",
            node_type="SlotCandidate",
            identity_ids=slot_candidate.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=slot_candidate.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_slot_candidate:evidenced",
            "وصف:structural_signature_derived:evidenced",
            "وصف:has_registry_entry_ref:evidenced",
            "وصف:has_membership_prior_type:evidenced",
            "وصف:slot_candidate_identity_preserved:evidenced",
            "علة:belongs_to_registry_projection_domain:verified",
            "علة:registry_projection_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Carried projection fields + opened priors (evidence, not identity).
        carried_trace = [
            f"{REGISTRY_ENTRY_REF_PREFIX}{signature}",
            f"{MEMBERSHIP_PRIOR_TYPE_PREFIX}{prior_type}",
        ]
        carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:registry_projection:{uuid.uuid4().hex[:8]}",
                    source_layer="RegistryProjectionQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=REGISTRY_PROJECTION_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="RegistryProjectionQiyas"),
        )

    def project(
        self,
        slot_candidate: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Project a SlotCandidate onto registry membership classes."""
        return self.kernel.apply(self.build_request(slot_candidate, trace_prefix))
