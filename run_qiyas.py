"""
run_qiyas.py — Canonical pipeline driver for the Qiyas algebra.

Takes an Arabic text string or a path to a UTF-8 file and walks every codepoint
through the full canonical Phase-1 chain, exactly as defined in src/qiyas_core:

    UnicodeQiyas
      → TypedCodePointClassificationQiyas
        → LetterIdentityQiyas   (only for LetterCodePoint)
        → HarakaFunctionQiyas   (only for HarakaCodePoint)
        → PositionQiyas         (only for LetterCodePoint, with sequence-derived
                                  INITIAL/MEDIAL/FINAL/ISOLATED)
          → SlotQiyas           (only when a LetterCodePoint at index i is
                                  followed by a HarakaCodePoint at i+1, per the
                                  canonical SLOT_COMPOSITION_RULE)

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
from qiyas_core.rules.position_rules import (
    POSITION_FINAL,
    POSITION_INITIAL,
    POSITION_ISOLATED,
    POSITION_MEDIAL,
)
from qiyas_core.slot_adapter import SlotLayerAdapter
from qiyas_core.typed_codepoint_adapter import (
    TypedCodePointLayerAdapter,
    is_arabic_haraka,
    is_arabic_letter,
    is_boundary,
    is_punctuation,
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
        )


def _classify_position(text: str, index: int) -> str:
    """
    Determine INITIAL/MEDIAL/FINAL/ISOLATED for an Arabic letter at `index`
    purely from sequence context.

    A letter at position i is INITIAL if it is preceded by a boundary or sits
    at index 0; FINAL if it is followed by a boundary or sits at len(text)-1;
    ISOLATED if both; otherwise MEDIAL. Harakat are transparent — they do not
    interrupt letter adjacency.

    This selection rule is the canonical sequence-position derivation; it
    introduces no new evidence claims (the four canonical position rules in
    src/qiyas_core/rules/position_rules.py remain the sole authority).
    """

    def _prev_letter_or_boundary(j: int) -> str:
        k = j - 1
        while k >= 0 and is_arabic_haraka(ord(text[k])):
            k -= 1
        if k < 0:
            return "boundary"
        cp = ord(text[k])
        if is_arabic_letter(cp):
            return "letter"
        return "boundary"

    def _next_letter_or_boundary(j: int) -> str:
        k = j + 1
        while k < len(text) and is_arabic_haraka(ord(text[k])):
            k += 1
        if k >= len(text):
            return "boundary"
        cp = ord(text[k])
        if is_arabic_letter(cp):
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


def _accepted(cs: CandidateSet) -> Candidate | None:
    accepted = cs.accepted
    return accepted[0] if accepted else None


# ---------------------------------------------------------------------------
# 3. Driver — walk every character through every applicable layer
# ---------------------------------------------------------------------------


def process_text(text: str, layers: PipelineLayers | None = None) -> list[CharacterReport]:
    layers = layers or PipelineLayers.build()
    reports: list[CharacterReport] = []

    # Pre-classify every character so the SlotQiyas composition can look ahead.
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
        report = CharacterReport(index=i, char=ch, codepoint=cp, steps=[])

        u_set = layers.unicode_layer.process_codepoint(cp, trace_prefix=f"text[{i}]:u:{cp:04x}")
        report.steps.append(LayerStep.from_set("UnicodeQiyas", u_set))

        u_cand = _accepted(u_set)
        if u_cand is None:
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
            li_set = layers.letter_identity_layer.prove_letter_identity(
                t_cand, trace_prefix=f"text[{i}]:li:{cp:04x}"
            )
            report.steps.append(LayerStep.from_set("LetterIdentityQiyas", li_set))
            li_cand = _accepted(li_set)

            # PositionQiyas with sequence-derived position type
            ptype = _classify_position(text, i)
            p_set = layers.position_layer.prove_position(
                t_cand,
                position_type=ptype,
                index=i,
                within_word=True,
                at_boundary=(ptype in (POSITION_INITIAL, POSITION_FINAL, POSITION_ISOLATED)),
                trace_prefix=f"text[{i}]:p:{cp:04x}",
            )
            report.steps.append(LayerStep.from_set(f"PositionQiyas[{ptype}]", p_set))
            p_cand = _accepted(p_set)

            # ConditionedTypedSequence + SlotQiyas (PR #27 wiring).
            # Per CLAUDE.md §8 the SlotCandidate now consumes an explicit
            # AlignmentEvidence / CarrierBindingCandidate from the CTS
            # layer; the driver does NOT self-assert any alignment.
            if (
                li_cand is not None
                and p_cand is not None
                and i + 1 < len(text)
                and classifications[i + 1][0] == "HarakaCodePoint"
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

        elif ctype == "HarakaCodePoint":
            hf_set = layers.haraka_function_layer.prove_haraka_function(
                t_cand, trace_prefix=f"text[{i}]:hf:{cp:04x}"
            )
            report.steps.append(LayerStep.from_set("HarakaFunctionQiyas", hf_set))

        else:
            # BoundaryCodePoint / PunctuationCodePoint / ResidualCodePoint:
            # the contract defines no further canonical layer for these — stop here.
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
