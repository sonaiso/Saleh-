"""MinimalIndependentUnitReadinessQiyas rules.

Implements the canonical rule for the readiness layer per
``MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`` (PR #71, merged).

  * MINIMAL_UNIT_READINESS_ADMIT_RULE
    Input:  SlotGeometryCandidate(length = 1, construction_mode = "seed")
    Output: MinimalUnitReadinessCandidate

The single admissible output type is ``MinimalUnitReadinessCandidate``
(contract §5). The name ``MinimalIndependentMeaningCandidate`` is
**forbidden** by §5 of the contract — readiness is not meaning. The
twelve forbidden output types (CONSTITUTIONAL_BASE + §8 list) are
declared locally as ``_FORBIDDEN_MIU_READINESS`` to keep this
batch's scope inside the three new files plus the rules/__init__.py
export, mirroring the precedent set by Phase-2 Batch 1
(``slot_geometry_rules.py``). Centralising the tuple into
``forbidden_outputs.py`` is a separate Micro Safety PR.

Per CLAUDE.md §0/§1 no new claim prefix, no new gate, and no new
rank is introduced. The Arabic-rooted claim grammar
(``اصل: / فرع: / وصف: / علة: / فارق: / وادي:``) fixed by
``TERMINOLOGY_MAP.md`` §4 is the canonical grammar consumed by the
kernel; the public English prefixes appear only in cross-layer
documentation.
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import CONSTITUTIONAL_BASE
from qiyas_core.rule import QiyasRule


_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


# Forbidden outputs for MinimalIndependentUnitReadinessQiyas, composed
# from:
#   * CONSTITUTIONAL_BASE (HukmCandidate, RealityClaim, FinalMeaning),
#   * the contract §8 list (eight higher-layer typed units plus
#     FinalCaseJudgment that the readiness layer must not produce),
#   * the forbidden type name ``MinimalIndependentMeaningCandidate``
#     (§5 — readiness is not meaning),
#   * ``SlotGeometryCandidate`` and ``SlotCandidate`` (the layer's own
#     input types — never re-emitted as output).
_FORBIDDEN_MIU_READINESS: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "FinalCaseJudgment",
    "DalalahCandidate",
    "WordCandidate",
    "LafzCandidate",
    "SentenceCandidate",
    "ParagraphCandidate",
    "DiscourseGeometryCandidate",
    "TextGeometryCandidate",
    "MinimalIndependentMeaningCandidate",
    "SlotGeometryCandidate",
    "SlotCandidate",
)


_MIU_READINESS_LAYER = "MinimalIndependentUnitReadinessQiyas"
_MIU_READINESS_DOMAIN = "MinimalIndependentUnitReadinessDomain"


# ---------------------------------------------------------------------------
# MINIMAL_UNIT_READINESS_ADMIT_RULE
#
#    SlotGeometryCandidate(length = 1, construction_mode = "seed")
#       + ArabicArticulationRegistry metadata
#       + MinimalCompleteClosureEvidence
#    → MinimalUnitReadinessCandidate
#
# Per the contract §3 the predicate Admit(S, M, E) is True iff:
#   * S satisfies §4.1 structural conditions,
#   * M.can_function_as_minimal_independent_unit == True,
#   * E (closure evidence) is not None,
#   * every §6 invariant holds.
#
# The eight failure invalidating-differences below cover every
# discriminable rejection / deferral cause.
# ---------------------------------------------------------------------------


MINIMAL_UNIT_READINESS_ADMIT_RULE = QiyasRule(
    rule_id="minimal_unit_readiness.admit",
    layer=_MIU_READINESS_LAYER,
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type=_MIU_READINESS_DOMAIN,
    far_type="SlotGeometryCandidate",
    required_effective_wasf=(
        # §4.1 — structural conditions of the consumed geometry.
        "input_is_slot_geometry_candidate",
        "geometry_length_is_one",
        "geometry_construction_mode_is_seed",
        # §4.3 — closure-evidence presence.
        "closure_evidence_present",
        # §4.2 — registry metadata witness for the geometry's symbol.
        "registry_metadata_present",
        # §5 — output discipline.
        "output_remains_candidate_only",
        "is_minimal_unit_ready_marker_emitted",
        # Note: `single_primary_articulation_resolved` and
        # `symbol_eligible_for_minimal_unit` are NOT required wasfs
        # because they are indeterminate in the DEFERRED (variant
        # ambiguity) case. Eligibility is enforced via the explicit
        # invalidating-difference `symbol_not_eligible_for_minimal_unit`
        # below — its presence blocks the ACCEPTED case, and its
        # absence (combined with `defer:variant_ambiguity:present`)
        # allows the kernel to defer. The adapter still emits both
        # wasfs as auditable claims on the ACCEPTED path for trace
        # completeness, even though the rule does not require them.
    ),
    required_illah=(
        "belongs_to_minimal_unit_readiness_domain",
        "minimal_unit_readiness_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        # §4.1 / §2.3 rejection discipline.
        "input_not_slot_geometry_candidate",
        "length_not_one",
        "construction_mode_not_seed",
        # §4.3 rejection.
        "closure_evidence_missing",
        # §4.2 rejection / deferral cases.
        "registry_metadata_missing_for_symbol",
        "symbol_not_eligible_for_minimal_unit",
        # §5 / §11 forbidden-jump enforcement.
        "miu_readiness_jumped_to_word",
        "miu_readiness_jumped_to_dalalah",
        "miu_readiness_jumped_to_meaning",
    ),
    neutral_identity_domain="minimal_unit_readiness_identity",
    output_candidate_type="MinimalUnitReadinessCandidate",
    forbidden_outputs=_FORBIDDEN_MIU_READINESS,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# Public registry — symmetric with sister rule modules.
MINIMAL_UNIT_READINESS_RULES: tuple[QiyasRule, ...] = (
    MINIMAL_UNIT_READINESS_ADMIT_RULE,
)
