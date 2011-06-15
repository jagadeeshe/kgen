'''
Created on Jun 10, 2011

@author: jagadeesh
'''

from kgen.datastructure import Node
from kgen.datastructure import NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_NEWLINE, NODE_TYPE_PAIR, NODE_TYPE_RULE, NODE_TYPE_STRING, NODE_TYPE_SUBSET
from kgen.datastructure import NODE_TYPE_KIMMOHEADER, NODE_TYPE_KIMMOTABLE

class Visitor(object):
    '''This interface specifies how the parse tree nodes will be called during pre-processing step and table generation step.'''
    
    def __init__(self, output, error, options):
        self.output = output
        self.error = error
        self.options = options
        self.nodes = []
        self.callbacks = {
            NODE_TYPE_NEWLINE      : self.visit_newline,
            NODE_TYPE_KIMMOCOMMENT : self.visit_kimmo_comment,
            NODE_TYPE_SUBSET       : self.visit_subset,
            NODE_TYPE_PAIR         : self.visit_pair,
            NODE_TYPE_RULE         : self.visit_rule,
            NODE_TYPE_STRING       : self.visit_string,
            NODE_TYPE_KIMMOHEADER  : self.visit_kimmo_header,
            NODE_TYPE_KIMMOTABLE   : self.visit_kimmo_table,
        }
    
    def visit_newline(self, value):
        '@value - "\n" character'
        self.nodes.append(Node(NODE_TYPE_STRING, ''))
    
    def visit_kimmo_comment(self, comment):
        '@comment - comment string'
        self.nodes.append(Node(NODE_TYPE_STRING, comment))
    
    def visit_subset(self, value):
        '@value - tuple (lineno, subset_name, subset_string)'
    
    def visit_pair(self, value):
        '@value - tuple (lineno, lex_string, sur_string)'
    
    def visit_rule(self, value):
        '@value - tuple (lineno, rule, columns)'
    
    def visit_rules_end(self):
        'called when rules section ends'
    
    def visit_string(self, value):
        '@value - string'
    
    def visit_kimmo_table(self, value):
        '@value - KGenTable'
    
    def visit_kimmo_header(self, value):
        '@value - tuple (alphabet, null, any, bondary)'
    
    def visit_parse_tree(self, nodes):
        for node in nodes:
            self.callbacks[node.type](node.value)
        
        self.visit_rules_end()
        return self
    
    def __iter__(self):
        for node in self.nodes:
            yield node
    

