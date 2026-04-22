from typing import Union, Callable

from self_graph.base_node import BaseNode


class ConditionNode(BaseNode):
    def __init__(self, cond: Union[Callable, bool], func_true: Callable, func_false: Callable):
        super().__init__()
        self.cond = cond
        self.func_true = func_true
        self.func_false = func_false

    def forward(self, *data):
        cond = self.cond() if callable(self.cond) else self.cond
        if cond:
            return self.func_true(*data)
        else:
            return self.func_false(*data)