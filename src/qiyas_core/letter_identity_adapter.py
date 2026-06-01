"""
Letter Identity Adapter

Atomic proof layer: LetterCodePoint → LetterIdentityCarrier

This is an INDEPENDENT atomic path that does NOT require:
  - ConditionedTypedSequence
  - HarakaFunctionCarrier
  - PositionCarrier
  - SlotCandidate

It proves letter identity (BAA, TAA, SEEN, etc.) from LetterCodePoint alone,
using Unicode identity, script identity, phonetic identity, makhraj, and sifat.

Constitutional Compliance:
  - Uses kernel.apply() not execute_qiyas()
  - Uses Evidence with proves tuple not claims
  - Uses QiyasNodeRef with identity_ids, trace_ids, rank
  - Preserves identity_ids through transformation
  - Proves invalidating_differences absence in evidence
  - Separates digital/script/name/phonetic/makhraj/sifat identities
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.letter_identity_rules import get_letter_identity_rule


def build_letter_identity_evidence(
    letter_name: str,
    codepoint: int,
    makhraj: str,
    voicing: str,
    manner: str,
    emphasis: str,
    invalidating_diffs: tuple[str, ...],
    trace_prefix: str,
) -> EvidenceSet:
    """
    Build evidence for letter identity with full representation contract.

    Proves:
      - Unicode identity (digital layer)
      - Script identity
      - Name identity
      - Phonetic proxy identity
      - Makhraj class identity
      - Sifat profile
      - Absence of invalidating differences (fariq)

    Args:
        letter_name: Lowercase letter name (e.g., "baa", "taa", "seen")
        codepoint: Unicode codepoint value
        makhraj: Makhraj class (uppercase, e.g., "BILABIAL")
        voicing: Voicing (uppercase, e.g., "VOICED")
        manner: Manner (uppercase, e.g., "STOP")
        emphasis: Emphasis (uppercase, e.g., "NON_EMPHATIC")
        invalidating_diffs: Tuple of invalidating difference names
        trace_prefix: Trace prefix for evidence
    """
    cp_hex = f"{codepoint:04x}"

    proves = [
        "asl:established",
        "far:determined",
        # Generic wasf
        "wasf:has_letter_codepoint:evidenced",
        # Type-specific wasf (representation contract layers) - must match rule format exactly
        f"wasf:has_unicode_identity:{cp_hex}:evidenced",
        f"wasf:has_script_identity:{letter_name}:evidenced",  # lowercase letter_name
        f"wasf:has_sound_identity:{voicing.lower()}_{manner.lower()}:evidenced",
        f"wasf:has_makhraj:{makhraj.lower()}:evidenced",
        # Generic illah
        "illah:belongs_to_letter_identity_domain:verified",
        # Type-specific illah - must match rule format exactly
        f"illah:letter_identity_is:{letter_name}:verified",  # lowercase letter_name
        # Wadi gates
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
    ]

    # Add invalidating differences (fariq) absence proofs
    for diff in invalidating_diffs:
        proves.append(f"fariq:{diff}:absent")

    return EvidenceSet(
        items=(
            Evidence(
                evidence_id=f"ev:letter_identity:{letter_name.lower()}:{uuid.uuid4().hex[:8]}",
                source_layer="LetterIdentityQiyas",
                proves=tuple(proves),
                rank=EvidenceRank.FORM,
                trace_ids=(f"{trace_prefix}:ev",),
            ),
        )
    )


def build_letter_identity_ids(
    letter_name: str,
    codepoint: int,
    makhraj: str,
    voicing: str,
    manner: str,
    input_identity_ids: tuple[str, ...],
) -> tuple[str, ...]:
    """
    Build identity_ids for LetterIdentityCarrier.

    Constitutional requirement: input_identity_ids ⊆ output_identity_ids

    Adds representation contract identities:
      - Digital identity (codepoint)
      - Script identity
      - Name identity
      - Phonetic proxy identity
      - Makhraj class identity
      - Sifat profile identity
      - Specific letter identity
    """
    cp_hex = f"{codepoint:04x}"
    phonetic_proxy = f"/{letter_name[0].lower()}/" if letter_name else "/?"

    new_identities = [
        # Preserve input identities
        *input_identity_ids,
        # Digital identity layer
        f"identity:unicode:{cp_hex}",
        # Script identity layer
        f"identity:script:arabic_letter_{letter_name.lower()}",
        # Name identity layer
        f"identity:name:{letter_name.lower()}",
        # Phonetic proxy identity layer
        f"identity:phonetic_proxy:{phonetic_proxy}",
        # Makhraj class identity layer
        f"identity:makhraj:{makhraj.lower()}",
        # Sifat profile identity layer
        f"identity:sifat:{voicing.lower()}_{manner.lower()}",
        # Specific letter identity (terminal)
        f"identity:letter:{letter_name.lower()}",
    ]

    return tuple(new_identities)


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

        if not trace_prefix:
            trace_prefix = f"letter_identity:{letter_name.lower()}"

        # Create asl node (letter identity domain)
        asl = QiyasNodeRef(
            node_id=f"asl:letter_identity_domain:{letter_name.lower()}",
            node_type="LetterIdentityDomain",
            identity_ids=("identity:letter_identity_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        # Create far node from letter_candidate (preserving its identity!)
        far = QiyasNodeRef(
            node_id=f"far:letter_codepoint:{codepoint:04x}",
            node_type="LetterCodePoint",
            identity_ids=letter_candidate.identity_ids,  # Preserve identity!
            trace_ids=(f"{trace_prefix}:far",),
            rank=letter_candidate.rank,
        )

        # Extract phonetic attributes from rule
        # Parse from required_effective_wasf
        makhraj = "UNKNOWN"
        voicing = "UNKNOWN"
        manner = "UNKNOWN"
        emphasis = "NON_EMPHATIC"

        for wasf in rule.required_effective_wasf:
            if "has_makhraj:" in wasf:
                makhraj = wasf.split(":")[-1].upper()
            elif "has_sound_identity:" in wasf:
                sound_parts = wasf.split(":")[-1].upper().split("_")
                if len(sound_parts) >= 2:
                    voicing = sound_parts[0]
                    manner = "_".join(sound_parts[1:])

        # Build evidence with representation contract
        evidence = build_letter_identity_evidence(
            letter_name=letter_name,
            codepoint=codepoint,
            makhraj=makhraj,
            voicing=voicing,
            manner=manner,
            emphasis=emphasis,
            invalidating_diffs=rule.invalidating_differences,
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
