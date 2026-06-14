# LICENSED_SYLLABLE_SEQUENCE_CONSTITUTION — Layer 5 (potential-only)

> **Status:** Constitutional record of the **narrow Layer 5 authorization**
> (2026-06-14). Layer 5 is a potential-only structural composition runtime. It
> is NOT semantic understanding, NOT wordhood, NOT final interpretation.
>
> **Authority:** maintainer directive 2026-06-14;
> `PROJECT_RECOVERY_CANONICAL_MAP.md` §1.2;
> `REPOSITORY_RESPONSIBILITY_MATRIX.md` §4.2; `CLAUDE.md` §0–§21.

---

## 1. Role

Layer 5 (`LicensedSyllableSequenceCandidate`,
`src/qiyas_core/licensed_syllable_sequence.py`) performs **structural
composition only**: it groups adjacent, ordered, boundary-preserving Layer 4
`LicensedSyllableCandidate` objects into a single potential-only sequence
candidate, or emits invalidation evidence when composition is not licensed.

```
Geometric/structural composition is not wordhood.
Sequence order is not grammar.
A licensed sequence is not a meaning.
```

## 2. Anti-duplication boundary

| Layer | Input | Output | Obligation |
| --- | --- | --- | --- |
| MIU readiness | one length-1 slot-geometry seed (+ witnesses) | `MinimalUnitReadinessCandidate` | is one minimal unit ready to stand alone? |
| Layer 4 | one token's codepoints | `LicensedSyllableCandidate` | license one syllable |
| `slot_geometry_closure_check` | slot geometry | `MinimalCompleteClosureEvidence` | is closure complete? |
| **Layer 5** | **≥1 already-licensed Layer 4 candidates** | `LicensedSyllableSequenceCandidate` | **compose adjacent syllables into one sequence** |

Layer 5 consumes Layer 4 output read-only; it never re-licenses syllables,
never assesses single-unit readiness, and never checks closure. It constructs;
it does not infer.

## 3. Required evidence objects

- lower-candidate evidence: Layer 4 `LicensedSyllableCandidate` (licensed,
  potential-only)
- `SequenceAdjacencyEvidence` — consecutive token indices, gap-free
- `SequenceOrderEvidence` — strictly increasing token order
- `SequenceIdentityPreservationEvidence` — each constituent surface preserved
- `SequenceBoundaryPreservationEvidence` — constituent boundaries preserved,
  spans non-overlapping
- `SyllableSequenceInvalidationEvidence` — residual when composition is refused

## 4. Required behavior

- preserve `surface_form_vocalized` (the sequence surface is the ordered join
  of constituent surfaces; the round-trip is enforced by test)
- preserve exact codepoint identity
- preserve original token boundaries and Layer 4 candidate boundaries
- preserve candidate order
- require adjacency and order evidence before emitting a candidate
- emit invalidation evidence instead of a candidate when composition is not
  licensed (non-adjacent, out-of-order, unlicensed/missing lower unit, identity
  drift, boundary drift, overlapping spans)
- remain potential-only; render/report only structural facts

## 5. Equality

- **Licensed:** two sequence candidates are equal iff they have identical
  ordered constituent token identities, identical `surface_form_vocalized`, and
  identical boundary spans.
- **Refused:** equality by "same word / root / wazn / meaning / i'rab", by
  phonetic similarity, by haraka-stripped normalization, or across token
  boundaries.

## 6. Potential-only / hard prohibitions

Every candidate carries `potential_only=True`,
`runtime_status="layer5_potential_only"`, and the bundle records
`meaning_status=hukm_status=irab_status=reality_status="not_introduced"`.

Layer 5 introduces **no** wordhood, lafz, root, wazn, morphology, grammar,
i'rab, dalalah, tafsir, lexical meaning, hukm, RealityClaim, FinalMeaning,
semantic runtime, source correction, hidden runtime admission, Layer 6+,
REC-6, global freeze release, Binary- writes, `new_arabic_analyzer/` changes,
or a runtime YAML loader.

## 7. Registry boundary

Layer 5 is a **standalone narrow runtime**, mirroring Layer 4. It is **not**
inserted into the canonical 19-layer SCG master registry; the registry layer
count, phases, ranks, statuses, gates, and origin notes are **unchanged**. A
negative guard test (`LAYER5-REG-*`) proves the 19-layer registry is untouched.

Enforced by `tests/qiyas_core/test_licensed_syllable_sequence.py` (`LAYER5-*`)
and the narrow-authorization records in the freeze-status verifier (§4.5).
