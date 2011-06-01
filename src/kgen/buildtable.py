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
    
    def calculate_next_state(current_state, pe):
        transition = 0
        for col_index, col in columns:
            cond = col.isPairwiseSame(pe) and (not col.isCOMMIT() or pe.isCOMMIT())
            if not cond: continue
            
            if transition == 0:
                # this is the first potential transition
                transition = table.get_transition(current_state, col_index)
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
        
        # calculate next stransition
        if len(pattern_string) == 1:
            # we are at the end of the pattern string
            if commit_flag:
                next_state = 1
            else:
                next_state = FAIL
        else:
            next_state = calculate_next_state(current_state, pe)
        
        for col_idx, col in columns:
            if not col.isPairwiseSame(pe): continue
            if not col.isCOMMIT() or pe.isCOMMIT():
                table.add_transition(current_state, col_idx, next_state, old_commit_flag)
        
        if len(pattern_string) > 1:
            insert_pattern_element(pattern_string[1:], next_state, commit_flag)
    
    
    def insert_rules(rules):
        for rule in rules:
            insert_pattern_element(rule, 1, False)
    
    
    def add_default_transitions():
        for row in range(1, len(table)):
#            log.debug("row: %d", row)
            for col_idx, col in columns:
                transition = table.get_transition(row, col_idx)
                if transition != 0: continue
                #log.debug("row: %d col: %d trans: %d", row, col_idx, transition)
                if table.is_row_commited(row):
                    back = FAIL
                else:
                    back = 1
                    if col.isCOMMIT():
                        if not table.is_row_commited(back):
                            back = FAIL
                    else:
                        if table.is_row_commited(back):
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

