'''
Created on Jun 10, 2011

@author: jagadeesh
'''

import unittest

from test_tokenizer import tokenizerTest
from test_PatternElement import PatternElementTest
from test_PEmap import PEmapTest
from test_parser import parserTest
from test_KgenTable import KgenTableTest
from test_buildtable import buildtableTest
from test_ParseTree import ParseTreeTest

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tokenizerTest))
    suite.addTest(unittest.makeSuite(PatternElementTest))
    suite.addTest(unittest.makeSuite(PEmapTest))
    suite.addTest(unittest.makeSuite(parserTest))
    suite.addTest(unittest.makeSuite(KgenTableTest))
    suite.addTest(unittest.makeSuite(buildtableTest))
    suite.addTest(unittest.makeSuite(ParseTreeTest))
    return suite
