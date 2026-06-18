"""
master_registry_seed.py — بذرة سجل الطبقات الرئيسي

PR-CORE-1: تسجيل المراحل P0-P12 كـ LayerSpecs مخططة فقط.
REC-2 (PROJECT_RECOVERY_CANONICAL_MAP.md §3 / §4.1 / §4.2): توحيد أسماء
الأطوار بالبادئة القانونية SCG- وإسناد كل طبقة إلى أصلها من الأصول الثلاثة.
هذا تحديث حوكمة فقط — لا تقدّم في الحالات، لا طبقات جديدة، لا runtime جديد.

القانون:
    كل مرحلة هي LayerSpec بحالة PLANNED.
    لا runtime جديد هنا.
    لا منطق خاص بالعربية أو Unicode.
    هذا السجل يمنع PRs المتفرقة من الظهور خارج خريطة المشروع.

الوظيفة:
    build_master_registry_seed() → MasterLayerRegistry
    تُرجع سجلًا يحتوي كل المراحل الـ 13 بحالة PLANNED.

تمييز البادئات (PROJECT_RECOVERY_CANONICAL_MAP.md §4.1 — binding):
    BF0    = Binary Foundation              (Binary- repository: L00…L04)
    SCG-P0 = SlotGeometry Core phase 0      (Saleh- repository: Unicode/TypedCodePoint/Glyph)
    AR-P0  = Arabic Voice/Verbal Origin     (future Arabic package/repo)
    Declared: Binary-P0 ≠ Arabic-SCG-P0.

المراحل (السلم القانوني بعد REC-2 — §4.2):
    SCG-P0  — SlotGeometry Core phase 0 (Unicode / TypedCodePoint / Glyph;
              kanat P0_BINARY_FOUNDATION — أُزيل لفظ BINARY_FOUNDATION
              حسمًا لتصادم §6.2 مع BF0)
    SCG-P1  — Dal Alone Atomic (الدال وحده ذريًا)
    SCG-P2  — Registry Projection (إسقاط السجل)
    SCG-P3  — Root Stem Closure (إغلاق الجذر والساق)
    SCG-P4  — Jamid Mushtaq (الجامد والمشتق)
    SCG-P5  — Mufrad Word Contracts (عقود الكلمة المفردة)
    SCG-P6  — Verbal Signified Alone (المدلول الفعلي وحده)
    SCG-P7  — Composition Readiness (استعداد التركيب)
    SCG-P8  — Amil Mamul (العامل والمعمول)
    SCG-P9  — Sentence Geometry (هندسة الجملة)
    SCG-P10 — Relation Geometry (هندسة العلاقة)
    SCG-P11 — Irab Geometry (هندسة الإعراب)
    SCG-P12 — Ifadah Speech Force (قوة الإفادة الكلامية)

إسناد الأصول (§3): جميع طبقات هذا السجل تخدم الأصل الثاني —
نظام لفظي عربي يحفظ انتقالات الصوت (Saleh- algebraic spine).
انظر LAYER_ORIGIN_NOTES أدناه.

غير مسموح بتنفيذ أي طبقة قبل أن تظهر في هذا السجل.
"""
from __future__ import annotations

from .layer_spec import BranchSpec, LayerSpec, LayerStatus, OriginSpec
from .master_layer_registry import MasterLayerRegistry

# ─────────────────────────────────────────────────────────────────────────────
# Layer IDs — معرفات الطبقات الكانونيكية
# ─────────────────────────────────────────────────────────────────────────────

LAYER_ID_ROOT = "ROOT"

# P0 — Binary Foundation
LAYER_ID_P0_UNICODE_CANDIDATE = "P0_UNICODE_CANDIDATE"
LAYER_ID_P0_TYPED_CODEPOINT = "P0_TYPED_CODEPOINT"
LAYER_ID_P0_GLYPH_CLASSIFICATION = "P0_GLYPH_CLASSIFICATION"

# P1 — Dal Alone Atomic
LAYER_ID_P1_LETTER_IDENTITY_CARRIER = "P1_LETTER_IDENTITY_CARRIER"
# REC-3 (Naming Correction Plan, option O3) — PROJECT_RECOVERY_CANONICAL_MAP §6.1:
# the atomic haraka layer is renamed HarakaFunctionCarrier → HarakaMarkIdentityCarrier
# (الحركة أولًا علامة ذات هوية؛ الوظيفة لاحقًا بعد Gate وسياق وتركيب). The new
# string below is the canonical layer id. See TERMINOLOGY_MAP.md §8.
LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER = "P1_HARAKA_MARK_IDENTITY_CARRIER"
# Transitional compatibility alias (REC-3 O3). The legacy constant resolves to
# the new canonical id, so untouched runtime/import sites keep working without a
# full transitive rename. The legacy string is NOT the canonical LayerSpec id or
# name — that is proved in tests/qiyas_core/test_naming_correction_rec3.py.
LAYER_ID_P1_HARAKA_FUNCTION_CARRIER = LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER
LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE = "P1_CONDITIONED_TYPED_SEQUENCE"
LAYER_ID_P1_POSITION_CARRIER = "P1_POSITION_CARRIER"
LAYER_ID_P1_SLOT_CANDIDATE = "P1_SLOT_CANDIDATE"

# P2 — Registry Projection
LAYER_ID_P2_REGISTRY_PROJECTION = "P2_REGISTRY_PROJECTION"

# P3 — Root Stem Closure
LAYER_ID_P3_ROOT_STEM_CLOSURE = "P3_ROOT_STEM_CLOSURE"

# P4 — Jamid Mushtaq
LAYER_ID_P4_JAMID_MUSHTAQ = "P4_JAMID_MUSHTAQ"

# P5 — Mufrad Word Contracts
LAYER_ID_P5_MUFRAD_WORD_CONTRACTS = "P5_MUFRAD_WORD_CONTRACTS"

# P6 — Verbal Signified Alone
LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE = "P6_VERBAL_SIGNIFIED_ALONE"

# P7 — Composition Readiness
LAYER_ID_P7_COMPOSITION_READINESS = "P7_COMPOSITION_READINESS"

# P8 — Amil Mamul
LAYER_ID_P8_AMIL_MAMUL = "P8_AMIL_MAMUL"

# P9 — Sentence Geometry
LAYER_ID_P9_SENTENCE_GEOMETRY = "P9_SENTENCE_GEOMETRY"

# P10 — Relation Geometry
LAYER_ID_P10_RELATION_GEOMETRY = "P10_RELATION_GEOMETRY"

# P11 — Irab Geometry
LAYER_ID_P11_IRAB_GEOMETRY = "P11_IRAB_GEOMETRY"

# P12 — Ifadah Speech Force
LAYER_ID_P12_IFADAH_SPEECH_FORCE = "P12_IFADAH_SPEECH_FORCE"

# ─────────────────────────────────────────────────────────────────────────────
# الممنوعات المطلقة — مشتركة بين جميع الطبقات
# ─────────────────────────────────────────────────────────────────────────────

_ABSOLUTE_FORBIDDEN: tuple[str, ...] = (
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
)


# ─────────────────────────────────────────────────────────────────────────────
# الأصول الثلاثة — Origin traceability (REC-2; PROJECT_RECOVERY_CANONICAL_MAP §3)
#
# قانون الإسناد: كل طبقة بلا أصل من هذه الأصول الثلاثة = خارج المشروع أو تجريبية.
# No layer without one of the three origins.
# ─────────────────────────────────────────────────────────────────────────────

# الأصل الأول: صوت بشري عربي محفوظ الأثر (preserved sound trace).
# يخدمه Binary- (BF0) للأثر المكتوب/المرمَّز، ثم AR-P0 مستقبلًا للأصل الصوتي.
ORIGIN_FIRST_PRESERVED_SOUND_TRACE = "الأصل الأول"

# الأصل الثاني: نظام لفظي عربي يحفظ انتقالات الصوت
# (verbal system preserving transitions). يخدمه Saleh- — العمود الفقري الجبري.
ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM = "الأصل الثاني"

# الأصل الثالث: مدلول وضعي — ثبات كيان أو علاقة نُقل إلى لفظ
# (conventional signified). حزمة/مستودع عربي مستقبلي فقط.
ORIGIN_THIRD_CONVENTIONAL_SIGNIFIED = "الأصل الثالث"

# إسناد كل طبقة مسجلة إلى أصلها — REC-2 (§3 registry-binding):
# جميع طبقات SCG-P0…SCG-P12 في هذا السجل تخدم الأصل الثاني
# (Saleh- algebraic spine: qiyas transitions, slot geometry).
LAYER_ORIGIN_NOTES: dict[str, str] = {
    # SCG-P0
    LAYER_ID_P0_UNICODE_CANDIDATE: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P0_TYPED_CODEPOINT: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P0_GLYPH_CLASSIFICATION: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    # SCG-P1
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P1_POSITION_CARRIER: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P1_SLOT_CANDIDATE: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    # SCG-P2 … SCG-P12
    LAYER_ID_P2_REGISTRY_PROJECTION: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P3_ROOT_STEM_CLOSURE: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P4_JAMID_MUSHTAQ: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P7_COMPOSITION_READINESS: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P8_AMIL_MAMUL: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P9_SENTENCE_GEOMETRY: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P10_RELATION_GEOMETRY: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P11_IRAB_GEOMETRY: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
    LAYER_ID_P12_IFADAH_SPEECH_FORCE: ORIGIN_SECOND_VERBAL_TRANSITION_SYSTEM,
}


# ─────────────────────────────────────────────────────────────────────────────
# SCG-P0 — SlotGeometry Core phase 0 (Unicode/TypedCodePoint/Glyph)
# ─────────────────────────────────────────────────────────────────────────────

_P0_UNICODE_CANDIDATE = LayerSpec(
    id=LAYER_ID_P0_UNICODE_CANDIDATE,
    name="UnicodeCandidateLayer",
    phase="SCG-P0",
    origin=OriginSpec(
        layer_id=LAYER_ID_ROOT,
        output_type="RawTextInput",
    ),
    branch=BranchSpec(
        output_type="UnicodeCandidate",
        branch_reason=(
            "تحويل النص الخام إلى مرشحات Unicode مرقمة قابلة للتحقق"
        ),
    ),
    shared_cause="قابلية النص الخام للتمثيل الرقمي عبر Unicode",
    conditions=("raw_input_not_empty",),
    blockers=("encoding_error",),
    invalidating_differences=("non_unicode_encoding",),
    target_boundary_closes=("unicode_candidates",),
    target_boundary_opens=("typed_codepoints",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "LetterIdentityCarrier",
        "SlotCandidate",
        "SlotGeometry",
    ),
    minimum_required_fields=("codepoint_value", "codepoint_position"),
    preserves_ids=("raw_input_identity",),
    allowed_changes=("encode_raw_to_codepoints",),
    forbidden_changes=(
        "assign_letter_identity",
        "assign_haraka_function",
        "assign_meaning",
    ),
    status=LayerStatus.PLANNED,
)

_P0_TYPED_CODEPOINT = LayerSpec(
    id=LAYER_ID_P0_TYPED_CODEPOINT,
    name="TypedCodePointLayer",
    phase="SCG-P0",
    origin=OriginSpec(
        layer_id=LAYER_ID_P0_UNICODE_CANDIDATE,
        output_type="UnicodeCandidate",
    ),
    branch=BranchSpec(
        output_type="TypedCodePoint",
        branch_reason=(
            "تصنيف كل Unicode codepoint إلى نوع مُثبَت: حرف، حركة، حد، علامة"
        ),
    ),
    shared_cause=(
        "قابلية الـ codepoint لحمل نوع واحد من أنواع الرموز العربية المُصنَّفة"
    ),
    conditions=("unicode_candidate_identity_established",),
    blockers=("ambiguous_codepoint_type",),
    invalidating_differences=("type_classification_conflict",),
    target_boundary_closes=("typed_codepoints",),
    target_boundary_opens=(
        "letter_identity_carriers",
        "haraka_function_carriers",
        "conditioned_sequences",
    ),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "LetterIdentityCarrier",
        "HarakaFunctionCarrier",
        "HarakaMarkIdentityCarrier",
        "SlotCandidate",
        "SlotGeometry",
    ),
    minimum_required_fields=(
        "codepoint_value",
        "codepoint_type",
        "unicode_identity_proof",
    ),
    preserves_ids=("unicode_candidate_identity",),
    allowed_changes=("classify_codepoint_type",),
    forbidden_changes=(
        "assign_letter_identity",
        "assign_haraka_function",
        "assign_root",
        "assign_meaning",
    ),
    status=LayerStatus.PLANNED,
)

_P0_GLYPH_CLASSIFICATION = LayerSpec(
    id=LAYER_ID_P0_GLYPH_CLASSIFICATION,
    name="GlyphClassificationLayer",
    phase="SCG-P0",
    origin=OriginSpec(
        layer_id=LAYER_ID_P0_TYPED_CODEPOINT,
        output_type="TypedCodePoint",
    ),
    branch=BranchSpec(
        output_type="GlyphClassificationCandidate",
        branch_reason=(
            "تصنيف الرمز المكتوب إلى مجموعة الرسم: حرف أساسي، زائد، وصل، فصل"
        ),
    ),
    shared_cause=(
        "قابلية الـ TypedCodePoint لحمل صفة الرسم الكتابي ضمن نظام الكتابة العربي"
    ),
    conditions=("typed_codepoint_is_letter_or_mark",),
    blockers=("non_glyph_codepoint",),
    invalidating_differences=("glyph_system_conflict",),
    target_boundary_closes=("glyph_classification_candidates",),
    target_boundary_opens=("letter_identity_carriers",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "LetterIdentityCarrier",
        "SlotCandidate",
        "SlotGeometry",
    ),
    minimum_required_fields=(
        "codepoint_value",
        "glyph_class",
        "script_identity",
    ),
    preserves_ids=("typed_codepoint_identity",),
    allowed_changes=("classify_glyph_class",),
    forbidden_changes=(
        "assign_letter_identity",
        "assign_meaning",
        "assign_root",
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P1 — Dal Alone Atomic
# ─────────────────────────────────────────────────────────────────────────────

_P1_LETTER_IDENTITY_CARRIER = LayerSpec(
    id=LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    name="LetterIdentityCarrierLayer",
    phase="SCG-P1",
    origin=OriginSpec(
        layer_id=LAYER_ID_P0_TYPED_CODEPOINT,
        output_type="TypedCodePoint",
    ),
    branch=BranchSpec(
        output_type="LetterIdentityCarrier",
        branch_reason=(
            "إثبات هوية الحرف ذريًا: unicode + script + letter_class + makhraj + sifat "
            "+ غياب الفارق القادح"
        ),
    ),
    shared_cause=(
        "قابلية الـ TypedCodePoint ذي النوع letter لحمل هوية حرف محدد بمخرجه وصفته"
    ),
    conditions=("codepoint_type_is_letter", "arabic_script_confirmed"),
    blockers=("non_letter_codepoint", "invalidating_difference_present"),
    invalidating_differences=("letter_class_conflict", "makhraj_conflict"),
    target_boundary_closes=("letter_identity_carriers",),
    target_boundary_opens=("slot_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "SlotCandidate",
        "SlotGeometry",
        "HarakaFunctionCarrier",
        "HarakaMarkIdentityCarrier",
        "ConditionedTypedSequence",
    ),
    minimum_required_fields=(
        "unicode_identity",
        "arabic_script_identity",
        "letter_class",
        "letter_name",
    ),
    preserves_ids=("typed_codepoint_identity",),
    allowed_changes=("prove_letter_identity",),
    forbidden_changes=(
        "assign_haraka_function",
        "assign_root",
        "assign_meaning",
        "assign_case",
    ),
    status=LayerStatus.PLANNED,
)

_P1_HARAKA_MARK_IDENTITY_CARRIER = LayerSpec(
    id=LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    name="HarakaMarkIdentityCarrierLayer",
    phase="SCG-P1",
    origin=OriginSpec(
        layer_id=LAYER_ID_P0_TYPED_CODEPOINT,
        output_type="TypedCodePoint",
    ),
    branch=BranchSpec(
        output_type="HarakaMarkIdentityCarrier",
        branch_reason=(
            "إثبات وظيفة الحركة ذريًا: unicode + mark_identity + haraka_class "
            "+ functional_role + غياب الفارق القادح"
        ),
    ),
    shared_cause=(
        "قابلية الـ TypedCodePoint ذي النوع haraka لحمل وظيفة فتح أو ضم أو كسر"
    ),
    conditions=("codepoint_type_is_haraka", "arabic_mark_confirmed"),
    blockers=("non_haraka_codepoint", "invalidating_difference_present"),
    invalidating_differences=("haraka_class_conflict", "functional_role_conflict"),
    target_boundary_closes=("haraka_function_carriers",),
    target_boundary_opens=("slot_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "SlotCandidate",
        "SlotGeometry",
        "LetterIdentityCarrier",
        "ConditionedTypedSequence",
    ),
    minimum_required_fields=(
        "unicode_identity",
        "arabic_mark_identity",
        "haraka_class",
        "functional_role",
    ),
    preserves_ids=("typed_codepoint_identity",),
    allowed_changes=("prove_haraka_function",),
    forbidden_changes=(
        "assign_letter_identity",
        "assign_root",
        "assign_meaning",
        "assign_case",
    ),
    status=LayerStatus.PLANNED,
)

_P1_CONDITIONED_TYPED_SEQUENCE = LayerSpec(
    id=LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    name="ConditionedTypedSequenceLayer",
    phase="SCG-P1",
    origin=OriginSpec(
        layer_id=LAYER_ID_P0_TYPED_CODEPOINT,
        output_type="TypedCodePoint",
    ),
    branch=BranchSpec(
        output_type="ConditionedTypedSequence",
        branch_reason=(
            "إثبات تهيئة تسلسل الرموز: حامل الحركة، موضع التنوين، حجب الحرف اليتيم، "
            "حفظ البقايا، إثبات الحدود"
        ),
    ),
    shared_cause=(
        "قابلية تسلسل TypedCodePoints للتحقق من صحة الترتيب والربط بين الرموز"
    ),
    conditions=("typed_codepoint_sequence_not_empty",),
    blockers=("sequence_ordering_violation",),
    invalidating_differences=("carrier_binding_conflict",),
    target_boundary_closes=("conditioned_typed_sequences",),
    target_boundary_opens=("alignment_evidence", "carrier_binding_candidates"),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "LetterIdentityCarrier",
        "HarakaFunctionCarrier",
        "HarakaMarkIdentityCarrier",
        "SlotCandidate",
        "SlotGeometry",
    ),
    minimum_required_fields=(
        "sequence_items",
        "position_evidence",
        "residual_preservation_evidence",
    ),
    preserves_ids=("typed_codepoint_sequence_identity",),
    allowed_changes=(
        "prove_carrier_binding",
        "prove_boundary_positions",
        "register_orphan_residuals",
    ),
    forbidden_changes=(
        "assign_letter_identity",
        "assign_haraka_function",
        "assign_root",
        "assign_meaning",
    ),
    status=LayerStatus.PLANNED,
)

_P1_POSITION_CARRIER = LayerSpec(
    id=LAYER_ID_P1_POSITION_CARRIER,
    name="PositionCarrierLayer",
    phase="SCG-P1",
    origin=OriginSpec(
        layer_id=LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
        output_type="ConditionedTypedSequence",
    ),
    branch=BranchSpec(
        output_type="PositionCarrier",
        branch_reason=(
            "إثبات موضع الرمز في التسلسل المُهيَّأ: ابتداء، وسط، نهاية، منفرد"
        ),
    ),
    shared_cause=(
        "قابلية الرمز في تسلسل مُهيَّأ لحمل موضع محدد"
    ),
    conditions=("conditioned_sequence_established",),
    blockers=("position_ambiguity",),
    invalidating_differences=("position_conflict",),
    target_boundary_closes=("position_carriers",),
    target_boundary_opens=("slot_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "SlotCandidate",
        "SlotGeometry",
        "LetterIdentityCarrier",
        "HarakaFunctionCarrier",
        "HarakaMarkIdentityCarrier",
    ),
    minimum_required_fields=(
        "position_index",
        "position_class",
        "sequence_context",
    ),
    preserves_ids=("conditioned_sequence_identity",),
    allowed_changes=("prove_position_in_sequence",),
    forbidden_changes=(
        "assign_letter_identity",
        "assign_haraka_function",
        "assign_root",
        "assign_meaning",
    ),
    status=LayerStatus.PLANNED,
)

_P1_SLOT_CANDIDATE = LayerSpec(
    id=LAYER_ID_P1_SLOT_CANDIDATE,
    name="SlotCandidateLayer",
    phase="SCG-P1",
    origin=OriginSpec(
        layer_id=LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
        output_type="LetterIdentityCarrier",
    ),
    branch=BranchSpec(
        output_type="SlotCandidate",
        branch_reason=(
            "دمج LetterIdentityCarrier + HarakaMarkIdentityCarrier + PositionCarrier "
            "+ AlignmentEvidence في مرشح خانة مرخّص"
        ),
    ),
    shared_cause=(
        "اجتماع الهوية الحرفية والوظيفة الحركية والموضع والدليل التهيئي لتكوين "
        "إمكان الخانة"
    ),
    conditions=(
        "letter_identity_carrier_present",
        "haraka_function_carrier_present",
        "position_carrier_present",
        "alignment_evidence_present",
    ),
    blockers=("missing_any_required_ingredient", "invalidating_difference_present"),
    invalidating_differences=("ingredient_identity_conflict",),
    target_boundary_closes=("slot_candidates",),
    target_boundary_opens=("slot_geometry",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "SlotGeometry",
        "ConditionedTypedSequence",
    ),
    minimum_required_fields=(
        "letter_identity_ref",
        "haraka_function_ref",
        "position_ref",
        "alignment_evidence_ref",
        "slot_rank",
        "slot_residuals",
    ),
    preserves_ids=(
        "letter_identity_carrier_identity",
        "haraka_function_carrier_identity",
    ),
    allowed_changes=("compose_slot_from_ingredients",),
    forbidden_changes=(
        "assign_root",
        "assign_meaning",
        "assign_case",
        "assign_irab",
    ),
    allowed_previous_layer_ids=(
        LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
        LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
        LAYER_ID_P1_POSITION_CARRIER,
        LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P3_ROOT_STEM_CLOSURE,
        LAYER_ID_P4_JAMID_MUSHTAQ,
        LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P2 — Registry Projection
# ─────────────────────────────────────────────────────────────────────────────

_P2_REGISTRY_PROJECTION = LayerSpec(
    id=LAYER_ID_P2_REGISTRY_PROJECTION,
    name="RegistryProjectionLayer",
    phase="SCG-P2",
    origin=OriginSpec(
        layer_id=LAYER_ID_P1_SLOT_CANDIDATE,
        output_type="SlotCandidate",
    ),
    branch=BranchSpec(
        output_type="RegistryProjectionCandidate",
        branch_reason=(
            "إسقاط مرشح الخانة على سجل المرحلة المعنية لفتح إمكانات صرفية "
            "أو نحوية محتملة"
        ),
    ),
    shared_cause=(
        "قابلية مرشح الخانة للإسقاط على سجل ترخيص لفتح Prior لا Judgment"
    ),
    conditions=("slot_candidate_is_licensed",),
    blockers=("slot_candidate_blocked",),
    invalidating_differences=("registry_membership_conflict",),
    target_boundary_closes=("registry_projection_candidates",),
    target_boundary_opens=(
        "root_stem_candidates",
        "word_type_priors",
    ),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards.
        "RootCandidate",
        "WordTypeJudgment",
        "CaseEffect",
        "IrabCandidate",
        # Exact downstream canonical output types P2 must NOT produce (no-jump;
        # SCG-P2 spec-authoring authorization 2026-06-15). P2 may only OPEN
        # these as priors via target_boundary_opens, never emit them.
        "RootStemCandidate",       # SCG-P3
        "JamidMushtaqCandidate",   # SCG-P4
        "MufradWordCandidate",     # SCG-P5
        "VerbalSignifiedCandidate",  # SCG-P6
        "CompositionReadinessCandidate",  # SCG-P7
        "AmilMamulCandidate",      # SCG-P8
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "slot_candidate_ref",
        "registry_entry_ref",
        "membership_prior_type",
    ),
    preserves_ids=("slot_candidate_identity",),
    allowed_changes=("project_slot_to_registry_prior",),
    forbidden_changes=(
        "assign_root",
        "assign_meaning",
        "assign_irab",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P3 — Root Stem Closure
# ─────────────────────────────────────────────────────────────────────────────

_P3_ROOT_STEM_CLOSURE = LayerSpec(
    id=LAYER_ID_P3_ROOT_STEM_CLOSURE,
    name="RootStemClosureLayer",
    phase="SCG-P3",
    origin=OriginSpec(
        layer_id=LAYER_ID_P2_REGISTRY_PROJECTION,
        output_type="RegistryProjectionCandidate",
    ),
    branch=BranchSpec(
        output_type="RootStemCandidate",
        branch_reason=(
            "إغلاق إمكان الجذر والساق من مرشح خانات متتالية عبر دليل تهيئة التسلسل"
        ),
    ),
    shared_cause=(
        "قابلية تسلسل مرشحات الخانات لتكوين إمكان جذر أو ساق مرخّص"
    ),
    conditions=(
        "registry_projection_established",
        "slot_sequence_consistent",
    ),
    blockers=("root_pattern_blocked",),
    invalidating_differences=("root_pattern_conflict",),
    target_boundary_closes=("root_stem_candidates",),
    target_boundary_opens=(
        "jamid_mushtaq_candidates",
        "word_pattern_candidates",
    ),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards.
        "WordTypeJudgment",
        "MeaningCandidate",
        "CaseEffect",
        "IrabCandidate",
        # Exact downstream canonical output types P3 must NOT produce (no-jump;
        # SCG-P3 spec-authoring authorization 2026-06-15). P3 may only OPEN
        # jamid/mushtaq + word-pattern priors via target_boundary_opens, never
        # emit any downstream candidate.
        "JamidMushtaqCandidate",   # SCG-P4
        "MufradWordCandidate",     # SCG-P5
        "VerbalSignifiedCandidate",  # SCG-P6
        "CompositionReadinessCandidate",  # SCG-P7
        "AmilMamulCandidate",      # SCG-P8
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "slot_sequence_refs",
        "root_pattern_evidence",
        "stem_boundary_evidence",
    ),
    preserves_ids=("slot_candidate_identities",),
    allowed_changes=("compose_root_stem_from_slots",),
    forbidden_changes=(
        "assign_meaning",
        "assign_irab",
        "assign_case",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P4 — Jamid Mushtaq
# ─────────────────────────────────────────────────────────────────────────────

_P4_JAMID_MUSHTAQ = LayerSpec(
    id=LAYER_ID_P4_JAMID_MUSHTAQ,
    name="JamidMushtaqLayer",
    phase="SCG-P4",
    origin=OriginSpec(
        layer_id=LAYER_ID_P3_ROOT_STEM_CLOSURE,
        output_type="RootStemCandidate",
    ),
    branch=BranchSpec(
        output_type="JamidMushtaqCandidate",
        branch_reason=(
            "تصنيف الجذر إلى جامد أو مشتق كإمكان لا حكم نهائي"
        ),
    ),
    shared_cause=(
        "قابلية إمكان الجذر للتصنيف إلى جامد أو مشتق بناءً على دليل النمط"
    ),
    conditions=("root_stem_candidate_established",),
    blockers=("derivation_pattern_blocked",),
    invalidating_differences=("derivation_classification_conflict",),
    target_boundary_closes=("jamid_mushtaq_candidates",),
    target_boundary_opens=("word_type_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards.
        "WordTypeJudgment",
        "MeaningCandidate",
        "IrabCandidate",
        # Exact downstream canonical output types P4 must NOT produce (no-jump;
        # SCG-P4 spec-authoring authorization 2026-06-16). P4 may only OPEN
        # word-type candidates as priors via target_boundary_opens, never emit
        # any downstream candidate.
        "MufradWordCandidate",     # SCG-P5
        "VerbalSignifiedCandidate",  # SCG-P6
        "CompositionReadinessCandidate",  # SCG-P7
        "AmilMamulCandidate",      # SCG-P8
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "root_stem_ref",
        "derivation_class_evidence",
        "pattern_evidence",
    ),
    preserves_ids=("root_stem_candidate_identity",),
    allowed_changes=("classify_jamid_or_mushtaq",),
    forbidden_changes=(
        "assign_meaning",
        "assign_irab",
        "assign_case",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P5 — Mufrad Word Contracts
# ─────────────────────────────────────────────────────────────────────────────

_P5_MUFRAD_WORD_CONTRACTS = LayerSpec(
    id=LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
    name="MufradWordContractsLayer",
    phase="SCG-P5",
    origin=OriginSpec(
        layer_id=LAYER_ID_P4_JAMID_MUSHTAQ,
        output_type="JamidMushtaqCandidate",
    ),
    branch=BranchSpec(
        output_type="MufradWordCandidate",
        branch_reason=(
            "إنشاء إمكان الكلمة المفردة كعقد اكتمال أدنى: اسم، فعل، حرف"
        ),
    ),
    shared_cause=(
        "قابلية إمكان الجامد/المشتق للانضمام إلى عقد كلمة مفردة محددة النوع"
    ),
    conditions=(
        "jamid_mushtaq_established",
        "word_boundary_closed",
    ),
    blockers=("word_type_ambiguity_blocking",),
    invalidating_differences=("word_class_conflict",),
    target_boundary_closes=("mufrad_word_candidates",),
    target_boundary_opens=(
        "verbal_signified_candidates",
        "composition_readiness_candidates",
    ),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards.
        "IrabCandidate",
        "CaseEffect",
        "SentenceCandidate",
        # Exact downstream canonical output types P5 must NOT produce (no-jump;
        # SCG-P5 spec-authoring authorization 2026-06-16). P5 may only OPEN
        # verbal-signified / composition-readiness priors via
        # target_boundary_opens, never emit any downstream candidate.
        "VerbalSignifiedCandidate",  # SCG-P6
        "CompositionReadinessCandidate",  # SCG-P7
        "AmilMamulCandidate",      # SCG-P8
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "root_stem_ref",
        "word_class_evidence",
        "word_boundary_evidence",
    ),
    preserves_ids=("jamid_mushtaq_candidate_identity",),
    allowed_changes=("compose_mufrad_word",),
    forbidden_changes=(
        "assign_irab",
        "assign_case",
        "assign_meaning",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P6 — Verbal Signified Alone
# ─────────────────────────────────────────────────────────────────────────────

_P6_VERBAL_SIGNIFIED_ALONE = LayerSpec(
    id=LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
    name="VerbalSignifiedAloneLayer",
    phase="SCG-P6",
    origin=OriginSpec(
        layer_id=LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
        output_type="MufradWordCandidate",
    ),
    branch=BranchSpec(
        output_type="VerbalSignifiedCandidate",
        branch_reason=(
            "استخراج المدلول اللفظي وحده كإمكان، منفصلًا عن المعنى المعجمي "
            "والحكم النحوي"
        ),
    ),
    shared_cause=(
        "قابلية إمكان الكلمة المفردة لحمل مدلول لفظي يُفيد إمكان المعنى دون إغلاقه"
    ),
    conditions=("mufrad_word_established",),
    blockers=("verbal_signified_ambiguity_blocking",),
    invalidating_differences=("signified_class_conflict",),
    target_boundary_closes=("verbal_signified_candidates",),
    target_boundary_opens=("composition_readiness_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards — "signified" must never close into meaning.
        "IrabCandidate",
        "CaseEffect",
        "SentenceCandidate",
        "MeaningJudgment",
        # Exact downstream canonical output types P6 must NOT produce (no-jump;
        # SCG-P6 spec-authoring authorization 2026-06-16). P6 may only OPEN
        # composition-readiness priors via target_boundary_opens, never emit
        # any downstream candidate.
        "CompositionReadinessCandidate",  # SCG-P7
        "AmilMamulCandidate",      # SCG-P8
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "mufrad_word_ref",
        "signified_class_evidence",
        "verbal_identity_evidence",
    ),
    preserves_ids=("mufrad_word_candidate_identity",),
    allowed_changes=("extract_verbal_signified",),
    forbidden_changes=(
        "assign_meaning",
        "assign_irab",
        "assign_case",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P7 — Composition Readiness
# ─────────────────────────────────────────────────────────────────────────────

_P7_COMPOSITION_READINESS = LayerSpec(
    id=LAYER_ID_P7_COMPOSITION_READINESS,
    name="CompositionReadinessLayer",
    phase="SCG-P7",
    origin=OriginSpec(
        layer_id=LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
        output_type="VerbalSignifiedCandidate",
    ),
    branch=BranchSpec(
        output_type="CompositionReadinessCandidate",
        branch_reason=(
            "التحقق من أن الوحدات اللفظية تستوفي شروط الدخول في تركيب: "
            "بنية ظاهرة، إسناد ممكن، حدود مغلقة"
        ),
    ),
    shared_cause=(
        "قابلية المدلول اللفظي للانضمام في تركيب نحوي عبر بوابة الاستعداد"
    ),
    conditions=(
        "verbal_signified_established",
        "composition_boundary_closed",
    ),
    blockers=("composition_precondition_blocked",),
    invalidating_differences=("composition_readiness_conflict",),
    target_boundary_closes=("composition_readiness_candidates",),
    target_boundary_opens=("amil_mamul_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards — readiness, not composition itself.
        "IrabCandidate",
        "CaseEffect",
        "SentenceCandidate",
        # Exact downstream canonical output types P7 must NOT produce (no-jump;
        # SCG-P7 spec-authoring authorization 2026-06-16). P7 may only OPEN
        # amil/mamul priors via target_boundary_opens, never emit any downstream
        # candidate.
        "AmilMamulCandidate",      # SCG-P8
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "verbal_signified_refs",
        "composition_boundary_evidence",
        "isnad_readiness_evidence",
    ),
    preserves_ids=("verbal_signified_candidate_identities",),
    allowed_changes=("verify_composition_preconditions",),
    forbidden_changes=(
        "assign_irab",
        "assign_case",
        "assign_meaning",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P8 — Amil Mamul
# ─────────────────────────────────────────────────────────────────────────────

_P8_AMIL_MAMUL = LayerSpec(
    id=LAYER_ID_P8_AMIL_MAMUL,
    name="AmilMamulLayer",
    phase="SCG-P8",
    origin=OriginSpec(
        layer_id=LAYER_ID_P7_COMPOSITION_READINESS,
        output_type="CompositionReadinessCandidate",
    ),
    branch=BranchSpec(
        output_type="AmilMamulCandidate",
        branch_reason=(
            "إثبات علاقة العامل بمعموله كإمكان: إسناد، تقييد، توكيد — "
            "دون إعطاء الحكم النهائي"
        ),
    ),
    shared_cause=(
        "قابلية وحدتين مستعدتين للتركيب لتكوين علاقة عامل-معمول مرخّصة"
    ),
    conditions=(
        "composition_readiness_established",
        "amil_identified",
        "mamul_identified",
    ),
    blockers=("amil_mamul_relation_blocked",),
    invalidating_differences=("amil_class_conflict",),
    target_boundary_closes=("amil_mamul_candidates",),
    target_boundary_opens=("sentence_geometry_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards — relation proven, case never judged.
        "IrabCandidate",
        "CaseJudgment",
        "SentenceCandidate",
        # Exact downstream canonical output types P8 must NOT produce (no-jump;
        # SCG-P8 spec-authoring authorization 2026-06-16). P8 may only OPEN
        # sentence-geometry priors via target_boundary_opens, never emit any
        # downstream candidate.
        "SentenceGeometryCandidate",  # SCG-P9
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
        "IfadahCandidate",         # SCG-P12
    ),
    minimum_required_fields=(
        "amil_ref",
        "mamul_ref",
        "relation_class_evidence",
        "domain_evidence",
    ),
    preserves_ids=("composition_readiness_identities",),
    allowed_changes=("prove_amil_mamul_relation",),
    forbidden_changes=(
        "assign_irab",
        "assign_case",
        "assign_sentence_type",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P9 — Sentence Geometry
# ─────────────────────────────────────────────────────────────────────────────

_P9_SENTENCE_GEOMETRY = LayerSpec(
    id=LAYER_ID_P9_SENTENCE_GEOMETRY,
    name="SentenceGeometryLayer",
    phase="SCG-P9",
    origin=OriginSpec(
        layer_id=LAYER_ID_P8_AMIL_MAMUL,
        output_type="AmilMamulCandidate",
    ),
    branch=BranchSpec(
        output_type="SentenceGeometryCandidate",
        branch_reason=(
            "بناء الهندسة الجملية كتنظيم فضائي للعلاقات: إسناد، نعت، حال، "
            "معطوف، مفعولية"
        ),
    ),
    shared_cause=(
        "قابلية علاقات العامل-المعمول للتنظيم الهندسي ضمن بنية الجملة"
    ),
    conditions=(
        "amil_mamul_candidates_ready",
        "sentence_boundary_closed",
    ),
    blockers=("sentence_structure_blocked",),
    invalidating_differences=("sentence_type_conflict",),
    target_boundary_closes=("sentence_geometry_candidates",),
    target_boundary_opens=("relation_geometry_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards — geometry, not i'rab/case/ifadah judgment.
        "IrabCandidate",
        "CaseJudgment",
        "IfadahCandidate",         # SCG-P12 (also a local guard)
        # Exact downstream canonical output types P9 must NOT produce (no-jump;
        # SCG-P9 spec-authoring authorization 2026-06-16). P9 may only OPEN
        # relation-geometry priors via target_boundary_opens, never emit any
        # downstream candidate.
        "RelationGeometryCandidate",  # SCG-P10
        "IrabGeometryCandidate",   # SCG-P11
    ),
    minimum_required_fields=(
        "amil_mamul_refs",
        "sentence_type_evidence",
        "isnad_boundary_evidence",
    ),
    preserves_ids=("amil_mamul_candidate_identities",),
    allowed_changes=("compose_sentence_geometry",),
    forbidden_changes=(
        "assign_irab",
        "assign_case",
        "assign_ifadah",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P10 — Relation Geometry
# ─────────────────────────────────────────────────────────────────────────────

_P10_RELATION_GEOMETRY = LayerSpec(
    id=LAYER_ID_P10_RELATION_GEOMETRY,
    name="RelationGeometryLayer",
    phase="SCG-P10",
    origin=OriginSpec(
        layer_id=LAYER_ID_P9_SENTENCE_GEOMETRY,
        output_type="SentenceGeometryCandidate",
    ),
    branch=BranchSpec(
        output_type="RelationGeometryCandidate",
        branch_reason=(
            "هندسة العلاقات الداخلية بين مكونات الجملة: تبعية، عطف، إبدال، توكيد"
        ),
    ),
    shared_cause=(
        "قابلية الهندسة الجملية لتحديد علاقات المكونات داخل الجملة هندسيًا"
    ),
    conditions=(
        "sentence_geometry_established",
        "relation_scope_closed",
    ),
    blockers=("relation_structure_blocked",),
    invalidating_differences=("relation_type_conflict",),
    target_boundary_closes=("relation_geometry_candidates",),
    target_boundary_opens=("irab_geometry_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        # Local no-overreach guards — relations mapped, i'rab never judged.
        "IrabCandidate",
        "CaseJudgment",
        "IfadahCandidate",         # SCG-P12 (also a local guard)
        # Exact downstream canonical output type P10 must NOT produce (no-jump;
        # SCG-P10 spec-authoring authorization 2026-06-16). P10 may only OPEN
        # irab-geometry priors via target_boundary_opens, never emit them.
        "IrabGeometryCandidate",   # SCG-P11
    ),
    minimum_required_fields=(
        "sentence_geometry_ref",
        "relation_type_evidence",
        "dependency_scope_evidence",
    ),
    preserves_ids=("sentence_geometry_identity",),
    allowed_changes=("map_internal_relations",),
    forbidden_changes=(
        "assign_irab",
        "assign_case",
        "assign_ifadah",
    ),
    forbidden_direct_next_layer_ids=(
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P11 — Irab Geometry
# ─────────────────────────────────────────────────────────────────────────────

_P11_IRAB_GEOMETRY = LayerSpec(
    id=LAYER_ID_P11_IRAB_GEOMETRY,
    name="IrabGeometryLayer",
    phase="SCG-P11",
    origin=OriginSpec(
        layer_id=LAYER_ID_P10_RELATION_GEOMETRY,
        output_type="RelationGeometryCandidate",
    ),
    branch=BranchSpec(
        output_type="IrabGeometryCandidate",
        branch_reason=(
            "رسم هندسة الإعراب: تعيين المواضع الإعرابية وإمكاناتها كمرشحات "
            "لا أحكام"
        ),
    ),
    shared_cause=(
        "قابلية هندسة العلاقات لحمل إمكانات الإعراب بناءً على العامل والمحل "
        "والعلامة"
    ),
    conditions=(
        "relation_geometry_established",
        "irab_context_closed",
    ),
    blockers=("irab_context_blocked",),
    invalidating_differences=("irab_position_conflict",),
    target_boundary_closes=("irab_geometry_candidates",),
    target_boundary_opens=("ifadah_speech_force_candidates",),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "CaseJudgment",
        "IfadahCandidate",
        "IrabFinalDecision",
    ),
    minimum_required_fields=(
        "relation_geometry_ref",
        "irab_position_evidence",
        "case_marker_evidence",
        "waqf_readiness_evidence",
    ),
    preserves_ids=("relation_geometry_identity",),
    allowed_changes=("map_irab_positions",),
    forbidden_changes=(
        "assign_case_judgment",
        "assign_ifadah",
        "assign_hukm",
    ),
    forbidden_direct_next_layer_ids=(),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# P12 — Ifadah Speech Force
# ─────────────────────────────────────────────────────────────────────────────

_P12_IFADAH_SPEECH_FORCE = LayerSpec(
    id=LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    name="IfadahSpeechForceLayer",
    phase="SCG-P12",
    origin=OriginSpec(
        layer_id=LAYER_ID_P11_IRAB_GEOMETRY,
        output_type="IrabGeometryCandidate",
    ),
    branch=BranchSpec(
        output_type="IfadahCandidate",
        branch_reason=(
            "بناء إمكان الإفادة الكلامية كمرشح قوة كلامية: خبر، إنشاء، طلب — "
            "لا حكم نهائي ولا ادعاء واقع"
        ),
    ),
    shared_cause=(
        "قابلية هندسة الإعراب المُغلَقة لحمل قوة كلامية محتملة تُفيد المخاطب"
    ),
    conditions=(
        "irab_geometry_established",
        "ifadah_context_closed",
    ),
    blockers=("ifadah_precondition_blocked",),
    invalidating_differences=("speech_force_conflict",),
    target_boundary_closes=("ifadah_candidates",),
    target_boundary_opens=(),
    forbidden_outputs=_ABSOLUTE_FORBIDDEN + (
        "IrabFinalDecision",
        "RealityMapping",
        "TruthJudgment",
    ),
    minimum_required_fields=(
        "irab_geometry_ref",
        "speech_force_evidence",
        "ifadah_boundary_evidence",
        "mukhatab_context_evidence",
    ),
    preserves_ids=("irab_geometry_identity",),
    allowed_changes=("compose_ifadah_candidate",),
    forbidden_changes=(
        "assign_reality_claim",
        "assign_truth_value",
        "assign_hukm",
    ),
    forbidden_direct_next_layer_ids=(),
    status=LayerStatus.PLANNED,
)


# ─────────────────────────────────────────────────────────────────────────────
# الدالة الرئيسية — بناء السجل
# ─────────────────────────────────────────────────────────────────────────────

def build_master_registry_seed() -> MasterLayerRegistry:
    """
    بناء سجل الطبقات الرئيسي مع بذرة المراحل P0-P12.

    كل طبقة مسجلة بحالة PLANNED.
    لا runtime، لا Arabic-specific logic.

    الترتيب إلزامي: كل طبقة يجب تسجيل أصلها أولًا.

    Returns:
        MasterLayerRegistry مع 15 طبقة مخططة.
    """
    registry = MasterLayerRegistry()

    # P0 — Binary Foundation (الأصل هو ROOT)
    registry.register(_P0_UNICODE_CANDIDATE)
    registry.register(_P0_TYPED_CODEPOINT)
    registry.register(_P0_GLYPH_CLASSIFICATION)

    # P1 — Dal Alone Atomic
    registry.register(_P1_LETTER_IDENTITY_CARRIER)
    registry.register(_P1_HARAKA_MARK_IDENTITY_CARRIER)
    registry.register(_P1_CONDITIONED_TYPED_SEQUENCE)
    registry.register(_P1_POSITION_CARRIER)
    registry.register(_P1_SLOT_CANDIDATE)

    # P2 — Registry Projection
    registry.register(_P2_REGISTRY_PROJECTION)

    # P3 — Root Stem Closure
    registry.register(_P3_ROOT_STEM_CLOSURE)

    # P4 — Jamid Mushtaq
    registry.register(_P4_JAMID_MUSHTAQ)

    # P5 — Mufrad Word Contracts
    registry.register(_P5_MUFRAD_WORD_CONTRACTS)

    # P6 — Verbal Signified Alone
    registry.register(_P6_VERBAL_SIGNIFIED_ALONE)

    # P7 — Composition Readiness
    registry.register(_P7_COMPOSITION_READINESS)

    # P8 — Amil Mamul
    registry.register(_P8_AMIL_MAMUL)

    # P9 — Sentence Geometry
    registry.register(_P9_SENTENCE_GEOMETRY)

    # P10 — Relation Geometry
    registry.register(_P10_RELATION_GEOMETRY)

    # P11 — Irab Geometry
    registry.register(_P11_IRAB_GEOMETRY)

    # P12 — Ifadah Speech Force
    registry.register(_P12_IFADAH_SPEECH_FORCE)

    return registry


# ─────────────────────────────────────────────────────────────────────────────
# P0 Implementation Registration — PR-CORE-2
# ─────────────────────────────────────────────────────────────────────────────

# الطبقات الكانونيكية لـ P0 مُنفَّذة بالفعل في:
#   src/qiyas_core/unicode_adapter.py          → UnicodeCandidate
#   src/qiyas_core/typed_codepoint_adapter.py  → TypedCodePoint
#   src/qiyas_core/registries/glyph_classification_registry.py → GlyphClassification
#   src/qiyas_core/letter_coordinate_adapter.py  (GlyphClassificationGate)
#
# هذه الدالة تُسجّل تلك الحالة رسميًا في السجل:
#   PLANNED → SPECIFIED → IMPLEMENTED
#
# القانون:
#   لا يجوز تجاوز SPECIFIED مباشرةً إلى IMPLEMENTED.
#   كل انتقال يمر عبر update_status مع التحقق من التسلسل المنطقي.

_P0_LAYER_IDS: tuple[str, ...] = (
    LAYER_ID_P0_UNICODE_CANDIDATE,
    LAYER_ID_P0_TYPED_CODEPOINT,
    LAYER_ID_P0_GLYPH_CLASSIFICATION,
)

# توثيق الملفات المصدرية لكل طبقة P0
_P0_IMPLEMENTATION_SOURCES: dict[str, str] = {
    LAYER_ID_P0_UNICODE_CANDIDATE: "src/qiyas_core/unicode_adapter.py",
    LAYER_ID_P0_TYPED_CODEPOINT: "src/qiyas_core/typed_codepoint_adapter.py",
    LAYER_ID_P0_GLYPH_CLASSIFICATION: (
        "src/qiyas_core/registries/glyph_classification_registry.py"
    ),
}


def build_p0_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم طبقات P0 إلى حالة IMPLEMENTED.

    PR-CORE-2: تسجيل حالة التنفيذ الفعلي لطبقات P0 الكانونيكية.

    الانتقال: PLANNED → SPECIFIED → IMPLEMENTED
    مُنفَّذ في ملفات مصدرية كانونيكية موجودة بالفعل.

    الطبقات المُنفَّذة:
        P0_UNICODE_CANDIDATE     → src/qiyas_core/unicode_adapter.py
        P0_TYPED_CODEPOINT       → src/qiyas_core/typed_codepoint_adapter.py
        P0_GLYPH_CLASSIFICATION  → src/qiyas_core/registries/glyph_classification_registry.py

    الطبقات غير المُنفَّذة (تبقى PLANNED):
        P1-P12 — لم تُنفَّذ بعد، تبقى PLANNED.

    Returns:
        MasterLayerRegistry مع P0 بحالة IMPLEMENTED وبقية الطبقات PLANNED.
    """
    registry = build_master_registry_seed()

    for layer_id in _P0_LAYER_IDS:
        # PLANNED → SPECIFIED
        registry.update_status(layer_id, LayerStatus.SPECIFIED)
        # SPECIFIED → IMPLEMENTED
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)

    return registry


# ─────────────────────────────────────────────────────────────────────────────
# P1 Specification Registration — PR-CORE-3
# ─────────────────────────────────────────────────────────────────────────────

# معرفات طبقات P1
_P1_LAYER_IDS: tuple[str, ...] = (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)


def build_p1_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم طبقات P1 إلى حالة SPECIFIED.

    PR-CORE-3: تعريف مواصفات P1 فقط — لا runtime، لا تنفيذ.

    الانتقال: PLANNED → SPECIFIED فقط.
    SPECIFIED تعني: المواصفة موثقة وقابلة للاختبار، لكن Runtime لم يُكتب بعد.

    الطبقات المُحدَّدة (SPECIFIED):
        P1_LETTER_IDENTITY_CARRIER     — إثبات هوية الحرف ذريًا
        P1_HARAKA_MARK_IDENTITY_CARRIER — إثبات وظيفة الحركة ذريًا
        P1_CONDITIONED_TYPED_SEQUENCE  — إثبات تهيئة التسلسل
        P1_POSITION_CARRIER            — إثبات الموضع في التسلسل
        P1_SLOT_CANDIDATE              — دمج المكونات الأربعة في مرشح خانة

    الطبقات غير المُحدَّدة (تبقى PLANNED):
        P2-P12 — لم تُحدَّد بعد، تبقى PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ LetterIdentityCarrier runtime.
        هذه الدالة لا تُنفِّذ HarakaMarkIdentityCarrier runtime.
        هذه الدالة لا تُنفِّذ ConditionedTypedSequence runtime.
        هذه الدالة لا تُنفِّذ PositionCarrier runtime.
        هذه الدالة لا تُنفِّذ SlotCandidate runtime.
        هذه الدالة لا تُنفِّذ SlotGeometry.
        هذه الدالة لا تُقدِّم P2-P12.
        هذه الدالة لا تحذف أي forbidden_outputs.
        هذه الدالة لا تنتج معنى نهائيًا أو حكمًا.

    Returns:
        MasterLayerRegistry مع P0 بحالة IMPLEMENTED وP1 بحالة SPECIFIED
        وبقية الطبقات P2-P12 بحالة PLANNED.
    """
    registry = build_p0_implemented_registry()

    for layer_id in _P1_LAYER_IDS:
        # PLANNED → SPECIFIED (تحديد المواصفة فقط — لا تنفيذ)
        registry.update_status(layer_id, LayerStatus.SPECIFIED)

    return registry


# معرفات الطبقتين الذريتين في SCG-P1 (atomic carriers — PR-1)
_P1_ATOMIC_CARRIER_IDS: tuple[str, ...] = (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
)


def build_p1_atomic_carriers_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم الطبقتين الذريتين فقط في SCG-P1 إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P1 PR-1 (atomic carriers, 2026-06-17): يُقدِّم
    **فقط** LetterIdentityCarrier و HarakaMarkIdentityCarrier من SPECIFIED إلى
    IMPLEMENTED عبر بوابة تبعية التنفيذ (كلاهما CROSS من P0 المُنفَّذة بالكامل).

    الاستراتيجية: certify-and-wire لـ Letter كما هي؛ Haraka runtime يُصدر الاسم
    الكانوني HarakaMarkIdentityCarrier (HarakaFunctionCarrier يبقى alias انتقالي).

    تبني على build_p12_specified_registry (P0 IMPLEMENTED، P1-P12 SPECIFIED —
    سلسلة المواصفات مكتملة) وتُقدِّم الطبقتين الذريتين فقط؛ تبقى
    ConditionedTypedSequence و PositionCarrier و SlotCandidate بحالة SPECIFIED،
    وتبقى P2-P12 بحالة SPECIFIED.

    Non-Goals (PR-1):
        لا تُقدِّم ConditionedTypedSequence ولا PositionCarrier ولا SlotCandidate.
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P2-P12 (تبقى SPECIFIED، لا IMPLEMENTED).
        لا تحذف أي forbidden_outputs ولا تُغيّر بيانات البذرة (seed).
        لا تنتج SlotGeometry ولا معنى ولا حكمًا.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED؛ LetterIdentityCarrier +
        HarakaMarkIdentityCarrier IMPLEMENTED؛ بقية P1 (CTS، Position، Slot)
        SPECIFIED؛ P2-P12 SPECIFIED. العدد يبقى 19.
    """
    registry = build_p12_specified_registry()
    for layer_id in _P1_ATOMIC_CARRIER_IDS:
        # SPECIFIED → IMPLEMENTED (الطبقتان الذريتان فقط — بوابة التبعية: CROSS من P0)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرفات طبقتي التسلسل/الموضع في SCG-P1 (sequence + position — PR-2)
# الترتيب مهم: CTS أولًا (CROSS من P0)، ثم Position (INTRA من CTS) — بوابة التبعية.
_P1_SEQUENCE_POSITION_IDS: tuple[str, ...] = (
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
)


def build_p1_sequence_position_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم ConditionedTypedSequence ثم PositionCarrier إلى IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P1 PR-2 (sequence + position, 2026-06-17): يُقدِّم
    **فقط** ConditionedTypedSequence و PositionCarrier من SPECIFIED إلى
    IMPLEMENTED، فوق الطبقتين الذريتين المُنفَّذتين (PR-1).

    الترتيب يحترم بوابة التبعية الهجينة:
      - ConditionedTypedSequence: CROSS من P0 المُنفَّذة → يجوز التقدم.
      - PositionCarrier: INTRA من ConditionedTypedSequence → بعد تنفيذ CTS فقط.

    القرارات (PR-2):
      - CTS = اسم نطاق/طبقة + مطابقة عائلة الأدلة (CarrierBindingCandidate،
        PositionEvidence، BoundaryEvidence، ResidualPreservationEvidence) —
        لا container جديد، لا تغيير output_type، لا تغيير schema.
      - PositionCarrier يستهلك PositionEvidence من CTS ويحفظ
        conditioned_sequence_identity كهوية كانونية (codepoint = trace/bridge فقط).

    Non-Goals (PR-2):
        لا تُنفِّذ SlotCandidate (تبقى SPECIFIED).
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P2-P12 (تبقى SPECIFIED).
        لا تُغيّر بيانات البذرة (seed) ولا schema.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED؛ Letter + Haraka + CTS + Position
        IMPLEMENTED؛ SlotCandidate SPECIFIED؛ P2-P12 SPECIFIED. العدد يبقى 19.
    """
    registry = build_p1_atomic_carriers_implemented_registry()
    for layer_id in _P1_SEQUENCE_POSITION_IDS:
        # SPECIFIED → IMPLEMENTED بالترتيب: CTS (CROSS) ثم Position (INTRA من CTS)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرّف طبقة الخانة في SCG-P1 (SlotCandidate convergence — PR-3)
_P1_SLOT_IDS: tuple[str, ...] = (LAYER_ID_P1_SLOT_CANDIDATE,)


def build_p1_slot_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SlotCandidate (نقطة الاجتماع) إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P1 PR-3 (SlotCandidate convergence, 2026-06-17): يُقدِّم
    **فقط** P1_SLOT_CANDIDATE من SPECIFIED إلى IMPLEMENTED، فوق الطبقات الأربع
    المُنفَّذة (PR-1 + PR-2). بهذا تكتمل المرحلة P1 بأكملها (الطبقات الخمس
    IMPLEMENTED).

    SlotCandidate = اجتماع مرخّص للمكوّنات الأربعة:
        LetterIdentityCarrier ⊗ HarakaMarkIdentityCarrier ⊗ PositionCarrier
        ⊗ AlignmentEvidence (CarrierBindingCandidate من CTS).
    بوابة التبعية تتحقق من أصل الخانة المُعلَن (LetterIdentityCarrier) فقط؛
    اشتراط المكوّنات الأربعة مفروض عبر الاختبارات (slot_adapter = CERTIFY_AS_IS).

    الاستراتيجية: certify-and-wire لـ slot_adapter كما هو (يُنتج SlotCandidate
    فعليًا في خط الأنابيب بالفعل) — التغيير هنا تسجيلي فقط (status) + اختبارات.

    Non-Goals (PR-3):
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P2-P12 (تبقى SPECIFIED).
        لا تنتج SlotGeometry ولا تدخل P2/RegistryProjection.
        لا تُغيّر بيانات البذرة (seed) ولا schema.
        لا معنى/جذر/وزن/كلمة/حكم/إعراب/دلالة.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED؛ الطبقات الخمس في P1 IMPLEMENTED؛
        P2-P12 SPECIFIED. العدد يبقى 19.
    """
    registry = build_p1_sequence_position_implemented_registry()
    for layer_id in _P1_SLOT_IDS:
        # SPECIFIED → IMPLEMENTED — SlotCandidate وحدها (بوابة التبعية: أصلها
        # LetterIdentityCarrier مُنفَّذ؛ المكوّنات الأربعة مُنفَّذة).
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرّف طبقة الإسقاط في SCG-P2 (RegistryProjection)
_P2_PROJECTION_IDS: tuple[str, ...] = (LAYER_ID_P2_REGISTRY_PROJECTION,)


def build_p2_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P2 (RegistryProjection) إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P2 فقط (2026-06-18): يُقدِّم **فقط**
    P2_REGISTRY_PROJECTION من SPECIFIED إلى IMPLEMENTED، فوق مرحلة P1 المكتملة
    التنفيذ (الطبقات الخمس). بوابة التبعية تتحقق: أصل P2 هو SlotCandidate (CROSS
    من مرحلة P1 المُنفَّذة بالكامل) → التقدم مرخّص.

    P2 = إسقاط هندسة الـ Slots على أصناف عضوية بنيوية مسجّلة (registry membership
    classes) — لا جذر، لا وزن، لا كلمة، لا معنى. candidate-only؛ يفتح
    root/stem + word-type **priors** فقط؛ لا يُنتج RootStemCandidate.

    Non-Goals (P2):
        لا تُنفِّذ P3 (RootStemCandidate تبقى SPECIFIED).
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P3-P12 (تبقى SPECIFIED).
        لا تُغيّر بيانات البذرة (seed) ولا schema.
        لا جذر/وزن/صرف/كلمة/معنى/حكم/إعراب/دلالة.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED؛ P1 (الخمس) IMPLEMENTED؛
        P2_REGISTRY_PROJECTION IMPLEMENTED؛ P3-P12 SPECIFIED. العدد يبقى 19.
    """
    registry = build_p1_slot_implemented_registry()
    for layer_id in _P2_PROJECTION_IDS:
        # SPECIFIED → IMPLEMENTED — P2 وحدها (CROSS من مرحلة P1 المُنفَّذة)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرّف طبقة إغلاق الجذر/الساق في SCG-P3 (RootStemClosure)
_P3_ROOT_STEM_IDS: tuple[str, ...] = (LAYER_ID_P3_ROOT_STEM_CLOSURE,)


def build_p3_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P3 (RootStemClosure) إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P3 فقط (2026-06-18): يُقدِّم **فقط**
    P3_ROOT_STEM_CLOSURE من SPECIFIED إلى IMPLEMENTED، فوق P2 المُنفَّذة. بوابة
    التبعية تتحقق: أصل P3 هو RegistryProjectionCandidate (CROSS من مرحلة P2
    المُنفَّذة بالكامل) → التقدم مرخّص.

    P3 = إغلاق **إمكان** جذر/ساق بنيوي من إسقاط هندسة الـ Slots — candidate-only.
    ليس استخراج جذر نهائي، ليس وزنًا، ليس صرفًا، ليس كلمة، ليس معنى. يفتح
    jamid/mushtaq + word-pattern **priors** فقط؛ لا يُنتج JamidMushtaqCandidate.

    Non-Goals (P3):
        لا تُنفِّذ P4 (JamidMushtaqCandidate تبقى SPECIFIED).
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P4-P12 (تبقى SPECIFIED).
        لا تُغيّر بيانات البذرة (seed) ولا schema.
        لا جذر نهائي/وزن/صرف/كلمة/معنى/حكم/إعراب/دلالة.

    Returns:
        MasterLayerRegistry مع P0/P1/P2 IMPLEMENTED؛ P3_ROOT_STEM_CLOSURE
        IMPLEMENTED؛ P4-P12 SPECIFIED. العدد يبقى 19.
    """
    registry = build_p2_implemented_registry()
    for layer_id in _P3_ROOT_STEM_IDS:
        # SPECIFIED → IMPLEMENTED — P3 وحدها (CROSS من مرحلة P2 المُنفَّذة)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرّف طبقة جامد/مشتق في SCG-P4 (JamidMushtaq)
_P4_JAMID_MUSHTAQ_IDS: tuple[str, ...] = (LAYER_ID_P4_JAMID_MUSHTAQ,)


def build_p4_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P4 (JamidMushtaq) إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P4 فقط (2026-06-18): يُقدِّم **فقط**
    P4_JAMID_MUSHTAQ من SPECIFIED إلى IMPLEMENTED، فوق P3 المُنفَّذة. بوابة
    التبعية تتحقق: أصل P4 هو RootStemCandidate (CROSS من مرحلة P3 المُنفَّذة
    بالكامل) → التقدم مرخّص.

    P4 = فتح **إمكان** تصنيف جامد/مشتق بنيوي من إمكان الجذر/الساق —
    candidate-only. ليس حكمًا نهائيًا بأن الكلمة جامدة أو مشتقة، ليس وزنًا، ليس
    صرفًا، ليس كلمة، ليس معنى. يفتح word-type **priors** فقط؛ لا يُنتج
    MufradWordCandidate.

    Non-Goals (P4):
        لا تُنفِّذ P5 (MufradWordCandidate تبقى SPECIFIED).
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P5-P12 (تبقى SPECIFIED).
        لا تُغيّر بيانات البذرة (seed) ولا schema.
        لا حكم جامد/مشتق نهائي/وزن/صرف/كلمة/معنى/حكم/إعراب/دلالة.

    Returns:
        MasterLayerRegistry مع P0/P1/P2/P3 IMPLEMENTED؛ P4_JAMID_MUSHTAQ
        IMPLEMENTED؛ P5-P12 SPECIFIED. العدد يبقى 19.
    """
    registry = build_p3_implemented_registry()
    for layer_id in _P4_JAMID_MUSHTAQ_IDS:
        # SPECIFIED → IMPLEMENTED — P4 وحدها (CROSS من مرحلة P3 المُنفَّذة)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرّف طبقة الكلمة المفردة في SCG-P5 (MufradWord)
_P5_MUFRAD_WORD_IDS: tuple[str, ...] = (LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,)


def build_p5_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P5 (MufradWord) إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P5 فقط (2026-06-18): يُقدِّم **فقط**
    P5_MUFRAD_WORD_CONTRACTS من SPECIFIED إلى IMPLEMENTED، فوق P4 المُنفَّذة.
    بوابة التبعية تتحقق: أصل P5 هو JamidMushtaqCandidate (CROSS من مرحلة P4
    المُنفَّذة بالكامل) → التقدم مرخّص.

    P5 = طبقة **إمكان** الكلمة المفردة (candidate-only). ليست كلمة معجمية نهائية،
    ليست مدخل قاموس، ليست صرفًا ولا نحوًا ولا معنى. تفتح verbal_signified +
    phrase-level **priors** فقط؛ لا تُنتج VerbalSignifiedCandidate.

    Non-Goals (P5):
        لا تُنفِّذ P6 (VerbalSignifiedCandidate تبقى SPECIFIED).
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P6-P12 (تبقى SPECIFIED).
        لا تُغيّر بيانات البذرة (seed) ولا schema.

    Returns:
        MasterLayerRegistry مع P0-P4 IMPLEMENTED؛ P5 IMPLEMENTED؛ P6-P12
        SPECIFIED. العدد يبقى 19.
    """
    registry = build_p4_implemented_registry()
    for layer_id in _P5_MUFRAD_WORD_IDS:
        # SPECIFIED → IMPLEMENTED — P5 وحدها (CROSS من مرحلة P4 المُنفَّذة)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


# معرّف طبقة المدلول اللفظي في SCG-P6 (VerbalSignified)
_P6_VERBAL_SIGNIFIED_IDS: tuple[str, ...] = (LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,)


def build_p6_implemented_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P6 (VerbalSignified) إلى حالة IMPLEMENTED.

    تفويض ضيق لتنفيذ SCG-P6 فقط (2026-06-18): يُقدِّم **فقط**
    P6_VERBAL_SIGNIFIED_ALONE من SPECIFIED إلى IMPLEMENTED، فوق P5 المُنفَّذة.
    بوابة التبعية تتحقق: أصل P6 هو MufradWordCandidate (CROSS من مرحلة P5
    المُنفَّذة بالكامل) → التقدم مرخّص.

    P6 = طبقة **فتح** الإمكانات الدلالية اللفظية (candidate-only). تفتح
    أوّليات المعنى والدلالة (priors) فقط؛ لا تُنتج معنىً ولا دلالةً ولا تفسيرًا
    ولا حكمًا ولا واقعًا ولا معنى نهائيًا (المخرجات الممنوعة محصورة في
    forbidden_outputs لطبقة P6).

    Non-Goals (P6):
        لا تُنفِّذ P7 (CompositionReadinessCandidate تبقى SPECIFIED).
        ليست build_p1_implemented_registry الكاملة.
        لا تُنفِّذ P7-P12 (تبقى SPECIFIED).
        لا تُغيّر بيانات البذرة (seed) ولا schema.

    Returns:
        MasterLayerRegistry مع P0-P5 IMPLEMENTED؛ P6 IMPLEMENTED؛ P7-P12
        SPECIFIED. العدد يبقى 19.
    """
    registry = build_p5_implemented_registry()
    for layer_id in _P6_VERBAL_SIGNIFIED_IDS:
        # SPECIFIED → IMPLEMENTED — P6 وحدها (CROSS من مرحلة P5 المُنفَّذة)
        registry.update_status(layer_id, LayerStatus.IMPLEMENTED)
    return registry


def build_p2_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P2 (RegistryProjection) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P2 فقط (2026-06-15): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا adapter. الانتقال: PLANNED → SPECIFIED فقط.

    SPECIFIED تعني: المواصفة موثقة وقابلة للاختبار، لكن Runtime لم يُكتب بعد.
    تبني على build_p1_specified_registry (P0 IMPLEMENTED، P1 SPECIFIED) وتُقدِّم
    P2 وحدها إلى SPECIFIED؛ تبقى P3-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ RegistryProjectionCandidate runtime.
        هذه الدالة لا تُقدِّم P3-P12.
        هذه الدالة لا تنتج RootStemCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج معنى أو جذرًا أو وزنًا أو كلمة أو إعرابًا أو حكمًا.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1 SPECIFIED، P2 SPECIFIED،
        وبقية الطبقات P3-P12 بحالة PLANNED.
    """
    registry = build_p1_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P2 وحدها (تأليف مواصفة فقط — لا تنفيذ)
    registry.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.SPECIFIED)
    return registry


def build_p3_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P3 (RootStemClosure) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P3 فقط (2026-06-15): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا adapter، ولا استخراج جذر. الانتقال:
    PLANNED → SPECIFIED فقط.

    SPECIFIED تعني: المواصفة موثقة وقابلة للاختبار، لكن Runtime لم يُكتب بعد.
    تبني على build_p2_specified_registry (P0 IMPLEMENTED، P1+P2 SPECIFIED)
    وتُقدِّم P3 وحدها إلى SPECIFIED؛ تبقى P4-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ RootStemCandidate runtime.
        هذه الدالة لا تستخرج جذرًا ولا تُسند وزنًا ولا تُصنِّف كلمة.
        هذه الدالة لا تُقدِّم P4-P12.
        هذه الدالة لا تنتج JamidMushtaqCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج معنى أو إعرابًا أو حكمًا.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1+P2+P3 SPECIFIED،
        وبقية الطبقات P4-P12 بحالة PLANNED.
    """
    registry = build_p2_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P3 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا استخراج)
    registry.update_status(LAYER_ID_P3_ROOT_STEM_CLOSURE, LayerStatus.SPECIFIED)
    return registry


def build_p4_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P4 (JamidMushtaq) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P4 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا adapter، لا استخراج جذر، لا إسناد وزن. الانتقال:
    PLANNED → SPECIFIED فقط.

    تبني على build_p3_specified_registry (P0 IMPLEMENTED، P1+P2+P3 SPECIFIED)
    وتُقدِّم P4 وحدها إلى SPECIFIED؛ تبقى P5-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ JamidMushtaqCandidate runtime.
        هذه الدالة لا تستخرج جذرًا ولا تُسند وزنًا ولا تُصنِّف معنى.
        هذه الدالة لا تُقدِّم P5-P12.
        هذه الدالة لا تنتج MufradWordCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج معنى أو إعرابًا أو حكمًا.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P4 SPECIFIED،
        وبقية الطبقات P5-P12 بحالة PLANNED.
    """
    registry = build_p3_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P4 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا استخراج)
    registry.update_status(LAYER_ID_P4_JAMID_MUSHTAQ, LayerStatus.SPECIFIED)
    return registry


def build_p5_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P5 (MufradWordContracts) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P5 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا ادعاء وجود كلمة معجمية، لا معنى. الانتقال:
    PLANNED → SPECIFIED فقط.

    تبني على build_p4_specified_registry وتُقدِّم P5 وحدها إلى SPECIFIED؛
    تبقى P6-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ MufradWordCandidate runtime.
        هذه الدالة لا تدّعي معنى الكلمة ولا حدودها النهائية المعجمية.
        هذه الدالة لا تُقدِّم P6-P12.
        هذه الدالة لا تنتج VerbalSignifiedCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج إعرابًا أو حكمًا.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P5 SPECIFIED،
        وبقية الطبقات P6-P12 بحالة PLANNED.
    """
    registry = build_p4_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P5 وحدها (تأليف مواصفة فقط — لا تنفيذ)
    registry.update_status(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS, LayerStatus.SPECIFIED)
    return registry


def build_p6_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P6 (VerbalSignifiedAlone) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P6 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا دلالة معجمية، لا معنى نهائي. الانتقال:
    PLANNED → SPECIFIED فقط.

    المدلول اللفظي هنا إمكان بنيوي وحده — لا يُغلق المعنى ولا يدّعيه.
    تبني على build_p5_specified_registry وتُقدِّم P6 وحدها إلى SPECIFIED؛
    تبقى P7-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ VerbalSignifiedCandidate runtime.
        هذه الدالة لا تُغلق المعنى المعجمي ولا تنتج MeaningJudgment.
        هذه الدالة لا تُقدِّم P7-P12.
        هذه الدالة لا تنتج CompositionReadinessCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج إعرابًا أو حكمًا.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P6 SPECIFIED،
        وبقية الطبقات P7-P12 بحالة PLANNED.
    """
    registry = build_p5_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P6 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا دلالة)
    registry.update_status(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE, LayerStatus.SPECIFIED)
    return registry


def build_p7_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P7 (CompositionReadiness) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P7 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا تركيب فعلي، لا إسناد محقَّق. الانتقال:
    PLANNED → SPECIFIED فقط.

    P7 تُثبت استعداد التركيب فقط (بوابة شروط)، لا التركيب نفسه.
    تبني على build_p6_specified_registry وتُقدِّم P7 وحدها إلى SPECIFIED؛
    تبقى P8-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ CompositionReadinessCandidate runtime.
        هذه الدالة لا تُكوِّن علاقة عامل-معمول ولا إسنادًا محقَّقًا.
        هذه الدالة لا تُقدِّم P8-P12.
        هذه الدالة لا تنتج AmilMamulCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج إعرابًا أو حكمًا.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P7 SPECIFIED،
        وبقية الطبقات P8-P12 بحالة PLANNED.
    """
    registry = build_p6_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P7 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا تركيب)
    registry.update_status(LAYER_ID_P7_COMPOSITION_READINESS, LayerStatus.SPECIFIED)
    return registry


def build_p8_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P8 (AmilMamul) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P8 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا adapter، لا إعراب فعلي، لا إسناد حكم نهائي.
    الانتقال: PLANNED → SPECIFIED فقط.

    P8 تُثبت علاقة عامل-معمول كإمكان فقط، لا تُسند حالة إعرابية ولا حكمًا.
    تبني على build_p7_specified_registry وتُقدِّم P8 وحدها إلى SPECIFIED؛
    تبقى P9-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ AmilMamulCandidate runtime.
        هذه الدالة لا تُسند إعرابًا ولا حالة (case) ولا نوع جملة.
        هذه الدالة لا تُقدِّم P9-P12.
        هذه الدالة لا تنتج SentenceGeometryCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج حكمًا أو ادعاء واقع.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P8 SPECIFIED،
        وبقية الطبقات P9-P12 بحالة PLANNED.
    """
    registry = build_p7_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P8 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا إعراب)
    registry.update_status(LAYER_ID_P8_AMIL_MAMUL, LayerStatus.SPECIFIED)
    return registry


def build_p9_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P9 (SentenceGeometry) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P9 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا إعراب فعلي، لا إفادة محقَّقة. الانتقال:
    PLANNED → SPECIFIED فقط.

    P9 تُنظِّم العلاقات هندسيًا في بنية جملة كإمكان، لا تُسند إعرابًا ولا إفادة.
    تبني على build_p8_specified_registry وتُقدِّم P9 وحدها إلى SPECIFIED؛
    تبقى P10-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ SentenceGeometryCandidate runtime.
        هذه الدالة لا تُسند إعرابًا ولا حالة ولا إفادة.
        هذه الدالة لا تُقدِّم P10-P12.
        هذه الدالة لا تنتج RelationGeometryCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج حكمًا أو ادعاء واقع.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P9 SPECIFIED،
        وبقية الطبقات P10-P12 بحالة PLANNED.
    """
    registry = build_p8_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P9 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا إعراب)
    registry.update_status(LAYER_ID_P9_SENTENCE_GEOMETRY, LayerStatus.SPECIFIED)
    return registry


def build_p10_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P10 (RelationGeometry) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P10 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، لا إعراب فعلي. الانتقال: PLANNED → SPECIFIED فقط.

    P10 تَرسم العلاقات الداخلية بين مكونات الجملة هندسيًا كإمكان، لا حكمًا
    نحويًا نهائيًا ولا إعرابًا. تبني على build_p9_specified_registry وتُقدِّم
    P10 وحدها إلى SPECIFIED؛ تبقى P11-P12 بحالة PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ RelationGeometryCandidate runtime.
        هذه الدالة لا تُسند إعرابًا ولا حالة ولا إفادة.
        هذه الدالة لا تُقدِّم P11-P12.
        هذه الدالة لا تنتج IrabGeometryCandidate أو أي مخرج لاحق.
        هذه الدالة لا تنتج حكمًا أو ادعاء واقع.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P10 SPECIFIED،
        وبقية الطبقات P11-P12 بحالة PLANNED.
    """
    registry = build_p9_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P10 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا إعراب)
    registry.update_status(LAYER_ID_P10_RELATION_GEOMETRY, LayerStatus.SPECIFIED)
    return registry


def build_p11_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P11 (IrabGeometry) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P11 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، **لا حكم إعرابي فعلي**، لا قرار إعراب نهائي.
    الانتقال: PLANNED → SPECIFIED فقط.

    P11 تَرسم *هندسة* الإعراب: مواضع الإعراب وإمكاناتها كمرشحات لا أحكام.
    إنها أخطر طبقة من حيث القرب من الحكم؛ forbidden_changes تمنع
    assign_case_judgment / assign_ifadah / assign_hukm. تبني على
    build_p10_specified_registry وتُقدِّم P11 وحدها إلى SPECIFIED؛ تبقى P12 PLANNED.

    Non-Goals:
        هذه الدالة لا تُنفِّذ IrabGeometryCandidate runtime.
        هذه الدالة لا تُصدر حكمًا إعرابيًا ولا قرار إعراب نهائيًا (IrabFinalDecision).
        هذه الدالة لا تُسند حالة (case) ولا إفادة ولا حكمًا.
        هذه الدالة لا تُقدِّم P12.
        هذه الدالة لا تنتج IfadahCandidate أو أي مخرج لاحق.
        هذه الدالة لا تحذف أي forbidden_outputs.

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P11 SPECIFIED، وP12 PLANNED.
    """
    registry = build_p10_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P11 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا حكم إعراب)
    registry.update_status(LAYER_ID_P11_IRAB_GEOMETRY, LayerStatus.SPECIFIED)
    return registry


def build_p12_specified_registry() -> MasterLayerRegistry:
    """
    بناء السجل مع تقدم SCG-P12 (IfadahSpeechForce) إلى حالة SPECIFIED.

    تفويض ضيق لتأليف مواصفة SCG-P12 فقط (2026-06-16): تعريف المواصفة —
    لا runtime، لا تنفيذ، **لا ادعاء واقع، لا قيمة صدق، لا حكم نهائي**.
    الانتقال: PLANNED → SPECIFIED فقط.

    P12 تَبني إمكان الإفادة الكلامية (قوة كلامية: خبر/إنشاء/طلب) كمرشح فقط —
    لا حكم ولا ادعاء واقع. إنها الطبقة الختامية للسلسلة الكانونيكية؛
    forbidden_changes تمنع assign_reality_claim / assign_truth_value / assign_hukm.
    تبني على build_p11_specified_registry وتُقدِّم P12 وحدها إلى SPECIFIED.
    بهذا تكتمل مواصفة P0-P12 (P0 IMPLEMENTED، P1-P12 SPECIFIED).

    Non-Goals:
        هذه الدالة لا تُنفِّذ IfadahCandidate runtime.
        هذه الدالة لا تدّعي واقعًا ولا تَرسم واقعًا ولا قيمة صدق ولا حكمًا
        (المخرجات الممنوعة محصورة في forbidden_outputs لطبقة P12).
        هذه الدالة لا تنتج معنى نهائيًا.
        هذه الدالة لا تحذف أي forbidden_outputs.
        هذه الدالة لا تُنشئ طبقة بعد P12 (لا يوجد target_boundary_opens).

    Returns:
        MasterLayerRegistry مع P0 IMPLEMENTED، P1-P12 SPECIFIED (السلسلة مكتملة
        المواصفة)؛ لا طبقة بحالة IMPLEMENTED بعد P0 (الـ freeze ساري).
    """
    registry = build_p11_specified_registry()
    # PLANNED → SPECIFIED لـ SCG-P12 وحدها (تأليف مواصفة فقط — لا تنفيذ، لا حكم/واقع)
    registry.update_status(LAYER_ID_P12_IFADAH_SPEECH_FORCE, LayerStatus.SPECIFIED)
    return registry


# ─────────────────────────────────────────────────────────────────────────────
# القانون الختامي
# ─────────────────────────────────────────────────────────────────────────────
# غير مسموح بتنفيذ أي طبقة خارج هذا السجل.
# غير مسموح بفتح PR يُضيف طبقة غير موجودة هنا.
# الحالة PLANNED تعني: مخطط — لم يُنفَّذ — لا تنفيذ بلا سجل.
