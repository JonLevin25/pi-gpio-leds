import json
import logging
import unittest
from LED_Server.actions.action_routers.ActionsRouter import ActionsRouter
from LED_Server.models.action_models import ActionRequestParam, ActionRequest
from LED_Server.actions.action_routers.reflection_builder import InvalidParamErrorMode


class TestClass:
    def __init__(self, something):
        self.something = something


# test is missing type on purpose - shouldnt care
def testAction0(test, x: int, a: str):
    logging.info(f'a: {a}; x: {x + 1}; test: {test.something}')


def testAction1(test: TestClass, x: int, a: str, c):
    pass


def testAction2(test: TestClass, x: int, y: set):
    pass


def testAction3(x: int):
    logging.info('OK')


supported_types = [int, str]
closure_params = {'test': TestClass('else')}

expected_params_0 = {
    'x': 'int',
    'a': 'str'
}

class FnCallTests(unittest.TestCase):
    def test_json_deserialize_fn_call_and_closure(self):
        router0 = ActionsRouter({'test0': testAction0}, supported_types, closure_params)
        action_json = '{"name":"test0", "params":[{"name": "x", "value": "3"}, {"name": "a", "value": "test"}]}'
        action_request = ActionRequest.fromDecodedJson(json.loads(action_json))

        with self.assertLogs(level='INFO') as log:
            router0.handle(action_request)
            self.assertEqual(1, len(log.output))
            self.assertEqual(f'a: test; x: 4; test: else', log.records[0].msg)

    def test_closure_doesnt_break_functions_without_it(self):
        router3 = ActionsRouter({'test3': testAction3}, supported_types, closure_params)
        action_request = ActionRequest('test3', [ActionRequestParam('x', 1)])

        with self.assertLogs(level='INFO') as log:
            router3.handle(action_request)
            self.assertEqual(f'OK', log.records[0].msg)


class ReflectionBuilderTests(unittest.TestCase):
    def test_simple(self):
        router0 = ActionsRouter({'test0': testAction0}, supported_types, closure_params)
        result = router0.get_metadata(InvalidParamErrorMode.THROW)
        self.assertEqual({'test0': expected_params_0}, result)

    def test_throws(self):
        router1 = ActionsRouter({'test1': testAction1}, supported_types, closure_params)
        router2 = ActionsRouter({'test2': testAction2}, supported_types, closure_params)
        self.assertRaises(ValueError,
                          lambda: router1.get_metadata(InvalidParamErrorMode.THROW))
        self.assertRaises(ValueError,
                          lambda: router2.get_metadata(InvalidParamErrorMode.THROW))

    def test_unannotated(self):
        router1 = ActionsRouter({'test0': testAction0, 'test1': testAction1}, supported_types, closure_params)
        # OMIT ACTION
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = router1.get_metadata(InvalidParamErrorMode.OMIT_ACTION)
            self.assertEqual({
                'test0': expected_params_0
            }, result)

    def test_unsupported_param(self):
        router2 = ActionsRouter({'test0': testAction0, 'test2': testAction2}, supported_types, closure_params)
        # OMIT
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = router2.get_metadata(InvalidParamErrorMode.OMIT_ACTION)
            self.assertEqual({
                'test0': expected_params_0,
            }, result)
