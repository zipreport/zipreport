from zipreport.processors.interface import ProcessorInterface
from zipreport.processors import ZipReportProcessor, ZipReportClient, ZipReportCliProcessor, MIMEProcessor, \
    WkHtml2PdfProcessor
from zipreport.report import ReportFile
from zipreport.report.job import ReportJob, JobResult
from zipreport.template import JinjaRender


class BaseReport:
    """
    Common base class for simple report generation
    """

    def __init__(self, processor: ProcessorInterface):
        if not isinstance(processor, ProcessorInterface):
            raise RuntimeError("Invalid processor")
        self._processor = processor

    @staticmethod
    def create_job(zpt: ReportFile) -> ReportJob:
        """
        Creates a ReportJob from a ReportFile
        :param zpt: ReportFile to use
        :return: newly created ReportJob
        """
        if not isinstance(zpt, ReportFile):
            raise RuntimeError("Invalid report file")
        return ReportJob(zpt)

    def render(self, job: ReportJob, data: dict = None) -> JobResult:
        """
        Render a report job, using Jinja
        :param job: ReportJob to render
        :param data: dict of variables for the report
        :return: JobResult
        """
        if not isinstance(job, ReportJob):
            raise RuntimeError("Invalid report file")
        JinjaRender(job.get_report()).render(data)
        return self._processor.process(job)

    def render_defaults(self, zpt: ReportFile, data: dict = None) -> JobResult:
        """
        Render a report file
        It will create a ReportJob with default configuration
        :param zpt: ReportFile to use
        :param data: dict of variables for the report
        :return: JobResult
        """
        return self.render(self.create_job(zpt), data)


class ZipReport(BaseReport):
    """
    zipreport-server API based report generation
    """

    def __init__(self, url: str, api_key: str, api_version: int = 1, secure_ssl: bool = False):
        """
        Constructor
        :param url: zipreport-server url
        :param api_key: zipreport-server api key
        :param api_version: api version (default 1)
        :param secure_ssl: if true, verifies CA validity for SSL certificates (default false)
        """
        super(ZipReport, self).__init__(ZipReportProcessor(ZipReportClient(url, api_key, api_version, secure_ssl)))


class ZipReportCli(BaseReport):
    """
    zipreport-cli local report generation
    """

    def __init__(self, cli_path: str):
        """
        Constructor
        :param cli_path: full path to zipreport-cli binary
        """
        super(ZipReportCli, self).__init__(ZipReportCliProcessor(cli_path))


class WkHtml2PdfReport(BaseReport):
    """
    wkhtmltopdf report generation
    """

    def __init__(self, cli_path: str):
        """
        Constructor
        :param cli_path: full path to wkhtmltopdf binary
        """
        super(WkHtml2PdfReport, self).__init__(WkHtml2PdfProcessor(cli_path))


class MIMEReport(BaseReport):
    """
    MIME email generation
    """

    def __init__(self):
        """
        Constructor
        """
        super(MIMEReport, self).__init__(MIMEProcessor())
