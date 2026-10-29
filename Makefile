# Ban2 Website - common development commands
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
.PHONY: help venv install setup run serve migrations migrate superuser shell check test collectstatic freeze

help:
	@echo Available targets:
	@echo   venv           Create the virtual environment
	@echo   install        Install dependencies from requirements.txt
	@echo   setup          venv + install + migrate
	@echo   run            Start dev server [HOST=$(HOST) PORT=$(PORT)]
	@echo   serve          Start production server - Waitress [HOST=$(HOST) PORT=$(PORT)]
	@echo   migrations     Create new migrations [app=name optional]
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

setup: venv install migrate

run:
	$(MANAGE) runserver $(HOST):$(PORT)

serve:
	$(VENV_BIN)/waitress-serve --host=$(HOST) --port=$(PORT) config.wsgi:application

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
