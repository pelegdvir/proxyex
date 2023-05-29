from http.client import HTTPConnection
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from classification.classifier import Classifier
from content.suites.mock_suite import MockSuite

REAL_SERVER_IP = '127.0.0.1'
REAL_SERVER_PORT = 8000
PROXY_PORT = 8001

classifier = Classifier(suite=MockSuite())


class ExampleProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Connect to the real server
        content_length = int(self.headers.get('Content-Length', 0))
        # Well... GET sometimes have body :(
        request_body = self.rfile.read(content_length) if content_length else b''
        if not classifier.decide_if_pass(
            src_addr=self.client_address[0],
            raw=request_body,
        ):
            self.send_error(403, 'Access denied')
            return

        conn = HTTPConnection(f"{REAL_SERVER_IP}:{REAL_SERVER_PORT}", timeout=1)
        conn.request("GET", self.path)
        res = conn.getresponse()
        self.send_response(res.status)
        self.send_header('Via', 'proxy')
        for header in res.getheaders():
            self.send_header(header[0], header[1])
        self.end_headers()
        self.copyfile(res.fp, self.wfile)
        conn.close()

    def do_POST(self):
        # Connect to the real server
        content_length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(content_length) if content_length else b''
        if not classifier.decide_if_pass(
            src_addr=self.client_address[0],
            raw=request_body,
        ):
            self.send_error(403, 'Access denied')
            return

        conn = HTTPConnection(f"{REAL_SERVER_IP}:{REAL_SERVER_PORT}", timeout=1)
        conn.request("POST", self.path)
        res = conn.getresponse()
        self.send_response(res.status)
        self.send_header('Via', 'proxy')
        for header in res.getheaders():
            self.send_header(header[0], header[1])
        self.end_headers()
        self.copyfile(res.fp, self.wfile)
        conn.close()


def run():
    port = PROXY_PORT
    with ThreadingHTTPServer(("", port), ExampleProxyHandler) as server:
        print(f"Starting proxy server on port {port}")
        server.serve_forever()


run()
