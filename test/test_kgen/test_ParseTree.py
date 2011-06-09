'''
Created on Jun 9, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from kgen.datastructure import ParseTree
from StringIO import StringIO

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
        input = ''
        self.do_test(input, [])


if __name__ == "__main__":
    unittest.main()
