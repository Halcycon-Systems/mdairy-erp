import { PageHeader, Table, Badge, StatCard, formatKes, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { Payout } from '@/types';

function stateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'paid') return 'success';
  if (state === 'approved') return 'info';
  if (state === 'failed') return 'danger';
  if (state === 'cancelled') return 'muted';
  return 'muted';
}

function payoutIcon(method: string) {
  if (method === 'mpesa') return '📱';
  if (method === 'bank') return '🏦';
  return '💵';
}

async function getData() {
  const [payouts, paidCount, pendingCount] = await Promise.allSettled([
    searchRead<Payout>('mdairy.payout', [], [
      'name', 'farmer_id', 'period_start', 'period_end',
      'total_litres', 'gross_amount', 'total_deductions', 'amount',
      'payout_method', 'mpesa_number', 'state', 'payment_date', 'transaction_reference',
    ], { limit: 50, order: 'period_start desc' }),
    searchCount('mdairy.payout', [['state', '=', 'paid']]),
    searchCount('mdairy.payout', [['state', 'in', ['draft', 'approved']]]),
  ]);

  return {
    payouts: payouts.status === 'fulfilled' ? payouts.value : [],
    paidCount: paidCount.status === 'fulfilled' ? paidCount.value : 0,
    pendingCount: pendingCount.status === 'fulfilled' ? pendingCount.value : 0,
  };
}

export default async function PayoutsPage() {
  let data = { payouts: [] as Payout[], paidCount: 0, pendingCount: 0 };
  try {
    data = await getData();
  } catch { /* Odoo unavailable */ }

  const totalPaid = data.payouts
    .filter((p) => p.state === 'paid')
    .reduce((s, p) => s + p.amount, 0);

  return (
    <div>
      <PageHeader title="Farmer Payouts" subtitle="Individual farmer payment records" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Records" value={data.payouts.length} icon="📑" color="blue" />
        <StatCard label="Paid" value={data.paidCount} icon="✅" color="green" />
        <StatCard label="Pending" value={data.pendingCount} icon="⏳" color="yellow" />
        <StatCard label="Total Paid (shown)" value={formatKes(totalPaid)} icon="💳" color="gray" />
      </div>

      <Table
        headers={['Reference', 'Farmer', 'Period', 'Litres', 'Gross', 'Deductions', 'Net', 'Method', 'Ref No.', 'Status']}
        rows={data.payouts.map((p) => [
          <span key="n" className="font-mono text-xs">{p.name}</span>,
          <span key="f">{Array.isArray(p.farmer_id) ? p.farmer_id[1] : '–'}</span>,
          <span key="pd" className="text-xs">{formatDate(p.period_start)} – {formatDate(p.period_end)}</span>,
          <span key="l">{p.total_litres.toFixed(1)}</span>,
          <span key="g">{formatKes(p.gross_amount)}</span>,
          <span key="d">{formatKes(p.total_deductions)}</span>,
          <span key="ne" className="font-semibold">{formatKes(p.amount)}</span>,
          <span key="m">{payoutIcon(p.payout_method)} {p.payout_method}</span>,
          <span key="tr" className="font-mono text-xs">{p.transaction_reference ?? '–'}</span>,
          <Badge key="s" label={p.state} variant={stateVariant(p.state)} />,
        ])}
        emptyMessage="No payout records found."
      />
    </div>
  );
}
