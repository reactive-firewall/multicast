# tests/test_hear_missing_params.py
import unittest
from multicast.hear import McastHEAR

class TestHearMissingParams(unittest.TestCase):
    def test_missing_group(self):
        hear_instance = McastHEAR()
        with self.assertRaises(ValueError):
            hear_instance.doStep(port=59259)