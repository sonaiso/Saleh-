"""Narrow runtime provider: committed v1 Hussein snapshot → P5.1 proposal evidence.

Reads ONLY the committed static snapshot
``data/external_snapshots/hussein_legacy_proposals/v1/`` (CSV + manifest.json) and
supplies closed-category / verb-kind readiness hints to the P5.1 InflectionalClosure
adapter. It is the runtime realization of Step C of LEGACY_PROPOSAL_SNAPSHOT_CONTRACT.md.

CONSTITUTIONAL CONTRACT (enforced here):
  - Reads the committed snapshot ONLY (a path under ``data/external_snapshots/``). It
    REFUSES any other path, so the capture-only Stage A data is never read. No
    subprocess, no Hussein-analyzer call — this module imports neither.
  - P5.1 ONLY. It never supplies root/wazn (those belong to a future P3.1 provider) and
    never supplies role/case/i'rab/relation/event/meaning/Q&A/tafsir.
  - The snapshot is a PROPOSER, never an authority: the P5.1 Qiyas rule decides
    ACCEPT/DEFER/BLOCK. The provider only hands over safe hints.
  - Consumable iff: review_status == manually_reviewed AND allowed_feed_targets includes
    P5_1_INFLECTIONAL_CLOSURE AND reliability_tag != suspicious_defer. Otherwise it
    returns no proposal (the P5.1 rule then DEFERs — never guesses). quarantined /
    rejected / pending rows are never consumed. The unsafe i'rab/role field is never in
    the evidence (it lives only in the snapshot's ignored_fields_summary).
"""

from __future__ import annotations

import csv
import json
import pathlib
from dataclasses import dataclass, field

P5_TARGET = "P5_1_INFLECTIONAL_CLOSURE"
PROPOSAL_SOURCE = "hussein_snapshot_v1"

# Closed functional/pronominal compounds the legacy reports as HARF+enclitic.
_CLOSED_COMPOUND_SURFACES = {"عليه", "منه", "بكم", "فيه", "به", "له", "منهم", "عليهم", "بهم"}
# Detached-pronoun surfaces (legacy ISM_MABNI gives no finer sub-type).
_PRONOUN_SURFACES = {"هو", "هي", "هم", "هن", "أنا", "أنت", "أنتم", "نحن", "هما", "أنتِ", "هُوَ"}


def _default_snapshot_dir() -> pathlib.Path:
    # src/qiyas_core/<this>.py  →  repo root is parents[2]
    return (pathlib.Path(__file__).resolve().parents[2]
            / "data" / "external_snapshots" / "hussein_legacy_proposals" / "v1")


@dataclass(frozen=True)
class P5_1SnapshotProposal:
    """A narrow P5.1 proposal carrying ONLY closed-category / verb-kind readiness hints."""
    proposal_source: str
    snapshot_version: str
    source_text_id: str
    token_index: str
    surface_form_vocalized: str
    normalized_surface_nfc: str
    legacy_class: str
    legacy_subclass: str
    legacy_verb_kind: str
    legacy_verb_tense: str
    reliability_tag: str
    certainty_class: str
    unsafe_final_looking: str
    p5_1_evidence_kind: str
    p5_1_candidate_hint: str          # "mabni" | "murab"
    ignored_fields_summary: str
    # The exact kwargs handed to InflectionalClosureLayerAdapter.classify — NO root/wazn,
    # NO role/case/relation/event/meaning.
    classify_kwargs: dict = field(default_factory=dict)


def _map_class_to_p5_1(row) -> tuple[dict, str, str] | None:
    """Map a snapshot row to (classify_kwargs, evidence_kind, candidate_hint).

    Returns None when the class is outside the P5.1-safe closed-category / verb-kind
    scope. Never reads root/wazn."""
    cls = row["legacy_class"]
    surface = row["surface_form_vocalized"]
    tense = row["legacy_verb_tense"]
    if cls == "HARF":
        if surface in _CLOSED_COMPOUND_SURFACES:
            return {"is_closed_compound": True}, "closed_functional_compound", "mabni"
        return {"closed_category": "harf"}, "closed_functional_particle", "mabni"
    if cls == "ISM_MAWSOOL":
        return {"closed_category": "relative"}, "relative_noun", "mabni"
    if cls == "ISM_MABNI":
        if surface in _PRONOUN_SURFACES:
            return {"closed_category": "pronoun"}, "pronoun", "mabni"
        return {"closed_category": "demonstrative"}, "demonstrative_or_mabni_noun", "mabni"
    if cls == "FIIL":
        if tense in ("past", "imperative"):
            return ({"word_kind": "verbal", "verb_tense": tense},
                    f"{tense}_verb", "mabni")
        if tense == "present":
            return ({"word_kind": "verbal", "verb_tense": "present"},
                    "present_verb_open", "murab")
        return None
    if cls in ("ISM_MUARAB", "JAMID"):
        return {"word_kind": "nominal"}, "open_declinable_nominal", "murab"
    return None


class HusseinSnapshotProvider:
    """Loads the committed v1 snapshot and serves P5.1 proposals (fixture-free / analyzer-free)."""

    def __init__(self, snapshot_dir: pathlib.Path | None = None):
        self._dir = pathlib.Path(snapshot_dir) if snapshot_dir else _default_snapshot_dir()
        # Allowlist guard: this provider may read ONLY a committed external-snapshot path,
        # so the capture-only Stage A data can never be read through it.
        if "external_snapshots" not in str(self._dir).replace("\\", "/"):
            raise ValueError("snapshot provider may read only a committed external_snapshots path")
        self._by_surface: dict[str, P5_1SnapshotProposal] = {}
        self._loaded = False

    # ── loading ────────────────────────────────────────────────────────────
    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        manifest = json.loads((self._dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest.get("snapshot_version") == "v1", "provider requires snapshot v1"
        # The one invariant that must hold: Stage A is never read at runtime.
        assert manifest.get("stage_a_read_at_runtime") is False, \
            "manifest must attest Stage A is not read at runtime"
        csv_path = self._dir / manifest["snapshot_file"]
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                prop = self._row_to_proposal(row)
                if prop is None:
                    continue
                self._by_surface[row["surface_form_vocalized"]] = prop
                self._by_surface[row["normalized_surface_nfc"]] = prop
        self._loaded = True

    def _row_to_proposal(self, row) -> P5_1SnapshotProposal | None:
        # Gating: only manually_reviewed, P5.1-targeted, non-suspicious rows are consumable.
        if row["review_status"] != "manually_reviewed":
            return None
        if P5_TARGET not in row["allowed_feed_targets"].split("|"):
            return None
        if row["reliability_tag"] == "suspicious_defer":
            return None  # suspicious → no evidence (P5.1 DEFERs; never ACCEPT)
        mapped = _map_class_to_p5_1(row)
        if mapped is None:
            return None
        kwargs, kind, hint = mapped
        return P5_1SnapshotProposal(
            proposal_source=PROPOSAL_SOURCE,
            snapshot_version=row["snapshot_version"],
            source_text_id=row["source_text_id"],
            token_index=row["token_index"],
            surface_form_vocalized=row["surface_form_vocalized"],
            normalized_surface_nfc=row["normalized_surface_nfc"],
            legacy_class=row["legacy_class"],
            legacy_subclass=row["legacy_subclass"],
            legacy_verb_kind=row["legacy_verb_kind"],
            legacy_verb_tense=row["legacy_verb_tense"],
            reliability_tag=row["reliability_tag"],
            certainty_class=row["certainty_class"],
            unsafe_final_looking=row["unsafe_final_looking"],
            p5_1_evidence_kind=kind,
            p5_1_candidate_hint=hint,
            ignored_fields_summary=row["ignored_fields_summary"],
            classify_kwargs=dict(kwargs),
        )

    # ── runtime query ────────────────────────────────────────────────────────
    def get_p5_1_proposal(self, surface: str | None) -> P5_1SnapshotProposal | None:
        if not surface:
            return None
        self._ensure_loaded()
        return self._by_surface.get(surface)

    def p5_1_classify_kwargs(self, surface: str | None) -> dict:
        """Safe kwargs for InflectionalClosureLayerAdapter.classify, or {} if none.

        Guaranteed to contain NO root/wazn and NO role/case/relation/event/meaning."""
        prop = self.get_p5_1_proposal(surface)
        return dict(prop.classify_kwargs) if prop else {}
