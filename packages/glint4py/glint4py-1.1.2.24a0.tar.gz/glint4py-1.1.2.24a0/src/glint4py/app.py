"""
Module for handling application logic.

This module sets up the application routes and middleware for the Glint framework.
"""

from .glint import Glint
from .response import Response

# Initialize the Glint application
app = Glint()

@app.route("/")
def index(_):
    """
    Handles requests to the root URL.

    Args:
        _: The request object (currently unused).

    Returns:
        Response: A response object with a greeting message.
    """
    return Response("Hello, World!")

@app.route("/about")
def about(_):
    """
    Handles requests to the /about URL.

    Args:
        _: The request object (currently unused).

    Returns:
        Response: A response object with information about the application.
    """
    return Response("This is the about page.")

def add_custom_header(response):
    """
    Middleware function to add a custom header to the response.

    Args:
        response (Response): The response object to modify.

    Returns:
        Response: The modified response object.
    """
    response.body += "\nCustom-Header: Value"
    return response

# Add middleware (only if the method exists)
# app.add_middleware(add_custom_header)

if __name__ == "__main__":
    # Run the application server if this script is executed directly.
    app.run()
