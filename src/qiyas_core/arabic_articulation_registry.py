"""ArabicArticulationRegistry — external data registry only.

This module is a *reader* for the JSON registry that ships at
`qiyas_core/data/arabic_articulation_registry.json`. The registry is
metadata only. Per the JSON's own `constitutional_role` and
`constitutional_constraints` payload, it:

  * is `external_data_registry_only`,
  * does not produce qiyas candidates,
  * does not use `QiyasRule` or `QiyasKernel`,
  * does not produce slot-layer outputs (no slot candidate, no slot
    geometry),
  * does not produce higher-layer outputs (no dalalah, no final
    meaning, no hukm candidate, no reality claim),
  * may support later evidence only — never licenses an algebraic
    transition by itself.

This reader honours that posture by importing nothing from the qiyas
algebra (no candidate primitives, no rule, no kernel, no slot
primitives, no slot-geometry primitives, no recursive-extension or
closure adapters). It is stdlib-only.

Authority basis:

  * PR_SCHEDULING_POLICY.md §1.4 (Data Registry PR shape),
  * RECURSIVE_LICENSED_EXTENSION_CONTRACT.md §12 (consumption
    surface; registries do not stand in for `SlotCandidate*`),
  * MINIMAL_COMPLETE_CLOSURE_CONTRACT.md §1 / §12 (closure is the
    layer's responsibility; this registry only supplies metadata
    that *may* support later evidence).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

_REGISTRY_PACKAGE = "qiyas_core.data"
_REGISTRY_FILENAME = "arabic_articulation_registry.json"


@dataclass(frozen=True)
class ArabicArticulationEntry:
    """One entry from the Arabic articulation registry.

    All fields are immutable. The entry is metadata only; consumers
    must not treat any field as a licensing claim, an identity, an
    alignment proof, or any qiyas evidence by itself.
    """

    id: str
    symbol: str
    form: str | None
    arabic_name: str
    transliteration: str
    makhraj_group: str
    makhraj_group_ar: str
    sub_makhraj_id: str
    sub_makhraj_ar: str
    variant: str
    is_madd: bool
    requires_previous_haraka: str | None
    can_seed_single_slot: bool
    can_extend_previous_slot: bool
    minimal_function_profile: str
    can_function_as_minimal_independent_unit: bool
    independent_unit_kind: str | None
    independent_unit_requires: tuple[str, ...]
    notes: str


def _entry_from_payload(raw: dict) -> ArabicArticulationEntry:
    return ArabicArticulationEntry(
        id=raw["id"],
        symbol=raw["symbol"],
        form=raw.get("form"),
        arabic_name=raw["arabic_name"],
        transliteration=raw["transliteration"],
        makhraj_group=raw["makhraj_group"],
        makhraj_group_ar=raw["makhraj_group_ar"],
        sub_makhraj_id=raw["sub_makhraj_id"],
        sub_makhraj_ar=raw["sub_makhraj_ar"],
        variant=raw["variant"],
        is_madd=raw["is_madd"],
        requires_previous_haraka=raw.get("requires_previous_haraka"),
        can_seed_single_slot=raw["can_seed_single_slot"],
        can_extend_previous_slot=raw["can_extend_previous_slot"],
        minimal_function_profile=raw["minimal_function_profile"],
        can_function_as_minimal_independent_unit=raw[
            "can_function_as_minimal_independent_unit"
        ],
        independent_unit_kind=raw.get("independent_unit_kind"),
        independent_unit_requires=tuple(raw.get("independent_unit_requires", ())),
        notes=raw.get("notes", "") or "",
    )


@lru_cache(maxsize=1)
def load_arabic_articulation_registry() -> tuple[ArabicArticulationEntry, ...]:
    """Load the registry and return all entries as an immutable tuple.

    The JSON file is located via ``importlib.resources`` so the
    registry travels with the installed package and does not depend
    on the current working directory.
    """
    with (
        resources.files(_REGISTRY_PACKAGE)
        .joinpath(_REGISTRY_FILENAME)
        .open("r", encoding="utf-8") as fh
    ):
        payload = json.load(fh)
    return tuple(_entry_from_payload(e) for e in payload["entries"])


def get_articulation_by_id(entry_id: str) -> ArabicArticulationEntry | None:
    """Return the entry whose ``id`` matches, or ``None`` if not found."""
    for entry in load_arabic_articulation_registry():
        if entry.id == entry_id:
            return entry
    return None


def get_articulations_by_symbol(
    symbol: str,
) -> tuple[ArabicArticulationEntry, ...]:
    """Return all entries whose ``symbol`` matches the given symbol.

    Returns an empty tuple if no entry matches.
    """
    return tuple(
        entry
        for entry in load_arabic_articulation_registry()
        if entry.symbol == symbol
    )


def get_primary_articulation(
    symbol: str,
) -> ArabicArticulationEntry | None:
    """Return the single articulation entry for ``symbol``, or ``None``.

    Returns ``None`` when:

      * the symbol has no entry, or
      * the symbol has more than one licensed variant (e.g. ``و`` /
        ``ي`` carry both madd and non-madd entries). Choosing one
        variant without evidence is unconstitutional; this function
        therefore refuses to pick.

    Returns the matching entry when (and only when) the symbol has
    exactly one entry in the registry.
    """
    matches = get_articulations_by_symbol(symbol)
    if len(matches) == 1:
        return matches[0]
    return None


def get_minimal_independent_units() -> tuple[ArabicArticulationEntry, ...]:
    """Return every entry with ``can_function_as_minimal_independent_unit``
    set to ``True``.

    Per the registry's ``minimal_independent_unit_policy`` field, the
    returned entries are *metadata signals* of possible later
    minimal-completion readiness only; they do not by themselves
    license a slot, a closure, or any dalalah evidence. Each entry's
    ``independent_unit_requires`` field names the strictly-later
    proofs that must run before any algebraic admission.
    """
    return tuple(
        entry
        for entry in load_arabic_articulation_registry()
        if entry.can_function_as_minimal_independent_unit
    )
