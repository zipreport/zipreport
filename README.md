# ZipReport

[![Tests](https://github.com/zipreport/zipreport/workflows/Tests/badge.svg?branch=master)](https://github.com/zipreport/zipreport/actions)
[![pypi](https://img.shields.io/pypi/v/zipreport-lib.svg)](https://pypi.org/project/zipreport-lib/)
[![license](https://img.shields.io/pypi/l/zipreport-lib.svg)](https://github.com/zipreport/zipreport/blob/master/LICENSE)

---

**Documentation:** [https://zipreport.github.io/zipreport/](https://zipreport.github.io/zipreport/)

---

Transform HTML templates into beautiful PDF or MIME reports, with full CSS and client Javascript support, under a
permissive license.

Want to see it in action? Check this [example](docs/samples/example_report.pdf)!

**Highlights**:

- Create your reports using Jinja templates;
- Customize the Jinja Environment();
- Dynamic image support (embedding of runtime-generated images);
- Reports are packed in a single file for easy distribution or bundling;
- Optional MIME processor to embed resources in a single email message;
- Support for browser-generated JS content (with zipreport-server);
- Support for headers, page numbers and ToC (using [PagedJS](https://pagedjs.org/), see details below);

**Requirements**:

- Python >= 3.8
- Jinja2 >= 3.1 
- Compatible backend for pdf generation (zipreport-server, xhtmltopdf, or WeasyPrint);

### v2.x.x breaking changes

Starting with zipreport 2.0.0, support for the electron-based zipreport-cli rendering backend is removed; using
a [zipreport-server](https://github.com/zipreport/zipreport-server) version 2.0.0 or later - preferably using a docker container,
is now the recommended approach.

The behavior of the JS event approach has also changed; PDF rendering can now be triggered via console message,
instead of dispatching an event. **If you use JS events to trigger rendering, you need to update your templates**.

Old method:
```javascript
    (...)
    // signal PDF generation after all DOM changes are performed
    document.dispatchEvent(new Event('zpt-view-ready'))
    (...)
```

New method, starting with v2.0.0:
```javascript
    (...)
    // signal PDF generation after all DOM changes are performed
    console.log('zpt-view-ready')
    (...)
```


### Installation

Installing via pip:
```shell script
$ pip install zipreport-lib
```

##### TL;DR; example

Using zipreport-cli backend to render a report file:
```python
from zipreport import ZipReport
from zipreport.report import ReportFileLoader

# existing zpt template
report_file = "report.zpt"

# output file
output_file = "result.pdf"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description',
}

# load report from file
zpt = ReportFileLoader.load(report_file)

# initialize api client
client = ZipReport("https://127.0.0.1:6543", "secretKey")
job = client.create_job(zpt)

# generate a PDF by calling the processor, using the API client
# this method returns a JobResult
result = client.render(job, report_data)

# if PDF generation was successful, save to file
if result.success:
    with open(output_file, 'wb') as rpt:
        rpt.write(result.report.read())
```  

### Paged.js

[PagedJS](https://www.pagedjs.org/) is an amazing javascript library that performs pagination of HTML documents for print,
under MIT license. It acts as polyfill for W3C specification for print, and allows the creation of headers, footers,
page numbers, table of contents, etc. in the browser.

To use PagedJS capabilities, [zipreport-server](https://github.com/zipreport/zipreport-server) must be used as a backend.

### Available backends

#### Zipreport-Server

[zipreport-server](https://github.com/zipreport/zipreport-server) is a headless browser daemon orchestrator, designed specifically to work with ZipReport. It can be
either installed locally or run via docker.

zipreport-server is the only supported backend that enables full usage of client-side JavaScript and leveraging the PagedJS
capabilities. 

#### WeasyPrint

This backend is provided for compatibility. For new projects, please use zipreport-server.

[WeasyPrint](https://weasyprint.org/) is a popular Python library to generate PDFs from HTML. It doesn't support JavaScript,
and CSS is limited. 


