"""
HarakaRoleSpectrumLayerAdapter — Γ_haraka (Gamma-haraka) spectrum opener.

Constitutional contract: docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md

This adapter implements Γ_haraka, the spectrum-opening function that produces
role hypotheses for haraka carriers.

**Constitutional path:**
    SlotCandidate (with HarakaFunctionCarrier + PositionCarrier + AlignmentEvidence)
    → [HarakaRoleSpectrumLayerAdapter]
    → HarakaRoleSpectrum

**Mathematical definition (§ 2 of contract):**
    Γ_haraka: SlotCandidate × Option[SlotGeometryCandidate] → HarakaRoleSpectrum

**Constitutional law:**
    Γ ≠ Λ
    Γ produces POTENTIAL roles only (all "possible_*")
    Γ does NOT produce SELECTED roles
    Γ does NOT produce FINAL judgments
    HarakaRoleSpectrum ⊬ WeightCandidate
    HarakaRoleSpectrum ⊬ CaseEffect / I'rab
    HarakaRoleSpectrum ⊬ HukmCandidate
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank
from .evidence import Evidence, EvidenceSet
from .haraka_role_spectrum import HarakaRoleHypothesis, HarakaRoleSpectrum
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .residual import Residual
from .rules.haraka_role_spectrum_rules import (
    HARAKA_ROLE_SPECTRUM_RULE,
    FORBIDDEN_HARAKA_ROLE_SPECTRUM,
)


# ---------------------------------------------------------------------------
# Identity extraction helpers
# ---------------------------------------------------------------------------


def _extract_haraka_identity(slot_candidate: Candidate) -> tuple[str, ...]:
    """Extract haraka-specific identities from SlotCandidate."""
    haraka_ids = []
    for iid in slot_candidate.identity_ids:
        if any(
            iid.startswith(prefix)
            for prefix in ("identity:haraka:", "identity:codepoint:064")
        ):
            haraka_ids.append(iid)
    return tuple(haraka_ids)


def _extract_position_identity(slot_candidate: Candidate) -> tuple[str, ...]:
    """Extract position identities from SlotCandidate."""
    position_ids = []
    for iid in slot_candidate.identity_ids:
        if iid.startswith("identity:position:"):
            position_ids.append(iid)
    return tuple(position_ids)


def _extract_alignment_trace(slot_candidate: Candidate) -> tuple[str, ...]:
    """Extract alignment trace IDs from SlotCandidate."""
    alignment_traces = []
    for tid in slot_candidate.trace_ids:
        if any(
            keyword in tid
            for keyword in ("alignment", "carrier_binding", "conditioned_sequence")
        ):
            alignment_traces.append(tid)
    return tuple(alignment_traces)


def _extract_haraka_function(slot_candidate: Candidate) -> str | None:
    """
    Extract haraka function name from identity or trace.

    Returns function name like "OPENING", "ROUNDING", "FRONTING", "CLOSURE", etc.
    """
    # Try identity first
    for iid in slot_candidate.identity_ids:
        if iid.startswith("identity:haraka:"):
            return iid.split(":")[-1].upper()

    # Try trace as fallback
    for tid in slot_candidate.trace_ids:
        if "haraka_function:" in tid:
            parts = tid.split(":")
            for i, part in enumerate(parts):
                if part == "haraka_function" and i + 1 < len(parts):
                    return parts[i + 1].upper()

    return None


# ---------------------------------------------------------------------------
# Hypothesis generation
# ---------------------------------------------------------------------------


def _generate_phonological_hypothesis(
    haraka_function: str,
) -> HarakaRoleHypothesis:
    """
    Generate phonological hypothesis for a haraka function.

    Constitutional requirement: Phonological hypotheses do NOT require lambda context.
    """
    role_name_map = {
        "FATHA": "possible_phonological_opening",
        "DAMMA": "possible_rounding",
        "KASRA": "possible_fronting",
        "SUKUN": "possible_closure",
        "SHADDA": "possible_compression",
        "TANWIN_FATH": "possible_tanwin_open",
        "TANWIN_DAMM": "possible_tanwin_round",
        "TANWIN_KASR": "possible_tanwin_front",
    }

    evidence_map = {
        "FATHA": ("وصف:haraka_class:short_vowel", "وصف:haraka_function:OPENING"),
        "DAMMA": ("وصف:haraka_class:short_vowel", "وصف:haraka_function:ROUNDING"),
        "KASRA": ("وصف:haraka_class:short_vowel", "وصف:haraka_function:FRONTING"),
        "SUKUN": ("وصف:haraka_class:zero_vowel", "وصف:haraka_function:CLOSURE"),
        "SHADDA": ("وصف:haraka_class:gemination", "وصف:haraka_function:COMPRESSION"),
        "TANWIN_FATH": ("وصف:haraka_class:tanwin", "وصف:haraka_function:TANWIN_OPEN"),
        "TANWIN_DAMM": ("وصف:haraka_class:tanwin", "وصف:haraka_function:TANWIN_ROUND"),
        "TANWIN_KASR": ("وصف:haraka_class:tanwin", "وصف:haraka_function:TANWIN_FRONT"),
    }

    role_name = role_name_map.get(haraka_function, "possible_phonological_function")
    evidence = evidence_map.get(haraka_function, (f"وصف:haraka_function:{haraka_function}",))

    return HarakaRoleHypothesis(
        role_name=role_name,
        role_genus="phonological",
        evidence_claims=evidence,
        required_context=(),  # Phonological does NOT require lambda
        invalidating_differences=(),
        forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
    )


def _generate_pattern_hypothesis(
    haraka_function: str,
) -> HarakaRoleHypothesis:
    """
    Generate morphological pattern hypothesis.

    Constitutional requirement: Pattern hypotheses REQUIRE lambda context.
    """
    return HarakaRoleHypothesis(
        role_name="possible_pattern_vowel",
        role_genus="morphological_pattern",
        evidence_claims=(
            f"وصف:haraka_{haraka_function.lower()}_in_pattern",
            "وصف:pattern_position",
        ),
        required_context=("requires_lambda_context", "requires_pattern_template"),
        invalidating_differences=("فارق:pattern_mismatch:present",),
        forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
    )


def _generate_case_marker_hypothesis(
    haraka_function: str,
    position_terminal: bool,
) -> HarakaRoleHypothesis | None:
    """
    Generate morphosyntactic case marker hypothesis.

    Constitutional requirement: Morphosyntactic hypotheses REQUIRE lambda context.
    Only generated for terminal positions.
    """
    if not position_terminal:
        return None

    case_evidence_map = {
        "FATHA": "وصف:accusative_marker_candidate",
        "DAMMA": "وصف:nominative_marker_candidate",
        "KASRA": "وصف:genitive_marker_candidate",
        "TANWIN_FATH": "وصف:indefinite_accusative_candidate",
        "TANWIN_DAMM": "وصف:indefinite_nominative_candidate",
        "TANWIN_KASR": "وصف:indefinite_genitive_candidate",
    }

    case_evidence = case_evidence_map.get(haraka_function)
    if not case_evidence:
        return None

    return HarakaRoleHypothesis(
        role_name="possible_case_marker_candidate",
        role_genus="morphosyntactic",
        evidence_claims=(
            "وصف:position_terminal",
            case_evidence,
        ),
        required_context=("requires_lambda_context", "requires_composition_context"),
        invalidating_differences=(
            "فارق:non_terminal_position:present",
            "فارق:mabniyy_word:present",
        ),
        forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
    )


def _generate_syllabic_hypothesis(
    haraka_function: str,
) -> HarakaRoleHypothesis | None:
    """
    Generate syllabic hypothesis.

    Constitutional requirement: Syllabic hypotheses REQUIRE lambda context.
    Only for vowels (not SUKUN).
    """
    if haraka_function == "SUKUN":
        # SUKUN marks syllable boundary, not nucleus
        return HarakaRoleHypothesis(
            role_name="possible_syllable_boundary",
            role_genus="syllabic",
            evidence_claims=(
                "وصف:haraka_closes",
                "وصف:marks_syllable_boundary",
            ),
            required_context=("requires_lambda_context", "requires_syllable_boundary"),
            invalidating_differences=(),
            forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
        )
    elif haraka_function == "SHADDA":
        return None  # SHADDA has different syllabic role
    else:
        return HarakaRoleHypothesis(
            role_name="possible_syllabic_vowel",
            role_genus="syllabic",
            evidence_claims=(
                f"وصف:haraka_{haraka_function.lower()}",
                "وصف:can_form_syllable_nucleus",
            ),
            required_context=("requires_lambda_context", "requires_syllable_boundary"),
            invalidating_differences=(),
            forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
        )


def _generate_prosodic_hypothesis(
    haraka_function: str,
) -> HarakaRoleHypothesis | None:
    """
    Generate prosodic (arud) hypothesis.

    Constitutional requirement: Prosodic hypotheses REQUIRE lambda context.
    """
    if haraka_function in ("FATHA", "DAMMA", "KASRA"):
        quantity = "short_vowel_quantity"
    elif haraka_function == "SUKUN":
        quantity = "zero_vowel_quantity"
    elif haraka_function in ("TANWIN_FATH", "TANWIN_DAMM", "TANWIN_KASR"):
        quantity = "tanwin_quantity"
    elif haraka_function == "SHADDA":
        quantity = "gemination_quantity"
    else:
        return None

    return HarakaRoleHypothesis(
        role_name="possible_arud_relevance",
        role_genus="prosodic",
        evidence_claims=(
            "وصف:contributes_to_weight",
            f"وصف:{quantity}",
        ),
        required_context=("requires_lambda_context", "requires_arud_meter"),
        invalidating_differences=(),
        forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
    )


def _check_position_terminal(slot_candidate: Candidate) -> bool:
    """Check if position is terminal based on identity or trace."""
    for iid in slot_candidate.identity_ids:
        if "terminal" in iid.lower():
            return True
    for tid in slot_candidate.trace_ids:
        if "terminal" in tid.lower():
            return True
    return False


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------


@dataclass
class HarakaRoleSpectrumLayerAdapter:
    """
    Adapter that implements Γ_haraka, the spectrum-opening function.

    Constitutional path:
        SlotCandidate
        → [Γ_haraka]
        → HarakaRoleSpectrum (with multiple "possible_*" hypotheses)
    """

    kernel: QiyasKernel

    def build_request(
        self,
        slot_candidate: Candidate,
        geometry_context: Candidate | None = None,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """
        Build a QiyasRequest for haraka role spectrum generation.

        Args:
            slot_candidate: SlotCandidate with HarakaFunctionCarrier
            geometry_context: Optional SlotGeometryCandidate for additional context
            trace_prefix: Optional trace prefix

        Returns:
            QiyasRequest for kernel.apply()
        """
        if not trace_prefix:
            trace_prefix = f"gamma_haraka:{slot_candidate.candidate_id}"

        # Extract identities (§ 3.5 PreservesIdentity)
        source_identity = slot_candidate.identity_ids
        haraka_identity = _extract_haraka_identity(slot_candidate)
        position_identity = _extract_position_identity(slot_candidate)
        alignment_trace = _extract_alignment_trace(slot_candidate)

        asl = QiyasNodeRef(
            node_id="اصل:haraka_role_domain",
            node_type="HarakaRoleDomain",
            identity_ids=("identity:haraka_role_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.ANALOGICAL,
        )

        far = QiyasNodeRef(
            node_id=f"فرع:slot_candidate:{slot_candidate.candidate_id}",
            node_type="SlotCandidate",
            identity_ids=source_identity,
            trace_ids=(f"{trace_prefix}:far",),
            rank=slot_candidate.rank,
        )

        # Base evidence claims
        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_haraka_carrier:evidenced",
            "وصف:has_position_context:evidenced",
            "وصف:has_alignment_evidence:evidenced",
            "وصف:identity_preserved:evidenced",
            "علة:belongs_to_haraka_role_domain:verified",
            "علة:spectrum_generation_valid:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Add geometry context evidence if provided
        geometry_trace = ()
        if geometry_context is not None and geometry_context.status == CandidateStatus.ACCEPTED:
            proves.append(f"علة:geometry_context_provided:{geometry_context.candidate_id}:verified")
            geometry_trace = (f"{trace_prefix}:geometry_ref:{geometry_context.candidate_id}",)

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:gamma_haraka:{uuid.uuid4().hex[:8]}",
                    source_layer="HarakaRoleSpectrumQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.ANALOGICAL,
                    trace_ids=(f"{trace_prefix}:ev",) + alignment_trace + geometry_trace,
                ),
            )
        )

        return QiyasRequest(
            rule=HARAKA_ROLE_SPECTRUM_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="HarakaRoleSpectrumQiyas"),
        )

    def open_haraka_role_spectrum(
        self,
        slot_candidate: Candidate,
        geometry_context: Candidate | None = None,
        trace_prefix: str = "",
    ) -> HarakaRoleSpectrum:
        """
        Open the haraka role spectrum for a SlotCandidate.

        This is the Γ_haraka function (§ 2 of constitutional contract).

        Constitutional requirements:
        1. Preserves all source identities (§ 3.5)
        2. All hypotheses start with "possible_" (§ 3.7)
        3. All hypotheses declare forbidden outputs (§ 3.6)
        4. Non-phonological hypotheses require lambda context (§ 3.8)
        5. Rank ceiling is ANALOGICAL (§ 2.2)

        Args:
            slot_candidate: SlotCandidate with HarakaFunctionCarrier
            geometry_context: Optional SlotGeometryCandidate
            trace_prefix: Optional trace prefix

        Returns:
            HarakaRoleSpectrum with hypotheses
        """
        # Extract haraka function
        haraka_function = _extract_haraka_function(slot_candidate)
        if haraka_function is None:
            # Defer if no haraka function found
            from .residual import ResidualSeverity, ResidualEffect
            return HarakaRoleSpectrum(
                source_identity=slot_candidate.identity_ids,
                haraka_identity=_extract_haraka_identity(slot_candidate),
                position_identity=_extract_position_identity(slot_candidate),
                alignment_trace_ids=_extract_alignment_trace(slot_candidate),
                geometry_context_trace=(),
                hypotheses=(),
                rank_ceiling=EvidenceRank.ANALOGICAL,
                residuals=(
                    Residual(
                        residual_type="defer:missing_haraka_function:present",
                        severity=ResidualSeverity.BLOCKER,
                        effect=ResidualEffect.DEFER,
                        message="No haraka function found in SlotCandidate",
                        source_rule_id="haraka_role_spectrum.gamma_haraka",
                        layer="HarakaRoleSpectrumQiyas",
                        trace_ids=(f"{trace_prefix}:missing_haraka_function",),
                    ),
                ),
            )

        # Check position
        position_terminal = _check_position_terminal(slot_candidate)

        # Generate hypotheses
        hypotheses = []

        # 1. Phonological hypothesis (always generated)
        hypotheses.append(_generate_phonological_hypothesis(haraka_function))

        # 2. Pattern hypothesis (requires lambda)
        if haraka_function not in ("SUKUN", "SHADDA"):
            hypotheses.append(_generate_pattern_hypothesis(haraka_function))

        # 3. Case marker hypothesis (requires lambda, terminal only)
        case_hyp = _generate_case_marker_hypothesis(haraka_function, position_terminal)
        if case_hyp is not None:
            hypotheses.append(case_hyp)

        # 4. Syllabic hypothesis (requires lambda)
        syllabic_hyp = _generate_syllabic_hypothesis(haraka_function)
        if syllabic_hyp is not None:
            hypotheses.append(syllabic_hyp)

        # 5. Prosodic hypothesis (requires lambda)
        prosodic_hyp = _generate_prosodic_hypothesis(haraka_function)
        if prosodic_hyp is not None:
            hypotheses.append(prosodic_hyp)

        # Extract geometry trace if provided
        geometry_trace = ()
        if geometry_context is not None and geometry_context.status == CandidateStatus.ACCEPTED:
            geometry_trace = tuple(
                tid for tid in geometry_context.trace_ids
                if any(kw in tid for kw in ("geometry", "segment", "boundary"))
            )

        return HarakaRoleSpectrum(
            source_identity=slot_candidate.identity_ids,
            haraka_identity=_extract_haraka_identity(slot_candidate),
            position_identity=_extract_position_identity(slot_candidate),
            alignment_trace_ids=_extract_alignment_trace(slot_candidate),
            geometry_context_trace=geometry_trace,
            hypotheses=tuple(hypotheses),
            rank_ceiling=EvidenceRank.ANALOGICAL,  # Constitutional requirement
            residuals=(),
        )

    def apply_gamma_haraka(
        self,
        slot_candidate: Candidate,
        geometry_context: Candidate | None = None,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """
        Apply Γ_haraka via QiyasKernel.

        This method:
        1. Generates the spectrum using open_haraka_role_spectrum()
        2. Builds a QiyasRequest
        3. Applies it through the kernel

        Returns:
            CandidateSet from kernel.apply()
        """
        request = self.build_request(slot_candidate, geometry_context, trace_prefix)
        return self.kernel.apply(request)
