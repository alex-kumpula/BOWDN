import shlex
from .command import Command
from .flag import Flag
from .command_context import CommandContext, FlagValue
from .exceptions import CommandNotRecognizedException

class CommandCatalogue:
    def __init__(self, commands_dict: dict):
        self.commands_dict = commands_dict
        self.commands = self.get_commands_from_dict(self.commands_dict)
    
    
    def get_commands_from_dict(self, input_dict):
        """
        Parses a user-defined dict of a certain structure into a CommandsDefinition class.
        """
        commands = {}
        for command_name, command in input_dict.items():
            commands[command_name] = Command(
                name         = command_name, 
                aliases      = command.get("aliases", []),
                description  = command.get("description", ""),
                function     = command.get("function", None),
                flags        = self.get_flags_from_dict(command.get("flags", {})),
                sub_commands = self.get_commands_from_dict(command.get("sub_commands", {})),
                meta_data    = command.get("meta_data", {})
            )
        return commands
    
    
    def get_flags_from_dict(self, input_dict_flags):
        """
        Parses a user-defined dict of flags into a list of Flags.
        """
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


    def tokenize_string(self, string: str):
        """
        Takes a string and turns it into a list of tokens delimited by whitespace, 
        accounting for substrings.
        """
        string = string.strip()
        # shlex.split preserves substrings when it splits
        tokens = shlex.split(string)
        return tokens

    
    def get_command(self, token):
        if token in self.commands.keys():
            return self.commands[token]
        else:
            for command in self.commands.values():
                if token in command.aliases:
                    return command
        return None

    def classify_tokens(self, message: str):
        """
        Takes an input string or "message" and returns two lists:
        -   A list of token types (token_types): ie. Command, Sub Command, Flag, Argument
        -   A list of token objects (token_objects): ie. Command (class), 
            Flags (just long name) and their values, and Arguments
        """

        tokens = self.tokenize_string(message)
        token_types = []
        token_objects = []

        last_command = None
        for token in tokens:
            if "Command" not in token_types:
                command = self.get_command(token)
                if command is not None:
                    token_types.append("Command")
                    token_objects.append(command)
                    last_command = command
                    continue
                else:
                    raise CommandNotRecognizedException
            
            token_type_last = token_types[-1]
            token_object_last = token_objects[-1]

            if token_type_last in ["Command", "Sub Command"]:
                sub_command = token_object_last.get_sub_command(token)
                if sub_command is not None:
                    token_types.append("Sub Command")
                    token_objects.append(sub_command)
                    last_command = sub_command
                    continue
            
            if token_type_last in ["Command", "Sub Command", "Flag"]:
                flag = last_command.get_flag(token)
                if flag is not None:
                    token_types.append("Flag")
                    token_objects.append(flag)
                    continue
            
            token_types.append("Argument")
            token_objects.append(token)
            continue
        
        return (tuple(token_types), tuple(token_objects))

    def parse(self, message: str, default = None, *args, **kwargs):
        """
        Takes in a string or "message" and runs the command it indicates,
        with the flags and positional arguments being passed through.
        Also accepts *args and **kwargs and passes it through to the command's 
        function being run.
        """
        token_types, token_objects = self.classify_tokens(message)
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
                flag_value_pair = token_objects[k]
                flag_name = flag_value_pair.flag.long_name
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