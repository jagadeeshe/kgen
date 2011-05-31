'''
Created on May 30, 2011

@author: jagadeesh
'''
from core import PEmap, KgenTable
import logging

def build_kgen_table(rule_list, rule_columns, output=None, padding=0):
    columns = PEmap(padding)
    table = KgenTable(1)
    log = logging.getLogger("KgenBuilder")
    
    def create_lhs_columns(rule_columns):
        for pe in rule_columns:
            columns.add(pe)
    
    def create_rule_columns(rule_list):
        for rule in rule_list:
            for pe in rule:
                columns.add(pe)
    
    def get_column_index(pe):
        # this is the simple pattern_element to column mapping. more will follow
        return columns.indexof(pe)
    
    def calculate_next_state(current_state, pe):
        return current_state + 1
    
    def insert_pattern_element(pattern_string, current_state, commit_flag):
        pe = pattern_string[0]
        old_commit_flag = commit_flag
        
        commit_flag |= pe.isCOMMIT()
        
        # calculate next stransition
        if len(pattern_string) == 1:
            # we are at the end of the pattern string
            if commit_flag:
                next_state = 1
            else:
                next_state = 0
        else:
            next_state = calculate_next_state(current_state, pe)
        
        column_index = get_column_index(pe)
        
        table.add_transition(current_state, column_index, next_state, old_commit_flag)
        
        if len(pattern_string) > 1:
            insert_pattern_element(pattern_string[1:], next_state, commit_flag)
    
    
    def insert_rules(rules):
        for rule in rules:
            insert_pattern_element(rule, 1, False)
    
    create_lhs_columns(rule_columns)
    create_rule_columns(rule_list)
    table = KgenTable(len(columns), padding)
    insert_rules(rule_list)
    
    output = "%s\n%s" %(columns, table)
    print output
    return output

