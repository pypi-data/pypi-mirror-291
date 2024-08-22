from .response import Response

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path: str, handler):
        self.routes[path] = handler

    def resolve(self, path: str):
        return self.routes.get(path, self.not_found)

    def not_found(self, request):
        return Response("404 Not Found", 404)