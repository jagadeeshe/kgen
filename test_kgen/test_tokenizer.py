'''
Created on May 11, 2011

@author: jagadeesh
'''
from kgen.tokenizer import KgenLexer
from tests.driver import DataDrivenTest, DataRecord

class R(DataRecord):
    def __init__(self, _input, *args):
        DataRecord.__init__(self, _input, _input, list(args))


@DataDrivenTest([
    R('\n',          ('EOL', '\n')),
    R('SUBSET',      ('SUBSET', 'SUBSET')),
    R('C',           ('SUBSET_NAME', 'C')),
    R('Kuril',       ('SUBSET_NAME', 'Kuril')),
    R('a',           ('SEGMENT', 'a')),
    R('PAIRS',       ('PAIRS', 'PAIRS')),
    R('RULE',        ('RULE', 'RULE')),
    R('=>',          ('ONLY_OCCURS', '=>')),
    R('<=',          ('ALWAYS_OCCURS', '<=')),
    R('<=>',         ('ALWAYS_AND_ONLY_OCCURS', '<=>')),
    R('/<=',         ('NEVER_OCCURS', '/<=')),
    R(':',           ('COLON', ':')),
    R(',',           ('COMMA', ',')),
    R('(',           ('LPAREN', '(')),
    R(')',           ('RPAREN', ')')),
    R('[',           ('LBRACKET', '[')),
    R(']',           ('RBRACKET', ']')),
    R('{',           ('LBRACE', '{')),
    R('}',           ('RBRACE', '}')),
    R('|',           ('REG_OR', '|')),
    R('*',           ('REG_REPEAT', '*')),
    R('_',           ('UNDER', '_')),
    R('+',           ('SEGMENT', '+')),
    R('@',           ('SEGMENT', '@')),
    R("'",           ('SEGMENT', "'")),
    R(u"\u0b85",     ('SEGMENT', u"\u0b85")),
    R(' ',           ),
    R('     ',       ),
    R('\t',          ),
    R(';comment\n',  ('EOL', '\n')),
    R('!;kimmo\n',   ('KIMMO_COMMENT', ';kimmo'), ('EOL', '\n')),
])
def test_tokenizer(data):
    klexer = KgenLexer()
    actual = [(actual.type, actual.value) for actual in klexer.generate_tokens(data)]
    return actual
