import shlex
from .command import Command
from .flag import Flag
from .command_context import CommandContext, FlagValue
from .exceptions import CommandNotRecognizedException

class CommandCatalogue:
    def __init__(self, commands_dict: dict):
        self.commands_dict = commands_dict
        self.commands = self.get_commands_from_dict(self.commands_dict)
    
    """
    Parses a user-defined dict of a certain structure into a CommandsDefinition class.
    """
    def get_commands_from_dict(self, input_dict):
        commands = []
        for command_name, command in input_dict.items():
            commands.append(Command(
                name         = command_name, 
                aliases      = command.get("aliases", []),
                description  = command.get("description", ""),
                function     = command.get("function", None),
                flags        = self.get_flags_from_dict(command.get("flags", {})),
                sub_commands = self.get_commands_from_dict(command.get("sub_commands", {})),
                meta_data    = command.get("meta_data", {})
            ))
        return commands
    
    """
    Parses a user-defined dict of flags into a list of Flags.
    """
    def get_flags_from_dict(self, input_dict_flags):
        flags = []
        for flag_name, flag in input_dict_flags.items():
            flags.append(Flag(
                long_name     = flag_name,
                long_aliases  = flag.get("long_aliases", []),
                short_name    = flag.get("short_name", None),
                short_aliases = flag.get("short_aliases", []),
                accepts_input = flag.get("accepts_input", False),
                default_value_present = flag.get("default_value_present", None),
                default_value_absent  = flag.get("default_value_absent", None)
            ))
        return flags

    """
    Takes a string and turns it into a list of tokens delimited by whitespace, 
    accounting for substrings.
    """
    def tokenize_string(self, string: str):
        string = string.strip()
        # shlex.split preserves substrings when it splits
        tokens = shlex.split(string)
        return tokens

    """
    Takes an input string or "message" and returns two lists:
    -   A list of token types (token_types): ie. Command, Sub Command, Flag, Argument
    -   A list of token objects (token_objects): ie. Command (class), 
        Flags (just long name) and their values, and Arguments
    """
    def read_tokens(self, message: str):
        tokens = self.tokenize_string(message)
        token_types = []
        token_objects = []

        i = 0
        recognized_command = False
        while i < len(self.commands) and not recognized_command:
            command = self.commands[i]
            token_types = []
            token_objects = []
            for j in range(len(tokens)):
                token = tokens[j]
                # Find base command
                if j == 0:
                    if (token == command.name or token in command.aliases):
                        token_types.append("Command")
                        token_objects.append(command)
                        recognized_command = True
                # Everything else
                if j >= 1 and recognized_command:
                    # Find sub command(s)
                    for sub_command in command.sub_commands:
                        if token == sub_command.name or token in sub_command.aliases:
                            token_types.append("Sub Command")
                            token_objects.append(sub_command)
                    # Find flag(s)
                    for flag in command.flags:
                        flag_value = None
                        flag_end_index = len(token)
                        if "=" in token:
                            flag_end_index = token.find("=")
                            if len(token) - 1 > flag_end_index:
                                flag_value = token[flag_end_index + 1:]
                        # Long flags
                        if len(token) >= 3 and token[0:2] == "--":
                            input_flag = token[2:flag_end_index]
                            if input_flag == flag.long_name or input_flag in flag.long_aliases:
                                token_types.append("Flag")
                                if not flag.accepts_input or flag_value is None:
                                    flag_value = flag.default_value_present
                                token_objects.append((flag.long_name, FlagValue(flag, flag_value)))
                        # Short flags
                        elif len(token) >= 2 and token[0] == "-":
                            input_flag = token[1:flag_end_index]
                            if input_flag == flag.short_name or input_flag in flag.short_aliases:
                                token_types.append("Flag")
                                if not flag.accepts_input or flag_value is None:
                                    flag_value = flag.default_value_present
                                token_objects.append((flag.long_name, FlagValue(flag, flag_value)))
                    # If none of the above has been found, assume the token is an argument
                    if len(token_types) - 1 < j:
                        token_types.append("Argument")
                        token_objects.append(token)
            i += 1
        return (tuple(token_types), tuple(token_objects))
    
    """
    Takes in a string or "message" and runs the command it indicates,
    with the flags and positional arguments being passed through.
    Also accepts *args and **kwargs and passes it through to the command's 
    function being run.
    """
    def parse(self, message: str, default = None, *args, **kwargs):
        token_types, token_objects = self.read_tokens(message)
        run_command = None
        arguments = []
        flags = {}

        # Find last occurence of a command or sub command in the message
        if "Command" in token_types:
            i = max((index for index, val in enumerate(token_types) if (val == "Command" or val == "Sub Command")), default=None)
            run_command = token_objects[i]
        # If there is no command found, return a default value
        else:
            return default

        # Populate the flags dict with the default values if the flags are absent
        for flag in run_command.flags:
            flags[flag.long_name] = flag.default_value_absent

        # Populate the flags dict with their values (default or inputted) if they are present
        for k in range(len(token_types)):
            if token_types[k] == "Flag":
                flag_name, flag_value_pair = token_objects[k]
                flags[flag_name] = flag_value_pair

        # The rest of the tokens are assumed to be argumments
        if "Argument" in token_types:
            j = token_types.index("Argument")
            arguments = token_objects[j:]
        
        # Creates a CommandContext that will be passed to the command's function for it to consume
        context = CommandContext(
            run_command,
            flags = flags,
            tokens = token_objects,
            token_types = token_types,
            message_raw = message
        )

        if run_command is not None:
            return run_command.run(*args, *arguments, context = context, **kwargs)
        else:
            raise CommandNotRecognizedException