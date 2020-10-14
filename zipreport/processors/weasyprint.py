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

        rpt = HTML(
            base_url="/",
            string=io.TextIOWrapper(zpt.get(REPORT_FILE_NAME), encoding='utf-8').read(),
            url_fetcher=f
        ).write_pdf(None, stylesheets=self._css, font_config=self._fconfig)
        return JobResult(io.BytesIO(rpt), True, "")

    def fetcher(self, zpt, url):
        """
        Internal fetcher for WeasyPrint to access in-report resources such as images, css and js
        :param zpt: ReportFile
        :param url: url of te resource to fetch
        :return:
        """
        if url.startswith("http"):
            return default_url_fetcher(url)

        fallback = url
        # support for both file:// and relative urls
        if url.startswith('file://'):
            url = url[7:]

        if zpt.exists(url):
            return {'string': zpt.get(url).read()}

        return default_url_fetcher(fallback)
