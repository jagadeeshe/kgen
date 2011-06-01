'''
Created on May 30, 2011

@author: jagadeesh
'''
from core import PEmap, KgenTable, FAIL
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
    
    def calculate_next_state(pattern_string, current_state, commit_flag):
        if len(pattern_string) == 1:
            # we are at the end of the pattern string
            if commit_flag:
                transition = 1
            else:
                transition = FAIL
            #log.debug("last pe trans to :%d", transition)
            return transition
        
        pe = pattern_string[0]
        transition = 0
        
        for col_index, _ in columns.match(pe):
            if transition == 0:
                # this is the first potential transition
                new_trans = table.get_transition(current_state, col_index)
                if new_trans != 0 and new_trans != current_state:
                    transition = new_trans
            else:
                # we already have a potential next state transition.
                new_trans = table.get_transition(current_state, col_index)
                if new_trans != transition and new_trans != current_state:
                    transition = 0
                    break
        
        if transition == 0:
            new_state = len(table)
            if new_state == current_state:
                new_state += 1
            return new_state
        else:
            return transition
    
    def insert_pattern_element(pattern_string, current_state, commit_flag):
        pe = pattern_string[0]
        old_commit_flag = commit_flag
        commit_flag |= pe.isCOMMIT()
        
        next_state = calculate_next_state(pattern_string, current_state, commit_flag)
        
        for col_idx, _ in columns.match(pe):
            table.add_transition(current_state, col_idx, next_state, old_commit_flag)
        
        if len(pattern_string) > 1:
            # if there are more pattern elements insert it recursively
            insert_pattern_element(pattern_string[1:], next_state, commit_flag)
    
    
    def insert_rules(rules):
        for rule in rules:
            insert_pattern_element(rule, 1, False)
    
    
    def add_default_transitions():
        for row in table.states():
            for col_idx, col in columns:
                transition = table.get_transition(row, col_idx)
                if transition != 0: continue
                if table.iscommitted(row):
                    back = FAIL
                else:
                    back = 1
                    if col.defaultToFail():
                        if not table.iscommitted(back):
                            back = FAIL
                    else:
                        if table.iscommitted(back):
                            back = 1
                
                table.add_transition(row, col_idx, back)
            
    create_lhs_columns(rule_columns)
    create_rule_columns(rule_list)
    table = KgenTable(len(columns), padding)
    insert_rules(rule_list)
    add_default_transitions()
    
    output = "%s\n%s" %(columns, table)
    print output
    return output

