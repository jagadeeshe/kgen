'''
Created on Mar 15, 2012

@author: jagadeesh
'''

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
