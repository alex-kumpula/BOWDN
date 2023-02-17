def raise_exception(exception):
    raise exception

class CommandFunctionNotAssignedException(Exception):
    """
    Raised when the command being run does not have
    a function assigned to it.
    """
    pass

class CommandNotRecognizedException(Exception):
    """
    Raised when the command inputed by the user is not a command
    in the CommandCatalogue.
    """
    pass