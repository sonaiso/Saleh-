from dataclasses import dataclass


@dataclass(frozen=True)
class SlotRoleSpec:
    """Defines a participant role in a slot operation.

    Roles replace the simple asl/far pattern with richer semantic roles such as:
    - carrier/mark (Unicode layer)
    - nucleus/onset/coda (Phonological layer)
    - root/pattern/affix (Morphological layer)
    - governor/governed (Syntactic layer)
    - entity_anchor/predicate_anchor (Semantic layer)
    """
    role_name: str
    required_type: str
    required_capabilities: tuple[str, ...]
    optional_evidence: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.role_name:
            raise ValueError("role_name is required")
        if not self.required_type:
            raise ValueError("required_type is required")
