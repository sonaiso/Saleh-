from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import ClosureReadiness, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.closure_readiness_rules import CLOSURE_READINESS_VALIDATION


def classify_closure_readiness(
    has_mabni_evidence: bool = False,
    has_murab_evidence: bool = False,
    has_case_evidence: bool = False,
    has_waqf_evidence: bool = False,
    has_continuation_evidence: bool = False
) -> ClosureReadiness:
    """
    Classify closure readiness based on available evidence.

    Args:
        has_mabni_evidence: Whether mabni (indeclinable) evidence exists
        has_murab_evidence: Whether muʿrab (declinable) evidence exists
        has_case_evidence: Whether case marking evidence exists
        has_waqf_evidence: Whether pause (waqf) evidence exists
        has_continuation_evidence: Whether continuation evidence exists

    Returns:
        ClosureReadiness classification

    Note:
        Conflicting mabni+murab evidence should be handled by caller
        and produce a blocking fariq or unknown closure state
    """
    # Closure law: mabni evidence => MABNI_CLOSURE_READY
    if has_mabni_evidence:
        return ClosureReadiness.MABNI_CLOSURE_READY

    # Closure law: muʿrab evidence without case/waqf/continuation => MURAB_CLOSURE_DEFERRED
    if has_murab_evidence:
        # Muʿrab closure must remain deferred unless case/waqf/continuation evidence exists
        if has_case_evidence or has_waqf_evidence or has_continuation_evidence:
            # Have additional evidence to determine closure state
            if has_waqf_evidence:
                return ClosureReadiness.PAUSE_CLOSURE_READY
            elif has_continuation_evidence:
                return ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED
            # Has case evidence - still muʿrab deferred
            return ClosureReadiness.MURAB_CLOSURE_DEFERRED
        else:
            # Muʿrab without case/waqf/continuation must be deferred
            return ClosureReadiness.MURAB_CLOSURE_DEFERRED

    # If we have evidence of pause/waqf (without mabni/murab classification), closure is ready
    if has_waqf_evidence:
        return ClosureReadiness.PAUSE_CLOSURE_READY

    # If we have evidence of continuation, closure is deferred
    if has_continuation_evidence:
        return ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED

    # Without evidence, we cannot determine closure readiness
    # Default: unknown closure (must be deferred)
    return ClosureReadiness.UNKNOWN_CLOSURE


@dataclass
class ClosureReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        has_mabni_evidence: bool = False,
        has_murab_evidence: bool = False,
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
            has_mabni_evidence: Whether mabni (indeclinable) evidence exists
            has_murab_evidence: Whether muʿrab (declinable) evidence exists
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
            node_id=f"اصل:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing closure context
        far = QiyasNodeRef(
            node_id=f"فرع:closure_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="ClosureContext",
            identity_ids=(f"identity:closure_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Classify closure readiness
        # First check for conflicting evidence
        if has_mabni_evidence and has_murab_evidence:
            # Conflicting evidence - cannot determine closure
            closure = ClosureReadiness.UNKNOWN_CLOSURE
            has_conflict = True
        else:
            closure = classify_closure_readiness(
                has_mabni_evidence, has_murab_evidence, has_case_evidence,
                has_waqf_evidence, has_continuation_evidence
            )
            has_conflict = False

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:closure_readiness_analyzed:evidenced",
            "علة:closure_readiness_determinable:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Add conflicting evidence fariq if detected
        if has_conflict:
            proves.append("فارق:conflicting_mabni_murab_evidence:present")

        # Add closure-specific evidence
        if closure == ClosureReadiness.PAUSE_CLOSURE_READY:
            proves.append("وصف:pause_closure_ready:evidenced")
        elif closure == ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED:
            proves.append("defer:continuation_closure_deferred:present")
        elif closure == ClosureReadiness.UNKNOWN_CLOSURE:
            # Unknown closure must be deferred
            proves.append("defer:unknown_closure_deferred:present")
        elif closure == ClosureReadiness.MABNI_CLOSURE_READY:
            # Mabni closure may be structurally stable (if we had evidence)
            proves.append("وصف:mabni_closure_ready:evidenced")
        elif closure == ClosureReadiness.MURAB_CLOSURE_DEFERRED:
            # Muʿrab closure must remain deferred
            proves.append("defer:murab_closure_deferred:present")

        proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:closure:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="ClosureReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
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
        has_mabni_evidence: bool = False,
        has_murab_evidence: bool = False,
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
            has_mabni_evidence: Whether mabni (indeclinable) evidence exists
            has_murab_evidence: Whether muʿrab (declinable) evidence exists
            has_case_evidence: Whether case marking evidence exists
            has_waqf_evidence: Whether pause (waqf) evidence exists
            has_continuation_evidence: Whether continuation evidence exists
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with ClosureReadinessCandidate result
        """
        request = self.build_request_for_validation(
            carrier_codepoint, mark_codepoint,
            has_mabni_evidence, has_murab_evidence, has_case_evidence,
            has_waqf_evidence, has_continuation_evidence,
            trace_prefix
        )
        return self.kernel.apply(request)
