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
        self.rules = []
        self.lhs = None
        self.operator = ''
        self.rhs = None
        self.lc = None
        self.rc = None
        self.columns = []
    
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
    
    def add_kimmo_comment(self, comment):
        self.kimmo_comments.append(comment)
    
    def has_subset_name(self, name):
        return self.subsets.has_key(name)
    
    def get_subset(self, name):
        return self.subsets[name][1]
    
    def subset_lineno(self, name):
        return self.subsets[name][0]
    
    def r_subset(self, subset, lineno):
        self.subsets[subset[0]] = (lineno, subset[1])
    
    def r_pair(self, s1, s2):
        for i in range(len(s1)):
            self.pairs[(s1[i], s2[i])] = True
    
    def r_rule(self):
        self.rules.append((self.lhs, self.operator, self.rhs, self.columns))
