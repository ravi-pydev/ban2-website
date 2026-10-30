# Event & Experience by Ban2 - common development commands
# Usage: make <target>   (run `make help` to list targets)

ifeq ($(OS),Windows_NT)
    VENV_BIN := venv/Scripts
    PYTHON_SYS := python
else
    VENV_BIN := venv/bin
    PYTHON_SYS := python3
endif

PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
MANAGE := $(PYTHON) manage.py

HOST ?= 127.0.0.1
PORT ?= 8000

.DEFAULT_GOAL := help
.PHONY: help venv install setup run server serve frontend frontend-install frontend-build seed migrations migrate superuser shell check test collectstatic freeze

help:
	@echo Available targets:
	@echo   venv              Create the virtual environment
	@echo   install           Install Python dependencies from requirements.txt
	@echo   setup             venv + install + migrate + seed + frontend-install + frontend-build
	@echo   run / server      Start Django dev server [HOST=$(HOST) PORT=$(PORT)]
	@echo   serve             Start production server - Waitress [HOST=$(HOST) PORT=$(PORT)]
	@echo   frontend          Start React dev server on http://localhost:5173 (needs `make run`)
	@echo   frontend-install  Install React dependencies (npm install)
	@echo   frontend-build    Build React for production into frontend/dist
	@echo   seed              Load site content from docs/sqls/12_seed_data.sql
	@echo   migrations        Create new migrations [app=name optional]
	@echo   migrate        Apply migrations
	@echo   superuser      Create an admin superuser
	@echo   shell          Open the Django shell
	@echo   check          Run Django system checks
	@echo   test           Run tests
	@echo   collectstatic  Collect static files
	@echo   freeze         Write installed packages to requirements.txt

venv:
	$(PYTHON_SYS) -m venv venv

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

setup: venv install migrate seed frontend-install frontend-build

run:
	$(MANAGE) runserver $(HOST):$(PORT)

server: run

serve:
	$(VENV_BIN)/waitress-serve --host=$(HOST) --port=$(PORT) config.wsgi:application

frontend:
	cd frontend && npm run dev

frontend-install:
	cd frontend && npm install

frontend-build:
	cd frontend && npm run build

seed:
	$(MANAGE) load_seed

migrations:
	$(MANAGE) makemigrations $(app)

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

check:
	$(MANAGE) check

test:
	$(MANAGE) test

collectstatic:
	$(MANAGE) collectstatic --noinput

freeze:
	$(PIP) freeze > requirements.txt



# Local settings and secrets. This file is git-ignored — never commit it.

# --- Database (MySQL) ---------------------------------------------------
# Remove or comment out DB_NAME to fall back to SQLite.
DB_HOST=127.0.0.1
DB_PORT=3306
# DB_NAME=ban2plans
DB_USER=root
DB_PASSWORD=ban21999

# --- Email (Gmail) ------------------------------------------------------
# Leave EMAIL_HOST_USER empty to print enquiry emails to the console instead.
# EMAIL_HOST_PASSWORD must be a Google App password: https://myaccount.google.com/apppasswords
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
ENQUIRY_EMAIL_TO=ravidarshan95@gmail.com
