"""
Phonetic grounding profiles for Arabic letters and harakat.

MakhrajGeometry: articulation place (bilabial, dental, alveolar, palatal,
                 velar, uvular, pharyngeal, glottal).
SifatGeometry:   phonetic features (voicing, manner, airflow, duration,
                 emphasis).
PhoneticGroundingProfile: binds a letter codepoint to its full phonetic
                          identity + invalidating_differences.
VocalicEnergyProfile:     binds a haraka codepoint to its vocalic function
                          (duration, aperture, tongue position).
"""

from dataclasses import dataclass, field
from typing import FrozenSet


# ---------------------------------------------------------------------------
# Enumerations (plain strings for zero-dependency simplicity)
# ---------------------------------------------------------------------------

# Makhraj (articulation place) constants
BILABIAL = "BILABIAL"
LABIODENTAL = "LABIODENTAL"
INTERDENTAL = "INTERDENTAL"
DENTAL = "DENTAL"
ALVEOLAR = "ALVEOLAR"
POSTALVEOLAR = "POSTALVEOLAR"
PALATAL = "PALATAL"
VELAR = "VELAR"
UVULAR = "UVULAR"
PHARYNGEAL = "PHARYNGEAL"
GLOTTAL = "GLOTTAL"

# Sifat (phonetic features) constants
VOICED = "VOICED"
VOICELESS = "VOICELESS"
STOP = "STOP"
FRICATIVE = "FRICATIVE"
AFFRICATE = "AFFRICATE"
NASAL = "NASAL"
LATERAL = "LATERAL"
TRILL = "TRILL"
APPROXIMANT = "APPROXIMANT"
EMPHATIC = "EMPHATIC"
NON_EMPHATIC = "NON_EMPHATIC"
PULMONIC = "PULMONIC"
SHORT_DURATION = "SHORT"
LONG_DURATION = "LONG"

# Vocalic function constants
OPENING_FUNCTION = "OPENING_FUNCTION"
ROUNDING_FUNCTION = "ROUNDING_FUNCTION"
FRONTING_FUNCTION = "FRONTING_FUNCTION"
CLOSURE_FUNCTION = "CLOSURE_FUNCTION"
COMPRESSION_FUNCTION = "COMPRESSION_FUNCTION"
TANWIN_OPEN_FUNCTION = "TANWIN_OPEN_FUNCTION"
TANWIN_ROUND_FUNCTION = "TANWIN_ROUND_FUNCTION"
TANWIN_FRONT_FUNCTION = "TANWIN_FRONT_FUNCTION"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MakhrajGeometry:
    """Articulation place geometry for a consonant."""
    spatial_source: str          # e.g. BILABIAL
    articulation_point: str      # human-readable description


@dataclass(frozen=True)
class SifatGeometry:
    """Phonological feature bundle for a consonant."""
    voicing: str                 # VOICED / VOICELESS
    manner: str                  # STOP / FRICATIVE / NASAL / …
    airflow: str                 # PULMONIC (all Arabic consonants are pulmonic)
    duration: str                # SHORT / LONG
    emphasis: str                # EMPHATIC / NON_EMPHATIC


@dataclass(frozen=True)
class PhoneticGroundingProfile:
    """
    Complete phonetic identity proof for an Arabic letter.

    Binds: unicode_identity + script_identity + sound_identity
           + makhraj_profile + sifat_profile
           + invalidating_differences (list of (label, difference_type) pairs).
    """
    arabic_name: str
    unicode_codepoint: int       # e.g. 0x0628
    unicode_identity: str        # e.g. "U+0628"
    script_identity: str         # e.g. "ARABIC_LETTER_BAA"
    sound_identity: str          # e.g. "VOICED_BILABIAL_STOP"
    makhraj: MakhrajGeometry
    sifat: SifatGeometry
    # Each entry: (pair_label, difference_dimension)
    # e.g. ("baa_vs_meem", "NASALITY_DIFF")
    invalidating_differences: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class VocalicEnergyProfile:
    """
    Vocalic function and energy profile for an Arabic haraka.

    Binds: unicode_identity + vocalic_function + acoustic_effect
           + duration + aperture + tongue_position.
    """
    arabic_name: str
    unicode_codepoint: int
    unicode_identity: str
    script_mark_identity: str
    vocalic_function: str
    acoustic_effect: str
    duration: str
    aperture: str
    tongue_position: str
    # Differences that invalidate function transfer
    invalidating_differences: tuple[tuple[str, str], ...]


# ---------------------------------------------------------------------------
# Phonetic profiles for all 28 core Arabic letters
# Ordered by Unicode codepoint (U+0621 … U+064A)
# ---------------------------------------------------------------------------

_M_GLOTTAL_HAMZA = MakhrajGeometry(
    spatial_source=GLOTTAL, articulation_point="GLOTTIS_CLOSURE")
_M_PHARYNGEAL = MakhrajGeometry(
    spatial_source=PHARYNGEAL, articulation_point="PHARYNX_CONSTRICTION")
_M_UVULAR = MakhrajGeometry(
    spatial_source=UVULAR, articulation_point="UVULA_CONTACT")
_M_VELAR = MakhrajGeometry(
    spatial_source=VELAR, articulation_point="VELUM_CONTACT")
_M_PALATAL = MakhrajGeometry(
    spatial_source=PALATAL, articulation_point="PALATE_CONTACT")
_M_ALVEOLAR = MakhrajGeometry(
    spatial_source=ALVEOLAR, articulation_point="ALVEOLAR_RIDGE")
_M_INTERDENTAL = MakhrajGeometry(
    spatial_source=INTERDENTAL, articulation_point="INTER_DENTAL")
_M_DENTAL = MakhrajGeometry(
    spatial_source=DENTAL, articulation_point="UPPER_TEETH")
_M_LABIODENTAL = MakhrajGeometry(
    spatial_source=LABIODENTAL, articulation_point="LOWER_LIP_UPPER_TEETH")
_M_BILABIAL = MakhrajGeometry(
    spatial_source=BILABIAL, articulation_point="LIPS_CLOSURE")
_M_POSTALVEOLAR = MakhrajGeometry(
    spatial_source=POSTALVEOLAR, articulation_point="POSTALVEOLAR_RIDGE")


LETTER_PHONETIC_PROFILES: dict[int, PhoneticGroundingProfile] = {
    # U+0621 ء HAMZA
    0x0621: PhoneticGroundingProfile(
        arabic_name="hamza",
        unicode_codepoint=0x0621,
        unicode_identity="U+0621",
        script_identity="ARABIC_LETTER_HAMZA",
        sound_identity="VOICELESS_GLOTTAL_STOP",
        makhraj=_M_GLOTTAL_HAMZA,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("hamza_vs_ayn", "PLACE_DIFF"),
            ("hamza_vs_haa_glottal", "VOICING_DIFF"),
        ),
    ),
    # U+0622 آ ALEF WITH MADDA (long vowel carrier)
    0x0622: PhoneticGroundingProfile(
        arabic_name="alef_madda",
        unicode_codepoint=0x0622,
        unicode_identity="U+0622",
        script_identity="ARABIC_LETTER_ALEF_WITH_MADDA_ABOVE",
        sound_identity="LONG_VOWEL_CARRIER_ALEF",
        makhraj=_M_GLOTTAL_HAMZA,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=LONG_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("alef_madda_vs_waw", "PLACE_DIFF"),
            ("alef_madda_vs_yaa", "HEIGHT_DIFF"),
        ),
    ),
    # U+0623 أ ALEF WITH HAMZA ABOVE
    0x0623: PhoneticGroundingProfile(
        arabic_name="alef_hamza_above",
        unicode_codepoint=0x0623,
        unicode_identity="U+0623",
        script_identity="ARABIC_LETTER_ALEF_WITH_HAMZA_ABOVE",
        sound_identity="VOICELESS_GLOTTAL_STOP_ABOVE",
        makhraj=_M_GLOTTAL_HAMZA,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("alef_hamza_above_vs_ayn", "PLACE_DIFF"),
        ),
    ),
    # U+0624 ؤ WAW WITH HAMZA
    0x0624: PhoneticGroundingProfile(
        arabic_name="waw_hamza",
        unicode_codepoint=0x0624,
        unicode_identity="U+0624",
        script_identity="ARABIC_LETTER_WAW_WITH_HAMZA_ABOVE",
        sound_identity="BILABIAL_HAMZA_WAW",
        makhraj=_M_BILABIAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("waw_hamza_vs_baa", "MANNER_DIFF"),
        ),
    ),
    # U+0625 إ ALEF WITH HAMZA BELOW
    0x0625: PhoneticGroundingProfile(
        arabic_name="alef_hamza_below",
        unicode_codepoint=0x0625,
        unicode_identity="U+0625",
        script_identity="ARABIC_LETTER_ALEF_WITH_HAMZA_BELOW",
        sound_identity="VOICELESS_GLOTTAL_STOP_BELOW",
        makhraj=_M_GLOTTAL_HAMZA,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("alef_hamza_below_vs_ayn", "PLACE_DIFF"),
        ),
    ),
    # U+0626 ئ YEH WITH HAMZA
    0x0626: PhoneticGroundingProfile(
        arabic_name="yeh_hamza",
        unicode_codepoint=0x0626,
        unicode_identity="U+0626",
        script_identity="ARABIC_LETTER_YEH_WITH_HAMZA_ABOVE",
        sound_identity="PALATAL_HAMZA_YEH",
        makhraj=_M_PALATAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("yeh_hamza_vs_yaa", "MANNER_DIFF"),
        ),
    ),
    # U+0627 ا ALEF (bare, long vowel / glottal carrier)
    0x0627: PhoneticGroundingProfile(
        arabic_name="alef",
        unicode_codepoint=0x0627,
        unicode_identity="U+0627",
        script_identity="ARABIC_LETTER_ALEF",
        sound_identity="LONG_VOWEL_CARRIER_BARE_ALEF",
        makhraj=_M_GLOTTAL_HAMZA,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=LONG_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("alef_vs_waw", "PLACE_DIFF"),
            ("alef_vs_yaa", "HEIGHT_DIFF"),
        ),
    ),
    # U+0628 ب BAA
    0x0628: PhoneticGroundingProfile(
        arabic_name="baa",
        unicode_codepoint=0x0628,
        unicode_identity="U+0628",
        script_identity="ARABIC_LETTER_BAA",
        sound_identity="VOICED_BILABIAL_STOP",
        makhraj=_M_BILABIAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("baa_vs_meem", "NASALITY_DIFF"),
            ("baa_vs_faa", "PLACE_DIFF"),
            ("baa_vs_taa", "VOICING_DIFF"),
            ("baa_vs_waw", "MANNER_DIFF"),
        ),
    ),
    # U+0629 ة TAA MARBUTA
    0x0629: PhoneticGroundingProfile(
        arabic_name="taa_marbuta",
        unicode_codepoint=0x0629,
        unicode_identity="U+0629",
        script_identity="ARABIC_LETTER_TAA_MARBUTA",
        sound_identity="VOICELESS_DENTAL_STOP_MARBUTA",
        makhraj=_M_DENTAL,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("taa_marbuta_vs_taa", "SCRIPT_DIFF"),
            ("taa_marbuta_vs_haa", "MANNER_DIFF"),
        ),
    ),
    # U+062A ت TAA
    0x062A: PhoneticGroundingProfile(
        arabic_name="taa",
        unicode_codepoint=0x062A,
        unicode_identity="U+062A",
        script_identity="ARABIC_LETTER_TAA",
        sound_identity="VOICELESS_DENTAL_STOP",
        makhraj=_M_DENTAL,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("taa_vs_baa", "VOICING_DIFF"),
            ("taa_vs_thaa", "PLACE_DIFF"),
            ("taa_vs_daal", "VOICING_DIFF"),
        ),
    ),
    # U+062B ث THAA
    0x062B: PhoneticGroundingProfile(
        arabic_name="thaa",
        unicode_codepoint=0x062B,
        unicode_identity="U+062B",
        script_identity="ARABIC_LETTER_THEH",
        sound_identity="VOICELESS_INTERDENTAL_FRICATIVE",
        makhraj=_M_INTERDENTAL,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("thaa_vs_taa", "PLACE_DIFF"),
            ("thaa_vs_dhaal", "VOICING_DIFF"),
        ),
    ),
    # U+062C ج JEEM
    0x062C: PhoneticGroundingProfile(
        arabic_name="jeem",
        unicode_codepoint=0x062C,
        unicode_identity="U+062C",
        script_identity="ARABIC_LETTER_JEEM",
        sound_identity="VOICED_POSTALVEOLAR_AFFRICATE",
        makhraj=_M_POSTALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICED, manner=AFFRICATE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("jeem_vs_sheen", "VOICING_DIFF"),
            ("jeem_vs_zay", "MANNER_DIFF"),
        ),
    ),
    # U+062D ح HAA (pharyngeal)
    0x062D: PhoneticGroundingProfile(
        arabic_name="haa_pharyngeal",
        unicode_codepoint=0x062D,
        unicode_identity="U+062D",
        script_identity="ARABIC_LETTER_HAH",
        sound_identity="VOICELESS_PHARYNGEAL_FRICATIVE",
        makhraj=_M_PHARYNGEAL,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("haa_pharyngeal_vs_ayn", "VOICING_DIFF"),
            ("haa_pharyngeal_vs_haa_glottal", "PLACE_DIFF"),
        ),
    ),
    # U+062E خ KHAA
    0x062E: PhoneticGroundingProfile(
        arabic_name="khaa",
        unicode_codepoint=0x062E,
        unicode_identity="U+062E",
        script_identity="ARABIC_LETTER_KHAH",
        sound_identity="VOICELESS_UVULAR_FRICATIVE",
        makhraj=_M_UVULAR,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("khaa_vs_ghain", "VOICING_DIFF"),
            ("khaa_vs_kaf", "MANNER_DIFF"),
        ),
    ),
    # U+062F د DAAL
    0x062F: PhoneticGroundingProfile(
        arabic_name="daal",
        unicode_codepoint=0x062F,
        unicode_identity="U+062F",
        script_identity="ARABIC_LETTER_DAL",
        sound_identity="VOICED_DENTAL_STOP",
        makhraj=_M_DENTAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("daal_vs_taa", "VOICING_DIFF"),
            ("daal_vs_daad", "EMPHASIS_DIFF"),
        ),
    ),
    # U+0630 ذ DHAAL
    0x0630: PhoneticGroundingProfile(
        arabic_name="dhaal",
        unicode_codepoint=0x0630,
        unicode_identity="U+0630",
        script_identity="ARABIC_LETTER_THAL",
        sound_identity="VOICED_INTERDENTAL_FRICATIVE",
        makhraj=_M_INTERDENTAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("dhaal_vs_thaa", "VOICING_DIFF"),
            ("dhaal_vs_zay", "PLACE_DIFF"),
        ),
    ),
    # U+0631 ر RAA
    0x0631: PhoneticGroundingProfile(
        arabic_name="raa",
        unicode_codepoint=0x0631,
        unicode_identity="U+0631",
        script_identity="ARABIC_LETTER_REH",
        sound_identity="VOICED_ALVEOLAR_TRILL",
        makhraj=_M_ALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICED, manner=TRILL,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("raa_vs_laam", "MANNER_DIFF"),
            ("raa_vs_noon", "MANNER_DIFF"),
        ),
    ),
    # U+0632 ز ZAY
    0x0632: PhoneticGroundingProfile(
        arabic_name="zay",
        unicode_codepoint=0x0632,
        unicode_identity="U+0632",
        script_identity="ARABIC_LETTER_ZAIN",
        sound_identity="VOICED_ALVEOLAR_FRICATIVE",
        makhraj=_M_ALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICED, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("zay_vs_seen", "VOICING_DIFF"),
            ("zay_vs_dhaal", "PLACE_DIFF"),
        ),
    ),
    # U+0633 س SEEN
    0x0633: PhoneticGroundingProfile(
        arabic_name="seen",
        unicode_codepoint=0x0633,
        unicode_identity="U+0633",
        script_identity="ARABIC_LETTER_SEEN",
        sound_identity="VOICELESS_ALVEOLAR_FRICATIVE",
        makhraj=_M_ALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("seen_vs_sheen", "PLACE_DIFF"),
            ("seen_vs_zay", "VOICING_DIFF"),
            ("seen_vs_saad", "EMPHASIS_DIFF"),
        ),
    ),
    # U+0634 ش SHEEN
    0x0634: PhoneticGroundingProfile(
        arabic_name="sheen",
        unicode_codepoint=0x0634,
        unicode_identity="U+0634",
        script_identity="ARABIC_LETTER_SHEEN",
        sound_identity="VOICELESS_POSTALVEOLAR_FRICATIVE",
        makhraj=_M_POSTALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("sheen_vs_seen", "PLACE_DIFF"),
            ("sheen_vs_jeem", "VOICING_DIFF"),
        ),
    ),
    # U+0635 ص SAAD (emphatic)
    0x0635: PhoneticGroundingProfile(
        arabic_name="saad",
        unicode_codepoint=0x0635,
        unicode_identity="U+0635",
        script_identity="ARABIC_LETTER_SAD",
        sound_identity="VOICELESS_EMPHATIC_ALVEOLAR_FRICATIVE",
        makhraj=_M_ALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=EMPHATIC),
        invalidating_differences=(
            ("saad_vs_seen", "EMPHASIS_DIFF"),
            ("saad_vs_daad", "MANNER_DIFF"),
        ),
    ),
    # U+0636 ض DAAD (emphatic)
    0x0636: PhoneticGroundingProfile(
        arabic_name="daad",
        unicode_codepoint=0x0636,
        unicode_identity="U+0636",
        script_identity="ARABIC_LETTER_DAD",
        sound_identity="VOICED_EMPHATIC_DENTAL_STOP",
        makhraj=_M_DENTAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=EMPHATIC),
        invalidating_differences=(
            ("daad_vs_daal", "EMPHASIS_DIFF"),
            ("daad_vs_taa_emphatic", "VOICING_DIFF"),
        ),
    ),
    # U+0637 ط TAA emphatic
    0x0637: PhoneticGroundingProfile(
        arabic_name="taa_emphatic",
        unicode_codepoint=0x0637,
        unicode_identity="U+0637",
        script_identity="ARABIC_LETTER_TAH",
        sound_identity="VOICELESS_EMPHATIC_DENTAL_STOP",
        makhraj=_M_DENTAL,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=EMPHATIC),
        invalidating_differences=(
            ("taa_emphatic_vs_taa", "EMPHASIS_DIFF"),
            ("taa_emphatic_vs_daad", "VOICING_DIFF"),
        ),
    ),
    # U+0638 ظ DHAA emphatic
    0x0638: PhoneticGroundingProfile(
        arabic_name="dhaa_emphatic",
        unicode_codepoint=0x0638,
        unicode_identity="U+0638",
        script_identity="ARABIC_LETTER_ZAH",
        sound_identity="VOICED_EMPHATIC_INTERDENTAL_FRICATIVE",
        makhraj=_M_INTERDENTAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=EMPHATIC),
        invalidating_differences=(
            ("dhaa_emphatic_vs_dhaal", "EMPHASIS_DIFF"),
        ),
    ),
    # U+0639 ع AYN
    0x0639: PhoneticGroundingProfile(
        arabic_name="ayn",
        unicode_codepoint=0x0639,
        unicode_identity="U+0639",
        script_identity="ARABIC_LETTER_AIN",
        sound_identity="VOICED_PHARYNGEAL_FRICATIVE",
        makhraj=_M_PHARYNGEAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("ayn_vs_haa_pharyngeal", "VOICING_DIFF"),
            ("ayn_vs_hamza", "PLACE_DIFF"),
        ),
    ),
    # U+063A غ GHAIN
    0x063A: PhoneticGroundingProfile(
        arabic_name="ghain",
        unicode_codepoint=0x063A,
        unicode_identity="U+063A",
        script_identity="ARABIC_LETTER_GHAIN",
        sound_identity="VOICED_UVULAR_FRICATIVE",
        makhraj=_M_UVULAR,
        sifat=SifatGeometry(
            voicing=VOICED, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("ghain_vs_khaa", "VOICING_DIFF"),
            ("ghain_vs_qaf", "MANNER_DIFF"),
        ),
    ),
    # U+0641 ف FAA
    0x0641: PhoneticGroundingProfile(
        arabic_name="faa",
        unicode_codepoint=0x0641,
        unicode_identity="U+0641",
        script_identity="ARABIC_LETTER_FA",
        sound_identity="VOICELESS_LABIODENTAL_FRICATIVE",
        makhraj=_M_LABIODENTAL,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("faa_vs_baa", "PLACE_DIFF"),
            ("faa_vs_waw", "MANNER_DIFF"),
        ),
    ),
    # U+0642 ق QAF
    0x0642: PhoneticGroundingProfile(
        arabic_name="qaf",
        unicode_codepoint=0x0642,
        unicode_identity="U+0642",
        script_identity="ARABIC_LETTER_QAF",
        sound_identity="VOICELESS_UVULAR_STOP",
        makhraj=_M_UVULAR,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("qaf_vs_kaf", "PLACE_DIFF"),
            ("qaf_vs_ghain", "MANNER_DIFF"),
        ),
    ),
    # U+0643 ك KAF
    0x0643: PhoneticGroundingProfile(
        arabic_name="kaf",
        unicode_codepoint=0x0643,
        unicode_identity="U+0643",
        script_identity="ARABIC_LETTER_KAF",
        sound_identity="VOICELESS_VELAR_STOP",
        makhraj=_M_VELAR,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=STOP,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("kaf_vs_qaf", "PLACE_DIFF"),
            ("kaf_vs_gaf", "VOICING_DIFF"),
        ),
    ),
    # U+0644 ل LAAM
    0x0644: PhoneticGroundingProfile(
        arabic_name="laam",
        unicode_codepoint=0x0644,
        unicode_identity="U+0644",
        script_identity="ARABIC_LETTER_LAM",
        sound_identity="VOICED_ALVEOLAR_LATERAL",
        makhraj=_M_ALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICED, manner=LATERAL,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("laam_vs_noon", "MANNER_DIFF"),
            ("laam_vs_raa", "MANNER_DIFF"),
        ),
    ),
    # U+0645 م MEEM
    0x0645: PhoneticGroundingProfile(
        arabic_name="meem",
        unicode_codepoint=0x0645,
        unicode_identity="U+0645",
        script_identity="ARABIC_LETTER_MEEM",
        sound_identity="VOICED_BILABIAL_NASAL",
        makhraj=_M_BILABIAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=NASAL,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("meem_vs_baa", "NASALITY_DIFF"),
            ("meem_vs_noon", "PLACE_DIFF"),
        ),
    ),
    # U+0646 ن NOON
    0x0646: PhoneticGroundingProfile(
        arabic_name="noon",
        unicode_codepoint=0x0646,
        unicode_identity="U+0646",
        script_identity="ARABIC_LETTER_NOON",
        sound_identity="VOICED_ALVEOLAR_NASAL",
        makhraj=_M_ALVEOLAR,
        sifat=SifatGeometry(
            voicing=VOICED, manner=NASAL,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("noon_vs_meem", "PLACE_DIFF"),
            ("noon_vs_laam", "MANNER_DIFF"),
        ),
    ),
    # U+0647 ه HAA (glottal)
    0x0647: PhoneticGroundingProfile(
        arabic_name="haa_glottal",
        unicode_codepoint=0x0647,
        unicode_identity="U+0647",
        script_identity="ARABIC_LETTER_HEH",
        sound_identity="VOICELESS_GLOTTAL_FRICATIVE",
        makhraj=_M_GLOTTAL_HAMZA,
        sifat=SifatGeometry(
            voicing=VOICELESS, manner=FRICATIVE,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("haa_glottal_vs_haa_pharyngeal", "PLACE_DIFF"),
            ("haa_glottal_vs_hamza", "MANNER_DIFF"),
        ),
    ),
    # U+0648 و WAW
    0x0648: PhoneticGroundingProfile(
        arabic_name="waw",
        unicode_codepoint=0x0648,
        unicode_identity="U+0648",
        script_identity="ARABIC_LETTER_WAW",
        sound_identity="VOICED_BILABIAL_APPROXIMANT",
        makhraj=_M_BILABIAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("waw_vs_baa", "MANNER_DIFF"),
            ("waw_vs_meem", "MANNER_DIFF"),
            ("waw_vs_yaa", "PLACE_DIFF"),
        ),
    ),
    # U+0649 ى ALEF MAQSURA
    0x0649: PhoneticGroundingProfile(
        arabic_name="alef_maqsura",
        unicode_codepoint=0x0649,
        unicode_identity="U+0649",
        script_identity="ARABIC_LETTER_ALEF_MAKSURA",
        sound_identity="LONG_VOWEL_CARRIER_ALEF_MAQSURA",
        makhraj=_M_PALATAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=LONG_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("alef_maqsura_vs_yaa", "SCRIPT_DIFF"),
        ),
    ),
    # U+064A ي YAA
    0x064A: PhoneticGroundingProfile(
        arabic_name="yaa",
        unicode_codepoint=0x064A,
        unicode_identity="U+064A",
        script_identity="ARABIC_LETTER_YEH",
        sound_identity="VOICED_PALATAL_APPROXIMANT",
        makhraj=_M_PALATAL,
        sifat=SifatGeometry(
            voicing=VOICED, manner=APPROXIMANT,
            airflow=PULMONIC, duration=SHORT_DURATION, emphasis=NON_EMPHATIC),
        invalidating_differences=(
            ("yaa_vs_waw", "PLACE_DIFF"),
            ("yaa_vs_jeem", "MANNER_DIFF"),
        ),
    ),
}


# ---------------------------------------------------------------------------
# Vocalic energy profiles for Arabic harakat
# ---------------------------------------------------------------------------

HARAKA_ENERGY_PROFILES: dict[int, VocalicEnergyProfile] = {
    # U+064E فتحة FATHA
    0x064E: VocalicEnergyProfile(
        arabic_name="fatha",
        unicode_codepoint=0x064E,
        unicode_identity="U+064E",
        script_mark_identity="ARABIC_FATHA",
        vocalic_function=OPENING_FUNCTION,
        acoustic_effect="SHORT_LOW_FRONT_VOWEL",
        duration="SHORT",
        aperture="OPEN",
        tongue_position="LOW_FRONT",
        invalidating_differences=(
            ("fatha_vs_damma", "ROUNDING_DIFF"),
            ("fatha_vs_kasra", "HEIGHT_DIFF"),
        ),
    ),
    # U+064F ضمة DAMMA
    0x064F: VocalicEnergyProfile(
        arabic_name="damma",
        unicode_codepoint=0x064F,
        unicode_identity="U+064F",
        script_mark_identity="ARABIC_DAMMA",
        vocalic_function=ROUNDING_FUNCTION,
        acoustic_effect="SHORT_HIGH_BACK_ROUNDED_VOWEL",
        duration="SHORT",
        aperture="CLOSE",
        tongue_position="HIGH_BACK",
        invalidating_differences=(
            ("damma_vs_fatha", "ROUNDING_DIFF"),
            ("damma_vs_kasra", "BACKNESS_DIFF"),
        ),
    ),
    # U+0650 كسرة KASRA
    0x0650: VocalicEnergyProfile(
        arabic_name="kasra",
        unicode_codepoint=0x0650,
        unicode_identity="U+0650",
        script_mark_identity="ARABIC_KASRA",
        vocalic_function=FRONTING_FUNCTION,
        acoustic_effect="SHORT_HIGH_FRONT_VOWEL",
        duration="SHORT",
        aperture="CLOSE",
        tongue_position="HIGH_FRONT",
        invalidating_differences=(
            ("kasra_vs_fatha", "HEIGHT_DIFF"),
            ("kasra_vs_damma", "BACKNESS_DIFF"),
        ),
    ),
    # U+0652 سكون SUKUN
    0x0652: VocalicEnergyProfile(
        arabic_name="sukun",
        unicode_codepoint=0x0652,
        unicode_identity="U+0652",
        script_mark_identity="ARABIC_SUKUN",
        vocalic_function=CLOSURE_FUNCTION,
        acoustic_effect="VOWEL_ABSENCE",
        duration="ZERO",
        aperture="CLOSED",
        tongue_position="NEUTRAL",
        invalidating_differences=(
            ("sukun_vs_fatha", "APERTURE_DIFF"),
            ("sukun_vs_shadda", "FUNCTION_DIFF"),
        ),
    ),
    # U+0651 شدة SHADDA
    0x0651: VocalicEnergyProfile(
        arabic_name="shadda",
        unicode_codepoint=0x0651,
        unicode_identity="U+0651",
        script_mark_identity="ARABIC_SHADDA",
        vocalic_function=COMPRESSION_FUNCTION,
        acoustic_effect="CONSONANT_GEMINATION",
        duration="DOUBLED",
        aperture="N/A",
        tongue_position="N/A",
        invalidating_differences=(
            ("shadda_vs_sukun", "FUNCTION_DIFF"),
            ("shadda_vs_fatha", "FUNCTION_DIFF"),
        ),
    ),
    # U+064B تنوين فتح TANWIN_FATH
    0x064B: VocalicEnergyProfile(
        arabic_name="tanwin_fath",
        unicode_codepoint=0x064B,
        unicode_identity="U+064B",
        script_mark_identity="ARABIC_FATHATAN",
        vocalic_function=TANWIN_OPEN_FUNCTION,
        acoustic_effect="SHORT_LOW_FRONT_VOWEL_NUNATION",
        duration="SHORT",
        aperture="OPEN",
        tongue_position="LOW_FRONT",
        invalidating_differences=(
            ("tanwin_fath_vs_tanwin_damm", "ROUNDING_DIFF"),
            ("tanwin_fath_vs_fatha", "NUNATION_DIFF"),
        ),
    ),
    # U+064C تنوين ضم TANWIN_DAMM
    0x064C: VocalicEnergyProfile(
        arabic_name="tanwin_damm",
        unicode_codepoint=0x064C,
        unicode_identity="U+064C",
        script_mark_identity="ARABIC_DAMMATAN",
        vocalic_function=TANWIN_ROUND_FUNCTION,
        acoustic_effect="SHORT_HIGH_BACK_ROUNDED_VOWEL_NUNATION",
        duration="SHORT",
        aperture="CLOSE",
        tongue_position="HIGH_BACK",
        invalidating_differences=(
            ("tanwin_damm_vs_tanwin_fath", "ROUNDING_DIFF"),
            ("tanwin_damm_vs_damma", "NUNATION_DIFF"),
        ),
    ),
    # U+064D تنوين كسر TANWIN_KASR
    0x064D: VocalicEnergyProfile(
        arabic_name="tanwin_kasr",
        unicode_codepoint=0x064D,
        unicode_identity="U+064D",
        script_mark_identity="ARABIC_KASRATAN",
        vocalic_function=TANWIN_FRONT_FUNCTION,
        acoustic_effect="SHORT_HIGH_FRONT_VOWEL_NUNATION",
        duration="SHORT",
        aperture="CLOSE",
        tongue_position="HIGH_FRONT",
        invalidating_differences=(
            ("tanwin_kasr_vs_tanwin_fath", "HEIGHT_DIFF"),
            ("tanwin_kasr_vs_kasra", "NUNATION_DIFF"),
        ),
    ),
}


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def get_phonetic_profile(codepoint: int) -> PhoneticGroundingProfile | None:
    """Return the PhoneticGroundingProfile for an Arabic letter codepoint, or None."""
    return LETTER_PHONETIC_PROFILES.get(codepoint)


def get_energy_profile(codepoint: int) -> VocalicEnergyProfile | None:
    """Return the VocalicEnergyProfile for an Arabic haraka codepoint, or None."""
    return HARAKA_ENERGY_PROFILES.get(codepoint)
