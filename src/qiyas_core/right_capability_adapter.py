from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank, MarkFunction
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .mark_function_adapter import classify_mark_function
from .node import QiyasNodeRef
from .rules.right_capability_rules import RIGHT_CAPABILITY_ANALYSIS


@dataclass
class RightCapabilityLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_analysis(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for right capability analysis.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for right capability analysis
        """
        if not trace_prefix:
            trace_prefix = f"right_cap:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing PhonoFunctionalUnitCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing right context
        far = QiyasNodeRef(
            node_id=f"far:right_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="RightContext",
            identity_ids=(f"identity:right_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Analyze right capability based on mark function
        mark_fn = classify_mark_function(mark_codepoint)

        # Sukun allows continuation (can be followed by another syllable)
        # Short vowels and tanwin allow continuation or closure
        if mark_fn == MarkFunction.SUKUN_MARK:
            proves = (
                "asl:established",
                "far:determined",
                "wasf:right_position_analyzed:evidenced",
                "wasf:right_continuation_capable:evidenced",
                "illah:right_capability_determinable:verified",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            )
        else:
            # Short vowels/tanwin: can continue or close
            proves = (
                "asl:established",
                "far:determined",
                "wasf:right_position_analyzed:evidenced",
                "wasf:right_continuation_capable:evidenced",
                "wasf:right_closure_capable:evidenced",
                "illah:right_capability_determinable:verified",
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
                    evidence_id=f"ev:right_cap:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="RightCapabilityQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=RIGHT_CAPABILITY_ANALYSIS,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="RightCapabilityQiyas"),
        )

    def process_analysis(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process right capability analysis.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with RightCapabilityCandidate result
        """
        request = self.build_request_for_analysis(carrier_codepoint, mark_codepoint, trace_prefix)
        return self.kernel.apply(request)
