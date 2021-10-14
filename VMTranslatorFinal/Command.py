class Command:
    def __init__(self, cmnd):
        self.cmnd = cmnd

    def report_data(self):
        data = vars(self)
        return data