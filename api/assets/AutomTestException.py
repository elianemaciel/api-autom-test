class AutomTestException(Exception):

    def __init__(self, exception=None, message=""):
        self.original_exception = exception
        self.message = message

