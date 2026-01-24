# Release Notes

## Latest Changes

## 2.3.1

### Features

* Increased minimum supported Python version to 3.9;
* Added Python 3.13 support;
* Updated WeasyPrint dependency to >= 63.0;
* Added markupsafe as explicit dependency;
* Made FsInterface and ProcessorInterface abstract base classes;
* Added path traversal protection in DiskFs;
* Added file overwrite support in FsInterface.add();
* Fixed session leak in ZipReportProcessor;
* Fixed WeasyPrint fetcher to properly return file objects;
* Improved HTML attribute escaping in misc/html.py;
* Fixed various logic errors (PathCache, InMemoryZip, JinjaRender filters);
* Code quality improvements (replaced type() checks with isinstance(), removed star imports);
* Integration tests are now skipped when zipreport-server is not available;

## 2.0.0

### Features

* Removal of ZipReport-Cli and WkHtml2Pdf Processors;
* Added support for [zipreport-server](https://github.com/zipreport/zipreport-server) v2.0.0 - this is now the preferred processor;
* Updated examples and unit tests;
* Removed/updated ReportJob parameters to match zipreport-server usage;
* Increased minimum supported Python version to 3.8;


## 1.1.0

### Features

* ZipReportCli() now supports optional cli arguments to be passed to the zpt-cli binary;
* Code formatting;
