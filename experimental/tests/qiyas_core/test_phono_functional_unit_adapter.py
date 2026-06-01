"""
Tests for PhonoFunctionalUnitLayerAdapter.

Validates that phono-functional unit binding correctly combines:
- Carrier function candidates
- Mark function candidates
Into unified phonotactic units without producing syllables.
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.phono_functional_unit_adapter import PhonoFunctionalUnitLayerAdapter


def test_adapter_processes_ba_fatha_binding():
    """Adapter should produce PhonoFunctionalUnitCandidate for Ba+Fatha."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    assert result.layer == "PhonoFunctionalUnitQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "PhonoFunctionalUnitCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.layer == "PhonoFunctionalUnitQiyas"


def test_adapter_processes_ta_damma_binding():
    """Adapter should produce PhonoFunctionalUnitCandidate for Ta+Damma."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x062A, 0x064F)  # Ta + Damma

    assert result.layer == "PhonoFunctionalUnitQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "PhonoFunctionalUnitCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_adapter_processes_ba_shadda_binding():
    """Adapter should produce PhonoFunctionalUnitCandidate for Ba+Shadda."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x0651)  # Ba + Shadda

    assert result.layer == "PhonoFunctionalUnitQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "PhonoFunctionalUnitCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_adapter_processes_ba_sukun_binding():
    """Adapter should produce PhonoFunctionalUnitCandidate for Ba+Sukun."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x0652)  # Ba + Sukun

    assert result.layer == "PhonoFunctionalUnitQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "PhonoFunctionalUnitCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_phono_functional_unit_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for phono-functional unit."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"


def test_phono_functional_unit_rank_not_exceeds_form():
    """Phono-functional unit candidate rank must not exceed FORM."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    candidate = result.accepted[0]
    from qiyas_core.enums import EvidenceRank
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE


def test_phono_functional_unit_forbidden_outputs_enforced():
    """PhonoFunctionalUnitCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    candidate = result.accepted[0]

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


def test_phono_functional_unit_does_not_produce_syllable():
    """PhonoFunctionalUnitCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "PhonoFunctionalUnitCandidate must not produce SyllableCandidate"


def test_phono_functional_unit_does_not_produce_pronunciation():
    """PhonoFunctionalUnitCandidate must never produce PronunciationCandidate."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    candidate = result.accepted[0]

    assert "PronunciationCandidate" not in candidate.output_flags, \
        "PhonoFunctionalUnitCandidate must not produce PronunciationCandidate"


def test_phono_functional_unit_does_not_produce_dal():
    """PhonoFunctionalUnitCandidate must never produce DalCandidate."""
    kernel = QiyasKernel()
    adapter = PhonoFunctionalUnitLayerAdapter(kernel=kernel)

    result = adapter.process_binding(0x0628, 0x064E)  # Ba + Fatha

    candidate = result.accepted[0]

    assert "DalCandidate" not in candidate.output_flags, \
        "PhonoFunctionalUnitCandidate must not produce DalCandidate"
