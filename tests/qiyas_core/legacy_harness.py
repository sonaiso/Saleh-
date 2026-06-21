"""Stage A — legacy analyzer fixture harness (READ-ONLY, AUDIT ONLY).

This module is a TEST-SIDE harness. It is deliberately NOT under `src/qiyas_core/`
and is NEVER imported by any Qiyas runtime module (`run_qiyas`, any adapter, any
rule). It exists only to (a) load the captured RAW outputs of the external legacy
analyzer verbatim, and (b) classify each output family by *Qiyas reliability*.

CONSTITUTIONAL CONTRACT (Stage A):
  - The legacy analyzer PROPOSES; only Qiyas rules license/defer/block. This harness
    performs NO licensing — it produces NO Candidate / CandidateSet and feeds nothing
    into Qiyas. It is audit evidence only.
  - Raw outputs are preserved EXACTLY — no silent correction. The parser only EXTRACTS
    verbatim substrings; it never rewrites them (errors are preserved as-is).
  - Two modes:
      * fixture-only (default): read the committed *.raw.txt snapshots. No external
        dependency — works in CI without the legacy analyzer present.
      * subprocess (regeneration only): run the external analyzer to refresh snapshots;
        used by hand, gated on the external directory existing.

The reliability classes below are a Qiyas-side TAGGING of the legacy output (how it
must be treated downstream), not a correction of the output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os
import re
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_DIR = os.path.join(_HERE, "legacy_fixtures")
WORDS_RAW = os.path.join(FIXTURE_DIR, "words_morph_i3rab.raw.txt")
PHRASE_RAW = os.path.join(FIXTURE_DIR, "phrase_all.raw.txt")

# External legacy analyzer (regeneration mode only — never imported, never required
# at test time).
LEGACY_DIR = "/Users/husseinhiyassat/fractal/hussein/clean_code"
LEGACY_ENTRY = "analyze_verse_v3.py"

# ── Qiyas reliability classes (how a legacy output must be treated) ────────────
PROPOSAL_EVIDENCE = "proposal_evidence"          # safe candidate-only proposal
USEFUL_AMBIGUOUS = "useful_ambiguous"            # useful but ambiguous
SUSPICIOUS_DEFER = "suspicious_defer"            # suspicious → DEFER
UNSAFE_FINAL_LOOKING = "unsafe_final_looking"    # a committed final-looking judgment
QUARANTINE = "quarantine"                        # ignore / out of scope

# Output families the harness recognises in the L1–L3 word capture.
FAMILY_SEGMENTATION = "segmentation"
FAMILY_ROOT_WAZN = "root_wazn"
FAMILY_WORD_CLASS = "word_class"
FAMILY_ROLE_CASE = "role_case"

# Audit-derived per-token reliability overrides (transparent; see the audit report).
# Tokens whose root/wazn require normalization (weak/hollow/hamza/shadda/madd) → DEFER.
_DEFER_ROOT_WAZN = {"قَالَ", "بَاعَ", "خَافَ", "صَامَ", "قِيلَ", "يَبِيعُ", "مَدَّ", "آمَنَ"}
# Tokens with a KNOWN-WRONG legacy label (preserved verbatim, tagged suspicious).
_SUSPICIOUS_WORD_CLASS = {"بَاعَ", "صَامَ"}          # misclassified ISM_MUARAB, should be FIIL
_SUSPICIOUS_ROOT_WAZN = {"قِيلَ", "يَبِيعُ", "مكتوب"}  # root not normalized / unvocalized → wrong


@dataclass(frozen=True)
class LegacyAnalyzerRawOutput:
    """Raw, verbatim stdout for one captured token. No correction."""
    token: str
    raw_stdout: str


@dataclass(frozen=True)
class LegacyCapabilityRow:
    """Raw-preserving extraction + Qiyas reliability tags for one token."""
    token: str
    raw_l3_line: str | None           # the verbatim L3 line, exactly as emitted
    legacy_class: str | None          # verbatim 'class=' value
    legacy_role: str | None           # verbatim 'role=' value (may embed case)
    legacy_root: str | None           # verbatim 'root=' value
    legacy_wazn: str | None           # verbatim 'wazn=' value
    family_reliability: dict = field(default_factory=dict)
    note: str = ""


class LegacyAnalyzerProposalProvider:
    """Narrow interface over the legacy analyzer. Default = fixture-only (read raw
    snapshots). subprocess mode only for regeneration; never used by Qiyas."""

    def __init__(self, mode: str = "fixture"):
        assert mode in ("fixture", "subprocess")
        self.mode = mode

    def get(self, token: str) -> LegacyAnalyzerRawOutput:
        if self.mode == "fixture":
            for ro in load_word_fixtures():
                if ro.token == token:
                    return ro
            raise KeyError(f"no captured fixture for {token!r}")
        # subprocess (regeneration only)
        if not os.path.isdir(LEGACY_DIR):
            raise RuntimeError("legacy analyzer dir not present (regeneration mode)")
        proc = subprocess.run(
            ["python3", LEGACY_ENTRY, token, "--morph", "--i3rab"],
            cwd=LEGACY_DIR, capture_output=True, text=True,
        )
        return LegacyAnalyzerRawOutput(token=token, raw_stdout=proc.stdout)


_BLOCK_RE = re.compile(
    r"### LEGACY_FIXTURE_TOKEN: (?P<tok>.+?)\n"
    r".*?### --- RAW STDOUT \(verbatim, uncorrected\) ---\n"
    r"(?P<raw>.*?)"
    r"### END_LEGACY_FIXTURE_TOKEN: (?P=tok)\n",
    re.DOTALL,
)
# Raw-preserving L3 field extractor — EXTRACTS verbatim, never rewrites.
_L3_RE = re.compile(
    r"class=(?P<cls>\S+)\s*\|\s*role=(?P<role>[^|]+?)\s*\|\s*root=(?P<root>\S+)\s*\|\s*wazn=(?P<wazn>\S+)"
)


def load_word_fixtures() -> list[LegacyAnalyzerRawOutput]:
    """Load the committed per-token raw snapshots, verbatim (no correction)."""
    with open(WORDS_RAW, encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for m in _BLOCK_RE.finditer(text):
        out.append(LegacyAnalyzerRawOutput(token=m.group("tok"), raw_stdout=m.group("raw")))
    return out


def load_phrase_fixture() -> str:
    with open(PHRASE_RAW, encoding="utf-8") as fh:
        return fh.read()


def parse_raw_preserving(raw: LegacyAnalyzerRawOutput):
    """Extract the verbatim L3 line + fields. Returns (l3_line, cls, role, root, wazn)
    with each value exactly as the analyzer emitted it (errors included)."""
    l3_line = None
    for line in raw.raw_stdout.splitlines():
        if "class=" in line and "role=" in line:
            l3_line = line.strip()
            break
    if l3_line is None:
        return None, None, None, None, None
    m = _L3_RE.search(l3_line)
    if not m:
        return l3_line, None, None, None, None
    return (l3_line, m.group("cls"), m.group("role").strip(),
            m.group("root"), m.group("wazn"))


def classify(token: str, role: str | None) -> tuple[dict, str]:
    """Qiyas-reliability TAGS for one token's output families (not a correction)."""
    fam = {}
    notes = []
    # word_class: usually proposal evidence; known-wrong labels → suspicious.
    if token in _SUSPICIOUS_WORD_CLASS:
        fam[FAMILY_WORD_CLASS] = SUSPICIOUS_DEFER
        notes.append("legacy word-class is a known misclassification (preserved verbatim)")
    else:
        fam[FAMILY_WORD_CLASS] = PROPOSAL_EVIDENCE
    # root_wazn: proposal; normalization-needed → DEFER; known-wrong → suspicious.
    if token in _SUSPICIOUS_ROOT_WAZN:
        fam[FAMILY_ROOT_WAZN] = SUSPICIOUS_DEFER
        notes.append("legacy root/wazn looks wrong (weak/unvocalized; preserved verbatim)")
    elif token in _DEFER_ROOT_WAZN:
        fam[FAMILY_ROOT_WAZN] = SUSPICIOUS_DEFER
        notes.append("weak/hollow/hamza/shadda/madd → normalization required → DEFER")
    else:
        fam[FAMILY_ROOT_WAZN] = PROPOSAL_EVIDENCE
    # role_case: the L3 committed i'rab/case is a single decided answer → UNSAFE FINAL.
    if role and role not in ("—",):
        fam[FAMILY_ROLE_CASE] = UNSAFE_FINAL_LOOKING
        notes.append("L3 role/case is a committed i'rab decision — Qiyas must downgrade, never trust")
    return fam, "; ".join(notes)


def capability_rows() -> list[LegacyCapabilityRow]:
    rows = []
    for raw in load_word_fixtures():
        l3, cls, role, root, wazn = parse_raw_preserving(raw)
        fam, note = classify(raw.token, role)
        rows.append(LegacyCapabilityRow(
            token=raw.token, raw_l3_line=l3, legacy_class=cls, legacy_role=role,
            legacy_root=root, legacy_wazn=wazn, family_reliability=fam, note=note,
        ))
    return rows


def produces_qiyas_candidates() -> bool:
    """Stage A invariant: this harness produces NO Qiyas Candidate/CandidateSet."""
    return False
