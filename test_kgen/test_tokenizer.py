'''
Created on May 11, 2011

@author: jagadeesh
'''
import unittest
from kgen.tokenizer import KgenLexer

class tokenizerTest(unittest.TestCase):


    def test_tokenizer(self):
        data = (
            ('\n',          [('EOL', '\n')]),
            ('SUBSET',      [('SUBSET', 'SUBSET')]),
            ('C',           [('SUBSET_NAME', 'C')]),
            ('Kuril',       [('SUBSET_NAME', 'Kuril')]),
            ('a',           [('SEGMENT', 'a')]),
            ('PAIRS',       [('PAIRS', 'PAIRS')]),
            ('RULE',        [('RULE', 'RULE')]),
            ('=>',          [('ONLY_OCCURS', '=>')]),
            ('<=',          [('ALWAYS_OCCURS', '<=')]),
            ('<=>',         [('ALWAYS_AND_ONLY_OCCURS', '<=>')]),
            ('/<=',         [('NEVER_OCCURS', '/<=')]),
            (':',           [('COLON', ':')]),
            (',',           [('COMMA', ',')]),
            ('(',           [('LPAREN', '(')]),
            (')',           [('RPAREN', ')')]),
            ('[',           [('LBRACKET', '[')]),
            (']',           [('RBRACKET', ']')]),
            ('{',           [('LBRACE', '{')]),
            ('}',           [('RBRACE', '}')]),
            ('|',           [('REG_OR', '|')]),
            ('*',           [('REG_REPEAT', '*')]),
            ('_',           [('UNDER', '_')]),
            ('+',           [('SEGMENT', '+')]),
            ('@',           [('SEGMENT', '@')]),
            ("'",           [('SEGMENT', "'")]),
            (u"\u0b85",     [('SEGMENT', u"\u0b85")]),
            (' ',           []),
            ('     ',       []),
            ('\t',          []),
            (';comment\n',  [('EOL', '\n')]),
            ('!;kimmo\n',   [('KIMMO_COMMENT', ';kimmo'), ('EOL', '\n')]),
        )
        
        for input, expectation in data:
            self._driver(input, expectation)
    
    
    def _driver(self, input, expectation):
        if type(expectation) == tuple:
            expectation = [expectation]
        elif type(expectation) != list:
            self.fail("cannot handle expectation %s" % expectation)
        
        klexer = KgenLexer()
        actual = [(actual.type, actual.value) for actual in klexer.generate_tokens(input)]
        self.assertEqual(expectation, actual)


