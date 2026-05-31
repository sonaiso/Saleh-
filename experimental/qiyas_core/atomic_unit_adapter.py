from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .haraka_adapter import classify_diacritic
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.atomic_unit_rules import ATOMIC_UNIT_BINDING


# Arabic letters range (excluding combining marks and digits)
# Main Arabic letters: U+0621 (Hamza) to U+064A (Ya)
ARABIC_LETTER_RANGE = (0x0621, 0x064A)


def is_arabic_letter(codepoint: int) -> bool:
    """
    Check if a codepoint is an Arabic letter (not a digit or combining mark).

    Args:
        codepoint: The Unicode codepoint value

    Returns:
        True if the codepoint is an Arabic letter, False otherwise
    """
    return ARABIC_LETTER_RANGE[0] <= codepoint <= ARABIC_LETTER_RANGE[1]


@dataclass
class AtomicUnitLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_binding(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for binding a carrier and mark without applying it.

        This method is useful for testing and inspecting the evidence that would be
        generated for an atomic unit binding without actually processing it.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier (e.g., Arabic letter)
            mark_codepoint: The Unicode codepoint of the mark (e.g., haraka/diacritic)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest that would be used to process this atomic unit binding
        """
        if not trace_prefix:
            trace_prefix = f"atomic:{carrier_codepoint:04x}+{mark_codepoint:04x}"

        # Create asl node representing the carrier (UnicodeCandidate)
        asl = QiyasNodeRef(
            node_id=f"asl:carrier:{carrier_codepoint:04x}",
            node_type="UnicodeCandidate",
            identity_ids=(f"identity:carrier:{carrier_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node representing the mark (HarakaCandidate)
        far = QiyasNodeRef(
            node_id=f"far:mark:{mark_codepoint:04x}",
            node_type="HarakaCandidate",
            identity_ids=(f"identity:mark:{mark_codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Build evidence based on whether binding is valid
        carrier_is_letter = is_arabic_letter(carrier_codepoint)
        mark_is_diacritic = classify_diacritic(mark_codepoint) is not None

        if carrier_is_letter and mark_is_diacritic:
            # Valid Arabic letter carrier + valid diacritic mark - all checks pass
            proves = [
                "asl:established",
                "far:determined",
                "wasf:carrier_accepts_mark:evidenced",
                "illah:licensed_atomic_binding:verified",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            ]
            proves = tuple(proves)
        elif not carrier_is_letter and not mark_is_diacritic:
            # Both invalid - establish basics but add both fariq
            proves = (
                "asl:established",
                "far:determined",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
                "fariq:carrier_is_not_arabic_letter:present",
                "fariq:mark_is_not_arabic_diacritic:present",
            )
        elif not carrier_is_letter:
            # Invalid carrier only - establish basics but add fariq
            proves = (
                "asl:established",
                "far:determined",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
                "fariq:carrier_is_not_arabic_letter:present",
            )
        else:
            # Invalid mark only - establish basics but add fariq
            proves = (
                "asl:established",
                "far:determined",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
                "fariq:mark_is_not_arabic_diacritic:present",
            )

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:atomic:{carrier_codepoint:04x}+{mark_codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="AtomicUnitQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        # Build and return request
        return QiyasRequest(
            rule=ATOMIC_UNIT_BINDING,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="AtomicUnitQiyas"),
        )

    def process_binding(
        self,
        carrier_codepoint: int,
        mark_codepoint: int,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a binding between a carrier codepoint and a mark codepoint.

        Args:
            carrier_codepoint: The Unicode codepoint of the carrier (e.g., 0x0628 for Ba)
            mark_codepoint: The Unicode codepoint of the mark (e.g., 0x064E for Fatha)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with the result of applying ATOMIC_UNIT_BINDING rule
        """
        request = self.build_request_for_binding(carrier_codepoint, mark_codepoint, trace_prefix)
        return self.kernel.apply(request)

    def process_from_candidates(
        self,
        carrier: Candidate,
        mark: Candidate,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a binding between existing Candidate objects.

        This method is currently not implemented because it requires extracting
        and validating the actual codepoint values from the candidates' identity/evidence,
        which is not yet safely implemented. An accepted UnicodeCandidate does not
        necessarily mean it's an Arabic letter carrier, and an accepted HarakaCandidate
        does not necessarily mean it's suitable for atomic binding.

        Args:
            carrier: A UnicodeCandidate representing the carrier
            mark: A HarakaCandidate representing the mark
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with the result of applying ATOMIC_UNIT_BINDING rule

        Raises:
            NotImplementedError: This method is not yet safely implemented
        """
        raise NotImplementedError(
            "process_from_candidates is not yet implemented. "
            "Use process_binding(carrier_codepoint, mark_codepoint) instead, "
            "which properly validates both carrier and mark codepoints."
        )
