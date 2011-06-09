'''
Created on Jun 9, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from kgen.datastructure import ParseTree, NODE_TYPE_KIMMOCOMMENT,\
    NODE_TYPE_SUBSET
from StringIO import StringIO
from kgen.datastructure import NODE_TYPE_NEWLINE

class ParseTreeTest(unittest.TestCase):

    def __init__(self, methodName='run'):
        unittest.TestCase.__init__(self, methodName)
        klexer = KgenLexer()
        ptree = ParseTree()
        self.output = StringIO()
        self.kparser = KgenParser(klexer, self.output, ptree)

    def do_test(self, input, output):
        ptree = ParseTree()
        self.kparser.parse(input, ptree)
        self.assertEqual(output, [node.type for node in ptree])

    def test_empty(self):
        data = ''
        self.do_test(data, [])

    def test_newline(self):
        data = '''
        '''
        self.do_test(data, [NODE_TYPE_NEWLINE])

    def test_newlines(self):
        data = '''
        
        '''
        self.do_test(data, [NODE_TYPE_NEWLINE, NODE_TYPE_NEWLINE])

    def test_kimmo_comments(self):
        data = '''
        !;first comment
        
        !;second comment
        '''
        self.do_test(data, [NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT])

    def test_subsets(self):
        data = '''
        !; consonent subset
        SUBSET C b c d f
        !; wovel subset
        SUBSET V a e i o u
        '''
        self.do_test(data, [NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_SUBSET, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_SUBSET])

if __name__ == "__main__":
    unittest.main()
