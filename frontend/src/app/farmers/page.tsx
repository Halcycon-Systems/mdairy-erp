import { PageHeader, Table, Badge, formatDate } from '@/components/ui';
import { searchRead } from '@/lib/odoo';
import type { Farmer } from '@/types';

function stateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'active') return 'success';
  if (state === 'draft') return 'info';
  if (state === 'suspended') return 'warning';
  return 'muted';
}

function payoutIcon(method: string) {
  if (method === 'mpesa') return '📱';
  if (method === 'bank') return '🏦';
  return '💵';
}

async function getFarmers(): Promise<Farmer[]> {
  return searchRead<Farmer>('mdairy.farmer', [], [
    'farmer_code', 'name', 'phone', 'mpesa_number', 'county',
    'cooperative_id', 'collection_centre_id', 'number_of_cows',
    'payout_method', 'state', 'total_collections', 'total_payouts', 'registration_date',
  ], { order: 'farmer_code asc' });
}

export default async function FarmersPage() {
  let farmers: Farmer[] = [];
  try {
    farmers = await getFarmers();
  } catch {
    // Odoo not available in this environment
  }

  return (
    <div>
      <PageHeader
        title="Farmers"
        subtitle={`${farmers.length} registered farmer${farmers.length !== 1 ? 's' : ''}`}
      />
      <Table
        headers={['Code', 'Name', 'Phone', 'County', 'Cooperative', 'Cows', 'Payout', 'Collections (L)', 'Status', 'Registered']}
        rows={farmers.map((f) => [
          <span key="c" className="font-mono text-xs text-gray-500">{f.farmer_code}</span>,
          <span key="n" className="font-medium">{f.name}</span>,
          <span key="p">{f.phone ?? f.mpesa_number ?? '–'}</span>,
          <span key="co">{f.county ?? '–'}</span>,
          <span key="cp">{Array.isArray(f.cooperative_id) ? f.cooperative_id[1] : '–'}</span>,
          <span key="cw">{f.number_of_cows ?? '–'}</span>,
          <span key="pm" title={f.payout_method}>{payoutIcon(f.payout_method)} {f.payout_method}</span>,
          <span key="cl">{(f.total_collections ?? 0).toFixed(1)}</span>,
          <Badge key="s" label={f.state} variant={stateVariant(f.state)} />,
          <span key="r">{formatDate(f.registration_date ?? '')}</span>,
        ])}
        emptyMessage="No farmers found. Add farmers via the Odoo backend."
      />
    </div>
  );
}
