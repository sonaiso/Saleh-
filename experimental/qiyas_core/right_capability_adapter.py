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
            node_id=f"اصل:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing right context
        far = QiyasNodeRef(
            node_id=f"فرع:right_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="RightContext",
            identity_ids=(f"identity:right_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Analyze right capability based on mark function
        mark_fn = classify_mark_function(mark_codepoint)

        # Sukun allows continuation (can be followed by another syllable)
        # Short vowels and tanwin allow continuation or closure
        if mark_fn == MarkFunction.SUKUN_MARK:
            proves = (
                "اصل:established",
                "فرع:determined",
                "وصف:right_position_analyzed:evidenced",
                "وصف:right_continuation_capable:evidenced",
                "علة:right_capability_determinable:verified",
                "وادي:cause:established",
                "وادي:condition:satisfied",
                "وادي:obstacle:absent",
                "وادي:validity:valid",
                "وادي:corruption:absent",
                "وادي:nullity:absent",
            )
        else:
            # Short vowels/tanwin: can continue or close
            proves = (
                "اصل:established",
                "فرع:determined",
                "وصف:right_position_analyzed:evidenced",
                "وصف:right_continuation_capable:evidenced",
                "وصف:right_closure_capable:evidenced",
                "علة:right_capability_determinable:verified",
                "وادي:cause:established",
                "وادي:condition:satisfied",
                "وادي:obstacle:absent",
                "وادي:validity:valid",
                "وادي:corruption:absent",
                "وادي:nullity:absent",
            )

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:right_cap:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="RightCapabilityQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
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
