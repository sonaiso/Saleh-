"""
test_canonical_phase_prefixes.py — REC2-* enforcement tests

REC-2 (PROJECT_RECOVERY_CANONICAL_MAP.md §3 / §4.1 / §4.2 / §7):
توحيد أسماء الأطوار بالبادئة القانونية SCG- وإسناد كل طبقة إلى أصلها
من الأصول الثلاثة — بلا طبقات جديدة وبلا تقدّم في الحالات.

أقسام الاختبارات:
    REC2-PHASE-*  — كل phase يحمل البادئة SCG- ويطابق سلم §4.2 حرفيًا
    REC2-STATUS-* — لا تقدّم في الحالات (non-goal: no status advancement)
    REC2-COUNT-*  — لا طبقات جديدة (non-goal: no new layers)
    REC2-ORIGIN-* — قانون الإسناد (§3): كل طبقة مسجلة لها أصل من الأصول الثلاثة
    REC2-DOC-*    — LAYER_REGISTRY.md والخريطة يوثقان البادئات والإسناد
"""
from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    build_master_registry_seed,
    build_p0_implemented_registry,
    build_p1_specified_registry,
)
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ORIGIN_NOTES,
    LAYER_ID_P0_GLYPH_CLASSIFICATION,
    LAYER_ID_P0_TYPED_CODEPOINT,
    LAYER_ID_P0_UNICODE_CANDIDATE,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
    LAYER_ID_P10_RELATION_GEOMETRY,
    LAYER_ID_P11_IRAB_GEOMETRY,
    LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    LAYER_ID_P2_REGISTRY_PROJECTION,
    LAYER_ID_P3_ROOT_STEM_CLOSURE,
    LAYER_ID_P4_JAMID_MUSHTAQ,
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
    LAYER_ID_P7_COMPOSITION_READINESS,
    LAYER_ID_P8_AMIL_MAMUL,
    LAYER_ID_P9_SENTENCE_GEOMETRY,
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

# سلم §4.2: المعرف القانوني لكل طبقة ← الطور القانوني بعد REC-2
EXPECTED_PHASE_BY_LAYER_ID = {
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

# الأطوار القديمة قبل REC-2 (عمود "current string" في جدول §4.2) — ممنوعة الآن
FORMER_PHASE_STRINGS = {
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
}

THREE_ORIGINS = {
    ORIGIN_FIRST_PRESERVED_SOUND_TRACE,
    ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    ORIGIN_THIRD_CONVENTIONAL_SIGNIFIED,
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@pytest.fixture
def seed_registry():
    """بذرة السجل الكاملة."""
    return build_master_registry_seed()


@pytest.fixture
def p0_registry():
    """سجل ما بعد PR-CORE-2 (P0 = IMPLEMENTED)."""
    return build_p0_implemented_registry()


@pytest.fixture
def p1_registry():
    """سجل ما بعد PR-CORE-3 (P1 = SPECIFIED)."""
    return build_p1_specified_registry()


# ─────────────────────────────────────────────────────────────────────────────
# REC2-PHASE — البادئة القانونية SCG- (§4.1 / §4.2)
# ─────────────────────────────────────────────────────────────────────────────

class TestCanonicalPhasePrefixes:
    """REC2-PHASE — كل phase في السجل يحمل البادئة SCG- ويطابق §4.2."""

    def test_REC2_PHASE_01_every_phase_has_scg_prefix(self, seed_registry):
        """REC2-PHASE-01: كل طور يبدأ بـ SCG-P (§4.1: BF0 ≠ SCG-P0 ≠ AR-P0)."""
        for spec in seed_registry.all_layers():
            assert spec.phase.startswith("SCG-P"), (
                f"Layer {spec.id} phase {spec.phase!r} "
                f"lacks the canonical SCG- prefix (§4.1)"
            )

    def test_REC2_PHASE_02_no_former_phase_strings_remain(self, seed_registry):
        """REC2-PHASE-02: لا يبقى أي طور قديم — خصوصًا P0_BINARY_FOUNDATION (§6.2)."""
        phases = {spec.phase for spec in seed_registry.all_layers()}
        leftovers = phases & FORMER_PHASE_STRINGS
        assert not leftovers, f"Former phase strings still in use: {leftovers}"
        assert not any("BINARY_FOUNDATION" in p for p in phases), (
            "BINARY_FOUNDATION wording collides with BF0 (Binary-) — §6.2"
        )

    def test_REC2_PHASE_03_phase_set_is_exactly_the_canonical_ladder(
        self, seed_registry
    ):
        """REC2-PHASE-03: مجموعة الأطوار == {SCG-P0 … SCG-P12} حرفيًا."""
        phases = {spec.phase for spec in seed_registry.all_layers()}
        assert phases == CANONICAL_PHASES

    @pytest.mark.parametrize(
        "layer_id,expected_phase",
        sorted(EXPECTED_PHASE_BY_LAYER_ID.items()),
    )
    def test_REC2_PHASE_04_each_layer_carries_its_canonical_phase(
        self, seed_registry, layer_id, expected_phase
    ):
        """REC2-PHASE-04: كل طبقة تحمل طورها القانوني من جدول §4.2."""
        assert seed_registry.get(layer_id).phase == expected_phase

    def test_REC2_PHASE_05_phases_identical_across_all_builders(
        self, seed_registry, p0_registry, p1_registry
    ):
        """REC2-PHASE-05: الأطوار لا تتغير مع تقدّم الحالات في أي بانٍ."""
        for layer_id, expected_phase in EXPECTED_PHASE_BY_LAYER_ID.items():
            assert seed_registry.get(layer_id).phase == expected_phase
            assert p0_registry.get(layer_id).phase == expected_phase
            assert p1_registry.get(layer_id).phase == expected_phase


# ─────────────────────────────────────────────────────────────────────────────
# REC2-STATUS — non-goal: no status advancement
# ─────────────────────────────────────────────────────────────────────────────

class TestNoStatusAdvancement:
    """REC2-STATUS — REC-2 لا يقدّم أي حالة (non-goal من جدول §7)."""

    def test_REC2_STATUS_01_seed_layers_all_planned(self, seed_registry):
        """REC2-STATUS-01: بذرة السجل كلها PLANNED كما قبل REC-2."""
        for spec in seed_registry.all_layers():
            assert spec.status == LayerStatus.PLANNED, (
                f"Layer {spec.id} advanced to {spec.status} — "
                f"REC-2 forbids status advancement"
            )

    def test_REC2_STATUS_02_p0_builder_statuses_unchanged(self, p0_registry):
        """REC2-STATUS-02: بانى P0: طبقات P0 IMPLEMENTED والبقية PLANNED."""
        for spec in p0_registry.all_layers():
            if spec.id in _P0_LAYER_IDS:
                assert spec.status == LayerStatus.IMPLEMENTED
            else:
                assert spec.status == LayerStatus.PLANNED

    def test_REC2_STATUS_03_p1_builder_statuses_unchanged(self, p1_registry):
        """REC2-STATUS-03: بانى P1: P0 IMPLEMENTED، P1 SPECIFIED، البقية PLANNED."""
        for spec in p1_registry.all_layers():
            if spec.id in _P0_LAYER_IDS:
                assert spec.status == LayerStatus.IMPLEMENTED
            elif spec.id in _P1_LAYER_IDS:
                assert spec.status == LayerStatus.SPECIFIED
            else:
                assert spec.status == LayerStatus.PLANNED


# ─────────────────────────────────────────────────────────────────────────────
# REC2-COUNT — non-goal: no new layers
# ─────────────────────────────────────────────────────────────────────────────

class TestNoNewLayers:
    """REC2-COUNT — REC-2 لا يضيف طبقات (non-goal من جدول §7)."""

    def test_REC2_COUNT_01_exactly_nineteen_layers(self, seed_registry):
        """REC2-COUNT-01: عدد الطبقات المسجلة 19 بلا زيادة ولا نقصان."""
        assert len(seed_registry) == 19
        assert len(EXPECTED_PHASE_BY_LAYER_ID) == 19


# ─────────────────────────────────────────────────────────────────────────────
# REC2-ORIGIN — قانون الإسناد (§3 registry-binding)
# ─────────────────────────────────────────────────────────────────────────────

class TestOriginTraceability:
    """REC2-ORIGIN — كل طبقة مسجلة تُسند إلى أصل من الأصول الثلاثة (§3)."""

    def test_REC2_ORIGIN_01_every_registered_layer_has_an_origin_note(
        self, seed_registry
    ):
        """REC2-ORIGIN-01: مفاتيح LAYER_ORIGIN_NOTES == معرفات السجل تمامًا.

        قانون الإسناد: كل طبقة بلا أصل من هذه الأصول الثلاثة
        = خارج المشروع أو تجريبية.
        """
        registered_ids = {spec.id for spec in seed_registry.all_layers()}
        assert set(LAYER_ORIGIN_NOTES) == registered_ids

    def test_REC2_ORIGIN_02_every_origin_is_one_of_the_three(self):
        """REC2-ORIGIN-02: كل قيمة إسناد هي أحد الأصول الثلاثة فقط."""
        for layer_id, origin in LAYER_ORIGIN_NOTES.items():
            assert origin in THREE_ORIGINS, (
                f"Layer {layer_id} traced to unknown origin {origin!r}"
            )

    def test_REC2_ORIGIN_03_all_scg_layers_trace_to_second_origin(self):
        """REC2-ORIGIN-03: جميع طبقات SCG في Saleh- تخدم الأصل الثاني (§3 table)."""
        for layer_id, origin in LAYER_ORIGIN_NOTES.items():
            assert origin == ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM, (
                f"Layer {layer_id} must trace to الأصل الثاني "
                f"(Saleh- algebraic spine), got {origin!r}"
            )

    def test_REC2_ORIGIN_04_origin_constants_are_distinct(self):
        """REC2-ORIGIN-04: الأصول الثلاثة متمايزة — لا دمج بين الأصول."""
        assert len(THREE_ORIGINS) == 3


# ─────────────────────────────────────────────────────────────────────────────
# REC2-DOC — التوثيق في LAYER_REGISTRY.md والخريطة
# ─────────────────────────────────────────────────────────────────────────────

class TestDocumentation:
    """REC2-DOC — LAYER_REGISTRY.md يوثق البادئات والإسناد؛ والخريطة تسجل التنفيذ."""

    def test_REC2_DOC_01_layer_registry_declares_prefix_disambiguation(self):
        """REC2-DOC-01: LAYER_REGISTRY.md يحمل تمييز §4.1 (BF0/SCG-P0/AR-P0)."""
        text = _read(LAYER_REGISTRY_DOC)
        assert "BF0" in text
        assert "SCG-P0" in text
        assert "AR-P0" in text
        assert "Binary-P0 ≠ Arabic-SCG-P0" in text

    def test_REC2_DOC_02_layer_registry_records_conversion_table(self):
        """REC2-DOC-02: جدول التحويل (قديم ← قانوني) كامل في LAYER_REGISTRY.md."""
        text = _read(LAYER_REGISTRY_DOC)
        for former in sorted(FORMER_PHASE_STRINGS):
            assert f"`{former}`" in text, (
                f"Conversion table row for {former} missing from LAYER_REGISTRY.md"
            )
        for canonical in sorted(CANONICAL_PHASES):
            assert f"`{canonical}`" in text, (
                f"Canonical phase {canonical} missing from LAYER_REGISTRY.md"
            )

    def test_REC2_DOC_03_layer_registry_records_origin_traceability(self):
        """REC2-DOC-03: LAYER_REGISTRY.md يحمل قانون الإسناد والأصل الثاني."""
        text = _read(LAYER_REGISTRY_DOC)
        assert "كل طبقة بلا أصل من هذه الأصول الثلاثة" in text
        assert "الأصل الثاني" in text
        assert "LAYER_ORIGIN_NOTES" in text

    def test_REC2_DOC_04_recovery_map_records_execution(self):
        """REC2-DOC-04: الخريطة (§6.2) تسجل أن REC-2 نُفِّذ."""
        text = _read(RECOVERY_MAP_DOC)
        assert "EXECUTED by REC-2" in text
        assert "test_canonical_phase_prefixes.py" in text
