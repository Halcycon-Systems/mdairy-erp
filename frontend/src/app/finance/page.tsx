import { PageHeader, Table, Badge, StatCard, formatKes, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { PayoutBatch } from '@/types';

function stateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'disbursed') return 'success';
  if (state === 'approved') return 'info';
  if (state === 'computed') return 'warning';
  if (state === 'cancelled') return 'danger';
  return 'muted';
}

async function getData() {
  const [batches, disbursed, pending] = await Promise.allSettled([
    searchRead<PayoutBatch>('mdairy.payout.batch', [], [
      'name', 'period_start', 'period_end', 'cooperative_id',
      'payout_count', 'total_gross', 'total_deductions', 'total_net', 'state',
    ], { order: 'period_start desc', limit: 50 }),
    searchCount('mdairy.payout.batch', [['state', '=', 'disbursed']]),
    searchCount('mdairy.payout.batch', [['state', 'in', ['draft', 'computed', 'approved']]]),
  ]);

  return {
    batches: batches.status === 'fulfilled' ? batches.value : [],
    disbursed: disbursed.status === 'fulfilled' ? disbursed.value : 0,
    pending: pending.status === 'fulfilled' ? pending.value : 0,
  };
}

export default async function FinancePage() {
  let data = { batches: [] as PayoutBatch[], disbursed: 0, pending: 0 };
  try {
    data = await getData();
  } catch { /* Odoo unavailable */ }

  const totalGross = data.batches.reduce((s, b) => s + b.total_gross, 0);

  return (
    <div>
      <PageHeader title="Payout Batches" subtitle="Manage periodic farmer payouts" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Batches" value={data.batches.length} icon="📋" color="blue" />
        <StatCard label="Disbursed" value={data.disbursed} icon="✅" color="green" />
        <StatCard label="Pending" value={data.pending} icon="⏳" color="yellow" />
        <StatCard label="Total Gross (shown)" value={formatKes(totalGross)} icon="💰" color="gray" />
      </div>

      <Table
        headers={['Batch', 'Period Start', 'Period End', 'Cooperative', 'Farmers', 'Gross', 'Deductions', 'Net', 'Status']}
        rows={data.batches.map((b) => [
          <span key="n" className="font-mono text-xs">{b.name}</span>,
          <span key="ps">{formatDate(b.period_start)}</span>,
          <span key="pe">{formatDate(b.period_end)}</span>,
          <span key="co">{Array.isArray(b.cooperative_id) ? b.cooperative_id[1] : 'All'}</span>,
          <span key="c">{b.payout_count}</span>,
          <span key="g">{formatKes(b.total_gross)}</span>,
          <span key="d">{formatKes(b.total_deductions)}</span>,
          <span key="ne" className="font-semibold">{formatKes(b.total_net)}</span>,
          <Badge key="s" label={b.state} variant={stateVariant(b.state)} />,
        ])}
        emptyMessage="No payout batches found."
      />

      <p className="mt-4 text-xs text-gray-400">
        💡 Use the Odoo backend to create, approve, and disburse payout batches.
      </p>
    </div>
  );
}
