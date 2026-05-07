# MDairy ERP

MDairy ERP is a collaborative Odoo 17 project focused on building a practical and maintainable dairy, farmer and societies management system.

The goal of this project is to provide a centralized platform for managing dairy operations from farmer registration and milk collection all the way to payouts, deductions, MPESA payments, and audit tracking.

This repository is intended for team collaboration and structured module-based development.

---

# Project Vision

The system is designed to support real-world dairy operations by providing:

* Farmer management
* Collection center management
* Daily milk collection
* Milk quality validation
* Financial tracking through farmer ledgers
* Loan management and deductions
* Controlled payout processing
* MPESA payment integration
* SMS notifications
* User roles and audit tracking

The project is built on top of Odoo 17 and reuses core Odoo features where appropriate instead of rebuilding existing functionality.

---

# Core Principles

The project follows a few important design principles:

* All financial activity must pass through the farmer ledger
* Posted financial records should not be editable
* Payouts must follow defined payment periods
* Frontend interfaces should not contain business logic
* Deductions should be rule-based and traceable
* Every important action should be auditable

The intention is to build a clean and scalable system that can grow over time without becoming difficult to maintain.

---

# Project Structure

```text
MDairy-erp/
│
├── custom_addons/
│   ├── farmer_management/
│   ├── collection_center/
│   ├── milk_collection/
│   ├── milk_quality/
│   ├── farmer_ledger/
│   ├── loans_management/
│   ├── deduction_engine/
│   ├── payment_period/
│   ├── payout_processing/
│   ├── mpesa_integration/
│   ├── sms_notifications/
│   ├── access_control/
│   └── audit_log/
│
├── config/
│   └── odoo.conf.example
│
├── docs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

Each developer creates `config\odoo.conf` locally by copying `config\odoo.conf.example`. That local file is intentionally not committed.

---

# Main Modules

## Foundation Modules

### farmer_management

Extends Odoo contacts to support:

* Farmer profiles
* Farmer codes
* National IDs
* MPESA phone numbers
* Farmer status
* Linked collection centers

### collection_center

Manages:

* Collection centers
* Center managers
* Locations
* Linked farmers

### milk_collection

Handles daily milk intake:

* Farmer deliveries
* Quantity tracking
* Pricing snapshots
* Gross amount calculations

---

# Control and Validation Modules

### milk_quality

Handles milk testing and validation:

* Fat percentage
* Density
* Temperature
* Acceptance or rejection status

Rejected milk should not proceed to financial posting.

### farmer_ledger

Acts as the financial source of truth for:

* Milk earnings
* Loan disbursements
* Deductions
* Feed purchases
* Adjustments

All financial flows should pass through this module.

---

# Financial Modules

### loans_management

Handles:

* Loan applications
* Approvals
* Disbursements
* Repayments
* Outstanding balances

### deduction_engine

Responsible for:

* Loan deductions
* Feed recovery deductions
* Rule prioritization
* Partial deductions
* Per-farmer deduction logic

This module is expected to be one of the more complex parts of the system.

---

# Payout Modules

### payment_period

Controls payout cycles using:

* Start dates
* End dates
* Status tracking

### payout_processing

Handles:

1. Earnings calculation
2. Deduction application
3. Approval workflows
4. Final posting and locking

Once payouts are posted, records should become read-only.

---

# Integration Modules

### mpesa_integration

Handles:

* MPESA payouts
* Transaction tracking
* Daraja API integration

### sms_notifications

Handles:

* Milk collection notifications
* Payment confirmations
* Loan updates

---

# System Control Modules

### access_control

Defines system roles such as:

* Clerk
* Supervisor
* Finance
* Admin

### audit_log

Tracks:

* Field changes
* Approval actions
* Loan modifications
* Financial activity changes

---

# Dependency Flow

The modules are expected to integrate in the following order:

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

---

# Development Workflow

This project uses Git and GitHub for collaboration.

## Branch Structure

* main → stable production-ready code
* develop → shared integration branch
* feature/* → individual feature branches

Examples:

* feature/farmer-management
* feature/milk-collection
* feature/ledger-posting

---

# Contributor Workflow

Before starting work:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/module-name
```

After completing work:

```bash
git add .
git commit -m "Describe your changes"
git push origin feature/module-name
```

Then open a Pull Request into `develop`.

Direct pushes to `main` are not allowed.

---

# Local Development Setup

## 1. Expected Local Versions

To keep the team setup predictable, please use:

* Python 3.11
* PostgreSQL 12+ supported by Odoo 17
* PostgreSQL 14+ recommended for this project

You can confirm your versions with:

```bash
python --version
psql --version
```

---

## 2. Clone Odoo 17

Odoo itself is kept outside this repository.

```bash
git clone --depth 1 --branch 17.0 https://github.com/odoo/odoo.git
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure PostgreSQL

```sql
CREATE USER odoo WITH PASSWORD '123@Odoo!';
ALTER USER odoo CREATEDB;
```

---

## 6. Create Your Local Odoo Config

Copy the shared example config:

```bash
copy config\odoo.conf.example config\odoo.conf
```

If you are on Linux or Mac:

```bash
cp config/odoo.conf.example config/odoo.conf
```

Then open `config\odoo.conf` and update:

* `db_password`
* `admin_passwd`

These are local values for your machine, so please keep them out of Git.

---

## 7. Run Odoo

```bash
python ../odoo/odoo-bin -c config/odoo.conf
```

Open:

```text
http://localhost:8069
```

If the server starts and the page opens, your environment is ready and you can begin working from `develop`.

---

# Reused Odoo Features

The project intends to reuse existing Odoo functionality where appropriate:

* Contacts
* Sales
* Inventory
* Accounting
* HR
* Users and permissions
* Chatter and activity tracking

Custom modules should only extend what is necessary.

---

# MVP Goal

The first working version of the system should support:

* Farmer registration
* Daily milk collection
* Milk quality validation
* Farmer earnings tracking
* Loan deductions
* Controlled payout periods
* MPESA payments
* SMS notifications
* Audit tracking

---

# Long-Term Goal

The intention is to build a stable, maintainable, and scalable ERP platform that reflects actual dairy operational workflows while remaining clean enough for long-term development and collaboration.

