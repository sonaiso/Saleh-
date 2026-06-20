"""
RelationGeometryLayerAdapter — SCG-P10 adapter (information-gain).

Refines a candidate-only **relation geometry** from a single **accepted P9
`SentenceGeometryCandidate`**, emitting a `RelationGeometryCandidate`
(RELATION_GEOMETRY_CONSTITUTION.md + SCG-P10 design gate / design resolution).

P10 does NOT re-prove sentencehood — the ≥2 distinct-unit requirement is already
enforced at P9. P10 maps the internal relations (تبعية، عطف، إبدال، توكيد) of an
accepted sentence geometry as *geometric possibility* (design resolution Q3:
requires at least one accepted P9 candidate, not multiple).

Discrimination (kernel `defer:` / `فارق:` machinery — no hardcoded all-pass):
  ACCEPT : an accepted P9 sentence geometry whose relation scope is closed, with
           structural relation-type evidence and dependency-scope evidence, and
           the multi-unit identity preserved → opens `irab_geometry_candidates`
           (prior, ACCEPT only) and closes `relation_geometry_candidates`.
  DEFER  : sentence geometry present but under-determined —
           relation_scope_underspecified / relation_type_underspecified /
           dependency_scope_underspecified / carried_sentence_geometry_residuals /
           relation_identity_underspecified.
  BLOCK  : structural contradiction — relation_structure_blocked (no usable
           sentence geometry), identity_collapse_blocked (multi-unit identity
           collapsed to <2), relation_type_conflict, forbidden_output_attempted.

CANDIDATE-ONLY / potential-only: identity-preserving (I(c) preserves the P9
`sentence_geometry_identity`), identity disjoint from trace, residual-preserving.
NOT i'rab / case / ifadah / meaning / dalalah / final-syntax / hukm / reality, NOT
any P11+ candidate.

Identity discipline (design resolution Q4):
  I(c) preserves the P9 candidate's `sentence_geometry_identity` (kernel-preserved
  via the far node) — the ordered multi-unit identity is NOT collapsed into one
  relation identity. Relation evidence (relation_scope / dependency_scope /
  relation-type) lives strictly in trace T(c); I(c) ∩ T(c) = ∅.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .forbidden_outputs import FORBIDDEN_RELATION_GEOMETRY
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.relation_geometry_rules import (
    CARRIED_SENTENCE_GEOMETRY_RESIDUALS,
    CLOSED_PRIORS,
    DEPENDENCY_SCOPE_UNDERSPECIFIED,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    OPENED_PRIORS,
    RELATION_GEOMETRY_RULE,
    RELATION_IDENTITY_UNDERSPECIFIED,
    RELATION_SCOPE_UNDERSPECIFIED,
    RELATION_STRUCTURE_BLOCKED,
    RELATION_TYPE_UNDERSPECIFIED,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
SENTENCE_GEOMETRY_REF_PREFIX = "sentence_geometry_ref:"
RELATION_UNIT_IDENTITIES_PREFIX = "relation_unit_identities:"
RELATION_GEOMETRY_EVIDENCE_PREFIX = "relation_geometry_evidence:"
RELATION_SCOPE_TRACE_PREFIX = "relation_scope_trace:"
DEPENDENCY_SCOPE_TRACE_PREFIX = "dependency_scope_trace:"
OPENED_PRIOR_PREFIX = "opens_prior:"
CLOSED_PRIOR_PREFIX = "closes_prior:"

# Structural verdicts.
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# Forbidden output type names the P9 candidate's trace must never carry (defensive).
_FORBIDDEN_EVIDENCE_TOKENS = frozenset(FORBIDDEN_RELATION_GEOMETRY)
# The P9 sentence-geometry evidence marker P10 reads its structure from.
_SENTENCE_GEOMETRY_EVIDENCE_MARKER = "sentence_geometry_evidence:"
_SENTENCE_UNIT_IDENTITIES_MARKER = "sentence_unit_identities:"


def _parse_sentence_geometry_evidence(candidate: Candidate) -> dict:
    """Read units/distinct/adjacency/boundary/verdict off a P9 candidate trace."""
    out: dict = {}
    for t in candidate.trace_ids:
        if t.startswith(_SENTENCE_GEOMETRY_EVIDENCE_MARKER):
            for kv in t.split(":", 1)[1].split(";"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    out[k] = v
    return out


def _distinct_unit_count(candidate: Candidate) -> int:
    """Number of distinct P9 word/segment units carried by the candidate trace."""
    for t in candidate.trace_ids:
        if t.startswith(_SENTENCE_UNIT_IDENTITIES_MARKER):
            body = t.split(":", 1)[1]
            entries = [e for e in body.split(";") if e.strip()]
            return len({e.split("=", 1)[0] for e in entries})
    return 0


@dataclass(frozen=True)
class RelationGeometryProfile:
    """Structural relation profile derived from an accepted P9 sentence geometry."""

    has_sentence_geometry: bool
    multi_unit_preserved: bool
    relation_scope_closed: bool
    relation_type_present: bool
    dependency_scope_present: bool
    relation_identity_determined: bool
    carried_residuals: bool
    relation_type_conflict: bool
    forbidden_attempted: bool

    @property
    def verdict(self) -> str:
        # BLOCK — structural contradictions first.
        if self.forbidden_attempted:
            return VERDICT_BLOCK
        if self.relation_type_conflict:
            return VERDICT_BLOCK
        if not self.has_sentence_geometry:
            return VERDICT_BLOCK            # relation_structure_blocked
        if not self.multi_unit_preserved:
            return VERDICT_BLOCK            # identity_collapse_blocked
        # DEFER — admissible (sentence geometry present) but under-determined.
        if not self.relation_scope_closed:
            return VERDICT_DEFER
        if not self.relation_type_present:
            return VERDICT_DEFER
        if not self.dependency_scope_present:
            return VERDICT_DEFER
        if self.carried_residuals:
            return VERDICT_DEFER
        if not self.relation_identity_determined:
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
            if self.relation_type_conflict:
                return "relation_type_conflict"
            if not self.has_sentence_geometry:
                return RELATION_STRUCTURE_BLOCKED
            return IDENTITY_COLLAPSE_BLOCKED
        # DEFER reasons (same precedence as verdict()).
        if not self.relation_scope_closed:
            return RELATION_SCOPE_UNDERSPECIFIED
        if not self.relation_type_present:
            return RELATION_TYPE_UNDERSPECIFIED
        if not self.dependency_scope_present:
            return DEPENDENCY_SCOPE_UNDERSPECIFIED
        if self.carried_residuals:
            return CARRIED_SENTENCE_GEOMETRY_RESIDUALS
        return RELATION_IDENTITY_UNDERSPECIFIED


def _build_profile(
    sentence_geometry: Candidate | None,
    relation_scope_closed: bool | None,
    relation_type_evidence: bool | None,
    dependency_scope_evidence: bool | None,
    relation_identity_determined: bool,
    relation_type_conflict: bool,
) -> RelationGeometryProfile:
    if sentence_geometry is None:
        return RelationGeometryProfile(
            has_sentence_geometry=False,
            multi_unit_preserved=False,
            relation_scope_closed=False,
            relation_type_present=False,
            dependency_scope_present=False,
            relation_identity_determined=False,
            carried_residuals=False,
            relation_type_conflict=relation_type_conflict,
            forbidden_attempted=False,
        )

    ev = _parse_sentence_geometry_evidence(sentence_geometry)
    distinct = _distinct_unit_count(sentence_geometry)
    # has_sentence_geometry: a usable accepted P9 candidate carries the
    # sentence-geometry evidence marker AND preserves a non-empty identity.
    has_sentence_geometry = bool(ev) and bool(sentence_geometry.identity_ids)
    # multi_unit_preserved: the ordered ≥2-distinct-unit structure survives.
    multi_unit_preserved = distinct >= 2 or int(ev.get("distinct", "0") or "0") >= 2

    # Structural relation evidence — derived from the P9 geometry unless the caller
    # overrides (tests). adjacency==1 & boundary==1 ⇒ relation scope is closed;
    # ≥2 distinct units ⇒ a structural relation possibility (relation-type) and a
    # dependency scope exist between the adjacent units.
    derived_scope_closed = ev.get("adjacency") == "1" and ev.get("boundary") == "1"
    derived_relation_type = int(ev.get("distinct", "0") or "0") >= 2
    derived_dependency_scope = int(ev.get("units", "0") or "0") >= 2

    rs_closed = derived_scope_closed if relation_scope_closed is None else relation_scope_closed
    rt_present = derived_relation_type if relation_type_evidence is None else relation_type_evidence
    dep_present = derived_dependency_scope if dependency_scope_evidence is None else dependency_scope_evidence

    carried_residuals = bool(sentence_geometry.residuals)
    forbidden_attempted = any(
        any(tok in t for tok in _FORBIDDEN_EVIDENCE_TOKENS)
        for t in sentence_geometry.trace_ids
    )
    return RelationGeometryProfile(
        has_sentence_geometry=has_sentence_geometry,
        multi_unit_preserved=multi_unit_preserved,
        relation_scope_closed=rs_closed,
        relation_type_present=rt_present,
        dependency_scope_present=dep_present,
        relation_identity_determined=relation_identity_determined,
        carried_residuals=carried_residuals,
        relation_type_conflict=relation_type_conflict,
        forbidden_attempted=forbidden_attempted,
    )


@dataclass
class RelationGeometryLayerAdapter:
    """Adapter that refines a relation-geometry possibility from a P9 candidate."""

    kernel: QiyasKernel

    def build_request(
        self,
        sentence_geometry: Candidate | None,
        *,
        relation_scope_closed: bool | None = None,
        relation_type_evidence: bool | None = None,
        dependency_scope_evidence: bool | None = None,
        relation_identity_determined: bool = True,
        relation_type_conflict: bool = False,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest refining a relation geometry from a P9 candidate."""
        profile = _build_profile(
            sentence_geometry,
            relation_scope_closed,
            relation_type_evidence,
            dependency_scope_evidence,
            relation_identity_determined,
            relation_type_conflict,
        )
        verdict = profile.verdict

        # I(c) far identity = the preserved P9 sentence_geometry identity (ordered
        # multi-unit identity, kept intact — never collapsed to one relation id).
        preserved_ids: tuple = (
            tuple(dict.fromkeys(sentence_geometry.identity_ids))
            if sentence_geometry is not None else tuple()
        )
        sg_ref = sentence_geometry.candidate_id if sentence_geometry is not None else "none"

        if not trace_prefix:
            trace_prefix = "relation_geometry"

        asl = QiyasNodeRef(
            node_id="اصل:relation_geometry_domain",
            node_type="RelationGeometryDomain",
            identity_ids=("identity:relation_geometry_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The accepted P9 sentence geometry rides on the far node — it preserves
        # the sentence_geometry_candidate identity (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:sentence_geometry:{uuid.uuid4().hex[:8]}",
            node_type="SentenceGeometryCandidate",
            identity_ids=preserved_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_sentence_geometry_ref:evidenced",
            "وصف:has_relation_type_evidence:evidenced",
            "وصف:has_dependency_scope_evidence:evidenced",
            "وصف:relation_scope_closed_present:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_relation_geometry_domain:verified",
            "علة:relation_geometry_composition_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:relation_geometry_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            proves.append(f"defer:{profile.reason}:present")
        else:  # VERDICT_BLOCK
            proves.append(f"فارق:{profile.reason}:present")

        rs = "1" if profile.relation_scope_closed else "0"
        rt = "1" if profile.relation_type_present else "0"
        dep = "1" if profile.dependency_scope_present else "0"
        distinct = _distinct_unit_count(sentence_geometry) if sentence_geometry is not None else 0
        carried_trace = [
            f"{SENTENCE_GEOMETRY_REF_PREFIX}{sg_ref}",
            f"{RELATION_UNIT_IDENTITIES_PREFIX}distinct={distinct}",
            f"{RELATION_GEOMETRY_EVIDENCE_PREFIX}"
            f"relation_scope_closed={rs};relation_type={rt};"
            f"dependency_scope={dep};verdict={verdict}",
            f"{RELATION_SCOPE_TRACE_PREFIX}closed={rs}",
            f"{DEPENDENCY_SCOPE_TRACE_PREFIX}present={dep}",
        ]
        if verdict == VERDICT_ACCEPT:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]
            carried_trace += [f"{CLOSED_PRIOR_PREFIX}{p}" for p in CLOSED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:relation_geometry:{uuid.uuid4().hex[:8]}",
                    source_layer="RelationGeometryQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=RELATION_GEOMETRY_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="RelationGeometryQiyas"),
        )

    def compose(
        self,
        sentence_geometry: Candidate | None,
        *,
        relation_scope_closed: bool | None = None,
        relation_type_evidence: bool | None = None,
        dependency_scope_evidence: bool | None = None,
        relation_identity_determined: bool = True,
        relation_type_conflict: bool = False,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Refine a relation-geometry possibility from a single accepted P9 candidate.

        The relation geometry drives the ACCEPT / DEFER / BLOCK verdict; ACCEPT opens
        only `irab_geometry_candidates` and closes `relation_geometry_candidates`.
        """
        return self.kernel.apply(
            self.build_request(
                sentence_geometry,
                relation_scope_closed=relation_scope_closed,
                relation_type_evidence=relation_type_evidence,
                dependency_scope_evidence=dependency_scope_evidence,
                relation_identity_determined=relation_identity_determined,
                relation_type_conflict=relation_type_conflict,
                trace_prefix=trace_prefix,
            )
        )
