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
from .registries.glyph_classification_registry import classify_glyph, GlyphClass


def _get_glyph_gate_residual(
    glyph_classification,
    codepoint: int,
    trace_prefix: str = ""
) -> Residual:
    """
    Generate specific residual based on glyph classification gate failure.

    Constitutional requirement: كل منع أو تأجيل = residual صريح مخصوص
    (Every block or defer must emit a specific, explicit residual)

    Args:
        glyph_classification: GlyphClassification from classify_glyph()
        codepoint: Unicode codepoint
        trace_prefix: Optional trace prefix

    Returns:
        Residual with specific type based on glyph classification failure reason
    """
    codepoint_hex = f"{codepoint:04x}"

    # Block: No phonetic coordinates allowed
    if not glyph_classification.allows_phonetic_coordinates:
        if glyph_classification.glyph_class == GlyphClass.TATWEEL_GLYPH:
            return Residual(
                residual_type="glyph_has_no_phonetic_coordinates",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.BLOCK,
                message=f"Tatweel U+{codepoint_hex} has no phonetic coordinates (spacing glyph only)",
                source_rule_id="glyph_gate.tatweel_no_coordinates",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:glyph_gate:blocked:tatweel",),
            )
        elif glyph_classification.glyph_class == GlyphClass.PUNCTUATION:
            return Residual(
                residual_type="glyph_has_no_phonetic_coordinates",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.BLOCK,
                message=f"Punctuation U+{codepoint_hex} has no phonetic coordinates",
                source_rule_id="glyph_gate.punctuation_no_coordinates",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:glyph_gate:blocked:punctuation",),
            )
        elif glyph_classification.glyph_class == GlyphClass.BOUNDARY:
            return Residual(
                residual_type="glyph_has_no_phonetic_coordinates",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.BLOCK,
                message=f"Boundary U+{codepoint_hex} has no phonetic coordinates",
                source_rule_id="glyph_gate.boundary_no_coordinates",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:glyph_gate:blocked:boundary",),
            )
        else:
            # RESIDUAL or unknown glyph class
            return Residual(
                residual_type="glyph_classification_residual",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.BLOCK,
                message=f"Glyph U+{codepoint_hex} classification prevents coordinate assignment",
                source_rule_id="glyph_gate.unclassified_no_coordinates",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:glyph_gate:blocked:unclassified",),
            )

    # Defer: Decomposition required
    if glyph_classification.requires_decomposition:
        if glyph_classification.glyph_class == GlyphClass.HAMZA_SEAT_GLYPH:
            return Residual(
                residual_type="glyph_decomposition_required",
                severity=ResidualSeverity.WARNING,
                effect=ResidualEffect.DEFER,
                message=f"Hamza seat U+{codepoint_hex} requires decomposition before coordinate assignment",
                source_rule_id="glyph_gate.hamza_seat_decomposition",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:glyph_gate:deferred:hamza_seat",),
            )
        elif glyph_classification.glyph_class == GlyphClass.COMPLEX_GLYPH:
            return Residual(
                residual_type="glyph_decomposition_required",
                severity=ResidualSeverity.WARNING,
                effect=ResidualEffect.DEFER,
                message=f"Complex glyph U+{codepoint_hex} requires decomposition before coordinate assignment",
                source_rule_id="glyph_gate.complex_glyph_decomposition",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:glyph_gate:deferred:complex_glyph",),
            )

    # Defer: Role disambiguation required
    if glyph_classification.requires_role_disambiguation:
        return Residual(
            residual_type="glyph_role_disambiguation_required",
            severity=ResidualSeverity.WARNING,
            effect=ResidualEffect.DEFER,
            message=f"Weak letter U+{codepoint_hex} requires role disambiguation before coordinate assignment",
            source_rule_id="glyph_gate.weak_letter_disambiguation",
            layer="ArabicLetterCoordinateQiyas",
            trace_ids=(f"{trace_prefix}:glyph_gate:deferred:weak_letter",),
        )

    # Fallback: Should not reach here if gate logic is correct
    return Residual(
        residual_type="glyph_classification_residual",
        severity=ResidualSeverity.WARNING,
        effect=ResidualEffect.DEFER,
        message=f"Glyph U+{codepoint_hex} blocked by glyph classification gate",
        source_rule_id="glyph_gate.unknown_failure",
        layer="ArabicLetterCoordinateQiyas",
        trace_ids=(f"{trace_prefix}:glyph_gate:unknown",),
    )


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
    ) -> tuple[QiyasRequest | None, Residual | None]:
        """
        Build a QiyasRequest for enriching letter identity with coordinates.

        Constitutional requirement: كل منع أو تأجيل = residual صريح مخصوص
        (Every block or defer must emit a specific, explicit residual)

        Args:
            letter_identity: Must be LetterIdentityCarrier from LetterIdentityLayerAdapter
            trace_prefix: Optional prefix for trace IDs

        Returns:
            Tuple of (QiyasRequest | None, Residual | None):
              - (QiyasRequest, None) if coordinate enrichment supported
              - (None, Residual) if blocked/deferred with specific reason
        """
        # Validate input type
        if letter_identity.candidate_type != "LetterIdentityCarrier":
            residual = Residual(
                residual_type="invalid_letter_identity_input",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.BLOCK,
                message=f"Expected LetterIdentityCarrier, got {letter_identity.candidate_type}",
                source_rule_id="letter_coordinate.invalid_input",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:invalid_input",),
            )
            return (None, residual)

        # Extract codepoint from identity_ids
        codepoint = None
        for identity_id in letter_identity.identity_ids:
            if identity_id.startswith("identity:codepoint:"):
                codepoint_hex = identity_id.split(":")[-1]
                codepoint = int(codepoint_hex, 16)
                break

        if codepoint is None:
            residual = Residual(
                residual_type="letter_codepoint_missing",
                severity=ResidualSeverity.BLOCKER,
                effect=ResidualEffect.BLOCK,
                message="Letter identity missing codepoint in identity_ids",
                source_rule_id="letter_coordinate.missing_codepoint",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:missing_codepoint",),
            )
            return (None, residual)

        if not trace_prefix:
            trace_prefix = f"letter_coordinate:{codepoint:04x}"

        # GLYPH CLASSIFICATION GATE
        # Constitutional requirement: No coordinates before glyph classification
        # Enforces: لا إحداثيات قبل تصنيف glyph
        glyph_classification = classify_glyph(codepoint)

        # Block glyphs that don't allow phonetic coordinates
        if not glyph_classification.allows_phonetic_coordinates:
            # TATWEEL, PUNCTUATION, BOUNDARY - no coordinates allowed
            residual = _get_glyph_gate_residual(glyph_classification, codepoint, trace_prefix)
            return (None, residual)

        # Defer glyphs requiring decomposition
        if glyph_classification.requires_decomposition:
            # HAMZA_SEAT_GLYPH, COMPLEX_GLYPH - need decomposition first
            residual = _get_glyph_gate_residual(glyph_classification, codepoint, trace_prefix)
            return (None, residual)

        # Defer glyphs requiring role disambiguation
        if glyph_classification.requires_role_disambiguation:
            # WEAK_LETTER_GLYPH (و ي ا) - need role determination first
            residual = _get_glyph_gate_residual(glyph_classification, codepoint, trace_prefix)
            return (None, residual)

        # At this stage, only CORE_ARABIC_LETTER and STANDALONE_HAMZA proceed
        # (assuming STANDALONE_HAMZA has phonetic profile and rule defined)

        # Get phonetic profile (makhraj, sifat, fariq)
        phonetic_profile = get_phonetic_profile(codepoint)
        if phonetic_profile is None:
            # Letter not yet mapped with phonetic profile
            residual = Residual(
                residual_type="phonetic_profile_missing",
                severity=ResidualSeverity.WARNING,
                effect=ResidualEffect.DEFER,
                message=f"Phonetic profile not yet defined for U+{codepoint:04x}",
                source_rule_id="letter_coordinate.missing_phonetic_profile",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:missing_phonetic_profile",),
            )
            return (None, residual)

        # Get coordinate rule
        rule = get_letter_coordinate_rule(codepoint)
        if rule is None:
            # Coordinate rule not yet defined
            residual = Residual(
                residual_type="coordinate_rule_missing",
                severity=ResidualSeverity.WARNING,
                effect=ResidualEffect.DEFER,
                message=f"Coordinate rule not yet defined for U+{codepoint:04x}",
                source_rule_id="letter_coordinate.missing_coordinate_rule",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:missing_coordinate_rule",),
            )
            return (None, residual)

        # Extract letter name from letter_identity source_rule_id
        # e.g., "letter_identity.baa" → "baa"
        letter_name = None
        if letter_identity.source_rule_id:
            parts = letter_identity.source_rule_id.split(".")
            if len(parts) == 2 and parts[0] == "letter_identity":
                letter_name = parts[1]

        if not letter_name:
            residual = Residual(
                residual_type="letter_name_extraction_failed",
                severity=ResidualSeverity.WARNING,
                effect=ResidualEffect.DEFER,
                message=f"Cannot extract letter name from source_rule_id: {letter_identity.source_rule_id}",
                source_rule_id="letter_coordinate.missing_letter_name",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:missing_letter_name",),
            )
            return (None, residual)

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
            residual = Residual(
                residual_type="coordinate_evidence_empty",
                severity=ResidualSeverity.WARNING,
                effect=ResidualEffect.DEFER,
                message=f"No evidence could be built for letter coordinate enrichment of {letter_name}",
                source_rule_id="letter_coordinate.empty_evidence",
                layer="ArabicLetterCoordinateQiyas",
                trace_ids=(f"{trace_prefix}:empty_evidence",),
            )
            return (None, residual)

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

        # Build and return request (no residual)
        request = QiyasRequest(
            rule=rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="ArabicLetterCoordinateQiyas"),
        )
        return (request, None)

    def process_letter_identity(
        self,
        letter_identity: Candidate,
        trace_prefix: str = ""
    ) -> CandidateSet:
        """
        Process a LetterIdentityCarrier to enrich with coordinates.

        Constitutional requirement: كل منع أو تأجيل = residual صريح مخصوص
        (Every block or defer must emit a specific, explicit residual)

        Args:
            letter_identity: Must be LetterIdentityCarrier with full evidence/rank/trace
            trace_prefix: Optional prefix for trace IDs

        Returns:
            CandidateSet with ArabicLetterCoordinateCarrier (if supported) or specific residual
        """
        request, residual = self.build_request_for_letter_coordinates(letter_identity, trace_prefix)

        if request is None:
            # Coordinate enrichment blocked/deferred - return CandidateSet with specific residual
            # residual is guaranteed to be non-None when request is None
            assert residual is not None, "build_request_for_letter_coordinates must return residual when request is None"

            return CandidateSet(
                set_id=f"letter_coordinate:{residual.residual_type}:{uuid.uuid4().hex[:8]}",
                layer="ArabicLetterCoordinateQiyas",
                candidates=(),
                residuals=(residual,),
                trace_ids=residual.trace_ids,
            )

        # Execute qiyas through kernel.apply() (canonical interface)
        return self.kernel.apply(request)
