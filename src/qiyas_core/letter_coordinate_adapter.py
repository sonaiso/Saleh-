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
from .enums import CandidateStatus, EvidenceRank, ResidualSeverity, ResidualEffect
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .residual import Residual
from .abjad_system import get_abjad_coordinate
from .phonetics import get_phonetic_profile
from .rules.letter_coordinate_rules import get_letter_coordinate_rule
from .registries.letter_name_registry import get_letter_names
from .registries.letter_role_registry import get_morpho_role_label
from .registries.letter_fariq_registry import get_fariq_pairs


def build_letter_coordinate_evidence(
    letter_name: str,
    codepoint: int,
    arabic_name: str,
    trace_prefix: str,
) -> EvidenceSet:
    """
    Build evidence for Layer 2 coordinate enrichment.

    Proves BOTH Layer 1 identity AND Layer 2 coordinates:
      Layer 1 (inherited):
        - Unicode identity
        - Script identity
        - Latin name
        - Arabic name
      Layer 2 (coordinate):
        - Phonetic proxy (sound_identity)
        - Makhraj (articulation place)
        - Sifat (voicing, manner, emphasis)
        - Abjad numeric value (if applicable) with semantic_force:FORBIDDEN
        - Morphological role potential (if applicable)
        - Invalidating differences (fariq) absence

    Args:
        letter_name: Lowercase letter name (e.g., "baa", "taa", "seen")
        codepoint: Unicode codepoint value
        arabic_name: Arabic name (e.g., "باء", "تاء", "سين")
        trace_prefix: Trace prefix for evidence
    """
    phonetic = get_phonetic_profile(codepoint)
    if phonetic is None:
        return EvidenceSet(items=())

    cp_hex = f"{codepoint:04x}"

    proves = [
        "اصل:established",
        "فرع:determined",
        # Layer 1 identity wasf (MUST be inherited for Layer 2 rule requirements)
        "وصف:has_letter_codepoint:evidenced",
        f"وصف:has_unicode_identity:{cp_hex}:evidenced",
        f"وصف:has_script_identity:{letter_name}:evidenced",
        f"وصف:has_latin_name:{letter_name}:evidenced",
        f"وصف:has_arabic_name:{arabic_name}:evidenced",
        # Layer 2 coordinate wasf - Phonetic
        f"وصف:has_sound_identity:{phonetic.sound_identity}:evidenced",
        f"وصف:has_makhraj:{phonetic.makhraj.spatial_source}:evidenced",
        f"وصف:has_voicing:{phonetic.sifat.voicing}:evidenced",
        f"وصف:has_manner:{phonetic.sifat.manner}:evidenced",
        f"وصف:has_emphasis:{phonetic.sifat.emphasis}:evidenced",
    ]

    # Abjad coordinate (if applicable) with semantic_force:FORBIDDEN
    abjad_coord = get_abjad_coordinate(codepoint)
    if abjad_coord:
        proves.extend([
            f"وصف:has_abjad_system:{abjad_coord.system}:evidenced",
            f"وصف:has_abjad_value:{abjad_coord.numeric_value}:evidenced",
            f"وصف:abjad_semantic_force:{abjad_coord.semantic_force}:evidenced",
        ])

    # Morphological role (if applicable)
    # Use letter_role_registry instead of local dict
    morpho_role = get_morpho_role_label(letter_name)
    if morpho_role and morpho_role != "SINGLE_ROLE":
        # Only add evidence for multi-role letters (not default single-role)
        proves.append(f"وصف:has_morpho_role:{morpho_role}:evidenced")

    # Illah
    proves.extend([
        "علة:belongs_to_letter_identity_domain:verified",
        f"علة:letter_identity_is:{letter_name}:verified",
        "علة:belongs_to_letter_coordinate_domain:verified",
    ])

    # Wadi gates
    proves.extend([
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    ])

    # Fariq (invalidating differences) - prove absence
    # NOTE: Kernel only checks for فارق:...:present (blocking).
    # Proving :absent is NOT consumed by kernel, but we document non-blocking here.
    # Derive from letter_fariq_registry (single source of truth)
    fariq_pairs = get_fariq_pairs(codepoint)
    for pair in fariq_pairs:
        pair_label = f"{pair.letter1_name}_vs_{pair.letter2_name}"
        proves.append(f"فارق:{pair_label}:absent")

    return EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:letter_coordinate:{letter_name}:{uuid.uuid4().hex[:8]}",
                source_layer="ArabicLetterCoordinateQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORMAL_STRUCTURE,
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

        # Get coordinate rule
        rule = get_letter_coordinate_rule(codepoint)
        if rule is None:
            # Coordinate rule not yet defined
            return None

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

        # Get Arabic name from registry
        letter_names = get_letter_names(codepoint)
        arabic_name = letter_names.arabic_name if letter_names else letter_name

        # Build evidence for coordinate enrichment
        evidence = build_letter_coordinate_evidence(
            letter_name=letter_name,
            codepoint=codepoint,
            arabic_name=arabic_name,
            trace_prefix=trace_prefix,
        )

        if not evidence.items:
            return None

        # Build asl node (letter coordinate domain)
        asl = QiyasNodeRef(
            node_id=f"asl:letter_coordinate_domain:{letter_name}",
            node_type="LetterCoordinateDomain",
            identity_ids=("identity:letter_coordinate_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Build far node from letter_identity (preserving identity!)
        far = QiyasNodeRef(
            node_id=f"far:letter_identity:{letter_name}",
            node_type="LetterIdentityCarrier",
            identity_ids=letter_identity.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=letter_identity.rank,
        )

        # Build and return request
        return QiyasRequest(
            rule=rule,
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
        """
        request = self.build_request_for_letter_coordinates(letter_identity, trace_prefix)

        if request is None:
            # Coordinate enrichment not supported yet - return CandidateSet with residual
            # Extract codepoint for residual message
            codepoint_hex = "unknown"
            for identity_id in letter_identity.identity_ids:
                if identity_id.startswith("identity:codepoint:"):
                    codepoint_hex = identity_id.split(":")[-1]
                    break

            residual = Residual(
                residual_type="coordinate_enrichment_not_supported",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.DEFER,
                message=f"Coordinate enrichment not yet supported for letter U+{codepoint_hex}",
                source_rule_id="letter_coordinate.unsupported",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"letter_coordinate:{codepoint_hex}:unsupported",),
            )

            return CandidateSet(
                set_id=f"letter_coordinate:unsupported:{uuid.uuid4().hex[:8]}",
                layer="ArabicLetterCoordinateQiyas",
                candidates=(),
                residuals=(residual,),
                trace_ids=(f"letter_coordinate:{codepoint_hex}:deferred",),
            )

        # Execute qiyas through kernel.apply() (canonical interface)
        return self.kernel.apply(request)
