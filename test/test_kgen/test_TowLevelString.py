'''
Created on May 19, 2011

@author: jagadeeshe
'''
import unittest
from kgen.core import TwoLevelString, KgenException

class TwoLevelStringTestCase(unittest.TestCase):

    def setUp(self):
        self.target = TwoLevelString()

    def add(self, other):
        self.target += other

    def test_invalid_other(self):
        self.assertRaises(KgenException, self.add, None)
        self.assertRaises(KgenException, self.add, [])

    def test_other_invalid_tuple(self):
        self.assertRaises(KgenException, self.add, ('a', 'b', 'c'))
        self.assertRaises(KgenException, self.add, ('', ''))
        self.assertRaises(KgenException, self.add, (None, ''))
        self.assertRaises(KgenException, self.add, ('', None))
        self.assertRaises(KgenException, self.add, (None, None))
        self.assertRaises(KgenException, self.add, ('aa', 'a'))
        self.assertRaises(KgenException, self.add, ('a', 'aa'))

    def test_tuple(self):
        s1 = TwoLevelString(('a', 'b'))
        self.add(('a', 'b'))
        self.assertEqual(self.target, s1)

    def test_same(self):
        s1 = TwoLevelString(('a', 'b'))
        self.add(s1)
        self.assertEqual(self.target, s1)

    def test_inequal(self):
        self.assertFalse(self.target == '')

    def test_length(self):
        self.assertEqual(0, len(self.target))

    def test_getitem(self):
        self.add(('a', 'b'))
        self.assertEqual(self.target[0], ('a', 'b'))

    def test_iter(self):
        self.add(('a', 'b'))
        for item in self.target: pass
        self.assertEqual(item, ('a', 'b'))

if __name__ == "__main__":
    unittest.main()