// A tiny, dependency-free client: auth, JSON, typed errors and retry on 429/5xx.
export class SalvageAlertError extends Error {
  constructor(status, body) {
    super(`${status} ${body?.error?.code}: ${body?.error?.message}`);
    this.status = status;
    this.code = body?.error?.code;
    this.requestId = body?.request_id;
    this.body = body;
  }
}

export function client({ key = process.env.SALVAGEALERT_KEY, base = 'https://salvagealert.com/api/v1', maxRetries = 4 } = {}) {
  if (!key) throw new Error('Set SALVAGEALERT_KEY');
  return async function call(method, path, body) {
    for (let attempt = 0; ; attempt++) {
      const res = await fetch(base + path, {
        method,
        headers: { Authorization: `Bearer ${key}`, ...(body ? { 'Content-Type': 'application/json' } : {}) },
        body: body ? JSON.stringify(body) : undefined,
      });
      if (res.ok) {
        return { data: await res.json(), charged: Number(res.headers.get('x-credits-charged') ?? 0), balance: Number(res.headers.get('x-credits-balance')) };
      }
      const retryable = res.status === 429 || res.status >= 500;
      if (!retryable || attempt >= maxRetries) throw new SalvageAlertError(res.status, await res.json().catch(() => null));
      const wait = res.status === 429 ? Number(res.headers.get('retry-after') ?? 1) * 1000 : Math.min(60_000, 1000 * 2 ** attempt);
      await new Promise((r) => setTimeout(r, wait));
    }
  };
}
