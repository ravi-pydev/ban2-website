# Event & Experience by Ban2

Website for **Event & Experience by Ban2**, Shashi Darshan's event planning and hospitality services business.

The site name shown to visitors comes from the `site_settings` table and can be changed in Django admin. Internal names such as the `ban2plans` MySQL database are unchanged.

The project has two parts:

- **Backend:** a Django REST Framework API (`/api/…`) that serves all site content from the database and handles enquiries.
- **Frontend:** a React app (Vite) in `frontend/` that fetches everything from the API.

## Tech stack

- **Backend:** Python 3.14, Django 6.1, Django REST Framework, WhiteNoise, Waitress
- **Frontend:** React 19, React Router 7, Vite 8 (requires Node.js 20+)
- **Database:** SQLite for development, MySQL 8 when configured (see [Database](#database-mysql))

## Project structure

```
ban2-website/
├── config/                     # Settings and root URLs (/admin/, /api/, React pages)
├── homepage/                   # API app
│   ├── models.py               # Database tables (all site content)
│   ├── serializers.py          # API output + enquiry validation
│   ├── views.py                # API views + view that serves the React app
│   ├── urls.py                 # /api/ routes
│   ├── seed.py                 # Loads docs/sqls/12_seed_data.sql (`make seed`)
│   ├── admin.py                # Django admin for every table
│   ├── tests.py
│   ├── static/homepage/img/    # Photos (served at /static/…)
│   └── templates/homepage/email/enquiry.txt
├── frontend/                   # React app
│   ├── index.html              # HTML shell
│   ├── vite.config.js          # Dev server + proxy to Django
│   ├── package.json
│   └── src/
│       ├── main.jsx            # Entry point
│       ├── App.jsx             # Routes: / and /about/
│       ├── api.js              # fetch helpers
│       ├── hooks.js            # useApi, useReveal, useScrollToHash…
│       ├── whatsapp.js         # WhatsApp message builder
│       ├── styles.css
│       ├── pages/              # Home.jsx, About.jsx
│       └── components/         # Header, Footer, Icon, home/ sections, Contact form…
├── manage.py
├── Makefile
├── requirements.txt
├── .env.example
└── .gitignore
```

## Getting started

### Prerequisites

- Python 3.14+
- Node.js 20+ (`winget install OpenJS.NodeJS.LTS` on Windows)
- Git
- `make` (optional, for the shortcut commands below)
  - Windows: `winget install ezwinports.make` or `choco install make`
  - macOS: included with the Xcode Command Line Tools
  - Linux: `sudo apt install make` or your distro's equivalent

### Setup with make

```bash
make setup     # Python venv + packages, migrate, load content, npm install, build React
make run       # http://127.0.0.1:8000
```

### Setup without make

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_seed
cd frontend; npm install; npm run build; cd ..
python manage.py runserver
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_seed
(cd frontend && npm install && npm run build)
python manage.py runserver
```

Then open http://127.0.0.1:8000.

## Development

Run two terminals:

```bash
make run        # Django API on http://127.0.0.1:8000
make frontend   # React dev server on http://localhost:5173 — open this one
```

The React dev server reloads instantly when you change files in `frontend/src/`. It forwards `/api` and `/static` requests to Django on port 8000 (see `frontend/vite.config.js`), so both servers must be running.

To preview the production build without the dev server, run `make frontend-build` and open http://127.0.0.1:8000. If `frontend/dist/` didn't exist when Django started, restart Django after the first build.

## Content

All site text comes from the database. Edit it in Django admin at `/admin/` (create a login with `make superuser`).

To load or reset the default content, run `make seed`, which runs `docs/sqls/12_seed_data.sql`. Re-running it overwrites edits made in admin, but never touches enquiries.

## API

| Method | Endpoint | Returns |
|---|---|---|
| GET | `/api/` | List of endpoints |
| GET | `/api/site/` | Site name, WhatsApp number, profile (name, photo, email…) |
| GET | `/api/home/` | Home page content: hero, intro, CTA, stats, services, sessions, testimonials, FAQs… |
| GET | `/api/about/` | Resume: experience, highlights, education, skills, languages, interests |
| GET | `/api/reviews/` | Published reviews sorted by rating (high to low) + `summary` (average, count, 5→1 star breakdown) |
| POST | `/api/feedback/` | Feedback from an existing client: `name`, `email`, `rating` (1–5), `feedback` (20–1000 chars), optional `company`, `role`, `event_session` (id), `consent`. Saved **unpublished**; the owner is emailed. Rate limit 10/hour |
| GET | `/api/enquiries/` | Allowed `event_type` values |
| POST | `/api/enquiries/` | Submit an enquiry (JSON or form data). `201` on success, `400` with `errors` if invalid, `429` if rate-limited (30 per hour per visitor) |

Image fields in the responses are full URLs. Open any endpoint in a browser to use DRF's browsable API. If the content tables are empty, endpoints return `503` and ask you to run `load_seed`.

Example enquiry:

```json
POST /api/enquiries/
{
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "phone": "+91 9800000010",
  "company": "Acme Technologies",
  "event_type": "Corporate Events & Conferences",
  "guests": 120,
  "date": "2026-12-15",
  "event_location": "Leela Ambience, Gurugram",
  "message": "Annual sales meet with lunch and AV."
}
```

Every valid enquiry is saved to the `enquiries` table (visible in `/admin/` → Enquiries) and then emailed. The response is `{"ok": true, "id": …, "email_sent": true|false}`. If the email fails, the enquiry is still saved and `email_sent` is `false`.

## Make commands

Run `make help` to see every command.

| Command | Description |
|---|---|
| `make setup` | Full first-time setup (Python, database, content, React build) |
| `make run` | Start the Django dev server (`make run PORT=9000` to change the port) |
| `make frontend` | Start the React dev server on port 5173 |
| `make frontend-install` | `npm install` in `frontend/` |
| `make frontend-build` | Build React into `frontend/dist/` for production |
| `make seed` | Load or reset the site content |
| `make serve` | Start the production server (Waitress) |
| `make migrations` | Create migrations (`make migrations app=homepage` for one app) |
| `make migrate` | Apply migrations |
| `make superuser` | Create an admin user |
| `make shell` | Open the Django shell |
| `make check` | Run Django system checks |
| `make test` | Run tests |
| `make collectstatic` | Collect static files |
| `make freeze` | Update `requirements.txt` from the venv |

## URLs

| Path | Description |
|---|---|
| `/` | Home: services, organised events, testimonials, FAQ and enquiry form (React) |
| `/about/` | About Me: resume (React) |
| `/api/` | REST API (see [API](#api)) |
| `/admin/` | Django admin (run `make superuser` first to create a login) |

Any other path loads the React app, which shows its own "Page not found" page.

## Client feedback and reviews

- **Feedback form** (home page, `#feedback`): existing clients rate 1–5 stars, write feedback and can tick consent to be published. Each submission is saved to `testimonials` with `is_published = False` and `source = website`, and you get an email with a link to approve it.
- **Approving:** in `/admin/` → Testimonials, select reviews and choose **Publish selected reviews**. Reviews without client consent are skipped, so ask the client first and then tick *Consent given*.
- **Client Reviews section** (`#reviews`): shows all published reviews, highest rated first, with the average rating and a star breakdown. Reviews without consent show a "Sample" badge.

## Enquiry form (email + WhatsApp)

Clicking **Send enquiry** on the home page does two things:

1. **WhatsApp** opens with the enquiry pre-written to the WhatsApp number in the `site_settings` table (editable in admin). The visitor taps Send. The message text is built in `frontend/src/whatsapp.js`.
2. **Database + email:** the form POSTs to `/api/enquiries/`. The server saves the enquiry to the `enquiries` table, then emails the inbox in `site_settings` (falling back to `ENQUIRY_EMAIL_TO` in `.env`) with Reply-To set to the visitor's address.

The email format is in `homepage/templates/homepage/email/enquiry.txt`.

### Email setup (Gmail)

1. Turn on 2-Step Verification for the Gmail account the site will send from.
2. Create an App password at https://myaccount.google.com/apppasswords.
3. Fill in `.env` (copy `.env.example` if you don't have one):

   ```
   EMAIL_HOST_USER=your.sender@gmail.com
   EMAIL_HOST_PASSWORD=your16charapppassword
   ```

4. Restart the server.

Without `EMAIL_HOST_USER` in `.env`, emails are printed to the terminal instead of being sent, which is handy for development.

## Database (MySQL)

The database is chosen in `.env`:

- **`DB_NAME` set:** MySQL, using `DB_HOST`, `DB_PORT`, `DB_USER` and `DB_PASSWORD`. The `mysqlclient` driver is in `requirements.txt`.
- **`DB_NAME` missing or commented out:** SQLite (`db.sqlite3`), with no setup needed.

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=ban2plans
DB_USER=root
DB_PASSWORD=your-mysql-password
```

First-time MySQL setup:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -u root -p -e "CREATE DATABASE IF NOT EXISTS ban2plans CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
make migrate
make seed
```

`make test` creates a temporary `test_ban2plans` database, so the MySQL user needs permission to create databases. `root` has it.

## Production

1. Build the frontend: `make frontend-build`.
2. Collect static files: `make collectstatic`.
3. Start Waitress, which runs on both Windows and Linux:

   ```bash
   make serve HOST=0.0.0.0 PORT=8000
   ```

Django serves everything from one server: the React build (`frontend/dist/`), the API, admin, and images via WhiteNoise.

Before going live:

- Set `DEBUG = False` and add your domain to `ALLOWED_HOSTS` in `config/settings.py`.
- Replace `SECRET_KEY` with a secret value that is kept out of git.
- Re-run `make frontend-build` and `make collectstatic` after every frontend or image change.

## Notes

- `db.sqlite3`, `venv/`, `.env`, `docs/`, `frontend/node_modules/` and `frontend/dist/` are git-ignored.
- `docs/sqls/12_seed_data.sql` is needed by `make seed` and the tests, but `docs/` is git-ignored, so a fresh clone won't have it.
