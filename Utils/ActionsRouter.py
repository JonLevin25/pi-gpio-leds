import inspect
import logging
import functools
from collections import OrderedDict
from typing import List, Mapping, Callable

from Utils.reflection_builder import InvalidParamErrorMode, ParamsMetadata, \
    validate_params, build_params_metadata

ActionsMetadata = Mapping[str, ParamsMetadata]


class ActionsRouter:
    """
    Handles parsing strings and mapping to actions.
    Holds a dictionary of string keys -> func(string-> void) values
    """

    def __init__(self, actions: Mapping[str, Callable], supported_types: List[type], closure_params: Mapping[str, any]):
        self.supported_types = supported_types
        self.closure_params = closure_params or {}
        self.omitted_params = list(closure_params.keys())

        for key in actions:
            fn_value = actions[key]
            if not callable(fn_value):
                raise TypeError("ActionsRouter expects {str: function} values! ")

        self.actions = actions

        assert self.actions
        assert self.supported_types is not None

    # def _parse(self, message):
    #     match = re.match('(.*?):(.*)$', message)
    #     if not match:
    #         print('Bad scheme!')
    #         return None, None
    #
    #     payload: str
    #     key, payload = match.groups()
    #     params = payload.split(',')
    #
    #     print('key: {}, params ({}): {}'.format(key, len(params), params))
    #
    #     return key, params
    #
    # def handle(self, message):
    #     (key, params) = self._parse(message)
    #     if key in self.actions:
    #         fn_handler = self.actions[key]
    #         self.do_action(fn_handler, params)

    def handle(self, action_request: 'ActionRequest'):
        assert action_request.name
        assert action_request.params

        action = self.actions[action_request.name]

        assert action
        self._apply(action, action_request.params)

    def get_metadata(self,
                     on_invalid_params: InvalidParamErrorMode = InvalidParamErrorMode.OMIT_ACTION) -> ActionsMetadata:

        result = OrderedDict()
        for actionName, action in self.actions.items():
            sig = inspect.signature(action)
            params = sig.parameters

            if not validate_params(on_invalid_params, actionName, params.values(), self.supported_types, self.omitted_params):
                continue

            params_metadata = build_params_metadata(params, self.omitted_params)
            result[actionName] = params_metadata

        return result

    def _apply(self, fn: Callable[[any], None], params: List['ActionRequestParam']):
        inspected_params = inspect.signature(fn).parameters
        parsed_params = self._parse_param_dict(fn, inspected_params, params)

        closure_params = {k:v for k,v in self.closure_params.items() if k in inspected_params.keys()}
        return fn(**closure_params, **parsed_params)

    def _parse_param_dict(self, fn, inspected_params, params) -> Mapping[str, any]:
        parsed_args = {}
        for request_param in params:
            param_name = request_param.name
            if not param_name in inspected_params.keys():
                logging.warning(
                    f'Request had param ({param_name}) that isn\'t in function ({fn.__name__})! Will be ignored')
                continue

            request_type = inspected_params[param_name].annotation
            assert request_type != inspect.Parameter.empty  # shouldnt be unannotated, and if it is shouldnt exposed to client

            parsed_param_value = request_type(request_param.value)
            parsed_args[param_name] = parsed_param_value

        return parsed_args


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
