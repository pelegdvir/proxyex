from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

EXAMPLE_SERVER_PORT = 8000


class ExampleHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self._send_body()

    def do_POST(self):
        self.send_response(201)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self._send_body()

    def _send_body(self):
        self.wfile.write(self.path.encode())
        self.wfile.write(b'\n')
        self.wfile.write(str(self.client_address[0]).encode())
        self.wfile.write(b'\n')
        for header in self.headers:
            self.wfile.write(header.encode())
            self.wfile.write(b': ')
            self.wfile.write(self.headers[header].encode())
            self.wfile.write(b'\n')


def run():
    port = EXAMPLE_SERVER_PORT
    with ThreadingHTTPServer(("", port), ExampleHandler) as server:
        print(f"Starting server on port {port}")
        server.serve_forever()


run()
