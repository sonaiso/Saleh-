"""
PositionLayerAdapter — Gap #5 adapter.

Converts a LetterCodePoint (with explicit position information supplied by
the caller) into a PositionCarrier via QiyasKernel.apply().
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.position_rules import get_position_rule, POSITION_INITIAL


def _extract_codepoint(candidate: Candidate) -> int | None:
    for iid in candidate.identity_ids:
        if iid.startswith("identity:codepoint:"):
            try:
                return int(iid.split(":")[-1], 16)
            except ValueError:
                pass
    return None


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
        letter_candidate: Candidate,
        position_type: str = POSITION_INITIAL,
        index: int = 0,
        within_word: bool = True,
        at_boundary: bool = False,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest for position classification."""
        codepoint = _extract_codepoint(letter_candidate)
        if codepoint is None:
            raise ValueError(
                "Candidate must have identity:codepoint:{hex} identity"
            )

        rule = get_position_rule(position_type)
        if rule is None:
            raise ValueError(f"Unknown position_type: {position_type!r}")

        cp_hex = f"{codepoint:04x}"
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

        far = QiyasNodeRef(
            node_id=f"فرع:letter_codepoint:{cp_hex}:pos{index}",
            node_type="LetterCodePoint",
            identity_ids=letter_candidate.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=letter_candidate.rank,
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
        letter_candidate: Candidate,
        position_type: str = POSITION_INITIAL,
        index: int = 0,
        within_word: bool = True,
        at_boundary: bool = False,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove the position carrier for a LetterCodePoint candidate."""
        request = self.build_request(
            letter_candidate, position_type, index, within_word, at_boundary, trace_prefix
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

        **WARNING: convenience/testing method only.**
        """
        cp_hex = f"{codepoint:04x}"
        letter_candidate = Candidate(
            candidate_id=f"letter_codepoint:{cp_hex}",
            candidate_type="LetterCodePoint",
            status=CandidateStatus.ACCEPTED,
            layer="TypedCodePointClassificationQiyas",
            source_rule_id="typed_codepoint.letter_classification",
            asl_id="اصل:typed_codepoint_classification_domain",
            far_id=f"فرع:unicode_candidate:{cp_hex}",
            identity_ids=(f"identity:codepoint:{cp_hex}",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
            residuals=(),
            trace_ids=(f"test:letter_codepoint:{cp_hex}",),
            output_flags=frozenset(),
        )
        return self.prove_position(
            letter_candidate, position_type=position_type, index=index, trace_prefix=trace_prefix
        )
