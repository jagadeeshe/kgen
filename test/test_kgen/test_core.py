'''
Created on May 20, 2011

@author: jagadeeshe
'''
import unittest
from kgen.core import cross_product

class Test(unittest.TestCase):

    def test_cross_product(self):
        l1 = ['a', 'b', 'c']
        l2 = ['d']
        target = ['ad', 'bd', 'cd']
        self.assertEqual(target, cross_product(l1, l2))

        l1 = ['a', 'b', 'c']
        l2 = ['d', 'e']
        target = ['ad', 'ae', 'bd', 'be', 'cd', 'ce']
        self.assertEqual(target, cross_product(l1, l2))

        l1 = [['a'], ['b'], ['c']]
        l2 = [['d'], ['e']]
        target = [['a','d'], ['a','e'], ['b','d'], ['b','e'], ['c','d'], ['c','e']]
        self.assertEqual(target, cross_product(l1, l2))

if __name__ == "__main__":
    unittest.main()