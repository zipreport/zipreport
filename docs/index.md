
![ZipReport](img/logo.png){style="display: block; margin: 0 auto" }

# Welcome to ZipReport documentation

[![Tests](https://github.com/zipreport/zipreport/workflows/Tests/badge.svg?branch=master)](https://github.com/zipreport/zipreport/actions)
[![docs](https://readthedocs.org/projects/zipreport/badge/?version=latest)](https://zipreport.readthedocs.io/en/latest/)
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

* example code is available in [examples](https://github.com/zipreport/zipreport/tree/master/examples/code)
* report template files are available in [reports](https://github.com/zipreport/zipreport/tree/master/examples/reports)
* paged.js examples are available in  [reports](https://github.com/zipreport/zipreport/tree/master/examples/pagedjs)

**Available samples:**

* [Simple report](samples/simple.pdf) - Simple report demonstrating Jinja templating
* [Dynamic image heneration](samples/filter_example.pdf) - Report demonstrating server-side dynamic image generation
* [MIME newsletter example](samples/newsletter.eml) - MIME report example
* [paged.js report](samples/example_report.pdf) - Complex report with front page, ToC, page numbers, chapters, server-side images and client-side images;
* [paged.js dynamic ToC](samples/toc_example_report.pdf) - Report showcasing automatic ToC generation

