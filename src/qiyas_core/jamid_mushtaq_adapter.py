"""
JamidMushtaqLayerAdapter — SCG-P4 adapter (information-gain layer).

Opens a structural derivation-class POSSIBILITY from a ``RootStemCandidate``,
emitting a ``JamidMushtaqCandidate`` (JAMID_MUSHTAQ_CONSTITUTION.md).

SCG-P4 STRENGTHENING (2026-06-18): P4 is no longer a forwarding stamp. It READS
the upstream P3 verdict + structural geometry that ride on the RootStemCandidate's
trace (``root_pattern_evidence:…;verdict=…`` and ``stem_boundary_evidence:…;nC=…``)
and discriminates the DERIVATION geometry into one of three verdicts, routed
through the kernel's residual machinery:

  ACCEPT : P3 ACCEPT and a consonantal skeleton sufficient to open a derivation-
           geometry possibility (n_consonants >= 2).
  DEFER  : derivation skeleton too thin (n_consonants == 1) — e.g. a single
           consonant + long vowel that P3 closed but that under-specifies a
           derivation geometry — emits ``defer:derivation_underspecified:present``.
  BLOCK  : P3 was DEFER/BLOCK (non-accepted upstream), or the derivation geometry
           conflicts — emits ``فارق:derivation_classification_conflict:present``.

This is GENUINE new information beyond P3: P3 asks "can this close a root/stem?"
(مَا: yes, via its long vowel); P4 asks "does the consonantal skeleton support a
derivation-geometry possibility?" (مَا: no — only one consonant → DEFER).

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT a final jamid/mushtaq judgment (WordTypeJudgment forbidden), NOT wazn
    (WeightCandidate forbidden), NOT morphology, NOT wordhood, NOT lexical
    meaning / dalalah / i'rab / hukm. ``jamid_mushtaq_prior_type`` is a STRUCTURAL
    derivation-geometry category (selected input-dependently), NEVER a linguistic
    جامد/مشتق/اسم/فعل label.

Carried fields (on the output candidate's trace_ids, documented prefixes):
  root_stem_candidate_ref:<id>                       the consumed P3 candidate
  structural_derivation_possibility:<derivsig:CV:cps>  input-dependent geometry
  jamid_mushtaq_prior_type:<structural class>         input-dependent (allowed set)
  pattern_evidence / derivation_geometry_evidence:cv=..;nC=..;gem=..;skeleton=..C;p3verdict=..
  opens_prior:word_type_candidates                    opened for SCG-P5 (ACCEPT only).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .root_stem_adapter import (
    ROOT_PATTERN_EVIDENCE_PREFIX,
    STEM_BOUNDARY_EVIDENCE_PREFIX,
    VERDICT_ACCEPT,
)
from .rules.jamid_mushtaq_rules import (
    DERIVATION_CLASSIFICATION_CONFLICT,
    DERIVATION_GEOMETRY_CLASS,
    DERIVATION_GEOMETRY_PRIOR,
    DERIVATION_UNDERSPECIFIED,
    JAMID_MUSHTAQ_RULE,
    OPENED_PRIORS,
    STRUCTURAL_DERIVATION_POSSIBILITY,
)
from .typed_codepoint_adapter import is_arabic_letter

# Trace prefixes for the carried structural fields (read back by tests/tools).
ROOT_STEM_CANDIDATE_REF_PREFIX = "root_stem_candidate_ref:"
DERIVATION_POSSIBILITY_PREFIX = "structural_derivation_possibility:"
JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX = "jamid_mushtaq_prior_type:"
PATTERN_EVIDENCE_PREFIX = "pattern_evidence:"
DERIVATION_GEOMETRY_EVIDENCE_PREFIX = "derivation_geometry_evidence:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts (SCG-P4 discrimination).
VERDICT_ACCEPT_P4 = "accept"
VERDICT_DEFER_P4 = "defer"
VERDICT_BLOCK_P4 = "block"

_LONG_VOWEL_LETTERS = frozenset({0x0627, 0x0648, 0x064A, 0x0649, 0x0622})


def _parse_kv(trace_ids, prefix):
    """Parse a ``prefix`` trace entry of the form ``k1=v1;k2=v2`` into a dict."""
    for t in trace_ids:
        if t.startswith(prefix):
            out = {}
            for part in t[len(prefix):].split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    out[k] = v
            return out
    return {}


@dataclass(frozen=True)
class DerivationGeometry:
    """Structural derivation geometry P4 reads from the upstream RootStemCandidate."""

    p3_verdict: str
    cv_signature: str
    n_consonants: int
    has_gemination: bool

    @property
    def verdict(self) -> str:
        # Propagate non-accepted upstream as a block (a deferred/blocked P3 carries
        # no licensed geometry to derive from).
        if self.p3_verdict and self.p3_verdict != VERDICT_ACCEPT:
            return VERDICT_BLOCK_P4
        if self.n_consonants >= 2:
            return VERDICT_ACCEPT_P4
        if self.n_consonants == 1:
            return VERDICT_DEFER_P4
        return VERDICT_BLOCK_P4  # no consonantal anchor

    @property
    def prior_type(self) -> str:
        # Input-dependent structural class (never a linguistic جامد/مشتق label).
        if self.has_gemination:
            return STRUCTURAL_DERIVATION_POSSIBILITY
        if self.n_consonants >= 3:
            return DERIVATION_GEOMETRY_CLASS
        return DERIVATION_GEOMETRY_PRIOR


def _read_derivation_geometry(root_stem: Candidate) -> DerivationGeometry:
    """Read P3's verdict + structural geometry from the RootStemCandidate trace.

    Falls back to deriving the consonant count from the candidate's own codepoints
    when no P3 evidence is present (e.g. a hand-built fixture)."""
    pat = _parse_kv(root_stem.trace_ids, ROOT_PATTERN_EVIDENCE_PREFIX)
    bnd = _parse_kv(root_stem.trace_ids, STEM_BOUNDARY_EVIDENCE_PREFIX)

    cv = pat.get("cv", "")
    p3_verdict = pat.get("verdict", "")
    gem = pat.get("gem") == "1"

    if "nC" in bnd:
        n_consonants = int(bnd["nC"])
    elif cv:
        n_consonants = cv.count("C")
    else:
        cps = [
            int(iid[len("identity:codepoint:"):], 16)
            for iid in root_stem.identity_ids
            if iid.startswith("identity:codepoint:")
        ]
        n_consonants = sum(
            1 for cp in cps if is_arabic_letter(cp) and cp not in _LONG_VOWEL_LETTERS
        )

    return DerivationGeometry(
        p3_verdict=p3_verdict,
        cv_signature=cv,
        n_consonants=n_consonants,
        has_gemination=gem,
    )


@dataclass
class JamidMushtaqLayerAdapter:
    """Adapter that opens a structural derivation-class possibility from a root/stem."""

    kernel: QiyasKernel

    def build_request(
        self,
        root_stem: Candidate,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest opening a structural derivation-class possibility
        from a RootStemCandidate (candidate-only). The verdict (ACCEPT / DEFER /
        BLOCK) and prior_type are driven by the derivation geometry read from P3."""
        geom = _read_derivation_geometry(root_stem)
        verdict = geom.verdict
        prior_type = geom.prior_type

        cps = sorted(
            iid[len("identity:codepoint:"):]
            for iid in root_stem.identity_ids
            if iid.startswith("identity:codepoint:")
        )
        slot_seq = "+".join(cps) or "none"
        signature = f"derivsig:{geom.cv_signature or 'none'}:{slot_seq}"

        if not trace_prefix:
            trace_prefix = f"jamid_mushtaq:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:jamid_mushtaq_domain",
            node_type="JamidMushtaqDomain",
            identity_ids=("identity:jamid_mushtaq_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The RootStemCandidate rides on the far node — it preserves the root/stem
        # (and slot) identities carried up from P3/P2/P1 (for every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:root_stem_candidate:{root_stem.candidate_id}",
            node_type="RootStemCandidate",
            identity_ids=root_stem.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=root_stem.rank,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_root_stem_candidate:evidenced",
            "وصف:structural_derivation_possibility_derived:evidenced",
            "وصف:has_jamid_mushtaq_prior_type:evidenced",
            "وصف:has_pattern_evidence:evidenced",
            "وصف:root_stem_candidate_identity_preserved:evidenced",
            "علة:belongs_to_jamid_mushtaq_domain:verified",
            "علة:jamid_mushtaq_classification_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Verdict-specific claims — input-dependent, NOT hardcoded all-pass.
        if verdict == VERDICT_ACCEPT_P4:
            proves.append("وصف:derivation_geometry_consistent:evidenced")
        elif verdict == VERDICT_DEFER_P4:
            proves.append(f"defer:{DERIVATION_UNDERSPECIFIED}:present")
        else:  # VERDICT_BLOCK_P4
            proves.append(f"فارق:{DERIVATION_CLASSIFICATION_CONFLICT}:present")

        gem = "1" if geom.has_gemination else "0"
        derivation_evidence = (
            f"cv={geom.cv_signature or 'none'};nC={geom.n_consonants};"
            f"gem={gem};skeleton={geom.n_consonants}C;"
            f"p3verdict={geom.p3_verdict or 'none'};verdict={verdict}"
        )
        carried_trace = [
            f"{ROOT_STEM_CANDIDATE_REF_PREFIX}{root_stem.candidate_id}",
            f"{DERIVATION_POSSIBILITY_PREFIX}{signature}",
            f"{JAMID_MUSHTAQ_PRIOR_TYPE_PREFIX}{prior_type}",
            f"{PATTERN_EVIDENCE_PREFIX}{derivation_evidence}",
            f"{DERIVATION_GEOMETRY_EVIDENCE_PREFIX}{derivation_evidence}",
        ]
        # Priors are opened only when the derivation possibility is licensed.
        if verdict == VERDICT_ACCEPT_P4:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:jamid_mushtaq:{uuid.uuid4().hex[:8]}",
                    source_layer="JamidMushtaqQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=JAMID_MUSHTAQ_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="JamidMushtaqQiyas"),
        )

    def classify(
        self,
        root_stem: Candidate,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Open a structural derivation-class possibility from a RootStemCandidate.

        The derivation geometry read from P3 drives the ACCEPT / DEFER / BLOCK
        verdict and the input-dependent prior_type."""
        return self.kernel.apply(self.build_request(root_stem, trace_prefix))
