from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import ClosureReadiness, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.mabni_murab_closure_readiness_rules import MABNI_MURAB_CLOSURE_READINESS_VALIDATION


@dataclass
class MabniMurabClosureReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        closure_readiness: ClosureReadiness,
        has_external_reference_evidence: bool = False,
        has_complement_evidence: bool = False,
        has_governor_evidence: bool = False,
        has_case_position_evidence: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for mabni/muʿrab closure readiness validation.

        This distinguishes between mabni (indeclinable) and muʿrab (declinable) forms
        at the readiness level, WITHOUT producing final meaning or case judgments.

        Args:
            closure_readiness: The ClosureReadiness classification from ClosureReadinessAdapter
            has_external_reference_evidence: Whether external reference evidence exists (for mabni)
            has_complement_evidence: Whether complement evidence exists (for mabni)
            has_governor_evidence: Whether governor evidence exists (for muʿrab)
            has_case_position_evidence: Whether case position evidence exists (for muʿrab)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for mabni/muʿrab closure readiness validation
        """
        if not trace_prefix:
            trace_prefix = f"mabni_murab:{closure_readiness.value}"

        # Create asl node - representing ClosureReadinessCandidate
        asl = QiyasNodeRef(
            node_id=f"اصل:closure_ready:{trace_prefix}",
            node_type="ClosureReadinessCandidate",
            identity_ids=(f"identity:closure_ready:{trace_prefix}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing mabni/muʿrab context
        far = QiyasNodeRef(
            node_id=f"فرع:mabni_murab_ctx:{trace_prefix}",
            node_type="MabniMurabContext",
            identity_ids=(f"identity:mabni_murab_ctx:{trace_prefix}",),
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

        # Distinguish mabni vs muʿrab readiness
        if closure_readiness == ClosureReadiness.MABNI_CLOSURE_READY:
            # Mabni form has stable internal structure
            proves.append("وصف:closure_type_distinguishable:evidenced")
            proves.append("وصف:mabni_form_stability:evidenced")
            proves.append("وصف:case_variation_blocked:evidenced")
            proves.append("وصف:mabni_murab_closure_ready:evidenced")
            proves.append("علة:mabni_murab_closure_determinable:verified")

            # But external reference/complement is still pending
            # This is readiness, not final meaning determination
            if not has_external_reference_evidence and not has_complement_evidence:
                proves.append("defer:external_reference_pending:present")

        elif closure_readiness == ClosureReadiness.MURAB_CLOSURE_DEFERRED:
            # Muʿrab form has open case slot
            proves.append("وصف:closure_type_distinguishable:evidenced")
            proves.append("وصف:murab_case_slot_open:evidenced")
            proves.append("وصف:mabni_murab_closure_ready:evidenced")
            proves.append("علة:mabni_murab_closure_determinable:verified")

            # Governor and case position are pending
            # This is readiness, not final case determination
            if not has_governor_evidence:
                proves.append("defer:governor_dependency_pending:present")
            if not has_case_position_evidence:
                proves.append("defer:case_position_pending:present")

            # Muʿrab closure readiness must be deferred
            proves.append("defer:murab_closure_deferred:present")

        elif closure_readiness == ClosureReadiness.UNKNOWN_CLOSURE:
            # Cannot determine closure type
            proves.append("فارق:closure_type_indeterminate:present")

        else:
            # Other closure types (PAUSE, CONTINUATION) may not have mabni/muʿrab distinction
            proves.append("وصف:closure_type_distinguishable:evidenced")
            proves.append("defer:mabni_murab_indeterminate:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:mabni_murab:{trace_prefix}:{uuid.uuid4().hex[:8]}",
                    source_layer="MabniMurabClosureReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=MABNI_MURAB_CLOSURE_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="MabniMurabClosureReadinessQiyas"),
        )

    def process_validation(
        self,
        closure_readiness: ClosureReadiness,
        has_external_reference_evidence: bool = False,
        has_complement_evidence: bool = False,
        has_governor_evidence: bool = False,
        has_case_position_evidence: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process mabni/muʿrab closure readiness validation.

        Args:
            closure_readiness: The ClosureReadiness classification from ClosureReadinessAdapter
            has_external_reference_evidence: Whether external reference evidence exists (for mabni)
            has_complement_evidence: Whether complement evidence exists (for mabni)
            has_governor_evidence: Whether governor evidence exists (for muʿrab)
            has_case_position_evidence: Whether case position evidence exists (for muʿrab)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with MabniMurabClosureReadinessCandidate result
        """
        request = self.build_request_for_validation(
            closure_readiness,
            has_external_reference_evidence,
            has_complement_evidence,
            has_governor_evidence,
            has_case_position_evidence,
            trace_prefix
        )
        return self.kernel.apply(request)
