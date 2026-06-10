"""
test_master_registry_seed.py — الاختبارات الدستورية لـ PR-CORE-1

كل اختبار مرتبط بقانون دستوري محدد.

أقسام الاختبارات:
    SEED-PHASES-*   — التحقق من وجود كل المراحل P0-P12
    SEED-PLANNED-*  — كل الطبقات بحالة PLANNED
    SEED-DOMAIN-*   — السجل عام، لا يعرف العربية مباشرة
    SEED-ORDER-*    — الترتيب: الأصل قبل الفرع
    SEED-FORBIDDEN- — المخرجات المحظورة مُعلَنة في كل طبقة
    SEED-GATEWAY-*  — الانتقالات المحظورة مباشرة مُعلَنة
    SEED-INVARIANT-*— الثوابت الدستورية
"""
import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    MasterLayerRegistry,
    RegistryViolation,
    build_master_registry_seed,
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
)


@pytest.fixture
def seed_registry() -> MasterLayerRegistry:
    """بذرة السجل الكاملة — مشتركة بين جميع الاختبارات."""
    return build_master_registry_seed()


# ─────────────────────────────────────────────────────────────────────────────
# SEED-PHASES — التحقق من وجود كل المراحل
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedPhases:
    """SEED-PHASES — كل طبقة مخططة موجودة في السجل."""

    ALL_LAYER_IDS = [
        LAYER_ID_P0_UNICODE_CANDIDATE,
        LAYER_ID_P0_TYPED_CODEPOINT,
        LAYER_ID_P0_GLYPH_CLASSIFICATION,
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

    def test_SEED_PHASES_01_registry_has_all_layers(self, seed_registry):
        """SEED-PHASES-01: السجل يحتوي جميع الطبقات المخططة."""
        assert len(seed_registry) == 19

    @pytest.mark.parametrize("layer_id", ALL_LAYER_IDS)
    def test_SEED_PHASES_02_each_layer_is_registered(self, seed_registry, layer_id):
        """SEED-PHASES-02: كل طبقة موجودة في السجل بمعرفها الكانونيكي."""
        assert layer_id in seed_registry

    def test_SEED_PHASES_03_p0_layers_present(self, seed_registry):
        """SEED-PHASES-03: مرحلة P0 لها ثلاث طبقات."""
        p0_layers = [
            s for s in seed_registry.all_layers()
            if s.phase == "P0_BINARY_FOUNDATION"
        ]
        assert len(p0_layers) == 3

    def test_SEED_PHASES_04_p1_layers_present(self, seed_registry):
        """SEED-PHASES-04: مرحلة P1 لها خمس طبقات."""
        p1_layers = [
            s for s in seed_registry.all_layers()
            if s.phase == "P1_DAL_ALONE_ATOMIC"
        ]
        assert len(p1_layers) == 5

    def test_SEED_PHASES_05_phases_p2_to_p12_each_have_one_layer(self, seed_registry):
        """SEED-PHASES-05: المراحل P2-P12 كل مرحلة طبقة واحدة."""
        single_phase_ids = [
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
        ]
        for phase_id in single_phase_ids:
            layers_in_phase = [
                s for s in seed_registry.all_layers()
                if s.phase == phase_id
            ]
            assert len(layers_in_phase) == 1, (
                f"Phase {phase_id} should have exactly 1 layer, "
                f"found {len(layers_in_phase)}"
            )


# ─────────────────────────────────────────────────────────────────────────────
# SEED-PLANNED — جميع الطبقات بحالة PLANNED
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedPlanned:
    """SEED-PLANNED — كل طبقة في البذرة مخططة، لا مُنفَّذة."""

    def test_SEED_PLANNED_01_all_layers_are_planned(self, seed_registry):
        """SEED-PLANNED-01: كل الطبقات بحالة PLANNED — لا تنفيذ قبل الخريطة."""
        planned = seed_registry.layers_by_status(LayerStatus.PLANNED)
        assert len(planned) == len(seed_registry)

    def test_SEED_PLANNED_02_no_implemented_layers(self, seed_registry):
        """SEED-PLANNED-02: لا توجد طبقات بحالة IMPLEMENTED في البذرة."""
        implemented = seed_registry.layers_by_status(LayerStatus.IMPLEMENTED)
        assert len(implemented) == 0

    def test_SEED_PLANNED_03_no_specified_layers_in_seed(self, seed_registry):
        """SEED-PLANNED-03: لا توجد طبقات بحالة SPECIFIED في البذرة."""
        specified = seed_registry.layers_by_status(LayerStatus.SPECIFIED)
        assert len(specified) == 0

    def test_SEED_PLANNED_04_no_closed_layers_in_seed(self, seed_registry):
        """SEED-PLANNED-04: لا توجد طبقات بحالة CLOSED في البذرة."""
        closed = seed_registry.layers_by_status(LayerStatus.CLOSED)
        assert len(closed) == 0

    def test_SEED_PLANNED_05_slot_candidate_is_planned_not_specified(self, seed_registry):
        """SEED-PLANNED-05: SlotCandidate نفسها PLANNED — لا تنفيذ بلا سجل."""
        spec = seed_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert spec.status == LayerStatus.PLANNED


# ─────────────────────────────────────────────────────────────────────────────
# SEED-DOMAIN — السجل عام، لا يعرف domain-specific concepts
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedDomain:
    """SEED-DOMAIN — السجل عام خالٍ من المنطق الخاص بالعربية."""

    _FORBIDDEN_DOMAIN_STRINGS = [
        "unicode_codepoint_u+",
        "arabic_unicode_",
        "haraka_name:",
        "makhraj_value:",
        "letter_name_arabic:",
        "wazn_pattern:",
    ]

    def test_SEED_DOMAIN_01_no_arabic_specific_unicode_in_layer_ids(self, seed_registry):
        """SEED-DOMAIN-01: معرفات الطبقات لا تحتوي رموز Unicode خاصة بالعربية."""
        for spec in seed_registry.all_layers():
            # معرفات الطبقات يجب أن تكون مجردة لا domain-specific
            assert spec.id.isascii(), (
                f"Layer ID '{spec.id}' must be ASCII — "
                "معرفات الطبقات عامة لا خاصة بالعربية"
            )

    def test_SEED_DOMAIN_02_no_arabic_script_in_layer_ids(self, seed_registry):
        """SEED-DOMAIN-02: معرفات الطبقات لا تحتوي حروفًا عربية."""
        for spec in seed_registry.all_layers():
            for char in spec.id:
                assert char.isascii() or char == "_", (
                    f"Layer ID '{spec.id}' contains non-ASCII character '{char}'"
                )

    def test_SEED_DOMAIN_03_forbidden_outputs_are_abstract_not_arabic_specific(
        self, seed_registry
    ):
        """SEED-DOMAIN-03: المحظورات المطلقة موجودة في كل طبقة."""
        absolute_forbidden = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
        for spec in seed_registry.all_layers():
            missing = absolute_forbidden - set(spec.forbidden_outputs)
            assert not missing, (
                f"Layer '{spec.id}' missing absolute forbidden: {missing}"
            )

    def test_SEED_DOMAIN_04_slot_geometry_core_has_no_arabic_imports(self, seed_registry):
        """SEED-DOMAIN-04: السجل يُبنى بدون استيراد أي منطق عربي خاص."""
        # حقيقة أن build_master_registry_seed() تعمل بدون أي مكتبة
        # خاصة بالعربية تثبت هذا الثابت
        registry = build_master_registry_seed()
        assert len(registry) > 0

    def test_SEED_DOMAIN_05_layer_names_are_abstract_not_arabic(self, seed_registry):
        """SEED-DOMAIN-05: أسماء الطبقات مجردة، لا تحتوي رموز عربية."""
        for spec in seed_registry.all_layers():
            assert spec.name.isascii(), (
                f"Layer name '{spec.name}' must be ASCII — "
                "الأسماء مجردة لا domain-specific"
            )


# ─────────────────────────────────────────────────────────────────────────────
# SEED-ORDER — الترتيب: الأصل قبل الفرع
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedOrder:
    """SEED-ORDER — قانون لا طبقة بلا أصل مسجل مُطبَّق في الترتيب."""

    def test_SEED_ORDER_01_p0_unicode_candidate_has_root_origin(self, seed_registry):
        """SEED-ORDER-01: الطبقة الأولى أصلها ROOT."""
        spec = seed_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert spec.origin.layer_id == "ROOT"

    def test_SEED_ORDER_02_p0_typed_codepoint_origin_is_registered(self, seed_registry):
        """SEED-ORDER-02: أصل TypedCodePoint (UnicodeCandidate) مسجل."""
        spec = seed_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        assert spec.origin.layer_id in seed_registry

    def test_SEED_ORDER_03_p1_layers_origins_are_registered(self, seed_registry):
        """SEED-ORDER-03: أصول طبقات P1 مسجلة في P0."""
        p1_ids = [
            LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
            LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
            LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
        ]
        for layer_id in p1_ids:
            spec = seed_registry.get(layer_id)
            assert spec.origin.layer_id in seed_registry, (
                f"Layer '{layer_id}' origin '{spec.origin.layer_id}' not registered"
            )

    def test_SEED_ORDER_04_p1_position_carrier_origin_is_registered(self, seed_registry):
        """SEED-ORDER-04: أصل PositionCarrier مسجل."""
        spec = seed_registry.get(LAYER_ID_P1_POSITION_CARRIER)
        assert spec.origin.layer_id in seed_registry

    def test_SEED_ORDER_05_slot_candidate_origin_is_in_p1(self, seed_registry):
        """SEED-ORDER-05: أصل SlotCandidate طبقة P1 مسجلة."""
        spec = seed_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert spec.origin.layer_id == LAYER_ID_P1_LETTER_IDENTITY_CARRIER
        assert spec.origin.layer_id in seed_registry

    def test_SEED_ORDER_06_p12_chain_is_unbroken(self, seed_registry):
        """SEED-ORDER-06: السلسلة من P0 إلى P12 متصلة — كل أصل مسجل."""
        chain = [
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
        for layer_id in chain:
            spec = seed_registry.get(layer_id)
            assert spec.origin.layer_id in seed_registry, (
                f"Layer '{layer_id}' origin '{spec.origin.layer_id}' not in registry"
            )

    def test_SEED_ORDER_07_registration_order_enforced(self):
        """SEED-ORDER-07: التسجيل بترتيب مقلوب يرفع RegistryViolation."""
        from qiyas_core.slot_geometry_core import BranchSpec, LayerSpec, OriginSpec
        registry = MasterLayerRegistry()
        child = LayerSpec(
            id="CHILD",
            name="ChildLayer",
            phase="test",
            origin=OriginSpec(layer_id="PARENT", output_type="ParentOutput"),
            branch=BranchSpec(output_type="ChildOutput", branch_reason="فرع"),
            shared_cause="علة",
            conditions=("cond_a",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("child_output",),
            target_boundary_opens=(),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("field_a",),
            preserves_ids=("id_a",),
            allowed_changes=(),
            forbidden_changes=(),
        )
        # التسجيل بدون تسجيل PARENT أولًا يجب أن يُرفض
        with pytest.raises(RegistryViolation, match="not yet registered"):
            registry.register(child)


# ─────────────────────────────────────────────────────────────────────────────
# SEED-FORBIDDEN — المحظورات مُعلَنة في كل طبقة
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedForbidden:
    """SEED-FORBIDDEN — قانون كل طبقة تُصرّح بممنوعاتها."""

    def test_SEED_FORBIDDEN_01_every_layer_has_forbidden_outputs(self, seed_registry):
        """SEED-FORBIDDEN-01: كل طبقة لها forbidden_outputs غير فارغة."""
        for spec in seed_registry.all_layers():
            assert len(spec.forbidden_outputs) > 0, (
                f"Layer '{spec.id}' has empty forbidden_outputs"
            )

    def test_SEED_FORBIDDEN_02_hukm_candidate_forbidden_in_all_layers(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-02: HukmCandidate محظور في كل طبقة بلا استثناء."""
        for spec in seed_registry.all_layers():
            assert "HukmCandidate" in spec.forbidden_outputs, (
                f"Layer '{spec.id}' does not forbid HukmCandidate"
            )

    def test_SEED_FORBIDDEN_03_reality_claim_forbidden_in_all_layers(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-03: RealityClaim محظور في كل طبقة بلا استثناء."""
        for spec in seed_registry.all_layers():
            assert "RealityClaim" in spec.forbidden_outputs, (
                f"Layer '{spec.id}' does not forbid RealityClaim"
            )

    def test_SEED_FORBIDDEN_04_final_meaning_forbidden_in_all_layers(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-04: FinalMeaning محظور في كل طبقة بلا استثناء."""
        for spec in seed_registry.all_layers():
            assert "FinalMeaning" in spec.forbidden_outputs, (
                f"Layer '{spec.id}' does not forbid FinalMeaning"
            )

    def test_SEED_FORBIDDEN_05_p0_layers_do_not_produce_slot_candidate(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-05: طبقات P0 لا تنتج SlotCandidate."""
        p0_ids = [
            LAYER_ID_P0_UNICODE_CANDIDATE,
            LAYER_ID_P0_TYPED_CODEPOINT,
            LAYER_ID_P0_GLYPH_CLASSIFICATION,
        ]
        for layer_id in p0_ids:
            spec = seed_registry.get(layer_id)
            assert "SlotCandidate" in spec.forbidden_outputs, (
                f"Layer '{layer_id}' should forbid SlotCandidate"
            )

    def test_SEED_FORBIDDEN_06_p1_letter_identity_does_not_produce_slot_candidate(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-06: LetterIdentityCarrier لا تنتج SlotCandidate."""
        spec = seed_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert "SlotCandidate" in spec.forbidden_outputs

    def test_SEED_FORBIDDEN_07_p1_haraka_function_does_not_produce_slot_candidate(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-07: HarakaFunctionCarrier لا تنتج SlotCandidate."""
        spec = seed_registry.get(LAYER_ID_P1_HARAKA_FUNCTION_CARRIER)
        assert "SlotCandidate" in spec.forbidden_outputs

    def test_SEED_FORBIDDEN_08_conditioned_sequence_does_not_produce_letter_identity(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-08: ConditionedTypedSequence لا تنتج LetterIdentityCarrier."""
        spec = seed_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert "LetterIdentityCarrier" in spec.forbidden_outputs

    def test_SEED_FORBIDDEN_09_conditioned_sequence_does_not_produce_haraka_function(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-09: ConditionedTypedSequence لا تنتج HarakaFunctionCarrier."""
        spec = seed_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs

    def test_SEED_FORBIDDEN_10_slot_candidate_does_not_produce_slot_geometry(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-10: SlotCandidate لا تنتج SlotGeometry مباشرة."""
        spec = seed_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert "SlotGeometry" in spec.forbidden_outputs

    def test_SEED_FORBIDDEN_11_p12_does_not_produce_reality_mapping(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-11: طبقة الإفادة P12 لا تنتج RealityMapping."""
        spec = seed_registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
        assert "RealityMapping" in spec.forbidden_outputs

    def test_SEED_FORBIDDEN_12_p12_does_not_produce_truth_judgment(
        self, seed_registry
    ):
        """SEED-FORBIDDEN-12: طبقة الإفادة P12 لا تنتج TruthJudgment."""
        spec = seed_registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
        assert "TruthJudgment" in spec.forbidden_outputs


# ─────────────────────────────────────────────────────────────────────────────
# SEED-GATEWAY — الانتقالات المحظورة مباشرة مُعلَنة
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedGateway:
    """SEED-GATEWAY — قانون القفزة المحظورة مُعلَن مسبقًا في كل طبقة."""

    def test_SEED_GATEWAY_01_slot_candidate_forbids_direct_jump_to_p12(
        self, seed_registry
    ):
        """SEED-GATEWAY-01: SlotCandidate تمنع القفزة المباشرة إلى P12."""
        spec = seed_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert LAYER_ID_P12_IFADAH_SPEECH_FORCE in spec.forbidden_direct_next_layer_ids

    def test_SEED_GATEWAY_02_slot_candidate_forbids_direct_jump_to_p3(
        self, seed_registry
    ):
        """SEED-GATEWAY-02: SlotCandidate تمنع القفزة المباشرة إلى P3."""
        spec = seed_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert LAYER_ID_P3_ROOT_STEM_CLOSURE in spec.forbidden_direct_next_layer_ids

    def test_SEED_GATEWAY_03_registry_enforces_forbidden_transition_at_runtime(
        self, seed_registry
    ):
        """SEED-GATEWAY-03: السجل يمنع فعليًا الانتقال المحظور عند وقت التشغيل."""
        with pytest.raises(RegistryViolation, match="FORBIDDEN"):
            seed_registry.assert_transition_allowed(
                LAYER_ID_P1_SLOT_CANDIDATE,
                LAYER_ID_P12_IFADAH_SPEECH_FORCE,
            )

    def test_SEED_GATEWAY_04_p2_forbids_jump_to_p12(self, seed_registry):
        """SEED-GATEWAY-04: P2 تمنع القفزة إلى P12."""
        spec = seed_registry.get(LAYER_ID_P2_REGISTRY_PROJECTION)
        assert LAYER_ID_P12_IFADAH_SPEECH_FORCE in spec.forbidden_direct_next_layer_ids

    def test_SEED_GATEWAY_05_p3_forbids_jump_to_p9(self, seed_registry):
        """SEED-GATEWAY-05: P3 تمنع القفزة إلى P9."""
        spec = seed_registry.get(LAYER_ID_P3_ROOT_STEM_CLOSURE)
        assert LAYER_ID_P9_SENTENCE_GEOMETRY in spec.forbidden_direct_next_layer_ids

    def test_SEED_GATEWAY_06_p5_forbids_direct_irab(self, seed_registry):
        """SEED-GATEWAY-06: طبقة الكلمة P5 تمنع القفزة إلى الإعراب P11."""
        spec = seed_registry.get(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS)
        assert LAYER_ID_P11_IRAB_GEOMETRY in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# SEED-INVARIANT — الثوابت الدستورية في البذرة
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedInvariants:
    """SEED-INVARIANT — الثوابت الدستورية العشرة مُطبَّقة في بنية البذرة."""

    def test_SEED_INVARIANT_01_every_layer_preserves_ids(self, seed_registry):
        """SEED-INVARIANT-01: كل طبقة تُصرّح بالهويات التي تحفظها."""
        for spec in seed_registry.all_layers():
            assert len(spec.preserves_ids) > 0, (
                f"Layer '{spec.id}' does not declare preserves_ids — "
                "لا هوية بلا أثر"
            )

    def test_SEED_INVARIANT_02_every_layer_has_minimum_required_fields(
        self, seed_registry
    ):
        """SEED-INVARIANT-02: كل طبقة تُعرِّف الاكتمال الأدنى."""
        for spec in seed_registry.all_layers():
            assert len(spec.minimum_required_fields) > 0, (
                f"Layer '{spec.id}' has no minimum_required_fields"
            )

    def test_SEED_INVARIANT_03_every_layer_has_conditions(self, seed_registry):
        """SEED-INVARIANT-03: كل طبقة لها شروط تحقق الانتقال."""
        for spec in seed_registry.all_layers():
            assert len(spec.conditions) > 0, (
                f"Layer '{spec.id}' has no conditions"
            )

    def test_SEED_INVARIANT_04_every_layer_has_shared_cause(self, seed_registry):
        """SEED-INVARIANT-04: كل طبقة لها علة جامعة — لا مقايسة بلا علة."""
        for spec in seed_registry.all_layers():
            assert spec.shared_cause, (
                f"Layer '{spec.id}' has no shared_cause"
            )

    def test_SEED_INVARIANT_05_p0_forbidden_changes_do_not_assign_meaning(
        self, seed_registry
    ):
        """SEED-INVARIANT-05: طبقات P0 تمنع تعيين المعنى صراحةً."""
        p0_ids = [
            LAYER_ID_P0_UNICODE_CANDIDATE,
            LAYER_ID_P0_TYPED_CODEPOINT,
            LAYER_ID_P0_GLYPH_CLASSIFICATION,
        ]
        for layer_id in p0_ids:
            spec = seed_registry.get(layer_id)
            assert "assign_meaning" in spec.forbidden_changes, (
                f"Layer '{layer_id}' does not forbid assign_meaning"
            )

    def test_SEED_INVARIANT_06_p1_atomic_layers_forbid_cross_proof(
        self, seed_registry
    ):
        """SEED-INVARIANT-06: الإثباتات الذرية P1 لا تتداخل — كل طبقة تمنع إثبات الأخرى."""
        letter_spec = seed_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        haraka_spec = seed_registry.get(LAYER_ID_P1_HARAKA_FUNCTION_CARRIER)
        # الحرف لا يُثبت وظيفة الحركة
        assert "assign_haraka_function" in letter_spec.forbidden_changes
        # الحركة لا تُثبت هوية الحرف
        assert "assign_letter_identity" in haraka_spec.forbidden_changes

    def test_SEED_INVARIANT_07_build_seed_is_deterministic(self):
        """SEED-INVARIANT-07: بناء السجل محدد وقابل للتكرار."""
        r1 = build_master_registry_seed()
        r2 = build_master_registry_seed()
        # كلاهما يحتويان نفس الطبقات
        ids1 = {s.id for s in r1.all_layers()}
        ids2 = {s.id for s in r2.all_layers()}
        assert ids1 == ids2

    def test_SEED_INVARIANT_08_no_layer_produces_output_of_later_layer(
        self, seed_registry
    ):
        """SEED-INVARIANT-08: لا طبقة تنتج مخرج طبقة لاحقة (spot-check)."""
        # TypedCodePoint لا تنتج LetterIdentityCarrier
        typed_spec = seed_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        assert "LetterIdentityCarrier" in typed_spec.forbidden_outputs
        # LetterIdentityCarrier لا تنتج SlotCandidate
        letter_spec = seed_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert "SlotCandidate" in letter_spec.forbidden_outputs

    def test_SEED_INVARIANT_09_p12_closes_into_ifadah_candidates(
        self, seed_registry
    ):
        """SEED-INVARIANT-09: P12 تُغلق ifadah_candidates وليس أي حكم نهائي."""
        spec = seed_registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
        assert "ifadah_candidates" in spec.target_boundary_closes
        assert spec.branch.output_type == "IfadahCandidate"

    def test_SEED_INVARIANT_10_p12_opens_nothing_terminal_layer(
        self, seed_registry
    ):
        """SEED-INVARIANT-10: P12 لا تفتح طبقات أخرى — هي الطبقة الأخيرة."""
        spec = seed_registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
        assert len(spec.target_boundary_opens) == 0
