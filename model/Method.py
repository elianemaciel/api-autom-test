from enum import Enum


class ParamType(Enum):
    STRING = 1
    INTEGER = 2
    BOOLEAN = 3
    FLOAT = 4


class Param:
    def __init__(self, name, param_type):
        self.name = name
        self.type = param_type


class Method:
    def __init__(self, name, return_type, params, package_name=None):
        self.name = name
        self.return_type = return_type
        self.params = params
        self.package_name = package_name
