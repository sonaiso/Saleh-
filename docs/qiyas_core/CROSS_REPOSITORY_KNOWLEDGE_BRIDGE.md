# CROSS-REPOSITORY KNOWLEDGE BRIDGE

> **Type:** Governance document — non-normative policy
> **Status:** Active
> **Scope:** Saleh- ↔ Binary- relationship
> **Authority:** Maintainer instruction (2026-06-09)
> **Constitutional basis:** LAYER_CONTRACT_CONSTITUTION.md §0 (no cross-domain authority transfer without licensed gate)

---

## 1. Principle

```text
No cross-repository authority.

A repository may learn from another repository,
but it may not inherit its scope, runtime, rank, or output authority.
```

---

## 2. Repository Roles

### Binary- (`sonaiso/Binary-`)

Foundational digital encoding repository. Scope:

```text
Binary
Bytes
Encoding
Unicode
WrittenSurface
SyllableBridgeExport
```

Binary- is a **digital surface foundation**. It proves that text exists and has structure. It does not perform qiyas, analogical reasoning, root extraction, grammatical analysis, or hukm.

### Saleh- (`sonaiso/Saleh-`)

Knowledge and inference repository. Scope:

```text
Qiyas (analogical proof)
Constitutional governance
Layer transitions
Evidence, Rank, Residuals
Slot Geometry
LCNV
Logarithmic Measurement
Deeper analysis layers
```

Saleh- is a **knowledge and inference system**. It receives surface carriers and performs licensed algebraic transitions through the QiyasKernel.

---

## 3. Permitted Relationship: Read-Only Knowledge Bridge

```text
ReadOnlyKnowledgeBridge
```

The only permitted cross-repository relationship is:

```text
Cross-read is allowed.
Cross-write is forbidden.
Cross-import is forbidden unless licensed by a Knowledge Transfer Record.
```

### What "read" means

Any agent, human, CI workflow, or GitHub App may:

- Read the source code, tests, and documentation of both repositories.
- Observe patterns, discoveries, and audit findings in either repository.
- Use those observations to improve the **local** repository via a local PR.

### What "read" does not authorize

Reading does not authorize:

- Modifying the other repository directly.
- Opening a PR in the other repository automatically.
- Importing a module from the other repository at runtime.
- Treating a discovery in one repository as a law in the other repository without a Knowledge Transfer Record.
- Expanding the scope of a layer because the other repository has that layer.

---

## 4. Forbidden Operations

The following are explicitly forbidden:

```text
FORBIDDEN-01  Binary- opens a root/wazn layer because Saleh- has root/wazn
FORBIDDEN-02  Saleh- copies Binary- code without a Knowledge Transfer Record
FORBIDDEN-03  A discovery in one repository automatically becomes law in the other
FORBIDDEN-04  An agent reads Binary- and writes to Saleh- in the same automated step
              without an explicit PR in Saleh-
FORBIDDEN-05  Runtime dependency: neither repository imports from the other at runtime
FORBIDDEN-06  Shared kernel: no shared QiyasKernel or BinaryKernel across repositories
FORBIDDEN-07  Shared dataclass: no dataclass definition shared between repositories
FORBIDDEN-08  Write access granted to an agent on both repositories simultaneously
              without explicit per-operation authorization
```

---

## 5. Knowledge Transfer Record

Every time a discovery in one repository is applied to the other, a Knowledge Transfer Record must be filed. The record is not a separate file — it is embedded in the PR description of the **target** repository.

### Required fields

```text
source_repository:
  [Binary- | Saleh-]

target_repository:
  [Binary- | Saleh-]

discovery:
  [Short description of what was found]

source_context:
  [PR number, audit document, or test file where discovery was made]

target_application:
  [Specific file or component in the target repository that was improved]

transfer_type:
  [test-governance | boundary-hardening | constitutional-alignment | other]

forbidden_in_this_transfer:
  - no runtime dependency introduced
  - no scope expansion
  - no layer imported from source repository

result:
  [Measurable outcome: tests added, assertion hardened, boundary documented]
```

### Completed example

The following transfer was executed correctly (2026-06-09):

```text
source_repository:
  Binary-

target_repository:
  Saleh-

discovery:
  Tautological constitutional assertion — `assert X or Y and False` collapses
  to `assert X` due to Python operator precedence; the intended boundary check
  was never exercised.

source_context:
  Binary- PR #82 Copilot review comment on
  tests/binary_core/test_syllable_bridge_export.py:217-221

target_application:
  tests/qiyas_core/test_logarithmic_measurement_carrier_readiness_constitution.py:270
  (test_rank_preservation_in_implementation)

transfer_type:
  test-governance

forbidden_in_this_transfer:
  - no runtime dependency introduced
  - no scope expansion
  - no layer imported from Binary-

result:
  Replaced tautological assertion with four precise rank-literal checks.
  1086 tests passed, 4 skipped, 0 failures.
```

---

## 6. Transfer Workflow

The correct transfer workflow is:

```text
1. Discovery in source repository
   (audit finding, review comment, CI failure, test pattern)

2. Record the discovery
   (note source: PR number, file, line)

3. Classify applicability to target repository
   (does the same pattern exist? does the same principle apply?)

4. Open a local PR in the target repository only
   (no changes to the source repository in this PR)

5. Add tests in the target repository that prove the transfer
   (the transfer must be verifiable independently of the source)

6. Document the Knowledge Transfer Record in the PR description

7. Merge only after tests pass
```

The incorrect workflow is:

```text
Read → Copy → Merge
```

The correct workflow is:

```text
Read → Discover → Classify → Transfer Record → Target PR → Tests → Merge
```

---

## 7. Agent Permissions Policy

When an agent operates on these repositories, the following permissions apply:

### Read permissions (always permitted)

```text
Binary-:  contents:read, pull_requests:read, issues:read, metadata:read
Saleh-:   contents:read, pull_requests:read, issues:read, metadata:read
```

### Write permissions (scoped and temporary)

When an agent executes a PR in a specific repository, write access is granted only to **that repository** for the duration of that operation:

```text
If writing to Saleh-:   contents:write on Saleh- only
If writing to Binary-:  contents:write on Binary- only
```

### Explicitly forbidden agent permissions

```text
- write on both repositories simultaneously without per-operation scope declaration
- admin on either repository
- secrets access
- actions:write
- workflows:write
```

Unless explicitly authorized by the maintainer for a specific named operation.

---

## 8. Scope Isolation Invariant

The scope of each repository is fixed by its constitutional documents.

```text
Binary- scope is fixed by:
  BINARY_FOUNDATION_SCOPE.md
  WRITTEN_SURFACE_CARRIER_CONSTITUTION.md
  ORIGIN_BRANCH_LEGITIMACY_CONSTITUTION.md

Saleh- scope is fixed by:
  PROJECT_MATHEMATICAL_FOUNDATION.md
  CANONICAL_ARCHITECTURE_CONTROL_FRAME.md
  LAYER_REGISTRY.md
  LAYER_CONTRACT_CONSTITUTION.md
```

A layer that exists in one repository does not authorize the existence of that layer in the other repository. Scope expansion requires a constitutional PR **in the target repository**, not merely the observation that the other repository has the layer.

---

## 9. Summary

```text
Read-only cross-repository knowledge bridge.

NOT: shared runtime dependency
NOT: automatic code transfer
NOT: mutual write access
NOT: scope inheritance

القراءة المتبادلة مسموحة.
الكتابة المتبادلة ممنوعة.
النقل البرمجي أو الدستوري لا يتم إلا بسجل نقل معرفة.
المستودع يتعلم من الآخر، لكنه لا يرث سلطته.
```
