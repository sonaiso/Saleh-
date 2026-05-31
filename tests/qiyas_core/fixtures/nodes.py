"""Node factories for constitutional tests."""

from qiyas_core.enums import EvidenceRank
from qiyas_core.node import QiyasNodeRef


def make_unicode_node(
    char: str = "ب",
    node_id: str = "unicode:1",
    *,
    identity_ids: tuple[str, ...] = ("id:unicode:1",),
    trace_ids: tuple[str, ...] = (),
    rank: EvidenceRank = EvidenceRank.FORM,
) -> QiyasNodeRef:
    """Create a UnicodeCandidate node for testing.

    Args:
        char: The Unicode character (default: Arabic letter Ba)
        node_id: Unique node identifier
        identity_ids: Identity IDs for the node
        trace_ids: Trace IDs from ancestors
        rank: Evidence rank

    Returns:
        QiyasNodeRef representing a UnicodeCandidate
    """
    return QiyasNodeRef(
        node_id=node_id,
        node_type="UnicodeCandidate",
        identity_ids=identity_ids,
        trace_ids=trace_ids,
        rank=rank,
    )


def make_haraka_node(
    diacritic: str = "fatha",
    node_id: str = "haraka:1",
    *,
    identity_ids: tuple[str, ...] = ("id:haraka:1",),
    trace_ids: tuple[str, ...] = (),
    rank: EvidenceRank = EvidenceRank.FORM,
) -> QiyasNodeRef:
    """Create a HarakaCandidate node for testing.

    Args:
        diacritic: The diacritic type (fatha, kasra, damma, etc.)
        node_id: Unique node identifier
        identity_ids: Identity IDs for the node
        trace_ids: Trace IDs from ancestors
        rank: Evidence rank

    Returns:
        QiyasNodeRef representing a HarakaCandidate
    """
    return QiyasNodeRef(
        node_id=node_id,
        node_type="HarakaCandidate",
        identity_ids=identity_ids,
        trace_ids=trace_ids,
        rank=rank,
    )


def make_atomic_unit_node(
    carrier: str = "ب",
    mark: str = "fatha",
    node_id: str = "atomic:1",
    *,
    identity_ids: tuple[str, ...] = ("id:atomic:1",),
    trace_ids: tuple[str, ...] = (),
    rank: EvidenceRank = EvidenceRank.FORM,
) -> QiyasNodeRef:
    """Create an AtomicUnitCandidate node for testing.

    Args:
        carrier: The carrier character
        mark: The mark (diacritic)
        node_id: Unique node identifier
        identity_ids: Identity IDs for the node
        trace_ids: Trace IDs from ancestors
        rank: Evidence rank

    Returns:
        QiyasNodeRef representing an AtomicUnitCandidate
    """
    return QiyasNodeRef(
        node_id=node_id,
        node_type="AtomicUnitCandidate",
        identity_ids=identity_ids,
        trace_ids=trace_ids,
        rank=rank,
    )
