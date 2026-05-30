import pytest

from qiyas_core.registry import QiyasRegistry
from tests.qiyas_core.helpers import build_rule


def test_registry_rejects_duplicate_rule_id():
    registry = QiyasRegistry()
    rule = build_rule()

    registry.register(rule)

    with pytest.raises(ValueError, match="Duplicate rule_id"):
        registry.register(rule)
