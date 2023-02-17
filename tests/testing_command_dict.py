from testing_commands import *

command_dict_1 = {
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