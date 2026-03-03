PYTHON ?= python

.PHONY: help install install-dev lint format test check clean

help:
	@echo "Available targets:"
	@echo "  install      Install runtime dependencies and package"
	@echo "  install-dev  Install dev tools and package (CI-friendly)"
	@echo "  lint         Run Ruff linter"
	@echo "  format       Run Ruff formatter"
	@echo "  test         Run pytest"
	@echo "  check        Run lint + test"
	@echo "  clean        Remove local caches/artifacts"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PYTHON) -m pip install -e . --no-deps

lint:
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests

test:
	$(PYTHON) -m pytest -q

check: lint test

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache','.ruff_cache','build','dist']]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc') if p.exists()]"