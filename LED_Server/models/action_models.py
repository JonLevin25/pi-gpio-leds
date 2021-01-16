import logging
from typing import List


class ActionRequestParam:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    @classmethod
    def fromDecodedJson(cls, obj) -> 'ActionRequestParam':
        return ActionRequestParam(obj['name'], obj['value'])


class ActionRequest:
    def __init__(self, name, params: List[ActionRequestParam]):
        self.name = name
        self.params = params

    @classmethod
    def fromDecodedJson(cls, obj) -> 'ActionRequest':
        name = obj['name']
        params_obj = obj['params']

        if not name or not params_obj:
            logging.error('missing root objects on action request')
            return None

        params = list(map(ActionRequestParam.fromDecodedJson, params_obj))
        return ActionRequest(name, params)