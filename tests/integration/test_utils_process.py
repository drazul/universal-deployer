import unittest

from udeploy.plugins.utils.process import execute


class TestExecute(unittest.TestCase):
    def test_foo(self):
        assert 0 is execute('')
