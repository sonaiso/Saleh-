# LICENSED LOGARITHMIC MEASUREMENT LAW

> **قانون القياس اللوغاريتمي المرخّص**
>
> **Licensed Logarithmic Measurement Law**

---

## 0. Constitutional Authority

**This document establishes constitutional constraints on logarithmic operations within the qiyas system.**

**Authority:**
- Below: PROJECT_MATHEMATICAL_FOUNDATION.md (defines algebraic qiyas system)
- Below: CANONICAL_ARCHITECTURE_CONTROL_FRAME.md (defines layer architecture)
- Below: LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md (defines numeric encoding constraints)
- Above: All runtime logarithmic measurement implementations

**Document Version:** 1.0

**Status:** Constitutional constraint with initial isolated runtime implementation

**Purpose:**
- Define what logarithmic operations ARE permitted (licensed measured quantities only)
- Define what logarithmic operations are FORBIDDEN (candidates, LCNV, meanings, hukm)

**Why this document exists NOW:**

After PR #52, the LCNV inverse law is corrected:
```
Unpack(Pack(c)) ≠ Candidate(c)
Unpack(Pack(c)) = EncodedStateProjection(c)
```

This correction prevents numeric values from becoming sources of authority. The next step is to prevent logarithmic operations from being applied to candidates, meanings, or other non-quantitative objects.

**The risk this prevents:**
```
❌ log(Candidate)
❌ log(LCNV)
❌ log(Meaning)
❌ log(Ifadah)
❌ log(Hukm)
❌ inverse_log(LogQuantity) → Candidate
❌ inverse_log(LogQuantity) → Meaning
```

---

## 1. Central Law

### 1.1 Domain Restriction

**Logarithm does NOT operate on:**
- ❌ Candidate
- ❌ LCNV
- ❌ EncodedStateProjection
- ❌ Meaning
- ❌ Ifadah
- ❌ Hukm
- ❌ RealityClaim
- ❌ Evidence
- ❌ Trace

**Logarithm ONLY operates on:**
- ✓ LicensedMeasuredQuantity

**The ONLY permitted operations:**

```
log : LicensedMeasuredQuantity → LogMeasuredQuantity

inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity
```

### 1.2 Forbidden Operations

**Explicitly forbidden:**

```
log(Candidate) ⇏ LogQuantity
log(LCNV) ⇏ LogQuantity
log(EncodedStateProjection) ⇏ LogQuantity
log(Meaning) ⇏ LogQuantity
log(Ifadah) ⇏ LogQuantity
log(Hukm) ⇏ LogQuantity

inverse_log(LogQuantity) ⇏ Candidate
inverse_log(LogQuantity) ⇏ LCNV
inverse_log(LogQuantity) ⇏ Meaning
inverse_log(LogQuantity) ⇏ Ifadah
inverse_log(LogQuantity) ⇏ Hukm
```

---

## 2. LicensedMeasuredQuantity Definition

### 2.1 Required Components

**A LicensedMeasuredQuantity is NOT just a number.**

**It MUST include ALL of the following:**

```
LicensedMeasuredQuantity =
  numeric_value           (the actual number)
+ quantitative_domain     (open numeric domain, not closed categorical domain)
+ unit_of_measurement     (what is being measured)
+ measurement_basis       (base of measurement, e.g., e, 2, 10)
+ sabab_tashghil         (reason for operation)
+ shart_tahaqquq         (condition of validity)
+ intifa_mani            (absence of blocking factor)
+ sihhah                 (correctness)
+ intifa_fasad           (absence of corruption)
+ intifa_butlan          (absence of invalidity)
+ Rank                   (Rank ceiling via meet semantics)
+ preserved_residuals    (residuals must be preserved)
+ trace                  (trace must be preserved and separated from identity)
```

### 2.2 Not Every Number Is Licensed

**Not every number may enter logarithm.**

**A number enters logarithm ONLY IF:**
1. It is a LicensedMeasuredQuantity (not just a raw number)
2. It is in an open quantitative domain (not a closed categorical domain)
3. It has a unit of measurement
4. It has a known measurement basis
5. Its gate is OPEN
6. It has no blocking residuals
7. It satisfies the wad' constraints (see § 3)

**Examples of what is NOT a LicensedMeasuredQuantity:**
- ❌ A Candidate (even if it has numeric fields)
- ❌ An LCNV value (it is compressed trace, not a quantity)
- ❌ An Abjad value (it is a coordinate, not a measured quantity)
- ❌ A rank value (it is a meet-semilattice value, not a measured quantity)
- ❌ A categorical numeric encoding (closed domain)

---

## 3. Ahkam Al-Wad' for Logarithm

**The five ahkam al-wad' (conditions of legal validity) for logarithmic operations:**

### 3.1 As-Sabab (The Cause)

**Sabab:**
- The presence of a need to measure a quantity
- OR the presence of a need to compress a numeric range

**Not a valid sabab:**
- Deriving meaning from a number
- Extracting semantic content from a coordinate
- Upgrading rank through numeric transformation
- Producing a Candidate from a numeric value

### 3.2 Ash-Shart (The Condition)

**Shart:**
- The input MUST be a LicensedMeasuredQuantity
- The input MUST be positive OR shifted by a licensed offset
- The input MUST have a unit of measurement
- The input MUST have a known basis

**Violations of shart:**
- Input is a Candidate (not a quantity)
- Input is LCNV (compressed trace, not a quantity)
- Input is Meaning (semantic object, not a quantity)
- Input is Hukm (judgment, not a quantity)
- Input is from a closed categorical domain
- Input is negative without a licensed offset

### 3.3 Al-Mani' (The Blocking Factor)

**Mani':**
- Input is a Candidate
- Input is LCNV
- Input is Meaning
- Input is Hukm
- Input is from a closed categorical domain
- Input is negative without a licensed offset
- Basis is zero, one, or negative
- Unit of measurement is absent
- Gate is CLOSED
- Blocking residuals are present

### 3.4 As-Sihhah (Correctness)

**Sihhah:**
- Quantitative domain is verified
- Basis is valid (b > 0, b ≠ 1)
- Unit is preserved
- Trace is preserved
- Residuals are preserved

### 3.5 Al-Fasad wa-l-Butlan (Corruption and Invalidity)

**Fasad (corruption, but potentially correctable):**
- Unit is inconsistent
- Offset is insufficient
- Non-blocking residuals exist but are not preserved

**Butlan (invalidity, uncorrectable):**
- Logarithm is applied to a non-quantity (Candidate, Meaning, Hukm, etc.)
- Logarithm is used to derive Candidate
- Logarithm is used to derive Meaning
- Logarithm is used to derive Hukm
- Inverse logarithm is used to produce Candidate
- Inverse logarithm is used to produce Meaning

---

## 4. Invalidating Difference (Al-Farq Al-Qadih)

**An invalidating difference in logarithm is NOT any difference,**
**but only what touches the cause of quantitative measurement.**

### 4.1 Examples of Invalidating Difference

**Farq qadih (invalidating difference):**
- Input is not a quantity
- Domain is not quantitative
- Gate is CLOSED
- Value is negative without a licensed offset
- Basis is zero, one, or negative
- Unit is absent
- Blocking residuals are present
- Output claims to be a Candidate
- Output claims to be a Meaning
- Output claims to be a Hukm

### 4.2 Examples of Non-Invalidating Difference

**NOT farq qadih (non-invalidating difference):**
- Different basis (e vs 2 vs 10) within valid range
- Different unit (as long as it is present and consistent)
- Different offset amount (as long as it is licensed)
- Different trace structure (as long as trace is preserved)

---

## 5. Inverse Law for Logarithm

### 5.1 Mathematical Formulation

**Mathematical form:**
```
y = log_b(1 + x)
x = b^y - 1
```

### 5.2 Constitutional Formulation

**Constitutional form:**
```
inverse_log(log(x)) = x

ONLY IF:
  x ∈ LicensedMeasuredQuantity
  b > 0
  b ≠ 1
  x ≥ 0  (or x ≥ offset if offset is licensed)
  Gate(x) = OPEN
  No blocking residuals
```

### 5.3 Inverse Returns Quantity Only, Not Candidate

**Critical law:**

```
inverse_log(log(Quantity)) = Quantity

inverse_log(log(Candidate)) is FORBIDDEN
```

**The inverse returns the measured quantity,**
**NOT the Candidate,**
**NOT the Meaning,**
**NOT the Hukm.**

---

## 6. LogMeasuredQuantity Definition

### 6.1 Structure

**LogMeasuredQuantity is NOT a raw logarithmic value.**

**It MUST include:**

```
LogMeasuredQuantity =
  log_value                    (the logarithmic value)
+ original_unit                (unit from input quantity)
+ measurement_basis            (base used in logarithm)
+ offset                       (offset applied before log, if any)
+ quantitative_domain_identity (domain of the input quantity)
+ rank                         (rank from input, preserved)
+ preserved_residuals          (residuals from input, preserved)
+ trace                        (trace from input plus log operation trace)
```

### 6.2 Constraints

**LogMeasuredQuantity MUST NOT:**
- Claim to be a Candidate
- Claim to be a Meaning
- Claim to be an Ifadah
- Claim to be a Hukm
- Derive semantic content
- Upgrade rank
- Hide residuals
- Consume identity into trace

**LogMeasuredQuantity MUST:**
- Preserve original unit
- Preserve measurement basis
- Preserve rank (ceiling via meet semantics)
- Preserve residuals
- Preserve and extend trace
- Remain a potential/candidate value (never final)

---

## 7. Governing Principles

### 7.1 In Arabic

```
المقدار المرخّص فقط يدخل اللوغاريتم.
والمرشح ليس مقدارًا.
والمعنى ليس مقدارًا.
والحكم ليس مقدارًا.
والقيمة العددية المضغوطة ليست مقدارًا.

واللوغاريتم لا يُنتج مرشحًا.
ولا يُنتج معنى.
ولا يُنتج حكمًا.
ولا يُنتج معرفة.

اللوغاريتم عملية كمية على كمية مرخّصة.
وعكس اللوغاريتم يعيد الكمية فقط، لا المرشح.

الكمية ليست هوية.
واللوغاريتم لا يمسّ الهوية.
الهوية محفوظة مستقلة عن الأثر.
```

### 7.2 In English

```
Only a LicensedMeasuredQuantity may enter logarithm.
Candidate is not a quantity.
Meaning is not a quantity.
Hukm is not a quantity.
Compressed numeric value is not a quantity.

Logarithm does not produce Candidate.
Logarithm does not produce Meaning.
Logarithm does not produce Hukm.
Logarithm does not produce knowledge.

Logarithm is a quantitative operation on a licensed quantity.
Inverse logarithm returns the quantity only, not the Candidate.

Quantity is not identity.
Logarithm does not touch identity.
Identity is preserved independent of trace.
```

---

## 8. Relationship to LCNV

### 8.1 Logarithm and LCNV Are Different

**Logarithm ≠ LCNV**

- LCNV compresses qiyas layer state (gates, evidence, rank, residuals)
- Logarithm compresses quantitative ranges (numeric measurements)

**Both share constraints:**
- Neither operates on Candidate
- Neither operates on Meaning
- Neither operates on Hukm
- Neither produces semantic derivation
- Both preserve rank
- Both preserve residuals
- Both preserve trace separate from identity

### 8.2 Potential Future Interaction

**IF logarithm is used within LCNV encoding (future possibility):**

It may ONLY be used on numeric blocks that:
1. Are already LicensedMeasuredQuantity instances
2. Have passed all wad' constraints
3. Have OPEN gates
4. Have no blocking residuals

**It may NOT be used on:**
- The LCNV value itself
- Candidates being compressed
- Meanings being compressed
- Any categorical coordinate

---

## 9. Constitutional Tests Required

**This document requires guard tests (textual, not runtime):**

### 9.1 Forbidden Phrases Test

**The test MUST verify the document does NOT contain** (without prohibition markers):
- "log(Candidate)" (without ⇏ or ❌ or FORBIDDEN)
- "log(LCNV)" (without ⇏ or ❌ or FORBIDDEN)
- "log(Meaning)" (without ⇏ or ❌ or FORBIDDEN)
- "log(Ifadah)" (without ⇏ or ❌ or FORBIDDEN)
- "log(Hukm)" (without ⇏ or ❌ or FORBIDDEN)

### 9.2 Required Phrases Test

**The test MUST verify the document DOES contain:**
- "LicensedMeasuredQuantity"
- "LogMeasuredQuantity"
- "log : LicensedMeasuredQuantity → LogMeasuredQuantity"
- "inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity"
- "log(Candidate) ⇏"
- "log(LCNV) ⇏"
- "log(Meaning) ⇏"
- "inverse_log(LogQuantity) ⇏ Candidate"
- "Quantity is not identity"
- "Only a LicensedMeasuredQuantity may enter logarithm"

---

## 10. Implementation Status

**Current status:** Constitutional constraint with initial isolated runtime implementation

**What exists:**

A minimal isolated runtime implementation exists in `src/qiyas_core/logarithmic_measurement.py` providing:
- LicensedMeasuredQuantity dataclass
- LogMeasuredQuantity dataclass
- log_quantity function with wad' validation
- inverse_log_quantity function with wad' validation

**What is NOT implemented:**
- No LCNV integration
- No Candidate integration
- No MCLO integration
- No Pack/Unpack integration
- No semantic or hukm integration

**What IS implemented:**
- Blocking residual classification and validation (rejects residual:blocking:*, *:blocking:*, blocking:*)
- Operation trace extension (appends trace:log_quantity:{quantity_id} to trace_ids)

**Future implementation requirements:**

Future enhancements to logarithmic measurement operations MUST:
1. Add farq qadih detection beyond basic type checking
2. Add rank preservation verification tests
3. Add comprehensive residual preservation tests
4. Prevent any integration with Candidate, LCNV, Meaning, Hukm systems

**Implementation MUST NOT:**
- Accept Candidate as input
- Accept LCNV as input
- Accept Meaning as input
- Produce Candidate as output
- Produce Meaning as output
- Skip wad' validation
- Skip farq qadih detection
- Hide or eliminate residuals
- Upgrade rank through numeric manipulation

---

## 11. Governing Law Summary

```
الكمية المرخّصة فقط تدخل اللوغاريتم.
واللوغاريتم لا ينتج مرشحًا ولا معنى ولا حكمًا.
والعكس يعيد الكمية فقط.
والكمية ليست هوية.
والهوية محفوظة مستقلة عن الأثر.
```

```
Only LicensedMeasuredQuantity enters logarithm.
Logarithm does not produce Candidate, Meaning, or Hukm.
Inverse returns quantity only.
Quantity is not identity.
Identity is preserved independent of trace.
```

---

**End of Constitutional Document**

**الحمد لله رب العالمين**
