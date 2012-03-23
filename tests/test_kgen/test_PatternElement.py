'''
Created on May 20, 2011

@author: jagadeeshe
'''
import unittest
from kgen.datastructure import PE

class PatternElementTest(unittest.TestCase):

    def test_default(self):
        p = PE('a', 'b')
        self.assertEqual('a', p.lex)
        self.assertEqual('b', p.sur)
        self.assertFalse(p.isCOMMIT())
        self.assertFalse(p.isREPEAT())
        self.assertFalse(p.isALTERNATIVE())

    def test_default2(self):
        p = PE('a')
        self.assertEqual('a', p.lex)
        self.assertEqual('a', p.sur)


    def test_COMMIT(self):
        p = PE('a', 'b')
        p.mark_COMMIT()
        self.assertTrue(p.isCOMMIT())
        self.assertFalse(p.isREPEAT())
        self.assertFalse(p.isALTERNATIVE())

    def test_REPEAT(self):
        p = PE('a', 'b')
        p.mark_REPEAT()
        self.assertFalse(p.isCOMMIT())
        self.assertTrue(p.isREPEAT())
        self.assertFalse(p.isALTERNATIVE())

    def test_ALTERNATIVE(self):
        p = PE('a', 'b')
        p.mark_ALTERNATIVE()
        self.assertFalse(p.isCOMMIT())
        self.assertFalse(p.isREPEAT())
        self.assertTrue(p.isALTERNATIVE())

    def test_all(self):
        p = PE('a', 'b')
        p.mark_COMMIT()
        p.mark_REPEAT()
        p.mark_ALTERNATIVE()
        self.assertTrue(p.isCOMMIT())
        self.assertTrue(p.isREPEAT())
        self.assertTrue(p.isALTERNATIVE())

