from .exceptions import raise_exception, CommandFunctionNotAssignedException
from .command_context import FlagValue

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

    def get_sub_command(self, token):
        if token in self.sub_commands.keys():
            return self.sub_commands[token]
        else:
            for sub_command in self.sub_commands.values():
                if token in sub_command.aliases:
                    return sub_command
        return None
    
    def get_flag(self, token):
        long_flag = False
        input_flag = None
        if len(token) >= 3 and token[0:2] == "--":
            long_flag = True
            input_flag = token[2:]
        elif len(token) >= 2 and token[0] == "-":
            long_flag = False
            input_flag = token[1:]
        else:
            return None

        flag_name = input_flag
        flag_value = None
        if "=" in input_flag:
            flag_end_index = token.find("=")
            if len(token) - 1 > flag_end_index:
                flag_name = input_flag[:flag_end_index - 1]
                flag_value = input_flag[flag_end_index:]
        
        for flag in self.flags:
            if (long_flag and (flag_name == flag.long_name or flag_name in flag.long_aliases)) or (flag_name == flag.short_name or flag_name in flag.short_aliases):
                if not flag.accepts_input or flag_value is None:
                    flag_value = flag.default_value_present
                token_object = FlagValue(flag, flag_value)
                return token_object


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

