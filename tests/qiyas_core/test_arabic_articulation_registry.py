"""Tests for ArabicArticulationRegistry — Data Registry Batch PR.

Per ``PR_SCHEDULING_POLICY.md`` §1.4, the data file, the derived
artifact, the reader, and the tests ship in one PR. These tests pin
the registry's shape, its consultation API, and — critically — the
reader's non-qiyas constitutional posture:

    * does not produce ``Candidate``,
    * does not use ``QiyasRule``,
    * does not use ``QiyasKernel``,
    * does not produce ``SlotCandidate`` or ``SlotGeometry``,
    * does not produce ``DalalahCandidate``, ``FinalMeaning``,
      ``HukmCandidate``, or ``RealityClaim``,
    * does not license algebraic transitions by itself.

The import-line guards below (§ "reader does not import algebra
primitives") enforce this at the module level so future drift is
caught by CI rather than by review.
"""

from __future__ import annotations

import inspect
import json
from importlib import resources

from qiyas_core import arabic_articulation_registry as registry
from qiyas_core.arabic_articulation_registry import (
    ArabicArticulationEntry,
    get_articulation_by_id,
    get_articulations_by_symbol,
    get_minimal_independent_units,
    get_primary_articulation,
    load_arabic_articulation_registry,
)


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------


def test_registry_has_32_entries():
    """Spec test 1: the registry currently contains exactly 32 entries."""
    assert len(load_arabic_articulation_registry()) == 32


def test_registry_groups_are_jawf_throat_tongue_lips_only():
    """Spec test 2: only the four makharij groups (jawf / halq /
    lisan / shafatan) appear; the Arabic transliterations used by
    this registry are jawf / throat / tongue / lips."""
    groups = {e.makhraj_group for e in load_arabic_articulation_registry()}
    assert groups == {"jawf", "throat", "tongue", "lips"}


def test_qaf_group_is_tongue():
    """Spec test 3: ق belongs to the tongue group."""
    entry = get_articulation_by_id("tongue_qaf")
    assert entry is not None
    assert entry.symbol == "ق"
    assert entry.makhraj_group == "tongue"


def test_kaf_group_is_tongue():
    """Spec test 4: ك belongs to the tongue group."""
    entry = get_articulation_by_id("tongue_kaf")
    assert entry is not None
    assert entry.symbol == "ك"
    assert entry.makhraj_group == "tongue"


def test_hamza_core_group_is_throat():
    """Spec test 5: the core hamza ء belongs to the throat group."""
    entry = get_articulation_by_id("throat_hamza_core")
    assert entry is not None
    assert entry.symbol == "ء"
    assert entry.makhraj_group == "throat"


def test_ba_group_is_lips():
    """Spec test 6: ب belongs to the lips group."""
    entry = get_articulation_by_id("lips_ba")
    assert entry is not None
    assert entry.symbol == "ب"
    assert entry.makhraj_group == "lips"


# ---------------------------------------------------------------------------
# Madd / non-madd separation
# ---------------------------------------------------------------------------


def test_alif_madd_is_madd_and_cannot_seed_single_slot():
    """Spec test 7: the madd alif is flagged as madd and cannot
    seed a single slot — it must extend a previously-licensed slot."""
    entry = get_articulation_by_id("jawf_alif_madd")
    assert entry is not None
    assert entry.is_madd is True
    assert entry.can_seed_single_slot is False


def test_waw_madd_differs_from_waw_non_madd():
    """Spec test 8: the symbol و carries two licensed variants — the
    madd waw (in jawf) and the non-madd waw (in lips). They are
    distinct entries."""
    waws = get_articulations_by_symbol("و")
    assert len(waws) == 2
    ids = {e.id for e in waws}
    assert ids == {"jawf_waw_madd", "lips_waw_non_madd"}
    variants = {e.variant for e in waws}
    assert variants == {"madd", "non_madd"}


def test_ya_madd_differs_from_ya_non_madd():
    """Spec test 9: the symbol ي carries two licensed variants — the
    madd ya (in jawf) and the non-madd ya (in tongue). They are
    distinct entries."""
    yas = get_articulations_by_symbol("ي")
    assert len(yas) == 2
    ids = {e.id for e in yas}
    assert ids == {"jawf_ya_madd", "tongue_ya_non_madd"}
    variants = {e.variant for e in yas}
    assert variants == {"madd", "non_madd"}


# ---------------------------------------------------------------------------
# Interrogative hamza is a distinct functional record
# ---------------------------------------------------------------------------


def test_functional_interrogative_hamza_exists():
    """Spec test 10: همزة الاستفهام أ is registered as its own
    functional entry, distinct from the core hamza ء."""
    entry = get_articulation_by_id("functional_interrogative_hamza")
    assert entry is not None
    assert entry.symbol == "أ"
    assert entry.variant == "orthographic_functional_hamza"
    assert entry.makhraj_group == "throat"
    assert entry.arabic_name == "همزة الاستفهام"


# ---------------------------------------------------------------------------
# Minimal independent units
# ---------------------------------------------------------------------------


def test_minimal_independent_units_are_exactly_eight_symbols():
    """Spec test 11: ``can_function_as_minimal_independent_unit ==
    True`` returns exactly the eight core letters fixed by the
    registry's minimal_independent_unit_policy."""
    units = get_minimal_independent_units()
    symbols = {e.symbol for e in units}
    assert symbols == {"و", "ف", "ب", "ك", "ل", "س", "أ", "ت"}


def test_contextual_letters_are_not_minimal_independent_units():
    """Spec test 12: ن / ه / م / ا are NOT minimal independent
    units — they are contextual / bound markers per the registry's
    own minimal_independent_unit_policy."""
    units = get_minimal_independent_units()
    unit_symbols = {e.symbol for e in units}
    for symbol in ("ن", "ه", "م", "ا"):
        assert symbol not in unit_symbols, (
            f"{symbol!r} must not be a minimal independent unit; "
            "it is a contextual / bound marker per the registry."
        )


# ---------------------------------------------------------------------------
# Missing-data behaviour
# ---------------------------------------------------------------------------


def test_get_articulations_by_unknown_symbol_returns_empty_tuple():
    """Spec test 13a: an unknown symbol yields ``()`` from
    ``get_articulations_by_symbol``."""
    assert get_articulations_by_symbol("Z") == ()


def test_get_articulation_by_unknown_id_returns_none():
    """Spec test 13b: an unknown id yields ``None`` from
    ``get_articulation_by_id``."""
    assert get_articulation_by_id("does_not_exist") is None


def test_get_primary_articulation_unknown_symbol_returns_none():
    """Spec test 13c: an unknown symbol yields ``None`` from
    ``get_primary_articulation``."""
    assert get_primary_articulation("Z") is None


# ---------------------------------------------------------------------------
# Primary-articulation discipline
# ---------------------------------------------------------------------------


def test_get_primary_articulation_qaf_returns_the_qaf_entry():
    """Spec test 14: ق has exactly one entry, so primary returns it."""
    primary = get_primary_articulation("ق")
    assert primary is not None
    assert primary.id == "tongue_qaf"
    assert primary.symbol == "ق"


def test_get_primary_articulation_waw_returns_none_due_to_variants():
    """Spec test 15: و carries two licensed variants; choosing one
    without evidence would be unconstitutional, so primary returns
    None."""
    assert get_primary_articulation("و") is None


def test_get_primary_articulation_ya_returns_none_due_to_variants():
    """Spec test 15 (companion): ي carries two licensed variants;
    same discipline as و."""
    assert get_primary_articulation("ي") is None


# ---------------------------------------------------------------------------
# Reader does not import algebra primitives
# ---------------------------------------------------------------------------


def _reader_import_lines() -> list[str]:
    """Return the reader's actual ``import`` / ``from … import``
    statement lines, stripped — docstring mentions of the forbidden
    names do not count."""
    source = inspect.getsource(registry)
    return [
        line.strip()
        for line in source.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]


def test_reader_does_not_import_candidate():
    """Spec test 16: the reader does not import ``Candidate`` (or
    anything from a qiyas candidate module)."""
    for line in _reader_import_lines():
        assert "Candidate" not in line, (
            f"reader must not import Candidate: {line!r}"
        )
        assert "qiyas_core.candidate" not in line, (
            f"reader must not import from qiyas_core.candidate: {line!r}"
        )


def test_reader_does_not_import_qiyas_rule():
    """Spec test 17: the reader does not import ``QiyasRule`` (or
    anything from the rules module)."""
    for line in _reader_import_lines():
        assert "QiyasRule" not in line, (
            f"reader must not import QiyasRule: {line!r}"
        )
        assert "qiyas_core.rule" not in line, (
            f"reader must not import from qiyas_core.rule: {line!r}"
        )
        assert "qiyas_core.rules" not in line, (
            f"reader must not import from qiyas_core.rules: {line!r}"
        )


def test_reader_does_not_import_qiyas_kernel():
    """Spec test 18: the reader does not import ``QiyasKernel``."""
    for line in _reader_import_lines():
        assert "QiyasKernel" not in line, (
            f"reader must not import QiyasKernel: {line!r}"
        )
        assert "qiyas_core.kernel" not in line, (
            f"reader must not import from qiyas_core.kernel: {line!r}"
        )


def test_reader_does_not_import_slot_candidate_or_slot_geometry():
    """Spec test 19: the reader does not import ``SlotCandidate``,
    ``SlotGeometry``, or any slot-layer adapter."""
    for line in _reader_import_lines():
        assert "SlotCandidate" not in line, (
            f"reader must not import SlotCandidate: {line!r}"
        )
        assert "SlotGeometry" not in line, (
            f"reader must not import SlotGeometry: {line!r}"
        )
        assert "slot_adapter" not in line, (
            f"reader must not import slot_adapter: {line!r}"
        )


# ---------------------------------------------------------------------------
# JSON declares its non-qiyas constitutional posture
# ---------------------------------------------------------------------------


def test_registry_json_declares_external_data_registry_role():
    """Spec test 20: the JSON file itself declares
    ``constitutional_role == "external_data_registry_only"``, so any
    future reader sees its non-qiyas posture before any code-level
    decision is taken."""
    with (
        resources.files("qiyas_core.data")
        .joinpath("arabic_articulation_registry.json")
        .open("r", encoding="utf-8") as fh
    ):
        payload = json.load(fh)
    assert payload["constitutional_role"] == "external_data_registry_only"


# ---------------------------------------------------------------------------
# Dataclass is frozen
# ---------------------------------------------------------------------------


def test_arabic_articulation_entry_is_frozen():
    """Sanity check: ``ArabicArticulationEntry`` is a frozen
    dataclass — entries are immutable, mirroring the read-only nature
    of the registry."""
    entry = get_articulation_by_id("tongue_qaf")
    assert entry is not None
    try:
        entry.symbol = "X"  # type: ignore[misc]
    except Exception as exc:
        assert "frozen" in str(exc).lower() or isinstance(exc, AttributeError)
        return
    raise AssertionError("ArabicArticulationEntry should be frozen")
