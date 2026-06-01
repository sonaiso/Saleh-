"""
Letter Identity Rules

Constitutional rules for proving atomic letter identities (BAA, TAA, SEEN, etc.)
from LetterCodePoint. This is an independent atomic path that does NOT require
sequence context or ConditionedTypedSequence.

Architecture:
    TypedCodePoint (if LetterCodePoint)
      ↓
    LetterIdentityCarrier(BAA | TAA | SEEN | ...)

Forbidden: This layer does NOT produce SlotCandidate or require sequence validation.
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule


ALL_WADI = (
    WadiGate.SABAB,
    WadiGate.SHART,
    WadiGate.MANI,
    WadiGate.SIHHA,
    WadiGate.FASAD,
    WadiGate.BUTLAN,
)


# Forbidden outputs: LetterIdentityCarrier is atomic, not compositional
FORBIDDEN_LETTER_IDENTITY_OUTPUTS = (
    "SlotCandidate",
    "SlotGeometry",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "FormCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
)


# BAA Identity Rule (ب)
BAA_LETTER_IDENTITY = QiyasRule(
    rule_id="letter_identity.baa",
    layer="LetterIdentityQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicLetterIdentitySpace",
    far_type="LetterCodePoint",
    required_effective_wasf=(
        "has_baa_unicode_identity",      # U+0628
        "has_baa_script_identity",        # ARABIC_LETTER_BAA
    ),
    required_illah=(
        "has_baa_sound_identity",         # VOICED_BILABIAL_STOP
        "has_baa_makhraj_sifat",          # BILABIAL + VOICED + STOP
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "baa_vs_meem_nasality",           # BAA is not MEEM (nasality)
        "baa_vs_faa_place",               # BAA is not FAA (place)
        "baa_vs_taa_voicing",             # BAA is not TAA (voicing)
    ),
    neutral_identity_domain="phonetic_identity",
    output_candidate_type="LetterIdentityCarrier",
    forbidden_outputs=FORBIDDEN_LETTER_IDENTITY_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
)


# TAA Identity Rule (ت)
TAA_LETTER_IDENTITY = QiyasRule(
    rule_id="letter_identity.taa",
    layer="LetterIdentityQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicLetterIdentitySpace",
    far_type="LetterCodePoint",
    required_effective_wasf=(
        "has_taa_unicode_identity",       # U+062A
        "has_taa_script_identity",        # ARABIC_LETTER_TAA
    ),
    required_illah=(
        "has_taa_sound_identity",         # VOICELESS_ALVEOLAR_STOP
        "has_taa_makhraj_sifat",          # ALVEOLAR + VOICELESS + STOP
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "taa_vs_baa_voicing",             # TAA is not BAA (voiceless)
        "taa_vs_daal_voicing",            # TAA is not DAAL (voiceless)
        "taa_vs_thaa_manner",             # TAA is not THAA (stop vs fricative)
    ),
    neutral_identity_domain="phonetic_identity",
    output_candidate_type="LetterIdentityCarrier",
    forbidden_outputs=FORBIDDEN_LETTER_IDENTITY_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
)


# SEEN Identity Rule (س)
SEEN_LETTER_IDENTITY = QiyasRule(
    rule_id="letter_identity.seen",
    layer="LetterIdentityQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicLetterIdentitySpace",
    far_type="LetterCodePoint",
    required_effective_wasf=(
        "has_seen_unicode_identity",      # U+0633
        "has_seen_script_identity",       # ARABIC_LETTER_SEEN
    ),
    required_illah=(
        "has_seen_sound_identity",        # VOICELESS_ALVEOLAR_FRICATIVE
        "has_seen_makhraj_sifat",         # ALVEOLAR + VOICELESS + FRICATIVE
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "seen_vs_sheen_voicing",          # SEEN is not SHEEN (voiceless)
        "seen_vs_saad_emphasis",          # SEEN is not SAAD (plain vs emphatic)
        "seen_vs_thaa_place",             # SEEN is not THAA (alveolar vs dental)
    ),
    neutral_identity_domain="phonetic_identity",
    output_candidate_type="LetterIdentityCarrier",
    forbidden_outputs=FORBIDDEN_LETTER_IDENTITY_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
)


# KAF Identity Rule (ك)
KAF_LETTER_IDENTITY = QiyasRule(
    rule_id="letter_identity.kaf",
    layer="LetterIdentityQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicLetterIdentitySpace",
    far_type="LetterCodePoint",
    required_effective_wasf=(
        "has_kaf_unicode_identity",       # U+0643
        "has_kaf_script_identity",        # ARABIC_LETTER_KAF
    ),
    required_illah=(
        "has_kaf_sound_identity",         # VOICELESS_VELAR_STOP
        "has_kaf_makhraj_sifat",          # VELAR + VOICELESS + STOP
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "kaf_vs_qaf_place",               # KAF is not QAF (velar vs uvular)
        "kaf_vs_gayn_voicing",            # KAF is not GAYN (voiceless)
        "kaf_vs_jiim_manner",             # KAF is not JIIM (stop vs affricate)
    ),
    neutral_identity_domain="phonetic_identity",
    output_candidate_type="LetterIdentityCarrier",
    forbidden_outputs=FORBIDDEN_LETTER_IDENTITY_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
)
