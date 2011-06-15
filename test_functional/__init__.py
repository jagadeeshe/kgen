'''
Created on Jun 15, 2011

@author: jagadeesh
'''
import unittest
from test_compiler import CompilerTest

def all_tests():
    suite = []
    suite.append(unittest.makeSuite(CompilerTest))
    return suite
