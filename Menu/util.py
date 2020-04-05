import copy
import operator
from functools import reduce
from typing import Dict


class CopyOnFetchDict(Dict):
    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return copy.deepcopy(val)

    def set_by_path(self, keys, f):
        try:
            reduce(operator.getitem, keys + [f], self)
        except KeyError:

            def nested_set(d, keys):
                for key in keys:
                    d = d.setdefault(key, dict())
                reduce(lambda o, k: dict.__getitem__(o, k), keys, self)[f.title] = f

            nested_set(self, keys)

    def get_item_by_title(self, title):

        # Adapted form https://stackoverflow.com/a/31439438
        def nested_dict_values(d):
            for v in d.values():
                if isinstance(v, dict):
                    yield from nested_dict_values(v)
                else:
                    yield v

        return next(filter(lambda i: i.title == title, nested_dict_values(self.copy())), None)
