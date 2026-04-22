from collections import deque
from typing import List, Tuple, Generic, TypeVar, Dict

from self_graph.base_graph import BaseGraph
from self_graph.local_types.name_param_types import input_types, output_types, graph_types
from self_graph.nodes.dict_node import NameWithMemoryNode, NameNode
from self_graph.tools.name_tool import NameConvert

D = TypeVar("D", bound=NameNode)


class DictGraph(BaseGraph[D]):
    def __init__(self):
        super().__init__()
        self.nodes: List[D] = []
        self.queue = deque()

    def add(self, node: D):
        self.nodes.append(node)
        return True

    def check(self, data, names):
        for name in names:
            if name not in data:
                return False
        return True

    def __call__(self, data: Dict):
        return self.forward(data)

    def forward(self, data: Dict):
        self.queue.extend(self.nodes)
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

    def __call__(self, *data: List):
        data_dict = NameConvert.list_to_dict(data, self.ini)
        data_dict = super().forward(data_dict)
        result = NameConvert.dict_to_list(data_dict, self.oui)
        return result


def main():
    def add(a, b):
        return a + b

    def x10(data):
        return data * 10, 10

    g = SeriesWithNameGraph(
        [
            (add, ['a', 'b'], 'c'),
            (x10, ['c'], ['c', 'd']),
            (add, ['c', 'd'], 'd')
        ],
        ['a', 'b'],
        'd'
    )
    c = g(5, 10)
    print(c)

    g1 = DictGraph[NameNode]()
    g1.add(NameNode(add, ['a', 'b'], 'a'))
    c1 = g1({'a': 10, 'b': 20})
    print(c1)


if __name__ == '__main__':
    main()
