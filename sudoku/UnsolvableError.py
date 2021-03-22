class MyError(Exception):
    pass

class UnsolvableError(MyError):
    def __init__(self, meassage):
        self.message = message

