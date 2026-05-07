# mDairy ERP

A practical dairy management system built with **Odoo 16** (backend) and **Next.js 15** (frontend).

## Features

| Module | Description |
|--------|-------------|
| 👨‍🌾 **Farmer Records** | Manage farmer profiles, cooperative membership, farm details, and payout preferences |
| 🥛 **Milk Collection** | Record daily milk deliveries by session (morning/evening), quantity, and quality |
| 🔬 **Quality Validation** | Automated milk grading (Grade A/B/C/Rejected) based on fat %, SNF, pH, antibiotics, and adulteration tests |
| 💰 **Financial Processing** | Periodic payout batch computation with deductions (loans, levies, insurance) |
| 💳 **Payouts** | Individual farmer payout records with approval and disbursement workflows |
| 📱 **MPESA Integration** | Safaricom Daraja B2C API for direct MPESA payouts to farmers |
| 💬 **SMS Notifications** | Africa's Talking / Twilio SMS notifications for collection confirmations and payout alerts |

---

## Repository Structure

```
mdairy-erp/
├── odoo/
│   ├── addons/
│   │   ├── mdairy_base/          # Farmer records, cooperatives, collection centres
│   │   ├── mdairy_collection/    # Milk collection & quality tests
│   │   ├── mdairy_finance/       # Payout batches, farmer payouts, deductions
│   │   ├── mdairy_mpesa/         # Safaricom Daraja MPESA B2C integration
│   │   └── mdairy_sms/           # SMS notifications (Africa's Talking / Twilio)
│   └── config/
│       └── odoo.conf             # Odoo server configuration
├── frontend/                     # Next.js 15 dashboard
│   ├── src/
│   │   ├── app/                  # App Router pages
│   │   │   ├── page.tsx          # Dashboard
│   │   │   ├── farmers/          # Farmer list
│   │   │   ├── collection/       # Collection records
│   │   │   ├── quality/          # Quality test results
│   │   │   ├── finance/          # Payout batches
│   │   │   ├── payouts/          # Farmer payouts
│   │   │   └── integrations/     # MPESA & SMS views
│   │   ├── components/           # Shared UI components
│   │   ├── lib/                  # Odoo JSON-RPC client
│   │   └── types/                # TypeScript types
│   └── Dockerfile
└── docker-compose.yml            # Full-stack development environment
```

---

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker + Compose)

### 1. Start the full stack

```bash
docker compose up -d
```

This starts:
- **PostgreSQL** on port `5432`
- **Odoo 16** on port `8069`
- **Next.js frontend** on port `3000`

### 2. Initialize Odoo

1. Open http://localhost:8069
2. Create a new database named `mdairy`
3. Install the modules in order:
   - `mDairy Base`
   - `mDairy Milk Collection`
   - `mDairy Finance & Payouts`
   - `mDairy MPESA Integration`
   - `mDairy SMS Notifications`

### 3. Open the dashboard

Navigate to http://localhost:3000

---

## Development

### Odoo Backend

```bash
# Run with hot-reload (requires local Odoo install)
cd odoo
odoo -c config/odoo.conf --dev=all

# Run tests
odoo -c config/odoo.conf --test-enable -u mdairy_base,mdairy_collection,mdairy_finance
```

### Next.js Frontend

```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build
npm start

# Lint
npm run lint
```

Set `NEXT_PUBLIC_ODOO_URL` in `frontend/.env.local` to point to your Odoo instance:

```env
NEXT_PUBLIC_ODOO_URL=http://localhost:8069
NEXT_PUBLIC_ODOO_DB=mdairy
```

---

## Module Details

### mdairy_base
- `mdairy.farmer` – Farmer profile with GPS, farm details, payout method
- `mdairy.cooperative` – Cooperative registration and management
- `mdairy.collection.centre` – Physical collection points

### mdairy_collection
- `mdairy.collection` – Per-delivery milk records (session, quantity, grade, price)
- `mdairy.quality.test` – Lab quality parameters (fat, SNF, pH, antibiotics, adulteration)
- `mdairy.collection.price` – Dynamic pricing configuration by cooperative/grade

### mdairy_finance
- `mdairy.payout.batch` – Batch payout computation (Draft → Computed → Approved → Disbursed)
- `mdairy.payout` – Individual farmer payout with deduction breakdown
- `mdairy.deduction` – Fixed, percentage, or loan-repayment deduction rules

### mdairy_mpesa
- `mdairy.mpesa.config` – Daraja API credentials (Consumer Key, Secret, Shortcode)
- `mdairy.mpesa.transaction` – B2C payment tracking with callback handling

### mdairy_sms
- `mdairy.sms.config` – Gateway settings (Africa's Talking / Twilio / Custom HTTP)
- `mdairy.sms.template` – Reusable message templates with variable substitution
- `mdairy.sms.message` – Delivery log

---

## Configuration

### MPESA (Safaricom Daraja)

1. Register at [Safaricom Developer Portal](https://developer.safaricom.co.ke)
2. Create a B2C app and note **Consumer Key**, **Consumer Secret**, and **Shortcode**
3. In Odoo: **Integrations → MPESA Configuration → New**
4. Set environment to `Sandbox` for testing or `Production` for live

### SMS

**Africa's Talking:**
1. Sign up at [africastalking.com](https://africastalking.com)
2. In Odoo: **Integrations → SMS Configuration → New**
3. Select provider `Africa's Talking`, enter username and API key

**Twilio:**
1. Sign up at [twilio.com](https://www.twilio.com)
2. In Odoo: **Integrations → SMS Configuration → New**
3. Select provider `Twilio`, enter Account SID, Auth Token, and From number

---

## License

LGPL-3 (Odoo modules) / MIT (Next.js frontend)
