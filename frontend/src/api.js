// All requests go to the same origin: Django in production, the Vite proxy in development.
const API_BASE = '/api/';

export async function getJson(path) {
  const res = await fetch(API_BASE + path, { headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error(`API ${path} returned ${res.status}`);
  return res.json();
}

/** POST JSON. Resolves to { ok, status, body } for any HTTP status; rejects only on network errors. */
export async function postJson(path, payload) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(payload),
  });
  const body = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, body };
}
