'''
Created on May 11, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from test_kgen.mock_ast import MockAST

class parserTest(unittest.TestCase):

    def __init__(self, methodName='run'):
        unittest.TestCase.__init__(self, methodName)
        klexer = KgenLexer()
        mockAST = MockAST()
        self.kparser = KgenParser(klexer, mockAST)


    def test_p_kimmo_comments_empty(self):
        data = ''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, len(mockAST.kimmo_comments))


    def test_p_kimmo_comment(self):
        data = '''!;kimmo comment
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual([';kimmo comment'], mockAST.kimmo_comments)
        self.assertEqual(1, mockAST.eol_term)


    def test_p_kimmo_comments(self):
        data = '''!;first comment
                  !;second comment
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual([';first comment', ';second comment'], mockAST.kimmo_comments)
        self.assertEqual(2, mockAST.eol_term)


    def test_p_eol_term(self):
        data = '''
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(1, mockAST.eol_term)


    def test_p_eol(self):
        data = '''
                
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(2, mockAST.eol_term)


    def test_p_opt_eol_empty(self):
        data = ''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, mockAST.opt_eol)
        self.assertEqual(1, mockAST.opt_eol_empty)


    def test_p_opt_eol(self):
        data = '''
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, mockAST.opt_eol_empty)
        self.assertEqual(1, mockAST.opt_eol)


    def test_p_subsets_empty(self):
        data = ''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(0, len(mockAST.subsets))


    def test_p_subsets(self):
        data = '''
                SUBSET V    a
                SUBSET C    b c d f
               '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        
        self.assertEqual(0, mockAST.error)
        self.assertEqual(2, len(mockAST.subsets))
        self.assertEqual('a', mockAST.subsets['V'])
        self.assertEqual('bcdf', mockAST.subsets['C'])



if __name__ == "__main__":
    unittest.main()