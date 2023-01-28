from BOWDN import CommandCatalogue

def command_function_to_run_1(argument_token_1, *args, **kwargs):
    context = kwargs['context']
    flags = context.flags
    command = context.command
    if flags['help'].value:
        print(command.description)
    example_response  = f"This function can return anything, not just strings."
    example_response += f"\nHere is some extra meta-data about the command: {command.meta_data['example_meta_data_key']}"
    example_response += f"\nPositional argument 1: {argument_token_1}"
    example_response += f"\nPositional argument 2: {args[0]}"
    example_response += f"\nFlags: {flags}"
    example_response += f"\nExtra Kwarg: {kwargs['kwarg_demo']}"
    example_response += f"\nThe inputted message: {context.message_raw}"
    example_response += f"\nInput message tokens: {context.tokens}"
    example_response += f"\nInput message token types: {context.token_types}"
    return example_response

def command_function_to_run_2(argument_token_1, argument_token_2, **kwargs):
    print("Test response 2! - Argument 1: " + argument_token_1)
    print(f"Argument 2: {argument_token_2}")
    print(kwargs['flags'])
    response = {
        "content": "This is the content :> (2)"
    }
    return response

command_dict = {
    "command_1": {
        "aliases": [
            "alias_1",
            "alias_2",
            "alias_3"
        ],
        "description": "This is the description of the command. It can be used for many things like --help flags.",
        "meta_data": {
            "example_meta_data_key": "You can specify extra info about a command here!"
        },
        "flags": {
            "help": {
                "short_name": "h",
                "short_aliases": [
                    "i"
                ],
                "long_aliases": [
                    "info"
                ],
                "accepts_input": False,
                "default_value_present": True,
                "default_value_absent": False
            },
            "extra_message": {
                "short_name": "em",
                "short_aliases": [
                    "am"
                ],
                "long_aliases": [
                    "additional_message"
                ],
                "accepts_input": True,
                "default_value_present": "Default value of this flag that is passed to the function if the flag is present",
                "default_value_absent": "Default value of this flag that is passed to the function if the flag is absent"
            },
            "example_flag_1": {
                "short_name": "ef1",
                "accepts_input": True,
                "default_value_present": "Default value of this flag that is passed to the function if the flag is present",
                "default_value_absent": "Default value of this flag that is passed to the function if the flag is absent"
            },
            "example_flag_2": {
                "short_name": "ef2",
                "accepts_input": True,
                "default_value_present": "Default value of this flag that is passed to the function if the flag is present",
                "default_value_absent": "Default value of this flag that is passed to the function if the flag is absent"
            }
        },
        "function": command_function_to_run_1,
        "sub_commands": {
            "sub_command_1": {
                "aliases": [
                    "sub_command_1_alias_1",
                    "sub_command_2_alias_2",
                    "sub_command_3_alias_3"
                ],
                "description": "This is a sub command. It will be run if the user inputs its parent command followed by this command.",
                "flags": {
                    "help": {
                        "short_name": "h",
                        "short_aliases": [
                            "i"
                        ],
                        "long_aliases": [
                            "info"
                        ],
                        "accepts_input": False,
                        "default_value_present": True,
                        "default_value_absent": False
                    }
                },
                "function": command_function_to_run_2
            }
        }
    }
}

commands = CommandCatalogue(command_dict)

print(commands.parse('command_1 -h --example_flag_2 -am="This flag gives it an extra message." This_is_argument_1 "This is argument 2"', kwarg_demo="This is an extra kwarg you can pass through. This can be anything of any type."))


# (commands.parse('test'))