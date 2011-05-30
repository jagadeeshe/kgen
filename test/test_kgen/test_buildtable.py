'''
Created on May 30, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from test_kgen.mock_ast import MockAST
from kgen.core import PE
from StringIO import StringIO
from kgen.buildtable import build_kgen_table

class buildtableTest(unittest.TestCase):
    def __init__(self, methodName='run'):
        unittest.TestCase.__init__(self, methodName)
        klexer = KgenLexer()
        mockAST = MockAST()
        self.output = StringIO()
        self.kparser = KgenParser(klexer, self.output, mockAST)

    def test_only_rule_case1(self):
        data = '''RULE 
            p:b => a c _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        result = build_kgen_table(mockAST.rules[0][2], mockAST.rules[0][3])
        
        self.assertEqual([PE('p','b',PE.COMMIT),PE('a'),PE('c')], result)


    def test_only_rule_case2(self):
        data = '''RULE 
            p:b <= a c _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        result = build_kgen_table(mockAST.rules[0][2], mockAST.rules[0][3])
        
        self.assertEqual([PE('p','b'),PE('p','@'),PE('a'),PE('c')], result)


    def test_only_rule_case3(self):
        data = '''RULE 
            p:b <=> a c _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        result = build_kgen_table(mockAST.rules[0][2], mockAST.rules[0][3])
        
        self.assertEqual([PE('p','b'),PE('p','@'),PE('p','b',PE.COMMIT),PE('a'),PE('c')], result)


    def test_only_rule_case4(self):
        data = '''RULE 
            p:b /<= a c _
        '''
        mockAST = MockAST()
        self.kparser.parse(data, mockAST)
        result = build_kgen_table(mockAST.rules[0][2], mockAST.rules[0][3])
        
        self.assertEqual([PE('a'),PE('c'),PE('p','b')], result)


if __name__ == "__main__":
    unittest.main()