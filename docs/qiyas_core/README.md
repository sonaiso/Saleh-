# Qiyas Core Documentation — Reading Guide

**Welcome to the constitutional documentation for the Saleh/Qiyas project.**

---

## Reading Order (MANDATORY for All Agents)

### 1. Mathematical Foundation (Read FIRST)

**📐 PROJECT_MATHEMATICAL_FOUNDATION.md**

This document defines what the project IS:
- NOT a linguistic pipeline
- IS an algebraic qiyas system
- Layer = Domain, Transition = Qiyas, Composition = Partial Algebra
- Governing law: "Do not create names. Prove transitions."

**Start here. Everything else implements this foundation.**

---

### 2. Governance Framework (Read BEFORE Implementation)

**🏛️ CANONICAL_ARCHITECTURE_CONTROL_FRAME.md**

Implements the mathematical foundation with governance rules:
- Current canonical vs experimental vs deprecated status
- **Duplicate Prevention Table (critical)** — prevents creating new names for existing concepts
- Canonical Name Registration Law
- Enforcement authority

**📋 LAYER_REGISTRY.md**

Single source of truth for all layers:
- Layer 0: Unicode
- Layer 1: TypedCodePoint
- Layer 2A-D: Parallel atomic proofs (Letter, Haraka, Position, Alignment)
- Layer 3: SlotCandidate
- Layer X: ArabicLetterCoordinateCarrier (partial)
- Not-implemented layers with constitutional contracts

**🔄 EXPERIMENTAL_TO_CANONICAL_MAP.md**

Prevents accidental revival of pre-constitutional components:
- Maps experimental/ to canonical replacements
- Specifies: Do NOT revive, Requires validation, Extract patterns
- Detailed analysis of replaced architectures

**🌳 NEXT_LAYER_DECISION_TREE.md**

7-point decision framework before proposing new layers:
- Existing layer check
- Missing data check
- Silent failure check
- Multiple roles check
- Sequence validation
- Constitutional gate check
- Duplicate check

**✅ AGENT_PR_CHECKLIST.md**

Mandatory pre-implementation checklist:
- 13 sections covering all compliance requirements
- Must be completed BEFORE writing code
- PRs rejected if incomplete

---

### 3. Constitutional Theory (Reference)

**📜 LAYER_CONTRACT_CONSTITUTION.md**

Defines constitutional gates for future layers:
- 14 transfer gates (reality type, derivational role, lexical attestation, etc.)
- Domain-specific contracts
- Layer sovereignty principles

**📖 TERMINOLOGY_MAP.md**

Fixed canonical naming conventions:
- EvidenceRank values
- WadiGate values
- Arabic claim prefixes
- Core type names

**⚖️ RESET_CONSTITUTION.md**

Historical: Established constitutional authority after pre-constitutional period.

**🔍 AUDIT_AFTER_RESET_CONSTITUTION.md**

Historical: Audit that identified 95% pre-constitutional code and recommended Path A isolation.

**📁 PATH_A_ISOLATION_RECORD.md**

Historical: Record of isolating pre-constitutional code to experimental/.

---

## Quick Navigation by Task

### "I want to add a new layer"

1. Read PROJECT_MATHEMATICAL_FOUNDATION.md § 4-5 (Concept Formation)
2. Use NEXT_LAYER_DECISION_TREE.md (7-point check)
3. Check CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 (Duplicate Prevention Table)
4. Consult LAYER_REGISTRY.md (existing layers)
5. Complete AGENT_PR_CHECKLIST.md
6. Create planning PR (NOT implementation yet)

### "I want to extend an existing layer"

1. Check LAYER_REGISTRY.md (find the layer)
2. Read PROJECT_MATHEMATICAL_FOUNDATION.md § 3 (Algebra as Operation)
3. Verify no duplicate in CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2
4. Complete AGENT_PR_CHECKLIST.md "For Extension PRs Only" section
5. Implement extension

### "I want to use something from experimental/"

1. Check EXPERIMENTAL_TO_CANONICAL_MAP.md
2. If status = "Replaced" → Use canonical replacement instead
3. If status = "Requires Validation" → Create constitutional planning PR first
4. If status = "Extract Patterns" → Extract pattern, rebuild constitutionally
5. NEVER copy experimental/ code directly to src/

### "I don't know if a layer exists"

1. Check LAYER_REGISTRY.md first
2. Check CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2 Duplicate Prevention Table
3. Search src/qiyas_core/ for similar names
4. Check EXPERIMENTAL_TO_CANONICAL_MAP.md
5. If still uncertain, ask maintainer

---

## Document Authority Hierarchy

```
Supreme Authority:
  └─ PROJECT_MATHEMATICAL_FOUNDATION.md
      └─ Defines what the project IS

Constitutional Authority:
  ├─ LAYER_CONTRACT_CONSTITUTION.md
  │   └─ Defines constitutional gates
  ├─ RESET_CONSTITUTION.md
  │   └─ Establishes constitutional order
  └─ TERMINOLOGY_MAP.md
      └─ Fixes canonical naming

Governance Authority:
  ├─ CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
  │   └─ Prevents layer duplication
  ├─ LAYER_REGISTRY.md
  │   └─ Catalogs all layers
  ├─ EXPERIMENTAL_TO_CANONICAL_MAP.md
  │   └─ Prevents drift from experimental/
  ├─ NEXT_LAYER_DECISION_TREE.md
  │   └─ Decision framework
  └─ AGENT_PR_CHECKLIST.md
      └─ Validation checklist

Historical Record:
  ├─ AUDIT_AFTER_RESET_CONSTITUTION.md
  ├─ PATH_A_ISOLATION_RECORD.md
  └─ THREE_LAYER_LETTER_ARCHITECTURE.md
```

---

## Critical Rules

### 1. Do Not Create Names. Prove Transitions.

Every new component must answer:
1. What domain does it delimit?
2. What qiyas transition does it prove?
3. What algebraic operation does it perform?
4. What identity does it preserve?
5. What residual does it produce?
6. What existing canonical layer does it extend or replace?

### 2. Check Duplicate Prevention Table

Before creating ANY new layer, check:
- CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 2

If a concept already has a canonical name, EXTEND it, do NOT create parallel implementation.

### 3. Use Decision Tree

Before proposing new layer:
- NEXT_LAYER_DECISION_TREE.md (7-point framework)

Most "new layers" are actually:
- Missing data for existing layer
- Missing evidence for existing layer
- Missing residual handling
- Missing role disambiguation

### 4. Complete Checklist

Before writing implementation code:
- AGENT_PR_CHECKLIST.md (13 sections)

PRs without completed checklist are REJECTED.

### 5. Experimental Boundary

experimental/ is historical archive, NOT source for copying:
- Check EXPERIMENTAL_TO_CANONICAL_MAP.md
- Rebuild constitutionally, do NOT copy directly

---

## Summary

**For Agents:**

```
Read Order:
1. PROJECT_MATHEMATICAL_FOUNDATION.md (what the project IS)
2. CANONICAL_ARCHITECTURE_CONTROL_FRAME.md (governance)
3. LAYER_REGISTRY.md (catalog)
4. NEXT_LAYER_DECISION_TREE.md (decision framework)
5. AGENT_PR_CHECKLIST.md (validation)

Before ANY new layer:
→ Check Duplicate Prevention Table
→ Use Decision Tree
→ Complete Checklist
→ Create planning PR (NOT implementation)
→ Wait for approval

Never:
→ Create new name for existing concept
→ Copy from experimental/ without validation
→ Skip checklist
→ Implement before planning approved
```

**For Maintainer:**

All governing documents are in place:
- Mathematical foundation defined
- Governance framework established
- Layer registry documented
- Decision tree created
- Checklist enforced

Next priority:
- Source-of-truth registry (if needed)
- Full Layer 2 planning (SifatVector + GlyphClassificationGate)

---

**Last Updated:** 2026-06-01
**Status:** Complete governance framework
