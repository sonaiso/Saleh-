"""
Abjad Numeric Coordinate System

Constitutional requirement:
  - Abjad values are CONVENTIONAL coordinates, not semantic.
  - semantic_force = FORBIDDEN
  - No meaning or hukm can be derived from numeric values.

The Abjad system assigns conventional numeric values to Arabic letters
for traditional calculation purposes (Hisab al-Jummal), but these values
carry NO semantic force and CANNOT be used to prove meaning or hukm.

Constitutional constraint:
  Abjad(ب) = 2  ✓ (conventional coordinate)
  Meaning(ب) = 2  ✗ (FORBIDDEN)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AbjadCoordinate:
    """
    Conventional numeric coordinate in the Abjad system.

    CRITICAL: semantic_force = FORBIDDEN
    This coordinate is CONVENTIONAL ONLY, not semantic.
    """
    system: str              # "ABJAD"
    letter_codepoint: int    # Unicode codepoint
    letter_name: str         # e.g., "baa", "taa"
    numeric_value: int       # Conventional numeric value
    evidence_source: str     # "abjad_convention"
    semantic_force: str      # MUST be "FORBIDDEN"


# Abjad system values for all 28 Arabic letters
# Source: Traditional Hisab al-Jummal ordering
ABJAD_VALUES = {
    # أبجد (Abjad)
    0x0627: 1,    # ا Alif
    0x0628: 2,    # ب Baa
    0x062C: 3,    # ج Jeem
    0x062F: 4,    # د Dal

    # هوز (Hawwaz)
    0x0647: 5,    # ه Haa
    0x0648: 6,    # و Waw
    0x0632: 7,    # ز Zay

    # حطي (Hutti)
    0x062D: 8,    # ح Haa (pharyngeal)
    0x0637: 9,    # ط Taa (emphatic)
    0x064A: 10,   # ي Yaa

    # كلمن (Kalaman)
    0x0643: 20,   # ك Kaf
    0x0644: 30,   # ل Lam
    0x0645: 40,   # م Meem
    0x0646: 50,   # ن Noon

    # سعفص (Sa'fas)
    0x0633: 60,   # س Seen
    0x0639: 70,   # ع Ayn
    0x0641: 80,   # ف Faa
    0x0635: 90,   # ص Saad

    # قرشت (Qarashat)
    0x0642: 100,  # ق Qaf
    0x0631: 200,  # ر Raa
    0x0634: 300,  # ش Sheen
    0x062A: 400,  # ت Taa

    # ثخذ (Thakhadh)
    0x062B: 500,  # ث Thaa
    0x062E: 600,  # خ Khaa
    0x0630: 700,  # ذ Dhal

    # ضظغ (Dhadhagh)
    0x0636: 800,  # ض Daad
    0x0638: 900,  # ظ Dhaa
    0x063A: 1000, # غ Ghayn
}


# Reverse mapping for lookups
ABJAD_LETTER_NAMES = {
    0x0621: "hamza",
    0x0627: "alif",
    0x0628: "baa",
    0x062A: "taa",
    0x062B: "thaa",
    0x062C: "jeem",
    0x062D: "haa",
    0x062E: "khaa",
    0x062F: "dal",
    0x0630: "dhal",
    0x0631: "raa",
    0x0632: "zay",
    0x0633: "seen",
    0x0634: "sheen",
    0x0635: "saad",
    0x0636: "daad",
    0x0637: "taa_emphatic",
    0x0638: "dhaa",
    0x0639: "ayn",
    0x063A: "ghayn",
    0x0641: "faa",
    0x0642: "qaf",
    0x0643: "kaf",
    0x0644: "lam",
    0x0645: "meem",
    0x0646: "noon",
    0x0647: "haa_final",
    0x0648: "waw",
    0x064A: "yaa",
}


def get_abjad_coordinate(codepoint: int) -> AbjadCoordinate | None:
    """
    Get Abjad coordinate for a letter codepoint.

    Returns None if the letter is not in the Abjad system.
    Note: Hamza (U+0621) has no Abjad value in traditional systems.

    Args:
        codepoint: Unicode codepoint of Arabic letter

    Returns:
        AbjadCoordinate if letter is in Abjad system, None otherwise
    """
    if codepoint not in ABJAD_VALUES:
        return None

    letter_name = ABJAD_LETTER_NAMES.get(codepoint, f"unknown_{codepoint:04x}")

    return AbjadCoordinate(
        system="ABJAD",
        letter_codepoint=codepoint,
        letter_name=letter_name,
        numeric_value=ABJAD_VALUES[codepoint],
        evidence_source="abjad_convention",
        semantic_force="FORBIDDEN",  # CRITICAL: no semantic meaning
    )


def has_abjad_value(codepoint: int) -> bool:
    """Check if a letter codepoint has an Abjad numeric value."""
    return codepoint in ABJAD_VALUES
