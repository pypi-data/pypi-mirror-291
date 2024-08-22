class Middleware:
    def __init__(self):
        self.middlewares = []

    def add_middleware(self, middleware_func):
        self.middlewares.append(middleware_func)

    def process(self, response):
        for middleware in self.middlewares:
            response = middleware(response)
        return response
