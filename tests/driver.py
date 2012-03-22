'''
Created on Mar 15, 2012

@author: jagadeesh
'''
import unittest
from functools import update_wrapper

class DataRecord:
    
    def __init__(self, name, data, expectation):
        self.name = name
        if type(data) != tuple:
            self.data = (data,)
        else:
            self.data = data
        self.expectation = expectation


class DataDrivenTest:
    
    def __init__(self, data_list):
        self.data_list = data_list
    
    def __call__(self, func):
        self.func = func
        
        def _driver(*args):
            for record in self.data_list:
                actual = self.func(*(args + record.data))
                if not actual == record.expectation:
                    raise AssertionError, \
                        ('%s %r != %r' % (record.name, actual, record.expectation))
        
        update_wrapper(_driver, func)
        return _driver


def generate_class(class_name, func, data_list):
    def test_wrapper(name, expectation, *args):
        def test_wrapped(self):
            actual = func(*args)
            self.assertEqual(actual, expectation)
        
        setattr(test_wrapped, '__doc__', 'test for %s' % name)
        return test_wrapped

    tests = {}
    index = 0
    for record in data_list:
        testfunc = test_wrapper(record.name, record.expectation, *record.data)
        tests['test_case_%s'%index] = testfunc
        index += 1

    klass = type(class_name, (unittest.TestCase,), tests)
    setattr(klass, '__module__', getattr(func, '__module__'))
    return klass


