import collections
from copy import deepcopy

from .const import (
    PDF_PAGE_A4,
    REPORT_FILE_NAME,
    PDF_MARGIN_DEFAULT,
    DEFAULT_SETTLING_TIME_MS,
    DEFAULT_RENDER_TIMEOUT_S,
    DEFAULT_JS_TIMEOUT_S,
    DEFAULT_PROCESS_TIMEOUT_S,
    MANIFEST_REPORT_FILE,
    VALID_PAGE_SIZES,
    VALID_MARGINS
)
from .reportfile import ReportFile

# Result type used by Processors
# pdf:io.BytesIO; success:bool, error:str
JobResult = collections.namedtuple("JobResult", ["report", "success", "error"])


class ReportJob:
    # Available options
    OPT_PAGE_SIZE = "page_size"
    OPT_MAIN_SCRIPT = "script"
    OPT_MARGINS = "margins"
    OPT_LANDSCAPE = "landscape"
    OPT_SETTLING_TIME = "settling_time"
    OPT_RENDER_TIMEOUT = "timeout_render"
    OPT_JS_TIMEOUT = "timeout_js"
    OPT_PROCESS_TIMEOUT = "timeout_process"
    OPT_JS_EVENT = "js_event"
    OPT_IGNORE_SSL_ERRORS = "ignore_ssl_errors"
    OPT_NO_INSECURE_CONTENT = "secure_only"

    # option defaults
    DEFAULT_OPTIONS = {
        "page_size": PDF_PAGE_A4,
        "script": REPORT_FILE_NAME,
        "margins": PDF_MARGIN_DEFAULT,
        "landscape": False,
        "settling_time": DEFAULT_SETTLING_TIME_MS,
        "timeout_render": DEFAULT_RENDER_TIMEOUT_S,
        "timeout_js": DEFAULT_JS_TIMEOUT_S,
        "timeout_process": DEFAULT_PROCESS_TIMEOUT_S,
        "js_event": False,
        "ignore_ssl_errors": False,
        "secure_only": False,
    }

    def __init__(self, report: ReportFile):
        """
        Constructor
        Create a new rendering job from a ReportFile
        :param report: ReportFile object to use
        """
        self._report = report
        self._options = deepcopy(self.DEFAULT_OPTIONS)
        # set optional report file name from manifest
        if report is not None:
            self._options[self.OPT_MAIN_SCRIPT] = report.get_param(
                MANIFEST_REPORT_FILE, REPORT_FILE_NAME
            )

    def get_options(self) -> dict:
        """
        Retrieve job options
        :return: dict
        """
        return self._options

    def get_report(self) -> ReportFile:
        """
        Retrieve job ReportFile
        :return: ReportFile
        """
        return self._report

    def set_page_size(self, size: str) -> bool:
        """
        Set job page size
        :param size: value in const.VALID_PAGE_SIZES
        :return: True on success, False on error
        """
        if size in VALID_PAGE_SIZES:
            self._options[self.OPT_PAGE_SIZE] = size
            return True
        return False

    def set_margins(self, margins: str) -> bool:
        """
        Set job margin type
        :param margins: value in const.VALID_MARGINS
        :return: True on success, False on error
        """
        if margins in VALID_MARGINS:
            self._options[self.OPT_MARGINS] = margins
            return True
        return False

    def set_main_script(self, script: str) -> bool:
        """
        Set rendering output file name (default: const.REPORT_FILE_NAME)
        :param script: name to be used for the render output file
        :return: True on success, False on error
        """
        self._options[self.OPT_MAIN_SCRIPT] = script
        return True

    def set_landscape(self, landscape: bool) -> bool:
        """
        Set landscape mode
        :param landscape: bool
        :return: True on success, False on error
        """
        self._options[self.OPT_LANDSCAPE] = landscape
        return True

    def set_settling_time(self, ms: int) -> bool:
        """
        Set wait time for rendering
        Settling time is the time a render backend will wait, after loading the report, to start generating the pdf
        :param ms: milisseconds to wait
        :return: True on success, False on error
        """
        if ms > 0:
            self._options[self.OPT_SETTLING_TIME] = ms
            return True
        return False

    def set_render_timeout(self, seconds: int) -> bool:
        """
        Set rendering timeout
        Render timeout is the time the render backend will wait for the whole rendering task
        :param seconds: seconds to wait
        :return: True on success, False on error
        """
        if seconds > 0:
            self._options[self.OPT_RENDER_TIMEOUT] = seconds
            return True
        return False

    def set_jsevent_timeout(self, seconds: int) -> bool:
        """
        Set JS Event timeout
        Js Event timeout is the amount of time to wait for the zpt-view-ready js event
        :param seconds: seconds to wait
        :return: True on success, False on error
        """
        if seconds > 0:
            self._options[self.OPT_JS_EVENT] = True
            self._options[self.OPT_JS_TIMEOUT] = seconds
            return True
        return False

    def set_process_timeout(self, seconds: int) -> bool:
        """
        Set Process timeout
        Time to wait for the render backend
        :param seconds:
        :return: True on success, False on error
        """
        if seconds > 0:
            self._options[self.OPT_PROCESS_TIMEOUT] = seconds
            return True
        return False

    def set_jsevent(self, jsevent: bool) -> bool:
        """
        Set if renderer backend should wait for zpt-view-ready event
        :param jsevent: True to enable
        :return: True on success, False on error
        """
        self._options[self.OPT_JS_EVENT] = jsevent
        return True

    def set_ignore_ssl_errors(self, ignore: bool) -> bool:
        """
        Enable or disable CA SSL verification
        :param ignore: true to disable
        :return: True on success, False on error
        """
        self._options[self.OPT_IGNORE_SSL_ERRORS] = ignore
        return True

    def set_no_insecure_content(self, no_insecure: bool) -> bool:
        """
        Enable or disable rendering of insecure content
        :param no_insecure: true to disable insecure content
        :return: True on success, False on error
        """
        self._options[self.OPT_NO_INSECURE_CONTENT] = no_insecure
        return True
