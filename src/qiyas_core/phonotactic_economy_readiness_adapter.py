from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.phonotactic_economy_readiness_rules import PHONOTACTIC_ECONOMY_READINESS_VALIDATION


@dataclass
class PhonotacticEconomyReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for phonotactic economy readiness validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for phonotactic economy readiness validation
        """
        if not trace_prefix:
            trace_prefix = f"phono_econ:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing PhonoFunctionalUnitCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing phonotactic economy context
        far = QiyasNodeRef(
            node_id=f"far:phono_econ_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonotacticEconomyContext",
            identity_ids=(f"identity:phono_econ_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Minimal phonotactic economy: carrier+mark is sufficient
        # No redundant structure detected at this level
        proves = (
            "asl:established",
            "far:determined",
            "wasf:minimal_phonotactic_economy:evidenced",
            "illah:phonotactic_economy_sufficient:verified",
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
                    evidence_id=f"ev:phono_econ:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="PhonotacticEconomyReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=PHONOTACTIC_ECONOMY_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="PhonotacticEconomyReadinessQiyas"),
        )

    def process_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process phonotactic economy readiness validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with PhonotacticEconomyReadinessCandidate result
        """
        request = self.build_request_for_validation(carrier_codepoint, mark_codepoint, trace_prefix)
        return self.kernel.apply(request)
