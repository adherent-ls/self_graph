from collections import deque
from typing import List, Tuple, Generic, TypeVar, Dict

from self_graph.local_types.name_param_types import input_types, output_types, graph_types
from self_graph.nodes.dict_node import NameWithMemoryNode, NameNode
from self_graph.tools.name_tool import NameConvert

D = TypeVar("D", bound=NameNode)


class DictGraph(Generic[D]):
    def __init__(self):
        super().__init__()
        self.nodes: List[D] = []
        self.queue = deque()

    def add(self, node: D):
        self.nodes.append(node)
        self.queue.append(node)
        return True

    def check(self, data, names):
        for name in names:
            if name not in data:
                return False
        return True

    def __call__(self, data: Dict):
        return self.forward(data)

    def forward(self, data: Dict):
        while self.queue:
            node = self.queue.popleft()
            # 依赖未满足 → 跳过（重新排队）
            if not self.check(data, node.ini):
                self.queue.append(node)
                continue
            # 执行
            data = node(data)
        return data


class SeriesWithNameGraph(DictGraph[NameWithMemoryNode]):
    def __init__(
            self,
            funcs: List[Tuple[graph_types, input_types, output_types]],
            ini: input_types,
            oui: output_types = None,
    ):
        super().__init__()
        self.ini = ini
        self.oui = oui
        for item in funcs:
            func, ini, oui = item
            self.add(NameWithMemoryNode(func, ini, oui))

    def forward(self, *data: List):
        data_dict = NameConvert.list_to_dict(data, self.ini)
        data_dict = super().forward(data_dict)
        result = NameConvert.dict_to_list(data_dict, self.oui)
        return result
