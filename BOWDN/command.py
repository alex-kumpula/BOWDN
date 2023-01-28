"""
The Command class defines all the components of a command.
"""
class Command:
    def __init__(self, 
        name: str, 
        aliases: list = None, 
        description: str = None, 
        function = None, 
        flags: dict = None, 
        sub_commands: dict = None, 
        meta_data: dict = None
    ):
        self.name         = name
        self.aliases      = aliases
        self.description  = description
        self.function     = function if function is not None else lambda: print(f"Command {self.name} was ran but does not yet have a function implemented.")
        self.flags        = flags
        self.sub_commands = sub_commands
        self.meta_data    = meta_data

    """
    Tries to run the self.function associated with the command.
    Takes in any amount of *args and **kwargs as input.
    If there is an exception, print the error to the console and continue.
    """
    def run(self, *args, **kwargs):
        try:
            return self.function(*args, **kwargs)
        except Exception as e:
            print(f"Something went wrong: {e}")
            return None