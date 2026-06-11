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
        rec_id="REC-1",
        label="repository responsibility matrix / governance ownership",
        status="open_or_pending",
        signal="PR #123 may exist as DRAFT (live PR status not queried by this tool)",
    ),
    RecQueueItem(
        rec_id="REC-2",
        label="pending",
        status="pending",
        signal="no public signal observed",
    ),
    RecQueueItem(
        rec_id="REC-3",
        label="pending",
        status="pending",
        signal="no public signal observed",
    ),
    RecQueueItem(
        rec_id="REC-4",
        label="pending",
        status="pending",
        signal="no public signal observed",
    ),
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
)


ALLOWED_WHILE_FROZEN: tuple[str, ...] = (
    "docs-only stabilization",
    "test-only regression guards",
    "terminal-visible demos",
    "source snapshot inventory verification",
    "consistency / readiness checks",
    "no runtime admission",
)


UNBLOCK_CONDITIONS: tuple[str, ...] = (
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
    lines.append("## 2. REC Queue")
    lines.append(SEPARATOR)
    for item in REC_QUEUE:
        lines.append(f"  {item.rec_id}: {item.label}")
        lines.append(f"         status={item.status}")
        lines.append(f"         signal={item.signal}")
    lines.append("")
    lines.append("Note: this tool does not inspect PR #123 or any other open PR diff.")
    lines.append("")


def _render_section_3_still_blocked(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 3. Still Blocked")
    lines.append(SEPARATOR)
    lines.append("While the freeze is active, the following remain blocked:")
    for blocked in STILL_BLOCKED:
        lines.append(f"  * {blocked}")
    lines.append("")


def _render_section_4_allowed_while_frozen(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 4. Allowed While Frozen")
    lines.append(SEPARATOR)
    lines.append("The following are allowed while the freeze is active:")
    for allowed in ALLOWED_WHILE_FROZEN:
        lines.append(f"  * {allowed}")
    lines.append("")


def _render_section_5_unblock_condition(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 5. Unblock Condition")
    lines.append(SEPARATOR)
    for condition in UNBLOCK_CONDITIONS:
        lines.append(f"  * {condition}")
    lines.append("")


def _render_section_6_constitutional_boundary(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 6. Constitutional Boundary")
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
    _render_section_3_still_blocked(lines)
    _render_section_4_allowed_while_frozen(lines)
    _render_section_5_unblock_condition(lines)
    _render_section_6_constitutional_boundary(lines)
    return "\n".join(lines)


def main() -> int:
    print(render_freeze_status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
