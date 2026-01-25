# ZipReport Examples

This directory contains examples demonstrating various ZipReport features and use cases.

## Directory Structure

```
examples/
├── code/           # Python code examples
├── reports/        # Report templates (.zpt source directories)
├── processors/     # Standalone processor examples
└── docker-compose/ # Docker Compose deployment example
```

## code/

Python scripts demonstrating how to use the ZipReport library. Most examples require a running zipreport-server instance.

| Example               | Description                                              | Backend          |
|-----------------------|----------------------------------------------------------|------------------|
| `simple/`             | Basic PDF generation from a `.zpt` file                  | zipreport-server |
| `filter_example/`     | Dynamic image generation with built-in Jinja filters     | zipreport-server |
| `custom_filter_example/` | Custom Jinja filter registration                      | zipreport-server |
| `pagedjs/`            | PagedJS client-side pagination with matplotlib graphics  | zipreport-server |
| `print_css_chrome/`   | CSS Paged Media features (Chrome-compatible)             | zipreport-server |
| `print_css/`          | Full CSS Paged Media with margin boxes                   | WeasyPrint       |
| `weasyprint/`         | WeasyPrint processor with running headers/footers        | WeasyPrint       |
| `newsletter/`         | MIME email generation                                    | MIMEProcessor    |

See [code/README.md](code/README.md) for setup instructions.

## reports/

Report template source directories. Each directory can be used directly or packaged as a `.zpt` file.

| Template              | Description                                              |
|-----------------------|----------------------------------------------------------|
| `simple/`             | Minimal template with basic styling                      |
| `filter_example/`     | Template using dynamic image filters                     |
| `env_wrapper/`        | Template for custom environment wrapper example          |
| `newsletter/`         | HTML email template                                      |
| `pagedjs/`            | PagedJS templates with TOC and radar charts              |
| `print_css/`          | CSS Paged Media template for WeasyPrint                  |
| `print_css_chrome/`   | CSS Paged Media template for Chrome/Chromium             |

## processors/

Standalone scripts demonstrating direct processor usage without the high-level `ZipReport` API.

| Script                | Description                                              |
|-----------------------|----------------------------------------------------------|
| `zipreport-server.py` | Direct `ZipReportProcessor` usage                        |
| `zipreport-mime.py`   | Direct `MIMEProcessor` usage                             |

## docker-compose/

Complete Docker Compose example showing how to run an application alongside zipreport-server.

See [docker-compose/README.md](docker-compose/README.md) for details.

## Quick Start

1. Start zipreport-server:
   ```bash
   docker run -d -p 6543:6543 -e ZIPREPORT_API_KEY="somePassword" \
       ghcr.io/zipreport/zipreport-server:2.3.1
   ```

2. Run an example:
   ```bash
   cd code/simple
   pip install zipreport-lib
   python main.py output.pdf
   ```
