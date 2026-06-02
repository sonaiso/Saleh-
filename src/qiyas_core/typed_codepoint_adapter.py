"""
TypedCodePoint classification adapter.

Z4 declassification note (PRE_QIYAS_TOKENIZER_CONSTITUTION §6):

    Whitespace and boundary characters are pre-qiyas sequence-framing
    markers handled by `SequenceContextTokenizer`. They must NOT enter
    `UnicodeQiyas` as `UnicodeCandidate` and therefore must NOT reach
    this layer in any canonical execution path.

    `UnicodeQiyas` already rejects U+0020, U+0009, U+000A, U+000D
    (outside ARABIC_RANGES), so `BOUNDARY_CODEPOINT_CLASSIFICATION` and
    the boundary branches below are **legacy unreachable** in the
    canonical path post-Z1/Z2. They survive only to keep legacy unit
    fixtures (which bypass `UnicodeQiyas` via
    `TypedCodePointLayerAdapter.classify_codepoint(int)`) and external
    re-exports stable until the Z5 wiring cleanup.

    Do not introduce new canonical callers of the boundary branch.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rule import QiyasRule
from .rules.typed_codepoint_rules import (
    LETTER_CODEPOINT_CLASSIFICATION,
    HARAKA_CODEPOINT_CLASSIFICATION,
    BOUNDARY_CODEPOINT_CLASSIFICATION,  # Z4: legacy unreachable in canonical path.
    PUNCTUATION_CODEPOINT_CLASSIFICATION,
    RESIDUAL_CODEPOINT_CLASSIFICATION,
)


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

# Z4 declassified — legacy testing-only fixture.
# Whitespace is handled by `SequenceContextTokenizer` (Z2). These
# codepoints are outside ARABIC_RANGES and therefore never accepted by
# `UnicodeQiyas`, so the constant is reachable only from test bypass
# helpers and from `run_qiyas._classify_position` (scheduled for Z5).
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
    """Z4 declassified — legacy testing-only predicate.

    Whitespace is detected by `SequenceContextTokenizer`, not by this
    layer. Retained because `run_qiyas._classify_position` (Z5 cleanup)
    still imports it.
    """
    return codepoint in BOUNDARY_CODEPOINTS


def is_punctuation(codepoint: int) -> bool:
    """Check if codepoint is Arabic punctuation."""
    return codepoint in PUNCTUATION_CODEPOINTS


def classify_codepoint(codepoint: int) -> tuple[str, str, str]:
    """
    Classify a codepoint into TypedCodePoint categories.

    Z4 note: the `is_boundary` branch is **legacy unreachable** in the
    canonical path. `UnicodeQiyas` rejects whitespace before this layer
    is reached. The branch survives only for the legacy testing
    convenience `TypedCodePointLayerAdapter.classify_codepoint(int)`
    which bypasses `UnicodeQiyas`.

    Returns:
        Tuple of (candidate_type, wasf, illah)
    """
    if is_arabic_letter(codepoint):
        return ("LetterCodePoint", "is_arabic_letter", "belongs_to_letter_class")
    elif is_arabic_haraka(codepoint):
        return ("HarakaCodePoint", "is_arabic_haraka", "belongs_to_haraka_class")
    elif is_boundary(codepoint):
        # Z4 legacy unreachable in canonical path; see module docstring.
        return ("BoundaryCodePoint", "is_whitespace_boundary", "belongs_to_boundary_class")
    elif is_punctuation(codepoint):
        return ("PunctuationCodePoint", "is_arabic_punctuation", "belongs_to_punctuation_class")
    else:
        return ("ResidualCodePoint", "is_unclassified_codepoint", "belongs_to_residual_class")


def select_rule_for_codepoint(codepoint: int) -> QiyasRule:
    """
    Select the appropriate classification rule based on codepoint type.

    Z4 note: the `is_boundary` branch returning
    `BOUNDARY_CODEPOINT_CLASSIFICATION` is **legacy unreachable** in the
    canonical path. See module docstring.

    Args:
        codepoint: The Unicode codepoint value

    Returns:
        The canonical QiyasRule for this codepoint type
    """
    if is_arabic_letter(codepoint):
        return LETTER_CODEPOINT_CLASSIFICATION
    elif is_arabic_haraka(codepoint):
        return HARAKA_CODEPOINT_CLASSIFICATION
    elif is_boundary(codepoint):
        # Z4 legacy unreachable in canonical path; see module docstring.
        return BOUNDARY_CODEPOINT_CLASSIFICATION
    elif is_punctuation(codepoint):
        return PUNCTUATION_CODEPOINT_CLASSIFICATION
    else:
        return RESIDUAL_CODEPOINT_CLASSIFICATION


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
            node_id="اصل:typed_codepoint_classification_domain",
            node_type="TypedCodePointClassificationDomain",
            identity_ids=("identity:typed_codepoint_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node from unicode_candidate (preserving its identity)
        far = QiyasNodeRef(
            node_id=f"فرع:unicode_candidate:{codepoint:04x}",
            node_type="UnicodeCandidate",
            identity_ids=unicode_candidate.identity_ids,  # Preserve identity!
            trace_ids=(f"{trace_prefix}:far",),
            rank=unicode_candidate.rank,
        )

        # Classify the codepoint and select the appropriate canonical rule
        candidate_type, wasf, illah = classify_codepoint(codepoint)
        selected_rule = select_rule_for_codepoint(codepoint)

        # Build evidence with both generic and type-specific wasf/illah
        proves = [
            "اصل:established",
            "فرع:determined",
            f"وصف:is_classifiable_codepoint:evidenced",  # Generic wasf
            f"وصف:{wasf}:evidenced",  # Type-specific wasf
            f"علة:belongs_to_typed_domain:verified",  # Generic illah
            f"علة:{illah}:verified",  # Type-specific illah
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:typed:{codepoint:04x}:{uuid.uuid4().hex[:8]}",
                    source_layer="TypedCodePointClassificationQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        # Build request with the selected canonical rule
        return QiyasRequest(
            rule=selected_rule,
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

        **WARNING: This is a testing/convenience method only.**

        **NOT FOR PRODUCTION USE.** This method bypasses the constitutional
        production path (UnicodeLayerAdapter.process_codepoint →
        TypedCodePointLayerAdapter.classify_unicode_candidate). It creates
        a synthetic UnicodeCandidate that has not passed through proper
        Arabic Unicode membership verification.

        For production code, use the full layer stack:
        1. UnicodeLayerAdapter.process_codepoint() → accepted UnicodeCandidate
        2. TypedCodePointLayerAdapter.classify_unicode_candidate() → TypedCodePoint

        This method is provided for:
        - Unit tests that need quick classification without full layer setup
        - Interactive debugging/exploration
        - Documentation examples

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
            asl_id="اصل:arabic_unicode_block",
            far_id=f"فرع:{codepoint:04x}",
            identity_ids=(f"identity:codepoint:{codepoint:04x}",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
            residuals=(),
            trace_ids=(f"test:unicode:{codepoint:04x}",),
            output_flags=frozenset(),
        )

        return self.classify_unicode_candidate(unicode_candidate, trace_prefix)
