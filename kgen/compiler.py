'''
Created on Jun 14, 2011

@author: jagadeesh
'''
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from kgen.datastructure import ParseTree
from kgen.codegen_visitor import CodeGeneratorVisitor
from kgen.tablebuilder_visitor import TableBuilderVisitor

def compile(text, output, error, options):
    ''' compiles the two-level rule description into two-level finite state table
    @text  - text string
    @output - output stream where the compiled rules were written
    @error  - error stream where syntax error and symantic errors were written
    @option - compilation options
    '''
    
    klexer = KgenLexer()
    ptree = ParseTree()
    kparser = KgenParser(klexer, error, ptree)

    ''' tokenize and parse the text string '''
    text = text.decode(options.encoding)
    kparser.parse(text)
    
    ''' now @ptree will have complete parse tree for the text '''
    if error.getvalue() != '':
        # if you are here then there are syntax errors so return
        return
    
    #print [node for node in ptree]
    
    codegen = CodeGeneratorVisitor(output, error, options)
    ptree2 = codegen.visit_parse_tree(ptree)
    
    builder = TableBuilderVisitor(output, error, options)
    builder.visit_parse_tree(ptree2)


