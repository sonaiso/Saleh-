from dataclasses import dataclass
import uuid

from .atomic_unit_adapter import is_arabic_letter
from .candidate import CandidateSet
from .enums import CarrierFunction, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.carrier_function_rules import CARRIER_FUNCTION_CLASSIFICATION


# Weak letters (حروف العلة): Alif, Waw, Ya
WEAK_LETTERS = (0x0627, 0x0648, 0x064A)  # ا و ي

# Hamza variants
HAMZA_CODEPOINTS = (0x0621, 0x0623, 0x0624, 0x0625, 0x0626)  # ء أ ؤ إ ئ


def classify_carrier_function(codepoint: int) -> CarrierFunction:
    """
    Classify an Arabic letter carrier by its phonotactic function.

    Args:
        codepoint: The Unicode codepoint value

    Returns:
        CarrierFunction classification
    """
    if not is_arabic_letter(codepoint):
        return CarrierFunction.NON_CARRIER

    # Hamza variants
    if codepoint in HAMZA_CODEPOINTS:
        return CarrierFunction.HAMZA_CARRIER

    # Weak letters (can function as long vowels)
    if codepoint in WEAK_LETTERS:
        # Initially classify as WEAK_LETTER_CARRIER
        # They can be LONG_VOWEL_LETTER in specific contexts, but that's
        # context-dependent and should be deferred to later analysis
        return CarrierFunction.WEAK_LETTER_CARRIER

    # All other Arabic consonants
    return CarrierFunction.ARABIC_CONSONANT_CARRIER


@dataclass
class CarrierFunctionLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_carrier(
        self,
        carrier_codepoint: int,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for classifying carrier function.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for carrier function classification
        """
        if not trace_prefix:
            trace_prefix = f"carrier_fn:{carrier_codepoint:04x}"

        # Create asl node - representing an AtomicUnitCandidate context
        asl = QiyasNodeRef(
            node_id=f"اصل:atomic_unit:{carrier_codepoint:04x}",
            node_type="AtomicUnitCandidate",
            identity_ids=(f"identity:atomic_unit:{carrier_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node - representing the carrier codepoint
        far = QiyasNodeRef(
            node_id=f"فرع:carrier:{carrier_codepoint:04x}",
            node_type="CarrierCodepoint",
            identity_ids=(f"identity:carrier:{carrier_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Classify carrier function
        carrier_fn = classify_carrier_function(carrier_codepoint)

        if carrier_fn == CarrierFunction.NON_CARRIER:
            # Non-carrier: establish basics but add fariq
            proves = (
                "اصل:established",
                "فرع:determined",
                "وادي:cause:established",
                "وادي:condition:satisfied",
                "وادي:obstacle:absent",
                "وادي:validity:valid",
                "وادي:corruption:absent",
                "وادي:nullity:absent",
                "فارق:non_carrier_codepoint:present",
            )
        else:
            # Valid carrier with determinable function
            proves = [
                "اصل:established",
                "فرع:determined",
                "وصف:carrier_has_phonotactic_role:evidenced",
                "علة:carrier_function_determinable:verified",
                "وادي:cause:established",
                "وادي:condition:satisfied",
                "وادي:obstacle:absent",
                "وادي:validity:valid",
                "وادي:corruption:absent",
                "وادي:nullity:absent",
            ]

            # Add function-specific classification evidence
            if carrier_fn == CarrierFunction.ARABIC_CONSONANT_CARRIER:
                proves.append("وصف:arabic_consonant_carrier:evidenced")
            elif carrier_fn == CarrierFunction.WEAK_LETTER_CARRIER:
                proves.append("وصف:weak_letter_carrier:evidenced")
                proves.append("residual:possible_long_vowel_context:deferred")
            elif carrier_fn == CarrierFunction.HAMZA_CARRIER:
                proves.append("وصف:hamza_carrier:evidenced")
            elif carrier_fn == CarrierFunction.LONG_VOWEL_LETTER:
                proves.append("وصف:long_vowel_letter:evidenced")

            # Add augmentation readiness (not a final judgment)
            if carrier_fn in (CarrierFunction.WEAK_LETTER_CARRIER, CarrierFunction.HAMZA_CARRIER):
                proves.append("residual:possible_augment_letter:readiness")

            proves = tuple(proves)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:carrier_fn:{carrier_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="CarrierFunctionQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=CARRIER_FUNCTION_CLASSIFICATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="CarrierFunctionQiyas"),
        )

    def process_carrier(
        self,
        carrier_codepoint: int,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a carrier codepoint for function classification.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with CarrierFunctionCandidate result
        """
        request = self.build_request_for_carrier(carrier_codepoint, trace_prefix)
        return self.kernel.apply(request)
