"""
test_master_registry_p0_implemented.py — الاختبارات الدستورية لـ PR-CORE-2

PR-CORE-2: تسجيل حالة التنفيذ الفعلي لطبقات P0 في MasterLayerRegistry.

الانتقال: PLANNED → SPECIFIED → IMPLEMENTED
الطبقات المُنفَّذة: P0_UNICODE_CANDIDATE، P0_TYPED_CODEPOINT، P0_GLYPH_CLASSIFICATION
الطبقات المتبقية: P1-P12 تبقى PLANNED

أقسام الاختبارات:
    CORE2-STATUS-*   — التحقق من حالة P0 بعد التقدم
    CORE2-SEED-*     — البذرة الأصلية لم تتأثر (كل طبقاتها لا تزال PLANNED)
    CORE2-P1PLUS-*   — P1-P12 لا تزال PLANNED
    CORE2-TRANSITION-* — الانتقالات المتسلسلة صحيحة (PLANNED→SPECIFIED→IMPLEMENTED)
    CORE2-SOURCE-*   — الملفات المصدرية موثقة
    CORE2-INVARIANT-* — الثوابت الدستورية محفوظة
    CORE2-NONJUMP-*  — لا قفز مباشر من PLANNED إلى IMPLEMENTED
"""
import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    MasterLayerRegistry,
    RegistryViolation,
    build_master_registry_seed,
    build_p0_implemented_registry,
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
    _P0_IMPLEMENTATION_SOURCES,
    _P0_LAYER_IDS,
)


@pytest.fixture
def p0_registry() -> MasterLayerRegistry:
    """سجل مع P0 بحالة IMPLEMENTED — مشترك بين جميع الاختبارات."""
    return build_p0_implemented_registry()


@pytest.fixture
def seed_registry() -> MasterLayerRegistry:
    """البذرة الأصلية — كل الطبقات PLANNED."""
    return build_master_registry_seed()


# ─────────────────────────────────────────────────────────────────────────────
# CORE2-STATUS — حالة طبقات P0 بعد التقدم
# ─────────────────────────────────────────────────────────────────────────────

class TestP0Status:
    """CORE2-STATUS — طبقات P0 وصلت إلى حالة IMPLEMENTED."""

    def test_CORE2_STATUS_01_p0_unicode_candidate_is_implemented(self, p0_registry):
        """CORE2-STATUS-01: P0_UNICODE_CANDIDATE وصلت إلى IMPLEMENTED."""
        spec = p0_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE2_STATUS_02_p0_typed_codepoint_is_implemented(self, p0_registry):
        """CORE2-STATUS-02: P0_TYPED_CODEPOINT وصلت إلى IMPLEMENTED."""
        spec = p0_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE2_STATUS_03_p0_glyph_classification_is_implemented(self, p0_registry):
        """CORE2-STATUS-03: P0_GLYPH_CLASSIFICATION وصلت إلى IMPLEMENTED."""
        spec = p0_registry.get(LAYER_ID_P0_GLYPH_CLASSIFICATION)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE2_STATUS_04_exactly_three_implemented_layers(self, p0_registry):
        """CORE2-STATUS-04: ثلاث طبقات فقط بحالة IMPLEMENTED — لا أكثر."""
        implemented = p0_registry.layers_by_status(LayerStatus.IMPLEMENTED)
        assert len(implemented) == 3

    def test_CORE2_STATUS_05_all_p0_layers_are_implemented(self, p0_registry):
        """CORE2-STATUS-05: جميع طبقات P0 الثلاث بحالة IMPLEMENTED."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert spec.status == LayerStatus.IMPLEMENTED, (
                f"Layer {layer_id} should be IMPLEMENTED, got {spec.status}"
            )

    def test_CORE2_STATUS_06_implemented_layer_ids_are_p0_only(self, p0_registry):
        """CORE2-STATUS-06: الطبقات المُنفَّذة هي P0 فقط — لا غيرها."""
        implemented = p0_registry.layers_by_status(LayerStatus.IMPLEMENTED)
        implemented_ids = {s.id for s in implemented}
        expected_ids = set(_P0_LAYER_IDS)
        assert implemented_ids == expected_ids

    def test_CORE2_STATUS_07_sixteen_layers_remain_planned(self, p0_registry):
        """CORE2-STATUS-07: ستة عشر طبقة تبقى بحالة PLANNED (P1-P12 = 16)."""
        planned = p0_registry.layers_by_status(LayerStatus.PLANNED)
        assert len(planned) == 16

    def test_CORE2_STATUS_08_no_specified_layers_after_advancement(self, p0_registry):
        """CORE2-STATUS-08: لا توجد طبقات بحالة SPECIFIED بعد اكتمال التقدم."""
        specified = p0_registry.layers_by_status(LayerStatus.SPECIFIED)
        assert len(specified) == 0

    def test_CORE2_STATUS_09_total_layer_count_unchanged(self, p0_registry):
        """CORE2-STATUS-09: عدد الطبقات الإجمالي لم يتغير — 19 طبقة."""
        assert len(p0_registry) == 19

    def test_CORE2_STATUS_10_no_audited_or_closed_layers(self, p0_registry):
        """CORE2-STATUS-10: لا توجد طبقات بحالة AUDITED أو CLOSED."""
        audited = p0_registry.layers_by_status(LayerStatus.AUDITED)
        closed = p0_registry.layers_by_status(LayerStatus.CLOSED)
        assert len(audited) == 0
        assert len(closed) == 0


# ─────────────────────────────────────────────────────────────────────────────
# CORE2-SEED — البذرة الأصلية لم تتأثر
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedUnchanged:
    """CORE2-SEED — build_master_registry_seed() لا تزال كل طبقاتها PLANNED."""

    def test_CORE2_SEED_01_original_seed_still_all_planned(self, seed_registry):
        """CORE2-SEED-01: البذرة الأصلية لا تزال كل طبقاتها PLANNED بعد PR-CORE-2."""
        planned = seed_registry.layers_by_status(LayerStatus.PLANNED)
        assert len(planned) == 19

    def test_CORE2_SEED_02_seed_p0_unicode_still_planned(self, seed_registry):
        """CORE2-SEED-02: P0_UNICODE_CANDIDATE في البذرة لا تزال PLANNED."""
        spec = seed_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert spec.status == LayerStatus.PLANNED

    def test_CORE2_SEED_03_seed_p0_typed_still_planned(self, seed_registry):
        """CORE2-SEED-03: P0_TYPED_CODEPOINT في البذرة لا تزال PLANNED."""
        spec = seed_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        assert spec.status == LayerStatus.PLANNED

    def test_CORE2_SEED_04_seed_p0_glyph_still_planned(self, seed_registry):
        """CORE2-SEED-04: P0_GLYPH_CLASSIFICATION في البذرة لا تزال PLANNED."""
        spec = seed_registry.get(LAYER_ID_P0_GLYPH_CLASSIFICATION)
        assert spec.status == LayerStatus.PLANNED

    def test_CORE2_SEED_05_p0_registry_is_independent_copy(self, seed_registry, p0_registry):
        """CORE2-SEED-05: السجلان مستقلان — التقدم في p0 لا يؤثر على البذرة."""
        seed_spec = seed_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        p0_spec = p0_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert seed_spec.status == LayerStatus.PLANNED
        assert p0_spec.status == LayerStatus.IMPLEMENTED


# ─────────────────────────────────────────────────────────────────────────────
# CORE2-P1PLUS — P1-P12 تبقى PLANNED
# ─────────────────────────────────────────────────────────────────────────────

class TestP1PlusRemainPlanned:
    """CORE2-P1PLUS — طبقات P1-P12 لا تزال PLANNED."""

    _P1_TO_P12_IDS = [
        LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
        LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
        LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
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
    ]

    @pytest.mark.parametrize("layer_id", _P1_TO_P12_IDS)
    def test_CORE2_P1PLUS_01_p1_to_p12_still_planned(self, p0_registry, layer_id):
        """CORE2-P1PLUS-01: طبقات P1-P12 لا تزال PLANNED — لا تنفيذ بلا خطة."""
        spec = p0_registry.get(layer_id)
        assert spec.status == LayerStatus.PLANNED, (
            f"Layer {layer_id} should still be PLANNED, got {spec.status}"
        )

    def test_CORE2_P1PLUS_02_p1_slot_candidate_not_implemented(self, p0_registry):
        """CORE2-P1PLUS-02: SlotCandidate لا تزال PLANNED — لا قفز إلى التنفيذ."""
        spec = p0_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert spec.status == LayerStatus.PLANNED

    def test_CORE2_P1PLUS_03_p12_ifadah_not_implemented(self, p0_registry):
        """CORE2-P1PLUS-03: IfadahSpeechForce لا تزال PLANNED — لا قفز للمعنى."""
        spec = p0_registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
        assert spec.status == LayerStatus.PLANNED


# ─────────────────────────────────────────────────────────────────────────────
# CORE2-TRANSITION — الانتقالات المتسلسلة صحيحة
# ─────────────────────────────────────────────────────────────────────────────

class TestStatusTransitions:
    """CORE2-TRANSITION — لا قفز مباشر من PLANNED إلى IMPLEMENTED."""

    def test_CORE2_TRANSITION_01_cannot_jump_planned_to_implemented(self):
        """CORE2-TRANSITION-01: لا يجوز الانتقال من PLANNED مباشرةً إلى IMPLEMENTED."""
        registry = build_master_registry_seed()
        with pytest.raises(RegistryViolation):
            # محاولة القفز مباشرة من PLANNED إلى IMPLEMENTED — يجب أن تفشل
            registry.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.IMPLEMENTED)

    def test_CORE2_TRANSITION_02_must_pass_through_specified(self):
        """CORE2-TRANSITION-02: الانتقال يجب أن يمر عبر SPECIFIED."""
        registry = build_master_registry_seed()
        # PLANNED → SPECIFIED (مسموح)
        registry.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.SPECIFIED)
        spec = registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert spec.status == LayerStatus.SPECIFIED
        # SPECIFIED → IMPLEMENTED (مسموح)
        registry.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.IMPLEMENTED)
        spec = registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE2_TRANSITION_03_cannot_jump_planned_to_audited(self):
        """CORE2-TRANSITION-03: لا يجوز الانتقال من PLANNED إلى AUDITED مباشرة."""
        registry = build_master_registry_seed()
        with pytest.raises(RegistryViolation):
            registry.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.AUDITED)

    def test_CORE2_TRANSITION_04_cannot_jump_planned_to_closed(self):
        """CORE2-TRANSITION-04: لا يجوز الانتقال من PLANNED إلى CLOSED مباشرة."""
        registry = build_master_registry_seed()
        with pytest.raises(RegistryViolation):
            registry.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.CLOSED)

    def test_CORE2_TRANSITION_05_build_function_does_not_skip_specified(self):
        """CORE2-TRANSITION-05: build_p0_implemented_registry مر عبر SPECIFIED بشكل صحيح."""
        # اختبار التحقق: إذا كانت الدالة قفزت مباشرة لكانت RegistryViolation
        # وصول IMPLEMENTED يثبت أن المرور عبر SPECIFIED كان صحيحًا
        registry = build_p0_implemented_registry()
        for layer_id in _P0_LAYER_IDS:
            spec = registry.get(layer_id)
            assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE2_TRANSITION_06_implemented_cannot_go_back_to_planned(self):
        """CORE2-TRANSITION-06: IMPLEMENTED لا يرجع إلى PLANNED."""
        registry = build_p0_implemented_registry()
        with pytest.raises(RegistryViolation):
            registry.update_status(LAYER_ID_P0_UNICODE_CANDIDATE, LayerStatus.PLANNED)


# ─────────────────────────────────────────────────────────────────────────────
# CORE2-SOURCE — الملفات المصدرية موثقة
# ─────────────────────────────────────────────────────────────────────────────

class TestImplementationSources:
    """CORE2-SOURCE — الطبقات المُنفَّذة لها توثيق مصادر."""

    def test_CORE2_SOURCE_01_all_p0_layers_have_source_documentation(self):
        """CORE2-SOURCE-01: كل طبقة P0 لها ملف مصدر موثق."""
        for layer_id in _P0_LAYER_IDS:
            assert layer_id in _P0_IMPLEMENTATION_SOURCES, (
                f"Layer {layer_id} must have documented implementation source"
            )

    def test_CORE2_SOURCE_02_unicode_candidate_source_is_unicode_adapter(self):
        """CORE2-SOURCE-02: P0_UNICODE_CANDIDATE مصدرها unicode_adapter.py."""
        source = _P0_IMPLEMENTATION_SOURCES[LAYER_ID_P0_UNICODE_CANDIDATE]
        assert "unicode_adapter" in source

    def test_CORE2_SOURCE_03_typed_codepoint_source_is_typed_codepoint_adapter(self):
        """CORE2-SOURCE-03: P0_TYPED_CODEPOINT مصدرها typed_codepoint_adapter.py."""
        source = _P0_IMPLEMENTATION_SOURCES[LAYER_ID_P0_TYPED_CODEPOINT]
        assert "typed_codepoint_adapter" in source

    def test_CORE2_SOURCE_04_glyph_classification_source_is_glyph_registry(self):
        """CORE2-SOURCE-04: P0_GLYPH_CLASSIFICATION مصدرها glyph_classification_registry.py."""
        source = _P0_IMPLEMENTATION_SOURCES[LAYER_ID_P0_GLYPH_CLASSIFICATION]
        assert "glyph_classification_registry" in source

    def test_CORE2_SOURCE_05_exactly_three_sources_documented(self):
        """CORE2-SOURCE-05: ثلاثة مصادر فقط موثقة — تطابق ثلاث طبقات P0."""
        assert len(_P0_IMPLEMENTATION_SOURCES) == 3


# ─────────────────────────────────────────────────────────────────────────────
# CORE2-INVARIANT — الثوابت الدستورية محفوظة
# ─────────────────────────────────────────────────────────────────────────────

class TestP0ImplementedInvariants:
    """CORE2-INVARIANT — الثوابت الدستورية محفوظة بعد التقدم."""

    def test_CORE2_INVARIANT_01_p0_forbidden_outputs_preserved(self, p0_registry):
        """CORE2-INVARIANT-01: الطبقات P0 لا تزال تحفظ قوائم المحظورات بعد التقدم."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert len(spec.forbidden_outputs) > 0, (
                f"Layer {layer_id} must declare forbidden_outputs"
            )

    def test_CORE2_INVARIANT_02_p0_absolute_forbidden_still_present(self, p0_registry):
        """CORE2-INVARIANT-02: المحظورات المطلقة (HukmCandidate/RealityClaim/FinalMeaning) موجودة."""
        _ABSOLUTE = ("HukmCandidate", "RealityClaim", "FinalMeaning")
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            for forbidden in _ABSOLUTE:
                assert forbidden in spec.forbidden_outputs, (
                    f"Layer {layer_id} must forbid {forbidden}"
                )

    def test_CORE2_INVARIANT_03_p0_minimum_required_fields_preserved(self, p0_registry):
        """CORE2-INVARIANT-03: حقول الاكتمال الأدنى محفوظة بعد التقدم."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert len(spec.minimum_required_fields) > 0, (
                f"Layer {layer_id} must declare minimum_required_fields"
            )

    def test_CORE2_INVARIANT_04_p0_preserves_ids_declared(self, p0_registry):
        """CORE2-INVARIANT-04: كل طبقة P0 تُعلن عن الهويات التي تحافظ عليها."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert len(spec.preserves_ids) > 0, (
                f"Layer {layer_id} must declare preserves_ids"
            )

    def test_CORE2_INVARIANT_05_p0_origin_chain_intact(self, p0_registry):
        """CORE2-INVARIANT-05: سلسلة الأصل لطبقات P0 سليمة بعد التقدم."""
        unicode_spec = p0_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        typed_spec = p0_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        glyph_spec = p0_registry.get(LAYER_ID_P0_GLYPH_CLASSIFICATION)

        assert unicode_spec.origin.layer_id == "ROOT"
        assert typed_spec.origin.layer_id == LAYER_ID_P0_UNICODE_CANDIDATE
        assert glyph_spec.origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT

    def test_CORE2_INVARIANT_06_p0_no_slot_candidate_in_forbidden_outputs(
        self, p0_registry
    ):
        """CORE2-INVARIANT-06: طبقات P0 تحظر SlotCandidate صراحةً."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert "SlotCandidate" in spec.forbidden_outputs, (
                f"Layer {layer_id} must forbid SlotCandidate"
            )

    def test_CORE2_INVARIANT_07_p0_no_slot_geometry_in_forbidden_outputs(
        self, p0_registry
    ):
        """CORE2-INVARIANT-07: طبقات P0 تحظر SlotGeometry صراحةً."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert "SlotGeometry" in spec.forbidden_outputs, (
                f"Layer {layer_id} must forbid SlotGeometry"
            )

    def test_CORE2_INVARIANT_08_p0_forbidden_changes_include_assign_meaning(
        self, p0_registry
    ):
        """CORE2-INVARIANT-08: طبقات P0 تحظر assign_meaning في التغييرات المحظورة."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert "assign_meaning" in spec.forbidden_changes, (
                f"Layer {layer_id} must forbid assign_meaning"
            )

    def test_CORE2_INVARIANT_09_p0_phases_unchanged_after_advancement(self, p0_registry):
        """CORE2-INVARIANT-09: مرحلة P0 لكل طبقة لم تتغير بعد التقدم."""
        for layer_id in _P0_LAYER_IDS:
            spec = p0_registry.get(layer_id)
            assert spec.phase == "P0_BINARY_FOUNDATION"

    def test_CORE2_INVARIANT_10_p0_output_types_unchanged_after_advancement(
        self, p0_registry
    ):
        """CORE2-INVARIANT-10: أنواع مخرجات P0 لم تتغير بعد التقدم."""
        assert p0_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE).branch.output_type == "UnicodeCandidate"
        assert p0_registry.get(LAYER_ID_P0_TYPED_CODEPOINT).branch.output_type == "TypedCodePoint"
        assert p0_registry.get(LAYER_ID_P0_GLYPH_CLASSIFICATION).branch.output_type == "GlyphClassificationCandidate"
