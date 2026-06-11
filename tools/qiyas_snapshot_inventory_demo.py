"""Read-only inventory demo for the landed Saleh/Qiyas source snapshots.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_snapshot_inventory_demo.py

Prints a terminal-visible inventory of the three frozen snapshot files under
docs/qiyas_core/snapshots/ together with the standing identity and runtime
boundaries. Does not import source data, does not consume any registry,
does not introduce any grammar / i'rab / hukm / dalalah / reality / meaning
claim, does not modify any file.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FrozenSnapshot:
    snapshot_id: str
    snapshot_path: str
    merge_commit: str
    pr_number: int
    included_count: int
    deferred_count: int
    deferred_label: str
    deferred_items: tuple[str, ...] = field(default_factory=tuple)


INVENTORY: tuple[FrozenSnapshot, ...] = (
    FrozenSnapshot(
        snapshot_id="SNAP-001",
        snapshot_path="docs/qiyas_core/snapshots/SNAP-001_OPERATORS_GROUP1_PILOT_SNAPSHOT.md",
        merge_commit="8935094",
        pr_number=104,
        included_count=13,
        deferred_count=0,
        deferred_label="deferred_rows",
        deferred_items=(),
    ),
    FrozenSnapshot(
        snapshot_id="SNAP-002",
        snapshot_path="docs/qiyas_core/snapshots/SNAP-002_OPERATORS_COLLISION_CLASS_SNAPSHOT.md",
        merge_commit="4595887",
        pr_number=113,
        included_count=6,
        deferred_count=3,
        deferred_label="deferred_groups",
        deferred_items=("ما", "أي", "إذا"),
    ),
    FrozenSnapshot(
        snapshot_id="MAB-001",
        snapshot_path="docs/qiyas_core/snapshots/MAB-001_MABNIYAT_ADVERBIAL_FIXED_FORMS_SNAPSHOT.md",
        merge_commit="7bc9daf",
        pr_number=121,
        included_count=16,
        deferred_count=2,
        deferred_label="deferred_rows",
        deferred_items=("ثََمََّةَ", "أَيَّْنَ"),
    ),
)


IDENTITY_INEQUALITIES: tuple[tuple[str, str], ...] = (
    ("مِنْ", "مَنْ"),
    ("إِنَّ", "إِنْ"),
    ("أَنَّ", "أَنْ"),
)


def render_inventory() -> str:
    lines: list[str] = []
    lines.append("Saleh/Qiyas Source Snapshot Inventory Demo")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Identity discipline (PR #86 § 12.1):")
    lines.append("  identity_carrier=surface_form_vocalized")
    lines.append("  diagnostic_key=surface_form_unvocalized_key")
    lines.append("")
    lines.append("Frozen snapshots on main:")
    for snap in INVENTORY:
        if snap.snapshot_id == "SNAP-001":
            lines.append(f"  {snap.snapshot_id} rows={snap.included_count}")
        elif snap.snapshot_id == "SNAP-002":
            lines.append(
                f"  {snap.snapshot_id} "
                f"included_rows={snap.included_count} "
                f"deferred_groups={snap.deferred_count}"
            )
        elif snap.snapshot_id == "MAB-001":
            lines.append(
                f"  {snap.snapshot_id} "
                f"included_rows={snap.included_count} "
                f"deferred_rows={snap.deferred_count}"
            )
        lines.append(f"    path={snap.snapshot_path}")
        lines.append(f"    merge_commit={snap.merge_commit} (PR #{snap.pr_number})")
        lines.append(f"    runtime_status=not_runtime")
    lines.append("")
    lines.append("Identity inequalities (vocalization-distinguished pairs):")
    for left, right in IDENTITY_INEQUALITIES:
        lines.append(f"  {left} != {right}")
    lines.append("")
    lines.append("Deferred items (not admitted; held for source-side recheck):")
    for snap in INVENTORY:
        if snap.deferred_items:
            joined = ", ".join(snap.deferred_items)
            lines.append(f"  {snap.snapshot_id} deferred: {joined}")
    lines.append("")
    lines.append("Constitutional boundary:")
    lines.append("  runtime_status=not_runtime for every admitted row")
    lines.append("  no source data import; no registry; no fixture consumption")
    lines.append("  no grammar / i'rab / meaning / hukm / reality / dalalah claim")
    lines.append("")
    lines.append("End of inventory.")
    return "\n".join(lines)


def main() -> int:
    print(render_inventory())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
