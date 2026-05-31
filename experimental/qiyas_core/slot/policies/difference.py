from dataclasses import dataclass


@dataclass(frozen=True)
class SlotDifferencePolicy:
    """Policy for handling differences during slot analysis.

    Distinguishes between different types of differences:
    - Invalidating: Completely invalid
    - Blocking: Prevents slot from being filled
    - Deferring: Requires deferral until more evidence
    - Ranking: Lowers rank but doesn't block
    - Non-blocking: Acceptable variation
    """
    invalidating_differences: tuple[str, ...]
    blocking_differences: tuple[str, ...]
    deferring_differences: tuple[str, ...]
    ranking_differences: tuple[str, ...]
    non_blocking_differences: tuple[str, ...]
