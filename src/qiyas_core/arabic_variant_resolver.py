"""ArabicVariantResolver — runtime producer for variant resolution.

Implements the producer reserved by
``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §3.1.

The producer is **observation only**. Per contract §3.2 / §3.3 it:

  * consumes the closed surface in §4 (``SlotGeometryCandidate(length=1)``
    + ``ArabicArticulationRegistry`` metadata, read-only, + already-
    preserved trace/identity context on the geometry),
  * does NOT modify the input geometry,
  * does NOT produce a ``Candidate`` of any type,
  * does NOT invoke ``QiyasKernel.apply``,
  * does NOT re-read raw text or call ``SequenceContextTokenizer``,
  * does NOT call back into ``MinimalIndependentUnitReadinessLayerAdapter``,
  * does NOT consume any higher-layer typed unit
    (``WordCandidate`` / ``LafzCandidate`` / ``DalalahCandidate`` /
    ``FinalMeaning`` / ``HukmCandidate`` / ``RealityClaim`` /
    ``MinimalUnitReadinessCandidate``).

Returns ``ArabicVariantResolutionEvidence | None``. Per §7 absence of
licensed basis is **always** ``None`` (DEFER-equivalent) — never a
BLOCK at this layer.

Per ``ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md`` §§4-5 the licensed
``(symbol, variant, basis)`` admissibility table is:

  ``(و, non_madd, haraka_function_self)``     — primary
  ``(و, non_madd, intra_utterance_position)`` — secondary, with primary
  ``(و, madd,     haraka_function_before)``   — only basis for madd on و
  ``(ي, non_madd, haraka_function_self)``     — primary
  ``(ي, non_madd, intra_utterance_position)`` — secondary, with primary
  ``(ي, madd,     haraka_function_before)``   — only basis for madd on ي

For ``ا`` the resolver returns ``None`` per §6 (future extensibility
only).

This initial implementation supports **only** the primary
``haraka_function_self`` basis for non_madd. Both other admissible
bases (``intra_utterance_position`` secondary; ``haraka_function_before``
for madd) require neighbouring-slot context that is not preserved on
Phase-1 length=1 seed geometries; per §4.4 / §5.4 the resolver
returns ``None`` in those cases (DEFER, not BLOCK). A strictly later
implementation contract may extend coverage when richer context
becomes available.

Authority basis:
  CLAUDE.md §0 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20,
  ARABIC_VARIANT_RESOLUTION_CONTRACT.md §1 / §3 / §4 / §6 / §7 / §8
    / §10 / §12,
  ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md §3 / §4 / §5 / §6 / §7
    / §8 / §9 / §16.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Protocol

from .arabic_articulation_registry import (
    ArabicArticulationEntry,
    get_articulations_by_symbol,
)
from .arabic_variant_resolution_evidence import (
    FIXED_GEOMETRY_CONSTRUCTION_MODE,
    FIXED_GEOMETRY_LAYER,
    FIXED_GEOMETRY_LENGTH,
    ArabicVariantResolutionEvidence,
    audit_trace_basis,
    audit_trace_geometry_id,
    audit_trace_selected_entry_id,
    audit_trace_selected_variant,
    audit_trace_symbol,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Symbols currently in scope per §5 of the resolution contract.
# `ا` is reserved as future extensibility only (§6) and not included.
_IN_SCOPE_SYMBOLS: frozenset[str] = frozenset({"و", "ي"})

# Arabic letter range — mirrors the MIU readiness adapter convention
# (`_ARABIC_LETTER_RANGE = (0x0621, 0x064A)`).
_ARABIC_LETTER_RANGE: tuple[int, int] = (0x0621, 0x064A)

# Active-haraka range — non-sukun harakat license non_madd via the
# primary basis ``haraka_function_self`` per §4.1 / §5.1 of the
# selection-rules contract. Range covers tanwin (0x064B..0x064D),
# fatha / damma / kasra (0x064E..0x0650), and shadda (0x0651).
# Sukun (0x0652) is **excluded** — its presence is the canonical
# signal of madd potential (§4.2 / §5.2) which requires a different
# basis (haraka_function_before) not implemented in this PR.
_ACTIVE_HARAKA_RANGE: tuple[int, int] = (0x064B, 0x0651)
_SUKUN_CODEPOINT: int = 0x0652

# Slot-geometry metadata-trace prefixes — mirror
# ``slot_geometry_closure_check`` and ``minimal_unit_readiness_adapter``.
_LENGTH_TRACE_PREFIX: str = "trace:slot_geometry:length:"
_MODE_TRACE_PREFIX: str = "trace:slot_geometry:construction_mode:"

_IDENTITY_CODEPOINT_PREFIX: str = "identity:codepoint:"

_EVIDENCE_ID_PREFIX: str = "ev:arabic_variant_resolver:"


# ---------------------------------------------------------------------------
# Public-facing Protocol — duck-typed SlotGeometryCandidate interface.
# Only the fields the resolver actually reads are declared.
# ---------------------------------------------------------------------------


class SlotGeometryCandidateLike(Protocol):
    """Structural interface this producer expects from its input.

    A real ``qiyas_core.candidate.Candidate`` with
    ``candidate_type == "SlotGeometryCandidate"`` satisfies this
    protocol; so does any test fixture that exposes the same
    attributes.
    """

    candidate_type: str
    layer: str
    candidate_id: str
    identity_ids: tuple[str, ...]
    trace_ids: tuple[str, ...]


# ---------------------------------------------------------------------------
# Geometry-shape predicates and field readers
# ---------------------------------------------------------------------------


def _read_length_from_trace(geom: Any) -> int | None:
    for tid in getattr(geom, "trace_ids", ()):
        if isinstance(tid, str) and tid.startswith(_LENGTH_TRACE_PREFIX):
            try:
                return int(tid[len(_LENGTH_TRACE_PREFIX):])
            except ValueError:
                return None
    return None


def _read_construction_mode_from_trace(geom: Any) -> str | None:
    for tid in getattr(geom, "trace_ids", ()):
        if isinstance(tid, str) and tid.startswith(_MODE_TRACE_PREFIX):
            return tid[len(_MODE_TRACE_PREFIX):]
    return None


def _is_length_one_seed_geometry(geom: Any) -> bool:
    """§4 surface gate: only ``SlotGeometryCandidate(length=1,
    construction_mode="seed")`` on the ``SlotGeometryQiyas`` layer
    is admissible. Anything else returns ``None`` upstream."""
    if getattr(geom, "candidate_type", None) != "SlotGeometryCandidate":
        return False
    if getattr(geom, "layer", None) != FIXED_GEOMETRY_LAYER:
        return False
    if _read_length_from_trace(geom) != FIXED_GEOMETRY_LENGTH:
        return False
    return (
        _read_construction_mode_from_trace(geom)
        == FIXED_GEOMETRY_CONSTRUCTION_MODE
    )


def _extract_letter_codepoint(geom: Any) -> int | None:
    """Return the first Arabic-letter codepoint carried by the
    geometry's ``identity_ids``, or ``None`` when no letter is
    present. Mirrors the MIU adapter convention so the resolver and
    readiness adapter agree on what counts as 'the slot's letter'."""
    lo, hi = _ARABIC_LETTER_RANGE
    for iid in getattr(geom, "identity_ids", ()):
        if not (isinstance(iid, str) and iid.startswith(
            _IDENTITY_CODEPOINT_PREFIX
        )):
            continue
        try:
            cp = int(iid[len(_IDENTITY_CODEPOINT_PREFIX):], 16)
        except ValueError:
            continue
        if lo <= cp <= hi:
            return cp
    return None


def _extract_haraka_codepoint(geom: Any) -> int | None:
    """Return the first haraka codepoint (active or sukun) on the
    geometry's ``identity_ids``, or ``None`` if no haraka is present.

    Per the slot-composition rule §2.1 a Phase-1 SlotCandidate
    requires a haraka pillar, so a real length=1 seed geometry will
    always carry a haraka codepoint. ``None`` is the defensive return
    for malformed fixtures (per CLAUDE.md §4 invariant 7:
    malformed ⇒ DEFER, never BLOCK)."""
    lo, hi = _ACTIVE_HARAKA_RANGE
    for iid in getattr(geom, "identity_ids", ()):
        if not (isinstance(iid, str) and iid.startswith(
            _IDENTITY_CODEPOINT_PREFIX
        )):
            continue
        try:
            cp = int(iid[len(_IDENTITY_CODEPOINT_PREFIX):], 16)
        except ValueError:
            continue
        if (lo <= cp <= hi) or cp == _SUKUN_CODEPOINT:
            return cp
    return None


def _is_active_haraka(cp: int) -> bool:
    """An active (non-sukun) haraka is the witness §4.1 / §5.1
    requires for the primary ``haraka_function_self`` basis."""
    lo, hi = _ACTIVE_HARAKA_RANGE
    return lo <= cp <= hi


def _select_entry_by_variant(
    entries: tuple[ArabicArticulationEntry, ...],
    variant: str,
) -> ArabicArticulationEntry | None:
    """Return the entry whose ``variant`` field matches, or ``None``
    when no entry exists for the requested variant."""
    for entry in entries:
        if entry.variant == variant:
            return entry
    return None


# ---------------------------------------------------------------------------
# ArabicVariantResolver — the producer
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArabicVariantResolver:
    """Deterministic producer of ``ArabicVariantResolutionEvidence``.

    Per ``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §3:

      * **Not** a Qiyas layer.
      * **Not** a ``QiyasRule``.
      * **Does not** invoke ``QiyasKernel.apply``.
      * **Does not** produce a ``Candidate`` of any type.
      * Returns ``ArabicVariantResolutionEvidence | None``.

    Construction is deterministic: given the same
    ``SlotGeometryCandidate`` and the same registry state the
    resolver returns either equivalent evidence (modulo the
    nondeterministic ``evidence_id`` uuid) or ``None`` — never one
    and then the other.

    The class is stateless; instances are interchangeable. A
    ``resolve(geom)`` call and a ``call(geom)`` are equivalent.
    """

    def resolve(
        self,
        geometry: SlotGeometryCandidateLike,
    ) -> ArabicVariantResolutionEvidence | None:
        return _resolve(geometry)

    def __call__(
        self,
        geometry: SlotGeometryCandidateLike,
    ) -> ArabicVariantResolutionEvidence | None:
        return _resolve(geometry)


def resolve_arabic_variant(
    geometry: SlotGeometryCandidateLike,
) -> ArabicVariantResolutionEvidence | None:
    """Module-level convenience — equivalent to
    ``ArabicVariantResolver().resolve(geometry)``."""
    return _resolve(geometry)


# ---------------------------------------------------------------------------
# Internal resolution driver
# ---------------------------------------------------------------------------


def _resolve(geom: Any) -> ArabicVariantResolutionEvidence | None:
    # §4 surface gate.
    if not _is_length_one_seed_geometry(geom):
        return None

    # Identify the slot's letter from the geometry's identity_ids.
    letter_cp = _extract_letter_codepoint(geom)
    if letter_cp is None:
        return None
    symbol = chr(letter_cp)

    # §5 registry-level ambiguity check: if the symbol has at most
    # one registry entry, the resolver does not apply (§5 — covers
    # ب / ف / ك / ل / س / أ / ت etc. — and also any future symbol
    # the registry resolves uniquely).
    entries = get_articulations_by_symbol(symbol)
    if len(entries) <= 1:
        return None

    # §5 / §6 scope: this contract reserves variant semantics for
    # ``و`` and ``ي`` only. ``ا`` is future-extensibility only and
    # is excluded explicitly; any other multi-variant symbol a future
    # registry amendment may introduce is also excluded until its
    # own constitutional amendment merges.
    if symbol not in _IN_SCOPE_SYMBOLS:
        return None

    # §4.1 / §5.1: read the slot's own haraka witness. An active
    # (non-sukun) haraka licenses non_madd via haraka_function_self.
    haraka_cp = _extract_haraka_codepoint(geom)
    if haraka_cp is None:
        return None
    if not _is_active_haraka(haraka_cp):
        # Sukun-bearing letter. The madd reading (§4.2 / §5.2)
        # would require the preceding-slot's haraka via the
        # ``haraka_function_before`` basis — not preserved on a
        # Phase-1 length=1 seed geometry. Per §7 (absence ≠ BLOCK):
        # return None.
        return None

    selected_variant = "non_madd"
    selected_entry = _select_entry_by_variant(entries, selected_variant)
    if selected_entry is None:
        # The symbol has multiple entries but none labelled
        # ``non_madd`` — structurally impossible for {و, ي} under
        # the current registry, but defer rather than crash.
        return None

    selection_basis = ("haraka_function_self",)

    audit_trace_ids = (
        audit_trace_symbol(symbol),
        audit_trace_selected_variant(selected_variant),
        audit_trace_selected_entry_id(selected_entry.id),
        audit_trace_basis("haraka_function_self"),
        audit_trace_geometry_id(geom.candidate_id),
    )

    return ArabicVariantResolutionEvidence(
        symbol=symbol,
        selected_variant=selected_variant,
        selected_entry_id=selected_entry.id,
        selection_basis=selection_basis,
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        evidence_id=f"{_EVIDENCE_ID_PREFIX}{uuid.uuid4().hex[:12]}",
        audit_trace_ids=audit_trace_ids,
    )
