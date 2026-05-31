from enum import Enum


class SlotDirection(Enum):
    """Operational directionality of a slot."""
    INTERNAL = "internal"
    LEFT_TO_RIGHT = "left_to_right"
    RIGHT_TO_LEFT = "right_to_left"
    BIDIRECTIONAL = "bidirectional"
    CONTEXTUAL = "contextual"


class SlotBoundary(Enum):
    """Scope boundaries for slot operations."""
    INTRA_ATOMIC = "intra_atomic"
    INTRA_LAFZ = "intra_lafz"
    INTRA_WORD = "intra_word"
    INTER_WORD = "inter_word"
    INTRA_COMPOSITION = "intra_composition"
    INTER_SENTENCE = "inter_sentence"
    MAQAM_CONTEXT = "maqam_context"


class SlotState(Enum):
    """Lifecycle state of a slot instance."""
    OPEN = "open"
    PARTIAL = "partial"
    FILLED = "filled"
    DEFERRED = "deferred"
    BLOCKED = "blocked"
    CONFLICTED = "conflicted"
    CLOSED = "closed"


class SlotMultiplicity(Enum):
    """Multiplicity policy for slot candidates."""
    SINGLE = "single"
    MULTIPLE = "multiple"


class SlotAmbiguityPolicy(Enum):
    """Policy for handling ambiguous slot fills."""
    DEFER = "defer"
    RANK = "rank"
    BLOCK = "block"
