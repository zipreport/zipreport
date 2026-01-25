import io
from weasyprint import HTML, URLFetcher
from weasyprint.urls import URLFetcherResponse

from zipreport.processors.interface import ProcessorInterface
from zipreport.report import ReportFile, JobResult, ReportJob
from zipreport.report.const import REPORT_FILE_NAME


class ZptURLFetcher(URLFetcher):
    """
    Custom URL fetcher that fetches resources from a ZipReport file.
    Falls back to parent URLFetcher for external URLs.
    """

    def __init__(self, zpt: ReportFile, **kwargs):
        super().__init__(**kwargs)
        self._zpt = zpt

    @staticmethod
    def _get_mime_type(path):
        """Get mime type based on file extension"""
        if path.endswith(".css"):
            return "text/css"
        elif path.endswith(".js"):
            return "application/javascript"
        elif path.endswith(".png"):
            return "image/png"
        elif path.endswith(".jpg") or path.endswith(".jpeg"):
            return "image/jpeg"
        elif path.endswith(".gif"):
            return "image/gif"
        elif path.endswith(".svg"):
            return "image/svg+xml"
        elif path.endswith(".woff"):
            return "font/woff"
        elif path.endswith(".woff2"):
            return "font/woff2"
        elif path.endswith(".ttf"):
            return "font/ttf"
        elif path.endswith(".otf"):
            return "font/otf"
        return None

    def _make_response(self, url, path):
        """Create a URLFetcherResponse for a file from the report"""
        file_obj = self._zpt.get(path)
        # Read bytes from the file object
        data = file_obj.read()
        mime_type = self._get_mime_type(path)
        headers = {"Content-Type": mime_type} if mime_type else {}
        # Use a non-file URL to prevent WeasyPrint from trying to read
        # the file from disk later (it extracts path from file:// URLs)
        safe_url = f"memory://zpt/{path}"
        return URLFetcherResponse(safe_url, body=data, headers=headers)

    def fetch(self, url, headers=None):
        """Fetch a resource from the ZipReport file or external URL"""
        if url.startswith("http"):
            return super().fetch(url, headers)

        original_url = url
        # support for both file:// and relative urls
        if url.startswith("file://"):
            url = url[7:]

        # Try the URL as-is first (handles relative paths like "data/image.png")
        if self._zpt.exists(url):
            return self._make_response(original_url, url)

        # Strip leading slash and try again
        if url.startswith("/"):
            stripped = url.lstrip("/")
            if self._zpt.exists(stripped):
                return self._make_response(original_url, stripped)

            # For absolute paths, try to find a matching relative path in the report
            # by progressively stripping path components from the left
            parts = url.split("/")
            for i in range(1, len(parts)):
                relative_path = "/".join(parts[i:])
                if self._zpt.exists(relative_path):
                    return self._make_response(original_url, relative_path)

        return super().fetch(original_url, headers)


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

        # custom weasyprint fetcher using URLFetcher class
        fetcher = ZptURLFetcher(zpt)

        try:
            rpt = HTML(
                base_url="",
                string=io.TextIOWrapper(zpt.get(REPORT_FILE_NAME), encoding="utf-8").read(),
                url_fetcher=fetcher,
            ).write_pdf(None, stylesheets=self._css, font_config=self._fconfig)
        except Exception as e:
            return JobResult(None, False, str(e))
        return JobResult(io.BytesIO(rpt), True, "")
