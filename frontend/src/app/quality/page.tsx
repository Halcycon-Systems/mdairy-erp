import { PageHeader, Table, Badge, StatCard, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { QualityTest } from '@/types';

function gradeVariant(grade: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (grade === 'A') return 'success';
  if (grade === 'B') return 'info';
  if (grade === 'C') return 'warning';
  return 'danger';
}

async function getData() {
  const [tests, gradeA, rejected] = await Promise.allSettled([
    searchRead<QualityTest>('mdairy.quality.test', [], [
      'name', 'test_date', 'session', 'farmer_id', 'fat_percentage',
      'snf_percentage', 'acidity_ph', 'antibiotics_present', 'grade',
    ], { limit: 50, order: 'test_date desc' }),
    searchCount('mdairy.quality.test', [['grade', '=', 'A']]),
    searchCount('mdairy.quality.test', [['grade', '=', 'rejected']]),
  ]);

  return {
    tests: tests.status === 'fulfilled' ? tests.value : [],
    gradeA: gradeA.status === 'fulfilled' ? gradeA.value : 0,
    rejected: rejected.status === 'fulfilled' ? rejected.value : 0,
  };
}

export default async function QualityPage() {
  let data = { tests: [] as QualityTest[], gradeA: 0, rejected: 0 };
  try {
    data = await getData();
  } catch { /* Odoo unavailable */ }

  return (
    <div>
      <PageHeader title="Quality Tests" subtitle="Milk quality validation results" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Tests" value={data.tests.length} icon="🔬" color="blue" />
        <StatCard label="Grade A" value={data.gradeA} icon="⭐" color="green" />
        <StatCard label="Rejected" value={data.rejected} icon="❌" color="red" />
        <StatCard
          label="Pass Rate"
          value={data.tests.length > 0 ? `${Math.round(((data.tests.length - data.rejected) / data.tests.length) * 100)}%` : '–'}
          icon="✅"
          color="yellow"
        />
      </div>

      <Table
        headers={['Reference', 'Date', 'Session', 'Farmer', 'Fat %', 'SNF %', 'pH', 'Antibiotics', 'Grade']}
        rows={data.tests.map((t) => [
          <span key="n" className="font-mono text-xs">{t.name}</span>,
          <span key="d">{formatDate(t.test_date)}</span>,
          <span key="s" className="capitalize">{t.session}</span>,
          <span key="f">{Array.isArray(t.farmer_id) ? t.farmer_id[1] : '–'}</span>,
          <span key="fa">{t.fat_percentage?.toFixed(2) ?? '–'}</span>,
          <span key="sn">{t.snf_percentage?.toFixed(2) ?? '–'}</span>,
          <span key="ph">{t.acidity_ph?.toFixed(2) ?? '–'}</span>,
          <Badge key="ab"
            label={t.antibiotics_present ? 'Detected' : 'Clear'}
            variant={t.antibiotics_present ? 'danger' : 'success'}
          />,
          <Badge key="g" label={`Grade ${t.grade}`} variant={gradeVariant(t.grade)} />,
        ])}
        emptyMessage="No quality test records found."
      />
    </div>
  );
}
