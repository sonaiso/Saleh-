"""
InflectionalClosureLayerAdapter — P5.1 (Mabni / Mu'rab readiness).

AUXILIARY non-registry sub-pass. NOT a registered LayerSpec — the constitutional
registry count stays 19, there is no P13, and the P0–P12 spine is untouched.
Registered only in `LAYER_FORBIDDEN_OUTPUTS` via the same auxiliary pattern as
HarakaRoleSpectrumQiyas / SyllableQiyas.

Runs AFTER an accepted P5 `MufradWordCandidate` and BEFORE P6+ consumers, producing
candidate-only structural classification evidence — a BINARY partition of every
Arabic word token into exactly one of:
    MabniReadinessCandidate   (structurally closed / inherently mabni)
    Mu'rabReadinessCandidate  (open to i'rab / inflection)

CANDIDATE-ONLY / NON-FINAL: identity-preserving (I(c) preserves the P5
`mufrad_word_candidate_identity`), identity disjoint from trace, residual-preserving.
It NEVER emits a grammatical judgment, an i'rab position/sign/decision
(raf'/nasb/jarr/jazm), dalalah, ifadah, hukm, reality, or final meaning.

EVIDENCE DISCIPLINE: the adapter READS word-kind / closed-category evidence (from
explicit kwargs, or from the upstream candidate's trace markers) and DEFERs when that
evidence is absent. It NEVER fabricates closed-category membership ("this is a harf")
and NEVER lets a known closed-category token slip to mu'rab because it happens to have
wazn / root / weight / side morphology.

ARCHITECTURAL REFERENCE: the real reference for this classification is the full Quran
token inventory AFTER tokenization. No filtered fixture is ever presented as the whole
Quran; full-Quran token-inventory completeness is a separate governed follow-up task
(requires an approved in-repo corpus snapshot/data contract). The classifier is
designed for that full inventory; current tests use honestly-labelled fixtures.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .forbidden_outputs import FORBIDDEN_INFLECTIONAL_CLOSURE
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.inflectional_closure_rules import (
    CLASS_MABNI,
    CLASS_MURAB,
    INFLECTIONAL_CLOSURE_RULE,
    MABNI_READINESS_RULE,
    MURAB_READINESS_RULE,
    VERDICT_ACCEPT,
    VERDICT_BLOCK,
    VERDICT_DEFER,
    classify_inflectional_closure,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
MUFRAD_WORD_REF_PREFIX = "mufrad_word_ref:"
INFLECTIONAL_CLOSURE_EVIDENCE_PREFIX = "inflectional_closure_evidence:"
CLASSIFICATION_TRACE_PREFIX = "inflectional_classification:"
WORD_KIND_TRACE_PREFIX = "word_kind:"
TOKEN_SURFACE_PREFIX = "token_surface:"

# Evidence markers the adapter reads off the upstream candidate when kwargs are absent.
_M_WORD_KIND = "word_kind:"
_M_CLOSED_CATEGORY = "closed_category:"
_M_VERB_TENSE = "verb_tense:"
_M_CLOSED_COMPOUND = "is_closed_compound:"
_M_FAWATIH = "is_fawatih:"
_M_DERIVED = "is_derived:"
_M_SURFACE = "token_surface:"

_FORBIDDEN_EVIDENCE_TOKENS = frozenset(FORBIDDEN_INFLECTIONAL_CLOSURE)


def _read_marker(candidate: Candidate, prefix: str):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


def _read_flag(candidate: Candidate, prefix: str) -> bool:
    v = _read_marker(candidate, prefix)
    return v == "1"


@dataclass
class InflectionalClosureLayerAdapter:
    """Adapter classifying a P5 MufradWordCandidate into mabni / mu'rab readiness."""

    kernel: QiyasKernel

    def build_request(
        self,
        mufrad_word: Candidate | None,
        *,
        word_kind=None,
        closed_category=None,
        verb_tense=None,
        is_closed_compound: bool | None = None,
        is_fawatih: bool | None = None,
        is_derived: bool | None = None,
        class_conflict: bool = False,
        identity_determined: bool = True,
        token_surface: str | None = None,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        # Evidence resolution: explicit kwargs win; otherwise read upstream trace markers.
        if mufrad_word is not None:
            if word_kind is None:
                word_kind = _read_marker(mufrad_word, _M_WORD_KIND)
            if closed_category is None:
                closed_category = _read_marker(mufrad_word, _M_CLOSED_CATEGORY)
            if verb_tense is None:
                verb_tense = _read_marker(mufrad_word, _M_VERB_TENSE)
            if is_closed_compound is None:
                is_closed_compound = _read_flag(mufrad_word, _M_CLOSED_COMPOUND)
            if is_fawatih is None:
                is_fawatih = _read_flag(mufrad_word, _M_FAWATIH)
            if is_derived is None:
                is_derived = _read_flag(mufrad_word, _M_DERIVED)
            if token_surface is None:
                token_surface = _read_marker(mufrad_word, _M_SURFACE)

        has_identity = mufrad_word is not None and bool(mufrad_word.identity_ids)
        carried_residuals = mufrad_word is not None and bool(mufrad_word.residuals)
        forbidden_attempted = mufrad_word is not None and any(
            any(tok in t for tok in _FORBIDDEN_EVIDENCE_TOKENS)
            for t in mufrad_word.trace_ids
        )

        verdict, classification, reason = classify_inflectional_closure(
            has_identity=has_identity,
            identity_determined=identity_determined,
            carried_residuals=carried_residuals,
            forbidden_attempted=forbidden_attempted,
            class_conflict=class_conflict,
            word_kind=word_kind,
            closed_category=closed_category,
            verb_tense=verb_tense,
            is_closed_compound=bool(is_closed_compound),
            is_fawatih=bool(is_fawatih),
            is_derived=bool(is_derived),
        )

        # Select the rule: ACCEPT → readiness candidate of the classified kind;
        # DEFER/BLOCK → neutral umbrella InflectionalClosureCandidate (not counted).
        if verdict == VERDICT_ACCEPT and classification == CLASS_MABNI:
            rule = MABNI_READINESS_RULE
        elif verdict == VERDICT_ACCEPT and classification == CLASS_MURAB:
            rule = MURAB_READINESS_RULE
        else:
            rule = INFLECTIONAL_CLOSURE_RULE

        preserved_ids: tuple = (
            tuple(dict.fromkeys(mufrad_word.identity_ids))
            if mufrad_word is not None else tuple()
        )
        mw_ref = mufrad_word.candidate_id if mufrad_word is not None else "none"
        surface = token_surface or "—"

        if not trace_prefix:
            trace_prefix = "inflectional_closure"

        asl = QiyasNodeRef(
            node_id="اصل:inflectional_closure_domain",
            node_type="InflectionalClosureDomain",
            identity_ids=("identity:inflectional_closure_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )
        # The accepted P5 mufrad word rides on the far node — preserves its identity.
        far = QiyasNodeRef(
            node_id=f"فرع:mufrad_word:{uuid.uuid4().hex[:8]}",
            node_type="MufradWordCandidate",
            identity_ids=preserved_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_mufrad_word_ref:evidenced",
            "وصف:has_word_kind_evidence:evidenced",
            "وصف:inflectional_closure_classified:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_inflectional_closure_domain:verified",
            "علة:inflectional_closure_classification_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]
        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:inflectional_closure_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            proves.append(f"defer:{reason}:present")
        else:  # VERDICT_BLOCK
            proves.append(f"فارق:{reason}:present")

        carried_trace = [
            f"{MUFRAD_WORD_REF_PREFIX}{mw_ref}",
            f"{TOKEN_SURFACE_PREFIX}{surface}",
            f"{WORD_KIND_TRACE_PREFIX}{word_kind or 'unknown'}",
            f"{CLASSIFICATION_TRACE_PREFIX}{classification or 'unclassified'}",
            f"{INFLECTIONAL_CLOSURE_EVIDENCE_PREFIX}"
            f"classification={classification or 'unclassified'};reason={reason};"
            f"verdict={verdict}",
        ]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:inflectional_closure:{uuid.uuid4().hex[:8]}",
                    source_layer="InflectionalClosureQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=rule,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="InflectionalClosureQiyas"),
        )

    def classify(
        self,
        mufrad_word: Candidate | None,
        *,
        word_kind=None,
        closed_category=None,
        verb_tense=None,
        is_closed_compound: bool | None = None,
        is_fawatih: bool | None = None,
        is_derived: bool | None = None,
        class_conflict: bool = False,
        identity_determined: bool = True,
        token_surface: str | None = None,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Classify a single accepted P5 MufradWordCandidate into mabni / mu'rab
        readiness (candidate-only). ACCEPT → MabniReadinessCandidate /
        Mu'rabReadinessCandidate; DEFER when evidence is underspecified (never guessed);
        BLOCK on contradiction or a forbidden-output attempt.
        """
        return self.kernel.apply(
            self.build_request(
                mufrad_word,
                word_kind=word_kind,
                closed_category=closed_category,
                verb_tense=verb_tense,
                is_closed_compound=is_closed_compound,
                is_fawatih=is_fawatih,
                is_derived=is_derived,
                class_conflict=class_conflict,
                identity_determined=identity_determined,
                token_surface=token_surface,
                trace_prefix=trace_prefix,
            )
        )
