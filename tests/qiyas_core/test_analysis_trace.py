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


# --- Boundary metadata tests ----------------------------------------------


SAMPLE_EXPECTED_OFFSETS = (
    ("بِ", 0, 2),
    ("ضَ", 3, 5),
    ("وَ", 6, 8),
    ("يَ", 9, 11),
    ("ضَرَبَ", 12, 18),
)


@pytest.mark.parametrize(
    "expected_index,expected_surface,expected_start,expected_end",
    [
        (i, surface, start, end)
        for i, (surface, start, end) in enumerate(SAMPLE_EXPECTED_OFFSETS)
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_boundary_start_end_indices_for_sample(
    trace: QiyasAnalysisTrace,
    expected_index: int,
    expected_surface: str,
    expected_start: int,
    expected_end: int,
) -> None:
    t = trace.tokens[expected_index]
    assert t.start_index == expected_start, (
        f"{expected_surface}: start_index expected {expected_start}, got {t.start_index}"
    )
    assert t.end_index == expected_end, (
        f"{expected_surface}: end_index expected {expected_end}, got {t.end_index}"
    )


def test_surface_equals_input_slice(trace: QiyasAnalysisTrace) -> None:
    for t in trace.tokens:
        assert t.surface_form_vocalized == trace.input_text[t.start_index:t.end_index], (
            f"token {t.token_index}: surface_form_vocalized {t.surface_form_vocalized!r} "
            f"does not match input_text[{t.start_index}:{t.end_index}]="
            f"{trace.input_text[t.start_index:t.end_index]!r}"
        )


def test_preceding_text_for_sample(trace: QiyasAnalysisTrace) -> None:
    expected = ["", " ", " ", " ", " "]
    for i, t in enumerate(trace.tokens):
        assert t.preceding_text == expected[i], (
            f"token {i}: preceding_text expected {expected[i]!r}, got {t.preceding_text!r}"
        )


def test_following_text_for_sample(trace: QiyasAnalysisTrace) -> None:
    expected = [" ", " ", " ", " ", ""]
    for i, t in enumerate(trace.tokens):
        assert t.following_text == expected[i], (
            f"token {i}: following_text expected {expected[i]!r}, got {t.following_text!r}"
        )


@pytest.mark.parametrize(
    "expected_index,expected_position",
    [
        (0, "initial"),
        (1, "medial"),
        (2, "medial"),
        (3, "medial"),
        (4, "final"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_token_position_for_sample(
    trace: QiyasAnalysisTrace, expected_index: int, expected_position: str
) -> None:
    assert trace.tokens[expected_index].token_position == expected_position


def test_all_tokens_have_leading_and_trailing_boundary_in_sample(
    trace: QiyasAnalysisTrace,
) -> None:
    # The whitespace-separated sample input gives every token at least one
    # boundary on each side (input-edge for first/last; whitespace for middle).
    for t in trace.tokens:
        assert t.has_leading_boundary is True
        assert t.has_trailing_boundary is True


def test_single_token_input_yields_position_single() -> None:
    single_trace = analyze_potential_trace("بِ")
    assert len(single_trace.tokens) == 1
    only = single_trace.tokens[0]
    assert only.token_position == "single"
    assert only.start_index == 0
    assert only.end_index == 2
    assert only.preceding_text == ""
    assert only.following_text == ""
    # Single token still has both boundaries (input edges).
    assert only.has_leading_boundary is True
    assert only.has_trailing_boundary is True


def test_repeated_token_surface_preserves_distinct_offsets() -> None:
    repeated_trace = analyze_potential_trace("بِ بِ بِ")
    assert len(repeated_trace.tokens) == 3
    # All three surfaces are identical but offsets must differ.
    surfaces = [t.surface_form_vocalized for t in repeated_trace.tokens]
    assert surfaces == ["بِ", "بِ", "بِ"]
    starts = [t.start_index for t in repeated_trace.tokens]
    assert starts == [0, 3, 6]
    ends = [t.end_index for t in repeated_trace.tokens]
    assert ends == [2, 5, 8]
    # Positions: initial, medial, final
    assert [t.token_position for t in repeated_trace.tokens] == [
        "initial",
        "medial",
        "final",
    ]


def test_multiple_spaces_preserved_in_preceding_following_text() -> None:
    # Two spaces between tokens; the boundary metadata must preserve them.
    spaced_trace = analyze_potential_trace("بِ  ضَ")
    assert len(spaced_trace.tokens) == 2
    first, second = spaced_trace.tokens
    assert second.preceding_text == "  "
    assert first.following_text == "  "


def test_leading_whitespace_in_input_recorded_in_first_preceding_text() -> None:
    leading_ws_trace = analyze_potential_trace("  بِ ضَ")
    assert len(leading_ws_trace.tokens) == 2
    first = leading_ws_trace.tokens[0]
    assert first.preceding_text == "  "
    assert first.start_index == 2
    assert first.has_leading_boundary is True


def test_trailing_whitespace_in_input_recorded_in_last_following_text() -> None:
    trailing_ws_trace = analyze_potential_trace("بِ ضَ  ")
    assert len(trailing_ws_trace.tokens) == 2
    last = trailing_ws_trace.tokens[-1]
    assert last.following_text == "  "
    assert last.has_trailing_boundary is True


def test_empty_input_yields_no_tokens() -> None:
    empty_trace = analyze_potential_trace("")
    assert empty_trace.input_text == ""
    assert empty_trace.tokens == ()


def test_whitespace_only_input_yields_no_tokens() -> None:
    ws_trace = analyze_potential_trace("   ")
    assert ws_trace.tokens == ()


def test_render_includes_boundary_lines_for_every_token(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    # Every token must have a corresponding boundary= line.
    boundary_lines = [
        line for line in rendered.splitlines() if line.strip().startswith("boundary=")
    ]
    assert len(boundary_lines) == len(trace.tokens)


@pytest.mark.parametrize(
    "expected_index,expected_surface,expected_start,expected_end,expected_position",
    [
        (0, "بِ", 0, 2, "initial"),
        (1, "ضَ", 3, 5, "medial"),
        (2, "وَ", 6, 8, "medial"),
        (3, "يَ", 9, 11, "medial"),
        (4, "ضَرَبَ", 12, 18, "final"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_render_boundary_line_format(
    trace: QiyasAnalysisTrace,
    expected_index: int,
    expected_surface: str,
    expected_start: int,
    expected_end: int,
    expected_position: str,
) -> None:
    rendered = render_analysis_trace(trace)
    expected_line = (
        f"  boundary=start:{expected_start} "
        f"end:{expected_end} "
        f"position={expected_position} "
        f"leading=True "
        f"trailing=True"
    )
    assert expected_line in rendered, (
        f"{expected_surface}: boundary line {expected_line!r} not found in rendered output"
    )


def test_cli_output_contains_boundary_lines(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    assert "boundary=" in cli_run.stdout
    boundary_lines = [
        line
        for line in cli_run.stdout.splitlines()
        if line.strip().startswith("boundary=")
    ]
    assert len(boundary_lines) == 5


@pytest.mark.parametrize(
    "surface,expected_without,expected_with",
    [
        ("بِ", "ACCEPTED", "ACCEPTED"),
        ("ضَ", "BLOCKED", "BLOCKED"),
        ("وَ", "DEFERRED", "ACCEPTED"),
        ("يَ", "DEFERRED", "BLOCKED"),
        ("ضَرَبَ", "BLOCKED", "BLOCKED"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_boundary_metadata_does_not_change_miu_statuses(
    trace_by_surface: dict[str, TokenAnalysisTrace],
    surface: str,
    expected_without: str,
    expected_with: str,
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert t.without_resolver_status == expected_without
    assert t.with_resolver_status == expected_with


def test_token_dataclass_has_all_boundary_fields() -> None:
    # Module-level sanity: the dataclass exposes all 7 new boundary fields.
    sample = analyze_potential_trace("بِ").tokens[0]
    assert hasattr(sample, "start_index")
    assert hasattr(sample, "end_index")
    assert hasattr(sample, "preceding_text")
    assert hasattr(sample, "following_text")
    assert hasattr(sample, "has_leading_boundary")
    assert hasattr(sample, "has_trailing_boundary")
    assert hasattr(sample, "token_position")


# --- Aggregate counts tests -----------------------------------------------


REPEATED_SAMPLE_INPUT = "بِ بِ وَ وَ"


@pytest.fixture(scope="module")
def repeated_trace() -> QiyasAnalysisTrace:
    return analyze_potential_trace(REPEATED_SAMPLE_INPUT)


@pytest.mark.parametrize(
    "field_name",
    [
        "total_token_count",
        "without_resolver_counts",
        "with_resolver_counts",
        "resolver_used_count",
        "unique_surface_count",
        "repeated_surface_count",
    ],
)
def test_aggregate_field_exists_on_trace(
    trace: QiyasAnalysisTrace, field_name: str
) -> None:
    assert hasattr(trace, field_name), f"aggregate field {field_name!r} missing"


def test_total_token_count_for_sample(trace: QiyasAnalysisTrace) -> None:
    assert trace.total_token_count == 5


def test_without_resolver_counts_for_sample(trace: QiyasAnalysisTrace) -> None:
    expected = {"ACCEPTED": 1, "BLOCKED": 2, "DEFERRED": 2}
    for bucket, count in expected.items():
        assert trace.without_resolver_counts.get(bucket) == count, (
            f"without_resolver_counts[{bucket!r}] expected {count}, "
            f"got {trace.without_resolver_counts.get(bucket)}"
        )


def test_with_resolver_counts_for_sample(trace: QiyasAnalysisTrace) -> None:
    expected = {"ACCEPTED": 2, "BLOCKED": 3, "DEFERRED": 0}
    for bucket, count in expected.items():
        assert trace.with_resolver_counts.get(bucket) == count, (
            f"with_resolver_counts[{bucket!r}] expected {count}, "
            f"got {trace.with_resolver_counts.get(bucket)}"
        )


def test_resolver_used_count_for_sample(trace: QiyasAnalysisTrace) -> None:
    assert trace.resolver_used_count == 2


def test_unique_surface_count_for_sample(trace: QiyasAnalysisTrace) -> None:
    assert trace.unique_surface_count == 5


def test_repeated_surface_count_for_sample(trace: QiyasAnalysisTrace) -> None:
    assert trace.repeated_surface_count == 0


def test_repeated_sample_total_token_count(repeated_trace: QiyasAnalysisTrace) -> None:
    assert repeated_trace.total_token_count == 4


def test_repeated_sample_unique_surface_count(
    repeated_trace: QiyasAnalysisTrace,
) -> None:
    assert repeated_trace.unique_surface_count == 2


def test_repeated_sample_repeated_surface_count(
    repeated_trace: QiyasAnalysisTrace,
) -> None:
    assert repeated_trace.repeated_surface_count == 2


def test_repeated_sample_sums_match_total(
    repeated_trace: QiyasAnalysisTrace,
) -> None:
    # unique + repeated == total
    assert (
        repeated_trace.unique_surface_count
        + repeated_trace.repeated_surface_count
        == repeated_trace.total_token_count
    )


def test_empty_input_aggregate_fields_are_zero_and_empty() -> None:
    empty_trace = analyze_potential_trace("")
    assert empty_trace.total_token_count == 0
    assert empty_trace.unique_surface_count == 0
    assert empty_trace.repeated_surface_count == 0
    assert empty_trace.resolver_used_count == 0
    # All canonical buckets present with 0 counts.
    assert empty_trace.without_resolver_counts == {
        "ACCEPTED": 0,
        "BLOCKED": 0,
        "DEFERRED": 0,
    }
    assert empty_trace.with_resolver_counts == {
        "ACCEPTED": 0,
        "BLOCKED": 0,
        "DEFERRED": 0,
    }


def test_render_includes_aggregate_summary_section(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "aggregate_summary:" in rendered


@pytest.mark.parametrize(
    "marker",
    [
        "total_token_count=5",
        "without_resolver_counts=ACCEPTED:1 BLOCKED:2 DEFERRED:2",
        "with_resolver_counts=ACCEPTED:2 BLOCKED:3 DEFERRED:0",
        "resolver_used_count=2",
        "unique_surface_count=5",
        "repeated_surface_count=0",
    ],
)
def test_render_aggregate_marker_present(
    trace: QiyasAnalysisTrace, marker: str
) -> None:
    rendered = render_analysis_trace(trace)
    assert marker in rendered, f"aggregate marker {marker!r} missing"


def test_cli_output_contains_aggregate_summary(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    assert "aggregate_summary:" in cli_run.stdout
    assert "total_token_count=5" in cli_run.stdout
    assert "without_resolver_counts=" in cli_run.stdout
    assert "with_resolver_counts=" in cli_run.stdout
    assert "resolver_used_count=2" in cli_run.stdout
    assert "unique_surface_count=5" in cli_run.stdout
    assert "repeated_surface_count=0" in cli_run.stdout


@pytest.mark.parametrize(
    "surface,expected_without,expected_with",
    [
        ("بِ", "ACCEPTED", "ACCEPTED"),
        ("ضَ", "BLOCKED", "BLOCKED"),
        ("وَ", "DEFERRED", "ACCEPTED"),
        ("يَ", "DEFERRED", "BLOCKED"),
        ("ضَرَبَ", "BLOCKED", "BLOCKED"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_aggregate_metadata_does_not_change_miu_statuses(
    trace_by_surface: dict[str, TokenAnalysisTrace],
    surface: str,
    expected_without: str,
    expected_with: str,
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert t.without_resolver_status == expected_without
    assert t.with_resolver_status == expected_with


def test_top_level_labels_still_present_after_aggregate_extension(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "mode=potential_only" in rendered
    assert "identity_carrier=surface_form_vocalized" in rendered
    assert "diagnostic_key=surface_form_unvocalized_key" in rendered


@pytest.mark.parametrize(
    "forbidden",
    [
        "final meaning",
        "hukm assigned",
        "dalalah assigned",
        "reality claim assigned",
        "i'rab assigned",
    ],
)
def test_aggregate_output_contains_no_semantic_claim(
    trace: QiyasAnalysisTrace, forbidden: str
) -> None:
    rendered = render_analysis_trace(trace).lower()
    assert forbidden.lower() not in rendered


def test_aggregate_extension_introduces_no_forbidden_higher_layer_names(
    trace: QiyasAnalysisTrace,
) -> None:
    """The aggregate section must not introduce any of the 8 forbidden
    higher-layer-artefact names — even though the PR #128 negation guard
    already covers them, this is a tight check against the rendered string."""
    rendered = render_analysis_trace(trace)
    forbidden_names = (
        "WordCandidate",
        "LafzCandidate",
        "DalalahCandidate",
        "FinalMeaning",
        "HukmCandidate",
        "RealityClaim",
        "AmilEffectEvidence",
        "I'rabEffectEvidence",
    )
    for name in forbidden_names:
        assert name not in rendered, (
            f"forbidden higher-layer-artefact name {name!r} appeared in rendered output"
        )


# --- Codepoint identity guard tests ----------------------------------------


@pytest.mark.parametrize(
    "field_name",
    [
        "surface_codepoints",
        "surface_codepoint_names",
        "surface_nfc_equal",
        "surface_slice_equal",
    ],
)
def test_every_token_has_codepoint_identity_field(
    trace: QiyasAnalysisTrace, field_name: str
) -> None:
    for t in trace.tokens:
        assert hasattr(t, field_name), f"token {t.token_index} missing {field_name!r}"


def test_bi_exact_codepoints(trace_by_surface: dict[str, TokenAnalysisTrace]) -> None:
    t = trace_by_surface[unicodedata.normalize("NFC", "بِ")]
    assert t.surface_codepoints == ("U+0628", "U+0650")


def test_bi_exact_codepoint_names(
    trace_by_surface: dict[str, TokenAnalysisTrace],
) -> None:
    t = trace_by_surface[unicodedata.normalize("NFC", "بِ")]
    assert t.surface_codepoint_names == ("ARABIC LETTER BEH", "ARABIC KASRA")


def test_da_exact_codepoints(trace_by_surface: dict[str, TokenAnalysisTrace]) -> None:
    t = trace_by_surface[unicodedata.normalize("NFC", "ضَ")]
    assert t.surface_codepoints == ("U+0636", "U+064E")


def test_da_exact_codepoint_names(
    trace_by_surface: dict[str, TokenAnalysisTrace],
) -> None:
    t = trace_by_surface[unicodedata.normalize("NFC", "ضَ")]
    assert t.surface_codepoint_names == ("ARABIC LETTER DAD", "ARABIC FATHA")


def test_every_sample_token_has_nfc_equal_true(trace: QiyasAnalysisTrace) -> None:
    for t in trace.tokens:
        assert t.surface_nfc_equal is True, (
            f"token {t.surface_form_vocalized!r} is not NFC-equal"
        )


def test_every_sample_token_has_slice_equal_true(trace: QiyasAnalysisTrace) -> None:
    for t in trace.tokens:
        assert t.surface_slice_equal is True, (
            f"token {t.surface_form_vocalized!r} surface_slice_equal=False"
        )


def test_every_token_surface_matches_input_slice(trace: QiyasAnalysisTrace) -> None:
    for t in trace.tokens:
        assert t.surface_form_vocalized == trace.input_text[t.start_index:t.end_index]


def test_codepoints_match_actual_surface_unicode(
    trace: QiyasAnalysisTrace,
) -> None:
    for t in trace.tokens:
        expected = tuple(f"U+{ord(ch):04X}" for ch in t.surface_form_vocalized)
        assert t.surface_codepoints == expected


def test_codepoint_names_match_actual_surface_unicode(
    trace: QiyasAnalysisTrace,
) -> None:
    for t in trace.tokens:
        expected = tuple(
            unicodedata.name(ch, "UNKNOWN") for ch in t.surface_form_vocalized
        )
        assert t.surface_codepoint_names == expected


def test_codepoint_count_matches_surface_length(
    trace: QiyasAnalysisTrace,
) -> None:
    for t in trace.tokens:
        assert len(t.surface_codepoints) == len(t.surface_form_vocalized)
        assert len(t.surface_codepoint_names) == len(t.surface_form_vocalized)


# --- regression: existing aggregate / boundary / MIU behavior unchanged ----


def test_codepoint_extension_preserves_aggregate_counts(
    trace: QiyasAnalysisTrace,
) -> None:
    assert trace.total_token_count == 5
    assert trace.without_resolver_counts.get("ACCEPTED") == 1
    assert trace.without_resolver_counts.get("BLOCKED") == 2
    assert trace.without_resolver_counts.get("DEFERRED") == 2
    assert trace.with_resolver_counts.get("ACCEPTED") == 2
    assert trace.with_resolver_counts.get("BLOCKED") == 3
    assert trace.with_resolver_counts.get("DEFERRED") == 0
    assert trace.resolver_used_count == 2
    assert trace.unique_surface_count == 5
    assert trace.repeated_surface_count == 0


@pytest.mark.parametrize(
    "expected_index,expected_surface,expected_start,expected_end,expected_position",
    [
        (0, "بِ", 0, 2, "initial"),
        (1, "ضَ", 3, 5, "medial"),
        (2, "وَ", 6, 8, "medial"),
        (3, "يَ", 9, 11, "medial"),
        (4, "ضَرَبَ", 12, 18, "final"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_codepoint_extension_preserves_boundary_metadata(
    trace: QiyasAnalysisTrace,
    expected_index: int,
    expected_surface: str,
    expected_start: int,
    expected_end: int,
    expected_position: str,
) -> None:
    t = trace.tokens[expected_index]
    assert t.start_index == expected_start
    assert t.end_index == expected_end
    assert t.token_position == expected_position


@pytest.mark.parametrize(
    "surface,expected_without,expected_with",
    [
        ("بِ", "ACCEPTED", "ACCEPTED"),
        ("ضَ", "BLOCKED", "BLOCKED"),
        ("وَ", "DEFERRED", "ACCEPTED"),
        ("يَ", "DEFERRED", "BLOCKED"),
        ("ضَرَبَ", "BLOCKED", "BLOCKED"),
    ],
    ids=["bi", "da", "wa", "ya", "daraba"],
)
def test_codepoint_extension_preserves_miu_statuses(
    trace_by_surface: dict[str, TokenAnalysisTrace],
    surface: str,
    expected_without: str,
    expected_with: str,
) -> None:
    nfc = unicodedata.normalize("NFC", surface)
    t = trace_by_surface[nfc]
    assert t.without_resolver_status == expected_without
    assert t.with_resolver_status == expected_with


# --- render / CLI tests ----------------------------------------------------


def test_render_includes_identity_codepoints_marker(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "identity_codepoints=" in rendered


def test_render_includes_identity_nfc_equal_true(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "identity_nfc_equal=True" in rendered


def test_render_includes_identity_slice_equal_true(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "identity_slice_equal=True" in rendered


def test_render_includes_identity_codepoint_names_marker(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "identity_codepoint_names=" in rendered


def test_cli_output_contains_bi_codepoints(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    assert "U+0628" in cli_run.stdout
    assert "U+0650" in cli_run.stdout


def test_cli_output_contains_da_codepoints(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    assert "U+0636" in cli_run.stdout
    assert "U+064E" in cli_run.stdout


def test_cli_output_contains_bi_codepoint_names(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    assert "ARABIC LETTER BEH" in cli_run.stdout
    assert "ARABIC KASRA" in cli_run.stdout


def test_cli_output_contains_da_codepoint_names(
    cli_run: subprocess.CompletedProcess[str],
) -> None:
    assert "ARABIC LETTER DAD" in cli_run.stdout
    assert "ARABIC FATHA" in cli_run.stdout


def test_top_level_labels_still_present_after_codepoint_extension(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    assert "mode=potential_only" in rendered
    assert "identity_carrier=surface_form_vocalized" in rendered
    assert "diagnostic_key=surface_form_unvocalized_key" in rendered


@pytest.mark.parametrize(
    "forbidden",
    [
        "final meaning",
        "hukm assigned",
        "dalalah assigned",
        "reality claim assigned",
        "i'rab assigned",
    ],
)
def test_codepoint_output_contains_no_semantic_claim(
    trace: QiyasAnalysisTrace, forbidden: str
) -> None:
    rendered = render_analysis_trace(trace).lower()
    assert forbidden.lower() not in rendered


def test_codepoint_extension_introduces_no_forbidden_higher_layer_names(
    trace: QiyasAnalysisTrace,
) -> None:
    rendered = render_analysis_trace(trace)
    forbidden_names = (
        "WordCandidate",
        "LafzCandidate",
        "DalalahCandidate",
        "FinalMeaning",
        "HukmCandidate",
        "RealityClaim",
        "AmilEffectEvidence",
        "I'rabEffectEvidence",
    )
    for name in forbidden_names:
        assert name not in rendered, (
            f"forbidden higher-layer-artefact name {name!r} appeared in rendered output"
        )
