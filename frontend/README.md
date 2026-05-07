# mDairy ERP — Frontend

The management dashboard for mDairy ERP, built with **Next.js 15** (App Router), **Tailwind CSS**, and **TypeScript**. It communicates with the Odoo 16 backend via a thin JSON-RPC client.

## Pages

| Route | Description |
|---|---|
| `/` | Dashboard — live stats, recent collections, pending payout batches |
| `/farmers` | Farmer list |
| `/collection` | Milk collection records with quality grade badges |
| `/quality` | Lab quality test results and pass-rate summary |
| `/finance` | Payout batch list with workflow state badges |
| `/payouts` | Per-farmer payout records |
| `/integrations/mpesa` | MPESA B2C transaction log |
| `/integrations/sms` | SMS delivery log |

All pages degrade gracefully when the Odoo backend is unreachable (empty-state tables, no crash).

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/
│   │   ├── Sidebar.tsx   # Navigation sidebar
│   │   └── ui.tsx        # Shared UI primitives (StatCard, Table, Badge, …)
│   ├── lib/
│   │   └── odoo.ts       # Odoo JSON-RPC client (searchRead, searchCount, …)
│   └── types/
│       └── index.ts      # TypeScript types mirroring Odoo models
├── Dockerfile            # Multi-stage production image
├── next.config.mjs
├── tailwind.config.ts
└── tsconfig.json
```

## Local Development

**Prerequisites:** Node.js ≥ 20

```bash
# Install dependencies
npm install

# Start dev server (hot-reload)
npm run dev
```

Open http://localhost:3000.

### Environment Variables

Create `frontend/.env.local` (git-ignored):

```env
NEXT_PUBLIC_ODOO_URL=http://localhost:8069
NEXT_PUBLIC_ODOO_DB=mdairy
```

If Odoo is not running locally, all pages render in empty-state mode automatically.

## Building for Production

```bash
npm run build   # outputs a standalone Next.js build
npm start       # serve the production build
```

The `output: 'standalone'` setting in `next.config.mjs` produces a self-contained `server.js` file used by the Docker image.

## Docker

Built automatically by `docker compose up` from the repository root. The `Dockerfile` uses a two-stage build (Node 20 builder → lightweight runner) and runs as a non-root user.

## Linting & Type-Checking

```bash
npm run lint        # ESLint via eslint-config-next
npx tsc --noEmit   # TypeScript strict type check
```

Both checks must pass before opening a pull request.

## Adding a New Page

1. Create `src/app/<route>/page.tsx` as an `async` Server Component.
2. Fetch data with helpers from `src/lib/odoo.ts` (`searchRead`, `searchCount`).
3. Wrap content in a `try/catch` so the page renders gracefully when Odoo is offline.
4. Add the route to the `NAV` array in `src/components/Sidebar.tsx`.
5. Export any new TypeScript types from `src/types/index.ts`.
