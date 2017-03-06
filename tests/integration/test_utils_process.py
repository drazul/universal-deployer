import unittest
import os
import sys

cwd = os.getcwd() + '/udeploy'
sys.path.insert(0, cwd)

from plugins.utils.process import execute


class TestExecute(unittest.TestCase):
    def test_foo(self):
        assert 0 is execute('')
