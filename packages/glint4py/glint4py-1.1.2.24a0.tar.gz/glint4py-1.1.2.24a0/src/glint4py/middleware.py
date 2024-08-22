"""
Module for handling middleware in the Glint web framework.

This module defines the Middleware class, which is used to manage and apply
middleware functions that can process HTTP responses.
"""

from typing import Callable
from .response import Response

class Middleware:
    """Class for managing and applying middleware functions.

    Middleware functions are functions that process HTTP responses before
    they are sent to the client. This class manages a list of such functions
    and applies them in sequence.
    """

    def __init__(self):
        """Initializes the Middleware with an empty list of middleware functions."""
        self.middlewares = []

    def add_middleware(self, middleware_func: Callable[[Response], Response]):
        """Adds a middleware function to the list.

        Args:
            middleware_func (Callable[[Response], Response]): The middleware 
            function to be added. It should accept a response object
            and return a modified response object.

        Raises:
            TypeError: If middleware_func is not callable.
        """
        if not callable(middleware_func):
            raise TypeError("middleware_func must be callable")
        self.middlewares.append(middleware_func)

    def process(self, response: Response) -> Response:
        """Processes the response through all added middleware functions.

        Args:
            response (Response): The response object to be processed by middleware functions.

        Returns:
            Response: The final response object after all middleware functions have been applied.
        """
        for middleware in self.middlewares:
            try:
                response = middleware(response)
            except (TypeError, ValueError) as ex:
                print(f"Middleware processing error: {ex}")
            except Exception as ex:
                print(f"Unexpected error in middleware processing: {ex}")
        return response
