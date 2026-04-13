from typing import List, Tuple

from base_graph import FuncGraph, SeriesListGraph
from tools.name_tool import NameConvert
from local_types.name_param_types import input_types, output_types, graph_types


class NameGraph(FuncGraph):
    def __init__(
            self,
            func: graph_types,
            ini: input_types,
            oui: output_types,
    ):
        super().__init__(func)
        self.ini = ini
        self.oui = oui

    def forward(self, data):
        input_data = NameConvert.dict_to_list(data, self.ini)
        func_data = super().forward(*input_data)
        output_data = NameConvert.list_to_dict(func_data, self.oui)
        return output_data


class NameUpdateGraph(NameGraph):
    def __init__(
            self,
            func: graph_types,
            ini: input_types,
            oui: output_types,
    ):
        super().__init__(func, ini, oui)

    def forward(self, data):
        func_data = super().forward(data)
        data.update(func_data)
        return data


class SeriesWithNameGraph(SeriesListGraph):
    def __init__(
            self,
            funcs: List[Tuple[graph_types, input_types, output_types]],
            ini: input_types,
            oui: output_types = None,
    ):
        super().__init__(self.build_children(funcs))
        self.ini = ini
        self.oui = oui

    def build_children(self, funcs):
        modules = []
        for idx, item in enumerate(funcs):
            func, ini, oui = item[:3]
            modules.append(NameUpdateGraph(func, ini, oui))
        return modules

    def forward(self, *data: List):
        data_dict = NameConvert.list_to_dict(data, self.ini)
        data_dict = super().forward(data_dict)
        result = NameConvert.dict_to_list(data_dict, self.oui)
        return result
