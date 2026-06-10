"""
master_registry_seed.py — بذرة سجل الطبقات الرئيسي

PR-CORE-1: تسجيل المراحل P0-P12 كـ LayerSpecs مخططة فقط.

القانون:
    كل مرحلة هي LayerSpec بحالة PLANNED.
    لا runtime جديد هنا.
    لا منطق خاص بالعربية أو Unicode.
    هذا السجل يمنع PRs المتفرقة من الظهور خارج خريطة المشروع.

الوظيفة:
    build_master_registry_seed() → MasterLayerRegistry
    تُرجع سجلًا يحتوي كل المراحل الـ 13 بحالة PLANNED.

المراحل:
    P0  — Binary Foundation (الأساس الثنائي)
    P1  — Dal Alone Atomic (الدال وحده ذريًا)
    P2  — Registry Projection (إسقاط السجل)
    P3  — Root Stem Closure (إغلاق الجذر والساق)
    P4  — Jamid Mushtaq (الجامد والمشتق)
    P5  — Mufrad Word Contracts (عقود الكلمة المفردة)
    P6  — Verbal Signified Alone (المدلول الفعلي وحده)
    P7  — Composition Readiness (استعداد التركيب)
    P8  — Amil Mamul (العامل والمعمول)
    P9  — Sentence Geometry (هندسة الجملة)
    P10 — Relation Geometry (هندسة العلاقة)
    P11 — Irab Geometry (هندسة الإعراب)
    P12 — Ifadah Speech Force (قوة الإفادة الكلامية)

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
LAYER_ID_P1_HARAKA_FUNCTION_CARRIER = "P1_HARAKA_FUNCTION_CARRIER"
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
# P0 — Binary Foundation
# ─────────────────────────────────────────────────────────────────────────────

_P0_UNICODE_CANDIDATE = LayerSpec(
    id=LAYER_ID_P0_UNICODE_CANDIDATE,
    name="UnicodeCandidateLayer",
    phase="P0_BINARY_FOUNDATION",
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
    phase="P0_BINARY_FOUNDATION",
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
    phase="P0_BINARY_FOUNDATION",
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
    phase="P1_DAL_ALONE_ATOMIC",
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

_P1_HARAKA_FUNCTION_CARRIER = LayerSpec(
    id=LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
    name="HarakaFunctionCarrierLayer",
    phase="P1_DAL_ALONE_ATOMIC",
    origin=OriginSpec(
        layer_id=LAYER_ID_P0_TYPED_CODEPOINT,
        output_type="TypedCodePoint",
    ),
    branch=BranchSpec(
        output_type="HarakaFunctionCarrier",
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
    phase="P1_DAL_ALONE_ATOMIC",
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
    phase="P1_DAL_ALONE_ATOMIC",
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
    phase="P1_DAL_ALONE_ATOMIC",
    origin=OriginSpec(
        layer_id=LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
        output_type="LetterIdentityCarrier",
    ),
    branch=BranchSpec(
        output_type="SlotCandidate",
        branch_reason=(
            "دمج LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier "
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
        LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
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
    phase="P2_REGISTRY_PROJECTION",
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
        "RootCandidate",
        "WordTypeJudgment",
        "CaseEffect",
        "IrabCandidate",
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
    phase="P3_ROOT_STEM_CLOSURE",
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
        "WordTypeJudgment",
        "MeaningCandidate",
        "CaseEffect",
        "IrabCandidate",
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
    phase="P4_JAMID_MUSHTAQ",
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
        "WordTypeJudgment",
        "MeaningCandidate",
        "IrabCandidate",
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
    phase="P5_MUFRAD_WORD_CONTRACTS",
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
        "IrabCandidate",
        "CaseEffect",
        "SentenceCandidate",
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
    phase="P6_VERBAL_SIGNIFIED_ALONE",
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
        "IrabCandidate",
        "CaseEffect",
        "SentenceCandidate",
        "MeaningJudgment",
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
    phase="P7_COMPOSITION_READINESS",
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
        "IrabCandidate",
        "CaseEffect",
        "SentenceCandidate",
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
    phase="P8_AMIL_MAMUL",
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
        "IrabCandidate",
        "CaseJudgment",
        "SentenceCandidate",
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
    phase="P9_SENTENCE_GEOMETRY",
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
        "IrabCandidate",
        "CaseJudgment",
        "IfadahCandidate",
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
    phase="P10_RELATION_GEOMETRY",
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
        "IrabCandidate",
        "CaseJudgment",
        "IfadahCandidate",
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
    phase="P11_IRAB_GEOMETRY",
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
    phase="P12_IFADAH_SPEECH_FORCE",
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
    registry.register(_P1_HARAKA_FUNCTION_CARRIER)
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
# القانون الختامي
# ─────────────────────────────────────────────────────────────────────────────
# غير مسموح بتنفيذ أي طبقة خارج هذا السجل.
# غير مسموح بفتح PR يُضيف طبقة غير موجودة هنا.
# الحالة PLANNED تعني: مخطط — لم يُنفَّذ — لا تنفيذ بلا سجل.
