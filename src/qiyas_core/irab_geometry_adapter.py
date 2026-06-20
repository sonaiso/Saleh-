"""
IrabGeometryLayerAdapter — SCG-P11 adapter (information-gain).

Refines a candidate-only **i'rab-position geometry** from a single **accepted P10
`RelationGeometryCandidate`**, emitting an `IrabGeometryCandidate`
(IRAB_GEOMETRY_CONSTITUTION.md + SCG-P11 design gate / design resolution).

THE JUDGMENT-ADJACENCY BOUNDARY: P11 maps the geometry of *possible i'rab
positions* (إمكانات المواضع الإعرابية) — NEVER an i'rab judgment. It names *where*
i'rab could fall and *what* it could be; it never declares a token *is*
marfū'/manṣūb/majrūr/majzūm. `case_marker_evidence` is the geometry of a possible
marker, NOT `CaseJudgment`; `irab_position_evidence` is a candidate locus, NOT
`IrabFinalDecision`. Opening `ifadah_speech_force_candidates` is NOT ifadah
assignment.

P11 does NOT re-prove relation geometry — it consumes one accepted P10 candidate
and refines i'rab geometry inside it (design resolution Q3: requires at least one
accepted P10 candidate).

Discrimination (kernel `defer:` / `فارق:` machinery — no hardcoded all-pass):
  ACCEPT : an accepted P10 relation geometry whose i'rab context is closed, with
           structural i'rab-position + case-marker + waqf-readiness evidence, and
           the identity preserved → opens `ifadah_speech_force_candidates` (prior,
           ACCEPT only) and closes `irab_geometry_candidates`.
  DEFER  : relation geometry present but under-determined —
           irab_context_underspecified / irab_position_underspecified /
           case_marker_underspecified / waqf_readiness_underspecified /
           carried_relation_geometry_residuals / irab_identity_underspecified.
  BLOCK  : structural contradiction — irab_context_blocked (no usable relation
           geometry / context not closed), identity_collapse_blocked (multi-unit
           identity collapsed to <2), irab_position_conflict, forbidden_output_attempted.

CANDIDATE-ONLY / potential-only: identity-preserving (I(c) preserves the P10
`relation_geometry_identity` and the transitive P9 multi-unit identity beneath it),
identity disjoint from trace, residual-preserving. NOT an i'rab verdict / case
decision / ifadah / speech-force judgment / hukm / reality / meaning / dalalah /
final, NOT any P12 candidate.

Identity discipline (design resolution Q4):
  I(c) preserves the P10 candidate's `relation_geometry_identity` + the transitive
  P9 multi-unit identity (kernel-preserved via the far node) — the ordered units
  are NOT collapsed into one i'rab identity. I'rab evidence (position /
  case-marker / waqf-readiness) lives strictly in trace T(c); I(c) ∩ T(c) = ∅.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .forbidden_outputs import FORBIDDEN_IRAB_GEOMETRY
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.irab_geometry_rules import (
    CARRIED_RELATION_GEOMETRY_RESIDUALS,
    CASE_MARKER_UNDERSPECIFIED,
    CLOSED_PRIORS,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    IRAB_CONTEXT_UNDERSPECIFIED,
    IRAB_GEOMETRY_RULE,
    IRAB_IDENTITY_UNDERSPECIFIED,
    IRAB_POSITION_UNDERSPECIFIED,
    IRAB_CONTEXT_BLOCKED,
    OPENED_PRIORS,
    WAQF_READINESS_UNDERSPECIFIED,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
RELATION_GEOMETRY_REF_PREFIX = "relation_geometry_ref:"
IRAB_UNIT_IDENTITIES_PREFIX = "irab_unit_identities:"
IRAB_GEOMETRY_EVIDENCE_PREFIX = "irab_geometry_evidence:"
IRAB_POSITION_TRACE_PREFIX = "irab_position_trace:"
CASE_MARKER_TRACE_PREFIX = "case_marker_trace:"
WAQF_READINESS_TRACE_PREFIX = "waqf_readiness_trace:"
OPENED_PRIOR_PREFIX = "opens_prior:"
CLOSED_PRIOR_PREFIX = "closes_prior:"

# Structural verdicts.
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# Forbidden output type names the P10 candidate's trace must never carry (defensive).
_FORBIDDEN_EVIDENCE_TOKENS = frozenset(FORBIDDEN_IRAB_GEOMETRY)
# The P10 relation-geometry evidence marker P11 reads its structure from.
_RELATION_GEOMETRY_EVIDENCE_MARKER = "relation_geometry_evidence:"
_RELATION_UNIT_IDENTITIES_MARKER = "relation_unit_identities:"


def _parse_relation_geometry_evidence(candidate: Candidate) -> dict:
    """Read relation_scope_closed/relation_type/dependency_scope/verdict off a P10
    candidate trace."""
    out: dict = {}
    for t in candidate.trace_ids:
        if t.startswith(_RELATION_GEOMETRY_EVIDENCE_MARKER):
            for kv in t.split(":", 1)[1].split(";"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    out[k] = v
    return out


def _distinct_unit_count(candidate: Candidate) -> int:
    """Number of distinct units carried transitively from P10 (relation_unit_identities)."""
    for t in candidate.trace_ids:
        if t.startswith(_RELATION_UNIT_IDENTITIES_MARKER):
            body = t.split("distinct=", 1)
            if len(body) == 2:
                try:
                    return int(body[1].split(";", 1)[0])
                except ValueError:
                    return 0
    return 0


@dataclass(frozen=True)
class IrabGeometryProfile:
    """Structural i'rab-position profile derived from an accepted P10 relation geometry."""

    has_relation_geometry: bool
    multi_unit_preserved: bool
    irab_context_closed: bool
    irab_position_present: bool
    case_marker_present: bool
    waqf_readiness_present: bool
    irab_identity_determined: bool
    carried_residuals: bool
    irab_position_conflict: bool
    forbidden_attempted: bool

    @property
    def verdict(self) -> str:
        # BLOCK — structural contradictions first.
        if self.forbidden_attempted:
            return VERDICT_BLOCK
        if self.irab_position_conflict:
            return VERDICT_BLOCK
        if not self.has_relation_geometry:
            return VERDICT_BLOCK            # irab_context_blocked
        if not self.multi_unit_preserved:
            return VERDICT_BLOCK            # identity_collapse_blocked
        # DEFER — admissible (relation geometry present) but under-determined.
        if not self.irab_context_closed:
            return VERDICT_DEFER
        if not self.irab_position_present:
            return VERDICT_DEFER
        if not self.case_marker_present:
            return VERDICT_DEFER
        if not self.waqf_readiness_present:
            return VERDICT_DEFER
        if self.carried_residuals:
            return VERDICT_DEFER
        if not self.irab_identity_determined:
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
            if self.irab_position_conflict:
                return "irab_position_conflict"
            if not self.has_relation_geometry:
                return IRAB_CONTEXT_BLOCKED
            return IDENTITY_COLLAPSE_BLOCKED
        # DEFER reasons (same precedence as verdict()).
        if not self.irab_context_closed:
            return IRAB_CONTEXT_UNDERSPECIFIED
        if not self.irab_position_present:
            return IRAB_POSITION_UNDERSPECIFIED
        if not self.case_marker_present:
            return CASE_MARKER_UNDERSPECIFIED
        if not self.waqf_readiness_present:
            return WAQF_READINESS_UNDERSPECIFIED
        if self.carried_residuals:
            return CARRIED_RELATION_GEOMETRY_RESIDUALS
        return IRAB_IDENTITY_UNDERSPECIFIED


def _build_profile(
    relation_geometry: Candidate | None,
    irab_context_closed: bool | None,
    irab_position_evidence: bool | None,
    case_marker_evidence: bool | None,
    waqf_readiness_evidence: bool | None,
    irab_identity_determined: bool,
    irab_position_conflict: bool,
) -> IrabGeometryProfile:
    if relation_geometry is None:
        return IrabGeometryProfile(
            has_relation_geometry=False,
            multi_unit_preserved=False,
            irab_context_closed=False,
            irab_position_present=False,
            case_marker_present=False,
            waqf_readiness_present=False,
            irab_identity_determined=False,
            carried_residuals=False,
            irab_position_conflict=irab_position_conflict,
            forbidden_attempted=False,
        )

    ev = _parse_relation_geometry_evidence(relation_geometry)
    distinct = _distinct_unit_count(relation_geometry)
    # has_relation_geometry: a usable accepted P10 candidate carries the
    # relation-geometry evidence marker AND preserves a non-empty identity.
    has_relation_geometry = bool(ev) and bool(relation_geometry.identity_ids)
    # multi_unit_preserved: the transitive ≥2-distinct-unit structure survives.
    multi_unit_preserved = distinct >= 2 or len(
        {i for i in relation_geometry.identity_ids if i.startswith("identity:codepoint:")}
    ) >= 2

    # Structural i'rab evidence — derived from the P10 geometry unless the caller
    # overrides (tests). An accepted P10 relation geometry (relation_scope_closed=1,
    # relation_type=1, dependency_scope=1) supplies a closed i'rab context and the
    # position / marker / waqf-readiness possibilities; these are POSSIBILITIES, not
    # verdicts.
    derived_context_closed = ev.get("relation_scope_closed") == "1"
    derived_position = ev.get("relation_type") == "1"
    derived_marker = ev.get("relation_type") == "1"
    derived_waqf = ev.get("dependency_scope") == "1"

    ctx_closed = derived_context_closed if irab_context_closed is None else irab_context_closed
    pos_present = derived_position if irab_position_evidence is None else irab_position_evidence
    marker_present = derived_marker if case_marker_evidence is None else case_marker_evidence
    waqf_present = derived_waqf if waqf_readiness_evidence is None else waqf_readiness_evidence

    carried_residuals = bool(relation_geometry.residuals)
    forbidden_attempted = any(
        any(tok in t for tok in _FORBIDDEN_EVIDENCE_TOKENS)
        for t in relation_geometry.trace_ids
    )
    return IrabGeometryProfile(
        has_relation_geometry=has_relation_geometry,
        multi_unit_preserved=multi_unit_preserved,
        irab_context_closed=ctx_closed,
        irab_position_present=pos_present,
        case_marker_present=marker_present,
        waqf_readiness_present=waqf_present,
        irab_identity_determined=irab_identity_determined,
        carried_residuals=carried_residuals,
        irab_position_conflict=irab_position_conflict,
        forbidden_attempted=forbidden_attempted,
    )


@dataclass
class IrabGeometryLayerAdapter:
    """Adapter that refines an i'rab-position geometry from a P10 candidate."""

    kernel: QiyasKernel

    def build_request(
        self,
        relation_geometry: Candidate | None,
        *,
        irab_context_closed: bool | None = None,
        irab_position_evidence: bool | None = None,
        case_marker_evidence: bool | None = None,
        waqf_readiness_evidence: bool | None = None,
        irab_identity_determined: bool = True,
        irab_position_conflict: bool = False,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest refining an i'rab geometry from a P10 candidate."""
        profile = _build_profile(
            relation_geometry,
            irab_context_closed,
            irab_position_evidence,
            case_marker_evidence,
            waqf_readiness_evidence,
            irab_identity_determined,
            irab_position_conflict,
        )
        verdict = profile.verdict

        # I(c) far identity = the preserved P10 relation_geometry identity (which
        # carries the transitive P9 multi-unit identity) — never collapsed to one id.
        preserved_ids: tuple = (
            tuple(dict.fromkeys(relation_geometry.identity_ids))
            if relation_geometry is not None else tuple()
        )
        rg_ref = relation_geometry.candidate_id if relation_geometry is not None else "none"

        if not trace_prefix:
            trace_prefix = "irab_geometry"

        asl = QiyasNodeRef(
            node_id="اصل:irab_geometry_domain",
            node_type="IrabGeometryDomain",
            identity_ids=("identity:irab_geometry_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The accepted P10 relation geometry rides on the far node — it preserves
        # the relation_geometry_candidate identity (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:relation_geometry:{uuid.uuid4().hex[:8]}",
            node_type="RelationGeometryCandidate",
            identity_ids=preserved_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_relation_geometry_ref:evidenced",
            "وصف:has_irab_position_evidence:evidenced",
            "وصف:has_case_marker_evidence:evidenced",
            "وصف:has_waqf_readiness_evidence:evidenced",
            "وصف:irab_context_closed_present:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_irab_geometry_domain:verified",
            "علة:irab_geometry_composition_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:irab_geometry_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            proves.append(f"defer:{profile.reason}:present")
        else:  # VERDICT_BLOCK
            proves.append(f"فارق:{profile.reason}:present")

        ctx = "1" if profile.irab_context_closed else "0"
        pos = "1" if profile.irab_position_present else "0"
        mark = "1" if profile.case_marker_present else "0"
        waqf = "1" if profile.waqf_readiness_present else "0"
        distinct = _distinct_unit_count(relation_geometry) if relation_geometry is not None else 0
        carried_trace = [
            f"{RELATION_GEOMETRY_REF_PREFIX}{rg_ref}",
            f"{IRAB_UNIT_IDENTITIES_PREFIX}distinct={distinct}",
            f"{IRAB_GEOMETRY_EVIDENCE_PREFIX}"
            f"irab_context_closed={ctx};irab_position={pos};case_marker={mark};"
            f"waqf_readiness={waqf};verdict={verdict}",
            f"{IRAB_POSITION_TRACE_PREFIX}present={pos}",
            f"{CASE_MARKER_TRACE_PREFIX}present={mark}",
            f"{WAQF_READINESS_TRACE_PREFIX}present={waqf}",
        ]
        if verdict == VERDICT_ACCEPT:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]
            carried_trace += [f"{CLOSED_PRIOR_PREFIX}{p}" for p in CLOSED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:irab_geometry:{uuid.uuid4().hex[:8]}",
                    source_layer="IrabGeometryQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=IRAB_GEOMETRY_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="IrabGeometryQiyas"),
        )

    def compose(
        self,
        relation_geometry: Candidate | None,
        *,
        irab_context_closed: bool | None = None,
        irab_position_evidence: bool | None = None,
        case_marker_evidence: bool | None = None,
        waqf_readiness_evidence: bool | None = None,
        irab_identity_determined: bool = True,
        irab_position_conflict: bool = False,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Refine an i'rab-position geometry from a single accepted P10 candidate.

        The i'rab geometry drives the ACCEPT / DEFER / BLOCK verdict; ACCEPT opens
        only `ifadah_speech_force_candidates` and closes `irab_geometry_candidates`.
        Positions are mapped — never a verdict.
        """
        return self.kernel.apply(
            self.build_request(
                relation_geometry,
                irab_context_closed=irab_context_closed,
                irab_position_evidence=irab_position_evidence,
                case_marker_evidence=case_marker_evidence,
                waqf_readiness_evidence=waqf_readiness_evidence,
                irab_identity_determined=irab_identity_determined,
                irab_position_conflict=irab_position_conflict,
                trace_prefix=trace_prefix,
            )
        )
