"""
test_master_registry_p1_specified.py — الاختبارات الدستورية لـ PR-CORE-3

PR-CORE-3: تعريف مواصفات P1 فقط — لا runtime، لا تنفيذ.

الانتقال: PLANNED → SPECIFIED فقط.
الطبقات المُحدَّدة: P1_LETTER_IDENTITY_CARRIER، P1_HARAKA_MARK_IDENTITY_CARRIER،
                    P1_CONDITIONED_TYPED_SEQUENCE، P1_POSITION_CARRIER، P1_SLOT_CANDIDATE
الطبقات المتبقية: P2-P12 تبقى PLANNED

أقسام الاختبارات:
    CORE3-STATUS-*     — التحقق من حالة P1 بعد التقدم إلى SPECIFIED
    CORE3-SEED-*       — البذرة الأصلية لم تتأثر (كل طبقاتها PLANNED)
    CORE3-P0-*         — P0 تبقى IMPLEMENTED (لم تتراجع)
    CORE3-P2PLUS-*     — P2-P12 تبقى PLANNED
    CORE3-TRANSITION-* — الانتقال صحيح (PLANNED→SPECIFIED فقط، لا PLANNED→IMPLEMENTED)
    CORE3-INVARIANT-*  — الثوابت الدستورية محفوظة بعد التقدم
    CORE3-NONGOAL-*    — التحقق من حدود PR (لا runtime، لا P2+، لا معنى نهائي)
    CORE3-PARALLEL-*   — البنية الموازية لـ P1 محفوظة (LetterIdentity و HarakaMarkIdentity مستقلتان)
"""
import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    MasterLayerRegistry,
    RegistryViolation,
    build_master_registry_seed,
    build_p0_implemented_registry,
    build_p1_specified_registry,
)
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P0_GLYPH_CLASSIFICATION,
    LAYER_ID_P0_TYPED_CODEPOINT,
    LAYER_ID_P0_UNICODE_CANDIDATE,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
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
    _P0_LAYER_IDS,
    _P1_LAYER_IDS,
)


@pytest.fixture
def p1_registry() -> MasterLayerRegistry:
    """سجل مع P0 بحالة IMPLEMENTED وP1 بحالة SPECIFIED — مشترك."""
    return build_p1_specified_registry()


@pytest.fixture
def seed_registry() -> MasterLayerRegistry:
    """البذرة الأصلية — كل الطبقات PLANNED."""
    return build_master_registry_seed()


@pytest.fixture
def p0_registry() -> MasterLayerRegistry:
    """سجل P0 فقط بحالة IMPLEMENTED — للتحقق من التراكم الصحيح."""
    return build_p0_implemented_registry()


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-STATUS — حالة طبقات P1 بعد التقدم إلى SPECIFIED
# ─────────────────────────────────────────────────────────────────────────────

class TestP1Status:
    """CORE3-STATUS — طبقات P1 وصلت إلى حالة SPECIFIED."""

    def test_CORE3_STATUS_01_p1_letter_identity_carrier_is_specified(self, p1_registry):
        """CORE3-STATUS-01: P1_LETTER_IDENTITY_CARRIER وصلت إلى SPECIFIED."""
        spec = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert spec.status == LayerStatus.SPECIFIED

    def test_CORE3_STATUS_02_p1_haraka_mark_identity_carrier_is_specified(self, p1_registry):
        """CORE3-STATUS-02: P1_HARAKA_MARK_IDENTITY_CARRIER وصلت إلى SPECIFIED."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert spec.status == LayerStatus.SPECIFIED

    def test_CORE3_STATUS_03_p1_conditioned_typed_sequence_is_specified(self, p1_registry):
        """CORE3-STATUS-03: P1_CONDITIONED_TYPED_SEQUENCE وصلت إلى SPECIFIED."""
        spec = p1_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert spec.status == LayerStatus.SPECIFIED

    def test_CORE3_STATUS_04_p1_position_carrier_is_specified(self, p1_registry):
        """CORE3-STATUS-04: P1_POSITION_CARRIER وصلت إلى SPECIFIED."""
        spec = p1_registry.get(LAYER_ID_P1_POSITION_CARRIER)
        assert spec.status == LayerStatus.SPECIFIED

    def test_CORE3_STATUS_05_p1_slot_candidate_is_specified(self, p1_registry):
        """CORE3-STATUS-05: P1_SLOT_CANDIDATE وصلت إلى SPECIFIED."""
        spec = p1_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert spec.status == LayerStatus.SPECIFIED

    def test_CORE3_STATUS_06_exactly_five_specified_layers(self, p1_registry):
        """CORE3-STATUS-06: خمس طبقات فقط بحالة SPECIFIED — لا أكثر."""
        specified = p1_registry.layers_by_status(LayerStatus.SPECIFIED)
        assert len(specified) == 5

    def test_CORE3_STATUS_07_all_p1_layers_are_specified(self, p1_registry):
        """CORE3-STATUS-07: جميع طبقات P1 الخمس بحالة SPECIFIED."""
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert spec.status == LayerStatus.SPECIFIED, (
                f"Layer {layer_id} should be SPECIFIED, got {spec.status}"
            )

    def test_CORE3_STATUS_08_specified_layer_ids_are_p1_only(self, p1_registry):
        """CORE3-STATUS-08: الطبقات بحالة SPECIFIED هي P1 فقط — لا غيرها."""
        specified = p1_registry.layers_by_status(LayerStatus.SPECIFIED)
        specified_ids = {s.id for s in specified}
        expected_ids = set(_P1_LAYER_IDS)
        assert specified_ids == expected_ids

    def test_CORE3_STATUS_09_total_layer_count_unchanged(self, p1_registry):
        """CORE3-STATUS-09: عدد الطبقات الإجمالي لم يتغير — 19 طبقة."""
        assert len(p1_registry) == 19

    def test_CORE3_STATUS_10_no_p1_layer_is_implemented(self, p1_registry):
        """CORE3-STATUS-10: لا توجد طبقة P1 بحالة IMPLEMENTED — SPECIFIED فقط."""
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert spec.status != LayerStatus.IMPLEMENTED, (
                f"Layer {layer_id} must NOT be IMPLEMENTED — SPECIFIED only in PR-CORE-3"
            )


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-SEED — البذرة الأصلية لم تتأثر
# ─────────────────────────────────────────────────────────────────────────────

class TestSeedUnaffected:
    """CORE3-SEED — build_master_registry_seed() لا تزال ترجع كل الطبقات PLANNED."""

    def test_CORE3_SEED_01_seed_all_planned(self, seed_registry):
        """CORE3-SEED-01: البذرة الأصلية — كل 19 طبقة PLANNED."""
        planned = seed_registry.layers_by_status(LayerStatus.PLANNED)
        assert len(planned) == 19

    def test_CORE3_SEED_02_seed_p1_layers_are_planned(self, seed_registry):
        """CORE3-SEED-02: طبقات P1 في البذرة PLANNED — لم تُقدِّمها build_p1_specified."""
        for layer_id in _P1_LAYER_IDS:
            spec = seed_registry.get(layer_id)
            assert spec.status == LayerStatus.PLANNED

    def test_CORE3_SEED_03_seed_no_specified_layers(self, seed_registry):
        """CORE3-SEED-03: البذرة لا تحتوي أي طبقة SPECIFIED."""
        specified = seed_registry.layers_by_status(LayerStatus.SPECIFIED)
        assert len(specified) == 0

    def test_CORE3_SEED_04_seed_no_implemented_layers(self, seed_registry):
        """CORE3-SEED-04: البذرة لا تحتوي أي طبقة IMPLEMENTED."""
        implemented = seed_registry.layers_by_status(LayerStatus.IMPLEMENTED)
        assert len(implemented) == 0

    def test_CORE3_SEED_05_registries_are_independent(self, seed_registry, p1_registry):
        """CORE3-SEED-05: السجلات مستقلة — تقدم P1 لا يُغيّر البذرة."""
        # بعد بناء p1_registry، البذرة لا تزال كما هي
        seed_p1_status = seed_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER).status
        assert seed_p1_status == LayerStatus.PLANNED


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-P0 — P0 تبقى IMPLEMENTED بعد تقدم P1
# ─────────────────────────────────────────────────────────────────────────────

class TestP0Preserved:
    """CORE3-P0 — طبقات P0 تبقى IMPLEMENTED بعد بناء p1_registry."""

    def test_CORE3_P0_01_p0_unicode_candidate_still_implemented(self, p1_registry):
        """CORE3-P0-01: P0_UNICODE_CANDIDATE تبقى IMPLEMENTED بعد تقدم P1."""
        spec = p1_registry.get(LAYER_ID_P0_UNICODE_CANDIDATE)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE3_P0_02_p0_typed_codepoint_still_implemented(self, p1_registry):
        """CORE3-P0-02: P0_TYPED_CODEPOINT تبقى IMPLEMENTED بعد تقدم P1."""
        spec = p1_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE3_P0_03_p0_glyph_classification_still_implemented(self, p1_registry):
        """CORE3-P0-03: P0_GLYPH_CLASSIFICATION تبقى IMPLEMENTED بعد تقدم P1."""
        spec = p1_registry.get(LAYER_ID_P0_GLYPH_CLASSIFICATION)
        assert spec.status == LayerStatus.IMPLEMENTED

    def test_CORE3_P0_04_exactly_three_implemented_layers(self, p1_registry):
        """CORE3-P0-04: ثلاث طبقات فقط بحالة IMPLEMENTED — P0 فقط."""
        implemented = p1_registry.layers_by_status(LayerStatus.IMPLEMENTED)
        assert len(implemented) == 3

    def test_CORE3_P0_05_implemented_layers_are_p0_only(self, p1_registry):
        """CORE3-P0-05: الطبقات بحالة IMPLEMENTED هي P0 فقط — P1 لا تُنفَّذ."""
        implemented = p1_registry.layers_by_status(LayerStatus.IMPLEMENTED)
        implemented_ids = {s.id for s in implemented}
        expected_ids = set(_P0_LAYER_IDS)
        assert implemented_ids == expected_ids


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-P2PLUS — P2-P12 تبقى PLANNED
# ─────────────────────────────────────────────────────────────────────────────

_P2_PLUS_LAYER_IDS = [
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


class TestP2PlusPlanned:
    """CORE3-P2PLUS — P2-P12 تبقى PLANNED بعد تقدم P1."""

    @pytest.mark.parametrize("layer_id", _P2_PLUS_LAYER_IDS)
    def test_CORE3_P2PLUS_01_p2_plus_remain_planned(self, p1_registry, layer_id):
        """CORE3-P2PLUS-01: طبقات P2-P12 تبقى PLANNED — لم تتقدم."""
        spec = p1_registry.get(layer_id)
        assert spec.status == LayerStatus.PLANNED, (
            f"Layer {layer_id} should remain PLANNED, got {spec.status}"
        )

    def test_CORE3_P2PLUS_02_exactly_eleven_planned_layers(self, p1_registry):
        """CORE3-P2PLUS-02: أحد عشر طبقة فقط بحالة PLANNED (P2-P12)."""
        planned = p1_registry.layers_by_status(LayerStatus.PLANNED)
        assert len(planned) == 11

    def test_CORE3_P2PLUS_03_p12_ifadah_not_specified(self, p1_registry):
        """CORE3-P2PLUS-03: P12_IFADAH_SPEECH_FORCE تبقى PLANNED — لا قفزة بلا أصل."""
        spec = p1_registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
        assert spec.status == LayerStatus.PLANNED


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-TRANSITION — الانتقالات الصحيحة
# ─────────────────────────────────────────────────────────────────────────────

class TestTransitions:
    """CORE3-TRANSITION — الانتقالات الصحيحة محفوظة والانتقالات المحظورة مرفوضة."""

    def test_CORE3_TRANSITION_01_planned_to_specified_allowed(self):
        """CORE3-TRANSITION-01: الانتقال PLANNED→SPECIFIED مسموح دون رفع استثناء."""
        registry = build_master_registry_seed()
        # يجب أن ينجح بدون استثناء
        registry.update_status(
            LAYER_ID_P1_LETTER_IDENTITY_CARRIER, LayerStatus.SPECIFIED
        )
        spec = registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert spec.status == LayerStatus.SPECIFIED

    def test_CORE3_TRANSITION_02_direct_planned_to_implemented_raises(self):
        """CORE3-TRANSITION-02: القفز المباشر PLANNED→IMPLEMENTED يرفع RegistryViolation."""
        registry = build_master_registry_seed()
        with pytest.raises(RegistryViolation):
            registry.update_status(
                LAYER_ID_P1_LETTER_IDENTITY_CARRIER, LayerStatus.IMPLEMENTED
            )

    def test_CORE3_TRANSITION_03_build_p1_specified_does_not_implement(self):
        """CORE3-TRANSITION-03: build_p1_specified_registry لا تُنتج IMPLEMENTED لـ P1."""
        registry = build_p1_specified_registry()
        for layer_id in _P1_LAYER_IDS:
            spec = registry.get(layer_id)
            assert spec.status == LayerStatus.SPECIFIED
            assert spec.status != LayerStatus.IMPLEMENTED

    def test_CORE3_TRANSITION_04_specified_does_not_regress_to_planned_via_build(self):
        """CORE3-TRANSITION-04: build_p1_specified_registry لا تُراجع P1 إلى PLANNED — جميع P1 SPECIFIED."""
        registry = build_p1_specified_registry()
        # التحقق أن الدالة لا تترك أي P1 بحالة PLANNED
        for layer_id in _P1_LAYER_IDS:
            spec = registry.get(layer_id)
            assert spec.status != LayerStatus.PLANNED, (
                f"Layer {layer_id} should not be PLANNED after build_p1_specified_registry"
            )

    def test_CORE3_TRANSITION_05_p2_direct_to_specified_from_planned_raises(self):
        """CORE3-TRANSITION-05: محاولة تقديم P2 لا تتم عبر build_p1_specified — P2 يبقى PLANNED."""
        registry = build_p1_specified_registry()
        # التحقق المباشر: محاولة تقديم P2 مباشرة إلى IMPLEMENTED ترفع استثناء
        with pytest.raises(RegistryViolation):
            registry.update_status(
                LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED
            )


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-INVARIANT — الثوابت الدستورية محفوظة بعد التقدم
# ─────────────────────────────────────────────────────────────────────────────

class TestInvariantsPreserved:
    """CORE3-INVARIANT — forbidden_outputs وforbidden_changes محفوظة بعد SPECIFIED."""

    def test_CORE3_INVARIANT_01_p1_letter_identity_forbidden_outputs_preserved(
        self, p1_registry
    ):
        """CORE3-INVARIANT-01: forbidden_outputs لـ LetterIdentityCarrier محفوظة."""
        spec = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        # الممنوعات المطلقة
        assert "HukmCandidate" in spec.forbidden_outputs
        assert "RealityClaim" in spec.forbidden_outputs
        assert "FinalMeaning" in spec.forbidden_outputs
        # ممنوعات خاصة بـ LetterIdentityCarrier
        assert "SlotCandidate" in spec.forbidden_outputs
        assert "SlotGeometry" in spec.forbidden_outputs
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs

    def test_CORE3_INVARIANT_02_p1_haraka_mark_identity_forbidden_outputs_preserved(
        self, p1_registry
    ):
        """CORE3-INVARIANT-02: forbidden_outputs لـ HarakaMarkIdentityCarrier محفوظة."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "HukmCandidate" in spec.forbidden_outputs
        assert "RealityClaim" in spec.forbidden_outputs
        assert "FinalMeaning" in spec.forbidden_outputs
        assert "SlotCandidate" in spec.forbidden_outputs
        assert "SlotGeometry" in spec.forbidden_outputs
        assert "LetterIdentityCarrier" in spec.forbidden_outputs
        # لا يجوز إنتاج وظيفة نحوية — هذا حد هوية السطح فقط
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs

    def test_CORE3_INVARIANT_03_p1_conditioned_typed_sequence_forbidden_outputs(
        self, p1_registry
    ):
        """CORE3-INVARIANT-03: ConditionedTypedSequence لا تنتج LetterIdentity أو HarakaMarkIdentity."""
        spec = p1_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert "LetterIdentityCarrier" in spec.forbidden_outputs
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs
        assert "SlotCandidate" in spec.forbidden_outputs
        assert "SlotGeometry" in spec.forbidden_outputs

    def test_CORE3_INVARIANT_04_p1_slot_candidate_forbidden_outputs_preserved(
        self, p1_registry
    ):
        """CORE3-INVARIANT-04: SlotCandidate لا تنتج SlotGeometry أو ConditionedTypedSequence."""
        spec = p1_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert "SlotGeometry" in spec.forbidden_outputs
        assert "HukmCandidate" in spec.forbidden_outputs
        assert "RealityClaim" in spec.forbidden_outputs
        assert "FinalMeaning" in spec.forbidden_outputs

    def test_CORE3_INVARIANT_05_all_p1_layers_have_absolute_forbidden(self, p1_registry):
        """CORE3-INVARIANT-05: جميع طبقات P1 تحتوي الممنوعات المطلقة الثلاثة."""
        absolute_forbidden = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            missing = absolute_forbidden - set(spec.forbidden_outputs)
            assert not missing, (
                f"Layer '{layer_id}' missing absolute forbidden after SPECIFIED: {missing}"
            )

    def test_CORE3_INVARIANT_06_p1_letter_identity_minimum_required_fields(
        self, p1_registry
    ):
        """CORE3-INVARIANT-06: minimum_required_fields لـ LetterIdentityCarrier محفوظة."""
        spec = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert "unicode_identity" in spec.minimum_required_fields
        assert "arabic_script_identity" in spec.minimum_required_fields
        assert "letter_class" in spec.minimum_required_fields
        assert "letter_name" in spec.minimum_required_fields

    def test_CORE3_INVARIANT_07_p1_haraka_mark_identity_minimum_required_fields(self, p1_registry):
        """CORE3-INVARIANT-07: minimum_required_fields لـ HarakaMarkIdentityCarrier محفوظة — بلا functional_role."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "unicode_identity" in spec.minimum_required_fields
        assert "arabic_mark_identity" in spec.minimum_required_fields
        assert "haraka_class" in spec.minimum_required_fields
        # functional_role ممنوع — هذا حد هوية السطح لا الوظيفة النحوية
        assert "functional_role" not in spec.minimum_required_fields

    def test_CORE3_INVARIANT_08_slot_candidate_minimum_required_fields(self, p1_registry):
        """CORE3-INVARIANT-08: minimum_required_fields لـ SlotCandidate محفوظة — أربعة مكونات."""
        spec = p1_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        assert "letter_identity_ref" in spec.minimum_required_fields
        assert "haraka_mark_identity_ref" in spec.minimum_required_fields
        assert "position_ref" in spec.minimum_required_fields
        assert "alignment_evidence_ref" in spec.minimum_required_fields

    def test_CORE3_INVARIANT_09_p1_origins_unchanged(self, p1_registry):
        """CORE3-INVARIANT-09: أصول P1 لم تتغير بعد التقدم."""
        # LetterIdentityCarrier و HarakaMarkIdentityCarrier أصلهما TypedCodePoint
        lic = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        hmic = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        cts = p1_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert lic.origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT
        assert hmic.origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT
        assert cts.origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT

    def test_CORE3_INVARIANT_10_p1_phases_unchanged(self, p1_registry):
        """CORE3-INVARIANT-10: مرحلة P1_DAL_ALONE_ATOMIC لم تتغير بعد التقدم."""
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert spec.phase == "P1_DAL_ALONE_ATOMIC", (
                f"Layer {layer_id} phase changed after SPECIFIED advancement"
            )


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-NONGOAL — حدود PR محفوظة
# ─────────────────────────────────────────────────────────────────────────────

class TestNonGoals:
    """CORE3-NONGOAL — PR-CORE-3 لا يُنفِّذ runtime، لا يُقدِّم P2+، لا ينتج معنى."""

    def test_CORE3_NONGOAL_01_no_p1_layer_produces_letter_identity_as_output(
        self, p1_registry
    ):
        """CORE3-NONGOAL-01: ConditionedTypedSequence لا تُنتج LetterIdentityCarrier."""
        spec = p1_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert "LetterIdentityCarrier" in spec.forbidden_outputs

    def test_CORE3_NONGOAL_02_no_p1_layer_produces_haraka_function_as_output(
        self, p1_registry
    ):
        """CORE3-NONGOAL-02: ConditionedTypedSequence لا تُنتج HarakaFunctionCarrier."""
        spec = p1_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs

    def test_CORE3_NONGOAL_03_no_p1_layer_produces_slot_geometry(self, p1_registry):
        """CORE3-NONGOAL-03: لا توجد طبقة P1 تُنتج SlotGeometry مباشرة."""
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert "SlotGeometry" in spec.forbidden_outputs, (
                f"Layer {layer_id} must forbid SlotGeometry"
            )

    def test_CORE3_NONGOAL_04_p2_plus_not_specified(self, p1_registry):
        """CORE3-NONGOAL-04: P2-P12 لا تُقدَّم بواسطة build_p1_specified_registry."""
        for layer_id in _P2_PLUS_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert spec.status == LayerStatus.PLANNED, (
                f"Layer {layer_id} must not advance in PR-CORE-3"
            )

    def test_CORE3_NONGOAL_05_no_final_meaning_allowed_in_any_p1_layer(self, p1_registry):
        """CORE3-NONGOAL-05: لا توجد طبقة P1 تُنتج FinalMeaning."""
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert "FinalMeaning" in spec.forbidden_outputs

    def test_CORE3_NONGOAL_06_no_hukm_candidate_in_any_p1_layer(self, p1_registry):
        """CORE3-NONGOAL-06: لا توجد طبقة P1 تُنتج HukmCandidate."""
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert "HukmCandidate" in spec.forbidden_outputs

    def test_CORE3_NONGOAL_07_p1_output_types_are_candidates_not_final(self, p1_registry):
        """CORE3-NONGOAL-07: مخرجات P1 هي مرشحات (Carrier/Candidate/Sequence) لا أحكام."""
        candidate_output_types = {
            "LetterIdentityCarrier",
            "HarakaMarkIdentityCarrier",
            "ConditionedTypedSequence",
            "PositionCarrier",
            "SlotCandidate",
        }
        for layer_id in _P1_LAYER_IDS:
            spec = p1_registry.get(layer_id)
            assert spec.branch.output_type in candidate_output_types, (
                f"Layer {layer_id} output_type '{spec.branch.output_type}' "
                "is not a candidate type"
            )


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-PARALLEL — البنية الموازية لـ P1 محفوظة
# ─────────────────────────────────────────────────────────────────────────────

class TestParallelArchitecture:
    """CORE3-PARALLEL — LetterIdentityCarrier وHarakaMarkIdentityCarrier مستقلتان متوازيتان."""

    def test_CORE3_PARALLEL_01_letter_identity_independent_of_conditioned_sequence(
        self, p1_registry
    ):
        """CORE3-PARALLEL-01: LetterIdentityCarrier أصلها TypedCodePoint — لا تعتمد على ConditionedTypedSequence."""
        spec = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert spec.origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT
        assert spec.origin.layer_id != LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE

    def test_CORE3_PARALLEL_02_haraka_mark_identity_independent_of_conditioned_sequence(
        self, p1_registry
    ):
        """CORE3-PARALLEL-02: HarakaMarkIdentityCarrier أصلها TypedCodePoint — لا تعتمد على ConditionedTypedSequence."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert spec.origin.layer_id == LAYER_ID_P0_TYPED_CODEPOINT
        assert spec.origin.layer_id != LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE

    def test_CORE3_PARALLEL_03_letter_identity_does_not_require_haraka_mark_identity(
        self, p1_registry
    ):
        """CORE3-PARALLEL-03: LetterIdentityCarrier تحظر إنتاج HarakaFunctionCarrier — مستقلتان."""
        spec = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs

    def test_CORE3_PARALLEL_04_haraka_mark_identity_does_not_require_letter_identity(
        self, p1_registry
    ):
        """CORE3-PARALLEL-04: HarakaMarkIdentityCarrier تحظر إنتاج LetterIdentityCarrier — مستقلتان."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "LetterIdentityCarrier" in spec.forbidden_outputs

    def test_CORE3_PARALLEL_05_slot_candidate_requires_four_ingredients(self, p1_registry):
        """CORE3-PARALLEL-05: SlotCandidate تشترط أربعة مكونات — تجمع المسارات الموازية."""
        spec = p1_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        # الشروط الأربعة يجب أن تكون موثقة في conditions
        conditions = set(spec.conditions)
        assert "letter_identity_carrier_present" in conditions
        assert "haraka_mark_identity_carrier_present" in conditions
        assert "position_carrier_present" in conditions
        assert "alignment_evidence_present" in conditions

    def test_CORE3_PARALLEL_06_slot_candidate_allowed_previous_layers_include_all_four(
        self, p1_registry
    ):
        """CORE3-PARALLEL-06: SlotCandidate تُعلن كل P1 الأربعة كأصول مسموحة."""
        spec = p1_registry.get(LAYER_ID_P1_SLOT_CANDIDATE)
        allowed = set(spec.allowed_previous_layer_ids)
        assert LAYER_ID_P1_LETTER_IDENTITY_CARRIER in allowed
        assert LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER in allowed
        assert LAYER_ID_P1_POSITION_CARRIER in allowed
        assert LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE in allowed

    def test_CORE3_PARALLEL_07_conditioned_typed_sequence_forbids_slot_candidate(
        self, p1_registry
    ):
        """CORE3-PARALLEL-07: ConditionedTypedSequence تحظر إنتاج SlotCandidate مباشرة."""
        spec = p1_registry.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
        assert "SlotCandidate" in spec.forbidden_outputs

    def test_CORE3_PARALLEL_08_letter_identity_forbids_slot_candidate(self, p1_registry):
        """CORE3-PARALLEL-08: LetterIdentityCarrier وحدها لا تُنتج SlotCandidate."""
        spec = p1_registry.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER)
        assert "SlotCandidate" in spec.forbidden_outputs

    def test_CORE3_PARALLEL_09_haraka_mark_identity_forbids_slot_candidate(self, p1_registry):
        """CORE3-PARALLEL-09: HarakaMarkIdentityCarrier وحدها لا تُنتج SlotCandidate."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "SlotCandidate" in spec.forbidden_outputs


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-BOUNDARY — حدود هوية علامة الحركة السطحية
# ─────────────────────────────────────────────────────────────────────────────

class TestHarakaMarkIdentityBoundary:
    """CORE3-BOUNDARY — HarakaMarkIdentityCarrier حد هوية السطح فقط — لا وظيفة نحوية."""

    def test_CORE3_BOUNDARY_01_haraka_mark_identity_closes_mark_identity_carriers(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-01: HarakaMarkIdentityCarrier تُغلق haraka_mark_identity_carriers."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "haraka_mark_identity_carriers" in spec.target_boundary_closes

    def test_CORE3_BOUNDARY_02_haraka_mark_identity_does_not_close_haraka_function_carriers(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-02: HarakaMarkIdentityCarrier لا تُغلق haraka_function_carriers — حد السطح لا الوظيفة."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "haraka_function_carriers" not in spec.target_boundary_closes

    def test_CORE3_BOUNDARY_03_haraka_mark_identity_forbids_haraka_function_carrier_output(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-03: HarakaMarkIdentityCarrier لا تُنتج HarakaFunctionCarrier — وظيفة نحوية تحتاج gate لاحق."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "HarakaFunctionCarrier" in spec.forbidden_outputs

    def test_CORE3_BOUNDARY_04_haraka_mark_identity_forbids_assign_haraka_function(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-04: HarakaMarkIdentityCarrier تحظر assign_haraka_function — لا وظيفة في هذه المرحلة."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "assign_haraka_function" in spec.forbidden_changes

    def test_CORE3_BOUNDARY_05_haraka_mark_identity_allowed_change_is_prove_mark_identity(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-05: HarakaMarkIdentityCarrier تُجيز prove_haraka_mark_identity فقط."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert "prove_haraka_mark_identity" in spec.allowed_changes

    def test_CORE3_BOUNDARY_06_p0_typed_codepoint_opens_mark_identity_not_function_carriers(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-06: P0_TYPED_CODEPOINT يفتح haraka_mark_identity_carriers لا haraka_function_carriers."""
        spec = p1_registry.get(LAYER_ID_P0_TYPED_CODEPOINT)
        assert "haraka_mark_identity_carriers" in spec.target_boundary_opens
        assert "haraka_function_carriers" not in spec.target_boundary_opens

    def test_CORE3_BOUNDARY_07_haraka_mark_identity_output_type_is_mark_carrier(
        self, p1_registry
    ):
        """CORE3-BOUNDARY-07: مخرج HarakaMarkIdentityCarrier هو HarakaMarkIdentityCarrier لا HarakaFunctionCarrier."""
        spec = p1_registry.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
        assert spec.branch.output_type == "HarakaMarkIdentityCarrier"
        assert spec.branch.output_type != "HarakaFunctionCarrier"


# ─────────────────────────────────────────────────────────────────────────────
# CORE3-LINEAGE — إنفاذ lineage في assert_transition_allowed
# ─────────────────────────────────────────────────────────────────────────────

class TestLineageEnforcement:
    """CORE3-LINEAGE — assert_transition_allowed يُنفِّذ قانون الأصل والفرع."""

    def test_CORE3_LINEAGE_01_valid_transition_along_origin_allowed(self):
        """CORE3-LINEAGE-01: الانتقال على طول origin line مسموح."""
        registry = build_master_registry_seed()
        # P0_UNICODE_CANDIDATE → P0_TYPED_CODEPOINT: أصل TypedCodePoint هو UnicodeCandiate
        registry.assert_transition_allowed(
            LAYER_ID_P0_UNICODE_CANDIDATE,
            LAYER_ID_P0_TYPED_CODEPOINT,
        )

    def test_CORE3_LINEAGE_02_transition_violating_origin_raises(self):
        """CORE3-LINEAGE-02: الانتقال الذي يخالف origin يرفع RegistryViolation."""
        from qiyas_core.slot_geometry_core import RegistryViolation
        registry = build_master_registry_seed()
        # P0_UNICODE_CANDIDATE → P1_LETTER_IDENTITY_CARRIER: أصل P1 هو TypedCodePoint لا UnicodeCandiate
        with pytest.raises(RegistryViolation):
            registry.assert_transition_allowed(
                LAYER_ID_P0_UNICODE_CANDIDATE,
                LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
            )

    def test_CORE3_LINEAGE_03_transition_violating_origin_for_haraka_mark_identity_raises(self):
        """CORE3-LINEAGE-03: الانتقال من UnicodeCandiate مباشرة إلى HarakaMarkIdentityCarrier يرفع استثناء."""
        from qiyas_core.slot_geometry_core import RegistryViolation
        registry = build_master_registry_seed()
        # P0_UNICODE_CANDIDATE → P1_HARAKA_MARK_IDENTITY_CARRIER: أصل P1 هو TypedCodePoint
        with pytest.raises(RegistryViolation):
            registry.assert_transition_allowed(
                LAYER_ID_P0_UNICODE_CANDIDATE,
                LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
            )

    def test_CORE3_LINEAGE_04_typed_codepoint_to_haraka_mark_identity_allowed(self):
        """CORE3-LINEAGE-04: الانتقال من TypedCodePoint إلى HarakaMarkIdentityCarrier مسموح."""
        registry = build_master_registry_seed()
        # P0_TYPED_CODEPOINT → P1_HARAKA_MARK_IDENTITY_CARRIER: أصل P1 هو TypedCodePoint — صحيح
        registry.assert_transition_allowed(
            LAYER_ID_P0_TYPED_CODEPOINT,
            LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
        )

    def test_CORE3_LINEAGE_05_typed_codepoint_to_letter_identity_allowed(self):
        """CORE3-LINEAGE-05: الانتقال من TypedCodePoint إلى LetterIdentityCarrier مسموح."""
        registry = build_master_registry_seed()
        registry.assert_transition_allowed(
            LAYER_ID_P0_TYPED_CODEPOINT,
            LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
        )

    def test_CORE3_LINEAGE_06_slot_candidate_multi_origin_allows_any_p1_source(self):
        """CORE3-LINEAGE-06: SlotCandidate يُعلن allowed_previous_layer_ids — عقد multi-origin مصرح."""
        registry = build_master_registry_seed()
        # SlotCandidate يملك allowed_previous_layer_ids صريح — يُسمح بالانتقال من أي مصدر P1 مُعلَن
        for from_layer_id in (
            LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
            LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
            LAYER_ID_P1_POSITION_CARRIER,
            LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
        ):
            registry.assert_transition_allowed(from_layer_id, LAYER_ID_P1_SLOT_CANDIDATE)
