"""
Inflectional Closure Rules — P5.1 (Mabni / Mu'rab readiness).

AUXILIARY non-registry sub-pass (NOT a registered LayerSpec; registry count stays 19,
no P13, P0–P12 spine untouched). Runs AFTER an accepted P5 MufradWordCandidate and
BEFORE P6+ consumers, producing candidate-only structural classification evidence:

  MufradWordCandidate → MabniReadinessCandidate | Mu'rabReadinessCandidate
  (umbrella concept: InflectionalClosureCandidate — مرشّح الانغلاق/الانفتاح الإعرابي)

This is a BINARY structural partition over Arabic word tokens:
    mabni_readiness  : the unit is structurally closed / inherently mabni
    murab_readiness  : the unit is open to i'rab / inflection
It is NOT a grammatical judgment. It never decides a final i'rab position
(raf'/nasb/jarr/jazm), an i'rab sign, dalalah, ifadah, hukm, reality, or final
meaning — those are forbidden outputs.

ARCHITECTURAL REFERENCE: the real classification reference is the full Quran token
inventory AFTER tokenization. No filtered fixture is ever the whole Quran; the
full-Quran completeness test is a separate governed task (corpus snapshot/data
contract). The classifier here is designed for that full inventory; current tests
use honestly-labelled fixtures.

CLASSIFICATION (mabni precedence — a known closed-category token must NEVER slip to
mu'rab merely because it has wazn / source / root / weight / side morphology):

  MABNI if any of:
    - fawatih al-suwar (الحروف المقطعة) — counted as mabni, in the denominator
    - closed functional / pronominal compound (عليه / منه / بكم)
    - closed functional particle / harf (preposition, negation, condition,
      conjunction, exception, nasb, jazm, other closed particles)
    - pronoun
    - demonstrative
    - relative noun / pronoun
    - past-tense verb
    - imperative verb
  MU'RAB if (and only if NO mabni signal matched) the unit is an open
  nominal/verbal token: visible declinable noun, derived noun, open nominal,
  present-tense verb open to i'rab, or open verbal token.

Layer: InflectionalClosureQiyas
Input (far): MufradWordCandidate (a single accepted P5 candidate)
Output:      MabniReadinessCandidate | Mu'rabReadinessCandidate (else deferred/blocked
             InflectionalClosureCandidate)
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_INFLECTIONAL_CLOSURE
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Structural classifications (the binary partition).
CLASS_MABNI = "mabni_readiness"
CLASS_MURAB = "murab_readiness"

# Verdicts.
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# ── MABNI reason codes (why a token is structurally closed / inherently mabni) ──
MABNI_FAWATIH_AL_SUWAR = "mabni_fawatih_al_suwar"
MABNI_CLOSED_COMPOUND = "mabni_closed_compound"
MABNI_CLOSED_PARTICLE = "mabni_closed_particle"
MABNI_PRONOUN = "mabni_pronoun"
MABNI_DEMONSTRATIVE = "mabni_demonstrative"
MABNI_RELATIVE = "mabni_relative"
MABNI_PAST_VERB = "mabni_past_verb"
MABNI_IMPERATIVE_VERB = "mabni_imperative_verb"

# ── MU'RAB reason codes (why a token is open to i'rab / inflection) ─────────────
MURAB_OPEN_DECLINABLE_NOUN = "murab_open_declinable_noun"
MURAB_DERIVED_NOUN = "murab_derived_noun"
MURAB_OPEN_NOMINAL = "murab_open_nominal"
MURAB_PRESENT_VERB_OPEN = "murab_present_verb_open"
MURAB_OPEN_VERBAL = "murab_open_verbal"

# ── DEFER reason codes (admissible but under-determined — never guessed) ────────
WORD_KIND_UNDERSPECIFIED = "word_kind_underspecified"
CLOSED_CATEGORY_EVIDENCE_ABSENT = "closed_category_evidence_absent"
CARRIED_MUFRAD_RESIDUALS = "carried_mufrad_residuals"
INFLECTION_IDENTITY_UNDERSPECIFIED = "inflection_identity_underspecified"

# ── BLOCK reason codes ─────────────────────────────────────────────────────────
INFLECTION_CLASS_CONFLICT = "inflection_class_conflict"        # mabni & mu'rab both asserted
IDENTITY_COLLAPSE_BLOCKED = "identity_collapse_blocked"
FORBIDDEN_OUTPUT_ATTEMPTED = "forbidden_output_attempted"

# Closed-category tokens that the precedence rule routes DIRECTLY to mabni.
_CLOSED_CATEGORY_REASON = {
    "harf": MABNI_CLOSED_PARTICLE,
    "particle": MABNI_CLOSED_PARTICLE,
    "preposition": MABNI_CLOSED_PARTICLE,
    "negation": MABNI_CLOSED_PARTICLE,
    "condition": MABNI_CLOSED_PARTICLE,
    "conjunction": MABNI_CLOSED_PARTICLE,
    "exception": MABNI_CLOSED_PARTICLE,
    "nasb_particle": MABNI_CLOSED_PARTICLE,
    "jazm_particle": MABNI_CLOSED_PARTICLE,
    "pronoun": MABNI_PRONOUN,
    "demonstrative": MABNI_DEMONSTRATIVE,
    "relative": MABNI_RELATIVE,
}


def classify_inflectional_closure(
    *,
    has_identity: bool,
    identity_determined: bool,
    carried_residuals: bool,
    forbidden_attempted: bool,
    class_conflict: bool,
    word_kind=None,            # "nominal" | "verbal" | "particle" | None
    closed_category=None,      # see _CLOSED_CATEGORY_REASON keys | None
    verb_tense=None,           # "past" | "present" | "imperative" | None
    is_closed_compound: bool = False,
    is_fawatih: bool = False,
    is_derived: bool = False,
):
    """Pure classification — returns (verdict, classification_or_None, reason).

    Mabni precedence first: a token whose closed-category / fawatih / closed-compound /
    past-or-imperative-verb evidence is present is classified mabni regardless of any
    morphological (wazn/root) analyzability. Mu'rab is reached ONLY when no mabni
    signal matched.
    """
    # BLOCK — contradictions / forbidden crossings first.
    if forbidden_attempted:
        return VERDICT_BLOCK, None, FORBIDDEN_OUTPUT_ATTEMPTED
    if class_conflict:
        return VERDICT_BLOCK, None, INFLECTION_CLASS_CONFLICT
    if not has_identity:
        return VERDICT_BLOCK, None, IDENTITY_COLLAPSE_BLOCKED

    # DEFER — carried residuals / underspecified identity (admissible, not guessed).
    if carried_residuals:
        return VERDICT_DEFER, None, CARRIED_MUFRAD_RESIDUALS
    if not identity_determined:
        return VERDICT_DEFER, None, INFLECTION_IDENTITY_UNDERSPECIFIED

    # MABNI precedence — closed / inherently-mabni categories, independent of morphology.
    if is_fawatih:
        return VERDICT_ACCEPT, CLASS_MABNI, MABNI_FAWATIH_AL_SUWAR
    if is_closed_compound:
        return VERDICT_ACCEPT, CLASS_MABNI, MABNI_CLOSED_COMPOUND
    if closed_category in _CLOSED_CATEGORY_REASON:
        return VERDICT_ACCEPT, CLASS_MABNI, _CLOSED_CATEGORY_REASON[closed_category]
    if word_kind == "particle":
        return VERDICT_ACCEPT, CLASS_MABNI, MABNI_CLOSED_PARTICLE
    if word_kind == "verbal" and verb_tense == "past":
        return VERDICT_ACCEPT, CLASS_MABNI, MABNI_PAST_VERB
    if word_kind == "verbal" and verb_tense == "imperative":
        return VERDICT_ACCEPT, CLASS_MABNI, MABNI_IMPERATIVE_VERB

    # MU'RAB — only when NO mabni signal matched: open nominal / verbal token.
    if word_kind == "nominal":
        if is_derived:
            return VERDICT_ACCEPT, CLASS_MURAB, MURAB_DERIVED_NOUN
        return VERDICT_ACCEPT, CLASS_MURAB, MURAB_OPEN_DECLINABLE_NOUN
    if word_kind == "verbal" and verb_tense == "present":
        return VERDICT_ACCEPT, CLASS_MURAB, MURAB_PRESENT_VERB_OPEN
    if word_kind == "verbal":
        return VERDICT_ACCEPT, CLASS_MURAB, MURAB_OPEN_VERBAL

    # DEFER — not enough evidence to classify (never guessed).
    if word_kind is None:
        return VERDICT_DEFER, None, WORD_KIND_UNDERSPECIFIED
    return VERDICT_DEFER, None, CLOSED_CATEGORY_EVIDENCE_ABSENT


def _rule(output_candidate_type: str) -> QiyasRule:
    return QiyasRule(
        rule_id="inflectional_closure.classify",
        layer="InflectionalClosureQiyas",
        pattern=QiyasPattern.MEMBERSHIP,
        asl_type="InflectionalClosureDomain",
        far_type="MufradWordCandidate",
        required_effective_wasf=(
            "has_mufrad_word_ref",
            "has_word_kind_evidence",
            "inflectional_closure_classified",
            "upstream_identity_preserved",
        ),
        required_illah=(
            "belongs_to_inflectional_closure_domain",
            "inflectional_closure_classification_licensed",
        ),
        required_wadi_gates=_ALL_WADI,
        invalidating_differences=(
            INFLECTION_CLASS_CONFLICT,
            IDENTITY_COLLAPSE_BLOCKED,
            FORBIDDEN_OUTPUT_ATTEMPTED,
        ),
        neutral_identity_domain="inflectional_closure_identity",
        output_candidate_type=output_candidate_type,
        forbidden_outputs=FORBIDDEN_INFLECTIONAL_CLOSURE,
        rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
    )


# ACCEPT → readiness candidate of the classified kind; DEFER/BLOCK → neutral umbrella.
MABNI_READINESS_RULE = _rule("MabniReadinessCandidate")
MURAB_READINESS_RULE = _rule("Mu'rabReadinessCandidate")
INFLECTIONAL_CLOSURE_RULE = _rule("InflectionalClosureCandidate")
