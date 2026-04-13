from typing import List, Union, Any

from base_graph import BaseGraph
from local_types.base_param_type import Value

graph_types = Union[BaseGraph, Any]

input_types = List[Union[str, Value]]

output_types = Union[str, List[str]]
