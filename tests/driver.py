'''
Created on Mar 15, 2012

@author: jagadeesh
'''
import unittest

class DataRecord:
    
    def __init__(self, name, data, expectation):
        self.name = name
        if type(data) != tuple:
            self.data = (data,)
        else:
            self.data = data
        self.expectation = expectation
    
    def verify(self, test, actual):
        test.assertEqual(actual, self.expectation)


def generate_class(class_name, func, data_list):
    def test_wrapper(record):
        def test_wrapped(self):
            actual = func(*record.data)
            record.verify(self, actual)
        
        setattr(test_wrapped, '__doc__', 'test for %s' % record.name)
        return test_wrapped

    tests = {}
    index = 0
    for record in data_list:
        testfunc = test_wrapper(record)
        tests['test_case_%s'%index] = testfunc
        index += 1

    klass = type(class_name, (unittest.TestCase,), tests)
    setattr(klass, '__module__', getattr(func, '__module__'))
    return klass


