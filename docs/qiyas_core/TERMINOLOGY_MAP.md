# TERMINOLOGY_MAP — Public Algebraic Vocabulary

> **Status:** Constitutional reference. This document fixes the public
> implementation vocabulary of `qiyas_core` for citation in the paper and in
> any external documentation. The Arabic claim prefixes used internally for
> proof provenance are *not* translated; they are part of the proof-relevant
> structure of licensed equality and must appear verbatim in evidence sets.

---

## 1. Policy

We normalize the **public implementation vocabulary** into English algebraic
labels while **preserving Arabic claim prefixes** for proof provenance. Thus:

- Evidence ranks are exposed as English type constants:
  `NO_EVIDENCE`, `FORMAL_STRUCTURE`, `ANALOGICAL`, `DIRECT_HEARING`,
  `INDIVIDUAL_REPORT`, `MASS_TRANSMISSION`.
- Six-gate (وادي) validity is exposed as English gate constants:
  `CAUSE`, `CONDITION`, `OBSTACLE`, `VALIDITY`, `CORRUPTION`, `NULLITY`.
- Proof claims retain their internal jurisprudential structure through
  Arabic prefixes:
  `اصل:`, `فرع:`, `وصف:`, `علة:`, `فارق:`, `وادي:`.

This separation keeps the algebraic API readable internationally without
severing the codebase from its Uṣūlī jurisprudential lineage.

---

## 2. Correspondence Table — Evidence Ranks (درجات الدليل)

| Mathematical term  | Implementation enum     | Arabic jurisprudential root |
| ------------------ | ----------------------- | --------------------------- |
| No evidence        | `NO_EVIDENCE`           | لا دليل                     |
| Formal structure   | `FORMAL_STRUCTURE`      | الصورة                      |
| Analogical rank    | `ANALOGICAL`            | القياس                      |
| Direct hearing     | `DIRECT_HEARING`        | السماع                      |
| Individual report  | `INDIVIDUAL_REPORT`     | الآحاد                      |
| Mass transmission  | `MASS_TRANSMISSION`     | التواتر                     |

The chain is a finite total order under `≤`, and the system computes
`rank_out = meet(slot_ceiling, evidence_rank, input_ranks…)` — the weakest
rank in any premise sequence determines the rank of the conclusion.

---

## 3. Correspondence Table — Wadi Gates (بوابات الحكم)

| Mathematical term | Implementation enum / value | Arabic jurisprudential root |
| ----------------- | --------------------------- | --------------------------- |
| Cause gate        | `WadiGate.CAUSE` / `"cause"`         | السبب |
| Condition gate    | `WadiGate.CONDITION` / `"condition"` | الشرط |
| Obstacle gate     | `WadiGate.OBSTACLE` / `"obstacle"`   | المانع |
| Validity gate     | `WadiGate.VALIDITY` / `"validity"`   | الصحة |
| Corruption gate   | `WadiGate.CORRUPTION` / `"corruption"` | الفساد |
| Nullity gate      | `WadiGate.NULLITY` / `"nullity"`     | البطلان |

The six gates are conjunctive: every rule declares `required_wadi_gates`
and the kernel blocks the conclusion unless **all** declared gates hold.

> **Translational caveat (mandatory in the paper).**
> `CAUSE` is the implementation label for *sabab*, not a full translation of
> causality in modern metaphysics. `OBSTACLE` is the implementation label
> for *māniʿ*, not a generic notion of impediment. Each English label is a
> binding identifier into the algebra; the Uṣūlī semantics are fixed by the
> jurisprudential root column above. When citing this work, the
> correspondence table — not isolated English labels — defines the term.

---

## 4. Claim Prefixes (Internal — Not Translated)

| Prefix     | Meaning (Uṣūlī)                                 |
| ---------- | ----------------------------------------------- |
| `اصل:`     | the established source (asl)                     |
| `فرع:`     | the determined target (farʿ)                     |
| `وصف:`     | the effective attribute (wasf)                   |
| `علة:`     | the licensing cause (ʿillah)                     |
| `فارق:`    | the invalidating difference (fāriq)              |
| `وادي:`    | the validity-gate claim (wadi)                   |

These prefixes appear inside string-valued evidence claims, e.g.
`"اصل:established"`, `"وادي:cause:established"`,
`"فارق:non_arabic_codepoint:present"`. They are **not** part of the public
algebraic vocabulary; they are part of the proof-relevant content of the
`EvidenceSet`, and they preserve the Uṣūlī lineage of each licensed
equality.

The kernel uses these prefixes structurally (e.g.
`request.evidence.proves(f"فارق:{diff}:present")` in
`_check_fariq`), so any external instrument that produces evidence for
`qiyas_core` must emit claims with these Arabic prefixes verbatim.

---

## 5. Paragraph for the Paper

> We normalize the public implementation vocabulary into English algebraic
> labels while preserving Arabic claim prefixes for proof provenance. Thus,
> evidence ranks are exposed as `NO_EVIDENCE`, `FORMAL_STRUCTURE`,
> `ANALOGICAL`, `DIRECT_HEARING`, `INDIVIDUAL_REPORT`, and
> `MASS_TRANSMISSION`, whereas proof claims retain their internal
> jurisprudential structure through prefixes such as `اصل:`, `فرع:`,
> `وصف:`, `علة:`, `فارق:`, and `وادي:`. The English labels are binding
> identifiers into the algebra and are not intended as full semantic
> translations of their Uṣūlī roots; the correspondence table in
> Appendix [TERMINOLOGY_MAP] fixes the binding.

---

## 6. Scope of the Renaming (Audit Record)

The unification of vocabulary was applied across:

- `src/qiyas_core/` — every adapter, rule, and the kernel itself.
- `tests/qiyas_core/` — all 172 canonical tests.
- `experimental/qiyas_core/` and `experimental/tests/qiyas_core/` — the
  pre-constitutional SlotGeometry reference is renamed for terminology
  consistency only; its non-canonical status under §7 of
  `RESET_CONSTITUTION.md` is unchanged.
- `run_qiyas.py` and `slot_geometry_algebra.py` at the repository root.

The canonical test suite (172/172) passes against the renamed vocabulary,
which establishes that the rename is observationally neutral with respect
to the kernel’s algebraic behavior.

---

## 7. Cross-References

- `RESET_CONSTITUTION.md` §7 — prohibits adopting any SlotGeometry under
  `src/` before constitutional validation.
- `LAYER_CONTRACT_CONSTITUTION.md` §2.3 — describes the prefix-based
  evidence machinery (`فارق:`, `defer:`) the kernel already enforces.
- `ALGEBRAIC_FOUNDATION_CONTRACT.md` — fixes the algebraic skeleton that
  this vocabulary describes.
