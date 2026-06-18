# A Structural Information-Gain Cascade for Proof-Relevant Arabic Slot Geometry

> **Paper-facing draft.** Publication-oriented prose distilled from the landed
> runtime. **Not a constitution and not a new theory/name** — descriptive of
> behavior already on `main`. Internal reference:
> `docs/qiyas_core/SCG_P3_P8_INFORMATION_GAIN_CASCADE.md`.

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

**Outline.** Section 2 defines forwarding vs information-gain layers and the
cascade. Section 3 details the six stages and their verdict rules. Section 4
presents the behavioral evidence and per-token trace. Section 5 states the safety
boundary and its enforcement. Section 6 discusses limitations and the bridge to
the first multi-unit, sentence-geometry stage, which we leave to future work.

## 2. Forwarding versus information-gain layers

The distinction between a forwarding stage and an information-gain stage is
operational and falsifiable. A forwarding stage maps every accepted input to one
accepted output, contributing provenance but no discrimination; an information-gain
stage *partitions* its candidate set — it can refuse inputs — and that partition is
what changes the candidate distribution.

> **Definition — Information-Gain Layer.**
> A layer $L_n$ is an *information-gain layer*, relative to its upstream layer
> $L_{n-1}$, iff:
> 1. it reads the structural evidence emitted by $L_{n-1}$;
> 2. it returns one of ACCEPT / DEFER / BLOCK through the kernel; and
> 3. there exists at least one admissible upstream input that $L_n$ does **not** ACCEPT.
>
> A *forwarding layer* is the degenerate case in which every accepted upstream
> input is mapped to an accepted downstream candidate, with no partition of the
> candidate set (condition 3 fails).

## 3. The cascade: six graded stages

Each stage $P_n$ reads the structural evidence emitted by $P_{n-1}$ directly off
the candidate it receives — a CV signature and derived geometric features
(consonant count, vowel count, gemination, short-vowel cadence, boundary/ending) —
and computes a small stage-specific sub-profile. It then returns one of three
verdicts through the proof kernel: **ACCEPT** (the geometry licenses this stage's
structural opening), **DEFER** (admissible but under-determined; residual
preserved, no downstream opening), or **BLOCK** (a structural contradiction;
residual preserved). DEFER and BLOCK are not cosmetic: they separate "not yet
warranted" from "impossible," a distinction a proof-relevant pipeline must keep.
The six questions are strictly graded — root/stem closure (P3) → derivation
skeleton (P4) → isolated word-unit body (P5) → verbal-signification carrier (P6)
→ composition boundary (P7) → operator–operand relation possibility (P8) — so the
cascade computes a *graded structural license*, each stage presupposing and
refining the one below. (The exact per-stage verdict thresholds and
input-dependent structural `prior_type` selections are given in the internal
reference note `docs/qiyas_core/SCG_P3_P8_INFORMATION_GAIN_CASCADE.md`.)

## 4. Behavioral evidence

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
produce. (A stage that shows no drop on a given probe, e.g. P5 here, still
exhibits discrimination on a constructed thin input, since information gain is a
property of the decision function, not of any single sample.)

## 5. Safety boundary

Every feature consumed is structural CV-geometry, and every category emitted is a
*structural* class, never a linguistic one (no noun/verb, jāmid/mushtaq, tense,
case, root, or wazn). An ACCEPT *opens priors* toward downstream questions but
emits none of their answers: no meaning, dalālah, or i'rab is produced. This is
enforced, not merely intended — the kernel preserves source identities, flags
every output candidate-only, and checks each stage's forbidden-output set,
including the standing prohibition on final-judgment, reality, and final-meaning
objects. Even an erroneous verdict therefore cannot cross the boundary: at worst
it opens a prior; it can never assert a final reading.

## 6. Limitations and the bridge to P9

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
