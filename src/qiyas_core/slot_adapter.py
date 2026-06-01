"""
SlotLayerAdapter — Gap #6 adapter (PR #26 update).

Composes the four pillars of a SlotCandidate via QiyasKernel.apply():

    1. LetterIdentityCarrier      (atomic identity proof)
    2. HarakaFunctionCarrier      (atomic function proof)
    3. PositionCarrier            (position proof)
    4. AlignmentEvidence /        (sequence-conditioning proof from
       CarrierBindingCandidate    ConditionedTypedSequenceQiyas)

Per CLAUDE.md §8, no SlotCandidate may be produced without all four
pillars. Per CLAUDE.md §0 and §2, this adapter MUST NOT self-assert the
compatibility wasfs (`compatible_letter_haraka`, `compatible_letter_position`)
or the alignment wasf (`has_alignment_evidence`) without a valid
upstream proof.

Constitutional law:
  SlotCandidate ⊬ SyllableCandidate  (adjacency not yet established)
  SlotCandidate ⊬ MeaningCandidate
  SlotCandidate ⊬ SlotGeometry       (single-slot proof only)
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.slot_rules import SLOT_COMPOSITION_RULE


# ---------------------------------------------------------------------------
# Identity extraction helpers (preserved from earlier PRs)
# ---------------------------------------------------------------------------


def _extract_letter_name(letter_carrier: Candidate) -> str:
    """Extract arabic_name from identity_ids (identity:letter:{name})."""
    for iid in letter_carrier.identity_ids:
        if iid.startswith("identity:letter:"):
            return iid[len("identity:letter:"):]
    return letter_carrier.candidate_id


def _extract_haraka_name(haraka_carrier: Candidate) -> str:
    """Extract arabic_name from identity_ids (identity:haraka:{name})."""
    for iid in haraka_carrier.identity_ids:
        if iid.startswith("identity:haraka:"):
            return iid[len("identity:haraka:"):]
    return haraka_carrier.candidate_id


# ---------------------------------------------------------------------------
# Alignment evidence validation
# ---------------------------------------------------------------------------

# Per CLAUDE.md §9, valid sequence-conditioning outputs that may serve as
# alignment proof for a SlotCandidate.
_VALID_ALIGNMENT_TYPES = frozenset({
    "CarrierBindingCandidate",
    "CarrierBindingEvidence",
    "AlignmentEvidence",
})


def _codepoint_identities(candidate: Candidate) -> frozenset[str]:
    """Return the identity:codepoint:* identifiers carried by a candidate."""
    return frozenset(
        iid for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )


def _alignment_is_valid(
    alignment: Candidate | None,
    letter_carrier: Candidate,
    haraka_carrier: Candidate,
) -> bool:
    """
    Decide whether a supplied alignment proof witnesses the binding of
    THIS specific letter to THIS specific haraka. Three conditions:

      1. alignment is present and ACCEPTED;
      2. alignment.candidate_type is one of the recognised CTS outputs;
      3. alignment's codepoint identities cover both the letter's and
         the haraka's codepoint identities (so the proof is *about*
         this pair, not some other pair).

    The adapter is the only place this check happens — the kernel sees
    only the resulting wasf claims.
    """
    if alignment is None:
        return False
    if alignment.status != CandidateStatus.ACCEPTED:
        return False
    if alignment.candidate_type not in _VALID_ALIGNMENT_TYPES:
        return False
    align_cps = _codepoint_identities(alignment)
    letter_cps = _codepoint_identities(letter_carrier)
    haraka_cps = _codepoint_identities(haraka_carrier)
    if not letter_cps.issubset(align_cps):
        return False
    if not haraka_cps.issubset(align_cps):
        return False
    return True


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------


@dataclass
class SlotLayerAdapter:
    """
    Adapter that composes the four pillars into a SlotCandidate.

    Constitutional path:
        LetterIdentityCarrier
        + HarakaFunctionCarrier
        + PositionCarrier
        + AlignmentEvidence / CarrierBindingCandidate
            → [SlotLayerAdapter] → SlotCandidate
    """

    kernel: QiyasKernel

    def build_request(
        self,
        letter_carrier: Candidate,
        haraka_carrier: Candidate,
        position_carrier: Candidate,
        alignment_evidence: Candidate | None = None,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for slot composition.

        ``alignment_evidence`` must be a CarrierBindingCandidate (or
        equivalent AlignmentEvidence/CarrierBindingEvidence) from
        ConditionedTypedSequenceQiyas, with codepoint identities
        covering both the letter and the haraka. When it is absent or
        invalid, the adapter declines to assert the alignment wasfs;
        the kernel then blocks the SlotCandidate with an
        effective_wasf_missing residual.
        """
        letter_name = _extract_letter_name(letter_carrier)
        haraka_name = _extract_haraka_name(haraka_carrier)

        if not trace_prefix:
            trace_prefix = f"slot:{letter_name}:{haraka_name}"

        combined_identity = (
            letter_carrier.identity_ids
            + haraka_carrier.identity_ids
            + position_carrier.identity_ids
        )
        seen: set[str] = set()
        deduped_identity: list[str] = []
        for iid in combined_identity:
            if iid not in seen:
                seen.add(iid)
                deduped_identity.append(iid)

        asl = QiyasNodeRef(
            node_id="اصل:slot_composition_domain",
            node_type="SlotCompositionDomain",
            identity_ids=("identity:slot_composition_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        far = QiyasNodeRef(
            node_id=f"فرع:letter_identity_carrier:{letter_name}",
            node_type="LetterIdentityCarrier",
            identity_ids=tuple(deduped_identity),
            trace_ids=(f"{trace_prefix}:far",),
            rank=min(
                (letter_carrier.rank, haraka_carrier.rank, position_carrier.rank),
                key=lambda r: r.value,
            ),
        )

        # Base claims that the adapter is always entitled to assert from
        # the three carriers' presence.
        proves: list[str] = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_letter_identity_carrier:evidenced",
            "وصف:has_haraka_function_carrier:evidenced",
            "وصف:has_position_carrier:evidenced",
            "وصف:identity_preserved:evidenced",
            "علة:belongs_to_slot_composition_domain:verified",
            "علة:slot_composition_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # The alignment / compatibility wasfs may ONLY be asserted when
        # a valid CTS-layer proof has been supplied. Per CLAUDE.md §2
        # the adapter MUST NOT self-assert them otherwise.
        align_trace_ids: tuple[str, ...] = ()
        if _alignment_is_valid(alignment_evidence, letter_carrier, haraka_carrier):
            assert alignment_evidence is not None  # for type checker
            proves.extend([
                "وصف:has_alignment_evidence:evidenced",
                "وصف:compatible_letter_haraka:evidenced",
                "وصف:compatible_letter_position:evidenced",
                f"علة:alignment_witness_layer:{alignment_evidence.layer}:verified",
            ])
            align_trace_ids = (
                f"{trace_prefix}:alignment_ref:{alignment_evidence.candidate_id}",
            )

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:slot:{letter_name}:{haraka_name}:{uuid.uuid4().hex[:8]}",
                    source_layer="SlotQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + align_trace_ids,
                ),
            )
        )

        return QiyasRequest(
            rule=SLOT_COMPOSITION_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SlotQiyas"),
        )

    def compose_slot(
        self,
        letter_carrier: Candidate,
        haraka_carrier: Candidate,
        position_carrier: Candidate,
        alignment_evidence: Candidate | None = None,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """
        Compose a SlotCandidate from the four pillars.

        If ``alignment_evidence`` is None or does not cover both the
        letter and the haraka, the kernel will block the result with
        an effective_wasf_missing residual for the alignment/compat
        wasfs.
        """
        request = self.build_request(
            letter_carrier,
            haraka_carrier,
            position_carrier,
            alignment_evidence=alignment_evidence,
            trace_prefix=trace_prefix,
        )
        return self.kernel.apply(request)
