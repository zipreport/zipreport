
![ZipReport](img/logo.png){style="display: block; margin: 0 auto" }

# Welcome to ZipReport documentation

[![Tests](https://github.com/zipreport/zipreport/workflows/Tests/badge.svg?branch=master)](https://github.com/zipreport/zipreport/actions)
[![pypi](https://img.shields.io/pypi/v/zipreport-lib.svg)](https://pypi.org/project/zipreport-lib/)
[![license](https://img.shields.io/pypi/l/zipreport-lib.svg)](https://github.com/zipreport/zipreport/blob/master/LICENSE)


ZipReport is a python library to aid the generation of visually
appealing PDF documents from HTML templates. It combines Jinja2 template
capabilities with PDF generation powered by a headless Chromium browser
daemon. By leveraging the browser rendering capabilities, it is possible
to use CSS and JS for composition of the document, just as if it was any
other web page. Available polyfills such as [paged.js](https://pagedjs.org) can be
used to generate headers, footers, page numbers, chapter numbers and
even table of contents. It is also possible to generate graphics using
popular JS libraries, such as [d3js](https://d3js.org), or even embed
runtime-generated graphics generated via Python functions.

## Features

* Design reports in HTML using Jinja templates;
* Reports are packaged on a single file for easy reuse/distribution;
* Pluggable rendering backends;
* Full support for CSS3 and client-side Javascript (when using zipreport-server);
* Page numbers, headers, footers, ToC, etc. via polyfills (using  [paged.js](https://pagedjs.org));
* Jinja tags for dynamic image generation in Python;
* CLI utility to aid development and packaging of reports;
* MIME multipart email message generation (with all local resources embedded on a single message);

## ZipReport Samples

* Example code is available in [examples/code](https://github.com/zipreport/zipreport/tree/master/examples/code)
* Report template files are available in [examples/reports](https://github.com/zipreport/zipreport/tree/master/examples/reports)
* Pre-generated sample outputs are available in [examples/samples](https://github.com/zipreport/zipreport/tree/master/examples/samples)

**Available samples:**

* [Simple report](samples/simple.pdf) - Simple report demonstrating Jinja templating
* [Dynamic image generation](samples/filter_example.pdf) - Report demonstrating server-side dynamic image generation
* [MIME newsletter example](samples/newsletter.eml) - MIME report example
* [paged.js report](samples/example_report.pdf) - Complex report with front page, ToC, page numbers, chapters, server-side images and client-side images
* [paged.js dynamic ToC](samples/toc_example_report.pdf) - Report showcasing automatic ToC generation

**PagedJS Examples:**

| Example | Description | Output |
|---------|-------------|--------|
| [pagedjs](https://github.com/zipreport/zipreport/tree/master/examples/code/pagedjs/) | Basic PagedJS with matplotlib graphics and radar charts | [PDF](https://github.com/zipreport/zipreport/tree/master/examples/samples/pagedjs_output.pdf) |
| [executive_report](https://github.com/zipreport/zipreport/tree/master/examples/code/executive_report/) | Modern executive report with KPIs, charts, and TOC | [PDF](https://github.com/zipreport/zipreport/tree/master/examples/samples/executive_report_output.pdf) |
| [product_brochure](https://github.com/zipreport/zipreport/tree/master/examples/code/product_brochure/) | Software product brochure with pricing and testimonials | [PDF](https://github.com/zipreport/zipreport/tree/master/examples/samples/product_brochure_output.pdf) |
| [analytics_dashboard](https://github.com/zipreport/zipreport/tree/master/examples/code/analytics_dashboard/) | Single-page site analytics dashboard (A4 landscape) | [PDF](https://github.com/zipreport/zipreport/tree/master/examples/samples/analytics_dashboard_output.pdf) |

