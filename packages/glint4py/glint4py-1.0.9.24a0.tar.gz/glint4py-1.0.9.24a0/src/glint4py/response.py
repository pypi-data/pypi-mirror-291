"""
Module for handling HTTP responses in the Glint web framework.

This module defines the Response class, which represents an HTTP response
that can be sent to the client. It encapsulates response data such as
the response body and status code.
"""

class Response:
    """Represents an HTTP response.

    The Response class encapsulates information about an HTTP response,
    including the response body and status code. It also provides methods
    to modify the response and convert it into the HTTP response format
    used in HTTP communication.
    """

    STATUS_MESSAGES = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error",
        # Add other status codes and messages as needed
    }

    def __init__(self, body: str, status_code: int = 200):
        """Initializes a Response instance.

        Args:
            body (str): The body of the HTTP response, which is the content
                        to be sent to the client.
            status_code (int, optional): The HTTP status code for the response.
                                          Defaults to 200 (OK).

        Raises:
            ValueError: If status_code is not within the valid range (100-599).
        """
        if not 100 <= status_code <= 599:
            raise ValueError("Invalid status code. Must be between 100 and 599.")
        self.body = body
        self.status_code = status_code
        self.headers = {
            "Content-Type": "text/html; charset=UTF-8"  # Default content type
        }

    def to_http_response(self) -> str:
        """Converts the Response instance to an HTTP response string.

        Returns:
            str: The HTTP response formatted as a string, including the status
                 line, headers, and body.
        """
        status_message = self.STATUS_MESSAGES.get(self.status_code, "Unknown Status")
        headers = [
            f"Content-Length: {len(self.body)}",
            *[f"{key}: {value}" for key, value in self.headers.items()]
        ]
        return (
            f"HTTP/1.1 {self.status_code} {status_message}\r\n"
            + "\r\n".join(headers) + "\r\n\r\n"
            + self.body
        )

    def get_status_message(self) -> str:
        """Returns the status message for the current status code.

        Returns:
            str: The status message corresponding to the status code.
        """
        return self.STATUS_MESSAGES.get(self.status_code, "Unknown Status")

    def set_body(self, body: str):
        """Sets the body of the response.

        Args:
            body (str): The new body content for the HTTP response.
        """
        self.body = body

    def set_status_code(self, status_code: int):
        """Sets the status code of the response.

        Args:
            status_code (int): The new HTTP status code.

        Raises:
            ValueError: If status_code is not within the valid range (100-599).
        """
        if not 100 <= status_code <= 599:
            raise ValueError("Invalid status code. Must be between 100 and 599.")
        self.status_code = status_code

    def add_header(self, key: str, value: str):
        """Adds or updates a custom header in the response.

        Args:
            key (str): The header name.
            value (str): The header value.
        """
        self.headers[key] = value
