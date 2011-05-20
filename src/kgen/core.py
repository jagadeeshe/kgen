'''
Created on May 5, 2011

@author: jagadeesh
'''


tokens = (
        'KIMMO_COMMENT',
        'COMMENT',

        'ID',

        'EOL',
        'SEGMENT',
        'SUBSET',
        'SUBSET_NAME',
        'PAIRS',
        'RULE',

        'ONLY_OCCURS',
        'ALWAYS_OCCURS',
        'ALWAYS_AND_ONLY_OCCURS',
        'NEVER_OCCURS',

        'COLON',
        'COMMA',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',

        'REG_OR',
        'REG_REPEAT',
        'UNDER',
    )

class PatternElement(list):
    DEFAULT = 0
    COMMIT = 1
    REPEAT = 2
    ALTERNATIVE = 4

    def __init__(self, lex, sur, flag=0):
        list.__init__(self, [lex, sur, flag])

    def mark_COMMIT(self):
        self[2] |= PatternElement.COMMIT

    def mark_REPEAT(self):
        self[2] |= PatternElement.REPEAT

    def mark_ALTERNATIVE(self):
        self[2] |= PatternElement.ALTERNATIVE

    def isCOMMIT(self):
        if (self[2] & PatternElement.COMMIT) == 0:
            return False
        else:
            return True

    def isREPEAT(self):
        if (self[2] & PatternElement.REPEAT) == 0:
            return False
        else:
            return True

    def isALTERNATIVE(self):
        if (self[2] & PatternElement.ALTERNATIVE) == 0:
            return False
        else:
            return True