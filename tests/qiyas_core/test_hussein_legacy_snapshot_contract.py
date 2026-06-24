"""Static-file contract validation for the v1 Hussein legacy proposal snapshot.

Validates ONLY the committed data artifact under
`data/external_snapshots/hussein_legacy_proposals/v1/` against
`docs/qiyas_core/LEGACY_PROPOSAL_SNAPSHOT_CONTRACT.md`. It wires NOTHING into runtime,
imports no provider, and never reads Stage A fixtures as a runtime source.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import pathlib
import unicodedata

REPO = pathlib.Path(__file__).resolve().parents[2]
SNAP_DIR = REPO / "data" / "external_snapshots" / "hussein_legacy_proposals" / "v1"
CSV_PATH = SNAP_DIR / "hussein_legacy_proposals_v1.csv"
MANIFEST_JSON = SNAP_DIR / "manifest.json"
MANIFEST_MD = SNAP_DIR / "MANIFEST.md"

REQUIRED_COLUMNS = [
    "snapshot_version", "source_provenance", "analyzer_name", "analyzer_version_or_commit",
    "offline_run_id", "review_status", "reviewer", "reviewed_at", "source_text_id",
    "token_index", "surface_form_vocalized", "surface_form_unvocalized_key",
    "normalized_surface_nfc", "segmentation_hint", "legacy_class", "legacy_subclass",
    "legacy_verb_kind", "legacy_verb_tense", "legacy_root", "legacy_wazn",
    "morphology_ambiguity_tags", "reliability_tag", "certainty_class",
    "unsafe_final_looking", "allowed_feed_targets", "ignored_fields_summary",
    "quarantine_reason",
]
VALID_REVIEW = {"manually_reviewed", "quarantined", "rejected", "pending_review"}
P5 = "P5_1_INFLECTIONAL_CLOSURE"
P3 = "P3_1_WEIGHT_PATTERN"

# Forbidden runtime-consumable families — must NEVER be a column header.
FORBIDDEN_COLUMN_TOKENS = (
    "role", "i3rab", "irab", "case", "marfu", "mansub", "majrur", "majzum",
    "relation", "agent_of", "patient_of", "jawab", "event", "speech", "mood",
    "anaphora", "resolution", "meaning", "tafsir", "hukm", "truth", "reality",
    "final_interpretation",
)


def _rows():
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _targets(row):
    return [t for t in row["allowed_feed_targets"].split("|") if t]


def test_HS_01_snapshot_outside_stage_a_fixtures():
    assert CSV_PATH.exists(), CSV_PATH
    assert "tests/qiyas_core/legacy_fixtures" not in str(CSV_PATH).replace("\\", "/")
    assert "external_snapshots" in str(CSV_PATH).replace("\\", "/")


def test_HS_02_every_row_has_required_columns():
    with open(CSV_PATH, encoding="utf-8") as f:
        header = csv.reader(f).__next__()
    assert header == REQUIRED_COLUMNS, header
    for r in _rows():
        assert set(r.keys()) == set(REQUIRED_COLUMNS)


def test_HS_03_every_row_is_nfc_normalized():
    for r in _rows():
        for col in ("surface_form_vocalized", "surface_form_unvocalized_key",
                    "normalized_surface_nfc"):
            assert r[col] == unicodedata.normalize("NFC", r[col]), (r[col], col)
        assert r["normalized_surface_nfc"] == unicodedata.normalize(
            "NFC", r["surface_form_vocalized"])


def test_HS_04_review_status_valid():
    for r in _rows():
        assert r["review_status"] in VALID_REVIEW, r["review_status"]


def test_HS_05_only_manually_reviewed_rows_are_feed_targetable():
    for r in _rows():
        if r["review_status"] != "manually_reviewed":
            assert _targets(r) == [], (r["surface_form_vocalized"], r["review_status"])
        # targets, when present, are only the two known feed tags
        assert set(_targets(r)) <= {P5, P3}


def test_HS_06_p5_1_does_not_consume_root_or_wazn():
    m = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    cols = m["consumable_columns_by_target"][P5]
    assert "legacy_root" not in cols and "legacy_wazn" not in cols
    assert "morphology_ambiguity_tags" not in cols


def test_HS_07_p3_1_does_not_consume_class_or_word_kind():
    m = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    cols = m["consumable_columns_by_target"][P3]
    for forbidden in ("legacy_class", "legacy_subclass", "legacy_verb_kind",
                      "legacy_verb_tense"):
        assert forbidden not in cols, forbidden
    # legacy_root present ONLY as audit metadata, never an identity-rewrite field
    assert "legacy_root" in cols and m["legacy_root_is_audit_metadata_only"] is True


def test_HS_08_suspicious_and_unsafe_never_imply_accept():
    # The snapshot carries NO accept-authorizing column; ACCEPT is the Qiyas adapter's
    # decision. Verify there is no such column and that gating tags are well-formed.
    rows = _rows()
    assert not any(c for c in REQUIRED_COLUMNS if "accept" in c.lower())
    for r in rows:
        assert r["reliability_tag"] in {"proposal_evidence", "suspicious_defer"}
        assert r["unsafe_final_looking"] in {"true", "false"}
    # every row flags the (ignored) legacy i'rab as unsafe_final_looking
    assert all(r["unsafe_final_looking"] == "true" for r in rows)


def test_HS_09_forbidden_columns_absent():
    with open(CSV_PATH, encoding="utf-8") as f:
        header = [h.lower() for h in csv.reader(f).__next__()]
    for col in header:
        assert not any(tok in col for tok in FORBIDDEN_COLUMN_TOKENS), col
    # the legacy role/i'rab text is allowed ONLY inside ignored_fields_summary
    for r in _rows():
        assert "legacy_role_i3rab=" in r["ignored_fields_summary"]


def test_HS_10_manifest_exists_and_checksum_matches():
    assert MANIFEST_JSON.exists() and MANIFEST_MD.exists()
    m = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    actual = hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()
    assert m["sha256"] == actual, "manifest sha256 must match the committed CSV"
    assert m["sha256"] in MANIFEST_MD.read_text(encoding="utf-8")
    assert m["runtime_consumed"] is False and m["stage_a_read_at_runtime"] is False


def test_HS_11_snapshot_version_is_v1():
    m = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    assert m["snapshot_version"] == "v1"
    for r in _rows():
        assert r["snapshot_version"] == "v1"
        assert r["analyzer_name"] == "hussein"


def test_HS_12_no_runtime_reference_to_the_snapshot():
    # No src/qiyas_core or run_qiyas module may import/reference the snapshot path.
    targets = list((REPO / "src" / "qiyas_core").rglob("*.py")) + [REPO / "run_qiyas.py"]
    needles = ("external_snapshots", "hussein_legacy_proposals", "snapshot_contract")
    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for n in needles:
            assert n not in text, f"{path} must not reference the snapshot ({n})"
        # belt-and-braces: no import of the validation test module either
        tree = ast.parse(text)
        for node in ast.walk(tree):
            mods = ([a.name for a in node.names] if isinstance(node, ast.Import)
                    else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            assert not any("hussein_legacy_snapshot" in (mod or "") for mod in mods)


def test_HS_13_governance_registry_19_no_p13():
    from qiyas_core.slot_geometry_core import master_registry_seed as MRS
    layers = list(MRS.build_master_registry_seed().all_layers())
    assert len(layers) == 19
    assert not any("P13" in n for n in dir(MRS) if n.startswith("LAYER_ID_"))


def test_HS_14_seed_count_and_quarantine_reasons_present():
    rows = _rows()
    assert len(rows) == 26
    for r in rows:
        if r["review_status"] == "quarantined":
            assert r["quarantine_reason"], r["surface_form_vocalized"]
            assert _targets(r) == []
