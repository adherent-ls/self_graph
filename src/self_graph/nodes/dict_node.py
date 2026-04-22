from typing import Callable

from self_graph.base_node import BaseNode
from self_graph.tools.name_tool import NameConvert


class NameNode(BaseNode):
    def __init__(
            self,
            func: Callable,
            ini,
            oui,
    ):
        super().__init__()
        self.func = func
        self.ini = ini
        self.oui = oui

    def forward(self, data):
        input_data = NameConvert.dict_to_list(data, self.ini)
        func_data = self.func(*input_data)
        output_data = NameConvert.list_to_dict(func_data, self.oui)
        return output_data


class NameWithMemoryNode(NameNode):
    def __init__(
            self,
            func: Callable,
            ini,
            oui,
    ):
        super().__init__(func, ini, oui)

    def forward(self, data):
        output_data = super().forward(data)
        data.update(output_data)
        return data
