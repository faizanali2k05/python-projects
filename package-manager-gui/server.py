from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import backend

class Handler(BaseHTTPRequestHandler):

    def render(self, output=""):
        with open("index.html") as f:
            page = f.read()
        self.wfile.write(page.replace("{{OUTPUT}}", output).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.render("Welcome! Select an action.")

    def do_POST(self):
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length).decode()
        params = parse_qs(data)

        action = params.get("action", [""])[0]
        pkg = params.get("package", [""])[0]

        if action == "user":
            output = backend.user_packages()
        elif action == "system":
            output = backend.system_packages()
        elif action == "install":
            output = backend.install(pkg)
        elif action == "remove":
            output = backend.remove(pkg)
        elif action == "update":
            output = backend.update(pkg)
        else:
            output = "Invalid action"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.render(output)

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("GUI running at http://localhost:8000")
server.serve_forever()
