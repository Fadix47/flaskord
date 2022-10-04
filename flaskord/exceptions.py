class HttpException(Exception):
    pass

class UndefinedToken(Exception):
    pass

class RateLimited(HttpException):
    def __init__(self, json, headers):
        self.json = json
        self.headers = headers
        self.message = self.json["message"]
        self.retry_after = self.json["retry_after"]
        super().__init__(self.message)

class Unauthorized(HttpException):
    pass

class AccessDenied(HttpException):
    pass
