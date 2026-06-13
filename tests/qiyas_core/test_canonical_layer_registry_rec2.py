"""REC-2 Canonical Layer Registry alignment — enforcement tests.

Authority: PROJECT_RECOVERY_CANONICAL_MAP.md §3 / §4.1 / §4.2 / §7 (REC-2).
Scope: phase-string prefix discipline + per-layer origin notes.

This is governance alignment, not runtime implementation. The tests
enforce that:

  REC2-PHASE-*     — canonical SCG- prefix on every layer; legacy strings gone
  REC2-COUNT-*     — exactly 19 layers (no additions, no removals)
  REC2-STATUS-*    — no LayerStatus advancement across REC-2
  REC2-ORIGIN-*    — every registered layer has an origin trace
  REC2-DOC-*       — LAYER_REGISTRY.md documents the prefixes and origins
  REC2-AGREE-*     — docs and master_registry_seed.py agree on the prefixes
  REC2-NONGOAL-*   — no HarakaFunctionCarrier rename (REC-3 scope)
                   — no Binary- boundary enforcement attempted in Saleh-
                   — global freeze remains active
                   — Layer 4 narrow authorization remains intact
                   — no Layer 5+ / semantic runtime / meaning / hukm / etc.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    build_master_registry_seed,
    build_p0_implemented_registry,
    build_p1_specified_registry,
)
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P0_GLYPH_CLASSIFICATION,
    LAYER_ID_P0_TYPED_CODEPOINT,
    LAYER_ID_P0_UNICODE_CANDIDATE,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
    LAYER_ID_P2_REGISTRY_PROJECTION,
    LAYER_ID_P3_ROOT_STEM_CLOSURE,
    LAYER_ID_P4_JAMID_MUSHTAQ,
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
    LAYER_ID_P7_COMPOSITION_READINESS,
    LAYER_ID_P8_AMIL_MAMUL,
    LAYER_ID_P9_SENTENCE_GEOMETRY,
    LAYER_ID_P10_RELATION_GEOMETRY,
    LAYER_ID_P11_IRAB_GEOMETRY,
    LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    LAYER_ORIGIN_NOTES,
    ORIGIN_FIRST_PRESERVED_SOUND_TRACE,
    ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    ORIGIN_THIRD_CONVENTIONAL_SIGNIFIED,
    _P0_LAYER_IDS,
    _P1_LAYER_IDS,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "docs" / "qiyas_core"
LAYER_REGISTRY_DOC = DOCS / "LAYER_REGISTRY.md"
RECOVERY_MAP_DOC = DOCS / "PROJECT_RECOVERY_CANONICAL_MAP.md"
MATRIX_DOC = DOCS / "REPOSITORY_RESPONSIBILITY_MATRIX.md"
SRC = REPO_ROOT / "src"
REGISTRY_SEED = SRC / "qiyas_core" / "slot_geometry_core" / "master_registry_seed.py"
LICENSED_SYLLABLE_SRC = SRC / "qiyas_core" / "licensed_syllable.py"


# Per §4.2 conversion table — every layer ID maps to exactly one canonical
# SCG-Pn phase string.
EXPECTED_PHASE_BY_LAYER_ID: dict[str, str] = {
    LAYER_ID_P0_UNICODE_CANDIDATE: "SCG-P0",
    LAYER_ID_P0_TYPED_CODEPOINT: "SCG-P0",
    LAYER_ID_P0_GLYPH_CLASSIFICATION: "SCG-P0",
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER: "SCG-P1",
    LAYER_ID_P1_HARAKA_FUNCTION_CARRIER: "SCG-P1",
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE: "SCG-P1",
    LAYER_ID_P1_POSITION_CARRIER: "SCG-P1",
    LAYER_ID_P1_SLOT_CANDIDATE: "SCG-P1",
    LAYER_ID_P2_REGISTRY_PROJECTION: "SCG-P2",
    LAYER_ID_P3_ROOT_STEM_CLOSURE: "SCG-P3",
    LAYER_ID_P4_JAMID_MUSHTAQ: "SCG-P4",
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS: "SCG-P5",
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE: "SCG-P6",
    LAYER_ID_P7_COMPOSITION_READINESS: "SCG-P7",
    LAYER_ID_P8_AMIL_MAMUL: "SCG-P8",
    LAYER_ID_P9_SENTENCE_GEOMETRY: "SCG-P9",
    LAYER_ID_P10_RELATION_GEOMETRY: "SCG-P10",
    LAYER_ID_P11_IRAB_GEOMETRY: "SCG-P11",
    LAYER_ID_P12_IFADAH_SPEECH_FORCE: "SCG-P12",
}

CANONICAL_PHASES = {f"SCG-P{n}" for n in range(13)}

# Legacy phase strings that REC-2 governs — these must NOT appear as
# `phase="..."` literals in the registry seed any more. The legacy
# identifier *names* (LAYER_ID_P*_* constants) are NOT governed by
# REC-2 — REC-2 renames the `phase` field values only.
LEGACY_PHASE_LITERALS = (
    "P0_BINARY_FOUNDATION",
    "P1_DAL_ALONE_ATOMIC",
    "P2_REGISTRY_PROJECTION",
    "P3_ROOT_STEM_CLOSURE",
    "P4_JAMID_MUSHTAQ",
    "P5_MUFRAD_WORD_CONTRACTS",
    "P6_VERBAL_SIGNIFIED_ALONE",
    "P7_COMPOSITION_READINESS",
    "P8_AMIL_MAMUL",
    "P9_SENTENCE_GEOMETRY",
    "P10_RELATION_GEOMETRY",
    "P11_IRAB_GEOMETRY",
    "P12_IFADAH_SPEECH_FORCE",
)

THREE_ORIGINS = (
    ORIGIN_FIRST_PRESERVED_SOUND_TRACE,
    ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    ORIGIN_THIRD_CONVENTIONAL_SIGNIFIED,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def seed_registry():
    return build_master_registry_seed()


@pytest.fixture(scope="module")
def p0_registry():
    return build_p0_implemented_registry()


@pytest.fixture(scope="module")
def p1_registry():
    return build_p1_specified_registry()


# ─────────────────────────────────────────────────────────────────────────────
# Group 1 — Canonical phase prefixes present everywhere REC-2 governs them
# ─────────────────────────────────────────────────────────────────────────────


def test_rec2_phase_prefixes_present_in_layer_registry_doc() -> None:
    """REC2-DOC-01: LAYER_REGISTRY.md declares BF0 / SCG-P0 / AR-P0 + every
    canonical SCG-Pn appears in the §4.2 conversion table."""
    text = _read(LAYER_REGISTRY_DOC)
    for prefix in ("BF0", "SCG-P0", "AR-P0"):
        assert prefix in text, f"prefix {prefix!r} missing from LAYER_REGISTRY.md"
    assert "Binary-P0 ≠ Arabic-SCG-P0" in text, (
        "phase-prefix disambiguation declaration missing"
    )
    for canonical in sorted(CANONICAL_PHASES):
        assert f"`{canonical}`" in text, (
            f"canonical phase {canonical!r} missing from LAYER_REGISTRY.md table"
        )


def test_rec2_master_registry_seed_uses_canonical_phase_prefixes(
    seed_registry,
) -> None:
    """REC2-PHASE-02: every layer in the seed carries a SCG-Pn phase string."""
    phases = {spec.phase for spec in seed_registry.all_layers()}
    assert phases == CANONICAL_PHASES, (
        f"registry phases must equal canonical SCG- ladder; got {sorted(phases)}"
    )


def test_rec2_no_legacy_unprefixed_phase_strings_for_governed_layers() -> None:
    """REC2-PHASE-03: no `phase="P*_<NAME>"` literal remains in the seed.

    The check inspects the seed source text and asserts that no legacy
    phase literal appears as the value of a `phase=` keyword argument.
    Layer ID *constant names* (LAYER_ID_P*_*) are NOT governed by REC-2
    and are explicitly allowed.
    """
    source = _read(REGISTRY_SEED)
    # Find every `phase="..."` assignment.
    phase_literals = re.findall(r'phase=\s*"([^"]+)"', source)
    assert phase_literals, "expected phase= literals in master_registry_seed.py"
    for literal in phase_literals:
        assert literal in CANONICAL_PHASES, (
            f"non-canonical phase literal {literal!r} remains in seed source"
        )
    for legacy in LEGACY_PHASE_LITERALS:
        assert f'phase="{legacy}"' not in source, (
            f"legacy phase literal phase=\"{legacy}\" remains in seed source"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Group 2 — Three foundational origins documented + per-layer notes
# ─────────────────────────────────────────────────────────────────────────────


def test_rec2_layer_registry_documents_three_foundational_origins() -> None:
    """REC2-DOC-02: LAYER_REGISTRY.md names the three foundational origins."""
    text = _read(LAYER_REGISTRY_DOC)
    assert "preserved sound trace" in text, "origin 1 (preserved sound trace) missing"
    assert "verbal system preserving transitions" in text, (
        "origin 2 (verbal transition system) missing"
    )
    assert "conventional signified" in text, "origin 3 (conventional signified) missing"
    assert "الأصل الأول" in text
    assert "الأصل الثاني" in text
    assert "الأصل الثالث" in text


def test_rec2_each_governed_layer_has_origin_traceability_note(
    seed_registry,
) -> None:
    """REC2-ORIGIN-01: every registered layer ID is keyed in LAYER_ORIGIN_NOTES."""
    registered_ids = {spec.id for spec in seed_registry.all_layers()}
    assert set(LAYER_ORIGIN_NOTES) == registered_ids, (
        "LAYER_ORIGIN_NOTES keys must exactly equal the registered layer IDs"
    )


def test_rec2_origin_values_are_one_of_three() -> None:
    """REC2-ORIGIN-02: every origin note is one of the three foundational origins."""
    for layer_id, origin in LAYER_ORIGIN_NOTES.items():
        assert origin in THREE_ORIGINS, (
            f"layer {layer_id} traced to unknown origin {origin!r}"
        )


def test_rec2_all_seeded_layers_trace_to_second_origin() -> None:
    """REC2-ORIGIN-03: all 19 seeded SCG layers trace to الأصل الثاني
    (Saleh- algebraic spine; verbal transition system)."""
    for layer_id, origin in LAYER_ORIGIN_NOTES.items():
        assert origin == ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM, (
            f"layer {layer_id} must trace to الأصل الثاني; got {origin!r}"
        )


def test_rec2_three_origins_are_distinct_constants() -> None:
    """REC2-ORIGIN-04: the three origin constants are pairwise distinct."""
    assert len(set(THREE_ORIGINS)) == 3


# ─────────────────────────────────────────────────────────────────────────────
# Group 3 — Docs and registry seed agree on the canonical prefixes
# ─────────────────────────────────────────────────────────────────────────────


def test_rec2_docs_and_master_registry_seed_phase_prefixes_agree(
    seed_registry,
) -> None:
    """REC2-AGREE-01: every canonical phase used by the seed appears in the
    LAYER_REGISTRY.md §4.2 table (and vice versa)."""
    text = _read(LAYER_REGISTRY_DOC)
    seed_phases = {spec.phase for spec in seed_registry.all_layers()}
    for phase in seed_phases:
        assert f"`{phase}`" in text, (
            f"seed phase {phase!r} not documented in LAYER_REGISTRY.md table"
        )
    # And: every documented canonical phase is actually used by the seed.
    for canonical in sorted(CANONICAL_PHASES):
        assert canonical in seed_phases, (
            f"canonical phase {canonical!r} documented but not used by seed"
        )


def test_rec2_layer_registry_records_conversion_table() -> None:
    """REC2-DOC-03: the doc records the full former → canonical conversion table."""
    text = _read(LAYER_REGISTRY_DOC)
    for former in LEGACY_PHASE_LITERALS:
        assert f"`{former}`" in text, (
            f"conversion-table row for {former!r} missing"
        )


def test_rec2_layer_registry_records_origin_tracing_rule() -> None:
    """REC2-DOC-04: LAYER_REGISTRY.md carries the tracing rule and references
    LAYER_ORIGIN_NOTES."""
    text = _read(LAYER_REGISTRY_DOC)
    assert "كل طبقة بلا أصل من هذه الأصول الثلاثة" in text
    assert "LAYER_ORIGIN_NOTES" in text


# ─────────────────────────────────────────────────────────────────────────────
# Group 4 — REC-2 non-goals (governance discipline)
# ─────────────────────────────────────────────────────────────────────────────


def test_rec2_does_not_advance_layer_statuses(
    seed_registry, p0_registry, p1_registry
) -> None:
    """REC2-STATUS-01: REC-2 must not change any LayerStatus.

    The three existing builders must still produce: seed=all PLANNED,
    p0_registry=P0 layers IMPLEMENTED / rest PLANNED, p1_registry=P0
    IMPLEMENTED / P1 SPECIFIED / rest PLANNED.
    """
    for spec in seed_registry.all_layers():
        assert spec.status == LayerStatus.PLANNED, (
            f"seed layer {spec.id} status changed to {spec.status} under REC-2"
        )
    for spec in p0_registry.all_layers():
        expected = (
            LayerStatus.IMPLEMENTED
            if spec.id in _P0_LAYER_IDS
            else LayerStatus.PLANNED
        )
        assert spec.status == expected, (
            f"p0 builder advanced {spec.id} unexpectedly to {spec.status}"
        )
    for spec in p1_registry.all_layers():
        if spec.id in _P0_LAYER_IDS:
            expected = LayerStatus.IMPLEMENTED
        elif spec.id in _P1_LAYER_IDS:
            expected = LayerStatus.SPECIFIED
        else:
            expected = LayerStatus.PLANNED
        assert spec.status == expected, (
            f"p1 builder advanced {spec.id} unexpectedly to {spec.status}"
        )


def test_rec2_does_not_introduce_new_layers(seed_registry) -> None:
    """REC2-COUNT-01: exactly 19 layers in the seed; same set as before REC-2."""
    assert len(seed_registry) == 19
    assert len(EXPECTED_PHASE_BY_LAYER_ID) == 19
    seed_ids = {spec.id for spec in seed_registry.all_layers()}
    assert seed_ids == set(EXPECTED_PHASE_BY_LAYER_ID)


def test_rec2_does_not_rename_haraka_function_carrier() -> None:
    """REC2-NONGOAL-01: the HarakaFunctionCarrier rename is REC-3 scope, not REC-2.

    The registry must still carry the legacy name on the layer-ID constant
    and on the LayerSpec, and the recovery map must still record the rename
    as pending under REC-3.
    """
    assert LAYER_ID_P1_HARAKA_FUNCTION_CARRIER == "P1_HARAKA_FUNCTION_CARRIER"
    seed_source = _read(REGISTRY_SEED)
    assert "HarakaFunctionCarrierLayer" in seed_source, (
        "HarakaFunctionCarrier layer name unexpectedly removed (REC-3 not REC-2)"
    )
    # The §7 queue must still list REC-3 with the rename target name.
    map_text = _read(RECOVERY_MAP_DOC)
    assert "HarakaMarkIdentityCarrier" in map_text


def test_rec2_does_not_touch_binary_boundary_enforcement() -> None:
    """REC2-NONGOAL-02: Saleh- does not perform Binary- boundary enforcement.

    REC-4 is maintainer-only inside Binary-. This PR must not introduce any
    binary_core import or src/binary_core/ package.
    """
    assert not (SRC / "binary_core").exists(), (
        "src/binary_core/ must not exist in Saleh-"
    )
    binary_import = re.compile(r"^\s*(?:from|import)\s+binary_core\b", re.MULTILINE)
    for path in (REGISTRY_SEED, LICENSED_SYLLABLE_SRC):
        if path.exists():
            assert not binary_import.search(_read(path)), (
                f"{path} imports binary_core — REC-4 must not run from Saleh-"
            )


def test_rec2_freeze_remains_active() -> None:
    """REC2-NONGOAL-03: the global REC freeze remains active. PROJECT FREEZE
    declaration in §1 of the recovery map is preserved verbatim."""
    map_text = _read(RECOVERY_MAP_DOC)
    assert "PROJECT FREEZE is in effect" in map_text
    assert "REC-1 … REC-4" in map_text or "REC-1 … REC-4" in map_text


def test_rec2_layer4_narrow_authorization_remains_intact() -> None:
    """REC2-NONGOAL-04: the Layer 4 narrow authorization (PR #135) remains
    intact: the matrix doc §4.1, the recovery map §1.1, and the licensed
    syllable runtime module are all still present and unmodified by REC-2."""
    assert LICENSED_SYLLABLE_SRC.is_file(), (
        "Layer 4 module src/qiyas_core/licensed_syllable.py must remain present"
    )
    licensed_source = _read(LICENSED_SYLLABLE_SRC)
    assert 'LAYER4_RUNTIME_STATUS = "layer4_potential_only"' in licensed_source
    assert 'CANDIDATE_RUNTIME_STATUS = "potential_only_not_semantic_runtime"' in (
        licensed_source
    )
    # Matrix doc §4.1 still records the narrow Layer 4 authorization.
    matrix_text = _read(MATRIX_DOC)
    assert "Narrow Layer 4 authorization" in matrix_text
    assert "LicensedSyllableCandidate" in matrix_text
    # Recovery map §1.1 still records the narrow Layer 4 authorization.
    assert "Narrow Layer 4 authorization" in _read(RECOVERY_MAP_DOC)


def test_rec2_no_layer5_runtime_or_semantic_runtime() -> None:
    """REC2-NONGOAL-05: no Layer 5+ class names appear as standalone tokens
    in the registry seed, and no new semantic-runtime surface is introduced.

    The check uses word-boundary regex so that `MufradWordCandidate` (a
    legitimate existing P5 output_type) does NOT trip the `WordCandidate`
    guard. Standalone occurrences of the forbidden names are tolerated
    only when quoted inside the `_ABSOLUTE_FORBIDDEN` enumeration.
    """
    seed_source = _read(REGISTRY_SEED)
    forbidden_layer5_names = (
        "WordCandidate",
        "LafzCandidate",
        "DalalahCandidate",
        "HukmCandidate",
        "FinalMeaning",
        "RealityClaim",
        "SemanticRuntime",
    )
    for name in forbidden_layer5_names:
        # Match the name as a standalone identifier (word boundaries on
        # both sides). This excludes substrings inside longer names like
        # `MufradWordCandidate`.
        pattern = re.compile(r"\b" + re.escape(name) + r"\b")
        for lineno, line in enumerate(seed_source.splitlines(), start=1):
            if not pattern.search(line):
                continue
            # Allowed only inside the explicit constitutional negation:
            # the `_ABSOLUTE_FORBIDDEN` tuple lists them as quoted strings.
            quoted_in_forbidden_enum = (
                f'"{name}"' in line or f"'{name}'" in line
            )
            assert quoted_in_forbidden_enum, (
                f"forbidden Layer 5+ name {name!r} appears outside the "
                f"_ABSOLUTE_FORBIDDEN enumeration at line {lineno}: {line!r}"
            )


def test_rec2_no_meaning_hukm_irab_dalalah_reality_claims() -> None:
    """REC2-NONGOAL-06: REC-2 introduces no positive meaning / hukm / i'rab /
    dalalah / reality claim — the seed source carries no such positive
    assertions, only the existing _ABSOLUTE_FORBIDDEN enumeration."""
    seed_source = _read(REGISTRY_SEED)
    forbidden_positive_phrases = (
        "meaning introduced",
        "hukm introduced",
        "i'rab introduced",
        "dalalah introduced",
        "reality claim introduced",
        "semantic runtime enabled",
    )
    lowered = seed_source.lower()
    for phrase in forbidden_positive_phrases:
        assert phrase not in lowered, (
            f"forbidden positive phrase {phrase!r} appeared in registry seed source"
        )
