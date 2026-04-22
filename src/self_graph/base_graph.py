from collections import deque
from typing import List, Generic, TypeVar

from self_graph.base_node import BaseNode, FuncNode

T = TypeVar("T", bound=BaseNode)


class BaseGraph(Generic[T]):
    def __init__(self):
        super().__init__()
        self.nodes: List[T] = []
        self.queue = deque()

    def add(self, node: T):
        self.nodes.append(node)
        return True

    def __call__(self, *data: List):
        return self.forward(*data)

    def forward(self, *data: List):
        self.queue.extend(self.nodes)
        while self.queue:
            node = self.queue.popleft()
            data = node(data)
        return data


class SeriesListGraph(BaseGraph[FuncNode]):
    def __init__(self, funcs: List):
        super().__init__()

        for func in funcs:
            self.add(FuncNode(func))


def main():
    def add(a, b):
        return a + b

    def x10(data):
        return data * 10, 10

    g = SeriesListGraph([
        add, x10, add
    ])
    c = g(5, 8)
    print(c)


if __name__ == '__main__':
    main()
