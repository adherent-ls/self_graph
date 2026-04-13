class BaseInstance(object):
    pass


class Condition(BaseInstance):
    def __init__(self, cond):
        super().__init__()
        self.cond = cond

    def __call__(self):
        return self.cond
