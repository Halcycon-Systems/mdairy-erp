# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| `main` branch | ✅ Active |
| Older releases | ❌ Not supported |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in mDairy ERP, please report it responsibly:

1. **Email the maintainer** directly — include `[SECURITY]` in the subject line.
2. **Provide enough detail** to reproduce the issue:
   - Component affected (Odoo addon, Next.js frontend, Docker config, etc.)
   - Steps to reproduce
   - Potential impact
   - Any suggested fix (optional)
3. **Allow time to respond** — you will receive an acknowledgement within **48 hours** and a resolution timeline within **7 days**.

## What We Ask

- Give us a reasonable amount of time to fix the issue before any public disclosure.
- Do not access or modify other users' data during your research.
- Do not perform denial-of-service attacks.
- Act in good faith.

## Sensitive Areas

The following areas of the codebase handle sensitive data and deserve particular scrutiny:

| Area | Risk |
|---|---|
| `mdairy_mpesa` — Daraja API credentials | MPESA Consumer Key/Secret stored in Odoo config |
| `mdairy_sms` — Gateway credentials | Africa's Talking / Twilio API keys |
| `odoo/config/odoo.conf` | Database password, admin password |
| `docker-compose.yml` | Default credentials (change before production) |
| `frontend/src/lib/odoo.ts` | Odoo session handling and JSON-RPC calls |

## Production Hardening Checklist

Before deploying mDairy ERP to production:

- [ ] Change all default passwords in `docker-compose.yml` and `odoo.conf`
- [ ] Store MPESA and SMS credentials in Odoo's encrypted `ir.config_parameter`, not in plain text
- [ ] Run Odoo and the database on a private network; do not expose port `5432` publicly
- [ ] Enable HTTPS (TLS) in front of both Odoo (port 8069) and the Next.js frontend (port 3000)
- [ ] Set `NEXT_PUBLIC_ODOO_URL` to an internal URL, not a public one, in production
- [ ] Review Odoo's built-in access control lists (ACLs) for each `mdairy.*` model

## Disclosure Policy

Once a fix is released, a security advisory will be published on the [GitHub Security Advisories](https://github.com/kirobi01/mdairy-erp/security/advisories) page. Credit will be given to the reporter unless they prefer to remain anonymous.
