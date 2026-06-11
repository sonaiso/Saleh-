"""Tests for the source snapshot inventory demo at tools/qiyas_snapshot_inventory_demo.py."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_SCRIPT = REPO_ROOT / "tools" / "qiyas_snapshot_inventory_demo.py"
SNAPSHOTS_DIR = REPO_ROOT / "docs" / "qiyas_core" / "snapshots"


def _load_demo_inventory() -> tuple:
    spec = importlib.util.spec_from_file_location(
        "qiyas_snapshot_inventory_demo_for_consistency_tests", DEMO_SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return tuple(module.INVENTORY)


INVENTORY = _load_demo_inventory()
INVENTORY_IDS = [entry.snapshot_id for entry in INVENTORY]
INVENTORY_ENTRIES_WITH_DEFERRED = [entry for entry in INVENTORY if entry.deferred_items]
INVENTORY_DEFERRED_IDS = [entry.snapshot_id for entry in INVENTORY_ENTRIES_WITH_DEFERRED]


@pytest.fixture(scope="module")
def demo_output() -> str:
    result = subprocess.run(
        [sys.executable, str(DEMO_SCRIPT)],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": f"{REPO_ROOT / 'src'}:{REPO_ROOT}"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"demo exited with code {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return result.stdout


def test_demo_script_exists() -> None:
    assert DEMO_SCRIPT.is_file(), f"demo script missing at {DEMO_SCRIPT}"


def test_title_present(demo_output: str) -> None:
    assert "Saleh/Qiyas Progress Demo" in demo_output


def test_all_three_snapshot_ids_present(demo_output: str) -> None:
    for snapshot_id in ("SNAP-001", "SNAP-002", "MAB-001"):
        assert snapshot_id in demo_output, f"{snapshot_id} missing from demo output"


def test_row_counts_present(demo_output: str) -> None:
    assert "SNAP-001 rows=13" in demo_output
    assert "SNAP-002 included_rows=6" in demo_output
    assert "MAB-001 included_rows=16" in demo_output


def test_deferred_counts_present(demo_output: str) -> None:
    assert "deferred_groups=3" in demo_output
    assert "deferred_rows=2" in demo_output


def test_identity_carrier_marker(demo_output: str) -> None:
    assert "identity_carrier=surface_form_vocalized" in demo_output
    assert "surface_form_vocalized" in demo_output


def test_diagnostic_key_marker(demo_output: str) -> None:
    assert "diagnostic_key=surface_form_unvocalized_key" in demo_output
    assert "surface_form_unvocalized_key" in demo_output


def test_runtime_status_marker(demo_output: str) -> None:
    assert "runtime_status=not_runtime" in demo_output
    assert "not_runtime" in demo_output


def test_identity_inequalities_present(demo_output: str) -> None:
    assert "مِنْ != مَنْ" in demo_output
    assert "إِنَّ != إِنْ" in demo_output
    assert "أَنَّ != أَنْ" in demo_output


def test_snap002_deferred_groups_listed(demo_output: str) -> None:
    assert "SNAP-002 deferred: ما, أي, إذا" in demo_output


def test_mab001_deferred_rows_listed(demo_output: str) -> None:
    assert "MAB-001 deferred: ثََمََّةَ, أَيَّْنَ" in demo_output


@pytest.mark.parametrize(
    "forbidden_phrase",
    [
        "runtime_status=runtime",
        "runtime_status=enabled",
        "runtime_admitted",
        "admitted to runtime",
        "is_runtime: true",
        "is_runtime=true",
        "runtime: enabled",
        "runtime_status: yes",
    ],
)
def test_no_positive_runtime_admission_language(demo_output: str, forbidden_phrase: str) -> None:
    assert forbidden_phrase.lower() not in demo_output.lower(), (
        f"forbidden positive runtime admission phrase {forbidden_phrase!r} appeared in demo output"
    )


FORBIDDEN_HIGHER_LAYER_NAMES = (
    "WordCandidate",
    "LafzCandidate",
    "DalalahCandidate",
    "FinalMeaning",
    "HukmCandidate",
    "RealityClaim",
    "AmilEffectEvidence",
    "I'rabEffectEvidence",
)
NEGATION_SECTION_HEADER = "explicitly does NOT"


def test_forbidden_higher_layer_names_only_within_negation_section(demo_output: str) -> None:
    """Higher-layer-artefact names may appear in the demo only after the
    explicit negation header. The demo lists them as things it does NOT
    introduce; positive occurrences (claiming the demo introduces them)
    are forbidden."""
    negation_index = demo_output.find(NEGATION_SECTION_HEADER)
    for name in FORBIDDEN_HIGHER_LAYER_NAMES:
        first_index = demo_output.find(name)
        if first_index < 0:
            continue
        assert negation_index >= 0 and first_index > negation_index, (
            f"forbidden higher-layer-artefact name {name!r} appears outside the "
            f"explicit negation section. Each occurrence must follow the "
            f"{NEGATION_SECTION_HEADER!r} header."
        )


@pytest.fixture(scope="module")
def disk_snapshot_files() -> list[Path]:
    return sorted(SNAPSHOTS_DIR.glob("*.md"))


@pytest.mark.parametrize("entry", INVENTORY, ids=INVENTORY_IDS)
def test_inventory_path_exists_on_disk(entry) -> None:
    path = REPO_ROOT / entry.snapshot_path
    assert path.is_file(), (
        f"{entry.snapshot_id}: demo INVENTORY declares snapshot_path={entry.snapshot_path!r} "
        f"but no file exists there. Either restore the file or update INVENTORY in the same PR."
    )


@pytest.mark.parametrize("entry", INVENTORY, ids=INVENTORY_IDS)
def test_inventory_snapshot_id_appears_in_file(entry) -> None:
    content = (REPO_ROOT / entry.snapshot_path).read_text(encoding="utf-8")
    assert entry.snapshot_id in content, (
        f"{entry.snapshot_id}: snapshot ID declared in demo INVENTORY does not appear "
        f"in the snapshot file at {entry.snapshot_path}"
    )


@pytest.mark.parametrize("entry", INVENTORY, ids=INVENTORY_IDS)
def test_inventory_row_ids_match_included_count(entry) -> None:
    content = (REPO_ROOT / entry.snapshot_path).read_text(encoding="utf-8")
    pattern = re.compile(rf"\b{re.escape(entry.snapshot_id)}-(\d{{3}})\b")
    unique_row_numbers = sorted({m for m in pattern.findall(content)}, key=int)
    expected_row_numbers = [f"{i:03d}" for i in range(1, entry.included_count + 1)]
    assert unique_row_numbers == expected_row_numbers, (
        f"{entry.snapshot_id}: demo INVENTORY declares included_count={entry.included_count} "
        f"(expecting row IDs {entry.snapshot_id}-001 through {entry.snapshot_id}-{entry.included_count:03d}); "
        f"file at {entry.snapshot_path} contains row IDs {[f'{entry.snapshot_id}-{n}' for n in unique_row_numbers]}. "
        f"If a row was added or removed, update INVENTORY in the same PR."
    )


@pytest.mark.parametrize(
    "entry", INVENTORY_ENTRIES_WITH_DEFERRED, ids=INVENTORY_DEFERRED_IDS
)
def test_inventory_deferred_items_appear_in_file(entry) -> None:
    content = (REPO_ROOT / entry.snapshot_path).read_text(encoding="utf-8")
    missing = [item for item in entry.deferred_items if item not in content]
    assert not missing, (
        f"{entry.snapshot_id}: demo INVENTORY declares deferred items {list(entry.deferred_items)} "
        f"but the following do not appear in the snapshot file at {entry.snapshot_path}: {missing}. "
        f"If a deferred item was admitted or removed, update INVENTORY in the same PR."
    )


NOT_RUNTIME_MARKERS = ("not_runtime", "no runtime")


@pytest.mark.parametrize("entry", INVENTORY, ids=INVENTORY_IDS)
def test_inventory_file_contains_not_runtime_marker(entry) -> None:
    content = (REPO_ROOT / entry.snapshot_path).read_text(encoding="utf-8")
    found = [marker for marker in NOT_RUNTIME_MARKERS if marker in content]
    assert found, (
        f"{entry.snapshot_id}: file at {entry.snapshot_path} contains none of the accepted "
        f"explicit not-runtime markers {list(NOT_RUNTIME_MARKERS)}. The runtime boundary must be "
        f"terminal-visible in every frozen snapshot."
    )


def test_no_orphan_snapshot_file_on_disk(disk_snapshot_files: list[Path]) -> None:
    inventory_resolved_paths = {(REPO_ROOT / e.snapshot_path).resolve() for e in INVENTORY}
    disk_resolved_paths = {p.resolve() for p in disk_snapshot_files}
    orphans = sorted(disk_resolved_paths - inventory_resolved_paths)
    assert not orphans, (
        "frozen snapshot file(s) on disk are not represented in demo INVENTORY:\n"
        + "\n".join(f"  - {p.relative_to(REPO_ROOT)}" for p in orphans)
        + "\nIf a new SNAP-NNN / MAB-NNN snapshot landed, the same PR must update "
        "tools/qiyas_snapshot_inventory_demo.py INVENTORY to include it."
    )


def test_no_dangling_inventory_path(disk_snapshot_files: list[Path]) -> None:
    inventory_resolved_paths = {(REPO_ROOT / e.snapshot_path).resolve() for e in INVENTORY}
    disk_resolved_paths = {p.resolve() for p in disk_snapshot_files}
    dangling = sorted(inventory_resolved_paths - disk_resolved_paths)
    assert not dangling, (
        "demo INVENTORY declares snapshot path(s) that do not exist on disk:\n"
        + "\n".join(f"  - {p.relative_to(REPO_ROOT)}" for p in dangling)
    )


@pytest.mark.parametrize(
    "marker",
    [
        "potential-only",
        "identity-preserving",
        "proof/trace oriented",
        "NOT semantic interpretation",
    ],
)
def test_progress_demo_intro_marker_present(demo_output: str, marker: str) -> None:
    assert marker in demo_output, f"intro marker {marker!r} missing from demo output"


def test_miu_sample_input_present(demo_output: str) -> None:
    assert "بِ ضَ وَ يَ ضَرَبَ" in demo_output


@pytest.mark.parametrize(
    "token,miu_status,resolver_status,explanation_keyword",
    [
        ("بِ", "ACCEPTED", "ACCEPTED", "single-variant registry-eligible"),
        ("ضَ", "BLOCKED", "BLOCKED", "blocking_fariq_present"),
        ("وَ", "DEFERRED", "ACCEPTED", "non_madd"),
        ("يَ", "DEFERRED", "BLOCKED", "registry says not eligible"),
        ("ضَرَبَ", "BLOCKED", "BLOCKED", "length > 1"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_miu_token_outcome_row_present(
    demo_output: str,
    token: str,
    miu_status: str,
    resolver_status: str,
    explanation_keyword: str,
) -> None:
    matching_line = None
    for line in demo_output.splitlines():
        if (
            token in line
            and f"MIU={miu_status}" in line
            and f"Resolver={resolver_status}" in line
            and explanation_keyword in line
        ):
            matching_line = line
            break
    assert matching_line is not None, (
        f"no single line contains token={token!r}, MIU={miu_status!r}, "
        f"Resolver={resolver_status!r}, and explanation keyword {explanation_keyword!r}"
    )


def test_section_1_miu_trace_header_present(demo_output: str) -> None:
    assert "## 1. MIU / VariantResolver Trace" in demo_output


def test_section_2_identity_discipline_header_present(demo_output: str) -> None:
    assert "## 2. Identity Discipline" in demo_output


def test_section_3_frozen_snapshot_inventory_header_present(demo_output: str) -> None:
    assert "## 3. Frozen Snapshot Inventory" in demo_output


def test_section_4_executable_guard_header_present(demo_output: str) -> None:
    assert "## 4. Executable Guard Status" in demo_output


def test_section_5_verification_baseline_header_present(demo_output: str) -> None:
    assert "## 5. Current Verification Baseline" in demo_output


def test_section_6_constitutional_boundary_header_present(demo_output: str) -> None:
    assert "## 6. Constitutional Boundary" in demo_output


@pytest.mark.parametrize(
    "marker",
    [
        "tests/qiyas_core/test_source_snapshot_inventory_demo.py",
        "36 focused tests",
        "verifies demo inventory against docs/qiyas_core/snapshots/",
        "snapshot exists on disk but is missing from",
        "demo inventory points to a missing snapshot",
        "row count drifts",
        "deferred item drifts",
        "not_runtime marker disappears",
    ],
)
def test_executable_guard_section_content(demo_output: str, marker: str) -> None:
    assert marker in demo_output, f"guard-section marker {marker!r} missing"


def test_focused_snapshot_test_count_marker(demo_output: str) -> None:
    assert "36 focused tests" in demo_output
    assert "36 passed" in demo_output


def test_focused_miu_baseline_marker(demo_output: str) -> None:
    assert "focused MIU integration: 17 passed" in demo_output


def test_full_suite_baseline_marker(demo_output: str) -> None:
    assert "1365 passed / 2 skipped" in demo_output


@pytest.mark.parametrize(
    "marker",
    [
        "admit any row into runtime",
        "create or modify any registry",
        "perform any source correction",
        "import external source data",
        "access new_arabic_analyzer/",
        "grammar",
        "i'rab",
        "meaning",
        "hukm",
        "dalalah",
        "reality",
    ],
)
def test_constitutional_boundary_section_content(demo_output: str, marker: str) -> None:
    assert marker in demo_output, f"boundary-section marker {marker!r} missing"


def test_end_marker_present(demo_output: str) -> None:
    assert "End of Saleh/Qiyas Progress Demo." in demo_output
