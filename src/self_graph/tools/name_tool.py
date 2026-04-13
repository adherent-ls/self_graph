from typing import Union, Dict, Tuple, List

from self_graph.base_instance import BaseInstance
from self_graph.local_types.base_param_type import Value


class NameConvert(BaseInstance):
    @staticmethod
    def dict_to_list(data: Dict, names: Union[Tuple, List, str] = None):
        if names is None:
            results = list(data.values())
        elif isinstance(names, str):
            results = data[names]
        elif isinstance(names, Value):
            results = names.value
        elif isinstance(names, List) or isinstance(names, Tuple):
            results = []
            for i, name in enumerate(names):
                results.append(NameConvert.dict_to_list(data, name))
        else:
            raise NotImplemented
        return results

    @staticmethod
    def list_to_dict(data: Union[Tuple, List], names: Union[Tuple, List, str]):
        result = {}
        if isinstance(names, str):
            result[names] = data
        elif isinstance(names, List) or isinstance(names, Tuple):
            for i, name in enumerate(names):
                item_result = NameConvert.list_to_dict(data[i], name)
                result.update(item_result)
        else:
            raise NotImplemented
        return result
