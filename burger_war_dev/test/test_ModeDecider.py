import os
import glob
import unittest2

from burger_war_dev/scripts/ModeDecider import ModeDecider

from ./testcases_ModeDecider import test_cases

class TestModeDecider(unittest2.TestCase):
    def setUp(self):
        self.test_cases = test_cases
        self.mode_dec = ModeDecider()

    def test_getActMode(self):
        print("\ntest_getActMode")
        for case in self.test_cases:
            with self.subTest(input_data=case["input"], result=case["next_mode"]):
                current_mode = input_data["current_mode"]
                info_dict = input_data["info_dict"]
                self.assertEqual(self.mode_dec.getActMode(current_mode, **info_dict), result)

if __name__ == '__main__':
    unittest2.main()