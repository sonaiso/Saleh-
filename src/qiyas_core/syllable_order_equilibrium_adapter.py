from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.syllable_order_equilibrium_rules import SYLLABLE_ORDER_EQUILIBRIUM_VALIDATION


@dataclass
class SyllableOrderEquilibriumLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        is_initial_position: bool = False,
        left_demand_accepted: bool = False,
        right_capability_accepted: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for syllable order equilibrium validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            is_initial_position: Whether this is at word/syllable start
            left_demand_accepted: Whether LeftDemandCandidate is accepted
            right_capability_accepted: Whether RightCapabilityCandidate is accepted
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for syllable order equilibrium validation
        """
        if not trace_prefix:
            trace_prefix = f"order_eq:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing LeftDemandCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:left_demand:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="LeftDemandCandidate",
            identity_ids=(f"identity:left_demand:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing RightCapabilityCandidate
        far = QiyasNodeRef(
            node_id=f"far:right_cap:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="RightCapabilityCandidate",
            identity_ids=(f"identity:right_cap:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Order equilibrium requires explicit evidence from both left and right
        # Cannot prove equilibrium automatically - must verify both demands are met
        proves = [
            "asl:established",
            "far:determined",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
        ]

        # Only prove left_demand_resolved if explicitly accepted
        if left_demand_accepted:
            proves.append("wasf:left_demand_resolved:evidenced")
        else:
            # Left demand unresolved - this is an invalidating difference
            proves.append("fariq:left_demand_unresolved:present")

        # Only prove right_capability_resolved if explicitly accepted
        if right_capability_accepted:
            proves.append("wasf:right_capability_resolved:evidenced")
        else:
            # Right capability unresolved - this is an invalidating difference
            proves.append("fariq:right_capability_unresolved:present")

        # Only prove equilibrium and order fit if BOTH are accepted
        if left_demand_accepted and right_capability_accepted:
            proves.append("wasf:syllable_order_equilibrium:evidenced")
            proves.append("illah:left_right_order_fit:verified")
        else:
            # Order imbalance - cannot prove equilibrium without both sides
            proves.append("fariq:order_imbalance:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:order_eq:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="SyllableOrderEquilibriumQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=SYLLABLE_ORDER_EQUILIBRIUM_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SyllableOrderEquilibriumQiyas"),
        )

    def process_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        is_initial_position: bool = False,
        left_demand_accepted: bool = False,
        right_capability_accepted: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process syllable order equilibrium validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            is_initial_position: Whether this is at word/syllable start
            left_demand_accepted: Whether LeftDemandCandidate is accepted
            right_capability_accepted: Whether RightCapabilityCandidate is accepted
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with SyllableOrderEquilibriumCandidate result
        """
        request = self.build_request_for_validation(
            carrier_codepoint, mark_codepoint, is_initial_position,
            left_demand_accepted, right_capability_accepted, trace_prefix
        )
        return self.kernel.apply(request)
