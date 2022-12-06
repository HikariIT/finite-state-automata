class TransitionFunctionError(Exception):

    def __init__(self, message):
        super().__init__(message)


class InvalidStateError(Exception):

    def __init__(self, message):
        super().__init__(message)


class InvalidSymbolError(Exception):

    def __init__(self, message):
        super().__init__(message)