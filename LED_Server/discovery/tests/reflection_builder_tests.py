import logging
import unittest

from Utils.ActionsRouter import ActionsRouter


class TestClass:
    pass


from LED_Server.discovery.reflection_builder import build_actions_metadata, ErrorMode


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
        'x': int,
        'a': str
    }


class ReflectionBuilderTests(unittest.TestCase):
    def test_simple(self):
        router0 = ActionsRouter(None, actions={'test0': testAction0})
        result = build_actions_metadata(router0, ErrorMode.THROW, supported_types, omitted_types)
        self.assertEqual({'test0': expected_params_0}, result)

    def test_throws(self):
        router1 = ActionsRouter(None, actions={'test1': testAction1})
        router2 = ActionsRouter(None, actions={'test2': testAction2})
        self.assertRaises(ValueError,
                          lambda: build_actions_metadata(router1, ErrorMode.THROW, supported_types, omitted_types))
        self.assertRaises(ValueError,
                          lambda: build_actions_metadata(router2, ErrorMode.THROW, supported_types, omitted_types))

    def test_unannotated(self):
        router1 = ActionsRouter(None, actions={'test0': testAction0, 'test1': testAction1})
        # OMIT
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = build_actions_metadata(router1, ErrorMode.LOG_AND_OMIT, supported_types, omitted_types)
            self.assertEqual({
                'test0': expected_params_0,
                'test1': {
                    'x': int,
                    'a': str
                }
            }, result)

        # INCLUDE
        with self.assertLogs(logging.getLogger(), level='ERROR'):
            result = build_actions_metadata(router1, ErrorMode.LOG_AND_INCLUDE, supported_types, omitted_types)
            self.assertEqual({
                'test0': expected_params_0,
                'test1': {
                    'x': int,
                    'a': str,
                    'c': None
                }
            }, result)
