#!/usr/bin/env python

'''
Created on Jun 10, 2011

@author: jagadeesh
'''
import sys
import unittest

sys.path.append('../src')
sys.path.append('../lib/ply-3.4-py2.6.egg')

import test_kgen
import test_functional

if __name__ == "__main__":
    tests = []
    tests += test_kgen.all_tests()
    tests += test_functional.all_tests()
    
    unittest.TextTestRunner().run(tests)
