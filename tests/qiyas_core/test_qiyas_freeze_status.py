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


@pytest.mark.parametrize(
    "rec_id", ["REC-0", "REC-1", "REC-2", "REC-3", "REC-4", "REC-5", "REC-6"]
)
def test_rec_queue_id_present(status_output: str, rec_id: str) -> None:
    assert rec_id in status_output, f"REC queue id {rec_id!r} missing"


def test_rec1_done_status(status_output: str) -> None:
    """REC-1 has merged (PR #134); the queue must no longer mark it pending."""
    rec1_index = status_output.find("REC-1")
    assert rec1_index >= 0
    rec1_section = status_output[rec1_index : rec1_index + 400]
    assert "status=done" in rec1_section, "REC-1 must be marked status=done after merge"
    assert "open_or_pending" not in rec1_section, (
        "REC-1 stale 'open_or_pending' status must be reconciled after merge"
    )


def test_pr_123_not_queried_statement_present(status_output: str) -> None:
    assert "PR #123" in status_output
    assert "not queried" in status_output


def test_section_2_rec_queue_header_present(status_output: str) -> None:
    assert "## 2. Canonical REC Queue" in status_output


def test_section_3_saleh_scope_boundary_header_present(status_output: str) -> None:
    assert "## 3. Saleh- Scope Boundary" in status_output


def test_section_4_still_blocked_header_present(status_output: str) -> None:
    assert "## 4. Still Blocked" in status_output


def test_section_5_allowed_header_present(status_output: str) -> None:
    assert "## 5. Allowed While Frozen" in status_output


def test_section_6_unblock_header_present(status_output: str) -> None:
    assert "## 6. Unblock Condition" in status_output


def test_section_7_constitutional_boundary_header_present(status_output: str) -> None:
    assert "## 7. Constitutional Boundary" in status_output


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


# --- Canonical REC map alignment tests ------------------------------------


def test_canonical_rec_queue_header_phrase_present(status_output: str) -> None:
    assert "Canonical REC Queue" in status_output


def test_rec0_references_canonical_map_filename(status_output: str) -> None:
    assert "PROJECT_RECOVERY_CANONICAL_MAP.md" in status_output


def test_rec1_label_present(status_output: str) -> None:
    assert "Responsibility Matrix" in status_output


def test_rec2_label_present(status_output: str) -> None:
    assert "Canonical Layer Registry alignment" in status_output


def test_rec3_label_present(status_output: str) -> None:
    assert "Naming Correction Plan" in status_output


def test_rec3_haraka_function_carrier_mentioned(status_output: str) -> None:
    assert "HarakaFunctionCarrier" in status_output


def test_rec4_label_present(status_output: str) -> None:
    assert "Binary- boundary enforcement" in status_output


def test_rec4_saleh_scope_statement_present(status_output: str) -> None:
    """The Saleh- scope boundary must explicitly state that Binary- work is
    outside this repository's allowed scope."""
    assert (
        "Binary- repo writes are outside this repository's allowed scope."
        in status_output
    )


def test_rec5_label_present(status_output: str) -> None:
    assert "YAML Schema" in status_output


def test_runtime_resumption_phrase_present(status_output: str) -> None:
    assert (
        "Runtime resumption / layer-by-layer unfreeze" in status_output
        or "runtime resumption" in status_output.lower()
    )


def test_unfreeze_layer_by_layer_phrase_present(status_output: str) -> None:
    assert "one layer at a time" in status_output


@pytest.mark.parametrize(
    "blocked_item",
    [
        "syllable registry",
        "syllable segmentation",
        "REC-6 runtime resumption until the maintainer explicitly lifts the freeze",
        "global REC freeze release",
    ],
)
def test_new_blocked_item_present(status_output: str, blocked_item: str) -> None:
    assert blocked_item in status_output, (
        f"new still-blocked item {blocked_item!r} missing"
    )


# --- Narrow Layer 4 authorization (2026-06-13 maintainer directive) -------


def test_section_4_5_narrowly_authorized_header_present(
    status_output: str,
) -> None:
    """The freeze tool surfaces a new §4.5 section for narrow per-layer
    authorizations granted ahead of REC unfreeze."""
    assert "## 4.5 Narrowly Authorized While Frozen" in status_output


@pytest.mark.parametrize(
    "authorized_phrase",
    [
        "Layer 4 LicensedSyllableCandidate runtime",
        "potential-only",
        "narrow authorization 2026-06-13",
        "not a global unfreeze",
        "BoundaryEvidence consumption by Layer 4",
        "read-only from qiyas_core.analysis_trace",
        "not promoted to a standalone runtime layer",
    ],
)
def test_narrowly_authorized_phrase_present(
    status_output: str, authorized_phrase: str
) -> None:
    assert authorized_phrase in status_output, (
        f"narrow-authorization phrase {authorized_phrase!r} missing"
    )


def test_narrow_authorization_does_not_lift_global_freeze(
    status_output: str,
) -> None:
    """The narrow Layer 4 authorization must not flip freeze_status away
    from ACTIVE. The global REC freeze stays active even after a narrow
    per-layer authorization."""
    assert "freeze_status=ACTIVE" in status_output
    # Narrow auth section must state its own non-lifting nature.
    assert "do not lift the global freeze" in status_output
    assert "do not authorize Layer 6 or higher" in status_output
    assert "do not authorize semantic runtime" in status_output


def test_layer5_recorded_as_narrow_authorization_only(status_output: str) -> None:
    """Layer 5 is recorded as a narrow per-layer authorization only — not a
    global unfreeze and not REC-6. The global freeze stays ACTIVE."""
    assert "Layer 5 LicensedSyllableSequenceCandidate runtime" in status_output
    assert "narrow authorization 2026-06-14" in status_output
    assert "not a global unfreeze, not REC-6" in status_output
    assert "freeze_status=ACTIVE" in status_output
    # Layer 6+ remains unauthorized.
    assert "do not authorize Layer 6 or higher" in status_output


def test_layer4_runtime_removed_from_still_blocked_section(
    status_output: str,
) -> None:
    """Section 4 (Still Blocked) must no longer list 'Layer 4 runtime',
    'LicensedSyllableCandidate runtime', or 'BoundaryEvidence runtime
    promotion' — these were moved to §4.5 Narrowly Authorized.

    The check is positional: the phrases may still appear in §4.5, but
    not in §4 (Still Blocked).
    """
    section_4_marker = "## 4. Still Blocked"
    section_4_5_marker = "## 4.5 Narrowly Authorized While Frozen"
    s4 = status_output.find(section_4_marker)
    s4_5 = status_output.find(section_4_5_marker)
    assert s4 >= 0 and s4_5 > s4
    section_4_body = status_output[s4:s4_5]
    for moved_phrase in (
        "Layer 4 runtime",
        "LicensedSyllableCandidate runtime",
        "BoundaryEvidence runtime promotion",
    ):
        # The §4 body must NOT list these as still-blocked bullet items.
        assert f"* {moved_phrase}" not in section_4_body, (
            f"{moved_phrase!r} must be removed from §4 Still Blocked "
            "after narrow Layer 4 authorization"
        )


def test_no_runtime_admission_phrase_present(status_output: str) -> None:
    assert "no runtime admission" in status_output


def test_pr_123_not_consumed_statement_present(status_output: str) -> None:
    assert (
        "PR #123, if present externally, is not consumed by this tool."
        in status_output
    )


# --- Determinism guard: tool performs no network/GitHub/file reads --------


def test_tool_source_does_not_import_network_or_io_libraries() -> None:
    """The freeze tool is hardcoded and deterministic by design. It must not
    import any network / GitHub / file-system library at module level, nor
    call open()/urllib/requests/subprocess on the gh CLI at runtime."""
    source = STATUS_SCRIPT.read_text(encoding="utf-8")
    forbidden_imports = (
        "import requests",
        "import urllib",
        "from urllib",
        "import http",
        "from http",
        "import socket",
        "import asyncio",
    )
    for forbidden in forbidden_imports:
        assert forbidden not in source, (
            f"forbidden network/IO import {forbidden!r} found in freeze tool source"
        )
    # The tool must not open files or call subprocess of gh.
    assert "open(" not in source, "freeze tool source contains open() call"
    assert 'subprocess.run(["gh"' not in source, (
        "freeze tool source contains a gh CLI subprocess call"
    )
    # The tool must not import gh or call any github_api function.
    assert "github_api" not in source.lower()
