from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

from zipreport.cli.debug.server import DebugServer


class DebugServerHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, report=None, **kwargs):
        self._report = report
        super().__init__(*args, **kwargs)


    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        print(self.path)
        print("Received:", self.command, self.path)
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())



#server_address = ('', 8000)
#httpd = HTTPServer(server_address, DebugServerHandler)
#httpd.report = "tadaa"
#httpd.serve_forever()


server = DebugServer()
server.run('./examples/reports/newsletter')
