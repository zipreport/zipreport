# How it works

ZipReport relies on two core concepts: Report Files and Processors. The rendering is executed in two stages - first,
the result of rendering the Jinja template is generated and stored within the memory representation of the report file
with the name *report.html*. Then, the in-memory report file is passed to a Processor, to be rendered onto its final
form - either PDF or MIME message.
Content, such as dynamically generated images is also embedded on the in-memory report file. It is also possible to add
extra files at runtime, before passing it to the desired processor. However, replacement of existing files is not
allowed.

## Report Files

A report file is a Jinja template, a manifest file and an optional data file packed into a zip file, usually with .zpt
extension. These files can be easily generated with the zipreport cli tool. For more information on the cli tool, check
the [cli documentation](cli.md)

For a Jinja template to be packed into a report file (and be a valid report), it needs to contain a manifest. A manifest
is a JSON file called manifest.json, that contains basic report information, such as title and mandatory template
variables.
The template may also contain a data.json file, that will be used when debugging (zipreport debug) the template. This
file
provides placeholder data for the required fields, for previewing purposes.

The main Jinja template file must be named **index.html**. A template cannot contain a file called named *report.html*.
This
is a reserved name, used to store the result of the Jinja rendering. The template can also include other files, such as
partials, css resources, javascript resources, images or fonts.

Example of structure from examples/reports/simple:

```shell
$ cd examples/reports/simple
.
├── css
│   └── style.css
├── data.json
├── index.html
├── manifest.json
└── partials
    └── base.html

2 directories, 5 files
$
```

### Supporting symbolic links (min version: 2.1.0)

The template file tree is often a well-defined, contained structure. Starting with version 2.1.0, to allow eg. sharing
of resources between
templates, the usage of symbolic links is supported in both *zipreport debug* and *zipreport build*. By using *-s*, the
commands
will follow and process any related symlinks, as long as they are linked within the structure of the template.

### Report file format (zpt)

ZipReport report files (*.zpt) are just regular zip files with - at least - the following entries:

| File          | Mandatory | Description                                                                                           |
|---------------|-----------|-------------------------------------------------------------------------------------------------------|
| index.html    | yes       | Report template main file                                                                             |
| manifest.json | yes       | Report manifest file. Contains report information such as title, description and mandatory parameters |
| data.json     | no        | Optional data file to be used when debugging the template                                             |

For more details on these files, see below.

### Manifest file: manifest.json

The manifest.json is a regular JSON file. Its structure is as follows:

| Field       | Type   | Description                                                                                                                                    |
|-------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------|
| author      | string | Report author identification                                                                                                                   |                                                                                                                    
| title       | string | Report title                                                                                                                                   |                                                                                                                                    
| description | string | Extended description                                                                                                                           |                                                                                                                            
| version     | string | ZipReport engine version (currently ignored)                                                                                                   |                                                                                                    
| useJSEvent  | string | If "true", will automatically use jsEvent with ZipReport =cli/server                                                                           |                                                                             
| params      | list   | List of mandatory parameter names. When rendering the report, will generate an exception if the passed parameter keys does not match this list |  

Additionally, the manifest **can** contain other fields relevant to the application, they are just ignored by ZipReport.
If other fields exist, they can be accessed from the application on certain usage patterns.

Example of manifest.json from examples/reports/simple:

```json
    {
  "author": "jpinheiro",
  "title": "Simple Report",
  "description": "Simple ZipReport Report",
  "version": "1.0",
  "params": [
    "title",
    "color_list",
    "description"
  ]
}
```

In this example, to render the report, it is necessary to pass a dict containing the keys specified in *params*. The
dict
may contain other keys. If the keys specified in the manifest are not present, rendering will generate a *RuntimeError*
exception.

### Data placeholder file: data.json

The data placeholder file is an optional JSON file named data.json. It contains a dictionary of predefined values for
the required params specified in the manifest file. This is used to aid the design and preview of the reports, during
development. It is ignored when used outside the scope of zipreport debug.

Example of data.json from examples/reports/simple, for the manifest in the previous example:

```json
{
  "title": "Simple report with Jinja templating",
  "color_list": [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "pink",
    "green"
  ],
  "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ut ornare metus."
}
```    

### Main template file: index.html

This is the Jinja template entrypoint for rendering. It can reference local resources residing below the template folder
in the filesystem hierarchy (meaning it is not possible to use partials from another template), or external resources
such
as javascript libraries, css frameworks or fonts.

Example of index.html from examples/reports/simple, using a partial (*partials/base.html*) as wel as some
Jinja template expressions:

```html
{% extends 'partials/base.html' %}

{% block title%}
{{ title }}
{% endblock %}

{% block content %}
<h1>{{ title }} : main</h1>
<h2>Some custom text:</h2>
<p>
    {{ description }}
</p>
<h2>A list of colors:</h2>
<ul>
    {% for item in color_list %}
    <li>Color: {{ item }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

## Processors

Processors are classes that implements *zipreport.processors.ProcessorInterface*.
Their role is to interact with a backend and generate a PDF file or a MIME message. The generation result is never an
actual file but a *io.BytesIO* buffer that can easily be stored to disk or streamed to a client.

Processors can be used directly or via convenient helper classes that wrap both Jinja rendering logic and processor
invocation.

### Available Processors

There are several available processors to interact with the different backend options. You can also easily create your
own, if necessary. Just implement a new class that implements  *zipreport.processors.ProcessorInterface*.

| Class                                               | Description                                |
|-----------------------------------------------------|--------------------------------------------|
| zipreport.processors.ZipReportProcessor             | zipreport-server API PDF report generation |
| zipreport.processors.MIMEProcessor                  | MIME email report generation               |
| zipreport.processors.weasyprint.WeasyPrintProcessor | WeasyPrint PDF report generation           |

#### Processor Interface

*zipreport.processors.ProcessorInterface* specifies a single method:

```python
ProcessorInterface.process(self, job: ReportJob) -> JobResult:
```

This method receives a *zipreport.report.ReportJob* object. This object contains
all PDF-related options such as margins and page size, as well as the required ReportFile.
It returns a *zipreport.report.JobResult* object, with the status of the operation,
error information (if any), and the result buffer.

#### Helper Classes

Helper classes encapsulate both the processor logic and the Jinja rendering logic. The following helper classes are
available:

| Class                | Description               |
|----------------------|---------------------------|
| zipreport.ZipReport  | ZipReportProcessor helper |
| zipreport.MIMEReport | MIMEProcessor helper      |

See below for usage examples for each processor.

#### ZipReportProcessor

*ZipReportProcessor* interacts with the zipreport-server API to generate a PDF. From a development perspective, all
required
operations are done in-memory and no local storage is needed.

Constructor:

```python
ZipReportProcessor(client: ZipReportClient)
``` 

*client* is an instance of *zipreport.processors.ZipReportClient*, whose function is to encapsulate API communication
logic.

ZipReportProcessor example:

```python
from zipreport.processors import ZipReportProcessor, ZipReportClient
from zipreport.report import ReportFileLoader, ReportJob
from zipreport.template import JinjaRender

# output file
output_file = "result.pdf"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description',
}

# load report from file
zpt = ReportFileLoader.load("simple.zpt")

# initialize api client
api_client = ZipReportClient("https://127.0.0.1:6543", "secretKey")

# first step:
# render the template using the report_data dict
# the result of the rendering is stored in-memory within the zpt file, with the name
# report.html
JinjaRender(zpt).render(report_data)

# create a rendering job from the zpt file
job = ReportJob(zpt)

# second step:
# generate a PDF by calling the processor, using the API client
# this method returns a JobResult
result = ZipReportProcessor(api_client).process(job)

# if PDF generation was successful, save to file
if result.success:
    with open(output_file, 'wb') as rpt:
        rpt.write(result.report.read())
```

#### Using ZipReport Helper

ZipReportProcessor can also be used in a simplified fashion, by using the helper class *ZipReport*.
This class will create an API client, as well as a default *ReportJob*, simplifying the code implementation.

Constructor:

```python
ZipReport(url: str, api_key: str, api_version: int = 2, secure_ssl: bool = False)
```

*url* is the API endpoint url, *api_key* is the API authentication token, and *secure_ssl* enables or disables full
certificate
chain verification on SSL certificates for HTTPS endpoints. *api_version* specifies the API version to connect;
currently,
only v2 is implemented.

Code example:

```python
from zipreport import ZipReport
from zipreport.report import ReportFileLoader

# output file
output_file = "result.pdf"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description',
}

# load report from file
zpt = ReportFileLoader.load("reports/simple.zpt")

# render the report using ZipReport helper class
result = ZipReport("https://127.0.0.1:6543", "someSecret").render_defaults(zpt, report_data)

# if PDF generation was successful, save file
if result.success:
    with open(output_file, 'wb') as rpt:
        rpt.write(result.report.read())
```

#### MimeProcessor

*MIMEProcessor* generates a multipart MIME email message with all local resources embedded. It requires no local
storage.

Constructor:

```python
MIMEProcessor()
```

MIMEProcessor example:

```python
from zipreport.processors import MIMEProcessor
from zipreport.report import ReportFileLoader, ReportJob
from zipreport.template import JinjaRender

# output file
output_file = "result.eml"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description',
}

# load report from file
zpt = ReportFileLoader.load("simple.zpt")

# first step:
# render the template using the report_data dict
# the result of the rendering is stored in-memory within the zpt file, with the name
# report.html
JinjaRender(zpt).render(report_data)

# create a rendering job from the zpt file
job = ReportJob(zpt)

# second step:
# generate a MIME message by calling the processor
# this method returns a JobResult
result = MIMEProcessor().process(job)

# if message generation was successful, save to file
if result.success:
    with open(output_file, 'wb') as rpt:
        # result.report is of type EmailMessage, not io.BytesIO
        rpt.write(result.report.as_bytes())

```

#### Using MIMEProcessor Helper

MIMEProcessor can also be used in a simplified fashion, by using the helper class *MIMEReport*.
This class will create a default *ReportJob<zipreport.reports.job.ReportJob*, simplifying the PDF generation process.

Constructor:

```python
MIMEReport()
```

Code example:

```python
from zipreport import MIMEReport
from zipreport.report import ReportFileLoader

# output file
output_file = "result.eml"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description',
}

# load report from file
zpt = ReportFileLoader.load("reports/simple.zpt")

# render the report with default job options, using the helper class
result = MIMEReport().render_defaults(zpt, report_data)

if result.success:
    with open(output_file, 'wb') as rpt:
        # result.report is of type EmailMessage, not io.BytesIO
        rpt.write(result.report.as_bytes())
```

#### WeasyPrintProcessor

*WeasyPrintProcessor* relies on WeasyPrint for PDF generation.
By using WeasyPrint, client-side Javascript is not supported, and CSS support is limited. Check WeasyPrint website for
more
details. Details on how to install ZipReport with WeasyPrint support can be found in
the [installation instructions](install.md).

Constructor:

```python
WeasyPrintProcessor()
```

The WeasyPrintProcessor includes some additional methods to map WeasyPrint basic requirements to ZipReport processor
logic:

```python
WeasyPrintProcessor.add_css(self, css)
```

where *css* is a WeasyPrint CSS object; see example below

Example:

```python
from zipreport.processors.weasyprint import WeasyPrintProcessor
from weasyprint import CSS

processor = WeasyPrintProcessor()
processor.add_css(CSS(string='body { font-family: serif !important }'))
```

```python
WeasyPrintProcessor.set_font_config(self, font_config)
```

*font_config* is a FontConfiguration() object. See WeasyPrint documentation for more details

Example:

```python
from zipreport.processors.weasyprint import WeasyPrintProcessor
from weasyprint import CSS
from weasyprint.fonts import FontConfiguration

processor = WeasyPrintProcessor()
font_config = FontConfiguration()
# taken from WeasyPrint tutorial in https://weasyprint.readthedocs.io/en/stable/tutorial.html
css = CSS(string='''
@font-face {
    font-family: Gentium;
    src: url(http://example.com/fonts/Gentium.otf);
}
h1 { font-family: Gentium }''', font_config=font_config)
processor.add_css(css)
processor.set_font_config(font_config)
```

WeasyPrintProcessor example:

```python
from zipreport.processors.weasyprint import WeasyPrintProcessor
from zipreport.report import ReportFileLoader, ReportJob
from zipreport.template import JinjaRender

# output file
output_file = "result.pdf"

# template variables
report_data = {
    'title': "Example report using Jinja templating",
    'color_list': ['red', 'blue', 'green'],
    'description': 'a long text field with some filler description',
}

# load report from file
zpt = ReportFileLoader.load("simple.zpt")

# first step:
# render the template using the report_data dict
# the result of the rendering is stored in-memory within the zpt file, with the name
# report.html
JinjaRender(zpt).render(report_data)

# create a rendering job from the zpt file
job = ReportJob(zpt)

# second step:
# generate a PDF by calling the processor, using the API client
# this method returns a JobResult
result = WeasyPrintProcessor().process(job)

# if PDF generation was successful, save to file
if result.success:
    with open(output_file, 'wb') as rpt:
        rpt.write(result.report.read())

```

**Note:** This processor does not have a helper class, to avoid having WeasyPrint as a required ZipReport dependency.
