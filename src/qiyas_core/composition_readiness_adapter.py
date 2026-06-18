"""
CompositionReadinessLayerAdapter — SCG-P7 adapter (information-gain layer).

Attests structural READINESS to enter composition from a
``VerbalSignifiedCandidate``, emitting a ``CompositionReadinessCandidate``
(COMPOSITION_READINESS_CONSTITUTION.md).

SCG-P7 STRENGTHENING (2026-06-18): P7 is no longer a forwarding stamp. It READS
the upstream P6 verdict + carrier geometry that ride on the VerbalSignifiedCandidate's
trace (``verbal_signified_carrier_evidence:cv=…;nC=…;cadence=…;gem=…;verdict=…``)
and discriminates the COMPOSITION-READINESS geometry into one of three verdicts,
routed through the kernel's residual machinery:

  ACCEPT : P6 ACCEPT and a clean composition boundary — short-vowel cadence
           AND n_consonants >= 3 (an unambiguous operand for composition).
  DEFER  : P6-accepted carrier whose composition boundary is ambiguous — e.g. a
           long-vowel-heavy / non-cadence shape (شَاذّ: CVVCC) that P6 accepts via
           gemination but which is under-specified as a composition operand —
           emits ``defer:composition_readiness_underspecified:present``.
  BLOCK  : P6 was DEFER/BLOCK (non-accepted upstream), or no usable geometry —
           emits ``فارق:composition_readiness_conflict:present``.

This is the readiness GATE, not actual composition: P7 attests readiness; it
performs NO composition, NO syntax, NO amil/mamul relation, NO i'rab, NO final
word-type / meaning / dalalah / hukm. ``composition_readiness_prior_type`` is a
STRUCTURAL readiness class (input-dependent), never a linguistic label. It OPENS
amil/mamul + sentence-geometry PRIORS (ACCEPT only); it never produces them.

Carried fields (on the output candidate's trace_ids, documented prefixes):
  verbal_signified_candidate_ref:<id>             the consumed P6 candidate
  structural_composability_profile:<compsig:CV:cps>  input-dependent geometry
  composition_readiness_structural_evidence:cv=..;nC=..;cadence=..;gem=..;p6verdict=..;verdict=..
  composition_boundary_evidence:closed=..;cadence=..
  composition_readiness_prior_type:<structural class>  input-dependent (allowed set)
  opens_prior:amil_mamul_relation_priors / opens_prior:sentence_geometry_priors  (ACCEPT only)
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.composition_readiness_rules import (
    CADENCE_BOUNDARY_PRIOR,
    COMPOSITION_PRECONDITION_BLOCKED,
    COMPOSITION_READINESS_GEOMETRY_CLASS,
    COMPOSITION_READINESS_RULE,
    COMPOSITION_READINESS_UNDERSPECIFIED,
    GEMINATED_READINESS_POSSIBILITY,
    OPENED_PRIORS,
    STRUCTURAL_READINESS_PRIOR,
)
from .typed_codepoint_adapter import is_arabic_letter
from .verbal_signified_adapter import VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX

# Trace prefixes for the carried structural fields (read back by tests/tools).
VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX = "verbal_signified_candidate_ref:"
COMPOSABILITY_PROFILE_PREFIX = "structural_composability_profile:"
READINESS_EVIDENCE_PREFIX = "composition_readiness_structural_evidence:"
COMPOSITION_BOUNDARY_EVIDENCE_PREFIX = "composition_boundary_evidence:"
COMPOSITION_READINESS_PRIOR_TYPE_PREFIX = "composition_readiness_prior_type:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts (SCG-P7 discrimination).
VERDICT_ACCEPT_P7 = "accept"
VERDICT_DEFER_P7 = "defer"
VERDICT_BLOCK_P7 = "block"

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
class CompositionReadinessProfile:
    """Structural composition-readiness geometry P7 reads from the VerbalSignifiedCandidate."""

    p6_verdict: str
    cv_geometry: str
    n_consonants: int
    has_short_vowel_cadence: bool
    has_gemination: bool
    has_closed_ending: bool

    @property
    def composition_ready(self) -> bool:
        # A clean composition operand: short-vowel cadence over a >=3 consonant
        # skeleton (unambiguous boundary). Gemination alone (without cadence) is
        # carrier-sufficient (P6) but boundary-ambiguous for composition (P7).
        return self.has_short_vowel_cadence and self.n_consonants >= 3

    @property
    def verdict(self) -> str:
        if self.p6_verdict and self.p6_verdict != VERDICT_ACCEPT_P7:
            return VERDICT_BLOCK_P7
        if self.n_consonants == 0:
            return VERDICT_BLOCK_P7
        if self.composition_ready:
            return VERDICT_ACCEPT_P7
        return VERDICT_DEFER_P7

    @property
    def prior_type(self) -> str:
        if self.has_closed_ending and self.has_short_vowel_cadence:
            return CADENCE_BOUNDARY_PRIOR
        if self.n_consonants >= 3 and self.has_short_vowel_cadence:
            return COMPOSITION_READINESS_GEOMETRY_CLASS
        if self.has_gemination:
            return GEMINATED_READINESS_POSSIBILITY
        return STRUCTURAL_READINESS_PRIOR


def _read_readiness_profile(verbal_signified: Candidate) -> CompositionReadinessProfile:
    """Read P6's verdict + carrier geometry from the VerbalSignifiedCandidate trace.

    Falls back to deriving the consonant count from the candidate's own codepoints
    when no P6 evidence is present (e.g. a hand-built fixture)."""
    ev = _parse_kv(verbal_signified.trace_ids, VERBAL_SIGNIFIED_CARRIER_EVIDENCE_PREFIX)
    cv = ev.get("cv", "")
    p6_verdict = ev.get("verdict", "")
    gem = ev.get("gem") == "1"
    cadence = ev.get("cadence") == "1"

    if cv:
        n_consonants = cv.count("C")
        closed_ending = cv.endswith("C")
    else:
        cps = [int(h, 16) for h in _codepoints(verbal_signified)]
        n_consonants = sum(
            1 for cp in cps if is_arabic_letter(cp) and cp not in _LONG_VOWEL_LETTERS
        )
        closed_ending = False

    if "nC" in ev:
        n_consonants = int(ev["nC"])

    return CompositionReadinessProfile(
        p6_verdict=p6_verdict,
        cv_geometry=cv,
        n_consonants=n_consonants,
        has_short_vowel_cadence=cadence,
        has_gemination=gem,
        has_closed_ending=closed_ending,
    )


@dataclass
class CompositionReadinessLayerAdapter:
    """Adapter that attests structural readiness to enter composition."""

    kernel: QiyasKernel

    def build_request(
        self,
        verbal_signified: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest attesting composition readiness from a
        VerbalSignifiedCandidate (candidate-only). The verdict (ACCEPT / DEFER /
        BLOCK) and prior_type are driven by the readiness geometry read from P6."""
        profile = _read_readiness_profile(verbal_signified)
        verdict = profile.verdict
        prior_type = profile.prior_type

        slot_seq = "+".join(_codepoints(verbal_signified)) or "none"
        signature = f"compsig:{profile.cv_geometry or 'none'}:{slot_seq}"

        if not trace_prefix:
            trace_prefix = f"composition_readiness:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:composition_readiness_domain",
            node_type="CompositionReadinessDomain",
            identity_ids=("identity:composition_readiness_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The VerbalSignifiedCandidate rides on the far node — it preserves the
        # verbal-signified (and upstream) identities carried up from P6 (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:verbal_signified_candidate:{verbal_signified.candidate_id}",
            node_type="VerbalSignifiedCandidate",
            identity_ids=verbal_signified.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=verbal_signified.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_verbal_signified_candidate:evidenced",
            "وصف:structural_composability_profile_derived:evidenced",
            "وصف:has_composition_readiness_evidence:evidenced",
            "وصف:has_slot_sequence_refs:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_composition_readiness_domain:verified",
            "علة:composition_readiness_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Verdict-specific claims — input-dependent, NOT hardcoded all-pass.
        if verdict == VERDICT_ACCEPT_P7:
            proves.append("وصف:composition_boundary_consistent:evidenced")
        elif verdict == VERDICT_DEFER_P7:
            proves.append(f"defer:{COMPOSITION_READINESS_UNDERSPECIFIED}:present")
        else:  # VERDICT_BLOCK_P7
            proves.append(f"فارق:{COMPOSITION_PRECONDITION_BLOCKED}:present")

        gem = "1" if profile.has_gemination else "0"
        cadence = "1" if profile.has_short_vowel_cadence else "0"
        closed = "1" if profile.has_closed_ending else "0"
        readiness_evidence = (
            f"cv={profile.cv_geometry or 'none'};nC={profile.n_consonants};"
            f"cadence={cadence};gem={gem};"
            f"p6verdict={profile.p6_verdict or 'none'};verdict={verdict}"
        )
        carried_trace = [
            f"{VERBAL_SIGNIFIED_CANDIDATE_REF_PREFIX}{verbal_signified.candidate_id}",
            f"{COMPOSABILITY_PROFILE_PREFIX}{signature}",
            f"{READINESS_EVIDENCE_PREFIX}{readiness_evidence}",
            f"{COMPOSITION_BOUNDARY_EVIDENCE_PREFIX}closed={closed};cadence={cadence}",
            f"{COMPOSITION_READINESS_PRIOR_TYPE_PREFIX}{prior_type}",
        ]
        # amil/mamul + sentence-geometry PRIORS opened only when readiness licensed.
        if verdict == VERDICT_ACCEPT_P7:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:composition_readiness:{uuid.uuid4().hex[:8]}",
                    source_layer="CompositionReadinessQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=COMPOSITION_READINESS_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="CompositionReadinessQiyas"),
        )

    def attest(
        self,
        verbal_signified: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Attest composition readiness from a VerbalSignifiedCandidate.

        The readiness geometry read from P6 drives the ACCEPT / DEFER / BLOCK
        verdict and the input-dependent prior_type."""
        return self.kernel.apply(self.build_request(verbal_signified, trace_prefix))
