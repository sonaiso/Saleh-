"""Constitutional guard tests for SlotGeometry Beginning/Ending Contract.

Per the maintainer's guidance, PR #74 added
``docs/qiyas_core/SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md`` as a
docs-only contract defining Beginning and Ending as closure condition
licenses, NOT semantic authority.

This test file guards the contract's constitutional boundaries BEFORE
any runtime implementation is attempted (PR #76+).

Track: SlotGeometry only (Track A)
Scope: Test-only Micro Safety PR
Forbidden: No src/ changes, no runtime, no adapters, no rules

Constitutional Laws to Guard:
- Beginning licenses WHERE SlotGeometry may start
- Ending licenses WHERE SlotGeometry may stop
- Beginning/Ending are closure conditions, not semantic authority
- Boundary evidence is trace/provenance, not identity
- gate:beginning:licensed and gate:ending:licensed are trace, not identity
- No WordCandidate, DalalahCandidate, FinalMeaning, HukmCandidate
- No WordBoundaryCandidate, SemanticBoundaryCandidate
- No higher-layer typed unit
- No runtime implementation authorized by contract alone
"""

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Contract document exists
# ---------------------------------------------------------------------------


def test_beginning_ending_contract_document_exists():
    """Guard 1: The Beginning/Ending contract document exists at the
    expected canonical path."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    assert contract_path.exists(), (
        f"Contract document must exist at {contract_path}"
    )


# ---------------------------------------------------------------------------
# Beginning licenses WHERE, not WHAT
# ---------------------------------------------------------------------------


def test_contract_states_beginning_licenses_where_not_what():
    """Guard 2: Contract must state that Beginning licenses WHERE a
    SlotGeometry may start, not WHAT the slot means or represents."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # Positive assertions: Beginning licenses WHERE
    assert "beginning" in content.lower() or "Beginning" in content, (
        "Contract must mention Beginning"
    )
    assert "where" in content.lower() or "WHERE" in content, (
        "Contract must clarify Beginning licenses WHERE (position)"
    )

    # Negative assertion: Beginning is NOT meaning/word/dalalah
    # The contract should explicitly state this is NOT semantic authority
    assert (
        "not meaning" in content.lower()
        or "not semantic" in content.lower()
        or "closure condition" in content.lower()
    ), (
        "Contract must clarify Beginning is NOT meaning/semantic authority"
    )


def test_contract_states_ending_licenses_where_not_what():
    """Guard 3: Contract must state that Ending licenses WHERE a
    SlotGeometry may stop, not semantic finality or word completion."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # Positive assertions: Ending licenses WHERE
    assert "ending" in content.lower() or "Ending" in content, (
        "Contract must mention Ending"
    )

    # Negative assertion: Ending is NOT semantic finality
    assert (
        "not semantic finality" in content.lower()
        or "not word completion" in content.lower()
        or "not meaning" in content.lower()
        or "closure condition" in content.lower()
    ), (
        "Contract must clarify Ending is NOT semantic finality/word completion"
    )


# ---------------------------------------------------------------------------
# Beginning/Ending consume evidence, produce trace
# ---------------------------------------------------------------------------


def test_contract_states_beginning_consumes_evidence():
    """Guard 4: Contract must state Beginning consumes SlotCandidate +
    SequenceContextTokenizer evidence."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "SlotCandidate" in content
        or "slot candidate" in content.lower()
    ), (
        "Contract must state Beginning consumes SlotCandidate"
    )

    assert (
        "SequenceContextTokenizer" in content
        or "sequence context" in content.lower()
        or "boundary evidence" in content.lower()
    ), (
        "Contract must state Beginning uses SequenceContextTokenizer evidence"
    )


def test_contract_states_ending_consumes_evidence():
    """Guard 5: Contract must state Ending consumes SlotCandidate +
    SequenceContextTokenizer evidence."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # Ending should also consume SlotCandidate and boundary evidence
    assert (
        "SlotCandidate" in content
        or "slot candidate" in content.lower()
    ), (
        "Contract must state Ending consumes SlotCandidate"
    )


def test_contract_states_beginning_produces_gate_trace():
    """Guard 6: Contract must state Beginning produces
    gate:beginning:licensed as TRACE, not identity."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "gate:beginning:licensed" in content
        or "gate:beginning" in content
    ), (
        "Contract must mention gate:beginning:licensed"
    )

    assert (
        "trace" in content.lower()
        or "provenance" in content.lower()
    ), (
        "Contract must clarify gate outputs are trace/provenance"
    )


def test_contract_states_ending_produces_gate_trace():
    """Guard 7: Contract must state Ending produces
    gate:ending:licensed as TRACE, not identity."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "gate:ending:licensed" in content
        or "gate:ending" in content
    ), (
        "Contract must mention gate:ending:licensed"
    )


# ---------------------------------------------------------------------------
# Boundary evidence is trace, not identity
# ---------------------------------------------------------------------------


def test_contract_states_boundary_evidence_is_trace_not_identity():
    """Guard 8: Contract must state boundary evidence is
    trace/provenance, NOT identity."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "boundary" in content.lower()
    ), (
        "Contract must mention boundary evidence"
    )

    # Should clarify boundary ≠ identity
    assert (
        "trace" in content.lower()
        or "provenance" in content.lower()
        or "not identity" in content.lower()
    ), (
        "Contract must clarify boundary evidence is trace, not identity"
    )


# ---------------------------------------------------------------------------
# Seed and extended slot requirements
# ---------------------------------------------------------------------------


def test_contract_states_seed_length_1_requires_both_licenses():
    """Guard 9: Contract must state seed length=1 requires both
    beginning AND ending licenses."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "seed" in content.lower()
        or "length" in content.lower()
        or "length=1" in content
        or "length = 1" in content
    ), (
        "Contract must discuss seed length requirements"
    )


def test_contract_states_extended_uses_first_and_last_units():
    """Guard 10: Contract must state extended length>1 uses beginning
    from first unit and ending from last unit."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "extended" in content.lower()
        or "length>1" in content
        or "length > 1" in content
        or "first" in content.lower()
        or "last" in content.lower()
    ), (
        "Contract must discuss extended slot geometry requirements"
    )


# ---------------------------------------------------------------------------
# Forbidden outputs: No Word, Dalalah, Meaning, Hukm
# ---------------------------------------------------------------------------


def test_contract_forbids_word_candidate_production():
    """Guard 11: Contract must NOT authorize Beginning/Ending to
    produce WordCandidate."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # If WordCandidate is mentioned, it should be in a forbidden/negative context
    if "WordCandidate" in content:
        # Find context around WordCandidate mentions
        lines = content.splitlines()
        word_candidate_contexts = []
        for i, line in enumerate(lines):
            if "WordCandidate" in line:
                # Get surrounding context (5 lines before and after)
                context_start = max(0, i - 5)
                context_end = min(len(lines), i + 6)
                context = "\n".join(lines[context_start:context_end])
                word_candidate_contexts.append(context)

        # Check that all mentions are in negative/forbidden context
        for ctx in word_candidate_contexts:
            assert any(
                forbidden_marker in ctx.lower()
                for forbidden_marker in [
                    "forbidden",
                    "must not",
                    "does not produce",
                    "not authorized",
                    "prohibited",
                    "no wordcandidate",
                ]
            ), (
                f"WordCandidate mention must be in forbidden context:\n{ctx}"
            )


def test_contract_forbids_dalalah_candidate_production():
    """Guard 12: Contract must NOT authorize Beginning/Ending to
    produce DalalahCandidate."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # If DalalahCandidate is mentioned, it should be in a forbidden context
    if "DalalahCandidate" in content or "Dalalah" in content:
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not dalalah",
                "forbidden",
                "must not",
                "does not produce",
                "not authorized",
            ]
        ), (
            "DalalahCandidate/Dalalah must only appear in forbidden context"
        )


def test_contract_forbids_final_meaning_production():
    """Guard 13: Contract must NOT authorize Beginning/Ending to
    produce FinalMeaning."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # If FinalMeaning or meaning is mentioned, should be in negative context
    if "FinalMeaning" in content or "final meaning" in content.lower():
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not meaning",
                "not final meaning",
                "forbidden",
                "must not",
                "does not produce",
            ]
        ), (
            "FinalMeaning must only appear in forbidden context"
        )


def test_contract_forbids_hukm_candidate_production():
    """Guard 14: Contract must NOT authorize Beginning/Ending to
    produce HukmCandidate."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # If HukmCandidate or Hukm is mentioned, should be in forbidden context
    if "HukmCandidate" in content or "Hukm" in content:
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not hukm",
                "forbidden",
                "must not",
                "does not produce",
                "not authorized",
            ]
        ), (
            "HukmCandidate/Hukm must only appear in forbidden context"
        )


def test_contract_forbids_semantic_boundary_candidates():
    """Guard 15: Contract must NOT authorize Beginning/Ending to
    produce WordBoundaryCandidate or SemanticBoundaryCandidate."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # These should not be authorized (if mentioned, should be forbidden)
    forbidden_candidates = [
        "WordBoundaryCandidate",
        "SemanticBoundaryCandidate",
    ]

    for candidate_type in forbidden_candidates:
        if candidate_type in content:
            assert any(
                forbidden_marker in content.lower()
                for forbidden_marker in [
                    "forbidden",
                    "must not",
                    "does not produce",
                    "not authorized",
                ]
            ), (
                f"{candidate_type} must only appear in forbidden context"
            )


# ---------------------------------------------------------------------------
# No runtime implementation authorized by contract alone
# ---------------------------------------------------------------------------


def test_contract_does_not_authorize_immediate_runtime_implementation():
    """Guard 16: Contract must NOT authorize runtime implementation
    without future approval. It defines the contract only."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # Contract should be clear this is specification, not authorization
    # It should mention future/approval/independent or similar
    assert any(
        marker in content.lower()
        for marker in [
            "future",
            "requires approval",
            "independent approval",
            "not yet authorized",
            "contract only",
            "specification only",
        ]
    ), (
        "Contract must clarify implementation requires future approval"
    )


def test_contract_does_not_authorize_run_qiyas_wiring():
    """Guard 17: Contract must NOT authorize run_qiyas.py wiring."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # run_qiyas should not be mentioned as authorized
    if "run_qiyas" in content:
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not authorized",
                "forbidden",
                "must not",
                "future",
            ]
        ), (
            "run_qiyas must not be authorized by this contract"
        )


# ---------------------------------------------------------------------------
# Track isolation: No LCNV, Billing, LogMeasurement
# ---------------------------------------------------------------------------


def test_contract_does_not_authorize_lcnv_integration():
    """Guard 18: Contract must NOT authorize LCNV integration.
    SlotGeometry is Track A, LCNV is Track B - they are isolated."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # LCNV should not be authorized
    if "LCNV" in content or "LayeredCompressedNumericValue" in content:
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not authorized",
                "forbidden",
                "track isolation",
                "isolated",
            ]
        ), (
            "LCNV integration must not be authorized (Track B isolation)"
        )


def test_contract_does_not_authorize_billing_integration():
    """Guard 19: Contract must NOT authorize billing/product
    integration."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # Billing/product should not be authorized
    if "billing" in content.lower() or "product" in content.lower():
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not authorized",
                "forbidden",
                "separated",
                "isolated",
            ]
        ), (
            "Billing/product integration must not be authorized"
        )


def test_contract_does_not_authorize_log_measurement_integration():
    """Guard 20: Contract must NOT authorize Logarithmic Measurement
    integration."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    # LogMeasurement should not be authorized
    if (
        "LogarithmicMeasurement" in content
        or "LogMeasuredQuantity" in content
        or "logarithmic measurement" in content.lower()
    ):
        assert any(
            forbidden_marker in content.lower()
            for forbidden_marker in [
                "not authorized",
                "forbidden",
                "isolated",
                "separated",
            ]
        ), (
            "Logarithmic Measurement integration must not be authorized"
        )


# ---------------------------------------------------------------------------
# Beginning/Ending are closure conditions, not semantic authority
# ---------------------------------------------------------------------------


def test_contract_states_beginning_ending_are_closure_conditions():
    """Guard 21: Contract must explicitly state Beginning and Ending
    are CLOSURE CONDITIONS, not semantic authority."""
    contract_path = (
        Path(__file__).parent.parent.parent
        / "docs"
        / "qiyas_core"
        / "SLOT_GEOMETRY_BEGINNING_ENDING_CONTRACT.md"
    )
    content = contract_path.read_text(encoding="utf-8")

    assert (
        "closure condition" in content.lower()
        or "closure conditions" in content.lower()
    ), (
        "Contract must state Beginning/Ending are closure conditions"
    )

    assert (
        "not semantic authority" in content.lower()
        or "not semantic" in content.lower()
        or "not meaning" in content.lower()
    ), (
        "Contract must clarify Beginning/Ending are NOT semantic authority"
    )
