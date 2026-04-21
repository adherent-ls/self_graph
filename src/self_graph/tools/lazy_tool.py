import inspect


class LazyCall():
    def __init__(self, func):
        super().__init__()
        # WARNING set会直接触发__setattr__，不能直接使用self.func=func进行赋值
        self.__dict__['func'] = func
        self.__dict__['sig'] = inspect.signature(func)
        # get会首先触发__getattribute__,失败后触发__getattr__，所以可以用self.sig的方式取
        self.__dict__['bound'] = self.sig.bind_partial()

    def __getattr__(self, name):
        return self.bound.arguments[name]

    def __setattr__(self, name, value):
        self.bound.arguments[name] = value

    def __call__(self, *args, **kwargs):
        bound = self.sig.bind_partial(*args, **kwargs)
        self.bound.arguments.update(bound.arguments)
        return self

    def build(self):
        return self.func(*self.bound.args, **self.bound.kwargs)
