import logging
from functools import reduce
from typing import List, Tuple, Dict, Callable, Mapping

import inspect

# returns (Generic wrapper type [null if ],
def get_generic_type_info(t: type) -> (type, Tuple[type]):
    if not hasattr(t, '__origin__'):
        return (None, t)
    return t.__origin__, t.__args__

def populate(init: Callable[[...], any], dict: Mapping[str, any]):
    def get_param_type(param: inspect.Parameter):
        param_type = param.annotation

        generic_type, generic_args = get_generic_type_info(param_type)
        if generic_type == list:
            return generic_args[0]
        return param_type

    def get_value(param_name, param: inspect.Paramater, dict):
        dict_value = dict[param_name]
        param_type = get_param_type(param)

        if param_type and hasattr(param_type, 'populate'):
            return param_type.populate(dict_value)
        return dict_value

    # go over init params, keep the ones that are in the dict passed in.
    # if param type has a 'populate' method - use it
    params = inspect.signature(init).parameters
    result_params = {}
    for param_name, param in params.items():
        if not param_name in dict:
            continue

        param_type = param.annotation
        result_params[param_name] = get_value(param_name, param_type, dict)

    return init(**result_params)


class ActionRequestParam:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    @classmethod
    def populate(cls, obj) -> 'ActionRequestParam':
        # TODO: Use populate
        # return populate(cls.__init__)
        return ActionRequestParam(obj['name'], obj['value'], obj['default_value'])


class ActionRequest:
    def __init__(self, name, params: List[ActionRequestParam]):
        self.name = name
        self.params = params

    @classmethod
    def populate(cls, obj) -> 'ActionRequest':
        name = obj['name']
        params_obj = obj['params']

        if not name or not params_obj:
            logging.error('missing root objects on action request')
            return None

        params = list(map(ActionRequestParam.populate, params_obj))
        return ActionRequest(name, params)
