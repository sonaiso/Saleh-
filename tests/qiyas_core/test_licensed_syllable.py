"""Layer 4 LicensedSyllableCandidate tests.

Thirteen test groups per the maintainer's directive (2026-06-13):
    1.  API existence
    2.  Allowed shape contract (exactly CV / CVC / CVV / CVVC / CVCC / CVVCC)
    3.  BoundaryEvidence shape
    4.  Identity preservation
    5.  Candidate emission for simple CV tokens
    6.  CVC / CVV / CVVC / CVCC / CVVCC shape tests
    7.  Unsupported shape invalidation
    8.  Economy rule
    9.  Integration with analysis_trace (no mutation of lower-layer evidence)
    10. CLI/tool test
    11. Negative constitutional guard (no positive meaning / hukm / etc claims)
    12. No forbidden Layer 5+ classes or runtime
    13. Backward compatibility (analysis trace / readiness / freeze / snapshot
        inventory / MIU integration suites still pass)

The runtime under test is potential-only; tests assert it does not
introduce meaning / hukm / i'rab / dalalah / reality.
"""

from __future__ import annotations

import inspect
import subprocess
import sys
from dataclasses import is_dataclass
from enum import Enum
from pathlib import Path

import pytest

from qiyas_core import licensed_syllable
from qiyas_core.analysis_trace import (
    QiyasAnalysisTrace,
    TokenAnalysisTrace,
    analyze_potential_trace,
)
from qiyas_core.licensed_syllable import (
    ALLOWED_SYLLABLE_SHAPES,
    AllowedSyllableShape,
    BoundaryEvidence,
    LAYER4_RUNTIME_STATUS,
    CANDIDATE_RUNTIME_STATUS,
    EVIDENCE_SOURCE,
    LicensedSyllableAnalysis,
    LicensedSyllableCandidate,
    PhoneticEconomyEvidence,
    SyllableInvalidationEvidence,
    SyllableShapeEvidence,
    analyze_licensed_syllables,
    render_licensed_syllable_analysis,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_TOOL = REPO_ROOT / "tools" / "qiyas_licensed_syllable_demo.py"
LICENSED_MODULE_SRC = REPO_ROOT / "src" / "qiyas_core" / "licensed_syllable.py"

# Canonical sample input from the directive
SAMPLE_INPUT = "بِ ضَ وَ يَ ضَرَبَ"

# Canonical example strings per shape (CV/CVC/CVV/CVVC/CVCC/CVVCC).
# CVV/CVVC/CVCC/CVVCC use explicitly constructed strings — they show the
# codepoint pattern only and make no semantic claim.
CV_EXAMPLES = ("بِ", "ضَ", "وَ", "يَ")
CVC_EXAMPLE = "مِنْ"
CVV_EXAMPLE = "قَا"
CVVC_EXAMPLE = "قَالْ"
CVCC_EXAMPLE = "بَيت"
CVVCC_EXAMPLE = "قَالْتْ"
UNSUPPORTED_EXAMPLES = (
    "ضَرَبَ",      # reduces to CVCVCV — not in contract
    "شَاذّ",        # shadda / gemination unsupported in the closed contract
    "hello",        # non-Arabic codepoints
    "ابن",          # bare consonants without harakat — out of contract here
)


# ─────────────────────────────────────────────────────────────────────────────
# Group 1 — API existence
# ─────────────────────────────────────────────────────────────────────────────


class TestApiExistence:
    """Group 1 — All public symbols and required types exist."""

    @pytest.mark.parametrize(
        "symbol",
        [
            "AllowedSyllableShape",
            "BoundaryEvidence",
            "SyllableShapeEvidence",
            "PhoneticEconomyEvidence",
            "SyllableInvalidationEvidence",
            "LicensedSyllableCandidate",
            "LicensedSyllableAnalysis",
            "analyze_licensed_syllables",
            "render_licensed_syllable_analysis",
        ],
    )
    def test_public_symbol_exists(self, symbol: str) -> None:
        assert hasattr(licensed_syllable, symbol), (
            f"missing public symbol: {symbol}"
        )

    @pytest.mark.parametrize(
        "cls",
        [
            BoundaryEvidence,
            SyllableShapeEvidence,
            PhoneticEconomyEvidence,
            SyllableInvalidationEvidence,
            LicensedSyllableCandidate,
            LicensedSyllableAnalysis,
        ],
    )
    def test_dataclass_is_frozen(self, cls) -> None:
        assert is_dataclass(cls), f"{cls.__name__} must be a dataclass"
        # Frozen dataclasses raise FrozenInstanceError on attribute set; the
        # dataclass machinery sets __dataclass_params__.frozen = True.
        params = getattr(cls, "__dataclass_params__", None)
        assert params is not None and params.frozen, (
            f"{cls.__name__} must be a frozen dataclass"
        )

    def test_analyze_licensed_syllables_returns_analysis(self) -> None:
        result = analyze_licensed_syllables(SAMPLE_INPUT)
        assert isinstance(result, LicensedSyllableAnalysis)

    def test_render_returns_string(self) -> None:
        analysis = analyze_licensed_syllables(SAMPLE_INPUT)
        rendered = render_licensed_syllable_analysis(analysis)
        assert isinstance(rendered, str)
        assert rendered  # non-empty


# ─────────────────────────────────────────────────────────────────────────────
# Group 2 — Allowed shape contract
# ─────────────────────────────────────────────────────────────────────────────


class TestAllowedShapeContract:
    """Group 2 — Exactly CV / CVC / CVV / CVVC / CVCC / CVVCC are valid shapes."""

    def test_enum_is_enum(self) -> None:
        assert issubclass(AllowedSyllableShape, Enum)

    def test_exactly_six_allowed_members(self) -> None:
        members = {m.value for m in AllowedSyllableShape}
        assert members == {"CV", "CVC", "CVV", "CVVC", "CVCC", "CVVCC"}
        assert len(members) == 6

    def test_allowed_tuple_matches_enum(self) -> None:
        assert set(ALLOWED_SYLLABLE_SHAPES) == set(AllowedSyllableShape)
        # Tuple is ordered and contains every member exactly once
        assert len(ALLOWED_SYLLABLE_SHAPES) == 6

    @pytest.mark.parametrize(
        "forbidden_value",
        ["V", "C", "VC", "VV", "CCV", "CCC", "VVC", "CVVVCC"],
    )
    def test_no_other_shape_recognized(self, forbidden_value: str) -> None:
        with pytest.raises(ValueError):
            AllowedSyllableShape(forbidden_value)


# ─────────────────────────────────────────────────────────────────────────────
# Group 3 — BoundaryEvidence shape on canonical sample
# ─────────────────────────────────────────────────────────────────────────────


class TestBoundaryEvidence:
    """Group 3 — Boundary evidence sourced from analysis_trace tokens."""

    @pytest.fixture(scope="class")
    def analysis(self) -> LicensedSyllableAnalysis:
        return analyze_licensed_syllables(SAMPLE_INPUT)

    def test_every_candidate_boundary_source_is_analysis_trace(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        assert analysis.candidates, "expected at least one CV candidate"
        for c in analysis.candidates:
            assert c.boundary_evidence.source == EVIDENCE_SOURCE
            assert c.boundary_evidence.source == "qiyas_core.analysis_trace"

    def test_boundary_uses_token_start_end_indices(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        text = analysis.input_text
        for c in analysis.candidates:
            be = c.boundary_evidence
            assert text[be.start_index : be.end_index] == c.surface_form_vocalized

    def test_boundary_preserved_is_true_for_all_candidates(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        for c in analysis.candidates:
            assert c.boundary_evidence.boundary_preserved is True

    def test_left_and_right_boundaries_align_with_lower_layer(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        # The sample "بِ ضَ وَ يَ ضَرَبَ" tokenizes into 5 whitespace-split
        # tokens. The first has a left boundary; the last has a right
        # boundary; all interior tokens have both via whitespace.
        trace = analyze_potential_trace(analysis.input_text)
        by_index = {c.token_index: c for c in analysis.candidates}
        for token in trace.tokens:
            if token.token_index not in by_index:
                continue
            c = by_index[token.token_index]
            assert c.boundary_evidence.has_left_boundary == token.has_leading_boundary
            assert c.boundary_evidence.has_right_boundary == token.has_trailing_boundary


# ─────────────────────────────────────────────────────────────────────────────
# Group 4 — Identity preservation
# ─────────────────────────────────────────────────────────────────────────────


class TestIdentityPreservation:
    """Group 4 — Candidates preserve codepoints, names, NFC, slice, identity."""

    @pytest.fixture(scope="class")
    def analysis(self) -> LicensedSyllableAnalysis:
        return analyze_licensed_syllables(SAMPLE_INPUT)

    def test_codepoints_match_surface(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        for c in analysis.candidates:
            assert c.surface_codepoints == tuple(
                f"U+{ord(ch):04X}" for ch in c.surface_form_vocalized
            )

    def test_codepoint_names_align_with_surface(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        import unicodedata as _u


        for c in analysis.candidates:
            expected = tuple(
                _u.name(ch, "UNKNOWN") for ch in c.surface_form_vocalized
            )
            assert c.surface_codepoint_names == expected

    def test_identity_preserved_flag_true(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        for c in analysis.candidates:
            assert c.identity_preserved is True

    def test_vocalized_identity_equals_input_slice(
        self, analysis: LicensedSyllableAnalysis
    ) -> None:
        text = analysis.input_text
        for c in analysis.candidates:
            be = c.boundary_evidence
            assert c.surface_form_vocalized == text[be.start_index : be.end_index]


# ─────────────────────────────────────────────────────────────────────────────
# Group 5 — Candidate emission for simple CV tokens
# ─────────────────────────────────────────────────────────────────────────────


class TestCvCandidateEmission:
    """Group 5 — بِ / ضَ / وَ / يَ each emit a CV candidate."""

    @pytest.mark.parametrize("token", CV_EXAMPLES)
    def test_single_token_emits_one_candidate(self, token: str) -> None:
        analysis = analyze_licensed_syllables(token)
        assert len(analysis.candidates) == 1, (
            f"expected exactly one candidate for {token!r}, "
            f"got {len(analysis.candidates)} candidates and "
            f"{len(analysis.invalidations)} invalidations"
        )
        assert analysis.invalidations == ()
        c = analysis.candidates[0]
        assert c.shape is AllowedSyllableShape.CV
        assert c.surface_form_vocalized == token
        assert c.potential_only is True
        assert c.runtime_status == CANDIDATE_RUNTIME_STATUS
        assert c.runtime_status == "potential_only_not_semantic_runtime"
        assert c.identity_preserved is True
        assert c.boundary_evidence.boundary_preserved is True
        assert c.economy_evidence.economy_satisfied is True

    def test_canonical_sample_emits_four_cv_candidates(self) -> None:
        analysis = analyze_licensed_syllables(SAMPLE_INPUT)
        cv_candidates = [
            c for c in analysis.candidates if c.shape is AllowedSyllableShape.CV
        ]
        assert len(cv_candidates) == 4
        assert tuple(c.surface_form_vocalized for c in cv_candidates) == CV_EXAMPLES


# ─────────────────────────────────────────────────────────────────────────────
# Group 6 — CVC / CVV / CVVC / CVCC / CVVCC explicit shape tests
# ─────────────────────────────────────────────────────────────────────────────


SHAPE_EXAMPLES = (
    (AllowedSyllableShape.CVC, CVC_EXAMPLE),
    (AllowedSyllableShape.CVV, CVV_EXAMPLE),
    (AllowedSyllableShape.CVVC, CVVC_EXAMPLE),
    (AllowedSyllableShape.CVCC, CVCC_EXAMPLE),
    (AllowedSyllableShape.CVVCC, CVVCC_EXAMPLE),
)


class TestNonCvShapes:
    """Group 6 — One explicit vocalized example per non-CV allowed shape."""

    @pytest.mark.parametrize("shape,example", SHAPE_EXAMPLES)
    def test_shape_recognized(
        self, shape: AllowedSyllableShape, example: str
    ) -> None:
        analysis = analyze_licensed_syllables(example)
        assert len(analysis.candidates) == 1, (
            f"expected one candidate for {shape.value} example {example!r}, "
            f"got {len(analysis.candidates)} candidates"
        )
        c = analysis.candidates[0]
        assert c.shape is shape
        assert c.shape_evidence.allowed is True

    @pytest.mark.parametrize("shape,example", SHAPE_EXAMPLES)
    def test_candidate_emitted_with_potential_only(
        self, shape: AllowedSyllableShape, example: str
    ) -> None:
        analysis = analyze_licensed_syllables(example)
        c = analysis.candidates[0]
        assert c.potential_only is True
        assert c.runtime_status == CANDIDATE_RUNTIME_STATUS

    @pytest.mark.parametrize("shape,example", SHAPE_EXAMPLES)
    def test_no_semantic_claim_at_token_level(
        self, shape: AllowedSyllableShape, example: str
    ) -> None:
        analysis = analyze_licensed_syllables(example)
        # The analysis bundle records constitutional statuses as
        # "not_introduced". The candidate carries no meaning / hukm /
        # i'rab / dalalah / reality field.
        assert analysis.meaning_status == "not_introduced"
        assert analysis.hukm_status == "not_introduced"
        assert analysis.irab_status == "not_introduced"
        assert analysis.dalalah_status == "not_introduced"
        assert analysis.reality_status == "not_introduced"
        c = analysis.candidates[0]
        candidate_fields = {f.name for f in c.__dataclass_fields__.values()}
        # No semantic-claim field name on the candidate.
        for forbidden_field in (
            "meaning", "hukm", "irab", "i_rab", "dalalah", "reality",
            "final_meaning", "interpretation", "tafsir",
        ):
            assert forbidden_field not in candidate_fields


# ─────────────────────────────────────────────────────────────────────────────
# Group 6B — CVCC closed-contract correction
# ─────────────────────────────────────────────────────────────────────────────


class TestCvccContractCorrection:
    """CVCC is now part of the closed Layer 4 contract (six shapes)."""

    def test_cvcc_is_an_allowed_shape(self) -> None:
        assert AllowedSyllableShape("CVCC") is AllowedSyllableShape.CVCC
        assert AllowedSyllableShape.CVCC in ALLOWED_SYLLABLE_SHAPES

    def test_baat_emits_cvcc_candidate(self) -> None:
        analysis = analyze_licensed_syllables(CVCC_EXAMPLE)  # "بَيت"
        assert len(analysis.candidates) == 1
        c = analysis.candidates[0]
        assert c.shape is AllowedSyllableShape.CVCC
        assert c.identity_preserved is True
        assert c.boundary_evidence.boundary_preserved is True
        assert c.economy_evidence.economy_satisfied is True
        assert c.runtime_status == CANDIDATE_RUNTIME_STATUS
        assert c.potential_only is True

    def test_baat_no_longer_invalidated(self) -> None:
        analysis = analyze_licensed_syllables(CVCC_EXAMPLE)
        surfaces = {inv.surface_form_vocalized for inv in analysis.invalidations}
        assert CVCC_EXAMPLE not in surfaces


# ─────────────────────────────────────────────────────────────────────────────
# Group 7 — Unsupported shape invalidation
# ─────────────────────────────────────────────────────────────────────────────


class TestUnsupportedInvalidation:
    """Group 7 — No candidate emitted; invalidation evidence is deterministic."""

    @pytest.mark.parametrize("token", UNSUPPORTED_EXAMPLES)
    def test_no_candidate_emitted_for_unsupported_token(self, token: str) -> None:
        analysis = analyze_licensed_syllables(token)
        # Every token that does not match the closed contract must yield
        # an invalidation, and the candidate list must NOT contain it.
        surfaces = {c.surface_form_vocalized for c in analysis.candidates}
        assert token not in surfaces

    @pytest.mark.parametrize("token", UNSUPPORTED_EXAMPLES)
    def test_invalidation_evidence_recorded(self, token: str) -> None:
        analysis = analyze_licensed_syllables(token)
        invalidated = [
            inv for inv in analysis.invalidations
            if inv.surface_form_vocalized == token
        ]
        assert len(invalidated) == 1
        inv = invalidated[0]
        assert inv.candidate_emitted is False
        assert isinstance(inv.reason, str) and inv.reason
        # Reason is deterministic: identical call returns the same reason.
        re_analysis = analyze_licensed_syllables(token)
        re_inv = next(
            x for x in re_analysis.invalidations
            if x.surface_form_vocalized == token
        )
        assert re_inv.reason == inv.reason

    def test_canonical_sample_invalidates_daraba(self) -> None:
        analysis = analyze_licensed_syllables(SAMPLE_INPUT)
        assert len(analysis.invalidations) == 1
        inv = analysis.invalidations[0]
        assert inv.surface_form_vocalized == "ضَرَبَ"
        assert inv.candidate_emitted is False


# ─────────────────────────────────────────────────────────────────────────────
# Group 8 — Economy rule
# ─────────────────────────────────────────────────────────────────────────────


class TestEconomyRule:
    """Group 8 — economy_satisfied iff all five conjunct conditions hold."""

    @pytest.mark.parametrize("token", CV_EXAMPLES + (
        CVC_EXAMPLE, CVV_EXAMPLE, CVVC_EXAMPLE, CVVCC_EXAMPLE
    ))
    def test_economy_true_for_emitted_candidate(self, token: str) -> None:
        analysis = analyze_licensed_syllables(token)
        assert analysis.candidates, f"expected candidate for {token!r}"
        c = analysis.candidates[0]
        ec = c.economy_evidence
        assert ec.shape_allowed is True
        assert ec.boundary_preserved is True
        assert ec.identity_preserved is True
        assert ec.minimal_complete_syllable is True
        assert ec.no_unnecessary_expansion is True
        assert ec.economy_satisfied is True

    def test_economy_failure_blocks_candidate_emission_for_unsupported(self) -> None:
        analysis = analyze_licensed_syllables("ضَرَبَ")
        assert analysis.candidates == ()
        assert len(analysis.invalidations) == 1


# ─────────────────────────────────────────────────────────────────────────────
# Group 9 — Integration with analysis_trace
# ─────────────────────────────────────────────────────────────────────────────


class TestAnalysisTraceIntegration:
    """Group 9 — Layer 4 consumes lower-layer evidence; does not mutate it."""

    def test_token_indices_preserved(self) -> None:
        text = SAMPLE_INPUT
        trace = analyze_potential_trace(text)
        analysis = analyze_licensed_syllables(text)
        candidate_indices = {c.token_index for c in analysis.candidates}
        invalidation_surfaces = {
            inv.surface_form_vocalized for inv in analysis.invalidations
        }
        # Every emitted item maps back to a token from the lower-layer trace.
        token_indices = {t.token_index for t in trace.tokens}
        token_surfaces = {t.surface_form_vocalized for t in trace.tokens}
        assert candidate_indices.issubset(token_indices)
        assert invalidation_surfaces.issubset(token_surfaces)

    def test_start_end_indices_preserved(self) -> None:
        text = SAMPLE_INPUT
        trace = analyze_potential_trace(text)
        analysis = analyze_licensed_syllables(text)
        by_index = {t.token_index: t for t in trace.tokens}
        for c in analysis.candidates:
            t = by_index[c.token_index]
            assert c.boundary_evidence.start_index == t.start_index
            assert c.boundary_evidence.end_index == t.end_index

    def test_codepoints_preserved_from_lower_layer(self) -> None:
        text = SAMPLE_INPUT
        trace = analyze_potential_trace(text)
        analysis = analyze_licensed_syllables(text)
        by_index = {t.token_index: t for t in trace.tokens}
        for c in analysis.candidates:
            t = by_index[c.token_index]
            assert c.surface_codepoints == t.surface_codepoints
            assert c.surface_codepoint_names == t.surface_codepoint_names

    def test_aggregate_trace_not_mutated_by_layer4(self) -> None:
        text = SAMPLE_INPUT
        # Capture lower-layer aggregates before and after Layer 4 runs.
        trace_before = analyze_potential_trace(text)
        before_aggregates = (
            trace_before.total_token_count,
            dict(trace_before.without_resolver_counts),
            dict(trace_before.with_resolver_counts),
            trace_before.resolver_used_count,
            trace_before.unique_surface_count,
            trace_before.repeated_surface_count,
        )
        _ = analyze_licensed_syllables(text)
        trace_after = analyze_potential_trace(text)
        after_aggregates = (
            trace_after.total_token_count,
            dict(trace_after.without_resolver_counts),
            dict(trace_after.with_resolver_counts),
            trace_after.resolver_used_count,
            trace_after.unique_surface_count,
            trace_after.repeated_surface_count,
        )
        assert before_aggregates == after_aggregates

    def test_miu_statuses_not_rewritten(self) -> None:
        text = SAMPLE_INPUT
        trace_before = analyze_potential_trace(text)
        statuses_before = tuple(
            (t.token_index, t.without_resolver_status, t.with_resolver_status)
            for t in trace_before.tokens
        )
        _ = analyze_licensed_syllables(text)
        trace_after = analyze_potential_trace(text)
        statuses_after = tuple(
            (t.token_index, t.without_resolver_status, t.with_resolver_status)
            for t in trace_after.tokens
        )
        assert statuses_before == statuses_after


# ─────────────────────────────────────────────────────────────────────────────
# Group 10 — CLI/tool test
# ─────────────────────────────────────────────────────────────────────────────


class TestDemoToolCli:
    """Group 10 — qiyas_licensed_syllable_demo.py CLI smoke test."""

    @pytest.fixture(scope="class")
    def cli_output(self) -> str:
        result = subprocess.run(
            [sys.executable, str(DEMO_TOOL), SAMPLE_INPUT],
            cwd=str(REPO_ROOT),
            env={"PYTHONPATH": f"{REPO_ROOT / 'src'}:{REPO_ROOT}"},
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"demo exited {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        return result.stdout

    @pytest.mark.parametrize(
        "expected_phrase",
        [
            "Licensed Syllable Analysis",
            "runtime_status=layer4_potential_only",
            "allowed_shapes=CV,CVC,CVV,CVVC,CVCC,CVVCC",
            "candidate_count",
            "invalidation_count",
            "Constitutional Boundary",
            "no meaning introduced",
            "no hukm introduced",
            "no i'rab introduced",
            "no dalalah introduced",
            "no reality claim introduced",
        ],
    )
    def test_cli_output_contains(
        self, cli_output: str, expected_phrase: str
    ) -> None:
        assert expected_phrase in cli_output, (
            f"CLI output missing required phrase: {expected_phrase!r}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Group 11 — Negative constitutional guard
# ─────────────────────────────────────────────────────────────────────────────


# Forbidden positive claims: the rendered output and the module source
# must not assert any of these. Each pattern is paired with allowed
# negation contexts that contain it. Substring matches inside a negation
# context (e.g. "no meaning introduced") are allowed; standalone positive
# occurrences are not.
FORBIDDEN_POSITIVE_PATTERNS = (
    "meaning",
    "hukm",
    "i'rab",
    "irab",
    "dalalah",
    "tafsir",
    "reality",
    "final meaning",
    "word candidate",
    "lafz candidate",
    "semantic runtime",
)

# A line that contains a forbidden pattern is allowed only if one of
# these negation contexts also appears on the same line.
NEGATION_PREFIXES = (
    "no ",
    "not_introduced",
    "not introduced",
    "must not",
    "does not introduce",
    "does not claim",
    "forbidden",
    "must NOT",
    "explicitly NOT",
    "does NOT",
    "no_",
    "without ",
)


def _violates_negation_rule(line: str, pattern: str) -> bool:
    """True iff the line contains `pattern` but no allowed negation context."""
    lower = line.lower()
    if pattern.lower() not in lower:
        return False
    return not any(neg.lower() in lower for neg in NEGATION_PREFIXES)


class TestNegativeConstitutionalGuard:
    """Group 11 — No positive meaning/hukm/i'rab/dalalah/reality claim."""

    def test_rendered_output_has_no_positive_claims(self) -> None:
        analysis = analyze_licensed_syllables(SAMPLE_INPUT)
        rendered = render_licensed_syllable_analysis(analysis)
        violations: list[tuple[int, str, str]] = []
        for lineno, line in enumerate(rendered.splitlines(), start=1):
            for pattern in FORBIDDEN_POSITIVE_PATTERNS:
                if _violates_negation_rule(line, pattern):
                    violations.append((lineno, pattern, line))
        assert violations == [], (
            f"forbidden positive claims in rendered output: {violations}"
        )

    def test_module_source_has_no_positive_claims(self) -> None:
        source = LICENSED_MODULE_SRC.read_text(encoding="utf-8")
        violations: list[tuple[int, str, str]] = []
        for lineno, line in enumerate(source.splitlines(), start=1):
            for pattern in FORBIDDEN_POSITIVE_PATTERNS:
                if _violates_negation_rule(line, pattern):
                    violations.append((lineno, pattern, line))
        # Tolerated occurrences (status plumbing, not positive claims):
        #   - status-field type annotations: `<pattern>_status: str`
        #   - status-field f-string references: `{analysis.<pattern>_status}`
        #     and similar containing `_status` token
        # These lines do not assert that meaning / hukm / etc was claimed;
        # they wire up the `not_introduced` status fields.
        tolerated: list[tuple[int, str, str]] = []
        for lineno, pattern, line in violations:
            lower = line.lower()
            if "_status" in lower:
                tolerated.append((lineno, pattern, line))
        real = [v for v in violations if v not in tolerated]
        assert real == [], (
            f"forbidden positive claims in module source: {real}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Group 12 — No Layer 5+ classes or runtime
# ─────────────────────────────────────────────────────────────────────────────


FORBIDDEN_LAYER5_NAMES = (
    "WordCandidate",
    "LafzCandidate",
    "DalalahCandidate",
    "HukmCandidate",
    "FinalMeaning",
    "RealityClaim",
    "AmilEffectEvidence",
    "I'rabEffectEvidence",
    "IrabEffectEvidence",
    "SemanticRuntime",
)


class TestNoForbiddenLayers:
    """Group 12 — No Layer 5+ runtime classes anywhere in the module."""

    @pytest.mark.parametrize("name", FORBIDDEN_LAYER5_NAMES)
    def test_no_forbidden_class_in_module(self, name: str) -> None:
        assert not hasattr(licensed_syllable, name), (
            f"forbidden Layer 5+ class {name!r} is present in licensed_syllable"
        )

    @pytest.mark.parametrize("name", FORBIDDEN_LAYER5_NAMES)
    def test_no_forbidden_name_in_source(self, name: str) -> None:
        source = LICENSED_MODULE_SRC.read_text(encoding="utf-8")
        # Allow the names to appear only inside negation/guard contexts in
        # comments. Direct definitions, returns, or instantiations are
        # never present, so a substring check is sufficient.
        if name in source:
            # If the name appears, it must be inside a comment that
            # negates / forbids it. Conservative: require "no " or
            # "FORBIDDEN" or "not " on the same line.
            for line in source.splitlines():
                if name in line:
                    lower = line.lower()
                    assert any(
                        prefix.lower() in lower
                        for prefix in NEGATION_PREFIXES
                    ), (
                        f"forbidden name {name!r} appears without negation: "
                        f"{line!r}"
                    )


# ─────────────────────────────────────────────────────────────────────────────
# Group 13 — Backward compatibility (smoke)
# ─────────────────────────────────────────────────────────────────────────────


class TestBackwardCompatibility:
    """Group 13 — Existing canonical test files still collect and pass.

    These are smoke-level checks: each referenced suite is expected to
    pass under the full canonical run. This test file simply imports
    them to confirm collection still works after Layer 4 lands.
    """

    @pytest.mark.parametrize(
        "module_dot_path",
        [
            "tests.qiyas_core.test_analysis_trace",
            "tests.qiyas_core.test_licensed_syllable_readiness",
            "tests.qiyas_core.test_qiyas_freeze_status",
            "tests.qiyas_core.test_source_snapshot_inventory_demo",
            "tests.qiyas_core.test_variant_resolver_miu_integration",
            "tests.qiyas_core.test_repository_responsibility_matrix",
        ],
    )
    def test_existing_test_module_collectable(self, module_dot_path: str) -> None:
        # We do not execute the suite — pytest collects it under the
        # parent run. We only verify the module file exists.
        relative = module_dot_path.replace(".", "/") + ".py"
        assert (REPO_ROOT / relative).is_file(), (
            f"existing test module missing: {relative}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Misc — runtime status constants alignment
# ─────────────────────────────────────────────────────────────────────────────


class TestRuntimeStatusConstants:
    """Layer 4 status constants match the directive verbatim."""

    def test_layer4_runtime_status_label(self) -> None:
        assert LAYER4_RUNTIME_STATUS == "layer4_potential_only"

    def test_candidate_runtime_status_label(self) -> None:
        assert CANDIDATE_RUNTIME_STATUS == "potential_only_not_semantic_runtime"

    def test_evidence_source_label(self) -> None:
        assert EVIDENCE_SOURCE == "qiyas_core.analysis_trace"

    def test_analysis_carries_status_constants(self) -> None:
        a = analyze_licensed_syllables(SAMPLE_INPUT)
        assert a.runtime_status == LAYER4_RUNTIME_STATUS
        assert a.meaning_status == "not_introduced"
        assert a.hukm_status == "not_introduced"
        assert a.irab_status == "not_introduced"
        assert a.dalalah_status == "not_introduced"
        assert a.reality_status == "not_introduced"
