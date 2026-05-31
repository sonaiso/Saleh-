from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank, MarkFunction
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .mark_function_adapter import classify_mark_function
from .node import QiyasNodeRef
from .rules.syllable_readiness_rules import SYLLABLE_READINESS_VALIDATION


@dataclass
class SyllableReadinessLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        is_initial_position: bool = False,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for syllable readiness validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            is_initial_position: Whether this is at word/syllable start
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for syllable readiness validation
        """
        if not trace_prefix:
            trace_prefix = f"syl_ready:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node - representing PhonoFunctionalUnitCandidate
        asl = QiyasNodeRef(
            node_id=f"asl:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="PhonoFunctionalUnitCandidate",
            identity_ids=(f"identity:phono_fn:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing syllable context
        far = QiyasNodeRef(
            node_id=f"far:syl_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",
            node_type="SyllableContext",
            identity_ids=(f"identity:syl_ctx:{carrier_codepoint:04x}+{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Check for blocking conditions
        mark_fn = classify_mark_function(mark_codepoint)
        blocking_conditions = []

        # Check for initial sukun (not allowed at word start)
        if is_initial_position and mark_fn == MarkFunction.SUKUN_MARK:
            blocking_conditions.append("fariq:initial_sukun:present")

        # Check for additional diacritic being treated as vowel
        if mark_fn == MarkFunction.ADDITIONAL_DIACRITIC_MARK:
            blocking_conditions.append("residual:additional_diacritic_as_vowel:blocked")

        # Build evidence
        if blocking_conditions:
            # Has blocking or deferring conditions
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
            proves.extend(blocking_conditions)
            proves = tuple(proves)
        else:
            # Minimal syllable readiness satisfied
            proves = (
                "asl:established",
                "far:determined",
                "wasf:minimal_syllabic_structure:evidenced",
                "illah:minimal_syllable_readiness:verified",
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
                    evidence_id=f"ev:syl_ready:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="SyllableReadinessQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=SYLLABLE_READINESS_VALIDATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SyllableReadinessQiyas"),
        )

    def process_validation(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        is_initial_position: bool = False,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process syllable readiness validation.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            mark_codepoint: The Unicode codepoint of the mark
            is_initial_position: Whether this is at word/syllable start
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with SyllableReadinessCandidate result
        """
        request = self.build_request_for_validation(
            carrier_codepoint, mark_codepoint, is_initial_position, trace_prefix
        )
        return self.kernel.apply(request)
