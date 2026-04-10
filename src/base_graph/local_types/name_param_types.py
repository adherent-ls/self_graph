from typing import List, Union, Any

from src.base_graph.base_graph import BaseGraph
from src.base_graph.local_types.base_param_type import Value

graph_types = Union[BaseGraph, Any]

input_types = List[Union[str, Value]]

output_types = Union[str, List[str]]
