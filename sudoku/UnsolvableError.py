class MyError(Exception):
    pass

class UnsolvableBoardError(MyError):
    def __init__(self, message):
        self.message = message

