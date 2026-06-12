"""Tests for the Layer 4 LicensedSyllableCandidate readiness audit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
READINESS_SCRIPT = REPO_ROOT / "tools" / "qiyas_licensed_syllable_readiness.py"


@pytest.fixture(scope="module")
def readiness_output() -> str:
    result = subprocess.run(
        [sys.executable, str(READINESS_SCRIPT)],
        cwd=str(REPO_ROOT),
        env={"PYTHONPATH": f"{REPO_ROOT / 'src'}:{REPO_ROOT}"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"readiness audit exited with code {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return result.stdout


def test_script_exists() -> None:
    assert READINESS_SCRIPT.is_file(), f"readiness script missing at {READINESS_SCRIPT}"


def test_title_present(readiness_output: str) -> None:
    assert "Licensed Syllable Readiness" in readiness_output


@pytest.mark.parametrize(
    "marker",
    [
        "layer=Layer 4",
        "target=LicensedSyllableCandidate",
        "status=readiness_only",
        "runtime_status=not_implemented",
        "freeze_sensitive=true",
    ],
)
def test_section_1_state_markers_present(readiness_output: str, marker: str) -> None:
    assert marker in readiness_output, f"section 1 marker {marker!r} missing"


def test_section_2_lower_layer_evidence_header(readiness_output: str) -> None:
    assert "## 2. Lower-Layer Evidence Available" in readiness_output


def test_section_2_potential_only_phrase_present(readiness_output: str) -> None:
    assert "potential-only MIU analysis trace" in readiness_output


def test_section_2_identity_carrier_marker(readiness_output: str) -> None:
    assert "identity_carrier=surface_form_vocalized" in readiness_output


def test_section_2_diagnostic_key_marker(readiness_output: str) -> None:
    assert "diagnostic_key=surface_form_unvocalized_key" in readiness_output


def test_section_2_sample_input_present(readiness_output: str) -> None:
    assert "بِ ضَ وَ يَ ضَرَبَ" in readiness_output


def test_section_2_input_preserved(readiness_output: str) -> None:
    assert "input preserved: True" in readiness_output


def test_section_2_token_count(readiness_output: str) -> None:
    assert "token_count=5" in readiness_output


def test_section_2_status_buckets_listed(readiness_output: str) -> None:
    for bucket in ("ACCEPTED", "DEFERRED", "BLOCKED"):
        assert bucket in readiness_output, f"bucket label {bucket!r} missing"


def test_section_2_resolver_trace_phrase(readiness_output: str) -> None:
    assert "resolver effects visible as trace, not final judgment" in readiness_output


def test_section_3_missing_evidence_header(readiness_output: str) -> None:
    assert "## 3. Required Missing Evidence Before Runtime" in readiness_output


@pytest.mark.parametrize(
    "missing",
    [
        "explicit boundary evidence model",
        "licensed syllable candidate data model",
        "phonetic economy proof rule",
        "allowed syllable-shape contract in code",
        "invalidation rule for unsupported shapes",
        "tests for CV, CVC, CVV, CVVC, CVVCC only",
        "proof that no meaning/hukm/i'rab/reality is introduced",
        "maintainer unfreeze / explicit authorization if freeze remains active",
    ],
)
def test_section_3_missing_gates_listed(
    readiness_output: str, missing: str
) -> None:
    assert missing in readiness_output, f"missing-gate item {missing!r} missing"


def test_section_4_allowed_syllable_shapes_header(readiness_output: str) -> None:
    assert "## 4. Allowed Syllable Shapes" in readiness_output


@pytest.mark.parametrize("shape", ["CV", "CVC", "CVV", "CVVC", "CVVCC"])
def test_section_4_syllable_shape_label_present(
    readiness_output: str, shape: str
) -> None:
    # Each shape must appear as a bullet item (look for "* SHAPE" or the
    # in-line list "CV, CVC, ...").
    assert (f"* {shape}" in readiness_output) or (shape in readiness_output), (
        f"syllable-shape label {shape!r} missing"
    )


def test_section_4_says_no_runtime_syllable_segmentation(
    readiness_output: str,
) -> None:
    assert "No runtime syllable segmentation is performed." in readiness_output


def test_section_4_says_no_word_classified(readiness_output: str) -> None:
    assert "No Arabic word is classified as a syllable in this PR." in readiness_output


def test_section_4_says_readiness_labels_only(readiness_output: str) -> None:
    assert "These are readiness labels only." in readiness_output


def test_section_5_constitutional_boundary_header(readiness_output: str) -> None:
    assert "## 5. Constitutional Boundary" in readiness_output


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
        "introduce LicensedSyllableCandidate implementation in this PR",
    ],
)
def test_section_5_boundary_markers_present(
    readiness_output: str, marker: str
) -> None:
    assert marker in readiness_output, (
        f"constitutional-boundary marker {marker!r} missing"
    )


def test_end_marker_present(readiness_output: str) -> None:
    assert "End of Licensed Syllable Readiness audit." in readiness_output


@pytest.mark.parametrize(
    "forbidden_phrase",
    [
        # positive runtime-admission language
        "runtime_status=runtime",
        "runtime_status=enabled",
        "runtime_admitted",
        "admitted to runtime",
        "is_runtime: true",
        "is_runtime=true",
        "runtime: enabled",
        # positive layer-4 admission language
        "status=implemented",
        "runtime_status=implemented",
        "LicensedSyllableCandidate admitted",
        "LicensedSyllableCandidate is implemented",
        # positive semantic / final-judgment language
        "final meaning",
        "hukm assigned",
        "dalalah assigned",
        "reality claim assigned",
        "i'rab assigned",
    ],
)
def test_no_positive_runtime_or_semantic_language(
    readiness_output: str, forbidden_phrase: str
) -> None:
    assert forbidden_phrase.lower() not in readiness_output.lower(), (
        f"forbidden positive phrase {forbidden_phrase!r} appeared in readiness output"
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
    readiness_output: str,
) -> None:
    """Higher-layer-artefact names may appear only after the explicit negation
    header in § 5. Positive occurrences are forbidden."""
    negation_index = readiness_output.find(NEGATION_SECTION_HEADER)
    for name in FORBIDDEN_HIGHER_LAYER_NAMES:
        first_index = readiness_output.find(name)
        if first_index < 0:
            continue
        assert negation_index >= 0 and first_index > negation_index, (
            f"forbidden higher-layer-artefact name {name!r} appears outside the "
            f"explicit negation section. Each occurrence must follow the "
            f"{NEGATION_SECTION_HEADER!r} header."
        )


def test_licensed_syllable_candidate_only_in_target_or_negation(
    readiness_output: str,
) -> None:
    """The string ``LicensedSyllableCandidate`` is allowed in two specific
    contexts: as the readiness target marker (``target=LicensedSyllableCandidate``)
    and inside the negation section (``introduce LicensedSyllableCandidate
    implementation in this PR``). Anywhere else would be a positive admission
    claim and is forbidden."""
    output = readiness_output
    target_marker = "target=LicensedSyllableCandidate"
    negation_marker = "introduce LicensedSyllableCandidate implementation in this PR"
    assert target_marker in output
    assert negation_marker in output
    # Replace the allowed contexts and confirm no other occurrence remains.
    stripped = output.replace(target_marker, "").replace(negation_marker, "")
    assert "LicensedSyllableCandidate" not in stripped, (
        "LicensedSyllableCandidate appeared outside the allowed contexts "
        "(target marker and negation section)"
    )
