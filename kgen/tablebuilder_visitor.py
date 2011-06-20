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
        alphabet, null, any, boundry = value
        buf = 'ALPHABET   '
        for a in alphabet:
            buf += ' %s' % a
        print >>self.output, buf
        print >>self.output, "NULL        %s" % null
        print >>self.output, "ANY         %s" % any
        print >>self.output, "BOUNDARY    %s" % boundry
        print >>self.output
    
    def visit_subset(self, value):
        '@value - tuple (lineno, subset_name, subset_string)'
        _, name, subset = value
        buf = "SUBSET    %s   " % name
        for a in subset:
            buf += ' %s' % a
        print >>self.output, buf
    
    def visit_kimmo_table(self, value):
        '@value - PEmap, KGenTable'
        columns, table = value
        tablestr = '%s' % table
        print >>self.output, columns
        print >>self.output, tablestr[:-1]