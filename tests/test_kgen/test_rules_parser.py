'''
Created on Mar 21, 2012

@author: jagadeeshe
'''
from kgen.tokenizer import KgenLexer
from kgen.parser import KgenParser
from mock_ast import MockAST
from kgen.datastructure import PE
from StringIO import StringIO
C = PE.COMMIT
S = PE.REPEAT

if PE.COMMIT <> 1:
    raise Exception("PE.COMMIT is expected to be 1. if changed, then this test needs to be changed")

if PE.REPEAT <> 2:
    raise Exception("PE.REPEAT is expected to be 2. if changed, then this test needs to be changed")

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
                    lst = el.split(':')
                    lst = map(lambda x: int(x) if x.isdigit() else x, lst)
                    el = tuple(lst)
                if type(el) <> tuple:
                    raise Exception("unsupported type")
                new_rhs_row.append(PE(*el))
            new_rhs_list.append(new_rhs_row)
        DataRecord.__init__(self, _input, _input + "\n", new_rhs_list)

data_list = [
#
# only_occurs rules with left, right and both context
#
R('RULE p:b => a _',
  ['a','p:b:1']
),
R('RULE p:b => a _ b',
  ['a','p:b:1','b']
),
R('RULE p:b => _ a',
  ['p:b:1','a']
),
#
# always_occurs rules with left, right and both context
#
R('RULE p:b <= a _',
  ['a','p:@']
),
R('RULE p:b <=  _ a',
  ['p:@','a']
),
R('RULE p:b <= a _ b',
  ['a','p:@','b']
),
#
# never_occurs rules with left, right and both context
#
R('RULE p:b /<= a _',
  ['a','p:b']
),
R('RULE p:b /<= _ a',
  ['p:b','a']
),
R('RULE p:b /<= a _ b',
  ['a','p:b','b']
),
#
# alwasy_and_only_occurs rules with left, right and both context
#
R('RULE p:b <=> a _ ',
  ['a','p:@'],
  ['a','p:b:1']
),
R('RULE p:b <=> _ a',
  ['p:@','a'],
  ['p:b:1','a']
),
R('RULE p:b <=> a _ b',
  ['a','p:@','b'],
  ['a','p:b:1','b']
),
#
# special correspondence with alternate
#
R('RULE p : {b, c} => a _',
  ['a','p:b:1'],
  ['a','p:c:1']
),
R('RULE {p, d} : b => a _',
  ['a','p:b:1'],
  ['a','d:b:1']
),
R('RULE {p, d} : {b, c} => a _',
  ['a','p:b:1'],
  ['a','d:c:1']
),
#
# all possible segment_pair
#
R('RULE p:b <= a:c _',
  ['a:c','p:@']
),
R('RULE p:b <= a: _',
  ['a:@','p:@']
),
R('RULE p:b <= :a _',
  ['@:a','p:@']
),
R('RULE p:b <= a _',
  ['a','p:@']
),
R('RULE p:b <= {a , b} : c _',
  ['a:c','p:@'],
  ['b:c','p:@']
),
R('RULE p:b <= c : {a , b} _',
  ['c:a','p:@'],
  ['c:b','p:@']
),
R('RULE p:b <= {a, b} : {c, d} _',
  ['a:c','p:@'],
  ['b:d','p:@']
),
R('RULE p:b <= {a, b} :  _',
  ['a:@','p:@'],
  ['b:@','p:@']
),
R('RULE p:b <= {a , b} _',
  ['a','p:@'],
  ['b','p:@']
),
#
# all possible segment_pair *
#
R('RULE p:b <= a:c * _',
  ['a:c:2','p:@']
),
R('RULE p:b <= a: * _',
  ['a:@:2','p:@']
),
R('RULE p:b <= :a * _',
  ['@:a:2','p:@']
),
R('RULE p:b <= a * _',
  ['a:a:2','p:@']
),
R('RULE p:b <= {a , b} : c * _',
  ['a:c:2','p:@'],
  ['b:c:2','p:@']
),
R('RULE p:b <= c : {a , b} * _',
  ['c:a:2','p:@'],
  ['c:b:2','p:@']
),
R('RULE p:b <= {a, b} : {c, d} * _',
  ['a:c:2','p:@'],
  ['b:d:2','p:@']
),
R('RULE p:b <= {a, b} : * _',
  ['a:@:2','p:@'],
  ['b:@:2','p:@']
),
R('RULE p:b <= {a , b} * _',
  ['a:a:2','p:@'],
  ['b:b:2','p:@']
),
#
# alternative_list test
#
R('RULE p:b <= [a:c | f] _',
  ['a:c','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [a: | f] _',
  ['a:@','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [:a | f] _',
  ['@:a','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [a | f] _',
  ['a','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [{a , b} : c | f] _',
  ['a:c','p:@'],
  ['b:c','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [c : {a , b} | f] _',
  ['c:a','p:@'],
  ['c:b','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [{a, b} : {c, d} | f] _',
  ['a:c','p:@'],
  ['b:d','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [{a, b} : | f] _',
  ['a:@','p:@'],
  ['b:@','p:@'],
  ['f', 'p:@']
),
R('RULE p:b <= [{a , b} | f] _',
  ['a','p:@'],
  ['b','p:@'],
  ['f', 'p:@']
),
#
# optional_list test
#
R('RULE p:b <= (a:c) _',
  ['a:c','p:@'],
  ['p:@']
),
R('RULE p:b <= (a:) _',
  ['a:@','p:@'],
  ['p:@']
),
R('RULE p:b <= (:a) _',
  ['@:a','p:@'],
  ['p:@']
),
R('RULE p:b <= (a) _',
  ['a','p:@'],
  ['p:@']
),
R('RULE p:b <= ({a , b} : c) _',
  ['a:c','p:@'],
  ['b:c','p:@'],
  ['p:@']
),
R('RULE p:b <= (c : {a , b}) _',
  ['c:a','p:@'],
  ['c:b','p:@'],
  ['p:@']
),
R('RULE p:b <= ({a, b} : {c, d}) _',
  ['a:c','p:@'],
  ['b:d','p:@'],
  ['p:@']
),
R('RULE p:b <= ({a, b} : ) _',
  ['a:@','p:@'],
  ['b:@','p:@'],
  ['p:@']
),
R('RULE p:b <= ({a , b}) _',
  ['a','p:@'],
  ['b','p:@'],
  ['p:@']
),
#
# pattern_list test
#
R('RULE p:b <= [a | b] c _',
  ['a','c','p:@'],
  ['b','c','p:@']
),
R('RULE p:b <= e [a | b] c _',
  ['e','a','c','p:@'],
  ['e','b','c','p:@']
),
R('RULE p:b <= (a) (b) _',
  ['a','b','p:@'],
  ['a','p:@'],
  ['b','p:@'],
  ['p:@']
),
R('RULE p:b <= (a (b)) _',
  ['a','b','p:@'],
  ['a','p:@'],
  ['p:@']
),
R('RULE p:b <= a _ | b _',
  ['a','p:@'],
  ['b','p:@']
),
R('RULE p:b => abc _',
  ['a','b','c','p:b:1']
),
R('RULE p:b => abc _ abcd',
  ['a','b','c','p:b:1','a','b','c','d']
),
R('RULE p:b => _ abc',
  ['p:b:1','a','b','c']
),
R('RULE p:b <= a:c * b _',
  ['a:c:2','b','p:@']
),
R('RULE p:b <= a:c * d:e * _',
  ['a:c:2','d:e:2','p:@']
),
R('RULE p:b <= a:c b:c _',
  ['a:c','b:c','p:@']
),
R('RULE p:b <= a b {c, d} e _',
  ['a','b','c','e','p:@'],
  ['a','b','d','e','p:@']
),
R('''
SUBSET V a e i o u
RULE p:b <= V _ +:0
''',
  ['V','p:@',('+','0')]
),
R('RULE c:t <= x (z [ f | :g | h: ]) _',
  ['x','z','f','c:@'],
  ['x','z','@:g','c:@'],
  ['x','z','h:@','c:@'],
  ['x','c:@'],
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
