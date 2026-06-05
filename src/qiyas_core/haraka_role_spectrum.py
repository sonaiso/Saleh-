"""
Haraka Role Spectrum — Γ_haraka data structures (Phase 2).

Constitutional contract: docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md

This module implements the data containers for Γ_haraka (Gamma-haraka),
the spectrum-opening function that produces role hypotheses for haraka carriers.

Phase 2 scope (this PR):
  ✓ HarakaRoleDomain enum
  ✓ HarakaRoleHypothesis dataclass
  ✓ HarakaRoleSpectrum dataclass
  ✓ FORBIDDEN_HARAKA_ROLE_SPECTRUM constant

Phase 3 scope (future PR):
  ✗ No adapter implementation
  ✗ No rules implementation
  ✗ No QiyasKernel.apply integration
  ✗ No Lambda (Λ) implementation

Constitutional principle:
  Γ ≠ Λ
  Γ = Spectrum opener (hypothesis generator)
  Λ = Selector (context-dependent chooser, FUTURE)
"""

from dataclasses import dataclass
from enum import Enum

from .enums import EvidenceRank
from .residual import Residual


class HarakaRoleDomain(str, Enum):
    """
    Domain for haraka role spectrum generation.

    Constitutional basis: HARAKA_ROLE_SPECTRUM_CONTRACT.md § 2.2

    This domain is SEPARATE from:
    - Phonological domain (Layer 2B HarakaFunctionCarrier)
    - Morphological domain (future Wazn layer)
    - Syntactic domain (future I'rab layer)
    - Prosodic domain (future 'Arud layer)

    HarakaRoleDomain produces POTENTIAL roles only.
    """

    HARAKA_ROLE_SPECTRUM = "haraka_role_spectrum"


@dataclass(frozen=True)
class HarakaRoleHypothesis:
    """
    Single hypothesis in a haraka role spectrum.

    Constitutional basis: HARAKA_ROLE_SPECTRUM_CONTRACT.md § 2.3

    A hypothesis represents ONE POTENTIAL role that a haraka may play
    in a specific linguistic domain (phonological, morphological, syntactic,
    prosodic, syllabic).

    Constitutional constraints:
    1. role_name MUST start with "possible_" (§ 3.7)
    2. forbidden_outputs MUST include at minimum:
       - All hypotheses: ("HukmCandidate", "RealityClaim", "FinalMeaning")
       - Morphosyntactic: + ("CaseEffect", "Irab", "FinalCaseJudgment")
       - Pattern: + ("WeightCandidate", "FinalPattern")
       - Prosodic: + ("ArudCandidate", "FinalMeterJudgment")
    3. Non-phonological hypotheses MUST declare "requires_lambda_context" (§ 3.8)

    Example:
        HarakaRoleHypothesis(
            role_name="possible_case_marker_candidate",
            role_genus="morphosyntactic",
            evidence_claims=(
                "وصف:position_terminal",
                "وصف:haraka_marks_ending",
            ),
            required_context=("requires_lambda_context", "requires_composition_context"),
            invalidating_differences=("فارق:non_terminal_position:present",),
            forbidden_outputs=("CaseEffect", "Irab", "FinalCaseJudgment"),
        )
    """

    role_name: str
    """Name of the potential role. MUST start with 'possible_'."""

    role_genus: str
    """
    Genus of the role hypothesis.

    Valid genera:
    - "phonological" — phonetic function (OPENING, CLOSING, etc.)
    - "morphological_pattern" — pattern vowel role
    - "morphosyntactic" — case/mood/indefiniteness marker candidate
    - "syntactic" — syntactic relevance (idafa, etc.)
    - "syllabic" — syllable nucleus or boundary relevance
    - "prosodic" — prosodic weight relevance (arud)
    - "phonological_boundary" — waqf/pause relevance
    - "morphological" — morpheme boundary relevance
    """

    evidence_claims: tuple[str, ...]
    """
    Evidence supporting this hypothesis.

    Evidence claims use Arabic-prefixed format:
    - وصف:{attribute}:{value}
    - علة:{cause}:{value}

    Example:
        ("وصف:position_terminal", "وصف:haraka_marks_ending")
    """

    required_context: tuple[str, ...]
    """
    Context requirements for this hypothesis.

    Non-phonological hypotheses MUST include "requires_lambda_context".

    Common context requirements:
    - "requires_lambda_context" — requires Λ selector (all non-phonological)
    - "requires_pattern_template" — requires wazn pattern
    - "requires_composition_context" — requires i'rab context
    - "requires_syllable_boundary" — requires syllable template
    - "requires_arud_meter" — requires 'arud meter
    - "requires_waqf_pattern" — requires waqf context
    - "requires_verb_context" — requires verb context (jazm)
    - "requires_noun_context" — requires noun context (tanwin)
    - "requires_idafa_context" — requires idafa context
    - "requires_morpheme_boundary" — requires morpheme boundary
    """

    invalidating_differences: tuple[str, ...]
    """
    Invalidating differences that block this hypothesis.

    Uses فارق:{difference}:present format.

    Example:
        ("فارق:non_terminal_position:present", "فارق:mabniyy_word:present")
    """

    forbidden_outputs: tuple[str, ...]
    """
    Forbidden outputs for this hypothesis.

    MUST include constitutional base:
        ("HukmCandidate", "RealityClaim", "FinalMeaning")

    Plus genus-specific forbidden outputs:
    - Morphosyntactic: + ("CaseEffect", "Irab", "FinalCaseJudgment")
    - Pattern: + ("WeightCandidate", "FinalPattern")
    - Prosodic: + ("ArudCandidate", "FinalMeterJudgment")
    - Syllabic: + ("FinalSyllable",)
    - Morphological: + ("FinalMorphologicalJudgment",)
    - Syntactic: + ("FinalIdafaJudgment",)
    - Phonological_boundary: + ("FinalWaqfJudgment",)
    """


@dataclass(frozen=True)
class HarakaRoleSpectrum:
    """
    Spectrum of potential roles for a haraka.

    Constitutional basis: HARAKA_ROLE_SPECTRUM_CONTRACT.md § 2.2

    This is the output of Γ_haraka (Gamma-haraka), the spectrum-opening function.

    Constitutional constraints:
    1. source_identity MUST be preserved from SlotCandidate (§ 3.5)
    2. haraka_identity MUST be subset of SlotCandidate.identity_ids (§ 3.5)
    3. All hypotheses MUST have role_name starting with "possible_" (§ 3.7)
    4. All hypotheses MUST declare forbidden_outputs (§ 3.6)
    5. Non-phonological hypotheses MUST require lambda context (§ 3.8)
    6. rank_ceiling MUST be EvidenceRank.ANALOGICAL (§ 2.2)
    7. Output candidate type MUST be "HarakaRoleSpectrum" (§ 3.7)

    Example:
        HarakaRoleSpectrum(
            source_identity=("identity:codepoint:U+064E", "identity:haraka:fatha"),
            haraka_identity=("identity:haraka:fatha",),
            position_identity=("identity:position:P0",),
            alignment_trace_ids=("trace:carrier_binding:valid",),
            geometry_context_trace=(),
            hypotheses=(
                # phonological hypothesis
                HarakaRoleHypothesis(
                    role_name="possible_phonological_opening",
                    role_genus="phonological",
                    ...
                ),
                # morphosyntactic hypothesis
                HarakaRoleHypothesis(
                    role_name="possible_case_marker_candidate",
                    role_genus="morphosyntactic",
                    required_context=("requires_lambda_context", ...),
                    ...
                ),
            ),
            rank_ceiling=EvidenceRank.ANALOGICAL,
            residuals=(),
        )
    """

    source_identity: tuple[str, ...]
    """
    Source identity from SlotCandidate.

    MUST preserve all identity_ids from the input SlotCandidate.
    Constitutional requirement: § 3.5 PreservesIdentity.
    """

    haraka_identity: tuple[str, ...]
    """
    Haraka-specific identity.

    MUST be subset of source_identity.
    Contains identity references like:
    - "identity:codepoint:U+064E"
    - "identity:haraka:fatha"
    - "identity:haraka_function:opening"
    """

    position_identity: tuple[str, ...]
    """
    Position identity from PositionCarrier.

    Contains identity references like:
    - "identity:position:P0"
    - "identity:position:terminal"
    - "identity:position:medial"
    """

    alignment_trace_ids: tuple[str, ...]
    """
    Alignment trace from AlignmentEvidence.

    Contains trace references like:
    - "trace:carrier_binding:valid"
    - "trace:alignment:evidenced"
    - "trace:conditioned_sequence:admitted"
    """

    geometry_context_trace: tuple[str, ...]
    """
    Optional geometry context trace from SlotGeometryCandidate.

    When SlotGeometry is provided as optional context, contains:
    - "trace:geometry_length:{n}"
    - "trace:position_in_geometry:{position}"
    - "trace:adjacent_boundaries:{bool}"
    - "trace:segment_transition:{bool}"

    When SlotGeometry is NOT provided, this is empty tuple.
    """

    hypotheses: tuple[HarakaRoleHypothesis, ...]
    """
    The spectrum of potential roles.

    This is the core output of Γ_haraka.

    Constitutional requirement: All hypotheses MUST:
    1. Have role_name starting with "possible_"
    2. Declare forbidden_outputs
    3. Include "requires_lambda_context" for non-phonological roles
    """

    rank_ceiling: EvidenceRank
    """
    Rank ceiling for the spectrum.

    MUST be EvidenceRank.ANALOGICAL (constitutional requirement § 2.2).

    Γ_haraka produces analogical/candidate-level outputs only.
    ANALOGICAL (rank 2) represents qiyas-based hypotheses.
    """

    residuals: tuple[Residual, ...]
    """
    Residuals from spectrum generation.

    May contain:
    - Deferred residuals if spectrum generation is blocked
    - Trace residuals preserving non-selected evidence
    - Blocking residuals if constitutional constraints are violated
    """
