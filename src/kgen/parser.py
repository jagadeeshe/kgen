'''
Created on May 5, 2011

@author: jagadeesh
'''

from ply import yacc
import core
from core import cross_product, mark_alternate, add_optional_lhs, add_obligatory_lhs
import copy
from datastructure import PE

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

    def __init__(self, klexer, output, ast, **kwargs):
        self.klexer = klexer
        self.output = output
        self.ast = ast
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_error(self, p):
        self.ast.r_error()

    def p_empty(self, p):
        '''empty : '''
        pass

    def p_ruleset(self, p):
        'ruleset : kimmo_comments subsets pairs rules'
        self.ast.add_ruleset()

    def p_kimmo_comments_list(self, p):
        'kimmo_comments : kimmo_comments kimmo_comment eol'
        pass

    def p_kimmo_comments_empty(self, p):
        'kimmo_comments : opt_eol'
        pass

    def p_kimmo_comment(self, p):
        'kimmo_comment :  KIMMO_COMMENT'
        self.ast.add_kimmo_comment(p[1])

    def p_eol_term(self, p):
        'eol : EOL'
        self.ast.add_eol()

    def p_eol(self, p):
        'eol : eol EOL'
        self.ast.add_eol()

    def p_opt_eol_empty(self, p):
        'opt_eol : empty'
        self.ast.r_opt_eol_empty()

    def p_opt_eol(self, p):
        'opt_eol : eol'
        self.ast.r_opt_eol()

    def p_subsets(self, p):
        'subsets : subsets subset kimmo_comments'
        pass

    def p_subsets_empty(self, p):
        'subsets : empty'
        pass

    def p_subset(self, p):
        'subset : SUBSET SUBSET_NAME segment_string EOL'
        if self.ast.has_subset_name(p[2]):
            print >> self.output, "Line %d: subset %s is already defined in line %s." % (p.lineno(1), p[2], self.ast.subset_lineno(p[2]))
            return
        p[0] = (p[2], p[3])
        self.ast.add_subset(p[0], p.lineno(1))

    def p_unnamed_subset_error(self, p):
        'subset : SUBSET error segment_string EOL'
        print >> self.output, "Line %d: subset should have name. see the rule for naming a subset." % p.lineno(1)
        self.parser.errok()

    def p_subset_definition_not_found(self, p):
        'subset : SUBSET SUBSET_NAME error EOL'
        print >> self.output, "Line %d: subset definition should be on the same line." % p.lineno(1)
        self.parser.errok()

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
        self.ast.add_pair(p[3], p[5])

    def p_rules_term(self, p):
        'rules : empty'
        pass

    def p_rules_list(self, p):
        'rules : rules rule kimmo_comments'
        pass

    def p_rule(self, p):
        'rule : RULE opt_eol lhs rhs EOL'
        self.ast.rhs = p[4]
        self.ast.add_rule(p.lineno(3))

    def p_lhs_only_occurs(self, p):
        'lhs : lhs_pair ONLY_OCCURS'
        add_optional_lhs(p[1][0], self.ast)
        p[0] = p[1]
        self.ast.operator = p[2]
        self.ast.lhs = p[0]

    def p_lhs_always_occurs(self, p):
        'lhs : lhs_pair ALWAYS_OCCURS'
        add_obligatory_lhs(p[1][0], self.ast)
        p[0] = p[1]
        self.ast.operator = p[2]
        self.ast.lhs = p[0]

    def p_lhs_always_and_only_occurs(self, p):
        'lhs : lhs_pair ALWAYS_AND_ONLY_OCCURS'
        l1 = copy.deepcopy(p[1][0])
        p[1].append(l1)
        add_obligatory_lhs(p[1][0], self.ast)
        add_optional_lhs(p[1][1], self.ast)
        p[0] = p[1]
        self.ast.operator = p[2]
        self.ast.lhs = p[0]

    def p_lhs_never_occurs(self, p):
        'lhs : lhs_pair NEVER_OCCURS'
        p[0] = p[1]
        self.ast.operator = p[2]
        self.ast.lhs = p[0]

    def p_lhs_pair(self, p):
        'lhs_pair : segment COLON segment'
        p[0] = [[PE(p[1], p[3])]]

    def p_lhs_pair_segment_alternate(self, p):
        'lhs_pair : segment COLON alternate'
        p[0] = [[PE(p[1], x) for x in p[3]]]
        mark_alternate(p[0])

    def p_lhs_pair_alternate_segment(self, p):
        'lhs_pair : alternate COLON segment'
        p[0] = [[PE(x, p[3]) for x in p[1]]]
        mark_alternate(p[0])

    def p_lhs_pair_alternate_alternate(self, p):
        'lhs_pair : alternate COLON alternate'
        if len(p[1]) != len(p[3]):
            # raise error
            pass
        p[0] = [[PE(p[1][x], p[3][x]) for x in range(len(p[1]))]]
        mark_alternate(p[0])
        self.ast.lhs = p[0]

    def p_rhs(self, p):
        'rhs : rhs_item'
        p[0] = p[1]

    def p_segment(self, p):
        '''segment : SEGMENT
                   | SUBSET_NAME'''
        p[0] = p[1]

    def p_rhs_list(self, p):
        'rhs : rhs REG_OR rhs_item'
        p[0] = p[1] + p[3]

    def p_rhs_item_only_left_context(self, p):
        'rhs_item : pattern_list UNDER'
        p[0] = cross_product(p[1], self.ast.lhs)
        self.ast.lc = p[1]

    def p_rhs_item_only_right_context(self, p):
        'rhs_item : UNDER pattern_list'
        p[0] = cross_product(self.ast.lhs, p[2])
        self.ast.rc = p[2]

    def p_rhs_item_both_left_right_context(self, p):
        'rhs_item : pattern_list UNDER pattern_list'
        p[0] = cross_product(p[1], cross_product(self.ast.lhs, p[3]))
        self.ast.lc = p[1]
        self.ast.rc = p[3]

    def p_pattern_list_single(self, p):
        'pattern_list : pattern_element'
        p[0] = p[1]

    def p_pattern_list(self, p):
        'pattern_list : pattern_list pattern_element'
        p[0] = cross_product(p[1], p[2])

    def p_pattern_element_segment_pair(self, p):
        'pattern_element : segment_pair'
        p[0] = p[1]

    def p_pattern_element_repeat(self, p):
        'pattern_element : segment_pair REG_REPEAT'
        p[1][0][0].mark_REPEAT()
        p[0] = p[1]

    def p_segment_pair(self, p):
        'segment_pair : segment COLON segment'
        p[0] = [[PE(p[1], p[3])]]

    def p_segment_pair_segment_any(self, p):
        'segment_pair : segment COLON'
        p[0] = [[PE(p[1], '@')]]

    def p_segment_pair_default(self, p):
        'segment_pair : segment'
        p[0] = [[PE(p[1])]]

    def p_segment_pair_any_segment(self, p):
        'segment_pair : COLON segment'
        p[0] = [[PE('@', p[2])]]

    def p_segment_pair_pattern_list(self, p):
        'segment_pair : LBRACKET pattern_list alternative_list RBRACKET'
        p[0] = p[2] + p[3]

    def p_segment_pair_optional_list(self, p):
        'segment_pair : LPAREN pattern_list RPAREN'
        for item in p[2]:
            if item[0] != PE(''):
                p[2].append([PE('')])
                break
        p[0] = p[2]

    def p_alternative_list_term(self, p):
        'alternative_list : REG_OR pattern_list'
        p[0] = p[2]

    def p_alternative_list(self, p):
        'alternative_list : alternative_list REG_OR pattern_list'
        p[0] = p[1] + p[3]

    def p_segment_pair_alternate(self, p):
        'segment_pair : alternate'
        p[0] = [[PE(x) for x in p[1]]]
        mark_alternate(p[0])

    def p_segment_pair_segment_alternate(self, p):
        'segment_pair : segment COLON alternate'
        p[0] = [[PE(p[1], x) for x in p[3]]]
        mark_alternate(p[0])

    def p_segment_pair_alternate_segment(self, p):
        'segment_pair : alternate COLON segment'
        p[0] = [[PE(x, p[3]) for x in p[1]]]
        mark_alternate(p[0])

    def p_segment_pair_alternate_alternate(self, p):
        'segment_pair : alternate COLON alternate'
        if len(p[1]) != len(p[3]):
            # TODO: raise error
            pass
        p[0] = [[PE(p[1][x], p[3][x]) for x in range(len(p[1]))]]
        mark_alternate(p[0])

    def p_segment_pair_alternate_any(self, p):
        'segment_pair : alternate COLON'
        p[0] = [[PE(x, '@') for x in p[1]]]
        mark_alternate(p[0])

    def p_alternate(self, p):
        'alternate : LBRACE segment alternate_list RBRACE'
        p[0] = [p[2]] + p[3]

    def p_alternate_list_term(self, p):
        'alternate_list : COMMA segment'
        p[0] = [p[2]]

    def p_alternate_list(self, p):
        'alternate_list : alternate_list COMMA segment'
        p[0] = p[1] + [p[3]]

    def parse(self, input, ast=None):
        if ast:
            self.ast = ast
        self.output.seek(0)
        self.output.truncate()
        self.parser.parse(input=input, lexer=self.klexer.lexer)
        

