"""ArabicVariantResolutionEvidence — runtime carrier shape.

Implements the runtime Evidence carrier
``ArabicVariantResolutionEvidence`` per
``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §6.1 (carrier shape) and
``ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md`` §3 (the seven reserved
``selection_basis`` labels).

This module is **carrier-only**. It does NOT define:

  * ``ArabicVariantResolver`` (the producer, reserved by
    ARABIC_VARIANT_RESOLUTION_CONTRACT.md §3.1 for a future
    implementation PR),
  * any consumption of ``ArabicArticulationRegistry``,
  * any ``MinimalUnitReadinessCandidate`` amendment,
  * any ``QiyasKernel`` invocation.

Per contract §2, ``ArabicVariantResolutionEvidence`` is an Evidence
carrier, **not** a ``Candidate``. The carrier deliberately omits
``candidate_type``, ``status``, and ``output_flags`` so it is
structurally NOT a Candidate-shape.

Per contract §6.1, the field layout is fixed and the carrier is
intended for construction by the future resolver only when the §6.1
construction preconditions hold; this module declares the carrier
shape and the reserved label tuples but does not itself enforce
those preconditions. Validation belongs to the producer (a later PR).

Authority basis:
  CLAUDE.md §0 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20,
  ARABIC_VARIANT_RESOLUTION_CONTRACT.md §1 / §2 / §3 / §4 / §6 / §7
    / §8 / §10 / §12 (this module's controlling contract),
  ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md §3 / §7 / §8 / §9 / §16
    (reserved selection_basis labels and license-not-require
    discipline),
  MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md
    (carrier-shape pattern this module follows).
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Reserved label tuples — single source of truth per contract §6.1 / §3
# ---------------------------------------------------------------------------

# ARABIC_VARIANT_RESOLUTION_CONTRACT.md §6.1: exactly two reserved
# variant labels. Future contracts may extend this set when new
# symbol coverage is ratified; this carrier does not introduce
# additional labels.
RESERVED_VARIANT_LABELS: tuple[str, ...] = ("madd", "non_madd")

# ARABIC_VARIANT_RESOLUTION_CONTRACT.md §6.1 (selection_basis block)
# and ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md §3: exactly seven
# reserved selection_basis labels in the canonical order. Future
# implementation contracts may extend this set when new context
# channels are ratified; this contract reserves only these.
RESERVED_SELECTION_BASIS_LABELS: tuple[str, ...] = (
    "haraka_function_before",
    "haraka_function_self",
    "haraka_function_after",
    "preceding_letter_identity",
    "following_letter_identity",
    "registry_default",
    "intra_utterance_position",
)

# ARABIC_VARIANT_RESOLUTION_CONTRACT.md §4 / §6.1: the resolver
# consumes only length=1 seed geometries on the SlotGeometryQiyas
# layer. These are the fixed values the carrier preserves.
FIXED_GEOMETRY_LAYER: str = "SlotGeometryQiyas"
FIXED_GEOMETRY_LENGTH: int = 1
FIXED_GEOMETRY_CONSTRUCTION_MODE: str = "seed"


# ---------------------------------------------------------------------------
# §6.2 audit-trace schema (non-binding) — helpers for emitting the
# recommended ``audit_trace_ids`` strings. The producer is free to
# use a different format that preserves reviewer legibility.
# ---------------------------------------------------------------------------

_AUDIT_TRACE_PREFIX: str = "trace:arabic_variant_resolution:"


def audit_trace_symbol(symbol: str) -> str:
    """§6.2: emit the ``symbol`` audit-trace entry."""
    return f"{_AUDIT_TRACE_PREFIX}symbol:{symbol}"


def audit_trace_selected_variant(variant: str) -> str:
    """§6.2: emit the ``selected_variant`` audit-trace entry."""
    return f"{_AUDIT_TRACE_PREFIX}selected_variant:{variant}"


def audit_trace_selected_entry_id(entry_id: str) -> str:
    """§6.2: emit the ``selected_entry_id`` audit-trace entry."""
    return f"{_AUDIT_TRACE_PREFIX}selected_entry_id:{entry_id}"


def audit_trace_basis(basis_label: str) -> str:
    """§6.2: emit a ``basis`` audit-trace entry — one per basis label.

    Rejects any label not in ``RESERVED_SELECTION_BASIS_LABELS`` —
    the carrier audit-trace schema knows only the seven §3 labels.
    """
    if basis_label not in RESERVED_SELECTION_BASIS_LABELS:
        raise ValueError(
            f"unknown selection_basis label: {basis_label!r}"
        )
    return f"{_AUDIT_TRACE_PREFIX}basis:{basis_label}"


def audit_trace_geometry_id(geometry_candidate_id: str) -> str:
    """§6.2: emit the ``geometry_id`` audit-trace entry."""
    return f"{_AUDIT_TRACE_PREFIX}geometry_id:{geometry_candidate_id}"


# ---------------------------------------------------------------------------
# ArabicVariantResolutionEvidence — frozen Evidence carrier (NOT a Candidate)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArabicVariantResolutionEvidence:
    """Immutable Evidence carrier for Arabic variant resolution.

    Per ``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §2:

      * **Evidence carrier**, not a ``Candidate``.
      * Layer-specific to the ``SlotGeometryQiyas`` length=1
        admission boundary; not portable upward or laterally (§9).
      * Construction is the producer's responsibility; this carrier
        does not enforce §6.1 construction preconditions. A future
        ``ArabicVariantResolver`` (§3.1 reserved name) is the
        gatekeeper.

    Deliberately has **no** ``candidate_type``, **no** ``status``,
    **no** ``output_flags`` field — the carrier is structurally
    NOT a Candidate-shape.
    """

    # The Arabic letter symbol being disambiguated (e.g. "و", "ي").
    # Per §5, the in-scope set is exactly {"و", "ي"} under the
    # current registry; "ا" is reserved as future extensibility only.
    symbol: str

    # The variant label chosen by the resolver — one of
    # RESERVED_VARIANT_LABELS. The producer validates against the
    # registry's entry ids (e.g. lips_waw_non_madd vs jawf_waw_madd).
    selected_variant: str

    # The ArabicArticulationEntry.id whose semantics the resolver
    # selected. Audit anchor back into the registry.
    selected_entry_id: str

    # One or more BASIS-LABEL strings from
    # RESERVED_SELECTION_BASIS_LABELS encoding which contextual
    # witnesses drove the selection. Per §6.1 the producer requires
    # this tuple to be non-empty when constructing the carrier;
    # the carrier shape itself does not encode that constraint.
    selection_basis: tuple[str, ...]

    # Consumed SlotGeometryCandidate audit anchors (§6.1). The
    # geometry_layer / geometry_length / geometry_construction_mode
    # triple is fixed by §4 to ("SlotGeometryQiyas", 1, "seed").
    geometry_candidate_id: str
    geometry_layer: str
    geometry_length: int
    geometry_construction_mode: str

    # The consumed geometry's identity_ids and trace_ids, preserved
    # verbatim — NEVER rewritten, reordered, or downcast.
    geometry_identity_ids: tuple[str, ...]
    geometry_trace_ids: tuple[str, ...]

    # Per-evidence unique identifier — never an identity.
    evidence_id: str

    # Auditable trace strings per §6.2 schema. The producer enforces
    # the §6.1 invariant
    # ``set(geometry_identity_ids) ∩ set(audit_trace_ids) == ∅``
    # at construction time; the carrier exposes both tuples so the
    # disjointness is externally verifiable.
    audit_trace_ids: tuple[str, ...]
