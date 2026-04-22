from typing import Callable, Collection


class BaseNode():
    def __init__(self):
        super().__init__()

    def __call__(self, data):
        return self.forward(data)

    def forward(self, data):
        raise NotImplementedError()


class FuncNode(BaseNode):
    def __init__(
            self,
            func: Callable,
    ):
        super().__init__()
        self.func = func

    def data_norm(self, data):
        if isinstance(data, Collection):
            return {str(i): item for i, item in enumerate(data)}
        else:
            return {'0': data}

    def forward(self, data):
        data = self.data_norm(data)
        data = self.func(*data.values())
        return data
