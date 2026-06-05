"""Tests for ArabicVariantResolutionEvidence runtime carrier.

Pins the constitutional contract of
``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §6.1 (carrier shape) and
``ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md`` §3 (the seven reserved
``selection_basis`` labels) for the runtime carrier itself:

  * ``ArabicVariantResolutionEvidence`` is an Evidence carrier — **not**
    a ``Candidate`` (contract §2).
  * The carrier is a frozen dataclass (mutation raises
    ``FrozenInstanceError``).
  * The carrier has no Candidate-shape fields (``candidate_type``,
    ``status``, ``output_flags``).
  * The two reserved variant labels and seven reserved
    selection_basis labels match the contract verbatim.
  * The §6.2 audit-trace schema helpers emit the documented strings
    and reject unreserved basis labels.
  * The module does NOT define ``ArabicVariantResolver`` yet — the
    producer is reserved for a future implementation PR per §3.1.
  * The module does NOT define any forbidden Candidate type
    (``ArabicVariantResolutionCandidate``, ``WordCandidate``,
    ``LafzCandidate``, ``DalalahCandidate``, ``FinalMeaning``,
    ``HukmCandidate``, ``RealityClaim``, ``FinalCaseJudgment``).
  * The module does NOT import ``QiyasKernel`` — per §3.3 even the
    future producer is forbidden from invoking ``QiyasKernel.apply``.
"""

from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

from qiyas_core import arabic_variant_resolution_evidence as avre
from qiyas_core.arabic_variant_resolution_evidence import (
    ArabicVariantResolutionEvidence,
    FIXED_GEOMETRY_CONSTRUCTION_MODE,
    FIXED_GEOMETRY_LAYER,
    FIXED_GEOMETRY_LENGTH,
    RESERVED_SELECTION_BASIS_LABELS,
    RESERVED_VARIANT_LABELS,
    audit_trace_basis,
    audit_trace_geometry_id,
    audit_trace_selected_entry_id,
    audit_trace_selected_variant,
    audit_trace_symbol,
)


# ---------------------------------------------------------------------------
# Reserved-label invariants — pinned verbatim from the contract
# ---------------------------------------------------------------------------


def test_reserved_variant_labels_match_contract_verbatim() -> None:
    """§6.1: exactly two reserved variant labels in canonical order."""
    assert RESERVED_VARIANT_LABELS == ("madd", "non_madd")


def test_reserved_selection_basis_labels_match_contract_verbatim() -> None:
    """§6.1 / §3: exactly seven reserved selection_basis labels in
    canonical order."""
    assert RESERVED_SELECTION_BASIS_LABELS == (
        "haraka_function_before",
        "haraka_function_self",
        "haraka_function_after",
        "preceding_letter_identity",
        "following_letter_identity",
        "registry_default",
        "intra_utterance_position",
    )


def test_fixed_geometry_constraints_match_contract() -> None:
    """§4 / §6.1: the resolver consumes only length=1 seed geometries
    on the SlotGeometryQiyas layer."""
    assert FIXED_GEOMETRY_LAYER == "SlotGeometryQiyas"
    assert FIXED_GEOMETRY_LENGTH == 1
    assert FIXED_GEOMETRY_CONSTRUCTION_MODE == "seed"


# ---------------------------------------------------------------------------
# Carrier shape — §6.1 field layout, frozen, NOT a Candidate
# ---------------------------------------------------------------------------


def test_carrier_is_frozen_dataclass() -> None:
    """The carrier MUST be a frozen dataclass — mutation raises."""
    assert dataclasses.is_dataclass(ArabicVariantResolutionEvidence)
    evidence = _make_sample_evidence()
    with pytest.raises(dataclasses.FrozenInstanceError):
        evidence.selected_variant = "madd"  # type: ignore[misc]


def test_carrier_has_all_section_6_1_fields() -> None:
    """§6.1: the field layout is fixed by the contract."""
    field_names = {
        f.name for f in dataclasses.fields(ArabicVariantResolutionEvidence)
    }
    assert field_names == {
        "symbol",
        "selected_variant",
        "selected_entry_id",
        "selection_basis",
        "geometry_candidate_id",
        "geometry_layer",
        "geometry_length",
        "geometry_construction_mode",
        "geometry_identity_ids",
        "geometry_trace_ids",
        "evidence_id",
        "audit_trace_ids",
    }


def test_carrier_has_no_candidate_shape_fields() -> None:
    """§2: the carrier is structurally NOT a Candidate-shape.

    Per CLAUDE.md §9 / §11 and contract §6 the carrier MUST NOT
    expose ``candidate_type``, ``status``, or ``output_flags``."""
    field_names = {
        f.name for f in dataclasses.fields(ArabicVariantResolutionEvidence)
    }
    assert "candidate_type" not in field_names
    assert "status" not in field_names
    assert "output_flags" not in field_names


def test_carrier_can_be_instantiated_with_well_formed_fields() -> None:
    """Smoke: a §6.1-shaped instance is constructible."""
    evidence = _make_sample_evidence()
    assert evidence.symbol == "و"
    assert evidence.selected_variant == "non_madd"
    assert evidence.selected_entry_id == "lips_waw_non_madd"
    assert "haraka_function_self" in evidence.selection_basis
    assert evidence.geometry_layer == FIXED_GEOMETRY_LAYER
    assert evidence.geometry_length == FIXED_GEOMETRY_LENGTH
    assert (
        evidence.geometry_construction_mode
        == FIXED_GEOMETRY_CONSTRUCTION_MODE
    )


def test_carrier_preserves_geometry_audit_anchors_verbatim() -> None:
    """§6.1: identity_ids and trace_ids are preserved verbatim —
    NEVER rewritten, reordered, or downcast."""
    identity_ids = (
        "identity:codepoint:0648",
        "identity:codepoint:064e",
        "identity:slot_geometry_domain",
    )
    trace_ids = (
        "trace:fixture:waw_seed",
        "trace:slot_geometry:length:1",
        "trace:slot_geometry:construction_mode:seed",
    )
    evidence = _make_sample_evidence(
        geometry_identity_ids=identity_ids,
        geometry_trace_ids=trace_ids,
    )
    assert evidence.geometry_identity_ids == identity_ids
    assert evidence.geometry_trace_ids == trace_ids


def test_identity_trace_separation_is_externally_verifiable() -> None:
    """§6.1: ``set(geometry_identity_ids) ∩ set(audit_trace_ids) == ∅``
    is the producer's invariant. The carrier exposes both tuples so
    the disjointness is externally verifiable by tests and consumers.
    """
    evidence = _make_sample_evidence()
    assert set(evidence.geometry_identity_ids).isdisjoint(
        set(evidence.audit_trace_ids)
    )


def test_carrier_accepts_multi_basis_selection() -> None:
    """§6.1: selection_basis is a tuple of one or more BASIS-LABEL
    strings; the carrier shape supports multiple bases."""
    evidence = _make_sample_evidence(
        selection_basis=(
            "haraka_function_self",
            "intra_utterance_position",
        ),
    )
    assert evidence.selection_basis == (
        "haraka_function_self",
        "intra_utterance_position",
    )


# ---------------------------------------------------------------------------
# §6.2 audit-trace helpers
# ---------------------------------------------------------------------------


def test_audit_trace_helpers_emit_documented_schema() -> None:
    """§6.2: helpers emit the recommended schema strings."""
    assert (
        audit_trace_symbol("و")
        == "trace:arabic_variant_resolution:symbol:و"
    )
    assert (
        audit_trace_selected_variant("non_madd")
        == "trace:arabic_variant_resolution:selected_variant:non_madd"
    )
    assert (
        audit_trace_selected_entry_id("lips_waw_non_madd")
        == "trace:arabic_variant_resolution:selected_entry_id:lips_waw_non_madd"
    )
    assert (
        audit_trace_basis("haraka_function_self")
        == "trace:arabic_variant_resolution:basis:haraka_function_self"
    )
    assert (
        audit_trace_geometry_id("geom:fixture:abc123")
        == "trace:arabic_variant_resolution:geometry_id:geom:fixture:abc123"
    )


def test_audit_trace_basis_rejects_unreserved_label() -> None:
    """§3: only the seven reserved labels are known to the carrier's
    audit-trace schema."""
    with pytest.raises(ValueError):
        audit_trace_basis("invented_basis_label")


def test_audit_trace_basis_accepts_every_reserved_label() -> None:
    """Every label in RESERVED_SELECTION_BASIS_LABELS is acceptable."""
    for label in RESERVED_SELECTION_BASIS_LABELS:
        entry = audit_trace_basis(label)
        assert entry == f"trace:arabic_variant_resolution:basis:{label}"


# ---------------------------------------------------------------------------
# Scope guards — producer not defined, no forbidden symbols, no kernel
# ---------------------------------------------------------------------------


def test_module_does_not_define_resolver_class_yet() -> None:
    """This PR's scope is the carrier only. The reserved producer
    name ``ArabicVariantResolver`` (§3.1) is for a future
    implementation PR."""
    assert not hasattr(avre, "ArabicVariantResolver")


def test_module_does_not_define_forbidden_candidate_types() -> None:
    """The carrier-only module MUST NOT define Candidate types per
    §8 / §12 forbidden outputs."""
    forbidden = (
        "ArabicVariantResolutionCandidate",
        "WordCandidate",
        "LafzCandidate",
        "SentenceCandidate",
        "ParagraphCandidate",
        "DalalahCandidate",
        "FinalMeaning",
        "HukmCandidate",
        "RealityClaim",
        "FinalCaseJudgment",
        "SlotCandidate",
        "SlotGeometryCandidate",
        "MinimalUnitReadinessCandidate",
    )
    for name in forbidden:
        assert not hasattr(avre, name), (
            f"forbidden symbol must not be defined here: {name}"
        )


def _imported_module_names(module) -> set[str]:
    """Return the set of dotted module names this module imports.

    Looks at the AST so docstring/contract citations that mention
    forbidden names by name (e.g. ``QiyasKernel.apply``) do not
    trigger scope-guard tests — only real imports do.
    """
    tree = ast.parse(inspect.getsource(module))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
    return imported


def test_module_does_not_import_qiyas_kernel() -> None:
    """Per §3.3 even the future producer is forbidden from invoking
    ``QiyasKernel.apply``. The carrier module is observation shape
    only and must not import ``qiyas_core.kernel``."""
    imported = _imported_module_names(avre)
    assert "qiyas_core.kernel" not in imported


def test_module_does_not_amend_minimal_unit_readiness() -> None:
    """Per the PR scope (no MIU adapter amendment), the carrier
    module must not reach into the readiness adapter."""
    imported = _imported_module_names(avre)
    assert "qiyas_core.minimal_unit_readiness_adapter" not in imported


def test_module_does_not_import_articulation_registry() -> None:
    """Per the PR scope (no registry changes / no producer), the
    carrier module does not consume the registry. Registry lookup,
    if any, belongs to the future producer."""
    imported = _imported_module_names(avre)
    assert "qiyas_core.arabic_articulation_registry" not in imported


# ---------------------------------------------------------------------------
# Sample-instance helper
# ---------------------------------------------------------------------------


def _make_sample_evidence(
    *,
    symbol: str = "و",
    selected_variant: str = "non_madd",
    selected_entry_id: str = "lips_waw_non_madd",
    selection_basis: tuple[str, ...] = ("haraka_function_self",),
    geometry_candidate_id: str = "geom:fixture:waw_seed",
    geometry_identity_ids: tuple[str, ...] = (
        "identity:codepoint:0648",
        "identity:codepoint:064e",
    ),
    geometry_trace_ids: tuple[str, ...] = (
        "trace:fixture:waw_seed",
        "trace:slot_geometry:length:1",
        "trace:slot_geometry:construction_mode:seed",
    ),
    evidence_id: str = "ev:arabic_variant_resolution:fixture_001",
    audit_trace_ids: tuple[str, ...] = (
        "trace:arabic_variant_resolution:symbol:و",
        "trace:arabic_variant_resolution:selected_variant:non_madd",
        "trace:arabic_variant_resolution:selected_entry_id:lips_waw_non_madd",
        "trace:arabic_variant_resolution:basis:haraka_function_self",
        "trace:arabic_variant_resolution:geometry_id:geom:fixture:waw_seed",
    ),
) -> ArabicVariantResolutionEvidence:
    return ArabicVariantResolutionEvidence(
        symbol=symbol,
        selected_variant=selected_variant,
        selected_entry_id=selected_entry_id,
        selection_basis=selection_basis,
        geometry_candidate_id=geometry_candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=geometry_identity_ids,
        geometry_trace_ids=geometry_trace_ids,
        evidence_id=evidence_id,
        audit_trace_ids=audit_trace_ids,
    )
