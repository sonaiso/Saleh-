"""
run_qiyas.py — Canonical pipeline driver for the Qiyas algebra.

Takes an Arabic text string or a path to a UTF-8 file and walks every codepoint
through the full canonical Phase-1 chain, exactly as defined in src/qiyas_core:

    raw text
      → SequenceContextTokenizer   (pre-qiyas; non-Candidate sequence framing)
      → UnicodeQiyas
        → TypedCodePointClassificationQiyas
          → LetterIdentityQiyas   (only for LetterCodePoint)
          → HarakaFunctionQiyas   (only for HarakaCodePoint)
          → PositionQiyas         (only for LetterCodePoint, with tokenizer-
                                    derived INITIAL/MEDIAL/FINAL/ISOLATED)
            → ConditionedTypedSequenceQiyas  (carrier-binding, gated by
                                    tokenizer segment context)
              → SlotQiyas         (only when a LetterCodePoint at index i is
                                    followed by a HarakaCodePoint at i+1 in the
                                    same tokenizer segment, per the canonical
                                    SLOT_COMPOSITION_RULE)

Per `PRE_QIYAS_TOKENIZER_CONSTITUTION.md` (Option C), whitespace/boundary and
punctuation framing is sourced from `SequenceContextTokenizer` markers, not
from `is_boundary` / `BoundaryCodePoint`. Boundary characters never enter
`UnicodeQiyas` as `UnicodeCandidate`, never become `TypedCodePoint`, and never
become identity — they appear in the audit as tokenizer markers only.

Every layer transition is performed by calling the canonical adapter, which in
turn invokes QiyasKernel.apply(QiyasRequest) -> CandidateSet. No new rules,
adapters, types, evidence claims, or candidates are introduced here; this file
only orchestrates what already lives in src/qiyas_core/.

Run from the repository root:

    PYTHONPATH=src python3 run_qiyas.py "بَتْ"
    PYTHONPATH=src python3 run_qiyas.py path/to/file.txt
    PYTHONPATH=src python3 run_qiyas.py --json "بَتْ"
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Make the canonical package importable when this script is invoked from any
# working directory (e.g. `python3 /abs/path/to/run_qiyas.py ...`). We simply
# prepend the project's `src/` directory — which sits next to this file — to
# sys.path. No algebraic behavior is added or altered.
_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from qiyas_core.candidate import Candidate, CandidateSet
from qiyas_core.conditioned_typed_sequence_adapter import (
    ConditionedTypedSequenceLayerAdapter,
)
from qiyas_core.enums import CandidateStatus
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.registry_projection_adapter import RegistryProjectionLayerAdapter
from qiyas_core.root_stem_adapter import RootStemLayerAdapter
from qiyas_core.jamid_mushtaq_adapter import JamidMushtaqLayerAdapter
from qiyas_core.mufrad_word_adapter import MufradWordLayerAdapter
from qiyas_core.rules.position_rules import (
    POSITION_FINAL,
    POSITION_INITIAL,
    POSITION_ISOLATED,
    POSITION_MEDIAL,
)
from qiyas_core.sequence_context_tokenizer import (
    MarkerType,
    SequenceContextTokenizer,
    SequenceMarker,
    TokenizedSequence,
)
from qiyas_core.slot_adapter import SlotLayerAdapter
from qiyas_core.typed_codepoint_adapter import (
    TypedCodePointLayerAdapter,
    is_arabic_haraka,
    is_arabic_letter,
)
from qiyas_core.unicode_adapter import UnicodeLayerAdapter


# ---------------------------------------------------------------------------
# 1. Canonical pipeline
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PipelineLayers:
    """Bundle of every canonical adapter, all sharing one QiyasKernel."""

    kernel: QiyasKernel
    unicode_layer: UnicodeLayerAdapter
    typed_layer: TypedCodePointLayerAdapter
    letter_identity_layer: LetterIdentityLayerAdapter
    haraka_function_layer: HarakaFunctionLayerAdapter
    position_layer: PositionLayerAdapter
    cts_layer: ConditionedTypedSequenceLayerAdapter
    slot_layer: SlotLayerAdapter
    registry_projection_layer: RegistryProjectionLayerAdapter
    root_stem_layer: RootStemLayerAdapter
    jamid_mushtaq_layer: JamidMushtaqLayerAdapter
    mufrad_word_layer: MufradWordLayerAdapter

    @classmethod
    def build(cls) -> "PipelineLayers":
        kernel = QiyasKernel()
        return cls(
            kernel=kernel,
            unicode_layer=UnicodeLayerAdapter(kernel=kernel),
            typed_layer=TypedCodePointLayerAdapter(kernel=kernel),
            letter_identity_layer=LetterIdentityLayerAdapter(kernel=kernel),
            haraka_function_layer=HarakaFunctionLayerAdapter(kernel=kernel),
            position_layer=PositionLayerAdapter(kernel=kernel),
            cts_layer=ConditionedTypedSequenceLayerAdapter(kernel=kernel),
            slot_layer=SlotLayerAdapter(kernel=kernel),
            registry_projection_layer=RegistryProjectionLayerAdapter(kernel=kernel),
            root_stem_layer=RootStemLayerAdapter(kernel=kernel),
            jamid_mushtaq_layer=JamidMushtaqLayerAdapter(kernel=kernel),
            mufrad_word_layer=MufradWordLayerAdapter(kernel=kernel),
        )


def _classify_position(
    text: str,
    index: int,
    markers_by_index: dict[int, SequenceMarker],
) -> str:
    """
    Determine INITIAL/MEDIAL/FINAL/ISOLATED for an Arabic letter at `index`
    using `SequenceContextTokenizer` segment context.

    A letter at position i is INITIAL if its tokenizer segment starts here
    (no preceding Arabic letter in the same segment); FINAL if its segment
    ends here (no following Arabic letter in the same segment); ISOLATED if
    both; otherwise MEDIAL. Harakat are transparent — they do not interrupt
    letter adjacency.

    Boundary detection is sourced from `SequenceContextTokenizer` markers,
    not from `is_boundary` (`PRE_QIYAS_TOKENIZER_CONSTITUTION.md` §1, §6).
    This selection rule introduces no new evidence claims; the four
    canonical position rules in `src/qiyas_core/rules/position_rules.py`
    remain the sole authority.
    """
    cur_marker = markers_by_index.get(index)
    cur_seg = cur_marker.segment_id if cur_marker is not None else None

    def _in_current_segment(k: int) -> bool:
        m = markers_by_index.get(k)
        return m is not None and m.segment_id == cur_seg

    def _prev_letter_or_boundary(j: int) -> str:
        k = j - 1
        while k >= 0 and _in_current_segment(k) and is_arabic_haraka(ord(text[k])):
            k -= 1
        if k < 0 or not _in_current_segment(k):
            return "boundary"
        if is_arabic_letter(ord(text[k])):
            return "letter"
        return "boundary"

    def _next_letter_or_boundary(j: int) -> str:
        k = j + 1
        while k < len(text) and _in_current_segment(k) and is_arabic_haraka(ord(text[k])):
            k += 1
        if k >= len(text) or not _in_current_segment(k):
            return "boundary"
        if is_arabic_letter(ord(text[k])):
            return "letter"
        return "boundary"

    prev = _prev_letter_or_boundary(index)
    nxt = _next_letter_or_boundary(index)

    if prev == "boundary" and nxt == "boundary":
        return POSITION_ISOLATED
    if prev == "boundary" and nxt == "letter":
        return POSITION_INITIAL
    if prev == "letter" and nxt == "boundary":
        return POSITION_FINAL
    return POSITION_MEDIAL


def _same_segment(
    markers_by_index: dict[int, SequenceMarker],
    i_left: int,
    i_right: int,
) -> bool:
    """Return True iff both text positions are in the same tokenizer segment.

    Used to gate carrier-binding: a letter and its candidate haraka may
    only bind when they share a `SequenceContextTokenizer` segment, so
    whitespace and punctuation framing block cross-boundary binding
    without ever entering the qiyas chain as candidates.
    """
    m_left = markers_by_index.get(i_left)
    m_right = markers_by_index.get(i_right)
    if m_left is None or m_right is None:
        return False
    return m_left.segment_id == m_right.segment_id


def _tokenizer_marker_dict(marker: SequenceMarker | None) -> dict[str, Any] | None:
    """Serialize a tokenizer marker for audit output (never a Candidate)."""
    if marker is None:
        return None
    return {
        "index": marker.index,
        "marker_type": marker.marker_type.value,
        "normalized_label": marker.normalized_label,
        "segment_id": marker.segment_id,
        "reason": marker.reason,
    }


# ---------------------------------------------------------------------------
# 2. Per-character step records (audit only; no domain logic)
# ---------------------------------------------------------------------------


@dataclass
class LayerStep:
    layer: str
    rule_id: str
    candidate_type: str
    status: str
    rank: str
    identity_ids: tuple[str, ...]
    trace_ids: tuple[str, ...]
    residuals: tuple[dict[str, str], ...]

    @classmethod
    def from_set(cls, layer: str, candidate_set: CandidateSet) -> "LayerStep":
        c = candidate_set.candidates[0]
        return cls(
            layer=layer,
            rule_id=c.source_rule_id,
            candidate_type=c.candidate_type,
            status=c.status.value,
            rank=c.rank.name,
            identity_ids=tuple(c.identity_ids),
            trace_ids=tuple(c.trace_ids),
            residuals=tuple(
                {
                    "type": r.residual_type,
                    "effect": r.effect.value,
                    "severity": r.severity.value,
                    "message": r.message,
                }
                for r in c.residuals
            ),
        )


@dataclass
class CharacterReport:
    index: int
    char: str
    codepoint: int
    steps: list[LayerStep]
    slot_step: LayerStep | None = None
    skipped_reason: str | None = None
    # Per PRE_QIYAS_TOKENIZER_CONSTITUTION.md §3, the tokenizer emits
    # structural markers — not Candidates. They appear on the audit
    # report as sequence context only.
    tokenizer_marker: dict[str, Any] | None = None


def _accepted(cs: CandidateSet) -> Candidate | None:
    accepted = cs.accepted
    return accepted[0] if accepted else None


# ---------------------------------------------------------------------------
# 3. Driver — walk every character through every applicable layer
# ---------------------------------------------------------------------------


def process_text(
    text: str,
    layers: PipelineLayers | None = None,
    tokenizer: SequenceContextTokenizer | None = None,
) -> list[CharacterReport]:
    layers = layers or PipelineLayers.build()
    tokenizer = tokenizer or SequenceContextTokenizer()

    # Pre-qiyas tokenization: structural markers for whitespace, punctuation,
    # arabic symbols, and residuals. These are NOT Candidates — they are
    # consumed by the driver to compute segment-based position context and to
    # gate cross-boundary carrier-binding. They never enter UnicodeQiyas.
    tokenized: TokenizedSequence = tokenizer.tokenize(text)
    markers_by_index: dict[int, SequenceMarker] = {
        m.index: m for m in tokenized.markers
    }

    reports: list[CharacterReport] = []

    # Pre-classify every Arabic-eligible character so the SlotQiyas
    # composition can look ahead. Non-Arabic characters are recorded as
    # "non_arabic" — their tokenizer markers travel on the audit report
    # but they never produce TypedCodePoint candidates.
    classifications: list[tuple[str, Candidate | None]] = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        u_set = layers.unicode_layer.process_codepoint(cp, trace_prefix=f"text[{i}]:u:{cp:04x}")
        u_cand = _accepted(u_set)
        if u_cand is None:
            classifications.append(("non_arabic", None))
            continue
        t_set = layers.typed_layer.classify_unicode_candidate(
            u_cand, trace_prefix=f"text[{i}]:t:{cp:04x}"
        )
        t_cand = _accepted(t_set)
        classifications.append((t_cand.candidate_type if t_cand else "blocked", t_cand))

    # Second pass: run all applicable downstream layers and capture audit
    for i, ch in enumerate(text):
        cp = ord(ch)
        marker = markers_by_index.get(i)
        report = CharacterReport(
            index=i,
            char=ch,
            codepoint=cp,
            steps=[],
            tokenizer_marker=_tokenizer_marker_dict(marker),
        )

        u_set = layers.unicode_layer.process_codepoint(cp, trace_prefix=f"text[{i}]:u:{cp:04x}")
        report.steps.append(LayerStep.from_set("UnicodeQiyas", u_set))

        u_cand = _accepted(u_set)
        if u_cand is None:
            # Skip reason is tokenizer-aware: whitespace / punctuation /
            # residual codepoints rejected by UnicodeQiyas are surfaced
            # by their tokenizer marker, not by any qiyas Candidate.
            if marker is not None and marker.marker_type == MarkerType.WHITESPACE_BOUNDARY:
                report.skipped_reason = (
                    f"whitespace tokenizer boundary marker "
                    f"(segment {marker.segment_id})"
                )
            elif marker is not None and marker.marker_type == MarkerType.PUNCTUATION_BOUNDARY:
                report.skipped_reason = (
                    f"punctuation tokenizer boundary marker "
                    f"(segment {marker.segment_id})"
                )
            elif marker is not None and marker.marker_type == MarkerType.RESIDUAL_PRESERVATION:
                report.skipped_reason = (
                    f"residual preservation marker "
                    f"(segment {marker.segment_id})"
                )
            else:
                report.skipped_reason = "not Arabic per UnicodeQiyas"
            reports.append(report)
            continue

        t_set = layers.typed_layer.classify_unicode_candidate(
            u_cand, trace_prefix=f"text[{i}]:t:{cp:04x}"
        )
        report.steps.append(LayerStep.from_set("TypedCodePointClassificationQiyas", t_set))
        t_cand = _accepted(t_set)
        if t_cand is None:
            report.skipped_reason = "TypedCodePoint classification blocked"
            reports.append(report)
            continue

        ctype = t_cand.candidate_type

        if ctype == "LetterCodePoint":
            # LetterIdentityQiyas
            # PR-rebase note: Option C refactored LetterIdentityLayerAdapter;
            # the entry point is now `process_letter_codepoint` (Layer 1 —
            # pure identity proof from LetterCodePoint, no makhraj/sifat).
            li_set = layers.letter_identity_layer.process_letter_codepoint(
                t_cand, trace_prefix=f"text[{i}]:li:{cp:04x}"
            )
            report.steps.append(LayerStep.from_set("LetterIdentityQiyas", li_set))
            li_cand = _accepted(li_set)

            # Canonical order (SCG-P1 PR-2): TypedCodePoint
            #   → ConditionedTypedSequence/PositionEvidence → PositionCarrier.
            # The sequence layer first stamps the conditioned-sequence identity
            # on a PositionEvidence; PositionCarrier then consumes that evidence
            # (preserving conditioned_sequence_identity as canonical; the
            # codepoint survives only as a trace/bridge reference).
            pe_set = layers.cts_layer.prove_letter_position(
                t_cand,
                index=i,
                sequence_length=len(text),
                trace_prefix=f"text[{i}]:cts:pos:{cp:04x}",
            )
            report.steps.append(
                LayerStep.from_set("ConditionedTypedSequenceQiyas[position]", pe_set)
            )
            pe_cand = _accepted(pe_set)

            # PositionQiyas — position type derived from tokenizer segment
            # context (Z5: §6 / §8 of PRE_QIYAS_TOKENIZER_CONSTITUTION),
            # consuming the CTS PositionEvidence as canonical origin.
            ptype = _classify_position(text, i, markers_by_index)
            p_cand = None
            if pe_cand is not None:
                p_set = layers.position_layer.prove_position(
                    pe_cand,
                    position_type=ptype,
                    index=i,
                    within_word=True,
                    at_boundary=(ptype in (POSITION_INITIAL, POSITION_FINAL, POSITION_ISOLATED)),
                    trace_prefix=f"text[{i}]:p:{cp:04x}",
                )
                report.steps.append(LayerStep.from_set(f"PositionQiyas[{ptype}]", p_set))
                p_cand = _accepted(p_set)

            # ConditionedTypedSequence + SlotQiyas (PR #27 wiring, Z5
            # tokenizer gate). Per CLAUDE.md §8 the SlotCandidate consumes
            # an explicit AlignmentEvidence / CarrierBindingCandidate from
            # the CTS layer; the driver does NOT self-assert any alignment
            # and binding is allowed only inside a single tokenizer
            # segment, so whitespace and punctuation framing block
            # cross-boundary carriers without ever entering the qiyas
            # chain as candidates.
            haraka_adjacent = (
                i + 1 < len(text)
                and classifications[i + 1][0] == "HarakaCodePoint"
            )
            if (
                li_cand is not None
                and p_cand is not None
                and haraka_adjacent
                and _same_segment(markers_by_index, i, i + 1)
            ):
                haraka_typed = classifications[i + 1][1]
                assert haraka_typed is not None
                hf_set = layers.haraka_function_layer.prove_haraka_function(
                    haraka_typed,
                    trace_prefix=f"text[{i+1}]:hf:{ord(text[i+1]):04x}",
                )
                hf_cand = _accepted(hf_set)

                # ConditionedTypedSequenceQiyas — produce the alignment
                # proof from the TypedCodePoint pair. The CTS layer is
                # parallel to the atomic identity/function proofs; its
                # output is consumed (not bypassed) by SlotQiyas below.
                cb_set = layers.cts_layer.prove_carrier_binding(
                    haraka_typed=haraka_typed,
                    carrier_letter_typed=t_cand,
                    index=i + 1,
                    sequence_length=len(text),
                    trace_prefix=(
                        f"text[{i}]:cts:cb:{cp:04x}+{ord(text[i+1]):04x}"
                    ),
                )
                report.steps.append(
                    LayerStep.from_set("ConditionedTypedSequenceQiyas", cb_set)
                )
                cb_cand = _accepted(cb_set)

                if hf_cand is not None and cb_cand is not None:
                    s_set = layers.slot_layer.compose_slot(
                        li_cand,
                        hf_cand,
                        p_cand,
                        alignment_evidence=cb_cand,
                        trace_prefix=f"text[{i}]:slot:{cp:04x}+{ord(text[i+1]):04x}",
                    )
                    report.slot_step = LayerStep.from_set("SlotQiyas", s_set)

                    # SCG-P2 — RegistryProjectionQiyas: project the licensed
                    # SlotCandidate onto registry membership classes
                    # (candidate-only; opens root/stem + word-type priors;
                    # never produces RootStemCandidate or any downstream type).
                    s_cand = _accepted(s_set)
                    if s_cand is not None:
                        rp_set = layers.registry_projection_layer.project(
                            s_cand, trace_prefix=f"text[{i}]:rp:{cp:04x}"
                        )
                        report.steps.append(
                            LayerStep.from_set("RegistryProjectionQiyas", rp_set)
                        )

                        # SCG-P3 — RootStemQiyas: close a structural root/stem
                        # POSSIBILITY from the projection (candidate-only; opens
                        # jamid/mushtaq + word-pattern priors; never produces a
                        # final root, wazn, word, or any P4+ candidate).
                        rp_cand = _accepted(rp_set)
                        if rp_cand is not None:
                            rs_set = layers.root_stem_layer.close(
                                rp_cand, trace_prefix=f"text[{i}]:rs:{cp:04x}"
                            )
                            report.steps.append(
                                LayerStep.from_set("RootStemQiyas", rs_set)
                            )

                            # SCG-P4 — JamidMushtaqQiyas: open a structural
                            # derivation-class POSSIBILITY from the root/stem
                            # (candidate-only; opens word-type priors; never a
                            # final jamid/mushtaq judgment, wazn, or P5+ candidate).
                            rs_cand = _accepted(rs_set)
                            if rs_cand is not None:
                                jm_set = layers.jamid_mushtaq_layer.classify(
                                    rs_cand, trace_prefix=f"text[{i}]:jm:{cp:04x}"
                                )
                                report.steps.append(
                                    LayerStep.from_set("JamidMushtaqQiyas", jm_set)
                                )

                                # SCG-P5 — MufradWordQiyas: form a candidate-only
                                # single-word POSSIBILITY (opens verbal-signified +
                                # phrase-level priors; never a final lexical word,
                                # dictionary entry, or P6+ candidate).
                                jm_cand = _accepted(jm_set)
                                if jm_cand is not None:
                                    mw_set = layers.mufrad_word_layer.form(
                                        jm_cand, trace_prefix=f"text[{i}]:mw:{cp:04x}"
                                    )
                                    report.steps.append(
                                        LayerStep.from_set("MufradWordQiyas", mw_set)
                                    )
            elif haraka_adjacent and not _same_segment(markers_by_index, i, i + 1):
                # Letter and following haraka are in different tokenizer
                # segments (whitespace / punctuation framing between them).
                # The carrier-binding is rejected at the driver gate without
                # invoking CTS — the rejection is recorded by the report's
                # tokenizer_marker, not by any boundary Candidate.
                report.skipped_reason = (
                    "carrier-binding declined: letter and following haraka "
                    f"are in different tokenizer segments "
                    f"({markers_by_index[i].segment_id} → "
                    f"{markers_by_index[i + 1].segment_id})"
                )

        elif ctype == "HarakaCodePoint":
            hf_set = layers.haraka_function_layer.prove_haraka_function(
                t_cand, trace_prefix=f"text[{i}]:hf:{cp:04x}"
            )
            report.steps.append(LayerStep.from_set("HarakaFunctionQiyas", hf_set))

        else:
            # PunctuationCodePoint / ResidualCodePoint: these still appear as
            # TypedCodePoint candidates (they are inside the Arabic Unicode
            # block and survive UnicodeQiyas), but the canonical pipeline
            # defines no further layer for them — punctuation is consumed
            # as sequence-framing context via the tokenizer marker on this
            # report. Whitespace never reaches this branch (it is rejected
            # at UnicodeQiyas above). `BoundaryCodePoint` is legacy
            # unreachable post-Z4 and is not part of the canonical path.
            report.skipped_reason = (
                f"no downstream canonical layer defined for {ctype}"
            )

        reports.append(report)

    return reports


# ---------------------------------------------------------------------------
# 4. Output formatting
# ---------------------------------------------------------------------------


def _step_dict(step: LayerStep) -> dict[str, Any]:
    return {
        "layer": step.layer,
        "rule_id": step.rule_id,
        "candidate_type": step.candidate_type,
        "status": step.status,
        "rank": step.rank,
        "identity_ids": list(step.identity_ids),
        "trace_ids": list(step.trace_ids),
        "residuals": [dict(r) for r in step.residuals],
    }


def reports_to_json(reports: list[CharacterReport]) -> str:
    payload = []
    for r in reports:
        payload.append(
            {
                "index": r.index,
                "char": r.char,
                "codepoint": f"U+{r.codepoint:04X}",
                "tokenizer_marker": r.tokenizer_marker,
                "steps": [_step_dict(s) for s in r.steps],
                "slot": _step_dict(r.slot_step) if r.slot_step else None,
                "skipped_reason": r.skipped_reason,
            }
        )
    return json.dumps(payload, ensure_ascii=False, indent=2)


def reports_to_text(reports: list[CharacterReport]) -> str:
    lines: list[str] = []
    for r in reports:
        lines.append(f"==[{r.index:3d}] '{r.char}'  U+{r.codepoint:04X}==")
        if r.tokenizer_marker is not None:
            tm = r.tokenizer_marker
            lines.append(
                f"  tokenizer_marker={tm['marker_type']:<35s} "
                f"segment={tm['segment_id']!s:<3s} label={tm['normalized_label']}"
            )
        for s in r.steps:
            lines.append(
                f"  {s.layer:<42s} rule={s.rule_id:<36s} "
                f"-> {s.candidate_type:<28s} status={s.status:<8s} rank={s.rank}"
            )
            for res in s.residuals:
                lines.append(
                    f"      residual {res['effect']:<6s} {res['severity']:<7s} "
                    f"{res['type']}: {res['message']}"
                )
        if r.slot_step:
            s = r.slot_step
            lines.append(
                f"  {s.layer:<42s} rule={s.rule_id:<36s} "
                f"-> {s.candidate_type:<28s} status={s.status:<8s} rank={s.rank}"
            )
            for res in s.residuals:
                lines.append(
                    f"      residual {res['effect']:<6s} {res['severity']:<7s} "
                    f"{res['type']}: {res['message']}"
                )
        if r.skipped_reason:
            lines.append(f"  (downstream skipped: {r.skipped_reason})")
    return "\n".join(lines)


def reports_to_summary(reports: list[CharacterReport]) -> str:
    n = len(reports)
    counts: dict[str, int] = {}
    for r in reports:
        for s in r.steps:
            counts[f"{s.layer}:{s.status}"] = counts.get(f"{s.layer}:{s.status}", 0) + 1
        if r.slot_step is not None:
            counts[f"SlotQiyas:{r.slot_step.status}"] = (
                counts.get(f"SlotQiyas:{r.slot_step.status}", 0) + 1
            )
    lines = [f"characters processed: {n}"]
    for key in sorted(counts):
        lines.append(f"  {key}: {counts[key]}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. CLI
# ---------------------------------------------------------------------------


def _read_input(arg: str) -> str:
    p = Path(arg)
    if p.is_file():
        return p.read_text(encoding="utf-8")
    return arg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run Arabic text through the full canonical Qiyas Phase-1 chain "
            "(Unicode → TypedCodePoint → LetterIdentity / HarakaFunction / "
            "Position → Slot), via QiyasKernel.apply()."
        )
    )
    parser.add_argument(
        "input",
        help=(
            "Either an Arabic text string, or a path to a UTF-8 text file. "
            "If the argument is a path that exists on disk, its contents are read; "
            "otherwise the argument itself is treated as the input text."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of the human-readable trace.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Emit only an aggregate counts summary.",
    )
    args = parser.parse_args(argv)

    text = _read_input(args.input)
    reports = process_text(text)

    if args.json:
        print(reports_to_json(reports))
    elif args.summary:
        print(reports_to_summary(reports))
    else:
        print(reports_to_text(reports))
        print()
        print(reports_to_summary(reports))
    return 0


if __name__ == "__main__":
    sys.exit(main())
