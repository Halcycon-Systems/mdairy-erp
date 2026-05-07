# Architecture and Module Status

This project is organized as a modular Odoo 17 build for dairy societies operations. The current repository already has the right module boundaries and collaboration flow in place, which gives the team a clean starting point without locking anyone into rushed design decisions.

## Working Architecture

The intended flow is:

```text
farmer_management
        ↓
collection_center
        ↓
milk_collection → milk_quality
        ↓
farmer_ledger
        ↓
loans_management
        ↓
deduction_engine
        ↓
payment_period
        ↓
payout_processing
        ↓
mpesa_integration + sms_notifications
```

## Current Module Status

| Module | Status | Expected Scope |
|---|---|---|
| farmer_management | Planned | Farmer profiles, farmer codes, national IDs, MPESA numbers, status tracking, and collection center linkage. |
| collection_center | Planned | Collection center records, center ownership, locations, staffing context, and farmer-to-center assignment. |
| milk_collection | Planned | Daily milk delivery capture, quantity records, pricing snapshots, and gross amount generation. |
| milk_quality | Planned | Milk test results, quality checks, acceptance or rejection rules, and downstream validation control. |
| farmer_ledger | Planned | The core farmer financial ledger for earnings, deductions, loan activity, adjustments, and traceable balances. |
| loans_management | Planned | Loan application handling, approval flow, disbursement tracking, repayment records, and outstanding balance visibility. |
| deduction_engine | Planned | Rule-based deductions for loans, feed recovery, prioritization, partial recovery logic, and farmer-level deduction rules. |
| payment_period | Planned | Payout period setup with start and end dates, lifecycle status, and payout cycle control. |
| payout_processing | Planned | Earnings calculation, deduction application, approvals, final posting, and locking after payout completion. |
| mpesa_integration | Planned | MPESA payout integration, transaction reference tracking, and Daraja-based payment workflow support. |
| sms_notifications | Planned | SMS alerts for milk collection updates, payment confirmations, loan activity, and key farmer notifications. |
| access_control | Planned | Role design for clerks, supervisors, finance teams, admins, and permission boundaries across modules. |
| audit_log | Planned | Traceability for important changes, approvals, financial actions, and key operational activity across the system. |

## What Contributors Should Know

* Most modules are still at scaffold stage, so implementation work should begin with clear scope and small, reviewable feature branches.
* `develop` is the shared working branch.
* Feature work should be done in `feature/*` branches and merged back through pull requests.

## Suggested Working Style

When picking up a module, keep the work small and easy to review:

1. Update the manifest to reflect the module purpose clearly.
2. Add or refine models first.
3. Add security and access rules early.
4. Add views only after the model shape is stable.
5. Leave a short note in `docs\` if your change affects other modules.
