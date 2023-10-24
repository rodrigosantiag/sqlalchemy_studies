# project settings
PROJECT_NAME  := sqlalchemy_poc
PROJECT_PATH  := $(shell ls */main.py | xargs dirname | head -n 1)

# venv settings
export PYTHONPATH := $(PROJECT_PATH):tests/fixtures
export VIRTUALENV := $(PWD)/.venv
export PATH       := $(VIRTUALENV)/bin:$(PATH)

# fix make < 3.81 (macOS and old Linux distros)
ifeq ($(filter undefine,$(value .FEATURES)),)
SHELL = env PATH="$(PATH)" /bin/bash
endif

.PHONY: .env .venv

all:

.env:
	echo 'PYTHONPATH="$(PYTHONPATH)"' > .env
	cat .env_sample >> .env

.venv:
	python3.11 -m venv $(VIRTUALENV)
	pip install --upgrade pip

install-hook:
	@echo "make lint" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit

install-dev: .venv .env install install-hook
	if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi

install:
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

lint:
	black --line-length=100 --target-version=py311 --check .
	flake8 --max-line-length=100 --ignore=E402,W503,E712 --exclude .venv,dependencies

format:
	black --line-length=100 --target-version=py311 .

build:
	@docker compose build

build-up:
	@docker compose up --wait --build

up:
	@docker compose up --wait

down:
	@docker compose down

logs:
	@docker compose logs -f
