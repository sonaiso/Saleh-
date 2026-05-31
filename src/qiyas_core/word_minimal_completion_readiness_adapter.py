from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.word_minimal_completion_readiness_rules import WORD_MINIMAL_COMPLETION_READINESS_VALIDATION


@dataclass
class WordMinimalCompletionReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        word_closure_readiness_candidate_id: str,
        has_minimal_components: bool = False,
        missing_components: list[str] = None,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for word minimal completion readiness validation.

        This validates that a word has all minimal components needed for completion,
        WITHOUT producing a final WordCandidate.

        Args:
            word_closure_readiness_candidate_id: ID of WordInternalClosureReadinessCandidate
            has_minimal_components: Whether all minimal components are present
            missing_components: List of missing component names (if any)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for word minimal completion readiness validation
        """
        if missing_components is None:
            missing_components = []

        if not trace_prefix:
            trace_prefix = f"word_completion:{word_closure_readiness_candidate_id}"

        # Create asl node - representing WordInternalClosureReadinessCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:word_closure_ready:{trace_prefix}",
            node_type="WordInternalClosureReadinessCandidate",
            identity_ids=(f"identity:word_closure:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing word completion context
        far = QiyasNodeRef(
            node_id=f"far:word_completion_ctx:{trace_prefix}",
            node_type="WordCompletionContext",
            identity_ids=(f"identity:word_completion_ctx:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Build evidence
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

        # We have word closure readiness as input
        proves.append("wasf:word_closure_readiness_available:evidenced")

        # Check if minimal components are present
        if has_minimal_components:
            proves.append("wasf:minimal_word_components_present:evidenced")
            proves.append("wasf:word_minimal_completion_ready:evidenced")
            proves.append("illah:word_minimal_completion_fit:verified")
        else:
            # Missing components - block or defer
            if missing_components:
                # Specific components missing - this blocks completion
                proves.append("fariq:word_components_missing:present")
            else:
                # Unknown if components are complete - defer
                proves.append("defer:word_completion_pending:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:word_completion:{trace_prefix}:{uuid.uuid4().hex[:8]}",
                    source_layer="WordMinimalCompletionReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=WORD_MINIMAL_COMPLETION_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="WordMinimalCompletionReadinessQiyas"),
        )

    def process_validation(
        self,
        word_closure_readiness_candidate_id: str,
        has_minimal_components: bool = False,
        missing_components: list[str] = None,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process word minimal completion readiness validation.

        Args:
            word_closure_readiness_candidate_id: ID of WordInternalClosureReadinessCandidate
            has_minimal_components: Whether all minimal components are present
            missing_components: List of missing component names (if any)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with WordMinimalCompletionReadinessCandidate result
        """
        request = self.build_request_for_validation(
            word_closure_readiness_candidate_id,
            has_minimal_components,
            missing_components,
            trace_prefix
        )
        return self.kernel.apply(request)
