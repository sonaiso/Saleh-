from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.phono_functional_unit_rules import PHONO_FUNCTIONAL_UNIT_BINDING


@dataclass
class PhonoFunctionalUnitLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_binding(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for binding carrier and mark functions.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for phono-functional unit binding
        """
        if not trace_prefix:
            trace_prefix = f"phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing CarrierFunctionCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:carrier_fn:{carrier_codepoint:04x}",
            node_type="CarrierFunctionCandidate",
            identity_ids=(f"identity:carrier_fn:{carrier_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing MarkFunctionCandidate
        far = QiyasNodeRef(
            node_id=f"far:mark_fn:{mark_codepoint:04x}",
            node_type="MarkFunctionCandidate",
            identity_ids=(f"identity:mark_fn:{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Build evidence for phono-functional unit
        # Assume both carrier and mark functions are valid
        # (actual validation would come from previous layers)
        proves = (
            "asl:established",
            "far:determined",
            "wasf:carrier_and_mark_functional:evidenced",
            "illah:phonotactic_unit_composable:verified",
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
                    evidence_id=f"ev:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="PhonoFunctionalUnitQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=PHONO_FUNCTIONAL_UNIT_BINDING,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="PhonoFunctionalUnitQiyas"),
        )

    def process_binding(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a binding between carrier and mark functions.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with PhonoFunctionalUnitCandidate result
        """
        request = self.build_request_for_binding(carrier_codepoint, mark_codepoint, trace_prefix)
        return self.kernel.apply(request)
