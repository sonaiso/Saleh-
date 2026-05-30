from dataclasses import dataclass, field

from .rule import QiyasRule
from .validators import validate_rule


@dataclass
class QiyasRegistry:
    _rules: dict[str, QiyasRule] = field(default_factory=dict)

    def register(self, rule: QiyasRule) -> None:
        validate_rule(rule)
        if rule.rule_id in self._rules:
            raise ValueError(f"Duplicate rule_id: {rule.rule_id}")
        self._rules[rule.rule_id] = rule

    def get(self, rule_id: str) -> QiyasRule:
        return self._rules[rule_id]

    def all(self) -> tuple[QiyasRule, ...]:
        return tuple(self._rules.values())

    def rules_for_layer(self, layer: str) -> tuple[QiyasRule, ...]:
        return tuple(rule for rule in self._rules.values() if rule.layer == layer)
