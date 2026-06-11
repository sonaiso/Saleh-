"""Tests for the freeze/readiness status check at tools/qiyas_freeze_status.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
STATUS_SCRIPT = REPO_ROOT / "tools" / "qiyas_freeze_status.py"


@pytest.fixture(scope="module")
def status_output() -> str:
    result = subprocess.run(
        [sys.executable, str(STATUS_SCRIPT)],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": f"{REPO_ROOT / 'src'}:{REPO_ROOT}"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"freeze status exited with code {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return result.stdout


def test_status_script_exists() -> None:
    assert STATUS_SCRIPT.is_file(), f"freeze status script missing at {STATUS_SCRIPT}"


def test_title_present(status_output: str) -> None:
    assert "Saleh/Qiyas Freeze Readiness Status" in status_output


def test_state_markers_present(status_output: str) -> None:
    for marker in (
        "phase=Phase 1 / stabilization",
        "freeze_status=ACTIVE",
        "mode=read_only_status_check",
        "runtime_status=not_runtime",
    ):
        assert marker in status_output, f"state marker {marker!r} missing"


@pytest.mark.parametrize("rec_id", ["REC-1", "REC-2", "REC-3", "REC-4"])
def test_rec_queue_id_present(status_output: str, rec_id: str) -> None:
    assert rec_id in status_output, f"REC queue id {rec_id!r} missing"


def test_rec1_open_or_pending_status(status_output: str) -> None:
    rec1_index = status_output.find("REC-1")
    assert rec1_index >= 0
    rec1_section = status_output[rec1_index : rec1_index + 400]
    assert "open_or_pending" in rec1_section, (
        "REC-1 must be marked status=open_or_pending while PR #123 is unresolved"
    )


def test_pr_123_not_queried_statement_present(status_output: str) -> None:
    assert "PR #123" in status_output
    assert "not queried" in status_output


def test_section_2_rec_queue_header_present(status_output: str) -> None:
    assert "## 2. REC Queue" in status_output


def test_section_3_still_blocked_header_present(status_output: str) -> None:
    assert "## 3. Still Blocked" in status_output


def test_section_4_allowed_header_present(status_output: str) -> None:
    assert "## 4. Allowed While Frozen" in status_output


def test_section_5_unblock_header_present(status_output: str) -> None:
    assert "## 5. Unblock Condition" in status_output


def test_section_6_constitutional_boundary_header_present(status_output: str) -> None:
    assert "## 6. Constitutional Boundary" in status_output


@pytest.mark.parametrize(
    "blocked",
    [
        "P1 runtime",
        "YAML implementation",
        "Lambert W",
        "HarakaFunction runtime",
        "LetterIdentity runtime",
        "MAB-002",
        "SNAP-003",
        "Track B / C / D",
    ],
)
def test_blocked_item_present(status_output: str, blocked: str) -> None:
    assert blocked in status_output, f"blocked item {blocked!r} missing"


@pytest.mark.parametrize(
    "allowed",
    [
        "docs-only stabilization",
        "test-only regression guards",
        "terminal-visible demos",
        "source snapshot inventory verification",
        "consistency / readiness checks",
    ],
)
def test_allowed_item_present(status_output: str, allowed: str) -> None:
    assert allowed in status_output, f"allowed item {allowed!r} missing"


@pytest.mark.parametrize(
    "condition",
    [
        "REC-1 through REC-4 must be complete",
        "maintainer must explicitly lift the freeze",
    ],
)
def test_unblock_condition_present(status_output: str, condition: str) -> None:
    assert condition in status_output, f"unblock condition {condition!r} missing"


@pytest.mark.parametrize(
    "boundary_marker",
    [
        "no runtime admission",
        "create or modify any registry",
        "access new_arabic_analyzer/",
    ],
)
def test_constitutional_boundary_marker_present(
    status_output: str, boundary_marker: str
) -> None:
    assert boundary_marker in status_output, (
        f"constitutional boundary marker {boundary_marker!r} missing"
    )


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
        "freeze_status=LIFTED",
        "freeze_status=INACTIVE",
        "freeze_status=COMPLETE",
    ],
)
def test_no_positive_runtime_or_unfreeze_language(
    status_output: str, forbidden_phrase: str
) -> None:
    assert forbidden_phrase.lower() not in status_output.lower(), (
        f"forbidden positive phrase {forbidden_phrase!r} appeared in status output"
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


def test_forbidden_higher_layer_names_only_within_negation_section(
    status_output: str,
) -> None:
    """Higher-layer-artefact names may appear in the status output only after
    the explicit negation header. Positive occurrences (claiming the tool
    introduces them) are forbidden."""
    negation_index = status_output.find(NEGATION_SECTION_HEADER)
    for name in FORBIDDEN_HIGHER_LAYER_NAMES:
        first_index = status_output.find(name)
        if first_index < 0:
            continue
        assert negation_index >= 0 and first_index > negation_index, (
            f"forbidden higher-layer-artefact name {name!r} appears outside the "
            f"explicit negation section. Each occurrence must follow the "
            f"{NEGATION_SECTION_HEADER!r} header."
        )


def test_end_marker_present(status_output: str) -> None:
    assert "End of Saleh/Qiyas Freeze Readiness Status." in status_output
