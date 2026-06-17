"""
PositionLayerAdapter — Gap #5 adapter.

SCG-P1 PR-2: converts a ConditionedTypedSequence ``PositionEvidence`` (with
explicit position information supplied by the caller) into a ``PositionCarrier``
via QiyasKernel.apply().

Canonical identity discipline (PR-2): the PositionCarrier **preserves the
``conditioned_typed_sequence`` identity** carried by the PositionEvidence as its
consumed canonical identity. The underlying codepoint is kept only as a
**trace/bridge** reference, never as consumed canonical identity.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.position_rules import get_position_rule, POSITION_INITIAL

# The sequence-level identity that ConditionedTypedSequence stamps on every
# PositionEvidence; PositionCarrier preserves it as canonical identity.
_CTS_IDENTITY = "identity:conditioned_typed_sequence_domain"


def _extract_codepoint(candidate: Candidate) -> int | None:
    for iid in candidate.identity_ids:
        if iid.startswith("identity:codepoint:"):
            try:
                return int(iid.split(":")[-1], 16)
            except ValueError:
                pass
    return None


def _conditioned_sequence_identity(candidate: Candidate) -> tuple[str, ...]:
    """The conditioned-sequence identity ids carried by a PositionEvidence."""
    return tuple(iid for iid in candidate.identity_ids if "conditioned_typed_sequence" in iid)


@dataclass
class PositionLayerAdapter:
    """
    Adapter that proves PositionCarrier for a LetterCodePoint.

    The caller must supply:
      - position_type: "INITIAL" | "MEDIAL" | "FINAL" | "ISOLATED"
      - index: integer position in the sequence
      - within_word: bool
      - at_boundary: bool
    """

    kernel: QiyasKernel

    def build_request(
        self,
        position_evidence: Candidate,
        position_type: str = POSITION_INITIAL,
        index: int = 0,
        within_word: bool = True,
        at_boundary: bool = False,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest for position classification from a
        ConditionedTypedSequence ``PositionEvidence`` (SCG-P1 PR-2)."""
        seq_identity = _conditioned_sequence_identity(position_evidence)
        if not seq_identity:
            raise ValueError(
                "PositionCarrier must consume a ConditionedTypedSequence "
                "PositionEvidence carrying the conditioned_typed_sequence identity"
            )

        rule = get_position_rule(position_type)
        if rule is None:
            raise ValueError(f"Unknown position_type: {position_type!r}")

        codepoint = _extract_codepoint(position_evidence)  # bridge/trace only
        cp_hex = f"{codepoint:04x}" if codepoint is not None else "unknown"
        if not trace_prefix:
            trace_prefix = f"position:{cp_hex}:{index}"

        pos_lower = position_type.lower()

        asl = QiyasNodeRef(
            node_id="اصل:position_domain",
            node_type="PositionDomain",
            identity_ids=("identity:position_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # Canonical identity preserved = the conditioned-sequence identity.
        # The codepoint is demoted to a trace/bridge reference — never consumed
        # as canonical identity (SCG-P1 PR-2 correction #2).
        far_trace = (f"{trace_prefix}:far",)
        if codepoint is not None:
            far_trace = far_trace + (f"bridge:codepoint:{cp_hex}",)
        far = QiyasNodeRef(
            node_id=f"فرع:position_evidence:{cp_hex}:pos{index}",
            node_type="PositionEvidence",
            identity_ids=seq_identity,
            trace_ids=far_trace,
            rank=position_evidence.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_position_index:evidenced",
            f"وصف:has_position_type:{pos_lower}:evidenced",
            "وصف:within_word_determined:evidenced",
            "علة:belongs_to_position_domain:verified",
            f"علة:position_type_is:{pos_lower}:verified",
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
                    evidence_id=f"ev:position:{cp_hex}:{index}:{uuid.uuid4().hex[:8]}",
                    source_layer="PositionQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        return QiyasRequest(
            rule=rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="PositionQiyas"),
        )

    def prove_position(
        self,
        position_evidence: Candidate,
        position_type: str = POSITION_INITIAL,
        index: int = 0,
        within_word: bool = True,
        at_boundary: bool = False,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove the position carrier for a ConditionedTypedSequence
        PositionEvidence candidate."""
        request = self.build_request(
            position_evidence, position_type, index, within_word, at_boundary, trace_prefix
        )
        return self.kernel.apply(request)

    def prove_from_codepoint(
        self,
        codepoint: int,
        position_type: str = POSITION_INITIAL,
        index: int = 0,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """
        Prove position from a raw codepoint.

        **WARNING: convenience/testing method only.** Synthesizes a
        ConditionedTypedSequence-shaped ``PositionEvidence`` (carrying the
        conditioned-sequence identity + a codepoint bridge id) and proves the
        PositionCarrier from it — mirroring the canonical
        ConditionedTypedSequence → PositionCarrier path.
        """
        cp_hex = f"{codepoint:04x}"
        position_evidence = Candidate(
            candidate_id=f"position_evidence:{cp_hex}:{index}",
            candidate_type="PositionEvidence",
            status=CandidateStatus.ACCEPTED,
            layer="ConditionedTypedSequenceQiyas",
            source_rule_id="conditioned_typed_sequence.letter_position",
            asl_id="اصل:conditioned_typed_sequence_domain",
            far_id=f"فرع:letter_codepoint:{cp_hex}",
            identity_ids=(_CTS_IDENTITY, f"identity:codepoint:{cp_hex}"),
            rank=EvidenceRank.FORMAL_STRUCTURE,
            residuals=(),
            trace_ids=(f"test:position_evidence:{cp_hex}",),
            output_flags=frozenset(),
        )
        return self.prove_position(
            position_evidence, position_type=position_type, index=index, trace_prefix=trace_prefix
        )
