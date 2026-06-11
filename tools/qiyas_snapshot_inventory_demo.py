"""Read-only progress demo for the Saleh/Qiyas project.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_snapshot_inventory_demo.py

Shows what the project has achieved across the recent PR sequence:
  - MIU / VariantResolver token-level outcomes on a sample input
  - identity-preserving vocalized surface discipline
  - frozen source snapshot inventory (SNAP-001 / SNAP-002 / MAB-001)
  - the executable consistency guard that protects the inventory
  - the current verifiable test baseline

The demo is potential-only, identity-preserving, proof/trace oriented, and
NOT semantic interpretation. It does not import source data, does not consume
any registry, does not introduce any grammar / i'rab / hukm / dalalah /
reality / meaning claim, does not modify any file. The `INVENTORY` tuple
below is the canonical mirror of the frozen snapshot files under
docs/qiyas_core/snapshots/ and is enforced against on-disk truth by
tests/qiyas_core/test_source_snapshot_inventory_demo.py.
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


MIU_SAMPLE_INPUT = "بِ ضَ وَ يَ ضَرَبَ"


@dataclass(frozen=True)
class MiuTokenOutcome:
    token: str
    miu_status: str
    resolver_status: str
    explanation: str


MIU_TOKEN_OUTCOMES: tuple[MiuTokenOutcome, ...] = (
    MiuTokenOutcome("بِ", "ACCEPTED", "ACCEPTED", "single-variant registry-eligible"),
    MiuTokenOutcome("ضَ", "BLOCKED", "BLOCKED", "blocking_fariq_present"),
    MiuTokenOutcome("وَ", "DEFERRED", "ACCEPTED", "variant ambiguity resolved by non_madd evidence"),
    MiuTokenOutcome("يَ", "DEFERRED", "BLOCKED", "ambiguity resolved but registry says not eligible"),
    MiuTokenOutcome("ضَرَبَ", "BLOCKED", "BLOCKED", "length > 1, rejected by MIU"),
)


VERIFICATION_BASELINE = {
    "focused_snapshot_test_count": 36,
    "focused_snapshot_test_label": (
        "tests/qiyas_core/test_source_snapshot_inventory_demo.py (as of PR #125)"
    ),
    "focused_miu_test_count": 17,
    "focused_miu_test_label": "tests/qiyas_core/test_variant_resolver_miu_integration.py",
    "full_suite_passed": 1365,
    "full_suite_skipped": 2,
    "full_suite_label": "tests/qiyas_core (post-PR-#125)",
}


SEPARATOR = "=" * 60


def _render_intro(lines: list[str]) -> None:
    lines.append("Saleh/Qiyas Progress Demo")
    lines.append(SEPARATOR)
    lines.append("")
    lines.append("This demonstration is:")
    lines.append("  * potential-only — no row, no claim, no judgment is final")
    lines.append("  * identity-preserving — surface_form_vocalized is identity; harakat preserved")
    lines.append("  * proof/trace oriented — separation of identity from trace per CLAUDE.md § 4")
    lines.append("  * NOT semantic interpretation — no meaning, no hukm, no reality claim")
    lines.append("")


def _render_section_1_miu_trace(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 1. MIU / VariantResolver Trace")
    lines.append(SEPARATOR)
    lines.append(f"Sample input: {MIU_SAMPLE_INPUT}")
    lines.append("")
    lines.append("Per-token outcomes (MIU / VariantResolver):")
    for outcome in MIU_TOKEN_OUTCOMES:
        lines.append(
            f"  {outcome.token:7s} MIU={outcome.miu_status:8s} "
            f"Resolver={outcome.resolver_status:8s} — {outcome.explanation}"
        )
    lines.append("")
    lines.append("This is a stable illustrative table. Outcomes are documented from prior")
    lines.append("MIU / VariantResolver focused tests; the demo does not call the runtime.")
    lines.append("")


def _render_section_2_identity_discipline(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 2. Identity Discipline")
    lines.append(SEPARATOR)
    lines.append("  identity_carrier=surface_form_vocalized")
    lines.append("  diagnostic_key=surface_form_unvocalized_key")
    lines.append("  harakat are not collapsed")
    lines.append("")
    lines.append("Identity inequalities (vocalization-distinguished pairs):")
    for left, right in IDENTITY_INEQUALITIES:
        lines.append(f"  {left} != {right}")
    lines.append("")


def _render_section_3_snapshot_inventory(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 3. Frozen Snapshot Inventory")
    lines.append(SEPARATOR)
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
    lines.append("Deferred items (not admitted; held for source-side recheck):")
    for snap in INVENTORY:
        if snap.deferred_items:
            joined = ", ".join(snap.deferred_items)
            lines.append(f"  {snap.snapshot_id} deferred: {joined}")
    lines.append("")


def _render_section_4_executable_guard(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 4. Executable Guard Status")
    lines.append(SEPARATOR)
    lines.append("  test file: tests/qiyas_core/test_source_snapshot_inventory_demo.py")
    lines.append(f"  {VERIFICATION_BASELINE['focused_snapshot_test_count']} focused tests "
                 f"(as of PR #125)")
    lines.append("  verifies demo inventory against docs/qiyas_core/snapshots/*.md")
    lines.append("")
    lines.append("The guard fails if:")
    lines.append("  * a snapshot exists on disk but is missing from the demo inventory")
    lines.append("  * the demo inventory points to a missing snapshot")
    lines.append("  * a row count drifts from on-disk row IDs")
    lines.append("  * a deferred item drifts (admitted, dropped, or surface edited)")
    lines.append("  * the not_runtime marker disappears from a frozen snapshot")
    lines.append("")


def _render_section_5_verification_baseline(lines: list[str]) -> None:
    baseline = VERIFICATION_BASELINE
    lines.append(SEPARATOR)
    lines.append("## 5. Current Verification Baseline")
    lines.append(SEPARATOR)
    lines.append(
        f"  focused snapshot inventory test: "
        f"{baseline['focused_snapshot_test_count']} passed (PR #125 milestone)"
    )
    lines.append(
        f"  focused MIU integration: {baseline['focused_miu_test_count']} passed"
    )
    lines.append(
        f"  full canonical suite (tests/qiyas_core, post-PR-#125): "
        f"{baseline['full_suite_passed']} passed / "
        f"{baseline['full_suite_skipped']} skipped"
    )
    lines.append("")


def _render_section_6_constitutional_boundary(lines: list[str]) -> None:
    lines.append(SEPARATOR)
    lines.append("## 6. Constitutional Boundary")
    lines.append(SEPARATOR)
    lines.append("This demonstration explicitly does NOT:")
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
    lines.append("End of Saleh/Qiyas Progress Demo.")


def render_progress_demo() -> str:
    lines: list[str] = []
    _render_intro(lines)
    _render_section_1_miu_trace(lines)
    _render_section_2_identity_discipline(lines)
    _render_section_3_snapshot_inventory(lines)
    _render_section_4_executable_guard(lines)
    _render_section_5_verification_baseline(lines)
    _render_section_6_constitutional_boundary(lines)
    return "\n".join(lines)


def render_inventory() -> str:
    return render_progress_demo()


def main() -> int:
    print(render_progress_demo())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
