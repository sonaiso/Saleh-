"""
Arabic Letter Coordinate Adapter (Layer 2)

Option C Architecture - Layer 2: ArabicLetterCoordinateCarrier

Enriches LetterIdentityCarrier with coordinate data:
  - Phonetic proxy (sound_identity)
  - Makhraj (articulation place)
  - Sifat (phonetic features)
  - Abjad numeric values
  - Invalidating differences (fariq)
  - Morphological role potential bits (سألتمونيها classification)

Path: LetterIdentityCarrier → ArabicLetterCoordinateCarrier

Constitutional Compliance:
  - Uses kernel.apply() not execute_qiyas()
  - Uses Evidence with proves tuple not claims
  - Uses QiyasNodeRef with identity_ids, trace_ids, rank
  - Preserves identity_ids through transformation
  - Proves invalidating_differences absence in evidence
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .abjad_system import get_abjad_coordinate
from .phonetics import get_phonetic_profile


@dataclass
class ArabicLetterCoordinateAdapter:
    """
    Adapter for ArabicLetterCoordinateQiyas layer (Layer 2).

    Enriches LetterIdentityCarrier with coordinates:
      - Phonetic proxy
      - Makhraj geometry
      - Sifat geometry
      - Abjad numeric
      - Fariq (invalidating differences)
      - Morphological role bits

    Constitutional path:
        LetterIdentityCarrier → [ArabicLetterCoordinateAdapter] → ArabicLetterCoordinateCarrier
    """

    kernel: QiyasKernel

    def build_request_for_letter_coordinates(
        self,
        letter_identity: Candidate,
        trace_prefix: str = ""
    ) -> QiyasRequest | None:
        """
        Build a QiyasRequest for enriching letter identity with coordinates.

        Args:
            letter_identity: Must be LetterIdentityCarrier from LetterIdentityLayerAdapter
            trace_prefix: Optional prefix for trace IDs

        Returns:
            QiyasRequest or None if coordinate enrichment not supported
        """
        # Validate input type
        if letter_identity.candidate_type != "LetterIdentityCarrier":
            return None

        # Extract codepoint from identity_ids
        codepoint = None
        for identity_id in letter_identity.identity_ids:
            if identity_id.startswith("identity:codepoint:"):
                codepoint_hex = identity_id.split(":")[-1]
                codepoint = int(codepoint_hex, 16)
                break

        if codepoint is None:
            return None

        # Get phonetic profile (makhraj, sifat, fariq)
        phonetic_profile = get_phonetic_profile(codepoint)
        if phonetic_profile is None:
            # Letter not yet mapped with phonetic profile
            return None

        # Get Abjad coordinate (conventional numeric value)
        abjad_coord = get_abjad_coordinate(codepoint)
        # Note: abjad_coord may be None for letters not in Abjad system (e.g., Hamza)

        # Extract letter name from letter_identity source_rule_id
        # e.g., "letter_identity.baa" → "baa"
        letter_name = None
        if letter_identity.source_rule_id:
            parts = letter_identity.source_rule_id.split(".")
            if len(parts) == 2 and parts[0] == "letter_identity":
                letter_name = parts[1]

        if not letter_name:
            return None

        if not trace_prefix:
            trace_prefix = f"letter_coordinate:{letter_name}"

        # TODO: Build evidence for coordinate enrichment
        # TODO: Build asl node (letter coordinate domain)
        # TODO: Build far node from letter_identity (preserving identity)
        # TODO: Get coordinate rule
        # TODO: Build and return request

        return None  # Placeholder

    def process_letter_identity(
        self,
        letter_identity: Candidate,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a LetterIdentityCarrier to enrich with coordinates.

        Args:
            letter_identity: Must be LetterIdentityCarrier with full evidence/rank/trace
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with ArabicLetterCoordinateCarrier (if supported)
        """
        request = self.build_request_for_letter_coordinates(letter_identity, trace_prefix)

        if request is None:
            # Coordinate enrichment not supported yet - return empty
            return CandidateSet(
                set_id=f"letter_coordinate:empty:{uuid.uuid4().hex[:8]}",
                layer="ArabicLetterCoordinateQiyas",
                candidates=(),
                residuals=(),
                trace_ids=(),
            )

        # Execute qiyas through kernel.apply() (canonical interface)
        return self.kernel.apply(request)
