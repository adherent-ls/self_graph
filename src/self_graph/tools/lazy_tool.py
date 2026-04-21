from self_graph.graph.name_graph import NameGraph


class LazyCall():
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.args = None
        self.kwargs = None

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def build(self):
        if self.args is not None:
            self.args = [arg.build() if isinstance(arg, LazyCall) else arg for arg in self.args]
        if self.kwargs is not None:
            self.kwargs = {k: v.build() if isinstance(v, LazyCall) else v for k, v in self.kwargs.items()}

        if self.args is None and self.kwargs is None:
            return self.func()
        elif self.args is not None and self.kwargs is None:
            return self.func(*self.args)
        elif self.args is None and self.kwargs is not None:
            return self.func(**self.kwargs)
        else:
            return self.func(*self.args, **self.kwargs)
