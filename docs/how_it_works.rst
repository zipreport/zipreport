.. _howitworks:

How it works
============

ZipReport relies on two core concepts: Report Files and Processors. The rendering is executed in two stages - first,
the result of rendering the Jinja template is generated and stored within the memory representation of the report file
with the name *report.html*. Then, the in-memory report file is passed to a Processor, to be rendered onto its final
form - either PDF or MIME message.
Content, such as dynamically generated images is also embedded on the in-memory report file. It is also possible to add
extra files at runtime, before passing it to the desired processor. However, replacement of existing files is not allowed.

Report Files
____________

A report file is a jinja template, a manifest file and an optional data file packed into a zip file, usually with .zpt
extension. These files can be easily generated with the zipreport cli tool. For more information on the cli tool, see
:ref:`zipreport_tool`.

For a jinja template to be packed into a report file (and be a valid report), it needs to contain a manifest. A manifest
is a json file called manifest.json, that contains basic report information, such as title and mandatory template variables.
The template may also contain a data.json file, that will be used when debugging (zipreport debug) the template. This file
provides placeholder data for the required fields, for previewing purposes.

The main jinja template file must be named **index.html**. A template cannot contain a file called named report.html. This
is a reserved name, used to store the result of the jinja rendering. The template can also include other files, such as
partials, css resources, javascript resources, images or fonts.

Example of structure from examples/reports/simple:

.. code-block:: sh

    $ cd examples/reports/simple
    .
    ├── css
    │   └── style.css
    ├── data.json
    ├── index.html
    ├── manifest.json
    └── partials
        └── base.html

    2 directories, 5 files
    $

Report file format (zpt)
------------------------

ZipReport report files (\*.zpt) are just regular zip files with - at least - the following entries:

+---------------+------------+-------------------------------------------------------------------------------------------------------+
| File          | Mandatory  | Description                                                                                           |
+---------------+------------+-------------------------------------------------------------------------------------------------------+
| index.html    | yes        | Report template main file                                                                             |
| manifest.json | yes        | Report manifest file. Contains report information such as title, description and mandatory parameters |
| data.json     | no         | Optional data file to be used when debugging the template                                             |
+---------------+------------+-------------------------------------------------------------------------------------------------------+

For more details on these files, see below.

Manifest file: manifest.json
----------------------------

The manifest.json is a regular json file. Its structure is as follows:

+-------------+--------+------------------------------------------------------------------------------------------------------------------------------------------------+
| Field       | Type   | Description                                                                                                                                    |
+-------------+--------+------------------------------------------------------------------------------------------------------------------------------------------------+
| author      | string | Report author identification                                                                                                                   |
| title       | string | Report title                                                                                                                                   |
| description | string | Extended description                                                                                                                           |
| version     | string | ZipReport engine version (currently ignored)                                                                                                   |
| useJSEvent  | string | If "true", will automatically use jsEvent with ZipReport-cli/server                                                                            |
| params      | list   | List of mandatory parameter names. When rendering the report, will generate an exception if the passed parameter keys does not match this list |
+-------------+--------+------------------------------------------------------------------------------------------------------------------------------------------------+

Additionally, the manifest **can** contain other fields relevant to the application, they are just ignored by ZipReport.
If other fields exist, they can be accessed from the application on certain usage patterns.

Example of manifest.json from examples/reports/simple:

.. code-block:: json

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

In this example, to render the report, it is necessary to pass a dict containing the keys specified in *params*. The dict
may contain other keys. If the keys specified in the manifest are not present, rendering will generate a *RuntimeError*
exception.

Data placeholder file: data.json
--------------------------------

The data placeholder file is an optional json file named data.json. It contains a dictionary of predefined values for
the required params specified in the manifest file. This is used to aid the design and preview of the reports, during
development. It is ignored when used outside the scope of *zipreport debug*.

Example of data.json from examples/reports/simple, for the manifest in the previous example:

.. code-block:: json

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


Main template file: index.html
------------------------------

This is the jinja template entrypoint for rendering. It can reference local resources residing below the template folder
in the filesystem hierarchy (eg. its not possible to use partials from another template), or external resources such
as javascript libraries, css frameworks or fonts.

Example of index.html from examples/reports/simple, using a partial (*partials/base.html*) as wel as some
Jinja template expressions:

.. code-block:: html

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


Processors
__________

Processors are classes that implements *zipreport.processors.ProcessorInterface*. Their role is to interact with a backend
and generate a PDF file or a MIME message. The generation result is never an actual file but a *io.BytesIO* buffer that
can easily be stored to disk or streamed to a client.

Available Processors
--------------------

There are several available processors to interact with the different backend options. You can also easily create your
own, if necessary.

+-----------------------------------------------------+--------------------------------------------+
| Class                                               | Description                                |
+-----------------------------------------------------+--------------------------------------------+
| zipreport.processors.ZipReportProcessor             | zipreport-server API PDF report generation |
| zipreport.processors.ZipReportCliProcessor          | zipreport-cli PDF report generation        |
| zipreport.processors.MIMEProcessor                  | MIME email report generation               |
| zipreport.processors.weasyprint.WeasyPrintProcessor | WeasyPrint PDF report generation           |
+-----------------------------------------------------+--------------------------------------------+

ZipReportProcessor
__________________

This processor interacts with the zipreport-server API to generate a PDF. From a development perspective, all required
operations are done in-memory and no local storage is needed.





Processor helpers
-----------------



