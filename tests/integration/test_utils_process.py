import unittest

from plugins.utils.process import execute


class TestExecute(unittest.TestCase):
    def test_foo(self):
        assert None == execute(None)        


