"""
SentenceGeometryLayerAdapter — SCG-P9 adapter (information-gain, FIRST multi-unit layer).

Composes a candidate-only **sentence geometry** from **≥2 distinct word/segment-level
units**, each of which produced accepted P8 `AmilMamulCandidate` evidence, emitting a
`SentenceGeometryCandidate` (SENTENCE_GEOMETRY_CONSTITUTION.md + SCG-P9 design gate /
design resolution).

UNIT RULE (critical):
  A P9 *unit* is a word/segment-level structural unit with accepted P8 evidence. A
  single word (e.g. ضَرَبَ), even if it produced several accepted P8 traces
  internally, is **one** unit. P9 ACCEPT requires **≥2 distinct** units; adjacency
  is evaluated **between distinct units**, never between slots inside one word.

Discrimination (kernel `defer:` / `فارق:` machinery — no hardcoded all-pass):
  ACCEPT : ≥2 distinct units, structurally-licensed adjacency (contiguous unit
           ordering), a closed sentence-geometry boundary → opens
           `relation_geometry_candidates` (prior, ACCEPT only).
  DEFER  : ≥2 units but under-determined — adjacency_underspecified /
           sentence_boundary_underspecified / relation_coverage_underspecified /
           carried_upstream_residuals / identity_join_underspecified.
  BLOCK  : structural contradiction — sentence_structure_blocked (<2 units),
           identity_collapse_blocked (units collapse to <2 distinct),
           sentence_type_conflict, forbidden_output_attempted.

CANDIDATE-ONLY / potential-only: identity-preserving (I(c) = union of the units'
identities), identity disjoint from trace, residual-preserving. NOT i'rab / case /
ifadah / meaning / dalalah / final-syntax / hukm / reality, NOT any P10+ candidate.

Identity representation (design resolution Q4):
  I(c) = union of the upstream P8 identity sets (kernel-preserved).
  T(c) additionally carries an *ordered tuple* of the per-unit identity sets for
  trace readability — kept strictly in the trace, disjoint from identity.
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .forbidden_outputs import FORBIDDEN_SENTENCE_GEOMETRY
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.sentence_geometry_rules import (
    ADJACENCY_UNDERSPECIFIED,
    CARRIED_UPSTREAM_RESIDUALS,
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    IDENTITY_JOIN_UNDERSPECIFIED,
    OPENED_PRIORS,
    RELATION_COVERAGE_UNDERSPECIFIED,
    SENTENCE_BOUNDARY_UNDERSPECIFIED,
    SENTENCE_GEOMETRY_RULE,
    SENTENCE_STRUCTURE_BLOCKED,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
AMIL_MAMUL_REFS_PREFIX = "amil_mamul_refs:"
SENTENCE_UNIT_IDENTITIES_PREFIX = "sentence_unit_identities:"
SENTENCE_GEOMETRY_EVIDENCE_PREFIX = "sentence_geometry_evidence:"
ADJACENCY_EVIDENCE_PREFIX = "adjacency_evidence:"
ISNAD_BOUNDARY_EVIDENCE_PREFIX = "isnad_boundary_evidence:"
OPENED_PRIOR_PREFIX = "opens_prior:"

# Structural verdicts.
VERDICT_ACCEPT = "accept"
VERDICT_DEFER = "defer"
VERDICT_BLOCK = "block"

# Forbidden output type names a unit's trace must never carry (defensive scan).
_FORBIDDEN_EVIDENCE_TOKENS = frozenset(FORBIDDEN_SENTENCE_GEOMETRY)
# P8 relation evidence each unit is expected to carry (relation coverage).
_RELATION_EVIDENCE_MARKER = "amil_mamul_prior_type:"


@dataclass(frozen=True)
class SentenceUnit:
    """A word/segment-level P9 unit: a representative accepted P8 candidate + its
    structural position (segment ordinal) used for adjacency."""

    candidate: Candidate
    position: int


def _unit_identity_key(unit: SentenceUnit) -> frozenset:
    """Distinctness key for a unit — its codepoint identities (a word's geometry)."""
    return frozenset(
        iid for iid in unit.candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    ) or frozenset(unit.candidate.identity_ids)


def _unit_codepoints(unit: SentenceUnit) -> str:
    cps = sorted(
        iid[len("identity:codepoint:"):]
        for iid in unit.candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    )
    return "+".join(cps) or "none"


@dataclass(frozen=True)
class SentenceGeometryProfile:
    """Structural multi-unit profile derived from the ≥2 P9 units."""

    n_raw: int
    n_distinct: int
    contiguous: bool
    boundary_closed: bool
    relation_coverage: bool
    carried_residuals: bool
    all_units_have_codepoint_id: bool
    forbidden_attempted: bool
    sentence_type_conflict: bool

    @property
    def verdict(self) -> str:
        # BLOCK — structural contradictions first.
        if self.forbidden_attempted:
            return VERDICT_BLOCK
        if self.sentence_type_conflict:
            return VERDICT_BLOCK
        if self.n_raw < 2 or self.n_distinct == 0:
            return VERDICT_BLOCK            # sentence_structure_blocked
        if self.n_distinct < 2:
            return VERDICT_BLOCK            # identity_collapse_blocked
        # DEFER — admissible (≥2 distinct units) but under-determined.
        if not self.boundary_closed:
            return VERDICT_DEFER
        if not self.relation_coverage:
            return VERDICT_DEFER
        if self.carried_residuals:
            return VERDICT_DEFER
        if not self.all_units_have_codepoint_id:
            return VERDICT_DEFER
        if not self.contiguous:
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
            if self.sentence_type_conflict:
                return "sentence_type_conflict"
            if self.n_raw < 2 or self.n_distinct == 0:
                return SENTENCE_STRUCTURE_BLOCKED
            return IDENTITY_COLLAPSE_BLOCKED
        # DEFER reasons (same precedence as verdict()).
        if not self.boundary_closed:
            return SENTENCE_BOUNDARY_UNDERSPECIFIED
        if not self.relation_coverage:
            return RELATION_COVERAGE_UNDERSPECIFIED
        if self.carried_residuals:
            return CARRIED_UPSTREAM_RESIDUALS
        if not self.all_units_have_codepoint_id:
            return IDENTITY_JOIN_UNDERSPECIFIED
        return ADJACENCY_UNDERSPECIFIED


def _build_profile(
    units: list[SentenceUnit],
    boundary_closed: bool,
    sentence_type_conflict: bool,
) -> SentenceGeometryProfile:
    n_raw = len(units)
    keys = [_unit_identity_key(u) for u in units]
    n_distinct = len({k for k in keys})
    positions = sorted(u.position for u in units)
    contiguous = (
        len(positions) >= 2
        and len(set(positions)) == len(positions)
        and positions[-1] - positions[0] == len(positions) - 1
    )
    relation_coverage = all(
        any(t.startswith(_RELATION_EVIDENCE_MARKER) for t in u.candidate.trace_ids)
        for u in units
    ) if units else False
    carried_residuals = any(bool(u.candidate.residuals) for u in units)
    all_units_have_codepoint_id = bool(units) and all(
        any(iid.startswith("identity:codepoint:") for iid in u.candidate.identity_ids)
        for u in units
    )
    forbidden_attempted = any(
        any(tok in t for tok in _FORBIDDEN_EVIDENCE_TOKENS)
        for u in units for t in u.candidate.trace_ids
    )
    return SentenceGeometryProfile(
        n_raw=n_raw,
        n_distinct=n_distinct,
        contiguous=contiguous,
        boundary_closed=boundary_closed,
        relation_coverage=relation_coverage,
        carried_residuals=carried_residuals,
        all_units_have_codepoint_id=all_units_have_codepoint_id,
        forbidden_attempted=forbidden_attempted,
        sentence_type_conflict=sentence_type_conflict,
    )


@dataclass
class SentenceGeometryLayerAdapter:
    """Adapter that composes a multi-unit sentence-geometry possibility."""

    kernel: QiyasKernel

    def build_request(
        self,
        units: list[SentenceUnit],
        boundary_closed: bool = True,
        sentence_type_conflict: bool = False,
        trace_prefix: str = "",
    ) -> QiyasRequest:
        """Build a QiyasRequest composing a sentence geometry from ≥2 units."""
        profile = _build_profile(units, boundary_closed, sentence_type_conflict)
        verdict = profile.verdict

        ordered = sorted(units, key=lambda u: u.position)
        # I(c) far identity = union of all units' identities (kernel-preserved).
        union_ids: tuple = tuple(dict.fromkeys(
            iid for u in ordered for iid in u.candidate.identity_ids
        ))
        signature = (
            "sentsig:units="
            + ",".join(f"{u.position}:{_unit_codepoints(u)}" for u in ordered)
        ) or "sentsig:none"

        if not trace_prefix:
            trace_prefix = "sentence_geometry"

        asl = QiyasNodeRef(
            node_id="اصل:sentence_geometry_domain",
            node_type="SentenceGeometryDomain",
            identity_ids=("identity:sentence_geometry_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        # The multi-unit collection of accepted P8 candidates rides on the far node —
        # it preserves the union of amil_mamul_candidate_identities (every verdict).
        far = QiyasNodeRef(
            node_id=f"فرع:amil_mamul_units:{uuid.uuid4().hex[:8]}",
            node_type="AmilMamulCandidate",
            identity_ids=union_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_amil_mamul_refs:evidenced",
            "وصف:has_sentence_type_evidence:evidenced",
            "وصف:has_isnad_boundary_evidence:evidenced",
            "وصف:multi_unit_geometry_present:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_sentence_geometry_domain:verified",
            "علة:sentence_geometry_composition_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]

        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:sentence_geometry_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            proves.append(f"defer:{profile.reason}:present")
        else:  # VERDICT_BLOCK
            proves.append(f"فارق:{profile.reason}:present")

        closed = "1" if profile.boundary_closed else "0"
        contig = "1" if profile.contiguous else "0"
        # Ordered tuple of per-unit identity sets — kept in TRACE, not identity.
        ordered_tuple = ";".join(
            f"u{u.position}=[{_unit_codepoints(u)}]" for u in ordered
        )
        refs = "+".join(u.candidate.candidate_id for u in ordered) or "none"
        carried_trace = [
            f"{AMIL_MAMUL_REFS_PREFIX}{refs}",
            f"{SENTENCE_UNIT_IDENTITIES_PREFIX}{ordered_tuple}",
            f"{SENTENCE_GEOMETRY_EVIDENCE_PREFIX}"
            f"units={profile.n_raw};distinct={profile.n_distinct};"
            f"adjacency={contig};boundary={closed};verdict={verdict}",
            f"{ADJACENCY_EVIDENCE_PREFIX}"
            f"positions={','.join(str(u.position) for u in ordered)};contiguous={contig}",
            f"{ISNAD_BOUNDARY_EVIDENCE_PREFIX}closed={closed}",
        ]
        if verdict == VERDICT_ACCEPT:
            carried_trace += [f"{OPENED_PRIOR_PREFIX}{p}" for p in OPENED_PRIORS]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:sentence_geometry:{uuid.uuid4().hex[:8]}",
                    source_layer="SentenceGeometryQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )

        return QiyasRequest(
            rule=SENTENCE_GEOMETRY_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="SentenceGeometryQiyas"),
        )

    def compose(
        self,
        units: list[SentenceUnit],
        boundary_closed: bool = True,
        sentence_type_conflict: bool = False,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Compose a sentence-geometry possibility from ≥2 word/segment-level units.

        The multi-unit structural geometry drives the ACCEPT / DEFER / BLOCK verdict;
        ACCEPT opens only `relation_geometry_candidates`.
        """
        return self.kernel.apply(
            self.build_request(units, boundary_closed, sentence_type_conflict, trace_prefix)
        )
