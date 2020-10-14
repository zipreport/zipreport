# ZPT File Format

ZipReport files (*.zpt) are just regular zip files with - at least - the following entries:



| File          | Mandatory? | Description                                                  |
| ------------- | ---------- | ------------------------------------------------------------ |
| index.html    | yes        | Report template main file. Other files can be included by using Jinja2 commands |
| manifest.json | yes        | Report manifest file. Contains report information such as title, description and mandatory parameters |
| data.json     | no         | Optional data file to be used when debugging the template    |



## Main file (index.html)

This file is the main template file, to be passed to Jinja2 to generate the final HTML.

Example (from examples/reports/simple/index.html):

```jinja2
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



## Manifest File (manifest.json)

The manifest file must contain the following fields:

| Field       | Type   | Description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| author      | string | Report author identification                                 |
| title       | string | Report title                                                 |
| description | string | Extended description                                         |
| version     | string | ZipReport engine version (currently ignored)                 |
| params      | list   | List of mandatory parameter names. When rendering the report, will generate an exception if the passed parameter keys does not match this list |

Additionally, the manifest **can** contain other fields relevant to the application, they are just ignored by ZipReport.



Example:

```json
{
  "author": "jpinheiro",
  "title": "Simple Report",
  "description": "Simple Jinja Report without dynamic generated content",
  "version": "1.0",
  "params": [
    "title",
    "color_list",
    "description"
  ]
}
```



## Optional data file (data.json)

This optional file contain variable values to be used when no data source is available, eg. when previewing the report. To be valid, it must implement at least all the variables specified in the manifest file.

**Previewing dynamic images with placeholders**

Due to the static nature of data.json, it is not possible to implement the callbacks for dynamic image generation. To work around this limitation, it is possible to specify a placeholder image (local or remote) instead of the callable parameter. The data source parameter, while mandatory, is ignored.

Template filter:

```jinja2
{{ png_graphic|png(png_graphic_data, "sample graphic", 256,256 ) }}
```

data.json contents to generate a placeholder image with placeholder.com:

```json
{
  "png_graphic": "https://via.placeholder.com/256//256/09f/fff.png",
  "png_graphic_data": ""
}
```

data.json contents to use a local placeholder image:

```json
{
  "png_graphic": "/images/png_graphic.png",
  "png_graphic_data": ""
}
```