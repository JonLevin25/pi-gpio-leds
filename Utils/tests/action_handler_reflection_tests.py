import logging
import unittest
from Utils.ActionsRouter import ActionsRouter
from Utils.reflection_builder import InvalidParamErrorMode


class TestClass:
    pass


# todo: test lambdas, test methods
def testAction0(test: TestClass, x: int, a: str):
    pass


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


class ReflectionBuilderTests(unittest.TestCase):
    def test_simple(self):
        router0 = ActionsRouter(actions={'test0': testAction0})
        result = router0.get_metadata(supported_types, omitted_types, InvalidParamErrorMode.THROW)
        self.assertEqual({'test0': expected_params_0}, result)

    def test_throws(self):
        router1 = ActionsRouter(actions={'test1': testAction1})
        router2 = ActionsRouter(actions={'test2': testAction2})
        self.assertRaises(ValueError,
                          lambda: router1.get_metadata(supported_types, omitted_types, InvalidParamErrorMode.THROW))
        self.assertRaises(ValueError,
                          lambda: router2.get_metadata(supported_types, omitted_types, InvalidParamErrorMode.THROW))

    def test_unannotated(self):
        router1 = ActionsRouter(actions={'test0': testAction0, 'test1': testAction1})
        # OMIT ACTION
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = router1.get_metadata(supported_types, omitted_types, InvalidParamErrorMode.OMIT_ACTION)
            self.assertEqual({
                'test0': expected_params_0
            }, result)

    def test_unsupported_param(self):
        router2 = ActionsRouter(actions={'test0': testAction0, 'test2': testAction2})
        # OMIT
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = router2.get_metadata(supported_types, omitted_types, InvalidParamErrorMode.OMIT_ACTION)
            self.assertEqual({
                'test0': expected_params_0,
            }, result)
