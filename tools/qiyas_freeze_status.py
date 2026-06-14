"""Read-only freeze/readiness status check for the Saleh/Qiyas project.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_freeze_status.py

Shows whether the project is still under the REC freeze (per
docs/qiyas_core/PROJECT_RECOVERY_CANONICAL_MAP.md § 1), what is blocked,
what is allowed during the freeze, and what the unblock condition is.

This is a terminal-readable status artifact, NOT an authority engine. It
does not query GitHub, does not call any runtime, does not parse the
recovery doc, and does not engage any open PR. The freeze state is
hardcoded against the maintainer's published declaration; the recovery
doc itself remains the constitutional authority.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecQueueItem:
    rec_id: str
    label: str
    status: str
    signal: str


REC_QUEUE: tuple[RecQueueItem, ...] = (
    RecQueueItem(
        rec_id="REC-0",
        label="PROJECT_RECOVERY_CANONICAL_MAP.md (this document)",
        status="landed",
        signal="reference map; merged via PR #122 and present on main",
    ),
    RecQueueItem(
        rec_id="REC-1",
        label="Responsibility Matrix",
        status="done",
        signal="merged on main — Responsibility Matrix doc + REC1-* enforcement tests (PR #134)",
    ),
    RecQueueItem(
        rec_id="REC-2",
        label="Canonical Layer Registry alignment",
        status="done",
        signal="merged on main — SCG- phase prefixes + §3 origin notes (PR #136)",
    ),
    RecQueueItem(
        rec_id="REC-3",
        label="Naming Correction Plan / HarakaFunctionCarrier rename",
        status="done",
        signal="merged on main — HarakaFunctionCarrier → HarakaMarkIdentityCarrier (PR #137)",
    ),
    RecQueueItem(
        rec_id="REC-4",
        label="Binary- boundary enforcement",
        status="recorded outside Saleh- (Binary-side / maintainer-owned)",
        signal="recorded in Saleh-; performed in Binary- by the maintainer; Saleh- writes are forbidden",
    ),
    RecQueueItem(
        rec_id="REC-5",
        label="YAML Schema",
        status="done",
        signal="merged on main — validated LayerSpec schema under schemas/slot_geometry/ (PR #138)",
    ),
    RecQueueItem(
        rec_id="REC-6",
        label="Runtime resumption / layer-by-layer unfreeze",
        status="blocked until prior REC items complete and maintainer explicitly lifts freeze",
        signal="no public signal observed",
    ),
)


SALEH_SCOPE_BOUNDARY: tuple[str, ...] = (
    "Saleh- may report REC-4, but must not implement Binary- boundary enforcement.",
    "Binary- repo writes are outside this repository's allowed scope.",
    "PR #123, if present externally, is not consumed by this tool.",
)


STILL_BLOCKED: tuple[str, ...] = (
    "P1 runtime",
    "YAML implementation",
    "Lambert W machinery",
    "HarakaFunction runtime",
    "LetterIdentity runtime",
    "MAB-002",
    "SNAP-003",
    "Track B / C / D",
    "runtime registry work",
    "syllable registry",
    "syllable segmentation",
    "HarakaFunction runtime / LetterIdentity runtime expansion",
    "REC-6 runtime resumption until the maintainer explicitly lifts the freeze",
    "global REC freeze release (only narrow per-layer authorizations granted)",
)


# Narrow per-layer authorizations granted by the maintainer ahead of the
# full REC-1…REC-5 sequence. Each entry must record the layer name and
# the authorization date. A narrow authorization here is NOT a global
# REC unfreeze; the global freeze remains active per §1 of the recovery
# map and §4 of REPOSITORY_RESPONSIBILITY_MATRIX.md.
NARROWLY_AUTHORIZED: tuple[str, ...] = (
    "Layer 4 LicensedSyllableCandidate runtime "
    "(potential-only, narrow authorization 2026-06-13; "
    "not a global unfreeze)",
    "BoundaryEvidence consumption by Layer 4 "
    "(read-only from qiyas_core.analysis_trace; "
    "not promoted to a standalone runtime layer)",
    "SyllableShapeEvidence / PhoneticEconomyEvidence / "
    "SyllableInvalidationEvidence (Layer 4 evidence types, potential-only)",
    "REC-5 validated LayerSpec schema/source under schemas/slot_geometry/ "
    "(potential-only source artifact, narrow freeze lift; no runtime YAML "
    "loader, no slot_geometry_yaml package)",
    "Layer 5 LicensedSyllableSequenceCandidate runtime "
    "(potential-only, narrow authorization 2026-06-14; structural composition "
    "of adjacent Layer 4 syllable candidates; not a global unfreeze, not REC-6, "
    "not Layer 6+)",
)


ALLOWED_WHILE_FROZEN: tuple[str, ...] = (
    "docs-only stabilization",
    "test-only regression guards",
    "terminal-visible demos",
    "source snapshot inventory verification",
    "consistency / readiness checks",
    "no runtime admission outside narrow per-layer authorizations",
)


UNBLOCK_CONDITIONS: tuple[str, ...] = (
    "REC-1, REC-2, REC-3, and REC-4 are complete",
    "REC-5 is completed where applicable",
    "the maintainer explicitly authorizes REC-6 runtime resumption",
    "unfreeze proceeds one layer at a time",
    "REC-1 through REC-4 must be complete",
    "maintainer must explicitly lift the freeze",
    "only then may Phase 2 / Track B readiness be considered",
    "even post-unfreeze, meaning / hukm / reality remain forbidden unless separately authorized",
)


SEPARATOR = "=" * 60


def _render_section_1_title_and_state(lines: list[str]) -> None:
    lines.append("## 1. Saleh/Qiyas Freeze Readiness Status")
    lines.append(SEPARATOR)
    lines.append("")
    lines.append("  phase=Phase 1 / stabilization")
    lines.append("  freeze_status=ACTIVE")
    lines.append("  mode=read_only_status_check")
    lines.append("  runtime_status=not_runtime")
    lines.append("")
    lines.append("This is a read-only terminal status check. It does not query GitHub,")
    lines.append("does not call any runtime, does not modify any file. The freeze state")
    lines.append("below is hardcoded against the maintainer's published")
    lines.append("PROJECT_RECOVERY_CANONICAL_MAP.md § 1 declaration. Live PR status")
    lines.append("(e.g. PR #123) is not queried by this tool.")
    lines.append("")


def _render_section_2_rec_queue(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 2. Canonical REC Queue")
    lines.append(SEPARATOR)
    lines.append("Mirrors PROJECT_RECOVERY_CANONICAL_MAP.md § 7 verbatim. Each item is")
    lines.append("docs/registry governance; no runtime implementation enters the queue")
    lines.append("before REC-6 (Runtime resumption) opens.")
    lines.append("")
    for item in REC_QUEUE:
        lines.append(f"  {item.rec_id}: {item.label}")
        lines.append(f"         status={item.status}")
        lines.append(f"         signal={item.signal}")
    lines.append("")
    lines.append("Note: this tool does not inspect PR #123 or any other open PR diff.")
    lines.append("")


def _render_section_3_saleh_scope_boundary(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 3. Saleh- Scope Boundary")
    lines.append(SEPARATOR)
    for statement in SALEH_SCOPE_BOUNDARY:
        lines.append(f"  * {statement}")
    lines.append("")


def _render_section_4_still_blocked(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 4. Still Blocked")
    lines.append(SEPARATOR)
    lines.append("While the freeze is active, the following remain blocked:")
    for blocked in STILL_BLOCKED:
        lines.append(f"  * {blocked}")
    lines.append("")


def _render_section_4_5_narrowly_authorized(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 4.5 Narrowly Authorized While Frozen")
    lines.append(SEPARATOR)
    lines.append("Narrow per-layer authorizations granted by the maintainer ahead of")
    lines.append("the full REC-1…REC-5 sequence. Each entry is a single explicit")
    lines.append("authorization for one runtime slice; the global REC freeze remains")
    lines.append("active and no other runtime layer is unfrozen by these entries.")
    lines.append("")
    for entry in NARROWLY_AUTHORIZED:
        lines.append(f"  * {entry}")
    lines.append("")
    lines.append("These narrow authorizations do not lift the global freeze,")
    lines.append("do not authorize Layer 6 or higher,")
    lines.append("do not authorize semantic runtime,")
    lines.append("and do not introduce meaning / hukm / i'rab / dalalah / reality claims.")
    lines.append("")


def _render_section_5_allowed_while_frozen(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 5. Allowed While Frozen")
    lines.append(SEPARATOR)
    lines.append("The following are allowed while the freeze is active:")
    for allowed in ALLOWED_WHILE_FROZEN:
        lines.append(f"  * {allowed}")
    lines.append("")


def _render_section_6_unblock_condition(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 6. Unblock Condition")
    lines.append(SEPARATOR)
    lines.append("Runtime remains blocked until:")
    for condition in UNBLOCK_CONDITIONS:
        lines.append(f"  * {condition}")
    lines.append("")


def _render_section_7_constitutional_boundary(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 7. Constitutional Boundary")
    lines.append(SEPARATOR)
    lines.append("This status check explicitly does NOT:")
    lines.append("  * admit any row into runtime")
    lines.append("  * create or modify any registry")
    lines.append("  * perform any source correction")
    lines.append("  * import external source data")
    lines.append("  * access new_arabic_analyzer/")
    lines.append("  * make any grammar / i'rab / meaning / hukm / dalalah / reality claim")
    lines.append("  * introduce WordCandidate / LafzCandidate / DalalahCandidate types")
    lines.append("  * introduce FinalMeaning / HukmCandidate / RealityClaim types")
    lines.append("  * introduce Amil runtime / I'rab runtime / "
                 "AmilEffectEvidence / I'rabEffectEvidence")
    lines.append("")
    lines.append("End of Saleh/Qiyas Freeze Readiness Status.")


def render_freeze_status() -> str:
    lines: list[str] = []
    _render_section_1_title_and_state(lines)
    _render_section_2_rec_queue(lines)
    _render_section_3_saleh_scope_boundary(lines)
    _render_section_4_still_blocked(lines)
    _render_section_4_5_narrowly_authorized(lines)
    _render_section_5_allowed_while_frozen(lines)
    _render_section_6_unblock_condition(lines)
    _render_section_7_constitutional_boundary(lines)
    return "\n".join(lines)


def main() -> int:
    print(render_freeze_status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
