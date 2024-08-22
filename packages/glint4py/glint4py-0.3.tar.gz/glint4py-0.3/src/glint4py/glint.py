import socket

from .router import Router
from .middleware import Middleware
from .error_handler import ErrorHandler
from .request import Request
from .response import Response

class Glint:
    def __init__(self):
        self.router = Router()
        self.middleware = Middleware()
        self.error_handler = ErrorHandler()

    def route(self, path: str):
        def decorator(func):
            self.router.add_route(path, func)
            return func
        return decorator

    def use(self, middleware_func):
        self.middleware.add_middleware(middleware_func)

    def handle_request(self, request_line: str):
        path = request_line.split(' ')[1]
        try:
            request = Request(path)
            handler = self.router.resolve(path)
            response = handler(request)
        except Exception as e:
            response = self.error_handler.handle_500()
        response = self.middleware.process(response)
        return response

    def run(self, host: str = '127.0.0.1', port: int = 8080):
        with socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()
            print(f"Listening on http://{host}:{port}")

            while True:
                client_socket, _ = server_socket.accept()
                with client_socket:
                    request_data = client_socket.recv(1024).decode()
                    if not request_data:
                        continue
                    request_line = request_data.splitlines()[0]
                    response = self.handle_request(request_line)
                    client_socket.sendall(response.to_http_response().encode())
