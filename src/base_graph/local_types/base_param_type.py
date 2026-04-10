from enum import Enum


class Value(object):
    def __init__(self, value):
        super().__init__()
        self.value = value


V = Value
