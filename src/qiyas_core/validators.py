from .rule import QiyasRule


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
