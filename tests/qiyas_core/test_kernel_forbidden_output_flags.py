"""
PR #30 — Kernel-level forbidden `output_flags` guard tests.

Open Constitutional Question Q3 from the Global Recursive Closure
Review identified a coverage gap: the per-rule `forbidden_outputs`
mechanism was tested (PRs #25, #26, #28, #29), but the second-layer
guard inside `Candidate.__post_init__` — which rejects any candidate
whose `output_flags` intersects the constitutional final-output set —
was only tested indirectly. This file closes that gap.

The guard under test (verbatim from `src/qiyas_core/candidate.py`):

    forbidden_runtime_flags = {
        "HukmCandidate", "RealityClaim", "FinalMeaning", "FinalCaseJudgment",
    }
    if self.output_flags & forbidden_runtime_flags:
        raise ValueError(...)

Two-level coverage:

  1. Dataclass-level: construct a `Candidate` directly with each
     forbidden flag and assert `ValueError` is raised.
  2. Kernel-level: run `QiyasKernel.apply()` end-to-end and assert
     the produced candidate's `output_flags` contains only
     `CandidateOnly` and never any forbidden flag.

Scope: tests only. No source code is modified.
"""

from __future__ import annotations

import pytest

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.unicode_adapter import UnicodeLayerAdapter


# ---------------------------------------------------------------------------
# Constants — the constitutional forbidden flags
# ---------------------------------------------------------------------------

FORBIDDEN_RUNTIME_FLAGS = (
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
    "FinalCaseJudgment",
)


# ---------------------------------------------------------------------------
# Builder helpers — keep the test bodies focused on the guard, not on
# Candidate field plumbing.
# ---------------------------------------------------------------------------


def _candidate_kwargs(
    output_flags: frozenset[str] = frozenset({"CandidateOnly"}),
) -> dict:
    """Return a minimal valid kwargs dict for `Candidate(...)`.

    Designed so swapping `output_flags` is the only variable. All other
    fields satisfy the dataclass's own invariants (non-empty identity,
    disjoint trace/identity sets).
    """
    return dict(
        candidate_id="test:candidate:1",
        candidate_type="TestCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="TestLayer",
        source_rule_id="test.rule",
        asl_id="اصل:test",
        far_id="فرع:test",
        identity_ids=("identity:test",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=("trace:test",),
        output_flags=output_flags,
    )


# ---------------------------------------------------------------------------
# Dataclass-level guard tests — one ValueError test per forbidden flag.
# ---------------------------------------------------------------------------


def test_candidate_rejects_hukm_candidate_flag():
    with pytest.raises(ValueError) as exc:
        Candidate(**_candidate_kwargs(
            output_flags=frozenset({"CandidateOnly", "HukmCandidate"}),
        ))
    assert "HukmCandidate" in str(exc.value)


def test_candidate_rejects_reality_claim_flag():
    with pytest.raises(ValueError) as exc:
        Candidate(**_candidate_kwargs(
            output_flags=frozenset({"CandidateOnly", "RealityClaim"}),
        ))
    assert "RealityClaim" in str(exc.value)


def test_candidate_rejects_final_meaning_flag():
    with pytest.raises(ValueError) as exc:
        Candidate(**_candidate_kwargs(
            output_flags=frozenset({"CandidateOnly", "FinalMeaning"}),
        ))
    assert "FinalMeaning" in str(exc.value)


def test_candidate_rejects_final_case_judgment_flag():
    with pytest.raises(ValueError) as exc:
        Candidate(**_candidate_kwargs(
            output_flags=frozenset({"CandidateOnly", "FinalCaseJudgment"}),
        ))
    assert "FinalCaseJudgment" in str(exc.value)


@pytest.mark.parametrize("flag", FORBIDDEN_RUNTIME_FLAGS)
def test_candidate_rejects_each_forbidden_flag_solo(flag):
    """The guard fires even if the forbidden flag is the only flag —
    no protective `CandidateOnly` companion is required."""
    with pytest.raises(ValueError):
        Candidate(**_candidate_kwargs(output_flags=frozenset({flag})))


def test_candidate_rejects_multiple_forbidden_flags_simultaneously():
    """When multiple forbidden flags are present at once, the
    ValueError message lists them — none is silently dropped."""
    forbidden_set = frozenset({"HukmCandidate", "RealityClaim", "FinalMeaning"})
    with pytest.raises(ValueError) as exc:
        Candidate(**_candidate_kwargs(
            output_flags=frozenset({"CandidateOnly"}) | forbidden_set,
        ))
    msg = str(exc.value)
    for flag in forbidden_set:
        assert flag in msg


# ---------------------------------------------------------------------------
# Positive controls — valid output_flags pass.
# ---------------------------------------------------------------------------


def test_candidate_accepts_candidate_only_flag():
    """The canonical `CandidateOnly` flag passes the guard."""
    c = Candidate(**_candidate_kwargs(
        output_flags=frozenset({"CandidateOnly"}),
    ))
    assert "CandidateOnly" in c.output_flags
    # And of course none of the forbidden flags slipped in.
    for flag in FORBIDDEN_RUNTIME_FLAGS:
        assert flag not in c.output_flags


def test_candidate_accepts_empty_output_flags():
    """An empty `output_flags` set is structurally valid (the guard
    only rejects forbidden flags; it does not require any positive
    flag). This pins the guard's behaviour as set-intersection-based,
    not membership-check-based."""
    c = Candidate(**_candidate_kwargs(output_flags=frozenset()))
    assert c.output_flags == frozenset()


# ---------------------------------------------------------------------------
# Kernel-level end-to-end guard tests — every candidate produced by
# `QiyasKernel.apply()` must carry `CandidateOnly` and never any
# forbidden flag.
# ---------------------------------------------------------------------------


def _kernel() -> QiyasKernel:
    return QiyasKernel()


def test_kernel_apply_produces_candidate_only_flag_for_accepted():
    """For an accepted Unicode classification, the produced candidate
    has `output_flags == {CandidateOnly}` — set by the kernel itself,
    not by the rule or the adapter."""
    cs = UnicodeLayerAdapter(kernel=_kernel()).process_codepoint(0x0628)
    assert len(cs.accepted) == 1
    c = cs.accepted[0]
    assert c.output_flags == frozenset({"CandidateOnly"})


def test_kernel_apply_never_emits_forbidden_flags_on_block():
    """When the kernel blocks (non-Arabic codepoint), the resulting
    candidate STILL must not carry any forbidden flag."""
    cs = UnicodeLayerAdapter(kernel=_kernel()).process_codepoint(0x0041)  # 'A'
    assert len(cs.blocked) == 1
    c = cs.blocked[0]
    for flag in FORBIDDEN_RUNTIME_FLAGS:
        assert flag not in c.output_flags


def test_kernel_apply_through_typed_codepoint_layer_emits_candidate_only():
    """Two-step chain: Unicode → TypedCodePoint. The TypedCodePoint
    candidate must have `output_flags == {CandidateOnly}` as well."""
    kernel = _kernel()
    u = UnicodeLayerAdapter(kernel=kernel).process_codepoint(0x0628)
    t = TypedCodePointLayerAdapter(kernel=kernel).classify_unicode_candidate(
        u.accepted[0]
    )
    assert len(t.accepted) == 1
    assert t.accepted[0].output_flags == frozenset({"CandidateOnly"})


@pytest.mark.parametrize("codepoint", [0x0628, 0x064E, 0x062A, 0x064F, 0x0631])
def test_kernel_apply_output_flags_invariant_across_codepoints(codepoint):
    """The `output_flags = {CandidateOnly}` invariant holds across
    every codepoint that the canonical pipeline accepts. Forbidden
    flags must never appear."""
    cs = UnicodeLayerAdapter(kernel=_kernel()).process_codepoint(codepoint)
    for c in cs.candidates:
        assert c.output_flags == frozenset({"CandidateOnly"})
        for flag in FORBIDDEN_RUNTIME_FLAGS:
            assert flag not in c.output_flags
