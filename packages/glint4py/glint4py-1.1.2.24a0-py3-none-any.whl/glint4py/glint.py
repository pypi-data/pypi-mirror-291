"""
Module for the Glint web framework.

This module defines the Glint class, which is the core of the Glint web framework.
It handles routing, middleware, error handling, and request processing.
"""

import socket
import logging
from typing import Callable

from .router import Router
from .middleware import Middleware
from .error_handler import ErrorHandler
from .request import Request
from .response import Response

# Configure logging
logging.basicConfig(level=logging.ERROR)

class Glint:
    """The core class for the Glint web framework.

    Manages routing, middleware, error handling, and serves as the entry point 
    for running the application.
    """

    def __init__(self):
        """Initializes the Glint framework with a router, middleware, and error handler."""
        self.router = Router()
        self.middleware = Middleware()
        self.error_handler = ErrorHandler()

    def route(self, path: str):
        """Defines a route for a given path.

        Args:
            path (str): The path for which this route will be used.

        Returns:
            function: A decorator function to register the route handler.
        """
        def decorator(func):
            self.router.add_route(path, func)
            return func
        return decorator

    def use(self, middleware_func: Callable[[Response], Response]):
        """Adds middleware to the framework.

        Args:
            middleware_func (Callable[[Response], Response]): The middleware function to be added.
        """
        self.middleware.add_middleware(middleware_func)

    def handle_request(self, request_line: str) -> Response:
        """Processes an incoming request and returns a response.

        Args:
            request_line (str): The request line from the HTTP request (e.g., 'GET /path HTTP/1.1').

        Returns:
            Response: The response object to be sent back to the client.
        """
        path = request_line.split(' ')[1]
        try:
            request = Request(path)
            handler = self.router.resolve(path)
            response = handler(request)
        except KeyError:
            logging.error("KeyError: Route not found for path %s", path)
            response = self.error_handler.handle_404()
        except ValueError:
            logging.error("ValueError: Invalid request for path %s", path)
            response = self.error_handler.handle_500()

        response = self.middleware.process(response)
        return response

    def run(self, host: str = '127.0.0.1', port: int = 8080):
        """Starts the Glint web server.

        Args:
            host (str, optional): The host to bind the server to (default is '127.0.0.1').
            port (int, optional): The port to bind the server to (default is 8080).
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
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
