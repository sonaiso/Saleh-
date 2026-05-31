from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import ClosureReadiness, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.closure_readiness_rules import CLOSURE_READINESS_VALIDATION


def classify_closure_readiness(
    has_case_evidence: bool = False,
    has_waqf_evidence: bool = False,
    has_continuation_evidence: bool = False
) -> ClosureReadiness:
    """
    Classify closure readiness based on available evidence.

    Args:
        has_case_evidence: Whether case marking evidence exists
        has_waqf_evidence: Whether pause (waqf) evidence exists
        has_continuation_evidence: Whether continuation evidence exists

    Returns:
        ClosureReadiness classification
    """
    # At this layer, we don't have morphological or syntactic evidence yet
    # So we defer closure decisions unless specific evidence exists

    # If we had evidence of pause/waqf, closure is ready
    if has_waqf_evidence:
        return ClosureReadiness.PAUSE_CLOSURE_READY

    # If we had evidence of continuation, closure is deferred
    if has_continuation_evidence:
        return ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED

    # Without evidence, we cannot determine if this is mabni or muʿrab
    # Default: unknown closure (must be deferred)
    return ClosureReadiness.UNKNOWN_CLOSURE


@dataclass
class ClosureReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        has_case_evidence: bool = False,
        has_waqf_evidence: bool = False,
        has_continuation_evidence: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for closure readiness validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            has_case_evidence: Whether case marking evidence exists
            has_waqf_evidence: Whether pause (waqf) evidence exists
            has_continuation_evidence: Whether continuation evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for closure readiness validation
        """
        if not trace_prefix:
            trace_prefix = f"closure:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing PhonoFunctionalUnitCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing closure context
        far = QiyasNodeRef(
            node_id=f"far:closure_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="ClosureContext",
            identity_ids=(f"identity:closure_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Classify closure readiness
        closure = classify_closure_readiness(
            has_case_evidence, has_waqf_evidence, has_continuation_evidence
        )

        proves = [
            "asl:established",
            "far:determined",
            "wasf:closure_readiness_analyzed:evidenced",
            "illah:closure_readiness_determinable:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
        ]

        # Add closure-specific evidence
        if closure == ClosureReadiness.PAUSE_CLOSURE_READY:
            proves.append("wasf:pause_closure_ready:evidenced")
        elif closure == ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED:
            proves.append("residual:continuation_closure_deferred:deferred")
        elif closure == ClosureReadiness.UNKNOWN_CLOSURE:
            # Unknown closure must be deferred
            proves.append("residual:unknown_closure_deferred:deferred")
        elif closure == ClosureReadiness.MABNI_CLOSURE_READY:
            # Mabni closure may be structurally stable (if we had evidence)
            proves.append("wasf:mabni_closure_ready:evidenced")
        elif closure == ClosureReadiness.MURAB_CLOSURE_DEFERRED:
            # Muʿrab closure must remain deferred
            proves.append("residual:murab_closure_deferred:deferred")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:closure:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="ClosureReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=CLOSURE_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="ClosureReadinessQiyas"),
        )

    def process_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        has_case_evidence: bool = False,
        has_waqf_evidence: bool = False,
        has_continuation_evidence: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process closure readiness validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            has_case_evidence: Whether case marking evidence exists
            has_waqf_evidence: Whether pause (waqf) evidence exists
            has_continuation_evidence: Whether continuation evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with ClosureReadinessCandidate result
        """
        request = self.build_request_for_validation(
            carrier_codepoint, mark_codepoint,
            has_case_evidence, has_waqf_evidence, has_continuation_evidence,
            trace_prefix
        )
        return self.kernel.apply(request)
