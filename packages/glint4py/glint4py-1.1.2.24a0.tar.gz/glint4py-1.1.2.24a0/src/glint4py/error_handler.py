"""
Module for handling errors.

This module defines error handling methods for the application,
including handling 404 Not Found and 500 Internal Server Error responses.
"""

from .response import Response

class ErrorHandler:
    """Class to handle different types of HTTP errors.

    Provides methods to generate error responses for 404 and 500 errors.
    """

    def handle_404(self) -> Response:
        """
        Generate a 404 Not Found response.

        Returns:
            Response: A response object with a 404 status code and a message
            indicating the resource was not found.
        """
        return Response("404 Not Found", 404)

    def handle_500(self) -> Response:
        """
        Generate a 500 Internal Server Error response.

        Returns:
            Response: A response object with a 500 status code and a message
            indicating an internal server error occurred.
        """
        return Response("500 Internal Server Error", 500)
