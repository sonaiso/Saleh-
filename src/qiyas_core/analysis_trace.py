"""Potential-only MIU analysis trace.

Run as a module:
    PYTHONPATH=src:. python3 -m qiyas_core.analysis_trace "بِ ضَ وَ يَ ضَرَبَ"

Or import:
    from qiyas_core.analysis_trace import analyze_potential_trace, render_analysis_trace

Given a whitespace-tokenized vocalized Arabic input, this module produces a
structured, identity-preserving, potential-only trace of MIU decisions and
optional VariantResolver effects. The trace is built by calling the existing
canonical ``ArabicVariantResolver`` and
``MinimalIndependentUnitReadinessLayerAdapter`` APIs in the same shape the
post-PR-#82 MIU integration tests use; this module does NOT re-implement that
logic.

Constitutional discipline:
  * potential-only — no row, no candidate, no claim is final
  * identity-preserving — surface_form_vocalized is the identity carrier;
    harakat are not collapsed
  * proof/trace oriented — separation of identity from trace per CLAUDE.md § 4
  * NOT semantic interpretation — no meaning, no hukm, no dalalah, no reality
    claim, no i'rab, no grammar derivation, no Word/Lafz/Dalalah/FinalMeaning/
    HukmCandidate/RealityClaim introduction
  * no source import — does not access ``new_arabic_analyzer/``
  * no registry admission beyond the existing MIU eligibility logic
"""

from __future__ import annotations

import sys
import unicodedata
import uuid
from dataclasses import dataclass, field
from typing import Iterable

from qiyas_core.arabic_variant_resolution_evidence import (
    ArabicVariantResolutionEvidence,
)
from qiyas_core.arabic_variant_resolver import ArabicVariantResolver
from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.minimal_unit_readiness_adapter import (
    MinimalIndependentUnitReadinessLayerAdapter,
)
from qiyas_core.slot_geometry_adapter import (
    SlotBindingEvidence,
    SlotGeometryLayerAdapter,
)
from qiyas_core.slot_geometry_closure_check import check_slot_geometry_closure


_ARABIC_LETTER_RANGE_START = 0x0621
_ARABIC_LETTER_RANGE_END_EXCLUSIVE = 0x064B
_ARABIC_HARAKA_RANGE_START = 0x064B
_ARABIC_HARAKA_RANGE_END_EXCLUSIVE = 0x0653
_DEFAULT_HARAKA = "064e"  # fatha — used when a token's letter carries no haraka

MODE_LABEL = "potential_only"
IDENTITY_CARRIER_LABEL = "surface_form_vocalized"
DIAGNOSTIC_KEY_LABEL = "surface_form_unvocalized_key"
RUNTIME_STATUS_LABEL = "not_semantic_runtime"


@dataclass(frozen=True)
class _LetterHarakaPair:
    letter_cp_hex: str
    haraka_cp_hex: str | None


@dataclass(frozen=True)
class TokenAnalysisTrace:
    token_index: int
    surface_form_vocalized: str
    surface_form_unvocalized_key: str
    pair_count: int
    without_resolver_status: str
    with_resolver_status: str
    resolver_used: bool
    residuals: tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class QiyasAnalysisTrace:
    input_text: str
    tokens: tuple[TokenAnalysisTrace, ...]
    mode: str = MODE_LABEL
    identity_carrier: str = IDENTITY_CARRIER_LABEL
    diagnostic_key: str = DIAGNOSTIC_KEY_LABEL
    runtime_status: str = RUNTIME_STATUS_LABEL


def _is_arabic_letter(ch: str) -> bool:
    cp = ord(ch)
    return _ARABIC_LETTER_RANGE_START <= cp < _ARABIC_LETTER_RANGE_END_EXCLUSIVE


def _is_arabic_haraka(ch: str) -> bool:
    cp = ord(ch)
    return _ARABIC_HARAKA_RANGE_START <= cp < _ARABIC_HARAKA_RANGE_END_EXCLUSIVE


def _parse_letter_haraka_pairs(token: str) -> tuple[_LetterHarakaPair, ...]:
    pairs: list[_LetterHarakaPair] = []
    current_letter: str | None = None
    current_haraka: str | None = None
    for ch in token:
        if _is_arabic_letter(ch):
            if current_letter is not None:
                pairs.append(
                    _LetterHarakaPair(
                        letter_cp_hex=f"{ord(current_letter):04x}",
                        haraka_cp_hex=current_haraka,
                    )
                )
            current_letter = ch
            current_haraka = None
        elif _is_arabic_haraka(ch):
            if current_letter is not None and current_haraka is None:
                current_haraka = f"{ord(ch):04x}"
    if current_letter is not None:
        pairs.append(
            _LetterHarakaPair(
                letter_cp_hex=f"{ord(current_letter):04x}",
                haraka_cp_hex=current_haraka,
            )
        )
    return tuple(pairs)


def _unvocalized_key(token: str) -> str:
    return "".join(ch for ch in token if not _is_arabic_haraka(ch))


def _make_slot_candidate(
    *, trace_label: str, letter_cp_hex: str, haraka_cp_hex: str
) -> Candidate:
    return Candidate(
        candidate_id=f"slot:analysis:{trace_label}:{uuid.uuid4().hex[:8]}",
        candidate_type="SlotCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id="slot.composition",
        asl_id="اصل:slot_composition_domain",
        far_id=f"فرع:slot:analysis:{trace_label}",
        identity_ids=(
            f"identity:codepoint:{letter_cp_hex}",
            f"identity:codepoint:{haraka_cp_hex}",
            "identity:slot_composition_domain",
        ),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(
            f"trace:analysis:{trace_label}:ev",
            f"trace:slot:alignment_ref:analysis:{trace_label}",
        ),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _seed_length_one_geometry(
    pair: _LetterHarakaPair, *, trace_label: str
) -> Candidate:
    haraka_hex = pair.haraka_cp_hex if pair.haraka_cp_hex is not None else _DEFAULT_HARAKA
    slot = _make_slot_candidate(
        trace_label=trace_label,
        letter_cp_hex=pair.letter_cp_hex,
        haraka_cp_hex=haraka_hex,
    )
    geom_adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    result = geom_adapter.seed_geometry(slot)
    if len(result.accepted) != 1:
        raise RuntimeError(
            "analysis_trace: length-1 SlotGeometry seed did not accept "
            f"letter_cp={pair.letter_cp_hex!r}"
        )
    return result.accepted[0]


def _build_length_two_geometry(
    first: _LetterHarakaPair,
    second: _LetterHarakaPair,
    *,
    trace_label: str,
) -> Candidate:
    first_slot = _make_slot_candidate(
        trace_label=f"{trace_label}_a",
        letter_cp_hex=first.letter_cp_hex,
        haraka_cp_hex=first.haraka_cp_hex or _DEFAULT_HARAKA,
    )
    second_slot = _make_slot_candidate(
        trace_label=f"{trace_label}_b",
        letter_cp_hex=second.letter_cp_hex,
        haraka_cp_hex=second.haraka_cp_hex or "0652",  # sukun for chained letter
    )
    geom_adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    seed_result = geom_adapter.seed_geometry(first_slot)
    if len(seed_result.accepted) != 1:
        raise RuntimeError(
            "analysis_trace: length-2 SlotGeometry seed did not accept first letter"
        )
    seed = seed_result.accepted[0]
    binding = SlotBindingEvidence(
        prev_segment_id=0,
        curr_segment_id=0,
        prev_position=0,
        curr_position=1,
        has_whitespace_between=False,
        has_punctuation_between=False,
        max_licensed_distance=1,
        binding_trace_ids=(f"trace:binding:analysis:{uuid.uuid4().hex[:8]}",),
    )
    extend_result = geom_adapter.extend_geometry(seed, second_slot, binding)
    if len(extend_result.accepted) != 1:
        raise RuntimeError(
            "analysis_trace: length-2 SlotGeometry extend did not accept second letter"
        )
    return extend_result.accepted[0]


def _classify(result) -> tuple[str, Candidate]:
    if result.accepted:
        return "ACCEPTED", result.accepted[0]
    if result.deferred:
        return "DEFERRED", result.deferred[0]
    return "BLOCKED", result.blocked[0]


def _residual_types(candidate: Candidate) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for r in candidate.residuals:
        if r.residual_type not in seen:
            seen.add(r.residual_type)
            ordered.append(r.residual_type)
    return tuple(ordered)


def _format_token_display(token: str) -> str:
    return token


def _explain(
    pair_count: int,
    without_status: str,
    with_status: str,
    resolver_used: bool,
) -> str:
    if pair_count > 1:
        return "length > 1 — MIU rejects"
    if without_status == "ACCEPTED" and with_status == "ACCEPTED" and not resolver_used:
        return "single-variant, registry-eligible"
    if without_status == "BLOCKED" and not resolver_used:
        return "symbol_not_eligible_for_minimal_unit"
    if without_status == "DEFERRED" and with_status == "ACCEPTED" and resolver_used:
        return "variant ambiguity resolved by non_madd evidence"
    if without_status == "DEFERRED" and with_status == "BLOCKED" and resolver_used:
        return "ambiguity resolved but registry says not eligible"
    return f"without_resolver={without_status} / with_resolver={with_status}"


def _analyze_token(token: str, *, token_index: int) -> TokenAnalysisTrace:
    nfc_token = unicodedata.normalize("NFC", token)
    pairs = _parse_letter_haraka_pairs(nfc_token)
    if not pairs:
        return TokenAnalysisTrace(
            token_index=token_index,
            surface_form_vocalized=nfc_token,
            surface_form_unvocalized_key=_unvocalized_key(nfc_token),
            pair_count=0,
            without_resolver_status="BLOCKED",
            with_resolver_status="BLOCKED",
            resolver_used=False,
            residuals=("no_arabic_letter_in_token",),
            explanation="no Arabic letter found in token",
        )

    trace_label = f"tok{token_index:02d}_{uuid.uuid4().hex[:6]}"
    miu_adapter = MinimalIndependentUnitReadinessLayerAdapter(kernel=QiyasKernel())
    resolver = ArabicVariantResolver()

    if len(pairs) == 1:
        geom = _seed_length_one_geometry(pairs[0], trace_label=trace_label)
    else:
        geom = _build_length_two_geometry(pairs[0], pairs[1], trace_label=trace_label)
    closure = check_slot_geometry_closure(geom)

    result_without = miu_adapter.admit(geom, closure)
    without_status, without_candidate = _classify(result_without)
    residuals_without = _residual_types(without_candidate)

    evidence = resolver.resolve(geom) if len(pairs) == 1 else None
    resolver_used = isinstance(evidence, ArabicVariantResolutionEvidence)

    if resolver_used:
        result_with = miu_adapter.admit(
            geom, closure, variant_resolution_evidence=evidence
        )
        with_status, with_candidate = _classify(result_with)
        residuals = _residual_types(with_candidate)
    else:
        with_status = without_status
        residuals = residuals_without

    return TokenAnalysisTrace(
        token_index=token_index,
        surface_form_vocalized=nfc_token,
        surface_form_unvocalized_key=_unvocalized_key(nfc_token),
        pair_count=len(pairs),
        without_resolver_status=without_status,
        with_resolver_status=with_status,
        resolver_used=resolver_used,
        residuals=residuals,
        explanation=_explain(
            pair_count=len(pairs),
            without_status=without_status,
            with_status=with_status,
            resolver_used=resolver_used,
        ),
    )


def analyze_potential_trace(text: str) -> QiyasAnalysisTrace:
    raw_tokens = text.split()
    token_traces: list[TokenAnalysisTrace] = []
    for idx, raw in enumerate(raw_tokens):
        token_traces.append(_analyze_token(raw, token_index=idx))
    return QiyasAnalysisTrace(input_text=text, tokens=tuple(token_traces))


def _format_residuals(residuals: Iterable[str]) -> str:
    items = ", ".join(residuals)
    return f"[{items}]"


def render_analysis_trace(trace: QiyasAnalysisTrace) -> str:
    lines: list[str] = []
    lines.append("Saleh/Qiyas Potential Analysis Trace")
    lines.append(f"input={trace.input_text}")
    lines.append(f"mode={trace.mode}")
    lines.append(f"identity_carrier={trace.identity_carrier}")
    lines.append(f"diagnostic_key={trace.diagnostic_key}")
    lines.append(f"runtime_status={trace.runtime_status}")
    lines.append("")
    for token_trace in trace.tokens:
        lines.append(f"token {token_trace.surface_form_vocalized}")
        lines.append(f"  without_resolver={token_trace.without_resolver_status}")
        lines.append(f"  with_resolver={token_trace.with_resolver_status}")
        lines.append(f"  resolver_used={'true' if token_trace.resolver_used else 'false'}")
        lines.append(f"  residuals={_format_residuals(token_trace.residuals)}")
        lines.append(f"  explanation={token_trace.explanation}")
        lines.append("")
    lines.append("End of Saleh/Qiyas Potential Analysis Trace.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    if not args:
        print(
            "usage: python3 -m qiyas_core.analysis_trace <vocalized_arabic_text>",
            file=sys.stderr,
        )
        return 2
    text = " ".join(args)
    trace = analyze_potential_trace(text)
    print(render_analysis_trace(trace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
