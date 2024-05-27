# CLI tool: zipreport

ZipReport includes a cli tool to ease the process of creation and maintenance of report templates, *zipreport*.

**Available command-line arguments**

| Argument                                       | Description                                            |
|------------------------------------------------|--------------------------------------------------------|
| help                                           | Show usage information                                 |
| version [-m]                                   | Show version (or version number only, if -m)           |
| list [path]                                    | List report files on the current or specified path     |
| info <file>                                    | Show basic report details                              |
| build <directory> [output_file] [-s]           | Build a zpt file from a jinja template                 |
| debug <directory\|file> [[host]:\<port\>] [-s] | Run debug server using the directory or specified file |

### List report files

List all available report files:

```shell
$ zipreport list
sample1.zpt          Sample report 1
$
```

### Show report file info

```shell
$ zipreport info sample1.zpt
sample1.zpt          Sample report 1
$
```

### Generate a report file

Generating a report file (zpt) from existing Jinja2 report files (the option -s can be used if templates use symlinks):

```shell
$ zipreport build reports/sample1 sample1-1.0.0
== Building Report sample1-1.0.0.zpt ==
Follow Symlinks: False
Checking manifest & index file...
Building...
Copying manifest.json...
Copying index.html...
Copying data.json...
Copying partials/base.html...
Generating sample1-1.0.0.zpt...
Done!
$
```

## Running a template for development purposes (debugging)

The debug argument creates a local webserver to run a given Jinja template or report file. At each page request (
refresh) it will re-render the template as HTML.

To use debug with a template that uses symbolic links, the -s option must be used.

Please note, the template should have a valid manifest.json and data.json files. If no data.json is present and
variables are required to render the template, the render will fail. See [building templates](build_templates.md) for
more information.

```shell
$ zipreport debug reports/sample1/
Started debug server at http://localhost:8001
Serving from: reports/sample1
Use Ctrl+C to stop...
```




