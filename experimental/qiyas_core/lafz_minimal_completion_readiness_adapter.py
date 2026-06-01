from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.lafz_minimal_completion_readiness_rules import LAFZ_MINIMAL_COMPLETION_READINESS_VALIDATION


@dataclass
class LafzMinimalCompletionReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        lafz_closure_readiness_candidate_id: str,
        has_minimal_components: bool = False,
        missing_components: list[str] = None,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for lafz minimal completion readiness validation.

        This validates that a lafz has all minimal components needed for completion,
        WITHOUT producing a final LafzCandidate.

        Args:
            lafz_closure_readiness_candidate_id: ID of LafzInternalClosureReadinessCandidate
            has_minimal_components: Whether all minimal components are present
            missing_components: List of missing component names (if any)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for lafz minimal completion readiness validation
        """
        if missing_components is None:
            missing_components = []

        if not trace_prefix:
            trace_prefix = f"lafz_completion:{lafz_closure_readiness_candidate_id}"

        # Create asl node - representing LafzInternalClosureReadinessCandidate
        asl = QiyasNodeRef(
            node_id=f"اصل:lafz_closure_ready:{trace_prefix}",
            node_type="LafzInternalClosureReadinessCandidate",
            identity_ids=(f"identity:lafz_closure:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing lafz completion context
        far = QiyasNodeRef(
            node_id=f"فرع:lafz_completion_ctx:{trace_prefix}",
            node_type="LafzCompletionContext",
            identity_ids=(f"identity:lafz_completion_ctx:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Build evidence
        proves = [
            "اصل:established",
            "فرع:determined",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # We have lafz closure readiness as input
        proves.append("وصف:lafz_closure_readiness_available:evidenced")

        # Check if minimal components are present
        if has_minimal_components:
            proves.append("وصف:minimal_lafz_components_present:evidenced")
            proves.append("وصف:lafz_minimal_completion_ready:evidenced")
            proves.append("علة:lafz_minimal_completion_fit:verified")
        else:
            # Missing components - block or defer
            if missing_components:
                # Specific components missing - this blocks completion
                proves.append("فارق:lafz_components_missing:present")
            else:
                # Unknown if components are complete - defer
                proves.append("defer:lafz_completion_pending:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:lafz_completion:{trace_prefix}:{uuid.uuid4().hex[:8]}",
                    source_layer="LafzMinimalCompletionReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=LAFZ_MINIMAL_COMPLETION_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="LafzMinimalCompletionReadinessQiyas"),
        )

    def process_validation(
        self,
        lafz_closure_readiness_candidate_id: str,
        has_minimal_components: bool = False,
        missing_components: list[str] = None,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process lafz minimal completion readiness validation.

        Args:
            lafz_closure_readiness_candidate_id: ID of LafzInternalClosureReadinessCandidate
            has_minimal_components: Whether all minimal components are present
            missing_components: List of missing component names (if any)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with LafzMinimalCompletionReadinessCandidate result
        """
        request = self.build_request_for_validation(
            lafz_closure_readiness_candidate_id,
            has_minimal_components,
            missing_components,
            trace_prefix
        )
        return self.kernel.apply(request)
