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
    suite = []
    suite.append(unittest.makeSuite(tokenizerTest))
    suite.append(unittest.makeSuite(PatternElementTest))
    suite.append(unittest.makeSuite(PEmapTest))
    suite.append(unittest.makeSuite(parserTest))
    suite.append(unittest.makeSuite(KgenTableTest))
    suite.append(unittest.makeSuite(buildtableTest))
    suite.append(unittest.makeSuite(ParseTreeTest))
    return suite
