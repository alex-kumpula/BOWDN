from .exceptions import raise_exception, CommandFunctionNotAssignedException

class Command:
    """
    The Command class defines all the components of a command.
    """ 
    def __init__(self, 
        name: str, 
        aliases: list = [], 
        description: str = None, 
        function = None, 
        flags: dict = {}, 
        sub_commands: dict = {}, 
        meta_data: dict = {}
    ):
        self.name         = name
        self.aliases      = aliases
        self.description  = description
        self.function     = function if function is not None else lambda *args, context = None, **kwargs: raise_exception(CommandFunctionNotAssignedException(f"Command {self.name} was ran but does not yet have a function implemented."))
        self.flags        = flags
        self.sub_commands = sub_commands
        self.meta_data    = meta_data

    def run(self, *args, **kwargs):
        """
        Tries to run the self.function associated with the command.
        Takes in any amount of *args and **kwargs as input.
        If there is an exception, reraise it.
        """
        try:
            return self.function(*args, **kwargs)
        except Exception as e:
            raise e
            return None

