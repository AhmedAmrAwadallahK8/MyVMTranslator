import CommandArgument


class Function(CommandArgument.CommandArgument):
    def __init__(self, name, n_vars):
        super().__init__()
        self.name = name
        self.n_vars = n_vars