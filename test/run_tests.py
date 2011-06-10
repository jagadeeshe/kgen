#!/usr/bin/env python

'''
Created on Jun 10, 2011

@author: jagadeesh
'''
import sys
import unittest

sys.path.append('../src')
sys.path.append('../lib/ply-3.4-py2.6.egg')

from test_kgen import all_tests

if __name__ == "__main__":
    tests = all_tests()
    unittest.TextTestRunner().run(tests)
