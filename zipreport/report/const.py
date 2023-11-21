ZIPREPORT_FILE_EXTENSION = ".zpt"

# Expected filenames
MANIFEST_FILE_NAME = "manifest.json"
DATA_FILE_NAME = "data.json"
INDEX_FILE_NAME = "index.html"
REPORT_FILE_NAME = "report.html"
PDF_FILE_NAME = "report.pdf"

# Manifest Constants
MANIFEST_TITLE = "title"
MANIFEST_AUTHOR = "author"
MANIFEST_VERSION = "version"
MANIFEST_PARAMETERS = "params"
MANIFEST_DESCRIPTION = "description"
MANIFEST_JS_EVENT = "useJSEvent"
MANIFEST_REPORT_FILE = "report"

MANIFEST_REQUIRED_FIELDS = {
    MANIFEST_TITLE: str,
    MANIFEST_DESCRIPTION: str,
    MANIFEST_AUTHOR: str,
    MANIFEST_VERSION: str,
    MANIFEST_PARAMETERS: list,
}

# margin options
PDF_MARGIN_DEFAULT = "standard"
PDF_MARGIN_NONE = "none"
PDF_MARGIN_MINIMUM = "minimum"
PDF_MARGIN_CUSTOM = "custom"

VALID_MARGINS = [
    PDF_MARGIN_DEFAULT,
    PDF_MARGIN_NONE,
    PDF_MARGIN_MINIMUM,
    PDF_MARGIN_CUSTOM,
]

# page size
PDF_PAGE_A5 = "A5"
PDF_PAGE_A4 = "A4"
PDF_PAGE_A3 = "A3"
PDF_PAGE_LEGAL = "Legal"
PDF_PAGE_LETTER = "Letter"
PDF_PAGE_TABLOID = "Tabloid"

VALID_PAGE_SIZES = [
    PDF_PAGE_A5,
    PDF_PAGE_A4,
    PDF_PAGE_A3,
    PDF_PAGE_LEGAL,
    PDF_PAGE_LETTER,
    PDF_PAGE_TABLOID,
]

# page orientation
PDF_PAGE_PORTRAIT = 0
PDF_PAGE_LANDSCAPE = 1

# Default timeouts
DEFAULT_JOB_TIMEOUT_S = 120
DEFAULT_SETTLING_TIME_MS = 200
DEFAULT_JS_TIMEOUT_S = 60


# ReportJob options
OPT_PAGE_SIZE = "page_size"
OPT_MAIN_SCRIPT = "script"
OPT_MARGIN_STYLE = "margins"
OPT_MARGIN_LEFT = "margin_left"
OPT_MARGIN_RIGHT = "margin_right"
OPT_MARGIN_TOP = "margin_top"
OPT_MARGIN_BOTTOM = "margin_bottom"
OPT_LANDSCAPE = "landscape"
OPT_SETTLING_TIME = "settling_time"
OPT_JS_TIMEOUT = "timeout_js"
OPT_JOB_TIMEOUT = "timeout_job"
OPT_JS_EVENT = "js_event"
OPT_IGNORE_SSL_ERRORS = "ignore_ssl_errors"
