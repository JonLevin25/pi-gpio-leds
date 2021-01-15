import inspect
import logging as log
from collections import OrderedDict
from enum import Enum
from typing import List, Iterator, Dict, Mapping, Callable

from Utils.ActionsRouter import ActionsRouter


class ErrorMode(Enum):
    LOG_AND_INCLUDE = 0,
    LOG_AND_OMIT = 1,
    THROW = 2,


ParamsMetadata = Mapping[str, type]
ActionsMetadata = Mapping[str, ParamsMetadata]


# ignored == types that will
def build_actions_metadata(router: ActionsRouter, on_invalid_action: ErrorMode, supported_types: List[type],
                           omitted_types: List[type] = None) -> ActionsMetadata:

    assert router and router.actions
    assert supported_types is not None

    omitted_types = omitted_types or []

    result = OrderedDict()
    for actionName, action in router.actions.items():
        sig = inspect.signature(action)
        params = sig.parameters
        param_map = params.values()

        if not _validate_params(on_invalid_action, actionName, param_map, supported_types, omitted_types):
            continue

        params_metadata = _build_params_metadata(params, omitted_types)
        result[actionName] = params_metadata

    return result


def _build_params_metadata(params: Mapping[str, inspect.Parameter], omitted_types: List[type]) -> ParamsMetadata:
    result = OrderedDict()
    for param_name, param_val in params.items():
        param_type = param_val.annotation
        if param_type in omitted_types:
            continue
        result[param_name] = param_type if _has_annotation(param_val) else None

    return result


def _has_annotation(inspected_param: inspect.Parameter):
    return inspected_param.annotation != inspect.Parameter.empty


def _valid_param(param: inspect.Parameter, supported_types: List[type],
                 ignored_types: List[type]):
    if not _has_annotation(param):
        return False

    param_type = param.annotation
    return param_type in ignored_types or param_type in supported_types


def _validate_params(error_mode: ErrorMode,
                     action_name: str,
                     params: Iterator[inspect.Parameter],
                     supported_types: List[type],
                     ignored_types: List[type]) -> bool:
    def is_invalid(param: inspect.Parameter):
        return not _valid_param(param, supported_types, ignored_types)

    invalid_params = list(filter(is_invalid, params))
    if len(invalid_params) == 0:
        return True

    msg = f'Action signature has invalid params! action: {action_name}. params: {", ".join(map(lambda param: param.name, invalid_params))}'
    if error_mode == ErrorMode.THROW:
        raise ValueError(msg)

    if error_mode == ErrorMode.LOG_AND_INCLUDE:
        log.error(msg)
        return True

    if error_mode == ErrorMode.LOG_AND_OMIT:
        log.error(msg)
        return False
