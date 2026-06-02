"""
SequenceContextTokenizer — Z2 Pre-Qiyas Component
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterator


class MarkerType(Enum):
    WHITESPACE_BOUNDARY        = "whitespace_boundary_marker"
    PUNCTUATION_BOUNDARY       = "punctuation_boundary_marker"
    NON_BOUNDARY_ARABIC_SYMBOL = "non_boundary_arabic_symbol"
    RESIDUAL_PRESERVATION      = "residual_preservation_marker"


@dataclass(frozen=True)
class SequenceMarker:
    index: int
    raw_char: str
    marker_type: MarkerType
    normalized_label: str | None = None
    segment_id: int | None = None
    reason: str | None = None


@dataclass(frozen=True)
class TokenizedSequence:
    source: str
    markers: tuple

    def by_type(self, marker_type):
        return tuple(m for m in self.markers if m.marker_type == marker_type)

    def boundary_markers(self):
        bt = {MarkerType.WHITESPACE_BOUNDARY, MarkerType.PUNCTUATION_BOUNDARY}
        return tuple(m for m in self.markers if m.marker_type in bt)


_ARABIC_LETTERS = frozenset([chr(c) for c in range(0x621, 0x64B)] + [chr(0x670)])
_ARABIC_DIACRITICS = frozenset([chr(c) for c in range(0x64B, 0x656)] + [chr(0x670)])
_ARABIC_PUNCTUATION = frozenset([
    chr(0x60C), chr(0x61B), chr(0x61F), chr(0x6D4),
    "!", ".", ":", ",", ";", "?", "(", ")", "[", "]",
    chr(0xAB), chr(0xBB), chr(0x2014), chr(0x2013),
])
_ARABIC_NON_BOUNDARY = _ARABIC_LETTERS | _ARABIC_DIACRITICS | frozenset([chr(0x640)])


def _classify_char(char):
    if char.isspace():
        return MarkerType.WHITESPACE_BOUNDARY
    if char in _ARABIC_PUNCTUATION:
        return MarkerType.PUNCTUATION_BOUNDARY
    if char in _ARABIC_NON_BOUNDARY:
        return MarkerType.NON_BOUNDARY_ARABIC_SYMBOL
    return MarkerType.RESIDUAL_PRESERVATION


def _normalized_label(char, mt):
    if mt == MarkerType.WHITESPACE_BOUNDARY:
        return "whitespace"
    if mt == MarkerType.PUNCTUATION_BOUNDARY:
        return f"punctuation:U+{ord(char):04X}"
    if mt == MarkerType.NON_BOUNDARY_ARABIC_SYMBOL:
        return f"arabic:U+{ord(char):04X}"
    return f"residual:U+{ord(char):04X}"


def _reason(char, mt):
    if mt == MarkerType.RESIDUAL_PRESERVATION:
        return f"symbol U+{ord(char):04X} not in arabic_letters, diacritics, or punctuation"
    return None


def _assign_segments(markers):
    bt = {MarkerType.WHITESPACE_BOUNDARY, MarkerType.PUNCTUATION_BOUNDARY}
    segment_id = 0
    result = []
    for m in markers:
        result.append(SequenceMarker(
            index=m.index, raw_char=m.raw_char, marker_type=m.marker_type,
            normalized_label=m.normalized_label, segment_id=segment_id, reason=m.reason,
        ))
        if m.marker_type in bt:
            segment_id += 1
    return result


class SequenceContextTokenizer:
    def tokenize(self, source: str) -> TokenizedSequence:
        if not source:
            return TokenizedSequence(source=source, markers=())
        raw = list(self._scan(source))
        segmented = _assign_segments(raw)
        return TokenizedSequence(source=source, markers=tuple(segmented))

    def tokenize_symbols(self, symbols):
        return self.tokenize("".join(symbols))

    def _scan(self, source):
        for index, char in enumerate(source):
            mt = _classify_char(char)
            yield SequenceMarker(
                index=index, raw_char=char, marker_type=mt,
                normalized_label=_normalized_label(char, mt),
                segment_id=None, reason=_reason(char, mt),
            )
