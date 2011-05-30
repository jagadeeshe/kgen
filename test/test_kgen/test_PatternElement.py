'''
Created on May 20, 2011

@author: jagadeeshe
'''
import unittest
from kgen.core import PatternElement

class PatternElementTest(unittest.TestCase):

    def test_default(self):
        p = PatternElement('a', 'b')
        self.assertEqual('a', p.lex)
        self.assertEqual('b', p.sur)
        self.assertFalse(p.isCOMMIT())
        self.assertFalse(p.isREPEAT())
        self.assertFalse(p.isALTERNATIVE())

    def test_default2(self):
        p = PatternElement('a')
        self.assertEqual('a', p.lex)
        self.assertEqual('a', p.sur)


    def test_COMMIT(self):
        p = PatternElement('a', 'b')
        p.mark_COMMIT()
        self.assertTrue(p.isCOMMIT())
        self.assertFalse(p.isREPEAT())
        self.assertFalse(p.isALTERNATIVE())

    def test_REPEAT(self):
        p = PatternElement('a', 'b')
        p.mark_REPEAT()
        self.assertFalse(p.isCOMMIT())
        self.assertTrue(p.isREPEAT())
        self.assertFalse(p.isALTERNATIVE())

    def test_ALTERNATIVE(self):
        p = PatternElement('a', 'b')
        p.mark_ALTERNATIVE()
        self.assertFalse(p.isCOMMIT())
        self.assertFalse(p.isREPEAT())
        self.assertTrue(p.isALTERNATIVE())

    def test_all(self):
        p = PatternElement('a', 'b')
        p.mark_COMMIT()
        p.mark_REPEAT()
        p.mark_ALTERNATIVE()
        self.assertTrue(p.isCOMMIT())
        self.assertTrue(p.isREPEAT())
        self.assertTrue(p.isALTERNATIVE())

if __name__ == "__main__":
    unittest.main()