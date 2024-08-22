"""
Module for handling HTTP requests in the Glint web framework.

This module defines the Request class, which represents an HTTP request
received by the Glint web framework. It encapsulates request data such as
the request path.
"""

class Request:
    """Represents an HTTP request.

    The Request class is used to encapsulate information about an HTTP
    request, including the requested path. Currently, this class only
    handles the request path but can be extended in the future.
    """

    def __init__(self, path: str):
        """Initializes a Request instance.

        Args:
            path (str): The path of the HTTP request, which is the part of the URL
                        that follows the domain name (e.g., '/home').

        Raises:
            ValueError: If the path is not a valid string.
        """
        if not isinstance(path, str) or not path.startswith('/'):
            raise ValueError("path must be a string starting with '/'")
        self.path = path

    def __repr__(self) -> str:
        """Provides a string representation of the Request instance.

        Returns:
            str: A string representation of the request path.
        """
        return f"Request(path={self.path!r})"

    def get_path(self) -> str:
        """Returns the request path.

        Returns:
            str: The path of the HTTP request.
        """
        return self.path

    def is_valid(self) -> bool:
        """Checks if the request path is valid.

        Returns:
            bool: True if the path is a valid string starting with '/', False otherwise.
        """
        return isinstance(self.path, str) and self.path.startswith('/')

    def get_segments(self) -> list:
        """Splits the path into segments.

        Returns:
            list: A list of path segments.
        """
        return self.path.strip('/').split('/')