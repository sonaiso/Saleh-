"""
ConditionedTypedSequenceLayerAdapter — PR #25.

Layer: ConditionedTypedSequenceQiyas

Per CLAUDE.md §5, this layer sits parallel to LetterIdentityCarrier and
HarakaFunctionCarrier, all branching off TypedCodePoint:

    TypedCodePoint*
        → ConditionedTypedSequence
        → AlignmentEvidence / CarrierBindingCandidate / PositionEvidence

It is the sequence-context proof obligation. It does NOT prove letter
identity, haraka function, or slot composition (§7, §11).

Per CLAUDE.md §14, the only valid outputs of this layer are:
    ConditionedTypedSequence
    AlignmentEvidence
    CarrierBindingEvidence | CarrierBindingCandidate
    PositionEvidence
    BoundaryEvidence
    ResidualPreservationEvidence

This adapter walks a sequence of TypedCodePoint candidates (the output
of TypedCodePointLayerAdapter) and emits per-position proofs by routing
each through QiyasKernel.apply().
"""

from dataclasses import dataclass
from typing import Sequence
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rule import QiyasRule
from .rules.conditioned_typed_sequence_rules import (
    BOUNDARY_EXCLUSION_PROOF,
    CARRIER_BINDING_PROOF,
    LETTER_POSITION_PROOF,
    PUNCTUATION_EXCLUSION_PROOF,
    RESIDUAL_PRESERVATION_PROOF,
    get_cts_rule_for_far_type,
)


# Tanwin codepoints (U+064B FATHATAN, U+064C DAMMATAN, U+064D KASRATAN)
_TANWIN_CODEPOINTS = frozenset({0x064B, 0x064C, 0x064D})
# Shadda codepoint (U+0651)
_SHADDA_CODEPOINT = 0x0651


def _extract_codepoint(candidate: Candidate) -> int | None:
    for iid in candidate.identity_ids:
        if iid.startswith("identity:codepoint:"):
            try:
                return int(iid.split(":")[-1], 16)
            except ValueError:
                pass
    return None


def _is_tanwin(candidate: Candidate) -> bool:
    cp = _extract_codepoint(candidate)
    return cp in _TANWIN_CODEPOINTS


def _is_shadda(candidate: Candidate) -> bool:
    return _extract_codepoint(candidate) == _SHADDA_CODEPOINT


@dataclass
class ConditionedTypedSequenceLayerAdapter:
    """
    Adapter for ConditionedTypedSequenceQiyas.

    Routes each TypedCodePoint candidate through one of the five
    sister-rules in conditioned_typed_sequence_rules.py based on the
    candidate's type (HarakaCodePoint / LetterCodePoint /
    BoundaryCodePoint / PunctuationCodePoint / ResidualCodePoint).
    """

    kernel: QiyasKernel

    # ----------------------------------------------------------- carrier binding

    def prove_carrier_binding(
        self,
        haraka_typed: Candidate,
        carrier_letter_typed: Candidate | None,
        index: int,
        sequence_length: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """
        Prove that a haraka has a carrier letter in the sequence.

        If carrier_letter_typed is None (orphan haraka), the rule's
        required wasf "preceded_by_letter_codepoint" is not asserted
        and the fariq "haraka_without_carrier" is asserted, producing
        a BLOCKED CarrierBindingCandidate with residuals.
        """
        cp = _extract_codepoint(haraka_typed)
        cp_hex = f"{cp:04x}" if cp is not None else "unknown"
        if not trace_prefix:
            trace_prefix = f"cts:carrier_binding:{cp_hex}:{index}"

        asl = QiyasNodeRef(
            node_id="اصل:conditioned_typed_sequence_domain",
            node_type="ConditionedTypedSequenceDomain",
            identity_ids=("identity:conditioned_typed_sequence_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        far_identity = haraka_typed.identity_ids
        if carrier_letter_typed is not None:
            far_identity = far_identity + carrier_letter_typed.identity_ids
        far = QiyasNodeRef(
            node_id=f"فرع:haraka_codepoint:{cp_hex}:pos{index}",
            node_type="HarakaCodePoint",
            identity_ids=far_identity,
            trace_ids=(f"{trace_prefix}:far",),
            rank=haraka_typed.rank,
        )

        proves: list[str] = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_haraka_in_sequence:evidenced",
            "وصف:sequence_index_determined:evidenced",
        ]

        if carrier_letter_typed is not None:
            proves.extend([
                "وصف:preceded_by_letter_codepoint:evidenced",
                "وصف:carrier_alignment_determined:evidenced",
                "علة:carrier_binding_licensed:verified",
            ])
            # Tanwin terminal-sensitivity marker (CLAUDE.md §7 test #4).
            # Tanwin remains a CarrierBindingCandidate; the marker is
            # auditable evidence, never a Slot.
            if _is_tanwin(haraka_typed):
                terminal = (index == sequence_length - 1)
                proves.append(
                    "وصف:tanwin_terminal_sensitive:evidenced"
                    if terminal
                    else "وصف:tanwin_non_terminal_position:evidenced"
                )
            if _is_shadda(haraka_typed):
                proves.append("وصف:shadda_has_carrier:evidenced")
        else:
            # Orphan mark: assert the invalidating-difference so the
            # kernel records a blocking fariq residual; required wasf
            # remains unsatisfied so the kernel also records an
            # effective_wasf_missing residual. Status will be BLOCKED.
            proves.append("فارق:haraka_without_carrier:present")
            if _is_shadda(haraka_typed):
                proves.append("فارق:orphan_mark:present")

        proves.extend([
            "علة:belongs_to_conditioned_typed_sequence_domain:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ])

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:cts:carrier_binding:{cp_hex}:{index}:{uuid.uuid4().hex[:8]}",
                    source_layer="ConditionedTypedSequenceQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        request = QiyasRequest(
            rule=CARRIER_BINDING_PROOF,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="ConditionedTypedSequenceQiyas"),
        )
        return self.kernel.apply(request)

    # ----------------------------------------------------------- letter position

    def prove_letter_position(
        self,
        letter_typed: Candidate,
        index: int,
        sequence_length: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove a letter has a sequence position (PositionEvidence)."""
        return self._prove_simple_position(
            LETTER_POSITION_PROOF,
            letter_typed,
            index,
            sequence_length,
            extra_wasf=("neighbor_context_determined",),
            illah_extra=("letter_position_in_sequence_licensed",),
            slug="letter_position",
            trace_prefix=trace_prefix,
        )

    # ----------------------------------------------------------- boundary

    def prove_boundary_exclusion(
        self,
        boundary_typed: Candidate,
        index: int,
        sequence_length: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Z4 LEGACY UNREACHABLE — kept for legacy fixtures only.

        Post-Z2/Z3 the canonical CTS path consumes
        `SequenceContextTokenizer` markers (segment_id / boundary_before
        / boundary_after) as evidence on `CARRIER_BINDING_PROOF`, and
        the canonical TypedCodePoint path never emits
        `BoundaryCodePoint` (UnicodeQiyas rejects whitespace upstream).
        This method therefore cannot fire from a canonical pipeline; it
        survives only to keep legacy unit tests that build synthetic
        `BoundaryCodePoint` candidates from the testing convenience
        `TypedCodePointLayerAdapter.classify_codepoint(int)` green.
        """
        return self._prove_simple_position(
            BOUNDARY_EXCLUSION_PROOF,
            boundary_typed,
            index,
            sequence_length,
            extra_wasf=("boundary_excluded_from_slot",),
            illah_extra=("boundary_exclusion_licensed",),
            slug="boundary_exclusion",
            trace_prefix=trace_prefix,
        )

    # ----------------------------------------------------------- punctuation

    def prove_punctuation_exclusion(
        self,
        punct_typed: Candidate,
        index: int,
        sequence_length: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove punctuation is excluded from any slot (BoundaryEvidence)."""
        return self._prove_simple_position(
            PUNCTUATION_EXCLUSION_PROOF,
            punct_typed,
            index,
            sequence_length,
            extra_wasf=("punctuation_excluded_from_slot",),
            illah_extra=("punctuation_exclusion_licensed",),
            slug="punctuation_exclusion",
            trace_prefix=trace_prefix,
        )

    # ----------------------------------------------------------- residual

    def prove_residual_preservation(
        self,
        residual_typed: Candidate,
        index: int,
        sequence_length: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove an unclassified symbol is recorded, not silently dropped."""
        return self._prove_simple_position(
            RESIDUAL_PRESERVATION_PROOF,
            residual_typed,
            index,
            sequence_length,
            extra_wasf=("residual_preserved",),
            illah_extra=("residual_preservation_licensed",),
            slug="residual_preservation",
            trace_prefix=trace_prefix,
        )

    # ----------------------------------------------------------- sequence walk

    def prove_for_sequence(
        self,
        typed_sequence: Sequence[Candidate],
        trace_prefix: str = "",
    ) -> list[CandidateSet]:
        """
        Walk a sequence of TypedCodePoint candidates and emit one CTS
        proof per position. Returns one CandidateSet per input
        candidate, in order. Every symbol receives a position-context
        proof (CLAUDE.md §7 bullet "every symbol has position and
        context").

        For HarakaCodePoint at index i, the carrier search looks at the
        immediately previous typed candidate; harakat between letters
        are treated as transparent to carrier-lookback only if the
        caller chooses to do so — for this base layer the carrier is
        strictly the immediately-preceding LetterCodePoint, otherwise
        the haraka is orphan.
        """
        results: list[CandidateSet] = []
        n = len(typed_sequence)
        for i, typed in enumerate(typed_sequence):
            ctype = typed.candidate_type
            if ctype == "HarakaCodePoint":
                carrier = None
                if i > 0 and typed_sequence[i - 1].candidate_type == "LetterCodePoint":
                    carrier = typed_sequence[i - 1]
                cs = self.prove_carrier_binding(typed, carrier, i, n, trace_prefix)
            elif ctype == "LetterCodePoint":
                cs = self.prove_letter_position(typed, i, n, trace_prefix)
            elif ctype == "BoundaryCodePoint":
                # Z4 legacy unreachable in canonical path; see
                # prove_boundary_exclusion docstring.
                cs = self.prove_boundary_exclusion(typed, i, n, trace_prefix)
            elif ctype == "PunctuationCodePoint":
                cs = self.prove_punctuation_exclusion(typed, i, n, trace_prefix)
            elif ctype == "ResidualCodePoint":
                cs = self.prove_residual_preservation(typed, i, n, trace_prefix)
            else:
                # Defensive: an unknown typed-codepoint subtype is treated
                # as residual. The rule registry returns None for unknown
                # far_types, so we raise rather than silently drop.
                raise ValueError(
                    f"Unknown TypedCodePoint candidate_type at index {i}: {ctype!r}"
                )
            results.append(cs)
        return results

    # ----------------------------------------------------------- shared helper

    def _prove_simple_position(
        self,
        rule: QiyasRule,
        typed: Candidate,
        index: int,
        sequence_length: int,
        extra_wasf: tuple[str, ...],
        illah_extra: tuple[str, ...],
        slug: str,
        trace_prefix: str,
    ) -> CandidateSet:
        cp = _extract_codepoint(typed)
        cp_hex = f"{cp:04x}" if cp is not None else "unknown"
        if not trace_prefix:
            trace_prefix = f"cts:{slug}:{cp_hex}:{index}"

        asl = QiyasNodeRef(
            node_id="اصل:conditioned_typed_sequence_domain",
            node_type="ConditionedTypedSequenceDomain",
            identity_ids=("identity:conditioned_typed_sequence_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        far = QiyasNodeRef(
            node_id=f"فرع:{rule.far_type}:{cp_hex}:pos{index}",
            node_type=rule.far_type,
            identity_ids=typed.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=typed.rank,
        )

        # Map the rule's first required wasf to a generic
        # "has_<thing>_in_sequence" pattern.
        first_wasf = rule.required_effective_wasf[0]
        proves: list[str] = [
            "اصل:established",
            "فرع:determined",
            f"وصف:{first_wasf}:evidenced",
            "وصف:sequence_index_determined:evidenced",
        ]
        for w in extra_wasf:
            proves.append(f"وصف:{w}:evidenced")
        proves.append("علة:belongs_to_conditioned_typed_sequence_domain:verified")
        for ie in illah_extra:
            proves.append(f"علة:{ie}:verified")
        proves.extend([
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ])

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:cts:{slug}:{cp_hex}:{index}:{uuid.uuid4().hex[:8]}",
                    source_layer="ConditionedTypedSequenceQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )

        request = QiyasRequest(
            rule=rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="ConditionedTypedSequenceQiyas"),
        )
        return self.kernel.apply(request)

    def prove_for_sequence_with_context(
        self,
        typed_sequence,
        tokenizer_context=None,
        trace_prefix: str = "",
    ):
        """
        Walk a typed sequence enforcing segment-boundary constraints
        from SequenceContextTokenizer markers.

        Constitutional:
        - markers consumed as context only, never as Candidates or identities
        - boundary never converted to identity
        - cross-boundary haraka treated as orphan (carrier=None)
        - segment_id/token_index recorded in evidence, not identity
        """
        if tokenizer_context is None:
            return self.prove_for_sequence(typed_sequence, trace_prefix)

        position_to_segment: dict = {}
        for marker in tokenizer_context.markers:
            position_to_segment[marker.index] = marker.segment_id

        results = []
        n = len(typed_sequence)

        for i, typed in enumerate(typed_sequence):
            ctype = typed.candidate_type

            if ctype == "HarakaCodePoint":
                carrier = None
                boundary_claims: tuple = ()

                if i > 0 and typed_sequence[i - 1].candidate_type == "LetterCodePoint":
                    prev_seg = position_to_segment.get(i - 1)
                    curr_seg = position_to_segment.get(i)
                    if (prev_seg is not None
                            and curr_seg is not None
                            and prev_seg != curr_seg):
                        boundary_claims = (
                            "وصف:boundary_separation_detected:evidenced",
                            f"وصف:carrier_segment:{prev_seg}:haraka_segment:{curr_seg}:evidenced",
                        )
                    else:
                        carrier = typed_sequence[i - 1]

                cs = self._prove_carrier_binding_with_boundary(
                    typed, carrier, i, n, trace_prefix, boundary_claims
                )

            elif ctype == "LetterCodePoint":
                cs = self.prove_letter_position(typed, i, n, trace_prefix)
            elif ctype == "BoundaryCodePoint":
                # Z4 legacy unreachable in canonical path; see
                # prove_boundary_exclusion docstring. Boundary context
                # is consumed from `tokenizer_context.markers` above.
                cs = self.prove_boundary_exclusion(typed, i, n, trace_prefix)
            elif ctype == "PunctuationCodePoint":
                cs = self.prove_punctuation_exclusion(typed, i, n, trace_prefix)
            elif ctype == "ResidualCodePoint":
                cs = self.prove_residual_preservation(typed, i, n, trace_prefix)
            else:
                raise ValueError(
                    f"Unknown TypedCodePoint candidate_type at index {i}: {ctype!r}"
                )
            results.append(cs)
        return results

    def _prove_carrier_binding_with_boundary(
        self,
        haraka_typed,
        carrier_letter_typed,
        index: int,
        sequence_length: int,
        trace_prefix: str = "",
        boundary_context_claims: tuple = (),
    ):
        """
        Like prove_carrier_binding but injects auditable boundary-context
        claims (وصف:) into evidence. Blocking uses existing orphan fariq.
        boundary_context_claims are never fariq: claims — auditability only.
        """
        import uuid as _uuid
        from .evidence import Evidence, EvidenceSet
        from .kernel import QiyasContext, QiyasRequest
        from .node import QiyasNodeRef
        from .enums import EvidenceRank

        cp = _extract_codepoint(haraka_typed)
        cp_hex = f"{cp:04x}" if cp is not None else "unknown"
        if not trace_prefix:
            trace_prefix = f"cts:carrier_binding:{cp_hex}:{index}"

        asl = QiyasNodeRef(
            node_id="اصل:conditioned_typed_sequence_domain",
            node_type="ConditionedTypedSequenceDomain",
            identity_ids=("identity:conditioned_typed_sequence_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )
        far_identity = haraka_typed.identity_ids
        if carrier_letter_typed is not None:
            far_identity = far_identity + carrier_letter_typed.identity_ids
        far = QiyasNodeRef(
            node_id=f"فرع:haraka_codepoint:{cp_hex}:pos{index}",
            node_type="HarakaCodePoint",
            identity_ids=far_identity,
            trace_ids=(f"{trace_prefix}:far",),
            rank=haraka_typed.rank,
        )

        proves: list = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_haraka_in_sequence:evidenced",
            "وصف:sequence_index_determined:evidenced",
        ]
        for bc in boundary_context_claims:
            proves.append(bc)

        if carrier_letter_typed is not None:
            proves.extend([
                "وصف:preceded_by_letter_codepoint:evidenced",
                "وصف:carrier_alignment_determined:evidenced",
                "علة:carrier_binding_licensed:verified",
            ])
            if _is_tanwin(haraka_typed):
                terminal = (index == sequence_length - 1)
                proves.append(
                    "وصف:tanwin_terminal_sensitive:evidenced"
                    if terminal
                    else "وصف:tanwin_non_terminal_position:evidenced"
                )
            if _is_shadda(haraka_typed):
                proves.append("وصف:shadda_has_carrier:evidenced")
        else:
            proves.append("فارق:haraka_without_carrier:present")
            if _is_shadda(haraka_typed):
                proves.append("فارق:orphan_mark:present")

        proves.extend([
            "علة:belongs_to_conditioned_typed_sequence_domain:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ])

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:cts:cbwb:{cp_hex}:{index}:{_uuid.uuid4().hex[:8]}",
                    source_layer="ConditionedTypedSequenceQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",),
                ),
            )
        )
        request = QiyasRequest(
            rule=CARRIER_BINDING_PROOF,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="ConditionedTypedSequenceQiyas"),
        )
        return self.kernel.apply(request)

