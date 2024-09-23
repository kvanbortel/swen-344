import unittest
import json
from rest_utils import *

class TestNutrikit(unittest.TestCase):
    def test_api(self):
        result = get_rest_call(self, 'http://localhost:5000/nutrikit_api')
        self.assertEqual(2, len(result),"Should have returned a length of '2'")
        print("API test successfully returned a list of '2' ")
        print(result)
