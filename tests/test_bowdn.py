from BOWDN import CommandCatalogue
from testing_command_dict import *




def test_create_catalogue():
    commands_1 = CommandCatalogue(command_dict_1)

    print(commands_1.commands)

    pass

# test_create_catalogue()






commands_1 = CommandCatalogue(command_dict_1)


message = 'command_1 -h --example_flag_2 -am="This flag gives it an extra message." This_is_argument_1 "This is argument 2"'
# print(commands_1.classify_tokens(message)[1][1].value)

print(commands_1.parse(message, kwarg_demo="This is an extra kwarg you can pass through. This can be anything of any type."))


# (commands.parse('test'))