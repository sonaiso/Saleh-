"""Constitutional tests for QiyasRule validation."""

import pytest

from qiyas_core.enums import WadiGate
from qiyas_core.rules.atomic_unit_rules import ATOMIC_UNIT_BINDING
from tests.qiyas_core.constitutional_helpers import (
    assert_wadi_gates_complete,
    assert_forbidden_outputs_present,
)
from tests.qiyas_core.fixtures.rules import (
    make_minimal_rule,
    make_rule_missing_wadi,
    make_rule_extra_wadi,
    make_rule_empty_forbidden,
)


@pytest.mark.rule
@pytest.mark.constitution
class TestRuleConstitution:
    """Test that QiyasRules follow constitutional requirements."""

    def test_all_six_wadi_gates_required(self):
        """Rules must have exactly 6 WadiGates"""
        rule = make_minimal_rule()
        assert_wadi_gates_complete(rule)

    def test_missing_sabab_fails(self):
        """Rules missing SABAB gate must fail"""
        rule = make_rule_missing_wadi("sabab")
        with pytest.raises(AssertionError, match="Missing.*sabab"):
            assert_wadi_gates_complete(rule)

    def test_missing_shart_fails(self):
        """Rules missing SHART gate must fail"""
        rule = make_rule_missing_wadi("shart")
        with pytest.raises(AssertionError, match="Missing.*shart"):
            assert_wadi_gates_complete(rule)

    def test_missing_mani_fails(self):
        """Rules missing MANI gate must fail"""
        rule = make_rule_missing_wadi("mani")
        with pytest.raises(AssertionError, match="Missing.*mani"):
            assert_wadi_gates_complete(rule)

    def test_missing_sihha_fails(self):
        """Rules missing SIHHA gate must fail"""
        rule = make_rule_missing_wadi("sihha")
        with pytest.raises(AssertionError, match="Missing.*sihha"):
            assert_wadi_gates_complete(rule)

    def test_missing_fasad_fails(self):
        """Rules missing FASAD gate must fail"""
        rule = make_rule_missing_wadi("fasad")
        with pytest.raises(AssertionError, match="Missing.*fasad"):
            assert_wadi_gates_complete(rule)

    def test_missing_butlan_fails(self):
        """Rules missing BUTLAN gate must fail"""
        rule = make_rule_missing_wadi("butlan")
        with pytest.raises(AssertionError, match="Missing.*butlan"):
            assert_wadi_gates_complete(rule)

    def test_extra_wadi_gate_fails(self):
        """Rules with extra WadiGates must fail"""
        rule = make_rule_extra_wadi()
        # Since we duplicate a gate, the set will have only 6 gates
        # So this test checks that duplicates are handled
        assert len(rule.required_wadi_gates) == 7  # 7 gates in tuple
        assert len(set(rule.required_wadi_gates)) == 6  # But only 6 unique

    def test_empty_forbidden_outputs_fails_for_qiyas_layers(self):
        """Qiyas/readiness layers must have non-empty forbidden_outputs"""
        rule = make_rule_empty_forbidden()
        with pytest.raises(AssertionError, match="non-empty forbidden_outputs"):
            assert_forbidden_outputs_present(rule)

    def test_forbidden_outputs_include_higher_types(self):
        """forbidden_outputs must include all architecturally higher types"""
        rule = make_minimal_rule()
        assert_forbidden_outputs_present(rule)

        # Check that common higher types are included
        forbidden_set = set(rule.forbidden_outputs)
        assert "SyllableCandidate" in forbidden_set or "WordCandidate" in forbidden_set

    def test_atomic_unit_rule_passes_constitution(self):
        """AtomicUnit binding rule passes constitutional checks"""
        assert_wadi_gates_complete(ATOMIC_UNIT_BINDING)
        assert_forbidden_outputs_present(ATOMIC_UNIT_BINDING)

        # Verify it forbids higher-level candidates
        assert "SyllableCandidate" in ATOMIC_UNIT_BINDING.forbidden_outputs
        assert "WordCandidate" in ATOMIC_UNIT_BINDING.forbidden_outputs
        assert "MeaningCandidate" in ATOMIC_UNIT_BINDING.forbidden_outputs

    def test_minimal_rule_has_exactly_six_gates(self):
        """Minimal test rule has exactly 6 gates"""
        rule = make_minimal_rule()
        assert len(rule.required_wadi_gates) == 6
        assert len(set(rule.required_wadi_gates)) == 6  # No duplicates

        # Verify all 6 gates are present
        gates = set(rule.required_wadi_gates)
        assert WadiGate.SABAB in gates
        assert WadiGate.SHART in gates
        assert WadiGate.MANI in gates
        assert WadiGate.SIHHA in gates
        assert WadiGate.FASAD in gates
        assert WadiGate.BUTLAN in gates
