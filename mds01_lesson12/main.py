import mimetypes
import json
import socket
import logging
from urllib.parse import urlparse, unquote_plus
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from jinja2 import Environment, FileSystemLoader
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = "mongodb://mds01_lesson12-mongodb-1:27017"
BASE_DIR = Path(__file__).parent
BUFFER_SIZE = 1024
HTTP_PORT = 8080
HTTP_HOST = '0.0.0.0'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 4000
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

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data.encode(), (SOCKET_HOST, SOCKET_PORT))
        client_socket.close()
        # print(unquote_plus(data))

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


def save_data(data):
    client = MongoClient(URI)
    db = client.homework
    parse_data = unquote_plus(data.decode())
    try:
        parse_data = {key: value for key, value in [el.split("=") for el in parse_data.split("&")]}
        db.messages.insert_one(parse_data)
    except ValueError as e:
        logging.error(f"Parse error: {e}")
    except Exception as e:
        logging.error(f"Failed to save: {e}")
    finally:
        client.close()


def run_http_server():
    httpd = HTTPServer((HTTP_HOST, HTTP_PORT), CatFramework)
    try:
        logging.info(f"Server started on http://{HTTP_HOST}:{HTTP_PORT}")
        httpd.serve_forever()
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        logging.info("Server stopped")
        httpd.server_close()


def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SOCKET_HOST, SOCKET_PORT))
    logging.info(f"Server started on socket://{SOCKET_HOST}:{SOCKET_PORT}")
    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            logging.info(f"Get message from {addr}: {data.decode()}")
            save_data(data)
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        logging.info("Server stopped")
        sock.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(threadName)s - %(message)s")
    http_thread = Thread(target=run_http_server, name="http_server")
    http_thread.start()

    socket_thread = Thread(target=run_socket_server, name="socket_server")
    socket_thread.start()
