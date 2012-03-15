'''
Created on Jun 9, 2011

@author: jagadeesh
'''
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from kgen.datastructure import ParseTree, NODE_TYPE_KIMMOCOMMENT,\
    NODE_TYPE_SUBSET, NODE_TYPE_PAIR, NODE_TYPE_RULE
from StringIO import StringIO
from kgen.datastructure import NODE_TYPE_NEWLINE

from tests.driver import DataDrivenTest, DataRecord

class R(DataRecord):
    def __init__(self, name, _input, *args):
        DataRecord.__init__(self, name, _input, list(args))


@DataDrivenTest([
R('test_empty', ''),

R('test_newline',
'''
''',
NODE_TYPE_NEWLINE),

R('test_newlines',
'''
    
''',
NODE_TYPE_NEWLINE, NODE_TYPE_NEWLINE),

R('test_kimmo_comments',
'''
!;first comment

!;second comment
''',
NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT),

R('test_subsets',
'''
!; consonent subset
SUBSET C b c d f
!; wovel subset
SUBSET V a e i o u
''',
NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_SUBSET, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_SUBSET),

R('test_pairs',
'''
SUBSET C b c d
!; default correspondence
PAIRS b c d +
      b c d 0
''',
NODE_TYPE_NEWLINE, NODE_TYPE_SUBSET, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_PAIR),

R('test_rules',
'''
!;only rule
RULE p:b => _ +:0 m
!;always rule
RULE p:b <= _ +:0 m
''',
NODE_TYPE_NEWLINE, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_RULE, NODE_TYPE_KIMMOCOMMENT, NODE_TYPE_RULE),

])
def test_ParseTree(data):
    klexer = KgenLexer()
    ptree = ParseTree()
    output = StringIO()
    kparser = KgenParser(klexer, output, ptree)
    kparser.parse(data, ptree)
    return [node.type for node in ptree]

