# Processors

The processor is responsible for the output generation (PDF or MIME) of a report rendering. There are several processors (see below) bundled with ZipReport, and - if necessary - you can add your own. Processors can be used directly or via helper classes. Typical usage will resort to using the helper classes.



## Processor helper classes

Helper classes encapsulate processor initialization and provide sane job defaults:

| Class                  | Description                  |
| ---------------------- | ---------------------------- |
| zipreport.ZipReport    | ZipReportProcessor helper    |
| zipreport.ZipReportCli | ZipReportCliProcessor helper |
| zipreport.MIMEReport   | MIMEProcessor helper         |



##### zipreport.BaseReport

BaseReport is the base class for report helpers. It provides the following methods:

Methods:

```python
create_job(zpt: ReportFile) -> ReportJob
```

​	Creates a ReportJob object based on the specified ReportFile

```python
render(self, job: ReportJob, data: dict = None) -> JobResult
```

​	Execute the specified rendering job, with the template variables in data. Returns a JobResult

```python
render_defaults(self, zpt: ReportFile, data: dict = None) -> JobResult
```

​	Creates a ReportJob based on the specified ReportFile, with default configuration, and execute therendering job, with the template variables in data. Returns a JobResult



##### zipreport.ZipReport(BaseReport)

Constructor: 

```python
ZipReport(url: str, api_key: str, api_version: int = 1, secure_ssl: bool = False)
```

Arguments:

| Argument    | Type | Mandatory          | Description                                                  |
| ----------- | ---- | ------------------ | ------------------------------------------------------------ |
| url         | str  | yes                | zipreport-server API url, including destination port         |
| api_key     | str  | yes                | Token for autentication in the zipreport-server API          |
| api_version | int  | no (default 1)     | API version to use                                           |
| secure_ssl  | bool | no (default False) | If True, it will verify the certificate chain for the SSL certificate when interacting with zipreport-server. |



Generating a PDF file from an existing report using ZipReport:

```python
from zipreport import ZipReport
from zipreport.report import ReportFileLoader

# output file
output_file = "result.pdf"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description so the page isn\'t that empty',
}

# load report from file
zpt = ReportFileLoader.load("reports/simple.zpt")

# render the report with default job options
result = ZipReport('http://127.0.0.1:6543', "").render_defaults(zpt, report_data)

if result.success:
    with open(output_file, 'wb') as rpt:
        rpt.write(result.report.read())

```



##### zipreport.ZipReportCli(BaseReport)

Constructor: 

```python
ZipReportCli(cli_path: str)
```

Arguments:

| Argument | Type | Mandatory | Description                            |
| -------- | ---- | --------- | -------------------------------------- |
| cli_path | str  | yes       | full path for the zipreport-cli binary |

Generate a PDF file from an existing report using ZipReportCli:

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



##### zipreport.MIMEReport(BaseReport)

Constructor: 

```python
MIMEReport()
```



Generating a MIME message from an existing report:

```python
from zipreport import MIMEReport
from zipreport.report import ReportFileLoader

# output file
output_file = "result.eml"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description so the page isn\'t that empty',
}

# load report from file
zpt = ReportFileLoader.load("reports/simple.zpt")

# render the report with default job options
result = MIMEReport().render_defaults(zpt, report_data)

if result.success:
    with open(output_file, 'wb') as rpt:
        rpt.write(result.report.as_bytes())  # result.report is of type EmailMessage

```



## Processors

The following processors are bundled with ZipReport:

| Class                                               | Description                                |
| --------------------------------------------------- | ------------------------------------------ |
| zipreport.processors.ZipReportProcessor             | zipreport-server API PDF report generation |
| zipreport.processors.ZipReportCliProcessor          | zipreport-cli PDF report generation        |
| zipreport.processors.MIMEProcessor                  | MIME email report generation               |
| zipreport.processors.weasyprint.WeasyPrintProcessor | WeasyPrint PDF report generation           |



### 