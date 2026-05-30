from dataclasses import dataclass
import uuid

from .candidate import CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.haraka_rules import HARAKA_ARABIC_DIACRITIC


# Arabic combining marks (diacritics/harakat) Unicode range
# U+064B to U+065F: Arabic combining marks
# Core harakat:
#   U+064B: Fathatan (double fatha/tanwin fath)
#   U+064C: Dammatan (double damma/tanwin damm)
#   U+064D: Kasratan (double kasra/tanwin kasr)
#   U+064E: Fatha (short vowel a)
#   U+064F: Damma (short vowel u)
#   U+0650: Kasra (short vowel i)
#   U+0651: Shadda (gemination/consonant doubling)
#   U+0652: Sukun (vowel absence marker)
#   U+0653-U+065F: Additional marks (maddah, hamza variants, etc.)
HARAKAT_RANGE = (0x064B, 0x065F)


def is_haraka_codepoint(codepoint: int) -> bool:
    """Check if a codepoint is an Arabic combining mark (haraka/diacritic)."""
    start, end = HARAKAT_RANGE
    return start <= codepoint <= end


@dataclass
class HarakaLayerAdapter:
    kernel: QiyasKernel

    def process_codepoint(self, codepoint: int, trace_prefix: str = "") -> CandidateSet:
        """
        Process a single Unicode codepoint through the Haraka layer.

        Args:
            codepoint: The Unicode codepoint value (e.g., 0x064E for Fatha)
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with the result of applying HARAKA_ARABIC_DIACRITIC rule
        """
        if not trace_prefix:
            trace_prefix = f"haraka:{codepoint:04x}"

        # Create asl node representing the Arabic diacritic domain
        asl = QiyasNodeRef(
            node_id="asl:arabic_diacritic_domain",
            node_type="ArabicDiacriticDomain",
            identity_ids=("identity:arabic_diacritic_domain",),
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

        # Build evidence based on whether codepoint is a haraka
        is_haraka = is_haraka_codepoint(codepoint)

        if is_haraka:
            # All checks pass for harakat codepoints
            proves = (
                "asl:established",
                "far:determined",
                "wasf:codepoint_is_arabic_combining_mark:evidenced",
                "illah:belongs_to_haraka_vocalization_domain:verified",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
            )
        else:
            # Non-haraka: establish asl, far, and all wadi conditions
            # The fariq (invalidating difference) will block, but wadi conditions are satisfied
            # This keeps blocking clean: only due to domain mismatch, not wadi failures
            proves = (
                "asl:established",
                "far:determined",
                "wadi:sabab:established",
                "wadi:shart:satisfied",
                "wadi:mani:absent",
                "wadi:sihha:valid",
                "wadi:fasad:absent",
                "wadi:butlan:absent",
                "fariq:non_haraka_codepoint:present",
            )

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:haraka:{codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="HarakaQiyas",
                    proves=proves,
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        # Build and apply request
        request = QiyasRequest(
            rule=HARAKA_ARABIC_DIACRITIC,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="HarakaQiyas"),
        )

        return self.kernel.apply(request)

    def process_text(self, text: str) -> list[CandidateSet]:
        """
        Process each character in text through the Haraka layer.

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
