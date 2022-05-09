# ZipReport

[![Tests](https://github.com/zipreport/zipreport/workflows/Tests/badge.svg?branch=master)](https://github.com/zipreport/zipreport/actions)
[![docs](https://readthedocs.org/projects/zipreport/badge/?version=latest)](https://zipreport.readthedocs.io/en/latest/)
[![pypi](https://img.shields.io/pypi/v/zipreport-lib.svg)](https://pypi.org/project/zipreport-lib/)
[![license](https://img.shields.io/pypi/l/zipreport-lib.svg)](https://github.com/zipreport/zipreport/blob/master/LICENSE)

Transform HTML templates into beautiful PDF or MIME reports, with full CSS and client Javascript support, under a
permissive license.

Want to see it in action? Check this [example](docs/samples/pagedjs.pdf)!

**Highlights**:

- Create your reports using Jinja templates;
- Dynamic image support (embedding of runtime-generated images);
- Reports are packed in a single file for easy distribution or bundling;
- Optional MIME processor to embed resources in a single email message;
- Support for generated JS content (with zipreport-server or zipreport-cli);
- Support for headers, page numbers and ToC (via PagedJS, see below);

**Requirements**:

- Python >= 3.6
- Jinja2 >= 3.1 
- Compatible backend for pdf generation (zipreport-server, zipreport-cli, xhtmltopdf, or WeasyPrint);

Note: For previous Jinja2 versions, zipreport-lib 0.9.5 is functionally similar.

### Installation

Installing via pip:
```shell script
$ pip install zipreport-lib
```

##### Quick example

Using zipreport-cli backend to render a report file:
```python
from zipreport import ZipReportCli
from zipreport.report import ReportFileLoader

# path to zipreport-cli binary
cli_path = "/opt/zpt-cli/zpt-cli"

# output file
output_file = "result.pdf"

# template variables to be used for rendering
report_data = {
	'title': "Example report using Jinja templating",
	'color_list': ['red', 'blue', 'green'],
	'description': 'a long text field with some filler description so the page isn\'t that empty',
}

# load zpt report file
zpt = ReportFileLoader.load("reports/simple.zpt")

# render the report with default job options
result = ZipReportCli(cli_path).render_defaults(zpt, report_data)

if result.success:
	# write output file
	with open(output_file, 'wb') as rpt:
		rpt.write(result.report.read())
```  

### Paged.js

[Paged.js](https://www.pagedjs.org/) is an amazing javascript library that performs pagination of HTML documents for print,
under MIT license. It acts as polyfill for W3C specification for print, and allows the creation of headers, footers,
page numbers, table of contents, etc. in the browser.

### Available backends

#### zipreport-server/zipreport-cli

This is the recommended backend to use, that enables full usage of client-side JavaScript and leveraging the Paged.js
capabilities.

[zipreport-cli](https://github.com/zipreport/zipreport-cli) is an electron-based command-line utility used to convert
webpages to PDF.

[zipreport-server](https://github.com/zipreport/zipreport-server) is a daemon that allows the usage of zipreport-cli via API. 

#### WeasyPrint

This backend is provided for compatibility. For new projects, please use zipreport-cli or zipreport-server.

[WeasyPrint](https://weasyprint.org/) is a popular Python library to generate PDFs from HTML. It doesn't support JavaScript,
and CSS is limited. 

#### wkhtmltopdf

This backend is provided for compatibility. While it supports some JavaScript, it's not able to run Paged.js.

[Wkhtmltopdf](https://wkhtmltopdf.org/) is a binary utility based on QtWebKit to generate PDF files from HTML pages.
While it features some JavaScript and CSS support, the underlying library is obsolete.


### Documentation

Detailed documentation on usage and report building is available on the [project documentation](https://zipreport.readthedocs.io/en/latest/).


