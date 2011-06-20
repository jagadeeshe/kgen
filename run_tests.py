#!/usr/bin/env python

'''
Created on Jun 10, 2011

@author: jagadeesh
'''
import unittest
import test_kgen
import test_functional

if __name__ == "__main__":
    tests = []
    tests += test_kgen.all_tests()
    tests += test_functional.all_tests()
    suite = unittest.TestSuite()
    suite.addTests(tests)
    
    unittest.TextTestRunner().run(suite)