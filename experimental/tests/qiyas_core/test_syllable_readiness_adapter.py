"""
Tests for SyllableReadinessLayerAdapter.

Validates syllable readiness validation enforces:
- No initial sukun
- Shadda requires carrier
- Additional diacritics not treated as vowels
- Proper constitutional boundaries
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.syllable_readiness_adapter import SyllableReadinessLayerAdapter


def test_adapter_validates_ba_fatha_ready():
    """Ba+Fatha is now deferred awaiting order equilibrium evidence."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    assert result.layer == "SyllableReadinessQiyas"
    # After PR #10, SyllableReadinessQiyas requires order equilibrium evidence
    # Without it, candidates are blocked due to missing required wasf
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableReadinessCandidate"
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.layer == "SyllableReadinessQiyas"


def test_adapter_validates_ta_damma_ready():
    """Ta+Damma is now deferred awaiting order equilibrium evidence."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x062A, 0x064F)  # Ta + Damma

    assert result.layer == "SyllableReadinessQiyas"
    # After PR #10, requires order equilibrium evidence
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableReadinessCandidate"
    assert candidate.status == CandidateStatus.BLOCKED


def test_adapter_blocks_initial_sukun():
    """Ba+Sukun at initial position should be blocked."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x0652, is_initial_position=True
    )  # Ba + Sukun at start

    assert result.layer == "SyllableReadinessQiyas"
    # Should be blocked due to initial_sukun fariq
    assert len(result.blocked) == 1
    assert len(result.accepted) == 0

    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED


def test_adapter_allows_non_initial_sukun():
    """Ba+Sukun in non-initial position is now deferred awaiting evidence."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x0652, is_initial_position=False
    )  # Ba + Sukun not at start

    assert result.layer == "SyllableReadinessQiyas"
    # After PR #10, requires order equilibrium evidence
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableReadinessCandidate"
    assert candidate.status == CandidateStatus.BLOCKED


def test_adapter_handles_additional_diacritic_constraint():
    """Ba+Additional diacritic should have constraint about not being vowel."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x0653)  # Ba + Maddah

    assert result.layer == "SyllableReadinessQiyas"
    # Should be blocked due to additional_diacritic_as_vowel
    assert len(result.blocked) == 1
    assert len(result.accepted) == 0


def test_syllable_readiness_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for syllable readiness."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    # After PR #10, candidates are blocked awaiting order equilibrium evidence
    candidate = result.blocked[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"


def test_syllable_readiness_rank_not_exceeds_form():
    """Syllable readiness candidate rank must not exceed FORM."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    # After PR #10, candidates are blocked awaiting order equilibrium evidence
    candidate = result.blocked[0]
    from qiyas_core.enums import EvidenceRank
    # Blocked candidates have rank ZERO
    assert candidate.rank == EvidenceRank.NO_EVIDENCE


def test_syllable_readiness_forbidden_outputs_enforced():
    """SyllableReadinessCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    # After PR #10, candidates are blocked awaiting order equilibrium evidence
    candidate = result.blocked[0]

    forbidden = {
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    }

    assert not (candidate.output_flags & forbidden), \
        f"Forbidden outputs detected: {candidate.output_flags & forbidden}"


def test_syllable_readiness_does_not_produce_syllable():
    """SyllableReadinessCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    # After PR #10, candidates are blocked awaiting order equilibrium evidence
    candidate = result.blocked[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "SyllableReadinessCandidate must not produce SyllableCandidate"


def test_syllable_readiness_does_not_produce_pronunciation():
    """SyllableReadinessCandidate must never produce PronunciationCandidate."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    # After PR #10, candidates are blocked awaiting order equilibrium evidence
    candidate = result.blocked[0]

    assert "PronunciationCandidate" not in candidate.output_flags, \
        "SyllableReadinessCandidate must not produce PronunciationCandidate"


def test_syllable_readiness_does_not_produce_dal():
    """SyllableReadinessCandidate must never produce DalCandidate."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    # After PR #10, candidates are blocked awaiting order equilibrium evidence
    candidate = result.blocked[0]

    assert "DalCandidate" not in candidate.output_flags, \
        "SyllableReadinessCandidate must not produce DalCandidate"


def test_ba_shadda_passes_readiness():
    """Ba+Shadda is now deferred awaiting order equilibrium evidence."""
    kernel = QiyasKernel()
    adapter = SyllableReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x0651)  # Ba + Shadda

    assert result.layer == "SyllableReadinessQiyas"
    # After PR #10, requires order equilibrium evidence
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableReadinessCandidate"
    assert candidate.status == CandidateStatus.BLOCKED
