import CommandArgument

class Memory(CommandArgument.CommandArgument):
    def __init__(self, mem, loc):
        super().__init__()
        self.mem = mem
        self.loc = loc