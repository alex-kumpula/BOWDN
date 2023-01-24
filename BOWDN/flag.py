"""
The Flag class defines all the components of a flag.
Each Command can have any number of Flags.
"""
class Flag:
    def __init__(self, 
            long_name: str, 
            long_aliases: list    = None, 
            short_name: str       = None, 
            short_aliases: list   = None, 
            accepts_input         = False,
            default_value_present = None,
            default_value_absent  = None
        ):
        self.long_name     = long_name
        self.long_aliases  = long_aliases
        self.short_name    = short_name
        self.short_aliases = short_aliases
        self.accepts_input = accepts_input
        self.default_value_present = default_value_present
        self.default_value_absent  = default_value_absent
    
    def __repr__(self):
        return self.long_name


class FlagValue:
    def __init__(self,
        flag,
        value
    ):
        self.flag = flag
        self.value = value

    def __repr__(self):
        return f"Flag: {self.flag}, Value: {self.value}"