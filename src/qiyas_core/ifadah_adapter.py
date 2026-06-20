"""
IfadahSpeechForceLayerAdapter — SCG-P12 adapter (information-gain). TERMINAL layer.

Builds a candidate-only **ifadah (speech-force) possibility** from a single
**accepted P11 IrabGeometryCandidate**, emitting an `IfadahCandidate`
(IFADAH_CONSTITUTION.md + SCG-P12 spec). This is the END of the structural spine.

THE HUKM/REALITY FRONTIER: "Ifadah" here is the *structural possibility* that an
utterance carries a speech force (خبر / إنشاء / طلب) — NEVER a decision of truth, a
reality claim, a hukm, or a final meaning. `speech_force_evidence` is a
*possibility* of speech force, not a verdict that the utterance HAS achieved
complete speech-force. HukmCandidate / RealityClaim / RealityMapping /
TruthJudgment / FinalMeaning / IrabFinalDecision are all forbidden, as are the
changes assign_reality_claim / assign_truth_value / assign_hukm.

TERMINAL: P12 OPENS nothing (target_boundary_opens=()). On ACCEPT it only CLOSES
the `ifadah_candidates` prior P11 opened. There is no P13.

P12 does NOT re-prove i'rab geometry — it consumes one accepted P11 candidate and
builds the speech-force possibility inside it.

Discrimination (kernel `defer:` / `فارق:` machinery — no hardcoded all-pass):
  ACCEPT : an accepted P11 i'rab geometry whose ifadah context is closed, with
           structural speech-force + ifadah-boundary + mukhatab-context evidence,
           and the identity preserved → an ifadah POSSIBILITY; closes
           `ifadah_candidates`; opens nothing.
  DEFER  : i'rab geometry present but under-determined —
           ifadah_context_underspecified / speech_force_readiness_underspecified /
           completion_boundary_underspecified / carried_irab_geometry_residuals /
           ifadah_identity_underspecified.
  BLOCK  : structural contradiction — ifadah_precondition_blocked (no usable i'rab
           geometry / context not closed), identity_collapse_blocked (multi-unit
           identity collapsed to <2), speech_force_conflict, forbidden_output_attempted,
           or final_judgment_attempted (a reality/truth/hukm/final crossing — blocked).

CANDIDATE-ONLY / potential-only: identity-preserving (I(c) preserves the P11
`irab_geometry_identity` and the transitive P9/P10 multi-unit identity beneath it),
identity disjoint from trace, residual-preserving. NOT a hukm / reality / truth /
final meaning / final tafsir / speech-act verdict / completed pragmatic force.

Identity discipline:
  I(c) preserves the P11 candidate's `irab_geometry_identity` + the transitive
  P9/P10 multi-unit identity (kernel-preserved via the far node) — the ordered
  units are NOT collapsed into one ifadah identity. Speech-force evidence lives
  strictly in trace T(c); I(c) ∩ T(c) = ∅.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .forbidden_outputs import FORBIDDEN_IFADAH
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.ifadah_rules import (
    CARRIED_IRAB_GEOMETRY_RESIDUALS,
    CLOSED_PRIORS,
    COMPLETION_BOUNDARY_UNDERSPECIFIED,
    FINAL_JUDGMENT_ATTEMPTED,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    IFADAH_CONTEXT_UNDERSPECIFIED,
    IFADAH_IDENTITY_UNDERSPECIFIED,
    IFADAH_PRECONDITION_BLOCKED,
    IFADAH_RULE,
    OPENED_PRIORS,
    SPEECH_FORCE_READINESS_UNDERSPECIFIED,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
IRAB_GEOMETRY_REF_PREFIX = "irab_geometry_ref:"
IFADAH_UNIT_IDENTITIES_PREFIX = "ifadah_unit_identities:"
IFADAH_GEOMETRY_EVIDENCE_PREFIX = "ifadah_evidence:"
IFADAH_READINESS_TRACE_PREFIX = "ifadah_readiness_trace:"
SPEECH_FORCE_READINESS_TRACE_PREFIX = "speech_force_readiness_trace:"
CLOSURE_TRACE_PREFIX = "closure_trace:"
OPENED_PRIOR_PREFIX = "opens_prior:"
CLOSED_PRIOR_PREFIX = "closes_prior:"

# Structural verdicts.
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# Forbidden output type names the P11 candidate's trace must never carry (defensive).
_FORBIDDEN_EVIDENCE_TOKENS = frozenset(FORBIDDEN_IFADAH)
# The P11 i'rab-geometry evidence marker P12 reads its structure from.
_IRAB_GEOMETRY_EVIDENCE_MARKER = "irab_geometry_evidence:"
_IRAB_UNIT_IDENTITIES_MARKER = "irab_unit_identities:"


def _parse_irab_geometry_evidence(candidate: Candidate) -> dict:
    """Read irab_context_closed/irab_position/case_marker/waqf_readiness/verdict off
    a P11 candidate trace."""
    out: dict = {}
    for t in candidate.trace_ids:
        if t.startswith(_IRAB_GEOMETRY_EVIDENCE_MARKER):
            for kv in t.split(":", 1)[1].split(";"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    out[k] = v
    return out


def _distinct_unit_count(candidate: Candidate) -> int:
    """Number of distinct units carried transitively from P11 (irab_unit_identities)."""
    for t in candidate.trace_ids:
        if t.startswith(_IRAB_UNIT_IDENTITIES_MARKER):
            body = t.split("distinct=", 1)
            if len(body) == 2:
                try:
                    return int(body[1].split(";", 1)[0])
                except ValueError:
                    return 0
    return 0


@dataclass(frozen=True)
class IfadahProfile:
    """Structural speech-force profile derived from an accepted P11 i'rab geometry."""

    has_irab_geometry: bool
    multi_unit_preserved: bool
    ifadah_context_closed: bool
    speech_force_present: bool
    completion_boundary_present: bool
    ifadah_identity_determined: bool
    carried_residuals: bool
    speech_force_conflict: bool
    forbidden_attempted: bool
    final_judgment_attempted: bool

    @property
    def verdict(self) -> str:
        # BLOCK — structural contradictions / frontier crossings first.
        if self.forbidden_attempted:
            return VERDICT_BLOCK
        if self.final_judgment_attempted:
            return VERDICT_BLOCK
        if self.speech_force_conflict:
            return VERDICT_BLOCK
        if not self.has_irab_geometry:
            return VERDICT_BLOCK            # ifadah_precondition_blocked
        if not self.multi_unit_preserved:
            return VERDICT_BLOCK            # identity_collapse_blocked
        # DEFER — admissible (i'rab geometry present) but under-determined.
        if not self.ifadah_context_closed:
            return VERDICT_DEFER
        if not self.speech_force_present:
            return VERDICT_DEFER
        if not self.completion_boundary_present:
            return VERDICT_DEFER
        if self.carried_residuals:
            return VERDICT_DEFER
        if not self.ifadah_identity_determined:
            return VERDICT_DEFER
        return VERDICT_ACCEPT

    @property
    def reason(self) -> str | None:
        v = self.verdict
        if v == VERDICT_ACCEPT:
            return None
        if v == VERDICT_BLOCK:
            if self.forbidden_attempted:
                return FORBIDDEN_OUTPUT_ATTEMPTED
            if self.final_judgment_attempted:
                return FINAL_JUDGMENT_ATTEMPTED
            if self.speech_force_conflict:
                return "speech_force_conflict"
            if not self.has_irab_geometry:
                return IFADAH_PRECONDITION_BLOCKED
            return IDENTITY_COLLAPSE_BLOCKED
        # DEFER reasons (same precedence as verdict()).
        if not self.ifadah_context_closed:
            return IFADAH_CONTEXT_UNDERSPECIFIED
        if not self.speech_force_present:
            return SPEECH_FORCE_READINESS_UNDERSPECIFIED
        if not self.completion_boundary_present:
            return COMPLETION_BOUNDARY_UNDERSPECIFIED
        if self.carried_residuals:
            return CARRIED_IRAB_GEOMETRY_RESIDUALS
        return IFADAH_IDENTITY_UNDERSPECIFIED


def _build_profile(
    irab_geometry: Candidate | None,
    ifadah_context_closed: bool | None,
    speech_force_evidence: bool | None,
    ifadah_boundary_evidence: bool | None,
    mukhatab_context_evidence: bool | None,
    ifadah_identity_determined: bool,
    speech_force_conflict: bool,
    final_judgment_attempted: bool,
) -> IfadahProfile:
    if irab_geometry is None:
        return IfadahProfile(
            has_irab_geometry=False,
            multi_unit_preserved=False,
            ifadah_context_closed=False,
            speech_force_present=False,
            completion_boundary_present=False,
            ifadah_identity_determined=False,
            carried_residuals=False,
            speech_force_conflict=speech_force_conflict,
            forbidden_attempted=False,
            final_judgment_attempted=final_judgment_attempted,
        )

    ev = _parse_irab_geometry_evidence(irab_geometry)
    distinct = _distinct_unit_count(irab_geometry)
    has_irab_geometry = bool(ev) and bool(irab_geometry.identity_ids)
    multi_unit_preserved = distinct >= 2 or len(
        {i for i in irab_geometry.identity_ids if i.startswith("identity:codepoint:")}
    ) >= 2

    # Structural speech-force evidence — derived from the P11 i'rab geometry unless
    # the caller overrides (tests). An accepted P11 i'rab geometry
    # (irab_context_closed=1, irab_position=1, case_marker=1, waqf_readiness=1)
    # supplies a closed ifadah context (mukhatab-bearing), a speech-force
    # POSSIBILITY, and a completion boundary. These are POSSIBILITIES, never a
    # reality/truth/hukm verdict.
    derived_ctx = ev.get("irab_context_closed") == "1"        # ifadah context closed
    derived_mukhatab = ev.get("irab_context_closed") == "1"   # mukhatab context (folded into context)
    derived_speech = ev.get("irab_position") == "1"           # speech-force possibility
    derived_boundary = ev.get("waqf_readiness") == "1"        # completion/waqf boundary

    ctx_arg = derived_ctx if ifadah_context_closed is None else ifadah_context_closed
    mukhatab_arg = derived_mukhatab if mukhatab_context_evidence is None else mukhatab_context_evidence
    ctx_closed = ctx_arg and mukhatab_arg
    speech_present = derived_speech if speech_force_evidence is None else speech_force_evidence
    boundary_present = derived_boundary if ifadah_boundary_evidence is None else ifadah_boundary_evidence

    carried_residuals = bool(irab_geometry.residuals)
    forbidden_attempted = any(
        any(tok in t for tok in _FORBIDDEN_EVIDENCE_TOKENS)
        for t in irab_geometry.trace_ids
    )
    return IfadahProfile(
        has_irab_geometry=has_irab_geometry,
        multi_unit_preserved=multi_unit_preserved,
        ifadah_context_closed=ctx_closed,
        speech_force_present=speech_present,
        completion_boundary_present=boundary_present,
        ifadah_identity_determined=ifadah_identity_determined,
        carried_residuals=carried_residuals,
        speech_force_conflict=speech_force_conflict,
        forbidden_attempted=forbidden_attempted,
        final_judgment_attempted=final_judgment_attempted,
    )


@dataclass
class IfadahSpeechForceLayerAdapter:
    """Adapter that builds an ifadah speech-force possibility from a P11 candidate."""

    kernel: QiyasKernel

    def build_request(
        self,
        irab_geometry: Candidate | None,
        *,
        ifadah_context_closed: bool | None = None,
        speech_force_evidence: bool | None = None,
        ifadah_boundary_evidence: bool | None = None,
        mukhatab_context_evidence: bool | None = None,
        ifadah_identity_determined: bool = True,
        speech_force_conflict: bool = False,
        final_judgment_attempted: bool = False,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest composing an ifadah possibility from a P11 candidate."""
        profile = _build_profile(
            irab_geometry,
            ifadah_context_closed,
            speech_force_evidence,
            ifadah_boundary_evidence,
            mukhatab_context_evidence,
            ifadah_identity_determined,
            speech_force_conflict,
            final_judgment_attempted,
        )
        verdict = profile.verdict

        # I(c) far identity = the preserved P11 irab_geometry identity (which carries
        # the transitive P9/P10 multi-unit identity) — never collapsed to one id.
        preserved_ids: tuple = (
            tuple(dict.fromkeys(irab_geometry.identity_ids))
            if irab_geometry is not None else tuple()
        )
        ig_ref = irab_geometry.candidate_id if irab_geometry is not None else "none"

        if not trace_prefix:
            trace_prefix = "ifadah"

        asl = QiyasNodeRef(
            node_id="اصل:ifadah_speech_force_domain",
            node_type="IfadahSpeechForceDomain",
            identity_ids=("identity:ifadah_speech_force_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The accepted P11 i'rab geometry rides on the far node — it preserves the
        # irab_geometry_candidate identity (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:irab_geometry:{uuid.uuid4().hex[:8]}",
            node_type="IrabGeometryCandidate",
            identity_ids=preserved_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_irab_geometry_ref:evidenced",
            "وصف:has_speech_force_evidence:evidenced",
            "وصف:has_ifadah_boundary_evidence:evidenced",
            "وصف:has_mukhatab_context_evidence:evidenced",
            "وصف:ifadah_context_closed_present:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_ifadah_speech_force_domain:verified",
            "علة:ifadah_speech_force_composition_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:ifadah_possibility_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            proves.append(f"defer:{profile.reason}:present")
        else:  # VERDICT_BLOCK
            proves.append(f"فارق:{profile.reason}:present")

        ctx = "1" if profile.ifadah_context_closed else "0"
        speech = "1" if profile.speech_force_present else "0"
        boundary = "1" if profile.completion_boundary_present else "0"
        distinct = _distinct_unit_count(irab_geometry) if irab_geometry is not None else 0
        carried_trace = [
            f"{IRAB_GEOMETRY_REF_PREFIX}{ig_ref}",
            f"{IFADAH_UNIT_IDENTITIES_PREFIX}distinct={distinct}",
            f"{IFADAH_GEOMETRY_EVIDENCE_PREFIX}"
            f"ifadah_context_closed={ctx};speech_force={speech};"
            f"completion_boundary={boundary};verdict={verdict}",
            f"{IFADAH_READINESS_TRACE_PREFIX}closed={ctx}",
            f"{SPEECH_FORCE_READINESS_TRACE_PREFIX}present={speech}",
            f"{CLOSURE_TRACE_PREFIX}boundary={boundary}",
        ]
        # TERMINAL: opens nothing. On ACCEPT it only closes ifadah_candidates.
        if verdict == VERDICT_ACCEPT:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]
            carried_trace += [f"{CLOSED_PRIOR_PREFIX}{p}" for p in CLOSED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:ifadah:{uuid.uuid4().hex[:8]}",
                    source_layer="IfadahSpeechForceQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=IFADAH_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="IfadahSpeechForceQiyas"),
        )

    def compose(
        self,
        irab_geometry: Candidate | None,
        *,
        ifadah_context_closed: bool | None = None,
        speech_force_evidence: bool | None = None,
        ifadah_boundary_evidence: bool | None = None,
        mukhatab_context_evidence: bool | None = None,
        ifadah_identity_determined: bool = True,
        speech_force_conflict: bool = False,
        final_judgment_attempted: bool = False,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Build an ifadah speech-force possibility from a single accepted P11 candidate.

        The speech-force possibility drives the ACCEPT / DEFER / BLOCK verdict; P12 is
        TERMINAL — ACCEPT opens nothing and only closes `ifadah_candidates`. It is a
        possibility, never a reality/truth/hukm/final claim.
        """
        return self.kernel.apply(
            self.build_request(
                irab_geometry,
                ifadah_context_closed=ifadah_context_closed,
                speech_force_evidence=speech_force_evidence,
                ifadah_boundary_evidence=ifadah_boundary_evidence,
                mukhatab_context_evidence=mukhatab_context_evidence,
                ifadah_identity_determined=ifadah_identity_determined,
                speech_force_conflict=speech_force_conflict,
                final_judgment_attempted=final_judgment_attempted,
                trace_prefix=trace_prefix,
            )
        )
