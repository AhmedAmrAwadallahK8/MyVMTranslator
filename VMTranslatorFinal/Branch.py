import CommandArgument


class Branch(CommandArgument.CommandArgument):
    def __init__(self, label):
        super().__init__()
        self.label = label
