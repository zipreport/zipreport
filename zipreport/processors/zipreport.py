import collections
import hashlib
import io
import time
import uuid
from typing import Union

import requests

from zipreport.processors.interface import ProcessorInterface
from zipreport.report import ReportFile
import zipreport.report.const as const
from zipreport.report.job import ReportJob, JobResult


class ZipReportClient:

    def __init__(self, url: str, api_key: str, api_version: int = 1, secure_ssl: bool = False):
        self._api_key = api_key
        self._url = url
        self._secure_ssl = secure_ssl
        self._api_version = api_version
        # assemble headers

    def exec(self, job: ReportJob) -> JobResult:

        url = "{}/v{}/render".format(self._url, self._api_version)
        request_data = {
            'report': ('report.zpt', job.get_report().save()),
        }
        for k, v in job.get_options().items():
            request_data[k] = (None, v)

        try:
            session = requests.sessions.session()
            session.headers['X-Auth-Key'] = self._api_key
            r = session.post(url, verify=self._secure_ssl, files=request_data)

            if r.status_code == 200:
                if r.headers.get('Content-Type') == "application/pdf":
                    return JobResult(io.BytesIO(r.content), True, "")

        except Exception as e:
            return JobResult(None, False, str(e))

        return JobResult(None, False, "HTTP Code {}".format(r.status_code))


class ZipReportProcessor(ProcessorInterface):

    def __init__(self, client: ZipReportClient):
        self._client = client

    def process(self, job: ReportJob) -> JobResult:

        zpt = job.get_report()
        # if manifest signals js event, enable it
        if zpt.get_param(const.MANIFEST_JS_EVENT, False):
            job.set_jsevent(True)

        # if manifest has a different main script, use it instead
        report_file = zpt.get_param(const.MANIFEST_REPORT, "")
        if len(report_file) > 0:
            job.set_main_script(report_file)

        return self._client.exec(job)
