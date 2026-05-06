// API base URL — set NEXT_PUBLIC_ODOO_URL in your .env.local
export const ODOO_URL = process.env.NEXT_PUBLIC_ODOO_URL ?? 'http://localhost:8069';
export const ODOO_DB  = process.env.NEXT_PUBLIC_ODOO_DB  ?? 'mdairy';

// ── Generic JSON-RPC helper ──────────────────────────────────────────────────

interface JsonRpcPayload {
  model: string;
  method: string;
  args?: unknown[];
  kwargs?: Record<string, unknown>;
}

export async function callOdoo<T = unknown>(
  payload: JsonRpcPayload,
  sessionId?: string,
): Promise<T> {
  const res = await fetch(`${ODOO_URL}/web/dataset/call_kw`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(sessionId ? { Cookie: `session_id=${sessionId}` } : {}),
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      method: 'call',
      id: Date.now(),
      params: {
        model: payload.model,
        method: payload.method,
        args: payload.args ?? [],
        kwargs: payload.kwargs ?? {},
      },
    }),
    credentials: 'include',
  });

  const json = await res.json();
  if (json.error) {
    throw new Error(json.error.data?.message ?? json.error.message ?? 'Odoo RPC error');
  }
  return json.result as T;
}

// ── Model-specific helpers ───────────────────────────────────────────────────

/** Search-read wrapper */
export async function searchRead<T = Record<string, unknown>>(
  model: string,
  domain: unknown[] = [],
  fields: string[] = [],
  options: { limit?: number; offset?: number; order?: string } = {},
): Promise<T[]> {
  return callOdoo<T[]>({
    model,
    method: 'search_read',
    args: [domain],
    kwargs: { fields, ...options },
  });
}

/** Read a single record */
export async function readRecord<T = Record<string, unknown>>(
  model: string,
  id: number,
  fields: string[] = [],
): Promise<T> {
  const records = await callOdoo<T[]>({
    model,
    method: 'read',
    args: [[id]],
    kwargs: { fields },
  });
  return records[0];
}

/** Create a record */
export async function createRecord(
  model: string,
  values: Record<string, unknown>,
): Promise<number> {
  return callOdoo<number>({
    model,
    method: 'create',
    args: [values],
  });
}

/** Write (update) a record */
export async function writeRecord(
  model: string,
  id: number,
  values: Record<string, unknown>,
): Promise<boolean> {
  return callOdoo<boolean>({
    model,
    method: 'write',
    args: [[id], values],
  });
}

/** Count records matching a domain */
export async function searchCount(model: string, domain: unknown[] = []): Promise<number> {
  return callOdoo<number>({
    model,
    method: 'search_count',
    args: [domain],
  });
}
