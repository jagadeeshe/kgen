'''
Created on Jun 15, 2011

@author: jagadeesh
'''
from kgen.visitor import Visitor

class TableBuilderVisitor(Visitor):
    
    def visit_string(self, value):
        '@value - string'
        print >>self.output, value
    
    def visit_kimmo_header(self, value):
        '@value - tuple (alphabet, null, any, bondary)'
    
    def visit_kimmo_table(self, value):
        '@value - KGenTable'
    