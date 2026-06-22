"""
Weight Pattern Rules — P3.1 (Arabic wazn extraction). مرشّح الوزن الصرفي.

AUXILIARY non-registry sub-pass (NOT a registered LayerSpec; registry count stays 19,
no P13, P0–P12 spine untouched). Runs AFTER an accepted P3 RootStemCandidate (letter/
haraka/position identity + CV syllable geometry over the six licensed patterns
CV/CVV/CVC/CVVC/CVCC/CVVCC + stem-matter normalization) and BEFORE WordForm / P5
MufradWordCandidate / word-kind readiness / P5.1 mabni-mu'rab / i'rab / dalalah.

It answers, for a preserved Arabic word surface + its structural matter trace:
  - which weight patterns (أوزان) are structurally LICENSED by this surface?
  - which surface letters align to root slots (ف/ع/ل)?
  - which letters appear as possible ziyadah (added letters)?
  - what is uncertain due to shadda / madd / hamza / weak letters / deletion /
    assimilation / ambiguous segmentation?
  - ACCEPT / DEFER / BLOCK?

CANDIDATE-ONLY: it may emit MULTIPLE WeightPatternCandidate objects for one token when
several weights are structurally licensed — they remain candidates; no final winner is
forced. It NEVER asserts a final root, a final wazn, a final word kind / part of speech,
a final i'rab, dalalah, ifadah, hukm, truth, reality, or intended meaning (forbidden).

Layer: WeightPatternQiyas
Input (far): RootStemCandidate (a single accepted P3 candidate)
Output:      WeightPatternCandidate (zero, one, or many — candidate-only)
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_WEIGHT_PATTERN
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Verdicts.
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# ── Reason codes ──────────────────────────────────────────────────────────────
WEIGHT_PATTERN_ACCEPTED_EXACT_ALIGNMENT = "weight_pattern_accepted_exact_alignment"
WEIGHT_PATTERN_DEFER_AMBIGUOUS_ROOT_SLOT = "weight_pattern_defer_ambiguous_root_slot"
WEIGHT_PATTERN_DEFER_WEAK_LETTER_AMBIGUITY = "weight_pattern_defer_weak_letter_ambiguity"
WEIGHT_PATTERN_DEFER_SHADDA_EXPANSION_REQUIRED = "weight_pattern_defer_shadda_expansion_required"
WEIGHT_PATTERN_DEFER_HAMZA_NORMALIZATION_REQUIRED = "weight_pattern_defer_hamza_normalization_required"
WEIGHT_PATTERN_DEFER_MADD_NORMALIZATION_REQUIRED = "weight_pattern_defer_madd_normalization_required"
WEIGHT_PATTERN_BLOCK_NO_LICENSED_PATTERN = "weight_pattern_block_no_licensed_pattern"
WEIGHT_PATTERN_BLOCK_INVALID_ALIGNMENT = "weight_pattern_block_invalid_alignment"
# Shared guards (mirror the other auxiliary layers).
IDENTITY_COLLAPSE_BLOCKED = "identity_collapse_blocked"
FORBIDDEN_OUTPUT_ATTEMPTED = "forbidden_output_attempted"

# ── Arabic character classes (structural only) ────────────────────────────────
_SHADDA = 0x0651
_TATWEEL = 0x0640
_DAGGER_ALIF = 0x0670
_HARAKAT = set(range(0x064B, 0x0653)) | {_DAGGER_ALIF, _TATWEEL}  # tanwin..sukun, ـٰ, ـ
_HAMZA_FORMS = {0x0621, 0x0623, 0x0625, 0x0624, 0x0626, 0x0622}    # ء أ إ ؤ ئ آ
_WEAK = {0x0627, 0x0648, 0x064A, 0x0649}                            # ا و ي ى

_ROOT_LABELS = ("ف", "ع", "ل")

# Licensed wazn templates as positional skeletons. 'R' = a root slot (must be a sound
# consonant); any other entry is a literal added (ziyadah) letter that must match the
# surface letter at that position exactly. (Sound-root templates; weak/hamza/shadda/madd
# surfaces require normalization first and are DEFERRED, never force-matched.)
_TEMPLATES = (
    ("فَعَلَ", ("R", "R", "R")),
    ("فَاعِل", ("R", "ا", "R", "R")),
    ("مَفْعُول", ("م", "R", "R", "و", "R")),
    ("مَفْعَل", ("م", "R", "R", "R")),
    ("مُفْعِل", ("م", "R", "R", "R")),
)


def _is_root_consonant(ch: str) -> bool:
    o = ord(ch)
    return o not in _WEAK and o not in _HAMZA_FORMS


def analyze_surface(surface: str):
    """Structural surface analysis (no rewriting): returns
    (base_letters, has_shadda, has_hamza, has_madd, has_weak)."""
    has_shadda = any(ord(ch) == _SHADDA for ch in surface)
    has_hamza = any(ord(ch) in _HAMZA_FORMS for ch in surface)
    has_madd = any(ord(ch) == _DAGGER_ALIF for ch in surface) or "آ" in surface
    base = [ch for ch in surface if ord(ch) not in _HARAKAT and ord(ch) != _SHADDA]
    has_weak = any(ord(ch) in _WEAK for ch in base)
    return base, has_shadda, has_hamza, has_madd, has_weak


def _match_template(base, skeleton):
    """Return (root_letters_with_index, added_letters_with_index) or None."""
    if len(base) != len(skeleton):
        return None
    root, added = [], []
    for i, (b, s) in enumerate(zip(base, skeleton)):
        if s == "R":
            if not _is_root_consonant(b):
                return None
            root.append((b, i))
        else:
            if b != s:
                return None
            added.append((b, i))
    if len(root) != 3:
        return None
    return root, added


def _alignment_strings(root, added):
    root_align = ";".join(f"{r}→{_ROOT_LABELS[j]}" for j, (r, _i) in enumerate(root))
    added_align = ";".join(f"{a}@{i}" for (a, i) in added) or "none"
    return root_align, added_align


def align_weight_patterns(surface: str, *, external_root_letters=None):
    """Pure structural wazn alignment — returns (verdict, specs, reason, flags).

    `specs` is a list of dicts (candidate_weight_pattern, root_slot_alignment,
    added_letter_alignment, reason) — possibly several (multiple licensed weights),
    possibly one tentative (DEFER), possibly empty (BLOCK). `flags` records
    shadda/hamza/madd/weak/deletion evidence. No surface letter is ever rewritten.
    """
    base, sh, hz, md, wk = analyze_surface(surface)
    flags = {
        "weak_letter": wk, "shadda": sh, "hamza": hz, "madd": md,
        "deletion_or_assimilation": False,
    }

    # External alignment claim that rewrites/invents a letter not on the surface →
    # invalid alignment (identity-preservation guard).
    if external_root_letters is not None:
        if any(r not in base for r in external_root_letters):
            return VERDICT_BLOCK, [], WEIGHT_PATTERN_BLOCK_INVALID_ALIGNMENT, flags

    if not base:
        return VERDICT_BLOCK, [], WEIGHT_PATTERN_BLOCK_NO_LICENSED_PATTERN, flags

    # Normalization-required surfaces are DEFERRED (never force-matched).
    tentative = [{
        "candidate_weight_pattern": "underdetermined",
        "root_slot_alignment": "underdetermined",
        "added_letter_alignment": "underdetermined",
        "reason": None,
    }]
    if sh:
        tentative[0]["reason"] = WEIGHT_PATTERN_DEFER_SHADDA_EXPANSION_REQUIRED
        return VERDICT_DEFER, tentative, WEIGHT_PATTERN_DEFER_SHADDA_EXPANSION_REQUIRED, flags
    if hz:
        tentative[0]["reason"] = WEIGHT_PATTERN_DEFER_HAMZA_NORMALIZATION_REQUIRED
        return VERDICT_DEFER, tentative, WEIGHT_PATTERN_DEFER_HAMZA_NORMALIZATION_REQUIRED, flags
    if md:
        tentative[0]["reason"] = WEIGHT_PATTERN_DEFER_MADD_NORMALIZATION_REQUIRED
        return VERDICT_DEFER, tentative, WEIGHT_PATTERN_DEFER_MADD_NORMALIZATION_REQUIRED, flags

    # Sound surfaces — match the licensed templates (a long-vowel that is a literal
    # added position is consumed as ziyadah, NOT as a weak root letter).
    specs = []
    for label, skeleton in _TEMPLATES:
        m = _match_template(base, skeleton)
        if m is None:
            continue
        root, added = m
        root_align, added_align = _alignment_strings(root, added)
        specs.append({
            "candidate_weight_pattern": label,
            "root_slot_alignment": root_align,
            "added_letter_alignment": added_align,
            "reason": WEIGHT_PATTERN_ACCEPTED_EXACT_ALIGNMENT,
        })
    if specs:
        return VERDICT_ACCEPT, specs, WEIGHT_PATTERN_ACCEPTED_EXACT_ALIGNMENT, flags

    # No sound template matched but a weak letter is present → hollow/defective
    # ambiguity (the weak letter occupies a root slot) → DEFER (never guessed).
    if wk:
        tentative[0]["reason"] = WEIGHT_PATTERN_DEFER_WEAK_LETTER_AMBIGUITY
        return VERDICT_DEFER, tentative, WEIGHT_PATTERN_DEFER_WEAK_LETTER_AMBIGUITY, flags

    # No licensed alignment exists.
    return VERDICT_BLOCK, [], WEIGHT_PATTERN_BLOCK_NO_LICENSED_PATTERN, flags


WEIGHT_PATTERN_RULE = QiyasRule(
    rule_id="weight_pattern.extract",
    layer="WeightPatternQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="WeightPatternDomain",
    far_type="RootStemCandidate",
    required_effective_wasf=(
        "has_root_stem_ref",
        "has_surface_evidence",
        "has_syllable_profile",
        "weight_pattern_alignment_evidenced",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_weight_pattern_domain",
        "weight_pattern_extraction_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        WEIGHT_PATTERN_BLOCK_NO_LICENSED_PATTERN,
        WEIGHT_PATTERN_BLOCK_INVALID_ALIGNMENT,
        IDENTITY_COLLAPSE_BLOCKED,
        FORBIDDEN_OUTPUT_ATTEMPTED,
    ),
    neutral_identity_domain="weight_pattern_identity",
    output_candidate_type="WeightPatternCandidate",
    forbidden_outputs=FORBIDDEN_WEIGHT_PATTERN,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
