"""SlotGeometryQiyas rules — Phase-2 Batch 1.

Implements the controlling rules for `SlotGeometryQiyas` per
`SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md` (§§1–6, §9, §11):

  * SLOT_GEOMETRY_SEED_RULE
    Input:  SlotCandidate (a Phase-1 slot composition output).
    Output: SlotGeometryCandidate (construction_mode = "seed").

  * SLOT_GEOMETRY_EXTEND_RULE
    Input:  SlotGeometryCandidate (the previous geometry).
    Output: SlotGeometryCandidate (construction_mode = "extension",
            length incremented by 1).

Both rules emit the **single** admissible output type
`SlotGeometryCandidate` (contract §9). `Seed` and `Extend` are
**construction modes** carried on the geometry's `trace_ids`, not
distinct candidate types. `SlotGeometrySeedCandidate` and
`SlotGeometryExtensionCandidate` are explicitly **not** reserved as
independent output types under the contract; introducing either
requires a strictly later contract PR that reopens the decision.

`MinimalCompletionReadinessCandidate` remains a future-reserved
concept name only and is **not** an admissible output of this
contract.

Per CLAUDE.md §0/§1 the rules below introduce no new claim prefix,
no new gate, and no new rank. The Arabic-rooted claim grammar
(`اصل: / فرع: / وصف: / علة: / فارق: / وادي:`) fixed by
`TERMINOLOGY_MAP.md` §4 is the canonical grammar consumed by the
kernel; the public English prefixes appear in documentation only.

Forbidden outputs are declared locally in `_FORBIDDEN_SLOT_GEOMETRY`
below rather than added to `forbidden_outputs.py`, to keep this
Batch Implementation PR's scope inside the three new files plus an
export entry in `rules/__init__.py`. Centralising the tuple into
`forbidden_outputs.py` is a separate Micro Safety PR per
`PR_SCHEDULING_POLICY.md` §1.2.
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


# Forbidden outputs for SlotGeometryQiyas. Composed from:
#   * CONSTITUTIONAL_BASE (HukmCandidate, RealityClaim, FinalMeaning),
#   * the contract §9 list (eight higher-layer typed units that
#     SlotGeometryQiyas may not produce),
#   * the contract §11 forbidden-jump list (final judgments and
#     higher-layer typed units the slot-geometry layer must not
#     skip into).
#
# `MinimalCompletionReadinessCandidate` appears here because §9 of
# the alignment-trace contract explicitly states that it is a
# future-reserved name only and is NOT an admissible output of this
# contract. A later implementation PR may reopen this decision.
_FORBIDDEN_SLOT_GEOMETRY: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "FinalCaseJudgment",
    "DalalahCandidate",
    "WordCandidate",
    "LafzCandidate",
    "SentenceCandidate",
    "ParagraphCandidate",
    "DiscourseGeometryCandidate",
    "TextGeometryCandidate",
    "MinimalCompletionReadinessCandidate",
)


_SLOT_GEOMETRY_LAYER = "SlotGeometryQiyas"
_SLOT_GEOMETRY_DOMAIN = "SlotGeometryDomain"


# ---------------------------------------------------------------------------
# 1. SLOT_GEOMETRY_SEED_RULE
#
#    SlotCandidate → SlotGeometryCandidate(length=1, construction_mode="seed")
#
#    The seed is the degenerate `n = 1` base case of the recursive
#    law (§3.1 of the alignment-trace contract). It admits a single
#    SlotCandidate as a one-unit geometry, *only* if the
#    SlotCandidate satisfies the §2 consumed-contract conditions.
# ---------------------------------------------------------------------------

SLOT_GEOMETRY_SEED_RULE = QiyasRule(
    rule_id="slot_geometry.seed",
    layer=_SLOT_GEOMETRY_LAYER,
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type=_SLOT_GEOMETRY_DOMAIN,
    far_type="SlotCandidate",
    required_effective_wasf=(
        # §2.1 — structural witnesses of the consumed SlotCandidate.
        "input_is_slot_candidate",
        "source_rule_is_slot_composition",
        "candidate_only_flag_present",
        "no_forbidden_final_flags",
        "identity_ids_non_empty",
        "identity_trace_disjoint",
        "rank_above_no_evidence",
        # §2.2 — required trace audit.
        "alignment_ref_in_trace",
        "letter_identity_source_audited",
        "haraka_function_source_audited",
        "position_source_audited",
        "cts_carrier_binding_source_audited",
        # §3.1 — the seed-specific witness.
        "slot_geometry_seed_admitted",
        "construction_mode_seed_evidenced",
        "geometry_length_one_evidenced",
    ),
    required_illah=(
        "belongs_to_slot_geometry_domain",
        "slot_geometry_seed_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        # §2.3 rejection discipline + §11 forbidden jumps mapped to
        # invalidating-difference claims so the kernel blocks them.
        "input_not_slot_candidate",
        "source_rule_not_slot_composition",
        "missing_alignment_ref",
        "candidate_only_missing",
        "forbidden_final_flag_present",
        "identity_ids_empty",
        "identity_trace_overlap",
        "rank_zero",
        "construction_mode_conflict",
    ),
    neutral_identity_domain="slot_geometry_identity",
    output_candidate_type="SlotGeometryCandidate",
    forbidden_outputs=_FORBIDDEN_SLOT_GEOMETRY,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# ---------------------------------------------------------------------------
# 2. SLOT_GEOMETRY_EXTEND_RULE
#
#    SlotGeometryCandidate(length=n)
#      + SlotCandidate
#      + SlotBindingEvidence
#    → SlotGeometryCandidate(length=n+1, construction_mode="extension")
#
#    The extension is the `n + 1` step of the recursive law (§3.2 of
#    the alignment-trace contract). The new SlotCandidate must
#    satisfy §2; the binding evidence must witness the twelve
#    claims of §5; and the result is a length-(n+1) geometry with
#    `construction_mode == "extension"`.
# ---------------------------------------------------------------------------

SLOT_GEOMETRY_EXTEND_RULE = QiyasRule(
    rule_id="slot_geometry.extend",
    layer=_SLOT_GEOMETRY_LAYER,
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type=_SLOT_GEOMETRY_DOMAIN,
    # The far of an extension request carries the combined identity
    # of the previous geometry and the new slot. The far_type is the
    # previous-geometry type, mirroring the slot-composition rule's
    # use of far_type for the principal input.
    far_type="SlotGeometryCandidate",
    required_effective_wasf=(
        # §2.1 + §2.2 for the consumed NEW SlotCandidate.
        "input_is_slot_candidate",
        "source_rule_is_slot_composition",
        "candidate_only_flag_present",
        "no_forbidden_final_flags",
        "identity_ids_non_empty",
        "identity_trace_disjoint",
        "rank_above_no_evidence",
        "alignment_ref_in_trace",
        "letter_identity_source_audited",
        "haraka_function_source_audited",
        "position_source_audited",
        "cts_carrier_binding_source_audited",
        # §3.2 — the previous geometry is itself a valid
        # SlotGeometryCandidate.
        "previous_is_slot_geometry_candidate",
        "previous_geometry_valid",
        # §5 — the twelve binding-evidence witnesses.
        "binding_evidence_present",
        "same_intra_utterance_segment",
        "ordered_after",
        "adjacent_or_licensed_distance",
        "no_whitespace_boundary_crossing",
        "no_punctuation_boundary_crossing",
        "no_tokenizer_boundary_between_slots",
        "rank_meet_valid",
        "identity_preservation_holds",
        "trace_preservation_holds",
        "residual_preservation_holds",
        "no_blocking_difference",
        # §3.2 — the extension-specific witnesses.
        "construction_mode_extension_evidenced",
        "geometry_length_incremented_evidenced",
    ),
    required_illah=(
        "belongs_to_slot_geometry_domain",
        "slot_geometry_extension_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        # §2.3 rejection discipline.
        "input_not_slot_candidate",
        "source_rule_not_slot_composition",
        "missing_alignment_ref",
        "candidate_only_missing",
        "forbidden_final_flag_present",
        "identity_ids_empty",
        "identity_trace_overlap",
        "rank_zero",
        # §3.2 + §5 specific differences.
        "previous_not_slot_geometry_candidate",
        "binding_evidence_missing",
        "cross_segment_binding",
        "whitespace_boundary_crossing",
        "punctuation_boundary_crossing",
        "tokenizer_boundary_crossing",
        "not_ordered_after",
        "distance_not_licensed",
        "construction_mode_conflict",
        "rank_meet_invalid",
    ),
    neutral_identity_domain="slot_geometry_identity",
    output_candidate_type="SlotGeometryCandidate",
    forbidden_outputs=_FORBIDDEN_SLOT_GEOMETRY,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# Public registry — symmetric with sister rule modules.
SLOT_GEOMETRY_RULES: tuple[QiyasRule, ...] = (
    SLOT_GEOMETRY_SEED_RULE,
    SLOT_GEOMETRY_EXTEND_RULE,
)


def get_slot_geometry_rule_for_construction_mode(mode: str) -> QiyasRule | None:
    """Return the rule that drives a given construction mode.

    ``mode == "seed"``      → ``SLOT_GEOMETRY_SEED_RULE``
    ``mode == "extension"`` → ``SLOT_GEOMETRY_EXTEND_RULE``

    Returns ``None`` for any other input.
    """
    if mode == "seed":
        return SLOT_GEOMETRY_SEED_RULE
    if mode == "extension":
        return SLOT_GEOMETRY_EXTEND_RULE
    return None
