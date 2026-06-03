# BILLING_ARCHITECTURE_CONTRACT

> **PR-B1 — Documentation only. Contract only. No implementation.**
>
> This file defines the **subscription and billing architecture** for the Saleh/Qiyas product layer. It contains no code, no tests, no modifications to `src/qiyas_core/`, `src/product/`, `tests/`, or `.github/workflows/`. Implementation comes in later PRs, each opening only one component with minimum sufficient scope.

---

## 0. Constitutional Position

| Reference | Function |
|-----------|----------|
| `docs/qiyas_core/LAYER_CONTRACT_CONSTITUTION.md` | Qiyas layer constitutional framework |
| `docs/qiyas_core/CANONICAL_ARCHITECTURE_CONTROL_FRAME.md` | Canonical architecture control |
| **`docs/product/BILLING_ARCHITECTURE_CONTRACT.md` (PR-B1)** | **Billing architecture contract — this file** |
| PR-B2+ | Implementation of entitlements, metering, payment adapters |

Governing principles inherited from qiyas_core:

```
Contract before layer.
Gate before implementation.
Constitution before testing.
```

Applied to product/billing:

```
Contract before billing code.
Architecture before payment provider.
Constitutional separation before integration.
```

---

## 1. Product Nature

### 1.1 What This Project Is

`sonaiso/Saleh-` is **NOT** a generic SaaS application, e-commerce platform, CRM, or content management system.

It **IS**:

```text
Arabic/Qiyas Analysis Engine
Constitutional linguistic/mathematical reasoning infrastructure
Proof-relevant identity-preserving slot geometry algebra
Layered qiyas transition system with evidence, rank, and residuals
```

The correct framing:

> Saleh/Qiyas provides **Qiyas-as-a-Service**: licensed analytical operations over Arabic text, producing algebraic candidates with constitutional guarantees, NOT final meaning or hukm claims.

### 1.2 Architectural Separation

The billing layer is a **product access layer** built **above** the qiyas engine, NOT integrated **within** it.

```text
Architecture:

┌─────────────────────────────────────┐
│   Product Layer (billing)           │
│   - Subscriptions                   │
│   - Usage metering                  │
│   - Entitlements                    │
│   - Payment providers               │
│   - Access control                  │
└─────────────────────────────────────┘
              ↓ (uses)
┌─────────────────────────────────────┐
│   qiyas_core (engine)               │
│   - TypedCodePoint                  │
│   - LetterIdentity                  │
│   - HarakaFunction                  │
│   - SlotCandidate                   │
│   - SlotGeometry                    │
│   - (future layers)                 │
└─────────────────────────────────────┘
```

**Constitutional law:**

```text
qiyas_core = epistemological engine (truth-seeking)
billing = commercial layer (access control)

Payment grants usage rights, NOT analytical authority.
Subscription controls access, NOT qiyas results.
Billing status MUST NEVER alter truth outcomes.
```

---

## 2. Customer Segments

### 2.1 Free / Research

**Target audience:** Researchers, students, individual explorers, academic curiosity.

**Purpose:** Enable exploration, build community, demonstrate value, support academic research.

**Pricing:** Free (永久مجاني)

**Limits:**
- Limited monthly qiyas analyses
- Basic layers only
- Abbreviated trace/residual output
- No API access
- Limited project storage
- No batch processing
- No advanced export formats

**Value proposition:** "Try qiyas analysis for free with academic-friendly limits."

### 2.2 Scholar

**Target audience:** Individual researchers, graduate students, independent scholars, Arabic language professionals.

**Purpose:** Support serious individual research with full analytical depth.

**Pricing:** $9–19 USD/month (or regional equivalent)

**Limits:**
- Higher monthly analysis count (e.g., 1,000 analyses/month)
- Full trace/residual/evidence audit
- Project storage (e.g., 20 projects)
- Advanced export (Markdown, PDF, structured JSON)
- Access to all available qiyas layers
- Email support

**Value proposition:** "Full analytical depth for individual research."

### 2.3 Pro

**Target audience:** Developers, small teams, integration projects, computational linguists.

**Purpose:** Enable programmatic access and batch operations.

**Pricing:** $29–59 USD/month (or regional equivalent)

**Limits:**
- High monthly analysis count (e.g., 10,000 analyses/month)
- API access (rate-limited)
- Batch text processing
- Advanced project management (e.g., 100 projects)
- Full trace/residual/evidence export
- GitHub/file workflow integration (future)
- Priority email support

**Value proposition:** "API access + batch processing for developers."

### 2.4 Enterprise

**Target audience:** Universities, research institutions, language academies, large teams.

**Purpose:** Institutional deployment with custom requirements, SLA, and support.

**Pricing:** Custom (annual contracts)

**Limits:**
- Custom analysis limits
- Custom user count
- Full API access (higher rate limits)
- Team management and permissions
- SLA guarantees
- Direct support channel
- On-premise deployment option (future)
- Custom integration support

**Value proposition:** "Institutional deployment with SLA and dedicated support."

---

## 3. Usage Units

Billing is NOT based solely on "number of users" (this is not a seat-based SaaS).

Billing is based on **analytical operations** because this is a qiyas analysis engine.

### 3.1 Primary Usage Units

| Unit | Definition | Metering Scope |
|------|------------|----------------|
| `qiyas_analysis_count` | Number of qiyas transitions executed (e.g., TypedCodePoint → LetterIdentity → SlotCandidate) | Per complete analysis operation |
| `api_calls` | Number of API requests (Pro+ only) | Per HTTP request to analysis API |
| `batch_jobs` | Number of batch text processing jobs submitted | Per batch job |
| `trace_audit_requests` | Number of detailed trace/residual/evidence inspections | Per audit request |
| `export_reports` | Number of structured exports (PDF, JSON, etc.) | Per export operation |
| `stored_projects` | Number of saved projects/workspaces | Per active project |

### 3.2 Secondary Usage Units (Future)

| Unit | Definition | Future Scope |
|------|------------|--------------|
| `layer_depth_access` | Access to higher computational layers (e.g., Dalalah, Word, when implemented) | Per layer tier |
| `storage_mb` | Total storage used for projects and outputs | Per MB |
| `concurrent_jobs` | Number of parallel batch jobs | Per concurrent slot |

**Important:** `layer_depth_access` does NOT mean "higher layers produce better truth." It means higher layers are computationally more expensive and require more constitutional guarantees. All layers preserve algebraic integrity equally.

---

## 4. Plan Limits

| Plan | Monthly Analyses | Projects | API | Batch | Trace Audit | Export | Support |
|------|-----------------|----------|-----|-------|-------------|--------|---------|
| **Free** | 50 | 2 | ❌ | ❌ | Limited | Text only | Community |
| **Scholar** | 1,000 | 20 | ❌ | ❌ | Full | Markdown/PDF | Email |
| **Pro** | 10,000 | 100 | ✅ Limited | ✅ | Full | All formats | Priority |
| **Enterprise** | Custom | Custom | ✅ Full | ✅ Custom | Full | All formats | Direct/SLA |

**Notes:**

- Limits are **per billing period** (monthly or annual).
- Exceeding limits triggers upgrade prompts, NOT service degradation.
- Analysis quality MUST be identical across all tiers for identical inputs.

---

## 5. Entitlements

### 5.1 Feature Flags

| Feature | Free | Scholar | Pro | Enterprise |
|---------|------|---------|-----|------------|
| Basic qiyas analysis | ✅ | ✅ | ✅ | ✅ |
| Full trace/residual audit | ❌ | ✅ | ✅ | ✅ |
| Project storage | Limited | ✅ | ✅ | ✅ |
| Export (Markdown/PDF) | ❌ | ✅ | ✅ | ✅ |
| Export (JSON/structured) | ❌ | ❌ | ✅ | ✅ |
| API access | ❌ | ❌ | ✅ | ✅ |
| Batch processing | ❌ | ❌ | ✅ | ✅ |
| Team management | ❌ | ❌ | ❌ | ✅ |
| SLA | ❌ | ❌ | ❌ | ✅ |

### 5.2 Entitlement Model (Future Runtime)

When implementing entitlements (PR-B2), the runtime model should be:

```python
@dataclass(frozen=True)
class Plan:
    plan_id: str
    tier: str  # "free", "scholar", "pro", "enterprise"
    monthly_analysis_limit: int
    project_limit: int
    api_enabled: bool
    batch_enabled: bool
    # ... other entitlements

@dataclass(frozen=True)
class Entitlement:
    user_id: str
    plan: Plan
    usage_period_start: str
    usage_period_end: str
    current_usage: dict[str, int]  # {"qiyas_analysis_count": 42, ...}
```

**Constitutional requirement:** Entitlement checks MUST occur at the **access layer**, NOT within qiyas_core analysis functions.

---

## 6. Constitutional Prohibitions

### 6.1 Absolute Prohibitions

The following are **constitutionally forbidden**:

```text
1. billing code MUST NOT exist inside src/qiyas_core/
2. payment status MUST NOT alter qiyas analysis results
3. payment status MUST NOT alter evidence proofs
4. payment status MUST NOT alter rank calculations
5. payment status MUST NOT alter residual preservation
6. payment status MUST NOT alter trace generation
7. subscription tier MUST NOT create analytical authority
8. subscription tier MUST NOT produce different candidate identities
9. Free tier and Enterprise tier MUST produce identical qiyas_core
   results for identical inputs
10. Usage limits MUST block access, NOT degrade quality
```

### 6.2 Governing Law

The core constitutional principle:

```text
الدفع يفتح الوصول، لكنه لا يغيّر الحقيقة التحليلية.

Payment opens access, but does not alter analytical truth.

Subscription grants usage rights, NOT epistemological authority.

Billing tier determines limits, NOT qiyas outcomes.
```

Algebraic parallel to existing qiyas_core laws:

```text
LCNV law: الرقم لا ينتج معرفة
          (Numbers don't produce knowledge)

Billing law: الدفع لا ينتج حقيقة
             (Payment doesn't produce truth)
```

### 6.3 Identity Preservation Across Tiers

Given identical input text `T`, the following MUST be preserved across all subscription tiers:

```text
For all tiers ∈ {Free, Scholar, Pro, Enterprise}:
  qiyas_core(T, tier_free).identity_ids
  = qiyas_core(T, tier_enterprise).identity_ids

  qiyas_core(T, tier_free).evidence.rank
  = qiyas_core(T, tier_enterprise).evidence.rank

  qiyas_core(T, tier_free).residuals
  = qiyas_core(T, tier_enterprise).residuals
```

The ONLY differences permitted across tiers:

```text
- Number of analyses allowed per period
- Access to API
- Access to batch processing
- Export format availability
- Trace detail level (abbreviated vs. full)
- Support response time
- Storage limits
```

---

## 7. Payment Providers (Future)

### 7.1 Target Payment Providers

This contract does NOT implement payment providers. It only declares future options:

**Global:**
- Stripe (recommended for SaaS recurring billing)
- PayPal (backup for global users)

**Arabic/Gulf region:**
- Tap Payments (Saudi Arabia, UAE, Kuwait)
- Moyasar (Saudi Arabia)
- HyperPay (MENA region)

**Additional:**
- Bank transfer (for Enterprise contracts)
- Invoice-based billing (for institutions)

### 7.2 Implementation Sequence

Payment provider integration is **NOT** part of PR-B1, PR-B2, or PR-B3.

It will be implemented in **PR-B4** (Payment Provider Adapter) ONLY after:
1. ✅ PR-B1: Billing architecture contract (this document)
2. ✅ PR-B2: Entitlements runtime (Plan, Entitlement models)
3. ✅ PR-B3: Usage metering runtime (analysis_count tracking)
4. ⏳ PR-B4: Payment provider adapter (Stripe/Tap checkout)

---

## 8. Implementation Sequence

### 8.1 Phase 1: Constitutional Foundation

**PR-B1: Billing Architecture Contract (this PR)**

```text
Scope: docs-only
Files: docs/product/BILLING_ARCHITECTURE_CONTRACT.md
Changes: Zero code, zero tests, zero src/ changes
```

### 8.2 Phase 2: Entitlements Runtime

**PR-B2: Subscription Entitlement Model**

```text
Scope: Runtime models only, no payment integration
Files:
  src/product/__init__.py
  src/product/entitlements.py
  tests/product/test_entitlements.py

Implements:
  - Plan dataclass
  - Entitlement dataclass
  - UsageLimit dataclass
  - FeatureFlag checks

Does NOT implement:
  - Payment provider integration
  - Checkout flows
  - Subscription creation API
  - User authentication
```

### 8.3 Phase 3: Usage Metering

**PR-B3: Qiyas Analysis Usage Metering**

```text
Scope: Track usage units, no billing enforcement yet
Files:
  src/product/usage_metering.py
  tests/product/test_usage_metering.py

Implements:
  - qiyas_analysis_count tracking
  - api_calls tracking
  - batch_jobs tracking
  - trace_audit_requests tracking
  - export_reports tracking

Does NOT implement:
  - Payment charging
  - Subscription enforcement
  - Access blocking (only tracking)
```

### 8.4 Phase 4: Payment Adapter

**PR-B4: Payment Provider Checkout Adapter**

```text
Scope: Stripe or Tap checkout integration
Files:
  src/product/billing/stripe_adapter.py (or tap_adapter.py)
  src/product/billing/checkout.py
  tests/product/billing/test_checkout.py

Implements:
  - Subscription creation
  - Payment method handling
  - Webhook processing
  - Subscription status sync

Requires:
  - PR-B2 entitlements exist
  - PR-B3 usage metering exists
```

### 8.5 Phase 5: Admin Dashboard (Future)

**PR-B5: Billing Admin Dashboard**

```text
Scope: Admin interface for subscription management
(Not part of initial billing contract scope)
```

---

## 9. Directory Structure

### 9.1 Proposed Structure

```text
src/
  qiyas_core/              ← remains pure engine (no billing awareness)
    __init__.py
    kernel.py
    typed_codepoint_adapter.py
    letter_coordinate_adapter.py
    haraka_function_adapter.py
    slot_candidate_adapter.py
    slot_geometry_adapter.py
    ...

  product/                 ← new product layer
    __init__.py
    entitlements.py        ← Plan, Tier, UsageLimit (PR-B2)
    usage_metering.py      ← analysis_count, api_calls (PR-B3)
    billing/               ← payment provider adapters (PR-B4)
      __init__.py
      stripe_adapter.py
      tap_adapter.py
      checkout.py

tests/
  qiyas_core/              ← qiyas engine tests (existing)
  product/                 ← product layer tests (new)
    test_entitlements.py
    test_usage_metering.py
    billing/
      test_checkout.py

docs/
  qiyas_core/              ← qiyas constitutional docs (existing)
  product/                 ← product/billing docs (new)
    BILLING_ARCHITECTURE_CONTRACT.md  ← this file
```

### 9.2 Import Rules

**Allowed:**

```python
# Product layer can import from qiyas_core
from qiyas_core import QiyasKernel
from qiyas_core.candidates import SlotCandidate
```

**Forbidden:**

```python
# qiyas_core MUST NEVER import from product
from product.entitlements import Plan  # ❌ FORBIDDEN in qiyas_core
from product.billing import Checkout   # ❌ FORBIDDEN in qiyas_core
```

**Rationale:** qiyas_core is the epistemological engine. It must remain independent of commercial concerns. The product layer **consumes** the engine, but the engine does NOT know about billing.

---

## 10. Testing Requirements

### 10.1 Entitlement Tests (PR-B2)

```python
def test_free_plan_limits():
    """Free plan enforces 50 analyses/month."""
    pass

def test_scholar_plan_enables_full_trace():
    """Scholar plan enables full trace audit."""
    pass

def test_pro_plan_enables_api():
    """Pro plan enables API access."""
    pass

def test_enterprise_custom_limits():
    """Enterprise plan supports custom limits."""
    pass
```

### 10.2 Usage Metering Tests (PR-B3)

```python
def test_analysis_count_increments():
    """qiyas_analysis_count increments on each analysis."""
    pass

def test_api_call_count_increments():
    """api_calls increments on each API request."""
    pass

def test_batch_job_count_increments():
    """batch_jobs increments on batch submission."""
    pass
```

### 10.3 Constitutional Tests (All PRs)

```python
def test_payment_status_does_not_alter_qiyas_results():
    """Payment status MUST NOT alter qiyas_core analysis results."""
    # Given identical input T
    # Free tier analysis and Enterprise tier analysis
    # MUST produce identical identity_ids, rank, residuals
    pass

def test_subscription_tier_does_not_alter_evidence():
    """Subscription tier MUST NOT alter evidence proofs."""
    pass

def test_billing_code_not_in_qiyas_core():
    """No billing imports in qiyas_core modules."""
    # Scan qiyas_core modules for forbidden imports
    pass
```

---

## 11. Migration Path

### 11.1 Current State (Before PR-B1)

```text
✅ qiyas_core exists as pure analysis engine
❌ No product layer
❌ No billing
❌ No subscriptions
❌ No usage metering
❌ No payment providers
```

### 11.2 After PR-B1 (This PR)

```text
✅ qiyas_core exists (unchanged)
✅ Billing architecture contract defined
✅ Customer tiers specified
✅ Constitutional prohibitions declared
❌ No runtime implementation yet
```

### 11.3 After PR-B2 (Entitlements)

```text
✅ qiyas_core exists (unchanged)
✅ Plan/Entitlement models exist
✅ Feature flags defined
❌ No usage tracking yet
❌ No payment integration yet
```

### 11.4 After PR-B3 (Usage Metering)

```text
✅ qiyas_core exists (unchanged)
✅ Entitlements exist
✅ Usage tracking exists (analysis_count, api_calls)
❌ No payment integration yet
❌ No subscription enforcement yet (only tracking)
```

### 11.5 After PR-B4 (Payment Adapter)

```text
✅ qiyas_core exists (unchanged)
✅ Entitlements exist
✅ Usage tracking exists
✅ Payment provider integration exists
✅ Subscription creation/management exists
✅ Full billing system operational
```

---

## 12. Non-Goals (Explicit Exclusions)

### 12.1 Not Part of This Contract

```text
❌ User authentication system
❌ User account management
❌ Password reset flows
❌ OAuth/SSO integration
❌ Admin dashboard UI
❌ Customer billing portal
❌ Invoice generation
❌ Tax calculation
❌ Refund processing
❌ Coupon/discount system
❌ Affiliate program
❌ Usage analytics dashboard
```

These MAY be added in future PRs, but are NOT part of the billing architecture contract scope.

### 12.2 Not Part of PR-B1 (This PR)

```text
❌ Runtime code (src/product/)
❌ Tests (tests/product/)
❌ Payment provider integration
❌ Database schema
❌ API endpoints
❌ Webhooks
❌ Subscription management UI
```

This PR is **docs-only**. Implementation comes in PR-B2+.

---

## 13. Appendix: Terminology

### 13.1 Billing Terms

| Term | Definition |
|------|------------|
| **Plan** | Subscription tier (Free, Scholar, Pro, Enterprise) |
| **Entitlement** | Feature access granted by a plan |
| **Usage Unit** | Metered analytical operation (qiyas_analysis_count, api_calls, etc.) |
| **Usage Limit** | Maximum allowed usage per billing period |
| **Billing Period** | Time window for usage tracking (monthly or annual) |
| **Payment Provider** | External service handling payments (Stripe, Tap, etc.) |
| **Checkout** | Payment flow for subscribing to a plan |
| **Subscription** | Active plan with payment method |

### 13.2 Qiyas Core Terms (For Reference)

| Term | Definition | Billing Impact |
|------|------------|----------------|
| **Candidate** | Identity-preserving algebraic result | Payment MUST NOT alter |
| **Evidence** | Proof for qiyas transition | Payment MUST NOT alter |
| **Rank** | Evidence strength level | Payment MUST NOT alter |
| **Residual** | Unprocessed remainder | Payment MUST NOT alter |
| **Trace** | Audit trail of qiyas operations | Payment MAY limit detail level |
| **Gate** | Domain transition requirement | Payment MUST NOT bypass |

---

## 14. Approval and Acceptance Criteria

### 14.1 This Contract is Approved When

```text
✅ Constitutional separation is clear
✅ Customer tiers are defined
✅ Usage units are specified
✅ Plan limits are documented
✅ Constitutional prohibitions are explicit
✅ Implementation sequence is defined
✅ Non-goals are clear
✅ No runtime code is added
✅ No qiyas_core changes are made
```

### 14.2 Follow-Up PRs Can Begin When

```text
✅ PR-B1 (this contract) is merged to main
```

Then:

```text
PR-B2 (Entitlements) can be opened
PR-B3 (Usage Metering) can be opened after PR-B2
PR-B4 (Payment Adapter) can be opened after PR-B3
```

---

## 15. Final Constitutional Declaration

```text
قانون الفصل الدستوري بين المحرك والمنتج:

qiyas_core هو محرك معرفي يسعى للحقيقة التحليلية.
product/billing هي طبقة وصول تجارية تحدد حق الاستخدام.

الدفع يفتح الوصول، لكنه لا يغيّر الحقيقة.
الاشتراك يمنح حق استخدام، لا سلطة معرفية.
الباقة تحدد الحدود، لا تغيّر نتائج qiyas_core.

---

Constitutional Law of Engine-Product Separation:

qiyas_core is an epistemological engine seeking analytical truth.
product/billing is a commercial access layer determining usage rights.

Payment opens access, but does not alter truth.
Subscription grants usage rights, NOT analytical authority.
Billing tier determines limits, NOT qiyas outcomes.
```

---

**End of BILLING_ARCHITECTURE_CONTRACT.md**
