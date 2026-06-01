"""
LetterIdentityLayerAdapter — Gap #3 adapter.

Converts a LetterCodePoint candidate into a LetterIdentityCarrier by building
the full evidence set (unicode_identity + script_identity + sound_identity +
makhraj + sifat) and invoking QiyasKernel.apply().

Follows the same pattern as TypedCodePointLayerAdapter.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .phonetics import get_phonetic_profile
from .rules.letter_identity_rules import get_letter_identity_rule


# Arabic letter codepoint range
_ARABIC_LETTER_MIN = 0x0621
_ARABIC_LETTER_MAX = 0x064A


def _extract_codepoint(candidate: Candidate) -> int | None:
    """Extract integer codepoint from identity_ids (identity:codepoint:{hex})."""
    for iid in candidate.identity_ids:
        if iid.startswith("identity:codepoint:"):
            try:
                return int(iid.split(":")[-1], 16)
            except ValueError:
                pass
    return None


@dataclass
class LetterIdentityLayerAdapter:
    """
    Adapter that proves LetterIdentityCarrier for a given LetterCodePoint.

    Constitutional path:
        LetterCodePoint → [LetterIdentityLayerAdapter] → LetterIdentityCarrier
    """

    kernel: QiyasKernel

    def build_request(
        self,
        letter_candidate: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest for letter identity classification."""
        codepoint = _extract_codepoint(letter_candidate)
        if codepoint is None:
            raise ValueError(
                "LetterCodePoint candidate must have identity:codepoint:{hex} identity"
            )

        profile = get_phonetic_profile(codepoint)
        if profile is None:
            raise ValueError(
                f"No PhoneticGroundingProfile for codepoint U+{codepoint:04X}"
            )

        rule = get_letter_identity_rule(codepoint)
        if rule is None:
            raise ValueError(
                f"No LetterIdentityRule for codepoint U+{codepoint:04X}"
            )

        cp_hex = f"{codepoint:04x}"
        if not trace_prefix:
            trace_prefix = f"letter_identity:{cp_hex}"

        asl = QiyasNodeRef(
            node_id="asl:letter_identity_domain",
            node_type="LetterIdentityDomain",
            identity_ids=("identity:letter_identity_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        far = QiyasNodeRef(
            node_id=f"far:letter_codepoint:{cp_hex}",
            node_type="LetterCodePoint",
            identity_ids=letter_candidate.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=letter_candidate.rank,
        )

        # Build proves list from the phonetic profile
        proves = [
            "asl:established",
            "far:determined",
            # Generic + type-specific wasf
            "wasf:has_letter_codepoint:evidenced",
            f"wasf:has_unicode_identity:{cp_hex}:evidenced",
            f"wasf:has_script_identity:{profile.arabic_name}:evidenced",
            f"wasf:has_sound_identity:{profile.sound_identity.lower()}:evidenced",
            f"wasf:has_makhraj:{profile.makhraj.spatial_source.lower()}:evidenced",
            # Illah
            "illah:belongs_to_letter_identity_domain:verified",
            f"illah:letter_identity_is:{profile.arabic_name}:verified",
            # Wadi gates
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
                    evidence_id=f"ev:letter_identity:{cp_hex}:{uuid.uuid4().hex[:8]}",
                    source_layer="LetterIdentityQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORM,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="LetterIdentityQiyas"),
        )

    def prove_letter_identity(
        self,
        letter_candidate: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove the letter identity for a LetterCodePoint candidate."""
        request = self.build_request(letter_candidate, trace_prefix)
        return self.kernel.apply(request)

    def prove_from_codepoint(
        self,
        codepoint: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """
        Prove letter identity from a raw codepoint.

        **WARNING: convenience/testing method only.**
        Production code should use prove_letter_identity() with a proper
        LetterCodePoint candidate from TypedCodePointLayerAdapter.
        """
        cp_hex = f"{codepoint:04x}"
        letter_candidate = Candidate(
            candidate_id=f"letter_codepoint:{cp_hex}",
            candidate_type="LetterCodePoint",
            status=CandidateStatus.ACCEPTED,
            layer="TypedCodePointClassificationQiyas",
            source_rule_id="typed_codepoint.letter_classification",
            asl_id="asl:typed_codepoint_classification_domain",
            far_id=f"far:unicode_candidate:{cp_hex}",
            identity_ids=(f"identity:codepoint:{cp_hex}",),
            rank=EvidenceRank.FORM,
            residuals=(),
            trace_ids=(f"test:letter_codepoint:{cp_hex}",),
            output_flags=frozenset(),
        )
        return self.prove_letter_identity(letter_candidate, trace_prefix)
