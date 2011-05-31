'''
Created on May 30, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from test_kgen.mock_ast import MockAST
from StringIO import StringIO
from kgen.buildtable import build_kgen_table

class buildtableTest(unittest.TestCase):
    def __init__(self, methodName='run'):
        unittest.TestCase.__init__(self, methodName)
        klexer = KgenLexer()
        mockAST = MockAST()
        self.output = StringIO()
        self.kparser = KgenParser(klexer, self.output, mockAST)

    def do_test(self, input, output):
        print input
        padding = 8
        mockAST = MockAST()
        self.kparser.parse(input+"\n", mockAST)
        result = build_kgen_table(mockAST.rules[0][2], mockAST.rules[0][3], padding=padding)
        self.assertEqual(output, "\n%s%s" % (result, ' ' * padding))


    def test_only_rule_case1(self):
        input = " RULE    p:b => a c _ d e"
        output = '''
           p a c d e
           b a c d e
          -----------
        1: 0 2 0 0 0
        2: 0 0 3 0 0
        3: 4 0 0 0 0
        4. 0 0 0 5 0
        5. 0 0 0 0 1
        '''
        self.do_test(input, output)


    def test_only_rule_case2(self):
        input = " RULE    p:b <= a c _ d e"
        output = '''
           p p a c d e
           b @ a c d e
          -------------
        1: 0 0 2 0 0 0
        2: 0 0 0 3 0 0
        3: 0 4 0 0 0 0
        4: 0 0 0 0 5 0
        5: 0 0 0 0 0 0
        '''
        self.do_test(input, output)


    def test_only_rule_case3(self):
        input = " RULE    p:b <=> a c _ d e"
        output = '''
           p p p a c d e
           b @ b a c d e
          ---------------
        1: 0 0 0 2 0 0 0
        2: 0 0 0 0 3 0 0
        3: 0 4 4 0 0 0 0
        4. 0 0 0 0 0 5 0
        5. 0 0 0 0 0 0 1
        '''
        self.do_test(input, output)


    def test_only_rule_case4(self):
        input = " RULE    p:b /<= a c _ d e"
        output = '''
           a c p d e
           a c b d e
          -----------
        1: 2 0 0 0 0
        2: 0 3 0 0 0
        3: 0 0 4 0 0
        4: 0 0 0 5 0
        5: 0 0 0 0 0
        '''
        self.do_test(input, output)


if __name__ == "__main__":
    unittest.main()