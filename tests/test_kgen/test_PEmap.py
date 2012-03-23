'''
Created on Jun 1, 2011

@author: jagadeeshe
'''
import unittest
from kgen.datastructure import PE, PEmap

class PEmapTest(unittest.TestCase):

    def test_unique(self):
        a = PE('a')
        b = PE('b')
        pemap = PEmap()
        self.assertEqual(0, pemap.add(a))
        self.assertEqual(1, pemap.add(b))
        self.assertEqual(2, len(pemap))
        self.assertEqual(a, pemap[0])
        self.assertEqual(b, pemap[1])
        self.assertEqual(0, pemap.indexof(a))
        self.assertEqual(1, pemap.indexof(b))
        for x, _ in pemap: pass
        self.assertEqual(1, x)
        self.assertEqual("   a b @\n   a b @\n  -------", str(pemap))

    def test_duplicate(self):
        a = PE('a','b')
        a2 = PE('a','b',PE.COMMIT)
        pemap = PEmap()
        pemap.add(a)
        pemap.add(a2)
        self.assertEqual(1, len(pemap))
        self.assertTrue(pemap[0].defaultToFail())

