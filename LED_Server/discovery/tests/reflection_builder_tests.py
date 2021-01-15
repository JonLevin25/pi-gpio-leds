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
class ReflectionBuilderTests(unittest.TestCase):
    def test_simple(self):
        router = ActionsRouter(None, actions={
            'test0': testAction0
        })

        result = build_actions_metadata(router, ErrorMode.THROW, supported_types, omitted_types)
        self.assertEqual(result, {
            'test0': {
                'x': int,
                'a': str
            }
        })

    