'''
Created on May 5, 2011

@author: jagadeesh
'''

import core
from ply import lex
import re

class KgenLexer:
    
    tokens = core.tokens
    
    reserved = {
        'SUBSET' : 'SUBSET',
        'PAIRS' : 'PAIRS',
        'RULE' : 'RULE',
        ':' : 'COLON',
        ',' : 'COMMA',
        '(' : 'LPAREN',
        ')' : 'RPAREN',
        '[' : 'LBRACKET',
        ']' : 'RBRACKET',
        '{' : 'LBRACE',
        '}' : 'RBRACE',
        '|' : 'REG_OR',
        '_' : 'UNDER', 
        '*' : 'REG_REPEAT',
        }
    
    t_SEGMENT = r"\w|\W"
    t_ignore = " \t"
    
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, reflags=re.UNICODE, **kwargs)
    
    def t_ignore_COMMENT(self, t):
        r';.*(?=\n)'
        pass
    
    def t_KIMMO_COMMENT(self, t):
        r'!.*(?=\n)'
        t.value = t.value[1:]
        return t
    
    def t_EOL(self, t):
        r'\n'
        t.lexer.lineno += 1
        return t
    
    def t_ALWAYS_AND_ONLY_OCCURS(self, t):
        r'<=>'
        return t
    
    def t_NEVER_OCCURS(self, t):
        r'/<='
        return t
    
    def t_ONLY_OCCURS(self, t):
        r'=>'
        return t
    
    def t_ALWAYS_OCCURS(self, t):
        r'<='
        return t
    
    def t_ID(self, t):
        r'([A-Z][A-Za-z]*)|(:|;|,|\(|\)|\[|\]|\{|\}|\||_|\*)'
        t.type = KgenLexer.reserved.get(t.value, 'SUBSET_NAME')
        return t
    
    def t_error(self, t):
        print "Illegal character: %s" % t.value[0]
        t.lexer.skip(1)
    
    
    def generate_tokens(self, input):
        self.lexer.input(input)
        while True:
            tok = self.lexer.token()
            if not tok: break
            yield tok


if __name__ == "__main__":
    data = """
!; ' = apostrophe
!; - = hyphen
!; ` = stress
!; + = morpheme break
!
;ALPHABET
;  a b c d e f g h i j k l m n o p q r s t u v w x y z ' - ` +
;NULL 0
;ANY  @
;BOUNDARY #

SUBSET C    b c d f g h j k l m n p q r s t v w x y z     ; consonants
SUBSET Csib s x z       ; sibilants
SUBSET Cpal c g         ; soft palatals

; Vowels and other defaults
; ` and + default to 0
; - defaults to either - or 0
PAIRS  a e i o u ' - - ` +
       a e i o u ' - 0 0 0

RULE
    p:b => _ +:0 m

RULE
    p:b <= _ +:0 m

RULE
    p:b <=> _ +:0 m

RULE
    p:b /<= _ +:0 m

RULE
    e:i <= _ C:C* @:i
"""

    klex = KgenLexer(debug=True)
    for tok in klex.generate_tokens(data):
        print tok
