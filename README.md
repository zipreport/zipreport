# ZipReport

Transform HTML templates into beautiful PDF or MIME reports, with full CSS and client Javascript support, under a
permissive license.

**Highlights**:

- Create your reports using Jinja templates;
- Dynamic image support (embedding of runtime-generated images);
- Reports are packed in a single file for easy distribution or bundling;
- Optional MIME processor to embed resources in a single email message;
- Support for generated JS content (with zipreport-server or zipreport-cli);
- Support for headers, page numbers and ToC (via third party javascript);

**Requirements**:

- Python >= 3.6
- Jinja2 >= 2.11
- Compatible backend for pdf generation (zipreport-server, zipreport-cli or WeasyPrint);

### Installation

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

### Documentation

Still a work in progress

- [FAQ](docs/faq.md)
- [Available Jinja filters](docs/filters.md)
- [Available render processors](docs/processors.md)
- [ZPT file structure](docs/zpt.md)
  