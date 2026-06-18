"""
VerbalSignifiedLayerAdapter — SCG-P6 adapter (information-gain layer).

Opens a verbal-signified carrier POSSIBILITY from a ``MufradWordCandidate``,
emitting a ``VerbalSignifiedCandidate`` (VERBAL_SIGNIFIED_CONSTITUTION.md).

SCG-P6 STRENGTHENING (2026-06-18): P6 is no longer a forwarding stamp. It READS
the upstream P5 verdict + word-unit/carrier geometry that ride on the
MufradWordCandidate's trace (``mufrad_unit_evidence:cv=…;nC=…;vowels=…;gem=…;verdict=…``)
and discriminates the VERBAL-SIGNIFIED CARRIER geometry into one of three
verdicts, routed through the kernel's residual machinery:

  ACCEPT : P5 ACCEPT and verbal-carrier geometry — n_consonants >= 2 AND
           ( (n_consonants >= 3 AND short-vowel cadence) OR gemination ).
  DEFER  : isolated word-unit support exists but verbal-carrier cadence is
           underspecified — e.g. a long-vowel-only CVVC unit (بَاب / بَيت) that
           P5 accepts as a word unit but which lacks verbal-carrier cadence —
           emits ``defer:verbal_carrier_underspecified:present``.
  BLOCK  : P5 was DEFER/BLOCK (non-accepted upstream), or no vowel geometry —
           emits ``فارق:signified_class_conflict:present``.

"Short-vowel cadence" is purely structural: the CV signature has NO adjacent
``VV`` (a long vowel), i.e. consonant/short-vowel alternation.

P6 means ONLY: "enough structural verbal-signification carrier geometry exists to
open a VerbalSignifiedCandidate." It is PRE-SEMANTIC and structural: NOT a verb /
فعل, NOT tense / aspect / mood / voice / person / number / gender, NOT
subject / object / agent / patient, NOT event meaning / dalalah / i'rab / hukm /
root / wazn / lemma. ``verbal_signified_prior_type`` is a STRUCTURAL carrier
class (input-dependent), never a linguistic label. It OPENS meaning + dalalah
PRIORS (ACCEPT only); it never produces meaning or dalalah.

Carried fields (on the output candidate's trace_ids, documented prefixes):
  mufrad_word_candidate_ref:<id>                    the consumed P5 candidate
  structural_signified_evidence:<sigsig:CV:cps>      input-dependent geometry
  verbal_signified_carrier_evidence:cv=..;nC=..;vowels=..;cadence=..;gem=..;p5verdict=..;verdict=..
  verbal_cadence_evidence:cadence=..;long_vowel=..
  signified_carrier_boundary_evidence:closed=..
  verbal_signified_prior_type:<structural class>     input-dependent (allowed set)
  opens_prior:meaning_priors / opens_prior:dalalah_priors   (ACCEPT only)
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .mufrad_word_adapter import MUFRAD_UNIT_EVIDENCE_PREFIX
from .node import QiyasNodeRef
from .rules.verbal_signified_rules import (
    GEMINATED_CARRIER_POSSIBILITY,
    OPENED_PRIORS,
    SHORT_VOWEL_CADENCE_PRIOR,
    SIGNIFIED_CLASS_CONFLICT,
    STRUCTURAL_SIGNIFIED_CARRIER_PRIOR,
    VERBAL_CARRIER_GEOMETRY_CLASS,
    VERBAL_CARRIER_UNDERSPECIFIED,
    VERBAL_SIGNIFIED_RULE,
)
from .typed_codepoint_adapter import is_arabic_letter

# Trace prefixes for the carried structural fields (read back by tests/tools).
MUFRAD_WORD_CANDIDATE_REF_PREFIX = "mufrad_word_candidate_ref:"
SIGNIFIED_EVIDENCE_PREFIX = "structural_signified_evidence:"
VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX = "verbal_signified_carrier_evidence:"
VERBAL_CADENCE_EVIDENCE_PREFIX = "verbal_cadence_evidence:"
SIGNIFIED_CARRIER_BOUNDARY_EVIDENCE_PREFIX = "signified_carrier_boundary_evidence:"
VERBAL_SIGNIFIED_PRIOR_TYPE_PREFIX = "verbal_signified_prior_type:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts (SCG-P6 discrimination).
VERDICT_ACCEPT_P6 = "accept"
VERDICT_DEFER_P6 = "defer"
VERDICT_BLOCK_P6 = "block"

_LONG_VOWEL_LETTERS = frozenset({0x0627, 0x0648, 0x064A, 0x0649, 0x0622})


def _parse_kv(trace_ids, prefix):
    for t in trace_ids:
        if t.startswith(prefix):
            out = {}
            for part in t[len(prefix):].split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    out[k] = v
            return out
    return {}


def _codepoints(candidate: Candidate) -> list[str]:
    return sorted(
        iid[len("identity:codepoint:"):]
        for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )


@dataclass(frozen=True)
class VerbalSignifiedCarrierProfile:
    """Structural verbal-signified carrier geometry P6 reads from the MufradWordCandidate."""

    p5_verdict: str
    cv_geometry: str
    n_consonants: int
    vowel_count: int
    has_gemination: bool
    has_closed_ending: bool

    @property
    def has_short_vowel_cadence(self) -> bool:
        # Structural: consonant/short-vowel alternation — no adjacent VV (long vowel).
        return self.vowel_count >= 1 and "VV" not in self.cv_geometry

    @property
    def has_long_vowel(self) -> bool:
        return "VV" in self.cv_geometry

    @property
    def verbal_carrier_sufficient(self) -> bool:
        if self.n_consonants < 2:
            return False
        if self.has_gemination:
            return True
        return self.n_consonants >= 3 and self.has_short_vowel_cadence

    @property
    def verdict(self) -> str:
        if self.p5_verdict and self.p5_verdict != VERDICT_ACCEPT_P6:
            return VERDICT_BLOCK_P6
        if self.n_consonants == 0 or self.vowel_count == 0:
            return VERDICT_BLOCK_P6
        if self.verbal_carrier_sufficient:
            return VERDICT_ACCEPT_P6
        return VERDICT_DEFER_P6

    @property
    def prior_type(self) -> str:
        if self.has_gemination:
            return GEMINATED_CARRIER_POSSIBILITY
        if self.n_consonants >= 3 and self.has_short_vowel_cadence:
            return SHORT_VOWEL_CADENCE_PRIOR
        if self.n_consonants >= 3:
            return VERBAL_CARRIER_GEOMETRY_CLASS
        return STRUCTURAL_SIGNIFIED_CARRIER_PRIOR


def _read_carrier_profile(mufrad_word: Candidate) -> VerbalSignifiedCarrierProfile:
    """Read P5's verdict + carrier geometry from the MufradWordCandidate trace.

    Falls back to deriving the consonant count from the candidate's own codepoints
    when no P5 evidence is present (e.g. a hand-built fixture)."""
    ev = _parse_kv(mufrad_word.trace_ids, MUFRAD_UNIT_EVIDENCE_PREFIX)
    cv = ev.get("cv", "")
    p5_verdict = ev.get("verdict", "")
    gem = ev.get("gem") == "1"

    if cv:
        n_consonants = cv.count("C")
        vowel_count = cv.count("V")
        closed_ending = cv.endswith("C")
    else:
        cps = [int(h, 16) for h in _codepoints(mufrad_word)]
        n_consonants = sum(
            1 for cp in cps if is_arabic_letter(cp) and cp not in _LONG_VOWEL_LETTERS
        )
        vowel_count = 0
        closed_ending = False

    if "nC" in ev:
        n_consonants = int(ev["nC"])
    if "vowels" in ev:
        vowel_count = int(ev["vowels"])
    if "closed" in ev:
        closed_ending = ev["closed"] == "1"

    return VerbalSignifiedCarrierProfile(
        p5_verdict=p5_verdict,
        cv_geometry=cv,
        n_consonants=n_consonants,
        vowel_count=vowel_count,
        has_gemination=gem,
        has_closed_ending=closed_ending,
    )


@dataclass
class VerbalSignifiedLayerAdapter:
    """Adapter that opens a verbal-signified carrier possibility (priors only)."""

    kernel: QiyasKernel

    def build_request(
        self,
        mufrad_word: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest opening a verbal-signified carrier possibility from
        a MufradWordCandidate (candidate-only; priors only). The verdict (ACCEPT /
        DEFER / BLOCK) and prior_type are driven by the carrier geometry read from P5."""
        profile = _read_carrier_profile(mufrad_word)
        verdict = profile.verdict
        prior_type = profile.prior_type

        slot_seq = "+".join(_codepoints(mufrad_word)) or "none"
        signature = f"sigsig:{profile.cv_geometry or 'none'}:{slot_seq}"

        if not trace_prefix:
            trace_prefix = f"verbal_signified:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:verbal_signified_domain",
            node_type="VerbalSignifiedDomain",
            identity_ids=("identity:verbal_signified_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The MufradWordCandidate rides on the far node — it preserves the
        # mufrad_word (and upstream) identities carried up from P5 (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:mufrad_word_candidate:{mufrad_word.candidate_id}",
            node_type="MufradWordCandidate",
            identity_ids=mufrad_word.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=mufrad_word.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_mufrad_word_candidate:evidenced",
            "وصف:structural_signified_possibility_derived:evidenced",
            "وصف:opens_meaning_priors:evidenced",
            "وصف:opens_dalalah_priors:evidenced",
            "وصف:mufrad_word_identity_preserved:evidenced",
            "علة:belongs_to_verbal_signified_domain:verified",
            "علة:verbal_signified_opening_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Verdict-specific claims — input-dependent, NOT hardcoded all-pass.
        if verdict == VERDICT_ACCEPT_P6:
            proves.append("وصف:verbal_carrier_consistent:evidenced")
        elif verdict == VERDICT_DEFER_P6:
            proves.append(f"defer:{VERBAL_CARRIER_UNDERSPECIFIED}:present")
        else:  # VERDICT_BLOCK_P6
            proves.append(f"فارق:{SIGNIFIED_CLASS_CONFLICT}:present")

        gem = "1" if profile.has_gemination else "0"
        cadence = "1" if profile.has_short_vowel_cadence else "0"
        long_v = "1" if profile.has_long_vowel else "0"
        closed = "1" if profile.has_closed_ending else "0"
        carrier_evidence = (
            f"cv={profile.cv_geometry or 'none'};nC={profile.n_consonants};"
            f"vowels={profile.vowel_count};cadence={cadence};gem={gem};"
            f"p5verdict={profile.p5_verdict or 'none'};verdict={verdict}"
        )
        carried_trace = [
            f"{MUFRAD_WORD_CANDIDATE_REF_PREFIX}{mufrad_word.candidate_id}",
            f"{SIGNIFIED_EVIDENCE_PREFIX}{signature}",
            f"{VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX}{carrier_evidence}",
            f"{VERBAL_CADENCE_EVIDENCE_PREFIX}cadence={cadence};long_vowel={long_v}",
            f"{SIGNIFIED_CARRIER_BOUNDARY_EVIDENCE_PREFIX}closed={closed}",
            f"{VERBAL_SIGNIFIED_PRIOR_TYPE_PREFIX}{prior_type}",
        ]
        # Meaning/dalalah PRIORS are opened only when the carrier opening is licensed.
        if verdict == VERDICT_ACCEPT_P6:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:verbal_signified:{uuid.uuid4().hex[:8]}",
                    source_layer="VerbalSignifiedQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=VERBAL_SIGNIFIED_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="VerbalSignifiedQiyas"),
        )

    def open(
        self,
        mufrad_word: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Open a verbal-signified carrier possibility from a MufradWordCandidate.

        The carrier geometry read from P5 drives the ACCEPT / DEFER / BLOCK verdict
        and the input-dependent prior_type."""
        return self.kernel.apply(self.build_request(mufrad_word, trace_prefix))
