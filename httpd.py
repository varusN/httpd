import argparse
import datetime
import logging
import mimetypes
import multiprocessing
import os
import socket
import threading
import urllib.parse

OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
ERRORS = {
    OK: "OK",
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    METHOD_NOT_ALLOWED: "Method Not Allowed",
}

logging.basicConfig(filename=None, level=logging.INFO,
                    format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')


class NotFound(Exception):
    pass


class Forbidden(Exception):
    pass


class MethodNotAllowed(Exception):
    pass


class BadRequest(Exception):
    pass


class HTTPServer:
    def __init__(self, bind_ip: str, bind_port: int):
        self.max_conn = 10
        self.bind_port = bind_port
        self.bind_ip = bind_ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.bind_ip, self.bind_port))
        except OSError as e:
            logging.exception(f"Can't open socket: {e}")
        self.socket.listen(self.max_conn)
        logging.info(f'HTTP server listening on address {self.bind_ip} and port {self.bind_port}')
        return self.socket

    def shutdown(self):
        try:
            self.socket.shutdown(socket.SHUT_WR)
        except OSError:
            pass

    def listener(self, doc_root: str):
        try:
            while True:
                try:
                    client, _ = self.socket.accept()
                    client_handler = threading.Thread(
                        target=handle_request,
                        args=(client, doc_root, )  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
                    )
                    client_handler.start()
                except OSError as e:
                    logging.exception(f"Can't initiate listener: {e}")
                    if client:
                        client.close()
        finally:
            self.shutdown()


def read_request(client: socket) -> str:
    request = ''
    while True:
        chunk = (client.recv(1024)).decode('utf8')
        request += chunk
        if len(chunk) < 1024:
            break
    return request


def parse_request(request_str: str) -> (str, str):
    request_str = tuple(request_str.split('\r\n\r\n'))
    http_lines = request_str[0].split('\r\n')
    try:
        method, url, _ = http_lines[0].split(' ')
    except Exception:
        raise BadRequest
    if method not in ('GET', 'HEAD'):
        raise MethodNotAllowed
    return method, url


def url_to_path(url: str, doc_root: str) -> str:
    if '../' in url:
        raise Forbidden
    path = url.split('?')[0].split("#")[0]
    if os.path.isdir(path):
        path = os.path.abspath(os.path.join(path, 'index.html'))
    if path.endswith('/'):
        path = path + 'index.html'
    path = urllib.parse.unquote(path)
    return path


def load_body(path: str, doc_root: str) -> (str, str):
    try:
        with open(f"{doc_root}/{path}", 'rb') as f:
            body = f.read()
        cont_type = mimetypes.guess_type(f"{doc_root}/{path}", strict=True)
    except FileNotFoundError:
        raise NotFound
    return cont_type[0], body


def build_response(request: str, doc_root: str) -> bytes:
    code = ''
    method = ''
    try:
        method, url = parse_request(request)
        try:
            path = url_to_path(url, doc_root)
            try:
                cont_type, body = load_body(path, doc_root)
            except NotFound:
                code = NOT_FOUND
        except Forbidden:
            code = FORBIDDEN
    except MethodNotAllowed:
        code = METHOD_NOT_ALLOWED
    except BadRequest:
        code = BAD_REQUEST
    if not code:
        code = OK
        response = (f'HTTP/1.1 {code} {ERRORS.get(code)}\r\n'
                    f'Date: {datetime.datetime.utcnow().strftime("%a, %d %b %G %T GMT")}\r\n'
                    'Accept-Ranges: bytes\r\n'
                    'Server: Otus-HTTP-1.1\r\n'
                    f'Content-Type: {cont_type}\r\n'
                    f'Content-Length: {len(body)}\r\n'
                    f'Connection: close\r\n'
                    '\r\n').encode('utf-8')
        if method == 'GET':
            if body:
                response += body
    else:
        response = (f'HTTP/1.1 {code} {ERRORS.get(code)}\r\n'
                    f'Date: {datetime.datetime.utcnow().strftime("%a, %d %b %G %T GMT")}\r\n'
                    'Server: Otus-HTTP-1.1\r\n'
                    f'Connection: close\r\n'
                    '\r\n').encode('utf-8')
    return response


def handle_request(client, doc_root):
    request = read_request(client)
    response = build_response(request, doc_root)
    client.sendall(response)
    client.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Basic HTTP server')
    parser.add_argument(
        '-i', '--interface', type=str, default='127.0.0.1',
        help='Interface to open listener, default - 127.0.0.1'
    )

    parser.add_argument(
        '-p', '--port', type=int, default=80,
        help='Port to open listener, default - 80'
    )

    parser.add_argument(
        '-w', '--workers', type=int, default=5,
        help='server workers count, default - 5'
    )
    parser.add_argument(
        '-r', '--root', type=str, default='static',
        help='DIRECTORY_ROOT with site files, default - ./static'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    server = HTTPServer(args.interface, args.port)
    server.start()
    logging.info(f'Starting {args.workers} workers, root dir: ./{args.root}')
    DOCUMENT_ROOT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        args.root
    )

    workers = []
    try:
        for i in range(args.workers):
            worker = multiprocessing.Process(target=server.listener, args=(DOCUMENT_ROOT, ))
            workers.append(worker)
            worker.start()
            logging.info(f'Worker {i+1} started')
        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        for worker in workers:
            if worker:
                worker.terminate()
        logging.info('Exit')
