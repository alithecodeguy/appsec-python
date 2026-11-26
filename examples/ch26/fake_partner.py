from io import BytesIO


class Reply:
    def __init__(self, status=200, body=b'', headers=(("Content-Type","application/json"),)):
        self.status, self.headers = status, headers
        self.stream = BytesIO(body)
        self.read_requests = []
        self.closed = False

    def read(self, size):
        self.read_requests.append(size)
        return self.stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.stream.close()
        self.closed = True


class FakeTransport:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def get(self, target, *, timeout, max_bytes):
        self.calls.append((target,timeout,max_bytes))
        if isinstance(self.result, Exception):
            raise self.result
        return self.result
