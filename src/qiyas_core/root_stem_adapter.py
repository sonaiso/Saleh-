"""
RootStemLayerAdapter — SCG-P3 adapter (information-gain layer).

Closes a structural root/stem POSSIBILITY from a ``RegistryProjectionCandidate``,
emitting a ``RootStemCandidate`` (ROOT_STEM_CLOSURE_CONSTITUTION.md).

SCG-P3 STRENGTHENING (2026-06-18): P3 is no longer a forwarding stamp. It
discriminates the token's slot-sequence geometry (a ``RootStemSequenceProfile``,
the constitutional ``slot_sequence_consistent`` evidence per §3) into one of three
structural verdicts, routed through the kernel's existing residual machinery:

  ACCEPT : geometry is sufficient to open a root/stem closure possibility
           (n_consonants >= 1 AND (slot_count >= 2 OR long-vowel OR gemination)).
  DEFER  : geometry is too small / underspecified but not impossible
           (a lone CV with no long-vowel / gemination enrichment) — emits
           ``defer:root_pattern_underspecified:present``.
  BLOCK  : geometry structurally contradicts closure (no consonantal anchor,
           n_consonants == 0) — emits ``فارق:root_pattern_conflict:present``.

The root_pattern_evidence / stem_boundary_evidence / structural_root_stem_signature
are now INPUT-DEPENDENT (they encode the CV signature, slot_count, gemination,
long-vowel and ending profile) — not constant strings.

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT final root extraction / RootCandidate, NOT wazn / WeightCandidate,
    NOT morphology, NOT wordhood, NOT lexical meaning / dalalah / i'rab / hukm.

Carried fields (on the output candidate's trace_ids, with documented prefixes —
they are structural evidence, not identity):
  registry_projection_ref:<id>                  the consumed P2 candidate
  structural_root_stem_signature:<rootstemsig:CV:cps>   input-dependent geometry
  slot_sequence_refs:<codepoints>               structural slot-sequence refs
  root_pattern_evidence:cv=..;slots=..;gem=..;lv=..     input-dependent pattern
  stem_boundary_evidence:ending=..;nC=..        input-dependent boundary profile
  opens_prior:jamid_mushtaq_candidates / opens_prior:word_pattern_candidates
      priors opened for SCG-P4 (ACCEPT only), NEVER produced here.

Identity: the output preserves the slot_candidate identities that the
RegistryProjectionCandidate carries (they ride on the far node), for ACCEPT,
DEFER and BLOCK alike.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.root_stem_rules import (
    OPENED_PRIORS,
    ROOT_PATTERN_CONFLICT,
    ROOT_PATTERN_UNDERSPECIFIED,
    ROOT_STEM_RULE,
)
from .typed_codepoint_adapter import is_arabic_haraka, is_arabic_letter

# Trace prefixes for the carried structural fields (read back by tests/tools).
REGISTRY_PROJECTION_REF_PREFIX = "registry_projection_ref:"
ROOT_STEM_SIGNATURE_PREFIX = "structural_root_stem_signature:"
SLOT_SEQUENCE_REFS_PREFIX = "slot_sequence_refs:"
ROOT_PATTERN_EVIDENCE_PREFIX = "root_pattern_evidence:"
STEM_BOUNDARY_EVIDENCE_PREFIX = "stem_boundary_evidence:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts (SCG-P3 discrimination).
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# Structural codepoint classes (purely geometric — no morphology / lexicon).
_LONG_VOWEL_LETTERS = frozenset({0x0627, 0x0648, 0x064A, 0x0649, 0x0622})  # ا و ي ى آ
_SHADDA = 0x0651
_SUKUN = 0x0652


# ---------------------------------------------------------------------------
# Structural slot-sequence profile (the slot_sequence_consistent evidence, §3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RootStemSequenceProfile:
    """Purely-structural distillation of a token's slot sequence geometry.

    Computed from the ordered Arabic codepoints of a single tokenizer segment
    (run_qiyas) or, as a fallback, from a single projection's own codepoints.
    Carries NO morphology, NO wazn, NO lexicon — only CV geometry.
    """

    slot_count: int
    cv_signature: str
    has_long_vowel: bool
    has_gemination: bool
    closed_ending: bool
    n_consonants: int

    @property
    def verdict(self) -> str:
        if self.n_consonants == 0:
            return VERDICT_BLOCK
        if self.slot_count >= 2 or self.has_long_vowel or self.has_gemination:
            return VERDICT_ACCEPT
        return VERDICT_DEFER


def build_sequence_profile(codepoints: list[int]) -> RootStemSequenceProfile:
    """Build a structural CV profile from an ordered list of Arabic codepoints.

    CV mapping (structural only): long-vowel letter -> V; other letter -> C;
    shadda -> C (gemination doubles the carrier); sukun -> closes (no symbol);
    other haraka (short vowel / tanwin) -> V. ``slot_count`` counts letter
    immediately followed by a haraka (the canonical slot-formation adjacency).
    """
    sig: list[str] = []
    for cp in codepoints:
        if is_arabic_letter(cp):
            sig.append("V" if cp in _LONG_VOWEL_LETTERS else "C")
        elif is_arabic_haraka(cp):
            if cp == _SHADDA:
                sig.append("C")
            elif cp == _SUKUN:
                continue
            else:
                sig.append("V")
    cv = "".join(sig)

    slot_count = sum(
        1
        for i in range(len(codepoints) - 1)
        if is_arabic_letter(codepoints[i]) and is_arabic_haraka(codepoints[i + 1])
    )
    has_long_vowel = any(cp in _LONG_VOWEL_LETTERS for cp in codepoints)
    has_gemination = _SHADDA in codepoints
    closed_ending = cv.endswith("C")
    n_consonants = cv.count("C")
    return RootStemSequenceProfile(
        slot_count=slot_count,
        cv_signature=cv,
        has_long_vowel=has_long_vowel,
        has_gemination=has_gemination,
        closed_ending=closed_ending,
        n_consonants=n_consonants,
    )


def _codepoints(candidate: Candidate) -> list[str]:
    return sorted(
        iid[len("identity:codepoint:"):]
        for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )


def _profile_from_projection(projection: Candidate) -> RootStemSequenceProfile:
    """Fallback profile for an isolated single projection (no segment context).

    Reconstructs the slot's [letter, haraka] codepoint order from the projection
    identities and builds the structural profile for that single slot.
    """
    cps = [int(h, 16) for h in _codepoints(projection)]
    letters = [cp for cp in cps if is_arabic_letter(cp)]
    harakat = [cp for cp in cps if is_arabic_haraka(cp)]
    ordered = letters + harakat  # letter(s) then haraka(s) — single-slot order
    return build_sequence_profile(ordered)


@dataclass
class RootStemLayerAdapter:
    """Adapter that closes a structural root/stem possibility from a projection."""

    kernel: QiyasKernel

    def build_request(
        self,
        projection: Candidate,
        sequence_profile: RootStemSequenceProfile | None = None,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest closing a structural root/stem possibility from a
        RegistryProjectionCandidate (candidate-only). The verdict (ACCEPT / DEFER
        / BLOCK) is driven by the structural ``sequence_profile``."""
        profile = sequence_profile or _profile_from_projection(projection)
        verdict = profile.verdict

        slot_seq = "+".join(_codepoints(projection)) or "none"
        signature = f"rootstemsig:{profile.cv_signature or 'none'}:{slot_seq}"

        if not trace_prefix:
            trace_prefix = f"root_stem:{signature}"

        asl = QiyasNodeRef(
            node_id="اصل:root_stem_closure_domain",
            node_type="RootStemClosureDomain",
            identity_ids=("identity:root_stem_closure_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The RegistryProjectionCandidate rides on the far node — it preserves the
        # slot_candidate identities carried up from P2/P1 (for every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:registry_projection_candidate:{projection.candidate_id}",
            node_type="RegistryProjectionCandidate",
            identity_ids=projection.identity_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=projection.rank,
        )

        # Required structural-presence claims (always provable for a reachable
        # projection — these are NOT the verdict; the verdict rides on the
        # defer:/فارق: claims below).
        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_registry_projection:evidenced",
            "وصف:structural_root_stem_signature_derived:evidenced",
            "وصف:has_slot_sequence_refs:evidenced",
            "وصف:has_root_pattern_evidence:evidenced",
            "وصف:has_stem_boundary_evidence:evidenced",
            "وصف:slot_candidate_identities_preserved:evidenced",
            "علة:belongs_to_root_stem_closure_domain:verified",
            "علة:root_stem_closure_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        # Verdict-specific claims — input-dependent, NOT hardcoded all-pass.
        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:slot_sequence_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            # Structurally underspecified (too small) — defer, residual preserved.
            proves.append(f"defer:{ROOT_PATTERN_UNDERSPECIFIED}:present")
        else:  # VERDICT_BLOCK
            # Structural contradiction — no consonantal anchor for closure.
            proves.append(f"فارق:{ROOT_PATTERN_CONFLICT}:present")

        # INPUT-DEPENDENT structural evidence (requirements 2/3/4) + opened priors.
        gem = "1" if profile.has_gemination else "0"
        lv = "1" if profile.has_long_vowel else "0"
        ending = "closed" if profile.closed_ending else "open"
        carried_trace = [
            f"{REGISTRY_PROJECTION_REF_PREFIX}{projection.candidate_id}",
            f"{ROOT_STEM_SIGNATURE_PREFIX}{signature}",
            f"{SLOT_SEQUENCE_REFS_PREFIX}{slot_seq}",
            f"{ROOT_PATTERN_EVIDENCE_PREFIX}"
            f"cv={profile.cv_signature or 'none'};slots={profile.slot_count};"
            f"gem={gem};lv={lv};verdict={verdict}",
            f"{STEM_BOUNDARY_EVIDENCE_PREFIX}"
            f"ending={ending};nC={profile.n_consonants}",
        ]
        # Priors are opened only when the closure is licensed (ACCEPT). A deferred
        # or blocked closure opens nothing downstream.
        if verdict == VERDICT_ACCEPT:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:root_stem:{uuid.uuid4().hex[:8]}",
                    source_layer="RootStemQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=ROOT_STEM_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="RootStemQiyas"),
        )

    def close(
        self,
        projection: Candidate,
        sequence_profile: RootStemSequenceProfile | None = None,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Close a structural root/stem possibility from a RegistryProjectionCandidate.

        The token's structural ``sequence_profile`` drives the ACCEPT / DEFER /
        BLOCK verdict. When omitted (isolated single-projection use), a minimal
        profile is derived from the projection's own codepoints.
        """
        return self.kernel.apply(
            self.build_request(projection, sequence_profile, trace_prefix)
        )
