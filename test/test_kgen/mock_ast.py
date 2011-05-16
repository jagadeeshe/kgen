'''
Created on May 11, 2011

@author: jagadeesh
'''

class MockAST:
    def __init__(self):
        self.error = 0
        self.ruleset = 0
        self.eol_term = 0
        self.opt_eol = 0
        self.opt_eol_empty = 0
        self.kimmo_comments = []
        self.subsets = {}
        self.pairs = {}
        self.lhs = None
        self.operator = ''
    
    def r_error(self):
        self.error += 1
    
    def r_ruleset(self):
        self.ruleset += 1
    
    def r_eol_term(self):
        self.eol_term += 1
    
    def r_opt_eol(self):
        self.opt_eol += 1
    
    def r_opt_eol_empty(self):
        self.opt_eol_empty += 1
    
    def r_kimmo_comment(self, comment):
        self.kimmo_comments.append(comment)
    
    def has_subset_name(self, name):
        return self.subsets.has_key(name)
    
    def r_subset(self, subset):
        self.subsets[subset[0]] = subset[1]
    
    def r_pair(self, s1, s2):
        for i in range(len(s1)):
            self.pairs[(s1[i], s2[i])] = True
    
    def r_lhs(self, pair):
        self.lhs = pair
    
    def r_operator(self, op):
        self.operator = op