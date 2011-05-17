'''
Created on May 5, 2011

@author: jagadeesh
'''

from ply import yacc
import core

"""
Example rules:  (blanks are ignored)

      SUBSET V      a e i o u
      SUBSET Vhigh  i u
      PAIRS  tcdkk
             tcdkg
      c:t => _ i:i
      c:t <= x:X (z [ f | :g | h: ]) _
      c:t \<= x _
      c:t <=> _ m '

"""

class KgenParser:

    ''' This is required '''    
    tokens = core.tokens

    start = 'ruleset'

    def __init__(self, klexer, ast, **kwargs):
        self.klexer = klexer
        self.ast = ast
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_error(self, p):
        self.ast.r_error()

    def p_empty(self, p):
        '''empty : '''
        pass

    def p_ruleset(self, p):
        'ruleset : kimmo_comments subsets pairs rules'
        self.ast.r_ruleset()

    def p_kimmo_comments_list(self, p):
        'kimmo_comments : kimmo_comments kimmo_comment'
        self.ast.r_kimmo_comment(p[2])

    def p_kimmo_comments_empty(self, p):
        'kimmo_comments : empty opt_eol'
        pass

    def p_kimmo_comment(self, p):
        'kimmo_comment :  KIMMO_COMMENT eol'
        p[0] = p[1]

    def p_eol_term(self, p):
        'eol : EOL'
        self.ast.r_eol_term()

    def p_eol(self, p):
        'eol : eol EOL'
        self.ast.r_eol_term()

    def p_opt_eol_empty(self, p):
        'opt_eol : empty'
        self.ast.r_opt_eol_empty()

    def p_opt_eol(self, p):
        'opt_eol : eol'
        self.ast.r_opt_eol()

    def p_subsets(self, p):
        'subsets : subsets subset'
        self.ast.r_subset(p[2])

    def p_subsets_empty(self, p):
        'subsets : empty'
        pass

    def p_subset(self, p):
        'subset : SUBSET SUBSET_NAME segment_string EOL kimmo_comments'
        if self.ast.has_subset_name(p[2]):
            # TODO: has semantic error: redeclared
            pass
        p[0] = (p[2], p[3])

    def p_segment_string_oneseg(self, p):
        'segment_string : oneseg'
        p[0] = p[1]

    def p_segment_string_expr(self, p):
        'segment_string : segment_string oneseg'
        p[0] = p[1] + p[2]

    def p_oneseg(self, p):
        'oneseg : SEGMENT'
        p[0] = p[1]

    def p_pairs_empty(self, p):
        'pairs : empty'
        pass

    def p_pairs_expr(self, p):
        'pairs : pairs pairlist kimmo_comments'
        pass

    def p_pairlist(self, p):
        'pairlist : PAIRS opt_eol segment_string EOL segment_string EOL'
        self.ast.r_pair(p[3], p[5])

    def p_rules_term(self, p):
        'rules : empty'
        pass

    def p_rules_list(self, p):
        'rules : rules rule'
        pass

    def p_rule(self, p):
        'rule : RULE opt_eol lhs_pair rule_operator rhs EOL kimmo_comments'
        self.ast.lhs = p[3]
        self.ast.operator = p[4]
        self.ast.rhs = p[5]

    def p_lhs_pair(self, p):
        'lhs_pair : segment COLON segment'
        p[0] = (p[1], p[3])

    def p_rule_operator(self, p):
        '''rule_operator : ONLY_OCCURS
                         | ALWAYS_OCCURS
                         | ALWAYS_AND_ONLY_OCCURS
                         | NEVER_OCCURS'''
        p[0] = p[1]

    def p_rhs(self, p):
        'rhs : rhs_item'
        p[0] = [p[1]]

    def p_segment(self, p):
        '''segment : SEGMENT
                   | SUBSET_NAME'''
        p[0] = p[1]

    def p_rhs_list(self, p):
        'rhs : rhs REG_OR rhs_item'
        p[0] = p[1].append(p[3])

    def p_rhs_item_only_left_context(self, p):
        'rhs_item : pattern_list UNDER'
        p[0] = (p[1], None)
        self.ast.lc = p[1]

    def p_rhs_item_only_right_context(self, p):
        'rhs_item : UNDER pattern_list'
        p[0] = (None, p[2])
        self.ast.rc = p[2]

    def p_rhs_item_both_left_right_context(self, p):
        'rhs_item : pattern_list UNDER pattern_list'
        p[0] = (p[1], p[3])
        self.ast.lc = p[1]
        self.ast.rc = p[3]

    def p_pattern_list_single(self, p):
        'pattern_list : pattern_element'
        p[0] = [p[1]]

    def p_pattern_list(self, p):
        'pattern_list : pattern_list pattern_element'
        p[0] = p[1].append(p[2])

    def p_pattern_element_segment_pair(self, p):
        'pattern_element : segment_pair'
        p[0] = p[1]

    def p_pattern_element_repeat(self, p):
        'pattern_element : segment_pair REG_REPEAT'
        p[0] = (p[1], p[2])

    def p_segment_pair(self, p):
        'segment_pair : segment COLON segment'
        p[0] = (p[1], p[3])

    def p_segment_pair_segment_any(self, p):
        'segment_pair : segment COLON'
        p[0] = (p[1], '@')

    def p_segment_pair_default(self, p):
        'segment_pair : segment'
        p[0] = (p[1], p[1])

    def p_segment_pair_any_segment(self, p):
        'segment_pair : COLON segment'
        p[0] = ('@', p[2])

    def p_segment_pair_alternate(self, p):
        'segment_pair : alternate'
        p[0] = (p[1],)

    def p_segment_pair_segment_alternate(self, p):
        'segment_pair : segment COLON alternate'
        p[0] = [(p[1], x) for x in p[3]]

    def p_segment_pair_alternate_segment(self, p):
        'segment_pair : alternate COLON segment'
        p[0] = [(x, p[3]) for x in p[1]]

    def p_segment_pair_alternate_alternate(self, p):
        'segment_pair : alternate COLON alternate'
        if len(p[1]) != len(p[3]):
            # TODO: raise error
            pass
        p[0] = [(p[1][x], p[3][x]) for x in range(len(p[1]))]

    def p_segment_pair_alternate_any(self, p):
        'segment_pair : alternate COLON'
        p[0] = [(x, '@') for x in p[1]]

    def p_alternate(self, p):
        'alternate : LBRACE segment alternate_list RBRACE'
        p[0] = [p[2],] + p[3]

    def p_alternate_list_term(self, p):
        'alternate_list : COMMA segment'
        p[0] = [p[2]]

    def p_alternate_list(self, p):
        'alternate_list : alternate_list COMMA segment'
        p[0] = p[1].append(p[3])


    def parse(self, input, ast=None):
        if ast:
            self.ast = ast
        
        self.parser.parse(input=input, lexer=self.klexer.lexer)
        

