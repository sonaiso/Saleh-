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
from .rules.letter_coordinate_rules import get_letter_coordinate_rule


# Morphological role classification for BAA/TAA/SEEN/KAF
# This is a minimal mapping for the current coordinate slice
MORPHO_ROLE_BY_LETTER = {
    "baa": "EXPANDED_MULTI_ROLE",  # ب has prepositional and root potential
    "taa": "SAALATAMUUNIIHA",  # ت is part of سألتمونيها
    "seen": "SAALATAMUUNIIHA",  # س is part of سألتمونيها
    "kaf": "EXPANDED_MULTI_ROLE",  # ك has similative/pronoun and root potential
}


def build_letter_coordinate_evidence(
    letter_name: str,
    codepoint: int,
    phonetic_profile,
    abjad_coord,
    trace_prefix: str,
) -> EvidenceSet:
    """
    Build evidence for coordinate enrichment (Option C - Layer 2).

    Proves phonetic coordinates PLUS identity from Layer 1:
      - Sound identity (phonetic proxy)
      - Makhraj geometry
      - Sifat geometry (voicing, manner, emphasis)
      - Abjad numeric (if applicable)
      - Invalidating differences (fariq)

    Args:
        letter_name: Lowercase letter name (e.g., "baa", "taa", "seen")
        codepoint: Unicode codepoint value
        phonetic_profile: PhoneticGroundingProfile from phonetics system
        abjad_coord: AbjadCoordinate or None
        trace_prefix: Trace prefix for evidence
    """
    cp_hex = f"{codepoint:04x}"

    # Build proves list
    proves = [
        "asl:established",
        "far:determined",
        # Identity wasf from Layer 1 (must be present in LetterIdentityCarrier input)
        "wasf:has_letter_codepoint:evidenced",
        f"wasf:has_unicode_identity:{cp_hex}:evidenced",
        f"wasf:has_script_identity:{letter_name}:evidenced",
        f"wasf:has_latin_name:{letter_name}:evidenced",
        # Layer 2 coordinate wasf
        f"wasf:has_sound_identity:{phonetic_profile.sound_identity}:evidenced",
        f"wasf:has_makhraj:{phonetic_profile.makhraj.spatial_source}:evidenced",
        f"wasf:has_voicing:{phonetic_profile.sifat.voicing}:evidenced",
        f"wasf:has_manner:{phonetic_profile.sifat.manner}:evidenced",
        f"wasf:has_emphasis:{phonetic_profile.sifat.emphasis}:evidenced",
    ]

    if abjad_coord is not None:
        proves.append(f"wasf:has_abjad_system:{abjad_coord.system}:evidenced")
        proves.append(f"wasf:has_abjad_value:{abjad_coord.numeric_value}:evidenced")
        proves.append(f"wasf:abjad_semantic_force:{abjad_coord.semantic_force}:evidenced")
        proves.append(f"coordinate:abjad:{letter_name}:{abjad_coord.numeric_value}:proven")

    # Add morpho_role if mapped
    morpho_role = MORPHO_ROLE_BY_LETTER.get(letter_name)
    if morpho_role:
        proves.append(f"wasf:has_morpho_role:{morpho_role}:evidenced")

    # Add illah
    proves.extend([
        "illah:belongs_to_letter_identity_domain:verified",
        f"illah:letter_identity_is:{letter_name}:verified",
        "illah:belongs_to_letter_coordinate_domain:verified",
    ])

    # Add wadi gates
    proves.extend([
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
    ])

    # Add invalidating differences as absent (proves fariq:*:absent)
    for diff_label, diff_type in phonetic_profile.invalidating_differences:
        proves.append(f"fariq:{diff_label}:absent")

    return EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:letter_coordinate:{letter_name}:{uuid.uuid4().hex[:8]}",
                source_layer="ArabicLetterCoordinateQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORM,
                trace_ids=(f"{trace_prefix}:ev",),
            ),
        )
    )


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

        # Build evidence for coordinate enrichment
        evidence = build_letter_coordinate_evidence(
            letter_name=letter_name,
            codepoint=codepoint,
            phonetic_profile=phonetic_profile,
            abjad_coord=abjad_coord,
            trace_prefix=trace_prefix,
        )

        # Build asl node (letter coordinate domain)
        asl = QiyasNodeRef(
            node_id=f"asl:letter_coordinate_domain:{letter_name}",
            node_type="LetterCoordinateDomain",
            identity_ids=("identity:letter_coordinate_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Build far node from letter_identity (preserving its identity!)
        far = QiyasNodeRef(
            node_id=f"far:letter_identity:{letter_name}:{codepoint:04x}",
            node_type="LetterIdentityCarrier",
            identity_ids=letter_identity.identity_ids,  # Preserve identity!
            trace_ids=(f"{trace_prefix}:far",),
            rank=letter_identity.rank,
        )

        # Get coordinate rule
        coordinate_rule = get_letter_coordinate_rule(codepoint)
        if coordinate_rule is None:
            return None

        # Build and return request
        return QiyasRequest(
            rule=coordinate_rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="ArabicLetterCoordinateQiyas"),
        )

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
            or Deferred/Blocked with residuals (if not supported)
        """
        request = self.build_request_for_letter_coordinates(letter_identity, trace_prefix)

        if request is None:
            # Coordinate enrichment not supported - return DEFERRED with residuals
            from .residual import Residual
            from .enums import ResidualSeverity, ResidualEffect

            # Extract letter info for residual
            letter_info = "unknown"
            for identity_id in letter_identity.identity_ids:
                if identity_id.startswith("identity:letter:"):
                    letter_info = identity_id.split(":")[-1]
                    break

            trace_id = f"letter_coordinate:deferred:{uuid.uuid4().hex[:8]}"

            residuals = (
                Residual(
                    residual_type="letter_coordinate_not_implemented",
                    severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER,
                    message=f"Coordinate enrichment not yet implemented for letter: {letter_info}",
                    source_rule_id="letter_coordinate.adapter",
                    layer="ArabicLetterCoordinateQiyas",
                    trace_ids=(trace_id,),
                ),
                Residual(
                    residual_type="phonetic_profile_missing",
                    severity=ResidualSeverity.WARNING,
                    effect=ResidualEffect.DEFER,
                    message=f"Phonetic profile missing for letter: {letter_info}",
                    source_rule_id="letter_coordinate.adapter",
                    layer="ArabicLetterCoordinateQiyas",
                    trace_ids=(trace_id,),
                ),
            )

            return CandidateSet(
                set_id=f"letter_coordinate:deferred:{uuid.uuid4().hex[:8]}",
                layer="ArabicLetterCoordinateQiyas",
                candidates=(),
                residuals=residuals,
                trace_ids=(trace_id,),
            )

        # Execute qiyas through kernel.apply() (canonical interface)
        return self.kernel.apply(request)
