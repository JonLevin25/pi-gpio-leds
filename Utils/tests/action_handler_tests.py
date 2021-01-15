import logging
import unittest
from Utils.ActionsRouter import ActionsRouter, ActionRequest, ActionRequestParam
from Utils.reflection_builder import InvalidParamErrorMode


class TestClass:
    pass


def testAction0(test: TestClass, x: int, a: str):
    logging.log(f'a: {a}; x: {x + 1}')


def testAction1(test: TestClass, x: int, a: str, c):
    pass


def testAction2(test: TestClass, x: int, y: set):
    pass


supported_types = [int, str]
omitted_types = [TestClass]

expected_params_0 = {
    'x': 'int',
    'a': 'str'
}

class JsonToFnCallTests(unittest.TestCase):
    def test_method_call(self):
        router0 = ActionsRouter({'test0': testAction0}, supported_types, omitted_types)
        action_request = ActionRequest('test0', [ActionRequestParam('x', '3'), ActionRequestParam('a', 'test')])

        with self.assertLogs(level='INFO') as log:
            router0.handle(action_request)
            self.assertEqual(1, len(log.output))
            self.assertEqual(f'a: test; x: 4', log.output[0])


class ReflectionBuilderTests(unittest.TestCase):
    def test_simple(self):
        router0 = ActionsRouter({'test0': testAction0}, supported_types, omitted_types)
        result = router0.get_metadata(InvalidParamErrorMode.THROW)
        self.assertEqual({'test0': expected_params_0}, result)

    def test_throws(self):
        router1 = ActionsRouter({'test1': testAction1}, supported_types, omitted_types)
        router2 = ActionsRouter({'test2': testAction2}, supported_types, omitted_types)
        self.assertRaises(ValueError,
                          lambda: router1.get_metadata(InvalidParamErrorMode.THROW))
        self.assertRaises(ValueError,
                          lambda: router2.get_metadata(InvalidParamErrorMode.THROW))

    def test_unannotated(self):
        router1 = ActionsRouter({'test0': testAction0, 'test1': testAction1}, supported_types, omitted_types)
        # OMIT ACTION
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = router1.get_metadata(InvalidParamErrorMode.OMIT_ACTION)
            self.assertEqual({
                'test0': expected_params_0
            }, result)

    def test_unsupported_param(self):
        router2 = ActionsRouter({'test0': testAction0, 'test2': testAction2}, supported_types, omitted_types)
        # OMIT
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = router2.get_metadata(InvalidParamErrorMode.OMIT_ACTION)
            self.assertEqual({
                'test0': expected_params_0,
            }, result)
