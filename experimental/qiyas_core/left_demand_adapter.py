from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.left_demand_rules import LEFT_DEMAND_ANALYSIS


@dataclass
class LeftDemandLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_analysis(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        is_initial_position: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for left demand analysis.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            is_initial_position: Whether this is at word/syllable start
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for left demand analysis
        """
        if not trace_prefix:
            trace_prefix = f"left_demand:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing PhonoFunctionalUnitCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing left context
        far = QiyasNodeRef(
            node_id=f"far:left_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="LeftContext",
            identity_ids=(f"identity:left_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Analyze left demand based on position
        # At initial position, no left demand (word/syllable boundary)
        # At non-initial position, left demand exists (needs preceding syllable)
        if is_initial_position:
            proves = (
                "asl:established",
                "far:determined",
                "wasf:left_position_analyzed:evidenced",
                "wasf:left_demand_satisfied:evidenced",
                "illah:left_demand_determinable:verified",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            )
        else:
            # Non-initial position: left demand exists but deferred
            proves = (
                "asl:established",
                "far:determined",
                "wasf:left_position_analyzed:evidenced",
                "illah:left_demand_determinable:verified",
                "residual:left_demand_requires_preceding:deferred",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            )

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:left_demand:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="LeftDemandQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=LEFT_DEMAND_ANALYSIS,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="LeftDemandQiyas"),
        )

    def process_analysis(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        is_initial_position: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process left demand analysis.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            is_initial_position: Whether this is at word/syllable start
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with LeftDemandCandidate result
        """
        request = self.build_request_for_analysis(
            carrier_codepoint, mark_codepoint, is_initial_position, trace_prefix
        )
        return self.kernel.apply(request)
