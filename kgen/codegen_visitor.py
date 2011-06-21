'''
Created on Jun 14, 2011

@author: jagadeesh
'''

from kgen.visitor import Visitor
from kgen.datastructure import Node, NODE_TYPE_KIMMOHEADER, NODE_TYPE_SUBSET, NODE_TYPE_KIMMOTABLE
from kgen.buildtable import build_pair_table, build_kgen_table

class CodeGeneratorVisitor(Visitor):
    def start(self):
        self.alphabet = set()
        self.first_rule = True
    
    def visit_subset(self, value):
        '@value - tuple (lineno, subset_name, subset_string)'
        _, _, subset = value
        self._add_to_alphabet(subset)
        self.nodes.append(Node(NODE_TYPE_SUBSET, value))
    
    def visit_pair(self, value):
        '@value - tuple (lineno, lex_string, sur_string)'
        s1, s2 = value
        self._add_to_alphabet(s1)
        self._add_to_alphabet(s2)
        columns, table = build_pair_table(s1, s2)
        self.nodes.append(Node(NODE_TYPE_KIMMOTABLE, (columns, table)))
    
    def visit_rule(self, value):
        '@value - tuple (lineno, rule, columns)'
        if self.first_rule:
            self.prepare_kimmo_header()
            self.first_rule = False
        _, rule_list, rule_columns = value
        columns, table = build_kgen_table(rule_list, rule_columns)
        self.nodes.append(Node(NODE_TYPE_KIMMOTABLE, (columns, table)))
    
    def prepare_kimmo_header(self):
        alphabet = [s for s in self.alphabet]
        alphabet.sort()
        index = 0
        for node in self.nodes:
            if node.type in [NODE_TYPE_SUBSET, NODE_TYPE_KIMMOTABLE]:
                break
            index += 1
        while index >= 1:
            if self.nodes[index-1].value != '':
                index = index -1
            else:
                break
        self.nodes.insert(index, Node(NODE_TYPE_KIMMOHEADER, (alphabet, '0', '@', '#')))
    
    def _add_to_alphabet(self, string):
        for s in string:
            self.alphabet.add(s)
    
    def visit_rules_end(self):
        'called when rules section ends'
        if self.first_rule:
            self.prepare_kimmo_header()
            self.first_rule = False
    