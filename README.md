# Ban2Plans

Website for Ban2Plans, Shashi Darshan's event planning and hospitality services business.

The project has two parts:

- **Backend:** a Django REST Framework API (`/api/…`) that serves the site content and handles enquiries.
- **Frontend:** plain HTML, CSS and JavaScript in `frontend/`, with no build step. It fetches everything from the API.

## Tech stack

- Python 3.14, Django 6.1, Django REST Framework
- django-cors-headers (lets the frontend call the API from another host or port)
- WhiteNoise (serves the frontend and static files)
- SQLite for development (MySQL will replace it later; see [Switching to MySQL](#switching-to-mysql))

## Project structure

```
ban2-website/
├── config/                     # Settings and root URLs (/admin/, /api/)
├── homepage/                   # API app
│   ├── content.py              # ALL site text: services, resume, FAQs…
│   ├── serializers.py          # Enquiry validation
│   ├── views.py                # API views
│   ├── urls.py                 # /api/ routes
│   ├── tests.py
│   ├── static/homepage/img/    # Photos (served at /static/…)
│   └── templates/homepage/email/enquiry.txt
├── frontend/                   # Website (static HTML/JS)
│   ├── index.html              # Home page  → /
│   ├── about/index.html        # About page → /about/
│   └── assets/
│       ├── css/style.css
│       └── js/
│           ├── config.js       # API base URL
│           ├── app.js          # Shared: API calls, header/footer, icons
│           ├── home.js         # Home page rendering + enquiry form
│           └── about.js        # About page rendering
├── manage.py
├── Makefile
├── requirements.txt
├── .env.example
└── .gitignore
```

## API

| Method | Endpoint | Returns |
|---|---|---|
| GET | `/api/` | List of endpoints |
| GET | `/api/site/` | Site name, WhatsApp number, profile (name, photo, email…) |
| GET | `/api/home/` | Home page content: hero, stats, services, sessions, testimonials, FAQs… |
| GET | `/api/about/` | Resume: experience, highlights, education, skills, languages, interests |
| GET | `/api/enquiries/` | Allowed `event_type` values |
| POST | `/api/enquiries/` | Submit an enquiry (JSON or form data). `201` on success, `400` with `errors` if invalid, `429` if rate-limited (30 per hour per visitor) |

Image fields in the responses are full URLs. Open any endpoint in a browser to use DRF's browsable API.

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
  "message": "Annual sales meet in Gurugram."
}
```

To change any text on the site, edit `homepage/content.py`. The API and pages pick it up automatically.

## Running the site

**One server (simplest, and how production works):** `make run`. Django serves the frontend at http://127.0.0.1:8000 and the API at `/api/`.

**Separate frontend server:** run `make run` (API on port 8000) and, in a second terminal, `make frontend` (frontend on http://127.0.0.1:5500). `frontend/assets/js/config.js` points the frontend at the API on port 8000. To allow other frontend addresses, set `CORS_ALLOWED_ORIGINS` in `.env`.

## Getting started

### Prerequisites

- Python 3.14+
- Git
- `make` (optional, for the shortcut commands below)
  - Windows: `winget install ezwinports.make` or `choco install make`
  - macOS: included with the Xcode Command Line Tools
  - Linux: `sudo apt install make` or your distro's equivalent

### Setup with make

```bash
make setup     # creates venv, installs dependencies, runs migrations
make run       # starts the dev server at http://127.0.0.1:8000
```

### Setup without make

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000.

## Make commands

Run `make help` to see every command.

| Command | Description |
|---|---|
| `make setup` | Create the venv, install dependencies and apply migrations |
| `make run` | Start the dev server (`make run PORT=9000` to change the port) |
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
| `/` | Home – services, organised events, testimonials, FAQ and enquiry form (`frontend/index.html`) |
| `/about/` | About Me – resume (`frontend/about/index.html`) |
| `/api/` | REST API (see [API](#api)) |
| `/admin/` | Django admin (run `make superuser` first to create a login) |

## Enquiry form (email + WhatsApp)

Clicking **Send enquiry** on the home page does two things:

1. **WhatsApp** opens with the enquiry pre-written to the number in `WHATSAPP_NUMBER` (`homepage/content.py`). The visitor taps Send. The message text is built in `frontend/assets/js/home.js`.
2. **Email:** the form POSTs to `/api/enquiries/`, and the server emails `ENQUIRY_EMAIL_TO` with Reply-To set to the visitor's address.

The email format is in `homepage/templates/homepage/email/enquiry.txt`.

### Email setup (Gmail)

1. Turn on 2-Step Verification for the Gmail account the site will send from.
2. Create an App password at https://myaccount.google.com/apppasswords.
3. Copy `.env.example` to `.env` and fill in:

   ```
   EMAIL_HOST_USER=your.sender@gmail.com
   EMAIL_HOST_PASSWORD=your16charapppassword
   ENQUIRY_EMAIL_TO=ravidarshan95@gmail.com
   ```

4. Restart the server.

Without `EMAIL_HOST_USER` in `.env`, emails are printed to the terminal instead of being sent, which is handy for development.

## Switching to MySQL

1. Install the MySQL driver and update the requirements:

   ```bash
   pip install mysqlclient
   make freeze
   ```

2. Change `DATABASES` in `config/settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'ban2_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

   Keep the real credentials out of git, for example by reading them from a `.env` file. `.env` is already listed in `.gitignore`.

3. Apply the migrations to the new database:

   ```bash
   make migrate
   ```

## Production server

`make run` uses Django's development server, which prints a warning that it is not for production. For production, use Waitress, which runs on both Windows and Linux:

```bash
make serve                          # http://127.0.0.1:8000
make serve HOST=0.0.0.0 PORT=8000   # listen on all interfaces
```

Without make:

```bash
waitress-serve --host=0.0.0.0 --port=8000 config.wsgi:application
```

Before serving in production:

- Set `DEBUG = False` and add your domain to `ALLOWED_HOSTS` in `config/settings.py`.
- Replace `SECRET_KEY` with a secret value that is kept out of git.
- Run `make collectstatic` after every change to CSS, JS or images. [WhiteNoise](https://whitenoise.readthedocs.io/) then serves the collected `staticfiles/` folder directly from Django, so no separate web server is needed for static files.

## Notes

- `db.sqlite3`, `venv/` and `.env` are git-ignored.
- `SECRET_KEY` in `config/settings.py` is a development key. Replace it, set `DEBUG = False` and fill in `ALLOWED_HOSTS` before deploying.
