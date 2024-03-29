import mimetypes
import json
from urllib.parse import urlparse, unquote_plus
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
jinja = Environment(loader=FileSystemLoader(BASE_DIR.joinpath("templates")))


class CatFramework(BaseHTTPRequestHandler):
    def do_GET(self):
        router = urlparse(self.path).path
        match router:
            case "/":
                self.send_html("index.html")
            case "/contact":
                self.send_html("contact.html")
            case "/blog":
                self.render_template("blog.jinja")
            case _:
                file = BASE_DIR.joinpath(router[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("404.html", 404)

    def do_POST(self):
        size = self.headers.get("Content-Length")
        data = self.rfile.read(int(size)).decode()
        print(unquote_plus(data))
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_html(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def render_template(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('db/data.json', 'r', encoding='utf-8') as f:
            content = json.load(f)

        template = jinja.get_template(filename)
        html = template.render(content=content, title="Блог").encode()
        self.wfile.write(html)

    def send_static(self, filename, status=200):
        self.send_response(status)
        mimetype = mimetypes.guess_type(filename)[0] if mimetypes.guess_type(filename)[0] else "text/plain"
        self.send_header("Content-type", mimetype)
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())


def run_server():
    httpd = HTTPServer(("localhost", 8000), CatFramework)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
