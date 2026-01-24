# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZipReport is a Python library (`zipreport-lib` on PyPI) that transforms Jinja2 HTML templates into PDF or MIME reports. Templates are packaged as `.zpt` files (ZIP archives containing `index.html`, `manifest.json`, assets). Rendering uses either a headless Chromium backend (zipreport-server) or WeasyPrint.

## Build & Test Commands

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests (requires Docker for server tests)
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/report/test_job.py -v

# Run a specific test class/method
python -m pytest tests/report/test_job.py::TestReportJob::test_init -v

# Run tests with coverage
coverage run -m pytest --cov=zipreport --cov-append --cov-report=term-missing

# Lint
flake8 zipreport/ tests/ setup.py

# Full test matrix via tox (runs flake8 + tests on py39-py313)
tox
```

**Note:** Server integration tests (`tests/server/`) require a running zipreport-server Docker container. Tox handles this automatically via `tox-docker`. For local runs without Docker, only unit tests in `tests/fileutils/`, `tests/report/`, `tests/render/`, and `tests/processors/` will pass.

## Architecture

### Data Flow

```
ReportFile (.zpt) → JinjaRender (template → report.html) → Processor → Output (PDF/MIME)
```

### Key Abstractions

- **`FsInterface`** (ABC in `fileutils/interface.py`): File system abstraction with two implementations:
  - `ZipFs`: In-memory ZIP operations backed by `InMemoryZip` + `PathCache` (trie-based path lookup)
  - `DiskFs`: Direct disk operations with path traversal protection

- **`ProcessorInterface`** (ABC in `processors/interface.py`): Pluggable rendering backends:
  - `ZipReportProcessor`: Sends rendered report to zipreport-server API for PDF generation
  - `WeasyPrintProcessor`: Local PDF generation (no JS support)
  - `MIMEProcessor`: Generates email messages with embedded resources

- **`ReportFile`** (`report/reportfile.py`): Container wrapping a `ZipFs` + parsed manifest. All file operations go through this.

- **`ReportJob`** (`report/job.py`): Rendering configuration (page size, margins, timeouts). `JobResult` is the namedtuple output.

### Template Processing Pipeline

1. `ReportFileLoader.load()` auto-detects source (directory or `.zpt` file) → `ReportFile`
2. `JinjaRender.render(data)` renders `index.html` with Jinja2 → writes `report.html` into the `ReportFile`
3. Processor takes the `ReportJob` and produces `JobResult`

### Custom Jinja Filters

Registered globally in `template/jinja/filters.py` via `DEFAULT_FILTERS`:
- `png`, `gif`, `jpg`, `svg`: Dynamic image generation from callables
- `json`: Serialize data to JSON in templates

### CLI (`zipreport` command)

Entry point: `cli/console.py:main()`. Commands are classes extending `CliCommand` in `cli/command/`. The debug server (`cli/debug/server.py`) serves rendered reports over HTTP for template development.

## Configuration

- `manifest.json` required fields: `title`, `author`, `version`, `description`, `params` (list of expected template parameter names)
- Optional manifest fields: `useJSEvent` (bool), `report` (alternate output filename)
- Strict parameter validation is on by default (`JinjaRender.OPT_STRICT_PARAMS`)

## Style

- Max line length: 120 characters
- Python 3.9+ (no walrus operator in core library for broader compat)
- Flake8 with ignored rules: E203, E501, W503, W504, F401, F403
