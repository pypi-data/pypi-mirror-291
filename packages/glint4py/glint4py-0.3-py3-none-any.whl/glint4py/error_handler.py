from response import Response

class ErrorHandler:
    def handle_404(self):
        return Response("404 Not Found", 404)

    def handle_500(self):
        return Response("500 Internal Server Error", 500)
