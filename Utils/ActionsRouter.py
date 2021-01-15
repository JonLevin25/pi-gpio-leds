import inspect
import re
from collections import OrderedDict
from typing import List, Mapping

from Utils.reflection_builder import InvalidParamErrorMode, ParamsMetadata, \
    validate_params, build_params_metadata

ActionsMetadata = Mapping[str, ParamsMetadata]
class ActionsRouter:
    """
    Handles parsing strings and mapping to actions.
    Holds a dictionary of string keys -> func(string-> void) values
    Expects a "scheme" (regex pattern with 2 capture groups - the first being the key and the second
    is a payload string that will be passed to the func
    """

    def __init__(self, scheme='(.*?):(.*)$', actions={}):
        self.scheme = scheme
        for key in actions:
            fn_value = actions[key]
            if not callable(fn_value):
                raise TypeError("ActionsRouter expects {str: function} values! ")
        self.actions = actions

    def _parse(self, message):
        match = re.match('(.*?):(.*)$', message)
        if not match:
            print('Bad scheme!')
            return None, None

        payload: str
        key, payload = match.groups()
        params = payload.split(',')

        print('key: {}, params ({}): {}'.format(key, len(params), params))

        return key, params

    def handle(self, message):
        (key, params) = self._parse(message)
        if key in self.actions:
            fn_handler = self.actions[key]
            self.do_action(fn_handler, params)

    def get_metadata(self, supported_types: List[type], omitted_types: List[type] = None,
                     on_invalid_params: InvalidParamErrorMode = InvalidParamErrorMode.OMIT_ACTION) -> ActionsMetadata:
        assert self.actions
        assert supported_types is not None

        omitted_types = omitted_types or []

        result = OrderedDict()
        for actionName, action in self.actions.items():
            sig = inspect.signature(action)
            params = sig.parameters

            if not validate_params(on_invalid_params, actionName, params.values(), supported_types, omitted_types):
                continue

            params_metadata = build_params_metadata(params, omitted_types)
            result[actionName] = params_metadata

        return result

    def do_action(self, fn_handler, params):
        fn_handler(*params)
