import { StatCard, Table, Badge, formatKes, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { CollectionRecord, PayoutBatch } from '@/types';

async function getDashboardData() {
  const today = new Date().toISOString().split('T')[0];

  const [
    totalFarmers,
    activeFarmers,
    todayCollections,
    pendingBatches,
    recentCollections,
  ] = await Promise.allSettled([
    searchCount('mdairy.farmer', []),
    searchCount('mdairy.farmer', [['state', '=', 'active']]),
    searchRead<CollectionRecord>('mdairy.collection', [['collection_date', '=', today]], [
      'name', 'farmer_id', 'quantity_litres', 'quality_grade', 'amount_due', 'state',
    ]),
    searchRead<PayoutBatch>('mdairy.payout.batch', [['state', 'in', ['draft', 'computed', 'approved']]], [
      'name', 'period_start', 'period_end', 'payout_count', 'total_net', 'state',
    ], { limit: 5 }),
    searchRead<CollectionRecord>('mdairy.collection', [], [
      'name', 'collection_date', 'session', 'farmer_id', 'quantity_litres', 'quality_grade', 'amount_due', 'state',
    ], { limit: 10, order: 'collection_date desc, id desc' }),
  ]);

  const todayCols = todayCollections.status === 'fulfilled' ? todayCollections.value : [];
  const todayLitres = todayCols.reduce((s, c) => s + c.quantity_litres, 0);

  return {
    totalFarmers: totalFarmers.status === 'fulfilled' ? totalFarmers.value : 0,
    activeFarmers: activeFarmers.status === 'fulfilled' ? activeFarmers.value : 0,
    todayCount: todayCols.length,
    todayLitres,
    pendingBatches: pendingBatches.status === 'fulfilled' ? pendingBatches.value : [],
    recentCollections: recentCollections.status === 'fulfilled' ? recentCollections.value : [],
  };
}

function gradeVariant(grade: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (grade === 'A') return 'success';
  if (grade === 'B') return 'info';
  if (grade === 'C') return 'warning';
  return 'danger';
}

function batchStateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'disbursed') return 'success';
  if (state === 'approved') return 'info';
  if (state === 'computed') return 'warning';
  return 'muted';
}

export default async function DashboardPage() {
  let data;
  try {
    data = await getDashboardData();
  } catch {
    data = {
      totalFarmers: 0,
      activeFarmers: 0,
      todayCount: 0,
      todayLitres: 0,
      pendingBatches: [] as PayoutBatch[],
      recentCollections: [] as CollectionRecord[],
    };
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">Welcome to mDairy ERP – your dairy management overview</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Farmers" value={data.totalFarmers} icon="👨‍🌾" color="green" />
        <StatCard label="Active Farmers" value={data.activeFarmers} icon="✅" color="blue" />
        <StatCard
          label="Today's Collections"
          value={data.todayCount}
          icon="🥛"
          color="yellow"
          sub={`${data.todayLitres.toFixed(1)} Litres`}
        />
        <StatCard
          label="Pending Payout Batches"
          value={data.pendingBatches.length}
          icon="💰"
          color="red"
          sub="awaiting disbursement"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Collections */}
        <div>
          <h2 className="text-base font-semibold text-gray-800 mb-3">Recent Collections</h2>
          <Table
            headers={['Ref', 'Farmer', 'Date', 'Litres', 'Grade', 'Amount']}
            rows={data.recentCollections.map((c) => [
              <span key="n" className="font-mono text-xs">{c.name}</span>,
              <span key="f">{Array.isArray(c.farmer_id) ? c.farmer_id[1] : '–'}</span>,
              <span key="d">{formatDate(c.collection_date)}</span>,
              <span key="l">{c.quantity_litres.toFixed(1)}</span>,
              <Badge key="g" label={`Grade ${c.quality_grade}`} variant={gradeVariant(c.quality_grade)} />,
              <span key="a">{formatKes(c.amount_due)}</span>,
            ])}
            emptyMessage="No collections recorded yet."
          />
        </div>

        {/* Pending Payout Batches */}
        <div>
          <h2 className="text-base font-semibold text-gray-800 mb-3">Pending Payout Batches</h2>
          <Table
            headers={['Batch', 'Period', 'Farmers', 'Net (KES)', 'Status']}
            rows={data.pendingBatches.map((b) => [
              <span key="n" className="font-mono text-xs">{b.name}</span>,
              <span key="p" className="text-xs">{formatDate(b.period_start)} – {formatDate(b.period_end)}</span>,
              <span key="c">{b.payout_count}</span>,
              <span key="a">{formatKes(b.total_net)}</span>,
              <Badge key="s" label={b.state} variant={batchStateVariant(b.state)} />,
            ])}
            emptyMessage="No pending payout batches."
          />
        </div>
      </div>
    </div>
  );
}
