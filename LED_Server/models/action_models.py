import logging
from typing import List


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
