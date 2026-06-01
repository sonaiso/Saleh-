"""
SlotLayerAdapter — Gap #6 adapter.

Composes LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier
into a SlotCandidate via QiyasKernel.apply().

This is the first algebraic composition in the chain.

Constitutional law:
  SlotCandidate ⊬ SyllableCandidate  (adjacency not yet established)
  SlotCandidate ⊬ MeaningCandidate
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.slot_rules import SLOT_COMPOSITION_RULE


def _extract_letter_name(letter_carrier: Candidate) -> str:
    """Extract arabic_name from identity_ids (identity:letter:{name})."""
    for iid in letter_carrier.identity_ids:
        if iid.startswith("identity:letter:"):
            return iid[len("identity:letter:"):]
    # Fall back to candidate_id
    return letter_carrier.candidate_id


def _extract_haraka_name(haraka_carrier: Candidate) -> str:
    """Extract arabic_name from identity_ids (identity:haraka:{name})."""
    for iid in haraka_carrier.identity_ids:
        if iid.startswith("identity:haraka:"):
            return iid[len("identity:haraka:"):]
    return haraka_carrier.candidate_id


@dataclass
class SlotLayerAdapter:
    """
    Adapter that composes three carriers into a SlotCandidate.

    Constitutional path:
        LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier
            → [SlotLayerAdapter] → SlotCandidate
    """

    kernel: QiyasKernel

    def build_request(
        self,
        letter_carrier: Candidate,
        haraka_carrier: Candidate,
        position_carrier: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest for slot composition."""
        letter_name = _extract_letter_name(letter_carrier)
        haraka_name = _extract_haraka_name(haraka_carrier)

        if not trace_prefix:
            trace_prefix = f"slot:{letter_name}:{haraka_name}"

        # The far node is the LetterIdentityCarrier (primary input)
        # All three carriers' identity_ids are combined in the nodes
        combined_identity = (
            letter_carrier.identity_ids
            + haraka_carrier.identity_ids
            + position_carrier.identity_ids
        )
        # Deduplicate while preserving order
        seen: set[str] = set()
        deduped_identity: list[str] = []
        for iid in combined_identity:
            if iid not in seen:
                seen.add(iid)
                deduped_identity.append(iid)

        asl = QiyasNodeRef(
            node_id="asl:slot_composition_domain",
            node_type="SlotCompositionDomain",
            identity_ids=("identity:slot_composition_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        far = QiyasNodeRef(
            node_id=f"far:letter_identity_carrier:{letter_name}",
            node_type="LetterIdentityCarrier",
            identity_ids=tuple(deduped_identity),
            trace_ids=(f"{trace_prefix}:far",),
            rank=min(
                (letter_carrier.rank, haraka_carrier.rank, position_carrier.rank),
                key=lambda r: r.value,
            ),
        )

        proves = [
            "asl:established",
            "far:determined",
            "wasf:has_letter_identity_carrier:evidenced",
            "wasf:has_haraka_function_carrier:evidenced",
            "wasf:has_position_carrier:evidenced",
            "wasf:compatible_letter_haraka:evidenced",
            "wasf:compatible_letter_position:evidenced",
            "wasf:identity_preserved:evidenced",
            "illah:belongs_to_slot_composition_domain:verified",
            "illah:slot_composition_licensed:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
        ]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:slot:{letter_name}:{haraka_name}:{uuid.uuid4().hex[:8]}",
                    source_layer="SlotQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=SLOT_COMPOSITION_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SlotQiyas"),
        )

    def compose_slot(
        self,
        letter_carrier: Candidate,
        haraka_carrier: Candidate,
        position_carrier: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Compose a SlotCandidate from the three carrier inputs."""
        request = self.build_request(
            letter_carrier, haraka_carrier, position_carrier, trace_prefix
        )
        return self.kernel.apply(request)
