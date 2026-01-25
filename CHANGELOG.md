# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-01-25

### Added
- Python 3.13 support
- Markupsafe as explicit dependency
- Path traversal protection in DiskFs
- File overwrite support in FsInterface.add()

### Changed
- Increased minimum supported Python version to 3.10
- Updated WeasyPrint minimum dependency to >= 68.0
- Refactored WeasyPrintProcessor to use URLFetcher class (replaces deprecated default_url_fetcher)
- Made FsInterface and ProcessorInterface abstract base classes
- Improved HTML attribute escaping in misc/html.py
- Code quality improvements (replaced type() checks with isinstance(), removed star imports)

### Fixed
- Session leak in ZipReportProcessor
- Various logic errors in PathCache, InMemoryZip, and JinjaRender filters
- Integration tests are now skipped when zipreport-server is not available

## [2.2.0] - 2024-01-15

### Added
- Python 3.12 and 3.13 support
- Threading support in TempSysPath for debug CLI
- Relative import support for environment wrapper loading

### Changed
- Updated WeasyPrint dependency version
- Removed base URL usage in WeasyPrint processor
- Updated development dependencies

### Removed
- Python 3.8 support

### Fixed
- Windows path separator handling in ZipFs

## [2.0.0] - 2023-06-01

### Added
- Support for [zipreport-server](https://github.com/zipreport/zipreport-server) v2.0.0 (now the preferred processor)

### Changed
- Updated examples and unit tests
- Updated ReportJob parameters to match zipreport-server usage
- Increased minimum supported Python version to 3.8

### Removed
- ZipReport-Cli processor
- WkHtml2Pdf processor

## [1.1.0] - 2022-01-01

### Added
- ZipReportCli() now supports optional cli arguments to be passed to the zpt-cli binary

### Changed
- Code formatting improvements
