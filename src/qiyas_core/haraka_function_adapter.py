"""
HarakaFunctionLayerAdapter — Gap #4 adapter.

Converts a HarakaCodePoint candidate into a HarakaFunctionCarrier by building
the full evidence set (vocalic_function, energy_profile) and invoking
QiyasKernel.apply().

Constitutional law enforced:
  HarakaFunctionCarrier ⊬ CaseEffect
  HarakaFunctionCarrier ⊬ I'rab
  HarakaFunctionCarrier ⊬ Hukm
(via forbidden_outputs in every HARAKA_FUNCTION rule)
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .phonetics import get_energy_profile
from .rules.haraka_function_rules import get_haraka_function_rule


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
class HarakaFunctionLayerAdapter:
    """
    Adapter that proves HarakaFunctionCarrier for a given HarakaCodePoint.

    Constitutional path:
        HarakaCodePoint → [HarakaFunctionLayerAdapter] → HarakaFunctionCarrier
    """

    kernel: QiyasKernel

    def build_request(
        self,
        haraka_candidate: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest for haraka function classification."""
        codepoint = _extract_codepoint(haraka_candidate)
        if codepoint is None:
            raise ValueError(
                "HarakaCodePoint candidate must have identity:codepoint:{hex} identity"
            )

        profile = get_energy_profile(codepoint)
        if profile is None:
            raise ValueError(
                f"No VocalicEnergyProfile for codepoint U+{codepoint:04X}"
            )

        rule = get_haraka_function_rule(codepoint)
        if rule is None:
            raise ValueError(
                f"No HarakaFunctionRule for codepoint U+{codepoint:04X}"
            )

        cp_hex = f"{codepoint:04x}"
        if not trace_prefix:
            trace_prefix = f"haraka_function:{cp_hex}"

        asl = QiyasNodeRef(
            node_id="asl:haraka_function_domain",
            node_type="HarakaFunctionDomain",
            identity_ids=("identity:haraka_function_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORM,
        )

        far = QiyasNodeRef(
            node_id=f"far:haraka_codepoint:{cp_hex}",
            node_type="HarakaCodePoint",
            identity_ids=haraka_candidate.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=haraka_candidate.rank,
        )

        proves = [
            "asl:established",
            "far:determined",
            "wasf:has_haraka_codepoint:evidenced",
            f"wasf:has_unicode_identity:{cp_hex}:evidenced",
            f"wasf:has_vocalic_function:{profile.vocalic_function.lower()}:evidenced",
            "illah:belongs_to_haraka_function_domain:verified",
            f"illah:haraka_function_is:{profile.arabic_name}:verified",
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
                    evidence_id=f"ev:haraka_function:{cp_hex}:{uuid.uuid4().hex[:8]}",
                    source_layer="HarakaFunctionQiyas",
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
            context=QiyasContext(layer="HarakaFunctionQiyas"),
        )

    def prove_haraka_function(
        self,
        haraka_candidate: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Prove the haraka function for a HarakaCodePoint candidate."""
        request = self.build_request(haraka_candidate, trace_prefix)
        return self.kernel.apply(request)

    def prove_from_codepoint(
        self,
        codepoint: int,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """
        Prove haraka function from a raw codepoint.

        **WARNING: convenience/testing method only.**
        """
        cp_hex = f"{codepoint:04x}"
        haraka_candidate = Candidate(
            candidate_id=f"haraka_codepoint:{cp_hex}",
            candidate_type="HarakaCodePoint",
            status=CandidateStatus.ACCEPTED,
            layer="TypedCodePointClassificationQiyas",
            source_rule_id="typed_codepoint.haraka_classification",
            asl_id="asl:typed_codepoint_classification_domain",
            far_id=f"far:unicode_candidate:{cp_hex}",
            identity_ids=(f"identity:codepoint:{cp_hex}",),
            rank=EvidenceRank.FORM,
            residuals=(),
            trace_ids=(f"test:haraka_codepoint:{cp_hex}",),
            output_flags=frozenset(),
        )
        return self.prove_haraka_function(haraka_candidate, trace_prefix)
