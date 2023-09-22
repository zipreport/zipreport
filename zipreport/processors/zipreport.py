import io
import subprocess
import tempfile
from pathlib import Path
from shutil import rmtree

import requests

from zipreport.processors import ProcessorInterface
import zipreport.report.const as const
from zipreport.report.job import ReportJob, JobResult


class ZipReportClient:
    """
    zipreport-server API Client
    """

    def __init__(
        self, url: str, api_key: str, api_version: int = 1, secure_ssl: bool = False
    ):
        """
        Constructor
        :param url: zipreport-server API url
        :param api_key: API key
        :param api_version: API version (default 1)
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
        url = f"{self._url}/v{self._api_version}/render"
        request_data = {
            "report": ("report.zpt", job.get_report().save()),
        }
        for k, v in job.get_options().items():
            request_data[k] = (None, v)

        try:
            session = requests.sessions.session()
            session.headers["X-Auth-Key"] = self._api_key
            r = session.post(url, verify=self._secure_ssl, files=request_data)

            if r.headers.get("Content-Type") == "application/pdf":
                if r.status_code == 200:
                    return JobResult(io.BytesIO(r.content), True, "")

        except Exception as e:
            return JobResult(None, False, str(e))

        return JobResult(None, False, f"HTTP Code {r.status_code}")


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
            job.set_jsevent(True)

        return self._client.exec(job)


class ZipReportCliProcessor(ProcessorInterface):
    """
    Local zipreport-cli report processor
    """

    def __init__(self, cli_path: str, *args):
        """
        Constructor
        :param cli_path: full path to zipreport-cli binary
        """
        self._cli = cli_path
        if not args:
            args = []
        self._args = args

    def process(self, job: ReportJob) -> JobResult:
        """
        Execute a ReportJob by calling the zipreport-cli binary
        :param job: ReportJob
        :return: JobResult
        """
        cmd = self.build_cmd(job)
        report = None
        success = False
        error = ""
        path = None
        try:
            path = Path(tempfile.mkdtemp())
            job.get_report().get_fs().get_backend().zip().extractall(path)

            subprocess.run(cmd, cwd=path, check=True)
            report_file = path / const.PDF_FILE_NAME
            if report_file.exists():
                with open(report_file, "rb") as f:
                    report = io.BytesIO(f.read())
                    success = True

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            PermissionError,
            FileExistsError,
        ) as e:
            error = str(e)

        if path:
            rmtree(path)

        return JobResult(report, success, error)

    def build_cmd(self, job: ReportJob, dest_file: str = const.PDF_FILE_NAME):
        """
        Parse ReportJob options and generate command-line arguments for zipreport-cli
        :param job: ReportJob
        :param dest_file: full path for PDF file to be generated
        :return: list
        """
        opts = job.get_options()
        args = [
            Path(self._cli),
            f"--pagesize={opts[ReportJob.OPT_PAGE_SIZE]}",
            f"--margins={opts[ReportJob.OPT_MARGINS]}",
            f"--timeout={opts[ReportJob.OPT_RENDER_TIMEOUT]}",
            f"--delay={opts[ReportJob.OPT_SETTLING_TIME]}",
        ]

        if opts[ReportJob.OPT_LANDSCAPE]:
            args.append("--no-portrait")

        if opts[ReportJob.OPT_JS_EVENT]:
            args.append("--js-event")
            args.append(f"--js-timeout={opts[ReportJob.OPT_JS_TIMEOUT]}")

        if opts[ReportJob.OPT_IGNORE_SSL_ERRORS]:
            args.append("--ignore-certificate-errors")

        if opts[ReportJob.OPT_NO_INSECURE_CONTENT]:
            args.append("--no-insecure")

        args.extend(self._args)
        args.extend([opts[ReportJob.OPT_MAIN_SCRIPT], dest_file])
        return args
