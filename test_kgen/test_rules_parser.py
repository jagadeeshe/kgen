'''
Created on Mar 21, 2012

@author: jagadeeshe
'''
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from test_kgen.mock_ast import MockAST
from kgen.datastructure import PE
from StringIO import StringIO
C = PE.COMMIT
S = PE.REPEAT

from tests.driver import DataRecord, generate_class

class R(DataRecord):
    def __init__(self, _input, *rhs):
        new_rhs_list = []
        for rhs_row in rhs:
            new_rhs_row = []
            for el in rhs_row:
                if el == '':
                    el = ('',)
                if type(el) == str:
                    el = tuple(el)
                if type(el) <> tuple:
                    raise Exception("unsupported type")
                new_rhs_row.append(PE(*el))
            new_rhs_list.append(new_rhs_row)
        DataRecord.__init__(self, _input, _input + "\n", new_rhs_list)

data_list = [
R('RULE p:b => a _',
  ['a', ('p','b',C)]
),
R('RULE p:b => a _ b',
  ['a', ('p','b',C), 'b']
),
R('RULE p:b => _ a',
  [('p','b',C), 'a']
),
R('RULE p:b <= a _',
  ['a', ('p','@')]
),
R('RULE p:b <=  _ a',
  [('p','@'), 'a']
),
R('RULE p:b <= a _ b',
  ['a', ('p','@'), 'b']
),
R('RULE p:b /<= a _',
  ['a', ('p','b')]
),
R('RULE p:b /<= _ a',
  [('p','b'), 'a']
),
R('RULE p:b /<= a _ b',
  ['a', ('p','b'), 'b']
),
R('RULE p:b <=> a _ ',
  ['a', ('p','@')],
  ['a', ('p','b',C)]
),
R('RULE p:b <=> _ a',
  [('p','@'), 'a'],
  [('p','b',C), 'a']
),
R('RULE p:b <=> a _ b',
  ['a', ('p','@'), 'b'],
  ['a', ('p','b',C), 'b']
),
R('RULE p:b => abc _',
  ['a', 'b', 'c', ('p','b',C)]
),
R('RULE p:b => abc _ abcd',
  ['a', 'b', 'c', ('p','b',C), 'a', 'b', 'c', 'd']
),
R('RULE p:b => _ abc',
  [('p','b',C), 'a', 'b', 'c']
),
R('RULE p: {b, c} => a _',
  ['a', ('p','b',C)],
  ['a', ('p','c',C)]
),
R('RULE {p, d}:b => a _',
  ['a', ('p','b',C)],
  ['a', ('d','b',C)]
),
R('RULE {p, d}:{b, c} => a _',
  ['a', ('p','b',C)],
  ['a', ('d','c',C)]
),
R('RULE p:b <= a:c _',
  [('a','c'), ('p','@')]
),
R('RULE p:b <= a: _',
  [('a','@'), ('p','@')]
),
R('RULE p:b <= a _',
  ['a', ('p','@')]
),
R('RULE p:b <= {a , b} _',
  ['a', ('p','@')],
  ['b', ('p','@')]
),
R('RULE p:b <= c : {a , b} _',
  [('c','a'), ('p','@')],
  [('c','b'), ('p','@')]
),
R('RULE p:b <= {a , b} : c _',
  [('a','c'), ('p','@')],
  [('b','c'), ('p','@')]
),
R('RULE p:b <= {a, b} : {c, d} _',
  [('a','c'), ('p','@')],
  [('b','d'), ('p','@')]
),
R('RULE p:b <= {a, b} :  _',
  [('a','@'), ('p','@')],
  [('b','@'), ('p','@')]
),
R('RULE p:b <= a:c * _',
  [('a','c',S), ('p','@')]
),
R('RULE p:b <= a:c * b _',
  [('a','c',S), 'b', ('p','@')]
),
R('RULE p:b <= a:c * d:e * _',
  [('a','c',S), ('d','e',S), ('p','@')]
),
R('RULE p:b <= {a, b} : {c, d} * _',
  [('a','c',S), ('p','@')],
  [('b','d',S), ('p','@')]
),
R('RULE p:b <= a:c b:c _',
  [('a','c'), ('b','c'), ('p','@')]
),
R('RULE p:b <= a b {c, d} e _',
  ['a','b','c','e',('p','@')],
  ['a','b','d','e',('p','@')]
),
R('RULE p:b <= [a | b] c _',
  ['a','c',('p','@')],
  ['b','c',('p','@')]
),
R('RULE p:b <= e [a | b] c _',
  ['e','a','c',('p','@')],
  ['e','b','c',('p','@')]
),
R('RULE p:b <= (a) _',
  ['a',('p','@')],
  [('p','@')]
),
R('RULE p:b <= (a) (b) _',
  ['a','b',('p','@')],
  ['a',('p','@')],
  ['b',('p','@')],
  [('p','@')]
),
R('RULE p:b <= (a (b)) _',
  ['a','b',('p','@')],
  ['a',('p','@')],
  [('p','@')]
),
R('RULE p:b <= a _ | b _',
  ['a',('p','@')],
  ['b',('p','@')]
),
R('''
SUBSET V a e i o u
RULE p:b <= V _ +:0
''',
  ['V',('p','@'),('+','0')]
),
]


def rules_parser_driver(data):
    klexer = KgenLexer()
    mockAST = MockAST()
    output = StringIO()
    kparser = KgenParser(klexer, output, mockAST)
    kparser.parse(data)
    return mockAST.rhs


RulesParserTestCase = generate_class('RulesParserTestCase', rules_parser_driver, data_list)
