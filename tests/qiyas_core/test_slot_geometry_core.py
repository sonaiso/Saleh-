"""
test_slot_geometry_core.py — الاختبارات الدستورية لـ PR-CORE-0

كل اختبار مرتبط بقانون دستوري محدد.
الاختبارات تمنع:
    - Layer بلا Origin
    - Layer بلا Branch
    - Layer بلا TargetBoundary
    - Layer بلا MinimumCompletionSpec
    - Transition بلا IdentityInheritance
    - RegistryEntry ينتج Judgment
    - PR/Layer غير موجود في MasterLayerRegistry
    - Gamma بلا TargetBoundary

أقسام الاختبارات:
    SGC-LAYERSPEC-*    — اختبارات LayerSpec
    SGC-BOUNDARY-*     — اختبارات TargetBoundary
    SGC-MINCOMP-*      — اختبارات MinimumCompletionSpec
    SGC-IDENTITY-*     — اختبارات IdentityInheritance
    SGC-REGISTRY-*     — اختبارات RegistryEntry
    SGC-MASTER-*       — اختبارات MasterLayerRegistry
    SGC-GAMMA-*        — اختبارات gamma()
    SGC-INTEGRATION-*  — اختبارات تكاملية
"""
import pytest

from qiyas_core.slot_geometry_core import (
    BranchSpec,
    GammaResult,
    GammaStatus,
    IdentityInheritance,
    IdentityInheritanceViolation,
    LayerSpec,
    LayerStatus,
    MasterLayerRegistry,
    MinimumCompletionSpec,
    MinimumCompletionViolation,
    OriginSpec,
    RegistryEntry,
    RegistryEntryViolation,
    RegistryViolation,
    TargetBoundary,
    gamma,
)
from qiyas_core.slot_geometry_core.registry_entry import RegistryDomain, RegistryScope
from qiyas_core.slot_geometry_core.target_boundary import ClosureState


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures — نماذج صالحة قابلة لإعادة الاستخدام
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_origin() -> OriginSpec:
    return OriginSpec(layer_id="L01_UNICODE", output_type="UnicodeCandidate")


@pytest.fixture
def valid_branch() -> BranchSpec:
    return BranchSpec(
        output_type="WrittenSurfaceCarrier",
        branch_reason="تمثيل الرمز المكتوب كحامل سطحي",
    )


@pytest.fixture
def valid_target_boundary() -> TargetBoundary:
    return TargetBoundary(
        closes=("written_surface_units",),
        does_not_close=("syllable", "phoneme", "root", "wazn", "meaning", "hukm"),
    )


@pytest.fixture
def valid_layer_spec(valid_origin, valid_branch) -> LayerSpec:
    return LayerSpec(
        id="L02_WRITTEN_SURFACE",
        name="WrittenSurfaceCarrier",
        phase="DalAlone",
        origin=valid_origin,
        branch=valid_branch,
        shared_cause="قابلية الرمز اليونيكودي للتمثيل كوحدة سطحية مكتوبة",
        conditions=("unicode_identity_established", "arabic_script_confirmed"),
        blockers=("non_arabic_script",),
        invalidating_differences=("encoding_corruption",),
        target_boundary_closes=("written_surface_units",),
        target_boundary_opens=("letter_surface", "haraka_surface"),
        forbidden_outputs=(
            "syllable", "phoneme", "root", "wazn", "meaning", "hukm",
            "HukmCandidate", "RealityClaim", "FinalMeaning",
        ),
        minimum_required_fields=(
            "original_text", "text_identity", "unicode_provenance",
            "base_letters", "forbidden_outputs", "residuals",
        ),
        preserves_ids=("source_text_identity", "codepoint_trace"),
        allowed_changes=("group_codepoints_into_surface_units",),
        forbidden_changes=("assign_root", "assign_meaning", "assign_case"),
        status=LayerStatus.SPECIFIED,
        allowed_previous_layer_ids=("L01_UNICODE",),
        allowed_next_layer_ids=("L03_LETTER_SURFACE", "L04_HARAKA_SURFACE"),
        forbidden_direct_next_layer_ids=("L_ROOT_GEOMETRY", "L_MEANING_GEOMETRY"),
    )


@pytest.fixture
def valid_min_completion() -> MinimumCompletionSpec:
    return MinimumCompletionSpec(
        required_fields=(
            "original_text", "text_identity", "unicode_provenance",
            "base_letters", "forbidden_outputs", "residuals",
        ),
        requires_origin=True,
        requires_residuals=True,
        requires_identity=True,
        requires_trace=True,
        requires_forbidden_declared=True,
    )


@pytest.fixture
def valid_identity_inheritance() -> IdentityInheritance:
    return IdentityInheritance(
        preserves=("source_text_identity",),
        allowed_changes=("group_codepoints_into_surface_units",),
        forbidden_changes=("assign_root", "assign_meaning", "assign_case"),
    )


@pytest.fixture
def valid_registry_entry() -> RegistryEntry:
    return RegistryEntry(
        id="AUGMENT_LETTERS",
        domain=RegistryDomain.MORPHOLOGICAL_PRIOR,
        scope=RegistryScope.PRE_JUDGMENT,
        membership_opens="AugmentEligibilityPrior",
        forbidden_outputs=(
            "actual_augmentation_judgment", "root_removal",
            "morphological_role", "HukmCandidate",
        ),
        upgrade_requires=(
            "word_context", "root_candidate", "wazn_candidate", "evidence_gate",
        ),
        members=("س", "أ", "ل", "ت", "م", "و", "ن", "ي", "ه", "ا"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# SGC-LAYERSPEC — اختبارات LayerSpec
# ─────────────────────────────────────────────────────────────────────────────

class TestLayerSpec:
    """SGC-LAYERSPEC — يجب أن تكون كل طبقة عقدًا كاملًا."""

    def test_SGC_LAYERSPEC_01_valid_spec_is_accepted(self, valid_layer_spec):
        """SGC-LAYERSPEC-01: طبقة كاملة الحقول تُقبل."""
        assert valid_layer_spec.id == "L02_WRITTEN_SURFACE"
        assert valid_layer_spec.origin.layer_id == "L01_UNICODE"

    def test_SGC_LAYERSPEC_02_no_layer_without_origin(self, valid_branch):
        """SGC-LAYERSPEC-02: لا طبقة بلا أصل — OriginSpec.layer_id مطلوب."""
        with pytest.raises(ValueError, match="layer_id is required"):
            OriginSpec(layer_id="", output_type="UnicodeCandidate")

    def test_SGC_LAYERSPEC_03_no_branch_without_reason(self):
        """SGC-LAYERSPEC-03: لا فرع بلا سبب تفريع."""
        with pytest.raises(ValueError, match="branch_reason is required"):
            BranchSpec(output_type="WrittenSurfaceCarrier", branch_reason="")

    def test_SGC_LAYERSPEC_04_forbidden_outputs_mandatory(self, valid_origin, valid_branch):
        """SGC-LAYERSPEC-04: كل طبقة يجب أن تُصرح بممنوعاتها."""
        with pytest.raises(ValueError, match="forbidden_outputs is required"):
            LayerSpec(
                id="L_TEST",
                name="Test",
                phase="test",
                origin=valid_origin,
                branch=valid_branch,
                shared_cause="علة",
                conditions=("cond_a",),
                blockers=(),
                invalidating_differences=(),
                target_boundary_closes=("test_output",),
                target_boundary_opens=(),
                forbidden_outputs=(),
                minimum_required_fields=("field_a",),
                preserves_ids=("id_a",),
                allowed_changes=(),
                forbidden_changes=(),
            )

    def test_SGC_LAYERSPEC_05_absolute_forbidden_always_required(self, valid_origin, valid_branch):
        """SGC-LAYERSPEC-05: HukmCandidate/RealityClaim/FinalMeaning محظورات مطلقة."""
        with pytest.raises(ValueError, match="must include"):
            LayerSpec(
                id="L_TEST",
                name="Test",
                phase="test",
                origin=valid_origin,
                branch=valid_branch,
                shared_cause="علة",
                conditions=("cond_a",),
                blockers=(),
                invalidating_differences=(),
                target_boundary_closes=("test_output",),
                target_boundary_opens=(),
                # ناقص HukmCandidate/RealityClaim/FinalMeaning
                forbidden_outputs=("syllable",),
                minimum_required_fields=("field_a",),
                preserves_ids=("id_a",),
                allowed_changes=(),
                forbidden_changes=(),
            )

    def test_SGC_LAYERSPEC_06_no_conditions_is_rejected(self, valid_origin, valid_branch):
        """SGC-LAYERSPEC-06: طبقة بلا شروط مرفوضة."""
        with pytest.raises(ValueError, match="conditions must have at least one"):
            LayerSpec(
                id="L_TEST",
                name="Test",
                phase="test",
                origin=valid_origin,
                branch=valid_branch,
                shared_cause="علة",
                conditions=(),
                blockers=(),
                invalidating_differences=(),
                target_boundary_closes=("test_output",),
                target_boundary_opens=(),
                forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
                minimum_required_fields=("field_a",),
                preserves_ids=("id_a",),
                allowed_changes=(),
                forbidden_changes=(),
            )

    def test_SGC_LAYERSPEC_07_allowed_and_forbidden_overlap_rejected(
        self, valid_origin, valid_branch
    ):
        """SGC-LAYERSPEC-07: لا يجوز أن يكون نفس الشيء مسموحًا ومحظورًا."""
        with pytest.raises(ValueError, match="overlap"):
            LayerSpec(
                id="L_TEST",
                name="Test",
                phase="test",
                origin=valid_origin,
                branch=valid_branch,
                shared_cause="علة",
                conditions=("cond_a",),
                blockers=(),
                invalidating_differences=(),
                target_boundary_closes=("test_output",),
                target_boundary_opens=(),
                forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
                minimum_required_fields=("field_a",),
                preserves_ids=("id_a",),
                allowed_changes=("assign_root",),
                forbidden_changes=("assign_root",),  # تعارض!
            )

    def test_SGC_LAYERSPEC_08_preserves_ids_mandatory(self, valid_origin, valid_branch):
        """SGC-LAYERSPEC-08: كل طبقة يجب أن تُحدد ما تحفظه من الهويات."""
        with pytest.raises(ValueError, match="preserves_ids is required"):
            LayerSpec(
                id="L_TEST",
                name="Test",
                phase="test",
                origin=valid_origin,
                branch=valid_branch,
                shared_cause="علة",
                conditions=("cond_a",),
                blockers=(),
                invalidating_differences=(),
                target_boundary_closes=("test_output",),
                target_boundary_opens=(),
                forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
                minimum_required_fields=("field_a",),
                preserves_ids=(),
                allowed_changes=(),
                forbidden_changes=(),
            )


# ─────────────────────────────────────────────────────────────────────────────
# SGC-BOUNDARY — اختبارات TargetBoundary
# ─────────────────────────────────────────────────────────────────────────────

class TestTargetBoundary:
    """SGC-BOUNDARY — الحد المستهدف يمنع القفزات المحظورة."""

    def test_SGC_BOUNDARY_01_valid_boundary_accepted(self, valid_target_boundary):
        """SGC-BOUNDARY-01: حد سليم يُقبل."""
        assert "written_surface_units" in valid_target_boundary.closes
        assert "syllable" in valid_target_boundary.does_not_close

    def test_SGC_BOUNDARY_02_empty_closes_rejected(self):
        """SGC-BOUNDARY-02: لا حد بلا ما يُغلقه."""
        with pytest.raises(ValueError, match="closes is required"):
            TargetBoundary(closes=(), does_not_close=("syllable",))

    def test_SGC_BOUNDARY_03_overlap_rejected(self):
        """SGC-BOUNDARY-03: نفس الشيء لا يكون في closes وdoes_not_close."""
        with pytest.raises(ValueError, match="in both closes and does_not_close"):
            TargetBoundary(
                closes=("syllable",),
                does_not_close=("syllable", "root"),
            )

    def test_SGC_BOUNDARY_04_allowed_output_returns_minimally_closed(
        self, valid_target_boundary
    ):
        """SGC-BOUNDARY-04: مخرج مسموح يُعطي MINIMALLY_CLOSED."""
        result = valid_target_boundary.check_output("written_surface_units")
        assert result == ClosureState.MINIMALLY_CLOSED

    def test_SGC_BOUNDARY_05_forbidden_output_returns_forbidden_leap(
        self, valid_target_boundary
    ):
        """SGC-BOUNDARY-05: مخرج محظور يُعطي FORBIDDEN_LEAP."""
        result = valid_target_boundary.check_output("syllable")
        assert result == ClosureState.FORBIDDEN_LEAP

    def test_SGC_BOUNDARY_06_undeclared_output_returns_open(self, valid_target_boundary):
        """SGC-BOUNDARY-06: مخرج غير مُعرَّف يُعطي OPEN."""
        result = valid_target_boundary.check_output("some_unknown_type")
        assert result == ClosureState.OPEN

    def test_SGC_BOUNDARY_07_forbidden_types_include_hukm_family(self):
        """SGC-BOUNDARY-07: الحد يمنع HukmCandidate/RealityClaim/FinalMeaning."""
        boundary = TargetBoundary(
            closes=("written_surface_units",),
            does_not_close=("HukmCandidate", "RealityClaim", "FinalMeaning"),
        )
        assert boundary.forbids("HukmCandidate")
        assert boundary.forbids("RealityClaim")
        assert boundary.forbids("FinalMeaning")


# ─────────────────────────────────────────────────────────────────────────────
# SGC-MINCOMP — اختبارات MinimumCompletionSpec
# ─────────────────────────────────────────────────────────────────────────────

class TestMinimumCompletionSpec:
    """SGC-MINCOMP — الاكتمال الأدنى برهان لا قائمة."""

    def test_SGC_MINCOMP_01_valid_completion_passes(
        self, valid_min_completion, valid_target_boundary
    ):
        """SGC-MINCOMP-01: مرشح كامل يجتاز التحقق."""
        valid_min_completion.verify(
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            has_origin_trace=True,
            has_residuals=True,
            has_identity=True,
            has_trace=True,
            has_forbidden_declared=True,
            output_type="written_surface_units",
            target_boundary=valid_target_boundary,
        )

    def test_SGC_MINCOMP_02_missing_field_raises(
        self, valid_min_completion, valid_target_boundary
    ):
        """SGC-MINCOMP-02: حقل ناقص يرفع MinimumCompletionViolation."""
        with pytest.raises(MinimumCompletionViolation, match="missing required fields"):
            valid_min_completion.verify(
                candidate_fields=frozenset({"original_text"}),  # ناقص كثير
                has_origin_trace=True,
                has_residuals=True,
                has_identity=True,
                has_trace=True,
                has_forbidden_declared=True,
                output_type="written_surface_units",
                target_boundary=valid_target_boundary,
            )

    def test_SGC_MINCOMP_03_missing_origin_trace_raises(
        self, valid_min_completion, valid_target_boundary
    ):
        """SGC-MINCOMP-03: غياب أثر الأصل يرفع خطأ."""
        with pytest.raises(MinimumCompletionViolation, match="origin trace is missing"):
            valid_min_completion.verify(
                candidate_fields=frozenset({
                    "original_text", "text_identity", "unicode_provenance",
                    "base_letters", "forbidden_outputs", "residuals",
                }),
                has_origin_trace=False,
                has_residuals=True,
                has_identity=True,
                has_trace=True,
                has_forbidden_declared=True,
                output_type="written_surface_units",
                target_boundary=valid_target_boundary,
            )

    def test_SGC_MINCOMP_04_missing_identity_raises(
        self, valid_min_completion, valid_target_boundary
    ):
        """SGC-MINCOMP-04: غياب الهوية يرفع خطأ."""
        with pytest.raises(MinimumCompletionViolation, match="identity not preserved"):
            valid_min_completion.verify(
                candidate_fields=frozenset({
                    "original_text", "text_identity", "unicode_provenance",
                    "base_letters", "forbidden_outputs", "residuals",
                }),
                has_origin_trace=True,
                has_residuals=True,
                has_identity=False,
                has_trace=True,
                has_forbidden_declared=True,
                output_type="written_surface_units",
                target_boundary=valid_target_boundary,
            )

    def test_SGC_MINCOMP_05_forbidden_leap_in_output_raises(
        self, valid_min_completion, valid_target_boundary
    ):
        """SGC-MINCOMP-05: مخرج يتجاوز الحد يرفع خطأ."""
        with pytest.raises(MinimumCompletionViolation, match="FORBIDDEN_LEAP"):
            valid_min_completion.verify(
                candidate_fields=frozenset({
                    "original_text", "text_identity", "unicode_provenance",
                    "base_letters", "forbidden_outputs", "residuals",
                }),
                has_origin_trace=True,
                has_residuals=True,
                has_identity=True,
                has_trace=True,
                has_forbidden_declared=True,
                output_type="syllable",  # تجاوز الحد!
                target_boundary=valid_target_boundary,
            )

    def test_SGC_MINCOMP_06_empty_required_fields_raises(self):
        """SGC-MINCOMP-06: MinimumCompletionSpec بلا حقول مرفوض."""
        with pytest.raises(ValueError, match="required_fields must not be empty"):
            MinimumCompletionSpec(required_fields=())

    def test_SGC_MINCOMP_07_multiple_violations_reported_together(
        self, valid_min_completion, valid_target_boundary
    ):
        """SGC-MINCOMP-07: كل الانتهاكات تُبلَّغ معًا لا واحدًا واحدًا."""
        with pytest.raises(MinimumCompletionViolation) as exc_info:
            valid_min_completion.verify(
                candidate_fields=frozenset({"original_text"}),
                has_origin_trace=False,
                has_residuals=False,
                has_identity=False,
                has_trace=False,
                has_forbidden_declared=False,
                output_type="written_surface_units",
                target_boundary=valid_target_boundary,
            )
        error_msg = str(exc_info.value)
        # يجب أن تُذكر عدة انتهاكات
        assert "missing required fields" in error_msg
        assert "origin trace is missing" in error_msg
        assert "residuals not registered" in error_msg


# ─────────────────────────────────────────────────────────────────────────────
# SGC-IDENTITY — اختبارات IdentityInheritance
# ─────────────────────────────────────────────────────────────────────────────

class TestIdentityInheritance:
    """SGC-IDENTITY — الهوية الموروثة عقد لا مجرد حقل."""

    def test_SGC_IDENTITY_01_valid_inheritance_passes(self, valid_identity_inheritance):
        """SGC-IDENTITY-01: انتقال سليم يجتاز التحقق."""
        valid_identity_inheritance.verify(
            source_identity_ids=frozenset({"source_text_identity:text_001"}),
            output_identity_ids=frozenset({"source_text_identity:text_001", "surface_unit:0"}),
            output_operation="group_codepoints_into_surface_units",
        )

    def test_SGC_IDENTITY_02_empty_preserves_rejected(self):
        """SGC-IDENTITY-02: لا هوية بلا أثر — preserves مطلوب."""
        with pytest.raises(ValueError, match="preserves is required"):
            IdentityInheritance(
                preserves=(),
                allowed_changes=("group",),
                forbidden_changes=(),
            )

    def test_SGC_IDENTITY_03_forbidden_operation_raises(self, valid_identity_inheritance):
        """SGC-IDENTITY-03: عملية محظورة تُرفع."""
        with pytest.raises(IdentityInheritanceViolation, match="is forbidden"):
            valid_identity_inheritance.verify(
                source_identity_ids=frozenset({"source_text_identity:text_001"}),
                output_identity_ids=frozenset({"source_text_identity:text_001"}),
                output_operation="assign_root",  # محظور!
            )

    def test_SGC_IDENTITY_04_assign_meaning_is_forbidden(self, valid_identity_inheritance):
        """SGC-IDENTITY-04: تعيين معنى في طبقة السطح محظور."""
        with pytest.raises(IdentityInheritanceViolation):
            valid_identity_inheritance.verify(
                source_identity_ids=frozenset({"source_text_identity:text_001"}),
                output_identity_ids=frozenset({"source_text_identity:text_001"}),
                output_operation="assign_meaning",  # محظور!
            )

    def test_SGC_IDENTITY_05_overlap_in_allowed_and_forbidden_rejected(self):
        """SGC-IDENTITY-05: لا يجوز أن يكون نفس الشيء مسموحًا ومحظورًا."""
        with pytest.raises(ValueError, match="same item"):
            IdentityInheritance(
                preserves=("id_a",),
                allowed_changes=("assign_root",),
                forbidden_changes=("assign_root",),
            )


# ─────────────────────────────────────────────────────────────────────────────
# SGC-REGISTRY — اختبارات RegistryEntry
# ─────────────────────────────────────────────────────────────────────────────

class TestRegistryEntry:
    """SGC-REGISTRY — السجل يفتح Prior لا يُصدر Judgment."""

    def test_SGC_REGISTRY_01_valid_entry_accepted(self, valid_registry_entry):
        """SGC-REGISTRY-01: مدخل سجل سليم يُقبل."""
        assert valid_registry_entry.id == "AUGMENT_LETTERS"
        assert valid_registry_entry.membership_opens == "AugmentEligibilityPrior"

    def test_SGC_REGISTRY_02_membership_opens_required(self):
        """SGC-REGISTRY-02: العضوية تفتح Prior — membership_opens مطلوب."""
        with pytest.raises(ValueError, match="membership_opens is required"):
            RegistryEntry(
                id="TEST",
                domain=RegistryDomain.MORPHOLOGICAL_PRIOR,
                scope=RegistryScope.PRE_JUDGMENT,
                membership_opens="",
                forbidden_outputs=("judgment",),
                upgrade_requires=("context",),
            )

    def test_SGC_REGISTRY_03_forbidden_outputs_required(self):
        """SGC-REGISTRY-03: كل entry يُصرح بما لا ينتجه."""
        with pytest.raises(ValueError, match="forbidden_outputs is required"):
            RegistryEntry(
                id="TEST",
                domain=RegistryDomain.MORPHOLOGICAL_PRIOR,
                scope=RegistryScope.PRE_JUDGMENT,
                membership_opens="TestPrior",
                forbidden_outputs=(),
                upgrade_requires=("context",),
            )

    def test_SGC_REGISTRY_04_opens_prior_returns_prior_type(self, valid_registry_entry):
        """SGC-REGISTRY-04: opens_prior يُعيد نوع الـ Prior فقط."""
        prior = valid_registry_entry.opens_prior("س")
        assert prior == "AugmentEligibilityPrior"

    def test_SGC_REGISTRY_05_assert_no_judgment_passes_for_allowed_type(
        self, valid_registry_entry
    ):
        """SGC-REGISTRY-05: نوع غير محظور يمر بلا خطأ."""
        valid_registry_entry.assert_no_judgment("AugmentEligibilityPrior")

    def test_SGC_REGISTRY_06_assert_no_judgment_raises_for_forbidden_type(
        self, valid_registry_entry
    ):
        """SGC-REGISTRY-06: نوع محظور يُرفع."""
        with pytest.raises(RegistryEntryViolation, match="cannot produce"):
            valid_registry_entry.assert_no_judgment("actual_augmentation_judgment")

    def test_SGC_REGISTRY_07_hukm_candidate_is_always_forbidden(self):
        """SGC-REGISTRY-07: HukmCandidate محظور في كل entry."""
        entry = RegistryEntry(
            id="TEST",
            domain=RegistryDomain.PHONOLOGICAL_PRIOR,
            scope=RegistryScope.PRE_JUDGMENT,
            membership_opens="PhoneticPrior",
            forbidden_outputs=("HukmCandidate", "RealityClaim"),
            upgrade_requires=("phonetic_context",),
        )
        with pytest.raises(RegistryEntryViolation):
            entry.assert_no_judgment("HukmCandidate")

    def test_SGC_REGISTRY_08_membership_is_prior_not_judgment(self, valid_registry_entry):
        """SGC-REGISTRY-08: العضوية prior لا حكم — اختبار المبدأ الجوهري."""
        # العضوية في "حروف الزيادة" لا تعني وقوع الزيادة
        prior = valid_registry_entry.opens_prior("و")
        assert "Prior" in prior, "membership must open a Prior, not a Judgment"
        assert "Judgment" not in prior
        assert "Final" not in prior


# ─────────────────────────────────────────────────────────────────────────────
# SGC-MASTER — اختبارات MasterLayerRegistry
# ─────────────────────────────────────────────────────────────────────────────

class TestMasterLayerRegistry:
    """SGC-MASTER — سجل الطبقات الرئيسي يمنع الفوضى."""

    def test_SGC_MASTER_01_register_and_get(self, valid_layer_spec):
        """SGC-MASTER-01: تسجيل وجلب طبقة يعمل."""
        registry = MasterLayerRegistry()
        # يجب تسجيل الأصل أولاً
        origin_spec = LayerSpec(
            id="L01_UNICODE",
            name="UnicodeQiyas",
            phase="DalAlone",
            origin=OriginSpec(layer_id="ROOT", output_type="RawText"),
            branch=BranchSpec(output_type="UnicodeCandidate", branch_reason="ترميز نصي"),
            shared_cause="قابلية النص للتمثيل الرقمي",
            conditions=("text_not_empty",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("unicode_codepoints",),
            target_boundary_opens=("written_surface",),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("text",),
            preserves_ids=("source_text",),
            allowed_changes=("encode_to_codepoints",),
            forbidden_changes=("assign_meaning",),
        )
        registry.register(origin_spec)
        registry.register(valid_layer_spec)
        retrieved = registry.get("L02_WRITTEN_SURFACE")
        assert retrieved.name == "WrittenSurfaceCarrier"

    def test_SGC_MASTER_02_duplicate_registration_rejected(self, valid_layer_spec):
        """SGC-MASTER-02: تسجيل طبقة مكررة يُرفض."""
        registry = MasterLayerRegistry()
        origin_spec = LayerSpec(
            id="L01_UNICODE",
            name="UnicodeQiyas",
            phase="DalAlone",
            origin=OriginSpec(layer_id="ROOT", output_type="RawText"),
            branch=BranchSpec(output_type="UnicodeCandidate", branch_reason="ترميز"),
            shared_cause="علة",
            conditions=("cond_a",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("unicode_codepoints",),
            target_boundary_opens=(),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("text",),
            preserves_ids=("source_text",),
            allowed_changes=(),
            forbidden_changes=(),
        )
        registry.register(origin_spec)
        registry.register(valid_layer_spec)
        with pytest.raises(RegistryViolation, match="already registered"):
            registry.register(valid_layer_spec)

    def test_SGC_MASTER_03_unregistered_origin_rejected(self, valid_layer_spec):
        """SGC-MASTER-03: طبقة بأصل غير مسجل تُرفض."""
        registry = MasterLayerRegistry()
        # L01_UNICODE غير مسجل
        with pytest.raises(RegistryViolation, match="not yet registered"):
            registry.register(valid_layer_spec)

    def test_SGC_MASTER_04_get_unregistered_raises(self):
        """SGC-MASTER-04: جلب طبقة غير مسجلة يرفع خطأ."""
        registry = MasterLayerRegistry()
        with pytest.raises(RegistryViolation, match="not registered"):
            registry.get("L_NONEXISTENT")

    def test_SGC_MASTER_05_forbidden_direct_next_blocked(self):
        """SGC-MASTER-05: الانتقال إلى طبقة محظورة مباشرة يُحجب."""
        registry = MasterLayerRegistry()
        l01 = LayerSpec(
            id="L01_UNICODE",
            name="Unicode",
            phase="test",
            origin=OriginSpec(layer_id="ROOT", output_type="RawText"),
            branch=BranchSpec(output_type="UnicodeCandidate", branch_reason="ترميز"),
            shared_cause="علة",
            conditions=("cond_a",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("unicode_codepoints",),
            target_boundary_opens=(),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("text",),
            preserves_ids=("source_text",),
            allowed_changes=(),
            forbidden_changes=(),
            forbidden_direct_next_layer_ids=("L_MEANING",),
        )
        l_meaning = LayerSpec(
            id="L_MEANING",
            name="MeaningLayer",
            phase="test",
            origin=OriginSpec(layer_id="L01_UNICODE", output_type="UnicodeCandidate"),
            branch=BranchSpec(output_type="MeaningCandidate", branch_reason="معنى"),
            shared_cause="علة",
            conditions=("cond_a",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("meaning_candidate",),
            target_boundary_opens=(),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("meaning",),
            preserves_ids=("source_id",),
            allowed_changes=(),
            forbidden_changes=(),
        )
        registry.register(l01)
        registry.register(l_meaning)
        with pytest.raises(RegistryViolation, match="FORBIDDEN"):
            registry.assert_transition_allowed("L01_UNICODE", "L_MEANING")

    def test_SGC_MASTER_06_root_origin_allowed(self):
        """SGC-MASTER-06: طبقة بأصل ROOT تُقبل بدون تسجيل مسبق."""
        registry = MasterLayerRegistry()
        root_layer = LayerSpec(
            id="L01_UNICODE",
            name="UnicodeQiyas",
            phase="DalAlone",
            origin=OriginSpec(layer_id="ROOT", output_type="RawText"),
            branch=BranchSpec(output_type="UnicodeCandidate", branch_reason="ترميز"),
            shared_cause="علة",
            conditions=("cond_a",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("unicode_codepoints",),
            target_boundary_opens=(),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("text",),
            preserves_ids=("source_text",),
            allowed_changes=(),
            forbidden_changes=(),
        )
        registry.register(root_layer)
        assert "L01_UNICODE" in registry

    def test_SGC_MASTER_07_len_and_contains(self, valid_layer_spec):
        """SGC-MASTER-07: __len__ و__contains__ يعملان."""
        registry = MasterLayerRegistry()
        origin = LayerSpec(
            id="L01_UNICODE",
            name="Unicode",
            phase="test",
            origin=OriginSpec(layer_id="ROOT", output_type="RawText"),
            branch=BranchSpec(output_type="UnicodeCandidate", branch_reason="ترميز"),
            shared_cause="علة",
            conditions=("cond_a",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("unicode_codepoints",),
            target_boundary_opens=(),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("text",),
            preserves_ids=("source_text",),
            allowed_changes=(),
            forbidden_changes=(),
        )
        assert len(registry) == 0
        registry.register(origin)
        assert len(registry) == 1
        registry.register(valid_layer_spec)
        assert len(registry) == 2
        assert "L02_WRITTEN_SURFACE" in registry
        assert "L_NONEXISTENT" not in registry


# ─────────────────────────────────────────────────────────────────────────────
# SGC-GAMMA — اختبارات gamma()
# ─────────────────────────────────────────────────────────────────────────────

class TestGamma:
    """SGC-GAMMA — Gamma مقيدة بالحد المستهدف."""

    def test_SGC_GAMMA_01_valid_candidate_is_minimally_closed(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-01: مرشح كامل يُعطي MINIMALLY_CLOSED."""
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
                "unicode_identity_established", "arabic_script_confirmed",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({"source_text_identity:text_001"}),
            candidate_trace_ids=frozenset({"trace:unicode:001"}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.MINIMALLY_CLOSED
        assert result.is_complete
        assert len(result.violations) == 0

    def test_SGC_GAMMA_02_forbidden_leap_detected(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-02: Gamma تكتشف FORBIDDEN_LEAP عند تجاوز الحد."""
        result = gamma(
            candidate_type="syllable",  # تجاوز الحد!
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({"id:001"}),
            candidate_trace_ids=frozenset({"trace:001"}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.FORBIDDEN_LEAP
        assert result.is_forbidden_leap
        assert not result.is_complete

    def test_SGC_GAMMA_03_missing_identity_is_blocked(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-03: غياب الهوية يُعطي BLOCKED."""
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset(),  # لا هوية!
            candidate_trace_ids=frozenset({"trace:001"}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.BLOCKED
        assert any("identity" in v for v in result.violations)

    def test_SGC_GAMMA_04_missing_trace_is_blocked(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-04: غياب الأثر يُعطي BLOCKED."""
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({"id:001"}),
            candidate_trace_ids=frozenset(),  # لا أثر!
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.BLOCKED
        assert any("trace" in v for v in result.violations)

    def test_SGC_GAMMA_05_identity_trace_overlap_is_blocked(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-05: اختلاط identity وtrace يُعطي BLOCKED — الثابت الدستوري #1."""
        shared_id = "shared:001"
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({shared_id}),
            candidate_trace_ids=frozenset({shared_id}),  # تعارض!
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.BLOCKED
        assert any("overlap" in v for v in result.violations)

    def test_SGC_GAMMA_06_gamma_result_has_layer_id(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-06: GammaResult تحمل معرّف الطبقة التي طُبّقت عليها."""
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({"id:001"}),
            candidate_trace_ids=frozenset({"trace:001"}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.layer_id == "L02_WRITTEN_SURFACE"
        assert result.target_boundary_closes == ("written_surface_units",)

    def test_SGC_GAMMA_07_gamma_for_written_surface_does_not_check_syllable(
        self, valid_layer_spec
    ):
        """SGC-GAMMA-07: Gamma طبقة السطح لا تفحص المقطع — كل Gamma مقيدة بحدها."""
        syllable_boundary = TargetBoundary(
            closes=("syllable_candidate",),
            does_not_close=("root", "meaning"),
        )
        # الحد المستهدف مختلف — Gamma طبقة السطح لا تُفعَّل على Gamma المقطع
        result = gamma(
            candidate_type="syllable_candidate",
            candidate_fields=frozenset({"letter", "haraka", "syllable_units"}),
            candidate_has_residuals=False,
            candidate_identity_ids=frozenset({"id:001"}),
            candidate_trace_ids=frozenset({"trace:001"}),
            layer_spec=valid_layer_spec,  # spec طبقة السطح
            target_boundary=syllable_boundary,  # لكن الحد حد المقطع
        )
        # المخرج "syllable_candidate" مسموح به في حد المقطع
        # لكن Gamma تفحص أيضًا minimum_required_fields من valid_layer_spec
        assert result.layer_id == "L02_WRITTEN_SURFACE"

    def test_SGC_GAMMA_08_active_blocker_causes_blocked_status(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-GAMMA-08: مانع نشط يُعطي BLOCKED."""
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
                "non_arabic_script",  # مانع نشط!
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({"id:001"}),
            candidate_trace_ids=frozenset({"trace:001"}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.BLOCKED
        assert any("blocker" in v for v in result.violations)


# ─────────────────────────────────────────────────────────────────────────────
# SGC-INTEGRATION — اختبارات تكاملية
# ─────────────────────────────────────────────────────────────────────────────

class TestSlotGeometryCoreIntegration:
    """SGC-INTEGRATION — النظام الكامل يعمل كعقد برمجي متكامل."""

    def test_SGC_INT_01_full_layer_lifecycle(self, valid_layer_spec, valid_target_boundary):
        """
        SGC-INT-01: دورة حياة الطبقة الكاملة:
            LayerSpec → MasterLayerRegistry → gamma() → GammaResult
        """
        registry = MasterLayerRegistry()
        # تسجيل الأصل
        root_spec = LayerSpec(
            id="L01_UNICODE",
            name="UnicodeQiyas",
            phase="DalAlone",
            origin=OriginSpec(layer_id="ROOT", output_type="RawText"),
            branch=BranchSpec(output_type="UnicodeCandidate", branch_reason="ترميز"),
            shared_cause="قابلية النص للتمثيل الرقمي",
            conditions=("text_not_empty",),
            blockers=(),
            invalidating_differences=(),
            target_boundary_closes=("unicode_codepoints",),
            target_boundary_opens=("written_surface",),
            forbidden_outputs=("HukmCandidate", "RealityClaim", "FinalMeaning"),
            minimum_required_fields=("text",),
            preserves_ids=("source_text",),
            allowed_changes=("encode_to_codepoints",),
            forbidden_changes=("assign_meaning",),
        )
        registry.register(root_spec)
        registry.register(valid_layer_spec)

        # تطبيق Gamma
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
                "unicode_identity_established", "arabic_script_confirmed",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({"source_text_identity:بسم"}),
            candidate_trace_ids=frozenset({"trace:unicode:u0628", "trace:unicode:u0633"}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )

        assert result.is_complete
        assert result.status == GammaStatus.MINIMALLY_CLOSED
        assert "L02_WRITTEN_SURFACE" in registry

    def test_SGC_INT_02_no_pr_without_registry_entry(self):
        """
        SGC-INT-02: لا PR بلا موقع في سجل الأصل والفرع.
        محاولة استخدام layer_id غير مسجل تُرفض.
        """
        registry = MasterLayerRegistry()
        with pytest.raises(RegistryViolation):
            registry.assert_layer_registered("L_NONEXISTENT_LAYER")

    def test_SGC_INT_03_registry_entry_opens_prior_not_hukm(self, valid_registry_entry):
        """
        SGC-INT-03: مبدأ Registry الجبري:
            و ∈ حروف العلة لا تعني: و وقع فيها إعلال
            بل تعني: WeaknessPrior مفتوح مع بقايا
        """
        weak_entry = RegistryEntry(
            id="WEAK_LETTERS",
            domain=RegistryDomain.PHONOLOGICAL_PRIOR,
            scope=RegistryScope.PRE_JUDGMENT,
            membership_opens="WeaknessPrior",
            forbidden_outputs=(
                "ilab_judgment", "actual_weakness", "HukmCandidate",
                "RealityClaim", "FinalMeaning",
            ),
            upgrade_requires=("word_context", "pattern_evidence", "irab_context"),
            members=("و", "ي", "ا"),
        )
        prior = weak_entry.opens_prior("و")
        assert prior == "WeaknessPrior"
        # لا يجوز أن يُنتج حكمًا
        with pytest.raises(RegistryEntryViolation):
            weak_entry.assert_no_judgment("ilab_judgment")

    def test_SGC_INT_04_constitutional_invariant_identity_not_trace(
        self, valid_layer_spec, valid_target_boundary
    ):
        """
        SGC-INT-04: الثابت الدستوري #1: Identity ≠ Trace
        أي مرشح يخلط بين الاثنين يُحجب.
        """
        shared = "shared_token:001"
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset({
                "original_text", "text_identity", "unicode_provenance",
                "base_letters", "forbidden_outputs", "residuals",
            }),
            candidate_has_residuals=True,
            candidate_identity_ids=frozenset({shared}),
            candidate_trace_ids=frozenset({shared}),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert result.status == GammaStatus.BLOCKED
        assert any("Constitutional Invariant #1" in v for v in result.violations)

    def test_SGC_INT_05_gamma_blocked_status_is_not_complete(
        self, valid_layer_spec, valid_target_boundary
    ):
        """SGC-INT-05: مرشح محجوب ليس مكتملًا — الإمكان لا يساوي الحكم."""
        result = gamma(
            candidate_type="written_surface_units",
            candidate_fields=frozenset(),  # فارغ
            candidate_has_residuals=False,
            candidate_identity_ids=frozenset(),
            candidate_trace_ids=frozenset(),
            layer_spec=valid_layer_spec,
            target_boundary=valid_target_boundary,
        )
        assert not result.is_complete
        assert result.status in (GammaStatus.BLOCKED, GammaStatus.FORBIDDEN_LEAP)
