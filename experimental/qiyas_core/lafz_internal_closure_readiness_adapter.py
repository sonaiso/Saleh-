from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.lafz_internal_closure_readiness_rules import LAFZ_INTERNAL_CLOSURE_READINESS_VALIDATION


@dataclass
class LafzInternalClosureReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        syllable_readiness_candidates: list[str],
        closure_readiness_candidates: list[str],
        has_syllable_order_equilibrium: bool = False,
        has_phonotactic_economy: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for lafz internal closure readiness validation.

        This validates that lafz-level closure readiness can be determined
        from constituent syllable readiness states, WITHOUT building SyllableCandidate.

        Args:
            syllable_readiness_candidates: List of SyllableReadinessCandidates IDs
            closure_readiness_candidates: List of ClosureReadinessCandidates IDs
            has_syllable_order_equilibrium: Whether syllable order equilibrium evidence exists
            has_phonotactic_economy: Whether phonotactic economy evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for lafz internal closure readiness validation
        """
        if not trace_prefix:
            trace_prefix = f"lafz_closure:{len(syllable_readiness_candidates)}_syllables"

        # Create asl node - representing SyllableReadinessCandidate
        # This is a representative node, not an actual syllable
        asl = QiyasNodeRef(
            node_id=f"اصل:syl_ready:{trace_prefix}",
            node_type="SyllableReadinessCandidate",
            identity_ids=(f"identity:syl_ready_set:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing lafz closure context
        far = QiyasNodeRef(
            node_id=f"فرع:lafz_closure_ctx:{trace_prefix}",
            node_type="LafzClosureContext",
            identity_ids=(f"identity:lafz_closure_ctx:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Check for blocking conditions
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

        # Check if we have syllable readiness evidence
        if not syllable_readiness_candidates or len(syllable_readiness_candidates) == 0:
            # Missing syllable readiness - this blocks lafz closure
            proves.append("فارق:syllable_readiness_missing:present")
        else:
            # We have syllable readiness evidence
            proves.append("وصف:syllable_readiness_available:evidenced")

            # Check if we have order preservation evidence
            if has_syllable_order_equilibrium:
                proves.append("وصف:internal_lafz_order_preserved:evidenced")
            else:
                # Order not established - defer
                proves.append("defer:lafz_order_pending:present")

            # Check closure readiness from constituent syllables
            if closure_readiness_candidates and len(closure_readiness_candidates) > 0:
                proves.append("وصف:lafz_internal_closure_ready:evidenced")
                proves.append("علة:lafz_internal_closure_fit:verified")
            else:
                # No closure readiness evidence yet - defer
                proves.append("defer:lafz_closure_readiness_pending:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:lafz_closure:{trace_prefix}:{uuid.uuid4().hex[:8]}",
                    source_layer="LafzInternalClosureReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=LAFZ_INTERNAL_CLOSURE_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="LafzInternalClosureReadinessQiyas"),
        )

    def process_validation(
        self,
        syllable_readiness_candidates: list[str],
        closure_readiness_candidates: list[str],
        has_syllable_order_equilibrium: bool = False,
        has_phonotactic_economy: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process lafz internal closure readiness validation.

        Args:
            syllable_readiness_candidates: List of SyllableReadinessCandidates IDs
            closure_readiness_candidates: List of ClosureReadinessCandidates IDs
            has_syllable_order_equilibrium: Whether syllable order equilibrium evidence exists
            has_phonotactic_economy: Whether phonotactic economy evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with LafzInternalClosureReadinessCandidate result
        """
        request = self.build_request_for_validation(
            syllable_readiness_candidates,
            closure_readiness_candidates,
            has_syllable_order_equilibrium,
            has_phonotactic_economy,
            trace_prefix
        )
        return self.kernel.apply(request)
