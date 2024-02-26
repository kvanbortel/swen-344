import unittest
from tests.test_utils import *


class TestExample(unittest.TestCase):

    def setUp(self):  
        """Initialize DB using API call"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        print("DB Should be reset now")

    def test_hello_world(self):
        expected = { '1' : 'hello, world!' }
        actual = get_rest_call(self, 'http://localhost:5000')
        self.assertEqual(expected, actual)
