"""Constitutional test fixtures for qiyas_core.

This package provides factory functions for creating test objects
with constitutional validity guarantees.
"""

from .nodes import make_unicode_node, make_haraka_node, make_atomic_unit_node
from .evidence import (
    make_evidence_set,
    make_valid_wadi_evidence,
    make_wasf_evidence,
    make_illah_evidence,
    make_fariq_evidence,
    make_defer_evidence,
)
from .rules import (
    make_minimal_rule,
    make_rule_missing_wadi,
    make_rule_extra_wadi,
    make_rule_empty_forbidden,
)
from .candidates import (
    make_unicode_candidate,
    make_haraka_candidate,
    make_atomic_unit_candidate,
    make_candidate_with_rank,
    make_candidate_with_overlapping_ids,
)
from .requests import make_qiyas_request, make_request_with_evidence

__all__ = [
    # Nodes
    "make_unicode_node",
    "make_haraka_node",
    "make_atomic_unit_node",
    # Evidence
    "make_evidence_set",
    "make_valid_wadi_evidence",
    "make_wasf_evidence",
    "make_illah_evidence",
    "make_fariq_evidence",
    "make_defer_evidence",
    # Rules
    "make_minimal_rule",
    "make_rule_missing_wadi",
    "make_rule_extra_wadi",
    "make_rule_empty_forbidden",
    # Candidates
    "make_unicode_candidate",
    "make_haraka_candidate",
    "make_atomic_unit_candidate",
    "make_candidate_with_rank",
    "make_candidate_with_overlapping_ids",
    # Requests
    "make_qiyas_request",
    "make_request_with_evidence",
]
