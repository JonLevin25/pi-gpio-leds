import inspect
import logging as log
from collections import OrderedDict
from enum import Enum
from typing import List, Iterator, Mapping

ParamsMetadata = Mapping[str, type]


class InvalidParamErrorMode(Enum):
    OMIT_ACTION = 0,
    # OMIT_PARAM = 1,
    THROW = 2,


def _has_annotation(inspected_param: inspect.Parameter):
    return inspected_param.annotation != inspect.Parameter.empty


def _valid_param(param: inspect.Parameter, supported_types: List[type], omitted_params: List[str]) -> bool:
    if param.name in omitted_params:
        return True
    if not _has_annotation(param):
        return False

    param_type = param.annotation
    return  param_type in supported_types


def build_params_metadata(params: Mapping[str, inspect.Parameter], omitted_params: List[str]) -> ParamsMetadata:
    result = OrderedDict()
    for param_name, param_val in params.items():
        param_type = param_val.annotation
        if param_name in omitted_params:
            continue
        result[param_name] = param_type.__name__ if _has_annotation(param_val) else 'None'

    return result


def validate_params(error_mode: InvalidParamErrorMode,
                    action_name: str,
                    params: Iterator[inspect.Parameter],
                    supported_types: List[type],
                    omitted_params: List[str]) -> bool:
    def is_invalid(param: inspect.Parameter):
        return not _valid_param(param, supported_types, omitted_params)

    invalid_params = list(filter(is_invalid, params))
    if len(invalid_params) == 0:
        return True

    msg = f'Action signature has invalid params! action: {action_name}. params: {", ".join(map(lambda param: param.name, invalid_params))}'
    if error_mode == InvalidParamErrorMode.THROW:
        raise ValueError(msg)

    if error_mode == InvalidParamErrorMode.OMIT_ACTION:
        log.error(msg)
        return False
