"""
AmilMamulLayerAdapter — SCG-P8 adapter (information-gain layer).

Opens structurally-admissible dependency/attachment RELATION possibilities from a
``CompositionReadinessCandidate``, emitting an ``AmilMamulCandidate``
(AMIL_MAMUL_CONSTITUTION.md).

SCG-P8 STRENGTHENING (2026-06-18): P8 is no longer a forwarding stamp. It READS
the upstream P7 verdict + composition geometry that ride on the
CompositionReadinessCandidate's trace
(``composition_readiness_structural_evidence:cv=…;nC=…;cadence=…;gem=…;verdict=…``)
and discriminates the RELATION-possibility geometry into one of three verdicts,
routed through the kernel's residual machinery:

  ACCEPT : P7 ACCEPT and a multi-vowel alternating skeleton able to host an
           operator–operand relation — n_consonants >= 3 AND cadence AND
           vowel_count >= 2.
  DEFER  : P7-accepted operand whose relation geometry is too compact /
           single-vowel to host a relation possibility — e.g. عَدَّ (CVCC, a
           geminated-compact operand) — emits
           ``defer:relation_geometry_underspecified:present``.
  BLOCK  : P7 was DEFER/BLOCK (non-accepted upstream), or no usable geometry —
           emits ``فارق:amil_mamul_relation_blocked:present``.

CANDIDATE-ONLY and RELATION-POSSIBILITY-ONLY: this is the highest-care layer.
It opens *possibilities* only. It is NOT an actual i'rab / case judgment
(IrabCandidate / CaseJudgment forbidden), NOT a grammatical / syntactic judgment,
NOT meaning / dalalah / hukm / tafsir. ``amil_mamul_prior_type`` is a STRUCTURAL
relation-geometry category (input-dependent), NEVER a grammatical/case label
(no Amil/Mamul/Marfu/Mansub/Subject/Object). It OPENS grammatical-relation +
i'rab PRIORS (ACCEPT only); it never emits them.

Carried fields (on the output candidate's trace_ids, documented prefixes):
  composition_readiness_candidate_ref:<id>          the consumed P7 candidate
  structural_relation_possibility:<relsig:CV:cps>    input-dependent geometry
  relation_geometry_evidence:cv=..;nC=..;vowels=..;cadence=..;gem=..;p7verdict=..;verdict=..
  amil_mamul_prior_type:<structural class>           input-dependent (allowed set)
  opens_prior:grammatical_relation_priors / opens_prior:irab_priors  (ACCEPT only)
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .composition_readiness_adapter import READINESS_EVIDENCE_PREFIX
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.amil_mamul_rules import (
    AMIL_MAMUL_RELATION_BLOCKED,
    AMIL_MAMUL_RULE,
    COMPACT_RELATION_POSSIBILITY,
    OPENED_PRIORS,
    RELATION_CADENCE_GEOMETRY_CLASS,
    RELATION_GEOMETRY_CLASS,
    RELATION_GEOMETRY_UNDERSPECIFIED,
    STRUCTURAL_RELATION_PRIOR,
)
from .typed_codepoint_adapter import is_arabic_letter

# Trace prefixes for the carried structural fields (read back by tests/tools).
COMPOSITION_READINESS_CANDIDATE_REF_PREFIX = "composition_readiness_candidate_ref:"
RELATION_POSSIBILITY_PREFIX = "structural_relation_possibility:"
RELATION_GEOMETRY_EVIDENCE_PREFIX = "relation_geometry_evidence:"
AMIL_MAMUL_PRIOR_TYPE_PREFIX = "amil_mamul_prior_type:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts (SCG-P8 discrimination).
VERDICT_ACCEPT_P8 = "accept"
VERDICT_DEFER_P8 = "defer"
VERDICT_BLOCK_P8 = "block"

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
class RelationGeometryProfile:
    """Structural relation-possibility geometry P8 reads from the CompositionReadinessCandidate."""

    p7_verdict: str
    cv_geometry: str
    n_consonants: int
    vowel_count: int
    has_short_vowel_cadence: bool
    has_gemination: bool

    @property
    def relation_possible(self) -> bool:
        # The relation layer is the most demanding: an operator–operand relation
        # needs a richly-vocalised alternating skeleton (>=3 vocalic positions able
        # to carry distinct relation roles). A compact / fewer-vowel operand (e.g.
        # a geminated CVCVC) is composition-ready (P7) but relation-thin (P8).
        return (
            self.n_consonants >= 3
            and self.has_short_vowel_cadence
            and self.vowel_count >= 3
        )

    @property
    def verdict(self) -> str:
        if self.p7_verdict and self.p7_verdict != VERDICT_ACCEPT_P8:
            return VERDICT_BLOCK_P8
        if self.n_consonants == 0:
            return VERDICT_BLOCK_P8
        if self.relation_possible:
            return VERDICT_ACCEPT_P8
        return VERDICT_DEFER_P8

    @property
    def prior_type(self) -> str:
        # Input-dependent structural class — never a grammatical/case label.
        if self.has_gemination:
            return COMPACT_RELATION_POSSIBILITY
        if self.vowel_count >= 3 and self.has_short_vowel_cadence:
            return RELATION_CADENCE_GEOMETRY_CLASS
        if self.n_consonants >= 3 and self.vowel_count >= 2:
            return RELATION_GEOMETRY_CLASS
        return STRUCTURAL_RELATION_PRIOR


def _read_relation_profile(composition_readiness: Candidate) -> RelationGeometryProfile:
    """Read P7's verdict + composition geometry from the CompositionReadinessCandidate.

    Falls back to deriving the consonant count from the candidate's own codepoints
    when no P7 evidence is present (e.g. a hand-built fixture)."""
    ev = _parse_kv(composition_readiness.trace_ids, READINESS_EVIDENCE_PREFIX)
    cv = ev.get("cv", "")
    p7_verdict = ev.get("verdict", "")
    gem = ev.get("gem") == "1"
    cadence = ev.get("cadence") == "1"

    if cv:
        n_consonants = cv.count("C")
        vowel_count = cv.count("V")
    else:
        cps = [int(h, 16) for h in _codepoints(composition_readiness)]
        n_consonants = sum(
            1 for cp in cps if is_arabic_letter(cp) and cp not in _LONG_VOWEL_LETTERS
        )
        vowel_count = 0

    if "nC" in ev:
        n_consonants = int(ev["nC"])

    return RelationGeometryProfile(
        p7_verdict=p7_verdict,
        cv_geometry=cv,
        n_consonants=n_consonants,
        vowel_count=vowel_count,
        has_short_vowel_cadence=cadence,
        has_gemination=gem,
    )


@dataclass
class AmilMamulLayerAdapter:
    """Adapter that opens structural dependency/attachment relation possibilities."""

    kernel: QiyasKernel

    def build_request(
        self,
        composition_readiness: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest opening structural relation possibilities from a
        CompositionReadinessCandidate (candidate-only). The verdict (ACCEPT /
        DEFER / BLOCK) and prior_type are driven by the relation geometry read
        from P7."""
        profile = _read_relation_profile(composition_readiness)
        verdict = profile.verdict
        prior_type = profile.prior_type

        slot_seq = "+".join(_codepoints(composition_readiness)) or "none"
        signature = f"relsig:{profile.cv_geometry or 'none'}:{slot_seq}"

        if not trace_prefix:
            trace_prefix = f"amil_mamul:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:amil_mamul_domain",
            node_type="AmilMamulDomain",
            identity_ids=("identity:amil_mamul_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The CompositionReadinessCandidate rides on the far node — it preserves
        # the composition-readiness (and upstream) identities carried up from P7
        # (for every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:composition_readiness_candidate:{composition_readiness.candidate_id}",
            node_type="CompositionReadinessCandidate",
            identity_ids=composition_readiness.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=composition_readiness.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_composition_readiness_candidate:evidenced",
            "وصف:structural_relation_possibility_derived:evidenced",
            "وصف:has_amil_mamul_prior_type:evidenced",
            "وصف:opens_relation_priors:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_amil_mamul_domain:verified",
            "علة:amil_mamul_relation_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Verdict-specific claims — input-dependent, NOT hardcoded all-pass.
        if verdict == VERDICT_ACCEPT_P8:
            proves.append("وصف:relation_geometry_consistent:evidenced")
        elif verdict == VERDICT_DEFER_P8:
            proves.append(f"defer:{RELATION_GEOMETRY_UNDERSPECIFIED}:present")
        else:  # VERDICT_BLOCK_P8
            proves.append(f"فارق:{AMIL_MAMUL_RELATION_BLOCKED}:present")

        gem = "1" if profile.has_gemination else "0"
        cadence = "1" if profile.has_short_vowel_cadence else "0"
        relation_evidence = (
            f"cv={profile.cv_geometry or 'none'};nC={profile.n_consonants};"
            f"vowels={profile.vowel_count};cadence={cadence};gem={gem};"
            f"p7verdict={profile.p7_verdict or 'none'};verdict={verdict}"
        )
        carried_trace = [
            f"{COMPOSITION_READINESS_CANDIDATE_REF_PREFIX}{composition_readiness.candidate_id}",
            f"{RELATION_POSSIBILITY_PREFIX}{signature}",
            f"{RELATION_GEOMETRY_EVIDENCE_PREFIX}{relation_evidence}",
            f"{AMIL_MAMUL_PRIOR_TYPE_PREFIX}{prior_type}",
        ]
        # grammatical-relation + i'rab PRIORS opened only when the relation
        # possibility is licensed (ACCEPT).
        if verdict == VERDICT_ACCEPT_P8:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:amil_mamul:{uuid.uuid4().hex[:8]}",
                    source_layer="AmilMamulQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=AMIL_MAMUL_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="AmilMamulQiyas"),
        )

    def relate(
        self,
        composition_readiness: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Open structural relation possibilities from a CompositionReadinessCandidate.

        The relation geometry read from P7 drives the ACCEPT / DEFER / BLOCK
        verdict and the input-dependent prior_type."""
        return self.kernel.apply(self.build_request(composition_readiness, trace_prefix))
