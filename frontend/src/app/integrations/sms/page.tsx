import { PageHeader, Table, Badge, StatCard, formatDate } from '@/components/ui';
import { searchRead, searchCount } from '@/lib/odoo';
import type { SmsMessage } from '@/types';

function stateVariant(state: string): 'success' | 'info' | 'warning' | 'danger' | 'muted' {
  if (state === 'delivered') return 'success';
  if (state === 'sent') return 'info';
  if (state === 'failed') return 'danger';
  return 'muted';
}

async function getData() {
  const [messages, sent, failed] = await Promise.allSettled([
    searchRead<SmsMessage>('mdairy.sms.message', [], [
      'name', 'farmer_id', 'to_number', 'message_body', 'state', 'sent_at',
    ], { limit: 50, order: 'id desc' }),
    searchCount('mdairy.sms.message', [['state', 'in', ['sent', 'delivered']]]),
    searchCount('mdairy.sms.message', [['state', '=', 'failed']]),
  ]);

  return {
    messages: messages.status === 'fulfilled' ? messages.value : [],
    sent: sent.status === 'fulfilled' ? sent.value : 0,
    failed: failed.status === 'fulfilled' ? failed.value : 0,
  };
}

export default async function SmsPage() {
  let data = { messages: [] as SmsMessage[], sent: 0, failed: 0 };
  try {
    data = await getData();
  } catch { /* Odoo unavailable */ }

  return (
    <div>
      <PageHeader title="SMS Messages" subtitle="Farmer notification history" />

      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <StatCard label="Total Messages" value={data.messages.length} icon="💬" color="blue" />
        <StatCard label="Sent / Delivered" value={data.sent} icon="✅" color="green" />
        <StatCard label="Failed" value={data.failed} icon="❌" color="red" />
      </div>

      <Table
        headers={['Reference', 'Farmer', 'To Number', 'Message', 'Sent At', 'Status']}
        rows={data.messages.map((m) => [
          <span key="n" className="font-mono text-xs">{m.name}</span>,
          <span key="f">{Array.isArray(m.farmer_id) ? m.farmer_id[1] : '–'}</span>,
          <span key="ph">{m.to_number}</span>,
          <span key="mb" className="max-w-xs truncate text-xs">{m.message_body}</span>,
          <span key="ts">{m.sent_at ? formatDate(m.sent_at) : '–'}</span>,
          <Badge key="s" label={m.state} variant={stateVariant(m.state)} />,
        ])}
        emptyMessage="No SMS messages found."
      />

      <div className="mt-6 rounded-xl border border-blue-100 bg-blue-50 p-4 text-sm text-blue-700">
        <p className="font-semibold mb-1">🔧 SMS Gateway Configuration</p>
        <p>Configure your SMS gateway (Africa&apos;s Talking or Twilio) and message templates in <strong>Odoo → Integrations → SMS Configuration</strong>.</p>
      </div>
    </div>
  );
}
