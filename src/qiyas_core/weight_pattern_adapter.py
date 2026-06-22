"""
WeightPatternLayerAdapter — P3.1 (Arabic wazn extraction). مرشّح الوزن الصرفي.

AUXILIARY non-registry sub-pass. NOT a registered LayerSpec — the constitutional
registry count stays 19, there is no P13, and the P0–P12 spine is untouched.
Registered only in `LAYER_FORBIDDEN_OUTPUTS` via the same auxiliary pattern as
HarakaRoleSpectrumQiyas / SyllableQiyas / InflectionalClosureQiyas.

Runs AFTER an accepted P3 `RootStemCandidate` (letter/haraka/position identity + CV
syllable geometry over the six licensed patterns + stem-matter normalization) and
BEFORE WordForm / P5 MufradWordCandidate / word-kind readiness / P5.1 mabni-mu'rab /
i'rab / dalalah. It produces candidate-only `WeightPatternCandidate` evidence —
zero, one, or MANY per token (multiple licensed weights co-exist as candidates; no
final winner is forced).

CANDIDATE-ONLY / NON-FINAL: identity-preserving (I(c) preserves the P3
`root_stem_candidate` identity — surface letters are NEVER silently rewritten),
identity disjoint from trace, residual-preserving. It NEVER asserts a final root, a
final wazn, a final word kind / part of speech, a final i'rab, dalalah, ifadah,
hukm, truth, reality, or intended meaning (all forbidden outputs).
"""

from dataclasses import dataclass
import uuid

from .candidate import Candidate, CandidateSet
from .enums import EvidenceRank
from .evidence import Evidence, EvidenceSet
from .forbidden_outputs import FORBIDDEN_WEIGHT_PATTERN
from .kernel import QiyasContext, QiyasKernel, QiyasRequest
from .node import QiyasNodeRef
from .rules.weight_pattern_rules import (
    FORBIDDEN_OUTPUT_ATTEMPTED,
    IDENTITY_COLLAPSE_BLOCKED,
    VERDICT_ACCEPT,
    VERDICT_BLOCK,
    VERDICT_DEFER,
    WEIGHT_PATTERN_RULE,
    align_weight_patterns,
)

# Trace prefixes for the carried structural fields (read back by tests/tools).
ROOT_STEM_REF_PREFIX = "root_stem_ref:"
TOKEN_SURFACE_PREFIX = "token_surface:"
NORMALIZED_SURFACE_PREFIX = "normalized_surface:"
SYLLABLE_PROFILE_PREFIX = "syllable_profile:"
STEM_MATTER_PREFIX = "stem_matter:"
CANDIDATE_WEIGHT_PATTERN_PREFIX = "candidate_weight_pattern:"
ROOT_SLOT_ALIGNMENT_PREFIX = "root_slot_alignment:"
ADDED_LETTER_ALIGNMENT_PREFIX = "added_letter_alignment:"
WEIGHT_PATTERN_EVIDENCE_PREFIX = "weight_pattern_evidence:"
AMBIGUITY_EVIDENCE_PREFIX = "ambiguity_evidence:"

_FORBIDDEN_EVIDENCE_TOKENS = frozenset(FORBIDDEN_WEIGHT_PATTERN)


def _surface_from_identity(candidate: Candidate) -> str:
    cps = [
        iid[len("identity:codepoint:"):]
        for iid in candidate.identity_ids
        if iid.startswith("identity:codepoint:")
    ]
    out = []
    for h in cps:
        try:
            out.append(chr(int(h, 16)))
        except ValueError:
            pass
    return "".join(out)


def _read_marker(candidate: Candidate, prefix: str):
    for t in candidate.trace_ids:
        if t.startswith(prefix):
            return t[len(prefix):]
    return None


@dataclass
class WeightPatternLayerAdapter:
    """Adapter extracting candidate-only wazn(s) from a P3 RootStemCandidate."""

    kernel: QiyasKernel

    def _build_request(
        self, root_stem, surface, syllable_profile, normalized_surface,
        verdict, reason, spec, flags, trace_prefix,
    ) -> QiyasRequest:
        preserved_ids: tuple = (
            tuple(dict.fromkeys(root_stem.identity_ids))
            if root_stem is not None else tuple()
        )
        rs_ref = root_stem.candidate_id if root_stem is not None else "none"

        asl = QiyasNodeRef(
            node_id="اصل:weight_pattern_domain",
            node_type="WeightPatternDomain",
            identity_ids=("identity:weight_pattern_domain",),
            trace_ids=(f"{trace_prefix}:asl",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )
        # The accepted P3 root/stem rides on the far node — preserves its identity.
        far = QiyasNodeRef(
            node_id=f"فرع:root_stem:{uuid.uuid4().hex[:8]}",
            node_type="RootStemCandidate",
            identity_ids=preserved_ids,
            trace_ids=(f"{trace_prefix}:far",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
        )

        proves = [
            "اصل:established",
            "فرع:determined",
            "وصف:has_root_stem_ref:evidenced",
            "وصف:has_surface_evidence:evidenced",
            "وصف:has_syllable_profile:evidenced",
            "وصف:weight_pattern_alignment_evidenced:evidenced",
            "وصف:upstream_identity_preserved:evidenced",
            "علة:belongs_to_weight_pattern_domain:verified",
            "علة:weight_pattern_extraction_licensed:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
        ]
        if verdict == VERDICT_ACCEPT:
            proves.append("وصف:weight_pattern_consistent:evidenced")
        elif verdict == VERDICT_DEFER:
            proves.append(f"defer:{reason}:present")
        else:  # VERDICT_BLOCK
            proves.append(f"فارق:{reason}:present")

        pat = spec["candidate_weight_pattern"] if spec else "none"
        root_align = spec["root_slot_alignment"] if spec else "none"
        added_align = spec["added_letter_alignment"] if spec else "none"
        amb = ";".join(f"{k}={int(bool(v))}" for k, v in flags.items())
        carried_trace = [
            f"{ROOT_STEM_REF_PREFIX}{rs_ref}",
            f"{TOKEN_SURFACE_PREFIX}{surface or '—'}",
            f"{NORMALIZED_SURFACE_PREFIX}{normalized_surface or surface or '—'}",
            f"{SYLLABLE_PROFILE_PREFIX}{syllable_profile or 'unknown'}",
            f"{CANDIDATE_WEIGHT_PATTERN_PREFIX}{pat}",
            f"{ROOT_SLOT_ALIGNMENT_PREFIX}{root_align}",
            f"{ADDED_LETTER_ALIGNMENT_PREFIX}{added_align}",
            f"{AMBIGUITY_EVIDENCE_PREFIX}{amb}",
            f"{WEIGHT_PATTERN_EVIDENCE_PREFIX}"
            f"pattern={pat};verdict={verdict};reason={reason}",
        ]

        evidence = EvidenceSet(
            items=(
                Evidence(
                    evidence_id=f"ev:weight_pattern:{uuid.uuid4().hex[:8]}",
                    source_layer="WeightPatternQiyas",
                    proves=tuple(proves),
                    rank=EvidenceRank.FORMAL_STRUCTURE,
                    trace_ids=(f"{trace_prefix}:ev",) + tuple(carried_trace),
                ),
            )
        )
        return QiyasRequest(
            rule=WEIGHT_PATTERN_RULE,
            asl=asl,
            far=far,
            evidence=evidence,
            context=QiyasContext(layer="WeightPatternQiyas"),
        )

    def extract(
        self,
        root_stem: Candidate | None,
        *,
        surface: str | None = None,
        syllable_profile: str | None = None,
        normalized_surface: str | None = None,
        external_root_letters=None,
        trace_prefix: str = "",
    ) -> CandidateSet:
        """Extract candidate-only wazn(s) from a single accepted P3 RootStemCandidate.

        Emits zero/one/many WeightPatternCandidate(s): ACCEPT exact alignment(s),
        DEFER on shadda/madd/hamza/weak/ambiguous segmentation (never guessed), BLOCK
        when no licensed alignment exists or identity is violated. Surface letters are
        never rewritten; identity is preserved.
        """
        if not trace_prefix:
            trace_prefix = "weight_pattern"
        if surface is None and root_stem is not None:
            surface = _surface_from_identity(root_stem)
        if syllable_profile is None and root_stem is not None:
            sig = _read_marker(root_stem, "root_pattern_evidence:")
            if sig and "cv=" in sig:
                syllable_profile = sig.split("cv=", 1)[1].split(";", 1)[0]

        has_identity = root_stem is not None and bool(root_stem.identity_ids)
        forbidden_attempted = root_stem is not None and any(
            any(tok in t for tok in _FORBIDDEN_EVIDENCE_TOKENS)
            for t in root_stem.trace_ids
        )

        # Identity / forbidden guards take precedence (override the aligner).
        if forbidden_attempted:
            verdict, specs, reason, flags = (
                VERDICT_BLOCK, [], FORBIDDEN_OUTPUT_ATTEMPTED,
                {"weak_letter": False, "shadda": False, "hamza": False,
                 "madd": False, "deletion_or_assimilation": False},
            )
        elif not has_identity:
            verdict, specs, reason, flags = (
                VERDICT_BLOCK, [], IDENTITY_COLLAPSE_BLOCKED,
                {"weak_letter": False, "shadda": False, "hamza": False,
                 "madd": False, "deletion_or_assimilation": False},
            )
        else:
            verdict, specs, reason, flags = align_weight_patterns(
                surface or "", external_root_letters=external_root_letters
            )

        requests = []
        if specs:
            for spec in specs:
                requests.append(self._build_request(
                    root_stem, surface, syllable_profile, normalized_surface,
                    verdict, spec.get("reason", reason), spec, flags, trace_prefix,
                ))
        else:
            requests.append(self._build_request(
                root_stem, surface, syllable_profile, normalized_surface,
                verdict, reason, None, flags, trace_prefix,
            ))

        # Apply each request and MERGE into a single CandidateSet (multiple licensed
        # weights remain candidates — no final winner is forced).
        results = [self.kernel.apply(r) for r in requests]
        candidates = tuple(c for s in results for c in s.candidates)
        residuals = tuple(r for s in results for r in s.residuals)
        trace_ids = tuple(dict.fromkeys(t for s in results for t in s.trace_ids))
        return CandidateSet(
            set_id=f"weight_pattern_set:{uuid.uuid4().hex[:8]}",
            layer="WeightPatternQiyas",
            candidates=candidates,
            residuals=residuals,
            trace_ids=trace_ids,
        )
