"""Constitutional assertion helpers for qiyas_core tests.

These helpers provide reusable assertion functions for validating
constitutional invariants across the qiyas system.
"""

import re
from typing import Sequence

from qiyas_core.candidate import Candidate
from qiyas_core.enums import EvidenceRank, WadiGate
from qiyas_core.rule import QiyasRule
from qiyas_core.slot.policies.difference import SlotDifferencePolicy


# Evidence claim grammar patterns
ALLOWED_CLAIM_PATTERNS = [
    r"^asl:established$",
    r"^far:determined$",
    r"^wasf:.+:evidenced$",
    r"^illah:.+:verified$",
    r"^wadi:sabab:established$",
    r"^wadi:shart:satisfied$",
    r"^wadi:mani:absent$",
    r"^wadi:sihha:valid$",
    r"^wadi:fasad:absent$",
    r"^wadi:butlan:absent$",
    r"^fariq:.+:present$",
    r"^defer:.+:present$",
]

FORBIDDEN_CLAIM_PATTERNS = [
    r"^diff:.+",  # Old difference format
    r"^residual:.+",  # Residuals are not evidence
    r"^hukm:.+",  # Hukm claims not allowed in evidence
    r"^meaning:.+:final$",  # Final meaning not evidence-level
    r"^reality:.+:claim$",  # Reality claims not evidence-level
    r"^final:.+",  # Final claims not evidence-level
]


def assert_evidence_claim_grammar(claim: str) -> None:
    """Assert that an evidence claim follows constitutional grammar.

    Args:
        claim: Evidence claim to validate

    Raises:
        AssertionError: If claim doesn't match allowed patterns
    """
    for pattern in ALLOWED_CLAIM_PATTERNS:
        if re.match(pattern, claim):
            return

    raise AssertionError(
        f"Evidence claim '{claim}' does not match any allowed pattern. "
        f"Allowed patterns: {ALLOWED_CLAIM_PATTERNS}"
    )


def assert_forbidden_claim(claim: str) -> None:
    """Assert that a claim matches forbidden patterns.

    Args:
        claim: Claim to check

    Raises:
        AssertionError: If claim doesn't match forbidden patterns
    """
    for pattern in FORBIDDEN_CLAIM_PATTERNS:
        if re.match(pattern, claim):
            return

    raise AssertionError(
        f"Claim '{claim}' does not match any forbidden pattern. "
        f"Forbidden patterns: {FORBIDDEN_CLAIM_PATTERNS}"
    )


def assert_disjoint_ids(candidate: Candidate) -> None:
    """Assert that candidate's identity_ids and trace_ids are disjoint.

    Args:
        candidate: Candidate to validate

    Raises:
        AssertionError: If identity_ids and trace_ids overlap
    """
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)
    overlap = identity_set & trace_set

    if overlap:
        raise AssertionError(
            f"Candidate {candidate.candidate_id} has overlapping identity and trace IDs: {overlap}"
        )


def assert_rank_ceiling(candidate: Candidate, max_rank: EvidenceRank) -> None:
    """Assert that candidate rank doesn't exceed maximum allowed rank.

    Args:
        candidate: Candidate to validate
        max_rank: Maximum allowed evidence rank

    Raises:
        AssertionError: If candidate.rank > max_rank
    """
    if candidate.rank.value > max_rank.value:
        raise AssertionError(
            f"Candidate {candidate.candidate_id} rank {candidate.rank} exceeds ceiling {max_rank}"
        )


def assert_wadi_gates_complete(rule: QiyasRule) -> None:
    """Assert that rule requires exactly 6 WadiGates (no more, no fewer).

    Args:
        rule: QiyasRule to validate

    Raises:
        AssertionError: If rule doesn't have exactly the 6 required WadiGates
    """
    required_gates = {
        WadiGate.SABAB,
        WadiGate.SHART,
        WadiGate.MANI,
        WadiGate.SIHHA,
        WadiGate.FASAD,
        WadiGate.BUTLAN,
    }

    actual_gates = set(rule.required_wadi_gates)

    if actual_gates != required_gates:
        missing = required_gates - actual_gates
        extra = actual_gates - required_gates

        error_parts = []
        if missing:
            error_parts.append(f"Missing: {sorted(g.value for g in missing)}")
        if extra:
            error_parts.append(f"Extra: {sorted(g.value for g in extra)}")

        raise AssertionError(
            f"Rule {rule.rule_id} must have exactly 6 WadiGates. " + ", ".join(error_parts)
        )


def assert_forbidden_outputs_present(rule: QiyasRule) -> None:
    """Assert that rule has non-empty forbidden_outputs.

    Args:
        rule: QiyasRule to validate

    Raises:
        AssertionError: If rule.forbidden_outputs is empty
    """
    if not rule.forbidden_outputs:
        raise AssertionError(
            f"Rule {rule.rule_id} must have non-empty forbidden_outputs for qiyas/readiness layers"
        )


def assert_no_higher_outputs(
    candidates: Sequence[Candidate],
    forbidden_types: Sequence[str],
) -> None:
    """Assert that no candidate has a type in forbidden_types.

    Args:
        candidates: Candidates to check
        forbidden_types: List of forbidden candidate types

    Raises:
        AssertionError: If any candidate has a forbidden type
    """
    forbidden_set = set(forbidden_types)

    for candidate in candidates:
        if candidate.candidate_type in forbidden_set:
            raise AssertionError(
                f"Candidate {candidate.candidate_id} has forbidden type "
                f"'{candidate.candidate_type}'. Forbidden types: {forbidden_types}"
            )


def assert_slot_policy_disjoint(policy: SlotDifferencePolicy) -> None:
    """Assert that SlotDifferencePolicy categories are mutually disjoint.

    Args:
        policy: SlotDifferencePolicy to validate

    Raises:
        AssertionError: If any difference appears in multiple categories
    """
    categories = {
        "invalidating": set(policy.invalidating_differences),
        "blocking": set(policy.blocking_differences),
        "deferring": set(policy.deferring_differences),
        "ranking": set(policy.ranking_differences),
        "non_blocking": set(policy.non_blocking_differences),
    }

    # Check all pairs for overlap
    category_names = list(categories.keys())
    for i, name1 in enumerate(category_names):
        for name2 in category_names[i + 1 :]:
            overlap = categories[name1] & categories[name2]
            if overlap:
                raise AssertionError(
                    f"SlotDifferencePolicy has overlapping differences in "
                    f"{name1} and {name2}: {overlap}"
                )


def assert_no_self_trace(candidate: Candidate) -> None:
    """Assert that candidate's identity doesn't appear in its own trace.

    Args:
        candidate: Candidate to validate

    Raises:
        AssertionError: If any identity_id appears in trace_ids
    """
    # This is actually enforced by assert_disjoint_ids, but we provide
    # a separate helper for semantic clarity
    assert_disjoint_ids(candidate)


def assert_rank_is_minimum(
    candidate: Candidate,
    rule_ceiling: EvidenceRank,
    asl_rank: EvidenceRank,
    far_rank: EvidenceRank,
    evidence_rank: EvidenceRank,
) -> None:
    """Assert that candidate rank equals minimum of all input ranks.

    Args:
        candidate: Candidate to validate
        rule_ceiling: Rule's rank ceiling
        asl_rank: Asl node's rank
        far_rank: Far node's rank
        evidence_rank: Evidence rank

    Raises:
        AssertionError: If candidate.rank != min(all ranks)
    """
    expected_rank = min(
        rule_ceiling,
        asl_rank,
        far_rank,
        evidence_rank,
        key=lambda r: r.value,
    )

    if candidate.rank != expected_rank:
        raise AssertionError(
            f"Candidate {candidate.candidate_id} rank {candidate.rank} "
            f"should be min({rule_ceiling}, {asl_rank}, {far_rank}, {evidence_rank}) = {expected_rank}"
        )
