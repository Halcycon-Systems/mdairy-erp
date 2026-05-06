import { PageHeader, Table, Badge, StatCard, formatKes, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { CollectionRecord } from '@/types';

function stateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'paid') return 'success';
  if (state === 'invoiced') return 'info';
  if (state === 'confirmed') return 'info';
  if (state === 'rejected') return 'danger';
  return 'muted';
}

function gradeVariant(grade: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (grade === 'A') return 'success';
  if (grade === 'B') return 'info';
  if (grade === 'C') return 'warning';
  return 'danger';
}

async function getData() {
  const today = new Date().toISOString().split('T')[0];
  const [collections, todayCount, confirmedCount] = await Promise.allSettled([
    searchRead<CollectionRecord>('mdairy.collection', [], [
      'name', 'collection_date', 'session', 'farmer_id', 'cooperative_id',
      'quantity_litres', 'quality_grade', 'unit_price', 'amount_due', 'state',
    ], { limit: 50, order: 'collection_date desc, session desc' }),
    searchCount('mdairy.collection', [['collection_date', '=', today]]),
    searchCount('mdairy.collection', [['state', '=', 'confirmed']]),
  ]);

  return {
    collections: collections.status === 'fulfilled' ? collections.value : [],
    todayCount: todayCount.status === 'fulfilled' ? todayCount.value : 0,
    confirmedCount: confirmedCount.status === 'fulfilled' ? confirmedCount.value : 0,
  };
}

export default async function CollectionPage() {
  let data = { collections: [] as CollectionRecord[], todayCount: 0, confirmedCount: 0 };
  try {
    data = await getData();
  } catch { /* Odoo unavailable */ }

  const totalLitres = data.collections.reduce((s, c) => s + c.quantity_litres, 0);
  const totalAmount = data.collections.reduce((s, c) => s + c.amount_due, 0);

  return (
    <div>
      <PageHeader title="Milk Collection" subtitle="Daily collection records and status" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Today's Records" value={data.todayCount} icon="📅" color="blue" />
        <StatCard label="Pending Confirmation" value={data.confirmedCount} icon="⏳" color="yellow" />
        <StatCard label="Total Litres (shown)" value={totalLitres.toFixed(1)} icon="🥛" color="green" />
        <StatCard label="Total Amount (shown)" value={formatKes(totalAmount)} icon="💰" color="gray" />
      </div>

      <Table
        headers={['Reference', 'Date', 'Session', 'Farmer', 'Litres', 'Grade', 'Unit Price', 'Amount', 'Status']}
        rows={data.collections.map((c) => [
          <span key="n" className="font-mono text-xs">{c.name}</span>,
          <span key="d">{formatDate(c.collection_date)}</span>,
          <span key="s" className="capitalize">{c.session}</span>,
          <span key="f">{Array.isArray(c.farmer_id) ? c.farmer_id[1] : '–'}</span>,
          <span key="l">{c.quantity_litres.toFixed(2)}</span>,
          <Badge key="g" label={`Grade ${c.quality_grade}`} variant={gradeVariant(c.quality_grade)} />,
          <span key="u">KES {c.unit_price.toFixed(2)}</span>,
          <span key="a">{formatKes(c.amount_due)}</span>,
          <Badge key="st" label={c.state} variant={stateVariant(c.state)} />,
        ])}
        emptyMessage="No collection records found."
      />
    </div>
  );
}
