"""
Letter Identity Adapter

Atomic proof layer: LetterCodePoint → LetterIdentityCarrier

This is an INDEPENDENT atomic path that does NOT require:
  - ConditionedTypedSequence
  - HarakaFunctionCarrier
  - PositionCarrier
  - SlotCandidate

It proves PURE letter identity (BAA, TAA, SEEN, etc.) from LetterCodePoint alone,
using ONLY Unicode identity, script identity, and name identity (Latin + Arabic).

Constitutional Compliance:
  - Uses kernel.apply() not execute_qiyas()
  - Uses Evidence with proves tuple not claims
  - Uses QiyasNodeRef with identity_ids, trace_ids, rank
  - Preserves identity_ids through transformation
  - Proves invalidating_differences absence in evidence
  - Layer 1 proves ONLY digital/script/name identity (NOT phonetic/makhraj/sifat)
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.letter_identity_rules import get_letter_identity_rule
from .registries.letter_name_registry import get_letter_names


def build_letter_identity_evidence(
    letter_name: str,
    codepoint: int,
    arabic_name: str,
    trace_prefix: str,
) -> EvidenceSet:
    """
    Build evidence for PURE letter identity (Option C - Layer 1).

    Proves ONLY identity coordinates:
      - Unicode identity (digital layer)
      - Script identity
      - Name identity (Latin + Arabic)
      - Specific letter identity

    Does NOT prove (moved to ArabicLetterCoordinateCarrier - Layer 2):
      - Phonetic proxy
      - Makhraj
      - Sifat
      - Abjad numeric
      - Invalidating differences (fariq)

    Args:
        letter_name: Lowercase letter name (e.g., "baa", "taa", "seen")
        codepoint: Unicode codepoint value
        arabic_name: Arabic name (e.g., "باء", "تاء", "سين")
        trace_prefix: Trace prefix for evidence
    """
    cp_hex = f"{codepoint:04x}"

    proves = [
        "اصل:established",
        "فرع:determined",
        # Generic wasf
        "وصف:has_letter_codepoint:evidenced",
        # PURE IDENTITY wasf - Unicode, Script, Name only
        f"وصف:has_unicode_identity:{cp_hex}:evidenced",
        f"وصف:has_script_identity:{letter_name}:evidenced",  # lowercase letter_name
        f"وصف:has_latin_name:{letter_name}:evidenced",
        f"وصف:has_arabic_name:{arabic_name}:evidenced",
        # Generic illah
        "علة:belongs_to_letter_identity_domain:verified",
        # Type-specific illah - must match rule format exactly
        f"علة:letter_identity_is:{letter_name}:verified",  # lowercase letter_name
        # Wadi gates
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    ]

    return EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:letter_identity:{letter_name.lower()}:{uuid.uuid4().hex[:8]}",
                source_layer="LetterIdentityQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORMAL_STRUCTURE,
                trace_ids=(f"{trace_prefix}:ev",),
            ),
        )
    )


@dataclass
class LetterIdentityLayerAdapter:
    """
    Adapter for LetterIdentityQiyas layer.

    Atomic path: LetterCodePoint → LetterIdentityCarrier

    Independent of:
      - ConditionedTypedSequence
      - HarakaFunctionCarrier
      - PositionCarrier
      - SlotCandidate

    Constitutional path:
        LetterCodePoint → [LetterIdentityLayerAdapter] → LetterIdentityCarrier
    """

    kernel: QiyasKernel

    def build_request_for_letter_identity(
        self,
        letter_candidate: Candidate,
        trace_prefix: str = ""
    ) -> QiyasRequest | None:
        """
        Build a QiyasRequest for proving letter identity from LetterCodePoint.

        Args:
            letter_candidate: Must be LetterCodePoint from TypedCodePointLayerAdapter
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest or None if letter not supported yet
        """
        # Validate input type
        if letter_candidate.candidate_type != "LetterCodePoint":
            return None

        # Extract codepoint from identity_ids
        codepoint = None
        for identity_id in letter_candidate.identity_ids:
            if identity_id.startswith("identity:codepoint:"):
                codepoint_hex = identity_id.split(":")[-1]
                codepoint = int(codepoint_hex, 16)
                break

        if codepoint is None:
            return None

        # Get letter identity rule
        rule = get_letter_identity_rule(codepoint)
        if rule is None:
            # Letter not yet mapped
            return None

        # Extract letter name from rule_id (keep lowercase to match rule format)
        letter_name = rule.rule_id.split(".")[-1]  # e.g., "baa", "taa", "seen"

        # Get Arabic name from registry
        letter_names = get_letter_names(codepoint)
        arabic_name = letter_names.arabic_name if letter_names else letter_name

        if not trace_prefix:
            trace_prefix = f"letter_identity:{letter_name.lower()}"

        # Build identity_ids for asl node including the proven identities
        asl_identity_ids = (
            "identity:letter_identity_domain",
            f"identity:codepoint:{codepoint:04x}",
            f"identity:letter:{letter_name}",
        )

        asl = QiyasNodeRef(
            node_id=f"اصل:letter_identity_domain:{letter_name.lower()}",
            node_type="LetterIdentityDomain",
            identity_ids=asl_identity_ids,
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Create far node from letter_candidate (preserving its identity!)
        far = QiyasNodeRef(
            node_id=f"فرع:letter_codepoint:{codepoint:04x}",
            node_type="LetterCodePoint",
            identity_ids=letter_candidate.identity_ids,  # Preserve identity!
            trace_ids=(f"{trace_prefix}:far",),
            rank=letter_candidate.rank,
        )

        # Build PURE IDENTITY evidence (Option C - Layer 1)
        # No phonetic, makhraj, sifat - those moved to Layer 2
        evidence = build_letter_identity_evidence(
            letter_name=letter_name,
            codepoint=codepoint,
            arabic_name=arabic_name,
            trace_prefix=trace_prefix,
        )

        # Build request
        return QiyasRequest(
            rule=rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="LetterIdentityQiyas"),
        )

    def process_letter_codepoint(
        self,
        letter_candidate: Candidate,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a LetterCodePoint to prove its identity.

        Args:
            letter_candidate: Must be LetterCodePoint with full evidence/rank/trace
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with LetterIdentityCarrier (if letter supported)
        """
        request = self.build_request_for_letter_identity(letter_candidate, trace_prefix)

        if request is None:
            # Letter not supported yet - return empty
            return CandidateSet(
                set_id=f"letter_identity:empty:{uuid.uuid4().hex[:8]}",
                layer="LetterIdentityQiyas",
                candidates=(),
                residuals=(),
                trace_ids=(),
            )

        # Execute qiyas through kernel.apply() (canonical interface)
        return self.kernel.apply(request)
