import io
from weasyprint import default_url_fetcher, HTML

from zipreport.processors.interface import ProcessorInterface
from zipreport.report import ReportFile, JobResult, ReportJob
from zipreport.report.const import REPORT_FILE_NAME


class WeasyPrintProcessor(ProcessorInterface):
    """
    WeasyPrint API report processor
    """

    def __init__(self):
        """
        Constructor
        """
        super(WeasyPrintProcessor, self).__init__()
        self._css = None
        self._fconfig = None

    def add_css(self, css):
        """
        Add CSS item to WeasyPrint stylesheets
        :param css:
        :return:
        """
        if self._css is None:
            self._css = [css]
        else:
            self._css.append(css)
        return self

    def set_font_config(self, font_config):
        """
        Set WeasyPrint font_config
        :param font_config:
        :return:
        """
        self._fconfig = font_config
        return self

    def process(self, job: ReportJob) -> JobResult:
        """
        Execute a job using WeasyPrint
        Note: all ReportJob options are ignored
        :param job: ReportJob
        :return:
        """

        zpt = job.get_report()

        # custom weasyprint fetcher
        def f(url):
            return self.fetcher(zpt, url)

        try:
            rpt = HTML(
                base_url="",
                string=io.TextIOWrapper(zpt.get(REPORT_FILE_NAME), encoding="utf-8").read(),
                url_fetcher=f,
            ).write_pdf(None, stylesheets=self._css, font_config=self._fconfig)
        except Exception as e:
            return JobResult(None, False, str(e))
        return JobResult(io.BytesIO(rpt), True, "")

    @staticmethod
    def _make_fetcher_result(path, file_obj):
        """
        Create a fetcher result dict with appropriate mime type
        :param path: file path for mime type detection
        :param file_obj: file-like object
        :return: dict for WeasyPrint url_fetcher
        """
        result = {"file_obj": file_obj}
        # Set mime type based on extension
        if path.endswith(".css"):
            result["mime_type"] = "text/css"
        elif path.endswith(".js"):
            result["mime_type"] = "application/javascript"
        elif path.endswith(".png"):
            result["mime_type"] = "image/png"
        elif path.endswith(".jpg") or path.endswith(".jpeg"):
            result["mime_type"] = "image/jpeg"
        elif path.endswith(".gif"):
            result["mime_type"] = "image/gif"
        elif path.endswith(".svg"):
            result["mime_type"] = "image/svg+xml"
        elif path.endswith(".woff"):
            result["mime_type"] = "font/woff"
        elif path.endswith(".woff2"):
            result["mime_type"] = "font/woff2"
        elif path.endswith(".ttf"):
            result["mime_type"] = "font/ttf"
        elif path.endswith(".otf"):
            result["mime_type"] = "font/otf"
        return result

    def fetcher(self, zpt, url):
        """
        Internal fetcher for WeasyPrint to access in-report resources such as images, css and js
        :param zpt: ReportFile
        :param url: url of the resource to fetch
        :return:
        """
        if url.startswith("http"):
            return default_url_fetcher(url)

        fallback = url
        # support for both file:// and relative urls
        if url.startswith("file://"):
            url = url[7:]

        # Try the URL as-is first
        if zpt.exists(url):
            return self._make_fetcher_result(url, zpt.get(url))

        # For absolute paths, try to find a matching relative path in the report
        # by checking if any suffix of the path exists
        if url.startswith("/"):
            parts = url.split("/")
            for i in range(1, len(parts)):
                relative_path = "/".join(parts[i:])
                if zpt.exists(relative_path):
                    return self._make_fetcher_result(relative_path, zpt.get(relative_path))

        return default_url_fetcher(fallback)
