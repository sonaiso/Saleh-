from .rule import QiyasRule
from .enums import WadiGate


class ValidationError(ValueError):
    pass


def validate_rule(rule: QiyasRule) -> None:
    if len(set(rule.required_effective_wasf)) != len(rule.required_effective_wasf):
        raise ValidationError("required_effective_wasf must not contain duplicates")
    if len(set(rule.required_illah)) != len(rule.required_illah):
        raise ValidationError("required_illah must not contain duplicates")
    if len(set(rule.required_wadi_gates)) != len(rule.required_wadi_gates):
        raise ValidationError("required_wadi_gates must not contain duplicates")
    if len(set(rule.invalidating_differences)) != len(rule.invalidating_differences):
        raise ValidationError("invalidating_differences must not contain duplicates")

    # Enforce all six constitutional WadiGate requirements (exact equality)
    required_gates = {
        WadiGate.CAUSE,
        WadiGate.CONDITION,
        WadiGate.OBSTACLE,
        WadiGate.VALIDITY,
        WadiGate.CORRUPTION,
        WadiGate.NULLITY,
    }
    actual_gates = set(rule.required_wadi_gates)

    if actual_gates != required_gates:
        if not required_gates.issubset(actual_gates):
            missing = required_gates - actual_gates
            raise ValidationError(
                f"Rule must require exactly the six WadiGates. Missing: {sorted(g.value for g in missing)}"
            )
        else:
            extra = actual_gates - required_gates
            raise ValidationError(
                f"Rule must require exactly the six WadiGates. Extra: {sorted(g.value for g in extra)}"
            )
