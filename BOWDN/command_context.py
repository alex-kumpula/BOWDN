class CommandContext:
    """
    The CommandContext class bundles useful information about the execution of a command.
    """
    def __init__(self,
        command,
        flags       = {},
        tokens      = (),
        token_types = (),
        message_raw = None
    ):
        self.command     = command
        self.flags       = flags
        self.tokens      = tokens
        self.token_types = token_types
        self.message_raw = message_raw


class FlagValue:
    def __init__(self,
        flag,
        value
    ):
        self.flag = flag
        self.value = value

    def __repr__(self):
        return f"Flag: {self.flag}, Value: {self.value}"