# Structural Information-Gain Cascade from SCG-P3 to SCG-P8

> **Paper-facing draft section.** Publication-oriented prose distilled from the
> landed runtime. **Not a constitution and not a new theory/name** — descriptive
> of behavior already on `main`. The internal reference is
> `docs/qiyas_core/SCG_P3_P8_INFORMATION_GAIN_CASCADE.md`.

## Claim

SCG layers P3 through P8 constitute a *structural information-gain cascade*: a
chain of six stages in which each stage is a genuine decision procedure over the
structural geometry produced by the stage below it, rather than a pass-through
that re-labels candidates. The distinguishing property is operational and
falsifiable — an information-gain stage *partitions* its candidate set (it can
refuse inputs), whereas a forwarding stage maps every accepted input to one
accepted output, contributing provenance but no discrimination. We further claim
the cascade is deliberately *sub-semantic* and *potential-only*: it decides
structural admissibility, never linguistic content, and emits only candidates and
licensed priors, never final judgments.

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

## Method

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
refining the one below.

## Behavioral evidence

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

## Safety boundary

Every feature consumed is structural CV-geometry, and every category emitted is a
*structural* class, never a linguistic one (no noun/verb, jāmid/mushtaq, tense,
case, root, or wazn). An ACCEPT *opens priors* toward downstream questions but
emits none of their answers: no meaning, dalālah, or i'rab is produced. This is
enforced, not merely intended — the kernel preserves source identities, flags
every output candidate-only, and checks each stage's forbidden-output set,
including the standing prohibition on final-judgment, reality, and final-meaning
objects. Even an erroneous verdict therefore cannot cross the boundary: at worst
it opens a prior; it can never assert a final reading.

## Limitation

The cascade is single-unit and pre-relational. Its thresholds are structural
heuristics over CV geometry, not learned parameters, and they are intentionally
conservative (favoring DEFER over speculative ACCEPT). In particular, P8 expresses
a *relation possibility* attached to one unit rather than a realized relation
between two units; the cascade conditions interpretation but does not perform
morphology, syntax, or semantics.

## Bridge to P9

P3–P8 sit entirely below the multi-unit level. SCG-P9 (sentence geometry) is the
first stage at which units are *composed*, and therefore the first at which
structural geometry borders syntactic and i'rab-adjacent territory — exactly where
admissibility risks shading into interpretation. We therefore treat this section
as a deliberate boundary specification: it fixes what the structural cascade does
and, equally, what it refuses to do, so the line P9 must not cross is documented
before it is approached. Extending the cascade to P9 requires lifting the pipeline
to multi-unit input while preserving the same potential-only, three-valued,
kernel-enforced discipline established here.
