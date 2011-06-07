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
import logging

class buildtableTest(unittest.TestCase):
    def __init__(self, methodName='run'):
        unittest.TestCase.__init__(self, methodName)
        logging.basicConfig(level=logging.DEBUG)
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
        input = " RULE    p:b => _ +:0 m"
        output = '''
           p + m @
           b 0 m @
          ---------
        1: 2 1 1 1
        2. 0 3 0 0
        3. 0 0 1 0
        '''
        self.do_test(input, output)


    def test_only_rule_case2(self):
        input = " RULE    p:b <= _ +:0 m"
        output = '''
           p p + m @
           b @ 0 m @
          -----------
        1: 1 2 1 1 1
        2: 1 2 3 1 1
        3: 1 2 1 0 1
        '''
        self.do_test(input, output)


    def t2est_only_rule_case3(self):
        input = " RULE    p:b <=> _ +:0 m"
        output = '''
           p p + m @
           b @ 0 m @
          -----------
        1: 4 2 1 1 1
        2: 4 2 3 1 1
        3: 4 2 1 0 1
        4. 0 0 5 0 0
        5. 0 0 0 1 0
        '''
        self.do_test(input, output)


    def test_only_rule_case4(self):
        input = " RULE    p:b /<= _ +:0 m"
        output = '''
           p + m @
           b 0 m @
          ---------
        1: 2 1 1 1
        2: 2 3 1 1
        3: 2 1 0 1
        '''
        self.do_test(input, output)


    def test_only_rule_case5(self):
        input = " RULE    p:b => m +:0 _ "
        output = '''
           p m + @
           b m 0 @
          ---------
        1: 0 2 1 1
        2: 0 2 3 1
        3: 1 2 1 1
        '''
        self.do_test(input, output)


    def test_only_rule_case6(self):
        input = " RULE    p:b <= m +:0 _ "
        output = '''
           p p m + @
           b @ m 0 @
          -----------
        1: 1 1 2 1 1
        2: 1 1 2 3 1
        3: 1 0 2 1 1
        '''
        self.do_test(input, output)


    def t2est_only_rule_case7(self):
        input = " RULE    p:b <=> m +:0 _ "
        output = '''
           p p m + @
           b @ m 0 @
          -----------
        1: 0 1 2 1 1
        2: 0 1 2 3 1
        3: 1 0 2 1 1
        '''
        self.do_test(input, output)


    def test_only_rule_case8(self):
        input = " RULE    p:b /<= m +:0 _ "
        output = '''
           m + p @
           m 0 b @
          ---------
        1: 2 1 1 1
        2: 2 3 1 1
        3: 2 1 0 1
        '''
        self.do_test(input, output)


    def test_only_rule_case9(self):
        input = " RULE    s:z => v _ v"
        output = '''
           s v @
           z v @
          -------
        1: 0 2 1
        2: 3 2 1
        3. 0 2 0
        '''
        self.do_test(input, output)


    def test_only_rule_case10(self):
        input = " RULE    s:z <= v _ v"
        output = '''
           s s v @
           z @ v @
          ---------
        1: 1 1 2 1
        2: 1 3 2 1
        3: 1 1 0 1
        '''
        self.do_test(input, output)


    def t2est_only_rule_case11(self):
        input = " RULE    s:z <=> v _ v"
        output = '''
           s s v @
           z @ v @
          ---------
        1: 0 1 2 1
        2: 4 3 2 1
        3: 0 1 0 1
        4. 0 0 2 0
        '''
        self.do_test(input, output)


    def test_only_rule_case12(self):
        input = " RULE    s:z /<= v _ v"
        output = '''
           v s @
           v z @
          -------
        1: 2 1 1
        2: 2 3 1
        3: 0 1 1
        '''
        self.do_test(input, output)



if __name__ == "__main__":
    unittest.main()