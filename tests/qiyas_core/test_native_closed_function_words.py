"""Tests for the Qiyas-native, snapshot-independent, inventory-gated closed-function-word
path (NativeClosedFunctionWordQiyas → P5.1 MabniReadiness).

Curated EXACT-surface inventory: بِ / كَ / وَ / لِ / مِن / مِنْ.
Native acceptance must NOT depend on the Hussein snapshot and must NOT confer tool/word
status on arbitrary vocalised letters (ضَ / صَ / ظُ).
"""

from __future__ import annotations

import dataclasses

import run_qiyas as rq
from qiyas_core.native_closed_function_word_provider import (
    NativeClosedFunctionWordProvider,
)

NATIVE = "qiyas_native_closed_function_word"
LISTED = ("بِ", "كَ", "وَ", "لِ", "مِن", "مِنْ")


class _SnapshotOff:
    """Disables ALL Hussein snapshot consumption → native-only behaviour."""

    def get_p5_1_proposal(self, surface):
        return None

    def p5_1_classify_kwargs(self, surface):
        return {}

    def closed_category_reachability(self, surface):
        return None


def _layers(snapshot: bool):
    base = rq.PipelineLayers.build()
    if snapshot:
        return base
    return dataclasses.replace(
        base, inflectional_closure_snapshot_provider=_SnapshotOff()
    )


def _steps(token, snapshot: bool = True):
    return [s for r in rq.process_text(token, layers=_layers(snapshot)) for s in r.steps]


def _p5_1(token, snapshot: bool = True):
    for s in _steps(token, snapshot):
        if s.layer == "InflectionalClosureQiyas":
            return s
    return None


def _has_marker(steps, needle):
    return any(
        needle in t for s in steps for t in (getattr(s, "trace_ids", ()) or ())
    )


# ── A. positive, snapshot OFF ────────────────────────────────────────────────


def test_NCFW_A01_listed_tools_accepted_native_snapshot_off():
    for tok in LISTED:
        s = _p5_1(tok, snapshot=False)
        assert s is not None and s.status == "accepted", tok
        assert s.candidate_type == "MabniReadinessCandidate", tok


def test_NCFW_A02_native_source_and_no_hussein_marker_snapshot_off():
    for tok in LISTED:
        steps = _steps(tok, snapshot=False)
        assert _has_marker(steps, NATIVE), tok
        assert not _has_marker(steps, "hussein_snapshot_v1"), tok


def test_NCFW_A03_native_carrier_layer_present_snapshot_off():
    # single-letter / non-MufradWord tools reach P5.1 via the native carrier bridge
    for tok in ("بِ", "كَ", "وَ", "لِ", "مِن"):
        layers = [s.layer for s in _steps(tok, snapshot=False)]
        assert "NativeClosedFunctionWordQiyas" in layers, tok


# ── B. positive, snapshot ON ─────────────────────────────────────────────────


def test_NCFW_B01_listed_tools_accepted_native_snapshot_on():
    for tok in LISTED:
        s = _p5_1(tok, snapshot=True)
        assert s is not None and s.status == "accepted", tok
        assert s.candidate_type == "MabniReadinessCandidate", tok


def test_NCFW_B02_native_wins_over_snapshot_for_min():
    # مِن exists in the v1 snapshot as HARF, but the native inventory takes precedence.
    steps = _steps("مِن", snapshot=True)
    assert _has_marker(steps, NATIVE)
    assert not _has_marker(steps, "hussein_snapshot_v1")


def test_NCFW_B03_behaviour_identical_on_and_off():
    for tok in LISTED:
        on = _p5_1(tok, snapshot=True)
        off = _p5_1(tok, snapshot=False)
        assert on.status == off.status == "accepted", tok
        assert on.candidate_type == off.candidate_type == "MabniReadinessCandidate", tok


# ── C. negatives ─────────────────────────────────────────────────────────────


def test_NCFW_C01_arbitrary_vocalised_letters_not_accepted():
    # shape-based acceptance is forbidden: ضَ / صَ / ظُ are NOT closed tools.
    for tok in ("ضَ", "صَ", "ظُ"):
        s = _p5_1(tok, snapshot=False)
        assert s is None, tok  # never reaches P5.1 natively
        assert "NativeClosedFunctionWordQiyas" not in [
            x.layer for x in _steps(tok, snapshot=False)
        ], tok


def test_NCFW_C02_man_remains_not_accepted():
    for tok in ("مَن", "من"):
        s = _p5_1(tok, snapshot=False)
        assert s is None or s.status != "accepted", tok
        assert not _has_marker(_steps(tok, snapshot=False), NATIVE), tok


def test_NCFW_C03_ala_unchanged():
    # عَلَى (vocalised) stays deferred; على keeps its existing snapshot-only behaviour.
    assert _p5_1("عَلَى", snapshot=False).status == "deferred"
    assert _p5_1("عَلَى", snapshot=True).status == "deferred"
    assert not _has_marker(_steps("عَلَى", snapshot=True), NATIVE)
    # على: accepted via snapshot ON, not reached OFF — native adds nothing.
    assert not _has_marker(_steps("على", snapshot=True), NATIVE)
    assert _p5_1("على", snapshot=False) is None


def test_NCFW_C04_idha_remains_deferred():
    assert _p5_1("إِذَا", snapshot=False).status == "deferred"
    assert not _has_marker(_steps("إِذَا", snapshot=False), NATIVE)


def test_NCFW_C05_biman_one_token_not_decomposed():
    steps = _steps("بِمَن", snapshot=False)
    # بِمَن is processed as ONE token: it is not in the inventory, so no native carrier,
    # and it must not be split into بِ + مَن native acceptances.
    assert "NativeClosedFunctionWordQiyas" not in [s.layer for s in steps]
    assert not _has_marker(steps, NATIVE)
    s = _p5_1("بِمَن", snapshot=False)
    assert s is not None and s.status == "deferred"


# ── D. safety / invariants ───────────────────────────────────────────────────


def test_NCFW_D01_no_root_wazn_into_p5_1():
    prov = NativeClosedFunctionWordProvider()
    for tok in LISTED:
        kwargs = prov.p5_1_classify_kwargs(tok)
        assert set(kwargs) <= {"closed_category"}, tok
        assert "root" not in str(kwargs) and "wazn" not in str(kwargs), tok


def test_NCFW_D02_no_final_meaning_irab_relation_leak():
    forbidden = ("FinalMeaning", "HukmCandidate", "RealityClaim", "Irab",
                 "MeaningCandidate", "DalalahCandidate", "RelationGeometry",
                 "SentenceGeometry", "CaseJudgment")
    for tok in LISTED:
        for s in _steps(tok, snapshot=False):
            blob = s.candidate_type + " " + " ".join(getattr(s, "trace_ids", ()) or ())
            for f in forbidden:
                assert f not in blob, (tok, f)


def test_NCFW_D03_registry_19_no_p13_p12_terminal():
    from qiyas_core.slot_geometry_core import master_registry_seed as MRS
    layers = list(MRS.build_master_registry_seed().all_layers())
    assert len(layers) == 19
    assert not any("P13" in n for n in dir(MRS) if n.startswith("LAYER_ID_"))


# ── E. provider unit-level (exact-surface gate) ──────────────────────────────


def test_NCFW_E01_exact_surface_only():
    prov = NativeClosedFunctionWordProvider()
    for tok in LISTED:
        assert prov.is_listed(tok), tok
    # bare / variant / non-listed surfaces are NOT listed (no fuzzy/normalised matching)
    for tok in ("من", "مَن", "ب", "ك", "و", "ل", "على", "عَلَى", "ضَ", "إِذَا", None, ""):
        assert not prov.is_listed(tok), tok


def test_NCFW_E02_reachability_none_for_unlisted():
    prov = NativeClosedFunctionWordProvider()
    assert prov.native_closed_category_reachability("ضَ") is None
    assert prov.native_closed_category_reachability("من") is None
    cs, kwargs = prov.native_closed_category_reachability("بِ")
    assert kwargs == {"closed_category": "harf"}
    assert cs.candidates[0].candidate_type == "NativeClosedFunctionWordCarrier"
