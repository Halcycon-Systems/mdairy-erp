# kwdhs Dairy ERP (Odoo 17)
## (kwdhs -KARIBUWEBDEV-HALCYCON SYSTEMS)

Enterprise-grade Dairy Management & Financial Settlement Platform built on Odoo 17.

---

# 1. PROJECT VISION

kwdhs Dairy ERP is NOT just a milk collection system.

It is designed as a:

> Controlled dairy operations, financial settlement, and farmer payout platform.

The architecture prioritizes:

- Financial integrity
- Traceability
- Controlled payout processing
- Modular scalability
- Long-term maintainability
- Enterprise-grade orchestration

The system is intentionally designed using layered architecture and modular domain separation.

---

# 2. CORE ARCHITECTURAL PRINCIPLE

## Operational Transactions Are Temporary
## Ledger Postings Are Truth

This principle governs the entire system.

Examples:

| Activity | Type |
|---|---|
| Milk collection | Operational |
| Quality testing | Operational |
| Loan application | Operational |
| Payout calculation | Operational |
| Ledger posting | Financial truth |
| Posted payout | Financial truth |

Nothing becomes financially authoritative until it is posted into the ledger.

---

# 3. SYSTEM ARCHITECTURE

The system is divided into independent layers.

---

# LAYER 1 — FOUNDATION / FRAMEWORK

Module:
- `kwdhs_dairy_base`

Purpose:
- Shared infrastructure
- Abstract mixins
- Shared utilities
- Sequences
- Common behaviors

This module contains NO business domain logic.

---

# LAYER 2 — OPERATIONAL CORE

Module:
- `kwdhs_dairy_core`

Purpose:
- Farmer management
- Collection centers
- Milk collection
- Milk quality
- Product pricing

This layer manages operational transactions.

---

# LAYER 3 — FINANCIAL ENGINE

Modules:
- `kwdhs_dairy_finance`
- `kwdhs_dairy_loans`
- `kwdhs_dairy_deductions`

Purpose:
- Ledger management
- Financial balances
- Loans
- Deductions
- Financial calculations

This is the HEART of the system.

---

# LAYER 4 — SETTLEMENT ENGINE

Modules:
- `kwdhs_dairy_payouts`

Purpose:
- Payment periods
- Payout processing
- Approval workflow
- Posting
- Freezing payouts

This layer controls all farmer settlements.

---

# LAYER 5 — INTEGRATIONS

Modules:
- `kwdhs_dairy_integrations`

Purpose:
- Mpesa integration
- SMS notifications
- External APIs

External communication belongs ONLY here.

---

# LAYER 6 — GOVERNANCE

Modules:
- `kwdhs_dairy_security`
- `kwdhs_dairy_audit`

Purpose:
- Access control
- Audit logs
- Approval tracking
- Record tracking

---

# LAYER 7 — PRESENTATION/UI

Module:
- `kwdhs_dairy_app`

Purpose:
- Menus
- Views
- Dashboards
- Navigation
- Reports
- User experience

This layer MUST NOT contain critical business logic.

---

# 4. MODULE DEPENDENCY FLOW

The dependency flow is STRICT.

```text
kwdhs_dairy_base
        ↓
kwdhs_dairy_core
        ↓
kwdhs_dairy_finance
        ↓
kwdhs_dairy_loans
        ↓
kwdhs_dairy_deductions
        ↓
kwdhs_dairy_payouts
        ↓
kwdhs_dairy_integrations
        ↓
kwdhs_dairy_app
```

IMPORTANT:
Dependencies must always flow downward.

Never create circular dependencies.

---

# 5. ODOO CORE MODULE STRATEGY

We DO NOT rebuild existing Odoo functionality.

We EXTEND strategically.

---

# STANDARD ODOO MODULES USED

| Odoo Module | Purpose |
|---|---|
| base | Core ORM |
| contacts | Farmer contact extension |
| account | Accounting backbone |
| sale | Milk/feed sales |
| stock | Inventory |
| purchase | Procurement |
| hr | Staff management |
| mail | Chatter/workflow |

---

# 6. MODEL EXTENSION STRATEGY

Understanding what extends what is CRITICAL.

---

# 6.1 Farmer Model

## Extends:
`res.partner`

Reason:
A farmer is fundamentally a specialized contact.

Benefits:
- Built-in addresses
- Phone/email handling
- Accounting integration
- Messaging
- Portal support
- Future invoicing/payment support

Implementation:

```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
```

Additional dairy-specific fields are added here.

IMPORTANT:
We DO NOT create a separate farmer master table initially.

---

# 6.2 Collection Centers

## Independent Model

Model:
`kwdhs.collection.center`

Reason:
Collection centers are dairy-domain entities unique to this system.

Implementation:

```python
class CollectionCenter(models.Model):
    _name = 'kwdhs.collection.center'
```

Relationship:
- One center → many farmers

---

# 6.3 Milk Collection

## Independent Transactional Model

Model:
`kwdhs.milk.collection`

Purpose:
Daily milk intake transactions.

This is a transactional model.

IMPORTANT:
Milk collection records are operational records, NOT direct financial postings.

---

# 6.4 Milk Quality

## Extends Milk Collection Functionally

Model:
`kwdhs.milk.quality`

Relationship:
- One quality record → one milk collection

Purpose:
Validation and acceptance control.

IMPORTANT:
Rejected quality tests must block financial posting.

---

# 6.5 Farmer Ledger

## Independent Financial Truth Model

Model:
`kwdhs.farmer.ledger`

Purpose:
Single source of financial truth.

ALL financial movements MUST pass through the ledger.

Examples:
- Milk earnings
- Loan disbursement
- Feed deductions
- Loan recovery
- Adjustments

IMPORTANT:
No manual edits after posting.

---

# 6.6 Loans

## Independent Financial Workflow

Model:
`kwdhs.loan`

Depends on:
- Farmer
- Ledger

Purpose:
Loan lifecycle management.

Loan posting creates ledger entries.

---

# 6.7 Deduction Engine

## Independent Rule Engine

Purpose:
Centralized deduction computation.

Handles:
- Loan deductions
- Feed recovery
- Custom deductions

Architecture:
Strategy pattern.

IMPORTANT:
Never hardcode deductions inside payout logic.

---

# 6.8 Payment Periods

## Independent Settlement Control Model

Model:
`kwdhs.payment.period`

Purpose:
Controlled payout windows.

Status Flow:
- Draft
- Open
- Closed
- Paid

No ad-hoc payouts allowed outside periods.

---

# 6.9 Payout Processing

## Orchestration Engine

Purpose:
Coordinates:
- Gross earnings
- Deductions
- Approvals
- Posting
- Freezing

This module orchestrates multiple modules together.

---

# 6.10 Mpesa Integration

## External Integration Layer

Purpose:
- Send payments
- Receive transaction references
- Sync statuses

IMPORTANT:
External APIs must NEVER contain core financial logic.

---

# 7. CORE DESIGN RULES

---

# RULE 1 — LEDGER IS KING

If the ledger is correct:
- balances are correct
- payouts are correct
- reports are correct

The ledger is the financial truth source.

---

# RULE 2 — NO DIRECT PAYMENTS FROM COLLECTIONS

INVALID:

```text
Milk Collection → Payment
```

CORRECT:

```text
Milk Collection
    ↓
Ledger Earnings
    ↓
Payment Period
    ↓
Payout Processing
    ↓
Mpesa Payment
```

---

# RULE 3 — EVERYTHING GOES THROUGH PERIODS

No:
- ad-hoc farmer payouts
- random settlements
- manual recalculations

All settlements belong to payment periods.

---

# RULE 4 — POSTED RECORDS BECOME IMMUTABLE

Posted records:
- cannot be edited
- cannot be deleted

Protected models:
- Ledger entries
- Posted payouts
- Posted loans
- Posted collections

---

# RULE 5 — SNAPSHOT IMPORTANT VALUES

Example:
Milk collection MUST store:
- price snapshot

Never dynamically recompute historical prices.

Historical financial integrity is critical.

---

# RULE 6 — BUSINESS LOGIC BELONGS IN SERVICES

DO NOT place complex business logic directly inside views or button methods.

Preferred structure:

```text
services/
    ledger_service.py
    payout_service.py
    deduction_service.py
```

Benefits:
- Testability
- Reusability
- Clean architecture

---

# RULE 7 — UI MODULES MUST NOT OWN CORE LOGIC

`kwdhs_dairy_app` should only contain:
- menus
- forms
- tree views
- reports
- dashboards

Core business rules belong to core modules.

---

# 8. STATE MACHINE DESIGN

All critical financial models must use explicit states.

---

# Example — Loans

```text
draft
↓
approved
↓
disbursed
↓
closed
```

---

# Example — Payouts

```text
draft
↓
review
↓
approved
↓
posted
↓
paid
```

---

# 9. LOCKING STRATEGY

Shared locking behavior is implemented through:

```python
kwdhs.state.lock.mixin
```

This prevents:
- modification
- deletion

after posting/locking.

---

# 10. NAMING CONVENTIONS

Consistency is mandatory.

---

# Module Names

```text
kwdhs_dairy_core
kwdhs_dairy_finance
kwdhs_dairy_loans
```

---

# Model Names

```text
kwdhs.collection.center
kwdhs.milk.collection
kwdhs.farmer.ledger
kwdhs.loan
kwdhs.payment.period
```

---

# XML IDs

```text
view_kwdhs_collection_center_form
action_kwdhs_milk_collection
menu_kwdhs_finance_root
```

---

# Sequence Codes

```text
kwdhs.farmer.code
kwdhs.loan.sequence
kwdhs.payment.period
```

---

# 11. RECOMMENDED DEVELOPMENT ORDER

---

# PHASE 1 — FOUNDATION

1. kwdhs_dairy_base
2. kwdhs_dairy_core

---

# PHASE 2 — FINANCIAL CORE

3. kwdhs_dairy_finance
4. kwdhs_dairy_loans
5. kwdhs_dairy_deductions

---

# PHASE 3 — SETTLEMENT ENGINE

6. kwdhs_dairy_payouts

---

# PHASE 4 — AUTOMATION

7. kwdhs_dairy_integrations

---

# PHASE 5 — UI & REPORTING

8. kwdhs_dairy_app

---

# 12. MVP DEFINITION

The MVP is NOT dashboards or reports.

The MVP is:

- Milk collected correctly
- Ledger accurate
- Deductions applied correctly
- Payouts frozen correctly
- Mpesa reconciliation successful

If those work:
the platform works.

---

# 13. LONG-TERM EXTENSIBILITY

The architecture is intentionally designed to support future expansion:

Future possibilities:
- Mobile app
- Farmer portal
- AI forecasting
- Milk route optimization
- Multi-branch cooperatives
- SACCO integration
- Insurance integrations
- Automated accounting sync
- BI dashboards

Because business logic is modularized, these additions can happen safely.

---

# 14. FINAL ARCHITECTURAL PHILOSOPHY

The system is designed around:

- Financial integrity
- Immutability
- Traceability
- Controlled settlement
- Modular extensibility

The primary goal is not rapid feature addition.

The primary goal is:
A stable, auditable, enterprise-grade dairy ERP platform.
