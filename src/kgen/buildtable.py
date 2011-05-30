'''
Created on May 30, 2011

@author: jagadeesh
'''
from core import PEmap

def build_kgen_table(rule_list, rule_columns):
    columns = PEmap()
    
    def create_lhs_columns(rule_columns):
        for pe in rule_columns:
            columns.add(pe)
    
    def create_rule_columns(rule_list):
        for rule in rule_list:
            for pe in rule:
                columns.add(pe)
    
    create_lhs_columns(rule_columns)
    create_rule_columns(rule_list)
    
    return [ x for x in columns]
