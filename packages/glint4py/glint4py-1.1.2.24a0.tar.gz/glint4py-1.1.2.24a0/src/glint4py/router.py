"""
Module for handling HTTP routing in the Glint web framework.

This module defines the Router class, which is responsible for managing
HTTP routes and resolving them to appropriate handlers.
"""

from typing import Callable, Dict
from .response import Response
from .request import Request

class Router:
    """Manages and resolves HTTP routes.

    The Router class is used to register routes and their associated
    handler functions. It also provides a method to resolve a request
    path to the corresponding handler or return a 404 Not Found response
    if the path is not registered.
    """

    def __init__(self):
        """Initializes the Router with an empty dictionary of routes."""
        self.routes: Dict[str, Callable[[Request], Response]] = {}

    def add_route(self, path: str, handler: Callable[[Request], Response]) -> None:
        """Registers a route with a path and its handler function.

        Args:
            path (str): The path for which this route should be handled.
            handler (Callable[[Request], Response]): The function to handle requests to this path.
                                                     It should accept a Request object and return
                                                     a Response object.

        Raises:
            TypeError: If handler is not callable.
        """
        if not callable(handler):
            raise TypeError("handler must be callable")
        self.routes[path] = handler

    def resolve(self, path: str) -> Callable[[Request], Response]:
        """Resolves a path to its handler function.

        Args:
            path (str): The path to resolve.

        Returns:
            Callable[[Request], Response]: The handler function associated with the path, or the
                                           not_found handler if the path is not registered.
        """
        return self.routes.get(path, self.not_found)

    def not_found(self, _: Request) -> Response:
        """Handles requests to unregistered paths with a 404 Not Found response.

        Args:
            _: The request object for which no handler was found.

        Returns:
            Response: A response object indicating a 404 Not Found error.
        """
        return Response("404 Not Found", 404)
