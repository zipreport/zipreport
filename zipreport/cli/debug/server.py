import io
import mimetypes
import posixpath
import shutil
import sys
from functools import partial
from urllib.parse import urlparse, urlsplit, unquote
from pathlib import Path
from typing import Union, Tuple
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

from zipreport.report import ReportFile, ReportFileLoader, ReportFileBuilder, const
from zipreport.template import JinjaRender

# shared ReportFile Object to be reused between requests
_zpt = None


class ReportFileHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET and HEAD commands.

    This class is based on the SimpleHTTPRequestHandler in http.server
    Due to its simplified implementation, the code is not thread-safe!!!
    """

    server_version = "ZipReport HTTP Server"
    root_paths = ['/', '/index.html', '/index.htm', '/report.html', '/report.htm', ]
    extensions_map = {
        '': 'application/octet-stream',
    }

    def __init__(self, *args, report_path=None, extra_mime_types=None, **kwargs):
        """
        Constructor
        :param args:
        :param report_path: path of the directory or zpt file to process
        :param extra_mime_types: optional extra mime types to register
        :param kwargs:
        """
        self.bootstrap_mime_types(extra_mime_types)
        if report_path is None:
            raise RuntimeError("Debug HTTP Server must work with a generated report")
        self.report_path = Path(report_path)
        self.is_report_file = self.report_path.is_file()
        self.enc = sys.getfilesystemencoding()

        super().__init__(*args, **kwargs)

    def bootstrap_mime_types(self, extra_mime_types: dict = None):
        """
        Bootstrap mime types
        :param mime_types: dictionary of entries to add/replace
        :return:
        """
        # try to use system mimetypes
        if not mimetypes.inited:
            mimetypes.init()
        self.extensions_map.update(mimetypes.types_map)
        # add extra mimetypes if necessary
        if extra_mime_types is not None:
            self.extensions_map.update(extra_mime_types)

    def build_report(self) -> Tuple[bool, Union[io.BytesIO, None]]:
        """
        Assembles, builds and renders the report file
        In case of errors, response is (False, io.BytesIO(response_message)), with headers already processed
        In case of success, response is (True, io.BytesIO()); response should be processed from the zpt path for the report file
        :return: (bool, io.BytesIO)
        """
        global _zpt
        _zpt = None
        try:
            # load file or build file, according to path
            if self.is_report_file:
                sys.stdout.write("Reloading report file...\n")
                _zpt = ReportFileLoader.load_file(self.report_path)
            else:
                sys.stdout.write("Rebuilding report from path...\n")
                bresult, zpt = ReportFileBuilder.build_zipfs(self.report_path)
                if not bresult.success():
                    return False, self.error_500(";".join(bresult.get_errors()))
                # create ReportFile from zipfs
                _zpt = ReportFileLoader.load_zipfs(zpt)
            # render template to REPORT_FILE_NAME
            # returns a dummy BytesIO object
            JinjaRender(_zpt).render()
            return True, io.BytesIO()

        except Exception as e:
            return False, self.error_500(str(e))

    def do_GET(self):
        """
        Process a GET request
        :return:
        """
        response = self.process_request()
        if response:
            try:
                shutil.copyfileobj(response, self.wfile)
            finally:
                response.close()

    def do_HEAD(self):
        """
        Process a HEAD request
        :return:
        """
        response = self.process_request()
        if response:
            response.close()

    def process_request(self):
        """
        Common request processing logic
        :return: io.BytesIO()
        """
        global _zpt
        path = self.clean_path(self.path)
        response = None

        if _zpt is None:
            success, response = self.build_report()
            if not success:
                return response

        if path in self.root_paths:
            if response is None:
                success, response = self.build_report()
                if not success:
                    return response
            # rewrite path to point to report file
            path = '/' + const.REPORT_FILE_NAME

        if _zpt.exists(path):
            return self.handle_file(Path(path).name, _zpt.get(path))

        # path not found
        return self.error_404(path)

    def clean_path(self, path: str) -> str:
        """
        Cleans up the request path
        :param path:str
        """
        # remove ignored parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        try:
            path = unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = unquote(path)
        return posixpath.normpath(path)

    def guess_type(self, fname: str):
        """
        Tries to determine a filename mime type
        """
        base, ext = posixpath.splitext(fname)
        if ext in self.extensions_map:
            return self.extensions_map[ext]

        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]

        return self.extensions_map['']

    def handle_file(self, fname: str, contents: io.BytesIO) -> io.BytesIO:
        """
        Generates response headers for a given file
        :param fname:
        :param contents:
        :return: io.BytesIO
        """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", self.guess_type(fname))
        self.send_header("Content-Length", str(contents.getbuffer().nbytes))
        self.end_headers()
        contents.seek(0)
        return contents

    def error_500(self, item: str):
        """
        Generates a customized 500 response
        :param item: optional error message
        :return: io.BytesIO
        """
        if item:
            response = "<html><body><h3>Internal Server Error: {}</h3></body></html>".format(item)
        else:
            response = "<html><body><h3>File not found</h3></body></html>"
        return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, response)

    def error_404(self, item: str = None) -> io.BytesIO:
        """
        Generates a customized 404 response
        :param item: optional error message
        :return: io.BytesIO
        """
        if item:
            response = "<html><body><h3>File not found: {}</h3></body></html>".format(item)
        else:
            response = "<html><body><h3>File not found</h3></body></html>"
        return self._error(HTTPStatus.NOT_FOUND, response)

    def _error(self, code: int, contents: str) -> io.BytesIO:
        """
        Common error response logic
        :param code: HTTP status code
        :param contents: optional HTML response
        :return: io.BytesIO
        """
        size = len(contents)
        response = io.BytesIO(bytes(contents, encoding='utf-8'))
        self.send_response(code)
        self.send_header("Content-type", "text/html; charset=%s" % sys.getfilesystemencoding())
        self.send_header("Content-Length", str(size))
        self.end_headers()
        response.seek(0)
        return response


class DebugServer:
    DEFAULT_ADDR = 'localhost'
    DEFAULT_PORT = 8001

    def __init__(self, addr: str = DEFAULT_ADDR, port: int = DEFAULT_PORT):
        self._addr = addr
        self._port = port

    def set_addr(self, addr: str):
        self._addr = addr

    def set_port(self, port: int):
        self._port = port

    def run(self, report_path: str):
        server_address = (self._addr, int(self._port))
        handler_class = partial(ReportFileHandler, report_path=report_path)
        sys.stdout.write(
            "\nStarted debug server at http://{addr}:{port}\nServing from: {path}\nUse Ctrl+C to stop...\n\n".format(
                addr=self._addr, port=int(self._port), path=Path(report_path).absolute()))
        httpd = HTTPServer(server_address, handler_class)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        return
