'''
Created on May 30, 2011

@author: jagadeesh
'''
from kgen.datastructure import PEmap, KgenTable, PE
from kgen.core import FAIL
import logging

def build_kgen_table(rule_list, rule_columns, output=None, padding=0):
    columns = PEmap(padding)
    table = KgenTable(1)
    log = logging.getLogger("KgenBuilder")
    
    def eachcell():
        for state in table:
            for col_idx, col in columns:
                yield state, col_idx, col
    
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
                new_trans = table[current_state, col_index]
                if new_trans != 0 and new_trans != current_state:
                    transition = new_trans
            else:
                # we already have a potential next state transition.
                new_trans = table[current_state, col_index]
                if new_trans != transition and new_trans != current_state:
                    transition = 0
                    break
        
        if transition == 0:
            return table.create_state(current_state, pe)
        else:
            return transition
    
    def insert_pattern_element(pattern_string, current_state, commit_flag):
        pe = pattern_string[0]
        table[current_state].committed = commit_flag
        commit_flag |= pe.isCOMMIT()
        
        next_state = calculate_next_state(pattern_string, current_state, commit_flag)
        
        for col_idx, _ in columns.match(pe):
            table.add_transition(current_state, col_idx, next_state)
        
        if len(pattern_string) > 1:
            # if there are more pattern elements insert it recursively
            insert_pattern_element(pattern_string[1:], next_state, commit_flag)
    
    
    def insert_rules(rules):
        for rule in rules:
            insert_pattern_element(rule, 1, False)
    
    
    def compute_back_loop(row, col_idx, col):
        longrow = 1
        tmp = [col]
        for row2 in range(2, len(table)+1):
            if tmp == table[row2].context:
                longrow = row2
        return longrow
    
    def add_default_transitions():
        for state, col_idx, col in eachcell():
            if table[state, col_idx] != 0:
                ''' if the state is not 0 means the [state, col_idx] position has a transition to some state or FAIL entry '''
                continue
            if table[state].committed:
                ''' only rule - states traversed after the special correspondence is recognized '''
                back = FAIL
            else:
                back = compute_back_loop(state, col_idx, col)
                if col.defaultToFail():
                    if not table[back].committed:
                        ''' only rule - special correspondence column transition to FAIL state '''
                        back = FAIL
                else:
                    if table[back].committed:
                        back = 1
            
            table.add_transition(state, col_idx, back)
    
    def add_back_loops():
        for state, col_idx, col in eachcell():
            if table[state, col_idx] == 1:
                back = compute_back_loop(state, col_idx, col)
                if not table[back].committed:
                    table.add_transition(state, col_idx, back)
    
    create_lhs_columns(rule_columns)
    create_rule_columns(rule_list)
    table = KgenTable(len(columns), padding)
    insert_rules(rule_list)
    add_default_transitions()
    add_back_loops()
    
    return (columns, table)


def build_pair_table(lexseg, surseg, padding=0):
    columns = PEmap(padding=padding, any_column=False)
    for i in range(len(lexseg)):
        lex = lexseg[i]
        sur = surseg[i]
        columns.add(PE(lex,sur))
    
    table = KgenTable(len(columns), padding=padding, any_column=False)
    for col_idx, _ in columns:
        table.add_transition(1, col_idx, 1)
    return columns, table
