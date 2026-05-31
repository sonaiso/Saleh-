from dataclasses import dataclass
import uuid

from .enums import DiacriticKind, EvidenceRank, MarkFunction
from .evidence import Evidence, EvidenceSet
from .haraka_adapter import classify_diacritic
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.mark_function_rules import MARK_FUNCTION_CLASSIFICATION


# Tanwin codepoints
TANWIN_MARKS = (0x064B, 0x064C, 0x064D)  # Fathatan, Dammatan, Kasratan

# Short vowel marks
SHORT_VOWEL_MARKS = (0x064E, 0x064F, 0x0650)  # Fatha, Damma, Kasra


def classify_mark_function(codepoint: int) -> MarkFunction:
    """
    Classify a diacritic mark by its phonotactic function.

    Args:
        codepoint: The Unicode codepoint value

    Returns:
        MarkFunction classification
    """
    diacritic_kind = classify_diacritic(codepoint)

    if diacritic_kind is None:
        return MarkFunction.UNKNOWN_MARK_FUNCTION

    if diacritic_kind == DiacriticKind.CORE_HARAKA:
        # Distinguish between short vowels and tanwin
        if codepoint in TANWIN_MARKS:
            return MarkFunction.TANWIN_MARK
        elif codepoint in SHORT_VOWEL_MARKS:
            return MarkFunction.SHORT_VOWEL_MARK
        else:
            # Shouldn't happen if classify_diacritic is correct
            return MarkFunction.UNKNOWN_MARK_FUNCTION

    elif diacritic_kind == DiacriticKind.SHADDA:
        return MarkFunction.SHADDA_MARK

    elif diacritic_kind == DiacriticKind.SUKUN:
        return MarkFunction.SUKUN_MARK

    elif diacritic_kind == DiacriticKind.ADDITIONAL:
        return MarkFunction.ADDITIONAL_DIACRITIC_MARK

    return MarkFunction.UNKNOWN_MARK_FUNCTION


@dataclass
class MarkFunctionLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_mark(
        self,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for classifying mark function.

        Args:
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for mark function classification
        """
        if not trace_prefix:
            trace_prefix = f"mark_fn:{mark_codepoint:04x}"

        # Create asl node - representing an AtomicUnitCandidate context
        asl = QiyasNodeRef(
            node_id=f"asl:atomic_unit:{mark_codepoint:04x}",
            node_type="AtomicUnitCandidate",
            identity_ids=(f"identity:atomic_unit:{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node - representing the mark codepoint
        far = QiyasNodeRef(
            node_id=f"far:mark:{mark_codepoint:04x}",
            node_type="MarkCodepoint",
            identity_ids=(f"identity:mark:{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Classify mark function
        mark_fn = classify_mark_function(mark_codepoint)

        if mark_fn == MarkFunction.UNKNOWN_MARK_FUNCTION:
            # Unknown mark: establish basics but add fariq
            proves = (
                "asl:established",
                "far:determined",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
                "fariq:mark_function_indeterminate:present",
            )
        else:
            # Valid mark with determinable function
            proves = [
                "asl:established",
                "far:determined",
                "wasf:mark_has_phonotactic_role:evidenced",
                "illah:mark_function_determinable:verified",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            ]

            # Add function-specific classification evidence
            if mark_fn == MarkFunction.SHORT_VOWEL_MARK:
                proves.append("wasf:short_vowel_mark:evidenced")
            elif mark_fn == MarkFunction.TANWIN_MARK:
                proves.append("wasf:tanwin_mark:evidenced")
            elif mark_fn == MarkFunction.SUKUN_MARK:
                proves.append("wasf:sukun_mark:evidenced")
                # Sukun may be problematic at word start
                proves.append("residual:initial_sukun_check:deferred")
            elif mark_fn == MarkFunction.SHADDA_MARK:
                proves.append("wasf:shadda_mark:evidenced")
                # Shadda requires carrier validation
                proves.append("residual:shadda_carrier_validation:deferred")
            elif mark_fn == MarkFunction.ADDITIONAL_DIACRITIC_MARK:
                proves.append("wasf:additional_diacritic_mark:evidenced")
                # Additional marks should not be treated as short vowels
                proves.append("residual:additional_not_vowel:constraint")

            proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:mark_fn:{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="MarkFunctionQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=MARK_FUNCTION_CLASSIFICATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="MarkFunctionQiyas"),
        )

    def process_mark(
        self,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> "CandidateSet":
        """
        Process a mark codepoint for function classification.

        Args:
            mark_codepoint: The Unicode codepoint of the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with MarkFunctionCandidate result
        """
        request = self.build_request_for_mark(mark_codepoint, trace_prefix)
        return self.kernel.apply(request)
