import io
import requests

from zipreport.processors import ProcessorInterface
import zipreport.report.const as const
from zipreport.report.job import ReportJob, JobResult


class ZipReportClient:
    """
    zipreport-server API Client
    """

    def __init__(
        self, url: str, api_key: str, api_version: int = 2, secure_ssl: bool = False
    ):
        """
        Constructor
        :param url: zipreport-server API url
        :param api_key: API key
        :param api_version: API version (default 2)
        :param secure_ssl: check SSL CA (default False)
        """
        self._api_key = api_key
        self._url = url
        self._secure_ssl = secure_ssl
        self._api_version = api_version
        # assemble headers

    def exec(self, job: ReportJob) -> JobResult:
        """
        Execute a ReportJob using API
        :param job: ReportJob
        :return: JobResult
        """
        url = "{}/v{}/render".format(self._url, self._api_version)
        request_data = {
            "report": ("report.zpt", job.get_report().save()),
        }
        for k, v in job.get_options().items():
            request_data[k] = (None, v)

        try:
            session = requests.sessions.session()
            session.headers["X-Auth-Key"] = self._api_key
            r = session.post(url, verify=self._secure_ssl, files=request_data)

            if r.status_code == 200:
                if r.headers.get("Content-Type") == "application/pdf":
                    return JobResult(io.BytesIO(r.content), True, "")

        except Exception as e:
            return JobResult(None, False, str(e))

        return JobResult(None, False, "HTTP Code {}".format(r.status_code))


class ZipReportProcessor(ProcessorInterface):
    """
    Zipreport-server API report processor
    """

    def __init__(self, client: ZipReportClient):
        """
        Constructor
        :param client: API Client
        """
        self._client = client

    def process(self, job: ReportJob) -> JobResult:
        """
        Execute a ReportJob using the API client
        :param job: ReportJob
        :return: JobResult
        """
        zpt = job.get_report()
        # if manifest signals js event, enable it
        if zpt.get_param(const.MANIFEST_JS_EVENT, False):
            job.use_jsevent(True)

        return self._client.exec(job)
