# Ban2 Website

The Ban2 website, built with Django.

## Tech stack

- Python 3.14
- Django 6.1
- SQLite for development (MySQL will replace it later; see [Switching to MySQL](#switching-to-mysql))

## Project structure

```
ban2-website/
├── config/                 # Project settings and root URL configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── homepage/               # Homepage app
│   ├── migrations/
│   ├── templates/homepage/
│   │   └── index.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── Makefile
├── requirements.txt
└── .gitignore
```

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
| `/` | Homepage |
| `/admin/` | Django admin (run `make superuser` first to create a login) |

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
- Run `make collectstatic`, and serve the collected `staticfiles/` with a web server such as Nginx or IIS. Waitress does not serve static files, so CSS (including the admin's) will be missing without this.

## Notes

- `db.sqlite3`, `venv/` and `.env` are git-ignored.
- `SECRET_KEY` in `config/settings.py` is a development key. Replace it, set `DEBUG = False` and fill in `ALLOWED_HOSTS` before deploying.
