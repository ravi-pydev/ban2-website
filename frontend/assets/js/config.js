// Where the Django API lives.
// Empty string = the same server that serves these pages (production, `make run`).
// When the frontend runs on its own dev server (`make frontend`, port 5500),
// it talks to the API on port 8000.
window.BAN2_API_BASE = window.location.port === '5500' ? 'http://127.0.0.1:8000' : '';
