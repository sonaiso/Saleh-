from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.unicode_rules import UNICODE_ARABIC_MEMBERSHIP


# Arabic Unicode ranges (main blocks)
# 0600-06FF: Arabic
# 0750-077F: Arabic Supplement
# 08A0-08FF: Arabic Extended-A
# FB50-FDFF: Arabic Presentation Forms-A
# FE70-FEFF: Arabic Presentation Forms-B
ARABIC_RANGES = [
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
]


def is_arabic_codepoint(codepoint: int) -> bool:
    """Check if a codepoint is in Arabic Unicode ranges."""
    return any(start <= codepoint <= end for start, end in ARABIC_RANGES)


@dataclass
class UnicodeLayerAdapter:
    kernel: QiyasKernel

    def process_codepoint(self, codepoint: int, trace_prefix: str = "") -> CandidateSet:
        """
        Process a single Unicode codepoint through the Unicode layer.

        Args:
            codepoint: The Unicode codepoint value (e.g., 0x0628 for Arabic letter Ba)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with the result of applying UNICODE_ARABIC_MEMBERSHIP rule
        """
        if not trace_prefix:
            trace_prefix = f"unicode:{codepoint:04x}"

        # Create asl node representing the Arabic Unicode block
        asl = QiyasNodeRef(
            node_id="asl:arabic_unicode_block",
            node_type="ArabicUnicodeBlock",
            identity_ids=("identity:arabic_unicode_block",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node representing the input codepoint
        far = QiyasNodeRef(
            node_id=f"far:{codepoint:04x}",
            node_type="InputCodepoint",
            identity_ids=(f"identity:codepoint:{codepoint:04x}",),
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORM,
        )

        # Build evidence based on whether codepoint is Arabic
        is_arabic = is_arabic_codepoint(codepoint)

        if is_arabic:
            # All checks pass for Arabic codepoints
            proves = (
                "asl:established",
                "far:determined",
                "wasf:unicode_codepoint_in_arabic_range:evidenced",
                "illah:belongs_to_arabic_script_domain:verified",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            )
        else:
            # Non-Arabic: still establish asl and far, but fail on Arabic-specific checks
            # This will trigger a fariq (invalidating difference)
            proves = (
                "asl:established",
                "far:determined",
                "fariq:non_arabic_codepoint:present",
            )

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:unicode:{codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="UnicodeQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        # Build and apply request
        request = QiyasRequest(
            rule=UNICODE_ARABIC_MEMBERSHIP,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="UnicodeQiyas"),
        )

        return self.kernel.apply(request)

    def process_text(self, text: str) -> list[CandidateSet]:
        """
        Process each character in text through the Unicode layer.

        Args:
            text: Input text string

        Returns:
            List of CandidateSet, one for each character in the text
        """
        results = []
        for char in text:
            codepoint = ord(char)
            result = self.process_codepoint(codepoint, trace_prefix=f"text:{codepoint:04x}")
            results.append(result)
        return results
