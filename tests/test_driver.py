'''
Created on Mar 22, 2012

@author: jagadeesh
'''
from driver import DataRecord as R, generate_class


def my_driver(in1):
    return in1

data_list = [
R('case1', 10, 10),
R('case2', 20, 20),
R('case3', 30, 30),
]


MyTestCase = generate_class('MyTestCase', my_driver, data_list)

