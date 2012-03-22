'''
Created on May 30, 2011

@author: jagadeesh
'''
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from test_kgen.mock_ast import MockAST
from StringIO import StringIO
from kgen.buildtable import build_kgen_table
import logging
from tests.driver import DataRecord, generate_class

logging.basicConfig(level=logging.DEBUG)

class R(DataRecord):
    def __init__(self, name, _input, expectation):
        DataRecord.__init__(self, name, _input + "\n", expectation)


data_list = [
R('test_only_rule_case1',
"RULE    p:b => _ +:0 m",
'''
   p + m @
   b 0 m @
  ---------
1: 2 1 1 1
2. 0 3 0 0
3. 0 0 1 0
'''),

R('test_only_rule_case2',
"RULE    p:b <= _ +:0 m",
'''
   p p + m @
   b @ 0 m @
  -----------
1: 1 2 1 1 1
2: 1 2 3 1 1
3: 1 2 1 0 1
'''),

R('test_only_rule_case3',
"RULE    p:b <=> _ +:0 m",
'''
   p p + m @
   b @ 0 m @
  -----------
1: 4 2 1 1 1
2: 4 2 3 1 1
3: 4 2 1 0 1
4. 0 0 5 0 0
5. 0 0 0 1 0
'''),

R('test_only_rule_case4',
"RULE    p:b /<= _ +:0 m",
'''
   p + m @
   b 0 m @
  ---------
1: 2 1 1 1
2: 2 3 1 1
3: 2 1 0 1
'''),

R('test_only_rule_case5',
"RULE    p:b => m +:0 _ ",
'''
   p m + @
   b m 0 @
  ---------
1: 0 2 1 1
2: 0 2 3 1
3: 1 2 1 1
'''),

R('test_only_rule_case6',
"RULE    p:b <= m +:0 _ ",
'''
   p p m + @
   b @ m 0 @
  -----------
1: 1 1 2 1 1
2: 1 1 2 3 1
3: 1 0 2 1 1
'''),

R('test_only_rule_case7',
"RULE    p:b <=> m +:0 _ ",
'''
   p p m + @
   b @ m 0 @
  -----------
1: 0 1 2 1 1
2: 0 1 2 3 1
3: 1 0 2 1 1
'''),

R('test_only_rule_case8',
"RULE    p:b /<= m +:0 _ ",
'''
   m + p @
   m 0 b @
  ---------
1: 2 1 1 1
2: 2 3 1 1
3: 2 1 0 1
'''),

R('test_only_rule_case9',
"RULE    s:z => v _ v",
'''
   s v @
   z v @
  -------
1: 0 2 1
2: 3 2 1
3. 0 2 0
'''),

R('test_only_rule_case10',
"RULE    s:z <= v _ v",
'''
   s s v @
   z @ v @
  ---------
1: 1 1 2 1
2: 1 3 2 1
3: 1 1 0 1
'''),

R('test_only_rule_case11',
"RULE    s:z <=> v _ v",
'''
   s s v @
   z @ v @
  ---------
1: 0 1 2 1
2: 4 3 2 1
3: 0 1 0 1
4. 0 0 2 0
'''),

R('test_only_rule_case12',
"RULE    s:z /<= v _ v",
'''
   v s @
   v z @
  -------
1: 2 1 1
2: 2 3 1
3: 0 1 1
'''),

]

def buildtable_driver(data):
    print data

    klexer = KgenLexer()
    mockAST = MockAST()
    output = StringIO()
    kparser = KgenParser(klexer, output, mockAST)

    kparser.parse(data, mockAST)
    columns, table = build_kgen_table(mockAST.rules[0][2], mockAST.rules[0][3])
    print "%s\n%s" % (columns, table)
    return "\n%s\n%s" % (columns, table,)


BuildTableTestCase = generate_class('BuildTableTestCase', buildtable_driver, data_list)
