# Odoo Architecture Overview

This project is built as a set of custom Odoo modules for dairy societies operations. Odoo provides the application framework, database layer, user interface, permissions, and workflow engine. The modules in `custom_addons\` extend that foundation with dairy-specific business processes.

## Architecture at a Glance

```text
Odoo Core
├── Base models and ORM
├── Web interface
├── Menus, actions, and views
├── User groups and access control
├── Messaging and activity tracking
└── Standard business modules

MDairy Custom Modules
├── farmer_management
├── collection_center
├── milk_collection
├── milk_quality
├── farmer_ledger
├── loans_management
├── deduction_engine
├── payment_period
├── payout_processing
├── mpesa_integration
├── sms_notifications
├── access_control
└── audit_log
```

## Why the Project Is Structured This Way

This architecture keeps the project aligned with standard Odoo development:

* Odoo handles the common platform concerns such as models, forms, lists, menus, permissions, and workflows.
* Custom modules focus only on dairy business rules and process-specific data.
* Separate modules make the codebase easier to maintain, test, review, and extend over time.
* Module boundaries help the team work in parallel without mixing unrelated business logic.

## How Odoo Connects to This Repository

Odoo loads add-ons from the paths defined in `config\odoo.conf`:

```ini
addons_path = ../odoo/addons,custom_addons
```

This means:

* `../odoo/addons` loads the standard Odoo modules.
* `custom_addons` loads the MDairy project modules.

When the Odoo server starts, it reads both locations and registers all installed modules in the same application.

## Reusing Free OCA Modules

Before building a feature from scratch, contributors should first review free modules from the **Odoo Community Association (OCA)**. OCA modules are community-maintained add-ons that often cover common technical and business needs and can reduce custom development.

Useful OCA areas to review for this project include:

* **partner-contact** - useful when extending partner and contact management for farmer records
* **server-tools** - useful for technical helpers, automation, and administration support
* **queue** - useful for background jobs such as SMS delivery or payment processing tasks
* **audit-log** - useful if the project needs stronger reusable audit tracking patterns
* **connector** - useful when integrating with external services such as MPESA or other APIs
* **bank-payment** and related finance modules - useful when reviewing payment processing patterns

OCA modules are not a replacement for the dairy-specific business logic in this repository, but they should be considered whenever they can provide a stable base for shared functionality.

## What an Odoo Module Contains

Each custom module usually has the following parts:

* `__manifest__.py` - module metadata, dependencies, and files to load
* `models/` - Python models and business logic
* `views/` - XML form, list, search, and menu definitions
* `security/` - access rights and user group rules
* `demo/` or `data/` - optional starter or sample records

Together, these parts define how a business feature behaves in Odoo.

## How Modules Connect to Each Other

Modules connect in three main ways:

### 1. Dependency Connection

A module can depend on another module in `__manifest__.py`.

Example:

```python
'depends': ['base', 'farmer_management']
```

This tells Odoo that one module must be available before another can be installed or used.

### 2. Data Connection

Modules connect records through Odoo relational fields such as:

* `Many2one`
* `One2many`
* `Many2many`

Example:

* a milk collection record links to one farmer
* a farmer links to one collection center
* a ledger entry links to one farmer

### 3. Workflow Connection

One module can trigger actions in another module as part of the business process.

Example:

* a validated milk collection can create a farmer ledger entry
* a payout run can read ledger balances and deduction rules
* an approved payout can trigger MPESA and SMS steps

## Functional Flow

The intended module flow is:

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

## What the Main Modules Are Expected to Do

### farmer_management

Extends farmer-related information such as farmer code, identification details, contact information, and operational status.

### collection_center

Defines collection centers and links farmers to their working center.

### milk_collection

Captures daily milk delivery records, quantities, and pricing references.

### milk_quality

Stores quality results and determines whether a collection can proceed into finance-related processes.

### farmer_ledger

Acts as the main financial record for farmer earnings, deductions, adjustments, and balances.

### loans_management

Handles loan records, approvals, disbursements, repayments, and outstanding balances.

### deduction_engine

Applies the rules used to calculate loan recovery, feed recovery, and other deductions.

### payment_period

Defines payout cycles and controls which records belong to a given payment window.

### payout_processing

Calculates final payout values, handles approvals, and posts completed payout results.

### mpesa_integration

Connects approved payouts to MPESA payment processing and transaction tracking.

### sms_notifications

Sends operational notifications such as payment confirmations and collection-related updates.

### access_control

Defines who can create, approve, edit, post, or review records across the project.

### audit_log

Provides traceability for important changes, approvals, and financial actions.

## Where the User Interface Comes From

The primary interface comes from Odoo itself. Internal users work through Odoo's built-in web application using:

* menu items
* list views
* form views
* search views
* action buttons
* reports

This means the project does not need a separate frontend for core internal operations. A separate frontend would only be needed for specific external-facing experiences such as a public portal or mobile-first self-service application.

## Development Approach

For each module, implementation should normally follow this order:

1. Define the business model and relationships.
2. Add the required security groups and access rights.
3. Create list, form, and search views.
4. Add workflow states, validations, and business rules.
5. Connect the module to upstream and downstream modules.

## Summary

The project is not a standalone application outside Odoo. It is an Odoo-based ERP solution where custom dairy modules plug into Odoo's standard platform and work together through dependencies, shared models, and business workflows.
