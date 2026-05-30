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
