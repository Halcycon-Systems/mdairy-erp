import { PageHeader, Table, Badge, StatCard, formatKes, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { MpesaTransaction } from '@/types';

function stateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'success') return 'success';
  if (state === 'queued') return 'info';
  if (state === 'timeout') return 'warning';
  if (state === 'failed') return 'danger';
  return 'muted';
}

async function getData() {
  const [txns, success, failed] = await Promise.allSettled([
    searchRead<MpesaTransaction>('mdairy.mpesa.transaction', [], [
      'name', 'farmer_id', 'phone_number', 'amount',
      'mpesa_receipt_number', 'state', 'request_timestamp', 'result_description',
    ], { limit: 50, order: 'request_timestamp desc' }),
    searchCount('mdairy.mpesa.transaction', [['state', '=', 'success']]),
    searchCount('mdairy.mpesa.transaction', [['state', '=', 'failed']]),
  ]);

  return {
    txns: txns.status === 'fulfilled' ? txns.value : [],
    success: success.status === 'fulfilled' ? success.value : 0,
    failed: failed.status === 'fulfilled' ? failed.value : 0,
  };
}

export default async function MpesaPage() {
  let data = { txns: [] as MpesaTransaction[], success: 0, failed: 0 };
  try {
    data = await getData();
  } catch { /* Odoo unavailable */ }

  const totalAmount = data.txns
    .filter((t) => t.state === 'success')
    .reduce((s, t) => s + t.amount, 0);

  return (
    <div>
      <PageHeader title="MPESA Transactions" subtitle="B2C payment tracking via Safaricom Daraja API" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Transactions" value={data.txns.length} icon="📱" color="blue" />
        <StatCard label="Successful" value={data.success} icon="✅" color="green" />
        <StatCard label="Failed" value={data.failed} icon="❌" color="red" />
        <StatCard label="Total Disbursed" value={formatKes(totalAmount)} icon="💰" color="gray" />
      </div>

      <Table
        headers={['Reference', 'Farmer', 'Phone', 'Amount', 'Receipt No.', 'Sent At', 'Status']}
        rows={data.txns.map((t) => [
          <span key="n" className="font-mono text-xs">{t.name}</span>,
          <span key="f">{Array.isArray(t.farmer_id) ? t.farmer_id[1] : '–'}</span>,
          <span key="ph">{t.phone_number}</span>,
          <span key="a">{formatKes(t.amount)}</span>,
          <span key="r" className="font-mono text-xs">{t.mpesa_receipt_number ?? '–'}</span>,
          <span key="ts">{formatDate(t.request_timestamp)}</span>,
          <Badge key="s" label={t.state} variant={stateVariant(t.state)} />,
        ])}
        emptyMessage="No MPESA transactions found."
      />

      <div className="mt-6 rounded-xl border border-blue-100 bg-blue-50 p-4 text-sm text-blue-700">
        <p className="font-semibold mb-1">🔧 MPESA Configuration</p>
        <p>Configure your Safaricom Daraja API credentials (Consumer Key, Consumer Secret, Security Credential, Shortcode) in <strong>Odoo → Integrations → MPESA Configuration</strong>.</p>
      </div>
    </div>
  );
}
