from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rule import QiyasRule
from .rules.typed_codepoint_rules import TYPED_CODEPOINT_CLASSIFICATION


# Arabic letter range (main consonants and long vowels)
# U+0621 (Hamza) to U+064A (Ya)
ARABIC_LETTER_RANGE = (0x0621, 0x064A)

# Arabic harakat (diacritics) ranges
# Core harakat: U+064B-U+0650 (tanwin + short vowels)
# Shadda: U+0651
# Sukun: U+0652
# Additional: U+0653-U+065F
HARAKA_RANGES = [
    (0x064B, 0x0652),  # Core harakat including shadda and sukun
    (0x0653, 0x065F),  # Additional Arabic diacritics
]

# Whitespace/boundary codepoints
BOUNDARY_CODEPOINTS = {
    0x0020,  # Space
    0x000A,  # Line Feed
    0x000D,  # Carriage Return
    0x0009,  # Tab
}

# Arabic punctuation
PUNCTUATION_CODEPOINTS = {
    0x060C,  # Arabic Comma
    0x061B,  # Arabic Semicolon
    0x061F,  # Arabic Question Mark
    0x06D4,  # Arabic Full Stop
}


def is_arabic_letter(codepoint: int) -> bool:
    """Check if codepoint is an Arabic letter."""
    return ARABIC_LETTER_RANGE[0] <= codepoint <= ARABIC_LETTER_RANGE[1]


def is_arabic_haraka(codepoint: int) -> bool:
    """Check if codepoint is an Arabic haraka (diacritic)."""
    return any(start <= codepoint <= end for start, end in HARAKA_RANGES)


def is_boundary(codepoint: int) -> bool:
    """Check if codepoint is a whitespace/boundary character."""
    return codepoint in BOUNDARY_CODEPOINTS


def is_punctuation(codepoint: int) -> bool:
    """Check if codepoint is Arabic punctuation."""
    return codepoint in PUNCTUATION_CODEPOINTS


def classify_codepoint(codepoint: int) -> tuple[str, str, str]:
    """
    Classify a codepoint into TypedCodePoint categories.

    Returns:
        Tuple of (candidate_type, wasf, illah)
    """
    if is_arabic_letter(codepoint):
        return ("LetterCodePoint", "is_arabic_letter", "belongs_to_letter_class")
    elif is_arabic_haraka(codepoint):
        return ("HarakaCodePoint", "is_arabic_haraka", "belongs_to_haraka_class")
    elif is_boundary(codepoint):
        return ("BoundaryCodePoint", "is_whitespace_boundary", "belongs_to_boundary_class")
    elif is_punctuation(codepoint):
        return ("PunctuationCodePoint", "is_arabic_punctuation", "belongs_to_punctuation_class")
    else:
        return ("ResidualCodePoint", "is_unclassified_codepoint", "belongs_to_residual_class")


@dataclass
class TypedCodePointLayerAdapter:
    kernel: QiyasKernel

    def build_request_for_classification(
        self,
        unicode_candidate: Candidate,
        trace_prefix: str = ""
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for classifying a UnicodeCandidate.

        Args:
            unicode_candidate: The UnicodeCandidate from UnicodeLayerAdapter
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest for TypedCodePoint classification
        """
        # Extract codepoint from unicode_candidate identity
        codepoint_identity = None
        for identity_id in unicode_candidate.identity_ids:
            if identity_id.startswith("identity:codepoint:"):
                codepoint_hex = identity_id.split(":")[-1]
                codepoint = int(codepoint_hex, 16)
                codepoint_identity = identity_id
                break

        if codepoint_identity is None:
            raise ValueError("UnicodeCandidate must have identity:codepoint:{hex} identity")

        if not trace_prefix:
            trace_prefix = f"typed:{codepoint:04x}"

        # Create asl node representing the classification domain
        asl = QiyasNodeRef(
            node_id="asl:typed_codepoint_classification_domain",
            node_type="TypedCodePointClassificationDomain",
            identity_ids=("identity:typed_codepoint_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node from unicode_candidate (preserving its identity)
        far = QiyasNodeRef(
            node_id=f"far:unicode_candidate:{codepoint:04x}",
            node_type="UnicodeCandidate",
            identity_ids=unicode_candidate.identity_ids,  # Preserve identity!
            trace_ids=(f"{trace_prefix}:far",),
            rank=unicode_candidate.rank,
        )

        # Classify the codepoint
        candidate_type, wasf, illah = classify_codepoint(codepoint)

        # Build evidence
        proves = [
            "asl:established",
            "far:determined",
            f"wasf:is_classifiable_codepoint:evidenced",
            f"illah:belongs_to_typed_domain:verified",
            "wadi:sabab:established",
            "wadi:shart:satisfied",
            "wadi:mani:absent",
            "wadi:sihha:valid",
            "wadi:fasad:absent",
            "wadi:butlan:absent",
        ]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:typed:{codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="TypedCodePointClassificationQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        # Build request with custom output candidate type
        request = QiyasRequest(
            rule=TYPED_CODEPOINT_CLASSIFICATION,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="TypedCodePointClassificationQiyas"),
        )

        # Override the output candidate type based on classification
        # This is done by modifying the rule temporarily for this request
        classified_rule = QiyasRule(
            rule_id=TYPED_CODEPOINT_CLASSIFICATION.rule_id,
            layer=TYPED_CODEPOINT_CLASSIFICATION.layer,
            pattern=TYPED_CODEPOINT_CLASSIFICATION.pattern,
            asl_type=TYPED_CODEPOINT_CLASSIFICATION.asl_type,
            far_type=TYPED_CODEPOINT_CLASSIFICATION.far_type,
            required_effective_wasf=TYPED_CODEPOINT_CLASSIFICATION.required_effective_wasf,
            required_illah=TYPED_CODEPOINT_CLASSIFICATION.required_illah,
            required_wadi_gates=TYPED_CODEPOINT_CLASSIFICATION.required_wadi_gates,
            invalidating_differences=TYPED_CODEPOINT_CLASSIFICATION.invalidating_differences,
            neutral_identity_domain=TYPED_CODEPOINT_CLASSIFICATION.neutral_identity_domain,
            output_candidate_type=candidate_type,  # Dynamic based on classification
            forbidden_outputs=TYPED_CODEPOINT_CLASSIFICATION.forbidden_outputs,
            rank_ceiling=TYPED_CODEPOINT_CLASSIFICATION.rank_ceiling,
        )

        return QiyasRequest(
            rule=classified_rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="TypedCodePointClassificationQiyas"),
        )

    def classify_unicode_candidate(
        self,
        unicode_candidate: Candidate,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Classify a UnicodeCandidate into TypedCodePoint.

        Args:
            unicode_candidate: The UnicodeCandidate to classify
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with TypedCodePoint classification
        """
        request = self.build_request_for_classification(unicode_candidate, trace_prefix)
        return self.kernel.apply(request)

    def classify_codepoint(self, codepoint: int, trace_prefix: str = "") -> CandidateSet:
        """
        Classify a raw codepoint by creating a minimal UnicodeCandidate first.

        This is a convenience method for testing.

        Args:
            codepoint: The Unicode codepoint value
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with TypedCodePoint classification
        """
        from .candidate import Candidate
        from .enums import CandidateStatus

        # Create a minimal UnicodeCandidate
        unicode_candidate = Candidate(
            candidate_id=f"unicode:{codepoint:04x}",
            candidate_type="UnicodeCandidate",
            status=CandidateStatus.ACCEPTED,
            layer="UnicodeQiyas",
            source_rule_id="unicode.arabic.membership",
            asl_id="asl:arabic_unicode_block",
            far_id=f"far:{codepoint:04x}",
            identity_ids=(f"identity:codepoint:{codepoint:04x}",),
            rank=EvidenceRank.FORM,
            residuals=(),
            trace_ids=(f"test:unicode:{codepoint:04x}",),
            output_flags=frozenset(),
        )

        return self.classify_unicode_candidate(unicode_candidate, trace_prefix)
