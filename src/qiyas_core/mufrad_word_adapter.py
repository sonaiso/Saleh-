"""
MufradWordLayerAdapter — SCG-P5 adapter (information-gain layer).

Forms a candidate-only single-word-unit POSSIBILITY from a ``JamidMushtaqCandidate``,
emitting a ``MufradWordCandidate`` (MUFRAD_WORD_CONSTITUTION.md).

SCG-P5 STRENGTHENING (2026-06-18): P5 is no longer a forwarding stamp. It READS
the upstream P4 verdict + word-unit geometry that ride on the JamidMushtaqCandidate's
trace (``derivation_geometry_evidence:cv=…;nC=…;gem=…;verdict=…``) and discriminates
the ISOLATED-WORD-UNIT geometry into one of three verdicts, routed through the
kernel's residual machinery:

  ACCEPT : P4 ACCEPT and enough isolated-word-unit body — n_consonants >= 2 AND
           at least one of {>=2 vowels, closed ending, gemination}.
  DEFER  : word-unit geometry too thin to open an isolated unit (e.g. a bare
           consonant cluster with a single open vowel) — emits
           ``defer:word_unit_underspecified:present``.
  BLOCK  : P4 was DEFER/BLOCK (non-accepted upstream), or geometry conflicts —
           emits ``فارق:word_class_conflict:present``.

P5 means ONLY: "enough structural isolated-word-unit geometry exists to open a
MufradWordCandidate." It is NOT a final word / مفرد / singular / noun / verb /
جامد / مشتق judgment, NOT wazn / root / lemma / dictionary entry, NOT meaning /
dalalah / i'rab / syntax / hukm. ``mufrad_word_prior_type`` is a STRUCTURAL
word-unit class (selected input-dependently), never a linguistic label.

Carried fields (on the output candidate's trace_ids, documented prefixes):
  jamid_mushtaq_candidate_ref:<id>                 the consumed P4 candidate
  structural_wordhood_evidence:<wordsig:CV:cps>     input-dependent geometry
  structural_word_boundary_evidence:closed=..;ending=..   input-dependent boundary
  slot_sequence_refs:<codepoints>                   structural slot-sequence refs
  mufrad_unit_evidence:cv=..;nC=..;vowels=..;closed=..;gem=..;p4verdict=..;verdict=..
  mufrad_word_prior_type:<structural class>         input-dependent (allowed set)
  opens_prior:verbal_signified_candidates / opens_prior:phrase_level_priors
      priors opened for SCG-P6 (ACCEPT only), NEVER produced here.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .jamid_mushtaq_adapter import DERIVATION_GEOMETRY_EVIDENCE_PREFIX
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.mufrad_word_rules import (
    ISOLATED_UNIT_BOUNDARY_PRIOR,
    MUFRAD_UNIT_GEOMETRY_CLASS,
    MUFRAD_WORD_RULE,
    OPENED_PRIORS,
    STRUCTURAL_WORD_UNIT_PRIOR,
    WORD_CLASS_CONFLICT,
    WORD_UNIT_SHAPE_POSSIBILITY,
    WORD_UNIT_UNDERSPECIFIED,
)
from .typed_codepoint_adapter import is_arabic_letter

# Trace prefixes for the carried structural fields (read back by tests/tools).
JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX = "jamid_mushtaq_candidate_ref:"
WORDHOOD_EVIDENCE_PREFIX = "structural_wordhood_evidence:"
WORD_BOUNDARY_EVIDENCE_PREFIX = "structural_word_boundary_evidence:"
SLOT_SEQUENCE_REFS_PREFIX = "slot_sequence_refs:"
MUFRAD_UNIT_EVIDENCE_PREFIX = "mufrad_unit_evidence:"
MUFRAD_WORD_PRIOR_TYPE_PREFIX = "mufrad_word_prior_type:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts (SCG-P5 discrimination).
VERDICT_ACCEPT_P5 = "accept"
VERDICT_DEFER_P5 = "defer"
VERDICT_BLOCK_P5 = "block"

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
class MufradUnitProfile:
    """Structural isolated-word-unit geometry P5 reads from the JamidMushtaqCandidate."""

    p4_verdict: str
    cv_geometry: str
    n_consonants: int
    vowel_count: int
    has_long_vowel: bool
    has_gemination: bool
    has_closed_ending: bool

    @property
    def word_unit_sufficient(self) -> bool:
        return self.vowel_count >= 2 or self.has_closed_ending or self.has_gemination

    @property
    def verdict(self) -> str:
        if self.p4_verdict and self.p4_verdict != VERDICT_ACCEPT_P5:
            return VERDICT_BLOCK_P5
        if self.n_consonants == 0:
            return VERDICT_BLOCK_P5
        if self.n_consonants >= 2 and self.word_unit_sufficient:
            return VERDICT_ACCEPT_P5
        return VERDICT_DEFER_P5  # too thin to open an isolated word unit

    @property
    def prior_type(self) -> str:
        if self.has_gemination:
            return WORD_UNIT_SHAPE_POSSIBILITY
        if self.has_closed_ending:
            return ISOLATED_UNIT_BOUNDARY_PRIOR
        if self.vowel_count >= 2:
            return MUFRAD_UNIT_GEOMETRY_CLASS
        return STRUCTURAL_WORD_UNIT_PRIOR


def _read_mufrad_unit_profile(jamid_mushtaq: Candidate) -> MufradUnitProfile:
    """Read P4's verdict + word-unit geometry from the JamidMushtaqCandidate trace.

    Falls back to deriving the consonant count from the candidate's own codepoints
    when no P4 evidence is present (e.g. a hand-built fixture)."""
    ev = _parse_kv(jamid_mushtaq.trace_ids, DERIVATION_GEOMETRY_EVIDENCE_PREFIX)
    cv = ev.get("cv", "")
    p4_verdict = ev.get("verdict", "")
    gem = ev.get("gem") == "1"

    if cv:
        n_consonants = cv.count("C")
        vowel_count = cv.count("V")
        closed_ending = cv.endswith("C")
    else:
        cps = [int(h, 16) for h in _codepoints(jamid_mushtaq)]
        n_consonants = sum(
            1 for cp in cps if is_arabic_letter(cp) and cp not in _LONG_VOWEL_LETTERS
        )
        vowel_count = 0
        closed_ending = False

    if "nC" in ev:
        n_consonants = int(ev["nC"])
    has_long_vowel = "V" in cv  # structural: a vocalic position present

    return MufradUnitProfile(
        p4_verdict=p4_verdict,
        cv_geometry=cv,
        n_consonants=n_consonants,
        vowel_count=vowel_count,
        has_long_vowel=has_long_vowel,
        has_gemination=gem,
        has_closed_ending=closed_ending,
    )


@dataclass
class MufradWordLayerAdapter:
    """Adapter that forms a candidate-only single-word-unit possibility."""

    kernel: QiyasKernel

    def build_request(
        self,
        jamid_mushtaq: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest forming a single-word-unit possibility from a
        JamidMushtaqCandidate (candidate-only). The verdict (ACCEPT / DEFER /
        BLOCK) and prior_type are driven by the word-unit geometry read from P4."""
        profile = _read_mufrad_unit_profile(jamid_mushtaq)
        verdict = profile.verdict
        prior_type = profile.prior_type

        slot_seq = "+".join(_codepoints(jamid_mushtaq)) or "none"
        signature = f"wordsig:{profile.cv_geometry or 'none'}:{slot_seq}"

        if not trace_prefix:
            trace_prefix = f"mufrad_word:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:mufrad_word_domain",
            node_type="MufradWordDomain",
            identity_ids=("identity:mufrad_word_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The JamidMushtaqCandidate rides on the far node — it preserves the
        # upstream (root/stem/slot) identities carried up from P4 (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:jamid_mushtaq_candidate:{jamid_mushtaq.candidate_id}",
            node_type="JamidMushtaqCandidate",
            identity_ids=jamid_mushtaq.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=jamid_mushtaq.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_jamid_mushtaq_candidate:evidenced",
            "وصف:structural_wordhood_evidence_derived:evidenced",
            "وصف:has_structural_word_boundary_evidence:evidenced",
            "وصف:has_slot_sequence_refs:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_mufrad_word_domain:verified",
            "علة:mufrad_word_formation_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Verdict-specific claims — input-dependent, NOT hardcoded all-pass.
        if verdict == VERDICT_ACCEPT_P5:
            proves.append("وصف:word_unit_consistent:evidenced")
        elif verdict == VERDICT_DEFER_P5:
            proves.append(f"defer:{WORD_UNIT_UNDERSPECIFIED}:present")
        else:  # VERDICT_BLOCK_P5
            proves.append(f"فارق:{WORD_CLASS_CONFLICT}:present")

        gem = "1" if profile.has_gemination else "0"
        closed = "1" if profile.has_closed_ending else "0"
        ending = "closed" if profile.has_closed_ending else "open"
        unit_evidence = (
            f"cv={profile.cv_geometry or 'none'};nC={profile.n_consonants};"
            f"vowels={profile.vowel_count};closed={closed};gem={gem};"
            f"p4verdict={profile.p4_verdict or 'none'};verdict={verdict}"
        )
        carried_trace = [
            f"{JAMID_MUSHTAQ_CANDIDATE_REF_PREFIX}{jamid_mushtaq.candidate_id}",
            f"{WORDHOOD_EVIDENCE_PREFIX}{signature}",
            f"{WORD_BOUNDARY_EVIDENCE_PREFIX}closed={closed};ending={ending}",
            f"{SLOT_SEQUENCE_REFS_PREFIX}{slot_seq}",
            f"{MUFRAD_UNIT_EVIDENCE_PREFIX}{unit_evidence}",
            f"{MUFRAD_WORD_PRIOR_TYPE_PREFIX}{prior_type}",
        ]
        # Priors are opened only when the word-unit opening is licensed (ACCEPT).
        if verdict == VERDICT_ACCEPT_P5:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:mufrad_word:{uuid.uuid4().hex[:8]}",
                    source_layer="MufradWordQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=MUFRAD_WORD_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="MufradWordQiyas"),
        )

    def form(
        self,
        jamid_mushtaq: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Form a single-word-unit possibility from a JamidMushtaqCandidate.

        The word-unit geometry read from P4 drives the ACCEPT / DEFER / BLOCK
        verdict and the input-dependent prior_type."""
        return self.kernel.apply(self.build_request(jamid_mushtaq, trace_prefix))
