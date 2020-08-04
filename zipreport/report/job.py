import collections
import io

import zipreport.report.const as const
from zipreport.report import ReportFile

# Result type used by Processors
# pdf:io.BytesIO; success:bool, error:str
JobResult = collections.namedtuple('JobResult', ['pdf', 'success', 'error'])


class ReportJob:
    # Available options
    OPT_PAGE_SIZE = 'page_size'
    OPT_MAIN_SCRIPT = 'script'
    OPT_MARGINS = 'margins'
    OPT_LANDSCAPE = 'landscape'
    OPT_SETTLING_TIME = 'settling_time'
    OPT_RENDER_TIMEOUT = 'timeout_render'
    OPT_JS_TIMEOUT = 'timeout_js'
    OPT_PROCESS_TIMEOUT = 'timeout_process'
    OPT_JS_EVENT = 'js_event'
    OPT_IGNORE_SSL_ERRORS = 'ignore_ssl_errors'
    OPT_NO_INSECURE_CONTENT = 'secure_only'

    DEFAULT_OPTIONS = {
        OPT_PAGE_SIZE: const.PDF_PAGE_A4,
        OPT_MAIN_SCRIPT: const.REPORT_FILE_NAME,
        OPT_MARGINS: const.PDF_MARGIN_DEFAULT,
        OPT_LANDSCAPE: False,
        OPT_SETTLING_TIME: const.DEFAULT_SETTLING_TIME_MS,
        OPT_RENDER_TIMEOUT: const.DEFAULT_RENDER_TIMEOUT_S,
        OPT_JS_TIMEOUT: const.DEFAULT_JS_TIMEOUT_S,
        OPT_PROCESS_TIMEOUT: const.DEFAULT_PROCESS_TIMEOUT_S,
        OPT_JS_EVENT: False,
        OPT_IGNORE_SSL_ERRORS: False,
        OPT_NO_INSECURE_CONTENT: False,
    }

    def __init__(self, report: ReportFile):
        self._report = report
        self._options = self.DEFAULT_OPTIONS

    def get_options(self) -> dict:
        return self._options

    def get_report(self) -> ReportFile:
        return self._report

    def set_page_size(self, size: str) -> bool:
        if size in const.VALID_PAGE_SIZES:
            self._options[self.OPT_PAGE_SIZE] = size
            return True
        return False

    def set_margins(self, margins: str) -> bool:
        if margins in const.VALID_MARGINS:
            self._options[self.OPT_MARGINS] = margins
            return True
        return False

    def set_main_script(self, script: str) -> bool:
        self._options[self.OPT_MAIN_SCRIPT] = script
        return True

    def set_landscape(self, landscape: bool) -> bool:
        self._options[self.OPT_LANDSCAPE] = landscape
        return True

    def set_settling_time(self, ms: int) -> bool:
        if ms > 0:
            self._options[self.OPT_SETTLING_TIME] = ms
            return True
        return False

    def set_render_timeout(self, seconds: int) -> bool:
        if seconds > 0:
            self._options[self.OPT_RENDER_TIMEOUT] = seconds
            return True
        return False

    def set_jsevent_timeout(self, seconds: int) -> bool:
        if seconds > 0:
            self._options[self.OPT_JS_EVENT] = True
            self._options[self.OPT_JS_TIMEOUT] = seconds
            return True
        return False

    def set_process_timeout(self, seconds: int) -> bool:
        if seconds > 0:
            self._options[self.OPT_PROCESS_TIMEOUT] = seconds
            return True
        return False

    def set_jsevent(self, jsevent: bool) -> bool:
        self._options[self.OPT_JS_EVENT] = jsevent
        return True

    def set_ignore_ssl_errors(self, ignore: bool) -> bool:
        self._options[self.OPT_IGNORE_SSL_ERRORS] = ignore
        return True

    def set_no_insecure_content(self, no_insecure: bool) -> bool:
        self._options[self.OPT_NO_INSECURE_CONTENT] = no_insecure
        return True
