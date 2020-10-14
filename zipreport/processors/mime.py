import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
from html.parser import HTMLParser

from zipreport.processors.interface import ProcessorInterface
from zipreport.report import JobResult, ReportJob


class ResourceParser(HTMLParser):
    """
    Custom HTML parser
    Generates a list of all local (relative) src and href resources
    """

    def __init__(self, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self._href = []
        self._src = []

    def reset(self):
        super().reset()
        self._src = []
        self._href = []

    def handle_starttag(self, tag, attrs):
        if not len(attrs):
            return
        attrs = dict(attrs)
        if 'src' in attrs.keys():
            src = attrs['src']
            if self.is_local(src):
                self._src.append(src)

        elif 'href' in attrs.keys() and tag.lower() == 'link':
            src = attrs['href']
            if self.is_local(src):
                self._href.append(src)

    def get_src_list(self) -> list:
        return list(dict.fromkeys(self._src))

    def get_href_list(self) -> list:
        return list(dict.fromkeys(self._href))

    def get_resource_list(self) -> list:
        a = self.get_src_list()
        a.extend(self.get_href_list())
        return list(dict.fromkeys(a))

    def is_local(self, url: str):
        url = url.lower()
        for prefix in ['http://', 'https://', '//']:
            if url.startswith(prefix):
                return False
        return True


class MIMEProcessor(ProcessorInterface):

    def process(self, job: ReportJob) -> JobResult:
        """
        Executes a rendering job to a MIME message
        Local resources such as images are embedded in the message
        :param job: ReportJob
        :return: JobResult
        """
        opts = job.get_options()
        rpt = job.get_report()
        html = str(rpt.get(opts[job.OPT_MAIN_SCRIPT]).read(), encoding='utf-8')

        mime_msg = EmailMessage()
        parser = ResourceParser()
        parser.feed(html)

        resources = {}
        # replace html references with cid
        for src in parser.get_resource_list():
            cid = make_msgid()
            resources[cid] = src
            html = html.replace('="{}"'.format(src), '="cid:{}"'.format(cid[1:-1]))
            html = html.replace("='{}'".format(src), "='cid:{}'".format(cid[1:-1]))

        mime_msg.add_alternative(html, subtype='html')

        # add related resources
        payload = mime_msg.get_payload()[0]
        for cid, fname in resources.items():
            res = rpt.get(fname)
            ctype, encoding = mimetypes.guess_type(fname)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            payload.add_related(res.read(), maintype, subtype, cid=cid)

        return JobResult(mime_msg, True, "")
