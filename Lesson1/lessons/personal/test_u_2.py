import unittest
from square import Square

""" Exposure to unittest """

class SquareTest(unittest.TestCase):
    """ Exposure to unit test lib """
    def test_pos_nums(self):
        nums = {
            1: 1,
            2: 4, 
            3: 9,
            12: 144,
            4: 16,
            15: 225
        }

        for key,val in nums.items():
            res = Square.calc(key)
            self.assertEqual(res, val, f"Squaring the num {key}")