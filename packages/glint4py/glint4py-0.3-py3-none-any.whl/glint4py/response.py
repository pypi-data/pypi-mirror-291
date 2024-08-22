class Response:
    def __init__(self, body: str, status_code: int = 200):
        self.body = body
        self.status_code = status_code

    def to_http_response(self) -> str:
        return f"HTTP/1.1 {self.status_code} OK\r\nContent-Length: {len(self.body)}\r\n\r\n{self.body}"
