# Contributing to mDairy ERP

Thank you for your interest in contributing! mDairy ERP is an open-source dairy management system for small and medium cooperatives. Every contribution — code, documentation, bug reports, or ideas — is welcome.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Commit Message Convention](#commit-message-convention)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Pull Request Checklist](#pull-request-checklist)
9. [Reporting Bugs](#reporting-bugs)
10. [Requesting Features](#requesting-features)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to uphold these standards. Please report unacceptable behaviour to the maintainers.

---

## Getting Started

### Prerequisites

| Tool | Minimum Version |
|---|---|
| Docker Desktop | 24+ |
| Node.js | 20 LTS |
| Python | 3.10+ |
| Git | 2.40+ |

### 1. Fork and clone the repository

```bash
git clone https://github.com/<your-username>/mdairy-erp.git
cd mdairy-erp
```

### 2. Start the full stack

```bash
docker compose up -d
```

This brings up:
- **PostgreSQL 15** on port `5432`
- **Odoo 16** on port `8069`
- **Next.js 15 frontend** on port `3000`

### 3. Initialise Odoo

1. Open http://localhost:8069
2. Create a database named `mdairy` (master password: `odoo`)
3. Install the modules in order: `mDairy Base` → `mDairy Milk Collection` → `mDairy Finance & Payouts` → `mDairy MPESA Integration` → `mDairy SMS Notifications`

### 4. Run the frontend in development mode

```bash
cd frontend
cp .env.local.example .env.local   # then edit if needed
npm install
npm run dev
```

Open http://localhost:3000.

---

## How to Contribute

1. **Browse open issues** — look for issues labelled `good first issue` or `help wanted`.
2. **Comment on the issue** you want to work on so maintainers can assign it to you.
3. **Fork** the repository and create a branch (see [Development Workflow](#development-workflow)).
4. **Open a pull request** against `main` once your work is ready.

---

## Development Workflow

```
main           ← protected; only merges via pull request
  └── feature/<short-description>   ← your work branch
  └── fix/<issue-id>-short-desc
  └── docs/<what-you-are-documenting>
  └── chore/<maintenance-task>
```

### Creating a branch

```bash
git checkout -b feature/sms-bulk-send
```

### Keeping your branch up to date

```bash
git fetch origin
git rebase origin/main
```

### Submitting

Push your branch and open a pull request:

```bash
git push origin feature/sms-bulk-send
```

---

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

**Types**

| Type | When to use |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructure, no behaviour change |
| `test` | Adding or fixing tests |
| `chore` | Build scripts, CI, dependencies |
| `security` | Security-related changes |

**Scope** (optional) — the affected area, e.g. `base`, `collection`, `finance`, `mpesa`, `sms`, `frontend`.

**Examples**

```
feat(collection): add bulk import from CSV
fix(mpesa): handle timeout on B2C callback
docs: update CONTRIBUTING guide
test(finance): add deduction computation tests
security(mpesa): rotate API credentials storage to ir.config_parameter
```

---

## Coding Standards

### Python (Odoo addons)

- Follow [PEP 8](https://peps.python.org/pep-0008/) and Odoo coding guidelines.
- All models must include `_name`, `_description`, and `_order`.
- Use `_()` for all user-visible strings (i18n).
- Raise `ValidationError` for field-level constraints and `UserError` for business-logic errors.
- Add `tracking=True` on fields that benefit from the chatter log.
- Do not hard-code credentials — use `ir.config_parameter` or model fields.

### TypeScript / Next.js (frontend)

- Use **TypeScript strict mode** — no `any` unless truly unavoidable.
- Pages are **async Server Components** by default; only opt into `'use client'` when you need browser APIs or state.
- All data fetching goes through `src/lib/odoo.ts` helpers.
- Shared UI primitives belong in `src/components/ui.tsx`; page-specific markup stays in the page file.
- Run `npm run lint` and `npx tsc --noEmit` — both must pass before raising a PR.

### General

- Do not commit secrets, credentials, or `.env` files.
- Keep functions small and focused; prefer readability over cleverness.
- Delete dead code rather than commenting it out.

---

## Testing

### Odoo unit tests

```bash
# From inside the Odoo container or with a local Odoo install:
odoo -c odoo/config/odoo.conf --test-enable -u mdairy_base,mdairy_collection,mdairy_finance
```

Every new model method or business-logic change must be accompanied by at least one test in the corresponding `tests/` folder.

### Frontend

The frontend currently relies on Next.js build-time type checking and ESLint:

```bash
cd frontend
npm run build   # fails loudly on TypeScript or compilation errors
npm run lint    # ESLint must report zero errors
```

If you add client-side logic, add unit tests using the project's test framework once one is adopted (tracked in [#TODO issue link]).

---

## Pull Request Checklist

Before marking your PR as "Ready for review":

- [ ] Branch is up to date with `main`
- [ ] `npm run lint` passes (frontend)
- [ ] `npx tsc --noEmit` passes (frontend)
- [ ] `npm run build` passes (frontend)
- [ ] Odoo tests pass for affected modules
- [ ] New code is covered by tests (models, business logic)
- [ ] No secrets or credentials committed
- [ ] Commit messages follow the [Conventional Commits](#commit-message-convention) format
- [ ] PR description explains **what** and **why** (not just what the diff shows)
- [ ] Screenshots included for any UI changes

---

## Reporting Bugs

Use the **Bug Report** issue template. Please include:

- Steps to reproduce
- Expected vs. actual behaviour
- Your environment (OS, Docker version, Odoo version if local)
- Relevant logs (redact any sensitive data)

---

## Requesting Features

Use the **Feature Request** issue template. Please describe:

- The problem you are trying to solve
- Your proposed solution (or alternative approaches)
- Any constraints specific to Kenyan dairy cooperatives or mobile-money systems

---

## Questions?

Open a [Discussion](https://github.com/kirobi01/mdairy-erp/discussions) rather than an issue for general questions. This keeps the issue tracker focused on actionable bug reports and feature requests.
