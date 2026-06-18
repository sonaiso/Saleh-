# A Structural Information-Gain Cascade for Proof-Relevant Arabic Slot Geometry

> **Paper-facing draft.** Publication-oriented prose distilled from the landed
> runtime. **Not a constitution and not a new theory/name** — descriptive of
> behavior already on `main`, and subordinate to the existing layer constitutions.
> Internal reference: `docs/qiyas_core/SCG_P3_P8_INFORMATION_GAIN_CASCADE.md`.

## Abstract

We present SCG-P3…P8, a six-stage layer of a proof-relevant, identity-preserving
slot-geometry pipeline for Arabic structural analysis, and we characterize it as a
*structural information-gain cascade*. Many layered analysis pipelines suffer from
a silent pathology: intermediate layers *forward* — they map every accepted input
to one accepted output and attach provenance, but never refuse, defer, or split —
so a stack of them adds labels without adding discrimination. We give an
operational, falsifiable definition that separates such forwarding layers from
*information-gain* layers, and we redesign six previously-forwarding SCG stages —
root/stem closure, derivation skeleton, isolated word-unit body,
verbal-signification carrier, composition boundary, and operator–operand relation
possibility — so that each reads the structural geometry emitted below it and
returns one of three kernel-checked verdicts (ACCEPT, DEFER, or BLOCK) over purely
geometric features. The result is a graded structural license whose discriminative
power is directly observable as a monotone contraction of the accepted-candidate
set (10→9→9→7→5→3 on a fixed probe), with representative tokens eliminated at
distinct stages. Crucially, the cascade is deliberately *sub-semantic* and
*potential-only*: it decides structural admissibility and opens downstream priors,
but a kernel-enforced boundary prevents it from emitting meaning, dalālah, i'rab,
or any final judgment. We argue this discipline is a prerequisite for safely
approaching the first multi-unit, sentence-level stage, which we leave to future
work.

## 1. Introduction

**Setting.** Computational treatments of Arabic structure typically commit early
to lexical and morphological decisions — a root, a pattern (*wazn*), a part of
speech — and propagate them downstream. The system studied here takes a different
stance, framing the front end of analysis as a *proof-relevant,
identity-preserving slot-geometry algebra*: it compiles a formally delimited
structural reading into *potential, licensed, auditable* algebraic candidates,
deliberately refusing to jump to final meaning, case, or judgment. Each transition
is a small proof obligation, each output preserves the identities of its inputs,
and nothing is silently discarded. The aim is not to "solve" Arabic but to build a
trustworthy structural substrate on which later, heavier commitments can be made
explicitly and accountably.

**Problem.** A layered design of this kind is only as valuable as the decisions
its layers make. We observed — and an audit confirmed — that six consecutive
stages of the pipeline had degenerated into *forwarding* layers: every accepted
candidate produced exactly one downstream candidate, the "evidence" each layer
emitted was a hard-coded all-pass, and the carried signature was a lossless
re-encoding of upstream identity. Such a layer adds provenance — a record that a
candidate passed through it — but contributes no discrimination: it cannot reject,
defer, or partition, and so cannot change the candidate distribution. A stack of
forwarding layers is therefore behaviorally indistinguishable from a single pass
plus a sequence of rubber stamps — and, worse, it is unfalsifiable, since no input
makes it behave differently.

**This paper.** We reframe and rebuild these six stages, SCG-P3 through P8, as a
structural information-gain cascade. We first give an operational definition: a
layer is information-gain, relative to the layer below it, iff it reads that
layer's structural evidence, returns a kernel-checked ACCEPT/DEFER/BLOCK verdict,
and there exists at least one admissible input it does not accept; forwarding is
the degenerate case in which this last condition fails. Each rebuilt stage answers
a strictly more demanding structural question than its predecessor — root/stem
closure, derivation skeleton, isolated word-unit body, verbal-signification
carrier, composition boundary, and operator–operand relation possibility — over
purely geometric features: consonant/vowel counts, gemination, short-vowel
cadence, and boundary profile. The three-valued verdict is essential: DEFER,
meaning admissible but not yet warranted, and BLOCK, meaning structurally
contradicted, are kept distinct, and every non-acceptance preserves an inspectable
residual, so the cascade is cautious without being lossy.

**Evidence.** Because an information-gain layer must be able to refuse, its effect
is measurable: the accepted-candidate count contracts monotonically along the
cascade, 10→9→9→7→5→3 on a fixed nine-token probe, and representative tokens drop
out at different stages, demonstrating that the layers test different structural
properties rather than re-testing one. Only the richest triliteral, short-vowel
-cadence geometry survives all six gates. This count contraction is a falsifiable
signature: a forwarding stage would necessarily reproduce its predecessor's count.

**Scope and non-claims.** The cascade is explicitly sub-semantic and
potential-only. Every feature it consumes is structural geometry and every
category it emits is a structural class, never a linguistic label; an ACCEPT opens
priors toward downstream questions but emits no meaning, dalālah, or i'rab. A
kernel-enforced boundary — identity preservation, candidate-only outputs, and
per-stage forbidden-output checks including a standing prohibition on
final-judgment, reality, and final-meaning objects — guarantees that even an
erroneous verdict cannot cross from admissibility into interpretation. We make no
claim to morphology, syntax, or semantics; we claim a verified structural front
end.

**Contributions.**

1. An operational, falsifiable criterion distinguishing information-gain from
   forwarding layers, and a reproducible behavioral test: accepted-candidate
   contraction.
2. A three-valued, residual-preserving discrimination scheme, ACCEPT/DEFER/BLOCK,
   over purely structural CV-geometry, instantiated across six graded stages.
3. A kernel-enforced potential-only boundary that separates structural
   admissibility from semantic interpretation, with an explicit specification of
   what the cascade refuses to do.

**Outline.** Section 2 situates the work. Section 3 distinguishes forwarding from
information-gain layers, and Section 4 formalizes the cascade. Section 5 details
the six stages and their verdict rules. Section 6 presents the behavioral evidence
and per-token trace. Section 7 states the safety boundary and its enforcement.
Section 8 discusses limitations and the bridge to the first multi-unit,
sentence-geometry stage, which we leave to future work.

## 2. Related work

We situate the cascade against broad families of prior approaches rather than an
exhaustive bibliography; the intended contribution is narrow.

*Traditional Arabic morphological analysis and root/pattern pipelines*
[ArabicMorphology] recover a root and a pattern (*wazn*) and commit to them as the
backbone of subsequent analysis. *Finite-state and rule-based morphology*
[FiniteStateMorphology] compile such analyses into transducers that are efficient
and inspectable, but typically emit committed analyses rather than graded,
deferrable structural licenses. *Dependency and syntactic pipelines*
[DependencyParsing] assign labels (heads, relations, cases) and propagate them
downstream, so an early label becomes a hard commitment carried by later stages.
*Neural and LLM approaches* [NeuralArabicNLP] produce fluent interpretations and
strong end-task performance, but their intermediate computations are not
proof-relevant: the boundary between structural admissibility and asserted meaning
is not explicit, and per-step evidence and refusals are not first-class. In a
different tradition, *type-theoretic and proof-relevant systems*
[ProofRelevantSystems] keep judgments and their evidence explicit, so that each
step records what was proved and what remains open; and *algebraic or structured
representations of linguistic form* [AlgebraicLinguisticStructure] model
form-level composition as operations on structured objects.

Our contribution is positioned narrowly and without a claim of superiority over
any of these. SCG-P3…P8 contributes a *proof-relevant, identity-preserving,
potential-only structural front end* whose intermediate layers are *falsifiable
decision procedures* — they can refuse and defer, and their discrimination is
observable as candidate-set contraction — rather than forwarding stages that
re-label a fixed candidate set. It does not attempt the morphological,
syntactic, or semantic commitments those other approaches target; it conditions
them while keeping the structural/semantic boundary explicit.

## 3. Forwarding versus information-gain layers

The distinction between a forwarding stage and an information-gain stage is
operational and falsifiable. A forwarding stage maps every accepted input to one
accepted output, contributing provenance but no discrimination; an information-gain
stage *partitions* its candidate set — it can refuse inputs — and that partition is
what changes the candidate distribution. The next section makes this precise.

## 4. Formal model

We model the pipeline as a sequence of layers over typed candidates. The model is
deliberately minimal; it formalizes the distinctions used in the rest of the paper.

**Candidate identity.** A candidate `c` carries two disjoint components: a
preserved *source identity* `I(c)` and a *trace* `T(c)`, with `I(c) ∩ T(c) = ∅`.
Identity records what the candidate *is* (its inherited source references); trace
records *how* it came to be (evidence, signatures, opened priors). Layers may add
trace but must preserve identity: for a downstream candidate `c_n` derived from
`c_{n-1}`, `I(c_{n-1}) ⊆ I(c_n)`.

**Verdict.** Each layer returns one of three values:

```
Verdict = ACCEPT | DEFER | BLOCK
```

**Layer.** A layer `L_n` maps an upstream candidate to a verdict, an *optional*
downstream candidate (present only on ACCEPT, written `⊥` when absent), and a
residual set:

```
L_n : C_{n-1}  →  Verdict × (C_n ∪ {⊥}) × Residual
```

ACCEPT yields a downstream candidate in `C_n` and may attach licensed priors; DEFER
and BLOCK yield `⊥` (no downstream candidate) and a non-empty residual recording,
respectively, under-determination or structural contradiction.

**Forwarding layer.** `L_n` is a *forwarding* layer iff, for every admissible
upstream candidate `c ∈ C_{n-1}`, `L_n(c)` returns `ACCEPT` and exactly one
downstream candidate — i.e. it never returns DEFER or BLOCK and induces no
partition of the admissible set.

**Information-gain layer.** `L_n` is an *information-gain* layer, relative to
`L_{n-1}`, iff:

1. it reads the structural evidence emitted by `L_{n-1}` (it is a function of
   `T(c)`/`I(c)` of its input, not a constant);
2. it returns `ACCEPT | DEFER | BLOCK` through the kernel; and
3. there exists at least one admissible upstream input `c` with
   `L_n(c) ≠ ACCEPT`.

Condition (3) is exactly what a forwarding layer lacks; it is the falsifiable core
of the definition.

**Potential-only safety.** Let `Forbidden` be the set of final semantic,
syntactic, i'rab, hukm, reality, and final-meaning object types. For every layer
and every verdict, the emitted candidate type is required to lie outside
`Forbidden`: an `ACCEPT` may *open licensed priors* toward downstream questions,
but it must not emit any object in `Forbidden`. This is checked per layer, so the
property holds regardless of input — even an erroneous verdict can at most open a
prior, never assert a final judgment.

**Monotone accepted-count contraction.** Fix a probe and let `A_n` be the number
of *accepted* candidates produced at stage `n`. Across the cascade we observe

```
A_3 → A_4 → A_5 → A_6 → A_7 → A_8  =  10 → 9 → 9 → 7 → 5 → 3
```

A strict drop `A_n < A_{n-1}` is behavioral evidence that `L_n` partitioned its
input (a forwarding layer would force `A_n = A_{n-1}`). The converse does not
hold: `A_n = A_{n-1}` on a *single* probe (here `A_5 = A_4 = 9`) does **not** refute
information gain, because the property is function-level — it suffices that *some*
admissible input is not accepted. P5's discrimination is witnessed on a separately
constructed thin input, a function-level counterexample, even though it drops no
candidate on this particular probe.

## 5. The cascade: six graded stages

Each stage `P_n` reads the structural evidence emitted by `P_{n-1}` directly off
the candidate it receives — a CV signature and derived geometric features
(consonant count, vowel count, gemination, short-vowel cadence, boundary/ending) —
and computes a small stage-specific sub-profile. It then returns one of three
verdicts through the proof kernel: **ACCEPT** (the geometry licenses this stage's
structural opening), **DEFER** (admissible but under-determined; residual
preserved, no downstream opening), or **BLOCK** (a structural contradiction;
residual preserved). The six questions are strictly graded — root/stem closure
(P3) → derivation skeleton (P4) → isolated word-unit body (P5) →
verbal-signification carrier (P6) → composition boundary (P7) → operator–operand
relation possibility (P8) — so the cascade computes a *graded structural license*,
each stage presupposing and refining the one below. (The exact per-stage verdict
thresholds and input-dependent structural `prior_type` selections are given in the
internal reference note `docs/qiyas_core/SCG_P3_P8_INFORMATION_GAIN_CASCADE.md`.)

## 6. Behavioral evidence

On a fixed probe the accepted-candidate count contracts monotonically across the
cascade: **10 → 9 → 9 → 7 → 5 → 3** (P3 → P8). This contraction is the central
evidence: (i) it is *falsifiable* — a forwarding stage necessarily reproduces its
predecessor's count, so any strict drop demonstrates partitioning; (ii) the drops
are *distributed and distinct* — different tokens exit at different stages, so the
stages test different structural properties rather than re-testing one; and
(iii) the cascade *terminates on a non-trivial survivor* — only the richest
triliteral, short-vowel-cadence geometry passes all eight gates.

**Per-token trace.** For representative tokens, the verdict at each reached stage
(`A` = accept, `D` = defer, `·` = not reached because the chain stopped above):

| token   | P3 | P4 | P5 | P6 | P7 | P8 | exits at |
|---------|----|----|----|----|----|----|----------|
| بَ      | D  | ·  | ·  | ·  | ·  | ·  | **P3** (defer — bare CV, thin root/stem) |
| مَا     | A  | D  | ·  | ·  | ·  | ·  | **P4** (defer — single-consonant skeleton) |
| بَاب    | A  | A  | A  | D  | ·  | ·  | **P6** (defer — long-vowel-only, no carrier cadence) |
| بَيت    | A  | A  | A  | D  | ·  | ·  | **P6** (defer — long-vowel-only, no carrier cadence) |
| شَاذّ   | A  | A  | A  | A  | D  | ·  | **P7** (defer — no clean composition boundary) |
| دَّ     | A  | A  | A  | A  | D  | ·  | **P7** (defer — boundary under-determined) |
| ضَرَبَ  | A  | A  | A  | A  | A  | A  | **P8** (accept — survives the full ladder) |

Each token is eliminated at a *different* structural criterion, and only `ضَرَبَ`
traverses all six stages — the qualitative outcome the cascade is designed to
produce. (As noted in Section 4, P5 shows no drop on this probe yet remains
information-gain by a function-level counterexample.)

## 7. Safety boundary

Every feature consumed is structural CV-geometry, and every category emitted is a
*structural* class, never a linguistic one (no noun/verb, jāmid/mushtaq, tense,
case, root, or wazn). An ACCEPT *opens priors* toward downstream questions but
emits none of their answers: no meaning, dalālah, or i'rab is produced. This is
enforced, not merely intended — the kernel preserves source identities, flags
every output candidate-only, and checks each stage's forbidden-output set,
including the standing prohibition on final-judgment, reality, and final-meaning
objects. Even an erroneous verdict therefore cannot cross the boundary: at worst
it opens a prior; it can never assert a final reading.

## 8. Limitations and the bridge to P9

The cascade is single-unit and pre-relational. Its thresholds are structural
heuristics over CV geometry, not learned parameters, and they are intentionally
conservative (favoring DEFER over speculative ACCEPT). In particular, P8 expresses
a *relation possibility* attached to one unit rather than a realized relation
between two units; the cascade conditions interpretation but does not perform
morphology, syntax, or semantics.

SCG-P3…P8 sit entirely below the multi-unit level. SCG-P9 (sentence geometry) is
the first stage at which units are *composed*, and therefore the first at which
structural geometry borders syntactic and i'rab-adjacent territory — exactly where
admissibility risks shading into interpretation. We therefore treat the present
work as a deliberate boundary specification: it fixes what the structural cascade
does and, equally, what it refuses to do, so the line P9 must not cross is
documented before it is approached. Extending the cascade to P9 requires lifting
the pipeline to multi-unit input while preserving the same potential-only,
three-valued, kernel-enforced discipline established here, and is left to future
work.
