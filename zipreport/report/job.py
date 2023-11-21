import collections
from copy import deepcopy

from .const import *
from .reportfile import ReportFile

# Result type used by Processors
# pdf:io.BytesIO; success:bool, error:str
JobResult = collections.namedtuple("JobResult", ["report", "success", "error"])


class ReportJob:
    # option defaults
    DEFAULT_OPTIONS = {
        OPT_PAGE_SIZE: PDF_PAGE_A4,
        OPT_MAIN_SCRIPT: REPORT_FILE_NAME,
        OPT_MARGIN_STYLE: PDF_MARGIN_DEFAULT,
        OPT_MARGIN_LEFT: "0.0",
        OPT_MARGIN_RIGHT: "0.0",
        OPT_MARGIN_TOP: "0.0",
        OPT_MARGIN_BOTTOM: "0.0",
        OPT_LANDSCAPE: False,
        OPT_SETTLING_TIME: DEFAULT_SETTLING_TIME_MS,
        OPT_JOB_TIMEOUT: DEFAULT_JOB_TIMEOUT_S,
        OPT_JS_TIMEOUT: DEFAULT_JS_TIMEOUT_S,
        OPT_JS_EVENT: False,
        OPT_IGNORE_SSL_ERRORS: False,
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
            self._options[OPT_MAIN_SCRIPT] = report.get_param(
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
            self._options[OPT_PAGE_SIZE] = size
            return True
        return False

    def set_margins(self, margins: str) -> bool:
        """
        Set job margin type
        :param margins: value in const.VALID_MARGINS
        :return: True on success, False on error
        """
        if margins in VALID_MARGINS:
            self._options[OPT_MARGIN_STYLE] = margins
            return True
        return False

    def set_main_script(self, script: str) -> bool:
        """
        Set rendering output file name (default: const.REPORT_FILE_NAME)
        :param script: name to be used for the render output file
        :return: True on success, False on error
        """
        self._options[OPT_MAIN_SCRIPT] = script
        return True

    def set_landscape(self, landscape: bool) -> bool:
        """
        Set landscape mode
        :param landscape: bool
        :return: True on success, False on error
        """
        self._options[OPT_LANDSCAPE] = landscape
        return True

    def set_settling_time(self, ms: int) -> bool:
        """
        Set wait time for rendering
        Settling time is the time a render backend will wait, after loading the report, to start generating the pdf
        :param ms: milisseconds to wait
        :return: True on success, False on error
        """
        if ms > 0:
            self._options[OPT_SETTLING_TIME] = ms
            return True
        return False

    def set_js_timeout(self, seconds: int) -> bool:
        """
        Set JS Event timeout
        Js Event timeout is the amount of time to wait for the zpt-view-ready js event
        :param seconds: seconds to wait
        :return: True on success, False on error
        """
        if seconds > 0:
            self._options[OPT_JS_EVENT] = True
            self._options[OPT_JS_TIMEOUT] = seconds
            return True
        return False

    def set_job_timeout(self, seconds: int) -> bool:
        """
        Set Job timeout
        Time to wait for the browser rendering process
        :param seconds:
        :return: True on success, False on error
        """
        if seconds > 0:
            self._options[OPT_JOB_TIMEOUT] = seconds
            return True
        return False

    def use_jsevent(self, jsevent: bool) -> bool:
        """
        Set if renderer backend should wait for zpt-view-ready event
        :param jsevent: True to enable
        :return: True on success, False on error
        """
        self._options[OPT_JS_EVENT] = jsevent
        return True

    def set_margins_custom_inch(self, left, right, top, bottom):
        self._options[OPT_MARGIN_LEFT] = str(left)
        self._options[OPT_MARGIN_RIGHT] = str(right)
        self._options[OPT_MARGIN_TOP] = str(top)
        self._options[OPT_MARGIN_BOTTOM] = str(bottom)
        return True

    def set_ignore_ssl_errors(self, ignore: bool) -> bool:
        """
        Enable or disable CA SSL verification
        :param ignore: true to disable
        :return: True on success, False on error
        """
        self._options[OPT_IGNORE_SSL_ERRORS] = ignore
        return True
