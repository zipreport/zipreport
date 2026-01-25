# ZipReport examples

Most examples require a zipreport-server instance running locally. A Docker-based instance can be started with:

```shell
docker run -d -p 6543:6543 -e ZIPREPORT_API_KEY="somePassword" ghcr.io/zipreport/zipreport-server:2.3.1
```

## Configuration

All examples that use zipreport-server read the connection settings from environment variables:

- `ZIPREPORT_URL` - Server URL (default: `https://127.0.0.1:6543`)
- `ZIPREPORT_KEY` - API key (default: `somePassword`)

## Examples

### simple

Basic example that loads a `.zpt` file and renders a PDF using zipreport-server.

### filter_example

Demonstrates dynamic image generation using Jinja filters (`png`, `jpg`, `gif`, `svg`). Requires `pillow` and `svgwrite`.

### custom_filter_example

Shows how to register custom Jinja filters using an `EnvironmentWrapper`.

### pagedjs

Uses PagedJS for client-side pagination with matplotlib-generated graphics. Requires `numpy` and `matplotlib`.

### newsletter

Generates a MIME email message using the `MIMEProcessor`. Does not require a server.

### print_css

Demonstrates CSS Paged Media features supported by Chromium: page breaks (`break-before`, `break-after`), named pages, and widows/orphans control. Uses zipreport-server.

### weasyprint

Generates a PDF using `WeasyPrintProcessor` with full CSS Paged Media support including running headers (`string-set`/`string()`), TOC page numbers (`target-counter`), margin boxes, and page counters. Does not require a server. Requires the `weasyprint` package.
