"""Tests for the source snapshot inventory demo at tools/qiyas_snapshot_inventory_demo.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_SCRIPT = REPO_ROOT / "tools" / "qiyas_snapshot_inventory_demo.py"


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
    assert "Saleh/Qiyas Source Snapshot Inventory Demo" in demo_output


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


def test_no_grammar_or_meaning_claims(demo_output: str) -> None:
    forbidden_claims = (
        "WordCandidate",
        "LafzCandidate",
        "DalalahCandidate",
        "FinalMeaning",
        "HukmCandidate",
        "RealityClaim",
        "AmilEffectEvidence",
        "I'rabEffectEvidence",
    )
    for claim in forbidden_claims:
        assert claim not in demo_output, (
            f"forbidden higher-layer-artefact name {claim!r} appeared in demo output"
        )
