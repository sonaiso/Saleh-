from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.word_internal_closure_readiness_rules import WORD_INTERNAL_CLOSURE_READINESS_VALIDATION


@dataclass
class WordInternalClosureReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        lafz_closure_readiness_candidates: list[str],
        has_word_boundary_capability: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for word internal closure readiness validation.

        This validates that word-level closure readiness can be determined
        from constituent lafz closure readiness states, WITHOUT building LafzCandidate.

        Args:
            lafz_closure_readiness_candidates: List of LafzInternalClosureReadinessCandidates IDs
            has_word_boundary_capability: Whether word boundary evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for word internal closure readiness validation
        """
        if not trace_prefix:
            trace_prefix = f"word_closure:{len(lafz_closure_readiness_candidates)}_lafz"

        # Create asl node - representing LafzInternalClosureReadinessCandidate
        asl = QiyasNodeRef(
            node_id=f"اصل:lafz_closure_ready:{trace_prefix}",
            node_type="LafzInternalClosureReadinessCandidate",
            identity_ids=(f"identity:lafz_closure_set:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing word closure context
        far = QiyasNodeRef(
            node_id=f"فرع:word_closure_ctx:{trace_prefix}",
            node_type="WordClosureContext",
            identity_ids=(f"identity:word_closure_ctx:{trace_prefix}",),
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

        # Check if we have lafz closure readiness evidence
        if not lafz_closure_readiness_candidates or len(lafz_closure_readiness_candidates) == 0:
            # Missing lafz closure readiness - this blocks word closure
            proves.append("فارق:lafz_closure_readiness_missing:present")
        else:
            # We have lafz closure readiness evidence
            proves.append("وصف:lafz_closure_readiness_available:evidenced")

            # Check word boundary capability
            if has_word_boundary_capability:
                proves.append("وصف:word_boundary_capability:evidenced")
                proves.append("وصف:word_internal_closure_ready:evidenced")
                proves.append("علة:word_internal_closure_fit:verified")
            else:
                # Word boundary not established - defer
                proves.append("defer:word_boundary_pending:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:word_closure:{trace_prefix}:{uuid.uuid4().hex[:8]}",
                    source_layer="WordInternalClosureReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=WORD_INTERNAL_CLOSURE_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="WordInternalClosureReadinessQiyas"),
        )

    def process_validation(
        self,
        lafz_closure_readiness_candidates: list[str],
        has_word_boundary_capability: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process word internal closure readiness validation.

        Args:
            lafz_closure_readiness_candidates: List of LafzInternalClosureReadinessCandidates IDs
            has_word_boundary_capability: Whether word boundary evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with WordInternalClosureReadinessCandidate result
        """
        request = self.build_request_for_validation(
            lafz_closure_readiness_candidates,
            has_word_boundary_capability,
            trace_prefix
        )
        return self.kernel.apply(request)
