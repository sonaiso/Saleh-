from enum import Enum


class QiyasPattern(Enum):
    MEMBERSHIP = "membership"
    PATTERN_FIT = "pattern_fit"
    TRANSFORMATION = "transformation"
    CAPABILITY = "capability"
    COMPOSITION_FIT = "composition_fit"
    ANALOGY = "analogy"


class WadiGate(Enum):
    SABAB = "sabab"
    SHART = "shart"
    MANI = "mani"
    SIHHA = "sihha"
    FASAD = "fasad"
    BUTLAN = "butlan"


class CandidateStatus(Enum):
    ACCEPTED = "accepted"
    DEFERRED = "deferred"
    BLOCKED = "blocked"


class EvidenceRank(Enum):
    ZERO = 0
    FORM = 1
    QIYAS = 2
    SAMA = 3
    AHAD = 4
    TAWATUR = 5


class ResidualSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKER = "blocker"


class ResidualEffect(Enum):
    NONE = "none"
    DEFER = "defer"
    BLOCK = "block"


class DiacriticKind(Enum):
    """Classification of Arabic diacritical marks by linguistic function."""
    CORE_HARAKA = "core_haraka"  # Short vowels and tanwin (064B-064D, 064E-0650)
    SHADDA = "shadda"  # Gemination/consonant doubling (0651)
    SUKUN = "sukun"  # Vowel absence marker (0652)
    ADDITIONAL = "additional"  # Maddah, hamza variants, etc. (0653-065F)


class CarrierFunction(Enum):
    """Classification of carrier letter phonotactic function."""
    ARABIC_CONSONANT_CARRIER = "arabic_consonant_carrier"
    WEAK_LETTER_CARRIER = "weak_letter_carrier"
    LONG_VOWEL_LETTER = "long_vowel_letter"
    HAMZA_CARRIER = "hamza_carrier"
    NON_CARRIER = "non_carrier"
    UNKNOWN_CARRIER_FUNCTION = "unknown_carrier_function"


class MarkFunction(Enum):
    """Classification of diacritic mark phonotactic function."""
    SHORT_VOWEL_MARK = "short_vowel_mark"
    TANWIN_MARK = "tanwin_mark"
    SUKUN_MARK = "sukun_mark"
    SHADDA_MARK = "shadda_mark"
    ADDITIONAL_DIACRITIC_MARK = "additional_diacritic_mark"
    UNKNOWN_MARK_FUNCTION = "unknown_mark_function"


class ClosureReadiness(Enum):
    """Classification of syllable closure readiness."""
    MABNI_CLOSURE_READY = "mabni_closure_ready"
    MURAB_CLOSURE_DEFERRED = "murab_closure_deferred"
    PAUSE_CLOSURE_READY = "pause_closure_ready"
    CONTINUATION_CLOSURE_DEFERRED = "continuation_closure_deferred"
    UNKNOWN_CLOSURE = "unknown_closure"
