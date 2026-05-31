"""Candidate factories for constitutional tests."""

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank


def make_unicode_candidate(
    candidate_id: str = "cand:unicode:1",
    *,
    status: CandidateStatus = CandidateStatus.ACCEPTED,
    identity_ids: tuple[str, ...] = ("id:unicode:1",),
    trace_ids: tuple[str, ...] = (),
    rank: EvidenceRank = EvidenceRank.FORM,
    output_flags: frozenset[str] = frozenset(),
) -> Candidate:
    """Create a UnicodeCandidate for testing.

    Args:
        candidate_id: Unique candidate identifier
        status: Candidate status
        identity_ids: Identity IDs
        trace_ids: Trace IDs from ancestors
        rank: Evidence rank
        output_flags: Output flags

    Returns:
        Candidate representing a UnicodeCandidate
    """
    return Candidate(
        candidate_id=candidate_id,
        candidate_type="UnicodeCandidate",
        status=status,
        layer="UnicodeQiyas",
        source_rule_id="rule:unicode",
        asl_id="asl:unicode",
        far_id="far:unicode",
        identity_ids=identity_ids,
        rank=rank,
        residuals=(),
        trace_ids=trace_ids,
        output_flags=output_flags,
    )


def make_haraka_candidate(
    candidate_id: str = "cand:haraka:1",
    *,
    status: CandidateStatus = CandidateStatus.ACCEPTED,
    identity_ids: tuple[str, ...] = ("id:haraka:1",),
    trace_ids: tuple[str, ...] = (),
    rank: EvidenceRank = EvidenceRank.FORM,
    output_flags: frozenset[str] = frozenset(),
) -> Candidate:
    """Create a HarakaCandidate for testing.

    Args:
        candidate_id: Unique candidate identifier
        status: Candidate status
        identity_ids: Identity IDs
        trace_ids: Trace IDs from ancestors
        rank: Evidence rank
        output_flags: Output flags

    Returns:
        Candidate representing a HarakaCandidate
    """
    return Candidate(
        candidate_id=candidate_id,
        candidate_type="HarakaCandidate",
        status=status,
        layer="HarakaQiyas",
        source_rule_id="rule:haraka",
        asl_id="asl:haraka",
        far_id="far:haraka",
        identity_ids=identity_ids,
        rank=rank,
        residuals=(),
        trace_ids=trace_ids,
        output_flags=output_flags,
    )


def make_atomic_unit_candidate(
    candidate_id: str = "cand:atomic:1",
    *,
    status: CandidateStatus = CandidateStatus.ACCEPTED,
    identity_ids: tuple[str, ...] = ("id:atomic:1",),
    trace_ids: tuple[str, ...] = (),
    rank: EvidenceRank = EvidenceRank.FORM,
    output_flags: frozenset[str] = frozenset(),
) -> Candidate:
    """Create an AtomicUnitCandidate for testing.

    Args:
        candidate_id: Unique candidate identifier
        status: Candidate status
        identity_ids: Identity IDs
        trace_ids: Trace IDs from ancestors
        rank: Evidence rank
        output_flags: Output flags

    Returns:
        Candidate representing an AtomicUnitCandidate
    """
    return Candidate(
        candidate_id=candidate_id,
        candidate_type="AtomicUnitCandidate",
        status=status,
        layer="AtomicUnitQiyas",
        source_rule_id="rule:atomic_unit",
        asl_id="asl:atomic",
        far_id="far:atomic",
        identity_ids=identity_ids,
        rank=rank,
        residuals=(),
        trace_ids=trace_ids,
        output_flags=output_flags,
    )


def make_candidate_with_rank(
    rank: EvidenceRank,
    candidate_id: str = "cand:test:1",
) -> Candidate:
    """Create a test candidate with specific rank.

    Args:
        rank: Evidence rank to set
        candidate_id: Unique candidate identifier

    Returns:
        Candidate with the specified rank
    """
    return Candidate(
        candidate_id=candidate_id,
        candidate_type="TestCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="TestLayer",
        source_rule_id="rule:test",
        asl_id="asl:test",
        far_id="far:test",
        identity_ids=("id:test:1",),
        rank=rank,
        residuals=(),
        trace_ids=(),
        output_flags=frozenset(),
    )


def make_candidate_with_overlapping_ids(
    candidate_id: str = "cand:overlap:1",
    overlapping_id: str = "id:overlap",
) -> Candidate:
    """Create a candidate with overlapping identity and trace IDs (for negative tests).

    Args:
        candidate_id: Unique candidate identifier
        overlapping_id: ID that appears in both identity_ids and trace_ids

    Returns:
        Candidate with overlapping IDs (will raise ValueError in __post_init__)

    Note:
        This will raise ValueError when called due to the overlap check in Candidate.__post_init__.
        Use this in test contexts where you expect and catch the exception.
    """
    # This will raise ValueError - used for testing the validation
    try:
        return Candidate(
            candidate_id=candidate_id,
            candidate_type="TestCandidate",
            status=CandidateStatus.ACCEPTED,
            layer="TestLayer",
            source_rule_id="rule:test",
            asl_id="asl:test",
            far_id="far:test",
            identity_ids=(overlapping_id,),
            rank=EvidenceRank.QIYAS,
            residuals=(),
            trace_ids=(overlapping_id, "id:other"),  # Overlapping ID
            output_flags=frozenset(),
        )
    except ValueError:
        # Re-raise with context
        raise
