class BojError(BaseException):
    def __init__(self, msg):
        super().__init__(msg)

class FileIOError(BojError):
    def __init__(self, msg):
        super().__init__(msg)
