"""Qiyas-NATIVE, snapshot-independent, inventory-gated closed-function-word path.

`NativeClosedFunctionWordProvider` supplies P5.1-safe closed-category evidence for a
small, curated, **exact-surface** inventory of closed function words (ḥarf / tool), so
listed tools reach **mabni-readiness** WITHOUT any Hussein snapshot, analyzer, subprocess,
or Stage A read. It is the native counterpart of the snapshot C2 bridge.

CONSTITUTIONAL CONTRACT (NativeClosedFunctionWordQiyas — auxiliary, NON-registry):
  - Asl:    this curated in-repo closed-function-word inventory.
  - Far:    the exact written token (e.g. بِ / كَ / وَ / لِ / مِن / مِنْ).
  - Illah:  closed functional tool — non-declinable, non-derived.
  - Wasf:   a LISTED closed particle with fixed surface behaviour.
  - Fariq:  not a lexical noun / verb / open-class stem / arbitrary CV-CVC token;
            no final meaning, no i'rab, no relation.
  - Evidence: this internal inventory ONLY — never the Hussein snapshot.
  - Rank:   FORMAL_STRUCTURE.
  - IdentityPreservation: the exact written surface identity is preserved.
  - Residual: an UNLISTED / ambiguous / un-normalised surface yields NO proposal, so the
            caller DEFERs (never guesses). Conceptual residual codes: unknown_tool,
            ambiguous_tool, diacritic_variant_unlicensed, normalization_required.

STRICT: EXACT surfaces only. No harakat-stripping, no fuzzy/normalised matching. Word/tool
status is conferred by IDENTITY (membership in this inventory), never by CV/CVC shape — so
arbitrary vocalised letters (ضَ / صَ / ظُ) are never accepted.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank

NATIVE_SOURCE = "qiyas_native_closed_function_word"
_LAYER = "NativeClosedFunctionWordQiyas"

# Curated EXACT-surface inventory. Key = exact vocalized written surface (NFC).
# value = (closed_category, tool_kind). closed_category is fed to the P5.1 rule, which
# maps "harf" → MABNI_CLOSED_PARTICLE → MabniReadinessCandidate. tool_kind is trace-only.
_NATIVE_CLOSED_FUNCTION_WORDS: dict[str, tuple[str, str]] = {
    "بِ": ("harf", "preposition_proclitic"),
    "كَ": ("harf", "simile_proclitic"),
    "وَ": ("harf", "conjunction_proclitic"),
    "لِ": ("harf", "preposition_purpose_proclitic"),
    "مِن": ("harf", "preposition"),
    "مِنْ": ("harf", "preposition"),
}


@dataclass(frozen=True)
class NativeClosedFunctionWordProvider:
    """Inventory-gated native provider of P5.1 closed-category hints (no Hussein)."""

    inventory: dict[str, tuple[str, str]] = field(
        default_factory=lambda: dict(_NATIVE_CLOSED_FUNCTION_WORDS)
    )

    # ── exact-surface gate ────────────────────────────────────────────────────
    def is_listed(self, surface: str | None) -> bool:
        """True iff `surface` is an EXACT listed closed-function-word surface."""
        return bool(surface) and surface in self.inventory

    # ── P5.1 call-site hint (for listed surfaces that DO form a MufradWord) ────
    def p5_1_classify_kwargs(self, surface: str | None) -> dict:
        """Safe kwargs for InflectionalClosureLayerAdapter.classify, or {} if unlisted.

        Guaranteed to contain ONLY `closed_category` — never root/wazn/role/relation."""
        if not self.is_listed(surface):
            return {}
        closed_category, _kind = self.inventory[surface]
        return {"closed_category": closed_category}

    # ── reachability bridge (for listed surfaces that do NOT form a MufradWord) ─
    def native_closed_category_reachability(self, surface: str | None):
        """For a LISTED closed-function-word that does not form an accepted P5
        MufradWord (e.g. a single-letter proclitic بِ/كَ/وَ/لِ or مِن), synthesize a
        narrow accepted NativeClosedFunctionWordCarrier so P5.1 can fire — returning
        ``(carrier_set, classify_kwargs)``. Returns None for any unlisted surface.

        STRUCTURAL ONLY: the carrier carries the unit's preserved codepoint identity and
        NO lexical meaning, root, wazn, i'rab, role, relation, or final judgment."""
        if not self.is_listed(surface):
            return None
        closed_category, kind = self.inventory[surface]
        return self._carrier_set(surface, kind), {"closed_category": closed_category}

    def _carrier_set(self, surface: str, kind: str) -> CandidateSet:
        ids = tuple(f"identity:codepoint:{ord(c):04x}" for c in surface
                    if 0x0621 <= ord(c) <= 0x064A) or ("identity:closed_function_word_unit",)
        carrier = Candidate(
            candidate_id=f"accepted:{_LAYER}:{surface}",
            candidate_type="NativeClosedFunctionWordCarrier",
            status=CandidateStatus.ACCEPTED,
            layer=_LAYER,
            source_rule_id="native_closed_function_word.bridge",
            asl_id="اصل:native_closed_function_word_inventory",
            far_id=f"فرع:closed_function_word:{surface}",
            identity_ids=ids,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            residuals=(),
            trace_ids=(
                f"native_closed_function_word_evidence:source={NATIVE_SOURCE};"
                f"kind={kind};inventory_gated;structural_only",
                f"src={NATIVE_SOURCE}",
            ),
            output_flags=frozenset({"CandidateOnly"}),
        )
        return CandidateSet(
            set_id=f"ncfw:{surface}",
            layer=_LAYER,
            candidates=(carrier,),
            residuals=(),
            trace_ids=(),
        )
