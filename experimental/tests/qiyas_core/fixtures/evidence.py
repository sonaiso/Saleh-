"""Evidence factories for constitutional tests."""

from qiyas_core.enums import EvidenceRank
from qiyas_core.evidence import Evidence, EvidenceSet


def make_evidence_set(
    *claims: str,
    evidence_id: str = "ev:1",
    source_layer: str = "TestLayer",
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
    trace_ids: tuple[str, ...] = ("trace:ev:1",),
) -> EvidenceSet:
    """Create an EvidenceSet with specified claims.

    Args:
        *claims: Evidence claims to include
        evidence_id: Unique evidence identifier
        source_layer: Source layer name
        rank: Evidence rank
        trace_ids: Trace IDs

    Returns:
        EvidenceSet containing the specified claims
    """
    return EvidenceSet(
        items=(
            Evidence(
                evidence_id=evidence_id,
                source_layer=source_layer,
                proves=claims,
                rank=rank,
                trace_ids=trace_ids,
            ),
        )
    )


def make_valid_wadi_evidence(
    evidence_id: str = "ev:wadi",
    source_layer: str = "TestLayer",
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
) -> EvidenceSet:
    """Create complete valid wadi evidence (all 6 gates).

    Args:
        evidence_id: Unique evidence identifier
        source_layer: Source layer name
        rank: Evidence rank

    Returns:
        EvidenceSet with all 6 wadi gates satisfied
    """
    return make_evidence_set(
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
        evidence_id=evidence_id,
        source_layer=source_layer,
        rank=rank,
    )


def make_wasf_evidence(
    wasf_claim: str,
    evidence_id: str = "ev:wasf",
    source_layer: str = "TestLayer",
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
) -> EvidenceSet:
    """Create evidence with a wasf claim.

    Args:
        wasf_claim: The wasf claim (e.g., "وصف:carrier_accepts_mark:evidenced")
        evidence_id: Unique evidence identifier
        source_layer: Source layer name
        rank: Evidence rank

    Returns:
        EvidenceSet containing the wasf claim
    """
    return make_evidence_set(
        wasf_claim,
        evidence_id=evidence_id,
        source_layer=source_layer,
        rank=rank,
    )


def make_illah_evidence(
    illah_claim: str,
    evidence_id: str = "ev:illah",
    source_layer: str = "TestLayer",
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
) -> EvidenceSet:
    """Create evidence with an illah claim.

    Args:
        illah_claim: The illah claim (e.g., "علة:licensed_atomic_binding:verified")
        evidence_id: Unique evidence identifier
        source_layer: Source layer name
        rank: Evidence rank

    Returns:
        EvidenceSet containing the illah claim
    """
    return make_evidence_set(
        illah_claim,
        evidence_id=evidence_id,
        source_layer=source_layer,
        rank=rank,
    )


def make_fariq_evidence(
    fariq_claim: str,
    evidence_id: str = "ev:fariq",
    source_layer: str = "TestLayer",
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
) -> EvidenceSet:
    """Create evidence with a fariq (blocking difference) claim.

    Args:
        fariq_claim: The fariq claim (e.g., "فارق:carrier_is_not_arabic_letter:present")
        evidence_id: Unique evidence identifier
        source_layer: Source layer name
        rank: Evidence rank

    Returns:
        EvidenceSet containing the fariq claim
    """
    return make_evidence_set(
        fariq_claim,
        evidence_id=evidence_id,
        source_layer=source_layer,
        rank=rank,
    )


def make_defer_evidence(
    defer_claim: str,
    evidence_id: str = "ev:defer",
    source_layer: str = "TestLayer",
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
) -> EvidenceSet:
    """Create evidence with a defer (deferral) claim.

    Args:
        defer_claim: The defer claim (e.g., "defer:murab_closure_deferred:present")
        evidence_id: Unique evidence identifier
        source_layer: Source layer name
        rank: Evidence rank

    Returns:
        EvidenceSet containing the defer claim
    """
    return make_evidence_set(
        defer_claim,
        evidence_id=evidence_id,
        source_layer=source_layer,
        rank=rank,
    )
