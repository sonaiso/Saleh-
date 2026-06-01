"""
Tests for ForbiddenOutputRegistry — Gap #12 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Required tests (from contract):
  test_letter_identity_forbids_weight
  test_haraka_function_forbids_case_effect
  test_slot_forbids_meaning
"""

from qiyas_core.forbidden_outputs import (
    CONSTITUTIONAL_BASE,
    FORBIDDEN_LETTER_IDENTITY,
    FORBIDDEN_HARAKA_FUNCTION,
    FORBIDDEN_POSITION,
    FORBIDDEN_SLOT,
    FORBIDDEN_SYLLABLE,
    LAYER_FORBIDDEN_OUTPUTS,
    get_forbidden_outputs,
)


# ---------------------------------------------------------------------------
# Constitutional base invariant
# ---------------------------------------------------------------------------

def test_constitutional_base_contains_required_triple():
    """Every layer's forbidden_outputs must include the constitutional triple."""
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    assert required.issubset(set(CONSTITUTIONAL_BASE))


def test_all_layers_include_constitutional_base():
    """Every layer in the registry includes the constitutional triple."""
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    for layer, outputs in LAYER_FORBIDDEN_OUTPUTS.items():
        assert required.issubset(set(outputs)), (
            f"Layer {layer!r} missing constitutional forbidden outputs"
        )


# ---------------------------------------------------------------------------
# Contract-required tests
# ---------------------------------------------------------------------------

def test_letter_identity_forbids_weight():
    """Contract test: LetterIdentityCarrier layer forbids WeightCandidate."""
    assert "WeightCandidate" in FORBIDDEN_LETTER_IDENTITY


def test_haraka_function_forbids_case_effect():
    """Contract test: HarakaFunctionCarrier layer forbids CaseEffect."""
    assert "CaseEffect" in FORBIDDEN_HARAKA_FUNCTION
    assert "Irab" in FORBIDDEN_HARAKA_FUNCTION


def test_slot_forbids_meaning():
    """Contract test: SlotCandidate layer forbids MeaningCandidate."""
    assert "MeaningCandidate" in FORBIDDEN_SLOT


# ---------------------------------------------------------------------------
# Additional registry tests
# ---------------------------------------------------------------------------

def test_letter_identity_forbids_root():
    """LetterIdentityCarrier must forbid RootCandidate."""
    assert "RootCandidate" in FORBIDDEN_LETTER_IDENTITY


def test_haraka_function_forbids_syllable():
    """HarakaFunctionCarrier must forbid SyllableCandidate."""
    assert "SyllableCandidate" in FORBIDDEN_HARAKA_FUNCTION


def test_slot_forbids_syllable():
    """SlotCandidate must forbid SyllableCandidate (adjacency not yet established)."""
    assert "SyllableCandidate" in FORBIDDEN_SLOT


def test_position_forbids_case_effect():
    """PositionCarrier must forbid CaseEffect."""
    assert "CaseEffect" in FORBIDDEN_POSITION


def test_get_forbidden_outputs_returns_layer_specific():
    """get_forbidden_outputs returns correct tuple for known layers."""
    assert get_forbidden_outputs("LetterIdentityQiyas") is FORBIDDEN_LETTER_IDENTITY
    assert get_forbidden_outputs("HarakaFunctionQiyas") is FORBIDDEN_HARAKA_FUNCTION
    assert get_forbidden_outputs("PositionQiyas") is FORBIDDEN_POSITION
    assert get_forbidden_outputs("SlotQiyas") is FORBIDDEN_SLOT


def test_get_forbidden_outputs_defaults_to_constitutional_base():
    """Unknown layer returns the constitutional base tuple."""
    result = get_forbidden_outputs("UnknownLayer")
    assert result is CONSTITUTIONAL_BASE
    required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    assert required.issubset(set(result))


def test_syllable_layer_registered():
    """SyllableQiyas is registered in the forbidden outputs registry."""
    assert "SyllableQiyas" in LAYER_FORBIDDEN_OUTPUTS
    assert "MeaningCandidate" in LAYER_FORBIDDEN_OUTPUTS["SyllableQiyas"]


# ===========================================================================
# PR #29 — Global recursion closure tests.
#
# Each pre-slot layer must explicitly forbid `SlotCandidate` and
# `SlotGeometry`. The slot layer itself MUST NOT forbid `SlotCandidate`
# (own output) but MUST forbid `SlotGeometry` (skip into next layer).
#
# Behavioural verification (not merely centralized-registry check): for
# the `TypedCodePoint` family we read the actual rule objects, because
# the source-of-truth fix in PR #29 redirected their `forbidden_outputs`
# field to import the central `FORBIDDEN_TYPED_CODEPOINT` tuple.
# ===========================================================================


from qiyas_core.forbidden_outputs import FORBIDDEN_TYPED_CODEPOINT  # noqa: E402
from qiyas_core.rules.typed_codepoint_rules import (  # noqa: E402
    LETTER_CODEPOINT_CLASSIFICATION,
    HARAKA_CODEPOINT_CLASSIFICATION,
    BOUNDARY_CODEPOINT_CLASSIFICATION,
    PUNCTUATION_CODEPOINT_CLASSIFICATION,
    RESIDUAL_CODEPOINT_CLASSIFICATION,
)
from qiyas_core.rules.unicode_rules import UNICODE_ARABIC_MEMBERSHIP  # noqa: E402


_TYPED_CODEPOINT_RULES = (
    LETTER_CODEPOINT_CLASSIFICATION,
    HARAKA_CODEPOINT_CLASSIFICATION,
    BOUNDARY_CODEPOINT_CLASSIFICATION,
    PUNCTUATION_CODEPOINT_CLASSIFICATION,
    RESIDUAL_CODEPOINT_CLASSIFICATION,
)


# §13 #1 — FORBIDDEN_TYPED_CODEPOINT contains SlotCandidate.

def test_forbidden_typed_codepoint_contains_slot_candidate():
    assert "SlotCandidate" in FORBIDDEN_TYPED_CODEPOINT


# §13 #2 — FORBIDDEN_TYPED_CODEPOINT contains SlotGeometry.

def test_forbidden_typed_codepoint_contains_slot_geometry():
    assert "SlotGeometry" in FORBIDDEN_TYPED_CODEPOINT


# §13 #3 — Every TypedCodePoint rule actually uses FORBIDDEN_TYPED_CODEPOINT
# (source-of-truth fix). Verified by behavioural identity of
# `rule.forbidden_outputs` with the central tuple.

def test_every_typed_codepoint_rule_uses_central_forbidden_tuple():
    for rule in _TYPED_CODEPOINT_RULES:
        assert rule.forbidden_outputs is FORBIDDEN_TYPED_CODEPOINT, (
            f"Rule {rule.rule_id!r} does not use the central "
            "FORBIDDEN_TYPED_CODEPOINT tuple; the source-of-truth fix "
            "is broken."
        )


# §13 #4 — TypedCodePoint rules forbid SlotCandidate (behavioural).

def test_every_typed_codepoint_rule_forbids_slot_candidate():
    for rule in _TYPED_CODEPOINT_RULES:
        assert "SlotCandidate" in rule.forbidden_outputs, (
            f"Rule {rule.rule_id!r} does not forbid SlotCandidate."
        )


# §13 #5 — TypedCodePoint rules forbid SlotGeometry (behavioural).

def test_every_typed_codepoint_rule_forbids_slot_geometry():
    for rule in _TYPED_CODEPOINT_RULES:
        assert "SlotGeometry" in rule.forbidden_outputs, (
            f"Rule {rule.rule_id!r} does not forbid SlotGeometry."
        )


# §13 #6 — FORBIDDEN_LETTER_IDENTITY forbids SlotCandidate.

def test_forbidden_letter_identity_contains_slot_candidate():
    assert "SlotCandidate" in FORBIDDEN_LETTER_IDENTITY


# §13 #7 — FORBIDDEN_LETTER_IDENTITY forbids SlotGeometry.

def test_forbidden_letter_identity_contains_slot_geometry():
    assert "SlotGeometry" in FORBIDDEN_LETTER_IDENTITY


# §13 #8 — FORBIDDEN_HARAKA_FUNCTION forbids SlotCandidate.

def test_forbidden_haraka_function_contains_slot_candidate():
    assert "SlotCandidate" in FORBIDDEN_HARAKA_FUNCTION


# §13 #9 — FORBIDDEN_HARAKA_FUNCTION forbids SlotGeometry.

def test_forbidden_haraka_function_contains_slot_geometry():
    assert "SlotGeometry" in FORBIDDEN_HARAKA_FUNCTION


# §13 #10 — FORBIDDEN_POSITION forbids SlotCandidate.

def test_forbidden_position_contains_slot_candidate():
    assert "SlotCandidate" in FORBIDDEN_POSITION


# §13 #11 — FORBIDDEN_POSITION forbids SlotGeometry.

def test_forbidden_position_contains_slot_geometry():
    assert "SlotGeometry" in FORBIDDEN_POSITION


# §13 #12 — UNICODE_ARABIC_MEMBERSHIP forbids SlotCandidate.

def test_unicode_arabic_membership_forbids_slot_candidate():
    assert "SlotCandidate" in UNICODE_ARABIC_MEMBERSHIP.forbidden_outputs


# §13 #13 — UNICODE_ARABIC_MEMBERSHIP forbids SlotGeometry.

def test_unicode_arabic_membership_forbids_slot_geometry():
    assert "SlotGeometry" in UNICODE_ARABIC_MEMBERSHIP.forbidden_outputs


# §13 #14 — FORBIDDEN_SLOT does NOT contain SlotCandidate (own output).

def test_forbidden_slot_does_not_contain_slot_candidate():
    assert "SlotCandidate" not in FORBIDDEN_SLOT


# §13 #15 — FORBIDDEN_SLOT contains SlotGeometry.

def test_forbidden_slot_contains_slot_geometry():
    assert "SlotGeometry" in FORBIDDEN_SLOT


# Defensive lateral closure for CTS — CTS produces PositionEvidence,
# never PositionCarrier.

def test_forbidden_conditioned_typed_sequence_contains_position_carrier():
    from qiyas_core.forbidden_outputs import FORBIDDEN_CONDITIONED_TYPED_SEQUENCE
    assert "PositionCarrier" in FORBIDDEN_CONDITIONED_TYPED_SEQUENCE


def test_forbidden_conditioned_typed_sequence_still_allows_its_own_outputs():
    """The defensive `PositionCarrier` addition must NOT inadvertently
    forbid any of CTS's four licit output candidate types."""
    from qiyas_core.forbidden_outputs import FORBIDDEN_CONDITIONED_TYPED_SEQUENCE
    licit_outputs = {
        "CarrierBindingCandidate",
        "PositionEvidence",
        "BoundaryEvidence",
        "ResidualPreservationEvidence",
    }
    assert licit_outputs.isdisjoint(set(FORBIDDEN_CONDITIONED_TYPED_SEQUENCE))


# ---------------------------------------------------------------------------
# PR #31 — terminology normalization lock-in.
#
# `UNICODE_ARABIC_MEMBERSHIP.forbidden_outputs` previously held the
# abbreviated form `"DalCandidate"`. The canonical name per
# `LAYER_CONTRACT_CONSTITUTION.md §7.7` (DalalahTypeGate) is
# `"DalalahCandidate"`, which is what `FORBIDDEN_TYPED_CODEPOINT` and
# every canonical test already use. This test pins the rename so it
# cannot silently regress.
# ---------------------------------------------------------------------------


def test_unicode_arabic_membership_uses_canonical_dalalah_term():
    assert "DalalahCandidate" in UNICODE_ARABIC_MEMBERSHIP.forbidden_outputs
    assert "DalCandidate" not in UNICODE_ARABIC_MEMBERSHIP.forbidden_outputs
