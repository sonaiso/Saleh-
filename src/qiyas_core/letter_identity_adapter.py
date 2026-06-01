"""
Letter Identity Adapter

Atomic proof layer: LetterCodePoint → LetterIdentityCarrier

This is an INDEPENDENT atomic path that does NOT require:
  - ConditionedTypedSequence
  - HarakaFunctionCarrier
  - SlotCandidate

It proves letter identity (BAA, TAA, SEEN, etc.) from LetterCodePoint alone,
using Unicode identity, script identity, phonetic identity, makhraj, and sifat.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rule import QiyasRule
from .rules.letter_identity_rules import (
    BAA_LETTER_IDENTITY,
    TAA_LETTER_IDENTITY,
    SEEN_LETTER_IDENTITY,
    KAF_LETTER_IDENTITY,
)


# Letter identity mappings
LETTER_IDENTITY_MAP = {
    0x0628: ("BAA", "VOICED_BILABIAL_STOP", BAA_LETTER_IDENTITY),
    0x062A: ("TAA", "VOICELESS_ALVEOLAR_STOP", TAA_LETTER_IDENTITY),
    0x0633: ("SEEN", "VOICELESS_ALVEOLAR_FRICATIVE", SEEN_LETTER_IDENTITY),
    0x0643: ("KAF", "VOICELESS_VELAR_STOP", KAF_LETTER_IDENTITY),
    # Add more letters as needed
}


def get_letter_identity_info(codepoint: int) -> tuple[str, str, QiyasRule] | None:
    """
    Get letter identity information for a codepoint.

    Returns:
        Tuple of (letter_name, sound_identity, qiyas_rule) or None
    """
    return LETTER_IDENTITY_MAP.get(codepoint)


def prove_letter_identity(
    letter_candidate: Candidate,
    kernel: QiyasKernel
) -> CandidateSet:
    """
    Prove atomic letter identity from LetterCodePoint.

    This is an atomic proof that does NOT require sequence context.

    Args:
        letter_candidate: Must be LetterCodePoint
        kernel: QiyasKernel for validation

    Returns:
        CandidateSet with LetterIdentityCarrier or empty if proof fails
    """
    # Validate input type
    if letter_candidate.candidate_type != "LetterCodePoint":
        return CandidateSet(candidates=())

    # Extract codepoint value
    codepoint_value = letter_candidate.value.get("codepoint")
    if codepoint_value is None:
        return CandidateSet(candidates=())

    # Get letter identity info
    identity_info = get_letter_identity_info(codepoint_value)
    if identity_info is None:
        # Letter not yet mapped - return empty
        return CandidateSet(candidates=())

    letter_name, sound_identity, rule = identity_info

    # Build evidence for letter identity
    evidence = EvidenceSet(
        claims=(
            # Unicode identity
            Evidence(
                claim_type="wasf",
                claim_key=f"has_{letter_name.lower()}_unicode_identity",
                claim_value="present",
                justification=f"Codepoint U+{codepoint_value:04X} is {letter_name}",
            ),
            # Script identity
            Evidence(
                claim_type="wasf",
                claim_key=f"has_{letter_name.lower()}_script_identity",
                claim_value="present",
                justification=f"Script identity ARABIC_LETTER_{letter_name}",
            ),
            # Sound identity
            Evidence(
                claim_type="illah",
                claim_key=f"has_{letter_name.lower()}_sound_identity",
                claim_value="present",
                justification=f"Sound identity {sound_identity}",
            ),
            # Makhraj and sifat
            Evidence(
                claim_type="illah",
                claim_key=f"has_{letter_name.lower()}_makhraj_sifat",
                claim_value="present",
                justification=f"Phonetic profile for {letter_name}",
            ),
        )
    )

    # Create ASL reference (identity space)
    asl_ref = QiyasNodeRef(
        node_id=f"letter_identity_space:{letter_name}",
        node_type="ArabicLetterIdentitySpace",
        identity_trace=(f"identity:{letter_name}",),
    )

    # Build qiyas request
    request = QiyasRequest(
        context=QiyasContext(layer="LetterIdentityQiyas"),
        rule=rule,
        asl=asl_ref,
        far=letter_candidate,
        evidence=evidence,
    )

    # Execute qiyas through kernel
    result = kernel.execute_qiyas(request)

    if not result.accepted:
        return CandidateSet(candidates=())

    # Build LetterIdentityCarrier candidate
    identity_candidate = Candidate(
        candidate_id=str(uuid.uuid4()),
        candidate_type="LetterIdentityCarrier",
        value={
            "letter_name": letter_name,
            "unicode_identity": f"U+{codepoint_value:04X}",
            "script_identity": f"ARABIC_LETTER_{letter_name}",
            "sound_identity": sound_identity,
            "codepoint": codepoint_value,
        },
        evidence=result.evidence,
        rank=result.rank,
        trace_ids=letter_candidate.trace_ids + (letter_candidate.candidate_id,),
    )

    return CandidateSet(candidates=(identity_candidate,))


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
    """

    kernel: QiyasKernel

    def process_letter_codepoint(self, letter_candidate: Candidate) -> CandidateSet:
        """
        Process a single LetterCodePoint to prove its identity.

        Args:
            letter_candidate: Must be LetterCodePoint

        Returns:
            CandidateSet with LetterIdentityCarrier
        """
        return prove_letter_identity(letter_candidate, self.kernel)
