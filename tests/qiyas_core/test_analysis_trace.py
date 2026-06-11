"""Tests for the potential-only MIU analysis trace at src/qiyas_core/analysis_trace.py."""

from __future__ import annotations

import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

from qiyas_core.analysis_trace import (
    DIAGNOSTIC_KEY_LABEL,
    IDENTITY_CARRIER_LABEL,
    MODE_LABEL,
    QiyasAnalysisTrace,
    RUNTIME_STATUS_LABEL,
    TokenAnalysisTrace,
    analyze_potential_trace,
    render_analysis_trace,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_INPUT = "بِ ضَ وَ يَ ضَرَبَ"
SAMPLE_TOKENS = ("بِ", "ضَ", "وَ", "يَ", "ضَرَبَ")


@pytest.fixture(scope="module")
def trace() -> QiyasAnalysisTrace:
    return analyze_potential_trace(SAMPLE_INPUT)


@pytest.fixture(scope="module")
def trace_by_surface(trace: QiyasAnalysisTrace) -> dict[str, TokenAnalysisTrace]:
    return {t.surface_form_vocalized: t for t in trace.tokens}


def test_returns_structured_trace(trace: QiyasAnalysisTrace) -> None:
    assert isinstance(trace, QiyasAnalysisTrace)


def test_input_text_preserved(trace: QiyasAnalysisTrace) -> None:
    assert trace.input_text == SAMPLE_INPUT


def test_token_count_is_5(trace: QiyasAnalysisTrace) -> None:
    assert len(trace.tokens) == 5


def test_top_level_labels(trace: QiyasAnalysisTrace) -> None:
    assert trace.mode == MODE_LABEL == "potential_only"
    assert trace.identity_carrier == IDENTITY_CARRIER_LABEL == "surface_form_vocalized"
    assert trace.diagnostic_key == DIAGNOSTIC_KEY_LABEL == "surface_form_unvocalized_key"
    assert trace.runtime_status == RUNTIME_STATUS_LABEL == "not_semantic_runtime"


@pytest.mark.parametrize(
    "expected_index,expected_surface",
    list(enumerate(SAMPLE_TOKENS)),
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_token_order_and_surface_preserved(
    trace: QiyasAnalysisTrace, expected_index: int, expected_surface: str
) -> None:
    t = trace.tokens[expected_index]
    assert t.token_index == expected_index
    assert t.surface_form_vocalized == unicodedata.normalize("NFC", expected_surface)


def test_each_token_is_TokenAnalysisTrace(trace: QiyasAnalysisTrace) -> None:
    for t in trace.tokens:
        assert isinstance(t, TokenAnalysisTrace)


def test_harakat_preserved_in_tokens(trace: QiyasAnalysisTrace) -> None:
    # Identity must include harakat — surface_form_vocalized differs from the
    # diagnostic key for every token that carries a haraka.
    for t in trace.tokens:
        if t.surface_form_vocalized == t.surface_form_unvocalized_key:
            # tokens without any haraka are allowed to coincide (no test input
            # like that in the sample)
            continue
        assert any(0x064B <= ord(ch) < 0x0653 for ch in t.surface_form_vocalized), (
            f"token {t.surface_form_vocalized!r} carries no haraka but differs "
            f"from its unvocalized key — should not happen"
        )


@pytest.mark.parametrize(
    "surface,without_expected,with_expected",
    [
        ("بِ", "ACCEPTED", "ACCEPTED"),
        ("ضَ", "BLOCKED", "BLOCKED"),
        ("وَ", "DEFERRED", "ACCEPTED"),
        ("يَ", "DEFERRED", "BLOCKED"),
        ("ضَرَبَ", "BLOCKED", "BLOCKED"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_expected_status_pair(
    trace_by_surface: dict[str, TokenAnalysisTrace],
    surface: str,
    without_expected: str,
    with_expected: str,
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert t.without_resolver_status == without_expected, (
        f"{surface}: without_resolver expected {without_expected}, "
        f"got {t.without_resolver_status}"
    )
    assert t.with_resolver_status == with_expected, (
        f"{surface}: with_resolver expected {with_expected}, "
        f"got {t.with_resolver_status}"
    )


@pytest.mark.parametrize(
    "surface,resolver_used_expected",
    [
        ("بِ", False),
        ("ضَ", False),
        ("وَ", True),
        ("يَ", True),
        ("ضَرَبَ", False),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_resolver_used_only_for_multivariant_single_letter_tokens(
    trace_by_surface: dict[str, TokenAnalysisTrace],
    surface: str,
    resolver_used_expected: bool,
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert t.resolver_used is resolver_used_expected


@pytest.mark.parametrize(
    "surface",
    ["ضَ", "يَ", "ضَرَبَ"],
    ids=["da", "ya", "daraba"],
)
def test_residuals_present_for_blocked_or_blocked_after_resolver(
    trace_by_surface: dict[str, TokenAnalysisTrace], surface: str
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert len(t.residuals) >= 1, (
        f"{surface}: expected at least one residual on a BLOCKED outcome; got {t.residuals!r}"
    )


@pytest.mark.parametrize(
    "surface",
    ["بِ", "وَ"],
    ids=["bi", "wa"],
)
def test_no_residuals_on_accepted_paths(
    trace_by_surface: dict[str, TokenAnalysisTrace], surface: str
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert t.with_resolver_status == "ACCEPTED"
    # The accepted path must not carry blocking residuals.
    assert "blocking_fariq_present" not in t.residuals
    assert "deferred_variant_ambiguity" not in t.residuals


def test_pair_count_matches_arabic_letter_count(
    trace_by_surface: dict[str, TokenAnalysisTrace],
) -> None:
    assert trace_by_surface[unicodedata.normalize("NFC", "بِ")].pair_count == 1
    assert trace_by_surface[unicodedata.normalize("NFC", "ضَ")].pair_count == 1
    assert trace_by_surface[unicodedata.normalize("NFC", "وَ")].pair_count == 1
    assert trace_by_surface[unicodedata.normalize("NFC", "يَ")].pair_count == 1
    assert trace_by_surface[unicodedata.normalize("NFC", "ضَرَبَ")].pair_count >= 2


def test_unvocalized_key_strips_harakat(
    trace_by_surface: dict[str, TokenAnalysisTrace],
) -> None:
    bi = trace_by_surface[unicodedata.normalize("NFC", "بِ")]
    assert bi.surface_form_unvocalized_key == "ب"
    da = trace_by_surface[unicodedata.normalize("NFC", "ضَ")]
    assert da.surface_form_unvocalized_key == "ض"


def test_render_includes_top_level_labels(trace: QiyasAnalysisTrace) -> None:
    rendered = render_analysis_trace(trace)
    assert "Saleh/Qiyas Potential Analysis Trace" in rendered
    assert "mode=potential_only" in rendered
    assert "identity_carrier=surface_form_vocalized" in rendered
    assert "diagnostic_key=surface_form_unvocalized_key" in rendered
    assert "runtime_status=not_semantic_runtime" in rendered


def test_render_includes_every_token(trace: QiyasAnalysisTrace) -> None:
    rendered = render_analysis_trace(trace)
    for surface in SAMPLE_TOKENS:
        nfc = unicodedata.normalize("NFC", surface)
        assert f"token {nfc}" in rendered


def test_render_includes_input_text(trace: QiyasAnalysisTrace) -> None:
    rendered = render_analysis_trace(trace)
    assert f"input={SAMPLE_INPUT}" in rendered


def test_render_end_marker_present(trace: QiyasAnalysisTrace) -> None:
    rendered = render_analysis_trace(trace)
    assert "End of Saleh/Qiyas Potential Analysis Trace." in rendered


@pytest.mark.parametrize(
    "forbidden_phrase",
    [
        # positive runtime / semantic admission language
        "runtime_status=runtime",
        "runtime_status=enabled",
        "runtime_admitted",
        "admitted to runtime",
        "is_runtime: true",
        "is_runtime=true",
        # semantic / final-judgment language
        "final meaning",
        "final judgment",
        "hukm assigned",
        "dalalah assigned",
        "reality claim assigned",
        "i'rab assigned",
    ],
)
def test_render_contains_no_positive_runtime_or_semantic_language(
    trace: QiyasAnalysisTrace, forbidden_phrase: str
) -> None:
    rendered = render_analysis_trace(trace).lower()
    assert forbidden_phrase.lower() not in rendered


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


@pytest.mark.parametrize("name", FORBIDDEN_HIGHER_LAYER_NAMES)
def test_render_does_not_contain_higher_layer_artefact_names(
    trace: QiyasAnalysisTrace, name: str
) -> None:
    rendered = render_analysis_trace(trace)
    assert name not in rendered


# --- CLI tests -------------------------------------------------------------


@pytest.fixture(scope="module")
def cli_run() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "qiyas_core.analysis_trace", SAMPLE_INPUT],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": f"{REPO_ROOT / 'src'}:{REPO_ROOT}"},
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_exits_zero(cli_run: subprocess.CompletedProcess[str]) -> None:
    assert cli_run.returncode == 0, (
        f"CLI exited with code {cli_run.returncode}\n"
        f"stdout:\n{cli_run.stdout}\nstderr:\n{cli_run.stderr}"
    )


def test_cli_output_contains_required_markers(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    output = cli_run.stdout
    for marker in (
        "Saleh/Qiyas Potential Analysis Trace",
        f"input={SAMPLE_INPUT}",
        "mode=potential_only",
        "identity_carrier=surface_form_vocalized",
        "diagnostic_key=surface_form_unvocalized_key",
        "runtime_status=not_semantic_runtime",
    ):
        assert marker in output, f"CLI output missing marker {marker!r}"


@pytest.mark.parametrize(
    "surface,without_expected,with_expected",
    [
        ("بِ", "ACCEPTED", "ACCEPTED"),
        ("ضَ", "BLOCKED", "BLOCKED"),
        ("وَ", "DEFERRED", "ACCEPTED"),
        ("يَ", "DEFERRED", "BLOCKED"),
        ("ضَرَبَ", "BLOCKED", "BLOCKED"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_cli_output_token_lines(
    cli_run: subprocess.CompletedProcess[str],
    surface: str,
    without_expected: str,
    with_expected: str,
) -> None:
    output = cli_run.stdout
    nfc = unicodedata.normalize("NFC", surface)
    assert f"token {nfc}" in output
    assert f"without_resolver={without_expected}" in output
    assert f"with_resolver={with_expected}" in output


def test_cli_with_no_args_returns_nonzero_and_usage(
    tmp_path: Path,
) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "qiyas_core.analysis_trace"],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": f"{REPO_ROOT / 'src'}:{REPO_ROOT}"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "usage:" in result.stderr.lower()
